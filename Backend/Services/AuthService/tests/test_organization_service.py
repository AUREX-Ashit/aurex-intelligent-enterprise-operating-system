import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.organization import Organization, OrganizationStatus
from models.organization_establishment_attempt import DomainVerificationStatus, OrganizationEstablishmentAttempt
from repositories.organization_repository import OrganizationRepository
from repositories.organization_establishment_attempt_repository import (
    OrganizationEstablishmentAttemptRepository,
)
from schemas.organization import UpdateOrganizationProfileRequest
from schemas.organization_establishment_attempt import (
    ActivateEstablishmentRequest,
    EstablishOrganizationAttemptRequest,
)
from services.organization_service import OrganizationService


def _service(session: AsyncSession) -> OrganizationService:
    return OrganizationService(
        OrganizationRepository(session), OrganizationEstablishmentAttemptRepository(session)
    )


async def _establish_and_activate(
    service: OrganizationService,
    organization_code: str,
    organization_name: str,
    organization_type: str = "CORPORATE",
    description: str | None = None,
) -> Organization:
    """
    Test-only helper (IRA-001A): BA-02 through BA-07's own tests need a
    real, ACTIVE Organization to exercise — establish() alone no longer
    produces one (BR-C004-01). Establishes an attempt, then activates it
    via the governed no-domain path, and returns the resulting
    Organization, preserving every downstream test's own assertions
    unchanged.
    """
    attempt = await service.establish(
        EstablishOrganizationAttemptRequest(
            organization_code=organization_code,
            organization_name=organization_name,
            organization_type=organization_type,
            description=description,
        )
    )
    return await service.activate_establishment(
        attempt.id, ActivateEstablishmentRequest(no_domain_activation_reason="Test fixture: no domain to claim.")
    )


# ---------------------------------------------------------------------------
# BA-01 — Establish Organization Identity (amended, IRA-001A)
# ---------------------------------------------------------------------------

async def test_establish_creates_establishment_attempt_not_organization(db_session: AsyncSession) -> None:
    """
    IRA-001A / BR-C004-01, Contract 5.4: a first-time Establish Organization
    call creates exactly one Organization Establishment Attempt row — never
    an Organization row, and never with any authoritative status.
    """
    service = _service(db_session)
    request = EstablishOrganizationAttemptRequest(
        organization_code="ACME-001",
        organization_name="Acme Corporation",
        organization_type="CORPORATE",
        description="A test organization.",
    )

    attempt = await service.establish(request, actor_id="platform-admin-1")

    assert attempt.organization_code == "ACME-001"
    assert attempt.organization_name == "Acme Corporation"
    assert attempt.organization_type == "CORPORATE"
    assert attempt.description == "A test organization."
    assert attempt.domain_verification_status == DomainVerificationStatus.NOT_CLAIMED.value
    assert attempt.activated_organization_id is None
    assert attempt.id is not None

    organizations = (await db_session.execute(select(Organization))).scalars().all()
    assert len(organizations) == 0


async def test_establish_allows_optional_description_to_be_omitted(db_session: AsyncSession) -> None:
    """description is the only optional identity field — establishment must not require it."""
    service = _service(db_session)
    request = EstablishOrganizationAttemptRequest(
        organization_code="ACME-002",
        organization_name="Acme Subsidiary",
        organization_type="SUBSIDIARY",
    )

    attempt = await service.establish(request)

    assert attempt.description is None


async def test_establish_with_primary_domain_starts_unverified(db_session: AsyncSession) -> None:
    """BR-C004-02: a claimed domain is never presented as verified before independent verification succeeds."""
    service = _service(db_session)
    request = EstablishOrganizationAttemptRequest(
        organization_code="ACME-002B",
        organization_name="Acme Domain Co",
        organization_type="CORPORATE",
        primary_domain="acme-domain-co.example",
    )

    attempt = await service.establish(request)

    assert attempt.primary_domain == "acme-domain-co.example"
    assert attempt.domain_verification_status == DomainVerificationStatus.UNVERIFIED.value


