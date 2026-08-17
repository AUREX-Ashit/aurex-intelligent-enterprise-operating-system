# tests/test_knowledge_asset_transition_concurrency.py
"""
WP-14 BA-04 Increment — Knowledge Asset Lifecycle Transition concurrency
probe (`TDS-014 §6`, `BA04-INC-DEC-004`). Purpose-built, from-scratch
runtime probe — not adapted from the existing sequential test suite
(`tests/test_knowledge_asset_api.py`), which never exercises two
genuinely concurrent requests against the same Knowledge Asset.

Mirrors `tests/test_intelligence_candidate_resolve_concurrency.py`'s own
established pattern exactly: the shared `tests/conftest.py` fixtures bind
a single in-memory SQLite connection pool, which cannot reproduce a real
check-then-act race (only one session is ever in flight). This file
builds its own isolated, temp-file-based SQLite database with its own
engine/sessionmaker, overriding `get_db` to hand out a genuinely separate
session/connection per request, and uses `asyncio.gather()` to force two
requests to execute at the same physical instant.
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
from models.database import Base, get_db
from models.knowledge_asset import KnowledgeAssetRegistryModel

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
async def concurrency_app_client(monkeypatch) -> AsyncGenerator[AsyncClient, None]:
    """
    A dedicated temp-file SQLite database + engine, isolated from the
    shared `conftest.py` in-memory engine, so genuinely separate
    connections are possible. `timeout=30` gives the losing connection a
    real busy-wait instead of an immediate `OperationalError`. Also
    patches `KafkaEventPublisher.publish` to capture publish attempts
    without depending on the mock broker's own no-op behavior.
    """
    from aurex.backend.shared.events.event_publisher import KafkaEventPublisher

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

    captured_events: list = []

    def fake_publish(self, event, destination, partition_key=None):
        captured_events.append(event)

    monkeypatch.setattr(KafkaEventPublisher, "publish", fake_publish)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as async_client:
        async_client._concurrency_session_local = session_local  # type: ignore[attr-defined]
        async_client._captured_events = captured_events  # type: ignore[attr-defined]
        yield async_client

    app.dependency_overrides.clear()
    await engine.dispose()
    os.remove(db_path)


async def _establish(client: AsyncClient) -> str:
    resp = await client.post(
        "/knowledge-assets",
        json={"provenance_reference": "concurrency-probe.pdf"},
        headers=_auth(),
    )
    assert resp.status_code == 201, resp.text
    return resp.json()["knowledge_asset_id"]


@pytest.mark.asyncio
async def test_two_concurrent_accept_attempts_exactly_one_winner(concurrency_app_client: AsyncClient):
    """
    Two coroutines call transition(target_status=ACCEPTED) on the SAME
    PROPOSED Knowledge Asset at the same instant. Required outcome
    (TDS-014 §6): exactly one 200 and one 409; the loser does not change
    state, does not produce a SUCCESS audit, and does not publish a
    second ACCEPTED event; the persisted state matches the winner.
    """
    client = concurrency_app_client
    knowledge_asset_id = await _establish(client)

    async def _attempt():
        return await client.post(
            f"/knowledge-assets/{knowledge_asset_id}/transition",
            json={"target_status": "ACCEPTED"},
            headers=_auth(),
        )

    resp_a, resp_b = await asyncio.gather(_attempt(), _attempt())

    statuses = sorted([resp_a.status_code, resp_b.status_code])
    assert statuses == [200, 409], (
        f"expected exactly one 200 and one 409, got {resp_a.status_code} and {resp_b.status_code} — "
        f"bodies: {resp_a.text} / {resp_b.text}"
    )

    winner = resp_a if resp_a.status_code == 200 else resp_b
    assert winner.json()["curation_status"] == "ACCEPTED"

    captured_events = client._captured_events  # type: ignore[attr-defined]
    assert len(captured_events) == 1, (
        f"expected exactly one ACCEPTED event publish attempt (no duplicate from the loser), "
        f"found {len(captured_events)}"
    )
    assert captured_events[0].to_dict()["knowledge_asset_id"] == knowledge_asset_id

    session_local = client._concurrency_session_local  # type: ignore[attr-defined]
    async with session_local() as verify_session:
        row = (
            await verify_session.execute(
                select(KnowledgeAssetRegistryModel).where(
                    KnowledgeAssetRegistryModel.knowledge_asset_id == UUID(knowledge_asset_id)
                )
            )
        ).scalar_one()
        assert row.curation_status == "ACCEPTED"


@pytest.mark.asyncio
async def test_two_concurrent_validate_attempts_exactly_one_winner(concurrency_app_client: AsyncClient):
    """Same invariant against the non-event-emitting VALIDATED target — confirms the guard itself, not merely event de-duplication, is race-safe."""
    client = concurrency_app_client
    knowledge_asset_id = await _establish(client)

    async def _attempt():
        return await client.post(
            f"/knowledge-assets/{knowledge_asset_id}/transition",
            json={"target_status": "VALIDATED"},
            headers=_auth(),
        )

    resp_a, resp_b = await asyncio.gather(_attempt(), _attempt())
    statuses = sorted([resp_a.status_code, resp_b.status_code])
    assert statuses == [200, 409], (
        f"expected exactly one 200 and one 409, got {resp_a.status_code} and {resp_b.status_code} — "
        f"bodies: {resp_a.text} / {resp_b.text}"
    )
    assert client._captured_events == []  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_concurrent_competing_transitions_exactly_one_winner(concurrency_app_client: AsyncClient):
    """
    One coroutine requests ACCEPTED, the other REJECTED, on the same
    PROPOSED Knowledge Asset, at the same instant. Exactly one target
    wins; the final persisted state matches whichever target won; an
    ACCEPTED event is published only if ACCEPTED actually won.
    """
    client = concurrency_app_client
    knowledge_asset_id = await _establish(client)

    async def _attempt(target_status: str):
        return await client.post(
            f"/knowledge-assets/{knowledge_asset_id}/transition",
            json={"target_status": target_status},
            headers=_auth(),
        )

    resp_accept, resp_reject = await asyncio.gather(_attempt("ACCEPTED"), _attempt("REJECTED"))

    statuses = sorted([resp_accept.status_code, resp_reject.status_code])
    assert statuses == [200, 409], (
        f"expected exactly one 200 and one 409, got ACCEPTED={resp_accept.status_code} "
        f"REJECTED={resp_reject.status_code} — bodies: {resp_accept.text} / {resp_reject.text}"
    )

    accept_won = resp_accept.status_code == 200
    captured_events = client._captured_events  # type: ignore[attr-defined]

    session_local = client._concurrency_session_local  # type: ignore[attr-defined]
    async with session_local() as verify_session:
        row = (
            await verify_session.execute(
                select(KnowledgeAssetRegistryModel).where(
                    KnowledgeAssetRegistryModel.knowledge_asset_id == UUID(knowledge_asset_id)
                )
            )
        ).scalar_one()

        if accept_won:
            assert row.curation_status == "ACCEPTED"
            assert len(captured_events) == 1, "ACCEPTED won the race — exactly one event must have been published"
        else:
            assert row.curation_status == "REJECTED"
            assert captured_events == [], "REJECTED won the race — no event may be published"
