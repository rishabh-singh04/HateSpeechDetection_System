from openai import AzureOpenAI
import os 
import dotenv

client = AzureOpenAI(
    api_version="2023-12-01-preview",
    azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
    api_key=os.getenv("OPENAI_API_KEY"),
)
 
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": "Hello!",
        }
    ]
)

print(response.choices[0].message.content)