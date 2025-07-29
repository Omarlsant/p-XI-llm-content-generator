# USE THIS IN LOCAL.
# # server/services/generator_service.py
# import asyncio
# import httpx
# import google.generativeai as genai
# import ollama
# from typing import Optional
# from traceback import format_exc

# # --- CORE LANGCHAIN IMPORTS ---
# from langchain_community.chat_models import ChatOllama
# from langchain_core.prompts import PromptTemplate
# from langchain.agents import create_react_agent, AgentExecutor
# from langchain_community.tools.tavily_search import TavilySearchResults

# from schemas.content import ContentGenerationRequest
# from core.config import settings
# from core.log_config import logger

# # --- Service Initializations & Helpers ---
# if settings.GOOGLE_API_KEY:
#     try: genai.configure(api_key=settings.GOOGLE_API_KEY)
#     except Exception as e: logger.error(f"Failed to configure Google Gemini API: {e}")
# else: logger.warning("GOOGLE_API_KEY not found. Gemini model will not be available.")

# async def find_relevant_image(topic: str) -> dict:
#     if not settings.UNSPLASH_ACCESS_KEY: return None
#     url, params = "https://api.unsplash.com/search/photos", {"query": topic, "per_page": 1, "orientation": "landscape"}
#     headers = {"Authorization": f"Client-ID {settings.UNSPLASH_ACCESS_KEY}"}
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(url, params=params, headers=headers)
#             response.raise_for_status()
#             data = response.json()
#             if data.get("results"):
#                 image = data["results"][0]
#                 return {"url": image["urls"]["regular"], "alt": image.get("alt_description", f"Image about {topic}")}
#     except Exception as e:
#         logger.error(f"Error fetching image: {e}", exc_info=True)
#     return None

# # --- STRATEGY 1: Simple, Non-Agentic Generation ---
# def get_simple_prompt_template(platform: str) -> str:
#     templates = {
#         "blog": ("{company_context}You are an expert blog writer. You must write in {language}. Write a comprehensive blog post about 300-400 words on the topic. Use markdown formatting. Topic: '{topic}'"),
#         "X": ("{company_context}You are a social media expert for X (Twitter). You must write in {language}. Write a short, witty post (under 280 characters) on the topic. Include relevant hashtags. Topic: '{topic}'"),
#         "instagram": ("{company_context}You are a creative social media manager. You must write in {language}. Write an engaging Instagram caption. Include relevant hashtags. Topic: '{topic}'"),
#     }
#     return templates.get(platform, "")

# async def generate_simple_content(platform: str, topic: str, company_info: Optional[str], language: str, **kwargs) -> str:
#     logger.info(f"Using SIMPLE generation for platform '{platform}'")
#     llm = ollama.AsyncClient()
#     raw_template = get_simple_prompt_template(platform)
#     if not raw_template: return ""
#     company_context = f"Company/Brand Information: '''{company_info}'''\n\n" if company_info else ""
#     full_prompt = raw_template.format(company_context=company_context, language=language, topic=topic)
#     try:
#         response = await llm.chat(model='llama3', messages=[{'role': 'user', 'content': full_prompt}])
#         return response['message']['content'].strip()
#     except Exception as e:
#         logger.error(f"Simple generation failed for {platform}: {e}", exc_info=True)
#         return f"Error: Standard generation failed for {platform}."

# # --- Platform-Specific Constraints for the Agent ---
# def get_platform_constraints(platform: str) -> str:
#     """Returns a string with specific formatting rules for a platform."""
#     constraints = {
#         "blog": "The output must be a well-structured blog post of 300-400 words, using markdown for formatting.",
#         "X": "The output MUST be a short, concise tweet under 280 characters and include relevant hashtags.",
#         "instagram": "The output must be an engaging Instagram caption, including emojis and relevant hashtags."
#     }
#     return constraints.get(platform, "The output should be a standard text response.")

# # --- STRATEGY 2: Agentic Generation ---
# async def generate_content_with_agent(platform: str, topic: str, company_info: Optional[str], language: str, use_search: bool, **kwargs) -> str:
#     logger.info(f"Using AGENTIC generation for platform '{platform}'")
#     llm = ChatOllama(model="llama3", temperature=0)
    
