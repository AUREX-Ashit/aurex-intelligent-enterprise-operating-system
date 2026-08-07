# TDS-012 — WP-12 AI Conversation Management (C-094) — Technical Design Specification

**Document ID:** TDS-012
**Work Package:** WP-12
**Basis:** `IRA-012` (accepted-pending-one-item; the one item — Business Object vs. Runtime Object — is resolved above and treated as closed for this document's own purposes)
**Governing constitutional authority (unchanged, cited not restated):** `RTA-001 §13.15a`, `SD-001 §16`, `ADR-020`, `ADR-021`, `ADR-022`, `CMD-001 §24.4`/`§24.5`
**Status:** Technical Design — implementation not yet authorized (`IRA-012 §13`)

---

## 1. Business Activity Decomposition

Unchanged from `IRA-012 §5` — reproduced here as the frame the rest of this document elaborates:

| BA | Purpose | Realizes |
|---|---|---|
| BA-01 | Establish and Manage Conversation Lifecycle | `RTA-001 §13.15a` Conversation Boundary, `ADR-020` Decision 2 |
| BA-02 | Execute Interaction | `RTA-001 §13.15a` Interaction, `ADR-020` Decision 4 |
| BA-03 | Retrieve Conversation | `ADR-022` Decision 1 (identity, ordering, accountability preserved) |

---

## 2. Conversation Lifecycle and State Transitions

Per `ADR-020` Decision 2 (state model and transition mechanism kept separate) and `IMP-001 §13.29`'s `ConversationStateResolver`:

```
                 ┌─────────────┐
   establish()   │             │   close() (explicit action)
   ───────────►  │    OPEN     │   or Runtime Policy (inactivity timeout)
                 │             │  ───────────────────────────────►  ┌─────────┐
                 └─────────────┘                                     │ CLOSED  │
                        │                                            └─────────┘
                        │ execute_interaction()                           │
                        │ (any number of times while OPEN)                │
                        ▼                                                 │
                 [ Interaction created, sequence_number += 1 ]      (terminal —
                                                                      no further
                                                                      Interactions
                                                                      accepted)
```

- No implicit transition exists — `ConversationStateResolver.resolve(triggerEvent)` only ever fires from an explicit action or an evaluated Runtime Policy (`RTA-001 §13.10`), never a default, per `ADR-020` Decision 2 and the `IMP-001 §13.51` boundary test that already requires this be verified structurally.
- `CLOSED` is terminal for this Work Package's own scope — no reopen path. If reopening is needed later, it is new scope, not assumed here.

---

## 3. Backend Services and Repositories

Per `IMP-001 §13.28`–`§13.30`, implemented for the first time by this Work Package (§3 of `IRA-012`):

| Component | Responsibility | Backing |
|---|---|---|
| `ConversationService` | Owns Conversation Boundary transitions; never executes an Interaction itself | `SessionRecordRepository` |
| `InteractionService` | Wraps one AI Request Lifecycle execution; sole caller permitted to read/write that execution's own record | `SessionRecordRepository`, `InteractionStateAssembler` |
| `ConversationStateResolver` | Resolves state transitions from an explicit trigger or Runtime Policy evaluation | — (stateless resolver) |
| `SessionRecordRepository` | Canonical System of Record for Conversation and Interaction; Session Cache is an optional, injected acceleration layer only | Database (below) |
| `InteractionStateAssembler` | Assembles prior same-Conversation Interactions into structured continuity context for the next Interaction; no `MemoryRepository` dependency reachable | `SessionRecordRepository` (read-only) |
| `ExperienceCompositionResolver` | Resolves which existing `SD-001` contracts (Progressive Disclosure, Evidence Panel) compose a given Interaction's own output for presentation | `ExistingContractRegistry` |

Owning service: `AIService` — same service as `C-093` (`WP-11`), per `CLAUDE.md §8`'s one-capability-one-owning-service discipline, no new service boundary.

---

## 4. Database Schema (Technical Design proposal — first concrete physical shape; `ADR-020` deliberately deferred this to implementation time)

Per the Business Object decision above: `conversation_registry` is the Business Object's own primary table; `interaction_registry` is its decomposition element, mirroring `AI Recommendation`'s own `recommendation`/`recommendation_context`/`recommendation_feedback`/`recommendation_audit` shape.

```
conversation_registry
├── conversation_id          UUID PK
├── organization_id          UUID NOT NULL         -- tenant boundary, SD-002 §13
├── established_by           UUID NOT NULL         -- person_id, accountability anchor
├── state                    ENUM('OPEN','CLOSED') NOT NULL DEFAULT 'OPEN'
├── state_transitioned_at    TIMESTAMPTZ NOT NULL
├── state_transition_reason  ENUM('EXPLICIT_ACTION','RUNTIME_POLICY') NULL
├── created_at                TIMESTAMPTZ NOT NULL
└── closed_at                 TIMESTAMPTZ NULL

interaction_registry                                -- decomposition of conversation_registry, per ADR-020 Clarification 1
├── interaction_id            UUID PK
├── conversation_id           UUID NOT NULL FK → conversation_registry
├── sequence_number            INT NOT NULL          -- ordering, per ADR-022 Decision 1
├── business_activity_id       UUID NOT NULL          -- accountability anchor, per SD-001-114
├── status                     ENUM('PENDING','COMPLETE','FAILED') NOT NULL
├── input_reference             TEXT NOT NULL
├── output_reference            TEXT NULL
├── confidence_score            NUMERIC NULL          -- populated once complete, Evidence Panel input
├── evidence_reference          TEXT NULL             -- populated once complete, Evidence Panel input
├── created_at                  TIMESTAMPTZ NOT NULL
└── completed_at                 TIMESTAMPTZ NULL

interaction_prompt_execution                          -- join table, containment per ADR-020 Clarification 2
├── interaction_id             UUID NOT NULL FK → interaction_registry
└── prompt_execution_id          UUID NOT NULL FK → (existing Prompt Execution table, CMD-001 §24.4)
```

`UNIQUE(conversation_id, sequence_number)` on `interaction_registry` enforces ordering integrity structurally, not by application convention alone — mirroring the `(organization_id, index_name)` uniqueness precedent `WP-11`'s own `vector_index_registry` established (`TD-128`'s own recommended follow-up, applied here from the start rather than retrofitted).

