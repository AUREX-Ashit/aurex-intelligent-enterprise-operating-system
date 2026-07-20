# middleware/tenant.py
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from config.settings import settings

class TenantHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Exclude documentation, swagger and health checks from tenant check
        bypass_paths = ["/docs", "/openapi.json", "/redoc", "/ai/health"]
        if any(request.url.path.startswith(p) for p in bypass_paths) or request.url.path == "/":
            return await call_next(request)

        tenant_id = request.headers.get(settings.tenant_header_name)
        if not tenant_id:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Tenancy isolation error",
                    "reason": f"Mandatory tenant ID header '{settings.tenant_header_name}' is missing."
                }
            )
            
        # Store tenant ID on request state for retrieval down the line
        request.state.tenant_id = tenant_id
        
        response = await call_next(request)
        
        # Append isolated headers to output response
        response.headers["X-Tenant-Isolation-Verified"] = "True"
        response.headers[settings.tenant_header_name] = tenant_id
        
        return response
