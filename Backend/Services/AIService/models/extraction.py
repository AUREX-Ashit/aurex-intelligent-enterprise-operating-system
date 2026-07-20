# models/extraction.py
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, JSON, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from models.database import Base

class ESGExtractionModel(Base):
    __tablename__ = "esg_extractions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tenant_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    document_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="completed")  # (completed, failed, manual_review)
    extracted_by: Mapped[str] = mapped_column(String(100), default="ai_orchestrator")
    
    # ESG Metrics and disclosure schemas stored as highly queryable JSON
    extracted_metrics: Mapped[dict] = mapped_column(JSON, nullable=False)
    
    # Confidence metrics for tracing
    overall_confidence: Mapped[float] = mapped_column(Float, default=1.0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
