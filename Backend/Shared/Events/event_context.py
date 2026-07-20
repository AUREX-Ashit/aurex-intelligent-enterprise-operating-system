"""
CorpStage Shared Events Framework - Event Context Module.

Bridges distributed-tracing correlation context with event telemetry.
Allows capturing, storing, and loading context variables safely during event execution.
"""

from contextvars import ContextVar, Token
from typing import Dict, Any, Optional

# Shared contextual attributes for Event Trace propagation
_EVENT_CORRELATION_ID: ContextVar[Optional[str]] = ContextVar("event_correlation_id", default=None)
_EVENT_TENANT_ID: ContextVar[Optional[str]] = ContextVar("event_tenant_id", default=None)
_EVENT_USER_ID: ContextVar[Optional[str]] = ContextVar("event_user_id", default=None)


class EventContext:
    """
    Manages task-local execution and dispatch boundaries for events.
    Enforces trace and tenant isolation during async processing.
    """

    @classmethod
    def get_correlation_id(cls) -> Optional[str]:
        """Fetch active event correlation context."""
        return _EVENT_CORRELATION_ID.get()

    @classmethod
    def set_correlation_id(cls, correlation_id: str) -> Token[Optional[str]]:
        """Bind dynamic event correlation ID."""
        return _EVENT_CORRELATION_ID.set(correlation_id)

    @classmethod
    def clear_correlation_id(cls, token: Token[Optional[str]]) -> None:
        """Undo previous correlation assignment."""
        _EVENT_CORRELATION_ID.reset(token)

    @classmethod
    def get_tenant_id(cls) -> Optional[str]:
        """Fetch current tenant identifier bound to this thread."""
        return _EVENT_TENANT_ID.get()

    @classmethod
    def set_tenant_id(cls, tenant_id: str) -> Token[Optional[str]]:
        """Bind tenant context strictly to current event pipeline."""
        return _EVENT_TENANT_ID.set(tenant_id)

    @classmethod
    def clear_tenant_id(cls, token: Token[Optional[str]]) -> None:
        """Release current tenant context binding."""
        _EVENT_TENANT_ID.reset(token)

    @classmethod
    def get_user_id(cls) -> Optional[str]:
        """Fetch current actor's user identifier."""
        return _EVENT_USER_ID.get()

    @classmethod
    def set_user_id(cls, user_id: str) -> Token[Optional[str]]:
        """Bind user identifier to task environment."""
        return _EVENT_USER_ID.set(user_id)

    @classmethod
    def clear_user_id(cls, token: Token[Optional[str]]) -> None:
        """Reset user identifier context boundary."""
        _EVENT_USER_ID.reset(token)

    @classmethod
    def export_context(cls) -> Dict[str, Any]:
        """
        Gathers active event context for envelope injection.
        Tries to import from Shared Logging CorrelationContext first if available.
        """
        # Try to hot-resolve from CorpStage Logging correlation context if it exists
        try:
            from corpstage.backend.shared.logging.correlation_context import CorrelationContext
            log_ctx = CorrelationContext.load_context_dict()
            return {
                "correlation_id": log_ctx.get("correlation_id") or cls.get_correlation_id(),
                "tenant_id": log_ctx.get("tenant_id") or cls.get_tenant_id(),
                "user_id": log_ctx.get("user_id") or cls.get_user_id()
            }
        except ImportError:
            return {
                "correlation_id": cls.get_correlation_id(),
                "tenant_id": cls.get_tenant_id(),
                "user_id": cls.get_user_id(),
            }

    @classmethod
    def set_context_from_dict(cls, context_dict: Dict[str, Any]) -> Dict[str, Token[Any]]:
        """
        Rehydrates background contexts from a serialized event snapshot.
        Enforces synchronized logs tracing inside event consumer daemon threads.
        """
        tokens = {}
        if context_dict.get("correlation_id"):
            tokens["correlation_id"] = _EVENT_CORRELATION_ID.set(context_dict["correlation_id"])
        if context_dict.get("tenant_id"):
            tokens["tenant_id"] = _EVENT_TENANT_ID.set(context_dict["tenant_id"])
        if context_dict.get("user_id"):
            tokens["user_id"] = _EVENT_USER_ID.set(context_dict["user_id"])
            
        # Re-inject to Logging context if possible
        try:
            from corpstage.backend.shared.logging.correlation_context import CorrelationContext
            CorrelationContext.set_context_from_dict(context_dict)
        except ImportError:
            pass
            
        return tokens

    @classmethod
    def clear_context_from_tokens(cls, tokens: Dict[str, Token[Any]]) -> None:
        """Restores context variables to prior values using provided tokens."""
        if "correlation_id" in tokens:
            _EVENT_CORRELATION_ID.reset(tokens["correlation_id"])
        if "tenant_id" in tokens:
            _EVENT_TENANT_ID.reset(tokens["tenant_id"])
        if "user_id" in tokens:
            _EVENT_USER_ID.reset(tokens["user_id"])
