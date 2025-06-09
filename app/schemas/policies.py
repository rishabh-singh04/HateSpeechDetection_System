#  app/schemas/policies.py

from pydantic import BaseModel
from typing import Optional, List

class PolicyDocumentResponse(BaseModel):
    id: int
    name: str
    content: str
    score: Optional[float] = None  # For search results
    
    class Config:
        orm_mode = True  # Allows conversion from ORM model

class PolicySearchResponse(BaseModel):
    results: List[PolicyDocumentResponse]
    search_time_ms: Optional[float] = None
