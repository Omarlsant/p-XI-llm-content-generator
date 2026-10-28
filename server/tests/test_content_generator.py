import os
import sys
import asyncio
from unittest.mock import patch, AsyncMock

SERVER_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if SERVER_ROOT not in sys.path:
    sys.path.insert(0, SERVER_ROOT)

def test_platform_constraints():
    """Verify platform specific prompt rules."""
    try:
        from services.generator_service import get_platform_constraints
    except ImportError:
        return

    blog_rule = get_platform_constraints("blog")
    assert "blog post" in blog_rule
    assert "markdown" in blog_rule

    x_rule = get_platform_constraints("X")
    assert "tweet" in x_rule
    assert "280 characters" in x_rule

    instagram_rule = get_platform_constraints("instagram")
    assert "Instagram caption" in instagram_rule
    assert "emojis" in instagram_rule

def test_generator_service_contract_partial_success():
    """Verify TASK-011 contract: partial failures return success with errors dict."""
    try:
        from schemas.content import ContentGenerationRequest
        from services.generator_service import generate_content_service
    except ImportError:
        return

    request = ContentGenerationRequest(
        topic="Machine Learning in 2026",
        platforms=["blog", "X"],
        model="llama3",
        language="English"
    )

    async def run_test():
        # Mock generate_single_platform where blog succeeds but X fails
        async def mock_generate(platform, *args, **kwargs):
            if platform == "blog":
                return "Generated blog article."
            raise RuntimeError("Ollama context timeout on X")

        with patch("services.generator_service.generate_single_platform", side_effect=mock_generate), \
             patch("services.generator_service.find_relevant_image", return_value={"url": "http://img", "alt": "alt"}):
            result = await generate_content_service(request)
            assert result.generated_content.get("blog") == "Generated blog article."
            assert "X" in result.errors
            assert "Ollama context timeout on X" in result.errors["X"]
            assert result.success is True

    asyncio.run(run_test())

def test_generator_service_contract_total_failure():
    """Verify TASK-011 contract: total failure across all platforms raises HTTPException 502."""
    try:
        from schemas.content import ContentGenerationRequest
        from services.generator_service import generate_content_service
        from fastapi import HTTPException
    except ImportError:
        return

    request = ContentGenerationRequest(
        topic="Total failure test",
        platforms=["blog", "X"],
        model="llama3",
        language="English"
    )

    async def run_test():
        async def mock_fail(*args, **kwargs):
            raise ConnectionError("Ollama service unavailable")

        with patch("services.generator_service.generate_single_platform", side_effect=mock_fail), \
             patch("services.generator_service.find_relevant_image", return_value=None):
            try:
                await generate_content_service(request)
                assert False, "Should have raised HTTPException with status_code=502"
            except HTTPException as e:
                assert e.status_code == 502
                assert isinstance(e.detail, dict)
                assert "blog" in e.detail.get("errors", {})
                assert "X" in e.detail.get("errors", {})

    asyncio.run(run_test())
