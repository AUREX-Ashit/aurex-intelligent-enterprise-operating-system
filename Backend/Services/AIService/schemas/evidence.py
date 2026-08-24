# schemas/evidence.py
"""WP-15 BA-01 — Understand Evidence Context (C-066 Evidence Management). Read-only response contracts (`TDS-015 §9`)."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EvidenceResponse(BaseModel):
    """Direct field mapping of `EvidenceRegistryModel` — no derived data (`TDS-015 §9`)."""
    evidence_id: UUID
    evidence_type: str | None
    linked_entity_type: str | None
    linked_entity_id: UUID | None
    evidence_source: str | None
    file_reference: str | None
    source_timestamp: datetime | None
    confidence_score: int | None
    externally_verified_flag: bool
    legal_defensibility_flag: bool
    retention_policy: str | None
    document_hash_signature: str | None
    ai_extracted_flag: bool
    active_flag: bool
    created_at: datetime
    organization_id: UUID
    confidence_rule_id: UUID | None

    model_config = {"from_attributes": True}


class EvidenceListResponse(BaseModel):
    """BA-01's own filtered list path — every Evidence row visible to the caller (`TDS-015 §9`/§11)."""
    evidence_items: list[EvidenceResponse]
