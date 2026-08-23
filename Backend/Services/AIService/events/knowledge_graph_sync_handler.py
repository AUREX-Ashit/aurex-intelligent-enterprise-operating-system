# events/knowledge_graph_sync_handler.py
"""
WP-14 BA-05 — Synchronize Enterprise Knowledge Graph. `KnowledgeGraphSyncHandler`
(`TDS-013 §7`, §8 step 3, §11, §19). A registered `EventSubscriber` handler
(`AsyncEventHandler`, `Backend/Shared/Events/event_subscriber.py`)
consuming `KnowledgeAssetAcceptedEvent`. Maps the event to exactly the one
relationship tuple `RO-DEC-WP14-BA05-02` decides — no other trigger, no
other relationship kind (`TDS-013 §8` step 3).

Trust boundary (`RO-DEC-WP14-BA05-02`, `TDS-013 §9`/§26a): the event
payload's own `organization_id` is NEVER used as authoritative — the
target Organization is always the Knowledge Asset's own freshly-read,
persisted `organization_id`, resolved inside `RelationshipResolutionService`
(`services/entity_ownership_resolver.py`), never a value taken from the
CloudEvent envelope. This handler reads only `event.knowledge_asset_id`
from the payload.

Rejections (`TDS-013 §16`) propagate as `RelationshipRejectedError` —
`EventSubscriber.handle_inbound_message`'s own existing dispatch loop
already catches any handler exception and routes it to the existing DLQ
mechanism (`route_to_dead_letter_queue`, phase `HANDLER_CRASH`) — reused
verbatim, no new DLQ mechanism invented (`TDS-013 §8` step 6). No live
concrete `EventSubscriber` subclass (broker-connected `start()`/`stop()`)
exists anywhere in this repository yet — a disclosed, pre-existing,
non-blocking infrastructure-maturity gap (`TDS-013 §24` item 2), unrelated
to this handler's own business-logic correctness, which is independently
invokable and testable via `handle()` directly.

Binds the triggering event's own `correlation_id` into `Backend/Shared/
Logging`'s real `CorrelationContext` for the duration of `handle()` (reset
afterward), mirroring `EventSubscriber.handle_inbound_message`'s own
existing context-propagation step — so `RelationshipResolutionService`'s
own `AuditLogger` calls carry a trace back to the originating event even
though no live dispatcher performs this propagation automatically yet
(`Gate 1` Finding `N-1` remediation).
"""
from __future__ import annotations

import logging
import sys
import uuid
from pathlib import Path
from typing import Callable

_BACKEND_ROOT = Path(__file__).resolve().parents[3]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from aurex.backend.shared.events.event_base import BaseEvent
from aurex.backend.shared.logging.correlation_context import CorrelationContext
from sqlalchemy.ext.asyncio import AsyncSession

from events.knowledge_asset_events import KnowledgeAssetAcceptedEvent
from models.database import AsyncSessionLocal
from services.relationship_resolution_service import RelationshipResolutionService

_logger = logging.getLogger("aiservice.knowledge_graph")


class KnowledgeGraphSyncHandler:
    """
    `TDS-013 §19` — `KnowledgeGraphSyncHandler.handle(event: BaseEvent) -> None`.
    Stateless; a new session is opened per invocation. `session_factory`
    defaults to AIService's own real `AsyncSessionLocal` (`models/database.py`)
    — the same construct `get_db()` itself uses — and is overridable only so
    tests can substitute an isolated session factory, mirroring the
    dependency-injection pattern every FastAPI route in this service already
    uses via `Depends(get_db)`; production behavior is unaffected.
    """

    def __init__(self, session_factory: Callable[[], AsyncSession] = AsyncSessionLocal) -> None:
        self._session_factory = session_factory

    async def handle(self, event: BaseEvent) -> None:
        if not isinstance(event, KnowledgeAssetAcceptedEvent):
            # Registered only against KnowledgeAssetAcceptedEvent's own
            # event_name — a mismatched type reaching here would be a
            # framework-routing defect, not a BA-05 rejection; fail loudly.
            raise TypeError(f"KnowledgeGraphSyncHandler.handle received an unexpected event type: {type(event)!r}")

        knowledge_asset_id = uuid.UUID(event.knowledge_asset_id)

        correlation_token = CorrelationContext.set_correlation_id(event.correlation_id)
        try:
            async with self._session_factory() as session:
                service = RelationshipResolutionService(session)
                try:
                    await service.resolve_and_persist(
                        source_entity_type="KNOWLEDGE_ASSET",
                        source_entity_id=knowledge_asset_id,
                        relationship_type="Governed By",
                        target_entity_type="ORGANIZATION",
                        # RO-DEC-WP14-BA05-02: target_entity_id is derived
                        # inside RelationshipResolutionService from the
                        # source's own resolved organization_id — never from
                        # event.organization_id (trust boundary, TDS-013 §9/§26a).
                        target_entity_id=None,
                    )
                except Exception:
                    await session.rollback()
                    raise
                else:
                    await session.commit()
        finally:
            CorrelationContext.clear_correlation_id(correlation_token)

        _logger.info(
            "KnowledgeGraphSyncHandler processed KnowledgeAssetAcceptedEvent (knowledge_asset_id=%s, event_id=%s)",
            knowledge_asset_id,
            event.event_id,
        )
