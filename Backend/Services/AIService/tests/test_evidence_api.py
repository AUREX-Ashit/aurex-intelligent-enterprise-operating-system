# tests/test_evidence_api.py
"""
WP-15 BA-01 — Understand Evidence Context (C-066 Evidence Management) API
tests (`TDS-015`, `WP-15_C066_BA-01_..._Business_Activity_Charter.md`).

No establish-Evidence endpoint exists (write path is WP-11's/WP-14's own
exclusive province, `TDS-015 §1`) — rows are seeded directly via
`db_session`, mirroring the existing repository precedent for read-only
Business Activities with no API-level establish path of their own.

Includes the Mandatory Tenant-Isolation Test Checklist (`CLAUDE.md
§21.4`): (a) two distinct, unrelated Organizations with no shared row;
(b) a caller in one Organization cannot retrieve or infer another
Organization's own Evidence through either endpoint; (c) an unrelated
Organization's `evidence_id` supplied explicitly to the single-item
endpoint is rejected as 404, not a disclosing 403.
"""
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient
from jose import jwt

from config.settings import settings
from models.search import EvidenceRegistryModel

ORG_A = str(uuid4())
ORG_B = str(uuid4())


def _token(organization_id: str, role_code: str = "MEMBER") -> str:
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


def _auth(organization_id: str, role_code: str = "MEMBER") -> dict:
    return {"Authorization": f"Bearer {_token(organization_id, role_code)}"}


def _token_missing_organization_id(role_code: str = "MEMBER") -> str:
    """
    Gate 2 V&V remediation (Finding C-2): a validly-signed token that omits
    the `organization_id` claim entirely — distinct from an invalid
    signature (already covered by `dependencies.get_current_claims`'s own
    401) and from a missing `Authorization` header (already covered, 400).
    """
    claims = {
        "person_id": str(uuid4()),
        "identity_id": str(uuid4()),
        "membership_id": str(uuid4()),
        "role_code": role_code,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=60),
    }
    return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def _auth_missing_organization_id(role_code: str = "MEMBER") -> dict:
    return {"Authorization": f"Bearer {_token_missing_organization_id(role_code)}"}


async def _seed_evidence(
    db_session,
    org: str,
    *,
    evidence_type: str | None = "invoice",
    evidence_source: str | None = "Test Source",
    linked_entity_type: str | None = None,
    linked_entity_id: UUID | None = None,
    confidence_score: int | None = 80,
) -> EvidenceRegistryModel:
    row = EvidenceRegistryModel(
        organization_id=UUID(org),
        evidence_type=evidence_type,
        evidence_source=evidence_source,
        linked_entity_type=linked_entity_type,
        linked_entity_id=linked_entity_id,
        confidence_score=confidence_score,
        active_flag=True,
    )
    db_session.add(row)
    await db_session.flush()
    return row


# ---------------------------------------------------------------------------
# GET /evidence/{evidence_id} — single item
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_evidence_own_organization_returns_200(client: AsyncClient, db_session):
    row = await _seed_evidence(db_session, ORG_A, evidence_type="invoice", evidence_source="Utility Co.")
    resp = await client.get(f"/evidence/{row.evidence_id}", headers=_auth(ORG_A))
    assert resp.status_code == 200
    body = resp.json()
    assert body["evidence_id"] == str(row.evidence_id)
    assert body["organization_id"] == ORG_A
    assert body["evidence_type"] == "invoice"
    assert body["evidence_source"] == "Utility Co."


@pytest.mark.asyncio
async def test_get_evidence_nonexistent_id_returns_404(client: AsyncClient):
    resp = await client.get(f"/evidence/{uuid4()}", headers=_auth(ORG_A))
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_evidence_no_x_tenant_id_header_required(client: AsyncClient, db_session):
    """RO-DEC-C066-BA01-03 (Option C): organization_id derives solely from the
    JWT claim via get_current_claims — no X-Tenant-ID header is required or
    consulted, unlike this middleware's own default-enforced routes."""
    row = await _seed_evidence(db_session, ORG_A)
    resp = await client.get(f"/evidence/{row.evidence_id}", headers=_auth(ORG_A))
    assert resp.status_code == 200
    assert "X-Tenant-ID" not in resp.request.headers


