"""
CorpStage Shared Database Framework - Tenant Context Module.

Provides asynchronous-safe task-local state isolation using ContextVars.
Secures tenant isolation boundaries for multi-tenant query filtration across
all microservices (AuthService, AIService, IngestionService, etc.).
"""

import logging
from contextvars import ContextVar
from contextlib import contextmanager
from typing import Generator, Optional

from corpstage.backend.shared.database.exceptions import TenantResolutionError

logger = logging.getLogger("CorpStage.Database.TenantContext")

# Async-safe task-local variable for tracking currently active Tenant Identity
_tenant_id_context_var: ContextVar[Optional[str]] = ContextVar("corpstage_tenant_id", default=None)


class TenantContext:
    """
    Utility class wrapper ensuring strict and isolated management of the
    thread/task-local tenant identifier.
    """

    @staticmethod
    def get_tenant_id() -> Optional[str]:
        """
        Retrieves the currently isolated tenant id for the active asynchronous task.
        """
        return _tenant_id_context_var.get()

    @staticmethod
    def set_tenant_id(tenant_id: str) -> None:
        """
        Explicitly enters a tenant boundary.
        
        Args:
            tenant_id: The unique identifier of the tenant.
        """
        if not tenant_id or not isinstance(tenant_id, str):
            raise TenantResolutionError("Tenant identifier must be a non-empty string.")
        
        _tenant_id_context_var.set(tenant_id)
        logger.debug(f"Task-local tenant context configured to: [{tenant_id}]")

    @staticmethod
    def clear_tenant_id() -> None:
        """
        Completely purges the active tenant boundary context to prevent data leaks or pollution.
        """
        _tenant_id_context_var.set(None)
        logger.debug("Task-local tenant context cleared.")

    @staticmethod
    def is_tenant_set() -> bool:
        """
        Checks if a tenant boundary has been configured.
        """
        return _tenant_id_context_var.get() is not None


@contextmanager
def tenant_context(tenant_id: str) -> Generator[None, None, None]:
    """
    Context manager allowing execution of context-bound database logic under a specific tenant identity.
    Automatically resets the tenant context upon exiting the scope.
    
    Example:
        with tenant_context("tenant_acme_corp"):
            # All queries made in this scope automatically apply tenant filters!
            result = await session.execute(select(Evidence))
    """
    token = _tenant_id_context_var.set(tenant_id)
    try:
        yield
    finally:
        _tenant_id_context_var.reset(token)
