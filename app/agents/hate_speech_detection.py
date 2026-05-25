# app/agents/hate_speech_detection.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import json
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

    """ 
    Classifies a given text message for hate speech.
    Returns a dictionary with classification, confidence, and explanation.
            input → LLM → error handler → recommendation
    """
    def classify(self, text: str, policies: list = None) -> dict:
        user_prompt = f"""
        Analyze this message for hate speech considering these policies:
        Policies: {json.dumps(policies, indent=2) if policies else 'No relevant policies'}
        
        Message to classify: {text}
        
        Provide your analysis in this exact format:
        Classification: [hate/toxic/offensive/neutral]
        Confidence: [0-1]
        Explanation: [your reasoning]
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            # Extract the message content from the response
            message = response.choices[0].message.content

            # Example response lines:
            # Classification: Hate
            # Confidence: 0.92
            # Explanation: The message contains explicit hate speech against a group.

            # Split the message into lines and parse the expected format
            lines = [line for line in message.strip().split("\n") if ":" in line]
            if len(lines) < 3:
                raise ValueError("LLM response does not contain 3 parseable lines")

            classification = lines[0].split(":", 1)[1].strip()
            # confidence = float(lines[1].split(":", 1)[1].strip())
            confidence_str = lines[1].split(":", 1)[1].strip()
            confidence = float(confidence_str.strip("[]").strip())  # Handles both "0.92" and "[0.92]"
            explanation = lines[2].split(":", 1)[1].strip()

            # Creates a Pydantic model and returns it as a Python dict.
            return HateSpeechClassificationResult(
                classification=classification,
                confidence=confidence,
                explanation=explanation
            ).dict()

        except Exception as e:
            raise ClassificationError(str(e))
    
    def classify_with_policies(self, text: str, policy_context: str) -> dict:
        prompt = f"""
        Analyze this message considering these policies:
        {policy_context}
        
        Message to classify: {text}
        
        Provide analysis in this JSON format:
        {{
            "classification": "[hate/toxic/offensive/neutral]",
            "confidence": 0-1,
            "action": "[block/review/allow]",
            "policy_references": [
                {{
                    "policy": "policy_name",
                    "section": "specific section violated",
                    "reason": "how it violates"
                }}
            ],
            "reasoning": "reasoning based on policies"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error in classify_with_policies: {e}")
            return {
                "classification": "error",
                "confidence": 0.0,
                "action": "block",
                "policy_references": [],
                "reasoning": f"Classification failed: {str(e)}"
            }
