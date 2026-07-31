"""
WP-08 BA-01 — Detect and Resolve Disrupted Identity Context (EX-C001-06,
PE-001-C001 v1.1/ERB-C001-04).

Read-only re-confirmation — no audit record or domain event, mirroring
OrganizationService.get_details()'s/PersonUnderstandingService.understand()'s
own precedent (WP-01/WP-07): a status check, not a governed action.

Re-resolves against C-006 (Person.is_active) rather than trusting the
last-known JWT claim state, per Contract 5.6: "SHALL NOT infer that a
disrupted or unresolved Identity Context remains valid absent a
freshly re-resolved, affirmative confirmation." RTA-001's own runtime
Identity Resolution capability is not consulted — its own reported
status is "where relevant" (conditional) per EX-C001-06's own Context
Required, and is not production ready (WP-RTA-001 Closure Report §7);
this service re-resolves the one signal that is available and
sufficient: current Person Context validity.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status

from repositories.identity_repository import IdentityRepository
from repositories.person_repository import PersonRepository
from schemas.identity import IdentityContextStatus, IdentityStatusResponse


class IdentityStatusService:
    """Business Activity orchestrator for Detect and Resolve Disrupted Identity Context (WP-08 BA-01)."""

    def __init__(self, identity_repo: IdentityRepository, person_repo: PersonRepository) -> None:
        self.identity_repo = identity_repo
        self.person_repo = person_repo

    async def refresh(self, identity_id: UUID) -> IdentityStatusResponse:
        identity = await self.identity_repo.get_by_id(identity_id)
        if identity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No identity found with id '{identity_id}'.",
            )

        person = await self.person_repo.get_by_id(identity.person_id)
        resolved_status = (
            IdentityContextStatus.CURRENT
            if person is not None and person.is_active
            else IdentityContextStatus.UNRESOLVED
        )

        return IdentityStatusResponse(
            identity_id=identity.id,
            person_id=identity.person_id,
            status=resolved_status,
            checked_at=datetime.now(timezone.utc),
        )
