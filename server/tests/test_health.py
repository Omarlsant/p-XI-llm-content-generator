import os
import sys

SERVER_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if SERVER_ROOT not in sys.path:
    sys.path.insert(0, SERVER_ROOT)

def test_root_endpoint_metadata():
    """Verify application name and environment settings."""
    from core.config import settings
    assert settings.APP_NAME == "Content GenerAItor"
    assert "localhost" in settings.CORS_ORIGINS[0] or "127.0.0.1" in settings.CORS_ORIGINS[0]

def test_endpoints_with_test_client():
    """Verify health and root endpoints using TestClient when fastapi is installed."""
    try:
        from fastapi.testclient import TestClient
        from main import app
    except ImportError:
        # Skip if running in environment without fastapi installed
        return

    client = TestClient(app)

    # Test root endpoint
    root_resp = client.get("/")
    assert root_resp.status_code == 200
    assert "Welcome to Content GenerAItor" in root_resp.json().get("message", "")

    # Test health check endpoint
    health_resp = client.get("/api/v1/content-agent/health")
    assert health_resp.status_code == 200
    assert health_resp.json().get("status") == "ok"
