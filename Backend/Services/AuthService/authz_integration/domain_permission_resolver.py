"""
WP-13 (Authorization Runtime Integration). The first real, database-
backed TierResolver bound to the Authorization Runtime Engine
(`Backend/Runtime/AuthorizationEngine`, WP-RTA-001) anywhere in this
repository — closing the gap that engine's own README discloses
directly: "No Business Activity or FastAPI endpoint consumes this
runtime yet."

Realizes URA-001-76's fifth and least-specific precedence tier
(Domain Permission) against AuthService's own real `DomainPermission`
table (WP-02 BA-02), reusing `DomainPermissionRepository`'s own new
`get_active_grant_at_or_above()` method (WP-13) rather than querying
the table directly here — this module is authorization-decision logic
only, not a second data-access layer.

Per `authorization.tier_resolvers`'s own module docstring, "the
specific governed request" (which Domain, which minimum
DomainPermissionLevel) is not part of the shared, capability-agnostic
`AuthorizationContext` — it is injected into this resolver's own
constructor at integration time, exactly as that module anticipates.
"""

from __future__ import annotations

import uuid

from authz_integration.runtime_engine_path import ensure_on_path

ensure_on_path()

from authorization.resolvers import TierResolution  # noqa: E402  (Runtime engine's own module, not this package's)
from authorization.tier_resolvers import DomainPermissionResolver as _BaseDomainPermissionResolver  # noqa: E402
from authorization.models import AuthorizationContext, AuthorizationDecision  # noqa: E402

from models.domain_permission import DomainPermissionLevel
from repositories.domain_permission_repository import DomainPermissionRepository


class AuthServiceDomainPermissionResolver(_BaseDomainPermissionResolver):
    """
    Concrete `DomainPermissionResolver` (Runtime Engine, M2 interface),
    bound to one specific Domain + minimum DomainPermissionLevel per
    instance — constructed fresh per request by the FastAPI dependency
    that uses it (`dependencies.py::require_domain_permission`), never
    shared or cached across requests, since the governed request itself
    (which Domain, which level) varies per call site.
    """

    def __init__(
        self,
        repository: DomainPermissionRepository,
        domain_id: uuid.UUID,
        minimum_level: DomainPermissionLevel,
    ) -> None:
        self._repository = repository
        self._domain_id = domain_id
        self._minimum_level = minimum_level

    async def resolve(self, context: AuthorizationContext) -> TierResolution | None:
        if context.membership_id is None:
            return None  # NO_MATCH — a caller with no Membership cannot hold a Domain Permission grant

        grant = await self._repository.get_active_grant_at_or_above(
            membership_id=uuid.UUID(context.membership_id),
            domain_id=self._domain_id,
            minimum_level=self._minimum_level.value,
        )
        if grant is None:
            return None  # NO_MATCH — checked, found nothing; the engine reports this as such, never fabricates ALLOW

        return TierResolution(
            decision=AuthorizationDecision.ALLOW,
            reason=(
                f"Active DomainPermission grant {grant.id} — membership {grant.membership_id} "
                f"holds '{grant.permission_level}' on domain {grant.domain_id}, "
                f"at or above the requested '{self._minimum_level.value}'."
            ),
        )
