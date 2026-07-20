import uuid
from typing import Any, Dict, Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date, DateTime, JSON, Float, ForeignKey, Enum, Text
import enum
from models.database import Base, TenantModelMixin

class ReportStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PEER_REVIEW = "PEER_REVIEW"
    STAKEHOLDER_APPROVAL = "STAKEHOLDER_APPROVAL"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"

class ReportFramework(str, enum.Enum):
    ESG_GENERAL = "ESG_GENERAL"
    BRSR = "BRSR"
    GRI = "GRI"
    CSRD = "CSRD"

class ESGReport(Base, TenantModelMixin):
    __tablename__ = "esg_reports"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    framework: Mapped[ReportFramework] = mapped_column(String(50), nullable=False)
    reporting_year: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[ReportStatus] = mapped_column(String(50), default=ReportStatus.DRAFT, nullable=False)
    
    # Elastic reporting fields (contains emissions, gender pay gap, waste, governance indexes)
    metrics_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    
    # Overall and Pillar Scores
    score_environmental: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    score_social: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    score_governance: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    score_overall: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Export Tracking Relation
    exports: Mapped[List["ReportExport"]] = relationship(back_populates="report", cascade="all, delete-orphan")

class ReportExport(Base, TenantModelMixin):
    __tablename__ = "report_exports"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    report_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("esg_reports.id", ondelete="CASCADE"), nullable=False)
    format: Mapped[str] = mapped_column(String(20), nullable=False) # "PDF", "XLSX", "PPTX", "JSON"
    export_url: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="COMPLETED", nullable=False) # "PENDING", "COMPLETED", "FAILED"
    file_size_bytes: Mapped[Optional[int]] = mapped_column(nullable=True)
    
    report: Mapped["ESGReport"] = relationship(back_populates="exports")

class Scorecard(Base, TenantModelMixin):
    __tablename__ = "scorecards"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    metric_name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False) # "Environmental", "Social", "Governance"
    actual_value: Mapped[float] = mapped_column(Float, nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(30), nullable=False) # "MT CO2e", "Percentage", "Hours"
    compliance_pct: Mapped[float] = mapped_column(Float, nullable=False)
    assessment_year: Mapped[int] = mapped_column(nullable=False)

class AuditLog(Base, TenantModelMixin):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # "GENERATE", "EXPORT_REQUEST", "APPROVAL", "MODIFY"
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False) # "ESGReport", "Scorecard"
    entity_id: Mapped[str] = mapped_column(String(100), nullable=False)
    changed_by: Mapped[str] = mapped_column(String(150), nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
