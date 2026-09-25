"""
WP-BAE-001 M1 -- structural contract tests.

Proves: BAR-issued identity is represented (and never issued) correctly;
the pipeline enumerates IMP-001 §6.16.3 verbatim, in canonical order
(ADR-042 / RO-M1-02); the state vocabulary is exactly IMP-001 §6.18.4 /
§6.18.6; the context names §6.17.5's ten sections; a result cannot
claim success unless every stage completed.
"""

from __future__ import annotations

import pytest

from business_activity_engine import (
    AUTHORITATIVE_TRANSITIONS,
    CANONICAL_ORDER,
    BusinessActivityContext,
    BusinessActivityExecutionResult,
    BusinessActivityIdentifier,
    BusinessActivityInvocation,
    ContextSection,
    ExecutionOutcome,
    ExecutionState,
    InvalidBusinessActivityIdentifierError,
    PipelineStage,
    StageReport,
    StageStatus,
)

# IMP-001 §6.16.3, verbatim.
IMP_001_6_16_3 = (
    "Request Reception",
    "Activity Resolution",
    "Execution Context Initialization",
    "Authorization Evaluation",
    "Input Contract Validation",
    "Business Validation",
    "Metadata Resolution",
    "Workflow Resolution",
    "Business Rule Execution",
    "Persistence Coordination",
    "Transaction Commit",
    "Domain Event Publication",
    "Notification Processing",
    "Audit Recording",
    "AI Assistance Hooks",
    "Response Generation",
)


# --- Business Activity identity ---------------------------------------------


@pytest.mark.parametrize("value", ["BA-000001", "BA-000089", "BA-999999"])
def test_bar_issued_identifier_shape_is_accepted(value: str) -> None:
    identifier = BusinessActivityIdentifier(value)
    assert identifier.value == value
    assert str(identifier) == value


@pytest.mark.parametrize("value", ["", "BA-1", "BA-0000001", "ba-000001", "BIA-000001", "BA-00000A", " BA-000001", 1])
def test_malformed_identifier_is_rejected(value: object) -> None:
    with pytest.raises(InvalidBusinessActivityIdentifierError):
        BusinessActivityIdentifier(value)  # type: ignore[arg-type]


def test_identifier_is_immutable_and_value_equal() -> None:
    identifier = BusinessActivityIdentifier("BA-000001")
    assert identifier == BusinessActivityIdentifier("BA-000001")
    with pytest.raises(AttributeError):
        identifier.value = "BA-000002"  # type: ignore[misc]


def test_identity_module_offers_no_way_to_issue_an_identifier() -> None:
    public = {name for name in dir(BusinessActivityIdentifier("BA-000001")) if not name.startswith("_")}
    assert public == {"value"}


def test_invocation_requires_a_typed_identifier() -> None:
    with pytest.raises(TypeError):
        BusinessActivityInvocation(identifier="BA-000001", identity_id="p", organization_id="o")  # type: ignore[arg-type]


def test_invocation_payload_is_read_only() -> None:
    source = {"k": "v"}
    invocation = BusinessActivityInvocation(
        identifier=BusinessActivityIdentifier("BA-000001"), identity_id="p", organization_id="o", payload=source
    )
    source["k"] = "changed"
    assert invocation.payload["k"] == "v"
    with pytest.raises(TypeError):
        invocation.payload["k"] = "x"  # type: ignore[index]


# --- Pipeline ordering (ADR-042 / RO-M1-02) ---------------------------------


def test_pipeline_is_imp_001_6_16_3_in_canonical_order() -> None:
    assert tuple(stage.value.replace("_", " ").title() for stage in CANONICAL_ORDER) == tuple(
        name.title() for name in IMP_001_6_16_3
    )
    assert CANONICAL_ORDER == tuple(PipelineStage)
    assert len(CANONICAL_ORDER) == 16


