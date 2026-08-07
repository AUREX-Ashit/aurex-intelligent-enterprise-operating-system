# tests/_vv_probe_wp12.py
"""
VV-AUDIT-WP-12 — from-scratch runtime probes (Gate 2, CLAUDE.md §19.7b).

NOT collected by pytest (filename does not match `test_*.py`), NOT part of
the shipped/certified suite. Retained in the repository as a reproducibility
artifact for this Gate's own findings, mirroring
`Backend/Services/AIService/tests/_vv_probe_wp11.py`'s own precedent.

None of these probes are adapted from `tests/test_conversation.py` — each
builds its own fresh database (in-memory or temp-file, as the defect class
requires) and its own `httpx.AsyncClient` + `ASGITransport`, independently
constructed, not imported from `conftest.py`.

Run:
    cd Backend/Services/AIService
    PYTHONCASEOK=1 python tests/_vv_probe_wp12.py
(`PYTHONCASEOK=1` works around this Windows Python install's case-sensitive
import matching against the repository's own `Config/` directory casing —
an unrelated, pre-existing environment quirk, not a WP-12 defect; the same
workaround `VV-AUDIT-WP-11`'s own header comment already documents.)
"""
from __future__ import annotations

import ast
import asyncio
import io
import logging
import os
import re
import sys
import tempfile
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

AISERVICE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AISERVICE_ROOT))  # allows running this file directly regardless of cwd

from httpx import ASGITransport, AsyncClient  # noqa: E402
from jose import jwt  # noqa: E402
from sqlalchemy import text  # noqa: E402
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine  # noqa: E402

from config.settings import settings  # noqa: E402
from main import app  # noqa: E402
from models.conversation import ConversationModel, InteractionModel  # noqa: E402
from models.database import Base, get_db  # noqa: E402
from repositories.conversation_repository import ConversationRepository, InteractionRepository  # noqa: E402

_RESULTS: list[tuple[str, bool, str]] = []


def record(name: str, passed: bool, detail: str) -> None:
    _RESULTS.append((name, passed, detail))
    tag = "PASS" if passed else "FAIL"
    print(f"[{tag}] {name}: {detail}")


def _token(*, organization_id: str, role_code: str, person_id: str | None = None) -> str:
    claims = {
        "person_id": person_id or str(uuid.uuid4()),
        "identity_id": str(uuid.uuid4()),
        "organization_id": organization_id,
        "membership_id": str(uuid.uuid4()),
        "role_code": role_code,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=60),
    }
    return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def _auth(*, organization_id: str, role_code: str = "PLATFORM_ADMIN") -> dict:
    return {"Authorization": f"Bearer {_token(organization_id=organization_id, role_code=role_code)}"}


# ---------------------------------------------------------------------------
# Harness builders — each probe constructs its own engine/session/app-client,
# independent of tests/conftest.py.
# ---------------------------------------------------------------------------

def make_memory_engine():
    """Mirrors the shipped harness's own engine configuration EXACTLY
    (sqlite+aiosqlite:///:memory:, no PRAGMA foreign_keys listener) — used
    by Probe 3a to independently re-confirm the harness/production-parity
    gap CLAUDE.md §19.7b names explicitly."""
    return create_async_engine("sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False})


def make_fk_enforced_file_engine(db_path: str):
    """A from-scratch engine on a temp SQLite FILE, with FK enforcement
    turned on via a connect-event listener — used by Probe 3b to confirm
    the FK declarations themselves are sound under real enforcement."""
    from sqlalchemy import event

    engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}", connect_args={"check_same_thread": False})

    @event.listens_for(engine.sync_engine, "connect")
    def _enable_fk(dbapi_connection, connection_record):  # noqa: ANN001
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine


