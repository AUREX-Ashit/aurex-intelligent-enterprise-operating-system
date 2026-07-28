"""
WP-02 BA-08 — Deprecate or Retire Authorization Policy Object
(ERB-C003-02 / EX-C003-08). Service-layer tests, one class per
authorization policy object type, covering the shared BR-C003-04
guarantee (no active dependency remains unresolved; never a hard
delete) and Role's own real dependency check (the only one of the five
types with an AuthService-implemented dependent table today).
"""
import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.domain import Domain
from models.membership import Membership
from models.organization import Organization
from models.person import Person
from models.role import Role, VersionStatus as RoleVersionStatus
from repositories.approval_authority_repository import ApprovalAuthorityRepository
from repositories.delegation_policy_repository import DelegationPolicyRepository
from repositories.domain_permission_repository import DomainPermissionRepository
from repositories.domain_repository import DomainRepository
from repositories.membership_repository import MembershipRepository
from repositories.organization_repository import OrganizationRepository
from repositories.role_repository import RoleRepository
from repositories.runtime_assignment_policy_repository import RuntimeAssignmentPolicyRepository
from schemas.approval_authority import EstablishApprovalAuthorityRequest
from schemas.delegation_policy import EstablishDelegationPolicyRequest
from schemas.domain_permission import EstablishDomainPermissionRequest
from schemas.role import EstablishRoleRequest, VersionRoleRequest
from schemas.runtime_assignment_policy import EstablishRuntimeAssignmentPolicyRequest
from services.approval_authority_service import ApprovalAuthorityService
from services.delegation_policy_service import DelegationPolicyService
from services.domain_permission_service import DomainPermissionService
from services.role_service import RoleService
from services.runtime_assignment_policy_service import RuntimeAssignmentPolicyService


# --- Role -------------------------------------------------------------


async def test_role_retire_succeeds_when_no_active_membership(db_session: AsyncSession) -> None:
    service = RoleService(RoleRepository(db_session))
    role = await service.establish(EstablishRoleRequest(role_code="BA08_ROLE_1", role_name="V1"))

    retired = await service.retire(role.id, actor_id="platform-admin-1")

    assert retired.status == RoleVersionStatus.RETIRED.value
    assert retired.effective_to is not None
    assert retired.role_name == "V1"


async def test_role_deprecate_rejects_role_with_active_membership(db_session: AsyncSession) -> None:
    person = Person(first_name="BA08", last_name="Dep", display_name="BA08 Dep")
    organization = Organization(organization_code="BA08-ROLE-ORG", organization_name="BA-08 Role Org", organization_type="CORPORATE")
    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.establish(EstablishRoleRequest(role_code="BA08_ROLE_2", role_name="V1"))

    db_session.add_all([person, organization])
    await db_session.flush()
    membership = Membership(person_id=person.id, organization_id=organization.id, role_id=role.id)
    db_session.add(membership)
    await db_session.flush()

    with pytest.raises(HTTPException) as exc_info:
        await role_service.deprecate(role.id)
    assert exc_info.value.status_code == 409
    assert "BR-C003-04" in exc_info.value.detail


async def test_role_retire_rejects_unknown_role(db_session: AsyncSession) -> None:
    service = RoleService(RoleRepository(db_session))
    with pytest.raises(HTTPException) as exc_info:
        await service.retire(uuid.uuid4())
    assert exc_info.value.status_code == 404


async def test_role_retire_is_terminal_rejects_second_retire(db_session: AsyncSession) -> None:
    service = RoleService(RoleRepository(db_session))
    role = await service.establish(EstablishRoleRequest(role_code="BA08_ROLE_3", role_name="V1"))
    await service.retire(role.id)

    with pytest.raises(HTTPException) as exc_info:
        await service.retire(role.id)
    assert exc_info.value.status_code == 409


async def test_role_deprecate_rejects_a_superseded_row(db_session: AsyncSession) -> None:
    """A SUPERSEDED (historical, non-current) version may not be deprecated directly."""
    service = RoleService(RoleRepository(db_session))
    role = await service.establish(EstablishRoleRequest(role_code="BA08_ROLE_4", role_name="V1"))
    await service.create_new_version(role.id, VersionRoleRequest(role_name="V2"))

    with pytest.raises(HTTPException) as exc_info:
        await service.deprecate(role.id)  # role.id is now SUPERSEDED, not ACTIVE
    assert exc_info.value.status_code == 409


# --- Domain Permission -------------------------------------------------


@pytest.fixture
async def seeded_membership_and_domain(db_session: AsyncSession):
    person = Person(first_name="BA08", last_name="DP", display_name="BA08 DP")
    organization = Organization(organization_code="BA08-DP-ORG", organization_name="BA-08 DP Org", organization_type="CORPORATE")
    role = Role(role_code="BA08_DP_ROLE", role_name="BA-08 DP Role")
    domain = Domain(domain_name="Finance")
    db_session.add_all([person, organization, role, domain])
    await db_session.flush()

    membership = Membership(person_id=person.id, organization_id=organization.id, role_id=role.id)
    db_session.add(membership)
    await db_session.flush()
    return membership, domain


def _domain_permission_service(session: AsyncSession) -> DomainPermissionService:
    return DomainPermissionService(
        DomainPermissionRepository(session), DomainRepository(session), MembershipRepository(session)
    )


