# schemas/unclassified_intelligence.py
"""WP-14 BA-02 — Register Enterprise Intelligence Candidate (C-090). Request/response contracts (`IRA-014 §6` BA-02 row)."""
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

# `IRA-014 §5.2`'s own explicit scope restriction — the DB's own CHECK
# constraint permits all seven `extraction_method` values (AMD-005); the
# five automated ones (OCR/NLP_PARSE/TABLE_EXTRACT/ENTITY_EXTRACT/
# SEMANTIC_PARSE) presuppose a live extraction pipeline over a connected
# Discovery Provider, which does not exist. This Business Activity is
# scoped to the two extraction methods that require no live connector.
ALLOWED_EXTRACTION_METHODS = ("MANUAL_ENTRY", "API_INGEST")
EXCLUDED_EXTRACTION_METHODS = ("OCR", "NLP_PARSE", "TABLE_EXTRACT", "ENTITY_EXTRACT", "SEMANTIC_PARSE")


class RegisterIntelligenceCandidateRequest(BaseModel):
    """
    Request body for BA-02's own register path. `raw_extracted_value`/
    `source_document_reference` are mandatory per AMD-005's own `NOT NULL`
    columns. `source_page_section` is optional — `IRA-014 §6`'s own text
    describes it as mandatory, but the physical schema itself carries no
    `NOT NULL` on this column; the LOCKED schema is treated as
    authoritative, mirroring the identical schema-vs-descriptive-text
    resolution already applied to BA-01's own category/type CHECK claim.
    """

    raw_extracted_value: str = Field(..., min_length=1)
    source_document_reference: str = Field(..., min_length=1)
    source_page_section: str | None = Field(None, max_length=500)
    extraction_method: str = Field(...)

    @field_validator("extraction_method")
    @classmethod
    def _validate_extraction_method(cls, value: str) -> str:
        if value not in ALLOWED_EXTRACTION_METHODS:
            if value in EXCLUDED_EXTRACTION_METHODS:
                raise ValueError(
                    f"extraction_method '{value}' requires a live extraction pipeline over a connected "
                    f"Discovery Provider, which this Business Activity does not build (IRA-014 §5.2) — "
                    f"use one of {ALLOWED_EXTRACTION_METHODS} instead"
                )
            raise ValueError(f"extraction_method must be one of {ALLOWED_EXTRACTION_METHODS}")
        return value

    model_config = {
        "json_schema_extra": {
            "example": {
                "raw_extracted_value": "Board independence ratio: 62%",
                "source_document_reference": "governance-report-fy25.pdf",
                "source_page_section": "p.12",
                "extraction_method": "MANUAL_ENTRY",
            }
        }
    }


class IntelligenceCandidateResponse(BaseModel):
    """Result of BA-02's own register path."""

    unclassified_id: UUID
    organization_id: UUID
    raw_extracted_value: str
    source_document_reference: str
    source_page_section: str | None
    extraction_method: str
    llm_label_suggestion: str | None
    llm_confidence_score: Decimal | None
    probable_domain: str | None
    probable_bq_id: str | None
    resolution_status: str
    convergence_signal_raised_flag: bool
    active_flag: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
