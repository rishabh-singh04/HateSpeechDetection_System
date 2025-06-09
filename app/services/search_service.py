# app/services/search_service.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy.orm import Session
from app.agents.hybrid_retriever import HybridRetrieverAgent    
from app.services.query_logger import QueryLogger, QueryLog
import logging

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self, db: Session):
        self.retriever = HybridRetrieverAgent()
        self.logger = QueryLogger(db)
        self.retriever.load_documents(db)

    def search(self, query: str):
        results = self.retriever.search(query)
        self.logger.log_query(query, len(results))
        
        # Add query expansion logic here
        if len(results) < 3:  # If few results
            expanded_queries = self._expand_query(query)
            for eq in expanded_queries:
                results += self.retriever.search(eq)
        
        return sorted(results, key=lambda x: x['score'], reverse=True)[:5]

    def _expand_query(self, query: str):
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        # Get historical queries
        historical_queries = [log.query for log in self.db.query(QueryLog.query).all()]
        
        if not historical_queries:
            return [query]
            
        # Find similar historical queries
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(historical_queries + [query])
        similarities = (X[-1] @ X[:-1].T).toarray()[0]
        
        # Return top 2 related queries
        return [
            historical_queries[i] 
            for i in similarities.argsort()[-2:] 
            if similarities[i] > 0.5
        ]