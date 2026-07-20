# services/vector_provider.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from config.settings import settings

class VectorProvider(ABC):
    """Abstract interface contract representing decoupled search engines (Azure Cognitive/Pinecone/Weaviate)."""
    
    @abstractmethod
    async def index_documents(self, index_name: str, documents: List[Dict[str, Any]]) -> bool:
        """Pushes items and tracking embeddings onto active registry."""
        pass

    @abstractmethod
    async def search_index(
        self, 
        index_name: str, 
        query_vector: List[float], 
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Executes vector and hybrid search filters returning score-ranked references."""
        pass


class AzureSearchStubProvider(VectorProvider):
    """Interfaced mock simulating Azure Cognitive Search capability layer."""
    
    def __init__(self, has_hybrid: bool = True):
        self.hybrid = has_hybrid

    async def index_documents(self, index_name: str, documents: List[Dict[str, Any]]) -> bool:
        return True

    async def search_index(
        self, 
        index_name: str, 
        query_vector: List[float], 
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        # High fidelity mocked responses representing matches inside index
        return [
            {
                "id": "doc_chunk_1",
                "score": 0.94,
                "text": "Overall energy strategy yields carbon emissions of 4200.50 Metric Tons under Scope 1 direct operations for FY25.",
                "metadata": {"page": 12, "source": "ESG_Report_2025.pdf"}
            },
            {
                "id": "doc_chunk_2",
                "score": 0.82,
                "text": "The Board maintains 11 permanent directors with 8 independent seats ensuring strong independence standards.",
                "metadata": {"page": 43, "source": "ESG_Report_2025.pdf"}
            }
        ]


def get_vector_provider() -> VectorProvider:
    return AzureSearchStubProvider(has_hybrid=True)
