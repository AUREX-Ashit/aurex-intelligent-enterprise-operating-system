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

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models.role import Role
from repositories.role_repository import RoleRepository
from schemas.role import EstablishRoleRequest
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
