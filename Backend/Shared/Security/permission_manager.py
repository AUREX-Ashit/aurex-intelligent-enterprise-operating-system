"""
CorpStage Shared Security Framework - Permission Manager Module.

Provides granular permission-based authorization checks with advanced wildcard (*), 
part-matching, and resource-scoping support. Emplements fail-fast, immutable 
evaluation logic compatible with zero-trust API layers.
"""

import logging
from enum import Enum
from typing import Set, List, Union

logger = logging.getLogger("CorpStage.Security.PermissionManager")


class PlatformPermission(str, Enum):
    """
    Standard Enterprise Permission list governing actions across 
    CorpStage services (Auth, Tenant, Ingestion, AI, Reporting).
    """
    # Tenant Operations
    TENANT_CREATE = "tenant:create"
    TENANT_READ = "tenant:read"
    TENANT_UPDATE = "tenant:update"
    TENANT_DELETE = "tenant:delete"

    # Ingestion Boundaries
    INGEST_DATA = "ingest:data"
    INGEST_SCHEMA = "ingest:schema"
    INGEST_REDUNDANCY = "ingest:redundancy"

    # AI Service Tasks
    AI_QUERY = "ai:query"
    AI_TRAIN = "ai:train"
    AI_TUNE = "ai:tune"

    # Reporting and Audit
    REPORT_GENERATE = "report:generate"
    REPORT_EXPORT = "report:export"
    REPORT_DELETE = "report:delete"
    AUDIT_READ = "audit:read"


class PermissionManager:
    """
    Evaluates permissions with wildcard matching support.
    
    Examples:
    - User with permissions ["*"] has access to everything.
    - User with permissions ["tenant:*"] matches "tenant:create" and "tenant:read".
    - User with permissions ["report:generate", "report:export"] matches exact actions.
    """

    @staticmethod
    def is_permission_match(assigned_permission: str, requested_action: str) -> bool:
        """
        Determines if a single assigned permission string matches the requested action,
        fully accounting for wildcard boundaries.
        
        Args:
            assigned_permission: The permission assigned to the principal (e.g. 'tenant:*', 'tenant:read', '*')
            requested_action: The precise action being guarded (e.g. 'tenant:read')
        """
        if not assigned_permission or not requested_action:
            return False

        # Global system wildcard
        if assigned_permission == "*":
            return True

        if assigned_permission == requested_action:
            return True

        # Segment matching for patterns with wildcards (e.g., 'tenant:*')
        if "*" in assigned_permission:
            assigned_parts = assigned_permission.split(":")
            requested_parts = requested_action.split(":")

            # Ensure prefix-level length bounds are consistent
            if len(assigned_parts) > len(requested_parts):
                return False

            for idx, part in enumerate(assigned_parts):
                if part == "*":
                    # Wildcard matches everything at this position and downstream
                    return True
                if part != requested_parts[idx]:
                    return False

        return False

    @classmethod
    def check_permissions(cls, assigned_permissions: List[str], required_permission: str) -> bool:
        """
        Validates if the user's assigned permissions satisfy the required permission parameter.
        
        Args:
            assigned_permissions: List of permission tokens assigned to the principal
            required_permission: The permission string stringently required to perform the action
        """
        if not required_permission:
            return True

        for assigned in assigned_permissions:
            if cls.is_permission_match(assigned, required_permission):
                return True

        return False

    @classmethod
    def check_all_permissions(cls, assigned_permissions: List[str], required_permissions: List[str]) -> bool:
        """Validates if the principal has permissions matching EVERY string in the required list (Logical AND)."""
        if not required_permissions:
            return True
        return all(cls.check_permissions(assigned_permissions, req) for req in required_permissions)

    @classmethod
    def check_any_permission(cls, assigned_permissions: List[str], required_permissions: List[str]) -> bool:
        """Validates if the principal has permissions matching ANY string in the required list (Logical OR)."""
        if not required_permissions:
            return True
        return any(cls.check_permissions(assigned_permissions, req) for req in required_permissions)
