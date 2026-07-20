import contextvars
import structlog
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from config.settings import settings

logger = structlog.get_logger()

# ContextVar to hold tenant context across async tasks safely
tenant_context: contextvars.ContextVar[str] = contextvars.ContextVar("tenant_id", default="")

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        header_name = settings.authentication.tenant.header_name
        tenant_id = request.headers.get(header_name)
        
        # Bypass for health check, docs, or schema validation
        if request.url.path in ["/health", "/docs", "/openapi.json", "/redoc"]:
            token = tenant_context.set("system_bypass")
            try:
                response = await call_next(request)
                return response
            finally:
                tenant_context.reset(token)

        if not tenant_id:
            # Let's check query params too as secondary fallback
            tenant_id = request.query_params.get("tenant_id")

        if not tenant_id:
            logger.warning("Missing required multi-tenant header", header_name=header_name, path=request.url.path)
            # For robustness we can raise a 400 or let the router fail
            # We'll raise 400 Bad Request to guarantee isolation
            raise HTTPException(
                status_code=400, 
                detail=f"CORP_STAGE_ERROR: Multi-tenant safety check failed. Missing header: '{header_name}'"
            )

        # Context isolation boundary setting
        token = tenant_context.set(tenant_id)
        
        # Bind tenant context to structured logging
        structlog.contextvars.bind_contextvars(tenant_id=tenant_id)
        
        try:
            logger.info("Routing tenant request", tenant_id=tenant_id, path=request.url.path)
            response = await call_next(request)
            
            # Echo back tenant context for validation
            response.headers[f"X-Routed-Tenant"] = tenant_id
            return response
        except Exception as e:
            logger.error("Error during tenant request processing", error=str(e), tenant_id=tenant_id)
            raise e
        finally:
            tenant_context.reset(token)
            structlog.contextvars.unbind_contextvars("tenant_id")

def get_current_tenant() -> str:
    """Safe helper to obtain current active tenant ID from async context"""
    return tenant_context.get()
