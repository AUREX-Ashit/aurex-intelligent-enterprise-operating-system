"""
Resolver Orchestrator (WP-RTA-001 M3).

Assembles a ResolverRegistry (M2, unchanged) into the resolver mapping
AuthorizationEngine's own constructor already accepted since M1 -- the
sole seam through which dependency injection happens. Exposes
discovery (which tiers are configured, which are missing) so a caller
can introspect configuration *before* invoking evaluation, without
AuthorizationEngine itself gaining any discovery responsibility.

This is deliberately a thin assembly/introspection layer, not a
re-implementation of precedence evaluation: URA-001-76's own
canonical order (`engine.PRECEDENCE_ORDER`) is read from `engine.py`,
never redefined here, so there is exactly one place in this codebase
that states the order.
"""

from __future__ import annotations

from .engine import PRECEDENCE_ORDER
from .models import AuthorizationTier
from .registry import ResolverRegistry
from .resolvers import TierResolver


class PipelineConfigurationError(Exception):
    """Raised when a Runtime Evaluation Pipeline component is constructed with an invalid configuration."""


class ResolverOrchestrator:
    """
    Resolver discovery, dependency-injection assembly, and
    configuration introspection for one evaluation pipeline.
    `AuthorizationEngine` never discovers or assembles resolvers
    itself (M1, unchanged) -- this class is where that responsibility
    lives instead.
    """

    def __init__(self, registry: ResolverRegistry) -> None:
        if registry is None:
            raise PipelineConfigurationError("ResolverOrchestrator requires a ResolverRegistry, got None.")
        self._resolvers: dict[AuthorizationTier, TierResolver] = registry.build()

    @property
    def configured_tiers(self) -> tuple[AuthorizationTier, ...]:
        """Tiers with a resolver bound, in URA-001-76's own canonical order."""
        return tuple(tier for tier in PRECEDENCE_ORDER if tier in self._resolvers)

    @property
    def missing_tiers(self) -> tuple[AuthorizationTier, ...]:
        """Tiers with no resolver bound, in URA-001-76's own canonical order -- discoverable before evaluation, not only after."""
        return tuple(tier for tier in PRECEDENCE_ORDER if tier not in self._resolvers)

    def resolvers(self) -> dict[AuthorizationTier, TierResolver]:
        """The assembled mapping -- the only thing AuthorizationEngine's own constructor ever consumes."""
        return dict(self._resolvers)
