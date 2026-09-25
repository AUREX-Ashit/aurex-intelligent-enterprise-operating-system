"""
Business Activity Engine -- execution result and outcome classes (WP-BAE-001 M1).

Runtime failures are returned, never raised, so the result stays
transport-independent (`IMP-001 §6.16.15`); mapping an outcome to an
HTTP status belongs to the invoker adapter.

`ExecutionOutcome` keeps the failure classes distinct:
  * NOT_IMPLEMENTED -- execution reached a stage this milestone has
    not built. Never a success.
  * ACTIVITY_NOT_REGISTERED -- BAR holds no registration for the
    identifier (`IMP-001 §6.22.7`; `RO-M1-04`).
  * AUTHORIZATION_DENIED -- the Authorization Engine returned anything
    other than ALLOW (fail-closed).
  * VALIDATION_FAILED -- the invocation itself is structurally invalid.
  * EXECUTION_FAILED -- a collaborator raised, or the registration
    source returned something other than a bool; execution fails closed.
  * COMPLETED -- every stage completed. Unreachable in M1 by
    construction: `BusinessActivityExecutionResult` refuses a COMPLETED
    outcome unless all sixteen stages report COMPLETED.

Error classification per `IMP-001 §6.28.4` is a recorded M6 dependency
(`IRA-BAE-001-M1 §14.5`, D-06); these classes are not that taxonomy.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from authorization.models import EvaluationResult

from .identity import BusinessActivityIdentifier
from .pipeline import CANONICAL_ORDER, PipelineStage, StageReport, StageStatus


class ExecutionOutcome(str, Enum):
    COMPLETED = "COMPLETED"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    ACTIVITY_NOT_REGISTERED = "ACTIVITY_NOT_REGISTERED"
    AUTHORIZATION_DENIED = "AUTHORIZATION_DENIED"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    EXECUTION_FAILED = "EXECUTION_FAILED"


@dataclass(frozen=True)
class BusinessActivityExecutionResult:
    """One execution's outcome, with a report for every canonical stage in order."""

    identifier: BusinessActivityIdentifier
    correlation_id: str
    outcome: ExecutionOutcome
    terminated_at: PipelineStage | None
    reason: str
    stage_reports: tuple[StageReport, ...]
    authorization: EvaluationResult | None = None
    """The Authorization Engine's own result, unchanged, whenever authorization was evaluated."""

    def __post_init__(self) -> None:
        if tuple(report.stage for report in self.stage_reports) != CANONICAL_ORDER:
            raise ValueError("stage_reports must cover every canonical stage exactly once, in canonical order.")
        all_completed = all(report.status is StageStatus.COMPLETED for report in self.stage_reports)
        if (self.outcome is ExecutionOutcome.COMPLETED) != all_completed:
            raise ValueError("outcome is COMPLETED if and only if every stage reports COMPLETED.")
        if (self.outcome is ExecutionOutcome.COMPLETED) != (self.terminated_at is None):
            raise ValueError("terminated_at is None if and only if the outcome is COMPLETED.")

    @property
    def succeeded(self) -> bool:
        return self.outcome is ExecutionOutcome.COMPLETED
