

# tests/test_hybrid_retriever.py


# import pytest
# from sqlalchemy.orm import Session
# from app.db.base import Base, get_db
# from app.agents.hybrid_retriever import HybridRetrieverAgent



# @pytest.fixture
# def retriever(db: Session = get_db()):
#     retriever = HybridRetrieverAgent()
#     retriever.load_documents(db)
#     return retriever

# def test_search(retriever):
#     results = retriever.search("hate speech", k=2)
#     assert len(results) == 2
#     assert "name" in results[0]
#     assert "snippet" in results[0]


# app/test/test_retriever.py

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import json
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.agents.hybrid_retriever import HybridRetrieverAgent
from app.db.models.policy import PolicyDocument

# Setup in-memory test database
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
db = Session()

# Create tables
from app.db.base import Base
Base.metadata.create_all(engine)

def test_hybrid_retriever():
    # Add test data
    test_doc = PolicyDocument(
        name="Test Policy",
        content="No hate speech allowed",
        embedding=json.dumps([0.1, 0.2, 0.3])  # Simple test embedding
    )
    db.add(test_doc)
    db.commit()

    # Test the retriever
    agent = HybridRetrieverAgent()
    agent.load_documents(db)
    
    results = agent.search(db, "hate speech", k=1)
    assert len(results) == 1
    assert results[0]["name"] == "Test Policy"
    assert isinstance(results[0]["score"], float)
    
    print("✅ HybridRetriever tests passed!")

if __name__ == "__main__":
    test_hybrid_retriever()