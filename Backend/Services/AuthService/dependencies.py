"""
Shared, cross-router FastAPI dependencies.

Currently: Bearer-token authentication and role-gating. Introduced by
WP-01 (Establish Organization) because it's the first Business Activity
in this service that requires an authenticated, role-checked caller —
every route before this (health, ready, auth, person) was deliberately
public or auth-agnostic. Lives here, not inside routers/organization.py,
so the next router that needs authentication reuses it instead of
re-implementing it (CLAUDE.md §8 — never duplicate business logic).

IRA-001 §2.7 scope note: this checks only the existing, WP-00-seeded
PLATFORM_ADMIN role_code claim — not Domain Permissions (URA-001 §4
VIEW/EDIT/APPROVE/etc.), which belong to the separate, not-yet-built
Role & Permission Management work package. This is a deliberate,
documented simplification, not a silent gap.
"""

from typing import Annotated, Callable
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from middleware.tenant import get_current_tenant
from models.database import db_manager
from models.domain_permission import DomainPermissionLevel
from services.auth_service import decode_access_token

PLATFORM_ADMIN_ROLE_CODE = "PLATFORM_ADMIN"


async def get_current_claims(
    authorization: Annotated[str | None, Header(description="Bearer <access_token>")] = None,
) -> dict:
    """Extracts and verifies the caller's access token. 400 if the header itself is missing/malformed, 401 if the token doesn't verify."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Header 'Authorization' must be populated with a Bearer token.",
        )
    token = authorization.split(" ", 1)[1]
    return decode_access_token(token)


async def require_platform_admin(
    claims: Annotated[dict, Depends(get_current_claims)],
) -> dict:
    """403 if the authenticated caller does not hold the PLATFORM_ADMIN role."""
    if claims.get("role_code") != PLATFORM_ADMIN_ROLE_CODE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"This operation requires the {PLATFORM_ADMIN_ROLE_CODE} role.",
        )
    return claims


async def require_matching_tenant_or_platform_admin(
    claims: Annotated[dict, Depends(get_current_claims)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant)],
) -> dict:
    """
    403 unless the authenticated caller's own JWT `organization_id` claim
    matches the request's `X-Tenant-ID`, or the caller holds
    PLATFORM_ADMIN (who may act on any tenant).

    Introduced by WP-10 (`routers/configuration.py`'s `GET /configuration`)
    to close a cross-tenant disclosure `CERT-WP-10` Finding B-1 confirmed
    empirically: without this check, any authenticated caller — including
    one with no Membership whatsoever in the target Organization — could
    read that Organization's Configuration simply by naming its UUID in
    `X-Tenant-ID`, since `get_current_tenant()` alone only verifies the
    header is a well-formed UUID, never that the caller has any
    relationship to it. This is the first endpoint in this codebase
    combining an intentionally-open (non-`PLATFORM_ADMIN`) authorization
    posture with a genuinely non-exempted tenant header — every prior
    genuinely-tenant-scoped resource used `require_platform_admin` alone
    (`TD-021`-class), which was sufficient there because those endpoints
    already restricted every caller to `PLATFORM_ADMIN` regardless of
    tenant. `GET /configuration` cannot reuse that gate without
    regressing BA-01's own Business Intent (every caller resolves their
    own tenant, not only an administrator's).
    """
    if claims.get("role_code") == PLATFORM_ADMIN_ROLE_CODE:
        return claims
    if claims.get("organization_id") != str(tenant_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="X-Tenant-ID must match your own Organization, unless you hold PLATFORM_ADMIN.",
        )
    return claims


async def enforce_domain_permission(
    claims: dict,
    session: AsyncSession,
    domain_id: UUID,
    minimum_level: DomainPermissionLevel,
) -> None:
    """
    WP-13 (Authorization Runtime Integration) — the real check, evaluated
    through the Authorization Runtime Engine
    (`Backend/Runtime/AuthorizationEngine`, WP-RTA-001) against a real,
    database-backed DomainPermission grant (URA-001-76's fifth
    precedence tier), replacing the interim `PLATFORM_ADMIN`-only
    pattern every prior Work Package in this repository used
    (`TD-021`-class). Raises `HTTPException(403)` on denial; returns
    `None` on success — call-site style (a plain function, not a
    dependency) so it works equally for a route's own static, known-at-
    registration-time domain (via `require_domain_permission`, below)
    and for a domain that is only known once the request body has been
    parsed inside the route handler itself (e.g. `establish_domain_permission`'s
    own `request.domain_id`) — a case the original single-shape
    dependency factory could not express, corrected here rather than
    worked around with a second, parallel mechanism.

    `PLATFORM_ADMIN` remains a universal bypass — this is a strictly
    additive replacement, never a narrowing of who was already permitted
    to act.

    A fresh `ResolverRegistry`/`EvaluationPipeline`/`AuthorizationAdapter`
    is constructed per call, since the governed request itself (which
    Domain, which minimum level) is injected into the bound resolver's
    own constructor and therefore varies per call site — consistent with
    `authorization.tier_resolvers`'s own documented integration contract
    (Runtime Engine, M2), not a deviation from it.
    """
    if claims.get("role_code") == PLATFORM_ADMIN_ROLE_CODE:
        return

    from authz_integration.domain_permission_resolver import AuthServiceDomainPermissionResolver
    from authorization.models import AuthorizationDecision
    from authorization.pipeline import EvaluationPipeline
    from authorization.registry import ResolverRegistry
    from adapters.authorization_adapter import AuthorizationAdapter, AuthorizationRequest
    from repositories.domain_permission_repository import DomainPermissionRepository

    repository = DomainPermissionRepository(session)
    resolver = AuthServiceDomainPermissionResolver(repository, domain_id, minimum_level)
    registry = ResolverRegistry().register(resolver)
    pipeline = EvaluationPipeline(registry)
    adapter = AuthorizationAdapter(pipeline)

    result = await adapter.evaluate(
        AuthorizationRequest(
            identity_id=claims.get("person_id", ""),
            organization_id=claims.get("organization_id", ""),
            membership_id=claims.get("membership_id"),
        )
    )
    if result.decision != AuthorizationDecision.ALLOW:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                f"This operation requires an active DomainPermission grant of "
                f"'{minimum_level.value}' or higher on domain {domain_id}."
            ),
        )


def require_domain_permission(domain_id: UUID, minimum_level: DomainPermissionLevel) -> Callable:
    """
    Dependency-factory wrapper around `enforce_domain_permission()`, for
    the common case where the governed Domain is fixed at route-
    registration time (a path-scoped or capability-scoped resource, not
    one named inside a request body). See `enforce_domain_permission`'s
    own docstring for the full design rationale.
    """

    async def _dependency(
        claims: Annotated[dict, Depends(get_current_claims)],
        session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    ) -> dict:
        await enforce_domain_permission(claims, session, domain_id, minimum_level)
        return claims

    return _dependency