async def test_domain_permission_retire_succeeds(db_session: AsyncSession, seeded_membership_and_domain) -> None:
    membership, domain = seeded_membership_and_domain
    service = _domain_permission_service(db_session)
    grant = await service.establish(
        EstablishDomainPermissionRequest(membership_id=membership.id, domain_id=domain.id, permission_level="VIEW")
    )

    retired = await service.retire(grant.id)

    assert retired.status == "RETIRED"
    assert retired.permission_level == "VIEW"


async def test_domain_permission_retire_rejects_unknown_grant(db_session: AsyncSession) -> None:
    service = _domain_permission_service(db_session)
    with pytest.raises(HTTPException) as exc_info:
        await service.retire(uuid.uuid4())
    assert exc_info.value.status_code == 404


# --- Approval Authority --------------------------------------------------


async def test_approval_authority_deprecate_succeeds(db_session: AsyncSession) -> None:
    organization = Organization(organization_code="BA08-AA-ORG", organization_name="BA-08 AA Org", organization_type="CORPORATE")
    db_session.add(organization)
    await db_session.flush()

    service = ApprovalAuthorityService(
        ApprovalAuthorityRepository(db_session), OrganizationRepository(db_session), DomainRepository(db_session)
    )
    authority = await service.establish(
        EstablishApprovalAuthorityRequest(
            organization_id=organization.id, authority_name="V1", approval_strategy="ANY_ONE", scope_type="GLOBAL"
        )
    )

    deprecated = await service.deprecate(authority.id)

    assert deprecated.status == "DEPRECATED"
    assert deprecated.scope_type == "GLOBAL"


async def test_approval_authority_retire_is_terminal(db_session: AsyncSession) -> None:
    organization = Organization(organization_code="BA08-AA-ORG-2", organization_name="BA-08 AA Org 2", organization_type="CORPORATE")
    db_session.add(organization)
    await db_session.flush()

    service = ApprovalAuthorityService(
        ApprovalAuthorityRepository(db_session), OrganizationRepository(db_session), DomainRepository(db_session)
    )
    authority = await service.establish(
        EstablishApprovalAuthorityRequest(
            organization_id=organization.id, authority_name="V1", approval_strategy="ANY_ONE", scope_type="GLOBAL"
        )
    )
    await service.retire(authority.id)

    with pytest.raises(HTTPException) as exc_info:
        await service.retire(authority.id)
    assert exc_info.value.status_code == 409


# --- Delegation Policy --------------------------------------------------


async def test_delegation_policy_retire_succeeds(db_session: AsyncSession) -> None:
    organization = Organization(organization_code="BA08-DEL-ORG", organization_name="BA-08 Delegation Org", organization_type="CORPORATE")
    db_session.add(organization)
    await db_session.flush()

    service = DelegationPolicyService(
        DelegationPolicyRepository(db_session), OrganizationRepository(db_session), DomainRepository(db_session)
    )
    policy = await service.establish(
        EstablishDelegationPolicyRequest(
            organization_id=organization.id, policy_name="V1", delegation_type="EMERGENCY", scope_type="ORGANIZATION"
        )
    )

    retired = await service.retire(policy.id)

    assert retired.status == "RETIRED"
    assert retired.delegation_type == "EMERGENCY"


async def test_delegation_policy_deprecate_rejects_unknown_policy(db_session: AsyncSession) -> None:
    service = DelegationPolicyService(
        DelegationPolicyRepository(db_session), OrganizationRepository(db_session), DomainRepository(db_session)
    )
    with pytest.raises(HTTPException) as exc_info:
        await service.deprecate(uuid.uuid4())
    assert exc_info.value.status_code == 404


# --- Runtime Assignment Policy -------------------------------------------


async def test_runtime_assignment_policy_deprecate_succeeds(db_session: AsyncSession) -> None:
    organization = Organization(organization_code="BA08-RAP-ORG", organization_name="BA-08 RAP Org", organization_type="CORPORATE")
    db_session.add(organization)
    await db_session.flush()

    service = RuntimeAssignmentPolicyService(
        RuntimeAssignmentPolicyRepository(db_session), OrganizationRepository(db_session)
    )
    policy = await service.establish(
        EstablishRuntimeAssignmentPolicyRequest(
            organization_id=organization.id, policy_name="V1", assignment_target_type="BUSINESS_ROLE"
        )
    )

    deprecated = await service.deprecate(policy.id)

    assert deprecated.status == "DEPRECATED"
    assert deprecated.assignment_target_type == "BUSINESS_ROLE"


async def test_runtime_assignment_policy_retire_is_terminal(db_session: AsyncSession) -> None:
    organization = Organization(organization_code="BA08-RAP-ORG-2", organization_name="BA-08 RAP Org 2", organization_type="CORPORATE")
    db_session.add(organization)
    await db_session.flush()

    service = RuntimeAssignmentPolicyService(
        RuntimeAssignmentPolicyRepository(db_session), OrganizationRepository(db_session)
    )
    policy = await service.establish(
        EstablishRuntimeAssignmentPolicyRequest(
            organization_id=organization.id, policy_name="V1", assignment_target_type="GROUP"
        )
    )
    await service.retire(policy.id)

    with pytest.raises(HTTPException) as exc_info:
        await service.deprecate(policy.id)
    assert exc_info.value.status_code == 409
