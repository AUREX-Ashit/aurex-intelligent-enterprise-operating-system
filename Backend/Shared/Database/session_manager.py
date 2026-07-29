"""
Aurex Shared Database Framework - Session Manager Module.

Manages scoped asynchronous database sessions, transactions, and event listeners
to enforce multi-tenant lifecycle hooks automatically on flush.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable
from sqlalchemy.ext.asyncio import (
    AsyncSession, 
    async_sessionmaker,
    AsyncEngine
)
from sqlalchemy import event

from aurex.backend.shared.database.engine_factory import EngineFactory
from aurex.backend.shared.database.base_model import TenantScopedModel
from aurex.backend.shared.database.exceptions import TransactionError

logger = logging.getLogger("Aurex.Database.SessionManager")


class SessionManager:
    """
    Primary interface for session lifecycles, transactional boundaries,
    and row-level tenant security listener registration.
    """

    _session_maker = None

    @classmethod
    def get_session_maker(cls, engine: Optional[AsyncEngine] = None) -> async_sessionmaker[AsyncSession]:
        """
        Retrieves or initializes the async sessionmaker configured with appropriate parameters.
        """
        if cls._session_maker is None:
            active_engine = engine or EngineFactory.get_shared_engine()
            
            # Form sessionmaker bound to asyncpg engine
            cls._session_maker = async_sessionmaker(
                bind=active_engine,
                class_=AsyncSession,
                expire_on_commit=False,  # Essential for safe asynchronous attribute fetches after commit
                autocommit=False,
                autoflush=False
            )
            
            # Register event hook to intercept flushes and enforce row isolation automatically!
            cls._register_hooks(cls._session_maker)
            
        return cls._session_maker

    @classmethod
    def _register_hooks(cls, session_maker_obj: async_sessionmaker[AsyncSession]) -> None:
        """
        Registers SQLAlchemy event-listeners ensuring that any object inheriting from TenantScopedModel
        is automatically checked for proper tenant isolation context during a flush.
        """
        @event.listens_for(AsyncSession, "before_flush")
        def audit_and_bind_tenant_id(session, flush_context, instances):
            """
            Event hook triggered before flushing changes to PostgreSQL.
            Intercepts any modified state changes, validating credentials.
            """
            # Iterate through newly added, modified, or deleted records in the transaction
            for obj in session.new | session.dirty:
                if isinstance(obj, TenantScopedModel):
                    obj.enforce_tenant_context_bound()

    @classmethod
    @asynccontextmanager
    async def transactional_session(cls) -> AsyncGenerator[AsyncSession, None]:
        """
        Acquires an AsyncSession and starts an explicit database transaction boundary.
        Automatically handles commit upon success, or rollback in the event of an raised exception.
        
        Example:
            async with SessionManager.transactional_session() as session:
                session.add(new_user)
            # Transaction commits cleanly here! If inside the block any exception occurred,
            # rollback triggers instantly.
        """
        maker = cls.get_session_maker()
        session: AsyncSession = maker()
        
        try:
            logger.debug("Opening async transaction boundary.")
            yield session
            logger.debug("Flushing work and committing db changes.")
            await session.commit()
        except Exception as e:
            logger.warning(f"Transaction aborted. Rolling back changes. Reason: {str(e)}")
            await session.rollback()
            raise TransactionError(f"Database transaction rolled back due to error: {str(e)}") from e
        finally:
            logger.debug("Closing async session pool instance.")
            await session.close()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Standard FastAPI dependency injection endpoint producing active transactional safe scoped sessions.
    
    Example:
        @app.get("/api/evidence")
        async def fetch_evidence(session: AsyncSession = Depends(get_db_session)):
            ...
    """
    maker = SessionManager.get_session_maker()
    session = maker()
    try:
        yield session
    finally:
        await session.close()
