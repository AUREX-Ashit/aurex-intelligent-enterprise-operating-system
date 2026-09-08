# TDS-C132 — Enterprise Notifications (C-132) — Minimum Business Activity Technical Design

**Document status: FINALIZED.** Per direct Repository Owner authorization ("AUREX — C-132 Next Phase — TDS Drafting + Service-Hosting RO Decision Analysis"), this document began Technical Design for C-132's minimum-scope first Business Activity, presenting §6's options without deciding any of them. Per a first follow-on authorization ("AUREX — C-132 Service-Hosting Decision"), the Repository Owner selected **Option 2** for the write-fan-in posture — host in an existing AUREX service (not a new dedicated service); the first increment's Notification creation is restricted to intra-service triggering only; cross-service write fan-in is explicitly deferred (§6.4). Per a second, final follow-on authorization ("AUREX — C-132 Existing Service Host Decision"), the Repository Owner selected **H-1 — `AuthService`** as the existing-service host (§6.5, now resolved). The consequent schema-shape STOP-and-report (§6.6) has been performed at the conceptual level — no further Repository Owner decision surfaced from it. All previously-blocked sections (§5, §16, §22, §23, §25) have been updated to reflect both resolutions, and a full consistency review (§28) has been performed. **No schema, migration, model, repository, service, router, frontend, or test is created or authorized by this document — finalization is a governance/design-completeness status, not an implementation authorization.** No WP is registered. No BA charter exists. Per explicit instruction, WP registration and BA charter creation are the next governance stage, not performed by this document or in this pass.

**Governing basis, in order:** `CAP-001` (C-132 registration) → `SD-003` §8 (Notifications, Attention & Cognitive Load Laws — primary governing law) → `architecture/06-Reviews/ROD-C132-Enterprise-Notifications-Capability-Boundary-and-Minimum-Scope.md` (RO Decisions 1/2/3/3a) → `architecture/05-Implementation/IRA-C132_Enterprise_Notifications_Implementation_Readiness_Assessment.md` (🟡 AMBER — ready for Technical Design preparation, not TDS finalization) → this document.

