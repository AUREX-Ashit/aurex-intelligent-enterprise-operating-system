# schemas/knowledge_asset.py
"""WP-14 BA-04 — Establish Knowledge Asset (C-091). Request/response contracts (Charter §6/§17)."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class EstablishKnowledgeAssetRequest(BaseModel):
    """
    Request body for BA-04's own establish path. `provenance_reference` is
    required here (Pydantic-level, application-layer enforcement) per
    `EIA-001 Vol. I §7.3`'s own invariant ("no Knowledge Asset without
    Provenance") — the physical schema itself carries no `NOT NULL` on this
    column (Charter §6/§7); this is the enforcement mechanism.
    """

    knowledge_asset_name: str | None = Field(None, max_length=255)
    knowledge_asset_type: str | None = Field(None, max_length=255)
    provenance_reference: str = Field(..., min_length=1, max_length=255)
    source_ingestion_id: UUID | None = Field(
        None,
        description="Optional — data_ingestion_registry has no physical model in this repository yet (Charter §16); leave unset until it does.",
    )
    confidence_rule_id: UUID | None = Field(
        None,
        description="Optional — confidence_scoring_registry has no physical model in this repository yet (Charter §15/§16); leave unset until it does.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "knowledge_asset_name": "Board Independence Ratio — FY25",
                "knowledge_asset_type": "fact",
                "provenance_reference": "governance-report-fy25.pdf#p12",
            }
        }
    }


# WP-14 BA-04 Increment (`TDS-014 §2`) — the only three targets `IRA-014 §6`
# BA-04's own row names, each requested directly from `PROPOSED`. No other
# transition is authorized by this Increment (`TDS-014 §2`, `BA04-INC-DEC-001`).
ALLOWED_TRANSITION_TARGETS = ("VALIDATED", "ACCEPTED", "REJECTED")


class TransitionKnowledgeAssetRequest(BaseModel):
    """Request body for the BA-04 Increment's own transition path (`TDS-014 §5`)."""

    target_status: str = Field(...)

    @field_validator("target_status")
    @classmethod
    def _validate_target_status(cls, value: str) -> str:
        if value not in ALLOWED_TRANSITION_TARGETS:
            raise ValueError(f"target_status must be one of {ALLOWED_TRANSITION_TARGETS}")
        return value

    model_config = {
        "json_schema_extra": {
            "example": {"target_status": "ACCEPTED"},
        }
    }


class KnowledgeAssetResponse(BaseModel):
    """Result of BA-04's own establish path, and its get-by-id path."""

    knowledge_asset_id: UUID
    knowledge_asset_name: str | None
    knowledge_asset_type: str | None
    curation_status: str
    provenance_reference: str | None
    source_ingestion_id: UUID | None
    confidence_rule_id: UUID | None
    freshness_last_confirmed_at: datetime | None
    graph_engine_reference: str | None
    active_flag: bool
    organization_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}
