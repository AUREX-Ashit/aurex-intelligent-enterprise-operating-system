"""
CorpStage Shared Security Framework - Tenant Authorization Module.

Maintains multi-tenant separation at the API boundary, validating individual 
principal scopes relative to requested resource tenants. Automatically synchronizes
verified states with the database TenantContext container.
"""

import logging
from typing import Optional

from corpstage.backend.shared.security.exceptions import TenantAuthorizationError
from corpstage.backend.shared.security.security_context import SecurityPrincipal, SecurityContext
from corpstage.backend.shared.security.role_manager import UserRole
# Circular-dependency resilient import or usage of database context
try:
    from corpstage.backend.shared.database.tenant_context import TenantContext
    _DB_TENANT_CONTEXT_AVAILABLE = True
except ImportError:
    _DB_TENANT_CONTEXT_AVAILABLE = False

logger = logging.getLogger("CorpStage.Security.TenantAuthorization")


class TenantAuthorization:
    """
    Coordinator validating active tenant cross-over attempts. Prevents cross-tenant
    information leakage by enforcing tenant-token matching.
    """

    @classmethod
    def authorize_tenant_access(cls, requested_tenant_id: str) -> None:
        """
        Validates if the active SecurityPrincipal is authorized to interact with
        the requested tenant ID space, and if valid, isolates the database layer.
        
        Rules:
        - SUPER_ADMIN: Can act on behalf of ANY tenant.
        - Other Roles: Must match the requested_tenant_id exactly.
        """
        if not requested_tenant_id:
            raise TenantAuthorizationError(
                "Tenant authorization failed: requested tenant identifier is empty or unsupplied."
            )

        principal = SecurityContext.get_required_principal()

        # Rule evaluation
        is_super_admin = principal.has_role(UserRole.SUPER_ADMIN.value)
        is_exact_match = principal.belongs_to_tenant(requested_tenant_id) if hasattr(principal, "belongs_to_tenant") else (principal.tenant_id == requested_tenant_id)

        if not is_super_admin and not is_exact_match:
            logger.critical(
                f"TENANT CROSS-OVER BOUNDARY BREACH DETECTED: User [{principal.user_id}] "
                f"representing tenant [{principal.tenant_id}] attempted to perform action "
                f"targeting tenant [{requested_tenant_id}]. Access Blocked."
            )
            raise TenantAuthorizationError(
                f"Access Denied: You are authenticated under tenant context '{principal.tenant_id}', "
                f"and are unauthorized to perform actions targeting tenant namespace '{requested_tenant_id}'."
            )

        # Synchronize database TenantContext layer if authorized
        if _DB_TENANT_CONTEXT_AVAILABLE:
            try:
                TenantContext.set_tenant_id(requested_tenant_id)
                logger.debug(
                    f"Successfully synchronized Database TenantContext context boundary to: [{requested_tenant_id}]"
                )
            except Exception as e:
                logger.error(
                    f"Failed to synchronize Database TenantContext context boundary to: [{requested_tenant_id}]. "
                    f"Error: {str(e)}"
                )

    @classmethod
    def get_authorized_tenant_or_fallback(cls, query_tenant_id: Optional[str] = None) -> str:
        """
        Calculates the authoritative tenant ID context, resolving overrides or defaulting to the
        user's native tenant ID container.
        """
        principal = SecurityContext.get_required_principal()
        is_super_admin = principal.has_role(UserRole.SUPER_ADMIN.value)

        if query_tenant_id:
            # If a specific tenant is requested, try to authorize it
            cls.authorize_tenant_access(query_tenant_id)
            return query_tenant_id
        else:
            # Fallback to the user's bound tenant
            tenant_id = principal.tenant_id
            if not tenant_id and not is_super_admin:
                raise TenantAuthorizationError(
                    "Account profile error: your profile is not linked to any tenant boundary."
                )
                
            # If SUPER_ADMIN doesn't request a tenant, they can act globally or we can use a system tenant
            resolved_tenant = tenant_id or "system_global"
            if _DB_TENANT_CONTEXT_AVAILABLE:
                TenantContext.set_tenant_id(resolved_tenant)
            return resolved_tenant
