import os
import re
import asyncio
from typing import Optional
import networkx as nx
from fastapi import HTTPException
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from core.config import settings
from core.log_config import logger

# --- Configuration & Helpers ---
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "chroma_db")
KNOWLEDGE_BASE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "knowledge_base", "rag_concepts.txt")
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# --- Standard Vector RAG Service ---
class RAGService:
    def __init__(self):
        logger.info("Initializing RAGService with Guardrails...")
        ollama_base_url = settings.OLLAMA_HOST
        logger.info(f"RAGService connecting to Ollama at: {ollama_base_url}")

        self.vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embedding_function)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        self.llm = ChatOllama(model="llama3", temperature=0.2, base_url=ollama_base_url)
        self.grading_llm = ChatOllama(model="llama3", format="json", temperature=0, base_url=ollama_base_url)

        self.generation_prompt = ChatPromptTemplate.from_template(
            "You are an AI research assistant. Your task is to answer the user's `question` based on the provided `context`.\n"
            "Synthesize the information from the context into a coherent and helpful answer.\n\n"
            "CONTEXT:\n{context}\n\nQUESTION:\n{question}\n\nANSWER:"
        )
        self.generation_chain = self.generation_prompt | self.llm | StrOutputParser()

        self.grading_prompt_template = (
            "You are a grader assessing whether an AI-generated `answer` is grounded in a provided `context`.\n"
            "An answer is hallucinated if it asserts information that is NOT supported by or CONTRADICTS the context.\n"
            "Synthesis and summarization of the context is acceptable.\n\n"
            "CONTEXT:\n'''{context}'''\n\n"
            "USER QUESTION:\n'''{question}'''\n\n"
            "AI-GENERATED ANSWER:\n'''{generation}'''\n\n"
            "Provide a JSON object with two keys: 'score' ('yes' or 'no') and 'reasoning' (a brief explanation).\n"
            "JSON Response:"
        )
        grading_prompt = PromptTemplate.from_template(self.grading_prompt_template)
        self.grading_chain = grading_prompt | self.grading_llm | JsonOutputParser()

        logger.info("RAGService with Guardrails initialized successfully.")

    def doc_count(self) -> int:
        try:
            return self.vectorstore._collection.count()
        except Exception:
            return 0

    async def query(self, question: str) -> str:
        logger.info(f"RAGService querying with: '{question}'")
        
        # Verify knowledge base availability without exposing internal file paths
        if not os.path.exists(DB_DIR) or self.doc_count() == 0:
            raise HTTPException(
                status_code=503,
                detail="The RAG knowledge base is empty. Please run the data ingestion script first."
            )

        # Step 1: Single retrieval and context generation
        retrieved_docs = await self.retriever.ainvoke(question)
        formatted_context = format_docs(retrieved_docs)
        
        logger.info("Step 1: Generating initial answer using retrieved context...")
        initial_generation = await self.generation_chain.ainvoke({
            "context": formatted_context,
            "question": question
        })

        # Step 2: Evaluation with guardrail
        logger.info("Step 2: Grading answer for hallucination...")
        grade = {}
        try:
            raw_grade = await self.grading_chain.ainvoke({
                "context": formatted_context,
                "question": question,
                "generation": initial_generation
            })
            if isinstance(raw_grade, dict):
                grade = raw_grade
            else:
                logger.warning(f"Grading output is not a dictionary: {raw_grade}")
                grade = {"score": "no", "reasoning": "Evaluator output was not structured as expected."}
        except Exception as e:
            logger.warning(f"Grading chain evaluation failed: {e}. Marking as unverified.")
            grade = {"score": "no", "reasoning": "Evaluator could not verify the answer."}

        raw_score = grade.get("score")
        score = raw_score.lower().strip() if isinstance(raw_score, str) else "no"
        reasoning = grade.get("reasoning", "No reasoning provided.")
        logger.info(f"Hallucination check result: Score='{score}', Reasoning='{reasoning}'")

        if score == "yes":
            return initial_generation
        else:
            return f"I found some information, but the generated answer was flagged as potentially unreliable. Grader's reasoning: '{reasoning}'."

_rag_service_instance: Optional[RAGService] = None

def get_rag_service() -> RAGService:
    global _rag_service_instance
    if _rag_service_instance is None:
        _rag_service_instance = RAGService()
    return _rag_service_instance


