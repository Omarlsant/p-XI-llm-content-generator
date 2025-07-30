from pydantic import BaseModel
from typing import List, Dict, Optional

# --- Content Agent Schemas ---
class ContentGenerationRequest(BaseModel):
    topic: str
    platforms: List[str]
    model: str = 'llama3'
    company_info: Optional[str] = None
    language: str = 'English'
    use_news_search: bool = False

class ContentGenerationResponse(BaseModel):
    generated_content: Dict[str, str]
    image_url: Optional[str] = None
    image_alt: Optional[str] = None

class QueryAgentRequest(BaseModel):
    question: str
    language: str
    use_search: bool
    company_info: Optional[str] = None