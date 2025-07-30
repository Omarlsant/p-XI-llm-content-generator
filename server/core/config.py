import os
from dotenv import load_dotenv

# Load environment variables.
load_dotenv()

# Define a settings class to hold configuration values.
class Settings:
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI App")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    UNSPLASH_ACCESS_KEY: str = os.getenv("UNSPLASH_ACCESS_KEY")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST")

# Create an instance of the Settings class.
settings = Settings()
