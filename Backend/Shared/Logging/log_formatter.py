"""
CorpStage Shared Logging Framework - Structured JSON Log Formatter.

Implements highly-performant, failure-resilient JSON serialization for standard
Python `logging.LogRecord` structures, enriching them with active thread/task contexts.
"""

import json
import logging
import datetime
import traceback
from typing import Any, Dict, Set

from corpstage.backend.shared.logging.correlation_context import CorrelationContext


class JSONLogFormatter(logging.Formatter):
    """
    Standardized formatting layout converting logging records to structured JSON strings.
    Auto-injects tenant, user, trace and correlation credentials from task-local scopes.
    """

    # Filter keys to omit standard logging variables from custom parameter collection
    STANDARD_RECORD_FIELDS: Set[str] = {
        "args", "asctime", "created", "exc_info", "exc_text", "filename", "funcName",
        "levelname", "levelno", "lineno", "module", "msecs", "message", "msg",
        "name", "pathname", "process", "processName", "relativeCreated", "stack_info",
        "thread", "threadName"
    }

    def __init__(self, service_name: str, **kwargs: Any) -> None:
        """
        Initializes formatter bound to specific client microservice identifier.
        """
        super().__init__(**kwargs)
        self.service_name = service_name

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats LogRecord to standard structured enterprise JSON string.
        """
        # Capture raw exception state safe serialization
        exc_data = None
        if record.exc_info:
            exc_data = "".join(traceback.format_exception(*record.exc_info))
        elif record.exc_text:
            exc_data = record.exc_text

        # Base structural logging contract
        payload: Dict[str, Any] = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "level": record.levelname,
            "service_name": self.service_name,
            "logger_name": record.name,
            "message": record.getMessage(),
            "duration_ms": getattr(record, "duration_ms", None),
            "correlation_id": CorrelationContext.get_correlation_id(),
            "tenant_id": CorrelationContext.get_tenant_id(),
            "user_id": CorrelationContext.get_user_id(),
            "span_id": CorrelationContext.get_span_id(),
            "trace_id": CorrelationContext.get_trace_id(),
            "source_code": {
                "filepath": record.pathname,
                "line": record.lineno,
                "function": record.funcName
            }
        }

        # Include exception stack if present
        if exc_data:
            payload["exception"] = exc_data

        # Discover custom keys passed as `extra` to the log statement
        custom_params: Dict[str, Any] = {}
        for key, value in record.__dict__.items():
            if key not in self.STANDARD_RECORD_FIELDS and not key.startswith("_"):
                custom_params[key] = value

        if custom_params:
            payload["context"] = custom_params

        # Safe serialisation fallback routine to avoid crash on uncaught non-JSON types
        try:
            return json.dumps(payload, default=self._json_fallback)
        except Exception as serialize_error:
            # Emergency fallback when custom payload content violates strict JSON rules
            fallback_payload = {
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "level": "ERROR",
                "service_name": self.service_name,
                "logger_name": "JSONLogFormatter",
                "message": f"SerializationFailure: Failed to format original log: {str(serialize_error)}",
                "original_log_message_fallback": str(record.msg)
            }
            return json.dumps(fallback_payload)

    def _json_fallback(self, obj: Any) -> Any:
        """Fallback JSON encoder serializer helper for objects not natively serializable."""
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, Exception):
            return str(obj)
        try:
            return str(obj)
        except Exception:
            return "<UNSERIALIZABLE OBJECT>"
