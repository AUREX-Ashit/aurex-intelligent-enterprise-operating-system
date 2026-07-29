"""
Aurex Shared Security Framework - Security Context Module.

Provides asynchronous, asyncio task-local encapsulation of security context.
Ensures that user identities, roles, permissions, and tenant scope bindings are 
accessible securely and uniformly across all execution stages of a transaction, 
avoiding parameter pollution or thread-leak issues.
"""

import logging
from contextvars import ContextVar
from contextlib import contextmanager
from typing import Generator, Optional, Set, List, Dict, Any

from aurex.backend.shared.security.exceptions import SecurityContextError

logger = logging.getLogger("Aurex.Security.Context")


class SecurityPrincipal:
    """
    Represents an immutable authenticated security principal bound to the active context.
    """

    def __init__(
        self,
        user_id: str,
        username: str,
        tenant_id: str,
        roles: Set[str],
        permissions: Set[str],
        additional_claims: Optional[Dict[str, Any]] = None
    ):
        self.user_id = user_id
        self.username = username
        self.tenant_id = tenant_id
        self.roles = frozenset(roles)
        self.permissions = frozenset(permissions)
        self.additional_claims = additional_claims or {}

    def has_role(self, role: str) -> bool:
        """Checks if the principal is assigned a specific role."""
        return role in self.roles

    def has_permission(self, permission: str) -> bool:
        """Checks if the principal contains a specific permission."""
        return permission in self.permissions

    def belongs_to_tenant(self, tenant_id: str) -> bool:
        """Verifies if tenant bounds match context."""
        return self.tenant_id == tenant_id

    def to_dict(self) -> Dict[str, Any]:
        """Serializes current principal context for debugging or internal auditing."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "tenant_id": self.tenant_id,
            "roles": list(self.roles),
            "permissions": list(self.permissions)
        }

    def __repr__(self) -> str:
        return f"SecurityPrincipal(user_id={self.user_id}, tenant={self.tenant_id}, roles={list(self.roles)})"


# Thread/Task local isolated state using ContextVars
_security_principal_context_var: ContextVar[Optional[SecurityPrincipal]] = ContextVar(
    "aurex_security_principal", default=None
)


class SecurityContext:
    """
    Low-level coordinator of task-local security principal parameters.
    """

    @staticmethod
    def get_principal() -> Optional[SecurityPrincipal]:
        """Retrieves currently isolated SecurityPrincipal for the active async task context."""
        return _security_principal_context_var.get()

    @staticmethod
    def get_required_principal() -> SecurityPrincipal:
        """
        Retrieves principal context, throwing exception if requested in unauthenticated environment scope.
        """
        principal = _security_principal_context_var.get()
        if not principal:
            raise SecurityContextError(
                "Access Blocked: Security context is uninitialized. "
                "Ensure action is performed inside authenticated request context bounds."
            )
        return principal

    @staticmethod
    def set_principal(principal: SecurityPrincipal) -> None:
        """Explicitly registers a SecurityPrincipal context."""
        if not isinstance(principal, SecurityPrincipal):
            raise SecurityContextError("Context registration failed: must provide a SecurityPrincipal instance.")
        _security_principal_context_var.set(principal)
        logger.debug(f"Task-local security context assigned to User ID: [{principal.user_id}]")

    @staticmethod
    def clear() -> None:
        """Completely purges the security context to isolate tasks and prevent data bleed."""
        _security_principal_context_var.set(None)
        logger.debug("Task-local security context cleared.")

    @staticmethod
    def is_authenticated() -> bool:
        """Verifies if security principal has been registered in the context."""
        return _security_principal_context_var.get() is not None


@contextmanager
def bound_security_context(principal: SecurityPrincipal) -> Generator[None, None, None]:
    """
    Context manager allowing runtime execution blocks bound to a custom SecurityPrincipal context.
    Useful for thread context passing, queue consumers background jobs execution, or integration tests.
    """
    token = _security_principal_context_var.set(principal)
    try:
        yield
    finally:
        _security_principal_context_var.reset(token)