def make_plain_file_engine(db_path: str):
    """A from-scratch engine on a temp SQLite FILE, no FK pragma — used for
    the concurrency probe (Probe 2) so that two independently constructed
    AsyncSession objects genuinely share one physical database, the way two
    concurrent production requests each obtaining their own pooled
    connection would (a `:memory:` DB would not share state across
    independently created connections without a StaticPool, which the
    shipped harness itself does not use either)."""
    return create_async_engine(f"sqlite+aiosqlite:///{db_path}", connect_args={"check_same_thread": False})


async def app_client_for_engine(engine):
    """Builds a fresh AsyncClient bound to the REAL `app` (real routers, real
    middleware stack, real exception handling — i.e., none) with `get_db`
    overridden to hand out a brand-new AsyncSession per call, exactly like
    production's own `models/database.py::get_db` — NOT a single
    session-per-test the way `conftest.py`'s own `client` fixture does."""
    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with session_factory() as session:
            try:
                yield session
            finally:
                await session.close()

    app.dependency_overrides[get_db] = override_get_db
    client = AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False),
        base_url="http://vv-probe-wp12",
    )
    return client


async def reset_overrides():
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Probe 1 — Cross-tenant adversarial probe, independently re-derived
# (all four endpoints, fresh organization IDs, never read from test_conversation.py)
# ---------------------------------------------------------------------------

async def probe_1_cross_tenant():
    print("\n=== Probe 1: Cross-tenant isolation across all four endpoints (fresh probe) ===")
    engine = make_memory_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    client = await app_client_for_engine(engine)
    try:
        ORG_ALPHA = str(uuid.uuid4())
        ORG_BETA = str(uuid.uuid4())

        # ORG_ALPHA establishes a Conversation and executes one Interaction.
        est = await client.post("/conversations", headers=_auth(organization_id=ORG_ALPHA))
        assert est.status_code == 201, f"setup failed: {est.status_code} {est.text}"
        conv_id = est.json()["conversation_id"]

        turn = await client.post(
            f"/conversations/{conv_id}/interactions",
            headers=_auth(organization_id=ORG_ALPHA),
            json={"input_text": "ORG_ALPHA_CONFIDENTIAL_STRATEGY_STRING_74123"},
        )
        assert turn.status_code == 201, f"setup failed: {turn.status_code} {turn.text}"

        # ORG_BETA attempts each of the four endpoints against ORG_ALPHA's own conversation_id.
        close_attempt = await client.post(
            f"/conversations/{conv_id}/close", headers=_auth(organization_id=ORG_BETA)
        )
        exec_attempt = await client.post(
            f"/conversations/{conv_id}/interactions",
            headers=_auth(organization_id=ORG_BETA),
            json={"input_text": "cross-tenant probe"},
        )
        get_attempt = await client.get(
            f"/conversations/{conv_id}/interactions", headers=_auth(organization_id=ORG_BETA, role_code="MEMBER")
        )

        leak_in_get_body = "ORG_ALPHA_CONFIDENTIAL_STRATEGY_STRING_74123" in get_attempt.text

        ok = (
            close_attempt.status_code == 404
            and exec_attempt.status_code == 404
            and get_attempt.status_code == 404
            and not leak_in_get_body
        )
        record(
            "Probe 1 — cross-tenant close/{id}/interactions POST/{id}/interactions GET",
            ok,
            f"close={close_attempt.status_code}, execute={exec_attempt.status_code}, "
            f"list={get_attempt.status_code}, content_leak={leak_in_get_body}",
        )

        # POST /conversations (establish) carries no caller-supplied conversation_id at all —
        # confirm ORG_BETA's own establish call cannot enumerate/return ORG_ALPHA's data either.
        beta_est = await client.post("/conversations", headers=_auth(organization_id=ORG_BETA))
        beta_leak = "ORG_ALPHA_CONFIDENTIAL_STRATEGY_STRING_74123" in beta_est.text
        record(
            "Probe 1b — establish (ORG_BETA) does not leak ORG_ALPHA content",
            beta_est.status_code == 201 and not beta_leak,
            f"status={beta_est.status_code}, content_leak={beta_leak}",
        )
    finally:
        await client.aclose()
        await reset_overrides()
        await engine.dispose()


