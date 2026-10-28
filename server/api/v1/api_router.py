from fastapi import APIRouter, Depends
from api.v1.endpoints import content_generator, scientific_rag, query_agent
from core.rate_limit import rate_limiter
from core.auth import verify_api_key

api_router = APIRouter(
    dependencies=[Depends(rate_limiter), Depends(verify_api_key)]
)

# Specialist Agent 1: The Content Generator
api_router.include_router(
    content_generator.router, 
    prefix="/v1/content-agent",
    tags=["Specialist: Content Agent"]
)

# Specialist Agent 2: The RAG System
api_router.include_router(
    scientific_rag.router,
    prefix="/v1/rag",
    tags=["Specialist: RAG Agent"]
)

# Supervisor/Main Agent: The Query Agent
api_router.include_router(
    query_agent.router,
    prefix="/v1/query-agent",
    tags=["Supervisor: Query Agent"]
)
