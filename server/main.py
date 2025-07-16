from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.v1.api_router import api_router
from core.log_config import logger

# 2. FastAPI app instance
app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    openapi_url=f"/api/v1/openapi.json"
)

# 3. GLOBAL EXCEPTION HANDLER
# This is a powerful feature. It catches any unhandled Exception
# and ensures a clean JSON response is sent to the client.
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the full traceback of the error
    logger.error(f"Unhandled exception for request {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please check the logs for more details."}
    )

# 4. CORS configuration (no changes here)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Root endpoint for testing
@app.get("/")
def read_root():
    logger.info("Root endpoint was hit.")
    return {"message": f"Welcome to {settings.APP_NAME}"}

# 6. Include the router for our API v1
# All routes defined in api_router will have the /api prefix
app.include_router(api_router, prefix="/api")

logger.info("Application startup complete.")