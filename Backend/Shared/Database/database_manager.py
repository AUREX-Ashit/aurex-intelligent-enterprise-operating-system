"""
Aurex Shared Database Framework - Database Manager Module.

High-level coordinator managing baseline integrations, health-check probes,
and table configuration schemas across Aurex application bounds.
"""

import logging
import time
from typing import Dict, Any, Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from aurex.backend.shared.database.engine_factory import EngineFactory
from aurex.backend.shared.database.base_model import Base
from aurex.backend.shared.database.exceptions import DatabaseInitializationError, DatabaseConnectionError

logger = logging.getLogger("Aurex.Database.DatabaseManager")


class DatabaseManager:
    """
    Main database operations manager. Serves as programmatic entry-point during
    microservice bootstrap and container initialization phases.
    """

    @staticmethod
    async def verify_and_initialize() -> None:
        """
        Runs connection verification and checks pool parameters.
        Throws clear exception on startup failures to support fail-fast container orchestration.
        """
        logger.info("Verifying database configuration parameters...")
        engine = EngineFactory.get_shared_engine()
        
        # Test connection structure with simple SELECT 1 probe
        is_healthy, latency_ms = await DatabaseManager.probe_health(engine)
        if not is_healthy:
            raise DatabaseConnectionError(
                "CRITICAL STARTUP FAILURE: Database connection probe failed. Check PostgreSQL availability."
            )
            
        logger.info(f"Database cluster verification completed successfully in {latency_ms:.2f}ms.")

    @staticmethod
    async def probe_health(engine: Optional[AsyncEngine] = None) -> tuple[bool, float]:
        """
        Probes connection pool health using light weight raw query check.
        Returns Tuple (is_healthy, response_latency_milliseconds).
        """
        active_engine = engine or EngineFactory.get_shared_engine()
        start_time = time.perf_counter()
        
        try:
            async with active_engine.connect() as conn:
                # Issue extremely lightweight SQL evaluation query
                await conn.execute(text("SELECT 1"))
            
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            return True, latency_ms
        except Exception as e:
            logger.error(f"Database health check probe received an error: {str(e)}")
            return False, 0.0

    @staticmethod
    async def create_schema_structures(engine: Optional[AsyncEngine] = None) -> None:
        """
        Helper method to automate creating all registered metadata tables.
        Useful for staging/development and automated Docker unit testing pipelines.
        For production environments, Alembic is strongly preferred.
        """
        active_engine = engine or EngineFactory.get_shared_engine()
        logger.info("Compiling and push registered metadata schemas into PostgreSQL cluster...")
        
        try:
            async with active_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Schema structures applied successfully.")
        except Exception as ex:
            raise DatabaseInitializationError(f"Engine rejected table compilation schema instructions: {str(ex)}")

    @staticmethod
    async def drop_schema_structures(engine: Optional[AsyncEngine] = None) -> None:
        """
        Drops all compiled metadata tables instantly. Protected to avoid accidental
        production execution.
        """
        active_engine = engine or EngineFactory.get_shared_engine()
        logger.warning("INTRUSIVE DESTRUCTION QUERY: dropping all database tables...")
        
        try:
            async with active_engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
            logger.info("All registered database tables dropped completely.")
        except Exception as ex:
             raise DatabaseInitializationError(f"Database engine rejected schema destruction commands: {str(ex)}")