# ---------------------------------------------------------------------------
# Mandatory Tenant-Isolation Test Checklist (CLAUDE.md §21.4)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_two_orgs_no_shared_row(client: AsyncClient, db_session):
    """(a) two distinct, unrelated Organizations, no shared row."""
    row_a = await _seed_evidence(db_session, ORG_A, evidence_source="Org A Source")
    row_b = await _seed_evidence(db_session, ORG_B, evidence_source="Org B Source")
    assert row_a.evidence_id != row_b.evidence_id
    assert row_a.organization_id != row_b.organization_id


@pytest.mark.asyncio
async def test_org_a_cannot_retrieve_org_bs_evidence_by_id(client: AsyncClient, db_session):
    """(b)/(c) — an unrelated Organization's evidence_id supplied explicitly
    to the single-item endpoint is rejected as 404, not disclosed via 403."""
    row_b = await _seed_evidence(db_session, ORG_B, evidence_source="Org B Confidential Source")
    resp = await client.get(f"/evidence/{row_b.evidence_id}", headers=_auth(ORG_A))
    assert resp.status_code == 404
    assert resp.status_code != 403


@pytest.mark.asyncio
async def test_org_a_list_never_contains_org_bs_evidence(client: AsyncClient, db_session):
    """(b) — a caller in one Organization cannot retrieve or infer another
    Organization's own Evidence through the list path."""
    await _seed_evidence(db_session, ORG_A, evidence_source="Org A Source")
    await _seed_evidence(db_session, ORG_B, evidence_source="Org B Source")

    resp = await client.get("/evidence", headers=_auth(ORG_A))
    assert resp.status_code == 200
    items = resp.json()["evidence_items"]
    assert len(items) == 1
    assert items[0]["organization_id"] == ORG_A
    assert all(item["organization_id"] == ORG_A for item in items)


# ---------------------------------------------------------------------------
# PLATFORM_ADMIN behavior — single-item vs. list are deliberately different
# (TDS-015 §9/§13 for single-item; RO-DEC-C066-BA01-05 for list)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_platform_admin_can_retrieve_another_orgs_evidence_by_id(client: AsyncClient, db_session):
    row_b = await _seed_evidence(db_session, ORG_B, evidence_source="Org B Source")
    resp = await client.get(f"/evidence/{row_b.evidence_id}", headers=_auth(ORG_A, role_code="PLATFORM_ADMIN"))
    assert resp.status_code == 200
    assert resp.json()["organization_id"] == ORG_B


@pytest.mark.asyncio
async def test_platform_admin_list_still_scoped_to_own_organization_only(client: AsyncClient, db_session):
    """RO-DEC-C066-BA01-05: no PLATFORM_ADMIN cross-Organization listing —
    the list endpoint's own restriction applies identically regardless of
    role, unlike the single-item endpoint's own permitted exception above."""
    await _seed_evidence(db_session, ORG_A, evidence_source="Org A Source")
    await _seed_evidence(db_session, ORG_B, evidence_source="Org B Source")

    resp = await client.get("/evidence", headers=_auth(ORG_A, role_code="PLATFORM_ADMIN"))
    assert resp.status_code == 200
    items = resp.json()["evidence_items"]
    assert len(items) == 1
    assert items[0]["organization_id"] == ORG_A


@pytest.mark.asyncio
async def test_no_target_organization_selector_accepted_by_list_endpoint(client: AsyncClient, db_session):
    """RO-DEC-C066-BA01-05: no target-Organization selector parameter exists
    at all — supplying an arbitrary/unknown query param has no effect on
    scoping (FastAPI ignores unrecognized query params; scope stays own-org)."""
    await _seed_evidence(db_session, ORG_A, evidence_source="Org A Source")
    await _seed_evidence(db_session, ORG_B, evidence_source="Org B Source")

    resp = await client.get(
        "/evidence",
        params={"organization_id": ORG_B, "target_organization_id": ORG_B},
        headers=_auth(ORG_A, role_code="PLATFORM_ADMIN"),
    )
    assert resp.status_code == 200
    items = resp.json()["evidence_items"]
    assert len(items) == 1
    assert items[0]["organization_id"] == ORG_A


