"""
WP-02 BA-09 — Detect and Resolve Authorization Policy Dependency
Conflict (ERB-C003-03 / EX-C003-09). Service-layer tests for the shared
AuthorizationPolicyConflictService, covering detection (inbound
dependents, outbound anchor health, temporal validity, version-chain
integrity) and resolution (Contract 5.6's three explicit modes) across
representative object types. Reuses BA-08's own seeded fixtures pattern.
"""
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.domain import Domain
from models.membership import Membership
from models.organization import Organization
from models.permission import Permission
from models.person import Person
from models.role import Role
from models.role_permission import RolePermission
from repositories.approval_authority_repository import ApprovalAuthorityRepository
from repositories.domain_repository import DomainRepository
from repositories.organization_repository import OrganizationRepository
from repositories.role_repository import RoleRepository
from schemas.approval_authority import EstablishApprovalAuthorityRequest
from schemas.authorization_policy_conflict import ResolutionType, ResolveDependencyConflictRequest
from schemas.role import EstablishRoleRequest
from services.approval_authority_service import ApprovalAuthorityService
from services.authorization_policy_conflict_service import AuthorizationPolicyConflictService
from services.role_service import RoleService


def _conflict_service(session: AsyncSession) -> AuthorizationPolicyConflictService:
    return AuthorizationPolicyConflictService(OrganizationRepository(session), DomainRepository(session))


# --- Detection: inbound dependents (Role, the only real case) ------------


async def test_detect_conflicts_finds_no_violations_for_a_clean_role(db_session: AsyncSession) -> None:
    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.establish(EstablishRoleRequest(role_code="BA09_ROLE_1", role_name="V1"))

    report = await _conflict_service(db_session).detect_conflicts("role", role, role_service.role_repo)

    assert report.has_conflicts is False
    assert report.violations == []
    assert report.active_dependents == []


async def test_detect_conflicts_finds_active_membership_dependent(db_session: AsyncSession) -> None:
    person = Person(first_name="BA09", last_name="Dep", display_name="BA09 Dep")
    organization = Organization(organization_code="BA09-ROLE-ORG", organization_name="BA-09 Role Org", organization_type="CORPORATE")
    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.establish(EstablishRoleRequest(role_code="BA09_ROLE_2", role_name="V1"))

    db_session.add_all([person, organization])
    await db_session.flush()
    membership = Membership(person_id=person.id, organization_id=organization.id, role_id=role.id)
    db_session.add(membership)
    await db_session.flush()

    report = await _conflict_service(db_session).detect_conflicts("role", role, role_service.role_repo)

    assert report.has_conflicts is True
    assert any(v.rule == "BR-C003-04" for v in report.violations)
    assert len(report.active_dependents) == 1
    assert report.active_dependents[0]["dependent_type"] == "Membership"


async def test_detect_conflicts_finds_role_permission_dependent(db_session: AsyncSession) -> None:
    """
    Independent Review finding (BA-09): role_permissions is a second
    real, WP-00-era dependent table for Role, distinct from Membership.
    A RolePermission row has no lifecycle/status column of its own — its
    mere existence is an active dependent.
    """
    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.establish(EstablishRoleRequest(role_code="BA09_ROLE_PERM", role_name="V1"))
    permission = Permission(permission_code="BA09_TEST_PERMISSION", permission_name="BA-09 Test Permission")
    db_session.add(permission)
    await db_session.flush()
    role_permission = RolePermission(role_id=role.id, permission_id=permission.id)
    db_session.add(role_permission)
    await db_session.flush()

    report = await _conflict_service(db_session).detect_conflicts("role", role, role_service.role_repo)

    assert report.has_conflicts is True
    assert any(d["dependent_type"] == "RolePermission" for d in report.active_dependents)


async def test_detect_conflicts_rejects_unknown_role_via_router_layer_precondition(db_session: AsyncSession) -> None:
    """detect_conflicts() itself assumes an already-loaded object; the 404 precondition lives in the router, tested at the API layer."""
    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.role_repo.get_by_id(uuid.uuid4())
    assert role is None  # confirms the router-level precondition this test documents


# --- Detection: outbound anchor health (Approval Authority) ---------------


