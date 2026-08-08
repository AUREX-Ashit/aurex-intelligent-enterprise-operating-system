"""
Authorization Runtime Engine -- Tier Resolver interface.

WP-RTA-001 Milestone M1. Defines the Runtime interface each of
URA-001-76's five precedence tiers is evaluated through, separating
the shared, capability-agnostic evaluation pipeline (this Work
Package) from any capability-specific data source (owned by whichever
capability's own Work Package -- e.g. Domain Permission, WP-02).

No concrete TierResolver is implemented in M1. Every tier is
NOT_EVALUATED by default until a future milestone binds a real
resolver (M5 -- real tier resolution) or a consuming Business Activity
supplies one at integration time (M3 -- pre-execution gate
integration). See WP-RTA-001 Deliverables.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from .models import AuthorizationContext, AuthorizationDecision


@dataclass(frozen=True)
class TierResolution:
    """
    A precedence tier's own concluded determination -- returned only
    when the tier has reached an answer for the given Authorization
    Context.

    Milestone note (M2, defect found and corrected -- see
    IMP-REPORT-WP-RTA-001): M1 originally implemented this class with
    `__slots__` and a docstring claiming "immutable by construction,"
    but `__slots__` alone does not prevent attribute reassignment --
    only attribute *creation* beyond the declared slots. It was not
    actually immutable. Converted to a frozen dataclass here, matching
    `TierEvaluation`/`EvaluationResult`'s own already-correct pattern in
    `models.py`. No other M1 file required this correction.
    """

    decision: AuthorizationDecision
    reason: str


@runtime_checkable
class TierResolver(Protocol):
    """
    The Runtime interface a future, capability-specific adapter
    implements to make one precedence tier real. Structural typing
    (Protocol) is used deliberately -- a concrete resolver need not
    import or depend on this module beyond satisfying this shape,
    keeping the shared engine free of any capability-specific coupling
    (Constitutional Principle 1, IRA-RTA-001 S10).
    """

    async def resolve(self, context: AuthorizationContext) -> TierResolution | None:
        """
        Return a TierResolution if this tier reaches a determination
        for the given context, or None if the tier was checked and
        found nothing applicable (a legitimate NO_MATCH). A tier with
        no TierResolver bound at all is never asked -- the engine
        reports that as NOT_EVALUATED without calling this method.
        """
        ...
