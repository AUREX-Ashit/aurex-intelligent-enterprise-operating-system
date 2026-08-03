# _vv_probe_wp11.py
"""
TEMPORARY, from-scratch V&V Audit (Gate 2) empirical probe script for WP-11
(Enterprise Search, C-093), per CLAUDE.md §19.7b. NOT part of the shipped
test suite (does not match test_*.py, not collected by pytest). Deleted
after use unless the auditor decides to keep specific probes as permanent
regression tests.

Run from Backend/Services/AIService:
    python tests/_vv_probe_wp11.py
"""
import asyncio
import math
import sys
import tempfile
import traceback
import uuid
from datetime import datetime, timedelta, timezone

from httpx import ASGITransport, AsyncClient
from jose import jwt
from sqlalchemy import event, text
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

sys.path.insert(0, ".")

from main import app  # noqa: E402
from models.database import Base, get_db  # noqa: E402
from config.settings import settings  # noqa: E402
from models.search import DocumentChunkRegistryModel, EvidenceRegistryModel, VectorIndexRegistryModel  # noqa: E402
from repositories.search_repository import (  # noqa: E402
    DocumentChunkRegistryRepository,
    EvidenceRegistryRepository,
    VectorIndexRegistryRepository,
)

PASS = "PASS"
FAIL = "FAIL"
results = []


def record(name: str, ok: bool, detail: str):
    results.append((name, PASS if ok else FAIL, detail))
    print(f"[{PASS if ok else FAIL}] {name}: {detail}")


def token(organization_id: str, role_code: str = "PLATFORM_ADMIN") -> str:
    claims = {
        "person_id": str(uuid.uuid4()),
        "identity_id": str(uuid.uuid4()),
        "organization_id": organization_id,
        "membership_id": str(uuid.uuid4()),
        "role_code": role_code,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=60),
    }
    return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def auth(org: str, role: str = "PLATFORM_ADMIN") -> dict:
    return {"Authorization": f"Bearer {token(org, role)}"}


async def make_client(engine):
    session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    session = session_maker()

    async def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    client = AsyncClient(transport=ASGITransport(app=app), base_url="http://probe")
    return client, session


async def fresh_engine(url: str):
    engine = create_async_engine(url, connect_args={"check_same_thread": False})
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine


# ---------------------------------------------------------------------------
# Probe 1 — Genuine two-organization adversarial probe over real HTTP calls,
# including a scenario the shipped suite never tries: IDENTICAL index_name
# registered independently by two different, unrelated organizations.
# ---------------------------------------------------------------------------
async def probe_1_two_org_same_name_adversarial():
    engine = await fresh_engine("sqlite+aiosqlite:///:memory:")
    client, session = await make_client(engine)
    try:
        org_a, org_b = str(uuid.uuid4()), str(uuid.uuid4())

        # Both orgs independently establish an index with the SAME name.
        r1 = await client.post(
            "/search/index-configurations",
            json={"index_name": "shared-name", "embedding_model": "m", "embedding_dimension": 16},
            headers=auth(org_a),
        )
        r2 = await client.post(
            "/search/index-configurations",
            json={"index_name": "shared-name", "embedding_model": "m", "embedding_dimension": 16},
            headers=auth(org_b),
        )
        record("P1a: both orgs can establish an index of the identical name", r1.status_code == 201 and r2.status_code == 201, f"org_a={r1.status_code} org_b={r2.status_code}")

        # Org A registers content; Org B registers different content, same index name.
        ca = await client.post(
            "/search/content",
            json={"index_name": "shared-name", "text": "ORG_A_SECRET_PAYROLL_FIGURE_999", "evidence_source": "A"},
            headers=auth(org_a),
        )
        cb = await client.post(
            "/search/content",
            json={"index_name": "shared-name", "text": "ORG_B_SECRET_PAYROLL_FIGURE_111", "evidence_source": "B"},
            headers=auth(org_b),
        )
        record("P1b: both orgs can register content under their own same-named index", ca.status_code == 201 and cb.status_code == 201, f"org_a={ca.status_code} org_b={cb.status_code}")

        # Org B searches "shared-name" — must see ONLY its own content, never Org A's.
        sb = await client.post("/search/query", json={"query": "payroll", "index_name": "shared-name"}, headers=auth(org_b, "MEMBER"))
        sb_texts = [r["citation"] for r in sb.json().get("results", [])]
        leak = any("ORG_A_SECRET" in t for t in sb_texts)
        contains_own = any("ORG_B" in (r["metadata"].get("source") or "") for r in sb.json().get("results", [])) or len(sb.json().get("results", [])) == 1
        record(
            "P1c: Org B searching identically-named index sees only its own content, never Org A's",
            sb.status_code == 200 and not leak,
            f"status={sb.status_code} results={sb.json().get('results')}",
        )

        sa = await client.post("/search/query", json={"query": "payroll", "index_name": "shared-name"}, headers=auth(org_a, "MEMBER"))
        sa_texts = [r["citation"] for r in sa.json().get("results", [])]
        leak_a = any("ORG_B_SECRET" in t for t in sa_texts)
        record(
            "P1d: Org A searching identically-named index sees only its own content, never Org B's",
            sa.status_code == 200 and not leak_a,
            f"status={sa.status_code} results={sa.json().get('results')}",
        )
    except Exception as e:
        record("P1: two-org same-name adversarial probe", False, f"UNHANDLED EXCEPTION: {type(e).__name__}: {e}\n{traceback.format_exc()}")
    finally:
        await client.aclose()
        await session.close()
        await engine.dispose()
        app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Probe 2 — Duplicate index_name WITHIN the same organization. No uniqueness
