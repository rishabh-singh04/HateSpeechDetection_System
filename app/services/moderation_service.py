# app/services/moderation_service.py

from app.agents.hate_speech_detection import HateSpeechDetectionAgent
from app.agents.hybrid_retriever import HybridRetrieverAgent
from app.agents.policy_reasoning import PolicyReasoningAgent
from app.agents.action_recommender import ActionRecommenderAgent
from app.schemas.moderation import ModerationResponse
from datetime import datetime

def moderate_content(text: str, db) -> ModerationResponse:
    # Step 1: Classify
    detector = HateSpeechDetectionAgent()
    classification = detector.classify(text)
    
    # Step 2: Retrieve policies
    retriever = HybridRetrieverAgent()
    retriever.load_documents(db)
    policies = retriever.search(text)
    
    # Step 3: Generate reasoning
    reasoner = PolicyReasoningAgent()
    reasoning = reasoner.reason(classification["classification"], text, policies)
    
    # Step 4: Recommend action
    recommender = ActionRecommenderAgent()
    recommendation = recommender.recommend(classification["classification"], reasoning)
    
    return ModerationResponse(
        action=recommendation["action"],
        classification=classification["classification"],
        reasoning=reasoning,
        timestamp=datetime.utcnow().isoformat(),
        confidence=classification.get("confidence")
    )

