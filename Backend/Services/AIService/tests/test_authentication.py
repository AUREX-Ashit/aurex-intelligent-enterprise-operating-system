# tests/test_authentication.py
"""
AIService Authentication Bootstrap — platform prerequisite tests (`IRA-011 §4.4`).

Proves the previously-nonexistent authentication gap (§3/§4.4 of that IRA —
every existing router trusted an unverified, client-supplied tenant header)
is closed: a real, verified JWT claims dependency now exists, matching
`AuthService`'s own token contract exactly. Not tied to any WP-11 Business
Activity — none exists yet — these are direct unit tests against the
prerequisite's own two functions.
"""
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException
from jose import jwt

from config.settings import settings
from dependencies import decode_access_token, get_current_claims

_CLAIMS = {
    "person_id": "11111111-1111-1111-1111-111111111111",
    "identity_id": "22222222-2222-2222-2222-222222222222",
    "organization_id": "33333333-3333-3333-3333-333333333333",
    "membership_id": "44444444-4444-4444-4444-444444444444",
    "role_code": "PLATFORM_ADMIN",
}


def _make_token(token_type: str = "access", expired: bool = False, secret: str | None = None) -> str:
    expire = datetime.now(timezone.utc) + (
        timedelta(minutes=-5) if expired else timedelta(minutes=60)
    )
    claims = {**_CLAIMS, "type": token_type, "exp": expire}
    return jwt.encode(claims, secret or settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def test_decode_access_token_accepts_a_valid_authservice_shaped_token():
    """A token carrying AuthService's own real claim shape decodes and verifies here identically."""
    token = _make_token()
    claims = decode_access_token(token)
    assert claims["organization_id"] == _CLAIMS["organization_id"]
    assert claims["person_id"] == _CLAIMS["person_id"]
    assert claims["role_code"] == "PLATFORM_ADMIN"
    assert claims["type"] == "access"


def test_decode_access_token_rejects_expired_token():
    token = _make_token(expired=True)
    with pytest.raises(HTTPException) as exc:
        decode_access_token(token)
    assert exc.value.status_code == 401


def test_decode_access_token_rejects_wrong_token_type():
    token = _make_token(token_type="refresh")
    with pytest.raises(HTTPException) as exc:
        decode_access_token(token)
    assert exc.value.status_code == 401


def test_decode_access_token_rejects_bad_signature():
    token = _make_token(secret="a-completely-different-secret-value")
    with pytest.raises(HTTPException) as exc:
        decode_access_token(token)
    assert exc.value.status_code == 401


def test_decode_access_token_rejects_malformed_token():
    with pytest.raises(HTTPException) as exc:
        decode_access_token("not-a-real-jwt")
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_claims_requires_bearer_header():
    with pytest.raises(HTTPException) as exc:
        await get_current_claims(authorization=None)
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_get_current_claims_rejects_non_bearer_scheme():
    with pytest.raises(HTTPException) as exc:
        await get_current_claims(authorization="Basic dXNlcjpwYXNz")
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_get_current_claims_accepts_valid_bearer_token():
    token = _make_token()
    claims = await get_current_claims(authorization=f"Bearer {token}")
    assert claims["organization_id"] == _CLAIMS["organization_id"]
