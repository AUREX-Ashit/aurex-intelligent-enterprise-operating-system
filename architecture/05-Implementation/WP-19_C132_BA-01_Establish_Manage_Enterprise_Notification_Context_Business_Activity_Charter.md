# WP-19 — BA-01 (C-132 Enterprise Notifications) — Establish / Manage Enterprise Notification Context — Business Activity Charter

**Work Package:** WP-19 — the next unclaimed Work Package number, verified directly this pass against `WPR-001` (highest Business Capability row: `WP-18`, C-003, CLOSED — CERTIFIED — RELEASE-READY) and `WP-REG-001` (highest registered row: `WP-16`); no `WP-19` row, reference, or reservation exists anywhere in `WPR-001`, `WP-REG-001`, or any other governance register checked this session.
**Business Activity:** BA-01 — Establish / Manage Enterprise Notification Context
**Capability:** C-132 Enterprise Notifications (`CAP-001` line 105, Domain D-007 Collaboration & Engagement, owning specification `SD-003`, Active)
**Status:** ~~**CHARTERED — IMPLEMENTATION NOT YET AUTHORIZED, NOT YET COMPLETE, NOT CERTIFIED.** No implementation code, schema, migration, router, service, repository, model, or frontend component exists. Not started; no `CLAUDE.md §19.7b` gate has been dispatched.~~ *(Superseded through 2026-09-09 — see the Change Control entries below.)* **CHARTERED — IMPLEMENTATION AUTHORIZED — IMPLEMENTATION COMPLETE — `CLAUDE.md §19.7b` GATE 1 PASSED — GATE 2 V&V PASSED — GATES 3/4 NOT TRIGGERED — GATE 5 RELEASE READINESS PASSED — FORMALLY CLOSED — CERTIFIED — RELEASE-READY** (2026-09-09; all five `CLAUDE.md §19.7b` gates complete; governance-recording complete; **repository commit outstanding — a separate, explicitly-authorized action**, mirroring `WP-16`/`WP-17`/`WP-18`). Gate sequence: original independent Gate 1 review **❌ FAIL** (finding F-1 — a HIGH-severity tenant-isolation defect in `POST /notifications`, 2026-09-05) → F-1 remediation (implementing session, RO-authorized, 2026-09-06) → **fresh independent Gate 1 re-review ✅ PASS** (2026-09-06) → **fresh independent Gate 2 V&V Audit ✅ PASS** (2026-09-08 — 24/0/0 RTM, 0 material findings, 8 non-material observations O1–O8, F-1 negative control confirming the pre-fix defect and its closure) → **Gate 3 NOT TRIGGERED / Gate 4 NOT TRIGGERED** → **fresh independent Gate 5 Release Readiness Audit ✅ PASS** (2026-09-09 — 0 material findings, release isolation CLEAN, explicit 19-path release allowlist) → **formal WP-19 / BA-01 closure** (2026-09-09). Full record: `architecture/06-Reviews/CERT-WP-19_Establish_Manage_Enterprise_Notification_Context.md` (Gate 1 record of record) and `IMP-REPORT-WP-19 §12/§13/§14/§15/§16/§17` (§15 = Gate 2 V&V result of record; §16/§17 = Gate 5 + formal-closure result of record); the original Gate 1 FAIL is preserved as historical fact. **This closure applies to WP-19 / C-132 BA-01 only — it does NOT close C-132 as a capability. C-132 capability-wide status remains 🟡 AMBER (`IRA-C132`, unchanged) — not reclassified; no capability-wide C-132 completion is claimed; all deferred C-132 scope (external delivery channels, real event bus, `SD-003-226`, C-131/C-133 integration, broader notification-platform infrastructure, further C-132 Business Activities) remains deferred.**
**Prepared under:** direct Repository Owner instruction ("AUREX — C-132 Next Governance Phase — WP Registration + BA Charter"), 2026-09-05, following `TDS-C132`'s own finalization (§1, §28 — full consistency review, TDS Readiness Test passed).

**A note on document type, disclosed rather than assumed (mirrors `WP-14 BA-04`'s, `WP-15 BA-01`'s, `WP-16 BA-01`'s, and `WP-17 BA-01`'s own identical disclosure):** this repository's own established convention charters at the Work Package level, with per-Business-Activity charter detail specified inside the governing IRA. `WP-14 BA-04`, `WP-15 BA-01`, `WP-16 BA-01`, and `WP-17 BA-01` each departed from that convention, per direct Repository Owner instruction, establishing a Business-Activity-level charter as real, repeated repository precedent. This document follows that same shape, again per direct instruction.

**Governing basis for BA-01, stated explicitly:** `CAP-001` (C-132 registration, line 105) → `SD-003` §8 (Notifications, Attention & Cognitive Load Laws) → `ROD-C132-Enterprise-Notifications-Capability-Boundary-and-Minimum-Scope.md` (RO Decisions 1/2/3/3a, architectural clarifications, event-infrastructure finding) → `IRA-C132_Enterprise_Notifications_Implementation_Readiness_Assessment.md` (🟡 AMBER — Ready for Technical Design preparation; not yet ready for Implementation Authorization) → `TDS-C132_Enterprise_Notifications_Minimum_BA_Technical_Design.md` (FINALIZED — service host `AuthService`, write-fan-in Option 2, schema shape recorded at §6.6) → this charter. **No implementation exists at any point in this chain.**

---

## Classification Key

