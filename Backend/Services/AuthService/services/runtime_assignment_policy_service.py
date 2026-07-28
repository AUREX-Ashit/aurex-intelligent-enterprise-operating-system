"""
WP-02 — Role & Permission Management (C-003).

Business Activity implemented here: BA-05 Establish Runtime Assignment
Policy, realizing PE-001-C003's ERB-C003-01 (Define Authorization Policy
Structure) / EX-C003-05 (Establish Runtime Assignment Policy). See
IRA-002 for the full ERB/EX -> Business Activity mapping.

Follows DelegationPolicyService.establish()'s exact pattern (WP-02
BA-04): a single structural existence pre-check (organization),
record_audit / publish_event for SD-002-054's seven audit questions and
RTA-001 §4.13 Domain Event Publication.

This method establishes the governed, reusable Runtime Assignment Policy
only — never a Runtime Assignment instance (object/event anchor,
assignee, status, concrete effective_from/effective_to window). Those
belong exclusively to runtime_assignment_registry, which EX-C003-05
itself places outside this capability's boundary; nothing in AuthService
reads or writes it here (it is not yet implemented in this codebase at
all, the same disposition as delegation_registry at BA-04).

configured_lifecycle_states defaults to URA-001-78's nine canonical
states when the caller supplies none — the "default and configurable"
wording EX-C003-05's Context Required uses verbatim.

Authorization disposition (mirrors IRA-002 §2.7's BA-01 precedent and
BA-02/BA-03/BA-04's TD-022/TD-023/TD-024 precedent exactly): PE-001-C003's
EX-C003-05 requires confirmed Corporate Admin or Domain Admin authority.
Neither exists as a distinct, enforceable claim today (same ADR-002 and
Domain-is-ownership-free gaps as BA-01/BA-03/BA-04 and BA-02
respectively). This method therefore gates on the same interim
PLATFORM_ADMIN dependency, disclosed here as a stated simplification and
recorded as technical debt (TD-025).
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException, status

from models.runtime_assignment_policy import RuntimeAssignmentPolicy, VersionStatus
from repositories.runtime_assignment_policy_repository import RuntimeAssignmentPolicyRepository
from repositories.organization_repository import OrganizationRepository
from schemas.runtime_assignment_policy import (
    EstablishRuntimeAssignmentPolicyRequest,
    VersionRuntimeAssignmentPolicyRequest,
    DEFAULT_LIFECYCLE_STATES,
)
from observability import record_audit, publish_event, AuditStatus


class RuntimeAssignmentPolicyService:
    """Business Activity orchestrator for Runtime Assignment Policy establishment (WP-02 BA-05)."""

    def __init__(
        self,
        runtime_assignment_policy_repo: RuntimeAssignmentPolicyRepository,
        organization_repo: OrganizationRepository,
    ) -> None:
        self.runtime_assignment_policy_repo = runtime_assignment_policy_repo
        self.organization_repo = organization_repo

    async def establish(
        self, request: EstablishRuntimeAssignmentPolicyRequest, actor_id: str | None = None
    ) -> RuntimeAssignmentPolicy:
        """
        Business Activity: Establish Runtime Assignment Policy (BA-05).

        Structural rules (BR-C003-01/03, EX-C003-05 Context Required):
        - The target Organization must already exist (404 if not).
        - assignment_target_type is exactly one of URA-001-75's four
          values, enforced before this method is ever reached (422, via
          Pydantic's enum validation on EstablishRuntimeAssignmentPolicyRequest).
        - configured_lifecycle_states defaults to URA-001-78's nine
          canonical states when the caller supplies none.
        """
        organization = await self.organization_repo.get_by_id(request.organization_id)
        if organization is None:
            record_audit(
                action="ESTABLISH_RUNTIME_ASSIGNMENT_POLICY",
                resource=f"organization:{request.organization_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "target organization does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No organization found with id '{request.organization_id}'.",
            )

        configured_lifecycle_states = request.configured_lifecycle_states or list(DEFAULT_LIFECYCLE_STATES)

        runtime_assignment_policy = await self.runtime_assignment_policy_repo.create(
            {
                "organization_id": request.organization_id,
                "policy_name": request.policy_name,
                "assignment_target_type": request.assignment_target_type.value,
                "configured_lifecycle_states": configured_lifecycle_states,
                "escalation_policy_id": request.escalation_policy_id,
            }
        )
        await self.runtime_assignment_policy_repo.session.flush()

        record_audit(
            action="ESTABLISH_RUNTIME_ASSIGNMENT_POLICY",
            resource=f"runtime_assignment_policy:{runtime_assignment_policy.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "organization_id": str(runtime_assignment_policy.organization_id),
                "policy_name": runtime_assignment_policy.policy_name,
                "assignment_target_type": runtime_assignment_policy.assignment_target_type,
                "configured_lifecycle_states": runtime_assignment_policy.configured_lifecycle_states,
            },
        )
        publish_event(
            "RUNTIME_ASSIGNMENT_POLICY_ESTABLISHED",
            {
                "runtime_assignment_policy_id": str(runtime_assignment_policy.id),
                "organization_id": str(runtime_assignment_policy.organization_id),
                "policy_name": runtime_assignment_policy.policy_name,
                "assignment_target_type": runtime_assignment_policy.assignment_target_type,
                "configured_lifecycle_states": runtime_assignment_policy.configured_lifecycle_states,
                "escalation_policy_id": str(runtime_assignment_policy.escalation_policy_id)
                if runtime_assignment_policy.escalation_policy_id else None,
            },
        )
        return runtime_assignment_policy

    async def create_new_version(
        self, runtime_assignment_policy_id, request: VersionRuntimeAssignmentPolicyRequest, actor_id: str | None = None
    ) -> RuntimeAssignmentPolicy:
        """
        Business Activity: Version and Re-effective-Date Authorization
        Policy Object (BA-07), applied to Runtime Assignment Policy.

        Structural rules (BR-C003-05, EX-C003-07 Context Required):
        - The target Runtime Assignment Policy must already exist and
          currently be ACTIVE (404 if it does not exist; 409 if the
          given id already names a SUPERSEDED, historical version).
        - The prior version is preserved, never mutated in place.
        - assignment_target_type is never amended here (structural rule
          conformance is outside EX-C003-07's own scope).
        """
        current = await self.runtime_assignment_policy_repo.get_by_id(runtime_assignment_policy_id)
        if current is None:
            record_audit(
                action="VERSION_RUNTIME_ASSIGNMENT_POLICY",
                resource=f"runtime_assignment_policy:{runtime_assignment_policy_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "target runtime assignment policy does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No runtime assignment policy found with id '{runtime_assignment_policy_id}'.",
            )

        if current.status != VersionStatus.ACTIVE.value:
            record_audit(
                action="VERSION_RUNTIME_ASSIGNMENT_POLICY",
                resource=f"runtime_assignment_policy:{runtime_assignment_policy_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "target runtime assignment policy is not the current ACTIVE version"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Runtime assignment policy '{runtime_assignment_policy_id}' is not the current ACTIVE version; version its current version instead.",
            )

        now = datetime.now(timezone.utc)
        current.status = VersionStatus.SUPERSEDED.value
        current.effective_to = now

        new_version = await self.runtime_assignment_policy_repo.create(
            {
                "organization_id": current.organization_id,
                "policy_name": request.policy_name if request.policy_name is not None else current.policy_name,
                "assignment_target_type": current.assignment_target_type,
                "configured_lifecycle_states": (
                    request.configured_lifecycle_states
                    if request.configured_lifecycle_states is not None
                    else current.configured_lifecycle_states
                ),
                "escalation_policy_id": (
                    request.escalation_policy_id
                    if request.escalation_policy_id is not None
                    else current.escalation_policy_id
                ),
                "version": current.version + 1,
                "status": VersionStatus.ACTIVE.value,
                "effective_from": request.effective_from or now,
                "effective_to": request.effective_to,
                "approval_reference": request.approval_reference,
                "supersedes_id": current.id,
            }
        )
        await self.runtime_assignment_policy_repo.session.flush()

        record_audit(
            action="VERSION_RUNTIME_ASSIGNMENT_POLICY",
            resource=f"runtime_assignment_policy:{new_version.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"supersedes_id": str(current.id), "version": new_version.version},
        )
        publish_event(
            "RUNTIME_ASSIGNMENT_POLICY_VERSIONED",
            {
                "runtime_assignment_policy_id": str(new_version.id),
                "supersedes_id": str(current.id),
                "version": new_version.version,
                "policy_name": new_version.policy_name,
            },
        )
        return new_version

    async def deprecate(self, runtime_assignment_policy_id, actor_id: str | None = None) -> RuntimeAssignmentPolicy:
        """
        Business Activity: Deprecate or Retire Authorization Policy
        Object (BA-08), applied to Runtime Assignment Policy —
        Deprecate (Hide) branch. Mirrors
        ApprovalAuthorityService.deprecate()'s exact shape, including
        the same organization-ownership existence check.
        """
        policy = await self.runtime_assignment_policy_repo.get_by_id(runtime_assignment_policy_id)
        if policy is None:
            record_audit(
                action="DEPRECATE_RUNTIME_ASSIGNMENT_POLICY",
                resource=f"runtime_assignment_policy:{runtime_assignment_policy_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "runtime assignment policy not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No runtime assignment policy found with id '{runtime_assignment_policy_id}'.",
            )

        if policy.status != VersionStatus.ACTIVE.value:
            record_audit(
                action="DEPRECATE_RUNTIME_ASSIGNMENT_POLICY",
                resource=f"runtime_assignment_policy:{policy.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "runtime assignment policy is not the current ACTIVE version", "current_status": policy.status},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Runtime assignment policy '{runtime_assignment_policy_id}' is not the current ACTIVE version (status: {policy.status}); only an ACTIVE version may be deprecated.",
            )

        organization = await self.organization_repo.get_by_id(policy.organization_id)
        if organization is None:
            record_audit(
                action="DEPRECATE_RUNTIME_ASSIGNMENT_POLICY",
                resource=f"runtime_assignment_policy:{policy.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "owning organization no longer exists"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Runtime assignment policy '{runtime_assignment_policy_id}' has no resolvable owning organization.",
            )

        if await self.runtime_assignment_policy_repo.has_active_dependents(policy.id):
            record_audit(
                action="DEPRECATE_RUNTIME_ASSIGNMENT_POLICY",
                resource=f"runtime_assignment_policy:{policy.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "BR-C003-04: active dependency remains unresolved"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"BR-C003-04 violated: Runtime assignment policy '{runtime_assignment_policy_id}' has an active "
                    "dependency remaining unresolved; deprecation SHALL occur only once none remains."
                ),
            )

        previous_status = policy.status
        now = datetime.now(timezone.utc)
        updated = await self.runtime_assignment_policy_repo.update(
            runtime_assignment_policy_id, {"status": VersionStatus.DEPRECATED.value, "effective_to": now}
        )
        await self.runtime_assignment_policy_repo.session.flush()

        record_audit(
            action="DEPRECATE_RUNTIME_ASSIGNMENT_POLICY",
            resource=f"runtime_assignment_policy:{updated.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"previous_status": previous_status, "new_status": updated.status},
        )
        publish_event(
            "RUNTIME_ASSIGNMENT_POLICY_DEPRECATED",
            {"runtime_assignment_policy_id": str(updated.id), "previous_status": previous_status, "status": updated.status},
        )
        return updated

    async def retire(self, runtime_assignment_policy_id, actor_id: str | None = None) -> RuntimeAssignmentPolicy:
        """
        Business Activity: Deprecate or Retire Authorization Policy
        Object (BA-08), applied to Runtime Assignment Policy — Retire
        (Archive) branch, terminal. Mirrors deprecate()'s exact shape
        above.
        """
        policy = await self.runtime_assignment_policy_repo.get_by_id(runtime_assignment_policy_id)
        if policy is None:
            record_audit(
                action="RETIRE_RUNTIME_ASSIGNMENT_POLICY",
                resource=f"runtime_assignment_policy:{runtime_assignment_policy_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "runtime assignment policy not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No runtime assignment policy found with id '{runtime_assignment_policy_id}'.",
            )

        if policy.status != VersionStatus.ACTIVE.value:
            record_audit(
                action="RETIRE_RUNTIME_ASSIGNMENT_POLICY",
                resource=f"runtime_assignment_policy:{policy.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "runtime assignment policy is not the current ACTIVE version", "current_status": policy.status},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Runtime assignment policy '{runtime_assignment_policy_id}' is not the current ACTIVE version (status: {policy.status}); only an ACTIVE version may be retired.",
            )

        organization = await self.organization_repo.get_by_id(policy.organization_id)
        if organization is None:
            record_audit(
                action="RETIRE_RUNTIME_ASSIGNMENT_POLICY",
                resource=f"runtime_assignment_policy:{policy.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "owning organization no longer exists"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Runtime assignment policy '{runtime_assignment_policy_id}' has no resolvable owning organization.",
            )

        if await self.runtime_assignment_policy_repo.has_active_dependents(policy.id):
            record_audit(
                action="RETIRE_RUNTIME_ASSIGNMENT_POLICY",
                resource=f"runtime_assignment_policy:{policy.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "BR-C003-04: active dependency remains unresolved"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"BR-C003-04 violated: Runtime assignment policy '{runtime_assignment_policy_id}' has an active "
                    "dependency remaining unresolved; retirement SHALL occur only once none remains."
                ),
            )

        previous_status = policy.status
        now = datetime.now(timezone.utc)
        updated = await self.runtime_assignment_policy_repo.update(
            runtime_assignment_policy_id, {"status": VersionStatus.RETIRED.value, "effective_to": now}
        )
        await self.runtime_assignment_policy_repo.session.flush()

        record_audit(
            action="RETIRE_RUNTIME_ASSIGNMENT_POLICY",
            resource=f"runtime_assignment_policy:{updated.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"previous_status": previous_status, "new_status": updated.status},
        )
        publish_event(
            "RUNTIME_ASSIGNMENT_POLICY_RETIRED",
            {"runtime_assignment_policy_id": str(updated.id), "previous_status": previous_status, "status": updated.status},
        )
        return updated
