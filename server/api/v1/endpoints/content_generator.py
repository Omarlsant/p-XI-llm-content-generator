from fastapi import APIRouter, HTTPException
from schemas.content import ContentGenerationRequest, ContentGenerationResponse
from services import generator_service 
from core.log_config import logger

router = APIRouter()

@router.post("", response_model=ContentGenerationResponse)
@router.post("/", response_model=ContentGenerationResponse) 
async def generate_content(request: ContentGenerationRequest):
    logger.info(f"Endpoint: Received generation request (platforms={request.platforms}, lang={request.language}, topic_length={len(request.topic)})")
    logger.debug(f"Topic content: {request.topic}")
    
    try:
        response_data = await generator_service.generate_content_service(request)
        if not response_data.get("generated_content"):
            errors = response_data.get("errors", {})
            detail_msg = f"Failed to generate text content for requested platforms: {errors}" if errors else "Failed to generate text content for requested platforms."
            raise HTTPException(status_code=502, detail=detail_msg)
        
        logger.info("Endpoint: Successfully generated content.")
        return response_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in generation endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")
    
@router.get("/health", response_model=dict)
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "ok", "message": "Content generation service is running."}
