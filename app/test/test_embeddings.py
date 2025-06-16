# app/test/test_embeddings.py

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import faiss
import json
from app.services.embedding_service import VectorStore

def test_embeddings():
    # Initialize vector store
    vs = VectorStore()
    
    # Mock index and documents
    vs.index = faiss.IndexFlatL2(384)  # Mock index
    vs.documents = [{"source": "test", "content": "test content"}]
    
    # Test search
    results = vs.search("test query", k=1)
    assert len(results) > 0
    assert "source" in results[0]