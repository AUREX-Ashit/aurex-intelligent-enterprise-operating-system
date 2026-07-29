"""
Aurex Shared Telemetry - Logger Factory.

Configures python logging infrastructures across tenant boundaries, establishing
standard handlers, dynamic filters, levels, and JSON formatters.
"""

import sys
import logging
from typing import Dict, Any, Optional

from aurex.backend.shared.logging.log_formatter import JSONLogFormatter
from aurex.backend.shared.logging.exceptions import LoggingConfigurationError

_global_service_name: Optional[str] = None
_configured_loggers: Dict[str, logging.Logger] = {}


class LoggerFactory:
    """
    Central control hub for standard, secure, tenant-scoped stream loggers.
    Ensures absolute alignment with OpenTelemetry conventions.
    """

    @classmethod
    def initialize(cls, service_name: str, default_level: str = "INFO") -> None:
        """
        Configures global log pipelines, binding appropriate service contexts.
        Must run exactly once at microservice ingress/bootstrap.
        """
        global _global_service_name
        
        if not service_name:
            raise LoggingConfigurationError("Logging initialization requires a non-empty service_name.")

        _global_service_name = service_name
        numeric_level = getattr(logging, default_level.upper(), logging.INFO)

        # Clear existing default handlers out of global root logger to ensure clean output streams
        root_logger = logging.getLogger()
        for handler in list(root_logger.handlers):
            root_logger.removeHandler(handler)

        # Build clean console standard outbound stream
        console_handler = logging.StreamHandler(sys.stdout)
        
        # Build standard structured formatter
        formatter = JSONLogFormatter(service_name=service_name)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(numeric_level)
        
        # Apply structured formatter globally
        root_logger.setLevel(numeric_level)
        root_logger.addHandler(console_handler)

        # Suppress noise from third party frameworks to prevent log spamming
        logging.getLogger("uvicorn.access").handlers = []
        logging.getLogger("uvicorn.error").handlers = []
        
        # Configure uvicorn loggers to route via our custom JSON logging formatter
        for uvicorn_logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"]:
            ulogger = logging.getLogger(uvicorn_logger_name)
            ulogger.propagate = True
            ulogger.setLevel(numeric_level)

        root_logger.info(
            f"Aurex Structured Logger initialized successfully for service: '{service_name}' [Level: {default_level}]"
        )

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Acquires named logging proxy bound with standard JSON filters.
        Automatically guarantees safe fallback initialization if called prematurely.
        """
        global _global_service_name
        
        if name in _configured_loggers:
            return _configured_loggers[name]

        # Fail-safe initialization to default "AurexService" to avoid crashes
        if _global_service_name is None:
            cls.initialize(service_name="AurexService", default_level="INFO")

        logger = logging.getLogger(name)
        # Prevent double handling if parent logger is configured
        _configured_loggers[name] = logger
        return logger
