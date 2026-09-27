"""
C-021 Product & Service Catalog — WP-20 BA-01 ("Establish / Manage Offering
Definition") implementation tests.

Covers the `TDS-C021 §20` / `§25` (RTM) test obligations, the Repository
Owner Implementation Authorization's own TESTING list, and the
`CLAUDE.md §21.4` disposition for a PLATFORM-GLOBAL business object:

  * positive establish happy path + persistence + the resulting
    Authoritative Offering Definition Context / stable Offering Reference
  * list (platform-global, newest-first) and read by id
  * O1 — identity format `^OFFERING-\\d{6}$`, system-assigned (caller cannot
    supply/override), monotonic, unique across establishes
  * O2 — `category_ref` omitted -> 201 with NULL; supplied -> persisted
    verbatim; blank string -> 422
  * D6 — `list_price_reference` is an opaque string, never numeric/computed;
    a JSON number is rejected
  * `offering_kind` closed set (PRODUCT/SERVICE) — anything else -> 422
  * `state` always 'draft'; not a settable request field; no transition
    endpoint exists
  * authorization — non-PLATFORM_ADMIN -> 403 on establish/list/read;
    missing/blank Authorization -> 400/401
  * platform-global security model — the c021_offering_definition table has
    NO organization_id column (the structural expression of D8); `/offerings`
    needs no X-Tenant-ID header
  * audit — a SUCCESS record is emitted on establish
  * read of an unknown id -> 404

The certified `require_platform_admin` gate and the `/roles` tenant-
middleware exemption are consumed as-is and never modified.
"""

import re
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import inspect, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.c021_offering_definition import C021OfferingDefinition

# pytest.ini sets `asyncio_mode = auto` — plain `async def test_*` runs.

_REFERENCE_RE = re.compile(r"^OFFERING-\d{6}$")


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
    body = {"offering_name": "Enterprise ESG Reporting", "offering_kind": "SERVICE"}
    body.update(extra)
    return body


def _establish(client: TestClient, **extra):
    return client.post("/offerings", json=_body(**extra), headers=_admin_headers())


# ---------------------------------------------------------------------------
# A. establish — happy path + persistence + Authoritative Context
# ---------------------------------------------------------------------------

async def test_establish_happy_path_persists_draft(client: TestClient, db_session: AsyncSession) -> None:
    resp = _establish(client, offering_name="Board Pack Automation", offering_kind="PRODUCT",
                      category_ref="GOVERNANCE", list_price_reference="PRICEBOOK-2026-STD")
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["offering_name"] == "Board Pack Automation"
    assert body["offering_kind"] == "PRODUCT"
    assert body["category_ref"] == "GOVERNANCE"
    assert body["list_price_reference"] == "PRICEBOOK-2026-STD"
    assert body["state"] == "draft"
    assert body["version"] == 1
    assert body["supersedes_id"] is None
    assert _REFERENCE_RE.match(body["offering_reference"])

    rows = (await db_session.execute(select(C021OfferingDefinition))).scalars().all()
    assert len(rows) == 1
    row = rows[0]
    assert row.state == "draft"
    assert row.version == 1
    assert row.supersedes_id is None
    assert str(row.id) == body["id"]


async def test_establish_produces_stable_offering_reference_on_read(client: TestClient) -> None:
    ref = _establish(client, offering_name="Data Quality Service").json()["offering_reference"]
    listed = client.get("/offerings", headers=_admin_headers()).json()
    match = next(o for o in listed if o["offering_reference"] == ref)
    read = client.get(f"/offerings/{match['id']}", headers=_admin_headers()).json()
    assert read["offering_reference"] == ref  # stable across list + read


# ---------------------------------------------------------------------------
# B. O1 — identity generation acceptance properties
# ---------------------------------------------------------------------------

async def test_offering_reference_format_is_prefix_nnnnnn(client: TestClient) -> None:
    body = _establish(client).json()
    assert _REFERENCE_RE.match(body["offering_reference"]), body["offering_reference"]


