from fastapi import Request, HTTPException, status
from fastapi.responses import JSONEncoder, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from config.settings import settings

class TenantIsolationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        # Exempt routes that form open API standards or health checkpoints
        exempt_paths = [
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json"
        ]
        
        if any(path.startswith(p) for p in exempt_paths):
            return await call_next(request)
            
        header_name = settings.auth.header_name
        tenant_id = request.headers.get(header_name)
        
        if not tenant_id:
            # Emit clear JSON structured response blocking execution
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Missing Tenant Header",
                    "message": f"Organization scope is missing. Please provide a valid '{header_name}' header in your request.",
                    "code": "MISSING_TENANT_CONTEXT"
                }
            )
            
        # Basic validation: ensure tenant ID is non-empty and has reasonable length
        if len(tenant_id.strip()) < 3:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Invalid Tenant Header",
                    "message": f"Tenant identifier '{tenant_id}' is malformed or invalid.",
                    "code": "INVALID_TENANT_CONTEXT"
                }
            )
            
        # Attach tenant ID to request state for standard global lookup in repositories and routers
        request.state.tenant_id = tenant_id.strip()
        
        # Proceed with request pipeline
        response = await call_next(request)
        
        # Append Tenant ID response header for platform tracing confirmation
        response.headers[f"X-Processed-Client-{header_name}"] = tenant_id
        return response
