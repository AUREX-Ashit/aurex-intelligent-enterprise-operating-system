# dependencies.py
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from jose import JWTError, jwt

from config.settings import settings

_INVALID_TOKEN = "Credentials verification failed."


def decode_access_token(token: str) -> dict:
    """
    Verifies an access token's signature and expiry and returns its claims.

    AIService Authentication Bootstrap (platform prerequisite, `IRA-011 §4.4`,
    gates WP-11 BA-01/02/03 — not itself a Business Activity). Mirrors
    `AuthService/services/auth_service.py::decode_access_token` exactly —
    same library (`python-jose`), same settings-resolved secret/algorithm,
    same claim shape (`person_id`, `identity_id`, `organization_id`,
    `membership_id`, `role_code`, `type`, `exp`) — so a token issued by
    `AuthService`'s own `/auth/login` verifies identically here. This is the
    existing `URA-001` authentication model reused, not a new one.

    `Backend/Shared/Security/jwt_manager.py` was evaluated as the
    architecturally cleaner reuse target and rejected: its own
    `create_token()` claim shape (`sub`, `tenant_id`, `roles`, `permissions`)
    does not match the claims `AuthService` actually issues — consuming it
    here would not let this service verify real, live tokens without also
    modifying already-certified `AuthService` code, which exceeds this
    prerequisite's own minimum-necessary scope.
    """
    try:
        claims = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_INVALID_TOKEN,
        )

    if claims.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type.",
        )

    return claims


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
    """
    403 if the authenticated caller does not hold the PLATFORM_ADMIN role.

    WP-11 BA-01/BA-03 write-path gate — the same interim measure this
    repository already uses platform-wide (`TD-021`-class) wherever no
    dedicated persona exists yet; `PE-001-C093` names none (`IRA-011 §5`).
    Mirrors `AuthService/dependencies.py::require_platform_admin` exactly.
    """
    if claims.get("role_code") != "PLATFORM_ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This operation requires the PLATFORM_ADMIN role.",
        )
    return claims
