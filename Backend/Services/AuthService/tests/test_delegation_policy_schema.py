import uuid

import pytest
from pydantic import ValidationError

from schemas.delegation_policy import EstablishDelegationPolicyRequest

_ORG_ID = uuid.uuid4()
_DOMAIN_ID = uuid.uuid4()
_OBJECT_ID = uuid.uuid4()


def _base_kwargs(**overrides) -> dict:
    kwargs = {
        "organization_id": _ORG_ID,
        "policy_name": "Emergency Financial Approval Delegation",
        "delegation_type": "EMERGENCY",
    }
    kwargs.update(overrides)
    return kwargs


# --- Valid combinations (the four rows of the required matrix) ---------


def test_organization_scope_requires_only_organization_id() -> None:
    request = EstablishDelegationPolicyRequest(**_base_kwargs(scope_type="ORGANIZATION"))
    assert request.scope_type.value == "ORGANIZATION"
    assert request.domain_id is None
    assert request.object_type is None
    assert request.object_id is None
    assert request.event_code is None


def test_domain_scope_requires_domain_id() -> None:
    request = EstablishDelegationPolicyRequest(
        **_base_kwargs(scope_type="DOMAIN", domain_id=_DOMAIN_ID)
    )
    assert request.domain_id == _DOMAIN_ID
    assert request.object_type is None
    assert request.event_code is None


def test_object_scope_requires_object_type_and_object_id() -> None:
    request = EstablishDelegationPolicyRequest(
        **_base_kwargs(scope_type="OBJECT", object_type="revenue_cde", object_id=_OBJECT_ID)
    )
    assert request.object_type == "revenue_cde"
    assert request.object_id == _OBJECT_ID
    assert request.domain_id is None
    assert request.event_code is None


def test_event_scope_requires_event_code() -> None:
    request = EstablishDelegationPolicyRequest(
        **_base_kwargs(scope_type="EVENT", event_code="CFO_SIGNOFF")
    )
    assert request.event_code == "CFO_SIGNOFF"
    assert request.domain_id is None
    assert request.object_type is None


def test_custom_delegation_type_is_accepted() -> None:
    """URA-001-90: organizations may define custom types beyond the five standard ones."""
    request = EstablishDelegationPolicyRequest(
        organization_id=_ORG_ID,
        policy_name="Interim CFO Delegation",
        delegation_type="INTERIM_CFO",
        scope_type="ORGANIZATION",
    )
    assert request.delegation_type == "INTERIM_CFO"


# --- Rejected: missing required anchor ----------------------------------


def test_domain_scope_without_domain_id_is_rejected() -> None:
    with pytest.raises(ValidationError, match="scope_type 'DOMAIN' requires domain_id"):
        EstablishDelegationPolicyRequest(**_base_kwargs(scope_type="DOMAIN"))


def test_object_scope_without_object_type_is_rejected() -> None:
    with pytest.raises(ValidationError, match="scope_type 'OBJECT' requires both object_type and object_id"):
        EstablishDelegationPolicyRequest(
            **_base_kwargs(scope_type="OBJECT", object_id=_OBJECT_ID)
        )


def test_event_scope_without_event_code_is_rejected() -> None:
    with pytest.raises(ValidationError, match="scope_type 'EVENT' requires event_code"):
        EstablishDelegationPolicyRequest(**_base_kwargs(scope_type="EVENT"))


# --- Rejected: ambiguous / dual-stated combinations ---------------------


def test_organization_scope_with_domain_id_is_rejected() -> None:
    with pytest.raises(ValidationError, match="must not include domain_id"):
        EstablishDelegationPolicyRequest(
            **_base_kwargs(scope_type="ORGANIZATION", domain_id=_DOMAIN_ID)
        )


def test_domain_scope_with_event_code_also_set_is_rejected() -> None:
    with pytest.raises(ValidationError, match="must not include object_type, object_id, or event_code"):
        EstablishDelegationPolicyRequest(
            **_base_kwargs(scope_type="DOMAIN", domain_id=_DOMAIN_ID, event_code="CFO_SIGNOFF")
        )


def test_object_scope_with_domain_id_also_set_is_rejected() -> None:
    with pytest.raises(ValidationError, match="must not include domain_id or event_code"):
        EstablishDelegationPolicyRequest(
            **_base_kwargs(
                scope_type="OBJECT", object_type="revenue_cde", object_id=_OBJECT_ID, domain_id=_DOMAIN_ID
            )
        )


def test_event_scope_with_object_anchor_also_set_is_rejected() -> None:
    with pytest.raises(ValidationError, match="must not include domain_id, object_type, or object_id"):
        EstablishDelegationPolicyRequest(
            **_base_kwargs(
                scope_type="EVENT", event_code="CFO_SIGNOFF", object_type="revenue_cde", object_id=_OBJECT_ID
            )
        )


def test_invalid_scope_type_value_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EstablishDelegationPolicyRequest(**_base_kwargs(scope_type="NOT_A_REAL_SCOPE"))


def test_empty_delegation_type_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EstablishDelegationPolicyRequest(
            organization_id=_ORG_ID,
            policy_name="Some Policy",
            delegation_type="",
            scope_type="ORGANIZATION",
        )
