"""
Unit tests for WP-RTA-001 Milestone M2 -- Runtime Resolver Framework & Tier Resolution.

Covers: successful resolution, missing resolution, multiple tier
combinations, empty authorization context, resolver failures,
deterministic behaviour -- against the five URA-001-76 tier resolver
interfaces and ResolverRegistry, with AuthorizationEngine (M1)
untouched. No database, no FastAPI, no capability-specific dependency.
"""

from __future__ import annotations

import dataclasses

import pytest

from authorization import (
    ApprovalAuthorityResolver,
    AuthorizationContext,
    AuthorizationDecision,
    AuthorizationEngine,
    AuthorizationTier,
    BaseTierResolver,
    BusinessRoleResolver,
    DomainPermissionResolver,
    DuplicateResolverError,
    GroupResolver,
    NamedUserResolver,
    ResolverRegistry,
    TierResolution,
    TierResult,
)


def _context(**overrides) -> AuthorizationContext:
    defaults = dict(identity_id="person-1", organization_id="org-1")
    defaults.update(overrides)
    return AuthorizationContext(**defaults)


def _stub(base_cls, *, outcome: TierResolution | None = None, error: Exception | None = None):
    """Build a minimal concrete instance of an abstract tier resolver, for testing only."""

    class _Stub(base_cls):  # type: ignore[misc,valid-type]
        def __init__(self) -> None:
            self.calls = 0

        async def resolve(self, context: AuthorizationContext) -> TierResolution | None:
            self.calls += 1
            if error is not None:
                raise error
            return outcome

    return _Stub()


# ---------------------------------------------------------------------------
# Tier resolver interface shape
# ---------------------------------------------------------------------------


def test_each_tier_resolver_class_declares_its_own_correct_tier() -> None:
    assert NamedUserResolver.TIER == AuthorizationTier.NAMED_USER
    assert GroupResolver.TIER == AuthorizationTier.GROUP
    assert ApprovalAuthorityResolver.TIER == AuthorizationTier.APPROVAL_AUTHORITY
    assert BusinessRoleResolver.TIER == AuthorizationTier.BUSINESS_ROLE
    assert DomainPermissionResolver.TIER == AuthorizationTier.DOMAIN_PERMISSION


def test_base_tier_resolver_cannot_be_instantiated_directly() -> None:
    with pytest.raises(TypeError):
        BaseTierResolver()  # type: ignore[abstract]


def test_tier_resolution_is_actually_immutable() -> None:
    """M2 defect fix: M1's TierResolution claimed immutability via __slots__ alone, which does not prevent reassignment."""
    resolution = TierResolution(decision=AuthorizationDecision.ALLOW, reason="test")

    assert dataclasses.is_dataclass(resolution)
    with pytest.raises(dataclasses.FrozenInstanceError):
        resolution.decision = AuthorizationDecision.DENY  # type: ignore[misc]


# ---------------------------------------------------------------------------
# ResolverRegistry
# ---------------------------------------------------------------------------


def test_registry_rejects_duplicate_tier_registration() -> None:
    registry = ResolverRegistry()
    registry.register(_stub(DomainPermissionResolver))

    with pytest.raises(DuplicateResolverError):
        registry.register(_stub(DomainPermissionResolver))


def test_registry_build_returns_an_independent_mapping() -> None:
    registry = ResolverRegistry()
    registry.register(_stub(DomainPermissionResolver))

    mapping_one = registry.build()
    mapping_two = registry.build()

    assert mapping_one == mapping_two
    assert mapping_one is not mapping_two  # each build() call returns its own copy


def test_registry_is_fluent() -> None:
    registry = ResolverRegistry()
    result = registry.register(_stub(NamedUserResolver)).register(_stub(GroupResolver))

    assert result is registry
    assert len(registry.build()) == 2


# ---------------------------------------------------------------------------
# End-to-end: registry-assembled resolvers feeding the (unmodified) M1 engine
# ---------------------------------------------------------------------------


async def test_successful_resolution_via_registry() -> None:
    registry = ResolverRegistry().register(
        _stub(DomainPermissionResolver, outcome=TierResolution(AuthorizationDecision.ALLOW, "active grant"))
    )
    engine = AuthorizationEngine(registry.build())

    result = await engine.evaluate(_context())

    assert result.decision == AuthorizationDecision.ALLOW
    assert result.matched_tier == AuthorizationTier.DOMAIN_PERMISSION