async def test_establish_rejects_duplicate_organization_code(db_session: AsyncSession) -> None:
    """
    Business Rule: organization_code is unique platform-wide. A second
    Establish Organization call for the same code is rejected (409), not
    silently deduplicated and not permitted to create a second row.
    """
    service = _service(db_session)
    request = EstablishOrganizationAttemptRequest(
        organization_code="ACME-003",
        organization_name="Acme Corporation",
        organization_type="CORPORATE",
    )
    await service.establish(request)

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)

    assert exc_info.value.status_code == 409

    result = await db_session.execute(
        select(OrganizationEstablishmentAttempt).where(
            OrganizationEstablishmentAttempt.organization_code == "ACME-003"
        )
    )
    assert len(result.scalars().all()) == 1


async def test_establish_rejects_code_already_used_by_an_activated_organization(db_session: AsyncSession) -> None:
    """
    BR-C004-01: organization_code uniqueness spans both already-activated
    Organizations and other in-flight establishment attempts — one shared
    namespace, not two independent ones.
    """
    service = _service(db_session)
    first = await service.establish(
        EstablishOrganizationAttemptRequest(
            organization_code="ACME-003B", organization_name="Acme Corp", organization_type="CORPORATE",
        )
    )
    await service.activate_establishment(first.id, ActivateEstablishmentRequest(no_domain_activation_reason="No domain to claim."))

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(
            EstablishOrganizationAttemptRequest(
                organization_code="ACME-003B", organization_name="Acme Corp Duplicate", organization_type="CORPORATE",
            )
        )

    assert exc_info.value.status_code == 409


# ---------------------------------------------------------------------------
# BA-01B — Verify Organization Domain Claim (new, IRA-001A)
# ---------------------------------------------------------------------------

async def test_verify_domain_claim_records_verified_outcome(db_session: AsyncSession) -> None:
    service = _service(db_session)
    attempt = await service.establish(
        EstablishOrganizationAttemptRequest(
            organization_code="ACME-010", organization_name="Acme Verified Co",
            organization_type="CORPORATE", primary_domain="acme-verified.example",
        )
    )

    updated = await service.verify_domain_claim(attempt.id, verified=True, actor_id="platform-admin-1")

    assert updated.domain_verification_status == DomainVerificationStatus.VERIFIED.value


async def test_verify_domain_claim_records_unverified_outcome(db_session: AsyncSession) -> None:
    service = _service(db_session)
    attempt = await service.establish(
        EstablishOrganizationAttemptRequest(
            organization_code="ACME-011", organization_name="Acme Unverified Co",
            organization_type="CORPORATE", primary_domain="acme-unverified.example",
        )
    )

    updated = await service.verify_domain_claim(attempt.id, verified=False)

    assert updated.domain_verification_status == DomainVerificationStatus.UNVERIFIED.value


