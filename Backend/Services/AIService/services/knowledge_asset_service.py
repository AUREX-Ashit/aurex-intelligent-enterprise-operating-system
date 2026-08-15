# services/knowledge_asset_service.py
"""
WP-14 BA-04 — Establish Knowledge Asset (C-091 Knowledge Management).
Realizes `EIA-001 Vol. I §7`'s own Knowledge Asset concept: "a curated,
governed unit of knowledge produced from one or more Signals," carrying
Provenance from first existence (Charter §2). Deliberately narrow: this
Business Activity implements establishment and retrieval only — the
`curation_status` transition graph is explicitly undecided by any
governing document (Charter §9) and is not invented here.
"""
from __future__ import annotations

import uuid

from fastapi import HTTPException, status

from observability import AuditStatus, record_audit
from repositories.knowledge_asset_repository import KnowledgeAssetRegistryRepository
from schemas.knowledge_asset import EstablishKnowledgeAssetRequest, KnowledgeAssetResponse


class KnowledgeAssetService:
    """Business Activity orchestrator for BA-04."""

    def __init__(self, repo: KnowledgeAssetRegistryRepository) -> None:
        self.repo = repo

    async def establish(
        self, organization_id: uuid.UUID, actor_id: uuid.UUID, request: EstablishKnowledgeAssetRequest
    ) -> KnowledgeAssetResponse:
        asset = await self.repo.create(
            organization_id=organization_id,
            knowledge_asset_name=request.knowledge_asset_name,
            knowledge_asset_type=request.knowledge_asset_type,
            provenance_reference=request.provenance_reference,
            source_ingestion_id=request.source_ingestion_id,
            confidence_rule_id=request.confidence_rule_id,
        )
        # Certification Remediation Finding 2 (Gate 1, 2026-08-11): a
        # state-changing establish action in AIService requires audit
        # evidence, per TDS-012 §8's own precedent for the closest,
        # same-service Business Activity shape (WP-12 BA-01's own
        # establish path, services/conversation_service.py::establish()).
        # Reuses the identical mechanism verbatim — no new audit
        # framework. No sensitive request content (e.g. provenance_
        # reference text) is written to the audit record, only the
        # resulting resource identifier, mirroring conversation_service's
        # own metadata-minimal SUCCESS record shape exactly.
        record_audit(
            action="ESTABLISH_KNOWLEDGE_ASSET",
            resource=f"knowledge_asset:{asset.knowledge_asset_id}",
            status=AuditStatus.SUCCESS,
            actor_id=str(actor_id),
            tenant_id=str(organization_id),
        )
        return KnowledgeAssetResponse.model_validate(asset)

    async def get_by_id(
        self, organization_id: uuid.UUID, knowledge_asset_id: uuid.UUID
    ) -> KnowledgeAssetResponse:
        asset = await self.repo.get_by_id_for_caller(organization_id, knowledge_asset_id)
        if asset is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Knowledge Asset with that id is visible to your own Organization.",
            )
        return KnowledgeAssetResponse.model_validate(asset)
