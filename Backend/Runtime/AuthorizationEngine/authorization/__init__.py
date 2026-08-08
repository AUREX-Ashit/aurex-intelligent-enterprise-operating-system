"""
Authorization Runtime Engine (WP-RTA-001).

RTA-001 S3.8/S11's own Authorization Engine -- shared Runtime
infrastructure, owned by no Business Capability, consumed by any
Business Activity that constructs an Authorization Context and invokes
it (RTA-001 S11.2). See IRA-RTA-001 and WP-RTA-001 for the full
constitutional charter this module implements.

M1 -- Authorization Evaluation Core: engine, models, generic
TierResolver Protocol.
M2 -- Runtime Resolver Framework: tier-specific resolver interfaces
(URA-001-76's own five, verified) and the injectable ResolverRegistry.
M3 -- Runtime Evaluation Pipeline & Resolver Orchestration: assembly,
discovery, and the PipelineObserver extension seam, wrapping the
unmodified M1 engine.
M4 -- (adapters, in the sibling `adapters` package -- not re-exported
here, per the one-way dependency direction: `authorization` never
imports from `adapters`.)
M5 -- Runtime Completeness: Enterprise Scope Validation
(pre-evaluation, wired into EvaluationPipeline) and Runtime
Observability (a concrete PipelineObserver). EvaluationPipeline's own
`execute()` gained scope validation and observer-failure isolation
this milestone -- see `pipeline.py`'s own docstring.
"""

from .engine import AuthorizationEngine
from .models import (
    AuthorizationContext,
    AuthorizationDecision,
    AuthorizationTier,
    EvaluationResult,
    TierEvaluation,
    TierResult,
)
from .observability import ObservabilityEvent, ObservabilityEventType, RuntimeObservabilityCollector
from .orchestrator import PipelineConfigurationError, ResolverOrchestrator
from .pipeline import EvaluationPipeline, PipelineExecution, PipelineObserver
from .registry import DuplicateResolverError, ResolverRegistry
from .resolvers import TierResolution, TierResolver
from .scope_validator import EnterpriseScopeValidationError, EnterpriseScopeValidator
from .tier_resolvers import (
    ApprovalAuthorityResolver,
    BaseTierResolver,
    BusinessRoleResolver,
    DomainPermissionResolver,
    GroupResolver,
    NamedUserResolver,
)

__all__ = [
    "AuthorizationEngine",
    "AuthorizationContext",
    "AuthorizationDecision",
    "AuthorizationTier",
    "EvaluationResult",
    "TierEvaluation",
    "TierResult",
    "TierResolver",
    "TierResolution",
    "BaseTierResolver",
    "NamedUserResolver",
    "GroupResolver",
    "ApprovalAuthorityResolver",
    "BusinessRoleResolver",
    "DomainPermissionResolver",
    "ResolverRegistry",
    "DuplicateResolverError",
    "ResolverOrchestrator",
    "PipelineConfigurationError",
    "EvaluationPipeline",
    "PipelineExecution",
    "PipelineObserver",
    "EnterpriseScopeValidator",
    "EnterpriseScopeValidationError",
    "RuntimeObservabilityCollector",
    "ObservabilityEvent",
    "ObservabilityEventType",
]
