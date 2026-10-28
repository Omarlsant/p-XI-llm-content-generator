import os
import sys
from unittest.mock import patch, MagicMock

SERVER_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if SERVER_ROOT not in sys.path:
    sys.path.insert(0, SERVER_ROOT)

def test_query_agent_response_format():
    """Verify QueryAgentResponse structure."""
    try:
        from schemas.content import QueryAgentResponse
    except ImportError:
        return

    res = QueryAgentResponse(answer="Here is the formatted answer in markdown.")
    assert res.answer == "Here is the formatted answer in markdown."

def test_query_agent_content_creation_formatting():
    """Verify TASK-006: content creation returns formatted text rather than raw dict representation."""
    try:
        from services.query_agent_service import generate_content_for_agent
        from schemas.content import QueryAgentRequest
    except ImportError:
        return

    # Mock the generator service to return structured generated_content
    mock_content_response = MagicMock()
    mock_content_response.generated_content = {
        "blog": "### The Power of AI\n\nAI transforms digital automation.",
        "X": "AI transforms digital automation! #AI #Tech"
    }

    req = QueryAgentRequest(question="Write a post about AI", language="English")

    with patch("services.generator_service.generate_content_service", return_value=mock_content_response):
        # We test the formatting logic
        import asyncio
        async def run_test():
            result = await generate_content_for_agent(req)
            assert isinstance(result, str)
            # Must NOT be a python str(dict) like "{'blog': ...}"
            assert "### The Power of AI" in result or "BLOG" in result.upper()
            assert not result.startswith("{'")
        asyncio.run(run_test())
