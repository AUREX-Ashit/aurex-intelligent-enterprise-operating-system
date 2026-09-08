# ROD-C132 — Enterprise Notifications: Capability-Boundary and Minimum-Scope Decision

**Document type:** Repository Owner Decision record (same class as `ROD-C040-Blocker-Closure-Assessment.md`, `ROD-ADR-002-Platform-Administrative-Identity.md`, `ROD-ADR-002-Internal-Option-Selection.md`) — a decision brief followed by a recorded Repository Owner decision, preceding the formal governance artifact (a future `IRA-C132`) that will cite it.

**Capability:** C-132 Enterprise Notifications (`CAP-001` line 105 — Active, Domain D-007 Collaboration & Engagement, owning specification `SD-003`).

**Recorded:** 2026-09-05, per direct Repository Owner instruction ("AUREX — C-132 Accelerated Governance Pass — Repository Owner Authorization"), following a prior read-only "C-132 Capability-Boundary Decision Brief" (this same session) that investigated `CAP-001`, `SD-003` §8/§9, `SER-001` `SE-018`/`SE-017`/`SE-040`/`SE-051`, `DS-001` Chapter 21 (Notification Styling, `DS-001-345`–`360`), the existing frontend notification scaffold (`NotificationCenter.tsx`, `lib/notifications.tsx`/`Toaster.tsx`), `Backend/Shared/Events`, `Backend/Shared/Logging`, `TECH-DEBT.md TD-151`, and the `C-066`/`C-023` minimum-scope precedents (`IRA-C066`/`WP-15`, `TDS-C023`/`WP-17`).

**Authority:** Repository Owner (same decision-authority pattern already established for `C-040`'s own pre-IRA decisions recorded in `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`, and for `ADR-002`'s own two `ROD-*` decision briefs).

---

## 1. RO DECISION 1 — C-131 / C-132 Boundary

**SELECTED: OPTION A — Clean initiator-based split.**

- **C-131 Enterprise Communication** owns human-authored comment/mention content: in-context collaboration attached to a specific business object, per `SD-003` §9 (Collaboration, Comments & Organizational Memory Laws, `SD-003-135`–`152`), becoming permanent organizational memory (`SD-002-100`/L37). Never a detached chat thread.
- **C-132 Enterprise Notifications** owns the resulting system-generated notification — including a notification generated when a user is mentioned.
- The originating C-131 content remains C-131-owned; the resulting notification record is C-132-owned. The seam is preserved explicitly, not collapsed.
- This is a **semantic ownership decision only**. It does not authorize implementation of C-131, C-132, or any notification delivery mechanism. It does not mean C-132 owns all communication.

## 2. RO DECISION 2 — C-132 / C-133 Boundary

**SELECTED: OPTION C — Build C-132 independently now, with explicit future-reconciliation disclosure.**

- C-132 may proceed independently because C-133 Activity Stream & Timeline is currently `CAP-001` **Planned**, not Active, and is not chartered.
- The first C-132 increment does **not** pre-decide that C-132 and C-133 can never share infrastructure or data.
- A future C-133 charter **must** explicitly assess whether C-133 should reconcile with, absorb, consume, or otherwise relate to C-132's own notification history.
- No shared schema, shared service, common ledger, or future merge is authorized by this decision.
- No C-133 activation is authorized.
- This is a sequencing and boundary decision, not an implementation decision.

## 3. RO DECISION 3 — First C-132 Business Activity Minimum Scope

**SELECTED: OPTION A — Notification record only.**

The first C-132 BA may be scoped to:
- establish Notification
- manage Notification
- list / read Notification
- acknowledge Notification

**Explicitly excluded from this first BA:**
- email delivery
- SMS delivery
- push delivery
- webhook delivery
- external channel delivery
- delivery-provider integration
- real event-bus / event-subscriber infrastructure
- multi-channel notification orchestration

