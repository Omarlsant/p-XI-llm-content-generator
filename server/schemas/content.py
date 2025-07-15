from pydantic import BaseModel
from typing import List, Dict

# This file defines the schemas for content generation requests and responses.
class ContentGenerationRequest(BaseModel):
    topic: str
    platforms: List[str]

class ContentGenerationResponse(BaseModel):
    generated_content: Dict[str, str]