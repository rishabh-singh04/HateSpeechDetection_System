#  app/agents/hybrid_retriever.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.db.models.policy import PolicyDocument
import json
import numpy as np
from app.services.embedding_service import get_embedding

class HybridRetrieverAgent:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        # self.index = faiss.IndexFlatL2(384)  # Dimension matching model
        self.documents = []  # Stores (id, name, content)
        self.embeddings = None
        if os.path.exists("policy_index.faiss"):
            self.load_index()

    def load_documents(self, db: Session):
        """Cache documents in memory, build FAISS index"""
        docs = db.query(PolicyDocument).all()
        self.documents = [(doc.id, doc.name, doc.content) for doc in docs]
        
        if self.documents:
            self.embeddings = self.model.encode([doc[2] for doc in self.documents])
            # Normalize embeddings for cosine similarity
            self.embeddings = self.embeddings / np.linalg.norm(self.embeddings, axis=1, keepdims=True)  # Normalize embeddings

    def search(self, query: str, k: int = 3):
        """Simple cosine similarity search"""
        if not self.documents or self.embeddings is None or len(self.embeddings) == 0:
            return []

        # Encode and normalize query
        query_embedding = self.model.encode(query)
        query_embedding = query_embedding / np.linalg.norm(query_embedding)
        
        # Calculate cosine similarities
        scores = np.dot(self.embeddings, query_embedding)
        top_k_indices = np.argsort(scores)[-k:][::-1] # Get top k indices
        
        return [{
            'id': self.documents[i][0],  # Ensure this matches your DB IDs
            'name': self.documents[i][1],
            'snippet': self.documents[i][2][:300],
            'score': float(scores[i])
        } for i in top_k_indices]

    
    def save_index(self, path: str = "policy_index.faiss"):
        faiss.write_index(self.index, path)

    def load_index(self, path: str = "policy_index.faiss"):
        self.index = faiss.read_index(path)