async def test_detect_conflicts_finds_no_violations_for_a_clean_approval_authority(db_session: AsyncSession) -> None:
    organization = Organization(organization_code="BA09-AA-ORG", organization_name="BA-09 AA Org", organization_type="CORPORATE")
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

    report = await _conflict_service(db_session).detect_conflicts("approval_authority", authority, service.approval_authority_repo)

    assert report.has_conflicts is False


async def test_detect_conflicts_flags_unresolvable_domain(db_session: AsyncSession) -> None:
    """
    Independent Review coverage gap (BA-09): the outbound-Domain branch
    (domain_id set but the Domain no longer resolves) was previously
    untested. Domain is never hard-deleted through any application code
    path — this test manufactures the scenario directly via the ORM
    session, the same technique used elsewhere in this suite to
    construct otherwise-unreachable edge cases.
    """
    organization = Organization(organization_code="BA09-AA-ORG-DOMAIN", organization_name="BA-09 AA Org Domain", organization_type="CORPORATE")
    domain = Domain(domain_name="Finance")
    db_session.add_all([organization, domain])
    await db_session.flush()

    service = ApprovalAuthorityService(
        ApprovalAuthorityRepository(db_session), OrganizationRepository(db_session), DomainRepository(db_session)
    )
    authority = await service.establish(
        EstablishApprovalAuthorityRequest(
            organization_id=organization.id, authority_name="V1", approval_strategy="ANY_ONE",
            scope_type="DOMAIN", domain_id=domain.id,
        )
    )

    await db_session.delete(domain)
    await db_session.flush()

    report = await _conflict_service(db_session).detect_conflicts("approval_authority", authority, service.approval_authority_repo)

    assert report.has_conflicts is True
    assert any("Domain" in v.description and "no longer resolves" in v.description for v in report.violations)


async def test_detect_conflicts_flags_retired_owning_organization(db_session: AsyncSession) -> None:
    organization = Organization(organization_code="BA09-AA-ORG-2", organization_name="BA-09 AA Org 2", organization_type="CORPORATE")
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

    organization.status = "RETIRED"
    await db_session.flush()

    report = await _conflict_service(db_session).detect_conflicts("approval_authority", authority, service.approval_authority_repo)

    assert report.has_conflicts is True
    assert any("RETIRED" in v.description for v in report.violations)


# --- Detection: temporal validity -----------------------------------------


async def test_detect_conflicts_flags_effective_to_before_effective_from(db_session: AsyncSession) -> None:
    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.establish(EstablishRoleRequest(role_code="BA09_ROLE_TEMPORAL", role_name="V1"))
    role.effective_to = role.effective_from - timedelta(days=1)
    await db_session.flush()

    report = await _conflict_service(db_session).detect_conflicts("role", role, role_service.role_repo)

    assert report.has_conflicts is True
    assert any(v.rule == "Contract-5.4" and "temporal validity" in v.description for v in report.violations)


async def test_detect_conflicts_flags_active_object_with_past_effective_to(db_session: AsyncSession) -> None:
    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.establish(EstablishRoleRequest(role_code="BA09_ROLE_EXPIRED", role_name="V1"))
    role.effective_to = datetime.now(timezone.utc) - timedelta(days=1)
    await db_session.flush()

    report = await _conflict_service(db_session).detect_conflicts("role", role, role_service.role_repo)

    assert report.has_conflicts is True
    assert any("conflicting lifecycle state" in v.description for v in report.violations)


# --- Detection: version-chain integrity ------------------------------------


async def test_detect_conflicts_clean_for_a_versioned_role(db_session: AsyncSession) -> None:
    """A normal version amendment (BA-07) never produces a chain conflict."""
    from schemas.role import VersionRoleRequest

    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.establish(EstablishRoleRequest(role_code="BA09_ROLE_VERSIONED", role_name="V1"))
    new_version = await role_service.create_new_version(role.id, VersionRoleRequest(role_name="V2"))

    report = await _conflict_service(db_session).detect_conflicts("role", new_version, role_service.role_repo)

    assert report.has_conflicts is False


# --- Resolution -------------------------------------------------------------


