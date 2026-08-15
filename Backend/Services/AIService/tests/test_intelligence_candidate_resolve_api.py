# tests/test_intelligence_candidate_resolve_api.py
"""
WP-14 BA-03 — Resolve Enterprise Intelligence Candidate (Convergence
Decision) API tests.

Includes the Mandatory Tenant-Isolation Test Checklist (`CLAUDE.md §21.4`):
(a) two distinct, unrelated Organizations with no shared row; (b) a caller
in one Organization cannot resolve or infer another Organization's own
candidate; (c) an unrelated tenant's own unclassified_id is probed
explicitly, not assumed safe.
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
from models.customer_metric import CustomerMetricRegistryModel
from models.search import EvidenceRegistryModel
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


async def _register_candidate(client: AsyncClient, org: str, raw_extracted_value: str = "Board fact") -> dict:
    resp = await client.post(
        "/intelligence-candidates",
        json={
            "raw_extracted_value": raw_extracted_value,
            "source_document_reference": "governance-report-fy25.pdf",
            "source_page_section": "p.12",
            "extraction_method": "MANUAL_ENTRY",
        },
        headers=_auth(org),
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


async def _resolve(client: AsyncClient, org: str, unclassified_id: str, body: dict):
    return await client.post(
        f"/intelligence-candidates/{unclassified_id}/resolve", json=body, headers=_auth(org)
    )


# ---------------------------------------------------------------------------
# Resolution — all three outcome paths, business rules, acceptance criteria
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_resolve_discarded_succeeds_with_no_cde_and_no_evidence(client: AsyncClient):
    candidate = await _register_candidate(client, ORG_A)
    resp = await _resolve(client, ORG_A, candidate["unclassified_id"], {"outcome": "DISCARDED"})
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["resolution_status"] == "DISCARDED"
    assert body["resolved_metric_id"] is None
    assert body["resolved_customer_metric_id"] is None
    assert body["evidence_id"] is None


@pytest.mark.asyncio
async def test_resolve_mapped_to_existing_succeeds(client: AsyncClient):
    candidate = await _register_candidate(client, ORG_A)
    target_metric_id = str(uuid4())
    resp = await _resolve(
        client, ORG_A, candidate["unclassified_id"], {"outcome": "MAPPED_TO_EXISTING", "metric_id": target_metric_id}
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["resolution_status"] == "MAPPED_TO_EXISTING"
    assert body["resolved_metric_id"] == target_metric_id
    assert body["evidence_id"] is not None


@pytest.mark.asyncio
async def test_resolve_mapped_to_existing_without_metric_id_is_rejected_with_422(client: AsyncClient):
    candidate = await _register_candidate(client, ORG_A)
    resp = await _resolve(client, ORG_A, candidate["unclassified_id"], {"outcome": "MAPPED_TO_EXISTING"})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_resolve_new_cde_created_succeeds_and_carries_semantic_match_attempt_record(
    client: AsyncClient, db_session
):
    """Acceptance criteria (IRA-014 §6 BA-03): 'NEW_CDE_CREATED always carries a Semantic Matching attempt record'."""
    candidate = await _register_candidate(client, ORG_A)
    resp = await _resolve(
        client,
        ORG_A,
        candidate["unclassified_id"],
        {
            "outcome": "NEW_CDE_CREATED",
            "metric_name": "Board Independence Ratio",
            "metric_code": "BOARD_INDEPENDENCE_RATIO",
            "unit_of_measure": "%",
        },
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["resolution_status"] == "NEW_CDE_CREATED"
    assert body["resolved_customer_metric_id"] is not None
    assert body["semantic_match_attempted_flag"] is True
    assert body["semantic_match_result_metric_id"] is None  # no prior CDE with this name
    assert body["evidence_id"] is not None

    query = select(CustomerMetricRegistryModel).where(
        CustomerMetricRegistryModel.customer_metric_id == UUID(body["resolved_customer_metric_id"])
    )
    row = (await db_session.execute(query)).scalar_one()
    assert row.cde_tier == "TENANT"
    assert row.convergence_count == 1
    assert row.promotion_decision is None  # promotion is never automatic (IRA-014 §6)


@pytest.mark.asyncio
async def test_resolve_new_cde_created_finds_existing_same_org_match(client: AsyncClient, db_session):
    """
    Semantic Matching placeholder: a second candidate with the identical
    metric_name, same org, is found. Gate 1 Finding 2 remediation: this is a
    same-organization Tenant-CDE duplicate, so it surfaces via
    `same_organization_duplicate_customer_metric_id` only —
    `semantic_match_result_metric_id` is contractually reserved for a
    Global `metric_registry` match and must remain `None` here (and in the
    persisted row itself).
    """
    candidate_1 = await _register_candidate(client, ORG_A, raw_extracted_value="fact 1")
    await _resolve(
        client,
        ORG_A,
        candidate_1["unclassified_id"],
        {"outcome": "NEW_CDE_CREATED", "metric_name": "Duplicate Metric", "metric_code": "DUP_METRIC_1"},
    )

    candidate_2 = await _register_candidate(client, ORG_A, raw_extracted_value="fact 2")
    resp = await _resolve(
        client,
        ORG_A,
        candidate_2["unclassified_id"],
        {"outcome": "NEW_CDE_CREATED", "metric_name": "duplicate metric", "metric_code": "DUP_METRIC_2"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["semantic_match_attempted_flag"] is True
    assert body["semantic_match_result_metric_id"] is None
    assert body["same_organization_duplicate_customer_metric_id"] is not None

    query = select(CustomerMetricRegistryModel).where(
        CustomerMetricRegistryModel.customer_metric_id == UUID(body["resolved_customer_metric_id"])
    )
    row = (await db_session.execute(query)).scalar_one()
    assert row.semantic_match_result_metric_id is None


@pytest.mark.asyncio
async def test_resolve_new_cde_created_without_metric_name_is_rejected_with_422(client: AsyncClient):
    candidate = await _register_candidate(client, ORG_A)
    resp = await _resolve(
        client, ORG_A, candidate["unclassified_id"], {"outcome": "NEW_CDE_CREATED", "metric_code": "X"}
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_resolve_with_invalid_outcome_is_rejected_with_422(client: AsyncClient):
    candidate = await _register_candidate(client, ORG_A)
    resp = await _resolve(client, ORG_A, candidate["unclassified_id"], {"outcome": "NOT_A_REAL_OUTCOME"})
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Idempotency / already-resolved
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_resolve_an_already_resolved_candidate_returns_409(client: AsyncClient):
    candidate = await _register_candidate(client, ORG_A)
    first = await _resolve(client, ORG_A, candidate["unclassified_id"], {"outcome": "DISCARDED"})
    assert first.status_code == 200

    second = await _resolve(client, ORG_A, candidate["unclassified_id"], {"outcome": "DISCARDED"})
    assert second.status_code == 409


@pytest.mark.asyncio
async def test_resolve_unknown_candidate_returns_404(client: AsyncClient):
    resp = await _resolve(client, ORG_A, str(uuid4()), {"outcome": "DISCARDED"})
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_resolve_writes_audit_record(client: AsyncClient, caplog):
    caplog.set_level(logging.INFO, logger="aiservice.audit")
    candidate = await _register_candidate(client, ORG_A)
    caplog.clear()
    resp = await _resolve(client, ORG_A, candidate["unclassified_id"], {"outcome": "DISCARDED"})
    assert resp.status_code == 200

    audit_records = [
        json.loads(record.getMessage()) for record in caplog.records if record.name == "aiservice.audit"
    ]
    assert len(audit_records) == 1
    payload = audit_records[0]
    assert payload["action"] == "RESOLVE_INTELLIGENCE_CANDIDATE"
    assert payload["resource"] == f"unclassified_intelligence:{candidate['unclassified_id']}"
    assert payload["status"] == "SUCCESS"
    assert payload["tenant_id"] == ORG_A


def _decoded_actor_id(token: str) -> str:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])["person_id"]


@pytest.mark.asyncio
async def test_resolve_not_found_writes_denied_audit_record(client: AsyncClient, caplog):
    """Post-Gate-4 remediation: the 404 not-found path must also produce an audit record (DENIED)."""
    caplog.set_level(logging.INFO, logger="aiservice.audit")
    token = _token(ORG_A)
    actor_id = _decoded_actor_id(token)
    unknown_id = str(uuid4())

    caplog.clear()
    resp = await client.post(
        f"/intelligence-candidates/{unknown_id}/resolve",
        json={"outcome": "DISCARDED"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 404

    audit_records = [
        json.loads(record.getMessage()) for record in caplog.records if record.name == "aiservice.audit"
    ]
    assert len(audit_records) == 1
    payload = audit_records[0]
    assert payload["action"] == "RESOLVE_INTELLIGENCE_CANDIDATE"
    assert payload["resource"] == f"unclassified_intelligence:{unknown_id}"
    assert payload["status"] == "DENIED"
    assert payload["actor_id"] == actor_id
    assert payload["tenant_id"] == ORG_A
    # No sensitive request payload leaked — only a short, non-identifying reason string.
    assert set(payload["metadata"].keys()) == {"reason"}


@pytest.mark.asyncio
async def test_resolve_already_resolved_writes_denied_audit_record(client: AsyncClient, caplog):
    """Post-Gate-4 remediation: the 409 already-resolved path must also produce an audit record (DENIED)."""
    token = _token(ORG_A)
    actor_id = _decoded_actor_id(token)
    candidate = await _register_candidate(client, ORG_A)
    first = await client.post(
        f"/intelligence-candidates/{candidate['unclassified_id']}/resolve",
        json={"outcome": "DISCARDED"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert first.status_code == 200

    caplog.set_level(logging.INFO, logger="aiservice.audit")
    caplog.clear()
    second = await client.post(
        f"/intelligence-candidates/{candidate['unclassified_id']}/resolve",
        json={"outcome": "DISCARDED"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert second.status_code == 409

    audit_records = [
        json.loads(record.getMessage()) for record in caplog.records if record.name == "aiservice.audit"
    ]
    assert len(audit_records) == 1
    payload = audit_records[0]
    assert payload["action"] == "RESOLVE_INTELLIGENCE_CANDIDATE"
    assert payload["resource"] == f"unclassified_intelligence:{candidate['unclassified_id']}"
    assert payload["status"] == "DENIED"
    assert payload["actor_id"] == actor_id
    assert payload["tenant_id"] == ORG_A
    assert set(payload["metadata"].keys()) == {"reason"}


@pytest.mark.asyncio
async def test_resolve_duplicate_metric_code_writes_denied_audit_record(client: AsyncClient, caplog):
    """Post-Gate-4 remediation: the 409 duplicate-metric_code path must also produce an audit record (DENIED)."""
    token = _token(ORG_A)
    actor_id = _decoded_actor_id(token)
    first_candidate = await _register_candidate(client, ORG_A, raw_extracted_value="audit-probe-1")
    first_resolve = await client.post(
        f"/intelligence-candidates/{first_candidate['unclassified_id']}/resolve",
        json={"outcome": "NEW_CDE_CREATED", "metric_name": "Audit Probe Metric", "metric_code": "AUDIT_PROBE_CODE"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert first_resolve.status_code == 200

    second_candidate = await _register_candidate(client, ORG_A, raw_extracted_value="audit-probe-2")
    caplog.set_level(logging.INFO, logger="aiservice.audit")
    caplog.clear()
    second_resolve = await client.post(
        f"/intelligence-candidates/{second_candidate['unclassified_id']}/resolve",
        json={"outcome": "NEW_CDE_CREATED", "metric_name": "Colliding Metric", "metric_code": "AUDIT_PROBE_CODE"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert second_resolve.status_code == 409

    audit_records = [
        json.loads(record.getMessage()) for record in caplog.records if record.name == "aiservice.audit"
    ]
    assert len(audit_records) == 1
    payload = audit_records[0]
    assert payload["action"] == "RESOLVE_INTELLIGENCE_CANDIDATE"
    assert payload["resource"] == f"unclassified_intelligence:{second_candidate['unclassified_id']}"
    assert payload["status"] == "DENIED"
    assert payload["actor_id"] == actor_id
    assert payload["tenant_id"] == ORG_A
    # metric_code is already disclosed to the caller in the 409 response body itself — not
    # sensitive — but no other request field (metric_description/formula_logic/etc.) is present.
    assert set(payload["metadata"].keys()) == {"reason", "metric_code"}
    assert payload["metadata"]["metric_code"] == "AUDIT_PROBE_CODE"


# ---------------------------------------------------------------------------
# Authorization
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_resolve_requires_platform_admin(client: AsyncClient):
    candidate = await _register_candidate(client, ORG_A)
    resp = await client.post(
        f"/intelligence-candidates/{candidate['unclassified_id']}/resolve",
        json={"outcome": "DISCARDED"},
        headers=_auth(ORG_A, role_code="MEMBER"),
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_resolve_requires_authentication(client: AsyncClient):
    candidate = await _register_candidate(client, ORG_A)
    resp = await client.post(
        f"/intelligence-candidates/{candidate['unclassified_id']}/resolve", json={"outcome": "DISCARDED"}
    )
    assert resp.status_code == 400


# ---------------------------------------------------------------------------
# Mandatory Tenant-Isolation Test Checklist (CLAUDE.md §21.4)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_org_a_cannot_resolve_org_bs_candidate(client: AsyncClient):
    """(b) a caller in one Organization cannot resolve another Organization's own candidate."""
    candidate_b = await _register_candidate(client, ORG_B, raw_extracted_value="org-b-fact")
    resp = await _resolve(client, ORG_A, candidate_b["unclassified_id"], {"outcome": "DISCARDED"})
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_unrelated_tenant_candidate_id_probe_never_accepted(client: AsyncClient):
    """(c) explicit probe: an unrelated tenant's own unclassified_id is never accepted as if it belonged to the caller."""
    candidate_b = await _register_candidate(client, ORG_B, raw_extracted_value="org-b-only-fact")

    cross_tenant_resp = await _resolve(client, ORG_A, candidate_b["unclassified_id"], {"outcome": "DISCARDED"})
    assert cross_tenant_resp.status_code == 404

    same_tenant_resp = await _resolve(client, ORG_B, candidate_b["unclassified_id"], {"outcome": "DISCARDED"})
    assert same_tenant_resp.status_code == 200


