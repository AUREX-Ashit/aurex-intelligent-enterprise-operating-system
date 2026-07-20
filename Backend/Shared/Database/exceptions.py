"""
CorpStage Shared Database Framework - Exceptions Module.

Defines custom enterprise exception hierarchies for database operations,
connection life cycles, and multi-tenant security boundary checks.
"""

class DatabaseError(Exception):
    """Base exception for all CorpStage database operations."""
    pass


class DatabaseConnectionError(DatabaseError):
    """Raised when the connection to the database cannot be established or is interrupted."""
    pass


class DatabaseInitializationError(DatabaseError):
    """Raised when database configuration, engine setup, or initial validation checks fail."""
    pass


class TenantResolutionError(DatabaseError):
    """Raised when the multi-tenant context cannot be resolved or is missing for tenant-scoped operations."""
    pass


class TransactionError(DatabaseError):
    """Raised when errors occur during transaction boundary lifecycle (commit, rollback, nesting)."""
    pass


class MissingEntityError(DatabaseError):
    """Raised when a query or lookup fails due to missing crucial schema tables or entities."""
    pass
