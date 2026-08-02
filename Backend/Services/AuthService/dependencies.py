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

from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status

from middleware.tenant import get_current_tenant
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