async def test_verify_domain_claim_rejects_when_no_domain_was_claimed(db_session: AsyncSession) -> None:
    """BR-C004-02: verification is only meaningful against a claimed domain — nothing to verify otherwise."""
    service = _service(db_session)
    attempt = await service.establish(
        EstablishOrganizationAttemptRequest(
            organization_code="ACME-012", organization_name="Acme No Domain Co", organization_type="CORPORATE",
        )
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.verify_domain_claim(attempt.id, verified=True)

    assert exc_info.value.status_code == 409


async def test_verify_domain_claim_raises_404_for_unknown_attempt(db_session: AsyncSession) -> None:
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.verify_domain_claim(uuid.uuid4(), verified=True)

    assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# BA-01C — Activate Organization, first-time (new, IRA-001A)
# ---------------------------------------------------------------------------

async def test_activate_establishment_with_verified_domain_creates_active_organization(db_session: AsyncSession) -> None:
    """
    BR-C004-01/Contract 5.4: activation is the first, distinct act that
    produces an Authoritative, ACTIVE Organization — never establish() alone.
    """
    service = _service(db_session)
    attempt = await service.establish(
        EstablishOrganizationAttemptRequest(
            organization_code="ACME-020", organization_name="Acme Activated Co",
            organization_type="CORPORATE", primary_domain="acme-activated.example",
        )
    )
    await service.verify_domain_claim(attempt.id, verified=True)

    organization = await service.activate_establishment(
        attempt.id, ActivateEstablishmentRequest(), actor_id="platform-admin-1"
    )

    assert organization.organization_code == "ACME-020"
    assert organization.status == OrganizationStatus.ACTIVE.value
    assert organization.id is not None


async def test_activate_establishment_links_attempt_to_activated_organization(db_session: AsyncSession) -> None:
    """PE-001-C004 §1.17: the Anchor is preserved in lineage, never deleted, once activation succeeds."""
    service = _service(db_session)
    attempt = await service.establish(
        EstablishOrganizationAttemptRequest(
            organization_code="ACME-021", organization_name="Acme Lineage Co", organization_type="CORPORATE",
        )
    )

    organization = await service.activate_establishment(
        attempt.id, ActivateEstablishmentRequest(no_domain_activation_reason="No domain to claim.")
    )

    reloaded = await db_session.get(OrganizationEstablishmentAttempt, attempt.id)
    assert reloaded is not None
    assert reloaded.activated_organization_id == organization.id
    assert reloaded.no_domain_activation_reason == "No domain to claim."


async def test_activate_establishment_rejects_without_verification_or_no_domain_reason(db_session: AsyncSession) -> None:
    """BR-C004-09: the no-domain path must be an explicit, recorded decision — never a silent default."""
    service = _service(db_session)
    attempt = await service.establish(
        EstablishOrganizationAttemptRequest(
            organization_code="ACME-022", organization_name="Acme Blocked Co",
            organization_type="CORPORATE", primary_domain="acme-blocked.example",
        )
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.activate_establishment(attempt.id, ActivateEstablishmentRequest())

    assert exc_info.value.status_code == 409


async def test_activate_establishment_rejects_whitespace_only_no_domain_reason(db_session: AsyncSession) -> None:
    """BR-C004-09: a whitespace-only reason is not a genuine recorded decision — must not bypass the gate."""
    service = _service(db_session)
    attempt = await service.establish(
        EstablishOrganizationAttemptRequest(
            organization_code="ACME-024", organization_name="Acme Whitespace Co", organization_type="CORPORATE",
        )
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.activate_establishment(attempt.id, ActivateEstablishmentRequest(no_domain_activation_reason="   "))

    assert exc_info.value.status_code == 409


async def test_activate_establishment_rejects_already_activated_attempt(db_session: AsyncSession) -> None:
    service = _service(db_session)
    attempt = await service.establish(
        EstablishOrganizationAttemptRequest(
            organization_code="ACME-023", organization_name="Acme Double Activate Co", organization_type="CORPORATE",
        )
    )
    await service.activate_establishment(attempt.id, ActivateEstablishmentRequest(no_domain_activation_reason="No domain."))

    with pytest.raises(HTTPException) as exc_info:
        await service.activate_establishment(attempt.id, ActivateEstablishmentRequest(no_domain_activation_reason="No domain."))

    assert exc_info.value.status_code == 409


async def test_activate_establishment_raises_404_for_unknown_attempt(db_session: AsyncSession) -> None:
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.activate_establishment(uuid.uuid4(), ActivateEstablishmentRequest(no_domain_activation_reason="x"))

    assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# BA-02 — View Organization Details
# ---------------------------------------------------------------------------

async def test_get_details_returns_the_established_organization(db_session: AsyncSession) -> None:
    """BA-02: fetching by id returns exactly the organization created by BA-01C's activate_establishment()."""
    service = _service(db_session)
    created = await _establish_and_activate(
        service, "ACME-004", "Acme Fourth", "CORPORATE", description="Fetched by id."
    )

    fetched = await service.get_details(created.id)

    assert fetched.id == created.id
    assert fetched.organization_code == "ACME-004"
    assert fetched.organization_name == "Acme Fourth"
    assert fetched.description == "Fetched by id."
    assert fetched.status == OrganizationStatus.ACTIVE.value


async def test_get_details_raises_404_for_unknown_id(db_session: AsyncSession) -> None:
    """BA-02: a well-formed but non-existent id is a 404, not a 500 or an empty success."""
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_details(uuid.uuid4())

    assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# BA-04 — Update Organization Profile
# ---------------------------------------------------------------------------

async def test_update_profile_updates_name_type_and_description(db_session: AsyncSession) -> None:
    """
    Business Activity Contract: Update Organization Profile persists the
    new organization_name, organization_type, and description.
    """
    service = _service(db_session)
    created = await _establish_and_activate(
        service, "UPD-001", "Original Name", "CORPORATE", description="Original description."
    )

    updated = await service.update_profile(
        created.id,
        UpdateOrganizationProfileRequest(
            organization_name="Renamed Corporation",
            organization_type="SUBSIDIARY",
            description="Updated description.",
        ),
        actor_id="platform-admin-1",
    )

    assert updated.id == created.id
    assert updated.organization_name == "Renamed Corporation"
    assert updated.organization_type == "SUBSIDIARY"
    assert updated.description == "Updated description."


async def test_update_profile_does_not_change_code_or_status(db_session: AsyncSession) -> None:
    """
    Business Rule: organization_code (immutable natural key) and status
    (owned by the Activate/Suspend Business Activities, ADR-005) are not
    touched by Update Organization Profile.
    """
    service = _service(db_session)
    created = await _establish_and_activate(service, "UPD-002", "Untouched Code Org", "CORPORATE")

    updated = await service.update_profile(
        created.id,
        UpdateOrganizationProfileRequest(organization_name="New Name", organization_type="CORPORATE"),
    )

    assert updated.organization_code == "UPD-002"
    assert updated.status == OrganizationStatus.ACTIVE.value


async def test_update_profile_allows_optional_description_to_be_cleared(db_session: AsyncSession) -> None:
    """description is optional on Update, same as Establish — omitting it clears any existing value."""
    service = _service(db_session)
    created = await _establish_and_activate(
        service, "UPD-003", "Has Description", "CORPORATE", description="Will be cleared."
    )

    updated = await service.update_profile(
        created.id,
        UpdateOrganizationProfileRequest(organization_name="Has Description", organization_type="CORPORATE"),
    )

    assert updated.description is None


async def test_update_profile_raises_404_for_unknown_id(db_session: AsyncSession) -> None:
    """A well-formed but non-existent id is a 404, not a 500 or a silent no-op, same as get_details."""
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.update_profile(
            uuid.uuid4(),
            UpdateOrganizationProfileRequest(organization_name="Ghost Org", organization_type="CORPORATE"),
        )

    assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# BA-05 — Activate Organization
# ---------------------------------------------------------------------------

async def test_activate_transitions_suspended_organization_to_active(db_session: AsyncSession) -> None:
    """
    Business Activity Contract: activating a SUSPENDED organization
    transitions its status to ACTIVE. No Suspend Business Activity
    exists yet (BA-06), so the SUSPENDED starting state is seeded
    directly through the repository, not a public Business Activity.
    """
    service = _service(db_session)
    created = await _establish_and_activate(service, "ACT-001", "Suspended Org", "CORPORATE")
    await service.organization_repo.update(created.id, {"status": OrganizationStatus.SUSPENDED.value})
    await db_session.flush()

    activated = await service.activate(created.id, actor_id="platform-admin-1")

    assert activated.id == created.id
    assert activated.status == OrganizationStatus.ACTIVE.value


async def test_activate_rejects_already_active_organization(db_session: AsyncSession) -> None:
    """Business Rule: activating an already-ACTIVE organization is a 409, not a silent no-op."""
    service = _service(db_session)
    created = await _establish_and_activate(service, "ACT-002", "Already Active Org", "CORPORATE")

    with pytest.raises(HTTPException) as exc_info:
        await service.activate(created.id)

    assert exc_info.value.status_code == 409


async def test_activate_raises_404_for_unknown_id(db_session: AsyncSession) -> None:
    """A well-formed but non-existent id is a 404, same basis as get_details/update_profile."""
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.activate(uuid.uuid4())

    assert exc_info.value.status_code == 404


async def test_activate_does_not_change_profile_fields(db_session: AsyncSession) -> None:
    """Activate Organization touches only status — name, type, description, and code are untouched."""
    service = _service(db_session)
    created = await _establish_and_activate(
        service, "ACT-003", "Stable Profile Org", "CORPORATE", description="Should not change."
    )
    await service.organization_repo.update(created.id, {"status": OrganizationStatus.SUSPENDED.value})
    await db_session.flush()

    activated = await service.activate(created.id)

    assert activated.organization_code == "ACT-003"
    assert activated.organization_name == "Stable Profile Org"
    assert activated.organization_type == "CORPORATE"
    assert activated.description == "Should not change."


# ---------------------------------------------------------------------------
# BA-06 — Suspend Organization
# ---------------------------------------------------------------------------

async def test_suspend_transitions_active_organization_to_suspended(db_session: AsyncSession) -> None:
    """Business Activity Contract: suspending an ACTIVE organization transitions its status to SUSPENDED."""
    service = _service(db_session)
    created = await _establish_and_activate(service, "SUS-001", "Active Org", "CORPORATE")

    suspended = await service.suspend(created.id, actor_id="platform-admin-1")

    assert suspended.id == created.id
    assert suspended.status == OrganizationStatus.SUSPENDED.value


async def test_suspend_rejects_already_suspended_organization(db_session: AsyncSession) -> None:
    """Business Rule: suspending an already-SUSPENDED organization is a 409, not a silent no-op."""
    service = _service(db_session)
    created = await _establish_and_activate(service, "SUS-002", "Already Suspended Org", "CORPORATE")
    await service.suspend(created.id)

    with pytest.raises(HTTPException) as exc_info:
        await service.suspend(created.id)

    assert exc_info.value.status_code == 409


async def test_suspend_raises_404_for_unknown_id(db_session: AsyncSession) -> None:
    """A well-formed but non-existent id is a 404, same basis as activate()/get_details()/update_profile()."""
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.suspend(uuid.uuid4())

    assert exc_info.value.status_code == 404


async def test_suspend_does_not_change_profile_fields(db_session: AsyncSession) -> None:
    """Suspend Organization touches only status/is_active — name, type, description, and code are untouched."""
    service = _service(db_session)
    created = await _establish_and_activate(
        service, "SUS-003", "Stable Profile Org", "CORPORATE", description="Should not change."
    )

    suspended = await service.suspend(created.id)

    assert suspended.organization_code == "SUS-003"
    assert suspended.organization_name == "Stable Profile Org"
    assert suspended.organization_type == "CORPORATE"
    assert suspended.description == "Should not change."


async def test_suspend_and_activate_keep_is_active_in_sync_with_status(db_session: AsyncSession) -> None:
    """
    TD-012 resolution: is_active must move in lockstep with status for
    both transitions — SUSPENDED implies is_active=False, and a
    subsequent activate() back to ACTIVE implies is_active=True again.
    """
    service = _service(db_session)
    created = await _establish_and_activate(service, "SUS-004", "Sync Org", "CORPORATE")
    assert created.is_active is True

    suspended = await service.suspend(created.id)
    assert suspended.status == OrganizationStatus.SUSPENDED.value
    assert suspended.is_active is False

    reactivated = await service.activate(created.id)
    assert reactivated.status == OrganizationStatus.ACTIVE.value
    assert reactivated.is_active is True


# ---------------------------------------------------------------------------
# BA-07 — Retire Organization & Preserve Continuity
# ---------------------------------------------------------------------------

async def test_retire_transitions_active_organization_to_retired(db_session: AsyncSession) -> None:
    """ERB-C004-07 Entry Context: retirement may be entered directly from ACTIVE."""
    service = _service(db_session)
    created = await _establish_and_activate(service, "RET-001", "Active Org", "CORPORATE")

    retired = await service.retire(created.id, actor_id="platform-admin-1")

    assert retired.id == created.id
    assert retired.status == OrganizationStatus.RETIRED.value
    assert retired.is_active is False


async def test_retire_transitions_suspended_organization_to_retired(db_session: AsyncSession) -> None:
    """ERB-C004-07 Entry Context: retirement may also be entered from SUSPENDED, not only ACTIVE."""
    service = _service(db_session)
    created = await _establish_and_activate(service, "RET-002", "Suspended Org", "CORPORATE")
    await service.suspend(created.id)

    retired = await service.retire(created.id)

    assert retired.status == OrganizationStatus.RETIRED.value
    assert retired.is_active is False


async def test_retire_rejects_already_retired_organization(db_session: AsyncSession) -> None:
    """Business Rule: retiring an already-RETIRED organization is a 409, not a silent no-op."""
    service = _service(db_session)
    created = await _establish_and_activate(service, "RET-003", "Org", "CORPORATE")
    await service.retire(created.id)

    with pytest.raises(HTTPException) as exc_info:
        await service.retire(created.id)

    assert exc_info.value.status_code == 409


async def test_retire_raises_404_for_unknown_id(db_session: AsyncSession) -> None:
    """A well-formed but non-existent id is a 404, same basis as activate()/suspend()/get_details()."""
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.retire(uuid.uuid4())

    assert exc_info.value.status_code == 404


async def test_retire_preserves_identity_and_profile_fields(db_session: AsyncSession) -> None:
    """
    Continuity requirement (ERB-C004-07): retirement SHALL NOT physically
    delete the Organization — code, name, type, and description all
    remain intact and queryable after retirement.
    """
    service = _service(db_session)
    created = await _establish_and_activate(
        service, "RET-004", "Preserved Org", "CORPORATE", description="Should survive retirement."
    )

    retired = await service.retire(created.id)

    assert retired.organization_code == "RET-004"
    assert retired.organization_name == "Preserved Org"
    assert retired.organization_type == "CORPORATE"
    assert retired.description == "Should survive retirement."

    fetched = await service.get_details(created.id)
    assert fetched.status == OrganizationStatus.RETIRED.value
    assert fetched.organization_code == "RET-004"


async def test_retire_is_findable_by_status_filter(db_session: AsyncSession) -> None:
    """A RETIRED organization is still discoverable via Search & List's status filter — not hidden or deleted."""
    service = _service(db_session)
    created = await _establish_and_activate(service, "RET-005", "Findable Retired Org", "CORPORATE")
    await service.retire(created.id)

    items, total = await service.search(
        query=None, status_filter="RETIRED", skip=0, limit=20, sort_by="organization_name", sort_order="asc"
    )

    assert total == 1
    assert items[0].organization_code == "RET-005"


async def test_activate_rejects_retired_organization(db_session: AsyncSession) -> None:
    """
    Irreversibility invariant (PE-001-C004 §3.8): a RETIRED organization
    can never be reactivated. activate() must reject it explicitly, not
    silently succeed.
    """
    service = _service(db_session)
    created = await _establish_and_activate(service, "RET-006", "Org", "CORPORATE")
    await service.retire(created.id)

    with pytest.raises(HTTPException) as exc_info:
        await service.activate(created.id)

    assert exc_info.value.status_code == 409
    # Confirm the organization did not silently flip back to ACTIVE.
    fetched = await service.get_details(created.id)
    assert fetched.status == OrganizationStatus.RETIRED.value


async def test_suspend_rejects_retired_organization(db_session: AsyncSession) -> None:
    """Same irreversibility invariant, exercised against suspend() instead of activate()."""
    service = _service(db_session)
    created = await _establish_and_activate(service, "RET-007", "Org", "CORPORATE")
    await service.retire(created.id)

    with pytest.raises(HTTPException) as exc_info:
        await service.suspend(created.id)

    assert exc_info.value.status_code == 409
    fetched = await service.get_details(created.id)
    assert fetched.status == OrganizationStatus.RETIRED.value


# ---------------------------------------------------------------------------
# BA-03 — Search & List Organizations
# ---------------------------------------------------------------------------

async def _seed(service: OrganizationService, code: str, name: str, org_type: str = "CORPORATE") -> Organization:
    return await _establish_and_activate(service, code, name, org_type)


async def test_search_returns_all_organizations_with_default_paging(db_session: AsyncSession) -> None:
    service = _service(db_session)
    await _seed(service, "SRCH-001", "Alpha Corp")
    await _seed(service, "SRCH-002", "Beta Corp")
    await _seed(service, "SRCH-003", "Gamma Corp")

    items, total = await service.search(
        query=None, status_filter=None, skip=0, limit=20, sort_by="organization_name", sort_order="asc"
    )

    assert total == 3
    assert [i.organization_name for i in items] == ["Alpha Corp", "Beta Corp", "Gamma Corp"]


async def test_search_matches_organization_name_case_insensitively(db_session: AsyncSession) -> None:
    service = _service(db_session)
    await _seed(service, "SRCH-010", "Northwind Traders")
    await _seed(service, "SRCH-011", "Contoso Ltd")

    items, total = await service.search(
        query="north", status_filter=None, skip=0, limit=20, sort_by="organization_name", sort_order="asc"
    )

    assert total == 1
    assert items[0].organization_code == "SRCH-010"


async def test_search_matches_organization_code(db_session: AsyncSession) -> None:
    service = _service(db_session)
    await _seed(service, "UNIQUE-CODE-042", "Some Company")
    await _seed(service, "OTHER-099", "Another Company")

    items, total = await service.search(
        query="unique-code", status_filter=None, skip=0, limit=20, sort_by="organization_name", sort_order="asc"
    )

    assert total == 1
    assert items[0].organization_code == "UNIQUE-CODE-042"


async def test_search_filters_by_status(db_session: AsyncSession) -> None:
    service = _service(db_session)
    await _seed(service, "SRCH-020", "Active One")
    await _seed(service, "SRCH-021", "Active Two")

    active_items, active_total = await service.search(
        query=None, status_filter="ACTIVE", skip=0, limit=20, sort_by="organization_name", sort_order="asc"
    )
    suspended_items, suspended_total = await service.search(
        query=None, status_filter="SUSPENDED", skip=0, limit=20, sort_by="organization_name", sort_order="asc"
    )

    assert active_total == 2
    assert suspended_total == 0
    assert suspended_items == []


async def test_search_status_filter_correctly_includes_and_excludes_mixed_statuses(db_session: AsyncSession) -> None:
    """
    TD-008 resolution: with Suspend Organization (BA-06) now available,
    prove the status filter's true inclusion/exclusion against a mixed
    ACTIVE/SUSPENDED dataset — previously only the trivial "SUSPENDED
    returns empty" case was provable, since no Business Activity could
    produce a SUSPENDED row.
    """
    service = _service(db_session)
    active_org = await _seed(service, "MIX-001", "Still Active Org")
    suspended_org = await _seed(service, "MIX-002", "Now Suspended Org")
    await service.suspend(suspended_org.id)

    active_items, active_total = await service.search(
        query=None, status_filter="ACTIVE", skip=0, limit=20, sort_by="organization_name", sort_order="asc"
    )
    suspended_items, suspended_total = await service.search(
        query=None, status_filter="SUSPENDED", skip=0, limit=20, sort_by="organization_name", sort_order="asc"
    )

    assert active_total == 1
    assert active_items[0].organization_code == active_org.organization_code
    assert suspended_total == 1
    assert suspended_items[0].organization_code == suspended_org.organization_code


async def test_search_pagination_returns_correct_page_and_total(db_session: AsyncSession) -> None:
    service = _service(db_session)
    for i in range(5):
        await _seed(service, f"PAGE-{i:03d}", f"Page Org {i}")

    page_1, total_1 = await service.search(
        query=None, status_filter=None, skip=0, limit=2, sort_by="organization_code", sort_order="asc"
    )
    page_2, total_2 = await service.search(
        query=None, status_filter=None, skip=2, limit=2, sort_by="organization_code", sort_order="asc"
    )

    assert total_1 == 5 and total_2 == 5
    assert len(page_1) == 2 and len(page_2) == 2
    assert [o.organization_code for o in page_1] == ["PAGE-000", "PAGE-001"]
    assert [o.organization_code for o in page_2] == ["PAGE-002", "PAGE-003"]


async def test_search_sort_order_descending(db_session: AsyncSession) -> None:
    service = _service(db_session)
    await _seed(service, "SORT-001", "Zeta Corp")
    await _seed(service, "SORT-002", "Alpha Corp")

    items, _total = await service.search(
        query=None, status_filter=None, skip=0, limit=20, sort_by="organization_name", sort_order="desc"
    )

    assert [i.organization_name for i in items] == ["Zeta Corp", "Alpha Corp"]
