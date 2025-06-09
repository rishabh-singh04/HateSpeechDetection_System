# app/agents/hate_speech_detection.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.core.config import settings
from app.core.exceptions import ClassificationError
from openai import AzureOpenAI
from app.utils.constants import HATE_SPEECH_SYSTEM_PROMPT
from app.schemas.classification_result import HateSpeechClassificationResult

class HateSpeechDetectionAgent:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=settings.OPENAI_API_KEY,
            api_version=settings.OPENAI_VERSION,
            azure_endpoint=settings.OPENAI_ENDPOINT
        )
        self.model = settings.OPENAI_MODEL
        self.system_prompt = HATE_SPEECH_SYSTEM_PROMPT


    def classify(self, text: str) -> dict:
        user_prompt = f"Classify the following message:\n\n{text}"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )

            message = response.choices[0].message.content

            # Example response lines:
            # Classification: Hate
            # Confidence: 0.92
            # Explanation: The message contains explicit hate speech against a group.

            lines = [line for line in message.strip().split("\n") if ":" in line]
            if len(lines) < 3:
                raise ValueError("LLM response does not contain 3 parseable lines")

            classification = lines[0].split(":", 1)[1].strip()
            # confidence = float(lines[1].split(":", 1)[1].strip())
            confidence_str = lines[1].split(":", 1)[1].strip()
            confidence = float(confidence_str.strip("[]").strip())  # Handles both "0.92" and "[0.92]"
            explanation = lines[2].split(":", 1)[1].strip()

            return HateSpeechClassificationResult(
                classification=classification,
                confidence=confidence,
                explanation=explanation
            ).dict()

        except Exception as e:
            raise ClassificationError(str(e))
        