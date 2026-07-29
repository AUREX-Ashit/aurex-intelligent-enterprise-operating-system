from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_claims, require_platform_admin
from models.database import db_manager
from repositories.membership_repository import MembershipRepository
from repositories.organization_node_repository import OrganizationNodeRepository
from repositories.organization_repository import OrganizationRepository
from repositories.person_repository import PersonRepository
from repositories.role_repository import RoleRepository
from schemas.membership import (
    ChangeMembershipTermsRequest,
    EstablishMembershipRequest,
    MembershipPortfolioResponse,
    MembershipResponse,
    MembershipUnderstandingResponse,
    MultiOrganizationAwarenessResponse,
    ReactivateMembershipRequest,
)
from services.membership_service import MembershipService, compute_membership_authority_consequence

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_membership_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> MembershipRepository:
    return MembershipRepository(session)


async def get_person_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> PersonRepository:
    return PersonRepository(session)


async def get_organization_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> OrganizationRepository:
    return OrganizationRepository(session)


async def get_role_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> RoleRepository:
    return RoleRepository(session)


async def get_organization_node_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> OrganizationNodeRepository:
    return OrganizationNodeRepository(session)


async def get_membership_service(
    membership_repo: Annotated[MembershipRepository, Depends(get_membership_repository)],
    person_repo: Annotated[PersonRepository, Depends(get_person_repository)],
    organization_repo: Annotated[OrganizationRepository, Depends(get_organization_repository)],
    role_repo: Annotated[RoleRepository, Depends(get_role_repository)],
    organization_node_repo: Annotated[OrganizationNodeRepository, Depends(get_organization_node_repository)],
) -> MembershipService:
    return MembershipService(membership_repo, person_repo, organization_repo, role_repo, organization_node_repo)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=MembershipResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish a new Membership Context",
    description=(
        "WP-03 Business Activity: Establish Membership Context (C-007), "
        "realizing PE-001-C007's ERB-C007-01 / EX-C007-01 (Recognize "
        "Existing Membership) + EX-C007-02 (Establish New Membership). "
        "Requires the PLATFORM_ADMIN role (interim gate — EX-C007-02's "
        "own Membership Steward/Sponsor personas are not yet "
        "implementable claims, tracked as TD-031). Rejects an unknown "
        "Person, Organization, Role, or home_node_id with 404, an "
        "inactive home_node_id with 409, and a duplicate Membership for "
        "the same (person_id, organization_id) pair with 409 "
        "(BR-C007-001's own recognition discipline)."
    ),
    responses={
        201: {"description": "Membership established."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Person, Organization, Role, or home_node_id does not exist."},
        409: {"description": "A Membership already exists for this person/organization pair, or the supplied home_node_id is not active."},
        422: {"description": "Invalid request (e.g., missing required field)."},
    },
)
async def establish_membership(
    request: EstablishMembershipRequest,
    membership_service: Annotated[MembershipService, Depends(get_membership_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> MembershipResponse:
    membership = await membership_service.establish(request, actor_id=claims.get("person_id"))
    return MembershipResponse.model_validate(membership)


# Registered before GET /{membership_id} below: Starlette matches routes in
# registration order, and this literal path would otherwise be captured by
# the dynamic membership_id route.
@router.get(
    "/multi-organization-awareness",
    response_model=MultiOrganizationAwarenessResponse,
    status_code=status.HTTP_200_OK,
    summary="Surface multi-organization Membership awareness",
    description=(
        "WP-03 Business Activity: Surface Multi-Organization Membership "
        "Awareness During Establishment (C-007), realizing PE-001-C007's "
        "ERB-C007-05 / EX-C007-09. Requires the PLATFORM_ADMIN role "
        "(interim gate — EX-C007-09's own Membership Sponsor/Steward/"
        "Platform Oversight Participant personas are not yet implementable "
        "claims, tracked as TD-039). Per BR-C007-008/Contract 5.4, returns "
        "at most an existence-only signal that the Person holds an ACTIVE "
        "Membership in an Organization other than the one supplied — "
        "never which Organization, on what terms, or under what standing "
        "(URA-001-17a)."
    ),
    responses={
        200: {"description": "Existence-only awareness signal computed."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "No Person or Organization exists with the supplied id."},
    },
)
async def surface_multi_organization_awareness(
    person_id: UUID,
    organization_id: UUID,
    membership_service: Annotated[MembershipService, Depends(get_membership_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> MultiOrganizationAwarenessResponse:
    return await membership_service.surface_multi_organization_awareness(
        person_id, organization_id, actor_id=claims.get("person_id")
    )


# Registered before GET /{membership_id} below, same reason as the
# multi-organization-awareness route above (Starlette route-matching order).
@router.get(
    "/my-portfolio",
    response_model=MembershipPortfolioResponse,
    status_code=status.HTTP_200_OK,
    summary="Present the caller's own cross-organization Membership portfolio",
    description=(
        "WP-03 Business Activity: Present Person's Own Cross-Organization "
        "Membership View (C-007), realizing PE-001-C007's ERB-C007-05 / "
        "EX-C007-10. Requires only a valid access token — no role gate — "
        "since BR-C007-009 entitles a Membership Subject to see the "
        "complete detail of their own Membership portfolio, and this is "
        "the caller's own data, never another Person's (person_id is "
        "taken from the caller's own verified claims, never a query "
        "parameter). EX-C007-10's own 'authorized aggregator' persona is "
        "not implemented here — see TD-041."
    ),
    responses={
        200: {"description": "The caller's own complete Membership portfolio."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
    },
)
async def present_own_portfolio(
    membership_service: Annotated[MembershipService, Depends(get_membership_service)],
    claims: Annotated[dict, Depends(get_current_claims)],
) -> MembershipPortfolioResponse:
    return await membership_service.present_own_portfolio(UUID(claims["person_id"]))


@router.get(
    "/{membership_id}",
    response_model=MembershipUnderstandingResponse,
    status_code=status.HTTP_200_OK,
    summary="Understand a Membership's authoritative context",
    description=(
        "WP-03 Business Activity: Understand Membership Context (C-007), "
        "realizing PE-001-C007's ERB-C007-02 / EX-C007-03. Requires the "
        "PLATFORM_ADMIN role (interim gate — EX-C007-03's own Membership "
        "Sponsor/Steward/Downstream Capability Consumer/Executive personas "
        "are not yet implementable claims, tracked as TD-034). Presents the "
        "Membership's stored terms/standing/home-node fields unchanged, "
        "plus a freshly computed authority_consequence/currently_effective "
        "pair — an ACTIVE Membership past its effective_to is never "
        "presented as currently effective (BR-C007-013)."
    ),
    responses={
        200: {"description": "Membership found; authority consequence freshly computed."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "No Membership exists with this id."},
        422: {"description": "membership_id is not a valid UUID."},
    },
)
async def understand_membership(
    membership_id: UUID,
    membership_service: Annotated[MembershipService, Depends(get_membership_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> MembershipUnderstandingResponse:
    membership = await membership_service.understand(membership_id)
    currently_effective, authority_consequence = compute_membership_authority_consequence(membership)
    return MembershipUnderstandingResponse(
        **MembershipResponse.model_validate(membership).model_dump(),
        currently_effective=currently_effective,
        authority_consequence=authority_consequence,
    )


@router.post(
    "/{membership_id}/terms",
    response_model=MembershipResponse,
    status_code=status.HTTP_200_OK,
    summary="Maintain a Membership's terms",
    description=(
        "WP-03 Business Activity: Maintain Membership Terms (C-007), "
        "realizing PE-001-C007's ERB-C007-03 / EX-C007-04 (Resolve "
        "Conflicting Membership Terms) + EX-C007-05 (Change Membership "
        "Terms). Requires the PLATFORM_ADMIN role (interim gate — "
        "EX-C007-04/05's own Membership Steward/Sponsor personas are not "
        "yet implementable claims, tracked as TD-035). At least one "
        "supplied field must genuinely differ from the Membership's "
        "current value, or the request is classified erroneous and "
        "rejected with 409 (BR-C007-003). The prior value of every "
        "changed field is preserved in the audit trail (BR-C007-004). "
        "EX-C007-06 (Reconfirm Home-Node Structural Congruence) is out "
        "of scope — no C-005/ERG-001 structural-change signal exists "
        "anywhere in this codebase to trigger it."
    ),
    responses={
        200: {"description": "Terms changed."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "No Membership exists with this id, or the supplied home_node_id does not exist."},
        409: {"description": "Requested terms match the Membership's current terms, or the supplied home_node_id is not active."},
        422: {"description": "No term field was supplied."},
    },
)
async def change_membership_terms(
    membership_id: UUID,
    request: ChangeMembershipTermsRequest,
    membership_service: Annotated[MembershipService, Depends(get_membership_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> MembershipResponse:
    membership = await membership_service.change_terms(membership_id, request, actor_id=claims.get("person_id"))
    return MembershipResponse.model_validate(membership)


@router.post(
    "/{membership_id}/reactivate",
    response_model=MembershipResponse,
    status_code=status.HTTP_200_OK,
    summary="Reactivate a non-active Membership",
    description=(
        "WP-03 Business Activity: Reactivate Membership (C-007), "
        "realizing PE-001-C007's ERB-C007-04 / EX-C007-08. Requires the "
        "PLATFORM_ADMIN role (interim gate — EX-C007-08's own Membership "
        "Steward/Sponsor personas are not yet implementable claims, "
        "tracked as TD-036). Per BR-C007-014 and Contract 5.3, no "
        "canonical authority anywhere establishes that any non-active "
        "standing may transition to ACTIVE, so every call is currently "
        "rejected with 409 (Pending Canonical Binding) and the existing "
        "Membership is preserved unchanged — this is not a defect, it is "
        "EX-C007-08's own explicitly named rejection/unresolved "
        "completion path. See TD-037."
    ),
    responses={
        200: {"description": "Membership reactivated. Not currently reachable — see TD-037."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "No Membership exists with this id."},
        409: {"description": "Membership is already ACTIVE, or reactivation from its current standing is not permitted (Pending Canonical Binding, TD-037)."},
    },
)
async def reactivate_membership(
    membership_id: UUID,
    request: ReactivateMembershipRequest,
    membership_service: Annotated[MembershipService, Depends(get_membership_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> MembershipResponse:
    membership = await membership_service.reactivate(membership_id, request, actor_id=claims.get("person_id"))
    return MembershipResponse.model_validate(membership)
