#  app/schemas/policies.py

from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class PolicyDocumentResponse(BaseModel):
    id: int
    name: str
    content: str
    score: Optional[float] = None  # For search results
    
    class Config:
        model_config = ConfigDict(from_attributes=True)

class PolicySearchResponse(BaseModel):
    results: List[PolicyDocumentResponse]
    search_time_ms: Optional[float] = None
