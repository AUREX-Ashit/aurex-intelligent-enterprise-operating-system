import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Performance and tracing middleware.
    Instruments request durations and registers correlated diagnostic metadata.
    """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.perf_counter()
        
        # Capture trace logs
        method = request.method
        path = request.url.path
        
        response = await call_next(request)
        
        duration = time.perf_counter() - start_time
        logger.info(
            f"HTTP {method} {path} - Status: {response.status_code} - Done in {duration:.4f}s"
        )
        
        # Append correlation headers
        response.headers["X-Process-Time"] = f"{duration:.4f}"
        return response
