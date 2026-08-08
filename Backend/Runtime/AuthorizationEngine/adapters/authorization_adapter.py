"""
Authorization Adapter (WP-RTA-001 M4).

Translation only, never a decision. Accepts an AuthorizationRequest
(this adapter's own public input type, deliberately distinct from
`authorization.AuthorizationContext`), builds the immutable
AuthorizationContext the runtime actually consumes, invokes
EvaluationPipeline (M3, unmodified), and returns its EvaluationResult
unchanged. `AuthorizationDecision` is never inspected, compared, or
branched on anywhere in this module -- an authorization decision is
exclusively AuthorizationEngine's own job (RTA-001 S11.2), never
this adapter's.

Dependency direction: this module imports from `authorization`;
`authorization` never imports from this module or this package. See
`Backend/Runtime/AuthorizationEngine/adapters/__init__.py` and
`tests/test_adapter.py`'s own dependency-direction test.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from authorization import AuthorizationContext, EvaluationResult
from authorization.pipeline import EvaluationPipeline


class InvalidAuthorizationRequestError(Exception):
    """Raised when an AuthorizationRequest is missing a required, non-blank field. A translation-layer failure, never an authorization decision."""


@dataclass(frozen=True)
class AuthorizationRequest:
    """
    This adapter's own public input type -- what a future caller
    (a Business Activity, not integrated by this milestone) supplies.

    Deliberately a distinct type from `AuthorizationContext`, even
    though today's field set mirrors it field-for-field: no caller-side
    vocabulary has been established yet (Business Activity integration
    is explicitly out of this milestone's scope), so the honest,
    undecorated translation is a direct mapping. The architectural
    value is the seam itself -- one translation point, so a future
    change to AuthorizationContext's own shape need only be absorbed
    here, never by every caller -- not that today's mapping is complex.
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


class AuthorizationAdapter:
    """
    The stable interface a future Business Activity depends on.
    Constructor-injected with an EvaluationPipeline (M3, unmodified) --
    this adapter never constructs a pipeline, engine, or resolver
    itself, and never queries a database, calls an API, or accesses a
    repository (all remain out of scope, per instruction).
    """

    def __init__(self, pipeline: EvaluationPipeline) -> None:
        self._pipeline = pipeline

    def build_context(self, request: AuthorizationRequest) -> AuthorizationContext:
        """Translate an AuthorizationRequest into the runtime's own AuthorizationContext. Raises on a blank required field; never guesses a default identity/organization."""
        self._validate(request)
        return AuthorizationContext(
            identity_id=request.identity_id,
            organization_id=request.organization_id,
            membership_id=request.membership_id,
            roles=request.roles,
            permissions=request.permissions,
            assignments=request.assignments,
            delegations=request.delegations,
            approval_authorities=request.approval_authorities,
            enterprise_scope=request.enterprise_scope,
            security_classification=request.security_classification,
            session_id=request.session_id,
            effective_time=request.effective_time,
        )

    async def evaluate(self, request: AuthorizationRequest) -> EvaluationResult:
        """Build the context, invoke the pipeline, and return its EvaluationResult unchanged -- no inspection, no branching on the decision."""
        context = self.build_context(request)
        return await self._pipeline.execute(context)

    @staticmethod
    def _validate(request: AuthorizationRequest) -> None:
        if not request.identity_id or not request.identity_id.strip():
            raise InvalidAuthorizationRequestError("AuthorizationRequest.identity_id is required and must not be blank.")
        if not request.organization_id or not request.organization_id.strip():
            raise InvalidAuthorizationRequestError("AuthorizationRequest.organization_id is required and must not be blank.")