#     tools = []
#     if use_search and settings.TAVILY_API_KEY:
#         search_tool = TavilySearchResults(max_results=3)
#         search_tool.description = (
#             "A search engine. Use this to find real-time information on any topic. "
#             "After using this tool once, you will have enough information to write the final answer."
#         )
#         tools.append(search_tool)
    
#     platform_specific_rules = get_platform_constraints(platform)
    
#     react_prompt_template = f"""
# Answer the user's request using the available tools if necessary.

# You have access to the following tools:
# {{tools}}

# Use the following format:
# Thought: Do I need to use a tool to find up-to-date information? Yes or No.
# Action: The action to take, should be one of [{{tool_names}}]
# Action Input: A clear and concise search query for the tool.
# Observation: The result of the action.
# Thought: I now have sufficient information to generate the final answer according to all the user's rules.
# Final Answer: [The final response]

# **Very Important Rules for your Final Answer:**
# 1. Your final answer MUST strictly follow these platform-specific rules: "{platform_specific_rules}"
# 2. Your final answer MUST be written entirely in {language}.
# 3. If provided, use this context: {{company_context}}.

# Begin!

# User request: Generate content for the {platform} platform about the topic: '{topic}'.
# Question: {{input}}
# Thought:{{agent_scratchpad}}
# """
#     prompt = PromptTemplate.from_template(react_prompt_template)
#     agent = create_react_agent(llm, tools, prompt)
#     agent_executor = AgentExecutor(
#         agent=agent, tools=tools, verbose=False, 
#         handle_parsing_errors=True, max_iterations=5,
#         early_stopping_method="generate"
#     )
    
#     company_context_str = f"'''{company_info}'''" if company_info else "No company info provided."
#     input_dict = {
#         "platform": platform,
#         "topic": topic,
#         "language": language,
#         "company_context": company_context_str,
#         "input": f"Generate content for {platform} about: {topic}",
#     }

#     try:
#         response = await agent_executor.ainvoke(input_dict)
#         return response['output'].strip()
#     except Exception as e:
#         logger.error(f"AGENT EXECUTION FAILED FOR '{platform}':\n{format_exc()}")
#         return f"Error: Agent failed for {platform}."

# # --- Main Service Function (Orchestrator) ---
# async def generate_content_service(request: ContentGenerationRequest) -> dict:
#     logger.info(f"SERVICE ENTRYPOINT. Received request with use_news_search = {request.use_news_search} (Type: {type(request.use_news_search)})")
    
#     platform_names = [p for p in request.platforms if p in ["blog", "X", "instagram"]]
#     text_gen_tasks = []

#     gen_function = generate_content_with_agent if request.use_news_search else generate_simple_content

#     for p in platform_names:
#         task = gen_function(
#             platform=p, 
#             topic=request.topic, 
#             company_info=request.company_info, 
#             language=request.language,
#             use_search=request.use_news_search 
#         )
#         text_gen_tasks.append(task)
            
#     image_gen_task = find_relevant_image(request.topic)
    
#     all_tasks = text_gen_tasks + [image_gen_task]
#     results = await asyncio.gather(*all_tasks, return_exceptions=True)
    
#     image_result = results[-1]
#     text_results = results[:-1]
#     content_dict = { name: res for name, res in zip(platform_names, text_results) if not isinstance(res, Exception) }
#     image_url, image_alt = (None, None)
#     if isinstance(image_result, dict) and image_result:
#         image_url, image_alt = image_result.get("url"), image_result.get("alt")

#     return {"generated_content": content_dict, "image_url": image_url, "image_alt": image_alt}


#USE THIS IN DOCKER.

# server/services/generator_service.py
import asyncio
import httpx
import google.generativeai as genai
import ollama
import json
from typing import Optional, List
from traceback import format_exc

# --- CORE LANGCHAIN IMPORTS (Minimal Set for Manual Agent) ---
from langchain_community.chat_models import ChatOllama
from langchain_community.tools.tavily_search import TavilySearchResults

from schemas.content import ContentGenerationRequest
from core.config import settings
from core.log_config import logger

# --- Service Initializations & Helpers ---
if settings.GOOGLE_API_KEY:
    try: genai.configure(api_key=settings.GOOGLE_API_KEY)
    except Exception as e: logger.error(f"Failed to configure Google Gemini API: {e}")
