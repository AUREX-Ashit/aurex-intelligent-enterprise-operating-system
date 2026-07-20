"""
CorpStage Shared Logging Framework - Performance Logger Module.

Provides precise runtime execution timing instrumentation via Context Managers,
synchronous/asynchronous Function Decorators, and direct performance logger APIs.
"""

import time
import functools
import inspect
from typing import Any, Dict, Callable, Optional, TypeVar, cast
from types import TracebackType

from corpstage.backend.shared.logging.logger_factory import LoggerFactory

logger = LoggerFactory.get_logger("cs.telemetry.performance")

F = TypeVar("F", bound=Callable[..., Any])


class PerformanceTimer:
    """
    Context Manager allowing high-precision timing measurements of structured logical blocks.
    
    Usage:
        with PerformanceTimer("fetch_tenant_metadata", extra={"tenant_id": "cust_123"}):
            await database.query(...)
    """

    def __init__(self, operation_name: str, extra: Optional[Dict[str, Any]] = None) -> None:
        self.operation_name = operation_name
        self.extra = extra or {}
        self.start_time: float = 0.0

    def __enter__(self) -> "PerformanceTimer":
        self.start_time = time.perf_counter()
        logger.debug(
            f"Starting operation '{self.operation_name}'",
            extra={"operation": self.operation_name, "stage": "start", **self.extra}
        )
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[TracebackType]) -> None:
        elapsed = time.perf_counter() - self.start_time
        duration_ms = round(elapsed * 1000, 3)
        
        status = "success" if exc_type is None else "failure"
        log_payload = {
            "operation": self.operation_name,
            "stage": "complete",
            "duration_ms": duration_ms,
            "status": status,
            **self.extra
        }

        if exc_type is not None:
            log_payload["error_class"] = exc_type.__name__
            logger.error(
                f"Operation '{self.operation_name}' failed after {duration_ms}ms: {str(exc_val)}",
                extra=log_payload,
                exc_info=True
            )
        else:
            logger.info(
                f"Operation '{self.operation_name}' completed in {duration_ms}ms [{status.upper()}]",
                extra=log_payload
            )


def measure_performance(operation_name: Optional[str] = None, extra: Optional[Dict[str, Any]] = None) -> Callable[[F], F]:
    """
    Modern performance measuring decorator that transparently instruments
    both synchronous and asynchronous methods.
    
    Usage:
        @measure_performance("retrieve_ai_inference")
        async def query_model(...):
            ...
    """
    def decorator(func: F) -> F:
        op_name = operation_name or func.__name__
        func_extra = extra or {}

        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                start = time.perf_counter()
                logger.debug(
                    f"Invoking async method {func.__name__}",
                    extra={"decorator": "measure_performance", "function": func.__name__, "stage": "start", **func_extra}
                )
                try:
                    result = await func(*args, **kwargs)
                    duration_ms = round((time.perf_counter() - start) * 1000, 3)
                    logger.info(
                        f"Async method {func.__name__} completed in {duration_ms}ms",
                        extra={
                            "decorator": "measure_performance",
                            "function": func.__name__,
                            "duration_ms": duration_ms,
                            "status": "success",
                            **func_extra
                        }
                    )
                    return result
                except Exception as e:
                    duration_ms = round((time.perf_counter() - start) * 1000, 3)
                    logger.error(
                        f"Async method {func.__name__} raised exception after {duration_ms}ms: {str(e)}",
                        extra={
                            "decorator": "measure_performance",
                            "function": func.__name__,
                            "duration_ms": duration_ms,
                            "status": "failure",
                            "error": e.__class__.__name__,
                            **func_extra
                        },
                        exc_info=True
                    )
                    raise
            return cast(F, async_wrapper)
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                start = time.perf_counter()
                logger.debug(
                    f"Invoking sync method {func.__name__}",
                    extra={"decorator": "measure_performance", "function": func.__name__, "stage": "start", **func_extra}
                )
                try:
                    result = func(*args, **kwargs)
                    duration_ms = round((time.perf_counter() - start) * 1000, 3)
                    logger.info(
                        f"Sync method {func.__name__} completed in {duration_ms}ms",
                        extra={
                            "decorator": "measure_performance",
                            "function": func.__name__,
                            "duration_ms": duration_ms,
                            "status": "success",
                            **func_extra
                        }
                    )
                    return result
                except Exception as e:
                    duration_ms = round((time.perf_counter() - start) * 1000, 3)
                    logger.error(
                        f"Sync method {func.__name__} raised exception after {duration_ms}ms: {str(e)}",
                        extra={
                            "decorator": "measure_performance",
                            "function": func.__name__,
                            "duration_ms": duration_ms,
                            "status": "failure",
                            "error": e.__class__.__name__,
                            **func_extra
                        },
                        exc_info=True
                    )
                    raise
            return cast(F, sync_wrapper)

    return decorator


class PerformanceLogger:
    """
    Unified performance reporting endpoint API for manual timing and performance reports.
    """

    @classmethod
    def log_timing(cls, operation: str, duration_ms: float, status: str = "success", extra: Optional[Dict[str, Any]] = None) -> None:
        """Manually records timing metric with complete trace variables."""
        payload = {
            "operation": operation,
            "duration_ms": round(duration_ms, 3),
            "status": status,
            **(extra or {})
        }
        logger.info(
            f"Performance Metric recorded: {operation} took {duration_ms}ms [{status.upper()}]",
            extra=payload
        )
