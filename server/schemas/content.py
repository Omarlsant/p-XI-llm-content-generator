from pydantic import BaseModel
from typing import List, Dict, Optional

class ContentGenerationRequest(BaseModel):
    topic: str
    platforms: List[str]
    model: Optional[str] = 'llama3'
    company_info: Optional[str] = None

class ContentGenerationResponse(BaseModel):
    generated_content: Dict[str, str]