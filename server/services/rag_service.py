import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from core.log_config import logger

# Configuration
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "chroma_db")
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

class RAGService:
    def __init__(self):
        logger.info("Initializing RAGService...")
        if not os.path.exists(DB_DIR):
            logger.error(f"ChromaDB directory not found at {DB_DIR}")
            raise FileNotFoundError(f"ChromaDB directory not found. Please run the ingestion script.")
        
        self.vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embedding_function)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        self.llm = ChatOllama(model="llama3")

        self.prompt = ChatPromptTemplate.from_template(
            "You are an AI research assistant. Answer the question based ONLY on the following context:\n\n"
            "{context}\n\n"
            "Question: {question}"
        )
        
        self.rag_chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt | self.llm | StrOutputParser()
        )
        logger.info("RAGService initialized successfully.")

    async def query(self, question: str) -> str:
        logger.info(f"RAGService querying with: '{question}'")
        response = await self.rag_chain.ainvoke(question)
        return response

# Dependency "getter" function.
# FastAPI will call this function to create an instance of the service.
def get_rag_service() -> RAGService:
    return RAGService()