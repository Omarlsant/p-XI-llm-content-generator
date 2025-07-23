import asyncio
import google.generativeai as genai
import ollama
import httpx
from typing import Optional
from schemas.content import ContentGenerationRequest
from core.config import settings
from core.log_config import logger

# --- Google Gemini Configuration ---
if settings.GOOGLE_API_KEY:
    try:
        genai.configure(api_key=settings.GOOGLE_API_KEY)
    except Exception as e:
        logger.error(f"Failed to configure Google Gemini API: {e}")
else:
    logger.warning("GOOGLE_API_KEY not found. Gemini model will not be available.")

# --- Unsplash Image Search Service ---
async def find_relevant_image(topic: str) -> dict:
    if not settings.UNSPLASH_ACCESS_KEY:
        logger.warning("UNSPLASH_ACCESS_KEY not found. Image generation is disabled.")
        return None
    
    url = "https://api.unsplash.com/search/photos"
    params = { "query": topic, "per_page": 1, "orientation": "landscape" }
    headers = {"Authorization": f"Client-ID {settings.UNSPLASH_ACCESS_KEY}"}
    
    try:
        async with httpx.AsyncClient() as client:
            logger.info(f"Searching for image with topic: {topic}")
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            if data.get("results"):
                image = data["results"][0]
                return {
                    "url": image["urls"]["regular"],
                    "alt": image.get("alt_description", f"A scenic image about {topic}")
                }
    except Exception as e:
        logger.error(f"Error fetching image from Unsplash: {e}", exc_info=True)
    return None

def get_prompt_template(platform: str) -> str:
    templates = {
        "blog": (
            "{company_context}"
            "You are an expert blog writer. You must write in {language}. "
            "Write a comprehensive blog post of about 300-400 words on the topic. "
            "Use markdown formatting. Topic: '{topic}'"
        ),
        "X": (
            "{company_context}"
            "You are a social media expert for X (Twitter). You must write in {language}. "
            "Write a short, witty post (under 280 characters) on the topic. "
            "Include relevant hashtags. Topic: '{topic}'"
        ),
        "instagram": (
            "{company_context}"
            "You are a creative social media manager. You must write in {language}. "
            "Write an engaging Instagram caption. Include relevant hashtags. "
            "Topic: '{topic}'"
        ),
    }
    return templates.get(platform, "")

async def _call_ollama(full_prompt: str) -> str:
    try:
        response = await ollama.AsyncClient().chat(model='llama3', messages=[{'role': 'user', 'content': full_prompt}])
        return response['message']['content'].strip()
    except Exception as e:
        logger.error(f"Ollama call failed: {e}", exc_info=True)
        return "Error: Ollama connection failed."

async def _call_gemini(full_prompt: str) -> str:
    if not settings.GOOGLE_API_KEY: return "Error: Gemini key not configured."
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = await model.generate_content_async(full_prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Gemini call failed: {e}", exc_info=True)
        return "Error: Gemini API call failed."

async def _generate_for_platform(platform: str, topic: str, model_choice: str, company_info: Optional[str], language: str) -> str:
    raw_template = get_prompt_template(platform)
    if not raw_template: return ""
    
    company_context = f"Company/Brand Information for context: '''{company_info}'''\n\n" if company_info else ""
    full_prompt = raw_template.format(company_context=company_context, language=language, topic=topic)
    
    logger.info(f"Generating content for '{platform}' in '{language}' using model '{model_choice}'.")
    
    if model_choice == 'gemini-1.5-flash':
        return await _call_gemini(full_prompt)
    return await _call_ollama(full_prompt)

async def generate_content_service(request: ContentGenerationRequest) -> dict:
    logger.info(f"Starting content service for topic '{request.topic}'")
    
    platform_names = [p for p in request.platforms if p in ["blog", "X", "instagram"]]
    text_gen_tasks = [_generate_for_platform(p, request.topic, request.model, request.company_info, request.language) for p in platform_names]
    image_gen_task = find_relevant_image(request.topic)
    
    all_tasks = text_gen_tasks + [image_gen_task]
    results = await asyncio.gather(*all_tasks, return_exceptions=True)
    
    image_result = results[-1]
    text_results = results[:-1]
    
    content_dict = {}
    for i, result in enumerate(text_results):
        platform_name = platform_names[i]
        content_dict[platform_name] = result if not isinstance(result, Exception) else f"Error: Failed to generate content for {platform_name}."

    image_url, image_alt = (None, None)
    if isinstance(image_result, dict) and image_result:
        image_url, image_alt = image_result.get("url"), image_result.get("alt")
    elif isinstance(image_result, Exception):
        logger.error(f"Image generation task failed: {image_result}")

    return {"generated_content": content_dict, "image_url": image_url, "image_alt": image_alt}