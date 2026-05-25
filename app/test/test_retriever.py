# tests/test_retriever.py

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# tests/test_hybrid_retriever.py
import json
from app.agents.hybrid_retriever import HybridRetrieverAgent
from app.db.models.policy import PolicyDocument

def test_hybrid_retriever(db_session):
    # Add test data
    test_doc = PolicyDocument(
        name="Test Policy",
        content="No hate speech allowed"
    )
    db_session.add(test_doc)
    db_session.commit()

    # Test the retriever
    from app.agents.hybrid_retriever import HybridRetrieverAgent
    agent = HybridRetrieverAgent()
    agent.load_documents(db_session)
    
    results = agent.search("hate speech", k=1)
    assert len(results) == 1
    assert results[0]["name"] == "Test Policy"
    assert isinstance(results[0]["score"], float)