"""
WP-05 -- Access Management (C-002).

Business Activities implemented here: BA-01 Evaluate Access for a
Governed Request (Unresolved/Deferred branches only), BA-02 Preserve
and Bound Access Evaluation Outcome Validity, BA-03 Detect and Resolve
Access Context Change (classification portion only), BA-04 Resolve
Dependent Capability Access Hand-off Rejection. See IRA-005 for the
full ERB/EX -> Business Activity mapping and IRA-005 S12 for this Work
Package's own authorized scope.

BA-01's own central purpose (producing Permitted/Denied outcomes)
requires a URA-001-76 precedence-chain resolver that exists nowhere in
this repository with a real TierResolver yet (WP-RTA-001's own Closure
Report S7, "Not production ready"). This module never fabricates a
Permitted/Denied determination -- per CLAUDE.md S19.8.5, a false
Permitted outcome is a security defect, not deferrable as ordinary
Technical Debt. Where a governed request would require that
determination, evaluate() raises HTTP 501 explicitly, rather than
silently declining or guessing.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException, status

from models.access_evaluation_outcome import AccessEvaluationOutcomeType, AccessEvaluationValidityStatus
from repositories.access_evaluation_outcome_repository import AccessEvaluationOutcomeRepository
from repositories.domain_repository import DomainRepository
from repositories.membership_repository import MembershipRepository
from schemas.access_evaluation import (
    AccessContextChangeOutcome,
    AccessHandoffRejectionClassification,
    AccessHandoffRejectionOutcome,
    DetectAccessContextChangeRequest,
    EvaluateAccessRequest,
    ReportAccessHandoffRejectionRequest,
)
from observability import record_audit, publish_event, AuditStatus

_LIVE_VALIDITY_STATUSES = {
    AccessEvaluationValidityStatus.CREATED.value,
    AccessEvaluationValidityStatus.PRESERVED.value,
}


class AccessEvaluationService:
    """Business Activity orchestrator for Access Evaluation Outcome (WP-05, BA-01 through BA-04)."""

    def __init__(
        self,
        outcome_repo: AccessEvaluationOutcomeRepository,
        membership_repo: MembershipRepository,
        domain_repo: DomainRepository,
    ) -> None:
        self.outcome_repo = outcome_repo
        self.membership_repo = membership_repo
        self.domain_repo = domain_repo

    # -----------------------------------------------------------------
    # BA-01 — Evaluate Access for a Governed Request
    # -----------------------------------------------------------------

    async def evaluate(self, request: EvaluateAccessRequest, actor_id: str | None = None):
        """
        Business Activity: Evaluate Access for a Governed Request (BA-01),
        Unresolved/Deferred branches only (IRA-005 S12).

        Structural rule: the target Domain AND the target Membership must
        already exist (404 if not) -- a governed request naming a
        nonexistent Domain or a nonexistent Membership is a malformed
        request, not a business outcome this Business Activity records
        (mirrors DomainPermissionService.establish()'s own structural
        pre-check). This is required, not stylistic: `membership_id` is a
        non-nullable foreign key on `access_evaluation_outcomes`
        (`models/access_evaluation_outcome.py`), so persisting an outcome
        anchored to a nonexistent Membership would violate that
        constraint on any FK-enforcing database (VV-AUDIT-WP-05 F-01).

        Business outcome, in order:
        1. Membership exists but is not ACTIVE -> UNRESOLVED (EX-C002-03:
           identity/membership standing cannot be confirmed). The
           Membership itself must be real -- see the structural rule
           above -- this branch covers a real Membership whose standing
           cannot be confirmed, not a phantom identifier.
        2. An ACTIVE, DOMAIN-scoped Approval Authority governing the
           requested Domain within the Membership's own Organization
           (VV-AUDIT-WP-05 F-02 -- the lookup is organization-scoped, not
           merely domain-scoped) -> DEFERRED (EX-C002-04: the request
           requires approval before resolution can proceed).
        3. Otherwise, resolving this request would require a
           Permitted/Denied determination -- explicitly out of this
           Work Package's own authorized scope. Raises 501, never a
           fabricated decision.
        """
        domain = await self.domain_repo.get_by_id(request.domain_id)
        if domain is None:
            record_audit(
                action="EVALUATE_ACCESS",
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
                action="EVALUATE_ACCESS",
                resource=f"membership:{request.membership_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "target membership does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No membership found with id '{request.membership_id}'.",
            )

        if membership.membership_status != "ACTIVE":
            reason = f"Membership standing is not ACTIVE (current standing: '{membership.membership_status}')."
            outcome = await self.outcome_repo.create(
                {
                    "membership_id": request.membership_id,
                    "domain_id": request.domain_id,
                    "permission_level": request.permission_level.value,
                    "outcome_type": AccessEvaluationOutcomeType.UNRESOLVED.value,
                    "reason": reason,
                }
            )
            await self.outcome_repo.session.flush()
            record_audit(
                action="EVALUATE_ACCESS",
                resource=f"access_evaluation_outcome:{outcome.id}",
                status=AuditStatus.SUCCESS,
                actor_id=actor_id or "SYSTEM",
                metadata={"outcome_type": outcome.outcome_type, "reason": reason},
            )
            publish_event(
                "ACCESS_EVALUATION_OUTCOME_CREATED",
                {"outcome_id": str(outcome.id), "outcome_type": outcome.outcome_type},
            )
            return outcome

        approval_authority = await self.outcome_repo.get_active_domain_approval_authority(
            request.domain_id, membership.organization_id
        )
        if approval_authority is not None:
            outcome = await self.outcome_repo.create(
                {
                    "membership_id": request.membership_id,
                    "domain_id": request.domain_id,
                    "permission_level": request.permission_level.value,
                    "outcome_type": AccessEvaluationOutcomeType.DEFERRED.value,
                    "reason": f"Governed by Approval Authority '{approval_authority.authority_name}' ({approval_authority.id}); resolution pending approval.",
                    "approval_authority_id": approval_authority.id,
                }
            )
            await self.outcome_repo.session.flush()
            record_audit(
                action="EVALUATE_ACCESS",
                resource=f"access_evaluation_outcome:{outcome.id}",
                status=AuditStatus.SUCCESS,
                actor_id=actor_id or "SYSTEM",
                metadata={"outcome_type": outcome.outcome_type, "approval_authority_id": str(approval_authority.id)},
            )
            publish_event(
                "ACCESS_EVALUATION_OUTCOME_CREATED",
                {"outcome_id": str(outcome.id), "outcome_type": outcome.outcome_type},
            )
            return outcome

        record_audit(
            action="EVALUATE_ACCESS",
            resource=f"membership:{request.membership_id}:domain:{request.domain_id}",
            status=AuditStatus.DENIED,
            actor_id=actor_id or "SYSTEM",
            metadata={"reason": "Permitted/Denied determination requires a URA-001-76 resolver not yet authorized for this Work Package (IRA-005 S12)"},
        )
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=(
                "Permitted/Denied determination is not implemented by this Work Package (IRA-005 S12) -- "
                "it requires a real URA-001-76 precedence-chain resolver, which does not yet exist in "
                "WP-RTA-001. This request cannot be silently approximated (CLAUDE.md S19.8.5)."
            ),
        )

    # -----------------------------------------------------------------
    # BA-02 — Preserve and Bound Access Evaluation Outcome Validity
    # -----------------------------------------------------------------

    async def preserve(self, outcome_id, actor_id: str | None = None):
        """
        Business Activity: Preserve Access Evaluation Outcome Within
        Governed Execution Scope (BA-02, EX-C002-05). CREATED -> PRESERVED.
        """
        outcome = await self._get_or_404(outcome_id, "PRESERVE_ACCESS_EVALUATION_OUTCOME", actor_id)
        if outcome.validity_status != AccessEvaluationValidityStatus.CREATED.value:
            record_audit(
                action="PRESERVE_ACCESS_EVALUATION_OUTCOME",
                resource=f"access_evaluation_outcome:{outcome.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "not CREATED", "current_status": outcome.validity_status},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Access Evaluation Outcome '{outcome_id}' is not CREATED (current: '{outcome.validity_status}'); only a newly-created outcome may be preserved.",
            )

        updated = await self.outcome_repo.update(outcome_id, {"validity_status": AccessEvaluationValidityStatus.PRESERVED.value})
        await self.outcome_repo.session.flush()
        record_audit(
            action="PRESERVE_ACCESS_EVALUATION_OUTCOME",
            resource=f"access_evaluation_outcome:{updated.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"validity_status": updated.validity_status},
        )
        publish_event("ACCESS_EVALUATION_OUTCOME_PRESERVED", {"outcome_id": str(updated.id)})
        return updated

    async def expire(self, outcome_id, actor_id: str | None = None):
        """
        Business Activity: Expire Access Evaluation Outcome at Scope
        Boundary (BA-02, EX-C002-06). PRESERVED -> EXPIRED. An explicit,
        caller-invoked action -- no automatic/time-based expiry is
        implemented (that would require a scheduler, a new architectural
        component out of this Work Package's own scope).
        """
        outcome = await self._get_or_404(outcome_id, "EXPIRE_ACCESS_EVALUATION_OUTCOME", actor_id)
        if outcome.validity_status != AccessEvaluationValidityStatus.PRESERVED.value:
            record_audit(
                action="EXPIRE_ACCESS_EVALUATION_OUTCOME",
                resource=f"access_evaluation_outcome:{outcome.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "not PRESERVED", "current_status": outcome.validity_status},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Access Evaluation Outcome '{outcome_id}' is not PRESERVED (current: '{outcome.validity_status}'); only a preserved outcome may expire.",
            )

        updated = await self.outcome_repo.update(outcome_id, {"validity_status": AccessEvaluationValidityStatus.EXPIRED.value})
        await self.outcome_repo.session.flush()
        record_audit(
            action="EXPIRE_ACCESS_EVALUATION_OUTCOME",
            resource=f"access_evaluation_outcome:{updated.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"validity_status": updated.validity_status},
        )
        publish_event("ACCESS_EVALUATION_OUTCOME_EXPIRED", {"outcome_id": str(updated.id)})
        return updated

    # -----------------------------------------------------------------
    # BA-03 — Detect and Resolve Access Context Change (classification only)
    # -----------------------------------------------------------------

    async def detect_context_change(
        self, outcome_id, request: DetectAccessContextChangeRequest, actor_id: str | None = None
    ) -> AccessContextChangeOutcome:
        """
        Business Activity: Detect and Resolve Access Context Change
        (BA-03, EX-C002-07), classification/detection portion only.

        A reported governing-fact change against a still-live outcome
        (CREATED or PRESERVED) always invalidates it -- the
        "re-resolve to a fresh determination" path is out of this Work
        Package's own scope (it re-enters BA-01's own excluded
        Permitted/Denied branches); the caller's own next step is a
        fresh BA-01 call, never auto-triggered here.
        """
        outcome = await self._get_or_404(outcome_id, "DETECT_ACCESS_CONTEXT_CHANGE", actor_id)
        if outcome.validity_status not in _LIVE_VALIDITY_STATUSES:
            record_audit(
                action="DETECT_ACCESS_CONTEXT_CHANGE",
                resource=f"access_evaluation_outcome:{outcome.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "outcome is not live", "current_status": outcome.validity_status},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Access Evaluation Outcome '{outcome_id}' is not live (current: '{outcome.validity_status}'); only a CREATED or PRESERVED outcome may be invalidated by a context change.",
            )

        now = datetime.now(timezone.utc)
        updated = await self.outcome_repo.update(
            outcome_id,
            {
                "validity_status": AccessEvaluationValidityStatus.INVALIDATED.value,
                "reason": f"{outcome.reason} | Invalidated: {request.changed_fact}",
            },
        )
        await self.outcome_repo.session.flush()
        record_audit(
            action="DETECT_ACCESS_CONTEXT_CHANGE",
            resource=f"access_evaluation_outcome:{updated.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"changed_fact": request.changed_fact},
        )
        publish_event(
            "ACCESS_EVALUATION_OUTCOME_INVALIDATED",
            {"outcome_id": str(updated.id), "changed_fact": request.changed_fact},
        )
        return AccessContextChangeOutcome(
            outcome_id=updated.id,
            invalidated=True,
            changed_fact=request.changed_fact,
            checked_at=now,
            re_evaluation_required=True,
        )

    # -----------------------------------------------------------------
    # BA-04 — Resolve Dependent Capability Access Hand-off Rejection
    # -----------------------------------------------------------------

    async def resolve_handoff_rejection(
        self, outcome_id, request: ReportAccessHandoffRejectionRequest, actor_id: str | None = None
    ) -> AccessHandoffRejectionOutcome:
        """
        Business Activity: Resolve Dependent Capability Access Hand-off
        Rejection (BA-04, EX-C002-08). Mirrors WP-02 BA-10's own
        classification pattern exactly: the outcome's own current
        validity_status is the classification basis, never the
        reporting capability's stated reason (Contract 5.6/5.7,
        "a signal, not an authority").
        """
        outcome = await self._get_or_404(outcome_id, "RESOLVE_ACCESS_HANDOFF_REJECTION", actor_id)
        now = datetime.now(timezone.utc)

        if outcome.validity_status in _LIVE_VALIDITY_STATUSES:
            classification = AccessHandoffRejectionClassification.CAPABILITY_SCOPED_INSUFFICIENCY
            object_preserved = True
            explanation = (
                f"Access Evaluation Outcome '{outcome.id}' is currently live (status: '{outcome.validity_status}') -- "
                "the rejection reflects the reporting capability's own scope, not a defect in this outcome."
            )
            routed_to = None
        else:
            classification = AccessHandoffRejectionClassification.INTEGRITY_SIGNAL
            object_preserved = False
            explanation = (
                f"Access Evaluation Outcome '{outcome.id}' is no longer live (status: '{outcome.validity_status}') -- "
                "the hand-off itself signals a genuine integrity concern, routed for re-evaluation."
            )
            routed_to = "BA-01 (Evaluate Access for a Governed Request)"

        record_audit(
            action="RESOLVE_ACCESS_HANDOFF_REJECTION",
            resource=f"access_evaluation_outcome:{outcome.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "reporting_capability": request.reporting_capability,
                "stated_reason": request.stated_reason,
                "classification": classification.value,
            },
        )
        publish_event(
            "ACCESS_HANDOFF_REJECTION_RESOLVED",
            {"outcome_id": str(outcome.id), "classification": classification.value},
        )
        return AccessHandoffRejectionOutcome(
            outcome_id=outcome.id,
            classification=classification,
            object_preserved=object_preserved,
            explanation=explanation,
            routed_to=routed_to,
            checked_at=now,
        )

    # -----------------------------------------------------------------
    # Shared
    # -----------------------------------------------------------------

    async def _get_or_404(self, outcome_id, action: str, actor_id: str | None):
        outcome = await self.outcome_repo.get_by_id(outcome_id)
        if outcome is None:
            record_audit(
                action=action,
                resource=f"access_evaluation_outcome:{outcome_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "access evaluation outcome not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Access Evaluation Outcome found with id '{outcome_id}'.",
            )
        return outcome
