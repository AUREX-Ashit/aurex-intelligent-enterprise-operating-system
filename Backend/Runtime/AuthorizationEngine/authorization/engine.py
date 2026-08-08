"""
Authorization Runtime Engine -- Evaluation pipeline (WP-RTA-001 M1).

Realizes RTA-001 S11's own Authorization Engine: "the sole authority
for runtime authorization decisions" (S11.2), evaluating URA-001-76's
five-tier Authorization Resolution Precedence (Named User > Group >
Approval Authority > Business Role > Domain Permission) in canonical
order and returning exactly one Authorization Decision (S11.8) plus a
full Runtime Trace (S11.15).

Milestone M1 scope only: the evaluation pipeline, decision model, and
precedence skeleton. No concrete TierResolver is bound by this module
-- every tier is NOT_EVALUATED until a future milestone (M3 gate
integration, M5 real tier resolution) binds one. This module never
fabricates a MATCH for an unbound tier (CLAUDE.md S19.8.5 -- a false
Permitted outcome is a security defect, not deferrable as ordinary
Technical Debt).

Explicitly out of M1's scope (WP-RTA-001 Deliverables, later
milestones): Enterprise Scope Validation (M2), Business Activity /
pre-execution-gate integration (M3), Authorization Observability
telemetry beyond the trace itself (M4), Assignment/Delegation/Approval
Authority real resolution (M5), Authorization Caching (M6).
"""

from __future__ import annotations

from .models import (
    AuthorizationContext,
    AuthorizationDecision,
    AuthorizationTier,
    EvaluationResult,
    TierEvaluation,
    TierResult,
)
from .resolvers import TierResolver

# URA-001-76's own precedence order, most specific first.
PRECEDENCE_ORDER: tuple[AuthorizationTier, ...] = (
    AuthorizationTier.NAMED_USER,
    AuthorizationTier.GROUP,
    AuthorizationTier.APPROVAL_AUTHORITY,
    AuthorizationTier.BUSINESS_ROLE,
    AuthorizationTier.DOMAIN_PERMISSION,
)


class AuthorizationEngine:
    """RTA-001 S11's own Authorization Engine -- evaluates one Authorization Context against the URA-001-76 precedence chain."""

    def __init__(self, resolvers: dict[AuthorizationTier, TierResolver] | None = None) -> None:
        """
        `resolvers` binds a concrete TierResolver to zero or more of
        URA-001-76's five tiers. Any tier absent from this mapping is
        reported NOT_EVALUATED -- a structural gap, never silently
        skipped and never fabricated as a match. M1 ships with no
        resolvers bound by default; binding real resolvers is a future
        milestone's own concern (M3/M5), not this module's.
        """
        self._resolvers: dict[AuthorizationTier, TierResolver] = dict(resolvers) if resolvers else {}

    async def evaluate(self, context: AuthorizationContext) -> EvaluationResult:
        """
        Evaluate `context` against URA-001-76's precedence chain in
        canonical order. Returns immediately on the first tier that
        reaches a determination (RTA-001 S11.7: deterministic and
        reproducible); lower-precedence tiers are never visited once a
        higher-precedence tier has answered. Returns DENY with a
        complete trace if no tier resolves -- this engine never
        defaults to ALLOW.
        """
        trace: list[TierEvaluation] = []

        for tier in PRECEDENCE_ORDER:
            resolver = self._resolvers.get(tier)

            if resolver is None:
                trace.append(
                    TierEvaluation(
                        tier=tier,
                        result=TierResult.NOT_EVALUATED,
                        reason="No resolver bound for this tier.",
                    )
                )
                continue

            resolution = await resolver.resolve(context)

            if resolution is None:
                trace.append(
                    TierEvaluation(
                        tier=tier,
                        result=TierResult.NO_MATCH,
                        reason="Resolver evaluated this tier and found no applicable grant.",
                    )
                )
                continue

            trace.append(
                TierEvaluation(
                    tier=tier,
                    result=TierResult.MATCH,
                    reason=resolution.reason,
                    decision=resolution.decision,
                )
            )
            return EvaluationResult(
                decision=resolution.decision,
                matched_tier=tier,
                reason=resolution.reason,
                trace=tuple(trace),
            )

        return EvaluationResult(
            decision=AuthorizationDecision.DENY,
            matched_tier=None,
            reason="No precedence tier resolved to a determination.",
            trace=tuple(trace),
        )
