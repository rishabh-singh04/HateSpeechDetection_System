# app/agents/hybrid_retriever.py
import faiss
import numpy as np
import json
from pathlib import Path
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from app.schemas.policies import PolicySearchResult
import logging

logger = logging.getLogger(__name__)

class HybridRetrieverAgent:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.metadata = []
        self.policy_dir = Path("app/data/policy_docs")
        self.content_cache = {}
        
    def load_index(self, faiss_index_path: Path, metadata_path: Path):
        """Load FAISS index and metadata"""
        try:
            self.index = faiss.read_index(str(faiss_index_path))
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
            logger.info(f"Loaded FAISS index with {len(self.metadata)} policies")
        except Exception as e:
            logger.error(f"Failed to load index: {str(e)}")
            raise
            
    def _load_policy_content(self, source: str) -> str:
        """Load policy content from file"""
        if source not in self.content_cache:
            try:
                policy_path = self.policy_dir / source
                if policy_path.exists():
                    with open(policy_path, 'r', encoding='utf-8') as f:
                        self.content_cache[source] = f.read()
                else:
                    self.content_cache[source] = ""
                    logger.warning(f"Policy file not found: {source}")
            except Exception as e:
                logger.error(f"Error loading policy {source}: {str(e)}")
                self.content_cache[source] = ""
        return self.content_cache[source]

    def search(self, query: str, k: int = 5, threshold: float = 0.3) -> List[Dict[str, Any]]:
        """
        Enhanced search with proper content loading and similarity verification
        """
        if not self.index:
            raise ValueError("FAISS index not loaded")
            
        # Get normalized query embedding
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        query_embedding = query_embedding / np.linalg.norm(query_embedding)
        
        # Search FAISS index
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for i, score in zip(indices[0], distances[0]):
            similarity = 1 - score  # Convert distance to similarity score
            
            if similarity < threshold:
                continue
                
            metadata = self.metadata[i]
            source = metadata["source"]
            full_content = self._load_policy_content(source)
            
            results.append({
                'id': i,
                'name': source.replace(".txt", "").replace("_", " ").title(),
                'content': full_content,
                'score': float(similarity),
                'source': source,
                'snippet': self._extract_relevant_snippet(full_content, query)
            })
        
        return results
    
    def _extract_relevant_snippet(self, content: str, query: str) -> str:
        """Improved snippet extraction using both keyword and semantic matching"""
        if not content:
            return ""
            
        # Split into paragraphs first
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        query_words = set(query.lower().split())
        
        best_para = ""
        best_score = 0
        
        for para in paragraphs:
            para_words = set(para.lower().split())
            score = len(query_words.intersection(para_words))
            
            # Add semantic similarity score
            para_embedding = self.model.encode([para], convert_to_numpy=True)
            para_embedding = para_embedding / np.linalg.norm(para_embedding)
            semantic_score = np.dot(self.query_embedding, para_embedding.T)[0][0]
            combined_score = score + semantic_score
            
            if combined_score > best_score:
                best_score = combined_score
                best_para = para
                
        return best_para or content[:300]