async def test_missing_resolution_reports_not_evaluated_for_unregistered_tiers() -> None:
    registry = ResolverRegistry().register(
        _stub(DomainPermissionResolver, outcome=None)  # bound, but checks and finds nothing
    )
    engine = AuthorizationEngine(registry.build())

    result = await engine.evaluate(_context())

    assert result.decision == AuthorizationDecision.DENY
    results_by_tier = {entry.tier: entry.result for entry in result.trace}
    assert results_by_tier[AuthorizationTier.NAMED_USER] == TierResult.NOT_EVALUATED
    assert results_by_tier[AuthorizationTier.GROUP] == TierResult.NOT_EVALUATED
    assert results_by_tier[AuthorizationTier.APPROVAL_AUTHORITY] == TierResult.NOT_EVALUATED
    assert results_by_tier[AuthorizationTier.BUSINESS_ROLE] == TierResult.NOT_EVALUATED
    assert results_by_tier[AuthorizationTier.DOMAIN_PERMISSION] == TierResult.NO_MATCH


@pytest.mark.parametrize(
    "bound_outcomes,expected_decision,expected_tier",
    [
        # Group denies explicitly; Business Role and Domain Permission are never reached.
        ({"group": AuthorizationDecision.DENY}, AuthorizationDecision.DENY, AuthorizationTier.GROUP),
        # Group checks and finds nothing; falls through to Business Role, which allows.
        ({"group": None, "business_role": AuthorizationDecision.ALLOW}, AuthorizationDecision.ALLOW, AuthorizationTier.BUSINESS_ROLE),
        # Approval Authority escalates.
        ({"approval_authority": AuthorizationDecision.ESCALATED}, AuthorizationDecision.ESCALATED, AuthorizationTier.APPROVAL_AUTHORITY),
    ],
)
async def test_multiple_tier_combinations(bound_outcomes, expected_decision, expected_tier) -> None:
    registry = ResolverRegistry()
    if "group" in bound_outcomes:
        outcome = bound_outcomes["group"]
        registry.register(
            _stub(GroupResolver, outcome=None if outcome is None else TierResolution(outcome, "group stub"))
        )
    if "business_role" in bound_outcomes:
        outcome = bound_outcomes["business_role"]
        registry.register(
            _stub(BusinessRoleResolver, outcome=None if outcome is None else TierResolution(outcome, "role stub"))
        )
    if "approval_authority" in bound_outcomes:
        outcome = bound_outcomes["approval_authority"]
        registry.register(
            _stub(ApprovalAuthorityResolver, outcome=None if outcome is None else TierResolution(outcome, "approval stub"))
        )

    engine = AuthorizationEngine(registry.build())
    result = await engine.evaluate(_context())

    assert result.decision == expected_decision
    assert result.matched_tier == expected_tier


async def test_empty_authorization_context_denies_deterministically() -> None:
    """A minimally-populated context (only the two required fields) with no resolvers bound must still fail closed."""
    engine = AuthorizationEngine(ResolverRegistry().build())

    result = await engine.evaluate(_context())

    assert result.decision == AuthorizationDecision.DENY
    assert result.matched_tier is None
    assert len(result.trace) == 5
    assert all(entry.result == TierResult.NOT_EVALUATED for entry in result.trace)


async def test_resolver_failure_propagates_and_is_never_silently_converted_to_a_decision() -> None:
    """A raising resolver must fail loud (CLAUDE.md coding standards: fail fast) -- never be swallowed into DENY or ALLOW."""

    class _ResolverBlewUp(RuntimeError):
        pass

    registry = ResolverRegistry().register(_stub(DomainPermissionResolver, error=_ResolverBlewUp("simulated failure")))
    engine = AuthorizationEngine(registry.build())

    with pytest.raises(_ResolverBlewUp):
        await engine.evaluate(_context())


async def test_evaluation_is_deterministic_across_repeated_calls() -> None:
    """RTA-001 S11.7: 'Authorization decisions shall be deterministic and reproducible.'"""
    registry = ResolverRegistry().register(
        _stub(DomainPermissionResolver, outcome=TierResolution(AuthorizationDecision.ALLOW, "active grant"))
    )
    engine = AuthorizationEngine(registry.build())
    context = _context()

    first = await engine.evaluate(context)
    second = await engine.evaluate(context)

    assert first.decision == second.decision
    assert first.matched_tier == second.matched_tier
    assert first.reason == second.reason
    assert first.trace == second.trace
