# IRA-C132 — Enterprise Notifications (C-132) — Implementation Readiness Assessment

**Document ID naming note (established fact, mirrors `IRA-C066`'s and `IRA-C114`'s own precedent):** this document is named capability-first, with no WP number, exactly as `IRA-C066` and `IRA-C114` were. No WP number exists for C-132 anywhere in `WP-REG-001` or `WPR-001` as of this drafting (`WPR-001 §3`'s own Maintenance Rule: "No future WP may be added speculatively... until it is properly assigned"). Capability-first naming avoids misrepresenting this document as governing an already-numbered, unrelated Work Package.

**Repository Owner authorization basis for this document:** a sequence of explicit Repository Owner instructions, this session — (1) a C-132 Capability-Boundary Decision Brief (read-only); (2) the Repository Owner's own recorded capability-boundary and minimum-scope decisions, `architecture/06-Reviews/ROD-C132-Enterprise-Notifications-Capability-Boundary-and-Minimum-Scope.md`; (3) a companion portfolio-status update, `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md` C-132 row; (4) an eight-workstream, read-only IRA-preparation evidence pass, consolidated into a "C-132 IRA Preparation Dossier"; (5) the Repository Owner's own explicit instruction to draft this document: *"Proceed with the formal IRA investigation and create the canonical IRA-C132 artifact using the repository's established IRA location, naming and structure conventions."* This document begins the governed IRA process against that already-decided boundary and scope — it does not reopen, reinterpret, or re-derive RO Decisions 1, 2, 3, or 3a.

---

## 1. Executive Summary

**(Established fact.)** C-132 Enterprise Notifications is `CAP-001`-registered (line 105 — Active, Domain D-007 Collaboration & Engagement, owning specification `SD-003`). No Business Activity has ever been chartered against C-132. No IRA has ever existed for it before this document. No `PE-001-C132` exists (a posture this repository has twice before found not disqualifying — `IRA-C066`, `IRA-C114`).

**(Repository Owner decisions, recorded, not re-derived by this document — `ROD-C132-Enterprise-Notifications-Capability-Boundary-and-Minimum-Scope.md`.)**
- **RO Decision 1** — C-131/C-132 boundary = Option A: C-131 owns human-authored comment/mention content (`SD-003` §9); C-132 owns the resulting system-generated notification, including a mention-notification.
- **RO Decision 2** — C-132/C-133 boundary = Option C: C-132 proceeds independently now; C-133 remains Planned/unchartered; a future C-133 charter must assess reconciliation; no shared schema/service/merge is authorized now.
- **RO Decision 3** — first-BA minimum scope = Option A: a Notification record only — establish / manage / list / read / acknowledge; email/SMS/push/webhook/provider-integration/real-event-bus/orchestration explicitly excluded.
- **RO Decision 3a** — `SD-003-226` interruption-ceiling/digest = Option B: deferred, not abandoned; must remain explicitly visible in this and every subsequent governance artifact.

**Readiness verdict (§17): 🟡 AMBER — READY FOR TECHNICAL DESIGN, CONDITIONAL ON ONE OUTSTANDING REPOSITORY OWNER DECISION (service hosting).** IRA Acceptance is **NOT YET GRANTED** by this document — per this repository's own no-self-authorization discipline (`CLAUDE.md §19.1`), acceptance requires a separate, future Repository Owner review and decision, exactly as `IRA-C066 §18` and `IRA-C114 §18` each record for themselves.

---

## 2. Capability Analysis

**(Established fact, `CAP-001` line 105, direct read.)**

| Field | Value |
|---|---|
| Capability ID | C-132 |
| Capability Name | Enterprise Notifications |
| Business Intent | "Deliver notifications." |
| Domain | D-007 — Collaboration & Engagement (C-130–C-149) |
| Owning Specification | `SD-003` (Enterprise Interaction Laws) |
| Status | Active |

**(Established fact, `SD-003` §8, direct read.)** Section 8 ("Notifications, Attention & Cognitive Load Laws," approximately `SD-003-117`–`134`, plus `SD-003-226` new) "operationalize[s] L9 (Maximum 7 Items) and L10 (Intelligent Silence) at the interaction level: how notifications are prioritized, batched, and suppressed... and how the platform decides that 'no notification' is the correct outcome for a given event." `SD-003-226` (fully specified, the only individually-restated rule in §8) establishes a per-user daily interruption ceiling (default 12/working day, tenant-adjustable) enforced across all notifications/escalations/routed items targeting that user, with an end-of-day digest fallback for items over the ceiling except where materiality (`SD-002-057`) requires immediate delivery.

**(Established fact, boundary evidence, per `ROD-C132` and the IRA Preparation Dossier §3.)** `SD-003` §9 ("Collaboration, Comments & Organizational Memory Laws," approximately `SD-003-135`–`152`) governs "in-context collaboration (comments, mentions, and discussion attached to a specific business object, never a detached chat thread)" becoming permanent organizational memory. RO Decision 1 draws the C-131/C-132 boundary at this §8/§9 seam. **(Disclosed, not resolved by this document.)** `CAP-001`'s own Primary Specification column assigns `SD-003` to **C-130** (Enterprise Collaboration), not C-131 (whose column reads `PE-001`) — RO Decision 1's own citation of `SD-003` §9 for C-131 sits against this registry framing. This is not re-litigated here; it is carried forward as an open item (§16, item 1) for a future C-130/C-131 charter to reconcile, exactly as the IRA Preparation Dossier §3 already disclosed it.

---

## 3. Existing Asset Discovery (`CLAUDE.md §19.2`, `IMP-001 §6.2a`)

**(Established fact, re-confirmed by direct repository inspection across Workstreams B and E of the IRA Preparation Dossier — not accepted from a prior session's summary alone.)**

### 3.1 Frontend — a real, honest, partially-compliant scaffold exists

- `source/frontend/src/components/layout/NotificationCenter.tsx` — a real, accessible (focus-trap, `aria-*`, overlay-close-on-outside-click), reusable panel, already globally mounted (via `GlobalHeader.tsx` → `AdminShell.tsx`, live on every `/platform-admin/(workspace)/*` route). Its own header comment cites `SD-003` §8 by name and states it is "ready to display notifications once a capability publishes them." Currently renders a static, honest empty state — no data source. **Directly reusable, not to be rebuilt.**
- `source/frontend/src/lib/notifications.tsx` + `source/frontend/src/components/ui/Toaster.tsx` — a separate, generic, ephemeral, client-only toast mechanism (`NotificationTone: "info"|"success"|"warning"|"danger"`, 5s auto-dismiss, `role="status"`). This is UI-feedback plumbing already used by other features (e.g. `useEntitlementLicense.ts`) to show "Established." toasts after an API call. **Not the persisted Notification business object** — reusable only as UX plumbing for reacting to a future C-132 API response, and its tone model is a useful reference for the DS-001 severity mapping (§10), not a substitute for it.
- `source/frontend/src/config/admin-navigation.ts` — a nav entry (slug `notifications`) already routes to `source/frontend/src/app/platform-admin/(workspace)/notifications/page.tsx`, currently a bare `PlaceholderPage` ("Platform notification configuration"). This route is unrelated in content to `NotificationCenter.tsx` and would need its own disposition (repurpose vs. leave as a separate future admin-config surface) at TDS time — not decided by this document.
- **Structural precedent:** the `source/frontend/src/features/entitlement-license/{components/*.tsx, state/useEntitlementLicense.ts}` shape (WP-17, C-023) is the established per-capability frontend pattern this repository would likely mirror for C-132's own establish/list/read/acknowledge screens — cited as precedent, not prescribed.

### 3.2 Backend — genuinely zero footprint

**(Established fact.)** A repository-wide, case-insensitive search of `Backend/` (excluding `venv`/`__pycache__`) for "notification" returns zero domain hits — the only two matches are unrelated generic-English uses of the word "notification" inside `Backend/Runtime/AuthorizationEngine`'s own Observer-pattern documentation. No model, repository, service, router, or schema file for Notification exists anywhere. `AuthService/models/__init__.py` and every `AIService/models/*.py` file were directly read; neither registers anything notification-shaped.

### 3.3 Shared infrastructure — audit and event mechanisms are cross-cutting, log-only, and structurally inapplicable as a Notification's own persistence layer

- `Backend/Shared/Logging/audit_logger.py` (`AuditLogger`) and each service's own `observability.py::record_audit()` — confirmed, by direct read, to be **log-only**: a structured payload written via Python `logging`, no database table, no query API anywhere. Used from 40+ call sites across `AuthService`/`AIService`. Directly confirms, structurally (not merely by definitional fiat), that **Notification ≠ Audit Event** — an audit record has no independent list/read/acknowledge surface of its own, and a Notification's own establish/acknowledge action should itself *call* `record_audit()` as every other Business Activity does, not *be* one.
- `Backend/Shared/Events/{event_publisher.py, event_subscriber.py, event_registry.py}` — `EventPublisher.publish()/publish_async()` and `EventSubscriber.start()/stop()` are `@abstractmethod`. Two `EventPublisher` subclasses exist (`KafkaEventPublisher`, `AzureServiceBusEventPublisher`) but their real broker-dispatch calls are commented out ("MOCK OUTBOUND BROADCAST FOR ARCHITECTURE STAGE"); zero production `EventSubscriber` subclass exists anywhere (one test-only fixture found, `AIService/tests/test_knowledge_graph_sync_handler.py::_NoOpSubscriber`); only one event type (`KnowledgeAssetAcceptedEvent`, WP-14) is ever registered in the shared `EventRegistry`. No broker SDK dependency is declared in any service's `requirements.txt`. **`TECH-DEBT.md TD-151`** additionally records that even the abstract dispatch path does not `await` an `async def` handler — a defect that would apply the moment a concrete subscriber is ever built.
- `publish_event()` (`AuthService/observability.py`, self-documented as *"a structured-log-based stand-in for `Backend/Shared/Events`' `EventPublisher`/`CloudEvent` abstraction"*) is the pattern every closed Work Package with an "event" actually uses — a JSON log line, not a queryable or subscribable event. `AIService` has no `publish_event` at all (it calls the mock `KafkaEventPublisher` directly instead); `ReportingService`/`IngestionService`/`TenantService` have no event-emission primitive of any kind. **Confirms, structurally: Notification ≠ Domain Event** — no live event bus exists anywhere in the running platform to source a Notification from, or to deliver one through.
- **Confirmed proven pattern:** `Backend/Services/AuthService/services/entitlement_license_establishment_service.py` (WP-17) calls `record_audit()` then `publish_event()` **synchronously, in-process, mid-transaction, unawaited**, immediately after its own write is flushed. Direct service-to-service in-process composition (one service's own class directly calling another's method, not merely a shared helper) is independently established elsewhere (`EstablishPersonContextService` → `PersonRecognitionService`, and two similar pairs). **This is the concrete, already-certified precedent for how a future `NotificationService.create(...)`-style call would be invoked by a causing capability's own service layer, with no event bus involved.**

### 3.4 No prior IRA/BA/WP/charter for C-132

Confirmed by direct inspection of `WPR-001` (WP-00 through WP-18, plus WP-13/WP-RTA-001 — no C-132 entry anywhere) and `WP-REG-001`.

---

## 4. RO Decision History (recorded, not re-derived)

Reproduced from `ROD-C132-Enterprise-Notifications-Capability-Boundary-and-Minimum-Scope.md` verbatim in substance (see that document for the full text; this section is a pointer and summary, not a re-decision):

1. **C-131/C-132 boundary — Option A.** C-131 owns human-authored comment/mention content (`SD-003` §9); C-132 owns the resulting system-generated notification, including mention-notifications. Semantic ownership only — does not authorize implementation of either capability.
2. **C-132/C-133 boundary — Option C.** C-132 proceeds independently; C-133 stays Planned/unchartered; a future C-133 charter must assess reconciliation/absorption/consumption; no shared schema/service/merge authorized now; no C-133 activation authorized.
3. **First-BA minimum scope — Option A.** Notification record only: establish / manage / list / read / acknowledge. Explicitly excluded: email, SMS, push, webhook, external-channel delivery, provider integration, real event-bus/subscriber infrastructure, multi-channel orchestration.
4. **`SD-003-226` interruption ceiling/digest — Option B (defer).** Deferred, not abandoned; must remain explicitly visible in this and every subsequent governance artifact — see §9 and §16 below.

**This IRA does not reopen, reinterpret, or add to these four decisions.**

---

## 5. Strategic Enhancement Disposition (`CLAUDE.md §21.3`)

**(Established fact.)** `SER-001` `SE-018` ("Notification backend and frontend wiring. No Notification model/table/API exists; the frontend shell is an honest, self-disclosed empty state") remains classified **Deferred** as of this drafting — correctly so, per `SER-001`'s own design ("an enhancement is a not-yet-built capability or feature, not a decision awaiting resolution") and Maintenance Rule (status changes are recorded "when an item is implemented," by that Work Package's own IRA). This document is the first IRA to formally engage `SE-018`.

**Disposition recorded by this IRA:** `SE-018` remains **Deferred** as of IRA acceptance (no implementation exists yet). Upon future implementation of the minimum-scope first BA described in §9 below, the eventual Implementation Report should reclassify `SE-018` as **Partially Implemented**, naming exactly which part is delivered (persisted record, establish/list/read/acknowledge) and which part remains open (all delivery channels; real event-bus infrastructure; the `SD-003-226` interruption-ceiling/digest regime, per RO Decision 3a).

Adjacent enhancements, reviewed and found not to require reclassification by this IRA:
- **`SE-040`** (C-133 Activity Stream & Timeline charter) — remains Deferred/Not Applicable to this BA, consistent with RO Decision 2's own text ("No C-133 activation is authorized").
- **`SE-017`** (feature-flag frontend wiring) and **`SE-051`** (general retention policy, 7-year constitutional floor) — no dependency link to C-132 exists in `SER-001` itself; noted as topically adjacent (feature-flagging a future notification rollout; retention policy for notification records, §9 below) but not owned or absorbed by this IRA.

---

## 6. Historical Screen Review (`CLAUDE.md §21.3`)

**(Established fact.)** `HISTORICAL-SCREEN-REALIZATION-MATRIX.md`'s own 14-item classification table names no Notification, Alert, Activity Stream, Timeline, Inbox, or Attention Center concept anywhere. Every incidentally notification-shaped affordance found in the underlying historical `.html` sources — a bell/badge nav item (`06-admin-dashboard.html`), an email/in-app notification preference toggle (`05-my-profile.html`), a simulated `showToast` deferral message (`I1_Intelligence_Center.html`), an alert-routing question (`G1_Organisation_Setup.html`) — is a subordinate element nested inside a *different* concept, and every hosting concept is either already **RETIRE CONCEPT** (not enterprise-facing) or tied to a different, unchartered capability (C-090/091/093 Enterprise Intelligence), never to C-132.

**No relevant historical screen concept exists for C-132.** This is the identical, "genuinely nothing found, not a blocker" disposition `IRA-C066 §6b` and `IRA-C114 §6b` each independently reached for their own capabilities.

---

## 7. Executive Cognition Review (`CLAUDE.md §21.3`)

**(Established fact.)** `EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md` never names notifications, alerts, or attention anywhere; it places no direct constraint on C-132. The "never through flashing indicators, red badges without context, or notification-style visual noise" language is **`SD-001-056`** (`SD-001` §8, the Sacred 12 / Two-Layer model) — a distinct principle from `DS-001` Chapter 21's own Notification Styling specification (`DS-001`'s own Ownership Matrix: "Notification Styling | DS-001 | Not addressed in SD-001"). These share vocabulary, not authority.

