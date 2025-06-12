# app/schemas/moderation.py

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, Dict, Any, Union
import json
import logging

logger = logging.getLogger(__name__)

class ModerationRequest(BaseModel):
    text: str

class ModerationResponse(BaseModel):
    action: str
    classification: str
    reasoning: str
    timestamp: str
    confidence: Optional[float] = Field(None, ge=0, le=1)

    @validator('reasoning', pre=True)
    def validate_reasoning(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)  # Try to parse JSON string
            except json.JSONDecodeError:
                return v  # Return as plain string
        return v

class ModerationResult(BaseModel):
    text: str
    result: str
    action: str
    reason: str
    full_reason: str  # Store as string for CSV compatibility
    snippet: str
    timestamp: datetime

    @classmethod
    def from_response(cls, text: str, response: ModerationResponse):
        # Handle reasoning conversion
        if isinstance(response.reasoning, dict):
            reason = response.reasoning.get("summary", str(response.reasoning)[:100])
            full_reason = json.dumps(response.reasoning, ensure_ascii=False)
        else:
            reason = str(response.reasoning)[:100]
            full_reason = str(response.reasoning)

        return cls(
            text=text,
            result=response.classification,
            action=response.action,
            reason=reason,
            full_reason=full_reason,
            snippet=text[:100] + "..." if len(text) > 100 else text,
            timestamp=datetime.fromisoformat(response.timestamp)
        )



class ExportRequest(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    filename_prefix: Optional[str] = "moderation"