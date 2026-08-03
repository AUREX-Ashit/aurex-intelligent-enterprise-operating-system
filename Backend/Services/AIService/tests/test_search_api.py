# tests/test_search_api.py
"""
WP-11 — Enterprise Search (C-093) API tests, BA-01/02/03 (`IRA-011 §5`/§10).

Includes the Mandatory Tenant-Isolation Test Checklist (`CLAUDE.md §21.4`):
(a) two distinct, unrelated Organizations with no shared row; (b) a caller
in one Organization cannot retrieve or infer another Organization's own
data through these endpoints; (c) an unrelated tenant's own index-name
identifier is probed explicitly, not assumed safe.
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


async def _establish_index(client: AsyncClient, org: str, index_name: str = "enterprise-knowledge-v1") -> dict:
    resp = await client.post(
        "/search/index-configurations",
        json={
            "index_name": index_name,
            "embedding_model": "text-embedding-3-large",
            "embedding_dimension": 1536,
            "retrieval_mode": "HYBRID",
        },
        headers=_auth(org),
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


async def _register_content(client: AsyncClient, org: str, index_name: str, text: str) -> dict:
    resp = await client.post(
        "/search/content",
        json={"index_name": index_name, "text": text, "evidence_source": "Test Source", "file_reference": "test.pdf"},
        headers=_auth(org),
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


# ---------------------------------------------------------------------------
# BA-01 — Establish Enterprise Search Index Configuration
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_establish_index_configuration_requires_platform_admin(client: AsyncClient):
    resp = await client.post(
        "/search/index-configurations",
        json={"index_name": "x", "embedding_model": "m", "embedding_dimension": 8},
        headers=_auth(ORG_A, role_code="MEMBER"),
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_establish_index_configuration_requires_authentication(client: AsyncClient):
    resp = await client.post(
        "/search/index-configurations",
        json={"index_name": "x", "embedding_model": "m", "embedding_dimension": 8},
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_establish_duplicate_index_name_in_same_scope_is_rejected_with_409(client: AsyncClient):
    """
    VV-AUDIT-WP-11 Finding 1 (High, remediated) regression: a second
    active establishment of the same (organization_id, index_name) must
    be rejected cleanly, not silently accepted only to later crash BA-02/
    BA-03 with an unhandled 500 (VectorIndexRegistryRepository.get_by_
    name_for_caller's own scalar_one_or_none() would otherwise raise
    MultipleResultsFound).
    """
    await _establish_index(client, ORG_A, "dup-index")

    resp = await client.post(
        "/search/index-configurations",
        json={
            "index_name": "dup-index",
            "embedding_model": "text-embedding-3-large",
            "embedding_dimension": 1536,
        },
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 409

    # Proves the fix closes the actual failure mode Finding 1 found, not
    # merely the establish path: content registration and search against
    # the (still singular) index continue to work normally afterward.
    registered = await _register_content(client, ORG_A, "dup-index", "Content after a rejected duplicate establish.")
    assert registered["chunk_count"] == 1

    search_resp = await client.post(
        "/search/query", json={"query": "anything", "index_name": "dup-index"}, headers=_auth(ORG_A, role_code="MEMBER")
    )
    assert search_resp.status_code == 200
    assert len(search_resp.json()["results"]) == 1


@pytest.mark.asyncio
async def test_establish_same_index_name_across_platform_wide_and_tenant_scopes_is_allowed(client: AsyncClient):
    """Platform-wide (organization_id NULL) and a tenant-dedicated row are distinct scopes — the same name in each is not a conflict."""
    await _establish_index(client, ORG_A, "scope-distinct-name")

    resp = await client.post(
        "/search/index-configurations",
        json={
            "index_name": "scope-distinct-name",
            "embedding_model": "text-embedding-3-large",
            "embedding_dimension": 1536,
            "platform_wide": True,
        },
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 201


@pytest.mark.asyncio
async def test_establish_and_list_tenant_dedicated_index(client: AsyncClient):
    created = await _establish_index(client, ORG_A)
    assert created["organization_id"] == ORG_A
    assert created["retrieval_mode"] == "HYBRID"

    resp = await client.get("/search/index-configurations", headers=_auth(ORG_A, role_code="MEMBER"))
    assert resp.status_code == 200
    names = [row["index_name"] for row in resp.json()["index_configurations"]]
    assert "enterprise-knowledge-v1" in names


@pytest.mark.asyncio
async def test_platform_wide_index_visible_to_every_tenant(client: AsyncClient):
    resp = await client.post(
        "/search/index-configurations",
        json={
            "index_name": "platform-shared-v1",
            "embedding_model": "text-embedding-3-large",
            "embedding_dimension": 1536,
            "platform_wide": True,
        },
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 201
    assert resp.json()["organization_id"] is None

    for org in (ORG_A, ORG_B):
        listing = await client.get("/search/index-configurations", headers=_auth(org, role_code="MEMBER"))
        names = [row["index_name"] for row in listing.json()["index_configurations"]]
        assert "platform-shared-v1" in names


# ---------------------------------------------------------------------------
# BA-03 — Register Enterprise Search Content
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_register_content_requires_platform_admin(client: AsyncClient):
    await _establish_index(client, ORG_A, "reg-content-index")
    resp = await client.post(
        "/search/content",
        json={"index_name": "reg-content-index", "text": "hello"},
        headers=_auth(ORG_A, role_code="MEMBER"),
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_register_content_against_unknown_index_returns_404(client: AsyncClient):
    resp = await client.post(
        "/search/content",
        json={"index_name": "does-not-exist-anywhere", "text": "hello"},
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_register_content_creates_evidence_and_chunks(client: AsyncClient):
    await _establish_index(client, ORG_A, "content-index")
    registered = await _register_content(
        client, ORG_A, "content-index",
        "The Board maintains 11 permanent directors with 8 independent seats ensuring strong independence.",
    )
    assert registered["chunk_count"] >= 1
    assert len(registered["document_chunk_ids"]) == registered["chunk_count"]


@pytest.mark.asyncio
async def test_register_content_succeeds_against_a_non_default_embedding_dimension(client: AsyncClient):
    """
    CERT-WP-11 Observation 2 regression: establishing an index at a
    dimension other than 1536 must not silently break content
    registration — embedding is now performed by a provider sized to
    the resolved index's own configured dimension, not a fixed default.
    """
    resp = await client.post(
        "/search/index-configurations",
        json={
            "index_name": "non-default-dimension-index",
            "embedding_model": "text-embedding-3-small",
            "embedding_dimension": 768,
            "retrieval_mode": "HYBRID",
        },
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 201

    registered = await _register_content(
        client, ORG_A, "non-default-dimension-index", "Content registered under a 768-dimension index."
    )
    assert registered["chunk_count"] == 1


# ---------------------------------------------------------------------------
# BA-02 — Execute Enterprise Search
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_with_no_registered_content_returns_honest_empty_state(client: AsyncClient):
    await _establish_index(client, ORG_A, "empty-index")
    resp = await client.post(
        "/search/query",
        json={"query": "anything", "index_name": "empty-index"},
        headers=_auth(ORG_A, role_code="MEMBER"),
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["results"] == []
    assert data["message"] is not None


@pytest.mark.asyncio
async def test_search_against_unknown_index_returns_404(client: AsyncClient):
    resp = await client.post(
        "/search/query",
        json={"query": "anything", "index_name": "totally-unregistered-index"},
        headers=_auth(ORG_A, role_code="MEMBER"),
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_search_returns_real_evidence_cited_results_after_registration(client: AsyncClient):
    await _establish_index(client, ORG_A, "real-search-index")
    await _register_content(
        client, ORG_A, "real-search-index",
        "Scope 1 direct emissions totalled 4200.50 metric tons for FY25.",
    )

    resp = await client.post(
        "/search/query",
        json={"query": "What were our Scope 1 emissions?", "index_name": "real-search-index"},
        headers=_auth(ORG_A, role_code="MEMBER"),
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["results"]) == 1
    assert data["message"] is None
    result = data["results"][0]
    assert "Test Source" in result["citation"]
    assert result["metadata"]["source"] == "Test Source"


@pytest.mark.asyncio
async def test_search_resolves_default_single_tenant_index_when_name_omitted(client: AsyncClient):
    await _establish_index(client, ORG_B, "org-b-only-index")
    await _register_content(client, ORG_B, "org-b-only-index", "Org B's own confidential content.")

    resp = await client.post("/search/query", json={"query": "anything"}, headers=_auth(ORG_B, role_code="MEMBER"))
    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 1


# ---------------------------------------------------------------------------
# Mandatory Tenant-Isolation Test Checklist (`CLAUDE.md §21.4`)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_tenant_isolation_index_listing_never_leaks_another_organizations_dedicated_index(
    client: AsyncClient,
):
    """(a)/(b): two distinct Organizations, no shared row; Org B's list never contains Org A's own tenant-dedicated index."""
    await _establish_index(client, ORG_A, "org-a-private-index")

    listing = await client.get("/search/index-configurations", headers=_auth(ORG_B, role_code="MEMBER"))
    names = [row["index_name"] for row in listing.json()["index_configurations"]]
    assert "org-a-private-index" not in names


@pytest.mark.asyncio
async def test_tenant_isolation_probe_unrelated_tenant_index_name_is_not_accepted(client: AsyncClient):
    """
    (c): explicit probe — Org B queries by the exact index_name string Org A
    privately registered. Must NOT resolve to Org A's own row (no shared
    name registered under Org B, no platform-wide row of that name) —
    proves resolution is scoped by organization_id, not merely by name.
    """
    await _establish_index(client, ORG_A, "org-a-exclusive-name")
    await _register_content(client, ORG_A, "org-a-exclusive-name", "Org A's own private ESG disclosure figures.")

    resp = await client.post(
        "/search/query",
        json={"query": "private figures", "index_name": "org-a-exclusive-name"},
        headers=_auth(ORG_B, role_code="MEMBER"),
    )
    assert resp.status_code == 404, "Org B must never resolve Org A's own tenant-dedicated index by name"


@pytest.mark.asyncio
async def test_tenant_isolation_content_registered_under_shared_platform_index_stays_org_scoped(
    client: AsyncClient,
):
    """
    A platform-wide (organization_id NULL) index is visible to every
    tenant, but content registered against it by Org A must not be
    returned to Org B's own search — registration itself is always
    organization-scoped (services/content_registration_service.py),
    independent of whether the index row itself is shared.
    """
    resp = await client.post(
        "/search/index-configurations",
        json={
            "index_name": "shared-index-isolation-test",
            "embedding_model": "text-embedding-3-large",
            "embedding_dimension": 1536,
            "platform_wide": True,
        },
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 201

    await _register_content(
        client, ORG_A, "shared-index-isolation-test", "Org A's own content registered under the shared index."
    )

    org_b_search = await client.post(
        "/search/query",
        json={"query": "anything", "index_name": "shared-index-isolation-test"},
        headers=_auth(ORG_B, role_code="MEMBER"),
    )
    assert org_b_search.status_code == 200
    assert org_b_search.json()["results"] == [], "Org B must not see Org A's own content, even under a shared index"
