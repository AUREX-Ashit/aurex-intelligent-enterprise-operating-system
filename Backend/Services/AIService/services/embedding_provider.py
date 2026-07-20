# services/embedding_provider.py
from abc import ABC, abstractmethod
from typing import List
from config.settings import settings

class EmbeddingProvider(ABC):
    """Defines uniform abstraction interfaces for vectorizing text chunks."""
    
    @abstractmethod
    async def get_embedding(self, text: str) -> List[float]:
        """Produces singular embedding vector for given string query/segment."""
        pass

    @abstractmethod
    async def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Processes multiple texts concurrently returning mapped vector list."""
        pass


class AzureEmbeddingStubProvider(EmbeddingProvider):
    """Embedded stub provider simulating Azure-powered Vectorization without running remote requests."""
    
    def __init__(self, model_name: str, dimensions: int = 1536):
        self.model_name = model_name
        self.dimensions = dimensions

    async def get_embedding(self, text: str) -> List[float]:
        # Create standard normalized dummy vector matching target footprint
        import math
        vec = [math.sin(i) / 10.0 for i in range(self.dimensions)]
        return vec

    async def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        return [await self.get_embedding(t) for t in texts]


def get_embedding_provider() -> EmbeddingProvider:
    """Dependency injection factory for fetching Embedding Providers."""
    return AzureEmbeddingStubProvider(model_name=settings.embedding_model)
