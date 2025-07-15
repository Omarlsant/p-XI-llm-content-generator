from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.v1.api_router import api_router

# 1. FastAPI app instance
app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    openapi_url=f"/api/v1/openapi.json" # URL de la documentación
)

# 2. CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Root endpoint for testing
@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.APP_NAME}"}

# 4. Include the router for our API v1
# All routes defined in api_router will have the /api prefix
app.include_router(api_router, prefix="/api")