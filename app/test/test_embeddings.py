# app/test/test_embeddings.py

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import faiss
import json
from app.services.embedding_service import VectorStore

if __name__ == "__main__":
    # Initialize vector store
    vs = VectorStore()
    
    # Load pre-built index
    vs.index = faiss.read_index("policy_index.faiss")
    with open("policy_metadata.json", "r") as f:
        vs.documents = json.load(f)
    
    # Test search
    query = "hate speech policy"
    results = vs.search(query, k=5)
    
    print(f"Search results for '{query}':")
    if isinstance(results[0], tuple):  # If returns (doc, score) tuples
        for i, (doc, score) in enumerate(results, 1):
            print(f"{i}. {doc['source']} (score: {score:.3f})")
    else:  # If returns just documents
        for i, doc in enumerate(results, 1):
            print(f"{i}. {doc['source']}")