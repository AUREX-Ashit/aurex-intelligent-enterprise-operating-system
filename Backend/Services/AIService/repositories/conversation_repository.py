# repositories/conversation_repository.py
"""
WP-12 — AI Conversation Management (C-094) repositories. Every read is
scoped to `organization_id == caller's own claim` — never an unscoped
lookup by a caller-supplied identifier, per `CLAUDE.md §21.4`(c). No
repository method here accepts a raw tenant identifier from the request
body; every caller-facing service method (`services/*.py`) passes the
caller's own JWT-derived `organization_id`.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.conversation import ConversationModel, InteractionModel


class ConversationRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def create(self, *, organization_id: uuid.UUID, established_by: uuid.UUID) -> ConversationModel:
        instance = ConversationModel(
            organization_id=organization_id,
            established_by=established_by,
            state="OPEN",
            state_transitioned_at=datetime.now(timezone.utc),
        )
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def get_by_id_for_caller(
        self, organization_id: uuid.UUID, conversation_id: uuid.UUID
    ) -> ConversationModel | None:
        """Scoped by id and tenant — never another tenant's Conversation (`CLAUDE.md §21.4`(c))."""
        query = select(ConversationModel).where(
            ConversationModel.conversation_id == conversation_id,
            ConversationModel.organization_id == organization_id,
        )
        return (await self.db.execute(query)).scalar_one_or_none()

    async def transition_state(
        self,
        instance: ConversationModel,
        *,
        new_state: str,
        reason: str,
    ) -> ConversationModel:
        """
        Applies a state transition already resolved by `ConversationStateResolver`
        (`ADR-020` Decision 2) — this method performs the write only; it does
        not itself decide whether the transition is valid. Callers MUST invoke
        the resolver first (`services/conversation_service.py`).
        """
        instance.state = new_state
        instance.state_transitioned_at = datetime.now(timezone.utc)
        instance.state_transition_reason = reason
        if new_state == "CLOSED":
            instance.closed_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance


class InteractionRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def next_sequence_number(self, conversation_id: uuid.UUID) -> int:
        query = select(InteractionModel.sequence_number).where(
            InteractionModel.conversation_id == conversation_id
        ).order_by(InteractionModel.sequence_number.desc()).limit(1)
        current_max = (await self.db.execute(query)).scalar_one_or_none()
        return 1 if current_max is None else current_max + 1

    async def create_pending(
        self,
        *,
        conversation_id: uuid.UUID,
        organization_id: uuid.UUID,
        business_activity_id: uuid.UUID,
        sequence_number: int,
        input_reference: str,
    ) -> InteractionModel:
        instance = InteractionModel(
            conversation_id=conversation_id,
            organization_id=organization_id,
            business_activity_id=business_activity_id,
            sequence_number=sequence_number,
            status="PENDING",
            input_reference=input_reference,
        )
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def list_for_conversation(
        self, *, conversation_id: uuid.UUID, organization_id: uuid.UUID
    ) -> list[InteractionModel]:
        """Ordered by sequence_number — identity, ordering, accountability preserved (`ADR-022` Decision 1). Tenant-scoped (`CLAUDE.md §21.4`)."""
        query = select(InteractionModel).where(
            InteractionModel.conversation_id == conversation_id,
            InteractionModel.organization_id == organization_id,
        ).order_by(InteractionModel.sequence_number.asc())
        return list((await self.db.execute(query)).scalars().all())

    async def complete(
        self,
        instance: InteractionModel,
        *,
        output_reference: str,
        confidence_score: int | None,
        evidence_reference: str | None,
    ) -> InteractionModel:
        """Applies the Reasoning Contract's own validated output (`RTA-001 §13.9c`) — called only after that validation succeeds, never before."""
        instance.status = "COMPLETE"
        instance.output_reference = output_reference
        instance.confidence_score = confidence_score
        instance.evidence_reference = evidence_reference
        instance.completed_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def mark_failed(self, instance: InteractionModel) -> InteractionModel:
        instance.status = "FAILED"
        instance.completed_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance
