# #  app/schemas/policies.py

# from pydantic import BaseModel, ConfigDict
# from typing import Optional, List

# class PolicyDocumentResponse(BaseModel):
#     id: int
#     name: str
#     content: str
#     score: float  # For search results
#     source: Optional[str] = None  # For source information
    
#     class Config:
#         model_config = ConfigDict(from_attributes=True)

# class PolicySearchResponse(BaseModel):
#     results: List[PolicyDocumentResponse]
#     search_time_ms: float
#     count: int

from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class PolicySearchResult(BaseModel):
    id: int
    name: str
    snippet: str
    score: float
    source: Optional[str] = None

class PolicySearchResponse(BaseModel):
    results: List[PolicySearchResult]
    search_time_ms: float
    count: int

class PolicyDocumentResponse(BaseModel):
    id: int
    name: str
    content: str
    score: Optional[float] = None
    source: Optional[str] = None
    
    class Config:
        model_config = ConfigDict(from_attributes = True)