"""
WP-02 BA-10 — Resolve Dependent Capability Authorization Policy
Hand-off Rejection (ERB-C003-03 / EX-C003-10). Service-layer tests for
AuthorizationPolicyConflictService.classify_handoff_rejection(),
covering both classification branches (CAPABILITY_SCOPED_INSUFFICIENCY,
INTEGRITY_SIGNAL) and confirming the classification is driven entirely
by the object's own status/BA-09 conflict state, never by the
reporting capability's stated reason.
"""
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from models.organization import Organization
from repositories.domain_repository import DomainRepository
from repositories.organization_repository import OrganizationRepository
from repositories.role_repository import RoleRepository
from schemas.authorization_policy_handoff import HandoffRejectionClassification, ReportHandoffRejectionRequest
from schemas.role import EstablishRoleRequest, VersionRoleRequest
from services.authorization_policy_conflict_service import AuthorizationPolicyConflictService
from services.role_service import RoleService


def _conflict_service(session: AsyncSession) -> AuthorizationPolicyConflictService:
    return AuthorizationPolicyConflictService(OrganizationRepository(session), DomainRepository(session))


async def test_classify_handoff_rejection_scoped_to_capability_for_a_clean_role(db_session: AsyncSession) -> None:
    """
    Contract 5.7's central guarantee: a clean, ACTIVE, conflict-free
    object is classified CAPABILITY_SCOPED_INSUFFICIENCY regardless of
    what the reporting capability claims — the object is preserved.
    """
    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.establish(EstablishRoleRequest(role_code="BA10_ROLE_CLEAN", role_name="V1"))

    outcome = await _conflict_service(db_session).classify_handoff_rejection(
        "role", role, role_service.role_repo,
        ReportHandoffRejectionRequest(
            reporting_capability="C-002",
            stated_reason="Access evaluation claims this role's definition is unsound.",
        ),
        actor_id="platform-admin-1",
    )

    assert outcome.classification == HandoffRejectionClassification.CAPABILITY_SCOPED_INSUFFICIENCY
    assert outcome.object_preserved is True
    assert outcome.routed_to is None
    assert outcome.conflict_report.has_conflicts is False


async def test_classify_handoff_rejection_integrity_signal_for_a_retired_role(db_session: AsyncSession) -> None:
    """A RETIRED object is unambiguously an integrity signal, independent of BA-09's own conflict check."""
    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.establish(EstablishRoleRequest(role_code="BA10_ROLE_RETIRED", role_name="V1"))
    retired = await role_service.retire(role.id)

    outcome = await _conflict_service(db_session).classify_handoff_rejection(
        "role", retired, role_service.role_repo,
        ReportHandoffRejectionRequest(reporting_capability="C-002", stated_reason="Cannot rely on this role."),
    )

    assert outcome.classification == HandoffRejectionClassification.INTEGRITY_SIGNAL
    assert outcome.object_preserved is False
    assert outcome.routed_to is not None
    assert "RETIRED" in outcome.explanation


async def test_classify_handoff_rejection_integrity_signal_for_a_deprecated_role(db_session: AsyncSession) -> None:
    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.establish(EstablishRoleRequest(role_code="BA10_ROLE_DEPRECATED", role_name="V1"))
    deprecated = await role_service.deprecate(role.id)

    outcome = await _conflict_service(db_session).classify_handoff_rejection(
        "role", deprecated, role_service.role_repo,
        ReportHandoffRejectionRequest(reporting_capability="C-002", stated_reason="Cannot rely on this role."),
    )

    assert outcome.classification == HandoffRejectionClassification.INTEGRITY_SIGNAL
    assert outcome.object_preserved is False


async def test_classify_handoff_rejection_integrity_signal_for_a_superseded_role(db_session: AsyncSession) -> None:
    """
    A SUPERSEDED row is a preserved historical version, never the
    object's current, in-force version — Independent Review found this
    was previously mis-classified as CAPABILITY_SCOPED_INSUFFICIENCY
    with an explanation that falsely claimed it was ACTIVE.
    """
    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.establish(EstablishRoleRequest(role_code="BA10_ROLE_SUPERSEDED", role_name="V1"))
    await role_service.create_new_version(role.id, VersionRoleRequest(role_name="V2"), actor_id="platform-admin-1")
    superseded = await role_service.role_repo.get_by_id(role.id)

    outcome = await _conflict_service(db_session).classify_handoff_rejection(
        "role", superseded, role_service.role_repo,
        ReportHandoffRejectionRequest(reporting_capability="C-002", stated_reason="Cannot rely on this role."),
    )

    assert outcome.classification == HandoffRejectionClassification.INTEGRITY_SIGNAL
    assert outcome.object_preserved is False
    assert "SUPERSEDED" in outcome.explanation
    assert "ACTIVE" not in outcome.explanation


async def test_classify_handoff_rejection_integrity_signal_for_a_temporally_broken_role(db_session: AsyncSession) -> None:
    """An ACTIVE object that BA-09's own check flags (here: broken temporal validity) is also an integrity signal."""
    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.establish(EstablishRoleRequest(role_code="BA10_ROLE_TEMPORAL", role_name="V1"))
    role.effective_to = role.effective_from - timedelta(days=1)
    await db_session.flush()

    outcome = await _conflict_service(db_session).classify_handoff_rejection(
        "role", role, role_service.role_repo,
        ReportHandoffRejectionRequest(reporting_capability="C-002", stated_reason="Temporal window looks wrong."),
    )

    assert outcome.classification == HandoffRejectionClassification.INTEGRITY_SIGNAL
    assert outcome.conflict_report.has_conflicts is True
    assert any(v.rule == "Contract-5.4" for v in outcome.conflict_report.violations)


async def test_classify_handoff_rejection_is_not_influenced_by_stated_reason(db_session: AsyncSession) -> None:
    """
    Contract 5.7: "The dependent capability's stated rejection reason is
    a signal, not an authority." A wildly alarming stated_reason on an
    otherwise clean object must still classify as capability-scoped.
    """
    role_service = RoleService(RoleRepository(db_session))
    role = await role_service.establish(EstablishRoleRequest(role_code="BA10_ROLE_IGNORE_REASON", role_name="V1"))

    outcome = await _conflict_service(db_session).classify_handoff_rejection(
        "role", role, role_service.role_repo,
        ReportHandoffRejectionRequest(
            reporting_capability="C-002",
            stated_reason="This role's definition is completely corrupt and must never be used again.",
        ),
    )

    assert outcome.classification == HandoffRejectionClassification.CAPABILITY_SCOPED_INSUFFICIENCY
    assert outcome.object_preserved is True
