"""
WP-BAE-001 M1 -- engine behaviour tests.

Proves: the entry point exists and is transport-independent; an
unimplemented stage never yields success; Manifest Resolution stays an
explicit NOT_IMPLEMENTED boundary; BAR is consulted read-only and an
unregistered activity cannot execute; the Authorization Engine's
decision is consumed unchanged and anything but ALLOW fails closed
before business execution; collaborator failures fail closed; each
failure class is reported distinctly.

No real Business Activity is used -- none is registered in M1. The
identifier values below are shape-valid literals only; no BAR row
exists for them and none is created.
"""

from __future__ import annotations

import inspect
from unittest.mock import AsyncMock, MagicMock

import pytest

from adapters.authorization_adapter import AuthorizationAdapter, AuthorizationRequest
from authorization import EvaluationPipeline, ResolverRegistry
from authorization.models import AuthorizationDecision, EvaluationResult
from business_activity_engine import (
    BusinessActivityEngine,
    BusinessActivityIdentifier,
    BusinessActivityInvocation,
    ExecutionOutcome,
    ManifestResolution,
    ManifestResolutionStatus,
    PipelineStage,
    StageStatus,
    UnimplementedManifestResolver,
)

IDENTIFIER = BusinessActivityIdentifier("BA-000001")


class RecordingRegistrationSource:
    """Test double for BAR's read-only surface. Exposes exactly the RegistrationSource method."""

    def __init__(self, registered: bool) -> None:
        self._registered = registered
        self.calls: list[BusinessActivityIdentifier] = []

    async def is_registered(self, identifier: BusinessActivityIdentifier) -> bool:
        self.calls.append(identifier)
        return self._registered


class ResolvedManifestResolver:
    """Test double standing in for the M2 resolver, so later M1 stages can be exercised."""

    async def resolve(self, identifier: BusinessActivityIdentifier) -> ManifestResolution:
        return ManifestResolution(ManifestResolutionStatus.RESOLVED, "test double")


class StubAuthorizer:
    def __init__(self, decision: AuthorizationDecision) -> None:
        self._decision = decision
        self.requests: list[AuthorizationRequest] = []

    async def evaluate(self, request: AuthorizationRequest) -> EvaluationResult:
        self.requests.append(request)
        return EvaluationResult(decision=self._decision, matched_tier=None, reason="stub", trace=())


class RaisingAuthorizer:
    async def evaluate(self, request: AuthorizationRequest) -> EvaluationResult:
        raise ConnectionError("authorization backend unavailable")


def _invocation(**overrides: object) -> BusinessActivityInvocation:
    fields: dict[str, object] = {
        "identifier": IDENTIFIER,
        "identity_id": "person-1",
        "organization_id": "org-1",
        "membership_id": "membership-1",
        "session_id": "session-1",
        "correlation_id": "corr-1",
    }
    fields.update(overrides)
    return BusinessActivityInvocation(**fields)  # type: ignore[arg-type]


def _engine(registered: bool = True, decision: AuthorizationDecision = AuthorizationDecision.ALLOW, *, resolved: bool = True):
    registration = RecordingRegistrationSource(registered)
    authorizer = StubAuthorizer(decision)
    engine = BusinessActivityEngine(
        registration_source=registration,
        authorizer=authorizer,
        manifest_resolver=ResolvedManifestResolver() if resolved else None,
    )
    return engine, registration, authorizer


def _status(result, stage: PipelineStage) -> StageStatus:
    return next(report.status for report in result.stage_reports if report.stage is stage)


# --- Entry point -----------------------------------------------------------------


def test_entry_point_is_a_single_async_execute_taking_only_an_invocation() -> None:
    assert inspect.iscoroutinefunction(BusinessActivityEngine.execute)
    assert list(inspect.signature(BusinessActivityEngine.execute).parameters) == ["self", "invocation"]


async def test_correlation_id_is_carried_or_generated() -> None:
    engine, _, _ = _engine()
    assert (await engine.execute(_invocation())).correlation_id == "corr-1"
    generated = (await engine.execute(_invocation(correlation_id=None))).correlation_id
    assert generated and generated != "corr-1"


# --- Manifest Resolution boundary (RO-M1-03) ----------------------------------------


async def test_default_manifest_resolution_is_not_implemented_and_stops_execution() -> None:
    engine, registration, authorizer = _engine(resolved=False)
    result = await engine.execute(_invocation())

    assert result.outcome is ExecutionOutcome.NOT_IMPLEMENTED
    assert result.terminated_at is PipelineStage.ACTIVITY_RESOLUTION
    assert _status(result, PipelineStage.ACTIVITY_RESOLUTION) is StageStatus.NOT_IMPLEMENTED
    assert registration.calls == [IDENTIFIER]
    assert authorizer.requests == []
    assert not result.succeeded


