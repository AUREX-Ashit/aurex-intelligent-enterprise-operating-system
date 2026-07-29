import json
import time
from datetime import datetime, timezone
import logging
import sys
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from middleware.tenant import get_current_tenant_id


# Setup structured console logger
logger = logging.getLogger("aurex_tenant_service")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    """
    HTTP middleware formatting request logs into production JSON blocks,
    capturing tenant routing, process latencies, HTTP paths, and status codes.
    """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.perf_counter()
        
        # Pull request properties
        client_host = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path
        query_params = dict(request.query_params)
        
        # Proceed with call stack
        response = None
        exception_thrown = None
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            exception_thrown = str(e)
            raise e
        finally:
            duration = time.perf_counter() - start_time
            tenant_id = get_current_tenant_id()
            status_code = response.status_code if response else 500
            
            # Format structured JSON output
            log_record = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "service": "TenantService",
                "environment": getattr(request.app.state, "env", "production"),
                "tenant_id": str(tenant_id) if tenant_id else None,
                "request": {
                    "method": method,
                    "path": path,
                    "query_params": query_params,
                    "client_ip": client_host
                },
                "response": {
                    "status_code": status_code,
                    "latency_ms": round(duration * 1000, 2)
                }
            }
            if exception_thrown:
                log_record["error"] = {
                    "message": exception_thrown,
                    "severity": "CRITICAL"
                }
                logger.error(json.dumps(log_record))
            else:
                logger.info(json.dumps(log_record))
