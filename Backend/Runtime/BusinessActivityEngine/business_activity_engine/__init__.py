"""
Business Activity Engine (WP-BAE-001).

`IMP-001 §6.15`–`§6.19`'s Business Activity Engine -- shared Runtime
infrastructure, owned by no Business Capability (`IRA-BAE-001 §9`).
Placement, pipeline ordering, and Manifest Resolution ownership are
fixed by ADR-042.

M1 -- Runtime Contract / Architecture Baseline: the transport-
independent entry point, BAR-issued identity, the canonical sixteen-
stage pipeline skeleton, the invocation/context/result contracts, the
execution-state vocabulary, and the injected collaborator boundaries
(BAR registration, Manifest Resolution, Authorization, Transaction).
Every stage M1 does not build reports NOT_IMPLEMENTED.

Requires the Authorization Runtime Engine (`Backend/Runtime/
AuthorizationEngine`) to be importable by the host (TD-165).
"""

from .context import BusinessActivityContext, BusinessActivityInvocation, ContextSection
from .engine import BusinessActivityEngine
from .identity import BusinessActivityIdentifier, InvalidBusinessActivityIdentifierError
from .pipeline import CANONICAL_ORDER, PipelineStage, StageReport, StageStatus
from .ports import (
    Authorizer,
    ManifestResolution,
    ManifestResolutionStatus,
    ManifestResolver,
    RegistrationSource,
    TransactionBoundary,
    UnimplementedManifestResolver,
)
from .results import BusinessActivityExecutionResult, ExecutionOutcome
from .state import AUTHORITATIVE_TRANSITIONS, ExecutionState

__all__ = [
    "AUTHORITATIVE_TRANSITIONS",
    "Authorizer",
    "BusinessActivityContext",
    "BusinessActivityEngine",
    "BusinessActivityExecutionResult",
    "BusinessActivityIdentifier",
    "BusinessActivityInvocation",
    "CANONICAL_ORDER",
    "ContextSection",
    "ExecutionOutcome",
    "ExecutionState",
    "InvalidBusinessActivityIdentifierError",
    "ManifestResolution",
    "ManifestResolutionStatus",
    "ManifestResolver",
    "PipelineStage",
    "RegistrationSource",
    "StageReport",
    "StageStatus",
    "TransactionBoundary",
    "UnimplementedManifestResolver",
]
