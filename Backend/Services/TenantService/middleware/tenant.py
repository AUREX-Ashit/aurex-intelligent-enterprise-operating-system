import contextvars
from typing import Optional
from uuid import UUID
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from config.settings import settings

# Thread-safe ContextVar to store current requested Tenant ID
_tenant_id_context: contextvars.ContextVar[Optional[UUID]] = contextvars.ContextVar(
    "tenant_id", default=None
)

def get_current_tenant_id() -> Optional[UUID]:
    """
    Retrieves the tenant ID from context, useful in services, repositories, and DB interceptors.
    """
    return _tenant_id_context.get()


class TenantHeaderMiddleware(BaseHTTPMiddleware):
    """
    FastAPI HTTP Middleware that extracts the X-Tenant-Id header,
    binds it contextually to contextvars, and ensures it's available down the call stack.
    """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        header_name = settings.authentication.tenant.header_name
        tenant_header = request.headers.get(header_name)
        
        tenant_id: Optional[UUID] = None
        if tenant_header:
            try:
                tenant_id = UUID(tenant_header)
            except ValueError:
                # Malformed header
                raise HTTPException(
                    status_code=400,
                    detail=f"Malformed header field {header_name}. Must be a valid UUID v4."
                )

        # Set context Token
        token = _tenant_id_context.set(tenant_id)
        
        try:
            response = await call_next(request)
            # Standardize safety: append resolved header to response
            if tenant_id:
                response.headers[f"X-Resolved-{header_name}"] = str(tenant_id)
            return response
        finally:
            # Clean context to prevent variable bleed
            _tenant_id_context.reset(token)