@pytest.mark.asyncio
async def test_new_cde_created_row_is_tenant_scoped(client: AsyncClient, db_session):
    """A NEW_CDE_CREATED row is always scoped to the resolving caller's own organization_id, never cross-tenant."""
    candidate_a = await _register_candidate(client, ORG_A, raw_extracted_value="org-a-fact")
    resp = await _resolve(
        client,
        ORG_A,
        candidate_a["unclassified_id"],
        {"outcome": "NEW_CDE_CREATED", "metric_name": "Org A Metric", "metric_code": "ORG_A_METRIC"},
    )
    assert resp.status_code == 200
    customer_metric_id = UUID(resp.json()["resolved_customer_metric_id"])

    org_a_query = select(CustomerMetricRegistryModel).where(
        CustomerMetricRegistryModel.organization_id == UUID(ORG_A),
        CustomerMetricRegistryModel.customer_metric_id == customer_metric_id,
    )
    org_b_query = select(CustomerMetricRegistryModel).where(
        CustomerMetricRegistryModel.organization_id == UUID(ORG_B),
        CustomerMetricRegistryModel.customer_metric_id == customer_metric_id,
    )
    assert (await db_session.execute(org_a_query)).scalar_one_or_none() is not None
    assert (await db_session.execute(org_b_query)).scalar_one_or_none() is None


