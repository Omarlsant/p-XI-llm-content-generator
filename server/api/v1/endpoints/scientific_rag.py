from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.rag_service import RAGService, get_rag_service
from core.log_config import logger

router = APIRouter()

class RAGQueryRequest(BaseModel):
    question: str

@router.post("/query")
async def query_rag_endpoint(
    request: RAGQueryRequest,
    # FastAPI resolverá esta dependencia y nos dará una instancia de RAGService
    rag_service: RAGService = Depends(get_rag_service) 
):
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    logger.info(f"RAG Endpoint: Received question: '{request.question}'")
    try:
        # Ahora llamamos directamente al método .query() del servicio inyectado
        answer = await rag_service.query(request.question)
        return {"answer": answer}
    except FileNotFoundError as e:
        logger.error(f"RAG database not found: {e}")
        raise HTTPException(status_code=503, detail="The RAG knowledge base is not available. Please contact an administrator.")
    except Exception as e:
        logger.error(f"Error in RAG endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process RAG query.")