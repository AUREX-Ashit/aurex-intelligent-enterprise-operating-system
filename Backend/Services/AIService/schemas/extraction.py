# schemas/extraction.py
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class ESGMetrics(BaseModel):
    # Environmental Dimensions
    scope_1_emissions_mt: Optional[float] = Field(None, description="Scope 1 greenhouse gas emissions in metric tons")
    scope_2_emissions_mt: Optional[float] = Field(None, description="Scope 2 greenhouse gas emissions in metric tons")
    scope_3_emissions_mt: Optional[float] = Field(None, description="Scope 3 greenhouse gas emissions in metric tons")
    renewable_energy_ratio: Optional[float] = Field(None, description="Renewable energy share of total consumption")
    water_consumption_m3: Optional[float] = Field(None, description="Water consumption in cubic meters")

    # Social Dimensions
    total_employee_count: Optional[int] = Field(None, description="Total corporate headcount")
    female_executive_ratio: Optional[float] = Field(None, description="Ratio of female leadership")
    gender_pay_gap_ratio: Optional[float] = Field(None, description="Gender pay gap disparity metric")
    employee_turnover_rate: Optional[float] = Field(None, description="Annual employee voluntary turnover")

    # Governance Dimensions
    board_size: Optional[int] = Field(None, description="Size of the board of directors")
    independent_directors_ratio: Optional[float] = Field(None, description="Independent directors percentage share")
    anti_corruption_policy: Optional[bool] = Field(False, description="Is anti-corruption policy active")
    whistleblower_hotline_active: Optional[bool] = Field(False, description="Active channel for whistleblower disclosures")

class ExtractionRequest(BaseModel):
    document_name: str = Field(..., description="Target file name for ESG Extraction processing")
    file_uri: Optional[str] = Field(None, description="Cloud storage blob link or path to the file")
    metadata_filters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Metadata filtering filters for context scoping")

class ExtractionResponse(BaseModel):
    id: int
    tenant_id: str
    document_name: str
    status: str
    extracted_metrics: ESGMetrics
    overall_confidence: float
    extracted_by: str
    created_at: datetime
