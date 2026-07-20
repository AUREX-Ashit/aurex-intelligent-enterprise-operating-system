"""
CorpStage Shared Security Framework.

A unified, multi-service security delivery mechanism built for Enterprise-grade
resiliency, zero-trust token isolation, strict cryptographic password hashing,
hierarchical RBAC permission evaluation, and multi-tenant security verification.
"""

from corpstage.backend.shared.security.exceptions import (
    SecurityError,
    AuthenticationError,
    InvalidTokenError,
    TokenExpiredError,
    PasswordError,
    PasswordHashingError,
    WeakPasswordError,
    AuthorizationError,
    PermissionDeniedError,
    TenantAuthorizationError,
    SecurityContextError
)
from corpstage.backend.shared.security.security_context import (
    SecurityPrincipal,
    SecurityContext,
    bound_security_context
)
from corpstage.backend.shared.security.jwt_manager import JWTManager
from corpstage.backend.shared.security.password_manager import PasswordManager
from corpstage.backend.shared.security.role_manager import UserRole, RoleManager
from corpstage.backend.shared.security.permission_manager import PlatformPermission, PermissionManager
from corpstage.backend.shared.security.tenant_authorization import TenantAuthorization
from corpstage.backend.shared.security.authorization_manager import SecurityGuard, SecurityContextMiddleware

__all__ = [
    # Exceptions
    "SecurityError",
    "AuthenticationError",
    "InvalidTokenError",
    "TokenExpiredError",
    "PasswordError",
    "PasswordHashingError",
    "WeakPasswordError",
    "AuthorizationError",
    "PermissionDeniedError",
    "TenantAuthorizationError",
    "SecurityContextError",
    
    # Security Context
    "SecurityPrincipal",
    "SecurityContext",
    "bound_security_context",
    
    # JWT & Secrets
    "JWTManager",
    
    # Password Cryptography
    "PasswordManager",
    
    # RBAC Roles
    "UserRole",
    "RoleManager",
    
    # PBAC Permissions
    "PlatformPermission",
    "PermissionManager",
    
    # Tenant Isolation
    "TenantAuthorization",
    
    # FastAPI Guard / Injections
    "SecurityGuard",
    "SecurityContextMiddleware"
]