**(Recommendation, explicitly flagged as inference, not a canonical determination — carried forward as an open item, not decided here.)** If a future C-132 notification is ever surfaced on a Sacred 12 (executive, Layer 2) screen, the combination of the Strategy document's own Understand-stage model and `SD-001-054`/`056`/`057` would suggest: consumption only as already-Layer-1-resolved evidence (never a discovery widget, per `SD-001-054`'s "consume, they do not discover"), never rendered as a badge/flashing/notification-styled element on that screen (`SD-001-056`), and always paired with a stated financial/governance consequence rather than a bare count (`SD-001-057`). This inference is **not required for, and does not block, the minimum first-BA scope** (§9), which delivers only a Layer-1 administrative panel (`NotificationCenter.tsx`), not a Sacred 12 surface.

**Reusable governance pattern, cited per this repository's own precedent:** `IRA-C066` and `IRA-C114` both establish, and `IRA-C023 §15a` explicitly names by cross-reference, the "charter off the owning constitutional spec, no dedicated `PE-001-Cxxx` needed" pattern this document also follows (`SD-003` in C-132's case), and the "defer, deliberately, with a recorded trigger" pattern `IRA-C114`'s own GAP-4 disposition established — the same shape RO Decision 3a already applies to `SD-003-226`.

---

