from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# --- Content Agent Schemas ---
class ContentGenerationRequest(BaseModel):
    topic: str
    platforms: List[str] = Field(default_factory=lambda: ["blog"])
    model: str = 'llama3'
    company_info: Optional[str] = None
    language: str = 'English'
    use_news_search: bool = False

class ContentGenerationResponse(BaseModel):
    generated_content: Dict[str, str] = Field(default_factory=dict)
    errors: Dict[str, str] = Field(default_factory=dict)
    image_url: Optional[str] = None
    image_alt: Optional[str] = None
    success: bool = True

class QueryAgentRequest(BaseModel):
    question: str
    language: str
    use_search: bool
    company_info: Optional[str] = None