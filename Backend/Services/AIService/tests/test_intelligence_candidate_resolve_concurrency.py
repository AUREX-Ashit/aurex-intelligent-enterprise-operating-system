# tests/test_intelligence_candidate_resolve_concurrency.py
"""
WP-14 BA-03 — Gate 1 remediation, Finding 1 (concurrent double-resolution
race). Purpose-built, from-scratch runtime probe per `CLAUDE.md §19.7b`'s
own method requirement — not adapted from the existing sequential test
suite (`tests/test_intelligence_candidate_resolve_api.py`), which never
exercises two genuinely concurrent requests against the same candidate.

The shared `tests/conftest.py` fixtures (`db_session`/`client`) bind a
single `sqlite+aiosqlite:///:memory:` connection pool used as one shared
in-process session per test — that shape cannot reproduce a real
check-then-act race, since there is only ever one session in flight. This
file therefore builds its own isolated, temp-file-based SQLite database
with its own engine/sessionmaker, and overrides `get_db` to hand out a
genuinely separate session (and therefore a genuinely separate
connection) per request, exactly mirroring `models/database.py::get_db`'s
own real per-request session lifecycle. `asyncio.gather()` fires two
resolve requests at the same physical instant to force interleaving; a
SQLite `timeout` busy-wait (rather than an immediate "database is
locked" error) lets the loser's write block on the winner's write lock
and then re-evaluate its own `WHERE resolution_status = 'PENDING'`
clause against the winner's already-committed state — the same
production mechanism `claim_for_resolution`'s own docstring describes,
reproduced here against a real second connection rather than asserted
only in prose.
"""
from __future__ import annotations

import asyncio
import os
import tempfile
from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config.settings import settings
from main import app
from models.customer_metric import CustomerMetricRegistryModel
from models.database import Base, get_db
from models.search import EvidenceRegistryModel
from models.unclassified_intelligence import UnclassifiedIntelligenceRegistryModel

ORG = str(uuid4())


def _auth() -> dict:
    claims = {
        "person_id": str(uuid4()),
        "identity_id": str(uuid4()),
        "organization_id": ORG,
        "membership_id": str(uuid4()),
        "role_code": "PLATFORM_ADMIN",
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=60),
    }
    token = jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture(scope="function")
async def concurrency_app_client() -> AsyncGenerator[AsyncClient, None]:
    """
    A dedicated temp-file SQLite database + engine, isolated from the
    shared `conftest.py` in-memory engine, so genuinely separate
    connections are possible. `timeout=30` gives the losing connection a
    real busy-wait instead of an immediate `OperationalError`.
    """
    fd, db_path = tempfile.mkstemp(suffix=".sqlite3")
    os.close(fd)

    engine = create_async_engine(
        f"sqlite+aiosqlite:///{db_path}",
        connect_args={"timeout": 30},
    )
    session_local = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with session_local() as session:
            try:
                yield session
            finally:
                await session.close()

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as async_client:
        async_client._concurrency_session_local = session_local  # type: ignore[attr-defined]
        yield async_client

    app.dependency_overrides.clear()
    await engine.dispose()
    os.remove(db_path)


