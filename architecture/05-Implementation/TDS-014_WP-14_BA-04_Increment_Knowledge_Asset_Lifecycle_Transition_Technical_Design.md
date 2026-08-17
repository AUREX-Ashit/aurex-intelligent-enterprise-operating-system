# TDS-014 — WP-14 BA-04 Increment (C-091 Knowledge Management) — Knowledge Asset Lifecycle Transition + `ACCEPTED` Domain Event — Technical Design Specification

**Document ID:** TDS-014
**Work Package:** WP-14
**Business Activity:** BA-04 Increment (extends BA-04 — Establish Knowledge Asset, already `CLOSED / CERTIFIED / PUSHED`)
**Basis:** `WP-14_BA-04_Establish_Knowledge_Asset_Business_Activity_Charter.md`'s own "BA-04 Increment — Repository Owner Decision Recording (`RO-DEC-WP14-BA05-01`)" section; `IRA-014 §6` BA-04 row; an independent WP-14 BA-04 Increment Technical Design Authorization Review that returned **NOT AUTHORIZED**, citing seven undefined design areas this document resolves.
**Governing constitutional authority (unchanged, cited not restated):** `EIA-001 Vol. II §13` (`curation_status` state names), `Master_Technical_Architecture.md` AMD-012 (`knowledge_asset_registry`, LOCKED), `RTA-001 §4.13`/`§8.6`–`§8.11` (Domain Event general rules), `RO-DEC-WP14-BA05-01`/`02`/`03` (recorded in the BA-04 charter and `TDS-013 §26a`), `CLAUDE.md §19.7`/`§19.8`.
**Status:** Technical Design — implementation NOT yet authorized. This document determines a mechanism and, where the authoritative record is silent, makes explicit, labeled design decisions or flags a Repository Owner decision as required. It does not authorize building anything (§23).

---

## Classification Key

Mirrors `TDS-013`'s own established convention:

- **A** — already determined by governing documents (`CLAUDE.md`, `EIA-001`, `Master_Technical_Architecture.md`, `IRA-014`, the BA-04 charter, `RO-DEC-WP14-BA05-01`/`02`/`03`)
- **B** — determined by repository precedent (already-certified patterns this design reuses, not invents)
- **C** — a Technical-Design-level decision this document makes explicitly, within the authority `IRA-014`/the charter already delegate to Technical Design (mirrors `TDS-013`'s own BR-1–BR-4 enforcement-mechanism precedent)
- **D** — requires a Repository Owner decision; NOT resolved by this document

---

## 1. Purpose and Scope

**Purpose [A]:** complete the BA-04 charter's own already-disclosed, deferred lifecycle-transition and event-publication scope (charter §9, §12, §183 items 2/4), so that BA-04 produces the Domain Event `RO-DEC-WP14-BA05-01` establishes as BA-05's sole trigger.

**Business problem [A]:** BA-04's own certified delivery provides only `establish()` (creates a `PROPOSED` row) and `get_by_id()`. No code path today transitions a Knowledge Asset out of `PROPOSED`, and no code path publishes any Domain Event. BA-05 cannot function without this.

**Relationship to BA-04 [A]:** this is an **Increment**, not a re-opening of BA-04's own certified behavior. `establish()`/`get_by_id()` are unchanged (§16). The Increment is purely additive: one new transition capability, one new event.

**Relationship to BA-05 [A]:** this Increment is the sole producer of BA-05's trigger. It does not implement any part of BA-05 itself — no Knowledge Graph code, no `enterprise_knowledge_graph_registry` write, no relationship-creation logic (§17).

### IN SCOPE

1. A Knowledge Asset lifecycle-transition capability, invoked from `PROPOSED` — the only state `establish()` ever produces — to one of the three targets `IRA-014 §6` BA-04's own row names together: `VALIDATED`, `ACCEPTED`, `REJECTED` (§2).
2. Domain Event publication, **only** on a successful transition to `ACCEPTED` (§8/§10).
3. The event information `RO-DEC-WP14-BA05-02` requires (§8).
4. Authorization for the transition (§4).
5. Audit/evidence for the transition (§11).
6. Tenant isolation for the transition and the event (§13).
7. Concurrency/idempotency semantics for the transition and the event (§6/§7).

### OUT OF SCOPE

- BA-05 implementation of any kind (no `enterprise_knowledge_graph_registry` code, no relationship creation, no entity/relationship resolution).
- Live Neo4j graph population (`SE-025`, unchanged).
- CDE creation or association.
- Semantic matching, convergence, promotion.
- Any transition not named in `IRA-014 §6` BA-04's own row (§2 — the full five-state graph beyond `PROPOSED`'s own three direct targets is explicitly **not** designed here; see `[D]` items below).
- A new Capability, Business Activity, SER, or relationship kind.
- Building live event-broker infrastructure (`§9` identifies what would be required; does not build it).

---

## 2. Knowledge Asset State Machine

**Authoritative states [A]:** `PROPOSED`, `VALIDATED`, `ACCEPTED`, `REJECTED`, `SUPERSEDED` — the physical `CHECK` constraint (`ck_knowledge_asset_registry_curation_status`, `models/knowledge_asset.py:47-50`) enumerates exactly these five values, matching `EIA-001 Vol. II §13`'s own naming. **The full transition graph between these five states is not defined by any governing document** — independently re-verified by the BA-04 charter itself, three separate times (§9, §183 item 2, "BA-04 Increment" section), and confirmed again by the independent Increment authorization review. This document does not invent that graph.

**`[C]` Technical Design decision — minimum sufficient transition scope, not the full graph:**

This design implements **exactly** the transitions `IRA-014 §6` BA-04's own row already names, and no others — the same "smallest sufficient scope" discipline this repository's own `CLAUDE.md §19.5` worked example (WP-04 BA-08, Option A) already establishes as the governing precedent for exactly this kind of scope decision:

| From | To | Supported by this Increment? | Authoritative basis |
|---|---|---|---|
| `PROPOSED` | `VALIDATED` | **Yes** | `IRA-014 §6` BA-04 row: "a status-transition endpoint (`PROPOSED`→`VALIDATED`/`ACCEPTED`/`REJECTED`)" |
| `PROPOSED` | `ACCEPTED` | **Yes** | Same citation |
| `PROPOSED` | `REJECTED` | **Yes** | Same citation |
| `VALIDATED` | `ACCEPTED` | **No — `[D]`** | Not named by `IRA-014 §6`'s own row (which lists three direct targets from `PROPOSED`, not a `VALIDATED`-mediated chain); inventing this edge would invent a business rule (does acceptance require prior validation, or not?) no document states |
| `VALIDATED` | `REJECTED` | **No — `[D]`** | Same reasoning |
| `ACCEPTED` | anything | **No — `[D]`** | No document states `ACCEPTED` is reversible or what a reversal would mean for BA-05's own already-published relationship |
| `REJECTED` | anything | **No — `[D]`** | No document states rejection is reconsiderable |
| anything | `SUPERSEDED` | **No — `[D]`** | No document names a trigger or actor for this state at all |