# --- GraphRAG PoC Service ---
class GraphRAGService:
    def __init__(self):
        logger.info("Initializing GraphRAGService...")
        self.graph = nx.Graph()
        self._initialized = False
        self._init_lock = asyncio.Lock()
        ollama_base_url = settings.OLLAMA_HOST
        self.llm_extractor = ChatOllama(model="llama3", temperature=0, base_url=ollama_base_url)

    async def ensure_initialized(self):
        if self._initialized and self.graph.number_of_nodes() > 0:
            return

        async with self._init_lock:
            if self._initialized and self.graph.number_of_nodes() > 0:
                return

            if not os.path.exists(KNOWLEDGE_BASE_FILE):
                logger.error(f"GraphRAG knowledge base file missing at: {KNOWLEDGE_BASE_FILE}")
                raise HTTPException(
                    status_code=503,
                    detail="GraphRAG knowledge base is not available. Missing knowledge base source."
                )

            try:
                with open(KNOWLEDGE_BASE_FILE, "r", encoding="utf-8") as f:
                    text_for_graph = f.read()

                if not text_for_graph.strip():
                    raise HTTPException(
                        status_code=503,
                        detail="GraphRAG knowledge base source is empty."
                    )

                await self._build_graph_async(text_for_graph)

                if self.graph.number_of_nodes() == 0:
                    raise HTTPException(
                        status_code=503,
                        detail="No relationships could be extracted for GraphRAG knowledge base."
                    )

                self._initialized = True
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Failed to initialize GraphRAG: {e}", exc_info=True)
                raise HTTPException(status_code=503, detail="GraphRAG service failed to initialize.")

    async def _build_graph_async(self, text_chunk: str):
        extraction_prompt = PromptTemplate.from_template(
            "You are a knowledge graph creator. From the TEXT below, extract relationships.\n"
            "List each relationship as `(Entity 1, Relationship, Entity 2)` on a new line.\n"
            "Example:\n(Lewis et al., proposed, RAG framework)\n(RAG framework, uses, retriever)\n\n"
            "TEXT:\n{text_chunk}"
        )
        extraction_chain = extraction_prompt | self.llm_extractor | StrOutputParser()
        triplets = []

        try:
            response_text = await extraction_chain.ainvoke({"text_chunk": text_chunk})
            triplets = re.findall(r'\((.*?),\s*(.*?),\s*(.*?)\)', response_text)
            logger.info(f"Extracted {len(triplets)} triplets using LLM.")
        except Exception as e:
            logger.warning(f"LLM extraction for GraphRAG failed: {e}. Falling back to source triplets.")

        # If LLM didn't produce triplets (e.g. LLM unavailable during build), extract from text directly
        if not triplets:
            triplets = re.findall(r'\((.*?),\s*(.*?),\s*(.*?)\)', text_chunk)
            logger.info(f"Extracted {len(triplets)} baseline triplets from knowledge base file.")

        for source, rel, target in triplets:
            source_clean = source.strip(' "`')
            rel_clean = rel.strip(' "`')
            target_clean = target.strip(' "`')
            if source_clean and target_clean:
                self.graph.add_node(source_clean.title())
                self.graph.add_node(target_clean.title())
                self.graph.add_edge(source_clean.title(), target_clean.title(), label=rel_clean)

        logger.info(f"Graph built with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges.")

    async def query(self, question: str) -> str:
        logger.info(f"GraphRAG querying with: '{question}'")
        await self.ensure_initialized()

        results = set()
        question_terms = {term.strip().lower() for term in question.lower().replace('?', '').split()}
        for node in self.graph.nodes:
            if any(term in node.lower() for term in question_terms if len(term) > 2):
                for neighbor in self.graph.neighbors(node):
                    edge_data = self.graph.get_edge_data(node, neighbor)
                    results.add(f"- '{node}' {edge_data.get('label', 'is related to')} '{neighbor}'.")

        if not results:
            return "No direct relationships found in the knowledge graph for your query."

        return "Based on the knowledge graph, I found these relationships:\n" + "\n".join(sorted(list(results)))

_graph_rag_service_instance: Optional[GraphRAGService] = None

def get_graph_rag_service() -> GraphRAGService:
    global _graph_rag_service_instance
    if _graph_rag_service_instance is None:
        _graph_rag_service_instance = GraphRAGService()
    return _graph_rag_service_instance
