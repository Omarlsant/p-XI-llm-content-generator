from pydantic import BaseModel
from typing import List, Dict, Optional

class ContentGenerationRequest(BaseModel):
    topic: str
    platforms: List[str]
    model: Optional[str] = 'llama3'
    company_info: Optional[str] = None
    language: Optional[str] = 'English'

class ContentGenerationResponse(BaseModel):
    generated_content: Dict[str, str]
    image_url: Optional[str] = None
    image_alt: Optional[str] = None