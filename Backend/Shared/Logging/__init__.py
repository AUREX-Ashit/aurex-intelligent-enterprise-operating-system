"""
CorpStage Shared Logging & Telemetry Framework.

An enterprise-ready, structured JSON-logging, security-auditable, and task-local
context-propagating logging framework built on OpenTelemetry-ready design principles.
"""

from corpstage.backend.shared.logging.exceptions import (
    LoggingError,
    LoggingConfigurationError,
    ContextPropagationError,
)
from corpstage.backend.shared.logging.correlation_context import (
    CorrelationContext,
)
from corpstage.backend.shared.logging.log_formatter import (
    JSONLogFormatter,
)
from corpstage.backend.shared.logging.logger_factory import (
    LoggerFactory,
)
from corpstage.backend.shared.logging.request_logger import (
    RequestTracingMiddleware,
)
from corpstage.backend.shared.logging.audit_logger import (
    AuditLogger,
    AuditStatus,
)
from corpstage.backend.shared.logging.performance_logger import (
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
