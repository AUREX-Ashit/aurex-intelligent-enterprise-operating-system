# tests/test_knowledge_graph_sync_handler.py
"""
WP-14 BA-05 — Synchronize Enterprise Knowledge Graph. End-to-end tests for
`events/knowledge_graph_sync_handler.py::KnowledgeGraphSyncHandler`,
including the Mandatory Tenant-Isolation Test Checklist (`CLAUDE.md
§21.4`): (a) two distinct, unrelated Organizations, no shared row; (b) a
caller in one Organization cannot cause a write scoped to another
Organization's own boundary through this handler; (c) the event payload's
own `organization_id` (a foreign-object-adjacent value not derived from
the caller's own claims — here, from BA-04's own event, not a caller at
all) is independently probed and confirmed non-authoritative.

`KnowledgeGraphSyncHandler` is invoked directly (`await handler.handle(
event)`), mirroring how the BA-04 Increment's own concurrency probe
invokes business logic without depending on a live message broker
(`TDS-013 §24` item 2 — the live broker itself remains a disclosed,
pre-existing stub, unrelated to this handler's own business-logic
correctness).
"""
from __future__ import annotations

import uuid

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from events.knowledge_asset_events import KnowledgeAssetAcceptedEvent
from events.knowledge_graph_sync_handler import KnowledgeGraphSyncHandler
from models.knowledge_asset import KnowledgeAssetRegistryModel
from models.knowledge_graph import EnterpriseKnowledgeGraphRegistryModel
from services.relationship_resolution_service import RejectionReason, RelationshipRejectedError
from tests.conftest import TestingSessionLocal

ORG_A = uuid.uuid4()
ORG_B = uuid.uuid4()


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


def _accepted_event(knowledge_asset_id: uuid.UUID, event_organization_id: uuid.UUID) -> KnowledgeAssetAcceptedEvent:
    """Builds a `KnowledgeAssetAcceptedEvent` directly — `event_organization_id` is the payload's own claim, which BA-05 must never trust as authoritative (TDS-013 §9/§26a)."""
    return KnowledgeAssetAcceptedEvent(
        knowledge_asset_id=str(knowledge_asset_id),
        organization_id=str(event_organization_id),
    )


@pytest_asyncio.fixture
def handler() -> KnowledgeGraphSyncHandler:
    """Injects the shared test session factory (`tests/conftest.py::TestingSessionLocal`) — production defaults to AIService's own real `AsyncSessionLocal`, unaffected."""
    return KnowledgeGraphSyncHandler(session_factory=TestingSessionLocal)


@pytest.mark.asyncio
async def test_handler_creates_governed_by_relationship(db_session: AsyncSession, handler: KnowledgeGraphSyncHandler):
    knowledge_asset_id = await _seed_knowledge_asset(db_session, ORG_A)
    event = _accepted_event(knowledge_asset_id, ORG_A)

    await handler.handle(event)

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


@pytest.mark.asyncio
async def test_handler_ignores_spoofed_event_payload_organization_id(
    db_session: AsyncSession, handler: KnowledgeGraphSyncHandler
):
    """
    Tenant-isolation probe (`CLAUDE.md §21.4`(c)): the Knowledge Asset is
    genuinely owned by Org A, but the triggering event's own payload
    claims `organization_id=Org B` (a spoofed/stale value). The persisted
    relationship MUST be scoped to Org A (the Knowledge Asset's own
    persisted value) — Org B must never appear anywhere in the write.
    """
    knowledge_asset_id = await _seed_knowledge_asset(db_session, ORG_A)
    event = _accepted_event(knowledge_asset_id, event_organization_id=ORG_B)

    await handler.handle(event)

    row = (
        await db_session.execute(
            select(EnterpriseKnowledgeGraphRegistryModel).where(
                EnterpriseKnowledgeGraphRegistryModel.source_entity_id == knowledge_asset_id
            )
        )
    ).scalar_one()
    assert row.organization_id == ORG_A
    assert row.target_entity_id == ORG_A
    assert row.organization_id != ORG_B
    assert row.target_entity_id != ORG_B