# ---------------------------------------------------------------------------
# Probe 2 — Concurrency race on UNIQUE(conversation_id, sequence_number)
# ---------------------------------------------------------------------------

async def probe_2a_deterministic_race():
    """Deterministic reproduction: two independently constructed AsyncSession
    objects against the SAME physical (file-based) database, manually
    interleaved to force the exact check-then-insert race window in
    `InteractionRepository.next_sequence_number()` / `.create_pending()` —
    not left to scheduler luck."""
    print("\n=== Probe 2a: Deterministic check-then-insert race (manual interleave) ===")
    fd, path = tempfile.mkstemp(suffix=".sqlite3")
    os.close(fd)
    engine = make_plain_file_engine(path)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
        org_id = uuid.uuid4()

        async with session_factory() as setup_session:
            conv_repo = ConversationRepository(setup_session)
            conv = await conv_repo.create(organization_id=org_id, established_by=uuid.uuid4())
            conv_id = conv.conversation_id

        session_a = session_factory()
        session_b = session_factory()
        try:
            repo_a = InteractionRepository(session_a)
            repo_b = InteractionRepository(session_b)

            # Both read the same "next" sequence number before either commits —
            # the exact race window: no row-level lock, no SELECT ... FOR UPDATE,
            # no application-level mutex.
            seq_a = await repo_a.next_sequence_number(conv_id)
            seq_b = await repo_b.next_sequence_number(conv_id)
            assert seq_a == seq_b == 1, f"expected both to compute 1, got {seq_a}/{seq_b}"

            # First writer commits cleanly.
            await repo_a.create_pending(
                conversation_id=conv_id,
                organization_id=org_id,
                business_activity_id=uuid.uuid4(),
                sequence_number=seq_a,
                input_reference="writer A",
            )

            # Second writer attempts the identical (conversation_id, sequence_number).
            raised: Exception | None = None
            try:
                await repo_b.create_pending(
                    conversation_id=conv_id,
                    organization_id=org_id,
                    business_activity_id=uuid.uuid4(),
                    sequence_number=seq_b,
                    input_reference="writer B",
                )
            except Exception as exc:  # noqa: BLE001 — capturing whatever the driver actually raises
                raised = exc

            exception_type = type(raised).__name__ if raised else None
            record(
                "Probe 2a — UNIQUE(conversation_id, sequence_number) race, repository layer",
                raised is not None,
                f"writer B raised: {exception_type}: {raised}" if raised else "writer B committed silently — UNIQUE constraint did not fire (unexpected)",
            )

            # Now check: is InteractionService.execute()'s own call site to
            # create_pending() wrapped in a try/except anywhere between it and
            # the router? Confirmed by direct AST inspection of the source
            # file, not by re-reading it informally.
            source = (AISERVICE_ROOT / "services" / "interaction_service.py").read_text(encoding="utf-8")
            tree = ast.parse(source)
            create_pending_call_is_guarded = _is_call_wrapped_in_try_except(tree, "create_pending")
            record(
                "Probe 2a — is the create_pending() call site wrapped in try/except in interaction_service.py?",
                create_pending_call_is_guarded is False,
                "NOT wrapped — an IntegrityError raised here propagates uncaught through InteractionService.execute()"
                if not create_pending_call_is_guarded
                else "Wrapped — would be handled",
            )
        finally:
            await session_a.close()
            await session_b.close()
    finally:
        await engine.dispose()
        try:
            os.remove(path)
        except OSError:
            pass


