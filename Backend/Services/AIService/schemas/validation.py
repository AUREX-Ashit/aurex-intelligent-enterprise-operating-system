# schemas/validation.py
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class RuleRunLog(BaseModel):
    rule_id: str
    rule_name: str
    passed: bool
    message: str

class AnomalyReport(BaseModel):
    field: str
    disclosed_value: Any
    expected_range: Optional[str] = None
    confidence_decay: float
    description: str

class ValidationRequest(BaseModel):
    extraction_id: int = Field(..., description="Target extraction entity ID to validate")
    custom_rules: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional governance filters to activate")

class ValidationResponse(BaseModel):
    id: int
    tenant_id: str
    extraction_id: int
    governance_verified: bool
    validation_timestamp: datetime
    rules_run: List[RuleRunLog]
    anomalies_detected: List[AnomalyReport]
    is_reviewed: bool
    reviewed_by: Optional[str] = None

class HumanReviewRequest(BaseModel):
    validation_id: int = Field(..., description="Target validation instance ID for manual governance check override")
    reviewer_email: str = Field(..., description="Auditor identity email")
    is_approved: bool = Field(True, description="Approving result overrides existing anomaly records")
    comments: Optional[str] = Field(None, description="Auditing record review comments")
