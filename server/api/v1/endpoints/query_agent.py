# server/api/v1/endpoints/query_agent.py
from fastapi import APIRouter, Depends, HTTPException
from schemas.content import QueryAgentRequest # <-- IMPORT FROM SCHEMAS
from services.query_agent_service import QueryAgentService, get_query_agent_service
from core.log_config import logger

router = APIRouter()

@router.post("/invoke")
async def invoke_query_agent_endpoint(
    request: QueryAgentRequest,
    agent_service: QueryAgentService = Depends(get_query_agent_service)
):
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    logger.info(f"Query Agent Endpoint received: '{request.question}' with options.")
    try:
        # Pass the entire validated request object to the service
        answer = await agent_service.invoke(request)
        return {"answer": answer}
    except Exception as e:
        logger.error(f"Error in Query Agent endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process query through agent.")