# models/rag.py
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from models.database import Base

class RAGConfigModel(Base):
    __tablename__ = "rag_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tenant_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    index_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Storage structure configuration metrics
    chunk_size: Mapped[int] = mapped_column(Integer, default=1000)
    overlap: Mapped[int] = mapped_column(Integer, default=200)
    semantic_search_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Embeddings/Search platform meta registries
    meta_attributes: Mapped[dict] = mapped_column(JSON, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
