"""
Aurex Shared Logging Framework - Correlation Context Module.

Manages task-local context variables (correlation IDs, tenant contexts,
user identifiers, and OpenTelemetry trace bounds) safely across synchronous
threads and asynchronous task schedulers using `contextvars`.
"""

from contextvars import ContextVar, Token
from typing import Dict, Any, Optional

# Context boundaries for Distributed Tracing and Context-Slicing
_CORRELATION_ID: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)
_TENANT_ID: ContextVar[Optional[str]] = ContextVar("tenant_id", default=None)
_USER_ID: ContextVar[Optional[str]] = ContextVar("user_id", default=None)
_TRACE_ID: ContextVar[Optional[str]] = ContextVar("trace_id", default=None)
_SPAN_ID: ContextVar[Optional[str]] = ContextVar("span_id", default=None)


class CorrelationContext:
    """
    Access controls and lifecycle managers for task-local telemetry states.
    Ensures safe retrieval, tokenized mutation, and restoration of context.
    """

    @classmethod
    def get_correlation_id(cls) -> Optional[str]:
        """Get the current correlation ID."""
        return _CORRELATION_ID.get()

    @classmethod
    def set_correlation_id(cls, correlation_id: str) -> Token[Optional[str]]:
        """Set the current correlation ID and return a token for restoration."""
        return _CORRELATION_ID.set(correlation_id)

    @classmethod
    def clear_correlation_id(cls, token: Token[Optional[str]]) -> None:
        """Restore the correlation ID setting prior to mutation."""
        _CORRELATION_ID.reset(token)

    @classmethod
    def get_tenant_id(cls) -> Optional[str]:
        """Get the bound Tenant context ID."""
        return _TENANT_ID.get()

    @classmethod
    def set_tenant_id(cls, tenant_id: str) -> Token[Optional[str]]:
        """Bind execution flow to a Tenant and return restoration token."""
        return _TENANT_ID.set(tenant_id)

    @classmethod
    def clear_tenant_id(cls, token: Token[Optional[str]]) -> None:
        """Unbind Tenant context back to previous context state."""
        _TENANT_ID.reset(token)

    @classmethod
    def get_user_id(cls) -> Optional[str]:
        """Get the authenticated principal's User ID."""
        return _USER_ID.get()

    @classmethod
    def set_user_id(cls, user_id: str) -> Token[Optional[str]]:
        """Bind current operations to specific User ID."""
        return _USER_ID.set(user_id)

    @classmethod
    def clear_user_id(cls, token: Token[Optional[str]]) -> None:
        """Reset the user ID context boundary."""
        _USER_ID.reset(token)

    @classmethod
    def get_trace_id(cls) -> Optional[str]:
        """Get the trace ID (congruent with OpenTelemetry spec)."""
        return _TRACE_ID.get()

    @classmethod
    def set_trace_id(cls, trace_id: str) -> Token[Optional[str]]:
        """Bind OpenTelemetry trace context."""
        return _TRACE_ID.set(trace_id)

    @classmethod
    def clear_trace_id(cls, token: Token[Optional[str]]) -> None:
        """Reset OpenTelemetry trace context."""
        _TRACE_ID.reset(token)

    @classmethod
    def get_span_id(cls) -> Optional[str]:
        """Get the active OpenTelemetry span ID."""
        return _SPAN_ID.get()

    @classmethod
    def set_span_id(cls, span_id: str) -> Token[Optional[str]]:
        """Set active OpenTelemetry span ID."""
        return _SPAN_ID.set(span_id)

    @classmethod
    def clear_span_id(cls, token: Token[Optional[str]]) -> None:
        """Reset OpenTelemetry span ID context."""
        _SPAN_ID.reset(token)

    @classmethod
    def load_context_dict(cls) -> Dict[str, Any]:
        """
        Extract the entire current context structure as a plain dictionary
        for serialization, RPC metadata headers, or logging injection points.
        """
        return {
            "correlation_id": _CORRELATION_ID.get(),
            "tenant_id": _TENANT_ID.get(),
            "user_id": _USER_ID.get(),
            "trace_id": _TRACE_ID.get(),
            "span_id": _SPAN_ID.get(),
        }

    @classmethod
    def set_context_from_dict(cls, context_dict: Dict[str, Any]) -> Dict[str, Token[Any]]:
        """
        Binds all contextual states present in the input dictionary.
        Returns a dictionary of reset tokens to restore environment safely.
        """
        tokens = {}
        if context_dict.get("correlation_id"):
            tokens["correlation_id"] = _CORRELATION_ID.set(context_dict["correlation_id"])
        if context_dict.get("tenant_id"):
            tokens["tenant_id"] = _TENANT_ID.set(context_dict["tenant_id"])
        if context_dict.get("user_id"):
            tokens["user_id"] = _USER_ID.set(context_dict["user_id"])
        if context_dict.get("trace_id"):
            tokens["trace_id"] = _TRACE_ID.set(context_dict["trace_id"])
        if context_dict.get("span_id"):
            tokens["span_id"] = _SPAN_ID.set(context_dict["span_id"])
        return tokens

    @classmethod
    def clear_context_from_tokens(cls, tokens: Dict[str, Token[Any]]) -> None:
        """Restores context variables to prior values using provided tokens."""
        if "correlation_id" in tokens:
            _CORRELATION_ID.reset(tokens["correlation_id"])
        if "tenant_id" in tokens:
            _TENANT_ID.reset(tokens["tenant_id"])
        if "user_id" in tokens:
            _USER_ID.reset(tokens["user_id"])
        if "trace_id" in tokens:
            _TRACE_ID.reset(tokens["trace_id"])
        if "span_id" in tokens:
            _SPAN_ID.reset(tokens["span_id"])