async def test_unimplemented_manifest_resolver_never_resolves() -> None:
    resolution = await UnimplementedManifestResolver().resolve(IDENTIFIER)
    assert resolution.status is ManifestResolutionStatus.NOT_IMPLEMENTED
    assert "M2" in resolution.reason


# --- Unimplemented stages never succeed --------------------------------------------


async def test_allow_reaches_the_first_unimplemented_stage_and_does_not_succeed() -> None:
    engine, _, _ = _engine(decision=AuthorizationDecision.ALLOW)
    result = await engine.execute(_invocation())

    assert result.outcome is ExecutionOutcome.NOT_IMPLEMENTED
    assert result.terminated_at is PipelineStage.INPUT_CONTRACT_VALIDATION
    assert _status(result, PipelineStage.AUTHORIZATION_EVALUATION) is StageStatus.COMPLETED
    assert _status(result, PipelineStage.BUSINESS_RULE_EXECUTION) is StageStatus.NOT_REACHED
    assert _status(result, PipelineStage.TRANSACTION_COMMIT) is StageStatus.NOT_REACHED
    assert not result.succeeded


@pytest.mark.parametrize("registered", [True, False])
@pytest.mark.parametrize("resolved", [True, False])
@pytest.mark.parametrize("decision", list(AuthorizationDecision))
async def test_no_m1_path_executes_business_rules_or_succeeds(registered: bool, resolved: bool, decision) -> None:
    engine, _, _ = _engine(registered, decision, resolved=resolved)
    result = await engine.execute(_invocation())

    assert not result.succeeded
    assert _status(result, PipelineStage.BUSINESS_RULE_EXECUTION) is StageStatus.NOT_REACHED
    assert [report.stage for report in result.stage_reports] == list(PipelineStage)


# --- Authorization boundary -----------------------------------------------------------


async def test_deny_prevents_business_execution() -> None:
    engine, _, authorizer = _engine(decision=AuthorizationDecision.DENY)
    result = await engine.execute(_invocation())

    assert result.outcome is ExecutionOutcome.AUTHORIZATION_DENIED
    assert result.terminated_at is PipelineStage.AUTHORIZATION_EVALUATION
    assert result.authorization is not None and result.authorization.decision is AuthorizationDecision.DENY
    assert all(
        _status(result, stage) is StageStatus.NOT_REACHED
        for stage in list(PipelineStage)[list(PipelineStage).index(PipelineStage.INPUT_CONTRACT_VALIDATION):]
    )
    assert len(authorizer.requests) == 1


@pytest.mark.parametrize(
    "decision",
    [AuthorizationDecision.DENY, AuthorizationDecision.CONDITIONAL, AuthorizationDecision.DELEGATED, AuthorizationDecision.ESCALATED],
)
async def test_every_non_allow_decision_fails_closed(decision: AuthorizationDecision) -> None:
    engine, _, _ = _engine(decision=decision)
    result = await engine.execute(_invocation())

    assert result.outcome is ExecutionOutcome.AUTHORIZATION_DENIED
    assert result.authorization.decision is decision


async def test_authorization_request_is_built_from_the_invocation_claims() -> None:
    engine, _, authorizer = _engine()
    await engine.execute(_invocation())

    (request,) = authorizer.requests
    assert request == AuthorizationRequest(
        identity_id="person-1", organization_id="org-1", membership_id="membership-1", session_id="session-1"
    )


async def test_authorizer_exception_fails_closed() -> None:
    engine = BusinessActivityEngine(
        registration_source=RecordingRegistrationSource(True),
        authorizer=RaisingAuthorizer(),
        manifest_resolver=ResolvedManifestResolver(),
    )
    result = await engine.execute(_invocation())

    assert result.outcome is ExecutionOutcome.EXECUTION_FAILED
    assert result.terminated_at is PipelineStage.AUTHORIZATION_EVALUATION
    assert "ConnectionError" in result.reason
    assert _status(result, PipelineStage.BUSINESS_RULE_EXECUTION) is StageStatus.NOT_REACHED