No new Alembic chain — this extends `AIService`'s existing chain (`WP-11`'s `d4a9c1e7f3b5` and successors), per `IRA-012 §3`.

---

## 5. API Contracts

| Endpoint | Method | Purpose | Auth |
|---|---|---|---|
| `/conversations` | `POST` | BA-01 — establish (state = OPEN) | `AIService`'s existing JWT dependency (`WP-11`, reused) |
| `/conversations/{id}/close` | `POST` | BA-01 — explicit close transition | Same |
| `/conversations/{id}/interactions` | `POST` | BA-02 — execute one Interaction | Same |
| `/conversations/{id}/interactions` | `GET` | BA-03 — retrieve, ordered by `sequence_number` | Same |

- `POST /conversations/{id}/interactions` against a `CLOSED` Conversation → `409 Conflict`, not a silent no-op.
- Every response body composes `Evidence Panel`/`Confidence` fields (`confidence_score`, `evidence_reference`) per `§4.4` of `IRA-012` — the first real, non-stub instance of these fields anywhere in `AIService`'s own API surface.
- Request/response schemas follow the existing Business Activity API pattern (`IMP-001` Section 8) — no new API convention introduced, per `IMP-001 §13.36`/`§13.51`.

---

## 6. Frontend Screens and UX Flows

Per `IRA-012 §7`: no existing nav slot for `C-094` — a new, minimal nav entry is required (exact `PE-001 §13.5` Workspace placement determined at implementation time, per that capability's own CRB, consistent with `SD-001-115`'s confirmed delegation).

