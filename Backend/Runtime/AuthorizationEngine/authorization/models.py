"""
Authorization Runtime Engine -- Decision, Trace, and Context models.

WP-RTA-001 Milestone M1 (Authorization Evaluation Core), realizing
RTA-001 S11's own Authorization Decision (S11.8) and Authorization
Context (S11.5) constructs as shared Runtime data models -- owned by
no Business Capability (IRA-RTA-001 S9), consumed by any Business
Activity that constructs an Authorization Context and invokes the
Authorization Engine (RTA-001 S11.2).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AuthorizationTier(str, Enum):
    """URA-001-76's own five-tier Authorization Resolution Precedence, most specific first."""

    NAMED_USER = "NAMED_USER"
    GROUP = "GROUP"
    APPROVAL_AUTHORITY = "APPROVAL_AUTHORITY"
    BUSINESS_ROLE = "BUSINESS_ROLE"
    DOMAIN_PERMISSION = "DOMAIN_PERMISSION"


class AuthorizationDecision(str, Enum):
    """RTA-001 S11.8's own five-value Authorization Decision taxonomy."""

    ALLOW = "ALLOW"
    DENY = "DENY"
    CONDITIONAL = "CONDITIONAL"
    DELEGATED = "DELEGATED"
    ESCALATED = "ESCALATED"


class TierResult(str, Enum):
    """One precedence tier's own outcome, for the Runtime Trace (RTA-001 S11.15)."""

    MATCH = "MATCH"
    NO_MATCH = "NO_MATCH"
    NOT_EVALUATED = "NOT_EVALUATED"


@dataclass(frozen=True)
class AuthorizationContext:
    """
    RTA-001 S11.5's own Authorization Context. Constructed by the
    Business Activity Engine (never by this engine itself) and handed
    to the Authorization Engine as input; immutable throughout
    evaluation (S11.5: "Authorization Context shall remain immutable
    throughout execution" -- enforced here via a frozen dataclass).

    Field set matches S11.5 verbatim (Identity, Organization,
    Membership, Roles, Permissions, Assignments, Delegations, Approval
    Authorities, Enterprise Scope, Security Classification, Session
    Information, Effective Time). The concrete shape of "the specific
    governed request" being evaluated (e.g. a Domain Permission's own
    domain_id/permission_level) is deliberately not modeled here -- it
    is capability-specific vocabulary belonging to whichever
    TierResolver a future milestone binds (WP-RTA-001 M5), not to this
    shared, capability-agnostic context.
    """

    identity_id: str
    organization_id: str
    membership_id: str | None = None
    roles: tuple[str, ...] = field(default_factory=tuple)
    permissions: tuple[str, ...] = field(default_factory=tuple)
    assignments: tuple[str, ...] = field(default_factory=tuple)
    delegations: tuple[str, ...] = field(default_factory=tuple)
    approval_authorities: tuple[str, ...] = field(default_factory=tuple)
    enterprise_scope: str | None = None
    security_classification: str | None = None
    session_id: str | None = None
    effective_time: datetime | None = None


@dataclass(frozen=True)
class TierEvaluation:
    """One precedence tier's own trace entry (RTA-001 S11.15 Authorization Observability)."""

    tier: AuthorizationTier
    result: TierResult
    reason: str
    decision: AuthorizationDecision | None = None


@dataclass(frozen=True)
class EvaluationResult:
    """The Authorization Engine's own output (RTA-001 S11.8) -- one decision plus its full trace."""

    decision: AuthorizationDecision
    matched_tier: AuthorizationTier | None
    reason: str
    trace: tuple[TierEvaluation, ...]
