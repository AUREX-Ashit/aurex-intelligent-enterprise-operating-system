# services/knowledge_asset_service.py
"""
WP-14 BA-04 — Establish Knowledge Asset (C-091 Knowledge Management).
Realizes `EIA-001 Vol. I §7`'s own Knowledge Asset concept: "a curated,
governed unit of knowledge produced from one or more Signals," carrying
Provenance from first existence (Charter §2). `establish()`/`get_by_id()`
are BA-04's own original, certified scope — unchanged by the Increment
below.

**WP-14 BA-04 Increment (`TDS-014`, implementation authorized 2026-08-16):**
`transition()` completes the `curation_status` transition scope this
module's own docstring previously described as "explicitly undecided" —
now resolved, within a deliberately narrow, frozen boundary (`TDS-014
§2`): only `PROPOSED`→{`VALIDATED`,`ACCEPTED`,`REJECTED`} is implemented;
the fuller five-state graph remains undecided and unimplemented, per
`TDS-014`'s own explicit scope decision. On a winning transition to
`ACCEPTED`, publishes `aurex.aiservice.knowledge_asset.accepted` v`1.0.0`
(`TDS-014 §8`) — a disclosed, best-effort delivery attempt only
(`RO-DEC-BA04-INC-007`); the real broker infrastructure is verified
mock-only (`Backend/Shared/Events/event_publisher.py`), a pre-existing,
platform-wide limitation this Increment does not build around. No BA-05
logic (no Knowledge Graph relationship creation) is implemented here —
BA-04 publishes only the fact of acceptance; BA-05 owns everything
downstream (`TDS-014 §17`).
"""
from __future__ import annotations

import logging
import uuid

from fastapi import HTTPException, status

from events.knowledge_asset_events import KnowledgeAssetAcceptedEvent
from observability import AuditStatus, CorrelationContext, record_audit
from repositories.knowledge_asset_repository import KnowledgeAssetRegistryRepository
from schemas.knowledge_asset import (
    EstablishKnowledgeAssetRequest,
    KnowledgeAssetResponse,
    TransitionKnowledgeAssetRequest,
)

