
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# import pytest
# from app.agents.hate_speech_detection import HateSpeechDetectionAgent

# @pytest.fixture
# def detector():
#     return HateSpeechDetectionAgent()

# def test_classify_hate(detector):
#     result = detector.classify("I hate all people from X country.")
#     assert result["classification"] in ["Hate", "Toxic", "Offensive", "Neutral"]
#     assert 0 <= result["confidence"] <= 1

# def test_classify_neutral(detector):
#     result = detector.classify("Hello, how are you?")
#     assert result["classification"] == "Neutral"

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