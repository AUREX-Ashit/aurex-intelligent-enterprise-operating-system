"""
Business Activity Engine -- canonical execution pipeline (WP-BAE-001 M1).

`PipelineStage` enumerates `IMP-001 §6.16.3`'s sixteen stages in their
canonical order, which ADR-042 (`RO-M1-02`) makes the ordering
authority for the BAE. Enum definition order IS the execution order;
`CANONICAL_ORDER` exposes it explicitly.

Deliberately absent (not stages under `§6.16.3`):
  * Manifest Resolution -- performed inside ACTIVITY_RESOLUTION
    (ADR-042 / `RO-M1-03`; `IMP-001 §6.16.5`).
  * Knowledge Graph Update (`RTA-001 §6.5`) -- stage membership is an
    unresolved, deferred question (`IRA-BAE-001-M1 §14.4`, `R-01`) and
    is not added here.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PipelineStage(str, Enum):
    """`IMP-001 §6.16.3`, verbatim, in canonical order."""

    REQUEST_RECEPTION = "REQUEST_RECEPTION"
    ACTIVITY_RESOLUTION = "ACTIVITY_RESOLUTION"
    EXECUTION_CONTEXT_INITIALIZATION = "EXECUTION_CONTEXT_INITIALIZATION"
    AUTHORIZATION_EVALUATION = "AUTHORIZATION_EVALUATION"
    INPUT_CONTRACT_VALIDATION = "INPUT_CONTRACT_VALIDATION"
    BUSINESS_VALIDATION = "BUSINESS_VALIDATION"
    METADATA_RESOLUTION = "METADATA_RESOLUTION"
    WORKFLOW_RESOLUTION = "WORKFLOW_RESOLUTION"
    BUSINESS_RULE_EXECUTION = "BUSINESS_RULE_EXECUTION"
    PERSISTENCE_COORDINATION = "PERSISTENCE_COORDINATION"
    TRANSACTION_COMMIT = "TRANSACTION_COMMIT"
    DOMAIN_EVENT_PUBLICATION = "DOMAIN_EVENT_PUBLICATION"
    NOTIFICATION_PROCESSING = "NOTIFICATION_PROCESSING"
    AUDIT_RECORDING = "AUDIT_RECORDING"
    AI_ASSISTANCE_HOOKS = "AI_ASSISTANCE_HOOKS"
    RESPONSE_GENERATION = "RESPONSE_GENERATION"


CANONICAL_ORDER: tuple[PipelineStage, ...] = tuple(PipelineStage)


class StageStatus(str, Enum):
    """One stage's own outcome within one execution."""

    COMPLETED = "COMPLETED"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    TERMINATED = "TERMINATED"
    NOT_REACHED = "NOT_REACHED"


@dataclass(frozen=True)
class StageReport:
    """What happened at one stage. Every execution reports all sixteen, in canonical order."""

    stage: PipelineStage
    status: StageStatus
    reason: str
