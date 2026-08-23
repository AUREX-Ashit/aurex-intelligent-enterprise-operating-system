# tests/test_relationship_resolution_service.py
"""
WP-14 BA-05 — Synchronize Enterprise Knowledge Graph. Direct unit/
integration tests for `services/relationship_resolution_service.py` —
BR-1–BR-4 derivation (pure-function positive/negative cases), Ontology
Validation, Entity Resolution failure, and idempotency — independent of
the event-handler call site (`test_knowledge_graph_sync_handler.py`
covers the end-to-end path). No public write API exists for BA-05
(`TDS-013 §19`), so these tests exercise the service directly against
`db_session`, mirroring BA-02's own established precedent ("tenant
isolation independently verified via a live direct-database read — no
retrieval API exists for this Business Activity").
"""
from __future__ import annotations

import uuid

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.knowledge_asset import KnowledgeAssetRegistryModel
from models.knowledge_graph import EnterpriseKnowledgeGraphRegistryModel
from services import relationship_resolution_service as rrs_module
from services.relationship_resolution_service import (
    AuditLogger,
    AuditStatus,
    RejectionReason,
    RelationshipRejectedError,
    RelationshipResolutionService,
    derive_organization_id,
)

ORG_A = uuid.uuid4()
ORG_B = uuid.uuid4()


# --- BR-1-BR-4 pure-function derivation (no I/O) -----------------------------


def test_br1_both_organization_scoped_matching_accepts_shared_value():
    accepted, org = derive_organization_id(ORG_A, ORG_A)
    assert accepted is True
    assert org == ORG_A


def test_br1_br4_both_organization_scoped_mismatched_rejects():
    accepted, org = derive_organization_id(ORG_A, ORG_B)
    assert accepted is False
    assert org is None


def test_br2_only_source_organization_scoped_inherits_source():
    accepted, org = derive_organization_id(ORG_A, None)
    assert accepted is True
    assert org == ORG_A


def test_br2_only_target_organization_scoped_inherits_target():
    accepted, org = derive_organization_id(None, ORG_B)
    assert accepted is True
    assert org == ORG_B


def test_br3_neither_organization_scoped_remains_null():
    accepted, org = derive_organization_id(None, None)
    assert accepted is True
    assert org is None


# --- resolve_and_persist: rejections, success, idempotency ------------------


async def _seed_knowledge_asset(db_session: AsyncSession, organization_id: uuid.UUID) -> uuid.UUID:
    asset = KnowledgeAssetRegistryModel(
        organization_id=organization_id,
        knowledge_asset_name="Test Asset",
        knowledge_asset_type="fact",
        provenance_reference="test-provenance.pdf",
        curation_status="ACCEPTED",
    )
    db_session.add(asset)
    await db_session.commit()
    await db_session.refresh(asset)
    return asset.knowledge_asset_id


@pytest.mark.asyncio
async def test_resolve_and_persist_rejects_invalid_relationship_type(db_session: AsyncSession):
    knowledge_asset_id = await _seed_knowledge_asset(db_session, ORG_A)
    service = RelationshipResolutionService(db_session)

    with pytest.raises(RelationshipRejectedError) as exc_info:
        await service.resolve_and_persist(
            source_entity_type="KNOWLEDGE_ASSET",
            source_entity_id=knowledge_asset_id,
            relationship_type="Not A Real Relationship",
            target_entity_type="ORGANIZATION",
        )
    assert exc_info.value.reason == RejectionReason.INVALID_RELATIONSHIP_TYPE

    rows = (await db_session.execute(select(EnterpriseKnowledgeGraphRegistryModel))).scalars().all()
    assert rows == []


@pytest.mark.asyncio
async def test_resolve_and_persist_rejects_source_not_found(db_session: AsyncSession):
    service = RelationshipResolutionService(db_session)
    nonexistent_id = uuid.uuid4()

    with pytest.raises(RelationshipRejectedError) as exc_info:
        await service.resolve_and_persist(
            source_entity_type="KNOWLEDGE_ASSET",
            source_entity_id=nonexistent_id,
            relationship_type="Governed By",
            target_entity_type="ORGANIZATION",
        )
    assert exc_info.value.reason == RejectionReason.SOURCE_NOT_FOUND

    rows = (await db_session.execute(select(EnterpriseKnowledgeGraphRegistryModel))).scalars().all()
    assert rows == []


@pytest.mark.asyncio
async def test_resolve_and_persist_rejects_unsupported_entity_type(db_session: AsyncSession):
    """An entity type outside EntityOwnershipResolver's own two-strategy minimum scope (TDS-013 §9) is an Entity Resolution failure, never a silent default."""
    service = RelationshipResolutionService(db_session)

    with pytest.raises(RelationshipRejectedError) as exc_info:
        await service.resolve_and_persist(
            source_entity_type="DISCOVERY_PROVIDER",  # not one of the two authorized strategies
            source_entity_id=uuid.uuid4(),
            relationship_type="Governed By",
            target_entity_type="ORGANIZATION",
        )
    assert exc_info.value.reason == RejectionReason.SOURCE_NOT_FOUND


