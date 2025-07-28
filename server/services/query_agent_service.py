# server/services/query_agent_service.py
import json
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.chat_models import ChatOllama
from pydantic.v1 import BaseModel as BaseModelV1, Field
from typing import Literal
from schemas.content import QueryAgentRequest

from services import generator_service
from services import rag_service
from core.log_config import logger

class RouteQuery(BaseModelV1):
    destination: Literal["rag_agent", "content_agent", "fallback"]

class QueryAgentService:
    def __init__(self):
        logger.info("Initializing Hybrid Router Query Agent...")
        # This LLM is now a simple classifier, not a complex extractor.
        llm = ChatOllama(model="llama3", format="json", temperature=0)
        
        # A much simpler prompt for a simpler task
        classifier_prompt_template = """You are an expert request classifier.
Your task is to classify the user's intent based on their query.
Choose one of the following destinations:
- `rag_agent`: If the user asks a factual question, a "what is" question, or mentions "RAG".
- `content_agent`: If the user explicitly asks to 'write', 'create', or 'generate' some content like a post or blog.
- `fallback`: For all other cases, like greetings or unclear requests.
You must respond with a JSON object with a single key "destination".

<< EXAMPLES >>
Query: "What is Retrieval-Augmented Generation?" -> {{"destination": "rag_agent"}}
Query: "Write a blog post about AI" -> {{"destination": "content_agent"}}
Query: "Hi there!" -> {{"destination": "fallback"}}

<< USER QUERY >>
{question}

<< YOUR JSON RESPONSE >>
"""
        parser = JsonOutputParser(pydantic_object=RouteQuery)
        prompt = ChatPromptTemplate.from_template(classifier_prompt_template)
        self.classifier_chain = prompt | llm | parser
        logger.info("Hybrid Router Query Agent initialized.")

    async def invoke(self, request: QueryAgentRequest) -> str:
        question_lower = request.question.lower()
        logger.info(f"Query Agent routing pure question: '{request.question}'")

        # --- Rule-Based Routing (Code First) ---
        content_keywords = ['write', 'create', 'generate', 'post', 'blog', 'tweet', 'caption']
        
        # If the user explicitly asks to create content, we force the content_agent.
        if any(keyword in question_lower for keyword in content_keywords):
            logger.info("Keyword match found. Routing directly to: content_agent")
            destination = "content_agent"
        else:
            # --- AI-Based Routing (LLM as Fallback Classifier) ---
            logger.info("No keyword match. Using LLM to classify intent...")
            try:
                classification = await self.classifier_chain.ainvoke({"question": request.question})
                destination = classification.get("destination", "fallback")
            except Exception:
                logger.error("LLM classifier failed. Defaulting to fallback.")
                destination = "fallback"

        logger.info(f"Query Agent final destination: {destination}")
        
        # --- Execute the chosen specialist ---
        if destination == "rag_agent":
            rag_svc = rag_service.get_rag_service()
            return await rag_svc.query(request.question)

        elif destination == "content_agent":
            from schemas.content import ContentGenerationRequest
            content_request = ContentGenerationRequest(
                topic=request.question, # The whole question is the topic
                platforms=["blog"],     # Default to blog for ambiguous content requests
                language=request.language,
                company_info=request.company_info,
                use_news_search=request.use_search,
                model="llama3"
            )
            result = await generator_service.generate_content_service(content_request)
            return str(result.get("generated_content", "Failed to generate content."))
            
        else:
            return "Thank you for your query. I can generate content or answer questions about RAG. Could you be more specific? (e.g., 'Write a blog about...' or 'What is...?')"

def get_query_agent_service() -> QueryAgentService:
    if "query_agent_service_instance" not in globals():
        globals()["query_agent_service_instance"] = QueryAgentService()
    return globals()["query_agent_service_instance"]