# server/services/rag_service.py
import os
import re
import networkx as nx
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from core.config import settings
from core.log_config import logger

# --- Configuration & Helpers ---
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "chroma_db")
KNOWLEDGE_BASE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "knowledge_base", "rag_concepts.txt")
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
def format_docs(docs): return "\n\n".join(doc.page_content for doc in docs)

# --- Standard Vector RAG Service ---
class RAGService:
    def __init__(self):
        logger.info("Initializing RAGService with Guardrails...")
        if not os.path.exists(DB_DIR): raise FileNotFoundError(f"ChromaDB not found. Please run ingestion script.")
        
        # --- THE FIX FOR DOCKER ---
        ollama_base_url = settings.OLLAMA_HOST or "http://localhost:11434"
        logger.info(f"RAGService connecting to Ollama at: {ollama_base_url}")

        self.vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embedding_function)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        self.llm = ChatOllama(model="llama3", temperature=0.2, base_url=ollama_base_url)
        self.grading_llm = ChatOllama(model="llama3", format="json", temperature=0, base_url=ollama_base_url)
        
        generation_prompt = ChatPromptTemplate.from_template(
            "You are an AI research assistant. Your task is to answer the user's `question` based on the provided `context`.\n"
            "Synthesize the information from the context into a coherent and helpful answer.\n"
            "CONTEXT:\n{context}\n\nQUESTION:\n{question}\n\nANSWER:"
        )
        self.rag_chain = ({"context": self.retriever | RunnableLambda(format_docs), "question": RunnablePassthrough()} | generation_prompt | self.llm | StrOutputParser())

        grading_prompt_template = """
        You are a grader assessing whether an AI-generated `answer` is grounded in a provided `context`.
        An answer is hallucinated if it asserts information that is NOT supported by or CONTRADICTS the context.
        Synthesis and summarization of the context is acceptable.
        Provide a JSON object with two keys: "score" ("yes" or "no") and "reasoning" (a brief explanation). JSON Response:"""
        grading_prompt = PromptTemplate.from_template(grading_prompt_template)
        self.grading_chain = (grading_prompt | self.grading_llm | JsonOutputParser())
        
        logger.info("RAGService with Guardrails initialized successfully.")

    async def query(self, question: str) -> str:
        logger.info(f"RAGService querying with: '{question}'")
        retrieved_docs = await self.retriever.ainvoke(question)
        formatted_context = format_docs(retrieved_docs)
        logger.info("Step 1: Generating initial answer...")
        initial_generation = await self.rag_chain.ainvoke(question)
        logger.info("Step 2: Grading answer for hallucination...")
        grade = await self.grading_chain.ainvoke({"context": formatted_context, "question": question, "generation": initial_generation})
        score = grade.get("score", "no").lower()
        reasoning = grade.get("reasoning", "No reasoning provided.")
        logger.info(f"Hallucination check result: Score='{score}', Reasoning='{reasoning}'")
        if score == "yes":
            return initial_generation
        else:
            return f"I found some information, but the generated answer was flagged as potentially unreliable. Grader's reasoning: '{reasoning}'."

def get_rag_service() -> RAGService:
    return RAGService()

# --- GraphRAG PoC Service ---
class GraphRAGService:
    def __init__(self):
        logger.info("Initializing GraphRAGService with clean knowledge base...")
        self.graph = nx.Graph()

        # --- THE FIX FOR DOCKER ---
        ollama_base_url = settings.OLLAMA_HOST or "http://localhost:11434"
        logger.info(f"GraphRAGService connecting to Ollama at: {ollama_base_url}")
        self.llm_extractor = ChatOllama(model="llama3", temperature=0, base_url=ollama_base_url)
        
        try:
            with open(KNOWLEDGE_BASE_FILE, "r", encoding="utf-8") as f:
                text_for_graph = f.read()
            self._build_graph(text_for_graph)
        except Exception as e:
            logger.error(f"Failed to initialize GraphRAG: {e}", exc_info=True)

    def _build_graph(self, text_chunk: str):
        extraction_prompt = PromptTemplate.from_template(
            "You are a knowledge graph creator. From the TEXT below, extract relationships.\n"
            "List each relationship as `(Entity 1, Relationship, Entity 2)` on a new line.\n"
            "Example:\n(Lewis et al., proposed, RAG framework)\n(RAG framework, uses, retriever)\n\n"
            "TEXT:\n{text_chunk}"
        )
        extraction_chain = extraction_prompt | self.llm_extractor | StrOutputParser()
        try:
            response_text = extraction_chain.invoke({"text_chunk": text_chunk})
            triplets = re.findall(r'\((.*?),\s*(.*?),\s*(.*?)\)', response_text)
            logger.info(f"Extracted {len(triplets)} triplets using regex parsing.")

            for source, rel, target in triplets:
                source_clean = source.strip(' "`')
                rel_clean = rel.strip(' "`')
                target_clean = target.strip(' "`')
                self.graph.add_node(source_clean.title())
                self.graph.add_node(target_clean.title())
                self.graph.add_edge(source_clean.title(), target_clean.title(), label=rel_clean)
            
            logger.info(f"Graph built with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges.")
        except Exception as e:
            logger.error(f"Failed to build graph from extracted text: {e}", exc_info=True)

    async def query(self, question: str) -> str:
        logger.info(f"GraphRAG querying with: '{question}'")
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

def get_graph_rag_service() -> GraphRAGService:
    if "graph_rag_service_instance" not in globals():
        globals()["graph_rag_service_instance"] = GraphRAGService()
    return globals()["graph_rag_service_instance"]