@pytest.mark.asyncio
async def test_resolve_and_persist_success_creates_governed_by_row(db_session: AsyncSession):
    knowledge_asset_id = await _seed_knowledge_asset(db_session, ORG_A)
    service = RelationshipResolutionService(db_session)

    await service.resolve_and_persist(
        source_entity_type="KNOWLEDGE_ASSET",
        source_entity_id=knowledge_asset_id,
        relationship_type="Governed By",
        target_entity_type="ORGANIZATION",
    )
    await db_session.commit()

    row = (
        await db_session.execute(
            select(EnterpriseKnowledgeGraphRegistryModel).where(
                EnterpriseKnowledgeGraphRegistryModel.source_entity_id == knowledge_asset_id
            )
        )
    ).scalar_one()
    assert row.source_entity_type == "KNOWLEDGE_ASSET"
    assert row.relationship_type == "Governed By"
    assert row.target_entity_type == "ORGANIZATION"
    assert row.target_entity_id == ORG_A
    assert row.organization_id == ORG_A
    assert row.graph_engine_reference is None  # live Neo4j write out of scope (TDS-013 §1)


@pytest.mark.asyncio
async def test_resolve_and_persist_is_idempotent_on_duplicate_call(db_session: AsyncSession):
    knowledge_asset_id = await _seed_knowledge_asset(db_session, ORG_A)
    service = RelationshipResolutionService(db_session)

    for _ in range(2):
        await service.resolve_and_persist(
            source_entity_type="KNOWLEDGE_ASSET",
            source_entity_id=knowledge_asset_id,
            relationship_type="Governed By",
            target_entity_type="ORGANIZATION",
        )
        await db_session.commit()

    rows = (
        (
            await db_session.execute(
                select(EnterpriseKnowledgeGraphRegistryModel).where(
                    EnterpriseKnowledgeGraphRegistryModel.source_entity_id == knowledge_asset_id
                )
            )
        )
        .scalars()
        .all()
    )
    assert len(rows) == 1, "duplicate resolve_and_persist calls on the same natural key must not create a second row"


# --- N-1 remediation: real Backend/Shared/Logging framework, not the local substitute ---


def test_uses_the_real_shared_logging_audit_framework_not_the_local_substitute():
    """
    Gate 1 Finding N-1: TDS-013 §5/§23/§24 item 1 states BA-05 "SHALL use
    the real framework directly... no local substitute is needed."
    `AuditLogger`/`AuditStatus` imported by `relationship_resolution_
    service.py` must be `Backend/Shared/Logging`'s real classes (reached
    via the `aurex.backend.shared.logging.audit_logger` alias package),
    never AIService's local, explicitly-temporary `observability.py`
    substitute (`record_audit`/its own local `AuditStatus`).
    """
    from aurex.backend.shared.logging.audit_logger import AuditLogger as RealAuditLogger
    from aurex.backend.shared.logging.audit_logger import AuditStatus as RealAuditStatus
    import observability as local_observability

    assert rrs_module.AuditLogger is RealAuditLogger
    assert rrs_module.AuditStatus is RealAuditStatus
    assert rrs_module.AuditStatus is not local_observability.AuditStatus
    assert not hasattr(rrs_module, "record_audit"), "the local observability.py substitute must not be imported here"


@pytest.mark.asyncio
async def test_success_emits_real_audit_logger_success_record(db_session: AsyncSession, monkeypatch: pytest.MonkeyPatch):
    knowledge_asset_id = await _seed_knowledge_asset(db_session, ORG_A)
    service = RelationshipResolutionService(db_session)

    captured: list[dict] = []
    original_log = AuditLogger.log

    def _capture(*args, **kwargs):
        captured.append(kwargs)
        return original_log(*args, **kwargs)

    monkeypatch.setattr(rrs_module.AuditLogger, "log", staticmethod(_capture))

    await service.resolve_and_persist(
        source_entity_type="KNOWLEDGE_ASSET",
        source_entity_id=knowledge_asset_id,
        relationship_type="Governed By",
        target_entity_type="ORGANIZATION",
    )

    assert len(captured) == 1
    call = captured[0]
    assert call["action"] == "SYNCHRONIZE_KNOWLEDGE_GRAPH_RELATIONSHIP"
    assert call["status"] == AuditStatus.SUCCESS
    assert call["tenant_id"] == str(ORG_A)


@pytest.mark.asyncio
async def test_rejection_emits_real_audit_logger_denied_record_with_reason(
    db_session: AsyncSession, monkeypatch: pytest.MonkeyPatch
):
    service = RelationshipResolutionService(db_session)

    captured: list[dict] = []
    original_log = AuditLogger.log

    def _capture(*args, **kwargs):
        captured.append(kwargs)
        return original_log(*args, **kwargs)

    monkeypatch.setattr(rrs_module.AuditLogger, "log", staticmethod(_capture))

    with pytest.raises(RelationshipRejectedError):
        await service.resolve_and_persist(
            source_entity_type="KNOWLEDGE_ASSET",
            source_entity_id=uuid.uuid4(),
            relationship_type="Governed By",
            target_entity_type="ORGANIZATION",
        )

    assert len(captured) == 1
    call = captured[0]
    assert call["status"] == AuditStatus.DENIED
    assert call["metadata"]["reason"] == RejectionReason.SOURCE_NOT_FOUND.value
