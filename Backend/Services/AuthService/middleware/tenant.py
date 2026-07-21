import uuid
from contextvars import ContextVar
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse

# Context variable to hold tenant ID throughout the current coroutine context
tenant_context: ContextVar[uuid.UUID | None] = ContextVar("tenant_context", default=None)

class TenantMiddleware(BaseHTTPMiddleware):
    """
    HTTP Middleware tasked with multi-tenant extraction.
    Interceptors ensure callers provide valid UUID X-Tenant-ID headers.
    """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Skip tenant checks for standard auth-agnostic paths (e.g. docs, openapi, health).
        # /person/recognize and /person/establish are tenant-agnostic on the same basis as
        # /auth/login: Person is independent of any company, role, license, or permission
        # (URA-001-15), and neither EX-C006-01 nor EX-C006-02 states an Organization/tenant
        # context requirement.
        # /ready (WP-00) is platform-scoped, not tenant-scoped, on the same basis as
        # /health: an orchestrator's readiness probe has no tenant context to supply.
        # /organizations and /organizations/{id} (WP-01, BA-01 Establish / BA-02 View)
        # are tenant-agnostic for the same reason as /person/establish: the
        # PLATFORM_ADMIN role these endpoints require (dependencies.require_platform_admin)
        # operates across every organization boundary, so there is no single tenant
        # to scope the request to. Prefix-matched (not exact-listed) because BA-02
        # introduced a path parameter (/organizations/{organization_id}); every future
        # WP-01 Business Activity's endpoint lives under this same prefix and is
        # covered by the same rationale, so it is not re-added per activity.
        path = request.url.path
        if path in [
            "/health", "/ready", "/docs", "/redoc", "/openapi.json",
            "/auth/login", "/auth/refresh",
            "/person/recognize", "/person/establish",
        ] or path == "/organizations" or path.startswith("/organizations/"):
            return await call_next(request)

        tenant_header = request.headers.get("X-Tenant-ID")

        if not tenant_header:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Header 'X-Tenant-ID' is required to route requests."}
            )

        try:
            tenant_uuid = uuid.UUID(tenant_header)
        except ValueError:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Header 'X-Tenant-ID' must be a valid RFC 4122 UUID."}
            )

        # Set Context Variable for SQLAlchemy automatic filters or logs
        token = tenant_context.set(tenant_uuid)
        request.state.tenant_id = tenant_uuid

        try:
            response = await call_next(request)
        finally:
            tenant_context.reset(token)

        return response


def get_current_tenant() -> uuid.UUID:
    """
    FastAPI dependency injector to obtain active tenant_id context.
    """
    tenant_id = tenant_context.get()
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Active tenant context is unresolved."
        )
    return tenant_id
