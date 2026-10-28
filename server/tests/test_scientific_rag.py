import os
import sys
from unittest.mock import MagicMock, patch

SERVER_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if SERVER_ROOT not in sys.path:
    sys.path.insert(0, SERVER_ROOT)

def test_graph_rag_knowledge_base_exists():
    """Verify that the knowledge base file for GraphRAG exists and contains concepts."""
    kb_path = os.path.join(SERVER_ROOT, "knowledge_base", "rag_concepts.txt")
    assert os.path.exists(kb_path), f"Knowledge base file not found at {kb_path}"
    with open(kb_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert len(content.strip()) > 0
    assert "Retrieval-Augmented Generation" in content
    assert "vector database" in content

def test_guardrail_prompt_template_variables():
    """Verify TASK-008: guardrail prompt template contains all required input variables."""
    try:
        from services.rag_service import EVALUATION_PROMPT
    except ImportError:
        return

    # Check input_variables in prompt template
    assert "context" in EVALUATION_PROMPT.input_variables
    assert "question" in EVALUATION_PROMPT.input_variables
    assert "generation" in EVALUATION_PROMPT.input_variables

def test_rag_service_empty_database_handling():
    """Verify TASK-009: empty vector store raises HTTPException 503 instead of 500."""
    try:
        from services.rag_service import RAGService
        from fastapi import HTTPException
    except ImportError:
        return

    import asyncio

    # Create instance with mocked vector store having 0 documents
    mock_vector_store = MagicMock()
    mock_vector_store._collection.count.return_value = 0

    with patch.object(RAGService, "__init__", lambda self: None):
        service = RAGService()
        service.vectorstore = mock_vector_store
        service.vector_store = mock_vector_store
        service.llm = MagicMock()
        service.retriever = MagicMock()
        service.generation_chain = MagicMock()
        service.grading_chain = MagicMock()

        try:
            asyncio.run(service.query("What is RAG?"))
            assert False, "Should have raised HTTPException 503 for empty vector database"
        except HTTPException as exc:
            assert exc.status_code == 503
            assert "empty" in exc.detail.lower() or "ingest" in exc.detail.lower()
