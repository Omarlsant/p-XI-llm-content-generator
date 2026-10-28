from fastapi import APIRouter, Depends, HTTPException
from schemas.content import QueryAgentRequest, QueryAgentResponse
from services.query_agent_service import QueryAgentService, get_query_agent_service
from core.log_config import logger

router = APIRouter()

# Endpoint to invoke the Query Agent
@router.post("/invoke", response_model=QueryAgentResponse)
async def invoke_query_agent_endpoint(
    request: QueryAgentRequest,
    agent_service: QueryAgentService = Depends(get_query_agent_service)
):
    logger.info(
        f"Query Agent Endpoint received request (lang={request.language}, "
        f"use_search={request.use_search}, question_length={len(request.question)})"
    )
    logger.debug(f"Query Agent question content: {request.question}")
    try:
        answer = await agent_service.invoke(request)
        return {"answer": answer}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in Query Agent endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process query through agent.")
