"""
WP-02 — Role & Permission Management (C-003).

Business Activity implemented here: BA-09 Detect and Resolve
Authorization Policy Dependency Conflict, realizing PE-001-C003's
ERB-C003-03 (Resolve Authorization Policy Dependency Conflict and
Cross-Capability Hand-off) / EX-C003-09 (Detect and Resolve
Authorization Policy Dependency Conflict). See IRA-002 for the full
ERB/EX -> Business Activity mapping.

This is the single, reusable dependency-resolution mechanism this
Business Activity's own instruction requires, shared across all five
WP-02 authorization policy object types (Role, Domain Permission,
Approval Authority, Delegation Policy, Runtime Assignment Policy) —
one service, dispatched generically over whichever object instance and
repository the caller's own router already resolved (mirroring every
other WP-02 service's own established pattern of receiving
already-fetched objects and already-injected repositories, never
re-deriving them).

Scope boundary (Contract 5.1): this service never writes to Membership
or any other C-007-owned table. Reassignment/expiry resolution is
recorded as the proposing authority's own explicit statement (Contract
5.6: "reassignment, natural expiry, or an affirmative accepted break
stated by the proposing authority"), not performed here — the
underlying dependent's own state change remains that dependent's own
capability's concern, consumed as an already-resolved input the next
time detect_conflicts() is run.

Scope boundary (this Business Activity's own instruction): this service
determines whether a change is safe. It never itself deprecates or
retires (BA-08's own, already-implemented, untouched capability).

Reuses BR-C003-04's dependency check exactly as BA-08 already
implemented it (each repository's get_active_dependents(), which
has_active_dependents() itself now composes from, per WP-02 BA-09's own
refactor) — never a duplicate query.

Business Activity implemented here (added, additive only): BA-10
Resolve Dependent Capability Authorization Policy Hand-off Rejection,
realizing ERB-C003-03 / EX-C003-10. classify_handoff_rejection()
orchestrates BA-08's own status field and BA-09's own detect_conflicts()
— it introduces no new detection logic, per this Business Activity's
own instruction not to duplicate conflict detection or dependency
analysis, or create another dependency engine.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, status

from repositories.domain_repository import DomainRepository
from repositories.organization_repository import OrganizationRepository
from schemas.authorization_policy_conflict import (
    DependencyConflictReport,
    DependencyViolation,
    ResolutionType,
    ResolveDependencyConflictRequest,
)
from schemas.authorization_policy_handoff import (
    HandoffRejectionClassification,
    HandoffRejectionOutcome,
    ReportHandoffRejectionRequest,
)
from observability import record_audit, publish_event, AuditStatus


class AuthorizationPolicyConflictService:
    """
    Business Activity orchestrator for Dependency Conflict Detection and
    Resolution (WP-02 BA-09) and Dependent Capability Hand-off Rejection
    Classification (WP-02 BA-10). One instance, shared across every
    WP-02 router that needs it — each call receives the already-loaded
    object and its own repository, never re-deriving either.
    """

    def __init__(
        self,
        organization_repo: OrganizationRepository,
        domain_repo: DomainRepository,
    ) -> None:
        self.organization_repo = organization_repo
        self.domain_repo = domain_repo

    async def detect_conflicts(self, object_type: str, obj: Any, repo: Any) -> DependencyConflictReport:
        """
        Business Activity: Detect Authorization Policy Dependency
        Conflict (BA-09).

        Realizes EX-C003-09's Purpose: "Enumerates every currently-active
        dependent... never silently proceeding" and this Business
        Activity's own Required Analysis (inbound/outbound/runtime/
        organizational/version/temporal dependencies), scoped to what
        this schema can actually support today — every check below cites
        the real relationship it inspects; nothing is invented.
        """
        violations: list[DependencyViolation] = []
        now = datetime.now(timezone.utc)

        # 1. Inbound dependencies (BR-C003-04 / Contract 5.6) — reuses
        # BA-08's own get_active_dependents(), never a duplicate query.
        active_dependents = await repo.get_active_dependents(obj.id)
        if active_dependents:
            violations.append(
                DependencyViolation(
                    rule="BR-C003-04",
                    description=(
                        f"{len(active_dependents)} currently-active dependent(s) still reference this object; "
                        "deprecation, retirement, or a breaking amendment SHALL occur only once none remains unresolved."
                    ),
                    detail={"active_dependents": active_dependents},
                )
            )

        # 2. Outbound dependencies (this object's own anchors) — verify
        # the Organization/Domain it references still exists and, for
        # Organization, is not itself RETIRED.
        organization_id = getattr(obj, "organization_id", None)
        if organization_id is not None:
            organization = await self.organization_repo.get_by_id(organization_id)
            if organization is None:
                violations.append(
                    DependencyViolation(
                        rule="Contract-5.6",
                        description="This object's owning Organization no longer resolves — an outbound dependency is broken.",
                        detail={"organization_id": str(organization_id)},
                    )
                )
            elif organization.status == "RETIRED":
                violations.append(
                    DependencyViolation(
                        rule="Contract-5.6",
                        description="This object's owning Organization is RETIRED — an outbound organizational dependency is in question.",
                        detail={"organization_id": str(organization_id)},
                    )
                )

        domain_id = getattr(obj, "domain_id", None)
        if domain_id is not None:
            domain = await self.domain_repo.get_by_id(domain_id)
            if domain is None:
                violations.append(
                    DependencyViolation(
                        rule="Contract-5.6",
                        description="This object's referenced Domain no longer resolves — an outbound dependency is broken.",
                        detail={"domain_id": str(domain_id)},
                    )
                )

        # 3. Temporal dependencies (SD-002-011 / Contract 5.4) — the
        # Canonical Temporal Model's own effective-date window must
        # remain internally consistent.
        effective_from = getattr(obj, "effective_from", None)
        effective_to = getattr(obj, "effective_to", None)
        if effective_from is not None and effective_to is not None and effective_to < effective_from:
            violations.append(
                DependencyViolation(
                    rule="Contract-5.4",
                    description="effective_to precedes effective_from — broken temporal validity.",
                    detail={"effective_from": effective_from.isoformat(), "effective_to": effective_to.isoformat()},
                )
            )
        if getattr(obj, "status", None) == "ACTIVE" and effective_to is not None and effective_to < now:
            violations.append(
                DependencyViolation(
                    rule="Contract-5.4",
                    description="Object is ACTIVE but its effective_to has already passed — a conflicting lifecycle state.",
                    detail={"effective_to": effective_to.isoformat()},
                )
            )

        # 4. Version dependencies (BA-07's own supersedes_id chain) —
        # walk it defensively: under normal application logic (BA-07's
        # own create_new_version(), never mutated elsewhere) a cycle or
        # a second ACTIVE row in one chain cannot occur; this check
        # exists as a genuine integrity guard, not a routine expectation,
        # and directly verifies TD-027's own concern has not materialized.
        chain_violation = await self._check_version_chain(obj, repo)
        if chain_violation is not None:
            violations.append(chain_violation)

        return DependencyConflictReport(
            object_type=object_type,
            object_id=obj.id,
            checked_at=now,
            has_conflicts=len(violations) > 0,
            violations=violations,
            active_dependents=active_dependents,
        )

    async def _check_version_chain(self, obj: Any, repo: Any) -> DependencyViolation | None:
        """
        Walks supersedes_id backward from obj, detecting a circular
        chain (a data-integrity impossibility under normal application
        logic, checked defensively) and counting how many rows in the
        chain claim ACTIVE (should never exceed one — see TD-027).
        """
        visited: set = {obj.id}
        active_count = 1 if getattr(obj, "status", None) == "ACTIVE" else 0
        current = obj
        while current.supersedes_id is not None:
            if current.supersedes_id in visited:
                return DependencyViolation(
                    rule="BR-C003-05",
                    description="This object's version chain (supersedes_id) contains a cycle — a data-integrity impossibility under normal application logic.",
                    detail={"object_id": str(obj.id), "cycle_at": str(current.supersedes_id)},
                )
            previous = await repo.get_by_id(current.supersedes_id)
            if previous is None:
                return DependencyViolation(
                    rule="BR-C003-05",
                    description="This object's version chain references a prior version that no longer resolves — an orphaned version-chain reference (should be impossible under BR-C003-04's never-hard-delete guarantee).",
                    detail={"missing_id": str(current.supersedes_id)},
                )
            visited.add(previous.id)
            if getattr(previous, "status", None) == "ACTIVE":
                active_count += 1
            current = previous

        if active_count > 1:
            return DependencyViolation(
                rule="TD-027",
                description=f"This object's version chain has {active_count} rows claiming ACTIVE status — should never exceed one.",
                detail={"active_count": active_count},
            )
        return None

    async def resolve_conflict(
        self,
        object_type: str,
        obj: Any,
        repo: Any,
        request: ResolveDependencyConflictRequest,
        actor_id: str | None = None,
    ) -> DependencyConflictReport:
        """
        Business Activity: Resolve Authorization Policy Dependency
        Conflict (BA-09).

        Records the proposing authority's explicit resolution statement
        (Contract 5.6) via the existing audit/event mechanism — the same
        mechanism every other WP-02 Business Activity already uses, not
        a new one. Does not itself mutate any dependent's own record
        (Contract 5.1's C-007 boundary); re-runs detect_conflicts()
        immediately after recording the statement and returns the
        current, honest result — a cleared report only if the
        underlying dependent has genuinely changed state (reassigned or
        naturally expired via its own capability) or the proposing
        authority explicitly accepted the break, which this method
        records as evidence, not as itself flipping any other row's
        state (see TD-030's disclosure of exactly this limitation).
        """
        if request.resolution_type == ResolutionType.REASSIGNMENT_CONFIRMED:
            if request.replacement_target_id is None:
                self._record_resolution_denial(object_type, obj.id, actor_id, "REASSIGNMENT_CONFIRMED requires replacement_target_id.")
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="REASSIGNMENT_CONFIRMED requires replacement_target_id.",
                )
            replacement = await repo.get_by_id(request.replacement_target_id)
            if replacement is None:
                self._record_resolution_denial(object_type, obj.id, actor_id, "replacement_target_id does not resolve")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No replacement target found with id '{request.replacement_target_id}'.",
                )
            if replacement.id == obj.id:
                self._record_resolution_denial(object_type, obj.id, actor_id, "replacement_target_id names the object being replaced")
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="replacement_target_id must not be the object being replaced.",
                )
            if getattr(replacement, "status", None) != "ACTIVE":
                self._record_resolution_denial(object_type, obj.id, actor_id, "replacement_target_id is not the current ACTIVE version")
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        f"Invalid replacement target: '{request.replacement_target_id}' is not the current ACTIVE "
                        "version of a same-type object."
                    ),
                )

        record_audit(
            action=f"RESOLVE_DEPENDENCY_CONFLICT_{object_type.upper()}",
            resource=f"{object_type}:{obj.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "resolution_type": request.resolution_type.value,
                "reason": request.reason,
                "replacement_target_id": str(request.replacement_target_id) if request.replacement_target_id else None,
            },
        )
        publish_event(
            "AUTHORIZATION_POLICY_DEPENDENCY_CONFLICT_RESOLUTION_RECORDED",
            {
                "object_type": object_type,
                "object_id": str(obj.id),
                "resolution_type": request.resolution_type.value,
                "reason": request.reason,
            },
        )

        return await self.detect_conflicts(object_type, obj, repo)

    def _record_resolution_denial(self, object_type: str, object_id: Any, actor_id: str | None, reason: str) -> None:
        """
        WP-02 BA-09 (found by Independent Review): every prior WP-02
        Business Activity audits both its success and every denial
        branch (SD-002-054's seven audit questions). resolve_conflict()'s
        own validation failures had not been audited — closed here,
        matching the same discipline established since BA-01.
        """
        record_audit(
            action=f"RESOLVE_DEPENDENCY_CONFLICT_{object_type.upper()}",
            resource=f"{object_type}:{object_id}",
            status=AuditStatus.DENIED,
            actor_id=actor_id or "SYSTEM",
            metadata={"reason": reason},
        )

    async def classify_handoff_rejection(
        self,
        object_type: str,
        obj: Any,
        repo: Any,
        request: ReportHandoffRejectionRequest,
        actor_id: str | None = None,
    ) -> HandoffRejectionOutcome:
        """
        Business Activity: Resolve Dependent Capability Authorization
        Policy Hand-off Rejection (BA-10).

        Classifies a dependent capability's stated rejection as either
        CAPABILITY_SCOPED_INSUFFICIENCY (the object is preserved,
        unchanged, and the rejection is scoped to that capability's own
        attempted use only) or INTEGRITY_SIGNAL (the object's own
        definition is genuinely in question), per BR-C003-06/Contract
        5.7. The classification is computed entirely from this
        capability's own already-established signals — BA-08's status
        field and BA-09's detect_conflicts() — never from
        request.stated_reason, which is recorded for traceability only:
        Contract 5.7's own text is explicit that "the dependent
        capability's stated rejection reason is a signal, not an
        authority," and that C-003 "SHALL NOT treat [the reporting
        capability's] report as an adjudication of the object's
        definition without independent classification."

        Never mutates the object (no status transition performed here —
        that remains BA-08's own capability, untouched); never itself
        determines whether a specific request is currently permitted
        (Contract 5.3 — that determination and its enforcement remain
        exclusively RTA-001's Authorization Engine and C-002's own
        concern, which consume this classification as an input).
        """
        now = datetime.now(timezone.utc)

        if getattr(obj, "status", None) in ("DEPRECATED", "RETIRED", "SUPERSEDED"):
            classification = HandoffRejectionClassification.INTEGRITY_SIGNAL
            explanation = (
                f"The object's own status is {obj.status} — it is not the object's current, in-force "
                "version and is no longer available for consumption (BR-C003-04/EX-C003-08), independent "
                "of the reporting capability's stated reason."
            )
            conflict_report = await self.detect_conflicts(object_type, obj, repo)
        else:
            conflict_report = await self.detect_conflicts(object_type, obj, repo)
            if conflict_report.has_conflicts:
                classification = HandoffRejectionClassification.INTEGRITY_SIGNAL
                explanation = (
                    "BA-09's own dependency/outbound/temporal/version-chain check found genuine violations — "
                    "the object's own definition is in question, not merely this capability's use of it."
                )
            else:
                classification = HandoffRejectionClassification.CAPABILITY_SCOPED_INSUFFICIENCY
                explanation = (
                    "The object is the current ACTIVE version and passes every BA-09 integrity check; the "
                    "reported rejection is scoped to the reporting capability's own attempted use only "
                    "(Contract 5.7 — the object is preserved unchanged)."
                )

        object_preserved = classification == HandoffRejectionClassification.CAPABILITY_SCOPED_INSUFFICIENCY
        routed_to = None if object_preserved else "ERB-C003-01/ERB-C003-02 (Establish/Version/Deprecate/Retire — routed for correction, never auto-corrected here per Contract 5.8)"

        record_audit(
            action=f"REPORT_HANDOFF_REJECTION_{object_type.upper()}",
            resource=f"{object_type}:{obj.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "reporting_capability": request.reporting_capability,
                "stated_reason": request.stated_reason,
                "classification": classification.value,
                "object_preserved": object_preserved,
            },
        )
        publish_event(
            "AUTHORIZATION_POLICY_HANDOFF_REJECTION_CLASSIFIED",
            {
                "object_type": object_type,
                "object_id": str(obj.id),
                "reporting_capability": request.reporting_capability,
                "classification": classification.value,
                "object_preserved": object_preserved,
            },
        )

        return HandoffRejectionOutcome(
            object_type=object_type,
            object_id=obj.id,
            classification=classification,
            object_preserved=object_preserved,
            explanation=explanation,
            routed_to=routed_to,
            conflict_report=conflict_report,
            checked_at=now,
        )