**Naming note (mirrors `TDS-C023`'s own precedent):** capability-first, no WP number — none exists yet for C-132.

---

## 1. Purpose

Design, at the level `IRA-C132`'s own AMBER verdict authorizes (preparation, not finalization), the minimum-scope first Business Activity for C-132: a persisted, user-facing Notification record supporting establish / manage / list / read / acknowledge, per `ROD-C132` RO Decision 3. This document carries forward every non-hosting design conclusion `IRA-C132` already reached, and isolates the one item that document found undecidable from existing precedent — service hosting and cross-service write fan-in — into a dedicated Repository Owner Decision Analysis (§6).

## 2. Scope (design-level; carried forward from `IRA-C132 §9`, RO Decision 3, unchanged)

- Establish a Notification record (recipient, causing-action reference, severity, and a composition payload consistent with `DS-001-351`'s three elements).
- List Notifications for the current user, tenant-scoped.
- Read one Notification by id, tenant-isolated (404-not-403 anti-enumeration, mirroring `WP-17`'s certified pattern).
- Acknowledge a Notification (lifecycle transition: unread → acknowledged).

## 3. Non-Goals (unchanged from `ROD-C132` RO Decision 3 — restated, not reinterpreted)

Email, SMS, push, webhook, or any external-channel delivery; delivery-provider integration; real event-bus/event-subscriber infrastructure; multi-channel notification orchestration; the full `SD-003-226` interruption-ceiling/digest mechanism (RO Decision 3a — deferred, not abandoned, see §19); any C-131 comment/mention implementation; any C-133 activation or shared ledger (RO Decision 2); any repair of `Backend/Shared/Events` (out of scope by direct instruction — see §18).

## 4. Business Activity Being Designed

Candidate name (illustrative, not decided): "Establish / Manage Enterprise Notification Context." One Business Activity, four-and-one operations (establish, list, read, acknowledge — "manage" per `IRA-C132 §9` carries no meaning beyond these four). No edit/delete of an established Notification's own content is designed here — a Notification is a record of what happened (§10), not a mutable document.

---

## 5. Domain Model (logical shape, RO-resolved this pass — physical Alembic migration/ORM model NOT created)

**No table, column, index, or ORM model is created by this section — the schema-shape STOP-and-report (§6.6) records the conceptual shape now that the host is decided; the physical migration remains a separate, later, implementation-time action, per §22.**

A Notification conceptually carries (physical shape recorded in full at §6.6, host: `AuthService`):

| Logical field | Purpose |
|---|---|
| Identity | independent identity, per `IRA-C132 §8` Step 1 finding (persists beyond the request/response that created it) |
| Recipient anchor | `Membership` (Person × Organization) — reuses `AccessEvaluationOutcome.membership_id`'s own precedent (§6.6), simultaneously satisfying recipient identity and tenant scoping without inventing a new anchor |
| Tenant anchor | organization scoping, per `CLAUDE.md §21.4` — enforced via the recipient's own `Membership.organization_id`, not a duplicated column (§6.6) |
| Severity | one of DS-001's four closed values (`DS-001-350`) — success / info / warning / danger |
| Composition payload | the closed three-element structure (`DS-001-351`): What Happened (mandatory), Why It Matters (optional), What Happens Next (optional) |
| Causing-action reference | a non-FK, point-in-time citation (`source_type` + `source_id`), mirroring `committed_by_actor_id`/`entitlement_source_reference`'s own established non-FK precedent (§6.6) — never a new polymorphic-association mechanism |
| Status | unread → acknowledged (§10) |
| Timestamps | created, acknowledged |

**Resolved this pass:** write-fan-in posture (§6.4 — intra-service triggers only, so the causing-action reference is always a same-service, in-process citation for this first increment) and existing-service host (§6.5 — `AuthService`). The full conceptual field/type/constraint list is recorded at §6.6; the physical Alembic migration itself is not created here (§22).

---

## 6. Service Hosting & Cross-Service Write Fan-In

**Status (this pass): the write-fan-in posture is now RO-DECIDED (§6.4 — Option 2). The exact existing-service host remains 🔴 RO DECISION REQUIRED (§6.5) — repository evidence does not clearly identify one canonical host, and this document does not infer one.**

§§6.1–6.3 below are preserved unchanged from the prior drafting pass — the original options analysis and recommendation, offered before the Repository Owner's selection. They are retained for their own evidentiary value and are not re-derived or altered by this pass's own §6.4/§6.5 additions.

### 6.1 Current facts (established, not in question)

- **FACT** — C-132 has no existing canonical persistence service. Domain D-007 (C-130–C-133) has zero physical footprint in any of the five running backend services (`AuthService`, `AIService`, `ReportingService`, `IngestionService`, `TenantService`).
- **FACT** — Notification is a new persisted Business Object (`IRA-C132 §8`: eligible under `CMD-001 §26.3a`, Step 1 + Step 3).
- **FACT** — Per `ROD-C132`/`IRA-C132`'s own framing, multiple, presently-unspecified capabilities may eventually cause a notification to be created (a mention per RO Decision 1's own seam; any future capability's own business event).
- **FACT** — `CLAUDE.md §8` prohibits direct cross-service database access ("never access another service's database... Communicate through APIs or events") — this is a binding, repository-wide rule, independent of which service is chosen.
- **FACT** — No live event bus exists anywhere in the running platform. `Backend/Shared/Events`' `EventPublisher`/`EventSubscriber` are abstract; the two in-tree `EventPublisher` subclasses have their real broker dispatch commented out; zero production `EventSubscriber` subclass exists; no broker SDK dependency is declared in any service. `publish_event()` (where it exists, `AuthService` only) is a structured-log stand-in, not a queryable/subscribable event. **Per direct instruction, this event infrastructure is not being repaired or implemented by this TDS or any option below.**
- **FACT** — Existing hosting precedents (`ADR-036` → C-023/`AuthService`; C-066 → `AIService`; `TDS-013 §26a`/`RO-DEC-WP14-BA05-03` → `AIService`; `TDS-012` → `AIService`, "same service as C-093, per `CLAUDE.md §8`'s one-capability-one-owning-service discipline") each rested on a canonical-data-anchor or sibling table **already physically present** in the chosen service. **No such anchor exists for C-132** — this repository has no precedent for a capability with zero existing footprint being assigned a host, and no precedent at all for the write-fan-in topology below (many different, currently-unspecified services each potentially needing to cause one new object's creation).

### 6.2 Options investigated

For each option: **A** Architecture · **B** Ownership · **C** Write path · **D** Transaction boundary · **E** Tenant isolation · **F** Audit · **G** Event dependency · **H** Future scalability/extraction · **I** Risks · **J** Governance implications.

---

#### OPTION 1 — Host in an existing service; cross-service creation via a best-effort, post-commit, synchronous API call (fire-and-log, not transactional)

**A.** A `Notification` model/repository/service/router built inside one existing service (candidate hosts: `AuthService` — broadest existing surface area, most capabilities already live there per `ADR-036`'s own modular-monolith trend; or `AIService` — hosts the Evidence/Intelligence side, C-066/C-090-095/C-114-candidate). Any capability, in *any* service, that needs to raise a notification calls the hosting service's own real HTTP API (`POST /notifications` or similar) **after its own causing transaction has already committed**, exactly mirroring how `EntitlementLicenseEstablishmentService` already calls `record_audit()`/`publish_event()` synchronously, in-process, post-flush, best-effort, unawaited (`IRA-C132 §3.3`) — the same pattern, extended from an in-process function call to a cross-service HTTP call for callers outside the host.
**B.** The hosting service owns the table, the model, and all four operations exclusively.
**C.** Intra-service callers (inside the host) call the service class directly, in-process (no HTTP hop, no cross-service concern at all). Cross-service callers make a real, authenticated internal HTTP call to the host's own API, wrapped in a try/except that logs and swallows failure — a lost notification is a degraded-but-tolerable outcome, never a reason to fail or roll back the causing action's own already-committed transaction.
**D.** No cross-service transaction is attempted or claimed. The notification write is explicitly **not** atomic with the causing action — this is disclosed, not hidden, and mirrors the existing `record_audit`/`publish_event` best-effort posture exactly (neither of those is transactional with the write it observes, either).
**E.** Standard, single point of enforcement — the host's own tenant-isolation logic (`CLAUDE.md §21.4`) applies uniformly regardless of which service originated the call.
**F.** Standard — the host's own `record_audit()` call on establish/acknowledge, per `IRA-C132 §15`.
**G.** None — no event bus required; this is a direct, synchronous API dependency, not an event.
**H.** If a real event bus is ever built, this option's own external callers could be migrated from "call the API directly" to "publish an event, the host subscribes" with no change to the host's own internal model/service — a clean future migration path.
**I.** **New pattern for this codebase:** no confirmed precedent of one service making a synchronous HTTP call to another service's own API for a write exists in the evidence gathered across `IRA-C132`'s own asset-discovery pass. This introduces cross-service network dependency, timeout/retry design, and inter-service authentication (no existing internal-service-auth mechanism was found in evidence gathered to date) — each a real, non-trivial design surface this TDS has not resolved. A failed/slow host does not block the causing service's own write (by design, §6.2 Option 1.D), but it does mean notifications can be silently lost under host unavailability, with no retry/backfill mechanism designed here.
**J.** Does not require a new service boundary (no `CLAUDE.md §18` new-service STOP-and-report); does require this TDS (once finalized) to design the internal API-auth mechanism, which itself may warrant its own STOP-and-report if no existing pattern covers it.

---

#### OPTION 2 — Host in an existing service; first Business Activity restricted to intra-service triggers only; cross-service triggering explicitly deferred to a disclosed future increment

**A.** Identical hosting/model/service/router build to Option 1, but the **only** callers of `establish` in this first increment are the hosting service's own internal capabilities. No cross-service call, HTTP or otherwise, is built in this increment.
**B.** Same as Option 1.
**C.** Only in-process, same-service calls (the already-proven, already-certified pattern, `IRA-C132 §3.3`/§19). No cross-service write path is designed or built in this increment.
**D.** Ordinary same-service atomic-write discipline — no cross-service transaction question arises at all, because no cross-service write exists yet.
**E.** Same as Option 1 — standard, unaffected by the narrower trigger scope.
**F.** Same as Option 1.
**G.** None.
**H.** Cleanest possible extraction path: the write-fan-in question is not yet answered by anything built, so a later increment can freely choose Option 1's synchronous-API pattern, a genuine event-bus pattern (once built), or another mechanism, without unwinding or migrating any existing caller.
**I.** **Lowest risk of any option** — no new inter-service pattern, no new failure mode, no new authentication surface. The only "risk" is scope: the first BA cannot yet be triggered by, e.g., a C-131 mention living in a different service, or any future capability outside the host — this is an explicit, disclosed scope narrowing, not a silent one, and mirrors this repository's own repeated minimum-scope discipline (`WP-17`'s Decision 3/4 deferral; `IRA-C114`'s GAP-4 deferral).
**J.** No new governance surface triggered at all in this increment; the cross-service question is explicitly deferred with a recorded trigger (a future increment), exactly the shape `CLAUDE.md §19.8`'s Technical Debt discipline and this repository's own established deferral pattern require for a *deliberate*, disclosed deferral rather than a silent omission.

---

#### OPTION 3 — A new, dedicated `NotificationService`

**A.** A brand-new backend deployable, its own database, its own API, exclusively owning Notification persistence for the whole platform.
**B.** The new service owns it exclusively — architecturally the cleanest single-owner shape of any option.
**C.** Every caller, including the causing capabilities that today live in `AuthService`/`AIService` themselves, calls the new service's API (no caller gets an in-process shortcut) — a uniform cross-service pattern from day one, with the same synchronous-call design questions as Option 1's cross-service leg, but for *every* caller, not only external ones.
**D.** Same non-atomic, best-effort posture as Option 1.
**E.** Standard, single enforcement point, same as Option 1.
**F.** Standard, but requires its own new `record_audit`/`observability.py`-equivalent wiring, since no service scaffold exists yet.
**G.** None required, same as Option 1; equally compatible with a future real event bus.
**H.** Best long-term extraction posture of any option — Notification never needs to be "extracted out of" a co-hosting capability later, because it was never co-hosted with anything.
**I.** **Highest cost of any option.** Requires standing up an entire new service (deployment, CI/CD, config, its own `main.py`/health/readiness endpoints, its own database connection, its own internal-service-auth question — same unresolved surface as Option 1, but now unavoidable for *every* caller including intra-"modular-monolith" ones). `ADR-036` (the closest, most recent precedent for exactly this kind of decision, for C-023) explicitly found: *"no dedicated service exists or is authorized to be created... service extraction is deferred to a future, separately-scoped ADR."* This repository's own stated modular-monolith phase preference disfavors new service boundaries.
**J.** **Independently triggers its own `CLAUDE.md §18`/`§19.4` STOP-and-report for a new service boundary**, on top of, and prior to, anything this TDS itself could authorize — selecting this option does not conclude this TDS's own governance sequence; it opens a further, separate one.

---

#### OPTION 4 — Distributed / one local Notification table per capability (no single owning service) — investigated, not viable

**A.** Every capability that needs notifications builds and owns its own local table.
**B.** No single owner — Notification-the-capability would have no owning service at all.
**I. / J.** **This option is not architecturally viable under this repository's own existing constitutional rule.** `CLAUDE.md §8`: "Each capability has one owning service... Never duplicate business logic... couple unrelated domains." A capability with no single owning service, and the same establish/list/read/acknowledge logic duplicated per-service, directly contradicts this already-binding rule. **Included here only to document that it was considered and to show why it is excluded, not as a live candidate.**

---

#### OPTION 5 (future, not viable now) — Genuine event-driven fan-in via a real, broker-connected event bus

**A.** Every causing capability publishes a real domain event; the hosting service's own concrete `EventSubscriber` consumes it and creates the Notification.
**G.** **Requires infrastructure that does not exist and that this TDS is explicitly not authorized to build**: a concrete, broker-connected `EventPublisher`/`EventSubscriber` pair (none exists — `IRA-C132 §16`); `TECH-DEBT.md TD-151`'s own async-handler-dispatch fix; a selected/deployed broker. **Not a viable option for the first increment under any circumstance, per the direct instruction governing this pass ("do not repair or implement event infrastructure").** Recorded for completeness as the option this repository would naturally converge on **after** its own event infrastructure is separately built and certified — not before.

### 6.3 RECOMMENDATION (analytical recommendation only — the Repository Owner selects the authoritative option)

**RECOMMENDATION: Option 2** (host in an existing service; first Business Activity restricted to intra-service triggers only; cross-service triggering explicitly deferred to a disclosed future increment), **with Option 1's synchronous best-effort API pattern recorded as the natural, low-risk next increment once a cross-service trigger is actually needed.**

Rationale (analysis, not a decision): Option 2 introduces no new inter-service pattern, no new authentication surface, and no new failure mode — it is buildable entirely from already-certified, already-proven precedent (`IRA-C132 §3.3`/§19). It does not foreclose Option 1 later (the host's own internal model/service is identical either way) and completely avoids Option 3's new-service governance/infrastructure cost and Option 4's constitutional non-viability. It is consistent with this repository's own repeated minimum-scope discipline (WP-17, WP-15, IRA-C114) of deliberately narrowing a first increment's own trigger surface rather than solving the hardest integration question before anything is proven to work at all.

**This recommendation is not a decision.** Options 1 and 3 remain live, RO-selectable alternatives; §6.2 discloses each option's own trade-offs without concealment, per the governing instruction.

### 6.4 REPOSITORY OWNER DECISION RECORDED — Write-Fan-In Posture (this pass)

**Recorded per direct Repository Owner instruction ("AUREX — C-132 Service-Hosting Decision"): OPTION 2 SELECTED.**

- C-132 Notification persistence **shall be hosted in an existing AUREX service — no dedicated new `NotificationService` is authorized.** Option 3 (§6.2) is accordingly **not selected** and is not further pursued by this TDS.
- **First increment:** Notification creation is restricted to **intra-service triggering only** — only the hosting service's own internal callers may invoke `establish`. No cross-service caller is designed or built in this increment.
- **Deferred future increment:** cross-service write fan-in (Option 1's synchronous best-effort API pattern, §6.2, remains the recorded candidate for that later increment, not decided now).
- **This decision does NOT authorize:** a specific existing service (§6.5, still open); cross-service database access (never authorized, `CLAUDE.md §8` remains binding regardless); a synchronous cross-service API call (explicitly deferred with the rest of cross-service fan-in); an event bus or any event-infrastructure repair (§6.1's event-infrastructure finding is unchanged and untouched — see §17); any future C-133 integration (`ROD-C132` RO Decision 2 stands, untouched); implementation of any kind.
- This is a governance/architecture decision for the first increment's own write-fan-in posture only.

### 6.5 REPOSITORY OWNER DECISION RECORDED — Existing Service Host

**Recorded per direct Repository Owner instruction ("AUREX — C-132 Existing Service Host Decision"): H-1 — `AuthService` SELECTED.**

- **C-132 Notification persistence shall be hosted in the existing `AuthService`.**
- This selection is made together with the previously-recorded Option 2 write-fan-in posture (§6.4): existing-service hosting, first increment restricted to intra-service triggers, cross-service fan-in deferred.
- **This decision does NOT authorize:** cross-service database access (`CLAUDE.md §8` remains binding); synchronous cross-service API notification creation (deferred with the rest of cross-service fan-in); a new `NotificationService`; an event bus; cross-service write fan-in of any kind; notification delivery infrastructure; C-133 integration. No workaround of `CLAUDE.md §8` is authorized or designed by this decision.
- The evidence and trade-offs originally presented for this decision (§6.5's own prior content, `AuthService` vs. `AIService` vs. deferral) are preserved immediately below as the historical record the Repository Owner selected from — not re-derived or altered by this resolution.

**Historical record — investigation as originally presented (preserved verbatim, not re-derived):**

**Repository evidence does NOT clearly identify one canonical existing service as C-132's host** at the time this investigation was performed. This was investigated, not inferred, below — no host was silently chosen at that time.

**Investigation performed this pass (in addition to `IRA-C132 §17`'s own prior finding):** a targeted search of `architecture/04-Technical/Master_Technical_Architecture.md` (the repository's own logical/physical service catalog) for "notification," "D-007," and any Collaboration/Engagement-domain service-hosting language returns **zero hits**. A search of `ARCH-000` for any general "cross-cutting concern defaults to service X" rule returns **zero hits**. No document anywhere assigns C-130, C-131, or C-133 (C-132's own domain siblings) to any service either — the entire D-007 domain has no logical or physical hosting precedent to reason from, confirming `IRA-C132 §17`'s own finding rather than merely repeating it.

**Every prior hosting decision this repository has made (`ADR-036` → C-023/`AuthService`; C-066 → `AIService`; `TDS-013 §26a` → `AIService`; `TDS-012` → `AIService`) rested on a canonical data anchor or sibling table already physically present in the chosen service.** No such anchor exists for C-132 in any service.

**Candidates, evaluated (none selected):**

| Candidate | Evidence for | Evidence against |
|---|---|---|
| **`AuthService`** | Broadest existing capability surface (C-001–008, C-020, C-023, C-040, C-041 all already live there); the growing modular-monolith host per `ADR-036`'s own stated trend; if a future C-131 (comment/mention, `ROD-C132` RO Decision 1) is ever hosted there, `Person`/`Membership` anchors it would need already live in `AuthService`, a weak forward-looking adjacency — **not itself an existing anchor for C-132 today**, since C-131 is itself unchartered. | No existing table, router, or model anywhere in `AuthService` relates to Notification, Collaboration, or D-007 today. |
| **`AIService`** | Hosts the Evidence/Intelligence side of the platform (C-066, C-090–095 candidate, C-094) — if C-132 is read as an "attention/cognitive load" concern (`SD-003` §8's own framing, adjacent to Enterprise Intelligence's own attention-management themes), a thematic adjacency exists. | Purely thematic — no existing table, router, or model anywhere in `AIService` relates to Notification, Collaboration, or D-007 either. `SD-003` (C-132's owning spec) is an Interaction/UX law family, not an Enterprise Intelligence spec — the thematic link is weaker than a genuine capability-domain match. |
| **`TenantService`** | — | **Ruled out** — confirmed fully mocked scaffolding; `ADR-036 §Decision(5)`: "not to be treated as a host or owner of any [capability] data," an explicit, repository-wide finding, not C-023-specific in its underlying fact (`TenantService` has no real persistence anywhere). |
| **`ReportingService`** | — | **Ruled out** — single-purpose (ESG/BRSR/GRI/CSRD reporting only); no D-007 adjacency; hosting a cross-cutting Interaction-law capability there would couple unrelated domains, contrary to `CLAUDE.md §8`. |
| **`IngestionService`** | — | **Ruled out** — single-purpose (data ingestion only); same reasoning as `ReportingService`. |

**Neither `AuthService` nor `AIService` has an existing canonical anchor for C-132** — both candidates rest on adjacency/trend arguments, not the kind of pre-existing-table evidence that resolved every prior hosting decision this repository has made. Selecting between them is a **governance/architecture judgment call this document is not authorized to make silently.**

**🔴 RO DECISION REQUIRED — EXISTING SERVICE HOST**

- **Option H-1 — `AuthService`.** Rationale available: broadest existing surface, most-likely future sibling to C-131. Trade-off: no capability-domain match to `SD-003`'s own Interaction/UX law family; `AuthService` continues absorbing unrelated domains (already hosts Identity, Access, Org, Structure, Person, Membership, Workspace, Configuration, Tenant-Establishment, Entitlement/License).
- **Option H-2 — `AIService`.** Rationale available: thematic proximity to attention/cognitive-load and Enterprise Intelligence framing. Trade-off: `SD-003` is not an Enterprise Intelligence specification; no existing capability there shares C-132's own Interaction-law lineage; would introduce a first "presentation/interaction law" capability into a service otherwise organized around Discovery/Knowledge/Search/Conversation/Evidence.
- **Option H-3 — defer the host selection and record it as a further, separately-scoped Repository Owner Decision Analysis**, mirroring how `WP-14 BA-05`'s own hosting question (`TDS-013 §26a`) was resolved via a dedicated `RO-DEC-WP14-BA05-03` decision made *during* TDS drafting rather than pre-supposed — i.e., the Repository Owner may wish additional evidence-gathering (e.g., a forward look at C-131's own likely first BA, if and when C-131 is ever chartered) before selecting H-1 or H-2.

~~**This document does not select H-1, H-2, or H-3. This is the sole remaining blocking item before TDS-C132 can be finalized.**~~ **Superseded, this pass: H-1 (`AuthService`) selected by the Repository Owner — see the resolution recorded above.**

### 6.6 Schema-Shape STOP-and-Report (host: `AuthService`) — conceptual level only, no migration/model created

Performed per direct Repository Owner instruction, now that §6.5 resolves the host. This is governance/Technical Design work — **it does not create an Alembic migration, an ORM model, a database table, a repository, a service, a router, frontend, or tests.** It records the conceptual schema shape the eventual physical design must satisfy, and states explicitly whether any further Repository Owner decision surfaced. Reasoning applies `CMD-001`, `CLAUDE.md §8/§21.4`, and `AuthService`'s own existing persistence conventions (`c023_entitlement_context.py`, `c023_license_context.py`, `access_evaluation_outcome.py` — read directly, this pass, as the governing precedent set).

**1. Proposed Notification BO fields/relationships (conceptual):**

| Field | Conceptual type | Notes |
|---|---|---|
| `id` | UUID, PK | Independent identity + audit correlation, mirroring every `AuthService` model's own PK convention. |
| `membership_id` | UUID, FK → `memberships.id`, NOT NULL, indexed | **Recipient anchor.** Reuses the existing `Membership` (Person × Organization) table directly — mirrors `AccessEvaluationOutcome.membership_id`'s own precedent exactly. No new anchor concept is introduced. |
| `severity` | String, NOT NULL, `CheckConstraint` closed-set | One of DS-001's four closed values (`DS-001-350`: success/info/warning/danger) — mirrors `AccessEvaluationOutcome`'s own `CheckConstraint`-enforced enum pattern. |
| `what_happened` | Text, NOT NULL | `DS-001-351`'s mandatory composition element. |
| `why_it_matters` | Text, NULLABLE | `DS-001-351`'s optional composition element. |
| `what_happens_next` | Text, NULLABLE | `DS-001-351`'s optional composition element. |
| `source_type` | String, NOT NULL | Free-text, non-authoritative citation of the causing capability/table (e.g. `"C023_ENTITLEMENT_CONTEXT"`, `"MEMBERSHIP"`) — mirrors `entitlement_source_reference`'s own free-text, non-authoritative precedent. |
| `source_id` | UUID, NULLABLE, **NOT a foreign key** | Point-in-time citation to the causing row's own id — mirrors `committed_by_actor_id`'s own established non-FK-citation precedent exactly. A real FK is not used because the causing table varies by capability, and inventing a polymorphic-association mechanism to support one would itself be new architecture `CLAUDE.md §18` does not authorize here. |
| `status` | String, NOT NULL, `CheckConstraint` closed-set | `UNREAD` / `ACKNOWLEDGED` only (§10's own minimum lifecycle — no third state). |
| `created_at` | `DateTime(timezone=True)`, NOT NULL, default now() | Standard platform timestamp convention. |
| `acknowledged_at` | `DateTime(timezone=True)`, NULLABLE | Set only on the `UNREAD → ACKNOWLEDGED` transition; NULL while unread. |

Candidate physical table name (naming convention only, not created): `c132_notification`, mirroring `c023_entitlement_context`/`c023_license_context`'s own capability-prefixed naming convention.

**2. Ownership:** `AuthService` exclusively, per §6.5 — no other service reads or writes this table, consistent with `CLAUDE.md §8`.

**3. Tenant/organization/user scope:** the recipient's own `Membership.organization_id` **is** the tenant anchor — no separate, duplicated `organization_id` column is added to Notification itself, exactly mirroring `AccessEvaluationOutcome`'s own choice not to duplicate organization scoping alongside `membership_id`. Every `list`/`read` query joins through `membership_id` to enforce `CLAUDE.md §21.4` tenant isolation; a cross-tenant `read` by id returns 404, mirroring `WP-17`'s own certified anti-enumeration pattern (§11).

**4. Lifecycle state:** `UNREAD` (on establish) → `ACKNOWLEDGED` (on acknowledge). One-directional; no un-acknowledge; no archive/expiry state designed (§10, unchanged from `IRA-C132 §13`).

**5. Temporal requirements:** `created_at` at establish; `acknowledged_at` at acknowledge; no other temporal field is governance-required (no effective-dating, unlike `c023_entitlement_context` — Notification is not a time-bound entitlement fact).

**6. Acknowledgement semantics:** only the recipient identified by `membership_id` (or `PLATFORM_ADMIN`, per standing platform convention, §9) may acknowledge. Acknowledging an already-`ACKNOWLEDGED` Notification's own exact behavior (idempotent no-op vs. error) is an **implementation-time choice**, not governance-required — either is consistent with §10's own one-directional lifecycle.

**7. Audit requirements:** `establish` and `acknowledge` each call `record_audit()` (and `publish_event()` where `AuthService` already defines it as its own structured-log stand-in, §14/§17) — the same universal pattern every other `AuthService` capability already uses. No new audit mechanism.

**8. Uniqueness/idempotency requirements:** **no uniqueness constraint is governance-required.** Unlike `c023_entitlement_context`'s own `ux_c023_entitlement_context_current` (which enforces a substantive business invariant — exactly one CURRENT entitlement per anchor+type), no equivalent invariant is named anywhere in `ROD-C132`/`IRA-C132`/`SD-003` for Notification — a recipient may legitimately receive multiple, distinct notifications from the same `source_type`/`source_id` over time (e.g., repeated status changes on the same object). Establish-time idempotency (e.g., de-duplicating a double-submit) remains an ordinary implementation-time concern, unless a concrete concurrency risk is later found — mirroring `TD-152`'s own disposition (`IRA-C132 §14`, carried forward unchanged).

**9. Retention implications:** Notification is **not** an Audit Event (§7) — `SE-051`'s 7-year retention floor binds the `record_audit()` trail itself (item 7, above), which is unaffected regardless of any future Notification-row retention policy. No purge/archive mechanism for the Notification row itself is designed here; its absence does not weaken any audit trail, security boundary, or tenant-isolation boundary, and is carried forward unchanged as a disclosed, non-blocking open item (`IRA-C132 §10`) — a Technical Debt candidate at WP registration time, not a TDS-level blocker under `CLAUDE.md §19.8.5`'s own carve-out (it is not a security, data-integrity, tenant-isolation, or audit defect).

**10. Indexes/constraints — governance-required vs. implementation-time:**
- **Governance-required:** an index on `membership_id` (enables the tenant/recipient-scoped `list`/`read` predicate `CLAUDE.md §21.4` requires); `CheckConstraint`s on `severity` and `status` enforcing DS-001's and §10's own closed sets (mirrors `AccessEvaluationOutcome`'s identical discipline for its own closed-set columns).
- **Implementation-time:** whether a composite `(membership_id, status)` index is added for the unread-count/list-filter query; exact constraint/index naming convention; exact `String` length bounds for `severity`/`status`/`source_type`.

**11. Unresolved schema question:** **none identified that requires further Repository Owner authority.** Every field above resolves via direct reuse of an already-established `AuthService` persistence pattern (`Membership` FK for recipient+tenant, `CheckConstraint` for closed sets, non-FK point-in-time citation for the causing reference) — no new architectural mechanism, no new cross-service concern, no new authority model is invented. **This schema-shape investigation does not surface a further RO decision.**

---

## 7. Ownership Boundaries (restating RO Decisions 1 and 2 — not reinterpreted)

- **C-131 / C-132** (RO Decision 1, Option A): C-131 owns human-authored comment/mention content (`SD-003` §9); C-132 owns the resulting system-generated notification, including a mention-notification. The seam: C-131's own content is never duplicated into C-132; C-132 holds only a reference/citation to the causing content, per §5's "causing-action reference" field.
- **C-132 / C-133** (RO Decision 2, Option C): C-132 proceeds independently; no shared schema/service/ledger with C-133 is designed or authorized here; a future C-133 charter must separately assess reconciliation.
- **C-132 / C-114 / Domain Event / `record_audit`** (`IRA-C132 §3.3`, restated): Notification ≠ Audit Event ≠ Domain Event — structurally confirmed, not merely asserted, by direct source inspection of `AuditLogger`/`record_audit`/`Backend/Shared/Events`.

## 8. Business Object Eligibility (carried forward from `IRA-C132 §8` — not re-derived)

**FINDING (already established):** Notification satisfies `CMD-001 §26.3a` — Step 1 (Independent Identity) and Step 3 (Governed Lifecycle) both satisfied; Step 2 (Cross-Experience Reference) not presently satisfied but not required once Step 3 is. **Eligible for CBOR registration.** Formal `§26.4` registration via a dedicated ADR is a downstream action, not performed by this TDS (mirroring `ADR-019`'s registration of `CFG-000001` for WP-10, performed alongside/after its own TDS, not inside it).

## 9. Authority Model (carried forward from `IRA-C132 §12` — not re-derived)

Establishing a Notification is not itself an authority-bearing act — no dedicated Approval/Commit Authority gate is designed for `establish`. Any authenticated internal caller, acting on behalf of an already-authorized causing action, may create a Notification (subject to §6's own hosting/trigger-scope decision governing *who* may call it). Acknowledging a Notification is gated to the recipient (or `PLATFORM_ADMIN`, per standing platform convention) — no new authorization mechanism beyond `get_current_claims`/tenant-header discipline.

## 10. Lifecycle and Temporal Semantics (carried forward from `IRA-C132 §13`)

Minimum lifecycle: **unread (established) → acknowledged.** No third state (archive, auto-expiry) is designed here — not named in RO Decision 3's own scope. `SE-051`'s 7-year retention floor's applicability to Notification records (which are not themselves audit/evidence records, §7) is an open TDS-implementation-time question (§27), not an RO decision. The full `SD-003-226` interruption-ceiling/digest lifecycle remains deferred per RO Decision 3a (§19).

## 11. Tenant / Organization Relationship (carried forward from `IRA-C132 §11`)

Standard `CLAUDE.md §21.4` tenant-isolation discipline: every Notification is organization-scoped; `list`/`read` are exact-match tenant predicates; `read` returns 404 (not 403) for a cross-tenant id, mirroring `WP-17`'s certified anti-enumeration pattern. No new isolation mechanism is designed.

## 12. Transaction Model

Intra-service `establish` (any option in §6): atomic, same-transaction write, mirroring every closed WP's own repository-layer discipline. Cross-service `establish` (Option 1 only, if selected): explicitly **non-atomic** with the causing action — a best-effort, post-commit, logged-on-failure call, per §6.2 Option 1.D. This is a deliberate, disclosed design choice, not an oversight — a lost notification is judged a tolerable degraded outcome; a rolled-back causing business transaction because a notification-side-call failed would not be.

## 13. Idempotency / Concurrency

Not resolved by this TDS — an ordinary implementation-time choice (§27), per `IRA-C132 §14`'s own finding, unless a specific natural key is later found to carry a genuine concurrency risk (mirroring `TD-152`'s disposition for WP-14 BA-05).

## 14. Audit Requirements (carried forward from `IRA-C132 §15`)

Establish and acknowledge each call `record_audit()` (and, where the hosting service defines it, `publish_event()` as the existing structured-log stand-in — never a real event bus, per §18) — the standard, universal platform pattern. No new audit mechanism is designed; Notification does not become, replace, or duplicate an audit record (§7).

## 15. DS-001 Compliance / Frontend Boundary (carried forward from `IRA-C132 §10`, §18)

**Design target (closed, not open):** `DS-001` Chapter 21's four severities (`DS-001-350`) and three-element composition (`DS-001-351`) govern the Notification's own presentation shape (§5's logical fields already mirror this). Reusable today: `NotificationCenter.tsx` (panel shell, accessibility, mount point — extend, do not rebuild), and the existing `NotificationTone` vocabulary as a reference for the severity mapping (not a substitute for the persisted model). The unrelated `notifications/page.tsx` admin-config placeholder is out of this BA's own scope — its disposition is a separate, future question, not addressed here. No new DS-001 component, token, or pattern is required; no `CLAUDE.md §19.1` STOP-and-report is triggered on this dimension.

## 16. API Contract (design-level — endpoint shapes only, no schema-bound field list finalized)

Mirroring `WP-17`'s own router shape (`entitlement_license.py`):

- `POST /notifications` (or the hosting service's own path convention) — establish. Caller set governed by §6's decision.
- `GET /notifications` — list, for the current authenticated user, tenant-scoped.
- `GET /notifications/{id}` — read, tenant-isolated, 404-not-403 on cross-tenant.
- A state-transition endpoint (e.g. `POST /notifications/{id}/acknowledge`) — recipient-only.

Caller set: intra-service only, per §6.4 — no cross-service caller exists in this increment, so no cross-service API-auth question arises for the establish endpoint itself. Host resolved (§6.5): **`AuthService`**, mounted per its own existing `main.py` router-registration convention (kebab-case plural resource prefix, e.g. `/organizations`, `/domain-permissions`, `/approval-authorities`) — candidate prefix: **`/notifications`**. Exact request/response schema field names and error-response shapes remain implementation-time (§26), consistent with §6.6's conceptual field list.

## 17. Event / Dependency Relationship (restated, not re-derived — `IRA-C132 §16`, direct instruction §5 of the authorizing prompt)

- **FACT, preserved exactly:** abstract event contracts exist (`EventPublisher`/`EventSubscriber`); no concrete `EventSubscriber` exists in production; `publish_event()` is a structured-log stand-in, not a queryable/subscribable event.
- **This TDS does not repair or implement the event bus.** Option 5 (§6.2) is the only option that would require it, and it is explicitly excluded from the first increment regardless of which §6 option is chosen.
- If Option 1 is eventually selected (or adopted as a later increment after Option 2), its own cross-service call is a direct API dependency, **not** an event — this distinction is preserved deliberately so no future reader mistakes a synchronous HTTP call for "the event bus is now live."

## 18. Security / Authorization Considerations

Standard bearer-token + `X-Tenant-ID` pattern for every endpoint (§16), per existing platform convention. If Option 1 (§6) is selected, the cross-service internal API call requires its own authentication mechanism — **no existing internal-service-to-service authentication pattern was found in the evidence gathered for this TDS** (flagged in §6.2 Option 1.I as an open design surface, not resolved here).

## 19. Deferred Governance Questions (restated precisely, not reinterpreted)

- **RO Decision 3a** — the full `SD-003-226` per-user daily interruption ceiling and end-of-day digest mechanism remains deferred. This TDS's own minimum lifecycle (§10) and API contract (§16) do not implement it; any future TDS/charter language must carry this disclosure forward verbatim, per the RO's own explicit instruction.
- **RO Decision 2's own reconciliation obligation** — a future C-133 charter must assess reconciliation with C-132's own notification history; nothing in this TDS forecloses or pre-decides that assessment.

## 20. Implementation Sequencing (informative — not authorized by this document)

If Option 2 (§6.3) is eventually selected: (1) build the hosting service's model/repository/service/router per §5/§16, intra-service triggers only; (2) as a disclosed, separate future increment, extend to Option 1's cross-service pattern once a genuine cross-service trigger is needed. If Option 1 is selected directly: build both the model and the cross-service API-auth mechanism (§18) together. Neither sequencing is authorized here — informative only.

## 21. Test / V&V Expectations (informative — no tests written here)

The eventual implementation must satisfy `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist (two unrelated organizations, no shared row; cross-tenant read returns 404; any foreign-object identifier accepted in a request body is explicitly probed) — mirroring `WP-17`'s own certified test suite shape.

## 22. Migration Considerations

**No migration, ORM model, or database table is created, drafted, or authorized by this document.** The schema-shape STOP-and-report required by `CLAUDE.md §18`/`§19.4` (mirroring `TDS-C023-A §19`) has been performed at the conceptual level, now that §6.5 resolves the host — see §6.6 for the full field/type/constraint list. The physical Alembic migration itself (in `Backend/Services/AuthService/alembic/versions/`, mirroring `2026_09_01_0900-c3d4e5f6a7b8_c023_license_entitlement_context.py`'s own precedent) remains a separate, later, implementation-time action — not created by this document, and not authorized until a WP/BA charter and explicit Implementation Authorization exist.

## 23. Open Questions (disclosed, not resolved)

- ~~🔴 **RO DECISION REQUIRED** — §6 (service hosting + write-fan-in posture). The sole blocking item.~~ **Resolved:** write-fan-in posture = Option 2 (§6.4); existing-service host = `AuthService` (§6.5). **No RO decision remains open at TDS level** — §6.6's own schema-shape investigation confirmed no further RO decision surfaced.
- Exact ORM/migration-level details (exact `String` length bounds, exact index/constraint naming, whether a composite `(membership_id, status)` index is added) — implementation-time, per §6.6 item 10.
- Idempotency mechanism (§13, §6.6 item 8) — implementation-time, unless a concurrency risk is later found (mirrors `TD-152`).
- `SE-051` retention applicability to the Notification row itself (§10, §6.6 item 9) — disclosed, non-blocking, carried forward; a Technical Debt candidate at WP registration time, not a TDS blocker.
- Internal service-to-service authentication mechanism, if Option 1 is ever adopted as a later increment (§18) — a real design gap, not yet resolved by any existing repository pattern found; not blocking for this increment since no cross-service caller exists (§6.4).
- The unrelated `notifications/page.tsx` placeholder's own disposition (§15) — separate, future, not this BA's concern.
- C-130's own umbrella-vs-coordinate relationship to C-131/C-132/C-133 (`IRA-C132 §2`) — non-blocking, carried forward.

## 24. Readiness Implications

This TDS's own finalization does not, by itself, change `IRA-C132`'s own recorded classification. **`IRA-C132` remains 🟡 AMBER**, per the Repository Owner's own explicit instruction that it stays AMBER "unless governance evidence justifies a different formal state through the repository's established process" — no such separate re-classification process has been run in this pass, so `IRA-C132`'s own document is not edited here. AMBER's own original meaning ("ready for Technical Design preparation; not yet ready for TDS finalization or Implementation Authorization") is now satisfied on its TDS-finalization half: this TDS **is** finalized (§1, §28). AMBER's Implementation-Authorization half is unaffected — WP registration, BA charter creation, and Implementation Authorization remain separate, later governance stages this document does not perform (§20, §27).

## 25. Traceability

| Requirement | Source | Design decision (this TDS) |
|---|---|---|
| C-131/C-132 boundary | `ROD-C132` RO Decision 1 | §7 — restated, not reinterpreted |
| C-132/C-133 boundary | `ROD-C132` RO Decision 2 | §7, §19 — restated |
| First-BA scope (establish/list/read/acknowledge) | `ROD-C132` RO Decision 3 | §2, §4, §16 |
| Delivery/event-bus exclusion | `ROD-C132` RO Decision 3 | §3, §17 |
| `SD-003-226` deferral | `ROD-C132` RO Decision 3a | §19 |
| Notification ≠ Audit/Domain/Timeline Event | `ROD-C132` architectural clarification | §7, §17 |
| Event-infrastructure finding | `ROD-C132` §6 / `IRA-C132 §16` | §6.1, §17 |
| BO eligibility | `IRA-C132 §8` | §8 |
| Tenant isolation pattern | `IRA-C132 §11`, `CLAUDE.md §21.4` | §11, §21 |
| Authority model | `IRA-C132 §12` | §9 |
| DS-001 severity/composition | `DS-001` Ch. 21 (`DS-001-345`–`360`) | §5, §15 |
| Service-hosting gap | `IRA-C132 §17` | §6 (this document's own centerpiece) |
| Write-fan-in posture = Option 2 (intra-service only, first increment) | RO instruction ("AUREX — C-132 Service-Hosting Decision," 2026-09-05) | §6.4 |
| Existing-service host = `AuthService` (H-1) | RO instruction ("AUREX — C-132 Existing Service Host Decision," 2026-09-05) | §6.5 |
| Conceptual schema shape (fields, ownership, tenant scope, lifecycle, temporal, acknowledgement, audit, idempotency, retention, indexes) | Schema-shape STOP-and-report, per `CLAUDE.md §18`/`§19.4`, mirroring `TDS-C023-A §19` | §6.6 |

No requirement above was manufactured; every row traces to an already-recorded decision or an already-completed IRA finding.

## 26. Implementation-Time Questions vs. TDS-Level Questions (explicit separation, per direct instruction)

**Resolved at TDS level (this document):** scope/non-scope (§2/§3), ownership boundaries (§7), BO eligibility (§8), authority model (§9), lifecycle floor (§10), tenant pattern (§11), transaction posture per option (§12), audit pattern (§14), DS-001 target (§15), API endpoint shape (§16), event non-dependency (§17), write-fan-in posture (§6.4), existing-service host (§6.5), conceptual schema shape (§6.6).

**Left to implementation time (not requiring further TDS or RO decision):** exact `String` length bounds and index/constraint naming; whether a composite `(membership_id, status)` index is added (§6.6 item 10); exact idempotency mechanism (unless a concurrency risk is later found, mirroring `TD-152`); exact repository method signatures; exact endpoint URL naming beyond the shape in §16; exact frontend component composition inside the already-reusable `NotificationCenter.tsx` shell; the Notification row's own retention/purge policy, if any (§6.6 item 9, disclosed non-blocking).

**Requires the Repository Owner, not decidable at TDS or implementation time:** none remaining. Both items this TDS originally isolated (service hosting, write-fan-in posture) are now resolved (§6.4, §6.5); the schema-shape investigation §6.6 performed did not surface a further item.

## 27. Change Control

**Files created (original drafting pass):** this document only — `architecture/05-Implementation/TDS-C132_Enterprise_Notifications_Minimum_BA_Technical_Design.md`.
**Files modified (write-fan-in pass, "AUREX — C-132 Service-Hosting Decision"):** this document only — recorded the RO's Option 2 write-fan-in selection (§6.4) and the then-open existing-service-host item (§6.5), with consistency updates to §1, §5, §16, §22, §23, §25.
**Files modified (this pass, "AUREX — C-132 Existing Service Host Decision"):** this document only — recorded the RO's H-1 (`AuthService`) host selection (§6.5), performed the schema-shape STOP-and-report (§6.6, new), and updated §1 (status paragraph — now FINALIZED), §5 (domain model, resolved), §16 (API contract, resolved), §22 (migration considerations, resolved), §23 (open questions, resolved), §24 (readiness implications), §25 (traceability), §26 (implementation-time separation), and added §28 (full consistency review). No other section's own substantive content was altered; §§6.1–6.3 and §6.5's own original investigation content are preserved verbatim as historical/evidentiary record, per direct instruction.
**Files read for cross-reference, not modified:** `ROD-C132-Enterprise-Notifications-Capability-Boundary-and-Minimum-Scope.md`, `IRA-C132_Enterprise_Notifications_Implementation_Readiness_Assessment.md`, `Master_Technical_Architecture.md`, `ARCH-000`, `CAP-001`, `SD-003` §8, `DS-001` (Chapter 21), `CLAUDE.md §8/§18/§19/§21.4`, `CMD-001 §26.3a`, `ADR-036`, `TDS-013 §26a`, `TDS-012`, `TDS-C023`/`TDS-C023-A`, `TECH-DEBT.md TD-151`/`TD-152`, `Backend/Services/AuthService/models/c023_entitlement_context.py`, `c023_license_context.py`, `access_evaluation_outcome.py`, `membership.py` (read directly, this pass, for the schema-shape STOP-and-report's own convention evidence), `Backend/Services/AuthService/main.py` (router-prefix convention, this pass), and the frontend/backend source files already cited by `IRA-C132 §3`.
**Not modified:** `CAP-001`, `SD-003`, `DS-001`, `PE-001`, `SER-001`, `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`, `WPR-001`, `WP-REG-001`, `CBOR-INDEX.md`, `TECH-DEBT.md`, any WP-17/C-023, WP-18, C-040, or C-114 artifact, `IRA-C132`, `ROD-C132`, any `Backend/`/`source/frontend/` file, any migration, any test, any schema. No WP registered. No BA charter created. No implementation of any kind performed. **This document is now FINALIZED** (§1, §28) — both isolated RO decisions (write-fan-in posture, existing-service host) are resolved, and the consequent schema-shape STOP-and-report surfaced no further RO decision. Nothing was staged, committed, or pushed.

## 28. Full Consistency Review (this pass) — TDS Readiness Test

Performed against `CAP-001`, `SD-003` §8, `ROD-C132`, `IRA-C132`, `CLAUDE.md`'s governance rules, and the repository's own hosting precedents, per direct instruction, before finalization.

**Preserved RO decisions, verified verbatim, none reopened:**
- RO Decision 1 (`ROD-C132`): C-131 owns comment/mention content; C-132 owns the resulting Notification. Restated §7 — unchanged.
- RO Decision 2 (`ROD-C132`): C-132 proceeds independently; C-133 remains Planned. Restated §7, §19 — unchanged.
- RO Decision 3 (`ROD-C132`): first BA = Notification record only (establish/manage/list/read/acknowledge). Restated §2, §4, §16 — unchanged; no delivery, event-bus, or orchestration scope leaked in anywhere (§3, §6.4's own explicit non-authorization list, §6.6 item 8's own explicit non-invention of new mechanisms).
- RO Decision 3a (`ROD-C132`): `SD-003-226` interruption ceiling/digest deferred. Restated §19 — unchanged; §10's own minimum lifecycle does not implement it.
- Service-hosting decision: H-1 `AuthService` (this pass, §6.5) — consistent with `CLAUDE.md §8`'s one-capability-one-owning-service rule; no cross-service database access designed anywhere (§6.6 item 3, item 1's `source_id` non-FK design).
- Write-fan-in: intra-service only for the first increment; cross-service fan-in deferred (§6.4) — no synchronous cross-service call, event bus, or delivery mechanism is designed by §6.6's schema shape.

**TDS Readiness Test — the sixteen questions, answered:**

| # | Question | Answer | Section |
|---|---|---|---|
| 1 | What is the Notification BO? | A persisted, tenant-scoped, recipient-anchored record of a system-generated notification, eligible under `CMD-001 §26.3a` | §8, §6.6.1 |
| 2 | Who owns it? | `AuthService`, exclusively (§6.5) | §6.5, §6.6.2 |
| 3 | Where is it persisted? | `AuthService`'s own database, candidate table `c132_notification` | §6.6.1 |
| 4 | What tenant boundary applies? | The recipient's own `Membership.organization_id`, via `membership_id` — no duplicated column | §6.6.3, §11 |
| 5 | Who can establish it? | Any authenticated intra-`AuthService` caller acting on behalf of an already-authorized causing action | §9, §6.4 |
| 6 | Who can acknowledge it? | The recipient (`membership_id`) only, or `PLATFORM_ADMIN` | §9, §6.6.6 |
| 7 | What is its lifecycle? | `UNREAD` → `ACKNOWLEDGED`, one-directional, no third state | §10, §6.6.4 |
| 8 | What transactions are atomic? | Intra-service `establish`/`acknowledge` — ordinary same-transaction write; no cross-service transaction exists in this increment | §12 |
| 9 | What prevents duplicate creation? | Nothing at the governance level — no invariant is named requiring one; ordinary implementation-time idempotency applies if a concrete risk is later found | §13, §6.6.8 |
| 10 | What is audited? | `establish`/`acknowledge`, via `record_audit()`/`publish_event()`, the standard universal pattern | §14, §6.6.7 |
| 11 | What API surface is required? | `POST /notifications`, `GET /notifications`, `GET /notifications/{id}`, `POST /notifications/{id}/acknowledge`, in `AuthService` | §16 |
| 12 | What frontend surface is required? | Extend the existing `NotificationCenter.tsx` shell; no new component/token | §15 |
| 13 | What is explicitly excluded? | Delivery (email/SMS/push/webhook), real event-bus infrastructure, multi-channel orchestration, the full `SD-003-226` regime, C-131/C-133 implementation | §3 |
| 14 | How does the first increment operate without cross-service DB access? | Every caller in this increment is intra-`AuthService`; no cross-service call of any kind is built | §6.4, §6.2 Option 2.C |
| 15 | What is deferred to the future increment? | Cross-service write fan-in (Option 1's synchronous API pattern, once a genuine cross-service trigger is needed) | §6.4, §20 |
| 16 | What implementation-time decisions remain? | Exact column bounds/index naming, exact idempotency mechanism, exact repository/router signatures, Notification-row retention policy | §26 |

**No unresolved TDS-level architectural question was found converted into a silent implementation decision.** No deferred scope (delivery, event bus, cross-service fan-in, `SD-003-226`, C-131/C-133) was found to have leaked into the first BA's own design anywhere in §§1–26. This TDS is accordingly finalized (§1).

*End of TDS-C132 (FINALIZED).*
