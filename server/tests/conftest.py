import os
import sys

# Ensure server root is in sys.path for test discovery
SERVER_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if SERVER_ROOT not in sys.path:
    sys.path.insert(0, SERVER_ROOT)

# Set test environment flags
os.environ["ENVIRONMENT"] = "test"
os.environ["API_KEY"] = ""  # No auth required by default in test
os.environ["OLLAMA_HOST"] = "http://localhost:11434"

try:
    import pytest
    from fastapi.testclient import TestClient
    from main import app

    @pytest.fixture
    def client():
        """FastAPI TestClient fixture without real network calls."""
        with TestClient(app) as test_client:
            yield test_client

except ImportError:
    # If pytest/fastapi not installed in this environment, conftest loads gracefully
    pass
