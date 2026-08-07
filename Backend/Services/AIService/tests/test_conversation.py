# tests/test_conversation.py
"""
WP-12 BA-01 — Establish and Manage Conversation Lifecycle (`IRA-012 §5`).
Covers the Mandatory Tenant-Isolation Test Checklist (`CLAUDE.md §21.4`)
and the structural state-transition guarantee `ADR-020` Decision 2 and
`services/conversation_state_resolver.py` establish.
"""
from datetime import datetime, timedelta, timezone

import pytest
from httpx import AsyncClient
from jose import jwt

from config.settings import settings
from services.conversation_state_resolver import (
    ConversationStateResolver,
    ConversationTransitionTrigger,
    InvalidConversationTransition,
)
import services.interaction_state_assembler as interaction_state_assembler_module

_ORG_A = "33333333-3333-3333-3333-333333333333"
_ORG_B = "99999999-9999-9999-9999-999999999999"
_PERSON = "11111111-1111-1111-1111-111111111111"


def _token(organization_id: str = _ORG_A, role_code: str = "PLATFORM_ADMIN") -> str:
    claims = {
        "person_id": _PERSON,
        "identity_id": "22222222-2222-2222-2222-222222222222",
        "organization_id": organization_id,
        "membership_id": "44444444-4444-4444-4444-444444444444",
        "role_code": role_code,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=60),
    }
    return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def _auth(organization_id: str = _ORG_A, role_code: str = "PLATFORM_ADMIN") -> dict:
    return {"Authorization": f"Bearer {_token(organization_id, role_code)}"}


# ---------------------------------------------------------------------------
# ConversationStateResolver — unit, structural (no DB, no HTTP)
# ---------------------------------------------------------------------------

def test_resolver_allows_open_to_closed_via_explicit_action():
    resolver = ConversationStateResolver()
    assert resolver.resolve("OPEN", "CLOSED", ConversationTransitionTrigger.EXPLICIT_ACTION) == "CLOSED"


def test_resolver_allows_open_to_closed_via_runtime_policy():
    resolver = ConversationStateResolver()
    assert resolver.resolve("OPEN", "CLOSED", ConversationTransitionTrigger.RUNTIME_POLICY) == "CLOSED"


def test_resolver_rejects_closed_to_closed_no_reopen_path():
    """CLOSED is terminal for this Work Package's own scope (TDS-012 §2)."""
    resolver = ConversationStateResolver()
    with pytest.raises(InvalidConversationTransition):
        resolver.resolve("CLOSED", "OPEN", ConversationTransitionTrigger.EXPLICIT_ACTION)


def test_resolver_never_transitions_without_a_recognized_trigger():
    """A transition is never reachable except from an actual, recognized trigger — never a default (ADR-020 Decision 2)."""
    resolver = ConversationStateResolver()
    with pytest.raises(InvalidConversationTransition):
        resolver.resolve("OPEN", "CLOSED", trigger="SOMETHING_ELSE")  # type: ignore[arg-type]


def test_state_assembler_has_no_memory_dependency():
    """
    Structural test (IMP-001 §13.36/§13.51 boundary discipline): asserts no
    Memory-related *symbol* is importable from InteractionStateAssembler's
    own module namespace — checks the actual import graph (what the module
    can reach), not its own prose docstring, which legitimately discusses
    the exclusion in words. Mirrors IMP-TEST-006's own vendor-SDK-absence
    check pattern.
    """
    module_symbols = [name for name in dir(interaction_state_assembler_module) if not name.startswith("_")]
    memory_related = [name for name in module_symbols if "memory" in name.lower()]
    assert memory_related == [], f"Unexpected Memory-related symbol(s) reachable: {memory_related}"


# ---------------------------------------------------------------------------
# API — BA-01
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_establish_creates_conversation_in_open_state(client: AsyncClient):
    response = await client.post("/conversations", headers=_auth())
    assert response.status_code == 201
    body = response.json()
    assert body["state"] == "OPEN"
    assert body["closed_at"] is None


@pytest.mark.asyncio
async def test_close_transitions_to_closed_with_explicit_action_reason(client: AsyncClient):
    established = await client.post("/conversations", headers=_auth())
    conversation_id = established.json()["conversation_id"]

    response = await client.post(f"/conversations/{conversation_id}/close", headers=_auth())
    assert response.status_code == 200
    body = response.json()
    assert body["state"] == "CLOSED"
    assert body["state_transition_reason"] == "EXPLICIT_ACTION"
    assert body["closed_at"] is not None


@pytest.mark.asyncio
async def test_close_on_already_closed_conversation_returns_409_not_a_silent_noop(client: AsyncClient):
    established = await client.post("/conversations", headers=_auth())
    conversation_id = established.json()["conversation_id"]
    await client.post(f"/conversations/{conversation_id}/close", headers=_auth())

    second_close = await client.post(f"/conversations/{conversation_id}/close", headers=_auth())
    assert second_close.status_code == 409


@pytest.mark.asyncio
async def test_establish_requires_authentication(client: AsyncClient):
    response = await client.post("/conversations")
    assert response.status_code == 400  # missing Authorization header, per dependencies.get_current_claims


