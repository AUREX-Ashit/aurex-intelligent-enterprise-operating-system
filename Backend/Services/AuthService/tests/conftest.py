import asyncio
from typing import AsyncGenerator, Generator
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from fastapi.testclient import TestClient

from main import app
from models.database import Base, db_manager

# Separate test SQLite DB to simulate concurrent tests safely in memory
SQLITE_TEST_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def test_engine():
    """
    Function-scoped (not session-scoped): each test gets its own empty
    in-memory database, so committed data from one test's fixtures (e.g.
    seeded_person_identity) never leaks into another test via a shared
    engine. Previously session-scoped, which worked only as long as no two
    tests committed conflicting data (e.g. the same unique email) — that
    assumption broke once a second Business Activity's tests reused the
    same seeding fixture.
    """
    engine = create_async_engine(SQLITE_TEST_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

@pytest.fixture
def client(db_session) -> Generator[TestClient, None, None]:
    """
    TestClient yielding fixture with database overrides logic configured.
    """
    async def override_get_session():
        yield db_session

    app.dependency_overrides[db_manager.get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