# ---------------------------------------------------------------------------
# Gate 2 V&V remediation, Finding 1 — duplicate metric_code within the same
# Organization must return a clean 409, never an unhandled 500, and must
# leave no orphan artifact and no stuck candidate state.
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_duplicate_metric_code_same_org_returns_409_not_500(client: AsyncClient, db_session):
    """
    Gate 2 V&V Finding 1. A second, independent NEW_CDE_CREATED resolution
    reusing a metric_code already established for the same Organization
    must return 409, not an unhandled 500 — and must leave the system in a
    clean state: the second candidate returns to PENDING (retryable), no
    partial customer_metric_registry row, no orphan evidence_registry row,
    and the first (original) metric is completely unaffected.
    """
    first_candidate = await _register_candidate(client, ORG_A, raw_extracted_value="first fact")
    first_resp = await _resolve(
        client,
        ORG_A,
        first_candidate["unclassified_id"],
        {"outcome": "NEW_CDE_CREATED", "metric_name": "Original Metric", "metric_code": "SHARED_CODE"},
    )
    assert first_resp.status_code == 200, first_resp.text
    first_metric_id = UUID(first_resp.json()["resolved_customer_metric_id"])

    second_candidate = await _register_candidate(client, ORG_A, raw_extracted_value="second fact")
    second_resp = await _resolve(
        client,
        ORG_A,
        second_candidate["unclassified_id"],
        {"outcome": "NEW_CDE_CREATED", "metric_name": "Colliding Metric", "metric_code": "SHARED_CODE"},
    )

    # 1-6: contractually meaningful conflict response, never an unhandled 500.
    assert second_resp.status_code == 409, second_resp.text
    assert "SHARED_CODE" in second_resp.json()["detail"]

    # 7: the second candidate was NOT left claimed/stuck — it returns to
    # PENDING, since the whole transaction (including the atomic claim) was
    # rolled back, and is retryable with a different metric_code.
    candidate_row = (
        await db_session.execute(
            select(UnclassifiedIntelligenceRegistryModel).where(
                UnclassifiedIntelligenceRegistryModel.unclassified_id == UUID(second_candidate["unclassified_id"])
            )
        )
    ).scalar_one()
    assert candidate_row.resolution_status == "PENDING"
    assert candidate_row.resolved_customer_metric_id is None

    # 8: no partial/orphan customer_metric_registry row from the losing attempt —
    # exactly one row exists for this org+code pair (the original).
    metric_rows = (
        await db_session.execute(
            select(CustomerMetricRegistryModel).where(
                CustomerMetricRegistryModel.organization_id == UUID(ORG_A),
                CustomerMetricRegistryModel.metric_code == "SHARED_CODE",
            )
        )
    ).scalars().all()
    assert len(metric_rows) == 1
    assert metric_rows[0].customer_metric_id == first_metric_id

    # 9: no orphan evidence_registry row was created for the failed attempt —
    # exactly one linked Evidence row exists, for the original metric only.
    evidence_rows = (
        await db_session.execute(
            select(EvidenceRegistryModel).where(
                EvidenceRegistryModel.linked_entity_type == "customer_metric_registry",
                EvidenceRegistryModel.linked_entity_id == first_metric_id,
            )
        )
    ).scalars().all()
    assert len(evidence_rows) == 1

    # 10: the original metric is completely unaffected by the failed collision.
    original_row = (
        await db_session.execute(
            select(CustomerMetricRegistryModel).where(
                CustomerMetricRegistryModel.customer_metric_id == first_metric_id
            )
        )
    ).scalar_one()
    assert original_row.metric_name == "Original Metric"

    # The second candidate is retryable with a different metric_code.
    retry_resp = await _resolve(
        client,
        ORG_A,
        second_candidate["unclassified_id"],
        {"outcome": "NEW_CDE_CREATED", "metric_name": "Colliding Metric", "metric_code": "SHARED_CODE_RETRY"},
    )
    assert retry_resp.status_code == 200, retry_resp.text


