# tests/test_policy_reasoning.py

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.agents.policy_reasoning import PolicyReasoningAgent

# Mock OpenAI response
class MockOpenAI:
    class ChatCompletion:
        @staticmethod
        def create(*args, **kwargs):
            class Choice:
                message = type("Message", (), {"content": "This violates Policy X."})
            return type("Response", (), {"choices": [Choice()]})

def test_policy_reasoning():
    agent = PolicyReasoningAgent()
    agent.client = type("MockClient", (), {"chat": MockOpenAI.ChatCompletion})()  # Inject mock
    
    policies = [{"name": "Policy X", "snippet": "No hate speech."}]
    reasoning = agent.reason("Hate", "Test input", policies)
    assert isinstance(reasoning, str)
    assert len(reasoning) > 0
    
    print("✅ PolicyReasoningAgent tests passed!")

if __name__ == "__main__":
    test_policy_reasoning()