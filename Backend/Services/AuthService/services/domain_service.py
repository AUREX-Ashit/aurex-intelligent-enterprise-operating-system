"""
AMD-014 — Domain reference/master-data lookup capability.

Implements the reference catalog and lookup support WP-02 BA-02 depends
on (PE-001-C003 EX-C003-02's Entry Context: "the target Domain, already
established"). Domain is reference data (URA-001 §4), seeded via
MDP-001 §B2a — this is deliberately not a Business Activity: there is no
establish()/lifecycle method here, matching AMD-014's own scope boundary
and the instruction that the Domain Registry supports BA-02 rather than
introducing a new Enterprise Experience of its own.
"""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from fastapi import HTTPException, status

from models.domain import Domain
from repositories.domain_repository import DomainRepository


class DomainService:
    """Read-only lookup orchestrator for the Domain reference catalog."""

    def __init__(self, domain_repo: DomainRepository) -> None:
        self.domain_repo = domain_repo

    async def list_domains(self, organization_id: UUID | None) -> Sequence[Domain]:
        return await self.domain_repo.list_visible(organization_id)

    async def get_details(self, domain_id: UUID) -> Domain:
        """
        Resolves a single Domain by id — 404 on unknown id, no audit/event
        (read-only lookup, same precedent as OrganizationService.get_details).
        """
        domain = await self.domain_repo.get_by_id(domain_id)
        if domain is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No domain found with id '{domain_id}'.",
            )
        return domain
