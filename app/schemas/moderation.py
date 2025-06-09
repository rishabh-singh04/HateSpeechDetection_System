# app/schemas/moderation.py

from pydantic import BaseModel
from typing import Optional

class ModerationRequest(BaseModel):
    text: str

class ModerationResponse(BaseModel):
    action: str
    classification: str
    reasoning: str
    timestamp: str
    confidence: Optional[float] = None