The first increment is therefore a persisted, user-facing, in-application Notification record. This is a **minimum-scope governance decision only**. It does not authorize implementation.

## 4. RO DECISION 3a — `SD-003-226` Interruption Ceiling / Digest

**SELECTED: OPTION B — Defer.**

- The full `SD-003-226` per-user daily interruption ceiling and end-of-day digest mechanism are **deferred** from the first C-132 BA.
- This deferral must be explicit and visible in the eventual IRA/TDS/charter.
- The first BA must not silently claim to implement the complete interruption-ceiling/digest regime.
- Any resulting constitutional-scope limitation must be disclosed.
- The deferred mechanism remains a future C-132 scope item and is not abandoned.
- This decision does not authorize implementation of the deferred mechanism.

---

## 5. Architectural Clarification (recorded, not a new decision)

The following distinctions are recorded without being collapsed:

**Notification is NOT:**
- an Audit Event
- a Domain Event
- a Timeline Event
- a C-131 comment/mention

**Relationships that MAY exist in the future, without changing the ownership decisions above:**
- A Notification may in the future be **caused by** a Domain Event, once real event infrastructure exists.
- A Notification may be **related to** a C-131 mention (per RO Decision 1's own seam).
- A future C-133 Timeline may potentially **consume or represent** related historical information (per RO Decision 2's own reconciliation clause).

None of these possible future relationships changes RO Decisions 1–3a.

---

## 6. Event-Infrastructure Finding (dependency / future consideration — not a decision)

Recorded as an implementation dependency and future consideration, independently re-verified this session by direct source read:

- `Backend/Shared/Events` (`event_publisher.py`, `event_subscriber.py`) defines `EventPublisher`/`EventSubscriber` as **abstract contracts** — `publish()`/`publish_async()` and `start()`/`stop()` are all `@abstractmethod`.
- **No concrete `EventSubscriber` subclass exists anywhere in this repository** (independently confirmed, corroborating `TECH-DEBT.md TD-151`).
- The `publish_event()` function every closed Work Package actually calls (`Backend/Services/*/observability.py`) is, by its own docstring, **"a structured-log-based stand-in for `Backend/Shared/Events`' `EventPublisher`/`CloudEvent` abstraction"** — a JSON log line, not a queryable or subscribable event.
- **Therefore, the first C-132 BA is intentionally NOT being authorized around a real event-driven delivery architecture.** No event infrastructure is created or repaired by this decision record.

---

## 7. Non-Authorization (explicit)

This document records governance decisions only. It does **NOT** authorize:

- IRA creation or acceptance
- TDS creation
- WP creation or registration
- BA charter creation or approval
- Implementation Authorization of any kind
- schema creation
- migration creation or execution
- frontend implementation or modification
- backend implementation or modification
- event-bus implementation or repair
- delivery infrastructure of any kind
- any `CLAUDE.md §19.7b` gate (1 through 5)
- certification of any kind
- release or closure of any kind

**Governance sequence, as recorded:** this decision → future `IRA-C132` → Strategic Enhancement Review → Historical Screen Review → Executive Cognition Review → existing-asset discovery → Business Object eligibility analysis → DS-001 conformance check → IRA acceptance → TDS → WP registration → BA charter → separate, explicit Implementation Authorization → implementation → `CLAUDE.md §19.7b` five-gate closure. **This document does not advance past "capability-boundary and minimum-scope decided" in that sequence.**

---

## 8. Change Control

**Files created:** this document only.
**Files modified by this pass:** `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md` — C-132 row only (strikethrough-preserve, additive), recorded in a companion edit to this document, per the same authorization.
**Not modified:** `CAP-001`, `SD-003`, `PE-001`, `DS-001`, `SER-001`, `WPR-001`, `C-130`/`C-131`/`C-133` rows or the `D-007` domain summary in the delivery map, any `Backend/`/`source/frontend/` file, any migration, any test, any other governance artifact. Nothing staged, committed, or pushed.

*End of ROD-C132.*
