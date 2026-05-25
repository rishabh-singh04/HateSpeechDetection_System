# app/services/policy_service.py

from typing import List, Dict
from pathlib import Path
import json
import logging
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.agents.hybrid_retriever import HybridRetrieverAgent
from app.schemas.policies import PolicySearchResult, PolicySearchResponse
from app.db.models.policy import PolicyDocument

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class PolicyService:
    def __init__(self, db_session: Optional[Session] = None):
        self.retriever = HybridRetrieverAgent()
        self.db = db_session or get_db() # Initialize database session
        self.policy_content = {}  # Cache for full policy content
        self._load_policy_content()  # Load full policy content for snippets
    
    def _load_policy_content(self):
        """Load full policy content from metadata for complete snippets"""
        self.policy_content = {}
        metadata_path = Path("embeddings/policy_metadata.json")
        
        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
                # Assuming policy documents are stored in app/data/policy_docs/
                for item in metadata:
                    policy_path = Path(f"app/data/policy_docs/{item['source']}")
                    if policy_path.exists():
                        with open(policy_path, 'r', encoding='utf-8') as policy_file:
                            self.policy_content[item['source']] = policy_file.read()
        except Exception as e:
            logger.error(f"Failed to load policy content: {str(e)}")
            self.policy_content = {}

    async def search_policies(self, query: str, limit: int = 5, threshold: float = 0.3, db: Optional[Session] = None) -> PolicySearchResponse:
        """
        Search policy documents using FAISS index and return complete policy snippets
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            threshold: Minimum similarity score threshold (0-1)
            db: Optional database session for enhanced results
            
        Returns:
            PolicySearchResponse with complete policy snippets
        """
        try:
            # Use the instance db if provided, otherwise use the method parameter
            db_session = self.db or db
            
            # Load FAISS index if not already loaded
            if not self.retriever.index:
                faiss_path = Path("embeddings/policy_index.faiss")
                metadata_path = Path("embeddings/policy_metadata.json")
                self.retriever.load_index(faiss_path, metadata_path)
            
            # Perform semantic search
            results = self.retriever.search(query, k=limit, threshold=threshold)
            
            # Enhance results with complete policy content
            enhanced_results = []
            for result in results:
                # First try to get content from pre-loaded files
                full_content = self.policy_content.get(result['source'], "")
                
                # Fallback to database if available and content not found
                if not full_content and db_session:
                    db_policy = db_session.query(PolicyDocument).filter(
                        PolicyDocument.name.ilike(f"%{result['name']}%")
                    ).first()
                    if db_policy:
                        full_content = db_policy.content
                        # Cache for future use
                        self.policy_content[result['source']] = full_content
                
                enhanced_results.append(
                    PolicySearchResult(
                        id=result['id'],
                        name=result['name'],
                        snippet=self._get_complete_snippet(full_content, query),
                        score=result['score'],
                        source=result['source']
                    )
                )
            
            return PolicySearchResponse(
                results=enhanced_results,
                count=len(enhanced_results),
                search_time_ms=0  # Will be set by the API endpoint
            )
            
        except Exception as e:
            logger.error(f"Policy search failed: {str(e)}")
            return PolicySearchResponse(results=[], count=0, search_time_ms=0)

    def _get_complete_snippet(self, content: str, query: str) -> str:
        """
        Extract a complete, coherent snippet around the most relevant part of the policy
        
        Args:
            content: Full policy content
            query: Original search query
            
        Returns:
            Complete paragraph containing the most relevant information
        """
        if not content:
            return "No content available"
            
        # Split into paragraphs (assuming policies use double newlines)
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        if not paragraphs:
            return content[:300] + "..." if len(content) > 300 else content
            
        # Find most relevant paragraph
        query_words = set(query.lower().split())
        best_paragraph = ""
        best_score = 0
        
        for para in paragraphs:
            para_words = set(para.lower().split())
            score = len(query_words.intersection(para_words))
            if score > best_score:
                best_score = score
                best_paragraph = para
                
        return best_paragraph or paragraphs[0]
    
    async def sync_with_db(self):
        """Sync FAISS index content with database"""
        if not self.db:
            return
            
        # Get all policies from DB
        db_policies = self.db.query(PolicyDocument).all()
        
        # Update metadata mapping
        for policy in db_policies:
            if policy.name not in self.policy_content:
                self.policy_content[policy.name] = policy.content

        # Sync FAISS index with updated policy content
        self.retriever.index.reset()
        for name, content in self.policy_content.items():
            self.retriever.index.add_document(name, content)

# Singleton instance
policy_service = PolicyService()