# ---------------------------------------------------------------------------
# GET /evidence — filtering and empty-state behavior
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_list_evidence_empty_result_is_200_not_404(client: AsyncClient):
    resp = await client.get("/evidence", headers=_auth(ORG_A))
    assert resp.status_code == 200
    assert resp.json()["evidence_items"] == []


@pytest.mark.asyncio
async def test_list_evidence_filters_by_linked_entity_type_and_id(client: AsyncClient, db_session):
    linked_id = uuid4()
    matching = await _seed_evidence(
        db_session, ORG_A, linked_entity_type="customer_metric_registry", linked_entity_id=linked_id
    )
    await _seed_evidence(
        db_session, ORG_A, linked_entity_type="customer_metric_registry", linked_entity_id=uuid4()
    )
    await _seed_evidence(db_session, ORG_A, linked_entity_type=None, linked_entity_id=None)

    resp = await client.get(
        "/evidence",
        params={"linked_entity_type": "customer_metric_registry", "linked_entity_id": str(linked_id)},
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 200
    items = resp.json()["evidence_items"]
    assert len(items) == 1
    assert items[0]["evidence_id"] == str(matching.evidence_id)


@pytest.mark.asyncio
async def test_list_evidence_filters_by_evidence_source_and_type(client: AsyncClient, db_session):
    matching = await _seed_evidence(db_session, ORG_A, evidence_type="invoice", evidence_source="Utility Co.")
    await _seed_evidence(db_session, ORG_A, evidence_type="report", evidence_source="Audit Firm")

    resp = await client.get(
        "/evidence",
        params={"evidence_type": "invoice", "evidence_source": "Utility Co."},
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 200
    items = resp.json()["evidence_items"]
    assert len(items) == 1
    assert items[0]["evidence_id"] == str(matching.evidence_id)


@pytest.mark.asyncio
async def test_list_evidence_no_filters_returns_all_own_org_rows(client: AsyncClient, db_session):
    await _seed_evidence(db_session, ORG_A, evidence_source="First")
    await _seed_evidence(db_session, ORG_A, evidence_source="Second")

    resp = await client.get("/evidence", headers=_auth(ORG_A))
    assert resp.status_code == 200
    assert len(resp.json()["evidence_items"]) == 2


# ---------------------------------------------------------------------------
# Error semantics (TDS-015 §13)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_evidence_unauthenticated_rejected(client: AsyncClient, db_session):
    row = await _seed_evidence(db_session, ORG_A)
    resp = await client.get(f"/evidence/{row.evidence_id}")
    assert resp.status_code == 400


# ---------------------------------------------------------------------------
# Gate 2 V&V remediation (Finding C-2) — missing organization_id claim
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_evidence_missing_organization_id_claim_returns_401_not_500(
    client: AsyncClient, db_session
):
    row = await _seed_evidence(db_session, ORG_A)
    resp = await client.get(f"/evidence/{row.evidence_id}", headers=_auth_missing_organization_id())
    assert resp.status_code == 401
    assert resp.status_code != 500


@pytest.mark.asyncio
async def test_list_evidence_missing_organization_id_claim_returns_401_not_500(client: AsyncClient):
    resp = await client.get("/evidence", headers=_auth_missing_organization_id())
    assert resp.status_code == 401
    assert resp.status_code != 500


@pytest.mark.asyncio
async def test_list_evidence_malformed_linked_entity_id_returns_422(client: AsyncClient):
    resp = await client.get(
        "/evidence",
        params={"linked_entity_id": "not-a-uuid"},
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_get_evidence_malformed_path_id_returns_422(client: AsyncClient):
    resp = await client.get("/evidence/not-a-uuid", headers=_auth(ORG_A))
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Zero-write-path constraint (TDS-015 §1/§7/§19) — no establish/mutate
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_no_write_endpoint_exists_for_evidence(client: AsyncClient):
    resp = await client.post("/evidence", json={"evidence_type": "invoice"}, headers=_auth(ORG_A))
    assert resp.status_code in (404, 405)
