"""
C-022 Customer & Account Management — WP-21 BA-01 ("Establish Commercial
Account") implementation tests.

Covers the `TDS-C022 §20` test-implications list, the WP-21 charter's own
Implementation Authorization scope (§25a), and the `CLAUDE.md §21.4`
disposition for a PLATFORM-GLOBAL business object:

  * positive establish happy path + persistence + the resulting
    Authoritative Commercial Account Context / stable Account Reference
  * identity format `^ACCOUNT-\\d{6}$`, system-assigned (caller cannot
    supply/override), monotonic, unique across establishes
  * `account_name` required, non-blank -> 422 when blank
  * `status` always 'active'; not a settable request field; no transition
    endpoint exists
  * `parent_account_id` always NULL; not a settable request field
  * NO `classification` field/column anywhere (`ADR-038` Option A)
  * NO read/list endpoint exists (`ROD-C022-A` D8) — establish-only
  * authorization — non-PLATFORM_ADMIN -> 403 on establish; missing/
    malformed Authorization -> 400
  * platform-global security model — the c022_commercial_account table has
    NO organization_id column (the structural expression of D2);
    `/commercial-accounts` needs no X-Tenant-ID header
  * audit — a SUCCESS record is emitted on establish

The certified `require_platform_admin` gate and the `/roles`/`/offerings`
tenant-middleware exemption are consumed as-is and never modified.
"""

import re
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.c022_commercial_account import C022CommercialAccount

# pytest.ini sets `asyncio_mode = auto` — plain `async def test_*` runs.

_REFERENCE_RE = re.compile(r"^ACCOUNT-\d{6}$")


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _token(role_code: str | None, *, person_id: str | None = None) -> str:
    claims = {
        "person_id": person_id or str(uuid.uuid4()),
        "identity_id": str(uuid.uuid4()),
        "organization_id": None,
        "membership_id": None,
        "role_code": role_code,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }
    return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def _admin_headers(person_id: str | None = None) -> dict:
    return {"Authorization": f"Bearer {_token('PLATFORM_ADMIN', person_id=person_id)}"}


def _body(**extra) -> dict:
    body = {"account_name": "Acme Global Holdings"}
    body.update(extra)
    return body


def _establish(client: TestClient, **extra):
    return client.post("/commercial-accounts", json=_body(**extra), headers=_admin_headers())


# ---------------------------------------------------------------------------
# A. establish — happy path + persistence + Authoritative Context
# ---------------------------------------------------------------------------

async def test_establish_happy_path_persists_active(client: TestClient, db_session: AsyncSession) -> None:
    resp = _establish(client, account_name="Board Pack Holdings")
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["account_name"] == "Board Pack Holdings"
    assert body["status"] == "active"
    assert body["parent_account_id"] is None
    assert _REFERENCE_RE.match(body["account_reference"])
    assert "classification" not in body

    rows = (await db_session.execute(select(C022CommercialAccount))).scalars().all()
    assert len(rows) == 1
    row = rows[0]
    assert row.status == "active"
    assert row.parent_account_id is None
    assert str(row.id) == body["id"]


# ---------------------------------------------------------------------------
# B. account_reference — identity generation acceptance properties
# ---------------------------------------------------------------------------

async def test_account_reference_format_is_prefix_nnnnnn(client: TestClient) -> None:
    body = _establish(client).json()
    assert _REFERENCE_RE.match(body["account_reference"]), body["account_reference"]


