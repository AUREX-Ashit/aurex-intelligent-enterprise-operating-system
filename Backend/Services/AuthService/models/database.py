from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    SQLAlchemy 2.x Declarative Base model using Mapped as default.
    """
    pass

class DatabaseSessionManager:
    """
    Thread-safe Database connection manager supporting modern asyncio pools.
    """
    def __init__(self) -> None:
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = None

    async def initialize(self) -> None:
        """
        Creates the AsyncEngine and Session Factory.
        """
        from config import settings
        database_url = settings.database_url

        # Enforce that database configuration must be defined on startup
        if not database_url:
            raise RuntimeError(
                "Database configuration is missing. "
                "Specify 'DATABASE_URL' environment variable or configure "
                "database url in Config/platform-config.yaml."
            )
        
        # Configure Async Engine with optimal production values
        self._engine = create_async_engine(
            database_url,
            echo=False,
            pool_size=20,
            max_overflow=10,
            pool_timeout=30.0,
            pool_recycle=1800,  # recycle connections after 30 mins
        )
        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def close(self) -> None:
        """
        Closes all active pooled connections.
        """
        if self._engine is None:
            return
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Dependency injection helper to yield standard transactional db sessions.
        """
        if self._sessionmaker is None:
            raise RuntimeError("DatabaseSessionManager index is uninitialized.")
        async with self._sessionmaker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

db_manager = DatabaseSessionManager()