@pytest.mark.asyncio
async def test_duplicate_metric_code_different_org_is_not_a_false_conflict(client: AsyncClient):
    """
    Tenant isolation counterpart to Finding 1: the same metric_code used by
    two DIFFERENT Organizations must not collide — uq_customer_metric_
    registry_org_code is scoped to (organization_id, metric_code), so this
    must succeed for both, not produce a false 409.
    """
    candidate_a = await _register_candidate(client, ORG_A, raw_extracted_value="org-a fact")
    resp_a = await _resolve(
        client,
        ORG_A,
        candidate_a["unclassified_id"],
        {"outcome": "NEW_CDE_CREATED", "metric_name": "Org A's Metric", "metric_code": "CROSS_ORG_CODE"},
    )
    assert resp_a.status_code == 200, resp_a.text

    candidate_b = await _register_candidate(client, ORG_B, raw_extracted_value="org-b fact")
    resp_b = await _resolve(
        client,
        ORG_B,
        candidate_b["unclassified_id"],
        {"outcome": "NEW_CDE_CREATED", "metric_name": "Org B's Metric", "metric_code": "CROSS_ORG_CODE"},
    )
    assert resp_b.status_code == 200, resp_b.text


# ---------------------------------------------------------------------------
# Gate 2 V&V remediation, Finding 3 — the LOCKED
# CHECK (semantic_match_score BETWEEN 0 AND 1) constraint must actually be
# enforced by the database, reject out-of-range values, accept valid
# values, and continue to accept NULL (this Business Activity's own
# current disposition for the column).
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_semantic_match_score_check_constraint_rejects_out_of_range(db_session):
    from sqlalchemy.exc import IntegrityError

    row = CustomerMetricRegistryModel(
        organization_id=UUID(ORG_A),
        metric_name="Constraint Probe Metric",
        metric_code="CONSTRAINT_PROBE_OUT_OF_RANGE",
        requested_by_user_id=uuid4(),
        semantic_match_score=1.5,
    )
    db_session.add(row)
    with pytest.raises(IntegrityError):
        await db_session.flush()
    await db_session.rollback()


@pytest.mark.asyncio
async def test_semantic_match_score_check_constraint_accepts_valid_value(db_session):
    row = CustomerMetricRegistryModel(
        organization_id=UUID(ORG_A),
        metric_name="Constraint Probe Metric Valid",
        metric_code="CONSTRAINT_PROBE_VALID",
        requested_by_user_id=uuid4(),
        semantic_match_score=0.5,
    )
    db_session.add(row)
    await db_session.flush()  # must not raise
    await db_session.rollback()


@pytest.mark.asyncio
async def test_semantic_match_score_check_constraint_accepts_null(db_session):
    row = CustomerMetricRegistryModel(
        organization_id=UUID(ORG_A),
        metric_name="Constraint Probe Metric Null",
        metric_code="CONSTRAINT_PROBE_NULL",
        requested_by_user_id=uuid4(),
        semantic_match_score=None,
    )
    db_session.add(row)
    await db_session.flush()  # must not raise — NULL passes a CHECK constraint under standard SQL semantics
    await db_session.rollback()
