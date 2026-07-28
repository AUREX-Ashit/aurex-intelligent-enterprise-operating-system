"""
WP-02 — Role & Permission Management (C-003).

Business Activity implemented here: BA-04 Establish Delegation Policy,
realizing PE-001-C003's ERB-C003-01 (Define Authorization Policy
Structure) / EX-C003-04 (Establish Delegation Policy). See IRA-002 for
the full ERB/EX -> Business Activity mapping.

Follows ApprovalAuthorityService.establish()'s exact pattern (WP-02
BA-03): structural existence pre-checks (organization, and domain where
scope_type is DOMAIN), record_audit / publish_event for SD-002-054's
seven audit questions and RTA-001 §4.13 Domain Event Publication.

This method establishes the governed, reusable Delegation Policy only —
never a delegation instance (delegator, delegatee, reason, concrete date
window). Those belong exclusively to delegation_registry, which
EX-C003-04 itself places outside this capability's boundary; nothing in
AuthService reads or writes it here (it is not yet implemented in this
codebase at all).

scope_type's own internal consistency (exactly one anchor populated per
scope_type) is validated at the request layer
(schemas/delegation_policy.py's model_validator) and re-enforced at the
database layer (ck_delegation_policies_scope_consistency) — this
service only needs to confirm the referenced Organization and, where
applicable, Domain actually exist.

Authorization disposition (mirrors IRA-002 §2.7's BA-01 precedent and
BA-02/BA-03's TD-022/TD-023 precedent exactly): PE-001-C003's EX-C003-04
requires confirmed Corporate Admin or Domain Owner authority. Neither
exists as a distinct, enforceable claim today (same ADR-002 and
Domain-is-ownership-free gaps as BA-01/BA-03 and BA-02 respectively).
This method therefore gates on the same interim PLATFORM_ADMIN
dependency, disclosed here as a stated simplification and recorded as
technical debt (TD-024).
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException, status

from models.delegation_policy import DelegationPolicy, DelegationScopeType, VersionStatus
from repositories.delegation_policy_repository import DelegationPolicyRepository
from repositories.domain_repository import DomainRepository
from repositories.organization_repository import OrganizationRepository
from schemas.delegation_policy import EstablishDelegationPolicyRequest, VersionDelegationPolicyRequest
from observability import record_audit, publish_event, AuditStatus


class DelegationPolicyService:
    """Business Activity orchestrator for Delegation Policy establishment (WP-02 BA-04)."""

    def __init__(
        self,
        delegation_policy_repo: DelegationPolicyRepository,
        organization_repo: OrganizationRepository,
        domain_repo: DomainRepository,
    ) -> None:
        self.delegation_policy_repo = delegation_policy_repo
        self.organization_repo = organization_repo
        self.domain_repo = domain_repo

    async def establish(
        self, request: EstablishDelegationPolicyRequest, actor_id: str | None = None
    ) -> DelegationPolicy:
        """
        Business Activity: Establish Delegation Policy (BA-04).

        Structural rules (BR-C003-01/03, EX-C003-04 Context Required):
        - The target Organization must already exist (404 if not —
          required for every scope, including ORGANIZATION).
        - Where scope_type is DOMAIN, the target Domain must already
          exist (404 if not — same discipline as BA-02/BA-03).
        - scope_type/domain_id/object_type/object_id/event_code's mutual
          consistency is validated before this method is ever reached
          (422, via EstablishDelegationPolicyRequest's model_validator).
        """
        organization = await self.organization_repo.get_by_id(request.organization_id)
        if organization is None:
            record_audit(
                action="ESTABLISH_DELEGATION_POLICY",
                resource=f"organization:{request.organization_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "target organization does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No organization found with id '{request.organization_id}'.",
            )

        if request.scope_type == DelegationScopeType.DOMAIN:
            domain = await self.domain_repo.get_by_id(request.domain_id)
            if domain is None:
                record_audit(
                    action="ESTABLISH_DELEGATION_POLICY",
                    resource=f"domain:{request.domain_id}",
                    status=AuditStatus.DENIED,
                    actor_id=actor_id or "SYSTEM",
                    metadata={"reason": "target domain does not exist"},
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No domain found with id '{request.domain_id}'.",
                )

        delegation_policy = await self.delegation_policy_repo.create(
            {
                "organization_id": request.organization_id,
                "policy_name": request.policy_name,
                "delegation_type": request.delegation_type,
                "scope_type": request.scope_type.value,
                "sub_delegation_allowed": request.sub_delegation_allowed,
                "domain_id": request.domain_id,
                "object_type": request.object_type,
                "object_id": request.object_id,
                "event_code": request.event_code,
            }
        )
        await self.delegation_policy_repo.session.flush()

        record_audit(
            action="ESTABLISH_DELEGATION_POLICY",
            resource=f"delegation_policy:{delegation_policy.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "organization_id": str(delegation_policy.organization_id),
                "policy_name": delegation_policy.policy_name,
                "delegation_type": delegation_policy.delegation_type,
                "scope_type": delegation_policy.scope_type,
                "sub_delegation_allowed": delegation_policy.sub_delegation_allowed,
            },
        )
        publish_event(
            "DELEGATION_POLICY_ESTABLISHED",
            {
                "delegation_policy_id": str(delegation_policy.id),
                "organization_id": str(delegation_policy.organization_id),
                "policy_name": delegation_policy.policy_name,
                "delegation_type": delegation_policy.delegation_type,
                "scope_type": delegation_policy.scope_type,
                "sub_delegation_allowed": delegation_policy.sub_delegation_allowed,
                "domain_id": str(delegation_policy.domain_id) if delegation_policy.domain_id else None,
                "object_type": delegation_policy.object_type,
                "object_id": str(delegation_policy.object_id) if delegation_policy.object_id else None,
                "event_code": delegation_policy.event_code,
            },
        )
        return delegation_policy

    async def create_new_version(
        self, delegation_policy_id, request: VersionDelegationPolicyRequest, actor_id: str | None = None
    ) -> DelegationPolicy:
        """
        Business Activity: Version and Re-effective-Date Authorization
        Policy Object (BA-07), applied to Delegation Policy.

        Structural rules (BR-C003-05, EX-C003-07 Context Required):
        - The target Delegation Policy must already exist and currently
          be ACTIVE (404 if it does not exist; 409 if the given id
          already names a SUPERSEDED, historical version).
        - The prior version is preserved, never mutated in place.
        - delegation_type and scope_type/domain_id/object_type/
          object_id/event_code are never amended here (structural rule
          conformance is outside EX-C003-07's own scope).
        """
        current = await self.delegation_policy_repo.get_by_id(delegation_policy_id)
        if current is None:
            record_audit(
                action="VERSION_DELEGATION_POLICY",
                resource=f"delegation_policy:{delegation_policy_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "target delegation policy does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No delegation policy found with id '{delegation_policy_id}'.",
            )

        if current.status != VersionStatus.ACTIVE.value:
            record_audit(
                action="VERSION_DELEGATION_POLICY",
                resource=f"delegation_policy:{delegation_policy_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "target delegation policy is not the current ACTIVE version"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Delegation policy '{delegation_policy_id}' is not the current ACTIVE version; version its current version instead.",
            )

        now = datetime.now(timezone.utc)
        current.status = VersionStatus.SUPERSEDED.value
        current.effective_to = now

        new_version = await self.delegation_policy_repo.create(
            {
                "organization_id": current.organization_id,
                "policy_name": request.policy_name if request.policy_name is not None else current.policy_name,
                "delegation_type": current.delegation_type,
                "scope_type": current.scope_type,
                "sub_delegation_allowed": request.sub_delegation_allowed if request.sub_delegation_allowed is not None else current.sub_delegation_allowed,
                "domain_id": current.domain_id,
                "object_type": current.object_type,
                "object_id": current.object_id,
                "event_code": current.event_code,
                "version": current.version + 1,
                "status": VersionStatus.ACTIVE.value,
                "effective_from": request.effective_from or now,
                "effective_to": request.effective_to,
                "approval_reference": request.approval_reference,
                "supersedes_id": current.id,
            }
        )
        await self.delegation_policy_repo.session.flush()

        record_audit(
            action="VERSION_DELEGATION_POLICY",
            resource=f"delegation_policy:{new_version.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"supersedes_id": str(current.id), "version": new_version.version},
        )
        publish_event(
            "DELEGATION_POLICY_VERSIONED",
            {
                "delegation_policy_id": str(new_version.id),
                "supersedes_id": str(current.id),
                "version": new_version.version,
                "policy_name": new_version.policy_name,
            },
        )
        return new_version

    async def deprecate(self, delegation_policy_id, actor_id: str | None = None) -> DelegationPolicy:
        """
        Business Activity: Deprecate or Retire Authorization Policy
        Object (BA-08), applied to Delegation Policy — Deprecate (Hide)
        branch. Mirrors ApprovalAuthorityService.deprecate()'s exact
        shape, including the same organization-ownership existence
        check.
        """
        policy = await self.delegation_policy_repo.get_by_id(delegation_policy_id)
        if policy is None:
            record_audit(
                action="DEPRECATE_DELEGATION_POLICY",
                resource=f"delegation_policy:{delegation_policy_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "delegation policy not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No delegation policy found with id '{delegation_policy_id}'.",
            )

        if policy.status != VersionStatus.ACTIVE.value:
            record_audit(
                action="DEPRECATE_DELEGATION_POLICY",
                resource=f"delegation_policy:{policy.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "delegation policy is not the current ACTIVE version", "current_status": policy.status},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Delegation policy '{delegation_policy_id}' is not the current ACTIVE version (status: {policy.status}); only an ACTIVE version may be deprecated.",
            )

        organization = await self.organization_repo.get_by_id(policy.organization_id)
        if organization is None:
            record_audit(
                action="DEPRECATE_DELEGATION_POLICY",
                resource=f"delegation_policy:{policy.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "owning organization no longer exists"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Delegation policy '{delegation_policy_id}' has no resolvable owning organization.",
            )

        if await self.delegation_policy_repo.has_active_dependents(policy.id):
            record_audit(
                action="DEPRECATE_DELEGATION_POLICY",
                resource=f"delegation_policy:{policy.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "BR-C003-04: active dependency remains unresolved"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"BR-C003-04 violated: Delegation policy '{delegation_policy_id}' has an active dependency "
                    "remaining unresolved; deprecation SHALL occur only once none remains."
                ),
            )

        previous_status = policy.status
        now = datetime.now(timezone.utc)
        updated = await self.delegation_policy_repo.update(
            delegation_policy_id, {"status": VersionStatus.DEPRECATED.value, "effective_to": now}
        )
        await self.delegation_policy_repo.session.flush()

        record_audit(
            action="DEPRECATE_DELEGATION_POLICY",
            resource=f"delegation_policy:{updated.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"previous_status": previous_status, "new_status": updated.status},
        )
        publish_event(
            "DELEGATION_POLICY_DEPRECATED",
            {"delegation_policy_id": str(updated.id), "previous_status": previous_status, "status": updated.status},
        )
        return updated

    async def retire(self, delegation_policy_id, actor_id: str | None = None) -> DelegationPolicy:
        """
        Business Activity: Deprecate or Retire Authorization Policy
        Object (BA-08), applied to Delegation Policy — Retire (Archive)
        branch, terminal. Mirrors deprecate()'s exact shape above.
        """
        policy = await self.delegation_policy_repo.get_by_id(delegation_policy_id)
        if policy is None:
            record_audit(
                action="RETIRE_DELEGATION_POLICY",
                resource=f"delegation_policy:{delegation_policy_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "delegation policy not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No delegation policy found with id '{delegation_policy_id}'.",
            )

        if policy.status != VersionStatus.ACTIVE.value:
            record_audit(
                action="RETIRE_DELEGATION_POLICY",
                resource=f"delegation_policy:{policy.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "delegation policy is not the current ACTIVE version", "current_status": policy.status},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Delegation policy '{delegation_policy_id}' is not the current ACTIVE version (status: {policy.status}); only an ACTIVE version may be retired.",
            )

        organization = await self.organization_repo.get_by_id(policy.organization_id)
        if organization is None:
            record_audit(
                action="RETIRE_DELEGATION_POLICY",
                resource=f"delegation_policy:{policy.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "owning organization no longer exists"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Delegation policy '{delegation_policy_id}' has no resolvable owning organization.",
            )

        if await self.delegation_policy_repo.has_active_dependents(policy.id):
            record_audit(
                action="RETIRE_DELEGATION_POLICY",
                resource=f"delegation_policy:{policy.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "BR-C003-04: active dependency remains unresolved"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"BR-C003-04 violated: Delegation policy '{delegation_policy_id}' has an active dependency "
                    "remaining unresolved; retirement SHALL occur only once none remains."
                ),
            )

        previous_status = policy.status
        now = datetime.now(timezone.utc)
        updated = await self.delegation_policy_repo.update(
            delegation_policy_id, {"status": VersionStatus.RETIRED.value, "effective_to": now}
        )
        await self.delegation_policy_repo.session.flush()

        record_audit(
            action="RETIRE_DELEGATION_POLICY",
            resource=f"delegation_policy:{updated.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"previous_status": previous_status, "new_status": updated.status},
        )
        publish_event(
            "DELEGATION_POLICY_RETIRED",
            {"delegation_policy_id": str(updated.id), "previous_status": previous_status, "status": updated.status},
        )
        return updated
