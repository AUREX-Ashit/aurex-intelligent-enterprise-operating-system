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


def require_authority_holder(authority_identity: str) -> Callable:
    """
    C-040 Authority Runtime Enforcement (TDS-017 §22/§24) — dependency
    factory, one instance per constitutional authority (`require_ai001_holder`/
    `require_ai002_holder`, below), mirroring `require_domain_permission`'s
    own factory shape.

    Deliberately structured like `require_platform_admin` (a direct claims
    comparison, Depends(get_current_claims), no `AuthorizationContext`, no
    `Backend/Runtime/AuthorizationEngine` involvement, per TDS-017 §5/§11) —
    but compares the caller's own `person_id` against a live database
    lookup of the currently ACTIVE `authority_holders` row for
    `authority_identity`, never a role, never `PLATFORM_ADMIN`, never
    `AUREX_ADMIN`, never a Group, never Organization membership, and never
    a self-asserted claim embedded in the token itself (TDS-017 §22's own
    "the runtime authorization check remains a live lookup... rather than
    trusting an authority claim embedded in the JWT").

    If no ACTIVE row exists for `authority_identity` (e.g. AI-002, `TD-157`,
    unpopulated), every caller is correctly and permanently denied — this
    dependency never simulates, infers, or defaults a holder.
    """

    async def _dependency(
        claims: Annotated[dict, Depends(get_current_claims)],
        session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    ) -> dict:
        from repositories.authority_holder_repository import AuthorityHolderRepository

        person_id_str = claims.get("person_id")
        if not person_id_str:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This operation requires the currently appointed {authority_identity} accountability point.",
            )

        repo = AuthorityHolderRepository(session)
        active_holder = await repo.get_active_by_authority(authority_identity)
        if not active_holder or str(active_holder.holder_person_id) != person_id_str:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This operation requires the currently appointed {authority_identity} accountability point.",
            )

        return claims

    return _dependency


require_ai001_holder = require_authority_holder("AI-001")
require_ai002_holder = require_authority_holder("AI-002")


async def enforce_approval_authority(
    claims: dict,
    session: AsyncSession,
    target_organization_id: UUID,
    authority_name: str,
) -> None:
    """
    WP-18 (C-003, TDS-018 §29.2) — the real check, evaluated through
    `resolve_approval_authority()`'s own 8-step algorithm against a real,
    database-backed `approval_authorities` row and
    `membership_approval_authority` binding. Raises `HTTPException(403)`
    on any DENY outcome; returns `None` on `AUTHORIZED` — call-site style
    (a plain function, not a dependency) mirroring
    `enforce_domain_permission`'s own established split.

    Deliberately structured like `require_authority_holder`/
    `require_platform_admin` (TDS-018 §12 Option B — a direct claims
    comparison plus one live database lookup, no `AuthorizationContext`,
    no `Backend/Runtime/AuthorizationEngine` involvement) — but resolves
    an Organization-scoped `approval_authorities` row via a Membership
    binding, never a role, never `PLATFORM_ADMIN`, never `AUREX_ADMIN`,
    never a Group. **No admin bypass exists here, unlike
    `enforce_domain_permission`'s own `PLATFORM_ADMIN` universal-bypass
    precedent** — TDS-018 §11/§18 explicitly prohibit any such fallback
    for this specific gate.

    `target_organization_id` is deliberately a separate parameter from
    the caller's own claimed `organization_id` — TDS-018 §29.2 step 4
    requires comparing the two, which would be vacuous if both were
    derived from the same claim.
    """
    from services.approval_authority_resolver import ApprovalAuthorityResolution, resolve_approval_authority

    person_id_str = claims.get("person_id")
    organization_id_str = claims.get("organization_id")
    membership_id_str = claims.get("membership_id")

    caller_organization_id = UUID(organization_id_str) if organization_id_str else None
    caller_membership_id = UUID(membership_id_str) if membership_id_str else None

    reason = await resolve_approval_authority(
        session=session,
        target_organization_id=target_organization_id,
        authority_name=authority_name,
        caller_organization_id=caller_organization_id,
        caller_membership_id=caller_membership_id,
        actor_id=person_id_str,
    )
    if reason != ApprovalAuthorityResolution.AUTHORIZED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"This operation requires the currently-satisfied '{authority_name}' Approval Authority ({reason.value}).",
        )


def require_approval_authority(authority_name: str) -> Callable:
    """
    Dependency-factory wrapper around `enforce_approval_authority()`, for
    the common case where the required `authority_name` is fixed at
    route-registration time and the target Organization is the request's
    own `X-Tenant-ID` — mirrors `require_domain_permission`'s own factory
    shape exactly (TDS-018 §12 Option B; `require_authority_holder` is
    the nearest existing precedent this dependency's own shape is
    modeled on).
    """

    async def _dependency(
        claims: Annotated[dict, Depends(get_current_claims)],
        tenant_id: Annotated[UUID, Depends(get_current_tenant)],
        session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    ) -> dict:
        await enforce_approval_authority(claims, session, tenant_id, authority_name)
        return claims

    return _dependency
