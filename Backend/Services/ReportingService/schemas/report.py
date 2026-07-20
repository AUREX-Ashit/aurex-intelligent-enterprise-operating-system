from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List
import uuid
from datetime import datetime
from models.report import ReportStatus, ReportFramework

# Base class with standard serialization settings (Pydantic v2 uses model_config)
class BaseConfigModel(BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {}
        }
    }

class ReportGenerateRequest(BaseConfigModel):
    title: str = Field(..., max_length=250, description="Title of the disclosure report")
    framework: ReportFramework = Field(..., description="Reporting framework used (ESG_GENERAL, BRSR, GRI, CSRD)")
    reporting_year: int = Field(..., ge=2000, le=2100, description="Target reporting calendar year")
    custom_parameters: Dict[str, Any] = Field(default_factory=dict, description="Custom properties or KPI limits to override")

class ReportExportRequest(BaseConfigModel):
    report_id: uuid.UUID = Field(..., description="ID of the generated ESG report to export")
    format: str = Field(..., description="Target file format: PDF, XLSX, PPTX, or JSON")

class ReportExportResponse(BaseConfigModel):
    id: uuid.UUID
    report_id: uuid.UUID
    format: str
    export_url: str
    status: str
    file_size_bytes: Optional[int] = None
    created_at: datetime

class ESGReportResponse(BaseConfigModel):
    id: uuid.UUID
    title: str
    framework: ReportFramework
    reporting_year: int
    status: ReportStatus
    metrics_payload: Dict[str, Any]
    score_environmental: Optional[float] = None
    score_social: Optional[float] = None
    score_governance: Optional[float] = None
    score_overall: Optional[float] = None
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class ScorecardCreate(BaseConfigModel):
    metric_name: str = Field(..., max_length=150)
    category: str = Field(..., description="Environmental, Social, or Governance")
    actual_value: float
    target_value: float
    unit: str = Field(..., max_length=30)
    assessment_year: int

class ScorecardResponse(BaseConfigModel):
    id: uuid.UUID
    metric_name: str
    category: str
    actual_value: float
    target_value: float
    unit: str
    compliance_pct: float
    assessment_year: int
    created_at: datetime

class AuditLogResponse(BaseConfigModel):
    id: uuid.UUID
    action: str
    entity_type: str
    entity_id: str
    changed_by: str
    details: Optional[str] = None
    created_at: datetime

class AggregatedCategoryValues(BaseModel):
    average_compliance: float
    metric_count: int

class DashboardSummaryResponse(BaseModel):
    reporting_year: int
    completed_reports_count: int
    overall_pbc_score: float # average of overall scores
    aggregates: Dict[str, AggregatedCategoryValues]
    recent_activity: List[AuditLogResponse]
