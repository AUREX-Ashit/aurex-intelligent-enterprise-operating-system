# services/search_index_service.py
"""
WP-11 BA-01 — Establish Enterprise Search Index Configuration
(`IRA-011 §5`). Writes/lists `vector_index_registry` (AMD-012, LOCKED).
Gated by `PLATFORM_ADMIN` at the router (establish) — no dedicated
persona exists yet (`PE-001-C093` names none), same interim measure this
repository already uses platform-wide (`TD-021`-class).
"""
from __future__ import annotations

import uuid

from fastapi import HTTPException, status

from repositories.search_repository import VectorIndexRegistryRepository
from schemas.search import (
    EstablishIndexConfigurationRequest,
    IndexConfigurationListResponse,
    IndexConfigurationResponse,
)


class SearchIndexConfigurationService:
    """Business Activity orchestrator for BA-01."""

    def __init__(self, index_repo: VectorIndexRegistryRepository) -> None:
        self.index_repo = index_repo

    async def establish(
        self, organization_id: uuid.UUID, request: EstablishIndexConfigurationRequest
    ) -> IndexConfigurationResponse:
        target_organization_id = None if request.platform_wide else organization_id

        # VV-AUDIT-WP-11 Finding 1 (High, remediated): AMD-012 declares no
        # uniqueness constraint on (organization_id, index_name), and
        # VectorIndexRegistryRepository.get_by_name_for_caller's own
        # .scalar_one_or_none() raises MultipleResultsFound — an unhandled
        # 500 in BA-02/BA-03 — the moment a second active row shares a
        # scope. Rejected here, before creation, with a clean 409.
        existing = await self.index_repo.get_active_by_exact_scope(target_organization_id, request.index_name)
        if existing is not None:
            scope_description = "platform-wide" if target_organization_id is None else "your own organization's"
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"An active {scope_description} index named '{request.index_name}' already exists "
                    f"(vector_index_id={existing.vector_index_id}). Choose a different index_name."
                ),
            )

        instance = await self.index_repo.create(
            organization_id=target_organization_id,
            index_name=request.index_name,
            embedding_model=request.embedding_model,
            embedding_dimension=request.embedding_dimension,
            retrieval_mode=request.retrieval_mode,
            refresh_cadence=request.refresh_cadence,
        )
        return IndexConfigurationResponse.model_validate(instance)

    async def list_visible(self, organization_id: uuid.UUID) -> IndexConfigurationListResponse:
        rows = await self.index_repo.list_visible(organization_id)
        return IndexConfigurationListResponse(
            index_configurations=[IndexConfigurationResponse.model_validate(row) for row in rows]
        )
