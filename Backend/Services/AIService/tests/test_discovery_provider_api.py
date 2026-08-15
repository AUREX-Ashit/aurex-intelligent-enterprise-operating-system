# tests/test_discovery_provider_api.py
"""
WP-14 BA-01 — Establish Discovery Provider Configuration (C-090) API tests.

Includes the Mandatory Tenant-Isolation Test Checklist (`CLAUDE.md §21.4`):
(a) two distinct, unrelated Organizations with no shared row; (b) a caller
in one Organization cannot retrieve or infer another Organization's own
tenant-dedicated Discovery Provider through the list path; (c) a
platform-wide provider is visible to every Organization, the disclosed,
intended contract for `organization_id IS NULL`, not an unintended leak.
"""
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from httpx import AsyncClient
from jose import jwt

from config.settings import settings

ORG_A = str(uuid4())
ORG_B = str(uuid4())


def _token(organization_id: str, role_code: str = "PLATFORM_ADMIN") -> str:
    claims = {
        "person_id": str(uuid4()),
        "identity_id": str(uuid4()),
        "organization_id": organization_id,
        "membership_id": str(uuid4()),
        "role_code": role_code,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=60),
    }
    return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def _auth(organization_id: str, role_code: str = "PLATFORM_ADMIN") -> dict:
    return {"Authorization": f"Bearer {_token(organization_id, role_code)}"}


