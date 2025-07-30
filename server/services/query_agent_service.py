from langchain_community.chat_models import ChatOllama
from schemas.content import QueryAgentRequest
from services import generator_service
from services import rag_service
from core.config import settings
from core.log_config import logger
from traceback import format_exc

class QueryAgentService:
    def __init__(self):
        logger.info("Initializing SIMPLEST Query Agent...")
        ollama_base_url = settings.OLLAMA_HOST or "http://localhost:11434"
        self.llm = ChatOllama(model="llama3", temperature=0, base_url=ollama_base_url)
        logger.info("SIMPLEST Query Agent initialized.")

    async def invoke(self, request: QueryAgentRequest) -> str:
        question = request.question
        logger.info(f"Manual Agent received question: '{question}'")

        # Classify the user's intent using a simple prompt
        classification_prompt = f"""Classify the user's intent. Choose ONE category: 'content_creation', 'rag_query', or 'fallback'.
        - Use 'content_creation' for requests to write or generate content.
        - Use 'rag_query' for questions asking for facts or definitions.
        - Use 'fallback' for greetings or anything else.
        Your answer MUST be a single word.
        User Request: "{question}"
        Category:"""
        
        # Attempt to classify the intent using the LLM
        try:
            logger.info("Agent Step 1: Classifying intent...")
            classification_response = await self.llm.ainvoke(classification_prompt)
            destination = classification_response.content.strip().lower().replace("'", "").replace('"', '').split()[0]
            logger.info(f"LLM classified intent as: '{destination}'")
        except Exception as e:
            logger.error(f"LLM classifier failed: {e}\n{format_exc()}")
            destination = "fallback"

        logger.info(f"Routing to destination: {destination}")

        if "rag_query" in destination:
            logger.info("Executing RAG Agent...")
            rag_svc = rag_service.get_rag_service()
            return await rag_svc.query(request.question)

        elif "content_creation" in destination:
            logger.info("Executing Content Agent...")
            from schemas.content import ContentGenerationRequest
            content_request = ContentGenerationRequest(
                topic=request.question,
                language=request.language,
                company_info=request.company_info,
                use_news_search=request.use_search
            )
            result = await generator_service.generate_content_service(content_request)
            return str(result.get("generated_content", "Failed to generate content."))
            
        else:
            logger.info("Routing to fallback.")
            return "Thank you for your query. I can either generate content (e.g., 'write a blog about AI') or answer questions (e.g., 'what is RAG?'). Please specify your request."

def get_query_agent_service() -> QueryAgentService:
    if "query_agent_service_instance" not in globals():
        globals()["query_agent_service_instance"] = QueryAgentService()
    return globals()["query_agent_service_instance"]