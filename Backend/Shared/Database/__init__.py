"""
Aurex Shared Database Framework

An Enterprise-grade asynchronous SQLAlchemy 2.0 multi-tenant database abstraction layer
enforcing row-level security context, transaction boundaries, connection pooling, and Alembic meta hooks.
"""

from aurex.backend.shared.database.exceptions import (
    DatabaseError,
    DatabaseConnectionError,
    DatabaseInitializationError,
    TenantResolutionError,
    TransactionError,
    MissingEntityError
)
from aurex.backend.shared.database.tenant_context import (
    TenantContext,
    tenant_context
)
from aurex.backend.shared.database.engine_factory import EngineFactory
from aurex.backend.shared.database.base_model import (
    Base,
    TenantScopedModel
)
from aurex.backend.shared.database.session_manager import (
    SessionManager,
    get_db_session
)
from aurex.backend.shared.database.database_manager import DatabaseManager
from aurex.backend.shared.database.migrations import MigrationHelper

__all__ = [
    "DatabaseManager",
    "EngineFactory",
    "SessionManager",
    "get_db_session",
    "Base",
    "TenantScopedModel",
    "TenantContext",
    "tenant_context",
    "MigrationHelper",
    "DatabaseError",
    "DatabaseConnectionError",
    "DatabaseInitializationError",
    "TenantResolutionError",
    "TransactionError",
    "MissingEntityError"
]
