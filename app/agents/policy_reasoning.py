# app/agnets/policy_reasoning.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.core.config import settings
from openai import AzureOpenAI

class PolicyReasoningAgent:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=settings.OPENAI_API_KEY,
            api_version=settings.OPENAI_VERSION,
            azure_endpoint=settings.OPENAI_ENDPOINT
        )
        self.model = settings.OPENAI_MODEL

    def reason(self, classification: str, user_input: str, policies: list[dict]) -> str:
        system_prompt = (
            "You are a responsible AI policy analyst. "
            "Your job is to explain why a given message is classified as hate/toxic/offensive. "
            "Use real examples from the provided policies to justify your reasoning clearly and fairly. "
            "Cite specific policy names or clauses where relevant."
        )

        policy_text = "\n\n".join([f"{p['name']}:\n{p['snippet']}" for p in policies])
        user_prompt = (
            f"User message: \"{user_input}\"\n"
            f"Classification: {classification}\n\n"
            f"Relevant policy snippets:\n{policy_text}\n\n"
            f"Explain the reasoning for this classification in detail:"
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"❌ Reasoning generation failed: {str(e)}"
