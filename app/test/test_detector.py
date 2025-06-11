# app/test/test_detector.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.agents.hate_speech_detection import HateSpeechDetectionAgent

# Corrected Mock OpenAI response
class MockOpenAI:
    class chat:
        class completions:
            @staticmethod
            def create(*args, **kwargs):
                class Choice:
                    class message:
                        content = "Classification: Hate\nConfidence: 0.95\nExplanation: Test"
                return type("Response", (), {"choices": [Choice()]})

def test_hate_speech_detection():
    agent = HateSpeechDetectionAgent()
    # Inject the mock client with correct structure
    agent.client = type("MockClient", (), {"chat": MockOpenAI.chat})()
    
    result = agent.classify("Test input")
    assert "classification" in result
    assert result["classification"] == "Hate"
    assert "confidence" in result
    assert 0 <= result["confidence"] <= 1
    assert "explanation" in result
    
    print("✅ HateSpeechDetectionAgent tests passed!")

if __name__ == "__main__":
    test_hate_speech_detection()