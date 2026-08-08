"""
Runtime Resolver Framework -- resolver registry (WP-RTA-001 M2).

Assembles a `{AuthorizationTier: TierResolver}` mapping for
`AuthorizationEngine` (M1, unchanged) to consume. `AuthorizationEngine`
never instantiates a resolver itself (M1's own constructor-injection
design, preserved); this registry is the injectable framework that
does the assembling, so a future milestone can replace any resolver
without modifying `AuthorizationEngine` or the resolvers it is not
replacing.
"""

from __future__ import annotations

from .models import AuthorizationTier
from .resolvers import TierResolver
from .tier_resolvers import BaseTierResolver


class DuplicateResolverError(Exception):
    """Raised when two resolvers are registered against the same tier -- fail fast, never silently overwrite."""


class ResolverRegistry:
    """
    Builds the tier-to-resolver mapping `AuthorizationEngine` consumes.
    Deliberately fluent and fail-fast: registering a second resolver
    for a tier already registered is an error, not a silent overwrite,
    since a silently-overwritten resolver could quietly change an
    authorization outcome with no trace of why.
    """

    def __init__(self) -> None:
        self._resolvers: dict[AuthorizationTier, TierResolver] = {}

    def register(self, resolver: BaseTierResolver) -> "ResolverRegistry":
        """Register `resolver` against its own declared `TIER`. Returns self for fluent chaining."""
        if resolver.TIER in self._resolvers:
            raise DuplicateResolverError(
                f"A resolver is already registered for tier {resolver.TIER.value}; "
                f"replace it explicitly via a new ResolverRegistry rather than registering a second one."
            )
        self._resolvers[resolver.TIER] = resolver
        return self

    def build(self) -> dict[AuthorizationTier, TierResolver]:
        """Return the assembled mapping, ready to construct `AuthorizationEngine(resolvers=...)`."""
        return dict(self._resolvers)
