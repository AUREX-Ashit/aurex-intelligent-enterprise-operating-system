import asyncio
import pytest
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from httpx import HTTPWithReactions, AsyncClient
from main import app
from models.database import Base, get_db_session

# Test configuration: We use a lightweight, in-memory SQLite async database for clean test separation
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """
    Overrides pytest-asyncio's event loop with a session-scoped loop.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def init_test_db():
    """
    Pre-creates all relational schema structures before executing test runs.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Generates a dedicated async transaction context rolled back automatically 
    after every test boundary.
    """
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()

@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Assembles a fully decoupled async test client, overidding active main database sessions
    to target the test memory database scope.
    """
    async def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db_session] = _get_test_db
    
    # Use ASGIPort or httpx with app link directly
    async with AsyncClient(app=app, base_url="http://testserver") as async_client:
        yield async_client
        
    app.dependency_overrides.clear()
