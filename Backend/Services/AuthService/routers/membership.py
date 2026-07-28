from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.membership_repository import MembershipRepository
from repositories.organization_node_repository import OrganizationNodeRepository
from repositories.organization_repository import OrganizationRepository
from repositories.person_repository import PersonRepository
from repositories.role_repository import RoleRepository
from schemas.membership import EstablishMembershipRequest, MembershipResponse
from services.membership_service import MembershipService

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
