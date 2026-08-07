# services/interaction_service.py
"""
WP-12 BA-02 (Execute Interaction) / BA-03 (Retrieve Conversation)
(`IRA-012 §5`, `TDS-012 §3`). Implements `InteractionService` (`IMP-001
§13.28`) — wraps one AI Request Lifecycle execution; sole caller
permitted to read/write an Interaction's own record.

Disclosed, honest placeholder — not fabricated as real: no Reasoning
Engine is wired to a live model anywhere in this repository yet
(`reasoning_engine_registry` names no default model, per the AI
Configuration Traceability Matrix's own finding). This mirrors exactly
`WP-11`'s own precedent (`AzureSearchStubProvider`, later replaced by a
real-persistence-but-stubbed-ranking provider): real Conversation/
Interaction persistence, real tenant scoping, real ordering and
continuity assembly — the actual model invocation is a disclosed
placeholder, never presented as computed. `confidence_score` is left
`None`, never a fabricated number, per this repository's own
"never fabricate data to look more finished than they are" discipline
(`PRODUCT-MILESTONE-ROADMAP.md §7`).
"""
from __future__ import annotations

import uuid

from fastapi import HTTPException, status

from observability import AuditStatus, record_audit
from repositories.conversation_repository import InteractionRepository
from schemas.conversation import InteractionListResponse, InteractionResponse
from services.conversation_service import ConversationService
from services.interaction_state_assembler import InteractionStateAssembler

_PLACEHOLDER_NOTICE = (
    "No Reasoning Engine is configured in this environment (reasoning_engine_registry names no default model). "
    "This response is a disclosed placeholder, not a computed AI output."
)


class InteractionService:
    """Business Activity orchestrator for BA-02/BA-03."""

    def __init__(
        self,
        interaction_repo: InteractionRepository,
        conversation_service: ConversationService,
        state_assembler: InteractionStateAssembler,
    ) -> None:
        self.interaction_repo = interaction_repo
        self.conversation_service = conversation_service
        self.state_assembler = state_assembler

    async def execute(
        self,
        *,
        organization_id: uuid.UUID,
        conversation_id: uuid.UUID,
        business_activity_id: uuid.UUID,
        input_text: str,
    ) -> InteractionResponse:
        # Gate: Conversation must be OPEN. Raises 404/409 via ConversationService.require_open.
        try:
            await self.conversation_service.require_open(organization_id, conversation_id)
        except HTTPException as exc:
            record_audit(
                action="EXECUTE_INTERACTION",
                resource=f"conversation:{conversation_id}",
                status=AuditStatus.DENIED,
                tenant_id=str(organization_id),
                metadata={"reason": exc.detail, "http_status": exc.status_code},
            )
            raise

        # Continuity assembled from prior same-Conversation Interactions only
        # (ADR-020 Decision 4) — computed but not yet used by the placeholder
        # response below; wiring a real Reasoning Engine to consume it is
        # future work, not invented here.
        await self.state_assembler.assemble(conversation_id=conversation_id, organization_id=organization_id)

        sequence_number = await self.interaction_repo.next_sequence_number(conversation_id)
        instance = await self.interaction_repo.create_pending(
            conversation_id=conversation_id,
            organization_id=organization_id,
            business_activity_id=business_activity_id,
            sequence_number=sequence_number,
            input_reference=input_text,
        )

        try:
            instance = await self.interaction_repo.complete(
                instance,
                output_reference=_PLACEHOLDER_NOTICE,
                confidence_score=None,
                evidence_reference=None,
            )
        except Exception:
            await self.interaction_repo.mark_failed(instance)
            record_audit(
                action="EXECUTE_INTERACTION",
                resource=f"interaction:{instance.interaction_id}",
                status=AuditStatus.FAILED,
                tenant_id=str(organization_id),
                metadata={"conversation_id": str(conversation_id), "sequence_number": sequence_number},
            )
            raise

        record_audit(
            action="EXECUTE_INTERACTION",
            resource=f"interaction:{instance.interaction_id}",
            status=AuditStatus.SUCCESS,
            tenant_id=str(organization_id),
            metadata={"conversation_id": str(conversation_id), "sequence_number": sequence_number},
        )
        return InteractionResponse.model_validate(instance)

    async def list_for_conversation(
        self, organization_id: uuid.UUID, conversation_id: uuid.UUID
    ) -> InteractionListResponse:
        # Gate: Conversation must exist for this caller's own tenant. Raises 404 otherwise —
        # without this, a cross-tenant conversation_id would silently return an empty list
        # instead of denying the request (Mandatory Tenant-Isolation Test Checklist, CLAUDE.md §21.4(b)).
        await self.conversation_service.require_exists(organization_id, conversation_id)

        rows = await self.interaction_repo.list_for_conversation(
            conversation_id=conversation_id, organization_id=organization_id
        )
        return InteractionListResponse(interactions=[InteractionResponse.model_validate(row) for row in rows])