## 8. Business Object / Persistence Eligibility Analysis (`CMD-001 §26.3a`)

**(Established fact — the applicable test, `CMD-001 §26.3a`, verbatim structure.)** A candidate is eligible for canonical registration if it satisfies **Step 1 (Independent Identity)** and at least one of **Step 2 (Cross-Experience Reference Test)** or **Step 3 (Governed Lifecycle)**.

**Applying the test to "Notification," per the RO-authorized minimum scope (establish / manage / list / read / acknowledge):**

- **Step 1 — Independent Identity: SATISFIED.** RO Decision 3 explicitly authorizes `list`/`read`/`acknowledge` as distinct, later actions against a previously-established record — by definition, a Notification's identity persists beyond the single request/response cycle that created it. It is not a value that exists only for the duration of one request.
- **Step 2 — Cross-Experience Reference Test: NOT SATISFIED TODAY.** No Business Activity or Enterprise Experience *other than* C-132's own establish/list/read/acknowledge BA currently names a Notification, by exact term or unambiguous content, as Required or Consumed Context. `ROD-C132 §5` explicitly frames the C-131-mention relationship and a future C-133 consumption relationship as *possible future* relationships, not present ones — per §26.3a's own Negative Indicator language ("not required downstream"), a merely-possible future reference does not satisfy Step 2 as drafted today.
- **Step 3 — Governed Lifecycle: SATISFIED.** `SD-003` §8's own governing text describes real, persisting, later-invalidated state: notifications are "prioritized, batched, and suppressed," and `SD-003-226` describes items being "queued into a single end-of-day digest" rather than delivered immediately — behavior only coherent for a record with a real lifecycle. RO Decision 3's own explicit inclusion of "acknowledge" as an authorized first-BA action is itself a lifecycle transition (unread/undelivered → acknowledged). Nothing in `SD-003` or `DS-001` Chapter 21 self-describes a notification as transient or "not carried forward."