def _is_call_wrapped_in_try_except(tree: ast.AST, call_name: str) -> bool:
    """Walks the AST: for every `Try` node, checks whether any call to
    `call_name` (e.g. `create_pending`) occurs textually inside its `body`
    (not its handlers). Returns True if at least one such call is inside a
    Try.body; False if every call to `call_name` anywhere in the module is
    outside any Try.body."""
    try_bodies: list[list[ast.stmt]] = [node.body for node in ast.walk(tree) if isinstance(node, ast.Try)]

    def _contains_call(stmts: list[ast.stmt]) -> bool:
        for stmt in stmts:
            for node in ast.walk(stmt):
                if isinstance(node, ast.Call):
                    func = node.func
                    name = getattr(func, "attr", None) or getattr(func, "id", None)
                    if name == call_name:
                        return True
        return False

    return any(_contains_call(body) for body in try_bodies)


async def probe_2b_http_layer_realistic_attempt():
    """Best-effort, real end-to-end HTTP attempt via `asyncio.gather` against
    the actual ASGI app (real middleware, real routers, real — i.e. absent —
    exception handling), using `raise_app_exceptions=False` so the response
    the test client receives is exactly what a real HTTP client (including
    the shipped frontend) would receive. Reports whatever actually happens;
    does not assume the race reproduces on every run (SQLite's own
    coarse-grained locking may serialize writes into `OperationalError`
    instead of `IntegrityError` — both are equally unhandled, so both are
    reported as evidence of the same defect class if seen)."""
    print("\n=== Probe 2b: Best-effort concurrent HTTP requests via asyncio.gather ===")
    fd, path = tempfile.mkstemp(suffix=".sqlite3")
    os.close(fd)
    engine = make_plain_file_engine(path)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        client = await app_client_for_engine(engine)
        try:
            org_id = str(uuid.uuid4())
            est = await client.post("/conversations", headers=_auth(organization_id=org_id))
            assert est.status_code == 201
            conv_id = est.json()["conversation_id"]

            async def fire(n: int):
                return await client.post(
                    f"/conversations/{conv_id}/interactions",
                    headers=_auth(organization_id=org_id),
                    json={"input_text": f"concurrent turn {n}"},
                )

            responses = await asyncio.gather(*(fire(i) for i in range(8)), return_exceptions=True)
            statuses = []
            for r in responses:
                if isinstance(r, Exception):
                    statuses.append(f"EXC:{type(r).__name__}")
                else:
                    statuses.append(r.status_code)

            unhandled_500s = sum(1 for s in statuses if s == 500)
            clean_success = sum(1 for s in statuses if s == 201)
            other = [s for s in statuses if s not in (500, 201)]

            record(
                "Probe 2b — 8 concurrent POST /interactions against one Conversation (best-effort, HTTP layer)",
                True,  # informative — pass/fail judgment made in the written report, not this boolean
                f"statuses={statuses} (201={clean_success}, 500={unhandled_500s}, other={other})",
            )

            # If any 500 occurred, capture the response body to confirm it is a
            # bare, undiagnosed 500 (no structured error), matching Probe 2a's
            # own repository-layer finding.
            for r in responses:
                if not isinstance(r, Exception) and r.status_code == 500:
                    record(
                        "Probe 2b — sample raw 500 response body",
                        True,
                        repr(r.text[:300]),
                    )
                    break
        finally:
            await client.aclose()
            await reset_overrides()
    finally:
        await engine.dispose()
        try:
            os.remove(path)
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Probe 3 — Harness/fixture production-parity: FK enforcement
# ---------------------------------------------------------------------------

async def probe_3a_harness_fk_not_enforced():
    print("\n=== Probe 3a: Harness FK enforcement (mirrors shipped conftest.py exactly) ===")
    engine = make_memory_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        repo = InteractionRepository(session)
        bogus_conversation_id = uuid.uuid4()  # never created — no such conversation_registry row exists
        raised = None
        try:
            await repo.create_pending(
                conversation_id=bogus_conversation_id,
                organization_id=uuid.uuid4(),
                business_activity_id=uuid.uuid4(),
                sequence_number=1,
                input_reference="orphan interaction, FK should reject this in production",
            )
        except Exception as exc:  # noqa: BLE001
            raised = exc

        record(
            "Probe 3a — harness (no PRAGMA foreign_keys) accepts an orphaned interaction_registry.conversation_id FK",
            raised is None,
            "Insert SUCCEEDED with no FK error (harness does not enforce FK — matches TD-096-class gap)"
            if raised is None
            else f"Insert failed: {type(raised).__name__}: {raised}",
        )
    await engine.dispose()


