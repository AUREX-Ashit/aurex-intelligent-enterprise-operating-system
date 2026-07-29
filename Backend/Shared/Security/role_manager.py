"""
Aurex Shared Security Framework - Role Manager Module.

Defines the roles matrix, structures, and hierarchical evaluations mapping to 
Role-Based Access Control (RBAC) schemas across standard Aurex microservices.
"""

import logging
from enum import Enum
from typing import Set, Dict, List, Optional

logger = logging.getLogger("Aurex.Security.RoleManager")


class UserRole(str, Enum):
    """
    Standard Enterprise System Roles supported in the Aurex Platform.
    Using flat string mappings for JSON and JWT serialization compatibility.
    """
    SUPER_ADMIN = "SUPER_ADMIN"       # Full platform access across all tenant contexts
    TENANT_ADMIN = "TENANT_ADMIN"     # Full control inside registered tenant bounds
    SEC_OPS = "SEC_OPS"               # Platform operations, security, policy updates
    AUDITOR = "AUDITOR"               # Read-only historical compliance reviews
    MEMBER = "MEMBER"                 # Standard operational team contributor
    GUEST = "GUEST"                   # Minimum access baseline / Read only shared links


# Unified Role Hierarchies Representation
# Higher roles inherently assume authorizations of children branches.
ROLE_HIERARCHY_TREE: Dict[UserRole, Set[UserRole]] = {
    UserRole.SUPER_ADMIN: {
        UserRole.SUPER_ADMIN,
        UserRole.TENANT_ADMIN,
        UserRole.SEC_OPS,
        UserRole.AUDITOR,
        UserRole.MEMBER,
        UserRole.GUEST
    },
    UserRole.TENANT_ADMIN: {
        UserRole.TENANT_ADMIN,
        UserRole.SEC_OPS,
        UserRole.MEMBER,
        UserRole.GUEST
    },
    UserRole.SEC_OPS: {
        UserRole.SEC_OPS,
        UserRole.MEMBER,
        UserRole.GUEST
    },
    UserRole.AUDITOR: {
        UserRole.AUDITOR,
        UserRole.GUEST
    },
    UserRole.MEMBER: {
        UserRole.MEMBER,
        UserRole.GUEST
    },
    UserRole.GUEST: {
        UserRole.GUEST
    }
}


class RoleManager:
    """
    Evaluator class for assessing principal role authorization structures 
    and resolving hierarchical access bounds.
    """

    @staticmethod
    def get_effective_roles(assigned_roles: List[str]) -> Set[str]:
        """
        Calculates the complete set of active and inherited role flags derived
        from a list of assigned roles.
        """
        effective: Set[str] = set()
        for role_str in assigned_roles:
            try:
                role_enum = UserRole(role_str)
                # Query child nodes from hierarchy tree
                family = ROLE_HIERARCHY_TREE.get(role_enum, {role_enum})
                for child in family:
                    effective.add(child.value)
            except ValueError:
                # Custom/unrecognized roles are appended as-is with no hierarchy expansion
                logger.warning(
                    f"Evaluating custom unmapped role token: [{role_str}]. "
                    f"No parent-child inheritance logic applied."
                )
                effective.add(role_str)
        return effective

    @staticmethod
    def is_authorized_role(assigned_roles: List[str], required_role: str) -> bool:
        """
        Validates if any of the assigned roles (or their hierarchical descendants) 
        match the required authorization role.
        """
        if not required_role:
            return True

        if not assigned_roles:
            return False

        effective_roles = RoleManager.get_effective_roles(assigned_roles)
        return required_role in effective_roles

    @staticmethod
    def has_any_role(assigned_roles: List[str], permissible_roles: List[str]) -> bool:
        """Checks if a user is assigned any role matching an acceptable set."""
        if not permissible_roles:
            return True

        effective_roles = RoleManager.get_effective_roles(assigned_roles)
        return any(req in effective_roles for req in permissible_roles)