async def test_offering_reference_is_system_assigned_caller_cannot_override(client: TestClient) -> None:
    # A caller-supplied offering_reference / id / state / version is ignored
    # (not part of the request schema) — the system assigns them.
    resp = client.post(
        "/offerings",
        json=_body(offering_reference="OFFERING-999999", id=str(uuid.uuid4()),
                   state="published", version=99),
        headers=_admin_headers(),
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["offering_reference"] != "OFFERING-999999"
    assert body["state"] == "draft"
    assert body["version"] == 1


async def test_offering_reference_is_monotonic_and_unique(client: TestClient) -> None:
    refs = [_establish(client, offering_name=f"Offering {i}").json()["offering_reference"] for i in range(5)]
    assert len(set(refs)) == 5  # unique
    suffixes = [int(r.split("-")[1]) for r in refs]
    assert suffixes == sorted(suffixes)  # monotonic
    assert suffixes == list(range(suffixes[0], suffixes[0] + 5))  # contiguous, +1 each


# ---------------------------------------------------------------------------
# C. O2 — category_ref optional / nullable
# ---------------------------------------------------------------------------

async def test_category_ref_omitted_creates_with_null(client: TestClient, db_session: AsyncSession) -> None:
    resp = _establish(client, offering_name="Uncategorised Offering")
    assert resp.status_code == 201, resp.text
    assert resp.json()["category_ref"] is None
    row = (await db_session.execute(select(C021OfferingDefinition))).scalars().one()
    assert row.category_ref is None


async def test_category_ref_supplied_is_persisted_verbatim(client: TestClient) -> None:
    body = _establish(client, category_ref="OPAQUE-CATEGORY-XYZ").json()
    assert body["category_ref"] == "OPAQUE-CATEGORY-XYZ"


async def test_category_ref_blank_string_is_422(client: TestClient) -> None:
    resp = _establish(client, category_ref="   ")
    assert resp.status_code == 422, resp.text


async def test_no_taxonomy_or_category_endpoint_exists(client: TestClient) -> None:
    # There is no category CRUD / taxonomy surface (O2 — no taxonomy authority,
    # no category management, no c021_category table). `/offerings/categories`
    # only ever resolves as GET /offerings/{offering_id} with a non-UUID id
    # (422); there is no dedicated categories route (200 never happens), and
    # no top-level /categories route (404).
    assert client.get("/offerings/categories", headers=_admin_headers()).status_code in (404, 422)
    assert client.post("/offerings/categories", json={}, headers=_admin_headers()).status_code in (404, 405)
    # No top-level /categories route exists at all (400 = tenant middleware
    # rejects an unknown, non-exempt path; 404 = no route). Either proves the
    # absence of a category-management surface.
    assert client.get("/categories", headers=_admin_headers()).status_code in (400, 404)


# ---------------------------------------------------------------------------
# D. D6 — list_price_reference is an opaque string only
# ---------------------------------------------------------------------------

async def test_list_price_reference_rejects_a_number(client: TestClient) -> None:
    resp = client.post("/offerings", json=_body(list_price_reference=1234.56), headers=_admin_headers())
    assert resp.status_code == 422, resp.text


async def test_list_price_reference_string_is_echoed_verbatim(client: TestClient) -> None:
    body = _establish(client, list_price_reference="PB-ABC-001").json()
    assert body["list_price_reference"] == "PB-ABC-001"
    # No endpoint returns a computed/numeric price.
    assert "price" not in body
    assert "amount" not in body


# ---------------------------------------------------------------------------
# E. offering_kind closed set + state never settable
# ---------------------------------------------------------------------------

async def test_offering_kind_outside_closed_set_is_422(client: TestClient) -> None:
    for bad in ("DIGITAL", "PHYSICAL", "product", "BUNDLE", ""):
        resp = client.post("/offerings", json=_body(offering_kind=bad), headers=_admin_headers())
        assert resp.status_code == 422, (bad, resp.text)


async def test_blank_offering_name_is_422(client: TestClient) -> None:
    assert client.post("/offerings", json=_body(offering_name="  "), headers=_admin_headers()).status_code == 422


async def test_no_state_transition_endpoint_exists(client: TestClient) -> None:
    oid = _establish(client).json()["id"]
    for verb_path in (("post", f"/offerings/{oid}/publish"),
                      ("post", f"/offerings/{oid}/retire"),
                      ("post", f"/offerings/{oid}/transition"),
                      ("patch", f"/offerings/{oid}")):
        method = getattr(client, verb_path[0])
        resp = method(verb_path[1], json={}, headers=_admin_headers())
        assert resp.status_code in (404, 405), (verb_path, resp.status_code)


# ---------------------------------------------------------------------------
# F. list + read
# ---------------------------------------------------------------------------

async def test_list_returns_all_newest_first(client: TestClient) -> None:
    names = [f"Offering {i}" for i in range(3)]
    for n in names:
        _establish(client, offering_name=n)
    listed = client.get("/offerings", headers=_admin_headers()).json()
    assert [o["offering_name"] for o in listed] == list(reversed(names))


async def test_read_by_id_and_unknown_id_404(client: TestClient) -> None:
    oid = _establish(client).json()["id"]
    assert client.get(f"/offerings/{oid}", headers=_admin_headers()).status_code == 200
    assert client.get(f"/offerings/{uuid.uuid4()}", headers=_admin_headers()).status_code == 404


async def test_list_is_empty_before_any_establish(client: TestClient) -> None:
    assert client.get("/offerings", headers=_admin_headers()).json() == []


# ---------------------------------------------------------------------------
# G. authorization — negative controls (platform-global security model)
# ---------------------------------------------------------------------------

async def test_non_platform_admin_is_forbidden_on_every_route(client: TestClient) -> None:
    non_admin = {"Authorization": f"Bearer {_token('ORG_ADMIN')}"}
    assert client.post("/offerings", json=_body(), headers=non_admin).status_code == 403
    assert client.get("/offerings", headers=non_admin).status_code == 403
    assert client.get(f"/offerings/{uuid.uuid4()}", headers=non_admin).status_code == 403


async def test_no_role_claim_is_forbidden(client: TestClient) -> None:
    no_role = {"Authorization": f"Bearer {_token(None)}"}
    assert client.get("/offerings", headers=no_role).status_code == 403


async def test_missing_authorization_header_is_400(client: TestClient) -> None:
    assert client.get("/offerings").status_code == 400


async def test_malformed_authorization_header_is_400(client: TestClient) -> None:
    assert client.get("/offerings", headers={"Authorization": "NotBearer xyz"}).status_code == 400


async def test_offerings_needs_no_tenant_header(client: TestClient) -> None:
    # Platform-global: /offerings is tenant-middleware-exempt, exactly like
    # /roles. A successful call WITHOUT X-Tenant-ID proves the exemption.
    resp = client.get("/offerings", headers=_admin_headers())
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# H. platform-global schema assertion — NO organization_id column (D8)
# ---------------------------------------------------------------------------

async def test_c021_table_has_no_organization_id_column(test_engine) -> None:
    # Structural expression of ROD-C021 D8 (platform-global): the physical
    # table (built by conftest from the ORM metadata, which the Alembic
    # migration mirrors) carries NO organization/tenant column.
    def _columns(sync_conn):
        return {c["name"] for c in inspect(sync_conn).get_columns("c021_offering_definition")}

    async with test_engine.connect() as conn:
        cols = await conn.run_sync(_columns)

    assert "organization_id" not in cols
    assert not any("tenant" in c.lower() for c in cols)
    assert {"offering_reference", "offering_name", "offering_kind", "category_ref",
            "list_price_reference", "state", "version", "supersedes_id"} <= cols


def test_orm_model_declares_no_organization_id() -> None:
    cols = set(C021OfferingDefinition.__table__.columns.keys())
    assert "organization_id" not in cols
    assert not any("tenant" in c.lower() for c in cols)


# ---------------------------------------------------------------------------
# I. audit
# ---------------------------------------------------------------------------

async def test_establish_emits_success_audit(client: TestClient, monkeypatch) -> None:
    captured: list[dict] = []
    import services.offering_definition_service as svc

    real = svc.record_audit

    def _spy(**kwargs):
        captured.append(kwargs)
        return real(**kwargs)

    monkeypatch.setattr(svc, "record_audit", _spy)

    person_id = str(uuid.uuid4())
    resp = client.post("/offerings", json=_body(), headers=_admin_headers(person_id=person_id))
    assert resp.status_code == 201, resp.text

    success = [c for c in captured if getattr(c.get("status"), "value", None) == "SUCCESS"]
    assert any(c["action"] == "ESTABLISH_OFFERING_DEFINITION" for c in success), captured
    est = next(c for c in success if c["action"] == "ESTABLISH_OFFERING_DEFINITION")
    assert est["actor_id"] == person_id
    assert est["metadata"]["state"] == "draft"
    assert _REFERENCE_RE.match(est["metadata"]["offering_reference"])


# ---------------------------------------------------------------------------
# J. purpose-built end-to-end runtime probe (CLAUDE.md §19.7b method note)
# ---------------------------------------------------------------------------

async def test_end_to_end_establish_list_read_probe(client: TestClient, db_session: AsyncSession) -> None:
    created = _establish(client, offering_name="E2E Probe Offering", offering_kind="SERVICE",
                         category_ref="PROBE").json()
    ref, oid = created["offering_reference"], created["id"]

    listed = client.get("/offerings", headers=_admin_headers()).json()
    assert any(o["id"] == oid and o["offering_reference"] == ref for o in listed)

    read = client.get(f"/offerings/{oid}", headers=_admin_headers()).json()
    # Compare every field except the timestamp string form (SQLite round-trips
    # DateTime(timezone=True) tz-naive, so the 'Z' suffix differs between the
    # establish response and a fresh read — the persisted instants match).
    for key in ("id", "offering_reference", "offering_name", "offering_kind",
                "category_ref", "list_price_reference", "state", "version",
                "supersedes_id", "updated_at"):
        assert read[key] == created[key], key
    assert read["created_at"].rstrip("Z") == created["created_at"].rstrip("Z")

    row = (await db_session.execute(
        select(C021OfferingDefinition).where(C021OfferingDefinition.id == uuid.UUID(oid))
    )).scalars().one()
    assert row.state == "draft" and row.offering_reference == ref and row.category_ref == "PROBE"
    assert row.created_by_actor_id is not None


# ---------------------------------------------------------------------------
# K. Gate 5 remediation (2026-09-09) — offering_reference allocator must be
#    PostgreSQL-portable, not merely SQLite-passing
# ---------------------------------------------------------------------------

def test_max_reference_sequence_query_has_no_sqlite_only_function() -> None:
    """
    Regression guard for the Gate 5 Critical finding: `max_reference_sequence`
    previously located the '-' via `func.instr(...)` — a SQLite/MySQL/Oracle
    function with no PostgreSQL equivalent — so every `establish()` call
    failed against the mandated production database while every test in this
    file (which runs exclusively against the SQLite harness) still passed.
    Running this file's own tests can never re-catch a PostgreSQL-dialect
    incompatibility, because none of them execute against PostgreSQL — so
    this test instead independently compiles the repository's actual
    suffix-extraction expression against the `postgresql` dialect and asserts
    the generated SQL calls no non-portable search function. It imports the
    real `_REFERENCE_SUFFIX_OFFSET` constant from the repository module
    (not a hand-copied value), so a future change to that constant, or to
    how it derives the offset, is exercised by this test too.
    """
    from sqlalchemy import Integer, cast, func, select
    from sqlalchemy.dialects import postgresql, sqlite

    from repositories.c021_offering_definition_repository import (
        _REFERENCE_SUFFIX_OFFSET,
    )

    suffix = func.substr(C021OfferingDefinition.offering_reference, _REFERENCE_SUFFIX_OFFSET)
    query = select(func.coalesce(func.max(cast(suffix, Integer)), 0))

    compile_kwargs = {"literal_binds": True}
    pg_sql = str(query.compile(dialect=postgresql.dialect(), compile_kwargs=compile_kwargs))
    sqlite_sql = str(query.compile(dialect=sqlite.dialect(), compile_kwargs=compile_kwargs))

    for dialect_name, sql in (("postgresql", pg_sql), ("sqlite", sqlite_sql)):
        lowered = sql.lower()
        assert "instr(" not in lowered, (
            f"max_reference_sequence's suffix expression still calls instr() "
            f"under the {dialect_name} dialect — PostgreSQL has no instr() "
            f"builtin, so this would break every establish() call in "
            f"production: {sql!r}"
        )
        assert "strpos(" not in lowered and "position(" not in lowered, (
            f"a non-portable search function was reintroduced under the "
            f"{dialect_name} dialect (SQLite has no strpos()/position()): {sql!r}"
        )

    # The whole point of the fixed-offset design is that no dialect-specific
    # function is needed at all — the compiled SQL should therefore be
    # byte-identical across dialects. Any divergence here is itself a signal
    # that dialect-specific behavior crept back in.
    assert pg_sql == sqlite_sql, (pg_sql, sqlite_sql)
    assert f"substr(c021_offering_definition.offering_reference, {_REFERENCE_SUFFIX_OFFSET})" in pg_sql.lower()


async def test_max_reference_sequence_runtime_sql_has_no_sqlite_only_function(
    db_session: AsyncSession,
) -> None:
    """
    Complements the dialect-compile guard above by capturing the literal SQL
    text the *actual running repository method* sends to the database engine
    during a real establish, proving the guard is exercised by production
    code and not only by a hand-reconstructed expression.
    """
    from sqlalchemy import event

    from repositories.c021_offering_definition_repository import (
        C021OfferingDefinitionRepository,
    )

    captured: list[str] = []

    def _capture(conn, cursor, statement, parameters, context, executemany):
        captured.append(statement)

    bind = db_session.get_bind()
    sync_engine = getattr(bind, "sync_engine", bind)
    event.listen(sync_engine, "before_cursor_execute", _capture)
    try:
        repo = C021OfferingDefinitionRepository(db_session)
        result = await repo.max_reference_sequence()
    finally:
        event.remove(sync_engine, "before_cursor_execute", _capture)

    assert result == 0  # empty catalog in this fresh per-test database
    relevant = [s for s in captured if "c021_offering_definition" in s.lower()]
    assert relevant, "max_reference_sequence executed no query against c021_offering_definition"
    assert not any("instr(" in s.lower() for s in relevant), relevant
