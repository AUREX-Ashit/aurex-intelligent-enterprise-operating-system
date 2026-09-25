"""
Business Activity Engine -- runtime entry point (WP-BAE-001 M1 skeleton).

One transport-independent entry point, `BusinessActivityEngine.execute()`,
running in-process within the hosting service (ADR-042 / `RO-M1-01`).
It walks `IMP-001 §6.16.3`'s stages in canonical order (ADR-042 /
`RO-M1-02`) and stops at the first stage that does not complete.

What the M1 skeleton actually does, stage by stage:
  1. REQUEST_RECEPTION -- structural validation of the invocation
     (VALIDATION_FAILED on a blank identity/organization).
  2. ACTIVITY_RESOLUTION -- consumes BAR registration state through the
     read-only `RegistrationSource`: only `True` proceeds, `False` gives
     ACTIVITY_NOT_REGISTERED, and any non-bool answer fails closed as
     EXECUTION_FAILED. Then Manifest Resolution through `ManifestResolver`. The shipped
     resolver reports NOT_IMPLEMENTED (M2), so real executions end here.
  3. EXECUTION_CONTEXT_INITIALIZATION -- builds the immutable context
     once, from the invocation only (M1 subset; full context is M3).
  4. AUTHORIZATION_EVALUATION -- builds an `AuthorizationRequest` and
     invokes the injected `Authorizer` (the existing Authorization
     Engine contract, unmodified). Any decision other than ALLOW, or
     any exception, fails closed.
  5. onward -- NOT_IMPLEMENTED. Business Rule Execution is never
     reached in M1; no transaction is opened or committed.

Collaborator exceptions are caught at the stage that raised them and
reported as EXECUTION_FAILED -- execution fails closed rather than
propagating an unclassified error across the invocation boundary.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from uuid import uuid4

from adapters.authorization_adapter import AuthorizationRequest
from authorization.models import AuthorizationDecision, EvaluationResult

from .context import BusinessActivityContext, BusinessActivityInvocation
from .identity import BusinessActivityIdentifier
from .pipeline import CANONICAL_ORDER, PipelineStage, StageReport, StageStatus
from .ports import (
    Authorizer,
    ManifestResolutionStatus,
    ManifestResolver,
    RegistrationSource,
    UnimplementedManifestResolver,
)
from .results import BusinessActivityExecutionResult, ExecutionOutcome

_logger = logging.getLogger("business_activity_engine")

_FIRST_UNIMPLEMENTED_STAGE = PipelineStage.INPUT_CONTRACT_VALIDATION


class BusinessActivityEngine:
    """The canonical execution path for BAE-routed Business Activities (`IMP-001 §6.15`)."""

    def __init__(
        self,
        registration_source: RegistrationSource,
        authorizer: Authorizer,
        manifest_resolver: ManifestResolver | None = None,
    ) -> None:
        self._registration_source = registration_source
        self._authorizer = authorizer
        self._manifest_resolver = manifest_resolver or UnimplementedManifestResolver()

    async def execute(self, invocation: BusinessActivityInvocation) -> BusinessActivityExecutionResult:
        run = _Run(invocation.identifier, invocation.correlation_id or str(uuid4()))
        result = await self._run_pipeline(invocation, run)
        _logger.info(
            json.dumps(
                {
                    "business_activity_execution": True,
                    "identifier": str(result.identifier),
                    "correlation_id": result.correlation_id,
                    "outcome": result.outcome.value,
                    "terminated_at": result.terminated_at.value if result.terminated_at else None,
                }
            )
        )
        return result

    async def _run_pipeline(
        self, invocation: BusinessActivityInvocation, run: _Run
    ) -> BusinessActivityExecutionResult:
        # 1. Request Reception
        problem = _invocation_problem(invocation)
        if problem is not None:
            return run.terminate(PipelineStage.REQUEST_RECEPTION, ExecutionOutcome.VALIDATION_FAILED, problem)
        run.complete(PipelineStage.REQUEST_RECEPTION, "Invocation accepted.")

        # 2. Activity Resolution -- registration prerequisite, then Manifest Resolution
        stage = PipelineStage.ACTIVITY_RESOLUTION
        try:
            registered = await self._registration_source.is_registered(invocation.identifier)
        except Exception as exc:
            return run.fail(stage, "Registration lookup", exc)
        # Strict identity checks, never truthiness: only a real `True` proceeds
        # (IRA-BAE-001-M1_Independent_Review.md F-02).
        if registered is False:
            return run.terminate(
                stage,
                ExecutionOutcome.ACTIVITY_NOT_REGISTERED,
                f"{invocation.identifier} is not registered in BAR and cannot execute.",
            )
        if registered is not True:
            return run.terminate(
                stage,
                ExecutionOutcome.EXECUTION_FAILED,
                f"Registration lookup returned {type(registered).__name__}, not bool; failing closed.",
            )
        try:
            manifest = await self._manifest_resolver.resolve(invocation.identifier)
        except Exception as exc:
            return run.fail(stage, "Manifest Resolution", exc)
        if manifest.status is not ManifestResolutionStatus.RESOLVED:
            return run.not_implemented(stage, manifest.reason)
        run.complete(stage, "Registered; manifest resolved.")

        # 3. Execution Context Initialization -- exactly once, by the engine
        context = BusinessActivityContext(
            identifier=invocation.identifier,
            identity_id=invocation.identity_id,
            organization_id=invocation.organization_id,
            membership_id=invocation.membership_id,
            session_id=invocation.session_id,
            correlation_id=run.correlation_id,
            started_at=datetime.now(timezone.utc),
        )
        run.complete(
            PipelineStage.EXECUTION_CONTEXT_INITIALIZATION,
            "Context constructed; unavailable sections: "
            + ", ".join(section.value for section in context.unavailable_sections)
            + ".",
        )

        # 4. Authorization Evaluation -- the Authorization Engine decides; fail closed
        stage = PipelineStage.AUTHORIZATION_EVALUATION
        try:
            evaluation = await self._authorizer.evaluate(_authorization_request(context))
        except Exception as exc:
            return run.fail(stage, "Authorization evaluation", exc)
        if evaluation.decision is not AuthorizationDecision.ALLOW:
            return run.terminate(
                stage,
                ExecutionOutcome.AUTHORIZATION_DENIED,
                f"Authorization decision {evaluation.decision.value}: {evaluation.reason}",
                authorization=evaluation,
            )
        run.complete(stage, f"Authorization decision ALLOW: {evaluation.reason}", authorization=evaluation)

        # 5+. Not built in M1
        return run.not_implemented(
            _FIRST_UNIMPLEMENTED_STAGE,
            f"{_FIRST_UNIMPLEMENTED_STAGE.value} is not implemented in WP-BAE-001 M1.",
        )


def _invocation_problem(invocation: BusinessActivityInvocation) -> str | None:
    if not isinstance(invocation.identity_id, str) or not invocation.identity_id.strip():
        return "identity_id is required and must not be blank."
    if not isinstance(invocation.organization_id, str) or not invocation.organization_id.strip():
        return "organization_id is required and must not be blank."
    return None


def _authorization_request(context: BusinessActivityContext) -> AuthorizationRequest:
    return AuthorizationRequest(
        identity_id=context.identity_id,
        organization_id=context.organization_id,
        membership_id=context.membership_id,
        session_id=context.session_id,
    )


class _Run:
    """Per-execution report accumulator. Never shared between executions."""

    def __init__(self, identifier: BusinessActivityIdentifier, correlation_id: str) -> None:
        self.identifier = identifier
        self.correlation_id = correlation_id
        self._reports: list[StageReport] = []
        self._authorization: EvaluationResult | None = None

    def complete(self, stage: PipelineStage, reason: str, authorization: EvaluationResult | None = None) -> None:
        self._append(stage, StageStatus.COMPLETED, reason)
        if authorization is not None:
            self._authorization = authorization

    def not_implemented(self, stage: PipelineStage, reason: str) -> BusinessActivityExecutionResult:
        self._append(stage, StageStatus.NOT_IMPLEMENTED, reason)
        return self._finish(stage, ExecutionOutcome.NOT_IMPLEMENTED, reason)

    def terminate(
        self,
        stage: PipelineStage,
        outcome: ExecutionOutcome,
        reason: str,
        authorization: EvaluationResult | None = None,
    ) -> BusinessActivityExecutionResult:
        self._append(stage, StageStatus.TERMINATED, reason)
        if authorization is not None:
            self._authorization = authorization
        return self._finish(stage, outcome, reason)

    def fail(self, stage: PipelineStage, step: str, exc: Exception) -> BusinessActivityExecutionResult:
        _logger.exception("%s failed at %s (correlation_id=%s)", step, stage.value, self.correlation_id)
        return self.terminate(stage, ExecutionOutcome.EXECUTION_FAILED, f"{step} raised {type(exc).__name__}: {exc}")

    def _append(self, stage: PipelineStage, status: StageStatus, reason: str) -> None:
        expected = CANONICAL_ORDER[len(self._reports)]
        if stage is not expected:
            raise RuntimeError(f"Stage {stage.value} reported out of canonical order (expected {expected.value}).")
        self._reports.append(StageReport(stage, status, reason))

    def _finish(
        self, stage: PipelineStage, outcome: ExecutionOutcome, reason: str
    ) -> BusinessActivityExecutionResult:
        remaining = CANONICAL_ORDER[len(self._reports):]
        reports = tuple(self._reports) + tuple(
            StageReport(later, StageStatus.NOT_REACHED, f"Not reached: execution ended at {stage.value}.")
            for later in remaining
        )
        return BusinessActivityExecutionResult(
            identifier=self.identifier,
            correlation_id=self.correlation_id,
            outcome=outcome,
            terminated_at=stage,
            reason=reason,
            stage_reports=reports,
            authorization=self._authorization,
        )
