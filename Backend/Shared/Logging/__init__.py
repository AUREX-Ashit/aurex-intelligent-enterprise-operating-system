"""
Aurex Shared Logging & Telemetry Framework.

An enterprise-ready, structured JSON-logging, security-auditable, and task-local
context-propagating logging framework built on OpenTelemetry-ready design principles.
"""

from aurex.backend.shared.logging.exceptions import (
    LoggingError,
    LoggingConfigurationError,
    ContextPropagationError,
)
from aurex.backend.shared.logging.correlation_context import (
    CorrelationContext,
)
from aurex.backend.shared.logging.log_formatter import (
    JSONLogFormatter,
)
from aurex.backend.shared.logging.logger_factory import (
    LoggerFactory,
)
from aurex.backend.shared.logging.request_logger import (
    RequestTracingMiddleware,
)
from aurex.backend.shared.logging.audit_logger import (
    AuditLogger,
    AuditStatus,
)
from aurex.backend.shared.logging.performance_logger import (
    PerformanceLogger,
    PerformanceTimer,
    measure_performance,
)

__all__ = [
    # General Exceptions
    "LoggingError",
    "LoggingConfigurationError",
    "ContextPropagationError",
    
    # Core Context Manager
    "CorrelationContext",
    
    # Formatters & Factories
    "JSONLogFormatter",
    "LoggerFactory",
    
    # Request Tracing Middleware
    "RequestTracingMiddleware",
    
    # Compliance Auditing
    "AuditLogger",
    "AuditStatus",
    
    # Performance timing
    "PerformanceLogger",
    "PerformanceTimer",
    "measure_performance",
]