**Composite finding: Step 1 (yes) + Step 3 (yes) → Notification satisfies `CMD-001 §26.3a` and is eligible for canonical registration**, notwithstanding Step 2's present-tense "not yet" finding (the test requires only Step 1 **and** *at least one* of Steps 2/3 — Step 3 alone is sufficient once Step 1 is satisfied).

**Procedural-track finding.** This IRA elects to run the full `CMD-001 §26.3a` analysis (the `WP-04`/`WP-07`/`WP-08`/`WP-10` track), not the narrower `CLAUDE.md §18`/`§19.4` schema-shape-only STOP-and-report `WP-17`/`TDS-C023-A` used without a recorded reason for the deviation. This IRA discloses, rather than silently repeats, that deviation: no repository text explains why C-023's two tables bypassed the CBOR track other precedents ran, and this IRA does not adopt that precedent for C-132 without a recorded justification of its own — running the standard track is the more conservative, better-precedented choice.

**What this eligibility finding does and does not authorize.** A positive `§26.3a` finding proceeds, per `CBOR-INDEX.md`'s own Amendment Procedure, to formal registration **via a dedicated ADR** (mirroring `ADR-019`'s registration of `CFG-000001`, `WP-10`) — **this IRA does not perform that registration.** It records the eligibility finding only; a future ADR (raised at TDS time or immediately after IRA acceptance, at Repository Owner discretion) would perform the actual `CMD-001 §26.4` registration (Business Object Identifier, Canonical Name, Owning Capability — C-132, Aggregate Root, Primary Data Category, etc.) and add the corresponding row to `CBOR-INDEX.md`.

