import uuid

import pytest
from pydantic import ValidationError

from schemas.approval_authority import EstablishApprovalAuthorityRequest

_ORG_ID = uuid.uuid4()
_DOMAIN_ID = uuid.uuid4()
_OBJECT_ID = uuid.uuid4()


def _base_kwargs(**overrides) -> dict:
    kwargs = {
        "organization_id": _ORG_ID,
        "authority_name": "Annual Report Approver",
        "approval_strategy": "SEQUENTIAL",
    }
    kwargs.update(overrides)
    return kwargs


# --- Valid combinations (the four rows of the required matrix) ---------


def test_global_scope_requires_only_organization_id() -> None:
    request = EstablishApprovalAuthorityRequest(**_base_kwargs(scope_type="GLOBAL"))
    assert request.scope_type.value == "GLOBAL"
    assert request.domain_id is None
    assert request.object_type is None
    assert request.object_id is None


def test_company_scope_requires_only_organization_id() -> None:
    request = EstablishApprovalAuthorityRequest(**_base_kwargs(scope_type="COMPANY"))
    assert request.scope_type.value == "COMPANY"


def test_domain_scope_requires_domain_id() -> None:
    request = EstablishApprovalAuthorityRequest(
        **_base_kwargs(scope_type="DOMAIN", domain_id=_DOMAIN_ID)
    )
    assert request.domain_id == _DOMAIN_ID
    assert request.object_type is None
    assert request.object_id is None


def test_object_scope_requires_object_type_and_object_id() -> None:
    request = EstablishApprovalAuthorityRequest(
        **_base_kwargs(scope_type="OBJECT", object_type="revenue_cde", object_id=_OBJECT_ID)
    )
    assert request.object_type == "revenue_cde"
    assert request.object_id == _OBJECT_ID
    assert request.domain_id is None


# --- Rejected: missing required anchor ----------------------------------


def test_domain_scope_without_domain_id_is_rejected() -> None:
    with pytest.raises(ValidationError, match="scope_type 'DOMAIN' requires domain_id"):
        EstablishApprovalAuthorityRequest(**_base_kwargs(scope_type="DOMAIN"))


def test_object_scope_without_object_type_is_rejected() -> None:
    with pytest.raises(ValidationError, match="scope_type 'OBJECT' requires both object_type and object_id"):
        EstablishApprovalAuthorityRequest(
            **_base_kwargs(scope_type="OBJECT", object_id=_OBJECT_ID)
        )


def test_object_scope_without_object_id_is_rejected() -> None:
    with pytest.raises(ValidationError, match="scope_type 'OBJECT' requires both object_type and object_id"):
        EstablishApprovalAuthorityRequest(
            **_base_kwargs(scope_type="OBJECT", object_type="revenue_cde")
        )


# --- Rejected: ambiguous / dual-stated combinations ---------------------


def test_global_scope_with_domain_id_is_rejected() -> None:
    """A GLOBAL/COMPANY scope carrying a Domain anchor is exactly the 'dual-stated' case EX-C003-03 forbids."""
    with pytest.raises(ValidationError, match="must not include domain_id"):
        EstablishApprovalAuthorityRequest(
            **_base_kwargs(scope_type="GLOBAL", domain_id=_DOMAIN_ID)
        )


def test_company_scope_with_object_anchor_is_rejected() -> None:
    with pytest.raises(ValidationError, match="must not include domain_id, object_type, or object_id"):
        EstablishApprovalAuthorityRequest(
            **_base_kwargs(scope_type="COMPANY", object_type="revenue_cde", object_id=_OBJECT_ID)
        )


def test_domain_scope_with_object_anchor_also_set_is_rejected() -> None:
    """Two anchors set at once — the multiple-scopes case."""
    with pytest.raises(ValidationError, match="must not include object_type or object_id"):
        EstablishApprovalAuthorityRequest(
            **_base_kwargs(
                scope_type="DOMAIN", domain_id=_DOMAIN_ID, object_type="revenue_cde", object_id=_OBJECT_ID
            )
        )


def test_object_scope_with_domain_id_also_set_is_rejected() -> None:
    with pytest.raises(ValidationError, match="must not include domain_id"):
        EstablishApprovalAuthorityRequest(
            **_base_kwargs(
                scope_type="OBJECT", object_type="revenue_cde", object_id=_OBJECT_ID, domain_id=_DOMAIN_ID
            )
        )


def test_invalid_scope_type_value_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EstablishApprovalAuthorityRequest(**_base_kwargs(scope_type="NOT_A_REAL_SCOPE"))


def test_invalid_approval_strategy_value_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EstablishApprovalAuthorityRequest(
            organization_id=_ORG_ID,
            authority_name="Annual Report Approver",
            approval_strategy="NOT_A_REAL_STRATEGY",
            scope_type="GLOBAL",
        )
