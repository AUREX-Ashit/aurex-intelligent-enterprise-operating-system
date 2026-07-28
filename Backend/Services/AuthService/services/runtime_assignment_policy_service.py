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

from fastapi import HTTPException, status

from models.runtime_assignment_policy import RuntimeAssignmentPolicy
from repositories.runtime_assignment_policy_repository import RuntimeAssignmentPolicyRepository
from repositories.organization_repository import OrganizationRepository
from schemas.runtime_assignment_policy import EstablishRuntimeAssignmentPolicyRequest, DEFAULT_LIFECYCLE_STATES
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
