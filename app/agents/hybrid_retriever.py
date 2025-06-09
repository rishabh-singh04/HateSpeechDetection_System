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

# class HybridRetrieverAgent:
#     def __init__(self):
#         self._doc_ids: List[int] = []
#         self._doc_texts: List[str] = []
#         self._embeddings = np.array([])  # Initialize empty array

#     def load_documents(self, db: Session) -> None:
#         """Preload policy documents and their embeddings."""
#         docs = db.query(PolicyDocument).filter(PolicyDocument.embedding.isnot(None)).all()
#         self._doc_ids = [doc.id for doc in docs]
#         self._doc_texts = [doc.content for doc in docs]
#         self._embeddings = np.array([json.loads(doc.embedding) for doc in docs])

#     def search(self, db: Session, query: str, k: int = 3) -> List[Dict]:
#         """Perform semantic search on preloaded embeddings and return top-k documents."""
#         if len(self._embeddings) == 0:
#             raise ValueError("Embeddings not loaded. Call `load_documents()` first.")

#         query_embedding = np.array(get_embedding(query))
#         similarities = self._embeddings @ query_embedding

#         top_k_indices = np.argsort(similarities)[::-1][:k]
#         top_doc_ids = [self._doc_ids[idx] for idx in top_k_indices]
#         top_scores = [float(similarities[idx]) for idx in top_k_indices]

#         docs = db.query(PolicyDocument).filter(PolicyDocument.id.in_(top_doc_ids)).all()
#         id_to_doc = {doc.id: doc for doc in docs}

#         return [
#             {
#                 "id": doc.id,
#                 "name": doc.name,
#                 "score": score,
#                 "snippet": doc.content[:300]
#             }
#             for doc, score in zip([id_to_doc[i] for i in top_doc_ids], top_scores)
#         ]



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
        
        # # Generate embeddings on-the-fly
        # embeddings = self.model.encode([doc[2] for doc in self.documents])
        # self.index.add(embeddings)
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