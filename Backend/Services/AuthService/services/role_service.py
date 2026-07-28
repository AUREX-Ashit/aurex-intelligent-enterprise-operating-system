"""
WP-02 — Role & Permission Management (C-003).

Business Activity implemented here: BA-01 Establish Business or System
Role, realizing PE-001-C003's ERB-C003-01 (Define Authorization Policy
Structure) / EX-C003-01 (Establish Business or System Role). See
IRA-002 for the full ERB/EX -> Business Activity mapping; BA-02 onward
are not yet implemented.

Follows OrganizationService.establish()'s exact pattern (WP-01):
duplicate-check-then-create, strengthened by also catching the
database's own uq role_code constraint (closing the same concurrent-
duplicate race organization_service.py documents), record_audit /
publish_event / AuditStatus for SD-002-054's seven audit questions and
RTA-001 §4.13 Domain Event Publication.

BR-C003-02 (a Role never automatically confers a Domain Permission,
Approval Authority, or Runtime Assignment) is satisfied by construction:
this method never writes to role_permissions or any other authorization
object table — it establishes exactly one Role row and nothing else.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models.role import Role, VersionStatus
from repositories.role_repository import RoleRepository
from schemas.role import EstablishRoleRequest, VersionRoleRequest
from observability import record_audit, publish_event, AuditStatus


class RoleService:
    """Business Activity orchestrator for Role & Permission Management (WP-02)."""

    def __init__(self, role_repo: RoleRepository) -> None:
        self.role_repo = role_repo

    async def establish(self, request: EstablishRoleRequest, actor_id: str | None = None) -> Role:
        """
        Business Activity: Establish Business or System Role (BA-01).

        Business Rule (BR-C003-01): role_code must be unique platform-wide
        (enforced both here, for a clean 409, and by the database's
        unique constraint on roles.role_code as a second line of defense
        against a concurrent duplicate request — mirrors
        OrganizationService.establish() exactly).
        """
        existing = await self.role_repo.get_by_code(request.role_code)
        if existing is not None:
            record_audit(
                action="ESTABLISH_ROLE",
                resource=f"role:{request.role_code}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "role_code already exists"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A role with code '{request.role_code}' already exists.",
            )

        try:
            role = await self.role_repo.create(
                {
                    "role_code": request.role_code,
                    "role_name": request.role_name,
                    "description": request.description,
                    "is_system_role": request.is_system_role,
                }
            )
            await self.role_repo.session.flush()
        except IntegrityError:
            # Closes the race window between the pre-check above and this
            # insert, same basis as OrganizationService.establish().
            await self.role_repo.session.rollback()
            record_audit(
                action="ESTABLISH_ROLE",
                resource=f"role:{request.role_code}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "role_code already exists (concurrent creation)"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A role with code '{request.role_code}' already exists.",
            )

        record_audit(
            action="ESTABLISH_ROLE",
            resource=f"role:{role.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"role_code": role.role_code, "is_system_role": role.is_system_role},
        )
        publish_event(
            "ROLE_ESTABLISHED",
            {
                "role_id": str(role.id),
                "role_code": role.role_code,
                "role_name": role.role_name,
                "is_system_role": role.is_system_role,
            },
        )
        return role

    async def create_new_version(
        self, role_id, request: VersionRoleRequest, actor_id: str | None = None
    ) -> Role:
        """
        Business Activity: Version and Re-effective-Date Authorization
        Policy Object (BA-07), applied to Role.

        Structural rules (BR-C003-05, EX-C003-07 Context Required):
        - The target Role must already exist and currently be ACTIVE
          (404 if it does not exist; 409 if the given id already names a
          SUPERSEDED, historical version — only the current version may
          be versioned again).
        - The prior version is preserved, never mutated in place: its
          effective_to is closed and its status becomes SUPERSEDED; a new
          row is created carrying the amendment, version + 1, and
          supersedes_id pointing at the row it replaces.
        - role_code and is_system_role are never amended here (identity
          and fundamental type are outside EX-C003-07's own scope).
        """
        current = await self.role_repo.get_by_id(role_id)
        if current is None:
            record_audit(
                action="VERSION_ROLE",
                resource=f"role:{role_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "target role does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No role found with id '{role_id}'.",
            )

        if current.status != VersionStatus.ACTIVE.value:
            record_audit(
                action="VERSION_ROLE",
                resource=f"role:{role_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "target role is not the current ACTIVE version"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Role '{role_id}' is not the current ACTIVE version; version its current version instead.",
            )

        now = datetime.now(timezone.utc)
        current.status = VersionStatus.SUPERSEDED.value
        current.effective_to = now

        try:
            new_version = await self.role_repo.create(
                {
                    "role_code": current.role_code,
                    "role_name": request.role_name if request.role_name is not None else current.role_name,
                    "description": request.description if request.description is not None else current.description,
                    "is_system_role": current.is_system_role,
                    "version": current.version + 1,
                    "status": VersionStatus.ACTIVE.value,
                    "effective_from": request.effective_from or now,
                    "effective_to": request.effective_to,
                    "approval_reference": request.approval_reference,
                    "supersedes_id": current.id,
                }
            )
            await self.role_repo.session.flush()
        except IntegrityError:
            # Closes a concurrent-double-amendment race against the same
            # role_id: two callers both reading the same ACTIVE current
            # row would both attempt to insert a new ACTIVE row sharing
            # role_code, which the partial unique index on
            # (role_code, status='ACTIVE') rejects as the second insert's
            # constraint violation — surfaced here as a clean 409 rather
            # than an unhandled 500, same basis as establish()'s own
            # concurrent-duplicate handling.
            await self.role_repo.session.rollback()
            record_audit(
                action="VERSION_ROLE",
                resource=f"role:{role_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "concurrent version amendment already superseded this role"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Role '{role_id}' was concurrently versioned by another request; re-fetch its current version and retry.",
            )

        record_audit(
            action="VERSION_ROLE",
            resource=f"role:{new_version.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "supersedes_id": str(current.id),
                "version": new_version.version,
            },
        )
        publish_event(
            "ROLE_VERSIONED",
            {
                "role_id": str(new_version.id),
                "supersedes_id": str(current.id),
                "version": new_version.version,
                "role_name": new_version.role_name,
            },
        )
        return new_version

    async def deprecate(self, role_id, actor_id: str | None = None) -> Role:
        """
        Business Activity: Deprecate or Retire Authorization Policy
        Object (BA-08), applied to Role — the Deprecate (Hide) branch.

        Mirrors OrganizationService.suspend()'s exact shape (WP-01
        BA-06): a plain, in-place status transition on the current row,
        never a new version row (that remains create_new_version()'s own
        mechanism, reused, not duplicated, per IMP-001 §13.17's
        governing rule that lifecycle/governance discipline is shared
        across specializations, not reinvented per type).

        Business Rules (BR-C003-04, EX-C003-08 Purpose):
        - Only the current ACTIVE version may be deprecated (404 if the
          Role does not exist; 409 if it is not ACTIVE — already
          SUPERSEDED, DEPRECATED, or RETIRED).
        - Deprecation is rejected (409, naming BR-C003-04 exactly) where
          any active dependent remains unresolved — for Role, a
          currently-ACTIVE Membership assigned this Role
          (RoleRepository.has_active_dependents()).
        """
        role = await self.role_repo.get_by_id(role_id)
        if role is None:
            record_audit(
                action="DEPRECATE_ROLE",
                resource=f"role:{role_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "role not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No role found with id '{role_id}'.",
            )

        if role.status != VersionStatus.ACTIVE.value:
            record_audit(
                action="DEPRECATE_ROLE",
                resource=f"role:{role.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "role is not the current ACTIVE version", "current_status": role.status},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Role '{role_id}' is not the current ACTIVE version (status: {role.status}); only an ACTIVE version may be deprecated.",
            )

        if await self.role_repo.has_active_dependents(role.id):
            record_audit(
                action="DEPRECATE_ROLE",
                resource=f"role:{role.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "BR-C003-04: active dependency (Membership) remains unresolved"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"BR-C003-04 violated: Role '{role_id}' has at least one active Membership still "
                    "assigned to it; deprecation SHALL occur only once no active dependency remains unresolved."
                ),
            )

        previous_status = role.status
        now = datetime.now(timezone.utc)
        updated = await self.role_repo.update(
            role_id, {"status": VersionStatus.DEPRECATED.value, "effective_to": now}
        )
        await self.role_repo.session.flush()

        record_audit(
            action="DEPRECATE_ROLE",
            resource=f"role:{updated.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"role_code": updated.role_code, "previous_status": previous_status, "new_status": updated.status},
        )
        publish_event(
            "ROLE_DEPRECATED",
            {
                "role_id": str(updated.id),
                "role_code": updated.role_code,
                "previous_status": previous_status,
                "status": updated.status,
            },
        )
        return updated

    async def retire(self, role_id, actor_id: str | None = None) -> Role:
        """
        Business Activity: Deprecate or Retire Authorization Policy
        Object (BA-08), applied to Role — the Retire (Archive) branch.

        Same shape as deprecate() above; RETIRED is terminal (no code
        path transitions away from it), the same discipline
        OrganizationService.activate()/suspend() already established for
        Organization's own RETIRED state (WP-01 BA-07).

        Business Rules (BR-C003-04, EX-C003-08 Purpose):
        - Only the current ACTIVE version may be retired (404 if the
          Role does not exist; 409 if it is not ACTIVE).
        - Retirement is rejected (409, naming BR-C003-04 exactly) where
          any active dependent remains unresolved.
        """
        role = await self.role_repo.get_by_id(role_id)
        if role is None:
            record_audit(
                action="RETIRE_ROLE",
                resource=f"role:{role_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "role not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No role found with id '{role_id}'.",
            )

        if role.status != VersionStatus.ACTIVE.value:
            record_audit(
                action="RETIRE_ROLE",
                resource=f"role:{role.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "role is not the current ACTIVE version", "current_status": role.status},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Role '{role_id}' is not the current ACTIVE version (status: {role.status}); only an ACTIVE version may be retired.",
            )

        if await self.role_repo.has_active_dependents(role.id):
            record_audit(
                action="RETIRE_ROLE",
                resource=f"role:{role.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "BR-C003-04: active dependency (Membership) remains unresolved"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"BR-C003-04 violated: Role '{role_id}' has at least one active Membership still "
                    "assigned to it; retirement SHALL occur only once no active dependency remains unresolved."
                ),
            )

        previous_status = role.status
        now = datetime.now(timezone.utc)
        updated = await self.role_repo.update(
            role_id, {"status": VersionStatus.RETIRED.value, "effective_to": now}
        )
        await self.role_repo.session.flush()

        record_audit(
            action="RETIRE_ROLE",
            resource=f"role:{updated.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"role_code": updated.role_code, "previous_status": previous_status, "new_status": updated.status},
        )
        publish_event(
            "ROLE_RETIRED",
            {
                "role_id": str(updated.id),
                "role_code": updated.role_code,
                "previous_status": previous_status,
                "status": updated.status,
            },
        )
        return updated
