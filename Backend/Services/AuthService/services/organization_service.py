"""
WP-01 — Organization Management (C-004).

Business Activities implemented here: BA-01 Establish Organization,
BA-02 View Organization Details, BA-03 Search & List Organizations,
BA-04 Update Organization Profile, BA-05 Activate Organization,
BA-06 Suspend Organization.

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

from typing import Sequence
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models.organization import Organization, OrganizationStatus
from repositories.organization_repository import OrganizationRepository
from schemas.organization import EstablishOrganizationRequest, UpdateOrganizationProfileRequest
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

    async def update_profile(
        self,
        organization_id: UUID,
        request: UpdateOrganizationProfileRequest,
        actor_id: str | None = None,
    ) -> Organization:
        """
        Business Activity: Update Organization Profile (BA-04).

        Preconditions: the organization must already exist (404 if not,
        same basis as get_details). Business Object Update touches only
        organization_name, organization_type, and description —
        organization_code and status (lifecycle) are out of this
        activity's scope (status belongs to the Activate/Suspend
        Business Activities, ADR-005).
        """
        organization = await self.organization_repo.update(
            organization_id,
            {
                "organization_name": request.organization_name,
                "organization_type": request.organization_type,
                "description": request.description,
            },
        )
        if organization is None:
            record_audit(
                action="UPDATE_ORGANIZATION_PROFILE",
                resource=f"organization:{organization_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No organization exists with id '{organization_id}'.",
            )

        await self.organization_repo.session.flush()

        record_audit(
            action="UPDATE_ORGANIZATION_PROFILE",
            resource=f"organization:{organization.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"organization_code": organization.organization_code},
        )
        publish_event(
            "ORGANIZATION_PROFILE_UPDATED",
            {
                "organization_id": str(organization.id),
                "organization_code": organization.organization_code,
                "organization_name": organization.organization_name,
                "organization_type": organization.organization_type,
            },
        )
        return organization

    async def activate(self, organization_id: UUID, actor_id: str | None = None) -> Organization:
        """
        Business Activity: Activate Organization (BA-05).

        Interim lifecycle model (ADR-005): a plain `status` transition,
        not yet the metadata-driven state machine SD-002-051 ultimately
        requires. Business Rule: only a SUSPENDED organization may be
        activated. Activating an already-ACTIVE organization is rejected
        with 409 rather than silently succeeding as a no-op — this keeps
        the interim state machine's transitions explicit, mirroring
        establish()'s duplicate-rejection precedent rather than inventing
        a new idempotent-success convention with no canonical basis.

        Does not touch organization_name/organization_type/description
        (BA-04's scope) or organization_code (immutable natural key).

        TD-012 resolution (BA-06): also syncs the legacy `is_active`
        boolean to `True` so it no longer silently diverges from
        `status` — see suspend()'s matching sync in the opposite
        direction.
        """
        organization = await self.organization_repo.get_by_id(organization_id)
        if organization is None:
            record_audit(
                action="ACTIVATE_ORGANIZATION",
                resource=f"organization:{organization_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No organization exists with id '{organization_id}'.",
            )

        if organization.status == OrganizationStatus.ACTIVE.value:
            record_audit(
                action="ACTIVATE_ORGANIZATION",
                resource=f"organization:{organization.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization already ACTIVE", "organization_code": organization.organization_code},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Organization '{organization_id}' is already ACTIVE.",
            )

        previous_status = organization.status
        updated = await self.organization_repo.update(
            organization_id, {"status": OrganizationStatus.ACTIVE.value, "is_active": True}
        )
        await self.organization_repo.session.flush()

        record_audit(
            action="ACTIVATE_ORGANIZATION",
            resource=f"organization:{updated.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "organization_code": updated.organization_code,
                "previous_status": previous_status,
                "new_status": updated.status,
            },
        )
        publish_event(
            "ORGANIZATION_ACTIVATED",
            {
                "organization_id": str(updated.id),
                "organization_code": updated.organization_code,
                "previous_status": previous_status,
                "status": updated.status,
            },
        )
        return updated

    async def suspend(self, organization_id: UUID, actor_id: str | None = None) -> Organization:
        """
        Business Activity: Suspend Organization (BA-06).

        Interim lifecycle model (ADR-005): mirrors activate()'s pattern
        in the opposite direction. Business Rule: only an ACTIVE
        organization may be suspended. Suspending an already-SUSPENDED
        organization is rejected with 409, the same explicit-transition
        precedent activate() established for BA-06 to follow.

        Does not touch organization_name/organization_type/description
        (BA-04's scope) or organization_code (immutable natural key).

        TD-012 resolution: also syncs the legacy `is_active` boolean to
        `False`, closing the divergence risk BA-05 flagged — `is_active`
        and `status` now always move together for both transitions.
        """
        organization = await self.organization_repo.get_by_id(organization_id)
        if organization is None:
            record_audit(
                action="SUSPEND_ORGANIZATION",
                resource=f"organization:{organization_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No organization exists with id '{organization_id}'.",
            )

        if organization.status == OrganizationStatus.SUSPENDED.value:
            record_audit(
                action="SUSPEND_ORGANIZATION",
                resource=f"organization:{organization.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization already SUSPENDED", "organization_code": organization.organization_code},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Organization '{organization_id}' is already SUSPENDED.",
            )

        previous_status = organization.status
        updated = await self.organization_repo.update(
            organization_id, {"status": OrganizationStatus.SUSPENDED.value, "is_active": False}
        )
        await self.organization_repo.session.flush()

        record_audit(
            action="SUSPEND_ORGANIZATION",
            resource=f"organization:{updated.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "organization_code": updated.organization_code,
                "previous_status": previous_status,
                "new_status": updated.status,
            },
        )
        publish_event(
            "ORGANIZATION_SUSPENDED",
            {
                "organization_id": str(updated.id),
                "organization_code": updated.organization_code,
                "previous_status": previous_status,
                "status": updated.status,
            },
        )
        return updated

    async def search(
        self,
        query: str | None,
        status_filter: str | None,
        skip: int,
        limit: int,
        sort_by: str,
        sort_order: str,
    ) -> tuple[Sequence[Organization], int]:
        """
        Business Activity: Search & List Organizations.

        Read-only, same basis as get_details — no audit record or domain
        event. Delegates filtering/sorting/counting entirely to
        OrganizationRepository.search(); this method's job is only to sit
        in the same Business Activity orchestration layer as establish()
        and get_details(), not to hold query logic itself (that stays in
        the repository, consistent with MembershipRepository's existing
        query methods).
        """
        return await self.organization_repo.search(
            query=query,
            status=status_filter,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
        )
