# services/rag_engine.py
from typing import List, Dict, Any, Optional
from fastapi import Depends
from services.embedding_provider import EmbeddingProvider, get_embedding_provider
from services.vector_provider import VectorProvider, get_vector_provider

class RAGEngine:
    """
    RAG Orchestration Core framework.
    Handles semantic contexts and abstracts injection logic separating search indexes from LLM calls.
    """
    def __init__(
        self, 
        embedder: EmbeddingProvider = Depends(get_embedding_provider),
        vector_db: VectorProvider = Depends(get_vector_provider)
    ):
        self.embedder = embedder
        self.vector_db = vector_db

    async def build_context(self, index_name: str, query: str, top_k: int = 3) -> str:
        """Assembles contextual summary based on query vector index matches."""
        # Embed query text
        query_vector = await self.embedder.get_embedding(query)
        
        # Search index
        results = await self.vector_db.search_index(index_name, query_vector, top_k=top_k)
        
        # Assemble references
        evidences = []
        for index, item in enumerate(results):
            text = item.get("text", "")
            score = item.get("score", 0.0)
            meta = item.get("metadata", {})
            evidences.append(f"[{index + 1}] Source: {meta.get('source')} (Score: {score}):\n\"{text}\"")
            
        return "\n\n".join(evidences) if evidences else "No matching references found."


def get_rag_engine(
    embed_provider: EmbeddingProvider = Depends(get_embedding_provider),
    vector_prov: VectorProvider = Depends(get_vector_provider)
) -> RAGEngine:
    """Creates RAGEngine dependent instances."""
    return RAGEngine(embedder=embed_provider, vector_db=vector_prov)
