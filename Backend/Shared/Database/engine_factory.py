"""
CorpStage Shared Database Framework - Engine Factory Module.

Handles building and configuring the asynchronous database engines for SQLAlchemy 2.x.
Ensures integration with the CorpStage Shared Configuration Framework for pool sizes,
timeouts, and cluster configurations.
"""

import logging
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool

from corpstage.backend.shared.config import SettingsManager
from corpstage.backend.shared.database.exceptions import DatabaseInitializationError

logger = logging.getLogger("CorpStage.Database.EngineFactory")


class EngineFactory:
    """
    Factory class designed to handle resilient construction and life cycle
    management of highly scalable, pooled, asynchronous SQLAlchemy engines.
    """

    _engine: Optional[AsyncEngine] = None

    @classmethod
    def get_connection_url(cls, config_override: Optional[Dict[str, Any]] = None) -> str:
        """
        Coordinates database parameters to formulate an asyncpg database connection URL.
        """
        if config_override:
            db_params = config_override
        else:
            try:
                settings = SettingsManager.get_settings()
                db_params = settings.database.postgresql.to_dict()
            except Exception as e:
                raise DatabaseInitializationError(
                    f"Failed to fetch database credentials from Shared Config: {str(e)}. "
                    "Ensure SettingsManager has been initialized."
                )

        # Build clean string
        host = db_params.get("host", "localhost")
        port = db_params.get("port", 5432)
        user = db_params.get("username", "corpstage")
        password = db_params.get("password")
        dbname = db_params.get("database_name", "corpstage")

        if not password or password == "CHANGE_IN_ENVIRONMENT":
            raise DatabaseInitializationError(
                "CRITICAL STARTUP FAILURE: Database password is unconfigured or carries default credentials. "
                "Ensure CORPSTAGE_DATABASE_PASSWORD is set in environment."
            )

        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}"

    @classmethod
    def create_engine(
        cls, 
        config_override: Optional[Dict[str, Any]] = None,
        use_pooling: bool = True
    ) -> AsyncEngine:
        """
        Builds and returns a database asynchronous engine.
        Implements intelligent connection pooling based on enterprise traffic parameters.
        """
        connection_url = cls.get_connection_url(config_override)

        # Retrieve configurations for connection pool
        pool_size = 30
        max_overflow = 10
        
        try:
            settings = SettingsManager.get_settings()
            pool_size = settings.database.postgresql.get("pool_size", 30)
            max_overflow = settings.database.postgresql.get("max_overflow", 10)
        except Exception:
            # Fall back to sensible enterprise baseline defaults if config manager is bypassed (e.g. in test scopes)
            pass

        engine_args: Dict[str, Any] = {
            "echo": False,  # Configurable in prod based on log levels
            "future": True  # Enforce SQLAlchemy 2.0 standards
        }

        if use_pooling:
            engine_args.update({
                "pool_size": pool_size,
                "max_overflow": max_overflow,
                "pool_recycle": 1800,       # Recycle connections older than 30 minutes
                "pool_pre_ping": True,      # Liveness checking (pings DB on checkout to verify liveness)
                "pool_timeout": 30          # Fail-fast timeout for checkout queues
            })
            logger.info(f"Instantiating pooled database engine with pool_size={pool_size}, max_overflow={max_overflow}")
        else:
            engine_args["pool"]class_ = NullPool
            logger.info("Instantiating database engine with connection pooling disabled (NullPool).")

        try:
            return create_async_engine(connection_url, **engine_args)
        except Exception as ex:
            raise DatabaseInitializationError(f"Engine connection string formulation rejected: {str(ex)}")

    @classmethod
    def get_shared_engine(cls) -> AsyncEngine:
        """
        Retrieves or instantiates a singleton AsyncEngine for standard reuse across the microservice.
        """
        if cls._engine is None:
            cls._engine = cls.create_engine()
        return cls._engine

    @classmethod
    async def dispose_shared_engine(cls) -> None:
        """
        Releases all connections allocated within the engine pool gracefully.
        Call this during application graceful server shutdown.
        """
        if cls._engine:
            logger.info("Closing all connection pools in the global database engine...")
            await cls._engine.dispose()
            cls._engine = None
            logger.info("Database engine gracefully disposed.")
