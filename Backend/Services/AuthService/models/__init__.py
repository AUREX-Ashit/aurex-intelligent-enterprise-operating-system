from .database import Base, db_manager

# Import all R-001 domain models so SQLAlchemy's mapper registry is populated
# at startup. Relationship string references ("Identity", "Membership", etc.)
# resolve only after each model module has been imported.
from .organization import Organization
from .person import Person
from .identity import Identity
from .role import Role
from .permission import Permission
from .role_permission import RolePermission
from .membership import Membership
from .refresh_token import RefreshToken
from .domain import Domain
from .domain_permission import DomainPermission
from .approval_authority import ApprovalAuthority

__all__ = [
    "Base",
    "db_manager",
    "Organization",
    "Person",
    "Identity",
    "Role",
    "Permission",
    "RolePermission",
    "Membership",
    "RefreshToken",
    "Domain",
    "DomainPermission",
    "ApprovalAuthority",
]