async def probe_3b_fk_enforced_with_pragma():
    print("\n=== Probe 3b: FK enforcement WITH PRAGMA foreign_keys=ON (confirms the FK declaration itself is sound) ===")
    fd, path = tempfile.mkstemp(suffix=".sqlite3")
    os.close(fd)
    engine = make_fk_enforced_file_engine(path)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
        async with session_factory() as session:
            repo = InteractionRepository(session)
            bogus_conversation_id = uuid.uuid4()
            raised = None
            try:
                await repo.create_pending(
                    conversation_id=bogus_conversation_id,
                    organization_id=uuid.uuid4(),
                    business_activity_id=uuid.uuid4(),
                    sequence_number=1,
                    input_reference="orphan interaction",
                )
            except Exception as exc:  # noqa: BLE001
                raised = exc

            record(
                "Probe 3b — with real FK enforcement, the identical insert correctly fails",
                raised is not None,
                f"{type(raised).__name__}: {raised}" if raised else "Insert unexpectedly succeeded even with FK enforcement ON",
            )
    finally:
        await engine.dispose()
        try:
            os.remove(path)
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Probe 4 — PLATFORM_ADMIN asymmetric gate (write-gated, read-open)
# ---------------------------------------------------------------------------

async def probe_4_platform_admin_gate():
    print("\n=== Probe 4: PLATFORM_ADMIN gate — asymmetric per TDS-012 §8 ===")
    engine = make_memory_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    client = await app_client_for_engine(engine)
    try:
        org_id = str(uuid.uuid4())

        # Establish as PLATFORM_ADMIN (baseline, needed to have something to close/execute/list against).
        est = await client.post("/conversations", headers=_auth(organization_id=org_id, role_code="PLATFORM_ADMIN"))
        assert est.status_code == 201
        conv_id = est.json()["conversation_id"]

        # --- Negative probes: non-PLATFORM_ADMIN caller on the three write-path endpoints ---
        establish_denied = await client.post("/conversations", headers=_auth(organization_id=org_id, role_code="MEMBER"))
        close_denied = await client.post(f"/conversations/{conv_id}/close", headers=_auth(organization_id=org_id, role_code="MEMBER"))
        execute_denied = await client.post(
            f"/conversations/{conv_id}/interactions",
            headers=_auth(organization_id=org_id, role_code="MEMBER"),
            json={"input_text": "should be rejected"},
        )
        record(
            "Probe 4 — negative: MEMBER role rejected (403) on establish/close/execute",
            establish_denied.status_code == 403 and close_denied.status_code == 403 and execute_denied.status_code == 403,
            f"establish={establish_denied.status_code}, close={close_denied.status_code}, execute={execute_denied.status_code}",
        )

        # Also probe an entirely unrecognized/absent role_code and an empty-string role.
        garbage_role_denied = await client.post(
            f"/conversations/{conv_id}/close", headers=_auth(organization_id=org_id, role_code="NOT_A_REAL_ROLE")
        )
        record(
            "Probe 4 — negative: nonsense role_code also rejected (403), not merely non-PLATFORM_ADMIN allow-listed roles",
            garbage_role_denied.status_code == 403,
            f"status={garbage_role_denied.status_code}",
        )

        # --- Positive probe: PLATFORM_ADMIN succeeds on all three write endpoints ---
        execute_allowed = await client.post(
            f"/conversations/{conv_id}/interactions",
            headers=_auth(organization_id=org_id, role_code="PLATFORM_ADMIN"),
            json={"input_text": "should succeed"},
        )
        record(
            "Probe 4 — positive: PLATFORM_ADMIN succeeds on execute",
            execute_allowed.status_code == 201,
            f"status={execute_allowed.status_code}",
        )

        # --- Read path: GET /{id}/interactions is NOT gated — any authenticated caller succeeds ---
        member_read = await client.get(f"/conversations/{conv_id}/interactions", headers=_auth(organization_id=org_id, role_code="MEMBER"))
        admin_read = await client.get(f"/conversations/{conv_id}/interactions", headers=_auth(organization_id=org_id, role_code="PLATFORM_ADMIN"))
        garbage_role_read = await client.get(
            f"/conversations/{conv_id}/interactions", headers=_auth(organization_id=org_id, role_code="NOT_A_REAL_ROLE")
        )
        record(
            "Probe 4 — read path GET /{id}/interactions is asymmetrically OPEN to any authenticated role (per TDS-012 §8)",
            member_read.status_code == 200 and admin_read.status_code == 200 and garbage_role_read.status_code == 200,
            f"MEMBER={member_read.status_code}, PLATFORM_ADMIN={admin_read.status_code}, NOT_A_REAL_ROLE={garbage_role_read.status_code}",
        )

        # --- Unauthenticated (no token at all) must still be rejected on the read path ---
        unauth_read = await client.get(f"/conversations/{conv_id}/interactions")
        record(
            "Probe 4 — read path still requires SOME valid token (400/401), not fully open",
            unauth_read.status_code in (400, 401),
            f"status={unauth_read.status_code}",
        )
    finally:
        await client.aclose()
        await reset_overrides()
        await engine.dispose()


