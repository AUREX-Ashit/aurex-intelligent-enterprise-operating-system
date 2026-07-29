"""
Aurex Shared Database Framework - Migrations Module.

Defines hooks and helper operations for Alembic database migrations.
Exposes uniform metadata interfaces for generating declarative schema files.
"""

import os
import logging
from typing import Dict, Any
from sqlalchemy import pool

from aurex.backend.shared.database.base_model import Base
from aurex.backend.shared.database.engine_factory import EngineFactory

logger = logging.getLogger("Aurex.Database.Migrations")


class MigrationHelper:
    """
    Acts as the bridge inside alembic/'env.py' deployment files.
    Allows declarative Alembic loaders to bind dynamically with SQLAlchemy metadata
    and environment configuration variables.
    """

    @staticmethod
    def get_target_metadata() -> Any:
        """
        Returns the collective enterprise database metadata standard.
        This represents the 'target_metadata' referenced inside Alembic migrations configurations.
        
        Example on Alembic env.py:
            # from aurex.backend.shared.database.migrations import MigrationHelper
            # target_metadata = MigrationHelper.get_target_metadata()
        """
        return Base.metadata

    @staticmethod
    def get_alembic_db_url() -> str:
        """
        Dynamically extracts and prepares the database endpoint URL specifically formatted
        for alembic run commands. Matches overrides and environment settings.
        
        Alembic often demands standard synchronous sync drivers like 'postgresql' or 'postgresql+psycopg2'
        for generating/running migrations, while code uses asynchronous 'postgresql+asyncpg'.
        This method gracefully maps variables to match.
        """
        try:
            # First, fetch standard async url
            url = EngineFactory.get_connection_url()
            # Parse async representation into sync equivalent for standard Alembic sync operations if needed
            if "postgresql+asyncpg://" in url:
                sync_url = url.replace("postgresql+asyncpg://", "postgresql://")
                return sync_url
            return url
        except Exception as ex:
            logger.warning(
                f"Shared Config uninitialized during Alembic phase. "
                f"Attempting environment direct lookup. Error: {str(ex)}"
            )
            
            # Fallback directly to raw environment or standard local dev address
            db_port = os.getenv("AUREX__DATABASE__POSTGRESQL__PORT", "5432")
            db_pw = os.getenv("AUREX_DATABASE_PASSWORD", "aurex")
            db_user = os.getenv("AUREX__DATABASE__POSTGRESQL__USERNAME", "aurex")
            db_host = os.getenv("AUREX__DATABASE__POSTGRESQL__HOST", "localhost")
            db_name = os.getenv("AUREX__DATABASE__POSTGRESQL__DATABASE_NAME", "aurex")
            
            return f"postgresql://{db_user}:{db_pw}@{db_host}:{db_port}/{db_name}"

    @staticmethod
    def get_engine_configuration() -> Dict[str, Any]:
        """
        Formulates configurations required to configure migration engines.
        """
        return {
            "url": MigrationHelper.get_alembic_db_url(),
            "poolclass": pool.NullPool,  # Migrations should not hoard persistent connection pools
            "future": True
        }
