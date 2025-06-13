# app/db/seed_embeddings.py

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.services.embedding_service import VectorStore

if __name__ == "__main__":
    vs = VectorStore()
    vs.create_embeddings()
    print("FAISS index created successfully!")