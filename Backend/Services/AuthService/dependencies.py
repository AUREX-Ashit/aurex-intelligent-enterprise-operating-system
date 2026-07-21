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

from fastapi import Depends, Header, HTTPException, status

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