async def _establish(
    client: AsyncClient,
    org: str,
    provider_name: str = "Finance SharePoint",
    provider_category: str = "ENTERPRISE",
    provider_type: str = "SHAREPOINT",
    platform_wide: bool = False,
) -> dict:
    resp = await client.post(
        "/discovery-providers",
        json={
            "provider_name": provider_name,
            "provider_category": provider_category,
            "provider_type": provider_type,
            "discovery_cadence": "SCHEDULED",
            "platform_wide": platform_wide,
        },
        headers=_auth(org),
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


# ---------------------------------------------------------------------------
# Establishment — success path, business rules, acceptance criteria
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_establish_discovery_provider_succeeds(client: AsyncClient):
    body = await _establish(client, ORG_A)
    assert body["provider_category"] == "ENTERPRISE"
    assert body["provider_type"] == "SHAREPOINT"
    assert body["organization_id"] == ORG_A
    assert body["active_flag"] is False
    assert body["credential_id"] is None
    assert body["governing_policy_id"] is None


@pytest.mark.asyncio
async def test_establish_with_category_type_mismatch_is_rejected_with_422(client: AsyncClient):
    """Acceptance criteria (IRA-014 §6 BA-01): 'provider_type/provider_category mismatch is rejected (422)'."""
    resp = await client.post(
        "/discovery-providers",
        json={
            "provider_category": "ENTERPRISE",
            "provider_type": "CORPORATE_WEBSITE",
            "platform_wide": False,
        },
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_establish_with_invalid_provider_type_is_rejected_with_422(client: AsyncClient):
    resp = await client.post(
        "/discovery-providers",
        json={"provider_category": "ENTERPRISE", "provider_type": "NOT_A_REAL_TYPE"},
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_establish_with_invalid_provider_category_is_rejected_with_422(client: AsyncClient):
    resp = await client.post(
        "/discovery-providers",
        json={"provider_category": "NOT_A_REAL_CATEGORY", "provider_type": "SHAREPOINT"},
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_establish_external_category_with_external_type_succeeds(client: AsyncClient):
    body = await _establish(
        client, ORG_A, provider_name="Annual Report Feed", provider_category="EXTERNAL", provider_type="ANNUAL_REPORT"
    )
    assert body["provider_category"] == "EXTERNAL"
    assert body["provider_type"] == "ANNUAL_REPORT"


@pytest.mark.asyncio
async def test_establish_realtime_category_with_realtime_type_succeeds(client: AsyncClient):
    body = await _establish(
        client, ORG_A, provider_name="Plant A IoT Feed", provider_category="REALTIME", provider_type="IOT"
    )
    assert body["provider_category"] == "REALTIME"
    assert body["provider_type"] == "IOT"


@pytest.mark.asyncio
async def test_establish_platform_wide_produces_null_organization_id(client: AsyncClient):
    body = await _establish(client, ORG_A, provider_name="Public Benchmark Feed", platform_wide=True)
    assert body["organization_id"] is None


# ---------------------------------------------------------------------------
# Authorization
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_establish_discovery_provider_requires_platform_admin(client: AsyncClient):
    resp = await client.post(
        "/discovery-providers",
        json={"provider_category": "ENTERPRISE", "provider_type": "SHAREPOINT"},
        headers=_auth(ORG_A, role_code="MEMBER"),
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_establish_discovery_provider_requires_authentication(client: AsyncClient):
    resp = await client.post(
        "/discovery-providers",
        json={"provider_category": "ENTERPRISE", "provider_type": "SHAREPOINT"},
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_list_discovery_providers_does_not_require_platform_admin(client: AsyncClient):
    """Mirrors WP-11 BA-01's own precedent — establish is gated, list is not."""
    resp = await client.get("/discovery-providers", headers=_auth(ORG_A, role_code="MEMBER"))
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Mandatory Tenant-Isolation Test Checklist (CLAUDE.md §21.4)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_two_orgs_no_shared_row(client: AsyncClient):
    """(a) two distinct, unrelated Organizations, no shared row."""
    provider_a = await _establish(client, ORG_A, provider_name="Org A SharePoint")
    provider_b = await _establish(client, ORG_B, provider_name="Org B SharePoint")
    assert provider_a["discovery_provider_id"] != provider_b["discovery_provider_id"]
    assert provider_a["organization_id"] == ORG_A
    assert provider_b["organization_id"] == ORG_B


@pytest.mark.asyncio
async def test_org_a_cannot_see_org_bs_tenant_dedicated_provider(client: AsyncClient):
    """(b) a caller in one Organization cannot retrieve or infer another Organization's own tenant-dedicated Discovery Provider."""
    provider_b = await _establish(client, ORG_B, provider_name="Org B Only Provider")

    resp = await client.get("/discovery-providers", headers=_auth(ORG_A))
    assert resp.status_code == 200
    visible_ids = [p["discovery_provider_id"] for p in resp.json()["discovery_providers"]]
    assert provider_b["discovery_provider_id"] not in visible_ids


@pytest.mark.asyncio
async def test_platform_wide_provider_visible_to_every_organization(client: AsyncClient):
    """(c) a platform-wide provider (organization_id NULL) is visible to every Organization — the disclosed, intended contract, not an unintended cross-tenant leak."""
    shared = await _establish(client, ORG_A, provider_name="Public Benchmark Feed", platform_wide=True)

    resp_a = await client.get("/discovery-providers", headers=_auth(ORG_A))
    resp_b = await client.get("/discovery-providers", headers=_auth(ORG_B))
    ids_a = [p["discovery_provider_id"] for p in resp_a.json()["discovery_providers"]]
    ids_b = [p["discovery_provider_id"] for p in resp_b.json()["discovery_providers"]]
    assert shared["discovery_provider_id"] in ids_a
    assert shared["discovery_provider_id"] in ids_b


@pytest.mark.asyncio
async def test_org_b_tenant_dedicated_provider_never_appears_in_org_a_list_even_with_shared_platform_wide_row(
    client: AsyncClient,
):
    """Explicit probe: mixing a platform-wide row with a tenant-dedicated row never leaks the tenant-dedicated one cross-tenant."""
    await _establish(client, ORG_A, provider_name="Shared Feed", platform_wide=True)
    provider_b = await _establish(client, ORG_B, provider_name="Org B Private Feed")

    resp = await client.get("/discovery-providers", headers=_auth(ORG_A))
    visible_ids = [p["discovery_provider_id"] for p in resp.json()["discovery_providers"]]
    assert provider_b["discovery_provider_id"] not in visible_ids
