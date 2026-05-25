# app/schemas/schemas.py

from pydantic import BaseModel

class ModerationRequest(BaseModel):
    text: str

class ModerationResponse(BaseModel):
    action: str
    classification: str
    reasoning: str
    timestamp: str