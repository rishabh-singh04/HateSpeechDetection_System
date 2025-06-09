# app/test/test_retriever_logger.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.models.policy import PolicyDocument
from app.services.query_logger import QueryLog, QueryLogger
from app.agents.hybrid_retriever import HybridRetrieverAgent

def test_hybrid_retriever_and_logger():
    # Setup in-memory database
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    db = Session()
    Base.metadata.create_all(engine)
    
    # Add test data
    test_policy = PolicyDocument(
        name="Test Policy",
        content="Hate speech is prohibited. Respect all users."
    )
    db.add(test_policy)
    db.commit()

    # Test HybridRetriever
    retriever = HybridRetrieverAgent()
    retriever.load_documents(db)
    
    # Test with a matching query
    results = retriever.search("hate speech")
    assert len(results) == 1
    assert results[0]["name"] == "Test Policy"
    assert "prohibited" in results[0]["snippet"]
    assert 0.5 <= results[0]["score"] <= 1.0  # Score should be reasonably high
    
    # Test with non-matching query
    empty_results = retriever.search("unrelated topic")
    assert len(empty_results) == 1  # Still returns the only document but with low score
    assert empty_results[0]["score"] < 0.3
    
    print("✅ HybridRetriever test passed!")

    # Test QueryLogger
    logger = QueryLogger(db)
    logger.log_query("test query", len(results))
    
    log_entry = db.query(QueryLog).first()
    assert log_entry.query == "test query"
    assert log_entry.results_count == 1
    print("✅ QueryLogger test passed!")

if __name__ == "__main__":
    test_hybrid_retriever_and_logger()