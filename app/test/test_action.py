# app/test/test_action.py
# import pytest
# from app.agents.action_recommender import ActionRecommenderAgent

# @pytest.fixture
# def recommender():
#     return ActionRecommenderAgent()

# def test_recommend_hate(recommender):
#     action = recommender.recommend("Hate", "This violates policies.")
#     assert action["action"] == "Remove"

# def test_recommend_neutral(recommender):
#     action = recommender.recommend("Neutral", "No issues found.")
#     assert action["action"] == "Allow"

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.agents.action_recommender import ActionRecommenderAgent

def test_action_recommender():
    agent = ActionRecommenderAgent()
    
    # Test known classifications
    assert agent.recommend("Hate", "Reason")["action"] == "Remove"
    assert agent.recommend("Toxic", "Reason")["action"] == "Warn"
    assert agent.recommend("Neutral", "Reason")["action"] == "Allow"
    
    # Test default for unknown classification
    assert agent.recommend("Unknown", "Reason")["action"] == "Review"
    
    print("✅ ActionRecommenderAgent tests passed!")

if __name__ == "__main__":
    test_action_recommender()