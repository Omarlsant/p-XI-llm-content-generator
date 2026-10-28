import asyncio
import httpx
import ollama
import json
from typing import Optional, List, Dict
from traceback import format_exc
from fastapi import HTTPException

# --- CORE LANGCHAIN IMPORTS ---
from langchain_community.chat_models import ChatOllama
from langchain_community.tools.tavily_search import TavilySearchResults

from schemas.content import ContentGenerationRequest
from core.config import settings
from core.log_config import logger


async def find_relevant_image(topic: str) -> Optional[dict]:
    if not settings.UNSPLASH_ACCESS_KEY:
        return None
    url, params = "https://api.unsplash.com/search/photos", {"query": topic, "per_page": 1, "orientation": "landscape"}
    headers = {"Authorization": f"Client-ID {settings.UNSPLASH_ACCESS_KEY}"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            if data.get("results"):
                image = data["results"][0]
                return {"url": image["urls"]["regular"], "alt": image.get("alt_description", f"Image about {topic}")}
    except Exception as e:
        logger.error(f"Error fetching image: {e}", exc_info=True)
    return None


# --- Simple Non-Agentic Generation ---
def get_simple_prompt_template(platform: str) -> str:
    templates = {
        "blog": ("{company_context}You are an expert blog writer in {language}. Write a comprehensive blog post about 300-400 words on: '{topic}'. Use markdown."),
        "X": ("{company_context}You are a social media expert for X (Twitter) writing in {language}. Write a short, witty post (under 280 characters) on: '{topic}'. Include hashtags."),
        "instagram": ("{company_context}You are a creative social media manager writing in {language}. Write an engaging Instagram caption for a post about: '{topic}'. Include hashtags."),
    }
    return templates.get(platform, "")


async def generate_simple_content(platform: str, topic: str, company_info: Optional[str], language: str, model: str = 'llama3', **kwargs) -> str:
    logger.info(f"Using SIMPLE generation for platform '{platform}' with model '{model}'")
    llm = ollama.AsyncClient(host=settings.OLLAMA_HOST)
    raw_template = get_simple_prompt_template(platform)
    if not raw_template:
        raise ValueError(f"No prompt template defined for platform '{platform}'")
    company_context = f"Context: '''{company_info}'''\n\n" if company_info else ""
    full_prompt = raw_template.format(company_context=company_context, language=language, topic=topic)
    try:
        response = await llm.chat(model=model, messages=[{'role': 'user', 'content': full_prompt}])
        content = response['message']['content'].strip()
        if not content:
            raise ValueError(f"Empty response received from Ollama for platform '{platform}'")
        return content
    except Exception as e:
        logger.error(f"Simple generation failed for '{platform}': {e}", exc_info=True)
        raise RuntimeError(f"Standard generation failed for {platform}: {str(e)}") from e


# --- Platform-Specific Constraints ---
def get_platform_constraints(platform: str) -> str:
    constraints = {
        "blog": "a well-structured blog post of 300-400 words with markdown.",
        "X": "a short tweet under 280 characters with hashtags.",
        "instagram": "an engaging Instagram caption with emojis and hashtags."
    }
    return constraints.get(platform, "a standard text response.")


# --- Agentic Generation ---
async def generate_content_with_agent(platform: str, topic: str, company_info: Optional[str], language: str, use_search: bool, model: str = 'llama3', **kwargs) -> str:
    logger.info(f"Using MANUAL AGENT for '{platform}' with model '{model}'")
    
    ollama_base_url = settings.OLLAMA_HOST
    planner_llm = ChatOllama(model=model, temperature=0, base_url=ollama_base_url, format="json")
    writer_llm = ChatOllama(model=model, temperature=0.2, base_url=ollama_base_url)
    
    platform_rules = get_platform_constraints(platform)
    company_context = f"Company Context: '''{company_info}'''" if company_info else "No company context provided."

    planner_prompt = f"""You are a planning assistant. Analyze the user's request and decide if a web search is necessary.
Respond with a single JSON object with two keys:
1. "search_query": A concise search query string if information is needed, otherwise an empty string "".
2. "final_content": If you can answer without searching, provide the full content here. If you need to search, leave this as an empty string "".

User Request: Generate {platform_rules} in {language} about: "{topic}".
{company_context}"""
    
    try:
        # Step 1: Planning
        logger.info("Agent Step 1: Planning...")
        planning_response_raw = await planner_llm.ainvoke(planner_prompt)
        plan = json.loads(planning_response_raw.content)
        search_query = plan.get("search_query")

        if search_query:
            # Step 2: Tool Use (if needed)
            if use_search and settings.TAVILY_API_KEY:
                logger.info(f"Agent Step 2: Searching for '{search_query}'...")
                search_tool = TavilySearchResults(max_results=3)
                search_results = await search_tool.ainvoke(search_query)
                logger.info("Agent received search results.")
            else:
                search_results = "Web search was planned but is disabled or not configured."
        else:
            # If the planner already wrote the content, we are done.
            if plan.get("final_content"):
                logger.info("Agent answered directly during planning step.")
                return plan["final_content"]
            search_results = "No web search was performed."
        
        # Step 3: Final Generation
        logger.info("Agent Step 3: Generating final content with retrieved info...")
        writer_prompt = f"""You are a content creation expert.
Based on the User's Rules and the Search Results, generate the final piece of content.
Your output MUST be ONLY the content itself, with no extra text or explanations.

**User's Rules:**
- Platform: {platform} ({platform_rules})
- Language: {language}
- Topic: {topic}
- Context: {company_context}

**Search Results:**
{search_results}

**Final Content:**"""

        final_response = await writer_llm.ainvoke(writer_prompt)
        return final_response.content.strip()

    except Exception as e:
        logger.error(f"MANUAL AGENT FAILED for '{platform}':\n{format_exc()}")
        raise RuntimeError(f"The agent for {platform} encountered an error: {str(e)}") from e


# --- Main Service Function (Orchestrator) ---
async def generate_content_service(request: ContentGenerationRequest) -> dict:
    logger.info(f"SERVICE ENTRYPOINT. Received request with use_news_search = {request.use_news_search}")
    
    if request.model not in ["llama3"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported model '{request.model}'. Supported models: ['llama3']"
        )

    platform_names = [p for p in request.platforms if p in ["blog", "X", "instagram"]]
    if not platform_names:
        raise HTTPException(
            status_code=400,
            detail="No valid platforms specified. Supported platforms: ['blog', 'X', 'instagram']"
        )
    
    text_gen_tasks = []
    gen_function = generate_content_with_agent if request.use_news_search else generate_simple_content
    
    for p in platform_names:
        task = gen_function(
            platform=p, 
            topic=request.topic, 
            company_info=request.company_info, 
            language=request.language,
            use_search=request.use_news_search,
            model=request.model
        )
        text_gen_tasks.append(task)
            
    image_gen_task = find_relevant_image(request.topic)
    
    all_tasks = text_gen_tasks + [image_gen_task]
    results = await asyncio.gather(*all_tasks, return_exceptions=True)
    
    image_result, text_results = results[-1], results[:-1]
    
    content_dict = {}
    error_dict = {}
    for i, res in enumerate(text_results):
        name = platform_names[i]
        if isinstance(res, Exception):
            logger.error(f"Generation for '{name}' failed with exception: {res}")
            error_dict[name] = str(res)
        elif isinstance(res, str) and res.startswith("Error:"):
            logger.error(f"Generation for '{name}' failed with error string: {res}")
            error_dict[name] = res
        else:
            content_dict[name] = res
            
    image_url, image_alt = (None, None)
    if isinstance(image_result, dict) and image_result:
        image_url, image_alt = image_result.get("url"), image_result.get("alt")
    elif isinstance(image_result, Exception):
        logger.warning(f"Image search failed: {image_result}")

    has_success = len(content_dict) > 0

    return {
        "generated_content": content_dict,
        "errors": error_dict,
        "image_url": image_url,
        "image_alt": image_alt,
        "success": has_success
    }
