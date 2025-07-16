from fastapi import APIRouter, HTTPException
from schemas.content import ContentGenerationRequest
from services import generator_service 
from core.log_config import logger

router = APIRouter()

@router.post("/generate")
async def generate_content(request: ContentGenerationRequest):
    logger.info(f"Endpoint: Received request to generate content for topic: '{request.topic}'")
    
    try:
        # Call the new main service function
        response_data = await generator_service.generate_content_service(request)
        
        if not response_data:
            logger.warning("No content generated. Platforms might be unsupported.")
            raise HTTPException(status_code=400, detail="No content could be generated for the selected platforms.")
        
        logger.info(f"Endpoint: Successfully generated content for platforms: {list(response_data.keys())}")
        return response_data
    except Exception as e:
        logger.error(f"Error in generation endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred in the server.")