def test_pipeline_adds_no_stage_outside_imp_001_6_16_3() -> None:
    names = {stage.name for stage in PipelineStage}
    assert "MANIFEST_RESOLUTION" not in names  # inside Activity Resolution (RO-M1-03)
    assert "KNOWLEDGE_GRAPH_UPDATE" not in names  # R-01, deferred -- not added from RTA-001 §6.5


def test_authorization_precedes_every_business_stage() -> None:
    index = CANONICAL_ORDER.index
    assert index(PipelineStage.AUTHORIZATION_EVALUATION) < index(PipelineStage.INPUT_CONTRACT_VALIDATION)
    assert index(PipelineStage.AUTHORIZATION_EVALUATION) < index(PipelineStage.BUSINESS_RULE_EXECUTION)
    assert index(PipelineStage.TRANSACTION_COMMIT) < index(PipelineStage.DOMAIN_EVENT_PUBLICATION)


# --- State vocabulary (IMP-001 §6.18) ----------------------------------------


def test_execution_states_are_the_nine_canonical_states() -> None:
    assert [state.value for state in ExecutionState] == [
        "CREATED", "READY", "RUNNING", "WAITING", "SUSPENDED", "COMPLETED", "FAILED", "CANCELLED", "ROLLED_BACK",
    ]


def test_only_the_ten_listed_transitions_are_authoritative() -> None:
    S = ExecutionState
    assert AUTHORITATIVE_TRANSITIONS == {
        (S.CREATED, S.READY), (S.READY, S.RUNNING), (S.RUNNING, S.WAITING), (S.WAITING, S.RUNNING),
        (S.RUNNING, S.SUSPENDED), (S.SUSPENDED, S.RUNNING), (S.RUNNING, S.COMPLETED), (S.RUNNING, S.FAILED),
        (S.RUNNING, S.CANCELLED), (S.FAILED, S.ROLLED_BACK),
    }


# --- Context sections (IMP-001 §6.17.5) --------------------------------------


def test_context_names_the_ten_canonical_sections_and_partitions_them() -> None:
    assert len(ContextSection) == 10
    available = set(BusinessActivityContext.AVAILABLE_SECTIONS)
    assert available == {ContextSection.ACTIVITY, ContextSection.IDENTITY, ContextSection.ORGANIZATION, ContextSection.RUNTIME}
    assert ContextSection.AUTHORIZATION not in available
    assert ContextSection.TRANSACTION not in available


# --- Result semantics ----------------------------------------------------------


def _reports(status: StageStatus) -> tuple[StageReport, ...]:
    return tuple(StageReport(stage, status, "") for stage in CANONICAL_ORDER)


def test_result_cannot_claim_success_while_any_stage_is_not_completed() -> None:
    reports = _reports(StageStatus.COMPLETED)[:-1] + (
        StageReport(PipelineStage.RESPONSE_GENERATION, StageStatus.NOT_IMPLEMENTED, ""),
    )
    with pytest.raises(ValueError):
        BusinessActivityExecutionResult(
            identifier=BusinessActivityIdentifier("BA-000001"), correlation_id="c",
            outcome=ExecutionOutcome.COMPLETED, terminated_at=None, reason="", stage_reports=reports,
        )


def test_result_must_report_every_stage_in_canonical_order() -> None:
    with pytest.raises(ValueError):
        BusinessActivityExecutionResult(
            identifier=BusinessActivityIdentifier("BA-000001"), correlation_id="c",
            outcome=ExecutionOutcome.NOT_IMPLEMENTED, terminated_at=PipelineStage.REQUEST_RECEPTION, reason="",
            stage_reports=tuple(reversed(_reports(StageStatus.NOT_REACHED))),
        )


def test_failure_classes_are_distinct() -> None:
    assert {outcome.value for outcome in ExecutionOutcome} == {
        "COMPLETED", "NOT_IMPLEMENTED", "ACTIVITY_NOT_REGISTERED", "AUTHORIZATION_DENIED",
        "VALIDATION_FAILED", "EXECUTION_FAILED",
    }
