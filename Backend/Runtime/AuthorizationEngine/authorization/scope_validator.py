"""
Enterprise Scope Validation (WP-RTA-001 M5).

RTA-001 S11.12: "Authorization decisions shall be evaluated within the
resolved Enterprise Context... Authorization shall never be evaluated
outside Enterprise Context." This module performs a structural,
pre-evaluation check that the Enterprise Context attributes an
AuthorizationContext claims to carry are actually present and
well-formed. It never makes a database call, never resolves real
Enterprise structure (ERG-001), and never produces an
AuthorizationDecision -- validation remains architecturally separate
from evaluation (this milestone's own Architectural Rule).

Disclosed simplification (see IMP-REPORT-WP-RTA-001 M5 for full
detail): RTA-001 S11.7's own canonical Authorization Resolution
Pipeline places Enterprise Scope Validation between Delegation
Evaluation and Approval Authority Evaluation, inside the five-tier
precedence walk. This milestone instead runs it once, before
evaluation begins, per this milestone's own explicit instruction
("validation of authorization scope before evaluation proceeds") --
threading it into the middle of AuthorizationEngine's own precedence
loop would mean redesigning M1's already-implemented evaluation
pipeline, which this milestone's own instruction prohibits. Validation
never consults or influences a precedence tier either way, so this
placement still satisfies S11.12's substantive guarantee (authorization
is never evaluated against an unvalidated Enterprise Context), even
though its position relative to Delegation/Approval-Authority
evaluation differs from S11.7's own literal step sequence.

Deliberately narrow scope (no persistence, per instruction): only
structural presence/well-formedness is checked here -- whether
`enterprise_scope` names a real, existing node under `organization_id`
in ERG-001's own structure is a materially different, data-backed
question this module does not answer, since answering it would require
real repository/persistence access, explicitly out of this milestone's
scope.
"""

from __future__ import annotations

from .models import AuthorizationContext


class EnterpriseScopeValidationError(Exception):
    """Raised when an AuthorizationContext's Enterprise Scope attributes are missing or malformed. A validation failure, never an authorization decision."""


class EnterpriseScopeValidator:
    """
    Structural Enterprise Scope validation only. Stateless -- safe to
    share a single instance across every evaluation (the default
    `EvaluationPipeline` does exactly this).
    """

    def validate(self, context: AuthorizationContext) -> None:
        """Raise EnterpriseScopeValidationError on a missing or malformed scope attribute; return None otherwise. Never returns a value the caller could mistake for a decision."""
        if not context.organization_id or not context.organization_id.strip():
            raise EnterpriseScopeValidationError(
                "AuthorizationContext.organization_id is required for Enterprise Scope Validation "
                "(RTA-001 S11.12) and must not be blank."
            )

        if context.enterprise_scope is not None and not context.enterprise_scope.strip():
            raise EnterpriseScopeValidationError(
                "AuthorizationContext.enterprise_scope, when provided, must not be blank -- "
                "an empty scope value is malformed, not the same as an absent one."
            )
