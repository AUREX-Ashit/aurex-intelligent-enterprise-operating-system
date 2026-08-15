# tests/test_intelligence_candidate_api.py
"""
WP-14 BA-02 — Register Enterprise Intelligence Candidate (C-090) API tests.

Includes the Mandatory Tenant-Isolation Test Checklist (`CLAUDE.md §21.4`):
(a) two distinct, unrelated Organizations with no shared row; (b) a caller
in one Organization cannot retrieve or infer another Organization's own
candidate; (c) an unrelated tenant's own unclassified_id is probed
explicitly, not assumed safe.

No GET/list endpoint exists for this Business Activity (IRA-014 §6 names
only POST) — tenant isolation for (b)/(c) is therefore verified via a
direct repository-level query (the only way to observe persisted rows,
since no API surface exposes them), not via a cross-tenant API read.
"""
import json
import logging
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient
from jose import jwt
from sqlalchemy import select

from config.settings import settings
from models.unclassified_intelligence import UnclassifiedIntelligenceRegistryModel

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


async def _register(
    client: AsyncClient,
    org: str,
    raw_extracted_value: str = "Board independence ratio: 62%",
    source_document_reference: str = "governance-report-fy25.pdf",
    extraction_method: str = "MANUAL_ENTRY",
) -> dict:
    resp = await client.post(
        "/intelligence-candidates",
        json={
            "raw_extracted_value": raw_extracted_value,
            "source_document_reference": source_document_reference,
            "source_page_section": "p.12",
            "extraction_method": extraction_method,
        },
        headers=_auth(org),
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


# ---------------------------------------------------------------------------
# Registration — success path, business rules, acceptance criteria
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_register_candidate_succeeds_with_manual_entry(client: AsyncClient):
    body = await _register(client, ORG_A)
    assert body["resolution_status"] == "PENDING"
    assert body["organization_id"] == ORG_A
    assert body["extraction_method"] == "MANUAL_ENTRY"
    assert body["llm_label_suggestion"] is None
    assert body["llm_confidence_score"] is None
    assert body["convergence_signal_raised_flag"] is False


@pytest.mark.asyncio
async def test_register_candidate_succeeds_with_api_ingest(client: AsyncClient):
    body = await _register(client, ORG_A, extraction_method="API_INGEST")
    assert body["extraction_method"] == "API_INGEST"


@pytest.mark.asyncio
async def test_register_candidate_without_source_page_section_succeeds(client: AsyncClient):
    """source_page_section is optional per the LOCKED schema (no NOT NULL) — diverges from IRA-014's own descriptive text, disclosed in schemas/unclassified_intelligence.py."""
    resp = await client.post(
        "/intelligence-candidates",
        json={
            "raw_extracted_value": "Some fact",
            "source_document_reference": "some-doc.pdf",
            "extraction_method": "MANUAL_ENTRY",
        },
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["source_page_section"] is None


@pytest.mark.parametrize(
    "excluded_method", ["OCR", "NLP_PARSE", "TABLE_EXTRACT", "ENTITY_EXTRACT", "SEMANTIC_PARSE"]
)
@pytest.mark.asyncio
async def test_register_candidate_with_automated_extraction_method_is_rejected_with_422(
    client: AsyncClient, excluded_method: str
):
    """Acceptance criteria (IRA-014 §6 BA-02): 'an automated extraction_method value is rejected (422) with a clear reason'."""
    resp = await client.post(
        "/intelligence-candidates",
        json={
            "raw_extracted_value": "Some fact",
            "source_document_reference": "some-doc.pdf",
            "extraction_method": excluded_method,
        },
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_register_candidate_with_invalid_extraction_method_is_rejected_with_422(client: AsyncClient):
    resp = await client.post(
        "/intelligence-candidates",
        json={
            "raw_extracted_value": "Some fact",
            "source_document_reference": "some-doc.pdf",
            "extraction_method": "NOT_A_REAL_METHOD",
        },
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_register_candidate_without_raw_extracted_value_is_rejected_with_422(client: AsyncClient):
    resp = await client.post(
        "/intelligence-candidates",
        json={"source_document_reference": "some-doc.pdf", "extraction_method": "MANUAL_ENTRY"},
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_register_candidate_without_source_document_reference_is_rejected_with_422(client: AsyncClient):
    resp = await client.post(
        "/intelligence-candidates",
        json={"raw_extracted_value": "Some fact", "extraction_method": "MANUAL_ENTRY"},
        headers=_auth(ORG_A),
    )
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_register_candidate_writes_audit_record(client: AsyncClient, caplog):
    caplog.set_level(logging.INFO, logger="aiservice.audit")
    created = await _register(client, ORG_A, raw_extracted_value="audit-check-fact")

    audit_records = [
        json.loads(record.getMessage()) for record in caplog.records if record.name == "aiservice.audit"
    ]
    assert len(audit_records) == 1
    payload = audit_records[0]
    assert payload["action"] == "REGISTER_INTELLIGENCE_CANDIDATE"
    assert payload["resource"] == f"unclassified_intelligence:{created['unclassified_id']}"
    assert payload["status"] == "SUCCESS"
    assert payload["tenant_id"] == ORG_A
    assert payload["actor_id"] and payload["actor_id"] != "SYSTEM"


# ---------------------------------------------------------------------------
# Authorization
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_register_candidate_requires_platform_admin(client: AsyncClient):
    resp = await client.post(
        "/intelligence-candidates",
        json={
            "raw_extracted_value": "x",
            "source_document_reference": "x.pdf",
            "extraction_method": "MANUAL_ENTRY",
        },
        headers=_auth(ORG_A, role_code="MEMBER"),
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_register_candidate_requires_authentication(client: AsyncClient):
    resp = await client.post(
        "/intelligence-candidates",
        json={
            "raw_extracted_value": "x",
            "source_document_reference": "x.pdf",
            "extraction_method": "MANUAL_ENTRY",
        },
    )
    assert resp.status_code == 400


# ---------------------------------------------------------------------------
# Mandatory Tenant-Isolation Test Checklist (CLAUDE.md §21.4)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_two_orgs_no_shared_row(client: AsyncClient, db_session):
    """(a) two distinct, unrelated Organizations, no shared row."""
    candidate_a = await _register(client, ORG_A, raw_extracted_value="org-a-fact")
    candidate_b = await _register(client, ORG_B, raw_extracted_value="org-b-fact")
    assert candidate_a["unclassified_id"] != candidate_b["unclassified_id"]
    assert candidate_a["organization_id"] == ORG_A
    assert candidate_b["organization_id"] == ORG_B


@pytest.mark.asyncio
async def test_org_b_row_not_visible_under_org_a_scope(client: AsyncClient, db_session):
    """(b)/(c) — no GET/list endpoint exists for this Business Activity (deliberately out of scope, see module docstring), so cross-tenant isolation is verified directly at the repository/query level: an Org B row, queried scoped to Org A's own organization_id, is never returned."""
    candidate_b = await _register(client, ORG_B, raw_extracted_value="org-b-only-fact")

    candidate_id = UUID(candidate_b["unclassified_id"])
    query = select(UnclassifiedIntelligenceRegistryModel).where(
        UnclassifiedIntelligenceRegistryModel.organization_id == UUID(ORG_A),
        UnclassifiedIntelligenceRegistryModel.unclassified_id == candidate_id,
    )
    result = await db_session.execute(query)
    assert result.scalar_one_or_none() is None

    same_tenant_query = select(UnclassifiedIntelligenceRegistryModel).where(
        UnclassifiedIntelligenceRegistryModel.organization_id == UUID(ORG_B),
        UnclassifiedIntelligenceRegistryModel.unclassified_id == candidate_id,
    )
    same_tenant_result = await db_session.execute(same_tenant_query)
    assert same_tenant_result.scalar_one_or_none() is not None
