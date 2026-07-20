"""
CorpStage Shared Logging Framework - Exceptions Module.

Provides custom, strongly-typed enterprise exceptions for structured logging,
context propagation, and telemetry configuration boundaries.
"""

class LoggingError(Exception):
    """Base exception for all logging and telemetry-related errors in CorpStage."""
    pass


class LoggingConfigurationError(LoggingError):
    """Raised when the logging system configuration is invalid or missing required values."""
    pass


class ContextPropagationError(LoggingError):
    """Raised when correlation or tenant contexts fail to propagate across tasks, threads, or boundaries."""
    pass