# constraint exists anywhere (model, migration, or service). get_by_name_
# for_caller uses .scalar_one_or_none() — does a second row for the same
# (organization_id, index_name) crash the request?
# ---------------------------------------------------------------------------
async def probe_2_duplicate_index_name_same_org():
    engine = await fresh_engine("sqlite+aiosqlite:///:memory:")
    client, session = await make_client(engine)
    try:
        org_a = str(uuid.uuid4())
        r1 = await client.post(
            "/search/index-configurations",
            json={"index_name": "dup-index", "embedding_model": "m", "embedding_dimension": 16},
            headers=auth(org_a),
        )
        r2 = await client.post(
            "/search/index-configurations",
            json={"index_name": "dup-index", "embedding_model": "m", "embedding_dimension": 16},
            headers=auth(org_a),
        )
        record(
            "P2a: establishing a second index with the identical name under the SAME org is accepted (no uniqueness constraint)",
            r1.status_code == 201 and r2.status_code == 201,
            f"first={r1.status_code} second={r2.status_code}",
        )

        # Now BA-03 (register content) resolves by name — get_by_name_for_caller
        # will find TWO rows matching (organization_id, index_name) and call
        # .scalar_one_or_none() on that query, which raises MultipleResultsFound
        # if the ORM query truly returns 2 rows.
        try:
            resp = await client.post(
                "/search/content",
                json={"index_name": "dup-index", "text": "some content"},
                headers=auth(org_a),
            )
            record(
                "P2b: registering content against an ambiguous (duplicate-name) index returns a handled HTTP response, not a raw exception",
                resp.status_code < 500,
                f"status={resp.status_code} body={resp.text[:300]}",
            )
        except MultipleResultsFound as e:
            record(
                "P2b: registering content against an ambiguous (duplicate-name) index returns a handled HTTP response, not a raw exception",
                False,
                f"UNHANDLED sqlalchemy.exc.MultipleResultsFound propagated out of the ASGI app: {e}",
            )
        except Exception as e:
            record(
                "P2b: registering content against an ambiguous (duplicate-name) index returns a handled HTTP response, not a raw exception",
                False,
                f"UNHANDLED EXCEPTION propagated: {type(e).__name__}: {e}",
            )

        # Same probe against BA-02 (execute search) — same get_by_name_for_caller call path.
        try:
            resp2 = await client.post(
                "/search/query",
                json={"query": "anything", "index_name": "dup-index"},
                headers=auth(org_a, "MEMBER"),
            )
            record(
                "P2c: querying against an ambiguous (duplicate-name) index returns a handled HTTP response, not a raw exception",
                resp2.status_code < 500,
                f"status={resp2.status_code} body={resp2.text[:300]}",
            )
        except MultipleResultsFound as e:
            record(
                "P2c: querying against an ambiguous (duplicate-name) index returns a handled HTTP response, not a raw exception",
                False,
                f"UNHANDLED sqlalchemy.exc.MultipleResultsFound propagated out of the ASGI app: {e}",
            )
        except Exception as e:
            record(
                "P2c: querying against an ambiguous (duplicate-name) index returns a handled HTTP response, not a raw exception",
                False,
                f"UNHANDLED EXCEPTION propagated: {type(e).__name__}: {e}",
            )
    finally:
        await client.aclose()
        await session.close()
        await engine.dispose()
        app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Probe 3 — Harness/fixture production-parity: does the test engine enforce
