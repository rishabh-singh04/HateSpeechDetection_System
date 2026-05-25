# app/agents/policy_reasoning.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.core.config import settings
from openai import AzureOpenAI
from app.utils.constants import ACTION_MAP  # Import the action map

class PolicyReasoningAgent:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=settings.OPENAI_API_KEY,
            api_version=settings.OPENAI_VERSION,
            azure_endpoint=settings.OPENAI_ENDPOINT
        )
        self.model = settings.OPENAI_MODEL
        self.action_map = ACTION_MAP  # Store the action map

    def reason(self, classification: str, user_input: str, policies: list[dict]) -> str:
        # Use the action map to get the recommended action
        recommended_action = self.action_map.get(classification, self.action_map["default"])
        
        system_prompt = f"""
        You are a responsible AI policy analyst. Your task is to:
        1. Reference specific policy clauses that apply
        2. Explain the recommended action: {recommended_action}
        3. Justify how the user input relates to each policy
        
        Available actions and their meanings:
        {self._format_action_map()}
        """

        policy_text = "\n\n".join([
            f"Policy: {p['name']}\nRelevance Score: {p['score']:.2f}\nContent: {p['snippet']}" 
            for p in policies
        ])

        user_prompt = f"""
        Classification: {classification}
        Recommended Action: {recommended_action}
        User Input: "{user_input}"
        
        Relevant Policies:
        {policy_text}
        
        Provide detailed reasoning:
        1. Which specific policy clauses apply
        2. Why the recommended action is appropriate
        3. How the content violates or aligns with each policy
        """

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

    def _format_action_map(self) -> str:
        """Format the action map for inclusion in the system prompt"""
        return "\n".join(
            f"- {classification}: {action}" 
            for classification, action in self.action_map.items()
        )