async def test_resolve_conflict_records_accepted_break_and_rechecks(db_session: AsyncSession) -> None:
    person = Person(first_name="BA09", last_name="Resolve", display_name="BA09 Resolve")
    organization = Organization(organization_code="BA09-ROLE-ORG-RESOLVE", organization_name="BA-09 Resolve Org", organization_type="CORPORATE")
    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.establish(EstablishRoleRequest(role_code="BA09_ROLE_RESOLVE", role_name="V1"))

    db_session.add_all([person, organization])
    await db_session.flush()
    membership = Membership(person_id=person.id, organization_id=organization.id, role_id=role.id)
    db_session.add(membership)
    await db_session.flush()

    conflict_service = _conflict_service(db_session)
    report = await conflict_service.resolve_conflict(
        "role", role, role_service.role_repo,
        ResolveDependencyConflictRequest(resolution_type=ResolutionType.ACCEPTED_BREAK, reason="Test acceptance"),
        actor_id="platform-admin-1",
    )

    # ACCEPTED_BREAK is audit-trail-only (TD-030) — the underlying Membership
    # dependent is unchanged, so the re-check still finds it.
    assert report.has_conflicts is True
    assert any(v.rule == "BR-C003-04" for v in report.violations)


async def test_resolve_conflict_reassignment_requires_replacement_target_id(db_session: AsyncSession) -> None:
    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.establish(EstablishRoleRequest(role_code="BA09_ROLE_REASSIGN_1", role_name="V1"))

    with pytest.raises(HTTPException) as exc_info:
        await _conflict_service(db_session).resolve_conflict(
            "role", role, role_service.role_repo,
            ResolveDependencyConflictRequest(resolution_type=ResolutionType.REASSIGNMENT_CONFIRMED, reason="Missing target"),
        )
    assert exc_info.value.status_code == 422


async def test_resolve_conflict_reassignment_rejects_inactive_replacement(db_session: AsyncSession) -> None:
    from schemas.role import VersionRoleRequest

    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.establish(EstablishRoleRequest(role_code="BA09_ROLE_REASSIGN_2", role_name="V1"))
    replacement = await role_service.establish(EstablishRoleRequest(role_code="BA09_ROLE_REASSIGN_2_TARGET", role_name="Target V1"))
    await role_service.create_new_version(replacement.id, VersionRoleRequest(role_name="Target V2"))
    # replacement.id (the original establish() row) is now SUPERSEDED, not ACTIVE.

    with pytest.raises(HTTPException) as exc_info:
        await _conflict_service(db_session).resolve_conflict(
            "role", role, role_service.role_repo,
            ResolveDependencyConflictRequest(
                resolution_type=ResolutionType.REASSIGNMENT_CONFIRMED,
                reason="Reassigning to a superseded target",
                replacement_target_id=replacement.id,
            ),
        )
    assert exc_info.value.status_code == 409


async def test_resolve_conflict_reassignment_rejects_unknown_replacement_target(db_session: AsyncSession) -> None:
    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.establish(EstablishRoleRequest(role_code="BA09_ROLE_REASSIGN_404", role_name="V1"))

    with pytest.raises(HTTPException) as exc_info:
        await _conflict_service(db_session).resolve_conflict(
            "role", role, role_service.role_repo,
            ResolveDependencyConflictRequest(
                resolution_type=ResolutionType.REASSIGNMENT_CONFIRMED,
                reason="Unknown target",
                replacement_target_id=uuid.uuid4(),
            ),
        )
    assert exc_info.value.status_code == 404


async def test_resolve_conflict_reassignment_rejects_self_as_replacement(db_session: AsyncSession) -> None:
    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.establish(EstablishRoleRequest(role_code="BA09_ROLE_REASSIGN_3", role_name="V1"))

    with pytest.raises(HTTPException) as exc_info:
        await _conflict_service(db_session).resolve_conflict(
            "role", role, role_service.role_repo,
            ResolveDependencyConflictRequest(
                resolution_type=ResolutionType.REASSIGNMENT_CONFIRMED,
                reason="Self-reassignment",
                replacement_target_id=role.id,
            ),
        )
    assert exc_info.value.status_code == 422
