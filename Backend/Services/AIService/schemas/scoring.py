# schemas/scoring.py
from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, Field

class SDGMappingDetail(BaseModel):
    sdg_id: int
    sdg_name: str
    relevance_score: float = Field(..., description="Mapping confidence score (0.0 to 1.0)")
    evidence_text: str = Field(..., description="Extract snippet demonstrating mapping justification")

class ScoringRequest(BaseModel):
    extraction_id: int = Field(..., description="Target extraction transaction ID for ESG scaling analysis")
    weightings: Optional[Dict[str, float]] = Field(None, description="Custom scoring weight allocation ratios")

class ScoringResponse(BaseModel):
    id: int
    tenant_id: str
    extraction_id: int
    environmental_score: float
    social_score: float
    governance_score: float
    composite_esg_score: float
    sdg_mapping: List[SDGMappingDetail]
    created_at: datetime
