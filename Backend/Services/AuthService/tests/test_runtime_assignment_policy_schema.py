import uuid

import pytest
from pydantic import ValidationError

from schemas.runtime_assignment_policy import EstablishRuntimeAssignmentPolicyRequest, DEFAULT_LIFECYCLE_STATES

_ORG_ID = uuid.uuid4()
_ESCALATION_POLICY_ID = uuid.uuid4()


def _base_kwargs(**overrides) -> dict:
    kwargs = {
        "organization_id": _ORG_ID,
        "policy_name": "Revenue CDE Review Assignment Policy",
        "assignment_target_type": "BUSINESS_ROLE",
    }
    kwargs.update(overrides)
    return kwargs


# --- Valid combinations --------------------------------------------------


def test_business_role_target_type_is_accepted() -> None:
    request = EstablishRuntimeAssignmentPolicyRequest(**_base_kwargs())
    assert request.assignment_target_type.value == "BUSINESS_ROLE"
    assert request.configured_lifecycle_states is None
    assert request.escalation_policy_id is None


def test_named_user_target_type_is_accepted() -> None:
    request = EstablishRuntimeAssignmentPolicyRequest(**_base_kwargs(assignment_target_type="NAMED_USER"))
    assert request.assignment_target_type.value == "NAMED_USER"


def test_group_target_type_is_accepted() -> None:
    request = EstablishRuntimeAssignmentPolicyRequest(**_base_kwargs(assignment_target_type="GROUP"))
    assert request.assignment_target_type.value == "GROUP"


def test_external_user_target_type_is_accepted() -> None:
    request = EstablishRuntimeAssignmentPolicyRequest(**_base_kwargs(assignment_target_type="EXTERNAL_USER"))
    assert request.assignment_target_type.value == "EXTERNAL_USER"


def test_custom_configured_lifecycle_states_are_accepted() -> None:
    """URA-001-78: companies may add states such as BOARD_APPROVED."""
    custom_states = DEFAULT_LIFECYCLE_STATES + ["BOARD_APPROVED"]
    request = EstablishRuntimeAssignmentPolicyRequest(
        **_base_kwargs(configured_lifecycle_states=custom_states)
    )
    assert request.configured_lifecycle_states == custom_states


def test_escalation_policy_id_is_accepted() -> None:
    request = EstablishRuntimeAssignmentPolicyRequest(
        **_base_kwargs(escalation_policy_id=_ESCALATION_POLICY_ID)
    )
    assert request.escalation_policy_id == _ESCALATION_POLICY_ID


# --- Rejected -------------------------------------------------------------


def test_invalid_assignment_target_type_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EstablishRuntimeAssignmentPolicyRequest(**_base_kwargs(assignment_target_type="NOT_A_REAL_TARGET"))


def test_empty_configured_lifecycle_states_is_rejected() -> None:
    with pytest.raises(ValidationError, match="must not be empty"):
        EstablishRuntimeAssignmentPolicyRequest(**_base_kwargs(configured_lifecycle_states=[]))


def test_empty_policy_name_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EstablishRuntimeAssignmentPolicyRequest(
            organization_id=_ORG_ID,
            policy_name="",
            assignment_target_type="BUSINESS_ROLE",
        )


def test_missing_organization_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EstablishRuntimeAssignmentPolicyRequest(
            policy_name="Revenue CDE Review Assignment Policy",
            assignment_target_type="BUSINESS_ROLE",
        )