# ---------------------------------------------------------------------------
# Probe 5 — record_audit wiring, empirically confirmed via real log capture
# ---------------------------------------------------------------------------

async def probe_5_audit_wiring():
    print("\n=== Probe 5: record_audit wiring — empirical log capture, success and failure paths ===")
    engine = make_memory_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    client = await app_client_for_engine(engine)

    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.DEBUG)
    audit_logger = logging.getLogger("aiservice.audit")
    previous_level = audit_logger.level
    audit_logger.addHandler(handler)
    audit_logger.setLevel(logging.DEBUG)
    audit_logger.propagate = True

    try:
        org_id = str(uuid.uuid4())

        # Success path: establish, execute, list.
        est = await client.post("/conversations", headers=_auth(organization_id=org_id))
        conv_id = est.json()["conversation_id"]
        await client.post(
            f"/conversations/{conv_id}/interactions",
            headers=_auth(organization_id=org_id),
            json={"input_text": "audit probe turn"},
        )
        await client.post(f"/conversations/{conv_id}/close", headers=_auth(organization_id=org_id))

        # Failure path: attempt to execute against the now-CLOSED conversation (409),
        # attempt to close an unrelated tenant's own conversation_id (404/DENIED).
        await client.post(
            f"/conversations/{conv_id}/interactions",
            headers=_auth(organization_id=org_id),
            json={"input_text": "too late"},
        )
        other_org = str(uuid.uuid4())
        await client.post(f"/conversations/{conv_id}/close", headers=_auth(organization_id=other_org))

        emitted = log_stream.getvalue().strip().splitlines()
        actions_seen = {}
        for line in emitted:
            for action in ("ESTABLISH_CONVERSATION", "CLOSE_CONVERSATION", "EXECUTE_INTERACTION"):
                if action in line:
                    actions_seen.setdefault(action, []).append(line)

        has_success = any('"status": "SUCCESS"' in l for l in emitted)
        has_denied = any('"status": "DENIED"' in l for l in emitted)
        expected_actions_present = all(a in actions_seen for a in ("ESTABLISH_CONVERSATION", "CLOSE_CONVERSATION", "EXECUTE_INTERACTION"))

        record(
            "Probe 5 — record_audit emits real structured log records for establish/execute/close (success path)",
            has_success and expected_actions_present,
            f"lines_emitted={len(emitted)}, actions_seen={list(actions_seen.keys())}, has_success={has_success}",
        )
        record(
            "Probe 5 — record_audit emits a DENIED record for the closed-conversation / cross-tenant failure paths",
            has_denied,
            f"has_denied={has_denied}; sample={[l for l in emitted if 'DENIED' in l][:1]}",
        )
        if emitted:
            record("Probe 5 — sample raw audit log line", True, emitted[0][:400])
    finally:
        audit_logger.removeHandler(handler)
        audit_logger.setLevel(previous_level)
        await client.aclose()
        await reset_overrides()
        await engine.dispose()


