import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import String, Integer, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class UploadTracker(Base):
    __tablename__ = "corpstage_upload_trackers"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    
    # Isolation key
    tenant_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    
    # Audit trail details
    initiator_user_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Overall stream state
    session_status: Mapped[str] = mapped_column(String(50), default="started", nullable=False)  # started, ingestion_completed, ingestion_failed
    
    # Metadata metrics
    total_files: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    overall_size_bytes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # General logging details
    client_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships mapping backwards
    documents = relationship("Document", back_populates="upload_session", cascade="all, delete-orphan")
