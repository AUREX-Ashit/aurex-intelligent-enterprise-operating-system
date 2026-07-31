"""
WP-07 BA-03 — Understand Authoritative Person Context (EX-C006-03,
PE-001-C006 §1.7/ERB-C006-02).

Read-only — no audit record or domain event, mirroring
OrganizationService.get_details()'s/StructuralCompletionService.get_details()'s
own precedent (WP-01/WP-04): "Read-only — no audit record or domain
event... no new repository method required."

Also structurally satisfies EX-C006-09 (Preserve Person Context Across
Enterprise Journeys) and, indirectly, EX-C006-12 (Continue from Person
Context Decision): a caller who already holds a person_id re-invokes
this same read rather than re-establishing, and every other WP-07
Business Activity's own response already returns the resulting Person
context directly — see IRA-007 §7.1/§7.2 for the full disclosed
reasoning (neither EX produces a distinct resource of its own for a
dedicated endpoint to expose, unlike WP-04's own RSC-000001).

Surfaces only boolean cross-capability existence signals (has_identity,
has_active_membership) — never Identity's or Membership's own data, per
PE-001-C006 §1.4's own Out-of-Scope boundary.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select, exists

from repositories.person_repository import PersonRepository
from schemas.person import PersonUnderstandingContext
from models.identity import Identity
from models.membership import Membership


class PersonUnderstandingService:
    """Business Activity orchestrator for Understand Authoritative Person Context (WP-07 BA-03)."""

    def __init__(self, person_repo: PersonRepository) -> None:
        self.person_repo = person_repo

    async def understand(self, person_id: UUID) -> PersonUnderstandingContext:
        person = await self.person_repo.get_by_id(person_id)
        if person is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No person found with id '{person_id}'.",
            )

        has_identity = await self.person_repo.session.scalar(
            select(exists().where(Identity.person_id == person_id))
        )
        has_active_membership = await self.person_repo.session.scalar(
            select(exists().where(
                Membership.person_id == person_id,
                Membership.membership_status == "ACTIVE",
            ))
        )

        return PersonUnderstandingContext(
            person_id=person.id,
            first_name=person.first_name,
            last_name=person.last_name,
            display_name=person.display_name,
            is_active=person.is_active,
            has_identity=bool(has_identity),
            has_active_membership=bool(has_active_membership),
        )
