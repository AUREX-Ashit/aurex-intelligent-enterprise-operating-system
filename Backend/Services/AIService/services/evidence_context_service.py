# services/evidence_context_service.py
"""
WP-15 BA-01 — Understand Evidence Context (C-066 Evidence Management,
`TDS-015`). Read-only. Reuses `evidence_registry` exactly as it exists
today (`TDS-015 §8`) — no write, mutate, or delete path is added here;
`create()`/`create_linked()` on `EvidenceRegistryRepository` remain
WP-11's and WP-14's own exclusive province, untouched by this service.
"""
from __future__ import annotations

import uuid

from fastapi import HTTPException, status

from repositories.search_repository import EvidenceRegistryRepository
from schemas.evidence import EvidenceListResponse, EvidenceResponse

_NOT_FOUND = "Evidence record not found."


class EvidenceContextService:
    """Business Activity orchestrator for BA-01."""

    def __init__(self, evidence_repo: EvidenceRegistryRepository) -> None:
        self.evidence_repo = evidence_repo

    async def get_by_id(
        self,
        organization_id: uuid.UUID,
        evidence_id: uuid.UUID,
        *,
        is_platform_admin: bool,
    ) -> EvidenceResponse:
        """
        404, not 403, for a foreign Organization's row (`TDS-015 §5`
        anti-enumeration rule) — a caller must not be able to distinguish
        "does not exist" from "exists, but is not yours" by response code.
        `PLATFORM_ADMIN` retains cross-Organization read access on this
        single-item path only (`TDS-015 §9`/§13) — never on the list path
        (`RO-DEC-C066-BA01-05`, `list_visible` below).
        """
        instance = await self.evidence_repo.get_by_id(evidence_id)
        if instance is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=_NOT_FOUND)
        if instance.organization_id != organization_id and not is_platform_admin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=_NOT_FOUND)
        return EvidenceResponse.model_validate(instance)

    async def list_visible(
        self,
        organization_id: uuid.UUID,
        *,
        linked_entity_type: str | None,
        linked_entity_id: uuid.UUID | None,
        evidence_source: str | None,
        evidence_type: str | None,
    ) -> EvidenceListResponse:
        """
        Always scoped to the caller's own Organization, for every caller
        including `PLATFORM_ADMIN` — no cross-Organization listing
        capability exists (`RO-DEC-C066-BA01-05`). An empty result is a
        valid 200, not a 404 (`TDS-015 §13`).
        """
        rows = await self.evidence_repo.list_visible(
            organization_id,
            linked_entity_type=linked_entity_type,
            linked_entity_id=linked_entity_id,
            evidence_source=evidence_source,
            evidence_type=evidence_type,
        )
        return EvidenceListResponse(evidence_items=[EvidenceResponse.model_validate(row) for row in rows])
