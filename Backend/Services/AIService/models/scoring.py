# models/scoring.py
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column
from models.database import Base

class ESGScoringModel(Base):
    __tablename__ = "esg_scalings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tenant_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    extraction_id: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Environmental, Social, and Governance individual dimensions
    environmental_score: Mapped[float] = mapped_column(Float, default=0.0)
    social_score: Mapped[float] = mapped_column(Float, default=0.0)
    governance_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Aggregate corporate metrics
    composite_esg_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Goal Mapping profiles (e.g. Map to SDGs)
    sdg_mapping: Mapped[dict] = mapped_column(JSON, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
