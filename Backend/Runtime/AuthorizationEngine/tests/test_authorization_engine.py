"""
Unit tests for WP-RTA-001 Milestone M1 -- Authorization Evaluation Core.

No database, no FastAPI, no capability-specific dependency: M1 is a
pure Runtime evaluation pipeline, tested here purely against stub
TierResolver implementations. Real tier resolution against actual
capability data (Domain Permission, etc.) is a future milestone (M5),
not exercised by these tests.
"""

from __future__ import annotations

import pytest

from authorization import (
    AuthorizationContext,
    AuthorizationDecision,
    AuthorizationEngine,
    AuthorizationTier,
    TierResolution,
    TierResult,
)
from authorization.engine import PRECEDENCE_ORDER


def _context(**overrides) -> AuthorizationContext:
    defaults = dict(identity_id="person-1", organization_id="org-1")
    defaults.update(overrides)
    return AuthorizationContext(**defaults)


class _AlwaysMatchResolver:
    """Stub resolver that always reaches the given decision."""

    def __init__(self, decision: AuthorizationDecision, reason: str = "stub match") -> None:
        self._decision = decision
        self._reason = reason
        self.calls = 0

    async def resolve(self, context: AuthorizationContext) -> TierResolution | None:
        self.calls += 1
        return TierResolution(decision=self._decision, reason=self._reason)


class _NeverMatchResolver:
    """Stub resolver that always checks and finds nothing (NO_MATCH, not NOT_EVALUATED)."""

    def __init__(self) -> None:
        self.calls = 0

    async def resolve(self, context: AuthorizationContext) -> TierResolution | None:
        self.calls += 1
        return None


async def test_evaluate_denies_when_no_resolvers_bound() -> None:
    """With zero resolvers bound, the engine must fail closed, never default to ALLOW."""
    engine = AuthorizationEngine()

    result = await engine.evaluate(_context())

    assert result.decision == AuthorizationDecision.DENY
    assert result.matched_tier is None
    assert len(result.trace) == 5


async def test_evaluate_trace_covers_all_five_tiers_in_precedence_order() -> None:
    engine = AuthorizationEngine()

    result = await engine.evaluate(_context())

    assert tuple(entry.tier for entry in result.trace) == PRECEDENCE_ORDER
    assert list(PRECEDENCE_ORDER) == [
        AuthorizationTier.NAMED_USER,
        AuthorizationTier.GROUP,
        AuthorizationTier.APPROVAL_AUTHORITY,
        AuthorizationTier.BUSINESS_ROLE,
        AuthorizationTier.DOMAIN_PERMISSION,
    ]


async def test_unbound_tier_is_reported_not_evaluated_never_fabricated() -> None:
    engine = AuthorizationEngine()

    result = await engine.evaluate(_context())

    for entry in result.trace:
        assert entry.result == TierResult.NOT_EVALUATED
        assert entry.decision is None
        assert entry.reason


async def test_bound_resolver_returning_none_is_no_match_not_not_evaluated() -> None:
    resolver = _NeverMatchResolver()
    engine = AuthorizationEngine({AuthorizationTier.DOMAIN_PERMISSION: resolver})

    result = await engine.evaluate(_context())

    assert result.decision == AuthorizationDecision.DENY
    domain_permission_entry = result.trace[-1]
    assert domain_permission_entry.tier == AuthorizationTier.DOMAIN_PERMISSION
    assert domain_permission_entry.result == TierResult.NO_MATCH
    assert resolver.calls == 1


async def test_matching_tier_short_circuits_and_returns_its_decision() -> None:
    resolver = _AlwaysMatchResolver(AuthorizationDecision.ALLOW, reason="active grant found")
    engine = AuthorizationEngine({AuthorizationTier.DOMAIN_PERMISSION: resolver})

    result = await engine.evaluate(_context())

    assert result.decision == AuthorizationDecision.ALLOW
    assert result.matched_tier == AuthorizationTier.DOMAIN_PERMISSION
    assert result.reason == "active grant found"
    assert result.trace[-1].result == TierResult.MATCH
    assert result.trace[-1].decision == AuthorizationDecision.ALLOW


async def test_higher_precedence_tier_wins_and_lower_tier_is_never_consulted() -> None:
    """URA-001-76: most specific tier that reaches a determination wins -- lower tiers are never even called."""
    named_user_resolver = _AlwaysMatchResolver(AuthorizationDecision.DENY, reason="explicit named-user deny")
    domain_permission_resolver = _AlwaysMatchResolver(AuthorizationDecision.ALLOW, reason="would-be grant")
    engine = AuthorizationEngine(
        {
            AuthorizationTier.NAMED_USER: named_user_resolver,
            AuthorizationTier.DOMAIN_PERMISSION: domain_permission_resolver,
        }
    )

    result = await engine.evaluate(_context())

    assert result.decision == AuthorizationDecision.DENY
    assert result.matched_tier == AuthorizationTier.NAMED_USER
    assert named_user_resolver.calls == 1
    assert domain_permission_resolver.calls == 0
    # Only the matched tier appears in the trace -- lower tiers were never visited.
    assert len(result.trace) == 1


async def test_intermediate_no_match_tiers_precede_the_matching_tier_in_trace() -> None:
    engine = AuthorizationEngine(
        {
            AuthorizationTier.NAMED_USER: _NeverMatchResolver(),
            AuthorizationTier.GROUP: _NeverMatchResolver(),
            AuthorizationTier.DOMAIN_PERMISSION: _AlwaysMatchResolver(AuthorizationDecision.ALLOW),
        }
    )

    result = await engine.evaluate(_context())

    assert [entry.result for entry in result.trace] == [
        TierResult.NO_MATCH,  # NAMED_USER
        TierResult.NO_MATCH,  # GROUP
        TierResult.NOT_EVALUATED,  # APPROVAL_AUTHORITY (no resolver bound)
        TierResult.NOT_EVALUATED,  # BUSINESS_ROLE (no resolver bound)
        TierResult.MATCH,  # DOMAIN_PERMISSION
    ]
    assert result.decision == AuthorizationDecision.ALLOW


async def test_conditional_delegated_escalated_are_reachable_via_a_resolver() -> None:
    """RTA-001 S11.8's full five-value taxonomy is structurally supported, not hardcoded to Allow/Deny only."""
    for decision in (
        AuthorizationDecision.CONDITIONAL,
        AuthorizationDecision.DELEGATED,
        AuthorizationDecision.ESCALATED,
    ):
        engine = AuthorizationEngine(
            {AuthorizationTier.APPROVAL_AUTHORITY: _AlwaysMatchResolver(decision, reason=f"stub {decision.value}")}
        )

        result = await engine.evaluate(_context())

        assert result.decision == decision
        assert result.matched_tier == AuthorizationTier.APPROVAL_AUTHORITY


def test_authorization_context_is_immutable() -> None:
    """RTA-001 S11.5: 'Authorization Context shall remain immutable throughout execution.'"""
    context = _context()

    with pytest.raises(AttributeError):
        context.identity_id = "someone-else"  # type: ignore[misc]