else: logger.warning("GOOGLE_API_KEY not found.")

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

# --- STRATEGY 1: Simple, Non-Agentic Generation ---
def get_simple_prompt_template(platform: str) -> str:
    templates = {
        "blog": ("{company_context}You are an expert blog writer in {language}. Write a comprehensive blog post about 300-400 words on: '{topic}'. Use markdown."),
        "X": ("{company_context}You are a social media expert for X (Twitter) writing in {language}. Write a short, witty post (under 280 characters) on: '{topic}'. Include hashtags."),
        "instagram": ("{company_context}You are a creative social media manager writing in {language}. Write an engaging Instagram caption for a post about: '{topic}'. Include hashtags."),
    }
    return templates.get(platform, "")

async def generate_simple_content(platform: str, topic: str, company_info: Optional[str], language: str, **kwargs) -> str:
    logger.info(f"Using SIMPLE generation for platform '{platform}'")
    llm = ollama.AsyncClient(host=settings.OLLAMA_HOST)
    raw_template = get_simple_prompt_template(platform)
    if not raw_template: return ""
    company_context = f"Context: '''{company_info}'''\n\n" if company_info else ""
    full_prompt = raw_template.format(company_context=company_context, language=language, topic=topic)
    try:
        response = await llm.chat(model='llama3', messages=[{'role': 'user', 'content': full_prompt}])
        return response['message']['content'].strip()
    except Exception as e:
        logger.error(f"Simple generation failed: {e}", exc_info=True)
        return "Error: Standard generation failed."

# --- Platform-Specific Constraints ---
def get_platform_constraints(platform: str) -> str:
    constraints = {
        "blog": "a well-structured blog post of 300-400 words with markdown.",
        "X": "a short tweet under 280 characters with hashtags.",
        "instagram": "an engaging Instagram caption with emojis and hashtags."
    }
    return constraints.get(platform, "a standard text response.")

# --- STRATEGY 2: Manual Agentic Generation ---
async def generate_content_with_agent(platform: str, topic: str, company_info: Optional[str], language: str, use_search: bool, **kwargs) -> str:
    logger.info(f"Using MANUAL AGENT for '{platform}'")
    
    ollama_base_url = settings.OLLAMA_HOST or "http://localhost:11434"
    planner_llm = ChatOllama(model="llama3", temperature=0, base_url=ollama_base_url, format="json")
    writer_llm = ChatOllama(model="llama3", temperature=0.2, base_url=ollama_base_url)
    
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
        return f"Error: The agent for {platform} encountered an error. See server logs."

# --- Main Service Function (Orchestrator) ---
async def generate_content_service(request: ContentGenerationRequest) -> dict:
    logger.info(f"SERVICE ENTRYPOINT. Received request with use_news_search = {request.use_news_search}")
    
    platform_names = [p for p in request.platforms if p in ["blog", "X", "instagram"]]
    
    text_gen_tasks = []
    # The flag from the frontend now correctly chooses the generation strategy
    gen_function = generate_content_with_agent if request.use_news_search else generate_simple_content
    
    for p in platform_names:
        task = gen_function(
            platform=p, 
            topic=request.topic, 
            company_info=request.company_info, 
            language=request.language,
            use_search=request.use_news_search
        )
        text_gen_tasks.append(task)
            
    image_gen_task = find_relevant_image(request.topic)
    
    all_tasks = text_gen_tasks + [image_gen_task]
    results = await asyncio.gather(*all_tasks, return_exceptions=True)
    
    image_result, text_results = results[-1], results[:-1]
    
    content_dict, has_success = {}, False
    for i, res in enumerate(text_results):
        name = platform_names[i]
        if not isinstance(res, Exception) and res and "Error:" not in res:
            content_dict[name] = res
            has_success = True
        else:
            logger.error(f"Generation for '{name}' failed with result: {res}")
            content_dict[name] = str(res) if isinstance(res, str) else "A critical agent error occurred."
            
    image_url, image_alt = (None, None)
    if isinstance(image_result, dict) and image_result:
        image_url, image_alt = image_result.get("url"), image_result.get("alt")

    return { "generated_content": content_dict, "image_url": image_url, "image_alt": image_alt, "success": has_success }