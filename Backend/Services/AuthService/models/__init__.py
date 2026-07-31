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
from .delegation_policy import DelegationPolicy
from .runtime_assignment_policy import RuntimeAssignmentPolicy
from .organization_node import OrganizationNode
from .organization_establishment_attempt import OrganizationEstablishmentAttempt
from .person_distinction_decision import PersonDistinctionDecision
from .person_reconciliation_decision import PersonReconciliationDecision
from .person_correction import PersonCorrection
from .person_enrichment import PersonEnrichment
from .identity_recovery_request import IdentityRecoveryRequest

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
    "DelegationPolicy",
    "RuntimeAssignmentPolicy",
    "OrganizationNode",
    "OrganizationEstablishmentAttempt",
    "PersonDistinctionDecision",
    "PersonReconciliationDecision",
    "PersonCorrection",
    "PersonEnrichment",
    "IdentityRecoveryRequest",
]
