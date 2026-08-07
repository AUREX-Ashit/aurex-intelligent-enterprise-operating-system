# services/conversation_service.py
"""
WP-12 BA-01 — Establish and Manage Conversation Lifecycle (`IRA-012 §5`,
`TDS-012 §3`). Implements `ConversationService` (`IMP-001 §13.28`): owns
Conversation Boundary transitions, never executes an Interaction itself.
"""
from __future__ import annotations

import uuid

from fastapi import HTTPException, status

from observability import AuditStatus, record_audit
from repositories.conversation_repository import ConversationRepository
from schemas.conversation import ConversationResponse
from services.conversation_state_resolver import (
    ConversationStateResolver,
    ConversationTransitionTrigger,
    InvalidConversationTransition,
)


class ConversationService:
    """Business Activity orchestrator for BA-01."""

    def __init__(self, conversation_repo: ConversationRepository, state_resolver: ConversationStateResolver) -> None:
        self.conversation_repo = conversation_repo
        self.state_resolver = state_resolver

    async def establish(self, organization_id: uuid.UUID, established_by: uuid.UUID) -> ConversationResponse:
        instance = await self.conversation_repo.create(
            organization_id=organization_id, established_by=established_by
        )
        record_audit(
            action="ESTABLISH_CONVERSATION",
            resource=f"conversation:{instance.conversation_id}",
            status=AuditStatus.SUCCESS,
            actor_id=str(established_by),
            tenant_id=str(organization_id),
        )
        return ConversationResponse.model_validate(instance)

    async def close(self, organization_id: uuid.UUID, conversation_id: uuid.UUID) -> ConversationResponse:
        instance = await self.conversation_repo.get_by_id_for_caller(organization_id, conversation_id)
        if instance is None:
            record_audit(
                action="CLOSE_CONVERSATION",
                resource=f"conversation:{conversation_id}",
                status=AuditStatus.DENIED,
                tenant_id=str(organization_id),
                metadata={"reason": "conversation not found"},
            )
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found.")

        try:
            new_state = self.state_resolver.resolve(
                current_state=instance.state,
                target_state="CLOSED",
                trigger=ConversationTransitionTrigger.EXPLICIT_ACTION,
            )
        except InvalidConversationTransition as exc:
            record_audit(
                action="CLOSE_CONVERSATION",
                resource=f"conversation:{conversation_id}",
                status=AuditStatus.DENIED,
                tenant_id=str(organization_id),
                metadata={"reason": str(exc), "current_state": instance.state},
            )
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

        updated = await self.conversation_repo.transition_state(
            instance, new_state=new_state, reason=ConversationTransitionTrigger.EXPLICIT_ACTION.value
        )
        record_audit(
            action="CLOSE_CONVERSATION",
            resource=f"conversation:{updated.conversation_id}",
            status=AuditStatus.SUCCESS,
            tenant_id=str(organization_id),
        )
        return ConversationResponse.model_validate(updated)

    async def require_open(self, organization_id: uuid.UUID, conversation_id: uuid.UUID):
        """Used by BA-02 (`services/interaction_service.py`) to gate execution against a Closed Conversation. Returns the ORM instance, not a schema — internal use only."""
        instance = await self.require_exists(organization_id, conversation_id)
        if instance.state != "OPEN":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Conversation is {instance.state}, not OPEN — no further Interactions accepted.",
            )
        return instance

    async def require_exists(self, organization_id: uuid.UUID, conversation_id: uuid.UUID):
        """Used by BA-03 (`services/interaction_service.py`) to gate retrieval — a Closed Conversation's own Interactions remain retrievable, only cross-tenant access is denied. Returns the ORM instance, not a schema — internal use only."""
        instance = await self.conversation_repo.get_by_id_for_caller(organization_id, conversation_id)
        if instance is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found.")
        return instance
