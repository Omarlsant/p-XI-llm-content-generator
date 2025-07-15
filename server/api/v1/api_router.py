from fastapi import APIRouter
from api.v1.endpoints import content_generator

# Include the routes defined previously.
api_router = APIRouter()
api_router.include_router(content_generator.router, prefix="/v1", tags=["Content Generation"])