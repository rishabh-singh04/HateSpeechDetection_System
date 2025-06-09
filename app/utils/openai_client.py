# app/utils/openai_client.py

from openai import AzureOpenAI
import os

class OpenAIClient:
    def __init__(self):
        self.client = AzureOpenAI(
            api_version="2023-12-01-preview",
            azure_endpoint=os.getenv("OPENAI_ENDPOINT"),  # e.g., "https://chat.<company>.com"
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def ask(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful content moderation assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=200
        )
        return response.choices[0].message.content
    
    @property
    def chat(self):
        return self.client.chat