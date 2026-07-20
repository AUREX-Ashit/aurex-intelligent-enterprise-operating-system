# models/validation.py
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, JSON, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column
from models.database import Base

class ESGValidationModel(Base):
    __tablename__ = "esg_validations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tenant_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    extraction_id: Mapped[int] = mapped_column(Integer, nullable=False)
    governance_verified: Mapped[bool] = mapped_column(Boolean, default=True)
    validation_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Detailed rules run tracker logs
    rules_run: Mapped[dict] = mapped_column(JSON, nullable=False)
    # Highlight anomalies / hallucinations
    anomalies_detected: Mapped[list] = mapped_column(JSON, default=list)
    
    reviewed_by: Mapped[str] = mapped_column(String(100), nullable=True)
    is_reviewed: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
