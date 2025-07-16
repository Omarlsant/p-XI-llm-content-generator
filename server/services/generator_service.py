import asyncio
import google.generativeai as genai
import ollama
from typing import Optional
from schemas.content import ContentGenerationRequest
from core.config import settings
from core.log_config import logger 

# Configure Google Gemini API key if available
if settings.GOOGLE_API_KEY:
    try:
        genai.configure(api_key=settings.GOOGLE_API_KEY)
    except Exception as e:
        logger.error(f"Failed to configure Google Gemini API: {e}")
else:
    logger.warning("GOOGLE_API_KEY not found in .env. Gemini model will not be available.")

def get_prompt_template(platform: str) -> str:
    templates = {
        "blog": (
            "{company_context}"
            "You are an expert blog writer. Your tone is insightful and informative. "
            "Write a comprehensive blog post of about 300-400 words on the topic. "
            "Use markdown formatting (headers, bold, lists). Topic: '{topic}'"
        ),
        "X": (
            "{company_context}"
            "You are a social media expert for X (formerly Twitter). Your tone is concise and witty. "
            "Write a short post (under 280 characters) on the topic. "
            "Include 2-3 relevant hashtags. Topic: '{topic}'"
        ),
        "instagram": (
            "{company_context}"
            "You are a creative social media manager. Your tone is inspiring and visual. "
            "Write an engaging Instagram caption for the topic. "
            "Start with a strong hook, add value, and end with a call to engagement. "
            "Include 5-7 relevant hashtags. Topic: '{topic}'"
        ),
    }
    return templates.get(platform, "")

async def _call_ollama(full_prompt: str) -> str:
    try:
        response = await ollama.AsyncClient().chat(
            model='llama3',
            messages=[{'role': 'user', 'content': full_prompt}],
            stream=False
        )
        return response['message']['content'].strip()
    except Exception as e:
        logger.error(f"Error calling Ollama: {e}", exc_info=True)
        return "Error: Could not get response from Ollama. Is the server running?"

async def _call_gemini(full_prompt: str) -> str:
    if not settings.GOOGLE_API_KEY:
        return "Error: Gemini API key is not configured in the server."
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = await model.generate_content_async(full_prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error calling Gemini: {e}", exc_info=True)
        return "Error: Could not get response from Gemini API. Check server logs."

async def _generate_for_platform(platform: str, topic: str, model_choice: str, company_info: Optional[str]) -> str:
    prompt_template = get_prompt_template(platform)
    if not prompt_template:
        return ""
    
    company_context = f"Company/Brand Information for context: '''{company_info}'''\n\n" if company_info else ""
    full_prompt = prompt_template.format(topic=topic, company_context=company_context)
    
    logger.info(f"Generating content for '{platform}' using model '{model_choice}'.")
    
    if model_choice == 'gemini-1.5-flash':
        return await _call_gemini(full_prompt)
    
    return await _call_ollama(full_prompt)

async def generate_content_service(request: ContentGenerationRequest) -> dict:
    logger.info(f"Starting content generation for topic '{request.topic}' with model '{request.model}'.")
    
    tasks = [
        _generate_for_platform(platform, request.topic, request.model, request.company_info)
        for platform in request.platforms if platform in ["blog", "X", "instagram"]
    ]
    
    platform_names = [p for p in request.platforms if p in ["blog", "X", "instagram"]]
    
    results = await asyncio.gather(*tasks)
    
    response_data = dict(zip(platform_names, results))
    return response_data