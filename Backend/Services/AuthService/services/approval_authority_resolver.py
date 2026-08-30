"""
WP-18 — Approval Authority Runtime Resolver (C-003, repository-wide
infrastructure), realizing TDS-018 §29.2's own corrected, authoritative
resolver algorithm exactly. This is the first implementation of Approval
Authority runtime enforcement anywhere in this codebase — independently
confirmed absent at every prior design stage (TDS-018 §4.4/§4.6).

Deliberately a plain, testable async function — not a FastAPI dependency
itself — mirroring `dependencies.py::enforce_domain_permission`'s own
established split (a plain function; `require_domain_permission` wraps
it), so the resolution logic is directly unit-testable without an HTTP
layer and reusable by more than one future call site (TDS-018 §16).

No `PLATFORM_ADMIN`/`AUREX_ADMIN` fallback anywhere in this module —
TDS-018 §11/§18 explicitly prohibit any admin bypass for this gate.
`ALL`/`MAJORITY`/`SEQUENTIAL` are denied, never resolved — no
counting/quorum/sequencing semantics are implemented here (TDS-018 §9/
§29.5, genuinely unresolved, not this module's concern).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession

from models.approval_authority import ApprovalStrategy
from repositories.approval_authority_repository import ApprovalAuthorityRepository
from repositories.membership_approval_authority_repository import MembershipApprovalAuthorityRepository
from repositories.membership_repository import MembershipRepository
from observability import record_audit, publish_event, AuditStatus


class ApprovalAuthorityResolution(str, Enum):
    """
    TDS-018 §29.4's own eight-label reason taxonomy — documentation/
    diagnostic content, not a competing decision enum (TDS-018 §20's own
    reuse-over-invention discipline: the outer ALLOW/DENY distinction is
    `AUTHORIZED` vs. everything else, mirroring `AuthorizationDecision`,
    `authorization/models.py`, without importing it directly here to
    avoid coupling this plain resolver function to the Runtime
    Authorization Engine, per TDS-018 §12 Option B's own explicit
    "no `AuthorizationContext`, no Engine involvement" design).
    """
    NO_AUTHORITY_CONFIGURED = "NO_AUTHORITY_CONFIGURED"
    INACTIVE_AUTHORITY = "INACTIVE_AUTHORITY"
    INVALID_CONFIGURATION = "INVALID_CONFIGURATION"
    UNSUPPORTED_STRATEGY = "UNSUPPORTED_STRATEGY"
    INVALID_SCOPE = "INVALID_SCOPE"
    NO_ELIGIBLE_ACTOR = "NO_ELIGIBLE_ACTOR"
    INACTIVE_MEMBERSHIP = "INACTIVE_MEMBERSHIP"
    AUTHORIZED = "AUTHORIZED"


_MEMBERSHIP_ACTIVE_STATUS = "ACTIVE"


async def resolve_approval_authority(
    session: AsyncSession,
    target_organization_id: uuid.UUID,
    authority_name: str,
    caller_organization_id: uuid.UUID | None,
    caller_membership_id: uuid.UUID | None,
    actor_id: str | None = None,
) -> ApprovalAuthorityResolution:
    """
    TDS-018 §29.2's own corrected, authoritative 8-step algorithm,
    implemented exactly, in this exact order, no step skippable or
    reorderable. Returns the diagnostic reason — `AUTHORIZED` is the sole
    ALLOW outcome; every other value is a DENY. Records an audit entry
    for every outcome (TDS-018 §21).
    """
    approval_authority_repo = ApprovalAuthorityRepository(session)
    binding_repo = MembershipApprovalAuthorityRepository(session)
    membership_repo = MembershipRepository(session)

    def _deny(reason: ApprovalAuthorityResolution, extra: dict | None = None) -> ApprovalAuthorityResolution:
        record_audit(
            action="RESOLVE_APPROVAL_AUTHORITY",
            resource=f"approval_authority:{target_organization_id}:{authority_name}",
            status=AuditStatus.DENIED,
            actor_id=actor_id or "SYSTEM",
            metadata={"reason": reason.value, **(extra or {})},
        )
        return reason

    # Step 1 -- Resolve the authority.
    authority = await approval_authority_repo.get_active_by_organization_and_name(
        target_organization_id, authority_name
    )
    if authority is None:
        any_row = await approval_authority_repo.get_any_by_organization_and_name(
            target_organization_id, authority_name
        )
        if any_row is not None:
            return _deny(ApprovalAuthorityResolution.INACTIVE_AUTHORITY, {"status": any_row.status})
        return _deny(ApprovalAuthorityResolution.NO_AUTHORITY_CONFIGURED)

    # Step 2 -- Validate configuration. Evaluated before the strategy
    # check and before any caller-specific step, so it cannot be
    # bypassed by a qualifying binding (TDS-018 §29.2 step 2's own
    # ordering fix).
    if (
        authority.approval_strategy == ApprovalStrategy.MAJORITY.value
        and authority.majority_threshold_pct is None
    ):
        return _deny(ApprovalAuthorityResolution.INVALID_CONFIGURATION)

    # Step 3 -- Inspect approval_strategy. The corrected design's own
    # central addition: ALL/MAJORITY/SEQUENTIAL deny here, before any
    # caller-specific step is ever evaluated -- this is what makes the
    # ANY_ONE-only scope boundary structurally enforced rather than
    # merely asserted in prose (TDS-018 §29.2 step 3).
    if authority.approval_strategy != ApprovalStrategy.ANY_ONE.value:
        return _deny(
            ApprovalAuthorityResolution.UNSUPPORTED_STRATEGY,
            {"approval_strategy": authority.approval_strategy},
        )

    # Step 4 -- Organization mismatch.
    if caller_organization_id is None or caller_organization_id != target_organization_id:
        return _deny(ApprovalAuthorityResolution.INVALID_SCOPE)

    # Step 5 -- Eligible actor / missing binding.
    if caller_membership_id is None:
        return _deny(ApprovalAuthorityResolution.NO_ELIGIBLE_ACTOR)
    binding = await binding_repo.get_effective_binding(caller_membership_id, authority.id)
    if binding is None:
        return _deny(ApprovalAuthorityResolution.NO_ELIGIBLE_ACTOR)

    # Step 6 -- Active/inactive actor.
    membership = await membership_repo.get_by_id(caller_membership_id)
    now = datetime.now(timezone.utc)
    membership_effective = (
        membership is not None
        and membership.membership_status == _MEMBERSHIP_ACTIVE_STATUS
        and membership.effective_from <= now
        and (membership.effective_to is None or membership.effective_to > now)
    )
    if not membership_effective:
        return _deny(ApprovalAuthorityResolution.INACTIVE_MEMBERSHIP)

    # Steps 7-8 -- exactly one qualifying binding for an ANY_ONE row is
    # sufficient; AUTHORIZED.
    record_audit(
        action="RESOLVE_APPROVAL_AUTHORITY",
        resource=f"approval_authority:{authority.id}",
        status=AuditStatus.SUCCESS,
        actor_id=actor_id or "SYSTEM",
        metadata={
            "approval_authority_id": str(authority.id),
            "membership_id": str(caller_membership_id),
            "authority_name": authority_name,
            "organization_id": str(target_organization_id),
        },
    )
    publish_event(
        "APPROVAL_AUTHORITY_RESOLVED",
        {
            "approval_authority_id": str(authority.id),
            "membership_id": str(caller_membership_id),
            "authority_name": authority_name,
            "organization_id": str(target_organization_id),
            "decision": ApprovalAuthorityResolution.AUTHORIZED.value,
        },
    )
    return ApprovalAuthorityResolution.AUTHORIZED
