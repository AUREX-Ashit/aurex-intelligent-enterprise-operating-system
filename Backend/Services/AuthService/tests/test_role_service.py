import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.role_repository import RoleRepository
from schemas.role import EstablishRoleRequest
from services.role_service import RoleService


def _service(session: AsyncSession) -> RoleService:
    return RoleService(RoleRepository(session))


async def test_establish_creates_business_role(db_session: AsyncSession) -> None:
    """
    Business Activity Contract (BA-01, ERB-C003-01/EX-C003-01): a
    first-time Establish Role call creates exactly one row with the
    requested type. is_system_role defaults to False (Business Role).
    """
    service = _service(db_session)
    request = EstablishRoleRequest(
        role_code="PLANT_HEAD",
        role_name="Plant Head",
        description="Plant-level operational accountability.",
    )

    role = await service.establish(request, actor_id="platform-admin-1")

    assert role.role_code == "PLANT_HEAD"
    assert role.role_name == "Plant Head"
    assert role.description == "Plant-level operational accountability."
    assert role.is_system_role is False
    assert role.id is not None


async def test_establish_creates_system_role(db_session: AsyncSession) -> None:
    """BR-C003-08: a System Role is established with is_system_role=True."""
    service = _service(db_session)
    request = EstablishRoleRequest(
        role_code="SECURITY_ADMIN",
        role_name="Security Admin",
        is_system_role=True,
    )

    role = await service.establish(request)

    assert role.is_system_role is True


async def test_establish_allows_optional_description_to_be_omitted(db_session: AsyncSession) -> None:
    """description is the only optional field — establishment must not require it."""
    service = _service(db_session)
    request = EstablishRoleRequest(role_code="AUDITOR_V2", role_name="Auditor V2")

    role = await service.establish(request)

    assert role.description is None


async def test_establish_rejects_duplicate_role_code(db_session: AsyncSession) -> None:
    """
    BR-C003-01: role_code is unique platform-wide. A second Establish
    Role call for the same code is rejected (409), naming the specific
    violated rule (Contract 5.5), not silently relaxed or partially
    established.
    """
    service = _service(db_session)
    request = EstablishRoleRequest(role_code="DUP_ROLE", role_name="Duplicate Role")

    await service.establish(request)

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)

    assert exc_info.value.status_code == 409
    assert "DUP_ROLE" in exc_info.value.detail


async def test_establish_never_grants_a_permission(db_session: AsyncSession) -> None:
    """
    BR-C003-02: establishing a Role SHALL NOT automatically confer a
    Domain Permission, Approval Authority, or Runtime Assignment. Since
    RoleService.establish() never writes to role_permissions, a freshly
    established role has no associated permissions.
    """
    service = _service(db_session)
    request = EstablishRoleRequest(role_code="NEW_ROLE", role_name="New Role")

    role = await service.establish(request)
    await db_session.refresh(role, attribute_names=["role_permissions"])

    assert role.role_permissions == []
