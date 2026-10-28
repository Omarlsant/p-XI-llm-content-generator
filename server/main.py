import uvicorn
from fastapi import FastAPI, Request, HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.v1.api_router import api_router
from core.log_config import logger

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    openapi_url="/api/v1/openapi.json"
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, (HTTPException, StarletteHTTPException)):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=getattr(exc, "headers", None)
        )
    logger.error(f"Unhandled exception for request {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."}
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key"],
)

@app.get("/")
def read_root():
    logger.info("Root endpoint was hit.")
    return {"message": f"Welcome to {settings.APP_NAME}"}

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    logger.info("Application starting up via uvicorn...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
