# app/agents/action_recommender.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.utils.constants import ACTION_MAP
from datetime import datetime

class ActionRecommenderAgent:
    def __init__(self):
        self.action_map = ACTION_MAP
        
        
    def recommend(self, classification: str, reasoning: str, user_id: str = None) -> dict:
        action = self.action_map.get(classification, "review")
        
        return {
            "action": action,
            "classification": classification,
            "reasoning": reasoning,
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
        }
