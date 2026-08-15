# tests/test_knowledge_asset_api.py
"""
WP-14 BA-04 — Establish Knowledge Asset (C-091) API tests.

Includes the Mandatory Tenant-Isolation Test Checklist (`CLAUDE.md §21.4`):
(a) two distinct, unrelated Organizations with no shared row; (b) a caller
in one Organization cannot retrieve or infer another Organization's own
Knowledge Asset; (c) an unrelated tenant's own knowledge_asset_id is
probed explicitly, not assumed safe.
"""
import json
import logging
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
    client: AsyncClient, org: str, provenance_reference: str = "governance-report-fy25.pdf#p12"
) -> dict:
    resp = await client.post(
        "/knowledge-assets",
        json={
            "knowledge_asset_name": "Board Independence Ratio — FY25",
            "knowledge_asset_type": "fact",
            "provenance_reference": provenance_reference,
        },
        headers=_auth(org),
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


# ---------------------------------------------------------------------------
# Establishment — success path, business rules, acceptance criteria
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_establish_knowledge_asset_succeeds_with_provenance(client: AsyncClient):
    body = await _establish(client, ORG_A)
    assert body["curation_status"] == "PROPOSED"
    assert body["provenance_reference"] == "governance-report-fy25.pdf#p12"
    assert body["organization_id"] == ORG_A
    assert body["source_ingestion_id"] is None
    assert body["confidence_rule_id"] is None
    assert body["graph_engine_reference"] is None


@pytest.mark.asyncio
async def test_establish_knowledge_asset_without_provenance_is_rejected_with_422(client: AsyncClient):
    """Acceptance criteria (Charter §17): 'a Knowledge Asset with no Provenance is rejected (422)'."""
    resp = await client.post(
        "/knowledge-assets",
        json={"knowledge_asset_name": "No Provenance", "knowledge_asset_type": "fact"},
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_establish_knowledge_asset_with_empty_provenance_is_rejected_with_422(client: AsyncClient):
    resp = await client.post(
        "/knowledge-assets",
        json={"provenance_reference": ""},
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_establish_knowledge_asset_accepts_optional_nullable_references(client: AsyncClient):
    """
    source_ingestion_id/confidence_rule_id are accepted when explicitly
    supplied (schema allows it) even though neither target table has a
    physical model in this repository — this test does not exercise that
    combination (no real ingestion_id/confidence_rule_id exists to supply),
    it confirms omitting both (the only currently-usable case) succeeds
    cleanly, per Charter §16.
    """
    body = await _establish(client, ORG_A, provenance_reference="omitted-fk-case.pdf")
    assert body["source_ingestion_id"] is None
    assert body["confidence_rule_id"] is None


# ---------------------------------------------------------------------------
# Audit (Certification Remediation Finding 2, Gate 1, 2026-08-11)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_establish_knowledge_asset_writes_audit_record(client: AsyncClient, caplog):
    """
    A state-changing establish action must produce audit evidence, mirroring
    services/conversation_service.py::establish()'s own identical pattern
    (same observability.py mechanism, no new framework).
    """
    caplog.set_level(logging.INFO, logger="aiservice.audit")
    created = await _establish(client, ORG_A, provenance_reference="audit-check.pdf")

    audit_records = [
        json.loads(record.getMessage()) for record in caplog.records if record.name == "aiservice.audit"
    ]
    assert len(audit_records) == 1, "expected exactly one audit record for one establish call"
    payload = audit_records[0]
    assert payload["action"] == "ESTABLISH_KNOWLEDGE_ASSET"
    assert payload["resource"] == f"knowledge_asset:{created['knowledge_asset_id']}"
    assert payload["status"] == "SUCCESS"
    assert payload["tenant_id"] == ORG_A
    assert payload["actor_id"] and payload["actor_id"] != "SYSTEM"
    # No caller-supplied request content leaks into the audit record.
    assert "audit-check.pdf" not in json.dumps(payload)


# ---------------------------------------------------------------------------
# Authorization
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_establish_knowledge_asset_requires_platform_admin(client: AsyncClient):
    resp = await client.post(
        "/knowledge-assets",
        json={"provenance_reference": "x.pdf"},
        headers=_auth(ORG_A, role_code="MEMBER"),
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_establish_knowledge_asset_requires_authentication(client: AsyncClient):
    resp = await client.post(
        "/knowledge-assets",
        json={"provenance_reference": "x.pdf"},
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_get_knowledge_asset_requires_platform_admin(client: AsyncClient):
    created = await _establish(client, ORG_A)
    resp = await client.get(
        f"/knowledge-assets/{created['knowledge_asset_id']}",
        headers=_auth(ORG_A, role_code="MEMBER"),
    )
    assert resp.status_code == 403


# ---------------------------------------------------------------------------
# Persistence / retrieval correctness
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_knowledge_asset_by_id_returns_established_asset(client: AsyncClient):
    created = await _establish(client, ORG_A)
    resp = await client.get(f"/knowledge-assets/{created['knowledge_asset_id']}", headers=_auth(ORG_A))
    assert resp.status_code == 200
    assert resp.json()["knowledge_asset_id"] == created["knowledge_asset_id"]


@pytest.mark.asyncio
async def test_get_knowledge_asset_by_unknown_id_returns_404(client: AsyncClient):
    resp = await client.get(f"/knowledge-assets/{uuid4()}", headers=_auth(ORG_A))
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Mandatory Tenant-Isolation Test Checklist (CLAUDE.md §21.4)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_two_orgs_no_shared_row(client: AsyncClient):
    """(a) two distinct, unrelated Organizations, no shared row."""
    asset_a = await _establish(client, ORG_A, provenance_reference="org-a-source.pdf")
    asset_b = await _establish(client, ORG_B, provenance_reference="org-b-source.pdf")
    assert asset_a["knowledge_asset_id"] != asset_b["knowledge_asset_id"]
    assert asset_a["organization_id"] == ORG_A
    assert asset_b["organization_id"] == ORG_B


@pytest.mark.asyncio
async def test_org_a_cannot_retrieve_org_b_knowledge_asset(client: AsyncClient):
    """(b) a caller in one Organization cannot retrieve another Organization's own Knowledge Asset."""
    asset_b = await _establish(client, ORG_B)
    resp = await client.get(f"/knowledge-assets/{asset_b['knowledge_asset_id']}", headers=_auth(ORG_A))
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_unrelated_tenant_foreign_identifier_probe(client: AsyncClient):
    """(c) explicit probe: an unrelated tenant's own knowledge_asset_id is never accepted as if it belonged to the caller."""
    asset_b = await _establish(client, ORG_B, provenance_reference="org-b-only.pdf")

    cross_tenant_resp = await client.get(
        f"/knowledge-assets/{asset_b['knowledge_asset_id']}", headers=_auth(ORG_A)
    )
    assert cross_tenant_resp.status_code == 404

    same_tenant_resp = await client.get(
        f"/knowledge-assets/{asset_b['knowledge_asset_id']}", headers=_auth(ORG_B)
    )
    assert same_tenant_resp.status_code == 200
    assert same_tenant_resp.json()["provenance_reference"] == "org-b-only.pdf"
