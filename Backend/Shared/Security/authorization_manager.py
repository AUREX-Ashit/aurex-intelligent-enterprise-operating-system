"""
Aurex Shared Security Framework - Authorization Manager Module.

High-level security coordinator. Exposes elite FastAPI dependency injections (Guards)
governing RBAC, Permission arrays, and Tenant scope claims. Integrates with task-local
context registration.
"""

import logging
from typing import List, Optional, Union

# Supports FastAPI dependency constructs gracefully
try:
    from fastapi import Request, Depends, HTTPException, status
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    _FASTAPI_AVAILABLE = True
except ImportError:
    _FASTAPI_AVAILABLE = False

from aurex.backend.shared.security.exceptions import (
    AuthenticationError,
    InvalidTokenError,
    PermissionDeniedError,
    TenantAuthorizationError
)
from aurex.backend.shared.security.security_context import SecurityPrincipal, SecurityContext
from aurex.backend.shared.security.jwt_manager import JWTManager
from aurex.backend.shared.security.role_manager import RoleManager, UserRole
from aurex.backend.shared.security.permission_manager import PermissionManager
from aurex.backend.shared.security.tenant_authorization import TenantAuthorization

logger = logging.getLogger("Aurex.Security.AuthorizationManager")


class SecurityGuard:
    """
    Stateful FastAPI security dependency injector. Generates re-usable route guards
    restricting operations based on roles and/or permission qualifiers.
    
    Usage:
        @router.post("/queries")
        async def process_ai_query(
            principal: SecurityPrincipal = Depends(SecurityGuard(
                required_roles=["MEMBER"],
                required_permissions=["ai:query"]
            ))
        ):
            return {"status": "authorized"}
    """

    def __init__(
        self,
        required_roles: Optional[List[str]] = None,
        required_permissions: Optional[List[str]] = None,
        require_all_permissions: bool = True,
        enforce_tenant_header: bool = False
    ):
        self.required_roles = required_roles or []
        self.required_permissions = required_permissions or []
        self.require_all_permissions = require_all_permissions
        self.enforce_tenant_header = enforce_tenant_header

    def _extract_token(self, request: "Request") -> str:
        """Parses the Bearer token directly from the request headers."""
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise AuthenticationError("Authorization header is missing.")

        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise InvalidTokenError("Authorization header must follow standard 'Bearer <Token>' formatting.")

        return parts[1]

    async def __call__(self, request: "Request") -> SecurityPrincipal:
        """
        FastAPI dependency evaluator callable.
        Acts as the primary gatekeeper for requested route paths.
        """
        if not _FASTAPI_AVAILABLE:
            raise AuthenticationError(
                "CRITICAL SYSTEM ERROR: FastAPI dependencies invoked but FastAPI library is uninstalled."
            )

        try:
            # 1. Fetch token and decode claims
            token = self._extract_token(request)
            claims = JWTManager.decode_and_validate_token(token, expected_type="access")

            # 2. Assemble SecurityPrincipal element
            principal = SecurityPrincipal(
                user_id=claims.get("sub", ""),
                username=claims.get("username", claims.get("sub", "")),
                tenant_id=claims.get("tenant_id", ""),
                roles=set(claims.get("roles", [])),
                permissions=set(claims.get("permissions", [])),
                additional_claims=claims
            )

            # 3. Mount in Task-Local context
            SecurityContext.set_principal(principal)

            # 4. Tenant isolation authorization
            if self.enforce_tenant_header:
                tenant_header = request.headers.get("X-Tenant-ID")
                if tenant_header:
                    TenantAuthorization.authorize_tenant_access(tenant_header)
                else:
                    # Enforce context tenant
                    TenantAuthorization.authorize_tenant_access(principal.tenant_id)
            else:
                TenantAuthorization.authorize_tenant_access(principal.tenant_id)

            # 5. Role-based access checks (RBAC)
            if self.required_roles:
                has_role = RoleManager.has_any_role(list(principal.roles), self.required_roles)
                if not has_role:
                    raise PermissionDeniedError(
                        f"Access Denied: Principal lacks required roles {self.required_roles}."
                    )

            # 6. Granular permissions checks (PBAC)
            if self.required_permissions:
                if self.require_all_permissions:
                    has_perm = PermissionManager.check_all_permissions(
                        list(principal.permissions), 
                        self.required_permissions
                    )
                else:
                    has_perm = PermissionManager.check_any_permission(
                        list(principal.permissions), 
                        self.required_permissions
                    )

                if not has_perm:
                    raise PermissionDeniedError(
                        f"Access Denied: Principal lacks required functional permissions {self.required_permissions}."
                    )

            return principal

        # Standardize custom exception mappings to precise HTTP responses
        except AuthenticationError as ex:
            logger.error(f"SecurityGuard Authentication Error: {str(ex)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(ex),
                headers={"WWW-Authenticate": "Bearer"}
            )
        except InvalidTokenError as ex:
            logger.error(f"SecurityGuard Token Error: {str(ex)}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(ex),
                headers={"WWW-Authenticate": "Bearer error=\"invalid_token\""}
            )
        except PermissionDeniedError as ex:
            logger.critical(f"SecurityGuard Permission Error: {str(ex)}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(ex)
            )
        except TenantAuthorizationError as ex:
            logger.critical(f"SecurityGuard Tenant Security Exception: {str(ex)}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(ex)
            )
        except Exception as ex:
            logger.critical(f"SecurityGuard Uncaught Exception: {str(ex)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="A general security pipeline violation occurred processing claims."
            )


if _FASTAPI_AVAILABLE:
    # Middleware standardizing security state cleanup inside request/response loops
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.responses import Response

    class SecurityContextMiddleware(BaseHTTPMiddleware):
        """
        FastAPI custom middleware ensuring Task-Local security context is purged
        completely after every HTTP transaction loop to prevent leakage in shared threads.
        """
        async def dispatch(self, request: Request, call_next) -> Response:
            try:
                response = await call_next(request)
                return response
            finally:
                # Crucial task isolation purge
                SecurityContext.clear()
                # Clear Database tenant context if it was set
                try:
                    from aurex.backend.shared.database.tenant_context import TenantContext
                    TenantContext.clear_tenant_id()
                except ImportError:
                    pass
else:
    class SecurityContextMiddleware:
        """Mock context middleware if FastAPI is unavailable."""
        pass
