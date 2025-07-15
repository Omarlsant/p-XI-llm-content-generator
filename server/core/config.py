import os
from dotenv import load_dotenv

# Load environment variables.
load_dotenv()

# Define a settings class to hold configuration values.
class Settings:
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI App")

# Create an instance of the Settings class.
settings = Settings()