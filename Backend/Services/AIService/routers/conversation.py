# routers/conversation.py
"""WP-12 — AI Conversation Management (C-094). BA-01 endpoints (`IRA-012 §5`, `TDS-012 §5`)."""
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_claims, require_platform_admin
from models.database import get_db
from repositories.conversation_repository import ConversationRepository, InteractionRepository
from schemas.conversation import (
    ConversationResponse,
    ExecuteInteractionRequest,
    InteractionListResponse,
    InteractionResponse,
)
from services.conversation_service import ConversationService
from services.conversation_state_resolver import ConversationStateResolver
from services.interaction_service import InteractionService
from services.interaction_state_assembler import InteractionStateAssembler

router = APIRouter(prefix="/conversations", tags=["AI Conversation Management"])


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_conversation_repo(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> ConversationRepository:
    return ConversationRepository(session)


async def get_interaction_repo(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> InteractionRepository:
    return InteractionRepository(session)


async def get_conversation_service(
    conversation_repo: Annotated[ConversationRepository, Depends(get_conversation_repo)],
) -> ConversationService:
    return ConversationService(conversation_repo, ConversationStateResolver())


async def get_interaction_service(
    interaction_repo: Annotated[InteractionRepository, Depends(get_interaction_repo)],
    conversation_service: Annotated[ConversationService, Depends(get_conversation_service)],
) -> InteractionService:
    return InteractionService(
        interaction_repo, conversation_service, InteractionStateAssembler(interaction_repo)
    )


# ---------------------------------------------------------------------------
# BA-01 — Establish and Manage Conversation Lifecycle
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
    description=(
        "Gated by PLATFORM_ADMIN — no dedicated persona exists yet for C-094 "
        "(TDS-012 §8, TD-candidate-E), same interim measure this repository "
        "already uses platform-wide."
    ),
)
async def establish_conversation(
    claims: Annotated[dict, Depends(require_platform_admin)],
    service: Annotated[ConversationService, Depends(get_conversation_service)],
) -> ConversationResponse:
    return await service.establish(
        organization_id=UUID(claims["organization_id"]),
        established_by=UUID(claims["person_id"]),
    )


@router.post(
    "/{conversation_id}/close",
    response_model=ConversationResponse,
    description="Gated by PLATFORM_ADMIN — same basis as establish_conversation's own gate.",
)
async def close_conversation(
    conversation_id: UUID,
    claims: Annotated[dict, Depends(require_platform_admin)],
    service: Annotated[ConversationService, Depends(get_conversation_service)],
) -> ConversationResponse:
    return await service.close(
        organization_id=UUID(claims["organization_id"]),
        conversation_id=conversation_id,
    )


# ---------------------------------------------------------------------------
# BA-02 — Execute Interaction
# ---------------------------------------------------------------------------

@router.post(
    "/{conversation_id}/interactions",
    response_model=InteractionResponse,
    status_code=status.HTTP_201_CREATED,
    description="Gated by PLATFORM_ADMIN — same basis as establish_conversation's own gate.",
)
async def execute_interaction(
    conversation_id: UUID,
    request: ExecuteInteractionRequest,
    claims: Annotated[dict, Depends(require_platform_admin)],
    service: Annotated[InteractionService, Depends(get_interaction_service)],
) -> InteractionResponse:
    return await service.execute(
        organization_id=UUID(claims["organization_id"]),
        conversation_id=conversation_id,
        business_activity_id=request.business_activity_id or uuid4(),
        input_text=request.input_text,
    )


# ---------------------------------------------------------------------------
# BA-03 — Retrieve Conversation
# ---------------------------------------------------------------------------

@router.get("/{conversation_id}/interactions", response_model=InteractionListResponse)
async def list_interactions(
    conversation_id: UUID,
    claims: Annotated[dict, Depends(get_current_claims)],
    service: Annotated[InteractionService, Depends(get_interaction_service)],
) -> InteractionListResponse:
    return await service.list_for_conversation(
        organization_id=UUID(claims["organization_id"]),
        conversation_id=conversation_id,
    )