# ---------------------------------------------------------------------------
# Probe 6 — Structural Memory exclusion, via import-graph (ast), not dir()
# ---------------------------------------------------------------------------

def probe_6_structural_memory_exclusion():
    print("\n=== Probe 6: Structural Memory exclusion — AST import-graph inspection ===")
    path = AISERVICE_ROOT / "services" / "interaction_state_assembler.py"
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    imported_names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_names.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imported_names.append(module)
            for alias in node.names:
                imported_names.append(f"{module}.{alias.name}")

    memory_related_imports = [n for n in imported_names if "memory" in n.lower()]

    # Also walk one level further: for every non-stdlib module actually
    # imported by this file, recursively check ITS OWN imports for anything
    # memory-related, so a re-exported/indirect Memory dependency (e.g.
    # `from repositories.conversation_repository import InteractionRepository`
    # secretly importing a MemoryRepository inside conversation_repository.py)
    # would also be caught — a pure `dir()` check on the assembler module
    # alone cannot see this, since re-exported names would appear directly,
    # but transitively-imported-and-not-re-exported names would not.
    transitive_findings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith(("repositories", "services", "models")):
            candidate = AISERVICE_ROOT / (node.module.replace(".", "/") + ".py")
            if candidate.exists():
                sub_source = candidate.read_text(encoding="utf-8")
                sub_tree = ast.parse(sub_source, filename=str(candidate))
                for sub_node in ast.walk(sub_tree):
                    if isinstance(sub_node, (ast.Import, ast.ImportFrom)):
                        sub_module = getattr(sub_node, "module", None) or ""
                        sub_names = [alias.name for alias in sub_node.names]
                        if "memory" in sub_module.lower() or any("memory" in n.lower() for n in sub_names):
                            transitive_findings.append(f"{node.module} -> {sub_module or sub_names}")

    record(
        "Probe 6 — no direct Memory-related import in interaction_state_assembler.py (AST-verified)",
        memory_related_imports == [],
        f"direct imports found: {memory_related_imports}" if memory_related_imports else f"all imports: {imported_names}",
    )
    record(
        "Probe 6 — no transitive Memory-related import reachable via this module's own direct imports",
        transitive_findings == [],
        f"transitive findings: {transitive_findings}" if transitive_findings else "no transitive Memory reference found one hop out",
    )


# ---------------------------------------------------------------------------
# Probe 7 — Frontend Progressive Disclosure / Evidence Panel required-prop contract
# ---------------------------------------------------------------------------

