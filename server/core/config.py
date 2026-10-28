import os
from typing import List, Optional

# Load environment variables if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Define a settings class to hold configuration values.
class Settings:
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    APP_NAME: str = os.getenv("APP_NAME", "Content GenerAItor")
    
    # External APIs (Optional strings)
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY") or None
    UNSPLASH_ACCESS_KEY: Optional[str] = os.getenv("UNSPLASH_ACCESS_KEY") or None
    TAVILY_API_KEY: Optional[str] = os.getenv("TAVILY_API_KEY") or None
    
    # Ollama Host
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST") or "http://localhost:11434"
    
    # Logging and Observability
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO" if os.getenv("ENVIRONMENT", "production") == "production" else "DEBUG").upper()
    
    # CORS Configuration
    _cors_raw: str = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost,http://127.0.0.1:5173")
    CORS_ORIGINS: List[str] = [origin.strip() for origin in _cors_raw.split(",") if origin.strip()]
    
    # Rate Limiting & Authentication
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    API_KEY: str = os.getenv("API_KEY", "").strip()

# Create an instance of the Settings class.
settings = Settings()
