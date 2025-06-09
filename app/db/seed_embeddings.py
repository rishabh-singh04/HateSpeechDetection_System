# app/db/seed_embeddings.py

from app.services.embedding_service import VectorStore

if __name__ == "__main__":
    vs = VectorStore()
    vs.create_embeddings()
    print("FAISS index created successfully!")