from fastapi import APIRouter, Depends, HTTPException
from schemas.content import RAGQueryRequest, RAGQueryResponse
from services.rag_service import RAGService, get_rag_service, GraphRAGService, get_graph_rag_service
from core.log_config import logger

router = APIRouter()

@router.post("/query-vector", response_model=RAGQueryResponse)
async def query_rag_endpoint(
    request: RAGQueryRequest,
    rag_service: RAGService = Depends(get_rag_service) 
):
    logger.info(f"Vector RAG Endpoint: Received request (question_length={len(request.question)})")
    logger.debug(f"Vector RAG Question: {request.question}")
    try:
        answer = await rag_service.query(request.question)
        return {"answer": answer}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in RAG endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process RAG query.")


# --- GRAPH RAG ---
@router.post("/query-graph", response_model=RAGQueryResponse)
async def query_graph_rag_endpoint(
    request: RAGQueryRequest,
    graph_rag_service: GraphRAGService = Depends(get_graph_rag_service)
):
    logger.info(f"Graph RAG Endpoint: Received request (question_length={len(request.question)})")
    logger.debug(f"Graph RAG Question: {request.question}")
    try:
        answer = await graph_rag_service.query(request.question)
        return {"answer": answer}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in Graph RAG endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process Graph RAG query.")