async def test_real_authorization_engine_with_no_resolvers_denies() -> None:
    """The existing, unmodified Authorization Engine contract: nothing bound ⇒ DENY, never a fabricated ALLOW."""
    adapter = AuthorizationAdapter(EvaluationPipeline(ResolverRegistry()))
    engine = BusinessActivityEngine(
        registration_source=RecordingRegistrationSource(True),
        authorizer=adapter,
        manifest_resolver=ResolvedManifestResolver(),
    )
    result = await engine.execute(_invocation())

    assert result.outcome is ExecutionOutcome.AUTHORIZATION_DENIED
    assert result.authorization.decision is AuthorizationDecision.DENY
    assert len(result.authorization.trace) == 5


# --- BAR boundary (RO-M1-04) ---------------------------------------------------------


async def test_unregistered_activity_cannot_execute_and_authorization_is_not_consulted() -> None:
    engine, registration, authorizer = _engine(registered=False)
    result = await engine.execute(_invocation())

    assert result.outcome is ExecutionOutcome.ACTIVITY_NOT_REGISTERED
    assert result.terminated_at is PipelineStage.ACTIVITY_RESOLUTION
    assert registration.calls == [IDENTIFIER]
    assert authorizer.requests == []


async def test_bar_is_only_ever_asked_whether_an_identifier_is_registered() -> None:
    class StrictReadOnlyRegistrationSource(RecordingRegistrationSource):
        """Fails the test on any access other than the read-only RegistrationSource method."""

        def __getattr__(self, name: str) -> object:
            raise AssertionError(f"BAE touched BAR surface '{name}', beyond is_registered")

    registration = StrictReadOnlyRegistrationSource(True)
    engine = BusinessActivityEngine(
        registration_source=registration,
        authorizer=StubAuthorizer(AuthorizationDecision.ALLOW),
        manifest_resolver=ResolvedManifestResolver(),
    )
    await engine.execute(_invocation())

    assert registration.calls == [IDENTIFIER]


async def test_registration_lookup_failure_fails_closed() -> None:
    class RaisingRegistrationSource:
        async def is_registered(self, identifier: BusinessActivityIdentifier) -> bool:
            raise TimeoutError("BAR unavailable")

    engine = BusinessActivityEngine(registration_source=RaisingRegistrationSource(), authorizer=StubAuthorizer(AuthorizationDecision.ALLOW))
    result = await engine.execute(_invocation())

    assert result.outcome is ExecutionOutcome.EXECUTION_FAILED
    assert result.terminated_at is PipelineStage.ACTIVITY_RESOLUTION


# --- Validation ------------------------------------------------------------------------


@pytest.mark.parametrize("field", ["identity_id", "organization_id"])
@pytest.mark.parametrize("blank", ["", "   "])
async def test_blank_identity_or_organization_is_a_validation_failure(field: str, blank: str) -> None:
    engine, registration, authorizer = _engine()
    result = await engine.execute(_invocation(**{field: blank}))

    assert result.outcome is ExecutionOutcome.VALIDATION_FAILED
    assert result.terminated_at is PipelineStage.REQUEST_RECEPTION
    assert registration.calls == []
    assert authorizer.requests == []


# --- Isolation between executions -----------------------------------------------------------


async def test_executions_do_not_share_state() -> None:
    engine, _, _ = _engine(decision=AuthorizationDecision.DENY)
    first = await engine.execute(_invocation(correlation_id="a"))
    second = await engine.execute(_invocation(correlation_id="b"))

    assert first.correlation_id == "a" and second.correlation_id == "b"
    assert first.stage_reports == second.stage_reports


# --- F-02 remediation: the registration prerequisite fails closed on anything but a real bool ----
# (IRA-BAE-001-M1_Independent_Review.md F-02, probes P1/P2/P9.)


class ReturningRegistrationSource:
    """Returns exactly the given value from is_registered, whatever its type."""

    def __init__(self, value: object) -> None:
        self._value = value
        self.calls = 0

    async def is_registered(self, identifier: BusinessActivityIdentifier) -> object:
        self.calls += 1
        return self._value


def _engine_with_registration(source: object):
    authorizer = StubAuthorizer(AuthorizationDecision.ALLOW)
    engine = BusinessActivityEngine(
        registration_source=source,  # type: ignore[arg-type]
        authorizer=authorizer,
        manifest_resolver=ResolvedManifestResolver(),
    )
    return engine, authorizer


async def test_registration_true_proceeds_past_activity_resolution() -> None:
    engine, authorizer = _engine_with_registration(ReturningRegistrationSource(True))
    result = await engine.execute(_invocation())

    assert _status(result, PipelineStage.ACTIVITY_RESOLUTION) is StageStatus.COMPLETED
    assert len(authorizer.requests) == 1


