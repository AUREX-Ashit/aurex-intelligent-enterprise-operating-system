"""
WP-02 — Role & Permission Management (C-003).

Business Activity implemented here: BA-02 Establish Domain Permission,
realizing PE-001-C003's ERB-C003-01 (Define Authorization Policy
Structure) / EX-C003-02 (Establish Domain Permission). See IRA-002 for
the full ERB/EX -> Business Activity mapping.

Follows RoleService.establish()'s exact pattern (WP-02 BA-01):
structural pre-checks, duplicate-check-then-create, record_audit /
publish_event for SD-002-054's seven audit questions and RTA-001 §4.13
Domain Event Publication.

BR-C003-02 (a Domain Permission is never an implicit consequence of a
Business Role) is satisfied by construction: this method never reads or
writes `roles`/`role_permissions` — a Domain Permission is anchored only
to a Membership and a Domain.

Authorization disposition (mirrors IRA-002 §2.7's BA-01 precedent
exactly): PE-001-C003's EX-C003-02 requires confirmed Domain Owner/Domain
Admin authority (URA-001-45/-46) for the target Domain. No such
relationship is modeled anywhere in this codebase — Domain (AMD-014) was
deliberately built as ownership-free reference data. This method
therefore gates on the same interim PLATFORM_ADMIN dependency BA-01
already uses, disclosed here as a stated simplification (not a silent
gap) and recorded as technical debt (TD-022), pending a future,
separately-scoped Domain Owner/Admin authority model.
"""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models.domain_permission import DomainPermission
from repositories.domain_permission_repository import DomainPermissionRepository
from repositories.domain_repository import DomainRepository
from repositories.membership_repository import MembershipRepository
from schemas.domain_permission import EstablishDomainPermissionRequest
from observability import record_audit, publish_event, AuditStatus


class DomainPermissionService:
    """Business Activity orchestrator for Domain Permission establishment (WP-02 BA-02)."""

    def __init__(
        self,
        domain_permission_repo: DomainPermissionRepository,
        domain_repo: DomainRepository,
        membership_repo: MembershipRepository,
    ) -> None:
        self.domain_permission_repo = domain_permission_repo
        self.domain_repo = domain_repo
        self.membership_repo = membership_repo

    async def establish(
        self, request: EstablishDomainPermissionRequest, actor_id: str | None = None
    ) -> DomainPermission:
        """
        Business Activity: Establish Domain Permission (BA-02).

        Structural rules (BR-C003-01, EX-C003-02 Entry Context):
        - The target Domain must already exist (404 if not — "the target
          Domain, already established").
        - The target Membership must already exist (404 if not — a grant
          anchored to nothing is not a valid structural state).
        - permission_level is one of URA-001-47's eight values (enforced
          by EstablishDomainPermissionRequest's DomainPermissionLevel type
          before this method is ever reached — a 422, not a service-layer
          check).
        - No duplicate currently-active grant of the same
          (membership, domain, permission_level) triple (409) — the same
          duplicate-prevention discipline BA-01/OrganizationService.establish()
          already apply to their own natural keys.
        """
        domain = await self.domain_repo.get_by_id(request.domain_id)
        if domain is None:
            record_audit(
                action="ESTABLISH_DOMAIN_PERMISSION",
                resource=f"domain:{request.domain_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "target domain does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No domain found with id '{request.domain_id}'.",
            )

        membership = await self.membership_repo.get_by_id(request.membership_id)
        if membership is None:
            record_audit(
                action="ESTABLISH_DOMAIN_PERMISSION",
                resource=f"membership:{request.membership_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "target membership does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No membership found with id '{request.membership_id}'.",
            )

        existing = await self.domain_permission_repo.get_active_grant(
            request.membership_id, request.domain_id, request.permission_level.value
        )
        if existing is not None:
            record_audit(
                action="ESTABLISH_DOMAIN_PERMISSION",
                resource=f"domain_permission:{request.membership_id}:{request.domain_id}:{request.permission_level.value}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "an active grant of this permission level already exists"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"An active '{request.permission_level.value}' Domain Permission already exists "
                    f"for this membership on this domain."
                ),
            )

        create_kwargs: dict = {
            "membership_id": request.membership_id,
            "domain_id": request.domain_id,
            "permission_level": request.permission_level.value,
        }
        if request.effective_from is not None:
            create_kwargs["effective_from"] = request.effective_from
        if request.effective_to is not None:
            create_kwargs["effective_to"] = request.effective_to

        try:
            domain_permission = await self.domain_permission_repo.create(create_kwargs)
            await self.domain_permission_repo.session.flush()
        except IntegrityError:
            # Closes the race window between the pre-check above and this
            # insert, same basis as RoleService.establish()/OrganizationService.establish().
            await self.domain_permission_repo.session.rollback()
            record_audit(
                action="ESTABLISH_DOMAIN_PERMISSION",
                resource=f"domain_permission:{request.membership_id}:{request.domain_id}:{request.permission_level.value}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "an active grant of this permission level already exists (concurrent creation)"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"An active '{request.permission_level.value}' Domain Permission already exists "
                    f"for this membership on this domain."
                ),
            )

        record_audit(
            action="ESTABLISH_DOMAIN_PERMISSION",
            resource=f"domain_permission:{domain_permission.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "membership_id": str(domain_permission.membership_id),
                "domain_id": str(domain_permission.domain_id),
                "permission_level": domain_permission.permission_level,
            },
        )
        publish_event(
            "DOMAIN_PERMISSION_ESTABLISHED",
            {
                "domain_permission_id": str(domain_permission.id),
                "membership_id": str(domain_permission.membership_id),
                "domain_id": str(domain_permission.domain_id),
                "permission_level": domain_permission.permission_level,
            },
        )
        return domain_permission
