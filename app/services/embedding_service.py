# app/services/embedding_service.py



import pathlib
from dotenv import load_dotenv
load_dotenv(dotenv_path="/.env") 

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import json


def get_embedding(text: str, model_name: str = "all-MiniLM-L6-v2") -> list:
    """Standalone function to get embedding for a single text"""
    model = SentenceTransformer(model_name)
    return model.encode(text, convert_to_numpy=True).tolist()

class VectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []

    def create_embeddings(self, docs_dir="app/data/policy_docs"):
        """Process text files and create FAISS index"""
        texts = []
        metadatas = []
        
        for filename in os.listdir(docs_dir):
            if filename.endswith(".txt"):
                with open(os.path.join(docs_dir, filename), "r", encoding="utf-8") as f:
                    content = f.read()
                    texts.append(content)
                    metadatas.append({"source": filename})

        # Generate embeddings
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        
        # Create FAISS index
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.documents = metadatas
        
        # Save index
        faiss.write_index(self.index, "embeddings/policy_index.faiss")
        with open("embeddings/policy_metadata.json", "w") as f:
            json.dump(self.documents, f)

    def search(self, query, k=3):
        """Search similar documents"""
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, k)
        return [self.documents[i] for i in indices[0]]