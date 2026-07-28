"""
WP-02 BA-07 — Version and Re-effective-Date Authorization Policy Object
(ERB-C003-02 / EX-C003-07). Service-layer tests, one class per
authorization policy object type, covering the shared BR-C003-05
guarantee (prior version preserved as SUPERSEDED, never mutated) and
each type's own amendable-field boundary.
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
from schemas.approval_authority import EstablishApprovalAuthorityRequest, VersionApprovalAuthorityRequest
from schemas.delegation_policy import EstablishDelegationPolicyRequest, VersionDelegationPolicyRequest
from schemas.domain_permission import EstablishDomainPermissionRequest, VersionDomainPermissionRequest
from schemas.role import EstablishRoleRequest, VersionRoleRequest
from schemas.runtime_assignment_policy import EstablishRuntimeAssignmentPolicyRequest, VersionRuntimeAssignmentPolicyRequest
from services.approval_authority_service import ApprovalAuthorityService
from services.delegation_policy_service import DelegationPolicyService
from services.domain_permission_service import DomainPermissionService
from services.role_service import RoleService
from services.runtime_assignment_policy_service import RuntimeAssignmentPolicyService


# --- Role -------------------------------------------------------------


async def test_role_version_preserves_prior_version_as_superseded(db_session: AsyncSession) -> None:
    service = RoleService(RoleRepository(db_session))
    role = await service.establish(
        EstablishRoleRequest(role_code="VERSION_TEST_ROLE", role_name="Original Name")
    )
    original_id = role.id

    new_version = await service.create_new_version(
        original_id, VersionRoleRequest(role_name="Amended Name"), actor_id="platform-admin-1"
    )

    assert new_version.id != original_id
    assert new_version.role_name == "Amended Name"
    assert new_version.role_code == "VERSION_TEST_ROLE"
    assert new_version.version == 2
    assert new_version.status == RoleVersionStatus.ACTIVE.value
    assert new_version.supersedes_id == original_id

    prior = await service.role_repo.get_by_id(original_id)
    assert prior.status == RoleVersionStatus.SUPERSEDED.value
    assert prior.effective_to is not None
    assert prior.role_name == "Original Name"  # never mutated in place


async def test_role_version_rejects_unknown_role(db_session: AsyncSession) -> None:
    service = RoleService(RoleRepository(db_session))
    with pytest.raises(HTTPException) as exc_info:
        await service.create_new_version(uuid.uuid4(), VersionRoleRequest(role_name="X"))
    assert exc_info.value.status_code == 404


async def test_role_version_rejects_already_superseded_version(db_session: AsyncSession) -> None:
    service = RoleService(RoleRepository(db_session))
    role = await service.establish(EstablishRoleRequest(role_code="VERSION_TEST_ROLE_2", role_name="V1"))
    await service.create_new_version(role.id, VersionRoleRequest(role_name="V2"))

    with pytest.raises(HTTPException) as exc_info:
        await service.create_new_version(role.id, VersionRoleRequest(role_name="V3"))
    assert exc_info.value.status_code == 409


async def test_role_version_omitting_a_field_leaves_it_unchanged(db_session: AsyncSession) -> None:
    service = RoleService(RoleRepository(db_session))
    role = await service.establish(
        EstablishRoleRequest(role_code="VERSION_TEST_ROLE_3", role_name="V1", description="Original description")
    )

    new_version = await service.create_new_version(role.id, VersionRoleRequest(role_name="V2"))

    assert new_version.role_name == "V2"
    assert new_version.description == "Original description"


# --- Domain Permission -------------------------------------------------


@pytest.fixture
async def seeded_membership_and_domain(db_session: AsyncSession):
    person = Person(first_name="BA07", last_name="Tester", display_name="BA07 Tester")
    organization = Organization(
        organization_code="BA07-DP-ORG", organization_name="BA-07 Domain Permission Org", organization_type="CORPORATE",
    )
    role = Role(role_code="BA07_DP_TEST_ROLE", role_name="BA-07 Domain Permission Test Role")
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


async def test_domain_permission_version_amends_only_effective_dates(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    membership, domain = seeded_membership_and_domain
    service = _domain_permission_service(db_session)
    grant = await service.establish(
        EstablishDomainPermissionRequest(membership_id=membership.id, domain_id=domain.id, permission_level="VIEW")
    )

    new_version = await service.create_new_version(
        grant.id, VersionDomainPermissionRequest(effective_to=None)
    )

    assert new_version.permission_level == "VIEW"
    assert new_version.membership_id == membership.id
    assert new_version.version == 2
    assert new_version.supersedes_id == grant.id

    prior = await service.domain_permission_repo.get_by_id(grant.id)
    assert prior.status == "SUPERSEDED"


async def test_domain_permission_version_rejects_unknown_grant(db_session: AsyncSession) -> None:
    service = _domain_permission_service(db_session)
    with pytest.raises(HTTPException) as exc_info:
        await service.create_new_version(uuid.uuid4(), VersionDomainPermissionRequest())
    assert exc_info.value.status_code == 404


# --- Approval Authority --------------------------------------------------


async def test_approval_authority_version_preserves_scope(db_session: AsyncSession) -> None:
    organization = Organization(organization_code="BA07-AA-ORG", organization_name="BA-07 AA Org", organization_type="CORPORATE")
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

    new_version = await service.create_new_version(
        authority.id, VersionApprovalAuthorityRequest(authority_name="V2", majority_threshold_pct=75)
    )

    assert new_version.authority_name == "V2"
    assert new_version.majority_threshold_pct == 75
    assert new_version.scope_type == "GLOBAL"
    assert new_version.approval_strategy == "ANY_ONE"
    assert new_version.version == 2


async def test_approval_authority_version_rejects_superseded_target(db_session: AsyncSession) -> None:
    organization = Organization(organization_code="BA07-AA-ORG-2", organization_name="BA-07 AA Org 2", organization_type="CORPORATE")
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
    await service.create_new_version(authority.id, VersionApprovalAuthorityRequest(authority_name="V2"))

    with pytest.raises(HTTPException) as exc_info:
        await service.create_new_version(authority.id, VersionApprovalAuthorityRequest(authority_name="V3"))
    assert exc_info.value.status_code == 409


# --- Delegation Policy --------------------------------------------------


async def test_delegation_policy_version_preserves_scope(db_session: AsyncSession) -> None:
    organization = Organization(organization_code="BA07-DEL-ORG", organization_name="BA-07 Delegation Org", organization_type="CORPORATE")
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

    new_version = await service.create_new_version(
        policy.id, VersionDelegationPolicyRequest(sub_delegation_allowed=True)
    )

    assert new_version.sub_delegation_allowed is True
    assert new_version.policy_name == "V1"
    assert new_version.delegation_type == "EMERGENCY"
    assert new_version.scope_type == "ORGANIZATION"
    assert new_version.version == 2


async def test_delegation_policy_version_rejects_unknown_policy(db_session: AsyncSession) -> None:
    service = DelegationPolicyService(
        DelegationPolicyRepository(db_session), OrganizationRepository(db_session), DomainRepository(db_session)
    )
    with pytest.raises(HTTPException) as exc_info:
        await service.create_new_version(uuid.uuid4(), VersionDelegationPolicyRequest(policy_name="X"))
    assert exc_info.value.status_code == 404


# --- Runtime Assignment Policy -------------------------------------------


async def test_runtime_assignment_policy_version_preserves_target_type(db_session: AsyncSession) -> None:
    organization = Organization(organization_code="BA07-RAP-ORG", organization_name="BA-07 RAP Org", organization_type="CORPORATE")
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

    new_version = await service.create_new_version(
        policy.id,
        VersionRuntimeAssignmentPolicyRequest(configured_lifecycle_states=["CREATED", "ASSIGNED", "BOARD_APPROVED"]),
    )

    assert new_version.configured_lifecycle_states == ["CREATED", "ASSIGNED", "BOARD_APPROVED"]
    assert new_version.assignment_target_type == "BUSINESS_ROLE"
    assert new_version.policy_name == "V1"
    assert new_version.version == 2


async def test_runtime_assignment_policy_version_rejects_superseded_target(db_session: AsyncSession) -> None:
    organization = Organization(organization_code="BA07-RAP-ORG-2", organization_name="BA-07 RAP Org 2", organization_type="CORPORATE")
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
    await service.create_new_version(policy.id, VersionRuntimeAssignmentPolicyRequest(policy_name="V2"))

    with pytest.raises(HTTPException) as exc_info:
        await service.create_new_version(policy.id, VersionRuntimeAssignmentPolicyRequest(policy_name="V3"))
    assert exc_info.value.status_code == 409
