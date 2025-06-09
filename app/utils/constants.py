# app/utils/constants.py

ACTION_MAP = {
    "Hate": "Remove",
    "Toxic": "Warn",
    "Offensive": "Flag",
    "Neutral": "Allow",
    "Ambiguous": "Review",
    "default": "Review",
    "Unknown": "Review"
}

HATE_SPEECH_SYSTEM_PROMPT = """
You are a hate speech classifier. Analyze the text and respond with:
- Classification: Hate/Toxic/Offensive/Neutral/Ambiguous
- Confidence: [0-1]
- Explanation: Brief reasoning.
"""