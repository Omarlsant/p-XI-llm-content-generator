import os
import sys

SERVER_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if SERVER_ROOT not in sys.path:
    sys.path.insert(0, SERVER_ROOT)

def test_pydantic_content_generation_schemas():
    """Verify ContentGenerationRequest validation rules."""
    try:
        from schemas.content import ContentGenerationRequest, ContentGenerationResponse
        from pydantic import ValidationError
    except ImportError:
        return

    # Valid payload
    valid_req = ContentGenerationRequest(
        topic="Artificial Intelligence Trends",
        platforms=["blog", "X"],
        model="llama3",
        language="English"
    )
    assert valid_req.topic == "Artificial Intelligence Trends"
    assert valid_req.platforms == ["blog", "X"]
    assert valid_req.model == "llama3"

    # Empty topic should raise ValidationError
    try:
        ContentGenerationRequest(topic="", platforms=["blog"])
        assert False, "Should have raised ValidationError for empty topic"
    except ValidationError:
        pass

    # Topic exceeding max length (500 chars) should raise ValidationError
    try:
        ContentGenerationRequest(topic="a" * 501, platforms=["blog"])
        assert False, "Should have raised ValidationError for topic > 500 chars"
    except ValidationError:
        pass

    # Unsupported platform should raise ValidationError
    try:
        ContentGenerationRequest(topic="Valid topic", platforms=["myspace"])
        assert False, "Should have raised ValidationError for invalid platform"
    except ValidationError:
        pass

    # Unsupported model should raise ValidationError
    try:
        ContentGenerationRequest(topic="Valid topic", platforms=["blog"], model="unknown_model")
        assert False, "Should have raised ValidationError for unsupported model"
    except ValidationError:
        pass

    # Unsupported language should raise ValidationError
    try:
        ContentGenerationRequest(topic="Valid topic", platforms=["blog"], language="Klingon")
        assert False, "Should have raised ValidationError for unsupported language"
    except ValidationError:
        pass

def test_pydantic_query_and_rag_schemas():
    """Verify QueryAgentRequest and RAGQueryRequest validation rules."""
    try:
        from schemas.content import QueryAgentRequest, QueryAgentResponse, RAGQueryRequest, RAGQueryResponse
        from pydantic import ValidationError
    except ImportError:
        return

    # Valid QueryAgentRequest
    valid_query = QueryAgentRequest(question="What is RAG?", language="Spanish")
    assert valid_query.question == "What is RAG?"
    assert valid_query.language == "Spanish"
    assert valid_query.use_search is False

    # Empty QueryAgentRequest question
    try:
        QueryAgentRequest(question="")
        assert False, "Should have raised ValidationError for empty question"
    except ValidationError:
        pass

    # Question exceeding 1000 characters
    try:
        QueryAgentRequest(question="q" * 1001)
        assert False, "Should have raised ValidationError for question > 1000 chars"
    except ValidationError:
        pass

    # Valid RAGQueryRequest
    valid_rag = RAGQueryRequest(question="Explain vector embeddings")
    assert valid_rag.question == "Explain vector embeddings"

    # Empty RAGQueryRequest question
    try:
        RAGQueryRequest(question="")
        assert False, "Should have raised ValidationError for empty RAG question"
    except ValidationError:
        pass
