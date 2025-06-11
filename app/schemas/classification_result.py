# app/schemas/classification_result.py

from pydantic import BaseModel

class HateSpeechClassificationResult(BaseModel):
    classification: str  # "Hate", "Toxic", etc.
    confidence: float   # 0.0 to 1.0 (e.g., 0.95 for 95% confidence)
    explanation: str    # Reasoning from LLM