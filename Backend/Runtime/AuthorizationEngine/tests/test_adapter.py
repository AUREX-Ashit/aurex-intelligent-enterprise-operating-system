"""
Unit tests for WP-RTA-001 Milestone M4 -- Runtime Integration Adapters.

Proves: the adapter correctly builds AuthorizationContext, invokes
EvaluationPipeline, returns EvaluationResult unchanged, the runtime
package remains independent of the adapter package (dependency
direction), and invalid requests fail cleanly. No database, no
FastAPI, no Business Activity, no WP-05 integration.
"""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

import pytest

from adapters import AuthorizationAdapter, AuthorizationRequest, InvalidAuthorizationRequestError
from authorization import (
    AuthorizationContext,
    AuthorizationDecision,
    AuthorizationTier,
    DomainPermissionResolver,
    EvaluationPipeline,
    EvaluationResult,
    ResolverRegistry,
    TierResolution,
)


def _request(**overrides) -> AuthorizationRequest:
    defaults = dict(identity_id="person-1", organization_id="org-1")
    defaults.update(overrides)
    return AuthorizationRequest(**defaults)


def _stub_domain_permission_resolver(outcome: TierResolution | None):
    class _Stub(DomainPermissionResolver):
        async def resolve(self, context: AuthorizationContext) -> TierResolution | None:
            return outcome

    return _Stub()


class _FakePipeline:
    """Spy pipeline -- proves the adapter delegates to it rather than deciding anything itself."""

    def __init__(self, result: EvaluationResult) -> None:
        self._result = result
        self.received_context: AuthorizationContext | None = None
        self.call_count = 0

    async def execute(self, context: AuthorizationContext) -> EvaluationResult:
        self.call_count += 1
        self.received_context = context
        return self._result


_ARBITRARY_RESULT = EvaluationResult(
    decision=AuthorizationDecision.ESCALATED,
    matched_tier=AuthorizationTier.APPROVAL_AUTHORITY,
    reason="arbitrary fake reason, unrelated to any real evaluation",
    trace=(),
)


# ---------------------------------------------------------------------------
# Context construction (translation)
# ---------------------------------------------------------------------------


def test_adapter_builds_context_with_every_field_mapped_correctly() -> None:
    request = _request(
        identity_id="person-42",
        organization_id="org-42",
        membership_id="membership-42",
        roles=("ORG_ADMIN",),
        permissions=("finance:view",),
        assignments=("assignment-1",),
        delegations=("delegation-1",),
        approval_authorities=("approval-1",),
        enterprise_scope="scope-1",
        security_classification="Internal",
        session_id="session-1",
    )
    adapter = AuthorizationAdapter(pipeline=_FakePipeline(_ARBITRARY_RESULT))

    context = adapter.build_context(request)

    assert context.identity_id == "person-42"
    assert context.organization_id == "org-42"
    assert context.membership_id == "membership-42"
    assert context.roles == ("ORG_ADMIN",)
    assert context.permissions == ("finance:view",)
    assert context.assignments == ("assignment-1",)
    assert context.delegations == ("delegation-1",)
    assert context.approval_authorities == ("approval-1",)
    assert context.enterprise_scope == "scope-1"
    assert context.security_classification == "Internal"
    assert context.session_id == "session-1"


def test_context_built_by_adapter_is_still_immutable() -> None:
    adapter = AuthorizationAdapter(pipeline=_FakePipeline(_ARBITRARY_RESULT))
    context = adapter.build_context(_request())

    with pytest.raises(Exception):
        context.identity_id = "someone-else"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Invocation and pass-through
# ---------------------------------------------------------------------------


async def test_adapter_invokes_the_pipeline_exactly_once_with_the_built_context() -> None:
    fake_pipeline = _FakePipeline(_ARBITRARY_RESULT)
    adapter = AuthorizationAdapter(pipeline=fake_pipeline)
    request = _request(identity_id="person-7", organization_id="org-7")

    await adapter.evaluate(request)

    assert fake_pipeline.call_count == 1
    assert fake_pipeline.received_context is not None
    assert fake_pipeline.received_context.identity_id == "person-7"
    assert fake_pipeline.received_context.organization_id == "org-7"


async def test_adapter_returns_the_pipeline_result_unchanged() -> None:
    """The adapter never inspects, branches on, or re-derives the decision -- it returns exactly what the pipeline returned."""
    fake_pipeline = _FakePipeline(_ARBITRARY_RESULT)
    adapter = AuthorizationAdapter(pipeline=fake_pipeline)

    result = await adapter.evaluate(_request())

    assert result is _ARBITRARY_RESULT


async def test_adapter_end_to_end_with_a_real_pipeline() -> None:
    """Not just a mocked interaction -- proves the full seam wires correctly against real M1-M3 components."""
    registry = ResolverRegistry().register(
        _stub_domain_permission_resolver(TierResolution(AuthorizationDecision.ALLOW, "active grant"))
    )
    pipeline = EvaluationPipeline(registry)
    adapter = AuthorizationAdapter(pipeline=pipeline)

    result = await adapter.evaluate(_request())

    assert result.decision == AuthorizationDecision.ALLOW
    assert result.matched_tier == AuthorizationTier.DOMAIN_PERMISSION
    assert len(result.trace) == 5


# ---------------------------------------------------------------------------
# Invalid requests fail cleanly
# ---------------------------------------------------------------------------


def test_blank_identity_id_fails_cleanly() -> None:
    adapter = AuthorizationAdapter(pipeline=_FakePipeline(_ARBITRARY_RESULT))

    with pytest.raises(InvalidAuthorizationRequestError):
        adapter.build_context(_request(identity_id="   "))


def test_blank_organization_id_fails_cleanly() -> None:
    adapter = AuthorizationAdapter(pipeline=_FakePipeline(_ARBITRARY_RESULT))

    with pytest.raises(InvalidAuthorizationRequestError):
        adapter.build_context(_request(organization_id=""))


async def test_invalid_request_never_reaches_the_pipeline() -> None:
    """Fail cleanly means fail *before* invoking the runtime, not after."""
    fake_pipeline = _FakePipeline(_ARBITRARY_RESULT)
    adapter = AuthorizationAdapter(pipeline=fake_pipeline)

    with pytest.raises(InvalidAuthorizationRequestError):
        await adapter.evaluate(_request(identity_id=""))

    assert fake_pipeline.call_count == 0


# ---------------------------------------------------------------------------
# Dependency direction: the runtime must never depend on the adapter
# ---------------------------------------------------------------------------


def test_authorization_runtime_package_never_imports_the_adapters_package() -> None:
    """
    AST-based, not string-based (defect found and fixed during M5): a naive
    substring search on "adapters" false-positives on any docstring/comment
    that merely *mentions* the package name (e.g. to explain the dependency
    direction) without actually importing it. Only real `import adapters`
    / `from adapters import ...` statements should fail this test.
    """
    authorization_dir = Path(inspect.getfile(AuthorizationContext)).parent

    for source_file in authorization_dir.glob("*.py"):
        tree = ast.parse(source_file.read_text(encoding="utf-8"), filename=str(source_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                imported_names = [node.module] if node.module else []
            else:
                continue

            for name in imported_names:
                assert not (name == "adapters" or name.startswith("adapters.")), (
                    f"{source_file.name} imports from 'adapters' -- the runtime must never depend on the adapter layer."
                )
