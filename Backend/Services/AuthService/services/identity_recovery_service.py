"""
WP-08 BA-02 — Recover Inaccessible Identity Context, self-service scope
(EX-C001-07, PE-001-C001 v1.1/ERB-C001-04).

Scoped to self-service recovery only (IRA-008 §4.5): the requesting
Person recovers their own Identity. Administrator-initiated recovery
on another Person's behalf is excluded pending the Access Evaluation
resolver IRA-008 §4.1 discloses as unavailable.

Confirms a currently valid Authoritative Person Context (C-006) exists,
determines the routing target (RE_RESOLUTION if the Person holds at
least one existing Identity record still on file, even if currently
unusable; NEW_IDENTITY otherwise), and records the request. Never
creates an Identity, never performs establishment (ERB-C001-01 is
excluded from WP-08's own scope) — "Experience Completion — Complete
once the Person is routed... those ERBs govern the substance of what
follows" (EX-C001-07).
"""

from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status

from repositories.identity_recovery_request_repository import IdentityRecoveryRequestRepository
from repositories.identity_repository import IdentityRepository
from repositories.person_repository import PersonRepository
from schemas.identity import IdentityRecoveryRequestResponse, RecoverIdentityRequest, RoutedPath
from observability import record_audit, publish_event, AuditStatus


class IdentityRecoveryService:
    """Business Activity orchestrator for Recover Inaccessible Identity Context, self-service (WP-08 BA-02)."""

    def __init__(
        self,
        recovery_repo: IdentityRecoveryRequestRepository,
        identity_repo: IdentityRepository,
        person_repo: PersonRepository,
    ) -> None:
        self.recovery_repo = recovery_repo
        self.identity_repo = identity_repo
        self.person_repo = person_repo

    async def request_recovery(
        self,
        request: RecoverIdentityRequest,
        requested_by_identity_id: UUID | None,
        actor_id: str | None = None,
    ) -> IdentityRecoveryRequestResponse:
        person = await self.person_repo.get_by_id(request.person_id)
        if person is None or not person.is_active:
            record_audit(
                action="RECOVER_IDENTITY",
                resource=f"person:{request.person_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "no currently valid Person Context"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No currently valid Person Context found for id '{request.person_id}'.",
            )

        existing_identities = await self.identity_repo.get_person_identities(request.person_id)
        routed_path = RoutedPath.RE_RESOLUTION if existing_identities else RoutedPath.NEW_IDENTITY

        recovery = await self.recovery_repo.create({
            "person_id": request.person_id,
            "requested_by_identity_id": requested_by_identity_id,
            "reason": request.reason,
            "routed_path": routed_path.value,
            "status": "PENDING",
        })
        await self.recovery_repo.session.flush()

        record_audit(
            action="RECOVER_IDENTITY",
            resource=f"person:{request.person_id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "recovery_request_id": str(recovery.id),
                "routed_path": routed_path.value,
            },
        )
        publish_event(
            "IDENTITY_RECOVERY_REQUESTED",
            {
                "recovery_request_id": str(recovery.id),
                "person_id": str(request.person_id),
                "routed_path": routed_path.value,
            },
        )

        return IdentityRecoveryRequestResponse(
            id=recovery.id,
            person_id=recovery.person_id,
            routed_path=routed_path,
            status=recovery.status,
            created_at=recovery.created_at,
        )