async def test_registration_false_stops_with_activity_not_registered() -> None:
    engine, authorizer = _engine_with_registration(ReturningRegistrationSource(False))
    result = await engine.execute(_invocation())

    assert result.outcome is ExecutionOutcome.ACTIVITY_NOT_REGISTERED
    assert result.terminated_at is PipelineStage.ACTIVITY_RESOLUTION
    assert authorizer.requests == []


@pytest.mark.parametrize(
    "value",
    [None, "false", "False", "0", "true", "", 1, 0, {}, [], {"registered": True}, object(), MagicMock()],
    ids=lambda value: type(value).__name__ + ":" + repr(value)[:20],
)
async def test_non_boolean_registration_result_fails_closed(value: object) -> None:
    engine, authorizer = _engine_with_registration(ReturningRegistrationSource(value))
    result = await engine.execute(_invocation())

    assert result.outcome is ExecutionOutcome.EXECUTION_FAILED
    assert result.terminated_at is PipelineStage.ACTIVITY_RESOLUTION
    assert _status(result, PipelineStage.ACTIVITY_RESOLUTION) is StageStatus.TERMINATED
    assert authorizer.requests == []
    assert not result.succeeded


async def test_missing_registration_result_fails_closed() -> None:
    class ImplicitlyReturningRegistrationSource:
        async def is_registered(self, identifier: BusinessActivityIdentifier):  # returns nothing
            pass

    engine, authorizer = _engine_with_registration(ImplicitlyReturningRegistrationSource())
    result = await engine.execute(_invocation())

    assert result.outcome is ExecutionOutcome.EXECUTION_FAILED
    assert result.terminated_at is PipelineStage.ACTIVITY_RESOLUTION
    assert authorizer.requests == []


async def test_default_async_mock_registration_source_fails_closed() -> None:
    engine, authorizer = _engine_with_registration(AsyncMock())
    result = await engine.execute(_invocation())

    assert result.outcome is ExecutionOutcome.EXECUTION_FAILED
    assert authorizer.requests == []


async def test_registration_source_without_the_lookup_method_fails_closed() -> None:
    engine, authorizer = _engine_with_registration(object())
    result = await engine.execute(_invocation())

    assert result.outcome is ExecutionOutcome.EXECUTION_FAILED
    assert result.terminated_at is PipelineStage.ACTIVITY_RESOLUTION
    assert authorizer.requests == []


# --- F-03 remediation: contract-critical negative paths ------------------------------------------
# (IRA-BAE-001-M1_Independent_Review.md F-03, mutations M4, M9, M10.)

SPOOFING_PAYLOAD = {
    "identity_id": "spoofed-person",
    "organization_id": "spoofed-org",
    "membership_id": "spoofed-membership",
    "session_id": "spoofed-session",
}


async def test_identity_and_organization_come_from_the_invocation_claims_never_the_payload() -> None:
    engine, _, authorizer = _engine()
    await engine.execute(_invocation(payload=SPOOFING_PAYLOAD))

    (request,) = authorizer.requests
    assert request == AuthorizationRequest(
        identity_id="person-1", organization_id="org-1", membership_id="membership-1", session_id="session-1"
    )


@pytest.mark.parametrize("field", ["identity_id", "organization_id"])
async def test_payload_never_fills_in_a_blank_claim(field: str) -> None:
    engine, registration, authorizer = _engine()
    result = await engine.execute(_invocation(payload=SPOOFING_PAYLOAD, **{field: ""}))

    assert result.outcome is ExecutionOutcome.VALIDATION_FAILED
    assert result.terminated_at is PipelineStage.REQUEST_RECEPTION
    assert registration.calls == []
    assert authorizer.requests == []


async def test_manifest_resolver_exception_fails_closed_without_escaping() -> None:
    class RaisingManifestResolver:
        async def resolve(self, identifier: BusinessActivityIdentifier) -> ManifestResolution:
            raise RuntimeError("manifest store unavailable")

    authorizer = StubAuthorizer(AuthorizationDecision.ALLOW)
    engine = BusinessActivityEngine(
        registration_source=RecordingRegistrationSource(True),
        authorizer=authorizer,
        manifest_resolver=RaisingManifestResolver(),
    )
    result = await engine.execute(_invocation())

    assert result.outcome is ExecutionOutcome.EXECUTION_FAILED
    assert result.terminated_at is PipelineStage.ACTIVITY_RESOLUTION
    assert _status(result, PipelineStage.ACTIVITY_RESOLUTION) is StageStatus.TERMINATED
    assert "Manifest Resolution" in result.reason
    assert authorizer.requests == []