**Consequence of this scope decision:** within this Increment, `PROPOSED` is the only state from which a transition may be requested. `VALIDATED`, `ACCEPTED`, and `REJECTED` are each reachable directly from `PROPOSED` and, within this Increment's own scope, no further transition is designed **from** any of them — this is a **scope boundary of this Increment**, not a general claim that these states are constitutionally terminal forever. A future Increment may extend the graph once the `[D]` items above receive a Repository Owner decision; this document does not foreclose that, and does not need to resolve it, since BA-05's own dependency (`RO-DEC-WP14-BA05-01`) requires only that `PROPOSED`→`ACCEPTED` exist and behave correctly.

**Guard invariant (ties directly into §6):** a transition request is valid if and only if the Knowledge Asset's own currently-persisted `curation_status` is `PROPOSED` and the requested target is one of `VALIDATED`/`ACCEPTED`/`REJECTED`. Any other combination is rejected (§5/§6).

---

## 3. `ACCEPTED` Semantics

**`[A]`, from `RO-DEC-WP14-BA05-02`:** `ACCEPTED` means the Knowledge Asset is now governed enterprise knowledge belonging to the Organization that owns it — this is BA-05's own downstream meaning, already frozen, not re-decided here.

**`[C]`, this document's own scope, for BA-04's internal handling:**
- **Who can perform it:** the same actor class already authorized for every other BA-04 write (`PLATFORM_ADMIN`, §4) — no new persona is invented.
- **Prerequisites:** the Knowledge Asset must currently be `PROPOSED` (§2). No additional business precondition (e.g., a minimum evidence threshold) is named by any document, so none is invented; this mirrors `establish()`'s own precedent of enforcing only what the schema/charter actually requires.
- **Validation requirements:** the requested target must be one of the three named values (§2); the caller-supplied identifier must resolve to a Knowledge Asset owned by the caller's own Organization (§13).
- **Evidence requirements:** none beyond `provenance_reference`, already mandatory at `establish()` time and unchanged by this Increment.
- **Audit requirements:** §11.
- **Tenant ownership:** unchanged — the Knowledge Asset's own persisted `organization_id`, set once at `establish()` time, is never altered by a transition.
- **Is `ACCEPTED` terminal within this Increment's own scope?** Yes — no outbound transition from `ACCEPTED` is designed (§2, `[D]`).
- **Can it be reversed?** Not designed — `[D]`, §2.
- **What happens if the asset is already `ACCEPTED`, already `VALIDATED`, or already `REJECTED` (i.e., not `PROPOSED`) when a transition is requested?** `409 Conflict` (§5/§6) — the same disposition BA-03's own `claim_for_resolution` precedent already establishes for "already resolved."
- **What happens if `REJECTED` is requested for an asset that is not `PROPOSED`?** Same `409 Conflict` — the guard (§2) applies uniformly to all three targets, not only `ACCEPTED`.
- **What happens on an invalid target value (not one of the three)?** `422` at the schema/validation layer, before the guard is ever evaluated — mirrors `ResolveIntelligenceCandidateRequest`'s own established `field_validator` pattern (BA-03).

---

## 4. Authorization / Permissions

**`[B]`, repository precedent, no invention required.** BA-04's own router already gates every existing endpoint with `require_platform_admin` (`routers/knowledge_assets.py:9,53,76`, independently re-verified by the Increment authorization review) and the charter's own router docstring treats BA-04 "as a single, undifferentiated interim-authorization Business Activity... not split by read/write." The transition endpoint reuses this exact, already-certified dependency — no new permission, role, or persona is created. Organization context is derived exclusively from the caller's own JWT `organization_id` claim, never from the request body — the same established platform-wide convention every other WP-14 write path (BA-01 through BA-03) already uses.

---

## 5. Transition API / Service Contract

**`[C]`, Technical Design decision.** A single, generic transition endpoint — not one named-action endpoint per target — mirroring the "single generic transition endpoint" half of the charter's own already-named `[C]` choice (§9 of the charter), selected over named-action endpoints (`/validate`, `/accept`, `/reject`) because the three targets share one identical guard/response shape (§2) and inventing three near-duplicate endpoints adds surface area without adding clarity, the same reasoning `ResolveIntelligenceCandidateRequest`'s own single-endpoint, outcome-discriminated-by-body-field design already established for BA-03's own three-way decision.

- **Endpoint:** `POST /knowledge-assets/{knowledge_asset_id}/transition` — appended to the existing `routers/knowledge_assets.py` router; the base path and existing `establish`/`get_by_id` routes are unchanged.
- **Request body:** `{"target_status": "VALIDATED" | "ACCEPTED" | "REJECTED"}` — `target_status` is the only field; `organization_id`/`actor_id` are never accepted in the body (§4/§13).
- **Response (200):** the same `KnowledgeAssetResponse` shape `establish()`/`get_by_id()` already return (`schemas/knowledge_asset.py`, unchanged) — reflecting the Knowledge Asset's own new, post-transition state. No new response schema is invented.
- **Status codes:** `200` (transition succeeded); `404` (no Knowledge Asset with that id visible to the caller's own Organization — mirrors BA-03's own `get_by_id` 404 precedent); `409` (guard failed — not currently `PROPOSED`, per §2/§3); `422` (invalid `target_status` value); `403`/`400` (authorization, per §4, unchanged from every other BA-04 endpoint).
- **Idempotency:** §6/§7.
- **Tenant scope:** §13.

---

## 6. Concurrency Design (MANDATORY)

**`[C]`, Technical Design decision — reuses BA-03's own atomic-claim pattern verbatim, explicitly rejecting the charter's own cited `OrganizationService.activate()/suspend()` precedent for this specific write.**

The independent authorization review found `activate()`/`suspend()` (`Backend/Services/AuthService/services/organization_service.py:486-618`) — the charter's own cited shape precedent — performs a plain read-then-separately-write sequence with no atomic guard, and correctly identified this as the exact pattern class `TD-147` already flags as unsafe and as the root cause of BA-03's own, since-fixed Gate 1 Finding 1 (a concurrent double-resolution race). **This design explicitly does not reuse that half of the `activate()`/`suspend()` precedent** — it reuses only the *endpoint shape* (§5), not the *write mechanism*.

**Mechanism, mirroring `UnclassifiedIntelligenceRegistryRepository.claim_for_resolution` (`repositories/unclassified_intelligence_repository.py:59-114`) exactly:**

