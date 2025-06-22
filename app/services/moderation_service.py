# # app/services/moderation_service.py

# from datetime import datetime
# from pathlib import Path
# from app.agents.hate_speech_detection import HateSpeechDetectionAgent
# from app.agents.hybrid_retriever import HybridRetrieverAgent
# from app.agents.policy_reasoning import PolicyReasoningAgent
# from app.agents.action_recommender import ActionRecommenderAgent
# from app.schemas.moderation import ModerationResponse
# from app.utils.decorators import export_moderation_results
# import logging

# logger = logging.getLogger(__name__)

# @export_moderation_results
# def moderate_content(text: str, db) -> ModerationResponse:
#     try:
#         # Step 1: Classify
#         detector = HateSpeechDetectionAgent()
#         classification = detector.classify(text)
        
#         # Step 2: Retrieve policies
#         retriever = HybridRetrieverAgent()
#         faiss_path = Path("embeddings/policy_index.faiss")
#         metadata_path = Path("embeddings/policy_metadata.json")
#         retriever.load_index(faiss_path, metadata_path)  # Changed from load_documents()
        
#         policies = retriever.search(text)
        
#         # Step 3: Generate reasoning
#         reasoner = PolicyReasoningAgent()
#         reasoning = reasoner.reason(
#             classification["classification"], 
#             text, 
#             policies
#         )
        
#         # Step 4: Recommend action
#         recommender = ActionRecommenderAgent()
#         recommendation = recommender.recommend(
#             classification["classification"],
#             reasoning
#         )
        
#         return ModerationResponse(
#             action=recommendation["action"],
#             classification=classification["classification"],
#             reasoning=reasoning,
#             timestamp=datetime.utcnow().isoformat(),
#             confidence=classification.get("confidence", 0.5),
#             keywords=[p['name'] for p in policies[:3]] if policies else []
#         )
        
#     except Exception as e:
#         logger.error(f"Moderation failed: {str(e)}")
#         return ModerationResponse(
#             action="block",
#             classification="error",
#             reasoning=f"Moderation failed: {str(e)}",
#             timestamp=datetime.utcnow().isoformat(),
#             confidence=0.0
#         )


# app/services/moderation_service.py
from typing import List, Dict
from pathlib import Path
import json
from datetime import datetime
from app.agents.hate_speech_detection import HateSpeechDetectionAgent
from app.agents.hybrid_retriever import HybridRetrieverAgent
from app.agents.policy_reasoning import PolicyReasoningAgent
from app.schemas.moderation import ModerationResponse
import logging

logger = logging.getLogger(__name__)

def moderate_content(text: str, db=None) -> ModerationResponse:
    try:
        # 1. Retrieve relevant policies first
        retriever = HybridRetrieverAgent()
        retriever.load_index(
            Path("embeddings/policy_index.faiss"),
            Path("embeddings/policy_metadata.json")
        )
        policies = retriever.search(text, k=3, threshold=0.3)  # Get top 3 relevant policies
        
        # 2. Format policy context for LLM
        policy_context = "\n\n".join(
            f"POLICY: {p['name']}\nCONTENT:\n{p['content'][:2000]}..."  # Limit content length
            for p in policies
        ) if policies else "No relevant policies found"

        # 3. Get LLM analysis with policy context
        detector = HateSpeechDetectionAgent()
        classification = detector.classify_with_policies(text, policy_context)
        
        # 4. Generate reasoning
        reasoner = PolicyReasoningAgent()
        reasoning = reasoner.reason(
            classification["classification"],
            text,
            policies
        )

        return ModerationResponse(
            action=classification.get("action", "review"),
            classification=classification["classification"],
            reasoning=reasoning,
            timestamp=datetime.utcnow().isoformat(),
            confidence=classification.get("confidence", 0.8),
            keywords=[p['name'] for p in policies]
        )

    except Exception as e:
        logger.error(f"Moderation failed: {str(e)}")
        return ModerationResponse(
            action="block",
            classification="error",
            reasoning=f"System error: {str(e)}",
            timestamp=datetime.utcnow().isoformat(),
            confidence=0.0
        )