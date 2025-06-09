# app/services/policy_service.py

from typing import List
from sqlalchemy.orm import Session
from app.db.models.policy import PolicyDocument
from app.agents.hybrid_retriever import HybridRetrieverAgent

class PolicyService:
    def __init__(self):
        self.retriever = HybridRetrieverAgent()

    async def search_policies(self, query: str, limit: int, db: Session) -> List[PolicyDocument]:
        """
        Search policy documents using hybrid retrieval
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            db: Database session
            
        Returns:
            List of matching PolicyDocument objects with scores
            
        Raises:
            Exception: If search fails
        """
        try:
            # Load documents if not already loaded
            if not self.retriever.documents:
                self.retriever.load_documents(db)
            
            # Perform semantic search
            results = self.retriever.search(query, k=limit)
            
            # Get full document objects from DB
            policy_ids = [result['id'] for result in results]
            policies = db.query(PolicyDocument).filter(
                PolicyDocument.id.in_(policy_ids)
            ).all()
            
            # Combine with scores
            policy_map = {p.id: p for p in policies}
            for result in results:
                if policy := policy_map.get(result['id']):
                    policy.score = result['score']  # Use the property
            
            return sorted(policies, key=lambda p: p.score or 0, reverse=True)
            
        except Exception as e:
            raise Exception(f"Policy search failed: {str(e)}")

# Singleton instance
policy_service = PolicyService()

# Public interface function
async def search_policies(query: str, limit: int, db: Session) -> List[PolicyDocument]:
    """Public interface for policy search"""
    return await policy_service.search_policies(query, limit, db)