@pytest.mark.asyncio
async def test_handler_duplicate_event_delivery_is_idempotent(
    db_session: AsyncSession, handler: KnowledgeGraphSyncHandler
):
    knowledge_asset_id = await _seed_knowledge_asset(db_session, ORG_A)
    event = _accepted_event(knowledge_asset_id, ORG_A)

    await handler.handle(event)
    await handler.handle(event)  # replay — same event, same natural key

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
    assert len(rows) == 1, "replayed KnowledgeAssetAcceptedEvent must not create a duplicate relationship row"


@pytest.mark.asyncio
async def test_handler_two_organizations_no_cross_tenant_leakage(
    db_session: AsyncSession, handler: KnowledgeGraphSyncHandler
):
    """Mandatory Tenant-Isolation Test Checklist (a)/(b), `CLAUDE.md §21.4`: two distinct, unrelated Organizations, no shared row."""
    knowledge_asset_a = await _seed_knowledge_asset(db_session, ORG_A)
    knowledge_asset_b = await _seed_knowledge_asset(db_session, ORG_B)

    await handler.handle(_accepted_event(knowledge_asset_a, ORG_A))
    await handler.handle(_accepted_event(knowledge_asset_b, ORG_B))

    row_a = (
        await db_session.execute(
            select(EnterpriseKnowledgeGraphRegistryModel).where(
                EnterpriseKnowledgeGraphRegistryModel.source_entity_id == knowledge_asset_a
            )
        )
    ).scalar_one()
    row_b = (
        await db_session.execute(
            select(EnterpriseKnowledgeGraphRegistryModel).where(
                EnterpriseKnowledgeGraphRegistryModel.source_entity_id == knowledge_asset_b
            )
        )
    ).scalar_one()

    assert row_a.organization_id == ORG_A
    assert row_b.organization_id == ORG_B
    assert row_a.organization_id != row_b.organization_id

    all_rows = (await db_session.execute(select(EnterpriseKnowledgeGraphRegistryModel))).scalars().all()
    assert len(all_rows) == 2, "exactly one row per Organization — no shared/merged row"


@pytest.mark.asyncio
async def test_handler_rejects_unknown_knowledge_asset_no_row_persisted(
    db_session: AsyncSession, handler: KnowledgeGraphSyncHandler
):
    event = _accepted_event(uuid.uuid4(), ORG_A)  # knowledge_asset_id never established

    with pytest.raises(RelationshipRejectedError) as exc_info:
        await handler.handle(event)
    assert exc_info.value.reason == RejectionReason.SOURCE_NOT_FOUND

    rows = (await db_session.execute(select(EnterpriseKnowledgeGraphRegistryModel))).scalars().all()
    assert rows == []


@pytest.mark.asyncio
async def test_handler_persistence_failure_rolls_back_no_partial_row(
    db_session: AsyncSession, handler: KnowledgeGraphSyncHandler, monkeypatch: pytest.MonkeyPatch
):
    """A failure after Entity Resolution/BR-1–BR-4 but before a successful commit must leave no partial row (TDS-013 §15's own commit-on-success/rollback-on-exception invariant)."""
    knowledge_asset_id = await _seed_knowledge_asset(db_session, ORG_A)
    event = _accepted_event(knowledge_asset_id, ORG_A)

    from repositories.knowledge_graph_repository import EnterpriseKnowledgeGraphRepository

    async def _boom(self, **kwargs):
        raise RuntimeError("simulated persistence failure")

    monkeypatch.setattr(EnterpriseKnowledgeGraphRepository, "insert", _boom)

    with pytest.raises(RuntimeError, match="simulated persistence failure"):
        await handler.handle(event)

    rows = (await db_session.execute(select(EnterpriseKnowledgeGraphRegistryModel))).scalars().all()
    assert rows == [], "a failed persistence attempt must not leave a partial row"


@pytest.mark.asyncio
async def test_handler_wrong_event_type_raises_type_error(handler: KnowledgeGraphSyncHandler):
    with pytest.raises(TypeError):
        await handler.handle(object())  # type: ignore[arg-type]