async def test_account_reference_is_system_assigned_caller_cannot_override(client: TestClient) -> None:
    # A caller-supplied account_reference / id / status / parent_account_id
    # / classification is ignored (not part of the request schema) — the
    # system assigns them.
    resp = client.post(
        "/commercial-accounts",
        json=_body(
            account_reference="ACCOUNT-999999",
            id=str(uuid.uuid4()),
            status="retired",
            parent_account_id=str(uuid.uuid4()),
            classification="ENTERPRISE",
        ),
        headers=_admin_headers(),
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["account_reference"] != "ACCOUNT-999999"
    assert body["status"] == "active"
    assert body["parent_account_id"] is None
    assert "classification" not in body


async def test_account_reference_is_monotonic_and_unique(client: TestClient) -> None:
    refs = [_establish(client, account_name=f"Account {i}").json()["account_reference"] for i in range(5)]
    assert len(set(refs)) == 5  # unique
    suffixes = [int(r.split("-")[1]) for r in refs]
    assert suffixes == sorted(suffixes)  # monotonic
    assert suffixes == list(range(suffixes[0], suffixes[0] + 5))  # contiguous, +1 each


# ---------------------------------------------------------------------------
# C. validation
# ---------------------------------------------------------------------------

async def test_blank_account_name_is_422(client: TestClient) -> None:
    assert client.post("/commercial-accounts", json=_body(account_name="  "), headers=_admin_headers()).status_code == 422


async def test_missing_account_name_is_422(client: TestClient) -> None:
    resp = client.post("/commercial-accounts", json={}, headers=_admin_headers())
    assert resp.status_code == 422, resp.text


# ---------------------------------------------------------------------------
# D. no classification, no lifecycle transition, no read/list surface
# ---------------------------------------------------------------------------

async def test_no_classification_field_in_response_or_schema(client: TestClient) -> None:
    body = _establish(client).json()
    assert "classification" not in body
    assert set(body.keys()) == {
        "id", "account_reference", "account_name", "status",
        "parent_account_id", "created_at", "updated_at",
    }


def test_orm_model_declares_no_classification_column() -> None:
    cols = set(C022CommercialAccount.__table__.columns.keys())
    assert "classification" not in cols


async def test_no_state_transition_endpoint_exists(client: TestClient) -> None:
    aid = _establish(client).json()["id"]
    for verb_path in (
        ("post", f"/commercial-accounts/{aid}/reclassify"),
        ("post", f"/commercial-accounts/{aid}/retire"),
        ("post", f"/commercial-accounts/{aid}/reactivate"),
        ("post", f"/commercial-accounts/{aid}/transition"),
        ("patch", f"/commercial-accounts/{aid}"),
    ):
        method = getattr(client, verb_path[0])
        resp = method(verb_path[1], json={}, headers=_admin_headers())
        assert resp.status_code in (404, 405), (verb_path, resp.status_code)


async def test_no_read_or_list_endpoint_exists(client: TestClient) -> None:
    # ROD-C022-A D8 — establish-only. GET /commercial-accounts and
    # GET /commercial-accounts/{id} do not exist at all.
    aid = _establish(client).json()["id"]
    assert client.get("/commercial-accounts", headers=_admin_headers()).status_code in (404, 405)
    assert client.get(f"/commercial-accounts/{aid}", headers=_admin_headers()).status_code in (404, 405)


# ---------------------------------------------------------------------------
# E. authorization — negative controls (platform-global security model)
# ---------------------------------------------------------------------------

async def test_non_platform_admin_is_forbidden(client: TestClient) -> None:
    non_admin = {"Authorization": f"Bearer {_token('ORG_ADMIN')}"}
    assert client.post("/commercial-accounts", json=_body(), headers=non_admin).status_code == 403


async def test_no_role_claim_is_forbidden(client: TestClient) -> None:
    no_role = {"Authorization": f"Bearer {_token(None)}"}
    assert client.post("/commercial-accounts", json=_body(), headers=no_role).status_code == 403


async def test_missing_authorization_header_is_400(client: TestClient) -> None:
    assert client.post("/commercial-accounts", json=_body()).status_code == 400


async def test_malformed_authorization_header_is_400(client: TestClient) -> None:
    assert client.post(
        "/commercial-accounts", json=_body(), headers={"Authorization": "NotBearer xyz"}
    ).status_code == 400


async def test_commercial_accounts_needs_no_tenant_header(client: TestClient) -> None:
    # Platform-global: /commercial-accounts is tenant-middleware-exempt,
    # exactly like /roles/offerings. A successful call WITHOUT X-Tenant-ID
    # proves the exemption.
    resp = _establish(client)
    assert resp.status_code == 201


# ---------------------------------------------------------------------------
# F. platform-global schema assertion — NO organization_id, NO classification
# ---------------------------------------------------------------------------

async def test_c022_table_has_no_organization_id_or_classification_column(test_engine) -> None:
    def _columns(sync_conn):
        return {c["name"] for c in inspect(sync_conn).get_columns("c022_commercial_account")}

    async with test_engine.connect() as conn:
        cols = await conn.run_sync(_columns)

    assert "organization_id" not in cols
    assert not any("tenant" in c.lower() for c in cols)
    assert "classification" not in cols
    assert {"account_reference", "account_name", "status", "parent_account_id"} <= cols


def test_orm_model_declares_no_organization_id() -> None:
    cols = set(C022CommercialAccount.__table__.columns.keys())
    assert "organization_id" not in cols
    assert not any("tenant" in c.lower() for c in cols)


# ---------------------------------------------------------------------------
# G. audit
# ---------------------------------------------------------------------------

async def test_establish_emits_success_audit(client: TestClient, monkeypatch) -> None:
    captured: list[dict] = []
    import services.commercial_account_service as svc

    real = svc.record_audit

    def _spy(**kwargs):
        captured.append(kwargs)
        return real(**kwargs)

    monkeypatch.setattr(svc, "record_audit", _spy)

    person_id = str(uuid.uuid4())
    resp = client.post("/commercial-accounts", json=_body(), headers=_admin_headers(person_id=person_id))
    assert resp.status_code == 201, resp.text

    success = [c for c in captured if getattr(c.get("status"), "value", None) == "SUCCESS"]
    assert any(c["action"] == "ESTABLISH_COMMERCIAL_ACCOUNT" for c in success), captured
    est = next(c for c in success if c["action"] == "ESTABLISH_COMMERCIAL_ACCOUNT")
    assert est["actor_id"] == person_id
    assert est["metadata"]["status"] == "active"
    assert _REFERENCE_RE.match(est["metadata"]["account_reference"])


# ---------------------------------------------------------------------------
# H. purpose-built end-to-end runtime probe (CLAUDE.md §19.7b method note)
# ---------------------------------------------------------------------------

async def test_end_to_end_establish_probe(client: TestClient, db_session: AsyncSession) -> None:
    created = _establish(client, account_name="E2E Probe Account").json()
    ref, aid = created["account_reference"], created["id"]

    row = (await db_session.execute(
        select(C022CommercialAccount).where(C022CommercialAccount.id == uuid.UUID(aid))
    )).scalars().one()
    assert row.status == "active"
    assert row.account_reference == ref
    assert row.parent_account_id is None
    assert row.created_by_actor_id is not None


# ---------------------------------------------------------------------------
# I. PostgreSQL-portability guard — the allocator must never use a
#    dialect-specific search function (mirrors the WP-20 Gate 5 remediation
#    for c021_offering_definition's own identical allocator shape)
# ---------------------------------------------------------------------------

def test_max_reference_sequence_query_has_no_sqlite_only_function() -> None:
    from sqlalchemy import Integer, cast, func, select
    from sqlalchemy.dialects import postgresql, sqlite

    from repositories.c022_commercial_account_repository import (
        _REFERENCE_SUFFIX_OFFSET,
    )

    suffix = func.substr(C022CommercialAccount.account_reference, _REFERENCE_SUFFIX_OFFSET)
    query = select(func.coalesce(func.max(cast(suffix, Integer)), 0))

    compile_kwargs = {"literal_binds": True}
    pg_sql = str(query.compile(dialect=postgresql.dialect(), compile_kwargs=compile_kwargs))
    sqlite_sql = str(query.compile(dialect=sqlite.dialect(), compile_kwargs=compile_kwargs))

    for dialect_name, sql in (("postgresql", pg_sql), ("sqlite", sqlite_sql)):
        lowered = sql.lower()
        assert "instr(" not in lowered, (
            f"max_reference_sequence's suffix expression calls instr() under "
            f"the {dialect_name} dialect — PostgreSQL has no instr() builtin: {sql!r}"
        )
        assert "strpos(" not in lowered and "position(" not in lowered, (
            f"a non-portable search function was introduced under the "
            f"{dialect_name} dialect: {sql!r}"
        )

    assert pg_sql == sqlite_sql, (pg_sql, sqlite_sql)
    assert f"substr(c022_commercial_account.account_reference, {_REFERENCE_SUFFIX_OFFSET})" in pg_sql.lower()


async def test_max_reference_sequence_runtime_sql_has_no_sqlite_only_function(
    db_session: AsyncSession,
) -> None:
    from sqlalchemy import event

    from repositories.c022_commercial_account_repository import (
        C022CommercialAccountRepository,
    )

    captured: list[str] = []

    def _capture(conn, cursor, statement, parameters, context, executemany):
        captured.append(statement)

    bind = db_session.get_bind()
    sync_engine = getattr(bind, "sync_engine", bind)
    event.listen(sync_engine, "before_cursor_execute", _capture)
    try:
        repo = C022CommercialAccountRepository(db_session)
        result = await repo.max_reference_sequence()
    finally:
        event.remove(sync_engine, "before_cursor_execute", _capture)

    assert result == 0  # empty table in this fresh per-test database
    relevant = [s for s in captured if "c022_commercial_account" in s.lower()]
    assert relevant, "max_reference_sequence executed no query against c022_commercial_account"
    assert not any("instr(" in s.lower() for s in relevant), relevant