**STOP-and-report finding, independent of the above (`CLAUDE.md §18`/`§19.4`).** A new `notification`-shaped database table is, regardless of its `§26.3a` eligibility outcome, unambiguously the class of artifact `CLAUDE.md §18`/`§19.4` requires be justified via STOP-and-report before any migration is run — this is not resolved by this IRA and is expected, per every recent precedent (`TDS-C023-A §19`, `TDS-016`), to be satisfied by the future `TDS-C132`'s own schema-decision section, not by this IRA.

---

## 9. Candidate First Business Activity — Definition and Scope

**(Recommendation — a candidate definition for a future charter, not itself a charter.)**

**Candidate name:** Establish / Manage Enterprise Notification Context (naming not decided; illustrative only).

**In scope, per RO Decision 3 (Option A):**
- **Establish** a Notification record (recipient, causing action/object reference, severity, and a composition payload consistent with `DS-001-351`'s three elements — What Happened mandatory, Why It Matters / What Happens Next included where applicable).
- **Manage** — no additional business meaning beyond establish/list/read/acknowledge is implied by RO Decision 3's own text; this IRA does not read "manage" as authorizing edit/delete of an established Notification's own content (a Notification, once established, is a record of what happened — see §11).
- **List** Notifications for the current user, tenant-scoped.
- **Read** one Notification by id, tenant-isolated (anti-enumeration — a cross-tenant id returns 404, not 403, mirroring `WP-17`'s own certified pattern).
- **Acknowledge** a Notification (a lifecycle state transition; see §11).

**Explicitly excluded from this first BA (per RO Decision 3, verbatim):** email delivery, SMS delivery, push delivery, webhook delivery, external channel delivery, delivery-provider integration, real event-bus/event-subscriber infrastructure, multi-channel notification orchestration.

**Explicitly deferred (per RO Decision 3a):** the full `SD-003-226` per-user daily interruption ceiling and end-of-day digest mechanism. The first BA's Notification-establishment path must not silently claim to implement `SD-003-226` in full; any TDS/charter describing this BA must carry an explicit, dated deferral note, mirroring `IRA-C023`'s own Decision 3/4 deferral-disclosure convention.

**Trigger mechanism (finding, §3.3):** synchronous, in-process creation — a causing capability's own service layer directly invoking a `NotificationService`-shaped method, in its own transaction, mirroring `EntitlementLicenseEstablishmentService`'s own already-certified `record_audit()`/`publish_event()` call shape. No event bus, broker, or subscriber is involved or required.

---

## 10. DS-001 Compliance

**(Established fact.)** `DS-001` Chapter 21 (`DS-001-345`–`360`) is a complete, closed, frozen Notification Styling specification: a four-severity taxonomy realizing the existing Semantic Status Colours (no fifth severity may be invented, `DS-001-350`); a closed three-element composition — What Happened / Why It Matters / What Happens Next (`DS-001-351`); calm-notification and attention-preservation discipline (`DS-001-347`/`349`/`352`/`352A`); Enterprise Intelligence content preservation (`DS-001-353`); motion completing Chapter 15 §15.3 (`DS-001-354`); token-only styling (`DS-001-355`); accessibility (`DS-001-356`); and a closed governance/extension process routing any genuinely new need through §22.4, not through a capability team (`DS-001-357`/`358`).

**Reuse assessment:** the existing `NotificationTone` type already matches the four severities exactly and is already token-resolved via `theme.css`'s semantic-status custom properties (no hard-coded colour found); `NotificationCenter.tsx`'s panel shell, focus-trap, and ARIA structure are directly reusable.

**Gaps (ordinary future implementation work — none is a DS-001 gap):** the generic `Notification{id,message,tone}` model does not yet structurally carry the three-element composition or an actionability/response field; no severity-proportionate persistence/motion exists yet; no Motion-token wiring exists for toast appearance/dismissal.

**No `CLAUDE.md §19.1` STOP-and-report is warranted on the DS-001 dimension** — Chapter 21 is self-described as a complete, closed specification, and every element the minimum BA touches has a corresponding closed principle to build against.

---

## 11. Tenant / Ownership / Isolation

**(Recommendation, consistent with universal platform precedent — not a new mechanism.)** A Notification record is tenant-scoped (organization_id, per `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist) and recipient-scoped (a `recipient_person_id` or equivalent). Ownership of the *acknowledge* action belongs exclusively to the recipient (or, per existing platform convention, `PLATFORM_ADMIN`); no new authorization mechanism is implied beyond the standard `get_current_claims`/tenant-header pattern every closed WP already uses. **No RO decision is required for this dimension** — it is a routine TDS/implementation-time application of an already-established pattern, to be verified against `CLAUDE.md §21.4` exactly as `WP-17`/`WP-15` were.

---

## 12. Authority / Accountability

**(Recommendation.)** Unlike `WP-17`'s own `POST /entitlement-license-contexts` (gated by a named Commit Authority, per `IRA-C023` Decision 1), **establishing a Notification is not itself an authority-bearing act** — it is a byproduct of an already-authorized action in the causing capability (e.g., WP-17's own entitlement-establishment already passed its own Commit Authority check before any hypothetical future notification would fire). This IRA finds **no basis in `SD-003` or any existing authority mechanism (`URA-001`, `approval_authorities`) for gating Notification *establishment* behind a dedicated Approval/Commit Authority** — any authenticated internal service call, acting on behalf of an already-authorized causing action, should be sufficient. **Acknowledging** a Notification is gated only by recipient identity (§11). **No RO decision is required for this dimension**; this finding should be confirmed, not re-derived, at TDS time.

---

## 13. Lifecycle and Temporal Semantics

**(Recommendation, with one disclosed deferral.)** Minimum lifecycle: established (unread) → acknowledged. Whether a third state (e.g., "archived" or auto-expiry) is needed is **not decided by this IRA** — the RO-authorized scope names only "acknowledge." `SE-051`'s general retention floor (7-year constitutional floor for audit-relevant evidence) is noted as topically adjacent but its applicability to Notification records specifically (which are not themselves audit/evidence records, per §3.3's own Notification ≠ Audit Event finding) is an open TDS-level question, not an RO decision. The full `SD-003-226` interruption-ceiling/digest lifecycle (queuing, digest delivery) is explicitly deferred per RO Decision 3a and must not be implemented by the first BA.

---

## 14. Transaction / Idempotency

**(Recommendation.)** Because the trigger mechanism is synchronous and in-process (§9), the atomic-write pattern every closed WP already uses applies directly: the Notification insert occurs within the causing capability's own transaction (or its own immediately-following transaction), with the same flush/rollback discipline `EntitlementLicenseEstablishmentService` already demonstrates. Whether duplicate-notification suppression (idempotency) is required for the first BA is **not decided by this IRA** — this repository's own precedent (`TD-141`-class findings) treats idempotency-mechanism selection as a routine implementation-time choice, not requiring a Repository Owner decision, unless a specific natural key is later found to carry a genuine concurrency risk (mirroring `TD-152`'s own disposition for WP-14 BA-05).

---

## 15. Audit

**(Recommendation, consistent with universal platform precedent.)** A Notification's own establish and acknowledge actions should call `record_audit()`/`publish_event()` exactly as every other Business Activity in this repository does (§3.3) — this is the standard cross-cutting pattern, not a new mechanism, and is independently confirmed structurally distinct from the Notification record itself (§3.3, §8's Step-2 discussion). **No RO decision is required for this dimension.**

---

## 16. Event / Dependency Implications

**(Established fact, §3.3.)** No live event bus, broker, or subscriber exists anywhere in the running platform (`Backend/Shared/Events`' `EventPublisher`/`EventSubscriber` are abstract with no production concrete subclass; `publish_event()` is a structured-log stand-in). Synchronous, in-process Notification creation is architecturally viable today with no missing infrastructure (§3.3, §9) and does not depend on any of RO Decision 3's excluded items. If a future increment pursues real delivery (Option B, not authorized here), it would require: a concrete, broker-connected `EventPublisher`/`EventSubscriber` pair (none exists); `TECH-DEBT.md TD-151`'s own async-handler-dispatch fix; and a selected delivery provider (none is named or scheduled anywhere in this repository).

---

## 17. Service Hosting — RO DECISION REQUIRED

**(Finding — this dimension cannot be resolved by this IRA from existing precedent alone.)** Every prior service-hosting decision in this repository (`ADR-036` → C-023/`AuthService`; C-066 → `AIService`; WP-14 BA-05 → `AIService`; WP-12 → `AIService`) was reasoned from a canonical-data-anchor or sibling-table already physically present in one service. **No such anchor exists for C-132**: Domain D-007 (C-130–C-133) has zero existing physical footprint in any service, and no logical "Notification Service" is named anywhere in `Master_Technical_Architecture.md`'s own (incomplete) service catalog — unlike, e.g., Knowledge Graph's `AMD-012` addendum precedent.

**A further, genuinely novel complication:** C-132's own minimum scope requires many *different*, unrelated services' own transactions to eventually trigger a Notification write — a write-fan-in pattern with no existing precedent in this repository (every prior hosting decision involved reads/writes originating from one owning service's own transaction only). Combined with `CLAUDE.md §8`'s binding "never access another service's database" rule and the absence of any live event bus (§16), this raises a question no prior hosting ADR has had to answer: **how does a service other than C-132's own host write a Notification record without direct cross-service database access and without an event bus?**

**Classification (per the IRA Preparation Dossier, Workstream F, re-confirmed here):**
- **DECIDED** — no cross-service database access regardless of host (`CLAUDE.md §8`, already binding); any new-service-boundary option would independently require its own `CLAUDE.md §18`/`§19.4` STOP-and-report.
- **EXISTING PRECEDENT** — `TenantService` is confirmed fully mocked scaffolding and not a viable host (`ADR-036 §Decision(5)`, by direct analogy).
- **🔴 RO DECISION REQUIRED** — (a) which existing service hosts C-132's Notification persistence, or whether a dedicated new service is warranted (subject to its own STOP-and-report); (b) the write-fan-in mechanism by which other services' own transactions cause a Notification to be written, given no cross-service DB access and no live event bus.
- **IMPLEMENTATION-TIME DECISION** — exact schema shape, once hosting is resolved.

**This IRA does not select a host or a write-fan-in mechanism.** It recommends, per this repository's own established precedent (`TDS-013 §26a`'s own `RO-DEC-WP14-BA05-03` process), that the hosting and write-fan-in questions be resolved via a dedicated Repository Owner Decision Analysis conducted **during** `TDS-C132` drafting — mirroring how WP-14 BA-05's own service-hosting question was resolved as a first-order TDS task, not as a precondition blocking TDS from beginning. **TDS-C132 drafting may begin; TDS-C132 may not be finalized, and no schema/migration may be authorized, until this Repository Owner decision is obtained.**

---

## 18. API / Frontend Implications

**(Recommendation, consistent with universal platform precedent — `WP-17`'s own precedent shape.)** Backend: one router exposing `POST` (establish), `GET /{id}` (read), `GET` (list), and a state-transition endpoint (acknowledge) — mirroring `entitlement_license.py`'s own shape (Pydantic schemas, DI-composed service, tenant-isolated repository). Frontend: extend `NotificationCenter.tsx` to fetch and render real data (list + acknowledge), reusing its existing panel/accessibility shell; the unrelated `notifications/page.tsx` admin-config placeholder requires its own, separate disposition at TDS time (not addressed by this IRA). No new DS-001 component, token, or pattern is required (§10) — no `CLAUDE.md §19.1` STOP-and-report is triggered on this dimension.

---

## 19. Implementation Feasibility

**(Finding, consolidating §3.3, §16, §17.)** Technically feasible with no missing infrastructure for the RO-authorized minimum scope: the trigger mechanism (synchronous in-process creation) is proven and already certified elsewhere in this repository; DS-001 conformance has a clear, closed target; tenant isolation, authority, audit, and API/frontend shape all follow already-established, low-risk patterns. **The one substantive gap standing between this IRA and a fully scopable TDS is the service-hosting / write-fan-in question (§17)** — a real, disclosed, non-trivial architectural question this repository has not previously had to answer in this shape, not a missing-capability blocker of the kind `IRA-C114`'s own GAP-4 represented (where nothing existed to consume).

---

## 20. Gate Assessment (mirroring `IRA-C040`'s own seven-gate framework, applied for comparability)

| Gate | Result |
|---|---|
| Gate 1 — Business Function | ✅ PASS — unambiguous Business Intent (`CAP-001` line 105); `SD-003` §8 governs it with material specificity (unlike a one-line CAP-001 intent alone). |
| Gate 2 — Architecture | ✅ PASS — `SD-003` is a mature, ratified constitutional specification; `DS-001` Chapter 21 fully specifies presentation; no architecture gap found. |
| Gate 3 — Data Model | 🟡 CONDITIONAL PASS — `CMD-001 §26.3a` eligibility resolved affirmatively by this IRA (§8); exact schema shape is an ordinary TDS-stage task, contingent on §17's hosting decision. |
| Gate 4 — Authority / Security | ✅ PASS — no dedicated Approval Authority needed for establish (§12); tenant isolation follows the standard, proven `CLAUDE.md §21.4` pattern (§11). |
| Gate 5 — Business Activities | ✅ PASS — a coherent, narrowly-scoped, RO-authorized candidate BA exists (§9), with explicit, disclosed exclusions (delivery, `SD-003-226`). |
| Gate 6 — Governance | 🔴 FAIL (single item) — service hosting and the write-fan-in mechanism are unresolved and are not decidable from existing precedent alone (§17); a Repository Owner decision is required before `TDS-C132` can be finalized. |
| Gate 7 — Implementation | 🟡 CONDITIONAL PASS — no missing infrastructure for the authorized minimum scope (§19); implementation cannot be fully planned until Gate 6's own hosting question resolves. |

**5 of 7 gates PASS, 2 CONDITIONAL, 1 FAIL (Gate 6, a single, precisely-named, resolvable item).** This is measurably closer to ready than `IRA-C023`'s own original four-FAIL finding or `IRA-C114`'s own GAP-4-blocked disposition — the gap here is a scoping/governance decision with a clear, precedented resolution path (`TDS-013 §26a`'s own RO-decision-during-TDS pattern), not an absent capability-function substrate.

---

## 21. Readiness Decision

**C-132 / candidate first BA is 🟡 AMBER — READY FOR TECHNICAL DESIGN PREPARATION, NOT YET READY FOR TDS FINALIZATION OR IMPLEMENTATION AUTHORIZATION.**

This is neither a forced GREEN nor a RED. It is not RED: no capability-defeating blocker was found (contrast `IRA-C114`'s own GAP-4, "nothing exists to consume" — this IRA finds the opposite for C-132's own trigger mechanism, §3.3/§19); the RO-authorized minimum scope is coherent, bounded, and technically feasible with existing infrastructure; `CMD-001 §26.3a` resolves affirmatively; DS-001 conformance is a clear, closed target; tenant isolation, authority, and audit all follow proven patterns. It is not GREEN: a genuine, disclosed, precisely-named Repository Owner decision (service hosting + write-fan-in mechanism, §17) remains outstanding, and this repository's own discipline (`CLAUDE.md §18`) prohibits proceeding to a finalized schema/migration without it.

**May TDS proceed?** **`TDS-C132` drafting MAY begin now** — it should incorporate, as its own first-order task, a dedicated Repository Owner Decision Analysis resolving §17's hosting/write-fan-in question, mirroring `TDS-013 §26a`'s own precedent (`RO-DEC-WP14-BA05-03`) for resolving a hosting question *during* TDS drafting rather than as a precondition to starting it. **`TDS-C132` may NOT be finalized, and no schema, migration, model, repository, service, router, or test may be authorized or created, until that Repository Owner decision is obtained.**

**Is any additional Repository Owner decision required?** **Yes — exactly one, precisely named:** the C-132 service-hosting and cross-service write-fan-in mechanism (§17). No other dimension investigated by this IRA (§§10–16, 18–19) requires a Repository Owner decision; each is either already governed by an existing binding rule or is an ordinary implementation-time/TDS-time choice this IRA has explicitly identified as such rather than silently deciding.

---

## 22. Explicit Statement of What Remains Unresolved (not decided by this IRA)

- **RO DECISION REQUIRED** — C-132 service hosting + cross-service write-fan-in mechanism (§17). **This is the sole blocking item.**
- **UNRESOLVED, non-blocking** — the C-130 (Enterprise Collaboration) umbrella-vs-coordinate question relative to C-131/C-132/C-133 (§2); this does not block C-132's own independent minimum-scope BA (RO Decision 2's own independence framing) but should be reconciled by a future C-130/C-131 charter.
- **UNRESOLVED, non-blocking** — whether/how a future C-132 notification is ever surfaced on a Sacred 12 executive screen (§7) — not required for, and does not block, the Layer-1 administrative minimum-scope BA.
- **UNRESOLVED, deferred by RO Decision 3a, not this IRA** — the full `SD-003-226` interruption-ceiling/digest mechanism (§9, §13).
- **Not yet performed** — `CMD-001 §26.4` formal CBOR registration (a future ADR, contingent on Repository Owner discretion on timing, not blocking TDS drafting) (§8).
- **Not yet decided, ordinary TDS-stage work, no RO decision needed** — exact schema shape; Notification retention policy applicability (`SE-051`); idempotency mechanism; the unrelated `notifications/page.tsx` admin-config placeholder's own disposition.

---

## 23. Change Control

**Files created:** this document only — `architecture/05-Implementation/IRA-C132_Enterprise_Notifications_Implementation_Readiness_Assessment.md`.
**Files read for cross-reference, not modified:** `CAP-001`, `SD-003`, `DS-001` (Chapter 21, Chapter 6 §6.3, Chapter 15 §15.3, Chapter 22 §22.4), `SER-001` (`SE-018`/`SE-017`/`SE-040`/`SE-051`), `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md` (C-132 row, read only), `ROD-C132-Enterprise-Notifications-Capability-Boundary-and-Minimum-Scope.md`, `CMD-001 §26.3–26.5`, `CBOR-INDEX.md`, `HISTORICAL-SCREEN-REALIZATION-MATRIX.md`, `EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md`, `WPR-001`, `WP-REG-001`, `TECH-DEBT.md` (`TD-151`/`TD-152`), `ADR-036`, `TDS-013`, `TDS-012`, `IRA-C066`, `IRA-C114`, `IRA-C023`, `IRA-014`, `TDS-C023-A`, plus the frontend/backend source files named throughout §3.
**Not modified:** `CAP-001`, `SD-003`, `DS-001`, `PE-001`, `SER-001`, `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`, `WPR-001`, `WP-REG-001`, `CBOR-INDEX.md`, `TECH-DEBT.md`, any WP-17/C-023, WP-18, C-040, or C-114 artifact, `ROD-C132-...md`, any `Backend/`/`source/frontend/` file, any migration, any test. No implementation of any kind was performed. **No IRA acceptance is granted by this document** — acceptance remains a separate, future Repository Owner review, per `CLAUDE.md §19.1` and this repository's own `IRA-C066`/`IRA-C114`/`IRA-C023` precedent. Nothing was staged, committed, or pushed.

*End of IRA-C132.*