@pytest.mark.asyncio
async def test_establish_requires_platform_admin(client: AsyncClient):
    """TDS-012 §8: write-path persona gate left PLATFORM_ADMIN-only (TD-candidate-E)."""
    response = await client.post("/conversations", headers=_auth(role_code="MEMBER"))
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_close_requires_platform_admin(client: AsyncClient):
    established = await client.post("/conversations", headers=_auth())
    conversation_id = established.json()["conversation_id"]

    response = await client.post(
        f"/conversations/{conversation_id}/close", headers=_auth(role_code="MEMBER")
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_execute_interaction_requires_platform_admin(client: AsyncClient):
    established = await client.post("/conversations", headers=_auth())
    conversation_id = established.json()["conversation_id"]

    response = await client.post(
        f"/conversations/{conversation_id}/interactions",
        headers=_auth(role_code="MEMBER"),
        json={"input_text": "Should be rejected before it is ever gated on Conversation state"},
    )
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# Mandatory Tenant-Isolation Test Checklist (CLAUDE.md §21.4)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_caller_in_org_a_cannot_close_org_bs_conversation(client: AsyncClient):
    """(a) two distinct Organizations seeded; (b) cross-tenant access confirmed denied."""
    org_b_conversation = await client.post("/conversations", headers=_auth(_ORG_B))
    conversation_id = org_b_conversation.json()["conversation_id"]

    cross_tenant_attempt = await client.post(f"/conversations/{conversation_id}/close", headers=_auth(_ORG_A))
    assert cross_tenant_attempt.status_code == 404  # not found, not 403 — existence itself is not disclosed


@pytest.mark.asyncio
async def test_unrelated_tenants_conversation_id_is_rejected_not_accepted(client: AsyncClient):
    """(c) explicit probe: a caller-supplied identifier belonging to an unrelated tenant is never accepted."""
    org_a_conversation = await client.post("/conversations", headers=_auth(_ORG_A))
    conversation_id = org_a_conversation.json()["conversation_id"]

    probe = await client.post(f"/conversations/{conversation_id}/close", headers=_auth(_ORG_B))
    assert probe.status_code == 404


# ---------------------------------------------------------------------------
# BA-02 — Execute Interaction / BA-03 — Retrieve Conversation
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_execute_interaction_persists_and_sequences_from_one(client: AsyncClient):
    established = await client.post("/conversations", headers=_auth())
    conversation_id = established.json()["conversation_id"]

    response = await client.post(
        f"/conversations/{conversation_id}/interactions",
        headers=_auth(),
        json={"input_text": "What is our current enterprise structure?"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["sequence_number"] == 1
    assert body["status"] == "COMPLETE"
    assert body["conversation_id"] == conversation_id
    assert body["confidence_score"] is None  # never fabricated — disclosed placeholder, IRA-012 §4.4


@pytest.mark.asyncio
async def test_second_interaction_gets_sequence_number_two(client: AsyncClient):
    established = await client.post("/conversations", headers=_auth())
    conversation_id = established.json()["conversation_id"]

    await client.post(f"/conversations/{conversation_id}/interactions", headers=_auth(), json={"input_text": "First turn"})
    second = await client.post(f"/conversations/{conversation_id}/interactions", headers=_auth(), json={"input_text": "Second turn"})
    assert second.json()["sequence_number"] == 2


@pytest.mark.asyncio
async def test_interaction_rejected_against_closed_conversation_with_409(client: AsyncClient):
    established = await client.post("/conversations", headers=_auth())
    conversation_id = established.json()["conversation_id"]
    await client.post(f"/conversations/{conversation_id}/close", headers=_auth())

    response = await client.post(
        f"/conversations/{conversation_id}/interactions", headers=_auth(), json={"input_text": "Too late"}
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_interaction_against_unknown_conversation_returns_404(client: AsyncClient):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.post(
        f"/conversations/{fake_id}/interactions", headers=_auth(), json={"input_text": "Nobody home"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_retrieve_conversation_returns_ordered_empty_state_for_new_conversation(client: AsyncClient):
    established = await client.post("/conversations", headers=_auth())
    conversation_id = established.json()["conversation_id"]

    response = await client.get(f"/conversations/{conversation_id}/interactions", headers=_auth())
    assert response.status_code == 200
    assert response.json()["interactions"] == []


@pytest.mark.asyncio
async def test_retrieve_conversation_preserves_ordering(client: AsyncClient):
    established = await client.post("/conversations", headers=_auth())
    conversation_id = established.json()["conversation_id"]
    for text in ("first", "second", "third"):
        await client.post(f"/conversations/{conversation_id}/interactions", headers=_auth(), json={"input_text": text})

    response = await client.get(f"/conversations/{conversation_id}/interactions", headers=_auth())
    body = response.json()["interactions"]
    assert [row["sequence_number"] for row in body] == [1, 2, 3]
    assert [row["input_reference"] for row in body] == ["first", "second", "third"]


@pytest.mark.asyncio
async def test_org_a_cannot_retrieve_org_bs_conversation_interactions(client: AsyncClient):
    """Mandatory Tenant-Isolation Test Checklist (b): cross-tenant retrieval denied."""
    org_b_conversation = await client.post("/conversations", headers=_auth(_ORG_B))
    conversation_id = org_b_conversation.json()["conversation_id"]
    await client.post(f"/conversations/{conversation_id}/interactions", headers=_auth(_ORG_B), json={"input_text": "secret"})

    cross_tenant = await client.get(f"/conversations/{conversation_id}/interactions", headers=_auth(_ORG_A))
    assert cross_tenant.status_code == 404


@pytest.mark.asyncio
async def test_org_a_cannot_execute_interaction_against_org_bs_conversation(client: AsyncClient):
    """Mandatory Tenant-Isolation Test Checklist (c): unrelated tenant's own conversation_id is never accepted."""
    org_b_conversation = await client.post("/conversations", headers=_auth(_ORG_B))
    conversation_id = org_b_conversation.json()["conversation_id"]

    probe = await client.post(
        f"/conversations/{conversation_id}/interactions", headers=_auth(_ORG_A), json={"input_text": "probe"}
    )
    assert probe.status_code == 404
