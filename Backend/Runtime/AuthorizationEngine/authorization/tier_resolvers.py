"""
Runtime Resolver Framework -- tier-specific resolver interfaces (WP-RTA-001 M2).

URA-001-76 (verified directly against
`architecture/02-Constitutional/URA-001 - User, Role, Permission, Event
and ssignment.md` for this milestone -- not assumed) names exactly five
precedence tiers: Named User > Group > Approval Authority > Business
Role > Domain Permission. This module gives each tier its own clean,
named interface, so a future concrete implementation (M5) has a
tier-specific contract rather than one generic, undifferentiated
`TierResolver`.

Each interface here is structurally compatible with M1's own
`TierResolver` Protocol (`authorization.resolvers`) without modifying
it -- `AuthorizationEngine` (M1, unchanged by this milestone) accepts
any object shaped like `TierResolver`; these classes are that shape,
plus a fixed `TIER` identity `ResolverRegistry` (this milestone) uses
to prevent a resolver from being bound to the wrong tier by mistake.

A resolver returns *resolved data about the tier* (a `TierResolution`)
if it reaches a determination for the given `AuthorizationContext`, or
`None` if it was checked and found nothing applicable. It never
queries a database, calls an API, or accesses a repository directly --
those are M5's own concern, injected into a concrete resolver's own
constructor at that time, never assumed by this framework.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from .models import AuthorizationContext, AuthorizationTier
from .resolvers import TierResolution


class BaseTierResolver(ABC):
    """
    Common shape every tier-specific resolver implements. `TIER` is
    fixed per subclass so `ResolverRegistry` (this milestone) can
    verify a resolver is registered against the tier it actually
    resolves, rather than trusting the caller to pair them correctly.
    """

    TIER: ClassVar[AuthorizationTier]

    @abstractmethod
    async def resolve(self, context: AuthorizationContext) -> TierResolution | None:
        """Return a TierResolution if this tier reaches a determination for `context`, else None."""
        raise NotImplementedError


class NamedUserResolver(BaseTierResolver):
    """
    URA-001-76's most specific tier. URA-001-75: assignments may target
    Named Users directly. Resolves whether the specific identity in
    `context` holds a direct, object-scoped assignment (URA-001-77:
    "assignments are always Object Scoped, Event Scoped, and Time
    Scoped") for the governed request -- never a role- or group-level
    inference.
    """

    TIER: ClassVar[AuthorizationTier] = AuthorizationTier.NAMED_USER


class GroupResolver(BaseTierResolver):
    """
    URA-001-76's second tier. URA-001-75: assignments may target
    Groups. Resolves whether the identity's Group membership carries an
    applicable assignment for the governed request, once no more
    specific Named User assignment exists.
    """

    TIER: ClassVar[AuthorizationTier] = AuthorizationTier.GROUP


class ApprovalAuthorityResolver(BaseTierResolver):
    """
    URA-001-76's third tier. Resolves whether an Approval Authority
    (WP-02, `ApprovalAuthority`) held by the identity's Membership
    applies to the governed request -- a policy/catalog record, not
    itself a workflow execution (RTA-001 S11.11: "Approval authority
    shall remain metadata-driven").
    """

    TIER: ClassVar[AuthorizationTier] = AuthorizationTier.APPROVAL_AUTHORITY


class BusinessRoleResolver(BaseTierResolver):
    """
    URA-001-76's fourth tier. Resolves whether the identity's Business
    Role (WP-02, `Role`) carries an applicable Permission for the
    governed request, independent of any Domain Permission grant
    (BR-C003-02 keeps the two deliberately independent).
    """

    TIER: ClassVar[AuthorizationTier] = AuthorizationTier.BUSINESS_ROLE


class DomainPermissionResolver(BaseTierResolver):
    """
    URA-001-76's fifth and least-specific tier -- the final fallback
    before a request is denied. Resolves whether an active Domain
    Permission grant (WP-02, `DomainPermission`) exists for the
    identity's Membership against the requested Domain/permission
    level.
    """

    TIER: ClassVar[AuthorizationTier] = AuthorizationTier.DOMAIN_PERMISSION