**Screens:**
1. **Conversation surface** — submit a turn (BA-02), view the response composed with the first real Progressive Disclosure/Evidence Panel instance (`IMP-001 §10.3`/`§10.4`, built for the first time by this Work Package per `IRA-012 §4.4`).
2. **Conversation history view** — ordered turn list (BA-03), same Evidence Panel composition per turn, no cross-Conversation content (`ADR-022` Decision 3).

**States implemented (`CLAUDE.md §20.6`):** loading (Interaction `PENDING`), empty (newly-established Conversation, zero Interactions), validation (turn submission), error (`FAILED` status, `409` on closed Conversation), confirmation (close action).

**Turn visual representation:** per `ADR-020` Decision 1 (as amended), no strict 1:1 visual-to-Interaction mapping is required — this Work Package's own first implementation renders one visual turn per Interaction (the simplest conforming choice), leaving streaming/progressive-rendering as future, separately-scoped enhancement (`TD-candidate-G`, `IRA-012 §9`), not built now.

---

## 7. Events

Per `IMP-001 §13.31` — reused exactly, no new taxonomy introduced:

`CONVERSATION_OPENED`, `CONVERSATION_STATE_TRANSITIONED`, `CONVERSATION_CLOSED`, `INTERACTION_STARTED`, `INTERACTION_COMPLETED`. (`HANDOFF_INITIATED`/`HANDOFF_COMPLETED` not emitted this Work Package — Handoff excluded, `IRA-012 §4.5`.) All routed through the existing Observability Platform, per `IMP-CICD-005`'s own "no parallel telemetry mechanism" principle, applied a third time.

---

## 8. Security, Authorization, Audit, Observability

- **Security/Authorization:** `AIService`'s existing JWT verification dependency (`WP-11`), unchanged, reused on every endpoint above. Write-path persona gate left `PLATFORM_ADMIN`-only pending a `PE-001-C094` persona decision (`TD-candidate-E`, `IRA-012 §9`) — same interim pattern `TD-021`-class entries already establish platform-wide.
- **Audit:** `record_audit` primitive, platform-wide (`RTA-001 §13.14`/`§13.15`). **Disclosed, not silently assumed:** `SER-001 SE-035` already tracks that this primitive is not yet wired into `AIService` at all — `WP-11` did not close this either. This Work Package inherits the same gap; wiring it is in scope for BA-01/02 (each Conversation/Interaction state change is exactly the kind of action `record_audit` exists to capture) since leaving AI-Conversation-specific actions unaudited would be a `CLAUDE.md §19.8.5`-class gap, not deferrable Technical Debt, the same reasoning `IRA-011 §4.4` already applied to a different gap.
- **Observability:** existing Observability Platform only (§7 above).
- **Tenant isolation:** `organization_id` on `conversation_registry`, inherited by `interaction_registry` via its FK — enforced per `SD-002 §13`, tested per `§10` below.

---

## 9. Testing Strategy

Unchanged from `IRA-012 §10`, restated as the binding testing gate for this design: two-organization tenant-isolation probe on all four endpoints; `ConversationStateResolver` transition-reachability test (never a default); `InteractionStateAssembler` `MemoryRepository`-absence test; `ExperienceCompositionResolver` hardcoded-identity-absence test; `UNIQUE(conversation_id, sequence_number)` concurrency probe (mirroring `TD-128`'s own recommended follow-up, built in from the start here rather than retrofitted). Full `AIService` regression suite re-run before closure.

---

## 10. Explicitly Not Decided Here

Consistent with `IRA-012`'s own exclusions, unchanged: Cross-Lifecycle Agent Handoff, multi-agent visualization, Ask User Gate integration, streaming/progressive-rendering mechanics, `C-095` Enterprise Memory. Exact `PE-001 §13.5` Workspace placement for the new nav entry remains an implementation-time CRB decision, not fixed by this document.
