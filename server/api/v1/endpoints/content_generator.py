from fastapi import APIRouter, HTTPException
from schemas.content import ContentGenerationRequest
from services import generator_service

router = APIRouter()

# Endpoint for content generation.
@router.post("/generate")
def generate_content(request: ContentGenerationRequest):
    response_data = generator_service.generate_mock_content(request)

    if not response_data:
        raise HTTPException(status_code=400, detail="Please select at least one platform.")
    return response_data