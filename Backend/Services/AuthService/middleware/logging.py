import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response

from observability import CorrelationContext, record_metric

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Performance and tracing middleware.
    Instruments request durations and registers correlated diagnostic metadata.

    WP-00: every request is now assigned a correlation ID (reused from the
    inbound X-Correlation-ID header if the caller supplied one, so a
    request can be traced across services, per the Aurex Platform
    Administrator Roadmap's Observability Framework: "one distributed
    trace per login request, spanning API -> AuthService -> DB"). The ID
    is bound to observability.CorrelationContext so bootstrap_service.py's
    audit/event/metric emissions (and any future Business Activity's) are
    automatically correlated to the request that triggered them, without
    every caller having to thread it through explicitly.
    """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        correlation_id = request.headers.get("X-Correlation-ID") or CorrelationContext.new()
        CorrelationContext.set(correlation_id)

        start_time = time.perf_counter()

        method = request.method
        path = request.url.path

        response = await call_next(request)

        duration = time.perf_counter() - start_time
        logger.info(
            f"HTTP {method} {path} - Status: {response.status_code} - "
            f"Done in {duration:.4f}s - Correlation-ID: {correlation_id}"
        )
        record_metric(
            "http.request.duration_seconds",
            duration,
            tags={"method": method, "path": path, "status": str(response.status_code)},
        )

        response.headers["X-Process-Time"] = f"{duration:.4f}"
        response.headers["X-Correlation-ID"] = correlation_id
        return response
