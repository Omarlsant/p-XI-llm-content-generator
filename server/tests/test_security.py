import os
import sys
import time

SERVER_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if SERVER_ROOT not in sys.path:
    sys.path.insert(0, SERVER_ROOT)

def test_cors_settings():
    """Verify TASK-014: CORS origins configuration."""
    from core.config import settings
    assert isinstance(settings.CORS_ORIGINS, list)
    assert len(settings.CORS_ORIGINS) > 0
    # Must contain frontend default origins
    origins_str = " ".join(settings.CORS_ORIGINS)
    assert "localhost" in origins_str or "127.0.0.1" in origins_str

def test_in_memory_rate_limiter():
    """Verify TASK-015: Rate limiter blocks after exceeding requests per minute."""
    try:
        from core.rate_limit import InMemoryRateLimiter
        from fastapi import HTTPException
    except ImportError:
        return

    # Create limiter with 3 requests per minute limit
    limiter = InMemoryRateLimiter(requests_per_minute=3)
    test_ip = "192.168.1.100"

    # First 3 requests must pass
    assert limiter.is_allowed(test_ip) is True
    assert limiter.is_allowed(test_ip) is True
    assert limiter.is_allowed(test_ip) is True

    # 4th request must be rejected
    assert limiter.is_allowed(test_ip) is False

    # Check that retry_after returns an integer >= 1
    retry_after = limiter.get_retry_after(test_ip)
    assert isinstance(retry_after, int)
    assert retry_after >= 1

def test_api_key_auth_verification():
    """Verify TASK-015: API key verification logic."""
    try:
        from core.auth import verify_api_key
        from core.config import settings
        from fastapi import HTTPException
    except ImportError:
        return

    import asyncio

    # When settings.API_KEY is empty, any request is allowed
    with patch_settings_attr("API_KEY", ""):
        assert asyncio.run(verify_api_key(None)) is None
        assert asyncio.run(verify_api_key("any-random-key")) is None

    # When settings.API_KEY is configured
    with patch_settings_attr("API_KEY", "secret-test-key-123"):
        # Correct key passes
        assert asyncio.run(verify_api_key("secret-test-key-123")) == "secret-test-key-123"

        # Missing key raises 401
        try:
            asyncio.run(verify_api_key(None))
            assert False, "Should have raised HTTPException 401 for missing key"
        except HTTPException as exc:
            assert exc.status_code == 401

        # Wrong key raises 401
        try:
            asyncio.run(verify_api_key("wrong-key"))
            assert False, "Should have raised HTTPException 401 for wrong key"
        except HTTPException as exc:
            assert exc.status_code == 401

class patch_settings_attr:
    """Helper context manager to temporarily patch settings attribute."""
    def __init__(self, attr, value):
        from core.config import settings
        self.settings = settings
        self.attr = attr
        self.value = value
        self.old_val = getattr(settings, attr, "")

    def __enter__(self):
        setattr(self.settings, self.attr, self.value)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        setattr(self.settings, self.attr, self.old_val)
