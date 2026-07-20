# schemas/rag.py
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class RAGConfigCreation(BaseModel):
    index_name: str = Field(..., description="Name of isolated target document index")
    chunk_size: int = Field(1000, description="Granular character count size of embedding chunk")
    overlap: int = Field(200, description="Token/character sliding contextual overlap buffer")
    meta_attributes: Optional[Dict[str, Any]] = Field(default_factory=dict)

class RAGConfigResponse(BaseModel):
    id: int
    tenant_id: str
    index_name: str
    chunk_size: int
    overlap: int
    semantic_search_enabled: bool
    created_at: datetime
