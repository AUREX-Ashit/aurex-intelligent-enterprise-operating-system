import time
import uuid
import json
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from config.settings import settings

# Configure standard logger to write structured format
logger = logging.getLogger("aurex.ingestion")
logger.setLevel(logging.INFO if not settings.debug else logging.DEBUG)

# Basic Stream Handler if not configured
if not logger.handlers:
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(sh)

class CustomLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Prevent logging path noise for health probes if needed, but let's log everything structured
        start_time = time.perf_counter()
        
        # Pull tenant details if available from headers
        tenant_id = request.headers.get(settings.auth.header_name, "SYSTEM")
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        
        # Attach details to request state for use downstream
        request.state.correlation_id = correlation_id
        request.state.tenant_id = tenant_id
        
        response = None
        error = None
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            error = str(e)
            raise e
        finally:
            duration = (time.perf_counter() - start_time) * 1000  # ms
            status_code = response.status_code if response else 500
            
            # Formulate Structured Log dictionary
            log_payload = {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "level": "INFO" if not error else "ERROR",
                "service": "IngestionService",
                "environment": settings.environment,
                "correlation_id": correlation_id,
                "tenant_id": tenant_id,
                "request": {
                    "method": request.method,
                    "url": str(request.url),
                    "client_ip": request.client.host if request.client else "unknown"
                },
                "response": {
                    "status_code": status_code,
                    "latency_ms": round(duration, 2)
                }
            }
            if error:
                log_payload["error"] = error
            
            # Emit in JSON format conform to settings
            if settings.observability.logging.structured_json if hasattr(settings, "observability") else True:
                logger.info(json.dumps(log_payload))
            else:
                msg = f"[{log_payload['level']}] {request.method} {request.url} - {status_code} ({duration:.2f}ms)"
                if error:
                    msg += f" Error: {error}"
                logger.info(msg)