# --- DLQ routing (existing EventSubscriber mechanism, TDS-013 §8 step 6) ----


@pytest.mark.asyncio
async def test_rejection_triggers_existing_dlq_mechanism(db_session: AsyncSession, handler: KnowledgeGraphSyncHandler):
    """
    `TDS-013 §8` step 6: a rejection routes to "the existing DLQ mechanism
    (`EventSubscriber.route_to_dead_letter_queue`)". `EventSubscriber` is
    abstract and its own `handle_inbound_message` dispatch loop invokes
    handlers synchronously (`handler(domain_event)`, not awaited) — it
    does not yet support awaiting an `AsyncEventHandler`, a disclosed,
    pre-existing, non-blocking infrastructure-maturity gap (`TDS-013 §24`
    item 2), not fixed by this Business Activity. This test therefore
    exercises the real `route_to_dead_letter_queue` method directly,
    orchestrated the way a future async-aware dispatcher would, to confirm
    BA-05's own contribution (raising `RelationshipRejectedError` with a
    specific reason) correctly drives the existing DLQ mechanism, without
    inventing a new one.
    """
    from aurex.backend.shared.events.event_subscriber import EventSubscriber

    class _NoOpSubscriber(EventSubscriber):
        def start(self) -> None:  # pragma: no cover - not exercised
            pass

        def stop(self) -> None:  # pragma: no cover - not exercised
            pass

    subscriber = _NoOpSubscriber(service_name="aiservice")
    dlq_calls: list[tuple[str, Exception]] = []
    monkeypatch_target = subscriber.route_to_dead_letter_queue

    def _capture_dlq(raw_payload, error_phase, exception):
        dlq_calls.append((error_phase, exception))
        return monkeypatch_target(raw_payload, error_phase, exception)

    subscriber.route_to_dead_letter_queue = _capture_dlq  # type: ignore[method-assign]

    event = _accepted_event(uuid.uuid4(), ORG_A)  # unknown knowledge asset -> SOURCE_NOT_FOUND

    try:
        await handler.handle(event)
    except RelationshipRejectedError as exc:
        subscriber.route_to_dead_letter_queue(raw_payload=repr(event), error_phase="HANDLER_CRASH", exception=exc)

    assert len(dlq_calls) == 1
    phase, exc = dlq_calls[0]
    assert phase == "HANDLER_CRASH"
    assert isinstance(exc, RelationshipRejectedError)
    assert exc.reason == RejectionReason.SOURCE_NOT_FOUND


# --- N-1 remediation: real CorrelationContext propagation --------------------


@pytest.mark.asyncio
async def test_handler_binds_and_clears_event_correlation_id(
    db_session: AsyncSession, handler: KnowledgeGraphSyncHandler
):
    """
    Gate 1 Finding N-1 remediation: the triggering event's own
    `correlation_id` must be bound into `Backend/Shared/Logging`'s real
    `CorrelationContext` for the duration of `handle()` (so `AuditLogger`
    calls inside `RelationshipResolutionService` carry a trace back to the
    originating event), and cleared afterward — never left leaked into a
    later, unrelated invocation.
    """
    from aurex.backend.shared.logging.correlation_context import CorrelationContext

    knowledge_asset_id = await _seed_knowledge_asset(db_session, ORG_A)
    event = _accepted_event(knowledge_asset_id, ORG_A)

    assert CorrelationContext.get_correlation_id() is None  # nothing leaked in from a prior test

    observed_during_handle: list[str | None] = []
    from services.relationship_resolution_service import RelationshipResolutionService

    original_resolve = RelationshipResolutionService.resolve_and_persist

    async def _spy(self, *args, **kwargs):
        observed_during_handle.append(CorrelationContext.get_correlation_id())
        return await original_resolve(self, *args, **kwargs)

    import services.relationship_resolution_service as rrs_module

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(rrs_module.RelationshipResolutionService, "resolve_and_persist", _spy)
        await handler.handle(event)

    assert observed_during_handle == [event.correlation_id]
    assert CorrelationContext.get_correlation_id() is None  # cleared after handle() returns