@pytest.mark.asyncio
async def test_two_concurrent_resolutions_of_same_candidate_exactly_one_wins(
    concurrency_app_client: AsyncClient,
):
    """
    Gate 1 Finding 1 probe. Two coroutines call resolve() on the SAME
    PENDING candidate at the same instant via `asyncio.gather()`. Required
    outcome (per the independent certification's own required properties):
    exactly one 200 and one 409; exactly one `customer_metric_registry`
    row exists; exactly one linked `evidence_registry` row exists; the
    candidate's final persisted state matches the winner, not a
    interleaved/partial write from the loser.
    """
    client = concurrency_app_client

    register_resp = await client.post(
        "/intelligence-candidates",
        json={
            "raw_extracted_value": "Concurrency probe fact",
            "source_document_reference": "concurrency-probe.pdf",
            "source_page_section": "p.1",
            "extraction_method": "MANUAL_ENTRY",
        },
        headers=_auth(),
    )
    assert register_resp.status_code == 201, register_resp.text
    unclassified_id = register_resp.json()["unclassified_id"]

    body = {
        "outcome": "NEW_CDE_CREATED",
        "metric_name": "Concurrency Probe Metric",
        "metric_code": "CONCURRENCY_PROBE_METRIC",
    }

    async def _attempt():
        return await client.post(
            f"/intelligence-candidates/{unclassified_id}/resolve",
            json=body,
            headers=_auth(),
        )

    resp_a, resp_b = await asyncio.gather(_attempt(), _attempt())

    statuses = sorted([resp_a.status_code, resp_b.status_code])
    assert statuses == [200, 409], (
        f"expected exactly one 200 and one 409, got {resp_a.status_code} and {resp_b.status_code} — "
        f"bodies: {resp_a.text} / {resp_b.text}"
    )

    winner = resp_a if resp_a.status_code == 200 else resp_b
    winner_body = winner.json()
    assert winner_body["resolution_status"] == "NEW_CDE_CREATED"
    winning_customer_metric_id = winner_body["resolved_customer_metric_id"]
    assert winning_customer_metric_id is not None

    session_local = client._concurrency_session_local  # type: ignore[attr-defined]
    async with session_local() as verify_session:
        metric_rows = (
            await verify_session.execute(
                select(CustomerMetricRegistryModel).where(
                    CustomerMetricRegistryModel.organization_id == UUID(ORG)
                )
            )
        ).scalars().all()
        assert len(metric_rows) == 1, (
            f"expected exactly one customer_metric_registry row (no orphan from the losing request), "
            f"found {len(metric_rows)}"
        )
        assert str(metric_rows[0].customer_metric_id) == winning_customer_metric_id

        evidence_rows = (
            await verify_session.execute(
                select(EvidenceRegistryModel).where(
                    EvidenceRegistryModel.linked_entity_id == metric_rows[0].customer_metric_id,
                    EvidenceRegistryModel.linked_entity_type == "customer_metric_registry",
                )
            )
        ).scalars().all()
        assert len(evidence_rows) == 1, (
            f"expected exactly one linked evidence_registry row (no orphan Evidence from the losing "
            f"request), found {len(evidence_rows)}"
        )

        candidate_row = (
            await verify_session.execute(
                select(UnclassifiedIntelligenceRegistryModel).where(
                    UnclassifiedIntelligenceRegistryModel.unclassified_id == UUID(unclassified_id)
                )
            )
        ).scalar_one()
        assert candidate_row.resolution_status == "NEW_CDE_CREATED"
        assert str(candidate_row.resolved_customer_metric_id) == winning_customer_metric_id


@pytest.mark.asyncio
async def test_two_concurrent_discards_of_same_candidate_exactly_one_wins(
    concurrency_app_client: AsyncClient,
):
    """
    Same probe against the DISCARDED path (no side-effecting rows at all
    on success) — confirms the claim itself, not merely the customer_metric
    orphan-prevention, is race-safe.
    """
    client = concurrency_app_client

    register_resp = await client.post(
        "/intelligence-candidates",
        json={
            "raw_extracted_value": "Concurrency discard probe fact",
            "source_document_reference": "concurrency-discard-probe.pdf",
            "source_page_section": "p.1",
            "extraction_method": "MANUAL_ENTRY",
        },
        headers=_auth(),
    )
    assert register_resp.status_code == 201, register_resp.text
    unclassified_id = register_resp.json()["unclassified_id"]

    async def _attempt():
        return await client.post(
            f"/intelligence-candidates/{unclassified_id}/resolve",
            json={"outcome": "DISCARDED"},
            headers=_auth(),
        )

    resp_a, resp_b = await asyncio.gather(_attempt(), _attempt())
    statuses = sorted([resp_a.status_code, resp_b.status_code])
    assert statuses == [200, 409], (
        f"expected exactly one 200 and one 409, got {resp_a.status_code} and {resp_b.status_code} — "
        f"bodies: {resp_a.text} / {resp_b.text}"
    )
