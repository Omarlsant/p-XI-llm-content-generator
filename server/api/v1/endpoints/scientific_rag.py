from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.rag_service import RAGService, get_rag_service, GraphRAGService, get_graph_rag_service
from core.log_config import logger

router = APIRouter()

class RAGQueryRequest(BaseModel):
    question: str

@router.post("/query-vector")
async def query_rag_endpoint(
    request: RAGQueryRequest,
    rag_service: RAGService = Depends(get_rag_service) 
):
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    logger.info(f"Vector RAG Endpoint: Received question: '{request.question}'")
    try:
        answer = await rag_service.query(request.question)
        return {"answer": answer}
    except FileNotFoundError as e:
        logger.error(f"RAG database not found: {e}")
        raise HTTPException(status_code=503, detail="The RAG knowledge base is not available.")
    except Exception as e:
        logger.error(f"Error in RAG endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process RAG query.")


# --- GRAPH RAG ---
@router.post("/query-graph")
async def query_graph_rag_endpoint(
    request: RAGQueryRequest,
    graph_rag_service: GraphRAGService = Depends(get_graph_rag_service)
):
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    logger.info(f"Graph RAG Endpoint: Received question: '{request.question}'")
    try:
        answer = await graph_rag_service.query(request.question)
        return {"answer": answer}
    except Exception as e:
        logger.error(f"Error in Graph RAG endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process Graph RAG query.")