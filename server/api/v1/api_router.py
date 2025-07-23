from fastapi import APIRouter
from api.v1.endpoints import content_generator
from api.v1.endpoints import scientific_rag

api_router = APIRouter()

api_router.include_router(
    content_generator.router, 
    prefix="/v1/generate",
    tags=["Content Generation"]
)

api_router.include_router(
    scientific_rag.router,
    prefix="/v1/rag",
    tags=["Scientific RAG"]
)