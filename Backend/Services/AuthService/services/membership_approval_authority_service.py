"""
WP-18 — Bind and Resolve Approval Authority (C-003, repository-wide
infrastructure), realizing TDS-018's own `membership_approval_authority`
binding-management layer (§5-§7, §19, §26 step C).

Mirrors `ApprovalAuthorityService.establish()`'s own existing structural
pre-check + FK-existence-validation pattern (WP-02 BA-03) — the same
precedent TDS-018 §7/§19 explicitly names for this service's own
cross-Organization guard: a Membership may only be bound to an Approval
Authority belonging to the same Organization, enforced here at the
service layer (never a database trigger or CHECK constraint — TDS-018
§19's own recorded, not-yet-chosen options at design time; this
implementation selects the service-layer option, matching precedent).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status

from models.membership_approval_authority import MembershipApprovalAuthority
from repositories.approval_authority_repository import ApprovalAuthorityRepository
from repositories.membership_approval_authority_repository import MembershipApprovalAuthorityRepository
from repositories.membership_repository import MembershipRepository
from observability import record_audit, publish_event, AuditStatus


class MembershipApprovalAuthorityService:
    """Binding-management orchestrator for `membership_approval_authority` (WP-18)."""

    def __init__(
        self,
        binding_repo: MembershipApprovalAuthorityRepository,
        membership_repo: MembershipRepository,
        approval_authority_repo: ApprovalAuthorityRepository,
    ) -> None:
        self.binding_repo = binding_repo
        self.membership_repo = membership_repo
        self.approval_authority_repo = approval_authority_repo

    async def bind(
        self,
        membership_id: uuid.UUID,
        approval_authority_id: uuid.UUID,
        actor_id: str | None = None,
    ) -> MembershipApprovalAuthority:
        """
        Business operation: bind a Membership to an Approval Authority
        (TDS-018 §5-§7). Structural rules:
        - The target Membership must already exist (404 if not).
        - The target Approval Authority must already exist (404 if not).
        - Cross-Organization bindings are rejected (409) — TDS-018 §7's
          own disclosed gap, closed here.
        - An already-open binding for the identical pair is rejected
          (409) — a second bind attempt for an already-bound pair is a
          caller error to surface, not silently absorbed, mirroring
          `ApprovalAuthorityService`'s own no-silent-duplicate precedent.
        """
        membership = await self.membership_repo.get_by_id(membership_id)
        if membership is None:
            record_audit(
                action="BIND_APPROVAL_AUTHORITY",
                resource=f"membership:{membership_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "target membership does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No membership found with id '{membership_id}'.",
            )

        authority = await self.approval_authority_repo.get_by_id(approval_authority_id)
        if authority is None:
            record_audit(
                action="BIND_APPROVAL_AUTHORITY",
                resource=f"approval_authority:{approval_authority_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "target approval authority does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No approval authority found with id '{approval_authority_id}'.",
            )

        if membership.organization_id != authority.organization_id:
            record_audit(
                action="BIND_APPROVAL_AUTHORITY",
                resource=f"membership_approval_authority:{membership_id}:{approval_authority_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={
                    "reason": "cross-Organization binding rejected",
                    "membership_organization_id": str(membership.organization_id),
                    "approval_authority_organization_id": str(authority.organization_id),
                },
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Membership '{membership_id}' belongs to a different Organization than "
                    f"Approval Authority '{approval_authority_id}'; cross-Organization bindings are not permitted."
                ),
            )

        existing = await self.binding_repo.get_open_binding(membership_id, approval_authority_id)
        if existing is not None:
            record_audit(
                action="BIND_APPROVAL_AUTHORITY",
                resource=f"membership_approval_authority:{membership_id}:{approval_authority_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "an open binding for this pair already exists"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"An open binding already exists for membership '{membership_id}' "
                    f"and approval authority '{approval_authority_id}'."
                ),
            )

        binding = await self.binding_repo.create(
            {
                "membership_id": membership_id,
                "approval_authority_id": approval_authority_id,
            }
        )
        await self.binding_repo.session.flush()

        record_audit(
            action="BIND_APPROVAL_AUTHORITY",
            resource=f"membership_approval_authority:{membership_id}:{approval_authority_id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "membership_id": str(membership_id),
                "approval_authority_id": str(approval_authority_id),
                "effective_from": binding.effective_from.isoformat(),
            },
        )
        publish_event(
            "MEMBERSHIP_APPROVAL_AUTHORITY_BOUND",
            {
                "membership_id": str(membership_id),
                "approval_authority_id": str(approval_authority_id),
                "effective_from": binding.effective_from.isoformat(),
            },
        )
        return binding

    async def close(
        self,
        membership_id: uuid.UUID,
        approval_authority_id: uuid.UUID,
        actor_id: str | None = None,
    ) -> MembershipApprovalAuthority:
        """
        Business operation: close (deactivate) an open binding by setting
        `effective_to` — TDS-018 §9's own soft-close convention, never a
        hard delete.
        """
        existing = await self.binding_repo.get_open_binding(membership_id, approval_authority_id)
        if existing is None:
            record_audit(
                action="CLOSE_APPROVAL_AUTHORITY_BINDING",
                resource=f"membership_approval_authority:{membership_id}:{approval_authority_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "no open binding exists for this pair"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"No open binding exists for membership '{membership_id}' "
                    f"and approval authority '{approval_authority_id}'."
                ),
            )

        now = datetime.now(timezone.utc)
        existing.effective_to = now
        await self.binding_repo.session.flush()

        record_audit(
            action="CLOSE_APPROVAL_AUTHORITY_BINDING",
            resource=f"membership_approval_authority:{membership_id}:{approval_authority_id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"effective_to": now.isoformat()},
        )
        publish_event(
            "MEMBERSHIP_APPROVAL_AUTHORITY_CLOSED",
            {
                "membership_id": str(membership_id),
                "approval_authority_id": str(approval_authority_id),
                "effective_to": now.isoformat(),
            },
        )
        return existing