def probe_7_frontend_contract():
    print("\n=== Probe 7: Frontend Progressive Disclosure / Evidence Panel required-prop contract (static parse) ===")
    frontend_root = AISERVICE_ROOT.parent.parent.parent / "source" / "frontend" / "src" / "components" / "ui"
    pd_path = frontend_root / "ProgressiveDisclosure.tsx"
    ep_path = frontend_root / "EvidencePanel.tsx"

    pd_source = pd_path.read_text(encoding="utf-8")
    ep_source = ep_path.read_text(encoding="utf-8")

    def extract_interface_fields(source: str, interface_name: str) -> dict[str, bool]:
        """Returns {field_name: is_optional}. Parses the TypeScript interface
        body textually (no TS compiler available in this environment) —
        matches `name?: Type` (optional) vs `name: Type` (required) per line,
        skipping comments/blank lines."""
        match = re.search(rf"interface {interface_name}\s*\{{(.*?)\n\}}", source, re.DOTALL)
        assert match, f"interface {interface_name} not found in source"
        body = match.group(1)
        fields: dict[str, bool] = {}
        for line in body.splitlines():
            line = line.strip()
            if not line or line.startswith("//") or line.startswith("*") or line.startswith("/*"):
                continue
            field_match = re.match(r"([a-zA-Z0-9_]+)(\?)?\s*:\s*.+;?", line)
            if field_match:
                name, optional_marker = field_match.group(1), field_match.group(2)
                fields[name] = optional_marker == "?"
        return fields

    pd_fields = extract_interface_fields(pd_source, "ProgressiveDisclosureProps")
    ep_fields = extract_interface_fields(ep_source, "EvidencePanelProps")

    mandatory_pd_states = ["summary", "details", "evidence", "auditHistory"]
    all_present = all(f in pd_fields for f in mandatory_pd_states)
    none_optional = all(pd_fields.get(f) is False for f in mandatory_pd_states)
    record(
        "Probe 7 — ProgressiveDisclosureProps requires all four states (summary/details/evidence/auditHistory), none optional",
        all_present and none_optional,
        f"parsed fields: {pd_fields}",
    )

    # defaultLevel/className are legitimately optional (have defaults / are styling hooks) — confirm they ARE optional,
    # as a sanity check that the parser itself is distinguishing correctly, not just returning all-False by accident.
    parser_sane = pd_fields.get("defaultLevel") is True and pd_fields.get("className") is True
    record(
        "Probe 7 — parser sanity check: defaultLevel/className ARE correctly detected as optional (non-state props)",
        parser_sane,
        f"defaultLevel_optional={pd_fields.get('defaultLevel')}, className_optional={pd_fields.get('className')}",
    )

    # EvidencePanel: confirm it always supplies all four ProgressiveDisclosure props at every call site
    # (i.e., the widget cannot silently omit a state even though EvidencePanelProps itself
    # makes detailsContent/auditTrail optional with sane defaults).
    composes_all_four = all(
        re.search(rf"{prop}\s*=\{{", ep_source) for prop in ["summary", "details", "evidence", "auditHistory"]
    )
    record(
        "Probe 7 — EvidencePanel's own JSX always supplies summary/details/evidence/auditHistory to ProgressiveDisclosure",
        composes_all_four,
        "all four props present as JSX attributes in EvidencePanel's own <ProgressiveDisclosure> composition"
        if composes_all_four
        else "one or more of the four props missing from EvidencePanel's own composition — would silently produce an incomplete widget",
    )


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

async def _run_async_probes():
    await probe_1_cross_tenant()
    await probe_2a_deterministic_race()
    await probe_2b_http_layer_realistic_attempt()
    await probe_3a_harness_fk_not_enforced()
    await probe_3b_fk_enforced_with_pragma()
    await probe_4_platform_admin_gate()
    await probe_5_audit_wiring()


def main() -> int:
    asyncio.run(_run_async_probes())
    probe_6_structural_memory_exclusion()
    probe_7_frontend_contract()

    print("\n" + "=" * 78)
    print("VV-AUDIT-WP-12 probe summary")
    print("=" * 78)
    failed = [r for r in _RESULTS if not r[1]]
    for name, passed, detail in _RESULTS:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
    print(f"\n{len(_RESULTS) - len(failed)}/{len(_RESULTS)} probe assertions passed.")
    if failed:
        print(f"{len(failed)} probe assertion(s) reported FAIL (see detail above; some FAILs are the *expected*,")
        print("defect-confirming outcome for the concurrency probe class — read the written audit report,")
        print("not this raw count, for the Determination.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
