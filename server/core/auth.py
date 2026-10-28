from typing import Optional
from fastapi import Header, HTTPException
from core.config import settings
from core.log_config import logger

async def verify_api_key(x_api_key: Optional[str] = Header(None, alias="X-API-Key")):
    """
    Validates optional server API key if configured in settings.
    If settings.API_KEY is not set or empty, authentication is bypassed (local dev mode).
    """
    configured_key = getattr(settings, "API_KEY", "").strip()
    if not configured_key:
        return

    if not x_api_key or x_api_key != configured_key:
        logger.warning("Unauthorized request: missing or invalid X-API-Key")
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key. Include a valid 'X-API-Key' header."
        )