Mirrors `WP-15 BA-01`'s, `WP-16 BA-01`'s, and `WP-17 BA-01`'s own key exactly:
- **A** — already determined by governing documents
- **B** — determined by repository precedent
- **C** — an implementation detail
- **D** — requires a Repository Owner decision, genuinely open
- **D → RESOLVED** — was **D**, now resolved by a recorded decision

---

## 1. Business Activity Identity — [A]

BA-01, WP-19, Capability C-132 Enterprise Notifications (`CAP-001` D-007, Active). Governed physical Business Object: a new C-132-owned Notification record (candidate table name `c132_notification`, `TDS-C132 §6.6` item 1 — a design recommendation, not yet built), eligible for `CMD-001 §26.3a` CBOR registration (Step 1 + Step 3 satisfied, `IRA-C132 §8`/`TDS-C132 §8`). Write path — establishes exactly one Notification per recipient-anchored, in-application, causing-action citation; supports list, read, and a one-directional acknowledge transition. No edit or delete of an established Notification's own content is designed (`TDS-C132 §4`).

## 2. Business Intent (Scope) — [A]

Verbatim basis, `CAP-001`: *"Deliver notifications."* Realized, at this BA's own minimum scope, per `ROD-C132` RO Decision 3 (Option A — Notification record only): a persisted, tenant-scoped, recipient-anchored, in-application Notification record supporting **establish, list, read, and acknowledge** — realizing `SD-003` §8's Notification composition/severity laws (`DS-001-350`/`351`) at the data layer, without any delivery, orchestration, or cross-capability integration. This is the narrowest slice `IRA-C132 §9`'s own Candidate First BA Definition and `TDS-C132 §2` already scoped, carried into this charter unchanged.

**Scope, stated explicitly:**
- **In scope:** establish a Notification (recipient, severity, three-element composition payload, non-FK causing-action citation); list Notifications for the current authenticated user, tenant-scoped; read one Notification by id, tenant-isolated; acknowledge a Notification (`UNREAD → ACKNOWLEDGED`).
- **Out of scope:** see §19.

## 3. Trigger — [A]

Caller-invoked, **intra-`AuthService` only**, per `TDS-C132 §6.4`'s RO-decided write-fan-in posture (Option 2). Any already-authorized `AuthService` capability (e.g., an Entitlement/License change, a Membership change, a structural change) may invoke `establish` on behalf of its own causing action. **No cross-service caller exists or is designed in this increment** — a C-131 mention, or any capability outside `AuthService`, cannot yet trigger a Notification; this is an explicit, disclosed scope narrowing (`TDS-C132 §6.2` Option 2.I), not a silent one.

## 4. Actor / Persona — [A]

The **recipient** (`Membership` — Person × Organization) for `list`/`read`/`acknowledge`; any authenticated intra-`AuthService` caller acting on behalf of an already-authorized causing action, for `establish` (`TDS-C132 §9`). `PLATFORM_ADMIN` may also acknowledge, per standing platform convention (`TDS-C132 §9`/§6.6 item 6). No dedicated "Notification Steward" or equivalent narrative persona is named in `SD-003` — none is invented here.

## 5. Preconditions — [A]

- A `Membership` row (Person × Organization) must already exist for the intended recipient (`C-007`, live, unchanged) — this is the recipient anchor and the tenant anchor simultaneously (`TDS-C132 §6.6` items 1/3).
- The causing action that triggers `establish` must already be an authorized, already-committed (or already-authorized) act within `AuthService` — `establish` never itself performs or re-authorizes the causing action (`TDS-C132 §6.4`).
- No precondition requires a real event bus, a delivery provider, or any cross-service call — none exists or is designed for this increment (`TDS-C132 §6.1`/§17).

## 6. Input Contract — [C]