# FK constraints? Insert a document_chunk_registry row with a nonexistent
# evidence_id directly via the repository layer, bypassing the service's
# own validation, first under the harness's own configuration (no PRAGMA),
# then under a from-scratch engine with PRAGMA foreign_keys=ON, to establish
# whether this would be silently accepted in the exact same test harness
# every WP-11 test also uses, and whether real FK enforcement would catch it.
# ---------------------------------------------------------------------------
async def probe_3_fk_enforcement_parity():
    # 3a — exactly the shipped harness's own engine configuration (no PRAGMA).
    engine_no_fk = await fresh_engine("sqlite+aiosqlite:///:memory:")
    session_maker = async_sessionmaker(bind=engine_no_fk, class_=AsyncSession, expire_on_commit=False)
    async with session_maker() as session:
        org = uuid.uuid4()
        chunk_repo = DocumentChunkRegistryRepository(session)
        nonexistent_evidence_id = uuid.uuid4()
        nonexistent_index_id = uuid.uuid4()
        try:
            await chunk_repo.create(
                organization_id=org,
                evidence_id=nonexistent_evidence_id,
                vector_index_id=nonexistent_index_id,
                chunk_sequence_number=0,
                chunk_locator="probe",
                chunk_text_hash="deadbeef",
                embedding_reference="local-chunk-deadbeef",
                embedding_model_version="probe-model",
            )
            await session.commit()
            record(
                "P3a: harness (no PRAGMA foreign_keys) silently accepts a document_chunk_registry row referencing a nonexistent evidence_registry.evidence_id",
                True,
                "INSERT succeeded with no FK error — confirms the harness does NOT enforce document_chunk_registry's own two NOT NULL FKs (evidence_id, vector_index_id), same defect class as TD-096.",
            )
        except Exception as e:
            record(
                "P3a: harness (no PRAGMA foreign_keys) silently accepts a document_chunk_registry row referencing a nonexistent evidence_registry.evidence_id",
                False,
                f"INSERT was rejected: {type(e).__name__}: {e}",
            )
    await engine_no_fk.dispose()

    # 3b — a from-scratch engine with PRAGMA foreign_keys=ON enabled via a
    # connect-event listener, mirroring how a real, constraint-enforcing
    # database (or a corrected test harness) would behave.
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    engine_fk = create_async_engine(f"sqlite+aiosqlite:///{tmp.name}", connect_args={"check_same_thread": False})

    @event.listens_for(engine_fk.sync_engine, "connect")
    def _enable_fk(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    async with engine_fk.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker_fk = async_sessionmaker(bind=engine_fk, class_=AsyncSession, expire_on_commit=False)
    async with session_maker_fk() as session:
        org = uuid.uuid4()
        chunk_repo = DocumentChunkRegistryRepository(session)
        nonexistent_evidence_id = uuid.uuid4()
        nonexistent_index_id = uuid.uuid4()
        try:
            await chunk_repo.create(
                organization_id=org,
                evidence_id=nonexistent_evidence_id,
                vector_index_id=nonexistent_index_id,
                chunk_sequence_number=0,
                chunk_locator="probe",
                chunk_text_hash="deadbeef",
                embedding_reference="local-chunk-deadbeef",
                embedding_model_version="probe-model",
            )
            await session.commit()
            record(
                "P3b: under real FK enforcement (PRAGMA foreign_keys=ON), the same insert is REJECTED",
                False,
                "INSERT unexpectedly succeeded even with FK enforcement on — the FK declaration itself may be broken.",
            )
        except Exception as e:
            record(
                "P3b: under real FK enforcement (PRAGMA foreign_keys=ON), the same insert is REJECTED",
                True,
                f"INSERT correctly rejected under real FK enforcement: {type(e).__name__}: {str(e)[:200]}",
            )
    await engine_fk.dispose()
    import os
    try:
        os.unlink(tmp.name)
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Probe 4 — top_k boundary values (1, 50, 51) and top_k smaller than the
# number of registered chunks.
# ---------------------------------------------------------------------------
async def probe_4_top_k_boundaries():
    engine = await fresh_engine("sqlite+aiosqlite:///:memory:")
    client, session = await make_client(engine)
    try:
        org = str(uuid.uuid4())
        await client.post(
            "/search/index-configurations",
            json={"index_name": "topk-index", "embedding_model": "m", "embedding_dimension": 8},
            headers=auth(org),
        )
        # A single text long enough to split into 5 chunks of 1000 chars each (fixed chunk size).
        long_text = "X" * 4500  # -> 5 chunks: 1000,1000,1000,1000,500
        reg = await client.post(
            "/search/content",
            json={"index_name": "topk-index", "text": long_text, "evidence_source": "long-doc"},
            headers=auth(org),
        )
        chunk_count = reg.json().get("chunk_count")
        record("P4a: long text registers multiple chunks (fixed-size chunker exercised)", chunk_count == 5, f"chunk_count={chunk_count}")

        for k, expect_status, expect_len in [(1, 200, 1), (50, 200, 5)]:
            resp = await client.post(
                "/search/query", json={"query": "anything", "index_name": "topk-index", "top_k": k}, headers=auth(org, "MEMBER")
            )
            n = len(resp.json().get("results", [])) if resp.status_code == 200 else None
            record(
                f"P4b: top_k={k} returns status {expect_status} with <= {expect_len} results (min(top_k, registered_chunks))",
                resp.status_code == expect_status and n == expect_len,
                f"status={resp.status_code} result_count={n}",
            )

        # top_k=51 exceeds the schema's own le=50 — must be rejected at validation (422), not silently clamped.
        resp51 = await client.post(
            "/search/query", json={"query": "anything", "index_name": "topk-index", "top_k": 51}, headers=auth(org, "MEMBER")
        )
        record("P4c: top_k=51 is rejected by schema validation (422), not silently clamped to 50", resp51.status_code == 422, f"status={resp51.status_code}")

        # top_k=0 also excluded by schema (gt=0).
        resp0 = await client.post(
            "/search/query", json={"query": "anything", "index_name": "topk-index", "top_k": 0}, headers=auth(org, "MEMBER")
        )
        record("P4d: top_k=0 is rejected by schema validation (422)", resp0.status_code == 422, f"status={resp0.status_code}")
    except Exception as e:
        record("P4: top_k boundary probe", False, f"UNHANDLED EXCEPTION: {type(e).__name__}: {e}\n{traceback.format_exc()}")
    finally:
        await client.aclose()
        await session.close()
        await engine.dispose()
        app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Probe 5 — Embedding-dimension fix: confirm it is NOT narrowly hard-coded
# to 1536/768 (the only two values the shipped suite ever exercises) by
# using dimensions neither value uses: 384 and 3072.
# ---------------------------------------------------------------------------
async def probe_5_embedding_dimension_generality():
    engine = await fresh_engine("sqlite+aiosqlite:///:memory:")
    client, session = await make_client(engine)
    try:
        org = str(uuid.uuid4())
        for dim in (384, 3072, 1):
            r_est = await client.post(
                "/search/index-configurations",
                json={"index_name": f"dim-{dim}", "embedding_model": "custom-model", "embedding_dimension": dim},
                headers=auth(org),
            )
            r_reg = await client.post(
                "/search/content",
                json={"index_name": f"dim-{dim}", "text": f"content for dimension {dim}"},
                headers=auth(org),
            )
            record(
                f"P5: establish+register succeeds at embedding_dimension={dim} (neither 1536 nor 768)",
                r_est.status_code == 201 and r_reg.status_code == 201,
                f"establish={r_est.status_code} register={r_reg.status_code} body={r_reg.text[:200] if r_reg.status_code != 201 else 'ok'}",
            )
    except Exception as e:
        record("P5: embedding dimension generality probe", False, f"UNHANDLED EXCEPTION: {type(e).__name__}: {e}\n{traceback.format_exc()}")
    finally:
        await client.aclose()
        await session.close()
        await engine.dispose()
        app.dependency_overrides.clear()


async def main():
    await probe_1_two_org_same_name_adversarial()
    await probe_2_duplicate_index_name_same_org()
    await probe_3_fk_enforcement_parity()
    await probe_4_top_k_boundaries()
    await probe_5_embedding_dimension_generality()

    print("\n===== SUMMARY =====")
    n_fail = sum(1 for _, status, _ in results if status == FAIL)
    for name, status, detail in results:
        print(f"[{status}] {name}")
    print(f"\n{len(results) - n_fail}/{len(results)} probe assertions passed, {n_fail} failed.")


if __name__ == "__main__":
    asyncio.run(main())