_event_logger = logging.getLogger("aiservice.events")


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

    async def transition(
        self,
        organization_id: uuid.UUID,
        actor_id: uuid.UUID,
        knowledge_asset_id: uuid.UUID,
        request: TransitionKnowledgeAssetRequest,
    ) -> KnowledgeAssetResponse:
        """WP-14 BA-04 Increment (`TDS-014 §3`/`§5`/`§6`/`§9`)."""
        asset = await self.repo.get_by_id_for_caller(organization_id, knowledge_asset_id)
        if asset is None:
            record_audit(
                action="TRANSITION_KNOWLEDGE_ASSET",
                resource=f"knowledge_asset:{knowledge_asset_id}",
                status=AuditStatus.DENIED,
                actor_id=str(actor_id),
                tenant_id=str(organization_id),
                metadata={"reason": "knowledge asset not found or not visible to this organization"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Knowledge Asset with that id is visible to your own Organization.",
            )

        # TDS-014 §6 / BA04-INC-DEC-004: the atomic UPDATE...WHERE guard is
        # the sole concurrency mechanism — no prior Python-level state
        # check is relied upon for correctness (the 404 check above reads
        # only to distinguish "does not exist" from "exists but not
        # PROPOSED," a distinction the guard itself cannot make, since a
        # non-matching UPDATE is silent on which reason caused it).
        claimed = await self.repo.claim_transition(
            organization_id, knowledge_asset_id, target_status=request.target_status
        )
        if not claimed:
            record_audit(
                action="TRANSITION_KNOWLEDGE_ASSET",
                resource=f"knowledge_asset:{knowledge_asset_id}",
                status=AuditStatus.DENIED,
                actor_id=str(actor_id),
                tenant_id=str(organization_id),
                metadata={"reason": "not currently PROPOSED", "requested_target": request.target_status},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This Knowledge Asset is not currently PROPOSED — it may already have been transitioned.",
            )

        # SQLAlchemy's default ORM-enabled UPDATE synchronization ("evaluate")
        # updates this already-loaded `asset` instance's own `curation_status`
        # in place, since the WHERE clause above is fully Python-evaluable —
        # the same mechanism BA-03's own claim_for_resolution relies on. No
        # second SELECT is needed to reflect the new state in the response.

        # Gate 1 F-01 remediation: TDS-014 §11's own frozen SUCCESS audit
        # metadata shape includes `event_id` for the ACCEPTED case
        # ("... if target_status == 'ACCEPTED' else None"). The event must
        # therefore be *constructed* (a pure, in-memory operation — no I/O,
        # no broker contact) before the audit call below, so its own
        # `event_id` is known at audit time. This is unrelated to, and does
        # not weaken, the DB-commit-before-PUBLISH-ATTEMPT invariant (§9)
        # — that invariant governs the `publish()` call specifically
        # (still strictly after this construction, still strictly after
        # the already-committed claim_transition() above), never
        # construction of the event object itself.
        event = (
            self._build_accepted_event(
                knowledge_asset_id=knowledge_asset_id, organization_id=organization_id, actor_id=actor_id
            )
            if request.target_status == "ACCEPTED"
            else None
        )

        record_audit(
            action="TRANSITION_KNOWLEDGE_ASSET",
            resource=f"knowledge_asset:{knowledge_asset_id}",
            status=AuditStatus.SUCCESS,
            actor_id=str(actor_id),
            tenant_id=str(organization_id),
            metadata={
                "from_status": "PROPOSED",
                "to_status": request.target_status,
                "event_id": event.event_id if event is not None else None,
            },
        )

        if event is not None:
            # TDS-014 §9 / RO-DEC-BA04-INC-007: the transition above has
            # already committed (claim_transition's own internal commit) —
            # this publish attempt strictly follows that commit, never
            # precedes it. Best-effort only: a publish failure does not
            # roll back the already-committed ACCEPTED state, is not
            # retried, and is disclosed via a structured log entry.
            await self._publish_accepted_event(
                event, knowledge_asset_id=knowledge_asset_id, organization_id=organization_id
            )

        return KnowledgeAssetResponse.model_validate(asset)

    def _build_accepted_event(
        self, *, knowledge_asset_id: uuid.UUID, organization_id: uuid.UUID, actor_id: uuid.UUID
    ) -> KnowledgeAssetAcceptedEvent:
        """
        TDS-014 §8/§11 — construct (never publish) the one
        `KnowledgeAssetAcceptedEvent` for a winning `ACCEPTED` transition.
        Pure, synchronous, no I/O — `event.event_id` is available
        immediately for the SUCCESS audit record (Gate 1 F-01
        remediation), independent of whether the later publish attempt
        (`_publish_accepted_event`) succeeds.
        """
        from aurex.backend.shared.events.event_factory import EventFactory

        return EventFactory.create_custom_event(
            KnowledgeAssetAcceptedEvent,
            knowledge_asset_id=str(knowledge_asset_id),
            organization_id=str(organization_id),
            tenant_id=str(organization_id),
            correlation_id=CorrelationContext.get(),
            user_id=str(actor_id),
        )

    async def _publish_accepted_event(
        self, event: KnowledgeAssetAcceptedEvent, *, knowledge_asset_id: uuid.UUID, organization_id: uuid.UUID
    ) -> None:
        """
        TDS-014 §8/§9 — attempt to publish an already-constructed
        `KnowledgeAssetAcceptedEvent` (`_build_accepted_event`). At most
        one attempt (this method is reached only from the one winning
        `transition()` call, per §6's own guard). Never raises — a publish
        failure is caught, logged as an event-publication failure (not a
        failed Knowledge Asset transition, per `RO-DEC-BA04-INC-007`), and
        swallowed; no retry.
        """
        from aurex.backend.shared.events.event_publisher import KafkaEventPublisher

        # No live broker configuration exists anywhere in this repository
        # yet (TDS-014 §11/§14, RO-DEC-BA04-INC-007) — KafkaEventPublisher
        # itself is verified mock-only (its own real dispatch call is
        # commented out), so `bootstrap_servers` is never actually
        # connected to; this is disclosed, not a live configuration value.
        publisher = KafkaEventPublisher(service_name="aiservice", bootstrap_servers="mock-broker:9092")
        try:
            publisher.publish(event, destination="aiservice.knowledge-asset-events")
        except Exception as publish_error:  # noqa: BLE001 — best-effort per RO-DEC-BA04-INC-007, never re-raised
            _event_logger.error(
                "Event publication failed after successful ACCEPTED transition "
                "(knowledge_asset_id=%s, organization_id=%s, event_id=%s, correlation_id=%s): %s",
                knowledge_asset_id,
                organization_id,
                event.event_id,
                event.correlation_id,
                publish_error,
            )
