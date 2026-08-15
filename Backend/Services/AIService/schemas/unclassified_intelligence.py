# schemas/unclassified_intelligence.py
"""WP-14 BA-02/BA-03 — Register + Resolve Enterprise Intelligence Candidate (C-090). Request/response contracts (`IRA-014 §6` BA-02/BA-03 rows)."""
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator

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


# ---------------------------------------------------------------------------
# BA-03 — Resolve Enterprise Intelligence Candidate (Convergence Decision)
# ---------------------------------------------------------------------------

RESOLUTION_OUTCOMES = ("MAPPED_TO_EXISTING", "NEW_CDE_CREATED", "DISCARDED")


class ResolveIntelligenceCandidateRequest(BaseModel):
    """
    Request body for BA-03's own resolve path (`Complete_Blueprint.md
    §5.0c` Binding 5's three-way decision). Exactly one of the three
    `outcome` values, each requiring its own supporting data:
    `MAPPED_TO_EXISTING` requires `metric_id` (a logical-only reference —
    `metric_registry`, the Global canonical CDE library, has zero
    physical rows anywhere in this repository, so this cannot be
    validated against a real row today, disclosed rather than silently
    assumed); `NEW_CDE_CREATED` requires `metric_name`/`metric_code`;
    `DISCARDED` requires no supporting data.
    """

    outcome: str = Field(...)
    metric_id: UUID | None = Field(None, description="Required for MAPPED_TO_EXISTING — logical reference only, not physically validated.")
    metric_name: str | None = Field(None, max_length=255, description="Required for NEW_CDE_CREATED.")
    metric_code: str | None = Field(None, max_length=100, description="Required for NEW_CDE_CREATED.")
    metric_description: str | None = Field(None)
    unit_of_measure: str | None = Field(None, max_length=50)
    formula_logic: str | None = Field(None)
    semantic_match_rejected_reason: str | None = Field(
        None, description="Why a Semantic Matching result (if any) was rejected in favor of creating a new CDE."
    )

    @field_validator("outcome")
    @classmethod
    def _validate_outcome(cls, value: str) -> str:
        if value not in RESOLUTION_OUTCOMES:
            raise ValueError(f"outcome must be one of {RESOLUTION_OUTCOMES}")
        return value

    @model_validator(mode="after")
    def _validate_supporting_data(self) -> "ResolveIntelligenceCandidateRequest":
        if self.outcome == "MAPPED_TO_EXISTING" and self.metric_id is None:
            raise ValueError("metric_id is required when outcome is MAPPED_TO_EXISTING")
        if self.outcome == "NEW_CDE_CREATED" and (not self.metric_name or not self.metric_code):
            raise ValueError("metric_name and metric_code are required when outcome is NEW_CDE_CREATED")
        return self

    model_config = {
        "json_schema_extra": {
            "example": {
                "outcome": "NEW_CDE_CREATED",
                "metric_name": "Board Independence Ratio",
                "metric_code": "BOARD_INDEPENDENCE_RATIO",
                "unit_of_measure": "%",
            }
        }
    }


class ResolvedIntelligenceCandidateResponse(BaseModel):
    """
    Result of BA-03's own resolve path. Surfaces the Semantic Matching
    attempt record and, for a CDE-producing outcome, the Evidence
    reference — both directly, without a second query, mirroring BA-04's
    own "establish response is the status view" precedent.

    `semantic_match_result_metric_id`/`semantic_match_score` mirror the
    LOCKED `customer_metric_registry` columns of the same name exactly —
    both always `None` in this implementation, since those columns are
    contractually reserved for a **Global** `metric_registry` match
    (`Master_Technical_Architecture.md`'s own `COMMENT ON COLUMN`) and
    `metric_registry` has zero physical rows anywhere in this repository
    (Gate 1 Finding 2 remediation — an earlier version of this response
    incorrectly populated `semantic_match_result_metric_id` with a Tenant
    `customer_metric_id`). `same_organization_duplicate_customer_metric_id`
    is the corrected, honestly-separate surface for the real, functioning
    same-organization Tenant-CDE duplicate heuristic `TD-145` discloses —
    it corresponds to no LOCKED column, since the schema provides none
    for a Tenant-to-Tenant match record.
    """

    unclassified_id: UUID
    resolution_status: str
    resolved_by_user_id: UUID | None
    resolved_at: datetime | None
    resolved_metric_id: UUID | None
    resolved_customer_metric_id: UUID | None
    semantic_match_attempted_flag: bool | None
    semantic_match_result_metric_id: UUID | None
    semantic_match_score: Decimal | None
    same_organization_duplicate_customer_metric_id: UUID | None
    evidence_id: UUID | None

    model_config = {"from_attributes": True}
