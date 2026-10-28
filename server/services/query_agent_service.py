from langchain_community.chat_models import ChatOllama
from schemas.content import QueryAgentRequest, ContentGenerationRequest
from services import generator_service
from services import rag_service
from core.config import settings
from core.log_config import logger
from traceback import format_exc

class QueryAgentService:
    def __init__(self):
        logger.info("Initializing SIMPLEST Query Agent...")
        ollama_base_url = settings.OLLAMA_HOST
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
            
            # Infer targeted platform(s) from question keywords, defaulting to blog
            q_lower = request.question.lower()
            target_platforms = []
            if any(k in q_lower for k in ["tweet", "twitter", "x post", "on x"]):
                target_platforms.append("X")
            if any(k in q_lower for k in ["instagram", "insta", "ig post", "caption"]):
                target_platforms.append("instagram")
            if any(k in q_lower for k in ["blog", "article", "post", "essay"]) or not target_platforms:
                if "blog" not in target_platforms:
                    target_platforms.append("blog")

            content_request = ContentGenerationRequest(
                topic=request.question,
                platforms=target_platforms,
                language=request.language,
                company_info=request.company_info,
                use_news_search=request.use_search
            )
            result = await generator_service.generate_content_service(content_request)
            generated = result.get("generated_content", {})

            if isinstance(generated, dict):
                sections = []
                for platform_name, text in generated.items():
                    platform_title = platform_name.upper() if platform_name.lower() == "x" else platform_name.capitalize()
                    sections.append(f"### {platform_title}\n\n{text}")
                response_text = "\n\n---\n\n".join(sections) if sections else "No content was generated."
            elif isinstance(generated, str):
                response_text = generated
            else:
                response_text = "Failed to generate content."

            image_url = result.get("image_url")
            if image_url:
                image_alt = result.get("image_alt") or "Generated visual"
                response_text += f"\n\n![{image_alt}]({image_url})"

            return response_text
            
        else:
            logger.info("Routing to fallback.")
            return "Thank you for your query. I can either generate content (e.g., 'write a blog about AI') or answer questions (e.g., 'what is RAG?'). Please specify your request."

def get_query_agent_service() -> QueryAgentService:
    if "query_agent_service_instance" not in globals():
        globals()["query_agent_service_instance"] = QueryAgentService()
    return globals()["query_agent_service_instance"]