Design-level only, per `TDS-C132 §16`/`§6.6` — not yet a frozen API contract (no router/schema exists): recipient `membership_id`; severity (one of DS-001's four closed values, `DS-001-350`); composition payload (`what_happened` mandatory, `why_it_matters`/`what_happens_next` optional, per `DS-001-351`); causing-action citation (`source_type` free-text, `source_id` non-FK UUID). **The actual request/response schema is implementation work, not performed by this charter.**

## 7. Business Rules — [A]

- A Notification's severity is one of exactly four closed values (`DS-001-350`); its composition payload is the closed three-element structure (`DS-001-351`) — no fifth severity or fourth composition element may be invented (`TDS-C132 §15`).
- A Notification is never itself an Audit Event, a Domain Event, a Timeline Event, or a C-131 comment/mention (`ROD-C132` architectural clarification, `TDS-C132 §7`) — these remain structurally distinct constructs, never merged or duplicated.
- The causing-action reference is a non-authoritative, point-in-time citation only (`source_type` + `source_id`, non-FK) — it never becomes an authoritative cross-reference or a substitute for the causing capability's own audit trail (`TDS-C132 §6.6` item 1).
- No uniqueness/idempotency invariant is imposed at the governance level — a recipient may legitimately receive multiple, distinct notifications from the same causing source over time (`TDS-C132 §6.6` item 8).
- AI assistance, if any is ever added, remains out of this BA's own scope entirely — no AI-assisted composition, prioritization, or delivery logic is designed or authorized here.

## 8. Persistence Target — [service host RESOLVED by direct Repository Owner decision; schema shape recorded, physical migration deferred]

A new C-132-owned Notification record, hosted in `AuthService` (`TDS-C132 §6.5` — Repository Owner selected H-1). Candidate physical table name `c132_notification` (`TDS-C132 §6.6` item 1, mirroring `c023_entitlement_context`/`c023_license_context`'s own capability-prefixed naming convention). **This charter does not create, authorize, or assign this table.** The conceptual field/type/constraint list is recorded in full at `TDS-C132 §6.6`; the physical Alembic migration itself remains implementation-time work, subject to `CLAUDE.md §18`/`§19.4` at the point of actual creation — the schema-shape STOP-and-report required by that rule has already been performed at the conceptual level (`TDS-C132 §6.6`), and surfaced no further Repository Owner decision.

## 9. State / Lifecycle Transition — [A]

`(none) → UNREAD` (establish) `→ ACKNOWLEDGED` (acknowledge) only, per `TDS-C132 §10`/`§6.6` item 4. One-directional; no un-acknowledge; no archive/expiry state is designed in this BA (`ROD-C132` RO Decision 3a — the full `SD-003-226` interruption-ceiling/digest lifecycle remains deferred, not implemented here, see §19).

## 10. Authorization / Accountability — [A, mechanism resolved; instance is implementation work]

`establish`: any authenticated, already-authorized intra-`AuthService` caller acting on behalf of an already-authorized causing action — establishing a Notification is not itself an authority-bearing act; no dedicated Approval/Commit Authority gate is designed (`TDS-C132 §9`, carried from `IRA-C132 §12`). `list`/`read`: the current authenticated user, tenant-scoped to their own `Membership`. `acknowledge`: gated to the recipient (`membership_id`) or `PLATFORM_ADMIN` — no new authorization mechanism beyond `get_current_claims`/tenant-header discipline (`TDS-C132 §9`, §6.6 item 6). No new authority model, approval mechanism, or accountability point is invented by this charter.

## 11. Organization / Membership Boundary (Tenant Isolation) — [A]

Every Notification is organization-scoped via its own recipient's `Membership.organization_id` — no separate, duplicated `organization_id` column is added (`TDS-C132 §11`/`§6.6` item 3, mirroring `AccessEvaluationOutcome`'s own established precedent of not duplicating tenant scope alongside `membership_id`). `list`/`read` enforce standard `CLAUDE.md §21.4` tenant-isolation discipline: exact-match tenant predicates via the join through `membership_id`; `read` returns 404 (not 403) for a cross-tenant id, mirroring `WP-17`'s own certified anti-enumeration pattern. `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist governs implementation-time test obligations (§18 below).

## 12. Events / Outcomes — [C]

Design-level only, per `TDS-C132 §14`/`§17` (carried from `IRA-C132 §15`/§16): `establish` and `acknowledge` each call `record_audit()` (and `publish_event()` where `AuthService` already defines it as its own structured-log stand-in) — the same universal pattern every other `AuthService` capability already uses. **No new audit or event mechanism is designed.** No real event bus, concrete `EventSubscriber`, or broker-connected publication exists or is authorized (`ROD-C132` event-infrastructure finding, `TDS-C132 §6.1`/§17, unchanged).

## 13. Error / Rejection Conditions (Validation) — [C]

Design-level only, per `TDS-C132 §6.6`/§16 (not yet implemented): recipient `Membership` not found → 404 (establish); a cross-tenant `read` by id → 404, not 403 (anti-enumeration, mirroring `WP-17`); an invalid/unrecognized `severity` value → rejected (`CheckConstraint`-enforced closed set, `DS-001-350`); a missing mandatory `what_happened` composition element → rejected (`DS-001-351`); acknowledging an already-`ACKNOWLEDGED` Notification's own exact behavior (idempotent no-op vs. error) is an implementation-time choice, not governance-required (`TDS-C132 §6.6` item 6).

## 14. Idempotency Expectations — [C]

Design-level, per `TDS-C132 §13`/`§6.6` item 8: no uniqueness constraint is governance-required — a recipient may legitimately receive multiple, distinct notifications from the same causing source over time. Establish-time idempotency (e.g., de-duplicating a double-submit) remains an ordinary implementation-time concern, unless a concrete concurrency risk is later found, mirroring `TD-152`'s own disposition. **Not yet implemented** — no code, no test exists.

## 15. Audit / Observability Expectations — [C]

Design-level only, per `TDS-C132 §14`/§6.6 item 7: `record_audit()` on `establish` and `acknowledge`, citing the recipient's `membership_id`, severity, composition payload, causing-action citation (`source_type`/`source_id`), resulting status, and a correlation identifier; on failure, the specific rejection reason. `SE-051`'s 7-year retention floor binds this audit trail, not the Notification row itself (`TDS-C132 §6.6` item 9, `ROD-C132` architectural clarification). **Not yet implemented.**

## 16. Dependencies — [A]

`C-007` (Membership) — already satisfied, closed, certified; the recipient/tenant anchor this BA reuses directly. `DS-001` Chapter 21 (Notification Styling) — already frozen, closed constitutional spec, realized at the data layer only by this BA. `NotificationCenter.tsx` — already-existing, reusable frontend shell, extended not rebuilt (§21 below). No dependency on `C-131` (unchartered), `C-133` (Planned, not Active — `ROD-C132` RO Decision 2), any event-bus/broker infrastructure (none exists, not built here), or any delivery-provider integration. No dependency on `C-023`/`WP-17`, `WP-18`, `C-040`, `C-114`, or `AI-002`/Sarika — none evidenced anywhere in `SD-003`'s own text, and none is asserted by this charter.

## 17. Acceptance Criteria — [C, not yet testable — no code exists]

**Cannot yet be stated as a testable, implementation-level criterion** — no code exists to test. The design-level acceptance criterion, per `TDS-C132 §21`/§28 (TDS Readiness Test): an authenticated intra-`AuthService` caller can establish a Notification for a valid recipient `Membership`; the recipient can list and read their own Notifications, tenant-isolated (404-not-403 on cross-tenant); the recipient (or `PLATFORM_ADMIN`) can acknowledge a Notification, transitioning it `UNREAD → ACKNOWLEDGED` exactly once in its governance-required sense; every closed-set field (`severity`, `status`) rejects a value outside its own closed set. **This becomes testable only once Implementation Authorization is separately granted and the schema/service work is built.**

## 18. Test Obligations — [D, NOT YET SATISFIED]

**No test exists.** A future implementing session must, at minimum, satisfy `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist (two distinct, unrelated Organizations, no shared row; a cross-Organization `read`/`list` visibility probe confirming 404-not-403; an explicit probe of whether an unrelated tenant's `membership_id` or Notification id is accepted) and `TDS-C132 §21`'s own designed V&V expectations, mirroring `WP-17`'s own certified test suite shape. **None of this C-132 test coverage exists today.**

## 19. Out-of-Scope Boundaries (Non-Scope) — [A]

Restated verbatim from `ROD-C132` RO Decision 3 and `TDS-C132 §3`, not reinterpreted:
- Email, SMS, push, webhook, or any external-channel delivery; delivery-provider integration.
- Real event-bus/event-subscriber infrastructure (`ROD-C132` event-infrastructure finding; `TDS-C132 §17`/§6.1, unchanged — `Backend/Shared/Events` is not repaired or implemented by this BA).
- Multi-channel notification orchestration.
- The full `SD-003-226` interruption-ceiling/digest mechanism (`ROD-C132` RO Decision 3a — deferred, not abandoned).
- Any C-131 comment/mention implementation (`ROD-C132` RO Decision 1 — the seam is preserved, not built).
- Any C-133 activation, shared schema, shared service, or common ledger (`ROD-C132` RO Decision 2 — C-133 remains Planned, not Active).
- Cross-service write fan-in of any kind, including Option 1's synchronous best-effort API pattern (`TDS-C132 §6.4` — explicitly deferred to a disclosed future increment, not this BA).
- Cross-service database access, a new dedicated `NotificationService`, or any workaround of `CLAUDE.md §8` (`TDS-C132 §6.4`/§6.5).
- Broader notification-platform infrastructure not explicitly named above.
- Any future capability not explicitly named in this charter.

## 20. Implementation Readiness Classification — TDS Sufficiency Acceptance

**`TDS-C132_Enterprise_Notifications_Minimum_BA_Technical_Design.md` is hereby formally accepted as the governing Technical Design for this Business Activity.** Result, per its own §28 full consistency review and TDS Readiness Test: **FINALIZED.** Acceptance is a governance act recognizing the TDS's own already-finalized conclusion — it does not alter `IRA-C132`'s own 🟡 AMBER classification, which remains unchanged, unreopened, and controlling for full implementation readiness. **This is a chartering-sufficiency acceptance, not an implementation-readiness acceptance — the two are deliberately not conflated anywhere in this charter**, mirroring `WP-17 BA-01`'s own identical distinction between "governance decisions resolved" and "implementation readiness achieved."

## 21. Enterprise Experience / API-UI Boundary Scope Decision — `CLAUDE.md §20.3` [A, resolved by direct carry-forward, not reopened]

**RESOLVED: Extend the existing `NotificationCenter.tsx` shell; no new component, token, or theme.** Per `TDS-C132 §15` (carried from `IRA-C132 §10`): `DS-001` Chapter 21's four severities (`DS-001-350`) and three-element composition (`DS-001-351`) govern the Notification's own presentation shape; `NotificationCenter.tsx` (panel shell, accessibility, mount point) is reusable today and is extended, not rebuilt. The unrelated `notifications/page.tsx` admin-config placeholder is out of this BA's own scope — its disposition is a separate, future question, not addressed here. **No frontend code exists — this remains implementation work, not performed by this charter.** API surface (design-level, `TDS-C132 §16`): `POST /notifications`, `GET /notifications`, `GET /notifications/{id}`, `POST /notifications/{id}/acknowledge`, mounted in `AuthService` under a candidate `/notifications` prefix, per its own existing router-registration convention. Caller set for `establish`: intra-`AuthService` only (§3 above).

**Scope of this decision, stated explicitly, mirroring `WP-17 §21`'s own convention:**
- Applies only to BA-01/WP-19's own current chartered scope. It is a scope decision for this Business Activity, not a constitutional prohibition on further Enterprise Experience work for C-132 generally.
- Does not mean C-132 can never have a fuller frontend (e.g., a dedicated notification-preferences screen) — a future, separately-chartered Business Activity remains fully possible and is not foreclosed.
- Does not expand BA-01's own scope (§19) — every excluded item there remains excluded, unaffected by this decision.

## 22. Repository Owner Decisions Recorded (summary — full text: `ROD-C132-Enterprise-Notifications-Capability-Boundary-and-Minimum-Scope.md` §1–4; `TDS-C132_Enterprise_Notifications_Minimum_BA_Technical_Design.md §6.4`/§6.5)

| Decision | Disposition |
|---|---|
| 1 — C-131 / C-132 boundary | RESOLVED, Option A — Clean initiator-based split (`ROD-C132 §1`). C-131 owns comment/mention content; C-132 owns the resulting Notification. Not reopened by this charter; C-131 implementation not part of this BA (§19 above). |
| 2 — C-132 / C-133 boundary | RESOLVED, Option C — Build C-132 independently now (`ROD-C132 §2`). C-133 remains Planned; no shared schema/service/ledger. Not reopened by this charter (§19 above). |
| 3 — First C-132 BA minimum scope | RESOLVED, Option A — Notification record only (`ROD-C132 §3`). This charter's own scope (§2) directly implements that resolution. |
| 3a — `SD-003-226` interruption ceiling/digest | RESOLVED (deferral), Option B — Defer (`ROD-C132 §4`). Not reopened by this charter; not part of this BA (§19 above). |
| Service-hosting / write-fan-in | RESOLVED — Host: `AuthService` (H-1); write-fan-in: Option 2, intra-service-only first increment, cross-service fan-in deferred (`TDS-C132 §6.4`/§6.5). Directly implemented at §3/§8/§10 above. |

**No decision above is reopened, altered, or reinterpreted by this charter.**

## 23. Operation-Level Detail — Establish / List / Read / Acknowledge

Restated at charter level for auditability, per direct instruction, deriving from `TDS-C132 §2`/§16/§6.6 — not reinterpreted:

- **Notification establishment:** an intra-`AuthService` caller, acting on an already-authorized causing action, creates one Notification for one recipient (`Membership`), with a severity, a composition payload, and a non-FK causing-action citation. Sets `status = UNREAD`, `created_at = now()`. Audited (§15).
- **Management:** per `IRA-C132 §9`, "manage" carries no meaning beyond the four operations named here — no separate edit/delete/reconfigure capability is designed or implied.
- **Listing:** the current authenticated user lists their own Notifications, tenant-scoped via their own `membership_id`. No cross-user or cross-tenant listing exists.
- **Reading:** the current authenticated user reads one Notification by id, tenant-isolated; a cross-tenant id returns 404, not 403 (anti-enumeration).
- **Acknowledgement:** the recipient (or `PLATFORM_ADMIN`) transitions one Notification `UNREAD → ACKNOWLEDGED`, setting `acknowledged_at = now()`. One-directional; no un-acknowledge. Audited (§15).

No operation above authorizes delivery, orchestration, or any mechanism excluded at §19.

## 24. Traceability

| Requirement | Source | Charter section |
|---|---|---|
| C-131/C-132 boundary | `ROD-C132` RO Decision 1 | §7, §16, §19, §22 |
| C-132/C-133 boundary | `ROD-C132` RO Decision 2 | §16, §19, §22 |
| First-BA scope (establish/list/read/acknowledge) | `ROD-C132` RO Decision 3 | §2, §23 |
| Delivery/event-bus exclusion | `ROD-C132` RO Decision 3, event-infrastructure finding | §12, §19 |
| `SD-003-226` deferral | `ROD-C132` RO Decision 3a | §9, §19 |
| Notification ≠ Audit/Domain/Timeline Event | `ROD-C132` architectural clarification | §7 |
| BO eligibility | `IRA-C132 §8`, `TDS-C132 §8` | §1 |
| Service host = `AuthService` | `TDS-C132 §6.5` | §8, §22 |
| Write-fan-in = Option 2 | `TDS-C132 §6.4` | §3, §22 |
| Conceptual schema shape | `TDS-C132 §6.6` | §8, §13, §14 |
| Tenant isolation pattern | `TDS-C132 §11`, `CLAUDE.md §21.4` | §11, §18 |
| Authority model | `TDS-C132 §9` | §10 |
| DS-001 severity/composition | `DS-001` Ch. 21 | §7, §21 |

No requirement above was manufactured; every row traces to an already-recorded decision or an already-finalized TDS finding.

## 25. Implementation Status and Sequencing Disclosure

**No implementation exists.** No production code, schema, migration, router, service, repository, model, or frontend component has been created for C-132 at any point, in this charter or any prior C-132 governance artifact. **`CLAUDE.md §19.7b` Gates 1, 2, and 5 have not been dispatched.** This charter does not authorize Implementation — a separate, explicit Repository Owner act is required (§20's own "TDS Sufficiency Acceptance" is not that act, mirroring `WP-17 §24`'s own identical disclaimer).

## 26. CBOR Status

**Not assessed for formal registration by this charter.** Whether the new C-132-owned Notification construct (§1) is eligible for Canonical Business Object Registration (`CMD-001 §26.3a`) has already been analyzed at the IRA/TDS level (`IRA-C132 §8`, `TDS-C132 §8`: Step 1 + Step 3 satisfied, eligible) — but formal `§26.4` registration via a dedicated ADR is a downstream action, not performed by this charter, mirroring `ADR-019`'s registration of `CFG-000001` for WP-10 (performed alongside/after its own TDS, not inside the charter) and `WP-17 §25`'s own identical disclosure pattern.

---

## Final Determinations

**This charter does NOT itself:** create the `c132_notification` table or any migration; write production code, tests, or frontend; perform CBOR registration (§26); grant Implementation Authorization (§25); resolve any decision beyond those already recorded in `ROD-C132`/`TDS-C132` (§22); commit or push anything.

**Explicitly preserved, unchanged by this charter:**
- `IRA-C132` remains **🟡 AMBER — Ready for Technical Design preparation** — unaffected by this charter, which addresses chartering sufficiency only.
- `ROD-C132` RO Decisions 1, 2, 3, 3a remain exactly as recorded — none reopened, altered, or reinterpreted.
- The service-hosting (`AuthService`) and write-fan-in (Option 2) decisions remain exactly as recorded in `TDS-C132 §6.4`/§6.5 — none reopened.
- `C-131` remains unchartered; `C-133` remains **Planned**, not Active.
- `SD-003-226`'s full interruption-ceiling/digest regime remains deferred, not implemented.
- `C-023`/`WP-17`, `WP-18`, `C-040`, `C-114`, `AI-002`/Sarika remain untouched — no dependency on any of them was found or asserted at any point in this governance cycle.
- `DS-001`, `PE-001`, `CAP-001`, `SER-001` remain unmodified.

**Final state, per direct instruction:** ~~**BA CHARTERED. IMPLEMENTATION NOT YET AUTHORIZED, NOT YET COMPLETE. NOT CERTIFIED.** Implementation has not started; no `CLAUDE.md §19.7b` gate has been dispatched. The next step is a separate, explicit Repository Owner **IMPLEMENTATION AUTHORIZATION** for C-132 BA-01 — not performed by this charter.~~ *(Superseded through 2026-09-09 — see the Change Control entries below.)* **BA CHARTERED. IMPLEMENTATION AUTHORIZED (RO, 2026-09-06, `IMP-REPORT-WP-19 §1`). IMPLEMENTATION COMPLETE. `CLAUDE.md §19.7b` GATE 1 PASSED** (original review FAIL on finding F-1 — HIGH tenant-isolation — → F-1 remediated → fresh independent Gate 1 re-review PASS; `CERT-WP-19`; `IMP-REPORT-WP-19 §12/§13/§14`; original FAIL preserved as historical fact) **— GATE 2 V&V PASSED** (fresh independent audit, 2026-09-08; `IMP-REPORT-WP-19 §15` — 24/0/0 RTM, 0 material findings, 8 non-material observations) **— GATES 3/4 NOT TRIGGERED** (no material defect requiring remediation) **— GATE 5 RELEASE READINESS PASSED** (fresh independent audit, 2026-09-09; `IMP-REPORT-WP-19 §16` — 0 material findings, release isolation CLEAN, explicit 19-path release allowlist). **BA-01 FORMALLY CLOSED — CERTIFIED — RELEASE-READY** (2026-09-09, `IMP-REPORT-WP-19 §17`; all five `CLAUDE.md §19.7b` gates complete; governance-recording complete; **repository commit outstanding — a separate, explicitly-authorized action**, mirroring `WP-16`/`WP-17`/`WP-18`). **This closure applies to WP-19 / C-132 BA-01 only — it does NOT close C-132 as a capability.** C-132 capability-wide remains **🟡 AMBER** (`IRA-C132`, unchanged; not reclassified; no capability-wide C-132 completion claim; all deferred C-132 scope remains deferred). The next step, if desired, is a separate explicit Repository Owner authorization for an explicit-path WP-19 commit using the verified 19-path allowlist (`IMP-REPORT-WP-19 §17.4`).

---

## Change Control

**Files created:** this document — `architecture/05-Implementation/WP-19_C132_BA-01_Establish_Manage_Enterprise_Notification_Context_Business_Activity_Charter.md`.
**Files modified:** `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md` — one new `WP-19` row added to §2, per `WPR-001 §3`'s own Maintenance Rule (b) ("a row is added to §2 only when... a Work Package... has an accepted IRA assigning it a specific capability" — `IRA-C132` was formally accepted at 🟡 AMBER, satisfying this condition exactly as `IRA-C023`'s own 🔴 RED acceptance satisfied it for `WP-17`), mirroring the identical addition pattern `WP-15`/`WP-16`/`WP-17` each already established. No other row in `WPR-001` was altered.
**Files read for cross-reference, not modified:** `ROD-C132-Enterprise-Notifications-Capability-Boundary-and-Minimum-Scope.md`, `IRA-C132_Enterprise_Notifications_Implementation_Readiness_Assessment.md`, `TDS-C132_Enterprise_Notifications_Minimum_BA_Technical_Design.md`, `CAP-001`, `SD-003`, `DS-001` (Chapter 21), `CLAUDE.md §8/§18/§19/§20/§21.4`, `CMD-001 §26.3a`, `WP-17_C023_BA-01_Establish_Entitlement_License_Context_Business_Activity_Charter.md` (structural precedent), `WP-REG-001_Enterprise_Work_Package_Register.md` (next-WP-number verification).
**Not modified:** production code, schema, migrations, frontend, `SD-003`, `DS-001`, `PE-001`, `CAP-001`, `SER-001`, `ROD-C132`, `IRA-C132`, `TDS-C132`, any C-023/WP-17, WP-18, C-040, C-114, or AI-002/Sarika artifact, `WP-REG-001` (execution-status register — not updated at chartering time, mirroring `WP-17`'s own identical precedent of updating only `WPR-001` at this stage), any unrelated ADR, any unrelated certified WP artifact. Nothing was staged, committed, or pushed.

---

**Gate 1 PASS recording pass — 2026-09-07, per direct Repository Owner authorization ("RECORD GATE 1 PASS — WP-19 / C-132 BA-01 — DOCUMENTATION-ONLY GOVERNANCE PASS").** Documentation-only. Between chartering and this pass: the Repository Owner granted Implementation Authorization for WP-19 / BA-01 (`IMP-REPORT-WP-19 §1`); implementation was completed within this charter's scope (§2, §19); a fresh independent `CLAUDE.md §19.7b` Gate 1 review returned **❌ FAIL** on finding **F-1** (a HIGH-severity tenant-isolation defect — `POST /notifications` did not bind the authenticated caller to `X-Tenant-ID`); F-1 was remediated by the implementing session under a dedicated RO remediation authorization (`IMP-REPORT-WP-19 §13`) using the pre-existing `require_matching_tenant_or_platform_admin` dependency (the WP-10 / `CERT-WP-10` Finding B-1 precedent — no new authorization mechanism); a **fresh, independent Gate 1 re-review** (a reviewer uninvolved in the implementation, the first Gate 1 review, or the F-1 remediation) then returned **✅ PASS** (2026-09-06), with a working negative control against a reconstructed pre-fix build, 25/25 WP-19 tests, 901/901 full AuthService regression, single Alembic head `d4e5f6a7b8c9`, clean frontend `tsc`/`eslint`/`next build`, and zero material findings. Reconciled in this charter, strikethrough-preserve, nothing erased: the header **Status** line and the **Final state, per direct instruction** line. **Strictly scoped:** no implementation code, migration, model, repository, service, router, schema, test, or frontend file was modified; no `TDS-C132` architecture change; no change to this charter's scope (§2, §19), technical requirements, or Repository Owner Decisions summary (§22); no `IRA-C132` classification change (C-132 remains **🟡 AMBER**); no `CAP-001` / delivery-map / `SD-003` / C-023 / WP-17 / WP-18 change. This pass records **Gate 1 only** — **Gate 2 (V&V Audit), Gates 3–4, and Gate 5 (Release Readiness) have NOT been run**; WP-19 is **NOT certified**; formal closure is **NOT complete**. The original Gate 1 FAIL is preserved as historical fact (`CERT-WP-19`; `IMP-REPORT-WP-19 §12`) and is not rewritten. Companion 2026-09-07 recording reconciliations in the same pass: `CERT-WP-19_Establish_Manage_Enterprise_Notification_Context.md` (created — the Gate 1 certification record of record); `IMP-REPORT-WP-19` (status line + new `§14`); the `WPR-001` WP-19 row + Gate column + a new maintenance note. Nothing was staged, committed, or pushed. Gate 2 was NOT dispatched.

**Gate 2 V&V PASS recording pass — 2026-09-08, per direct Repository Owner authorization ("REPOSITORY OWNER AUTHORIZATION — WP-19 / C-132 BA-01 — RECORD INDEPENDENT GATE 2 V&V PASS — DOCUMENTATION ONLY").** Documentation-only. A fresh-context independent `CLAUDE.md §19.7b` **Gate 2 Verification & Validation Audit** — performed by a reviewer with **no** involvement in the WP-19 implementation, the original Gate 1 review, the F-1 remediation, the fresh Gate 1 re-review, or the Gate 1 PASS recording — **returned ✅ V&V PASS** (2026-09-08): an independent Requirements Traceability Matrix of every material `TDS-C132` / charter requirement (**24 PASS / 0 PARTIAL / 0 FAIL**), **0 material findings**, **8 non-material observations (O1–O8)** recorded as Gate 5 inputs, a from-scratch F-1 **negative control** reproducing the pre-fix defect (HTTP 201 + persisted cross-tenant Notification visible to the victim) and confirming closure (HTTP 403, zero rows), the caller-vs-header binding + PLATFORM_ADMIN positive/negative controls re-verified, an exhaustive tenant-isolation matrix, field-by-field schema/model/migration conformance to `TDS-C132 §6.6`, single non-branching Alembic head `d4e5f6a7b8c9` with additive-only offline PostgreSQL upgrade/downgrade DDL, the 200-row list cap verified, and independent re-execution of 25/25 targeted + 901/901 regression + 40/40 probes + clean frontend `tsc`/`eslint`/`next build`. **Gate 3 and Gate 4 were NOT TRIGGERED** — no material defect requiring remediation. Reconciled in this charter, strikethrough-preserve, nothing erased: the header **Status** line and the **Final state, per direct instruction** line. **Strictly scoped:** no implementation code, migration, model, repository, service, router, schema, test, middleware, dependency, or frontend file was modified — the implementation that passed Gate 2 remains byte-untouched; no change to this charter's scope (§2, §19), technical requirements, or Repository Owner Decisions summary (§22); no `IRA-C132` classification change (C-132 remains **🟡 AMBER**; no capability-wide C-132 completion claim); no `ROD-C132` decision change; no `TDS-C132` architecture change; no `CAP-001` / `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md` / `SD-003` / `SER-001` / `DS-001` / `PE-001` / C-023 / WP-17 / WP-18 change. **No non-material observation (O1–O8) was remediated; `SER-001` `SE-018` was NOT reclassified; no broad governance reconciliation was performed** — O1–O8 are recorded as Gate 5 reconciliation inputs only. **The Gate 2 V&V result of record is `IMP-REPORT-WP-19 §15`; `CERT-WP-19` remains the Gate 1 record of record.** **Gate 5 (Release Readiness Audit) has NOT been run** and remains PENDING, awaiting a separate Repository Owner authorization and a further fresh-context reviewer. WP-19 is **NOT closed, NOT certified, NOT release-ready**. The original Gate 1 FAIL and the full Gate 1 sequence remain preserved as historical fact. Companion 2026-09-08 recording reconciliations in the same pass: `IMP-REPORT-WP-19` (status line + new `§15`); the `WPR-001` WP-19 row + Gate column + a new maintenance note; `CERT-WP-19` (a "Gate 2 subsequently PASSED" pointer in its CURRENT CERTIFICATION STATE banner and its Recommendation-for-Gate-2 section). Nothing was staged, committed, or pushed. Gate 5 was NOT dispatched; Gates 3/4 were NOT performed.

---

~~*End of WP-19 / BA-01 Charter (chartered — implementation authorized, implementation complete, `CLAUDE.md §19.7b` Gate 1 PASSED; Gates 2–5 not run; not certified; formal closure not complete).*~~ *(Superseded 2026-09-08.)*

~~*End of WP-19 / BA-01 Charter (chartered — implementation authorized, implementation complete, `CLAUDE.md §19.7b` Gate 1 PASSED, Gate 2 V&V PASSED; Gates 3/4 NOT TRIGGERED; Gate 5 Release Readiness PENDING / NOT RUN; NOT certified; formal closure NOT complete; release readiness NOT established; C-132 remains 🟡 AMBER).*~~ *(Superseded 2026-09-09.)*

**Gate 5 recording + formal-closure pass — 2026-09-09, per direct Repository Owner authorization ("REPOSITORY OWNER AUTHORIZATION — WP-19 / C-132 BA-01 — GATE 5 RECORDING + FORMAL WP-19 CLOSURE — DOCUMENTATION / GOVERNANCE ONLY — NO COMMIT / NO PUSH").** Documentation-only. A fresh-context independent `CLAUDE.md §19.7b` **Gate 5 Release Readiness Audit** — by a reviewer with **no** involvement in the WP-19 implementation, the original Gate 1 review, the F-1 remediation, the fresh Gate 1 re-review, the Gate 1 PASS recording, the Gate 2 V&V audit, or the Gate 2 PASS recording — **returned ✅ PASS** (2026-09-09): 0 material findings; release isolation CLEAN; an explicit 19-path WP-19 release allowlist produced and verified; independent re-run of 25/25 targeted + 901/901 regression, single Alembic head `d4e5f6a7b8c9` with offline PostgreSQL upgrade/downgrade DDL verified additive-only, clean frontend `tsc`/`eslint`/`next build`; a from-scratch F-1 probe + negative control 11/11 (pre-fix reconstruction reproduced the defect; fixed code → 403, zero rows) and a from-scratch E2E + list-cap + CHECK/FK probe 21/21; the four status-of-record documents confirmed mutually consistent; the original Gate 1 FAIL confirmed preserved verbatim; no Repository Owner decision required. **Gate 3 and Gate 4 remain NOT TRIGGERED.** Following that PASS, **WP-19 / C-132 BA-01 is FORMALLY CLOSED — CERTIFIED — RELEASE-READY** (`IMP-REPORT-WP-19 §17`; repository commit outstanding — a separate, explicitly-authorized action, mirroring `WP-16`/`WP-17`/`WP-18`). Reconciled in this charter, strikethrough-preserve, nothing erased: the header **Status** line and the **Final state, per direct instruction** line. **Strictly scoped:** no implementation code, migration, model, repository, schema, service, router, test, middleware, dependency, or frontend file was modified — the implementation that passed all five gates remains byte-untouched; no change to this charter's scope (§2, §19), technical requirements, or Repository Owner Decisions summary (§22); no `IRA-C132` classification change (C-132 remains **🟡 AMBER**; no capability-wide C-132 completion claim; all deferred C-132 scope remains deferred); no `ROD-C132` / `TDS-C132` / `CAP-001` / `SD-003` / `DS-001` / `PE-001` / C-023 / WP-17 / WP-18 change. **This closure applies to WP-19 / C-132 BA-01 only; it does NOT close C-132 as a capability.** The two Gate 2 closure reconciliations were performed additively, C-132/WP-19-content only, under existing authority: **O1** — `SER-001` `SE-018` reclassified **Deferred → Partially Implemented**, authorized by the accepted `IRA-C132 §5` Strategic Enhancement Disposition (`SE-018` row only; the unrelated `SE-052` / C-040 pending hunk NOT touched); a Strategic Enhancement Review recorded at `IMP-REPORT-WP-19 §17.3a`. **O2** — the `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md` C-132 row + D-007 summary mention reconciled to the actual closed state (C-132 content only; the unrelated WP-16/WP-17/C-040 hunks NOT touched). **O3–O8** preserved as historical Gate 5 findings. Companion 2026-09-09 reconciliations in the same pass: `IMP-REPORT-WP-19` (status line + `§16`/`§17`/`§17.3a`); `CERT-WP-19` (banner + closing line); the `WPR-001` WP-19 row + Gate column + a new maintenance note; `SER-001` (`SE-018` row only); `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md` (C-132 row + D-007 summary mention only). Nothing was staged, committed, or pushed. No further gate dispatched. `git reset` / `clean` / `stash` / `checkout --` / `restore` not used. The eventual WP-19 repository commit will use the explicit 19-path allowlist at `IMP-REPORT-WP-19 §17.4` under a separate Repository Owner authorization; `git add -A` / `git add .` remain prohibited (`CLAUDE.md §21.5`).

---

*End of WP-19 / BA-01 Charter (chartered — implementation authorized, implementation complete, `CLAUDE.md §19.7b` Gate 1 PASSED, Gate 2 V&V PASSED; Gates 3/4 NOT TRIGGERED; Gate 5 Release Readiness PASSED; **WP-19 / C-132 BA-01 FORMALLY CLOSED — CERTIFIED — RELEASE-READY**, repository commit outstanding; closure applies to WP-19 / BA-01 only; C-132 capability-wide remains 🟡 AMBER, all deferred C-132 scope remains deferred; the original Gate 1 FAIL is preserved as historical fact).*