```
UPDATE knowledge_asset_registry
SET curation_status = :target_status
WHERE knowledge_asset_id = :id
  AND organization_id = :org_id
  AND curation_status = 'PROPOSED'
```

executed via SQLAlchemy Core `update(...)`, never a `get_by_id()`-then-attribute-assignment sequence. `rowcount == 1` means this caller's request won the claim; `rowcount == 0` means either the asset does not exist for this Organization (already excluded by a prior `404` check, mirroring BA-03's own two-step 404-then-claim shape) or it was not `PROPOSED` at the moment the `UPDATE` executed — translated to `409 Conflict`, never a silent no-op and never a second success.

**Invariant, stated explicitly per this section's own requirement:** for two concurrent transition requests (same or different targets) against the same Knowledge Asset, **exactly one succeeds** (`200`, `rowcount == 1`) and **every other request fails** (`409`, `rowcount == 0`) — never two successes, never a lost update, never a corrupted intermediate state. This holds under Postgres's own row-level locking (an `UPDATE` takes a write lock held until commit; a second concurrent `UPDATE` blocks, then re-evaluates its own `WHERE` clause against the now-committed row and finds no match) — the identical reasoning already independently verified for BA-03's own instance of this pattern, requiring no new locking primitive.

- **Winner:** the request whose `UPDATE` actually matches the row; database state reflects its own requested `target_status`; response `200`; audit `SUCCESS` (§11); if `target_status == 'ACCEPTED'`, event publication is attempted (§9) — for this winner only.
- **Loser(s):** `rowcount == 0`; response `409`; audit `DENIED` (§11, mirroring BA-03's own `AuditStatus.DENIED` precedent for "already resolved"); **no event is ever attempted** for a losing request — the guard sits strictly before the event-publication code path, so a losing request cannot cause even an attempted duplicate publish.
- **No optimistic-locking/version column is introduced.** The existing model carries no `updated_at`/version column (independently confirmed absent by the authorization review); this design does not add one — the atomic `WHERE curation_status = 'PROPOSED'` predicate is itself the concurrency guard and requires no separate version field, exactly mirroring `claim_for_resolution`'s own equivalent reasoning for `resolution_status`.

---

## 7. Idempotency

**A. Transition idempotency `[C]`:** a retried identical request (same target, same asset, after the first request already succeeded) is **not** silently treated as a repeat success — it is a `409 Conflict`, since by the time it executes the guard's own `curation_status = 'PROPOSED'` predicate no longer matches. This is a deliberate design choice, not an oversight: it mirrors BA-03's own established "already resolved → 409, not a silent 200" precedent exactly (`test_resolve_an_already_resolved_candidate_returns_409`). A caller that needs to confirm the asset's own current state after a `409` uses the existing, unchanged `GET /knowledge-assets/{id}`.

**B. Event idempotency `[C]`:** BA-04's own responsibility is limited to **not publishing more than once per successful transition inside its own code path** — trivially guaranteed by §6's own invariant, since the event-publication call is reached only immediately following a winning `rowcount == 1` `UPDATE`, which can happen at most once per Knowledge Asset (given §2's own "no outbound transition from `ACCEPTED`" scope decision, a given asset can reach `ACCEPTED` at most once, ever, within this Increment's own scope). **Protecting against duplicate event *delivery*** (a network-level retry, an at-least-once broker replaying a message, a manual reconciliation replay per §9) **is explicitly BA-05's own responsibility, not BA-04's** — `TDS-013 §17` already designs for this on BA-05's own consuming side (check-before-insert or a `UNIQUE` constraint against the natural key). This design supplies exactly the natural key BA-05's own already-existing design needs: `knowledge_asset_id` (§8) — since at most one `ACCEPTED` transition can ever occur per asset, `knowledge_asset_id` alone is sufficient as BA-05's own deduplication key, without BA-04 needing to invent anything further.

---

## 8. Domain Event Contract (MOST IMPORTANT)

**Envelope — `[B]`, already fixed by `Backend/Shared/Events`, not re-decided here.** Directly verified by reading `event_base.py`/`cloud_event.py`: `BaseEvent.__init__` already fixes `event_id` (UUID, auto-generated), `timestamp` (UTC, auto-generated), `correlation_id`, `tenant_id`, `user_id` (each sourced from `EventContext.export_context()`, with documented fallbacks). `CloudEvent.wrap()` already fixes the CNCF v1.0 envelope (`specversion`, `id`, `source`, `type`, `subject`, `time`, `datacontenttype`, `datacontentversion`) plus the `correlationid`/`tenantid`/`userid` extensions. **No `causation_id` field exists anywhere in this framework** — independently verified by `grep`; this design does not invent one. `correlation_id` is the only cross-reference field available and is what this design uses.

**Business payload — `[C]`, Technical Design decision, since no document names a concrete event class for this outcome (charter §12; `TDS-013 §26a`, both explicit that this is not decided by any prior document):**

| Field | Value | Rationale |
|---|---|---|
| `event_name` | `"aurex.aiservice.knowledge_asset.accepted"` | Follows the framework's own documented convention verbatim (`event_base.py:46`: `"aurex.auth.user.created"`, `"aurex.ingestion.job.started"`) — `<platform>.<service>.<entity>.<action>`. `aiservice` matches this Increment's own hosting service (unchanged from BA-04's own existing host). |
| `event_version` | `"1.0.0"` | First version of this event; no prior version exists to be compatible with. |
| Concrete class name | `KnowledgeAssetAcceptedEvent` | Implementation-time naming choice — see §18, `MAY CHOOSE`. |
| Payload (`to_dict()`) — `knowledge_asset_id` | The transitioned asset's own UUID, as string | The identifier BA-05 needs (§17) |
| Payload — `organization_id` | The Knowledge Asset's own persisted `organization_id` at the moment of the winning transition, as string | **Not** the same thing as the envelope's own `tenant_id` (which may fall back to `"SYSTEM"` per `event_base.py:38` if no context var is set) — this field is always explicitly, deliberately set from the just-transitioned row's own column value, never inferred. Per `RO-DEC-WP14-BA05-02`'s own explicit warning, BA-05 must still treat this as a hint, not ground truth (§17) — this design does not relax that requirement by supplying the field. |
| Payload — `previous_status` | `"PROPOSED"` | Always `PROPOSED`, given §2's own scope (only `PROPOSED`→`ACCEPTED` triggers this event) — included for completeness/future-proofing, not because BA-05 needs it today. |
| Payload — `new_status` | `"ACCEPTED"` | Redundant with `event_name` itself but included for a consumer that dispatches on payload content rather than envelope `type` — a defensive, low-cost inclusion, not a new architectural requirement. |
| `validate()` | Raises `EventValidationError` if `knowledge_asset_id`/`organization_id` are missing/malformed, or if `previous_status != "PROPOSED"` or `new_status != "ACCEPTED"` | Enforces this event class only ever represents the one fact it claims to |

**Registration `[B]`:** the concrete event class is registered with `EventRegistry.register()` at module import time, the same pattern any future consumer of `event_registry.py`'s own documented mechanism already requires — no new registration mechanism invented.

---

## 9. Event / Database Consistency (CRITICAL)

**Ordering invariant `[A]`, already fixed by `RTA-001 §8.10`:** *"Events shall be published only after successful Business Transaction commitment."* This design follows this literally: the `UPDATE` (§6) is committed **first**; the event is constructed and `publish()` is attempted **only after** the commit call returns successfully. If the commit itself fails or raises, `publish()` is never called at all — this alone fully resolves **Case B** (event succeeds, DB fails) by construction: that ordering makes Case B structurally unreachable, not merely unlikely.

**`[A]`, empirically re-verified this pass — the actual current publisher is not merely a "risk of failure," it never delivers anything at all, regardless of design correctness.** Direct read of `Backend/Shared/Events/event_publisher.py::KafkaEventPublisher.publish()` confirms the real broker dispatch call is commented out (`# --- MOCK OUTBOUND BROADCAST FOR ARCHITECTURE STAGE ---`); the method logs a debug line and returns normally, without raising and without actually sending anything anywhere. `AzureServiceBusEventPublisher` is equally a stub. The consumer-side `event_subscriber.py::route_to_dead_letter_queue` is likewise log-only (`self.dlq_publisher.publish_raw(...)` is commented out). **This is a pre-existing, platform-wide infrastructure-maturity gap, not something this Increment introduces or can fix** — it mirrors `TDS-013 §24` item 2's own identical disclosure for BA-05's own consuming side ("the live message-bus transport itself remains a stub... mirrors `IRA-014 §5a`'s own `SE-025` disclosure... the same class of infrastructure-maturity gap, not new"). **Consequence, stated plainly: even once this Increment and BA-05 are both fully implemented and certified, no event will actually reach BA-05 until a real broker replaces the mock publisher/subscriber — this is a real, disclosed limitation of the current platform, not a design defect of this Increment.**

**Given this constraint, the design defines the correct contract for both today (mock) and the future (real broker), without building the real broker:**

- **Case 1 / Case A (DB transition fails):** no event is ever attempted (§9's own ordering invariant); the Knowledge Asset remains in its prior state (`PROPOSED`). No publish call is reached.
- **Case 2 (DB commits, publish attempt succeeds):** normal flow — winner response `200`, audit `SUCCESS` (§11), event constructed and `publish()` called once.
- **Case 3 (DB commits, publish attempt fails):** the already-committed transition is **not** rolled back — rolling back an already-committed transaction is not a real database operation, and `RTA-001 §8.10`'s own ordering rule already forbids publishing before commit, so the DB state is, and remains, the authoritative source of truth regardless of publish outcome. `publish()` is wrapped in a `try`/`except`; on failure, the exception is caught and a structured, high-severity log entry is written (`knowledge_asset_id`, `organization_id`, `event_id`, `correlation_id`, target status, underlying error) via the existing observability pattern (§11) — recorded explicitly as an **event-publication failure**, never as a failed Knowledge Asset transition. The caller's own HTTP response is still `200` (the business transition genuinely succeeded; from the caller's own perspective the requested state change did happen). **No automatic retry is attempted in this Increment (`RO-DEC-BA04-INC-007`, §19).**
- **Case 4 (DB commits, process crashes before the publish attempt is even reached):** behaviorally identical to Case 3 from the system's own perspective, except no failure log is even possible (the process is gone) — the Knowledge Asset remains `ACCEPTED`, and the event may never be delivered. **Explicitly accepted by the Repository Owner as a consequence of the best-effort posture (`RO-DEC-BA04-INC-007`, §19) — not a defect this Increment is required to close.**
- **Case 5 (the event publisher/broker later becomes available, but no durable record of the missed event exists):** no automatic recovery or replay is guaranteed by this Increment — the current implementation has nothing to replay from, by design (no outbox, no durable event store). **Explicitly accepted (`RO-DEC-BA04-INC-007`, §19).**
- **Case B, legacy label (event succeeds, DB fails):** structurally unreachable by the ordering invariant above, unchanged from the original analysis.
- **Case C, legacy label (event published twice):** BA-04's own code path cannot cause this on its own (§7B, at most one publish attempt per successful transition); a duplicate *delivery* caused by broker-level at-least-once semantics or a manual future replay is BA-05's own consuming-side responsibility (`TDS-013 §17`), using `knowledge_asset_id` as the natural dedup key this design supplies (§8).
- **Case D, legacy label (consumer temporarily unavailable):** out of this Increment's own scope — a broker/consumer-availability concern, unaffected by anything BA-04 does; the existing (currently log-only) DLQ concept in `event_subscriber.py` is BA-05's/the framework's own concern, not redesigned here.

**Minimum infrastructure required to fully close Case A/E, identified, not built:** a **transactional outbox** — writing the event's own serialized payload into a durable outbox table inside the *same* database transaction as the `curation_status` `UPDATE` (§6), with a separate, reliable relay process publishing from the outbox with at-least-once retry, independent of whether the original request's own process survives. This is the textbook-correct fix for exactly this class of problem and remains **not implemented by this document or this Increment** — named as the identified gap, consistent with this repository's own established practice of disclosing rather than silently building around an infrastructure-maturity limitation (`TDS-013 §24` item 2's own precedent, `TD-105`'s own now-Closed precedent for a related but distinct gap).

**`[A]`, resolved 2026-08-16 by direct Repository Owner decision (`RO-DEC-BA04-INC-007`, recorded in full in §19/§21 below):** the Repository Owner has explicitly accepted a **best-effort event-delivery posture** for this Increment's own initial scope — the ordering invariant above (commit strictly before publish) is the entire consistency guarantee this Increment provides; no durable delivery, retry, replay, or recovery mechanism is built, and none of Case A/C/E is fully closed. This is not a silent default — it is a bounded, explicitly-scoped Repository Owner decision, stated in full in §19. The transactional outbox named above remains a named, future, platform-level concern, not decided or scheduled by this decision.

---

## 10. Event Semantics

**`[A]`, confirmed against `RTA-001 §4.13`/`§8.6`–`§8.11` directly:** a Domain Event "describes a completed business fact," is immutable, and is published after commit — never a command. This design's event represents exactly one fact: "this specific Knowledge Asset has reached `ACCEPTED`." It contains no relationship-creation logic, no graph-mutation instruction, and no BA-05-specific business rule — `RO-DEC-WP14-BA05-02`'s own `Governed By` relationship-construction logic belongs entirely to BA-05's own future `KnowledgeGraphSyncHandler`, never to this event's own payload or to BA-04's own code (§17).

---

## 11. Audit / Evidence

**`[B]`, direct extension of the already-certified BA-04 pattern.** `services/knowledge_asset_service.py::establish()` already calls `record_audit(action="ESTABLISH_KNOWLEDGE_ASSET", resource=f"knowledge_asset:{...}", status=AuditStatus.SUCCESS, actor_id=..., tenant_id=...)` (independently re-verified, lines 49-55), an exact mirror of `conversation_service.py::establish()`'s own shape. This design extends the same call shape to the transition:

- **On success (winner, §6):** `record_audit(action="TRANSITION_KNOWLEDGE_ASSET", resource=f"knowledge_asset:{knowledge_asset_id}", status=AuditStatus.SUCCESS, actor_id=str(actor_id), tenant_id=str(organization_id), metadata={"from_status": "PROPOSED", "to_status": target_status, "event_id": ... if target_status == "ACCEPTED" else None})`.
- **On guard failure (loser, §6):** `record_audit(..., status=AuditStatus.DENIED, metadata={"reason": "not currently PROPOSED", "requested_target": target_status})` — mirrors BA-03's own `DENIED`-for-already-resolved precedent (`services/conversation_service.py::close()`, `services/intelligence_candidate_resolution_service.py::resolve()`), independently confirmed by both the BA-05 authorization review and the BA-04 audit-finding remediation earlier this Work Package to be the correct status for a foreseeable, correctly-handled business-rule rejection (as distinct from `AuditStatus.FAILED`, reserved for an unexpected system fault).
- **On not-found (404):** `record_audit(..., status=AuditStatus.DENIED, metadata={"reason": "knowledge asset not found or not visible to this organization"})` — mirrors the same pattern BA-03's own audit-remediation established for its own 404 path.

**The event is not the audit record and does not substitute for one** — `record_audit` remains the authoritative internal audit trail (per `SD-002-054`'s seven questions, as `observability.py`'s own docstring already establishes); the Domain Event is a separate, external-facing fact for BA-05's own consumption. No new evidence model is introduced; no `evidence_registry` row is created by this transition (BA-04's own charter never establishes an Evidence requirement for the transition itself, only `provenance_reference` at `establish()` time, unchanged).

---

## 12. Data Model

**`[A]`, no schema change required.** The existing `curation_status` `CHECK` constraint (`models/knowledge_asset.py:47-50`) already enumerates all five legal values — no new column, table, index, or constraint is needed for §2's own minimum-scope transitions. `organization_id`, already `NOT NULL` and indexed, is unchanged. This is explicitly confirmed, not assumed: the atomic `UPDATE`'s own guard (§6) requires only `knowledge_asset_id`, `organization_id`, and `curation_status` — all three already exist on the physical table.

**If the `[D]` items in §2 (the fuller transition graph) or §9 (a transactional outbox) are later resolved and require a schema change** — a transition-history table, an outbox table, or a version column — that is **explicitly a future, separately-scoped amendment**, not designed or authorized here.

---

## 13. Tenant Isolation

**`[A]`/`[B]`, unambiguous, no invention required.** The Knowledge Asset's own persisted `organization_id` (never a request-body or event-payload value) is the sole authority for every check in this design: the `404` lookup, the atomic `UPDATE`'s own `WHERE organization_id = :org_id` clause (§6), and the event payload's own `organization_id` field (§8, explicitly disclosed as a hint for BA-05, not ground truth). No caller can transition an asset outside their own Organization — the `404`/guard combination makes a cross-tenant asset indistinguishable from a nonexistent one, mirroring BA-01–BA-03's own established precedent exactly. `RO-DEC-WP14-BA05-02`'s own text already states the downstream principle this design's own event payload is built to satisfy: "an `organization_id` supplied by the triggering event payload is never treated as authoritative on its own" (by BA-05).

---

## 14. Evidence / Audit

(Combined with §11 above per this document's own structure — no separate content; retained as a numbered section only to preserve this task's own requested section numbering.)

---

## 15. Data Model

(Combined with §12 above — retained only for numbering parity with this task's own requested structure.)

---

## 16. BA-04 Regression / Closed-BA Integrity

**`[A]`, directly verified.** `establish()` and `get_by_id()` (`services/knowledge_asset_service.py:28-67`) contain no transition or event logic; this design adds one new method (`transition()`) and one new router path, touching neither existing method's own code path, request schema, or response schema. Existing tenant rules (`organization_id NOT NULL`, RLS-equivalent scoping) and existing authorization (`require_platform_admin`) are reused verbatim, not altered. BA-01–BA-03 are structurally unrelated (charter §16, independently re-verified: no FK from `knowledge_asset_registry` to any BA-01–03 table) and are untouched by anything in this design.

---

## 17. BA-05 Compatibility

**`[A]`, confirmed sufficient for `RO-DEC-WP14-BA05-02`'s own stated need.** The event (§8) provides: `knowledge_asset_id` (source entity identifier), `organization_id` (target entity identifier, explicitly caveated as non-authoritative on its own), and the fact of the `ACCEPTED` transition (via `event_name`/`new_status`) — exactly what BA-05's own future `KnowledgeGraphSyncHandler` needs to construct one `Knowledge Asset —[Governed By]→ Organization` relationship (`TDS-013 §26a`). **Validation principle, stated explicitly per this section's own requirement:** BA-05 MUST NOT create a relationship using the event payload's own `organization_id` without first independently re-reading the Knowledge Asset's own currently-persisted `organization_id` (via its own same-database read, per `TDS-013 §9`'s own `EntityOwnershipResolver` design) and confirming the two values match — the event is a *trigger and a hint*, never a substitute for the authoritative source-of-truth read. This design does not implement that validation (it is BA-05's own code, out of scope, §1) — it only confirms the event supplies enough information for BA-05 to perform it.

---

## 18. Implementation Boundary

**MAY CHOOSE** (within the frozen contract below):
- Internal class/method names (e.g., `KnowledgeAssetAcceptedEvent`'s own exact Python class name, `transition()`'s own internal helper structure).
- Repository method names and internal SQLAlchemy query construction, provided the atomic `UPDATE ... WHERE curation_status = 'PROPOSED'` guard (§6) is preserved exactly.
- Exact log message wording for the failure-disclosure path (§9), provided the required fields (§9) are present.
- Whether `transition()` lives on `KnowledgeAssetService` directly or a new, adjacent service class — either is consistent with this Work Package's own established "one service class per Business Activity" precedent, since this is an Increment of the same Business Activity, not a new one.

**MUST NOT CHOOSE** (frozen by this document):
- The transition graph (§2) — only `PROPOSED`→{`VALIDATED`,`ACCEPTED`,`REJECTED`} may be implemented; no other edge.
- The relationship kind BA-05 uses (`Governed By`, `RO-DEC-WP14-BA05-02`, not this Increment's own concern to alter).
- The event's own `event_name`/`event_version`/payload field names (§8).
- The concurrency mechanism (§6) — the atomic `UPDATE...WHERE` guard, never a read-then-write sequence.
- The tenant-scoping predicate (§13).
- The authorization dependency (§4) — `require_platform_admin`, not a new permission.
- The ordering invariant (commit before publish, §9).

---

## 19. Design Decision Register

**BA04-INC-DEC-001 — Lifecycle transition graph scope**
*Context:* `EIA-001 Vol. II §13` names five `curation_status` states but no transition graph; the BA-04 charter discloses this as genuinely open three times.
*Decision:* implement exactly `PROPOSED`→{`VALIDATED`,`ACCEPTED`,`REJECTED`}, the three targets `IRA-014 §6` BA-04's own row already names; no further edge.
*Rationale:* the smallest scope faithful to the one document that does name anything (`IRA-014 §6`), applying this repository's own established minimum-sufficient-scope discipline (`CLAUDE.md §19.5`, WP-04 BA-08 precedent).
*Alternatives considered:* the full five-state graph with all plausible edges (rejected — would invent business rules no document states); only `PROPOSED`→`ACCEPTED` (rejected — narrower than what `IRA-014 §6`'s own row already authorizes, under-delivering against the charter without cause).
*Consequences:* `VALIDATED`/`REJECTED` are scope-terminal within this Increment, not constitutionally terminal.
*Affected documents:* this document (§2) only.
*Implementation constraint:* the guard (§6) enforces this scope; no code path may accept a fourth target.
*Authorization requirement:* Technical-Design-level `[C]` — no Repository Owner approval sought, mirroring `TDS-013`'s own BR-1–BR-4-mechanism precedent (a "how," not a "what," within already-delegated authority).

**BA04-INC-DEC-002 — `ACCEPTED` internal semantics**
*Context:* `RO-DEC-WP14-BA05-02` defines `ACCEPTED`'s downstream (BA-05-facing) meaning only.
*Decision:* `ACCEPTED` (and `VALIDATED`/`REJECTED`) require only that the asset currently be `PROPOSED`; no additional business precondition is enforced.
*Rationale:* no document names a further precondition; inventing one (e.g., a minimum evidence count) would be inventing a business rule.
*Alternatives considered:* requiring `VALIDATED` before `ACCEPTED` (rejected — see DEC-001); requiring additional evidence (rejected — not named anywhere).
*Consequences:* the transition is deliberately "thin" — a pure state-machine move, not a business-validation gate.
*Affected documents:* this document (§3).
*Implementation constraint:* none beyond §6's own guard.
*Authorization requirement:* `[C]`.

**BA04-INC-DEC-003 — Authorization**
*Context:* no document names a specific permission for this transition.
*Decision:* reuse `require_platform_admin` verbatim.
*Rationale:* the only actor pattern this Business Activity has ever used; charter's own established "undifferentiated interim-authorization" posture.
*Alternatives considered:* a new, narrower permission (rejected — not required by any document, and inventing one is explicitly prohibited by this task's own instruction).
*Consequences:* none — no new authorization surface.
*Affected documents:* none beyond this document.
*Implementation constraint:* `Depends(require_platform_admin)`, the existing router dependency.
*Authorization requirement:* `[B]`, no approval needed — pure precedent reuse.

**BA04-INC-DEC-004 — Concurrency mechanism**
*Context:* the charter's own cited shape precedent (`activate()`/`suspend()`) is check-then-act, unsafe per `TD-147`/BA-03's own prior defect.
*Decision:* atomic `UPDATE knowledge_asset_registry SET curation_status = :target WHERE knowledge_asset_id = :id AND organization_id = :org_id AND curation_status = 'PROPOSED'`, mirroring `claim_for_resolution` exactly.
*Rationale:* the repository's own proven, already-certified fix for this exact defect class; explicitly required by this task's own "do not copy the unsafe pattern" instruction.
*Alternatives considered:* `SELECT ... FOR UPDATE` (rejected — dialect-specific, `claim_for_resolution`'s own docstring already rejected this for portability); a version/`updated_at` column (rejected — none exists, and none is justified by this Increment's own minimum needs).
*Consequences:* exactly one of two concurrent requests succeeds; the other receives `409`.
*Affected documents:* none beyond this document.
*Implementation constraint:* the exact `WHERE` clause above; no plain `get_by_id()`-then-assign sequence permitted.
*Authorization requirement:* `[C]`, mandated by this review cycle's own explicit instruction not to reproduce the unsafe pattern.

**BA04-INC-DEC-005 — Transition idempotency**
*Context:* a retried transition request could be misinterpreted as a repeat success.
*Decision:* a retry after success returns `409`, not a silent `200`.
*Rationale:* mirrors BA-03's own established "already resolved → 409" precedent; avoids a caller mistaking a stale retry for a fresh success.
*Alternatives considered:* returning `200` idempotently on retry (rejected — would require distinguishing "my own retry" from "someone else's concurrent request," which the guard alone cannot do without additional state this design does not introduce).
*Consequences:* callers needing current state after a `409` use the existing `GET`.
*Affected documents:* none.
*Implementation constraint:* none beyond §6's own guard, which already produces this behavior for free.
*Authorization requirement:* `[C]`.

**BA04-INC-DEC-006 — Domain Event contract**
*Context:* no document names a concrete event class, name, version, or payload for this outcome.
*Decision:* `event_name = "aurex.aiservice.knowledge_asset.accepted"`, `event_version = "1.0.0"`, payload = `{knowledge_asset_id, organization_id, previous_status, new_status}`.
*Rationale:* follows the framework's own documented naming convention exactly; payload fields are the minimum BA-05 needs (§17) plus the framework's own required `validate()`/`to_dict()`/`from_dict()` contract.
*Alternatives considered:* omitting `organization_id` from the payload and relying on envelope `tenant_id` alone (rejected — envelope `tenant_id` can fall back to `"SYSTEM"`, per `event_base.py:38`, and is not guaranteed to equal the Knowledge Asset's own persisted value).
*Consequences:* BA-05's own future `KnowledgeGraphSyncHandler` can deserialize this event once it exists.
*Affected documents:* none beyond this document; `TDS-013` is not modified by this document (§25).
*Implementation constraint:* exact field names above.
*Authorization requirement:* `[C]`.

**BA04-INC-DEC-007 — DB/event consistency posture — `APPROVED`, 2026-08-16 (`RO-DEC-BA04-INC-007`)**
*Context:* the real event publisher is verified mock-only; no durable delivery exists today.

*Decision:* **best-effort event delivery is accepted for the BA-04 Increment's own current implementation scope.** The required and sole consistency invariant is: `DATABASE COMMIT → DOMAIN EVENT PUBLISH ATTEMPT`. The event MUST NOT be published before the corresponding Knowledge Asset state transition has successfully committed; a DB rollback means no `ACCEPTED` event publication is ever attempted; a DB commit means publication is attempted exactly once (§7B). This decision does **not** claim guaranteed delivery, exactly-once delivery, eventual delivery, automatic retry, replay, recovery after process failure, Kafka durability, or transactional event publication — none of these is provided, and this document does not claim otherwise.

*Rationale (Repository Owner's own, recorded verbatim):* DB commit precedes publication; no event can represent a rolled-back state; current publisher infrastructure is mock-only; durable delivery infrastructure is outside this Increment; the Repository Owner explicitly accepts the possibility that an `ACCEPTED` transition may not produce a delivered event.

*Alternatives considered:* building a transactional outbox now (rejected by the Repository Owner as disproportionate to this Increment's own current scope — remains a named future platform concern, §21); silently assuming the mock publisher is reliable (rejected — dishonest, and the independent authorization review specifically warned against this); introducing retry infrastructure within this Increment (rejected — explicitly out of scope for this decision).

*Consequences:* `ACCEPTED` is authoritative the moment DB commit succeeds, independent of event outcome; event delivery is not guaranteed; BA-05 may not execute for a given transition if the event is not delivered (§17 — an accepted limitation of this Increment, not a defect); a publication failure is observable through the existing structured-logging/observability mechanism (§11), recorded as an event-publication failure, never as a failed Knowledge Asset transition; no automatic retry or replay exists in this Increment. Five accepted failure/consistency cases are enumerated in full in §9 above (DB failure; normal flow; publish failure; process crash before publish; no durable replay on later recovery) — each explicitly accepted by this decision, not merely tolerated by omission.

*Affected documents:* this document only (§9, this entry). `TDS-013`'s own trigger model (`RO-DEC-WP14-BA05-01`) is unchanged — the approved trigger remains the BA-04 `ACCEPTED` Domain Event; BA-05 must not independently poll or invent an alternative trigger to compensate for this decision.

*Implementation constraint:* commit-then-publish ordering (already frozen, §9); try/except around the single `publish()` call, non-retrying; no outbox, no new event store, no generalized event-delivery subsystem introduced by this Increment.

*Authorization requirement:* `[A]` — Repository Owner decision recorded, no longer open. Durable Domain Event delivery (transactional outbox, durable event store, retry, replay, dead-letter handling, guaranteed-delivery semantics) remains an explicitly named **future platform-level design concern**, not decided, scheduled, or foreclosed by this entry.

**BA04-INC-DEC-008 — Event delivery/retry**
*Context:* no live broker exists; DLQ is log-only.
*Decision:* no new retry/redrive mechanism is built by this Increment; BA-04 publishes at most once per successful transition (§7B) and does not itself retry a failed `publish()` call.
*Rationale:* building retry infrastructure without a real broker to retry against is premature; matches this Increment's own minimum scope.
*Alternatives considered:* an application-level retry loop around `publish()` (rejected — risks Case C duplicate-publish if a "failed" call actually partially succeeded; better handled once real broker semantics exist).
*Consequences:* delivery reliability is bounded by whatever DEC-007 resolves to.
*Affected documents:* none.
*Implementation constraint:* none beyond DEC-007.
*Authorization requirement:* `[C]`, subordinate to DEC-007's own resolution.

**BA04-INC-DEC-009 — Tenant validation**
*Context:* the event payload carries `organization_id`, which must not be treated as independently authoritative by BA-05.
*Decision:* the payload field is explicitly documented (§8, §17) as a hint, not ground truth; BA-05 must independently re-validate against its own same-database read.
*Rationale:* directly required by `RO-DEC-WP14-BA05-02`'s own text.
*Alternatives considered:* omitting the field entirely and forcing BA-05 to look it up fresh every time (rejected — the field is still useful as a fast-path/sanity-check value, provided it is never trusted blindly).
*Consequences:* none beyond the documentation obligation on BA-05's own future implementation.
*Affected documents:* none beyond this document.
*Implementation constraint:* none for BA-04 itself; a constraint on BA-05's own future code.
*Authorization requirement:* `[A]`, already settled by `RO-DEC-WP14-BA05-02`.

**BA04-INC-DEC-010 — Audit/evidence semantics**
*Context:* no document specifies the transition's own audit shape.
*Decision:* extend the existing `record_audit` pattern (§11) — `SUCCESS` for the winner, `DENIED` for a losing/already-transitioned/not-found request.
*Rationale:* direct, low-risk extension of BA-04's own already-certified `establish()` pattern; `DENIED` (not `FAILED`) matches this repository's own established, independently-reconfirmed semantic split (foreseeable business-rule rejection vs. unexpected system fault).
*Alternatives considered:* a new evidence-registry row per transition (rejected — no document requires Evidence for a state transition, only for `establish()`'s own `provenance_reference`).
*Consequences:* none beyond the new `record_audit` calls.
*Affected documents:* none.
*Implementation constraint:* action names `TRANSITION_KNOWLEDGE_ASSET`; resource `knowledge_asset:{id}`.
*Authorization requirement:* `[C]`.

---

## 20. Traceability Matrix

| Requirement | Authoritative Source | Design Decision | Implementation Constraint | Verification Method |
|---|---|---|---|---|
| Transition endpoint exists | `IRA-014 §6` BA-04 row | §5, DEC-001 | `POST .../transition` | API test: 200 on valid transition |
| Only `PROPOSED`→{V,A,R} legal | `IRA-014 §6`; DEC-001 | §2 | Guard predicate (§6) | Test: `VALIDATED`→`ACCEPTED` rejected (409 or 422 per design) |
| Exactly one concurrent winner | `TD-147`; BA-03 precedent; this task's own mandate | §6, DEC-004 | Atomic `UPDATE...WHERE` | Concurrency test, `asyncio.gather`, mirroring `test_intelligence_candidate_resolve_concurrency.py` |
| `ACCEPTED` publishes exactly one event, others none | `RO-DEC-WP14-BA05-01` | §8/§9 | Event call only inside the `ACCEPTED` winner branch | Test: assert event captured only for `ACCEPTED`, never `VALIDATED`/`REJECTED` |
| Event contains `knowledge_asset_id`/`organization_id`/fact of acceptance | `RO-DEC-WP14-BA05-02` | §8, DEC-006 | Payload field names frozen | Test: deserialize event, assert fields |
| No cross-tenant transition | `CLAUDE.md §21.4` | §13 | `WHERE organization_id = :org_id` | Mandatory Tenant-Isolation Test Checklist: two-org fixture, cross-org 404 |
| `establish()`/`get_by_id()` unaffected | Charter, this document §16 | §16 | No shared code path touched | Full BA-04 regression suite re-run, 13/13 expected unchanged |
| Audit on every outcome | This repository's own precedent (`conversation_service.py`, BA-03) | §11, DEC-010 | `record_audit` calls | Test: `caplog`-based audit assertions, mirroring BA-03's own pattern |
| Best-effort event delivery, disclosed | `RTA-001 §8.10`; verified mock publisher | §9, DEC-007 | try/except + structured log | Manual/log-inspection verification; **DEC-007 itself requires a Repository Owner decision before implementation** |

---

## 21. Open Repository Owner Decisions

**None remain open.** `BA04-INC-DEC-007` (DB/event consistency posture) — the sole item requiring Repository Owner approval — was resolved 2026-08-16 via direct Repository Owner instruction ("WP-14 BA-04 Increment — Repository Owner Decision, RO-DEC-BA04-INC-007 — Database / Domain Event Consistency Posture"): **best-effort event delivery is APPROVED for this Increment's own current scope**, with the ordering invariant (`DB COMMIT → EVENT PUBLISH ATTEMPT`) as the sole consistency guarantee, and no durable-delivery guarantee of any kind claimed. Full decision text recorded in §19 above (`BA04-INC-DEC-007`).

This closes the last open item from the prior independent authorization review. Every other previously-open item (`§5` transition graph scope, `§6` concurrency mechanism, `§8` event contract, `§7` idempotency, `§4` authorization, `§13` tenant isolation) was already resolved as an explicit, labeled `[C]` Technical Design decision within the authority `IRA-014`/the charter already delegate to Technical Design, mirroring exactly how `TDS-013` itself resolved BR-1–BR-4's own enforcement mechanism without requiring a fresh Repository Owner decision for that "how" question.

**Durable Domain Event delivery** (transactional outbox, durable event store, retry, replay, dead-letter handling, guaranteed-delivery semantics) **remains an explicitly named future platform-level design concern**, not decided, scheduled, or foreclosed by `RO-DEC-BA04-INC-007` — it is not decided *in* this document at all, only named as a future concern outside this Increment's own scope.

---

## 22. Implementation Boundary

(See §18 above — retained as a separate heading only for numbering parity with this task's own requested structure; content is identical, not duplicated further here.)

---

## 23. Authorization Readiness

| # | Dimension | Status |
|---|---|---|
| 1 | Business semantics | READY (§1/§3, `RO-DEC-WP14-BA05-01/02` + this document's own `[C]` decisions) |
| 2 | State machine | READY, scoped (§2, DEC-001 — full five-state graph remains `[D]` but is out of this Increment's own minimum scope, not a blocker to it) |
| 3 | `ACCEPTED` semantics | READY (§3) |
| 4 | Authorization | READY (§4, pure precedent reuse) |
| 5 | API/service | READY (§5) |
| 6 | Event contract | READY (§8, DEC-006) |
| 7 | Event consistency | READY — `RO-DEC-BA04-INC-007` (§19/§21) approved a best-effort posture with the commit-then-publish ordering invariant as the sole guarantee; no further Repository Owner input required for this Increment's own scope |
| 8 | Concurrency | READY (§6, DEC-004) |
| 9 | Idempotency | READY (§7) |
| 10 | Tenant isolation | READY (§13) |
| 11 | Evidence/audit | READY (§11) |
| 12 | Data model | READY (§12, no change required) |
| 13 | Regression | READY (§16) |
| 14 | BA-05 compatibility | READY (§17) |
| 15 | Architecture | READY (§1 out-of-scope list; no new capability/relationship kind) |
| 16 | Testability | READY (§20's own traceability matrix ties every requirement to a concrete verification method) |
| 17 | Observability | READY (§9's own structured-log requirement; reuses `correlation_id`/existing logger conventions, no new platform) |

17 of 17 dimensions READY — every design decision this specification requires, including the transition graph, concurrency mechanism, event contract, and DB/event consistency posture, is now explicit and either Technical-Design-level `[C]` (within delegated authority) or `[A]` (a recorded Repository Owner decision, `RO-DEC-BA04-INC-007`).

---

## 24. Governance Status

**`BA-04 Increment = DESIGNED / READY FOR FRESH INDEPENDENT TECHNICAL DESIGN AUTHORIZATION REVIEW.`** This document does not itself authorize implementation — only a fresh, independent reviewer, uninvolved in authoring this document, may determine whether it is now sufficiently specified and whether the accepted best-effort consistency posture is permissible under the governing architecture. `BA-04 = CLOSED / CERTIFIED / PUSHED`, unaffected, unchanged, unreopened by this document. `BA-05 = DESIGNED / NOT AUTHORIZED / ZERO IMPLEMENTATION`, unaffected — no BA-05 code, migration, or logic is created, modified, or implied to exist by this document beyond what `RO-DEC-WP14-BA05-01/02/03` already established. `TDS-013`'s own trigger model is unchanged.

## 25. Final Recommendation

**READY FOR INDEPENDENT TECHNICAL DESIGN AUTHORIZATION REVIEW.**

All seventeen authorization-readiness dimensions are now resolved by this document's own explicit, labeled decisions (§19) — sixteen as Technical-Design-level `[C]` decisions within the authority already delegated to Technical Design by `IRA-014`/the BA-04 charter (mirroring exactly how `TDS-013` itself resolved BR-1–BR-4's own enforcement mechanism), and one (`BA04-INC-DEC-007`, DB/event consistency posture) as a recorded Repository Owner decision (`RO-DEC-BA04-INC-007`, 2026-08-16), not silently defaulted or converted into Technical Debt. No open Repository Owner decision remains. This document itself does not authorize implementation — a fresh, independent Technical Design Authorization Review of this completed specification is the required next governed step.

---

*End of TDS-014. No implementation, migration, model, router, service, API, frontend, event publisher, or test has been created or authorized by this document. `Backend/Services/AIService/models/knowledge_asset.py`, `services/knowledge_asset_service.py`, `routers/knowledge_assets.py`, `RTA-001`, `ONT-001`, and all BA-05 files remain unmodified. `TDS-013` is not modified by this document — it is cross-referenced only, per this task's own explicit instruction that BA-05's own design remain there and this Increment's own design remain here.*
