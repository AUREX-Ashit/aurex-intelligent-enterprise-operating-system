"""
Aurex Shared Logging Framework - Request-Tracing Middleware Module.

Implements high-fidelity request tracking, context propagation, and correlation injection
via a full-featured FastAPI / Starlette compliance middleware pipeline.
"""

import time
import uuid
from typing import Any, Callable, Optional, Awaitable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from aurex.backend.shared.logging.logger_factory import LoggerFactory
from aurex.backend.shared.logging.correlation_context import CorrelationContext

logger = LoggerFactory.get_logger("cs.telemetry.requests")


class RequestTracingMiddleware(BaseHTTPMiddleware):
    """
    Standard HTTP Request interceptor utilizing ASGI specifications.
    Extracts, generates, attaches, propagates, and teardown-clears task-local contexts.
    """

    def __init__(
        self,
        app: Any = None,
        tenant_header: str = "X-Tenant-ID",
        correlation_header: str = "X-Correlation-ID",
        user_header: str = "X-User-ID",
        log_health_checks: bool = False,
    ) -> None:
        super().__init__(app)
        self.tenant_header = tenant_header
        self.correlation_header = correlation_header
        self.user_header = user_header
        self.log_health_checks = log_health_checks

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """
        Main intercept-handling logic, timing execution and tracing boundaries.
        """
        # Determine if current request points to health probe endpoints
        is_health_check = request.url.path in ["/api/health", "/health", "/metrics", "/healthz", "/docs", "/openapi.json"]
        should_log = self.log_health_checks or not is_health_check

        # Step 1: Extract telemetry keys from inbound headers or create new ones
        correlation_id = request.headers.get(self.correlation_header) or str(uuid.uuid4())
        tenant_id = request.headers.get(self.tenant_header) or "SYSTEM_DEFAULT"
        user_id = request.headers.get(self.user_header) or "ANONYMOUS"

        # Also support OpenTelemetry-ready traces if injected in headers
        trace_id = request.headers.get("X-Trace-ID") or request.headers.get("tracestate") or None
        span_id = request.headers.get("X-Span-ID") or None

        # Step 2: Bind variables to local task context safely
        ctx_dict = {
            "correlation_id": correlation_id,
            "tenant_id": tenant_id,
            "user_id": user_id,
        }
        if trace_id:
            ctx_dict["trace_id"] = trace_id
        if span_id:
            ctx_dict["span_id"] = span_id

        tokens = CorrelationContext.set_context_from_dict(ctx_dict)

        # Log inbound request start
        if should_log:
            logger.info(
                f"Inbound HTTP request: {request.method} {request.url.path}",
                extra={
                    "stage": "inbound",
                    "http_method": request.method,
                    "url_path": request.url.path,
                    "query_params": dict(request.query_params),
                    "client_host": request.client.host if request.client else "0.0.0.0",
                }
            )

        start_time = time.perf_counter()

        # Step 3: Route transaction execution down downstream chains
        try:
            response = await call_next(request)
            duration_ms = round((time.perf_counter() - start_time) * 1000, 3)

            # Step 4: Inject tracing variables into client headers
            response.headers[self.correlation_header] = correlation_id
            response.headers[self.tenant_header] = tenant_id

            if should_log:
                # Decide logging tier based on response status category
                log_extra = {
                    "stage": "outbound",
                    "http_method": request.method,
                    "url_path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                }
                status_msg = f"Outbound HTTP response: {request.method} {request.url.path} -> {response.status_code} ({duration_ms}ms)"
                
                if response.status_code >= 500:
                    logger.error(status_msg, extra=log_extra)
                elif response.status_code >= 400:
                    logger.warning(status_msg, extra=log_extra)
                else:
                    logger.info(status_msg, extra=log_extra)

            return response

        except Exception as request_error:
            # Step 5: Catch uncaught downstream crashes to record error context before exiting thread scope variables
            duration_ms = round((time.perf_counter() - start_time) * 1000, 3)
            logger.error(
                f"Fatal Request Error: Unhandled crash inside route handler '{request.url.path}' after {duration_ms}ms: {str(request_error)}",
                extra={
                    "stage": "crash",
                    "http_method": request.method,
                    "url_path": request.url.path,
                    "duration_ms": duration_ms,
                    "exception_class": request_error.__class__.__name__
                },
                exc_info=True
            )
            raise request_error

        finally:
            # Step 6: Absolutely guarantee clearing of context vars on thread exit to prevent collision/leakages
            CorrelationContext.clear_context_from_tokens(tokens)
