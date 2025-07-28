import asyncio
import httpx
import google.generativeai as genai
import ollama
from typing import Optional
from traceback import format_exc

# --- CORE LANGCHAIN IMPORTS ---
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults

from schemas.content import ContentGenerationRequest
from core.config import settings
from core.log_config import logger

# --- Service Initializations & Helpers ---
if settings.GOOGLE_API_KEY:
    try: genai.configure(api_key=settings.GOOGLE_API_KEY)
    except Exception as e: logger.error(f"Failed to configure Google Gemini API: {e}")
else: logger.warning("GOOGLE_API_KEY not found. Gemini model will not be available.")

async def find_relevant_image(topic: str) -> dict:
    if not settings.UNSPLASH_ACCESS_KEY: return None
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

# --- Simple, Non-Agentic Generation ---
def get_simple_prompt_template(platform: str) -> str:
    templates = {
        "blog": ("{company_context}You are an expert blog writer. You must write in {language}. Write a comprehensive blog post about 300-400 words on the topic. Use markdown formatting. Topic: '{topic}'"),
        "X": ("{company_context}You are a social media expert for X (Twitter). You must write in {language}. Write a short, witty post (under 280 characters) on the topic. Include relevant hashtags. Topic: '{topic}'"),
        "instagram": ("{company_context}You are a creative social media manager. You must write in {language}. Write an engaging Instagram caption. Include relevant hashtags. Topic: '{topic}'"),
    }
    return templates.get(platform, "")

async def generate_simple_content(platform: str, topic: str, company_info: Optional[str], language: str) -> str:
    logger.info(f"Using SIMPLE generation for platform '{platform}'")
    llm = ollama.AsyncClient()
    
    raw_template = get_simple_prompt_template(platform)
    if not raw_template: return ""
    
    company_context = f"Company/Brand Information: '''{company_info}'''\n\n" if company_info else ""
    full_prompt = raw_template.format(company_context=company_context, language=language, topic=topic)
    
    try:
        response = await llm.chat(model='llama3', messages=[{'role': 'user', 'content': full_prompt}])
        return response['message']['content'].strip()
    except Exception as e:
        logger.error(f"Simple generation failed for {platform}: {e}", exc_info=True)
        return f"Error: Standard generation failed for {platform}."

# --- Agentic Generation ---
async def generate_content_with_agent(platform: str, topic: str, company_info: Optional[str], language: str) -> str:
    logger.info(f"Using AGENTIC generation for platform '{platform}'")
    llm = ChatOllama(model="llama3", temperature=0)
    tools = [TavilySearchResults(max_results=3)]
    
    react_prompt_template = """
You are a helpful assistant. Answer the user's question as best as you can. You have access to the following tools:
{tools}

Use the following format:
Thought: Do I need to use a tool? Yes or No.
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
Thought: I now know the final answer.
Final Answer: [the final response to the user's original question]

**Important instructions:**
- If you can answer the question from your own knowledge without using a tool, respond immediately with your 'Final Answer:'.
- Your final answer must fulfill the user's request precisely.

Begin!

User request: Generate content for the {platform} platform about the topic: '{topic}'.
You must write the final answer entirely in {language}.
If company information is provided, use it for context: {company_context}.
Question: {input}
Thought:{agent_scratchpad}
"""
    prompt = PromptTemplate.from_template(react_prompt_template)
    agent = create_react_agent(llm, tools, prompt)
    
    # --- Cleaner logs ---
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False, handle_parsing_errors=True, max_iterations=8)
    
    company_context_str = f"Company/Brand Information: '''{company_info}'''" if company_info else "No company info provided."
    input_dict = { "platform": platform, "topic": topic, "language": language, "company_context": company_context_str, "input": f"Generate content for {platform} about: {topic}" }

    try:
        response = await agent_executor.ainvoke(input_dict)
        return response['output'].strip()
    except Exception as e:
        error_details = format_exc()
        logger.error(f"!!!!!! AGENT EXECUTION FAILED FOR PLATFORM '{platform}' !!!!!!\n{error_details}")
        return f"Error: Agent failed for {platform}."


# --- Main Service Function (Orchestrator) ---
async def generate_content_service(request: ContentGenerationRequest) -> dict:
    logger.info(f"Starting content service for topic '{request.topic}'")
    platform_names = [p for p in request.platforms if p in ["blog", "X", "instagram"]]
    text_gen_tasks = []

    if request.use_news_search:
        gen_function = generate_content_with_agent
    else:
        gen_function = generate_simple_content
            
    for p in platform_names:
        task = gen_function(p, request.topic, request.company_info, request.language)
        text_gen_tasks.append(task)

    image_gen_task = find_relevant_image(request.topic)
    
    all_tasks = text_gen_tasks + [image_gen_task]
    results = await asyncio.gather(*all_tasks, return_exceptions=True)
    image_result = results[-1]
    text_results = results[:-1]
    content_dict = { name: res if not isinstance(res, Exception) else f"Error." for name, res in zip(platform_names, text_results) }
    image_url, image_alt = (None, None)
    if isinstance(image_result, dict) and image_result:
        image_url, image_alt = image_result.get("url"), image_result.get("alt")
    return {"generated_content": content_dict, "image_url": image_url, "image_alt": image_alt}