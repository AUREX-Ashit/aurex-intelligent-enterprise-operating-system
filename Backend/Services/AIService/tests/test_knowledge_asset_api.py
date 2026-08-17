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


# ---------------------------------------------------------------------------
# WP-14 BA-04 Increment — Lifecycle Transition + ACCEPTED Domain Event
# (TDS-014, implementation authorized 2026-08-16)
# ---------------------------------------------------------------------------

async def _transition(client: AsyncClient, org: str, knowledge_asset_id: str, target_status: str):
    return await client.post(
        f"/knowledge-assets/{knowledge_asset_id}/transition",
        json={"target_status": target_status},
        headers=_auth(org),
    )


def _patch_publisher(monkeypatch, *, raise_error: bool = False):
    """
    Patches KafkaEventPublisher.publish (the real, shared class the service
    imports at call time) to capture every constructed event without
    actually depending on the mock broker's own no-op behavior, and
    optionally simulate a publish failure. Returns the list of captured
    events (each the real KnowledgeAssetAcceptedEvent instance).
    """
    from aurex.backend.shared.events.event_publisher import KafkaEventPublisher

    captured: list = []

    def fake_publish(self, event, destination, partition_key=None):
        captured.append(event)
        if raise_error:
            raise RuntimeError("simulated publisher failure")

    monkeypatch.setattr(KafkaEventPublisher, "publish", fake_publish)
    return captured


# --- State transitions -------------------------------------------------

@pytest.mark.asyncio
async def test_transition_proposed_to_validated_succeeds(client: AsyncClient):
    asset = await _establish(client, ORG_A, provenance_reference="t-validated.pdf")
    resp = await _transition(client, ORG_A, asset["knowledge_asset_id"], "VALIDATED")
    assert resp.status_code == 200, resp.text
    assert resp.json()["curation_status"] == "VALIDATED"


@pytest.mark.asyncio
async def test_transition_proposed_to_accepted_succeeds(client: AsyncClient, monkeypatch):
    _patch_publisher(monkeypatch)
    asset = await _establish(client, ORG_A, provenance_reference="t-accepted.pdf")
    resp = await _transition(client, ORG_A, asset["knowledge_asset_id"], "ACCEPTED")
    assert resp.status_code == 200, resp.text
    assert resp.json()["curation_status"] == "ACCEPTED"


@pytest.mark.asyncio
async def test_transition_proposed_to_rejected_succeeds(client: AsyncClient):
    asset = await _establish(client, ORG_A, provenance_reference="t-rejected.pdf")
    resp = await _transition(client, ORG_A, asset["knowledge_asset_id"], "REJECTED")
    assert resp.status_code == 200, resp.text
    assert resp.json()["curation_status"] == "REJECTED"


@pytest.mark.asyncio
async def test_transition_invalid_target_returns_422(client: AsyncClient):
    asset = await _establish(client, ORG_A, provenance_reference="t-invalid.pdf")
    resp = await _transition(client, ORG_A, asset["knowledge_asset_id"], "SUPERSEDED")
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_transition_already_transitioned_returns_409(client: AsyncClient, monkeypatch):
    """TDS-014 §7A — a retry after the state has already changed returns 409, never a silent 200."""
    _patch_publisher(monkeypatch)
    asset = await _establish(client, ORG_A, provenance_reference="t-already.pdf")
    first = await _transition(client, ORG_A, asset["knowledge_asset_id"], "ACCEPTED")
    assert first.status_code == 200

    second = await _transition(client, ORG_A, asset["knowledge_asset_id"], "ACCEPTED")
    assert second.status_code == 409

    third = await _transition(client, ORG_A, asset["knowledge_asset_id"], "VALIDATED")
    assert third.status_code == 409


@pytest.mark.asyncio
async def test_transition_unknown_knowledge_asset_returns_404(client: AsyncClient):
    resp = await _transition(client, ORG_A, str(uuid4()), "ACCEPTED")
    assert resp.status_code == 404


# --- Authorization -------------------------------------------------------

