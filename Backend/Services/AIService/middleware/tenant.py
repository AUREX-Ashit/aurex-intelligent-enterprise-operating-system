# middleware/tenant.py
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from config.settings import settings

class TenantHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Exclude documentation, swagger and health checks from tenant check.
        # "/search" (WP-11, IRA-011 §5), "/conversations" (WP-12, IRA-012 §5),
        # and "/knowledge-assets" (WP-14 BA-04, charter §6) are also excluded:
        # their own endpoints derive organization_id from a real, verified JWT
        # claim (dependencies.get_current_claims) — the raw, unverified
        # X-Tenant-ID header this middleware enforces elsewhere is superseded,
        # not required in addition, for these routes specifically.
        # Pre-existing endpoints (/ai/extract, /ai/validate, /ai/scoring) are
        # unaffected.
        bypass_paths = ["/docs", "/openapi.json", "/redoc", "/ai/health", "/search", "/conversations", "/knowledge-assets"]
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
