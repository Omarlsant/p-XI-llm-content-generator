from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal

# Allowed domains and enums
SupportedLanguage = Literal["English", "Spanish", "French", "German", "Japanese", "Italian"]
SupportedPlatform = Literal["blog", "X", "instagram"]
SupportedModel = Literal["llama3"]

# --- Content Agent Schemas ---
class ContentGenerationRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Topic to generate content about (1-500 characters)"
    )
    platforms: List[SupportedPlatform] = Field(
        default_factory=lambda: ["blog"],
        min_length=1,
        description="Target platforms (at least one of 'blog', 'X', 'instagram')"
    )
    model: SupportedModel = Field(
        default="llama3",
        description="AI model to use (supported: 'llama3')"
    )
    company_info: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional company/brand context (max 1000 characters)"
    )
    language: SupportedLanguage = Field(
        default="English",
        description="Content language"
    )
    use_news_search: bool = Field(
        default=False,
        description="Enable real-time web search for news"
    )

class ContentGenerationResponse(BaseModel):
    generated_content: Dict[str, str] = Field(default_factory=dict)
    errors: Dict[str, str] = Field(default_factory=dict)
    image_url: Optional[str] = None
    image_alt: Optional[str] = None
    success: bool = True

# --- Query Agent Schemas ---
class QueryAgentRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User query or command (1-1000 characters)"
    )
    language: SupportedLanguage = Field(
        default="English",
        description="Target language"
    )
    use_search: bool = Field(
        default=False,
        description="Enable web search"
    )
    company_info: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional company background context (max 1000 characters)"
    )

class QueryAgentResponse(BaseModel):
    answer: str

# --- RAG Schemas ---
class RAGQueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Scientific or technical query (1-1000 characters)"
    )

class RAGQueryResponse(BaseModel):
    answer: str

# --- System & Operational Schemas ---
class RootResponse(BaseModel):
    message: str

class HealthResponse(BaseModel):
    status: str = "ok"
    message: Optional[str] = None

