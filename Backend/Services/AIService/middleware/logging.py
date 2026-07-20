# middleware/logging.py
import json
import time
import sys
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        
        # Standard tracking details
        tenant_id = request.headers.get("X-Tenant-ID", "shared")
        path = request.url.path
        method = request.method
        
        try:
            response = await call_next(request)
            duration_ms = round((time.time() - start_time) * 1000, 2)
            
            structured_log = {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "level": "INFO",
                "message": f"HTTP {method} {path} processed in {duration_ms}ms",
                "metadata": {
                    "tenant_id": tenant_id,
                    "method": method,
                    "path": path,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms
                }
            }
            # Output matching structured config
            print(json.dumps(structured_log), file=sys.stdout, flush=True)
            return response
            
        except Exception as e:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            structured_log = {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "level": "ERROR",
                "message": f"Exception raised during request processing: {str(e)}",
                "metadata": {
                    "tenant_id": tenant_id,
                    "method": method,
                    "path": path,
                    "duration_ms": duration_ms,
                    "exception_type": type(e).__name__
                }
            }
            print(json.dumps(structured_log), file=sys.stderr, flush=True)
            raise e
