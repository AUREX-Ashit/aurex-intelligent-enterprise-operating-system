"""
WP-01 — Organization Management (C-004).

Business Activities implemented here: BA-01 Establish Organization,
BA-02 View Organization Details.

Realizes CAP-001 C-004 per the ADR-003/ADR-004/ADR-005-scoped
implementation approved in IRA-001. Follows IMP-001 §6.3's Business
Activity Lifecycle (Request -> Validation -> Business Rule Execution ->
Business Object Update -> Domain Event Publication -> Audit Recording ->
Response) and reuses WP-00's established patterns exactly:
  - duplicate-check-then-create, mirroring EstablishPersonContextService
    (services/establish_person_context_service.py), strengthened here by
    also catching the database's own uq_organizations_organization_code
    constraint (Organization has a real natural-key constraint; Person
    does not), closing the concurrent-duplicate race that service's own
    docstring documents as intentionally open for Person.
  - observability.py's record_audit/publish_event/AuditStatus, exactly as
    bootstrap_service.py already uses them (SD-002-054's seven audit
    questions; RTA-001 §4.13 Domain Event Publication).
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models.organization import Organization, OrganizationStatus
from repositories.organization_repository import OrganizationRepository
from schemas.organization import EstablishOrganizationRequest
from observability import record_audit, publish_event, AuditStatus


class OrganizationService:
    """Business Activity orchestrator for Organization Management (WP-01)."""

    def __init__(self, organization_repo: OrganizationRepository) -> None:
        self.organization_repo = organization_repo

    async def establish(self, request: EstablishOrganizationRequest, actor_id: str | None = None) -> Organization:
        """
        Business Activity: Establish Organization.

        Business Rule: organization_code must be unique platform-wide
        (enforced both here, for a clean 409, and by the database's
        uq_organizations_organization_code constraint as a second line of
        defense against a concurrent duplicate request).
        """
        existing = await self.organization_repo.get_by_code(request.organization_code)
        if existing is not None:
            record_audit(
                action="ESTABLISH_ORGANIZATION",
                resource=f"organization:{request.organization_code}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization_code already exists"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"An organization with code '{request.organization_code}' already exists.",
            )

        try:
            organization = await self.organization_repo.create(
                {
                    "organization_code": request.organization_code,
                    "organization_name": request.organization_name,
                    "organization_type": request.organization_type,
                    "description": request.description,
                    "status": OrganizationStatus.ACTIVE.value,
                }
            )
            await self.organization_repo.session.flush()
        except IntegrityError:
            # Closes the race window between the pre-check above and this
            # insert: two concurrent requests for the same organization_code
            # can both pass the pre-check before either commits. The
            # database's unique constraint catches the second one here.
            await self.organization_repo.session.rollback()
            record_audit(
                action="ESTABLISH_ORGANIZATION",
                resource=f"organization:{request.organization_code}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization_code already exists (concurrent creation)"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"An organization with code '{request.organization_code}' already exists.",
            )

        record_audit(
            action="ESTABLISH_ORGANIZATION",
            resource=f"organization:{organization.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"organization_code": organization.organization_code},
        )
        publish_event(
            "ORGANIZATION_ESTABLISHED",
            {
                "organization_id": str(organization.id),
                "organization_code": organization.organization_code,
                "organization_name": organization.organization_name,
                "organization_type": organization.organization_type,
                "status": organization.status,
            },
        )
        return organization

    async def get_details(self, organization_id: UUID) -> Organization:
        """
        Business Activity: View Organization Details.

        Read-only — no audit record or domain event, on the same basis
        already established for Person's read-side Business Activity
        (PersonRecognitionService.recognize does not audit either; only
        the write path, establish, does). Reuses BaseRepository.get_by_id
        via OrganizationRepository as-is — no new repository method
        required.
        """
        organization = await self.organization_repo.get_by_id(organization_id)
        if organization is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No organization exists with id '{organization_id}'.",
            )
        return organization