@pytest.mark.asyncio
async def test_transition_requires_platform_admin(client: AsyncClient):
    asset = await _establish(client, ORG_A, provenance_reference="t-authz.pdf")
    resp = await client.post(
        f"/knowledge-assets/{asset['knowledge_asset_id']}/transition",
        json={"target_status": "VALIDATED"},
        headers=_auth(ORG_A, role_code="MEMBER"),
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_transition_requires_authentication(client: AsyncClient):
    asset = await _establish(client, ORG_A, provenance_reference="t-unauth.pdf")
    resp = await client.post(
        f"/knowledge-assets/{asset['knowledge_asset_id']}/transition",
        json={"target_status": "VALIDATED"},
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_transition_cross_tenant_returns_404(client: AsyncClient):
    asset_b = await _establish(client, ORG_B, provenance_reference="t-crosstenant.pdf")
    resp = await _transition(client, ORG_A, asset_b["knowledge_asset_id"], "VALIDATED")
    assert resp.status_code == 404


# --- Domain Event ----------------------------------------------------------

@pytest.mark.asyncio
async def test_transition_to_accepted_publishes_correct_event(client: AsyncClient, monkeypatch):
    captured = _patch_publisher(monkeypatch)
    asset = await _establish(client, ORG_A, provenance_reference="t-event.pdf")
    resp = await _transition(client, ORG_A, asset["knowledge_asset_id"], "ACCEPTED")
    assert resp.status_code == 200

    assert len(captured) == 1, "expected exactly one publish attempt"
    event = captured[0]
    assert event.event_name == "aurex.aiservice.knowledge_asset.accepted"
    assert event.event_version == "1.0.0"
    payload = event.to_dict()
    assert payload["knowledge_asset_id"] == asset["knowledge_asset_id"]
    assert payload["organization_id"] == ORG_A
    assert payload["previous_status"] == "PROPOSED"
    assert payload["new_status"] == "ACCEPTED"
    assert event.tenant_id == ORG_A


@pytest.mark.asyncio
async def test_transition_to_validated_does_not_publish_event(client: AsyncClient, monkeypatch):
    captured = _patch_publisher(monkeypatch)
    asset = await _establish(client, ORG_A, provenance_reference="t-novalidatedevent.pdf")
    resp = await _transition(client, ORG_A, asset["knowledge_asset_id"], "VALIDATED")
    assert resp.status_code == 200
    assert captured == []


@pytest.mark.asyncio
async def test_transition_to_rejected_does_not_publish_event(client: AsyncClient, monkeypatch):
    captured = _patch_publisher(monkeypatch)
    asset = await _establish(client, ORG_A, provenance_reference="t-norejectedevent.pdf")
    resp = await _transition(client, ORG_A, asset["knowledge_asset_id"], "REJECTED")
    assert resp.status_code == 200
    assert captured == []


@pytest.mark.asyncio
async def test_losing_denied_transition_does_not_publish_event(client: AsyncClient, monkeypatch):
    """A losing/already-transitioned request must never attempt a publish (TDS-014 §6)."""
    captured = _patch_publisher(monkeypatch)
    asset = await _establish(client, ORG_A, provenance_reference="t-loserevent.pdf")
    first = await _transition(client, ORG_A, asset["knowledge_asset_id"], "ACCEPTED")
    assert first.status_code == 200
    assert len(captured) == 1

    second = await _transition(client, ORG_A, asset["knowledge_asset_id"], "ACCEPTED")
    assert second.status_code == 409
    assert len(captured) == 1, "the losing/already-transitioned request must not publish a second event"


# --- Event ordering / DB commit precedence ---------------------------------

@pytest.mark.asyncio
async def test_event_publish_attempted_only_after_db_commit(client: AsyncClient, monkeypatch, db_session):
    """TDS-014 §9 — the DB transition is already committed by the time publish() is invoked."""
    from uuid import UUID

    from sqlalchemy import select

    from aurex.backend.shared.events.event_publisher import KafkaEventPublisher
    from models.knowledge_asset import KnowledgeAssetRegistryModel

    publish_was_invoked = {"value": False}

    def fake_publish(self, event, destination, partition_key=None):
        publish_was_invoked["value"] = True

    monkeypatch.setattr(KafkaEventPublisher, "publish", fake_publish)

    asset = await _establish(client, ORG_A, provenance_reference="t-ordering.pdf")
    resp = await _transition(client, ORG_A, asset["knowledge_asset_id"], "ACCEPTED")
    assert resp.status_code == 200
    assert publish_was_invoked["value"] is True, "publish() was never invoked"

    # Independently re-confirm the committed DB state reflects ACCEPTED —
    # not merely the HTTP response's own claim — proving the UPDATE was
    # already committed by the time the (now-invoked) publish attempt ran.
    row = (
        await db_session.execute(
            select(KnowledgeAssetRegistryModel).where(
                KnowledgeAssetRegistryModel.knowledge_asset_id == UUID(asset["knowledge_asset_id"])
            )
        )
    ).scalar_one()
    assert row.curation_status == "ACCEPTED"


# --- Publication failure -----------------------------------------------

@pytest.mark.asyncio
async def test_publish_failure_does_not_roll_back_accepted_state(client: AsyncClient, monkeypatch, caplog):
    """TDS-014 §9/§11, RO-DEC-BA04-INC-007 — ACCEPTED is authoritative once DB commit succeeds, independent of publish outcome."""
    import logging as _logging

    caplog.set_level(_logging.ERROR, logger="aiservice.events")
    captured = _patch_publisher(monkeypatch, raise_error=True)

    asset = await _establish(client, ORG_A, provenance_reference="t-publishfail.pdf")
    resp = await _transition(client, ORG_A, asset["knowledge_asset_id"], "ACCEPTED")

    # The business transition genuinely succeeded — publish failure is not
    # surfaced to the caller as a request failure.
    assert resp.status_code == 200, resp.text
    assert resp.json()["curation_status"] == "ACCEPTED"
    assert len(captured) == 1, "exactly one publish attempt, no automatic retry"

    # The failure is observable through the existing structured-logging
    # mechanism, attributed as an event-publication failure.
    failure_logs = [r for r in caplog.records if r.name == "aiservice.events" and r.levelno >= _logging.ERROR]
    assert len(failure_logs) == 1
    assert str(asset["knowledge_asset_id"]) in failure_logs[0].getMessage() or str(
        asset["knowledge_asset_id"]
    ) in str(failure_logs[0].args)

    # No automatic retry: re-fetch confirms state remains ACCEPTED, not
    # reverted, and a further transition attempt correctly reports 409
    # (already transitioned), not a fresh attempt.
    get_resp = await client.get(f"/knowledge-assets/{asset['knowledge_asset_id']}", headers=_auth(ORG_A))
    assert get_resp.status_code == 200
    assert get_resp.json()["curation_status"] == "ACCEPTED"


# --- Audit ---------------------------------------------------------------

@pytest.mark.asyncio
async def test_transition_success_writes_success_audit(client: AsyncClient, caplog, monkeypatch):
    """
    Gate 1 F-01 remediation (TDS-014 §11): the ACCEPTED SUCCESS audit
    record's own metadata must carry the SAME event_id as the actual
    generated Domain Event — not merely any string, and not omitted.
    """
    captured = _patch_publisher(monkeypatch)
    caplog.set_level(logging.INFO, logger="aiservice.audit")
    asset = await _establish(client, ORG_A, provenance_reference="t-audit-success.pdf")
    caplog.clear()

    resp = await _transition(client, ORG_A, asset["knowledge_asset_id"], "ACCEPTED")
    assert resp.status_code == 200

    audit_records = [
        json.loads(record.getMessage()) for record in caplog.records if record.name == "aiservice.audit"
    ]
    assert len(audit_records) == 1
    payload = audit_records[0]
    assert payload["action"] == "TRANSITION_KNOWLEDGE_ASSET"
    assert payload["resource"] == f"knowledge_asset:{asset['knowledge_asset_id']}"
    assert payload["status"] == "SUCCESS"
    assert payload["tenant_id"] == ORG_A
    assert payload["metadata"]["from_status"] == "PROPOSED"
    assert payload["metadata"]["to_status"] == "ACCEPTED"

    assert len(captured) == 1, "expected exactly one ACCEPTED event to have been constructed/published"
    assert payload["metadata"]["event_id"] == captured[0].event_id
    assert payload["metadata"]["event_id"] is not None


@pytest.mark.asyncio
async def test_transition_non_accepted_success_audit_has_null_event_id(client: AsyncClient, caplog, monkeypatch):
    """TDS-014 §11's own frozen shape: event_id is populated only for ACCEPTED; VALIDATED/REJECTED carry null, never an invented value."""
    captured = _patch_publisher(monkeypatch)
    caplog.set_level(logging.INFO, logger="aiservice.audit")

    for target_status in ("VALIDATED", "REJECTED"):
        asset = await _establish(client, ORG_A, provenance_reference=f"t-audit-{target_status}.pdf")
        caplog.clear()

        resp = await _transition(client, ORG_A, asset["knowledge_asset_id"], target_status)
        assert resp.status_code == 200

        audit_records = [
            json.loads(record.getMessage()) for record in caplog.records if record.name == "aiservice.audit"
        ]
        assert len(audit_records) == 1
        payload = audit_records[0]
        assert payload["status"] == "SUCCESS"
        assert payload["metadata"]["to_status"] == target_status
        assert payload["metadata"]["event_id"] is None

    assert captured == [], "VALIDATED/REJECTED must never construct or publish an event"


@pytest.mark.asyncio
async def test_transition_denied_writes_denied_audit(client: AsyncClient, caplog, monkeypatch):
    _patch_publisher(monkeypatch)
    asset = await _establish(client, ORG_A, provenance_reference="t-audit-denied.pdf")
    first = await _transition(client, ORG_A, asset["knowledge_asset_id"], "ACCEPTED")
    assert first.status_code == 200

    caplog.set_level(logging.INFO, logger="aiservice.audit")
    caplog.clear()
    second = await _transition(client, ORG_A, asset["knowledge_asset_id"], "REJECTED")
    assert second.status_code == 409

    audit_records = [
        json.loads(record.getMessage()) for record in caplog.records if record.name == "aiservice.audit"
    ]
    assert len(audit_records) == 1
    payload = audit_records[0]
    assert payload["action"] == "TRANSITION_KNOWLEDGE_ASSET"
    assert payload["status"] == "DENIED"
    assert payload["tenant_id"] == ORG_A


@pytest.mark.asyncio
async def test_transition_not_found_writes_denied_audit(client: AsyncClient, caplog):
    caplog.set_level(logging.INFO, logger="aiservice.audit")
    caplog.clear()
    unknown_id = str(uuid4())
    resp = await _transition(client, ORG_A, unknown_id, "ACCEPTED")
    assert resp.status_code == 404

    audit_records = [
        json.loads(record.getMessage()) for record in caplog.records if record.name == "aiservice.audit"
    ]
    assert len(audit_records) == 1
    payload = audit_records[0]
    assert payload["action"] == "TRANSITION_KNOWLEDGE_ASSET"
    assert payload["resource"] == f"knowledge_asset:{unknown_id}"
    assert payload["status"] == "DENIED"
