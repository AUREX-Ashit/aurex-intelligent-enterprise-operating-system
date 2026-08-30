# WP-16 — BA-01 (C-040 Tenant Administration) — Tenant Establishment — Business Activity Charter

**Work Package:** WP-16 — the next unclaimed Work Package number (`WP-15` = C-066, closed; `WP-16` named only in negative statements — "not created, not authorized" — throughout every prior C-040 governance artifact, `ROD-C040-Blocker-Closure-Assessment.md §14`, `CAP-001` v1.6 changelog — until this charter).
**Business Activity:** BA-01 — Tenant Establishment (Business Approval → Infrastructure Allocation)
**Capability:** C-040 Tenant Administration (`CAP-001` line 80, Domain D-003 Enterprise Administration, Primary Specification `SD-002`, Active)
**Status:** ~~**CHARTERED (retroactive) — BA-01 IMPLEMENTATION COMPLETE (pre-charter) — NOT YET CERTIFIED.**~~ *(Historical, drafting-time statement, preserved per this repository's own no-silent-fix discipline — accurate on 2026-08-26, before Gates 1/2/5 had run.)* **CLOSED — CERTIFIED (governance-recording complete; repository commit outstanding) — see "BA-01 — Closure" below.** This charter formalizes the already-accepted `IRA-C040` (Parts I–III, GREEN — Implementation Ready), the already-independently-reviewed `TDS-016`/`TDS-017`, and the already-*completed* implementation into the charter-level structure this repository's own precedent (`WP-14 BA-04`, `WP-15 BA-01`) established — with one deliberate structural difference from both precedents, disclosed in full at §24: implementation occurred **before** this charter and before WP-16 existed as a registered number, not after.
**Prepared under:** direct Repository Owner instruction ("C-040 — Execute Post-GREEN Transition: Formally Accept IRA + Charter WP-16"), 2026-08-26.

**A note on document type, disclosed rather than assumed (mirrors `WP-14 BA-04`'s and `WP-15 BA-01`'s own identical disclosure):** this repository's own established convention charters at the Work Package level, with per-Business-Activity charter detail specified inside the governing IRA. `WP-14 BA-04` and `WP-15 BA-01` each departed from that convention, per direct Repository Owner instruction, establishing a Business-Activity-level charter as real, repeated repository precedent. This document follows that same shape, again per direct instruction.

**Governing basis for BA-01, stated explicitly:** `CAP-001` (C-040 registration) → `SD-002 §2`/`§13` → `ADR-024`–`ADR-035` → `AI-001`/`AI-002`/`AI-003` → `ROD-C040-Blocker-Closure-Assessment.md` (blocker-closure planning) → `IRA-C040` Parts I–III (Part III: **GREEN — Implementation Ready**, accepted by this charter, §20 below) → `TDS-016` (`tenant_registry` remediation, independently reviewed) → `TDS-017` (Authority Runtime Enforcement, independently reviewed) → the completed implementation itself (§24).

---

## Classification Key

Mirrors `WP-15 BA-01`'s own key exactly:
- **A** — already determined by governing documents
- **B** — determined by repository precedent
- **C** — an implementation detail
- **D** — requires a Repository Owner decision, genuinely open
- **D → RESOLVED** — was **D**, now resolved by a recorded decision

---

## 1. Business Activity Identity — [A]

BA-01, WP-16, Capability C-040 Tenant Administration (`CAP-001` D-003, Active). Governed physical Business Object: `tenant_registry` (new table, `TDS-016 §5`) plus `organizations.tenant_id` (new column, `TDS-016 §5`/`§7`). Write path — creates exactly one `tenant_registry` row and populates exactly one `organizations.tenant_id` value, atomically, per Organization, exactly once.

## 2. Business Intent — [A]

Verbatim basis, `IRA-C040` Part I §3.2: *"the Enterprise Experience through which the enterprise establishes... the administrative standing of a Tenant — the infrastructure/data-isolation partition underlying an already-valid Organization."* BA-01 realizes only the narrowest slice of this: the first, foundational Commit (`ERB-C040-05`, `EX-C040-11`) that brings a Tenant into existence for an already-valid Organization, per the dual-authority process (`ADR-026`, `ADR-029`).

## 3. Trigger — [A]

Caller-invoked (`POST /tenants`), executed by the Infrastructure Allocation Authority's own currently-appointed accountability point (`AI-002`), per `TDS-016 §8` step 1/point 3 ("decision/execution split").

## 4. Actor / Persona — [A]

Not an ordinary Persona in the `PE-001` Chapter 12 sense — the sole caller is the platform-wide, pre-Organization `AI-002` (Infrastructure Allocation Authority) accountability point, gated by `require_ai002_holder` (`TDS-017`, live `authority_holders` lookup, no `PLATFORM_ADMIN`/`AUREX_ADMIN` substitution). `AI-001` (Business Approval Authority) participates as a required, live-looked-up co-attribution, not as caller.

## 5. Preconditions — [A]

- The target Organization (`organizations` row) must already exist (`ADR-024 §1.7`, "Organization before Tenant").
- `organizations.tenant_id IS NULL` for that Organization — the idempotency guard (`TDS-016 §8` step 3).
- A currently-appointed `AI-001` accountability point must exist (live `authority_holders` lookup) — if none exists, the transaction is rejected 409 (`services/tenant_establishment_service.py`).

## 6. Input Contract — [A]

`POST /tenants` — `organization_id` (UUID, request body). Both actor attributions (`approved_by_actor_id`, `allocated_by_actor_id`) are server-derived from live `authority_holders` lookups and the caller's own verified claims — never caller-supplied (`schemas/tenant_establishment.py`).

## 7. Business Rules — [A]

- Exactly one `tenant_registry` row may ever exist per Organization (`ADR-025` 1:1 cardinality; `TDS-016 §6` invariant 1).
- The Establishment transaction is atomic — the `tenant_registry` INSERT and the `organizations.tenant_id` UPDATE commit together or not at all (`TDS-016 §8`/`§9`).
- A duplicate/replayed Establishment request for an already-established Organization is rejected 409, never silently accepted or overwritten (`TDS-016 §9`).
- `tenant_id` becomes non-NULL only at Establishment commit — never inferred, never defaulted, and remains nullable at the schema level (Delivery Map Decision 1, 2026-08-26; `TDS-016 §7`).

## 8. Persistence Target — [A]

`tenant_registry` (new table) and `organizations.tenant_id` (new column), both in `AuthService` — the sole real, migrated owner of Organization data (`ADR-003`). `Backend/Services/TenantService` (a separate, fully-mocked scaffold) is untouched, per `ADR-003`'s own explicit disposition — not extended, not adopted, not deleted.

## 9. State / Lifecycle Transition — [A]

`(none) → PROVISIONED` only (`TDS-016 §10`, the corrected four-state model). BA-01 never produces `MIGRATING`, `OFFBOARDING`, or `OFFBOARDED` — those transitions, and the approval authorities that would trigger them, remain explicitly out of scope (§19 below).

## 10. Authorization — [A]

`require_ai002_holder` (`TDS-017`, unmodified) — a live database lookup of the currently-ACTIVE `authority_holders` row for `AI-002`, compared against the caller's own `person_id` claim. No `PLATFORM_ADMIN`/`AUREX_ADMIN` bypass exists or is permitted (`ADR-029 §10`/`§11`'s own prohibition, independently tested — `test_role_claim_does_not_substitute_for_ai002_holder`).

## 11. Tenant Boundary — [A]

Not applicable in the usual `organization_id`-scoping sense — this Business Activity *creates* the Tenant boundary rather than operating inside one. The caller is platform-wide/pre-Organization by design (`TDS-017`); `POST /tenants` is exempted from `TenantMiddleware`'s `X-Tenant-ID` requirement, purely additively (`middleware/tenant.py`, one new exemption line, mirroring `/auth/authority-login`'s own precedent) — `X-Tenant-ID`'s existing meaning for every other endpoint is unchanged (`TD-158`, preserved).

## 12. Events / Outcomes — [A]

`record_audit("ESTABLISH_TENANT", ...)` and `publish_event("TENANT_ESTABLISHED", ...)`, per this repository's own established `observability.py` convention (`SD-002-054`), mirroring `organization_service.py`'s own `establish()`/`activate_establishment()` precedent exactly.

## 13. Error / Rejection Conditions — [A]

- Caller not the live `AI-002` holder → 403.
- Organization not found → 404.
- Organization already has an established Tenant → 409.
- No currently-appointed `AI-001` accountability point exists → 409.
- Concurrent establishment race (lost the conditional-UPDATE) → 409, full rollback including the `tenant_registry` INSERT.
- Success → 201, `TenantResponse`.

## 14. Idempotency Expectations — [A]

A second Establishment request for an already-established Organization is a safe no-op from the caller's perspective (rejected 409, no duplicate row, no data corruption) — `TDS-016 §9`, independently tested (`test_duplicate_establishment_rejected`, `test_rejected_establishment_leaves_no_orphaned_tenant_row`).

## 15. Audit / Observability Expectations — [A]

Both actor attributions (`approved_by_actor_id`/`approved_at`, `allocated_by_actor_id`/`allocated_at`) are written in the same atomic transaction (`SD-002-056`, "no approval exists without an audit record"), plus `record_audit`/`publish_event` per §12.

## 16. Dependencies — [A]

`AuthService.Organization` (pre-existing, `ADR-003`), `authority_holders`/`require_ai002_holder` (pre-existing, `TDS-017`, this session), `ADR-025`/`ADR-029`/`ADR-034` (pre-existing decisions). No dependency on any unchartered capability.

## 17. Acceptance Criteria — [A]

`POST /tenants` establishes exactly one Tenant per Organization, atomically, attributable to both currently-appointed authorities, rejecting every duplicate/unauthorized/missing-authority/missing-organization case with the correct status code — independently verified this session, 13 dedicated tests (§18), all passing.

## 18. Test Obligations — [A, SATISFIED]

`tests/test_tenant_establishment.py` — 13 tests covering the Repository Owner's own minimum list (successful establishment; missing-Authorization rejection; `AI-001`-unpopulated rejection; `PLATFORM_ADMIN`/`AUREX_ADMIN` non-substitution; duplicate/replay rejection; atomic-rollback/no-orphan verification; Tenant↔Organization 1:1 invariant across two Organizations; lifecycle correctness; `AI-002`-unpopulated rejection; existing `/organizations` read path unaffected; existing `X-Tenant-ID` semantics unaffected elsewhere; unknown-Organization rejection). `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist satisfied via the two-Organization invariant test. Full `AuthService` regression: **823/823 passing** (810 pre-existing + 13 new), independently re-run twice this session (once during implementation, once during the Part III reassessment), zero regressions.

## 19. Out-of-Scope Boundaries — [A]

- Technical Provisioning Authority (`ADR-026 §13`) — entirely undecided, not designed or implemented.
- Tenant migration, offboarding, and cross-tenant-sharing approval authority — the `MIGRATING`/`OFFBOARDING`/`OFFBOARDED` lifecycle *state shapes* are named canonically (`PE-001-C040 §5.5`) but no triggering authority or transaction exists.
- Any future executor-relationship design beyond the disclosed v1 direct-execution choice (`ROD-C040-Blocker-Closure-Assessment.md §3` item 8).
- CBOR registration for Tenant as a Canonical Business Object — preliminarily ELIGIBLE (`TDS-016 §13`), registration itself not performed; a downstream WP-16 closure activity, not a chartering prerequisite (§25).
- `AI-002` accountability-point population, any further Key-2 case, `AI-004` — explicitly not touched by this charter (§26).
- `Backend/Services/TenantService` — untouched (`ADR-003`).
- Frontend / Enterprise Experience — **open**, not resolved by any existing decision (§21).

## 20. Implementation Readiness Classification — IRA Acceptance

**`IRA-C040` (Parts I, II, III) is hereby formally ACCEPTED.** Result: **🟢 GREEN — Implementation Ready**, scoped to this Business Activity (Tenant Establishment, Business Approval → Infrastructure Allocation) exclusively. Acceptance is a governance act recognizing the assessment's own conclusion — it does not retroactively alter Part I's RED finding (2026-08-25, accurate at the time, superseded by Part II) or Part II's AMBER finding (accurate at the time, superseded by Part III), both of which remain the historical record, preserved verbatim, per this repository's own no-silent-fix discipline. Six of seven readiness gates PASS; Domain remains Conditional Pass pending CBOR registration (§25), disclosed and non-blocking.

## 21. Enterprise Experience Scope Decision — `CLAUDE.md §20.3` [D → RESOLVED, `RO-DEC-C040-BA01-01`]

**RESOLVED, Option A: Backend-only.** Per `RO-DEC-C040-BA01-01`, direct Repository Owner instruction ("C-040 / WP-16 — Resolve Enterprise Experience Scope Decision," 2026-08-26): **BA-01 (Tenant Establishment) is backend-only**, the disclosed exception `CLAUDE.md §20.3` permits — mirroring `WP-15 BA-01`'s own `RO-DEC-C066-BA01-02` and `WP-14 BA-05`'s own precedent for the identical exception, and consistent with §4 above's own independent finding that BA-01 has no ordinary Persona caller at all (its sole caller is the platform-wide `AI-002` accountability point).

**No frontend/UI implementation is required for WP-16 Independent Certification, V&V Audit, Release Readiness Audit, or closure.** `POST /tenants` (backend only, already implemented and tested — §17/§18/§24) satisfies BA-01's own Vertical Slice Requirement in full under this Option A exception.

**Scope of this decision, stated explicitly per the governing instruction:**
- Applies **only** to BA-01/WP-16's own current chartered scope (Tenant Establishment: Business Approval → Infrastructure Allocation). It is a scope decision for this Business Activity, not a constitutional prohibition on Enterprise Experience for C-040 generally.
- Does **not** mean C-040 can never have a frontend, that Tenant Administration UI is prohibited, that future Enterprise Experience work is cancelled, or that future Tenant Administration screens cannot be created. A future, separately-chartered Business Activity (e.g., an Understand/Observe Tenant Standing screen, once a real interface for `AI-001`/`AI-002` accountability points is needed) remains fully possible and is not foreclosed by this decision.
- Does **not** expand BA-01's own scope (§19) — Technical Provisioning, migration, offboarding, and cross-tenant sharing remain excluded, unaffected by this decision.
- Does **not** alter `IRA-C040`'s own GREEN — Implementation Ready classification (Part III), which this decision neither depends on nor modifies.

This is the sole `D` item this charter identified (§20/§22); with `RO-DEC-C040-BA01-01` now recorded, no open Repository Owner decision remains blocking WP-16's own path to Certification.

## 22. Repository Owner Decisions Recorded (summary — full text: `ROD-C040-Blocker-Closure-Assessment.md`, `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`, `ADR-024`–`ADR-035`, `AI-001`–`AI-003`)

| Decision | Disposition |
|---|---|
| Tenant–Organization cardinality | RESOLVED — 1:1 (`ADR-025`) |
| `tenant_registry` as system-of-record implementation candidate | RESOLVED (`ADR-034`, conditional on `§7` remediation — performed, `TDS-016`) |
| `tenant_id` NULL semantics | RESOLVED, 2026-08-26 — NULL means Establishment not yet completed, never that the Organization is its own Tenant; the obsolete `Master_Technical_Architecture.md` schema comment is not authoritative (Delivery Map Decision 1) |
| Existing `X-Tenant-ID`/`TenantMiddleware` compatibility | RESOLVED, 2026-08-26 — preserved unchanged as a legacy Organization-scoped surface, `TD-158` (Delivery Map Decision 2) |
| Business Approval Authority (`AI-001`) architectural model / identity | RESOLVED (`ADR-029 §10`, `AI-001`, `AI-003` — Ashit Padhi appointed) |
| Infrastructure Allocation Authority (`AI-002`) architectural model / identity | RESOLVED at the constitutional level (`ADR-029 §11`, `AI-002`); accountability point **unpopulated** — `TD-157` (§26) |
| Business Governance Authority minimum membership structure | RESOLVED (`ADR-035`) |
| Two-Key/per-case Key-2 appointment mechanism | RESOLVED, twice-proven (`ADR-030`–`033`, `AI-001`, `AI-003`) |
| BA-01 minimum scope ("Tenant Establishment only") | RESOLVED, 2026-08-26 (Delivery Map) |
| Enterprise Experience/frontend scope for BA-01 | RESOLVED, 2026-08-26 — Option A, Backend-only (`RO-DEC-C040-BA01-01`, §21) |

---

## 23. Retroactive Governance Reviews — `CLAUDE.md §21.3`

Performed for this charter, per §21.3's Standard Work Package Lifecycle (Release → Work Package (Charter + IRA) → SER-001 Review → Historical Screen Review → Executive Cognition Review → Business Activity → ...), retroactively, since WP-16 did not exist when `IRA-C040`/`TDS-016`/`TDS-017` were drafted or implemented (§24 discloses this sequencing explicitly).

### 23a. SER-001 Strategic Enhancement Review

Direct search of `SER-001_Strategic_Enhancement_Register.md`: **zero entries reference C-040 or Tenant Administration.** (One incidental match, `SE-051`, uses "tenant" only as a generic adjective in "tenant/category-configurable" retention-policy language — unrelated to C-040.) **Classification: Not Applicable — no relevant SER-001 entry found.** No enhancement is Implemented, Partially Implemented, or Deferred by this Business Activity; none required reclassification.

### 23b. Historical Screen Review

Direct search of `HISTORICAL-SCREEN-REALIZATION-MATRIX.md`'s full 14-item classification table: no item maps to Tenant Administration/Tenant Establishment as a distinct concept. The closest adjacent item, `02-registration.html` ("Self-service enterprise onboarding... Tenant creation"), is classified **RETIRE CONCEPT**, tied explicitly to C-004 Organization Management/WP-01 ("the platform's own actual organization-establishment model... is internal-admin-only by governed design") — not to C-040, which by `ADR-024 §1.7`'s own "Organization before Tenant" sequencing is a distinct, later concern. **Classification: No relevant historical screen concept found for C-040.** Nothing is evolved, merged, or retired by this Business Activity.

### 23c. Executive Cognition Review

Per `EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md §3`'s own required worksheet:
- **Which Executive capabilities become available (even partially)?** None. BA-01's sole caller is the platform-wide `AI-002` accountability point (§4), not an Executive Persona in the `PE-001` Chapter 12 sense.
- **Which Executive screens evolve?** None — no frontend exists or is authorized (§21).
- **Which Enterprise Intelligence capabilities become visible?** None — C-040 has no dependency on C-090+.
- **Which Executive workflows become possible?** None new.
- **Deferred:** any future Executive-facing Tenant Administration screen (e.g., understanding/observing Tenant standing) — **Planned Release:** unscheduled/future; **Planned Work Package:** unassigned, contingent on Technical Provisioning/migration/offboarding/sharing being chartered; **Reason for deferral:** BA-01 is establishment-only, minimum chartered scope (§19).

None of these three reviews identified a genuine open decision or blocker beyond §21 (already disclosed, not newly discovered here) — no STOP condition is triggered by this section.

---

## 24. Implementation Status and Sequencing Disclosure

**BA-01 is IMPLEMENTATION COMPLETE.** `tenant_registry`, `organizations.tenant_id`, the atomic Establishment transaction, authorization, audit attribution, duplicate/rollback handling, and 13 dedicated tests all exist, verified directly against the repository (not taken on report) during the Part III reassessment and again in preparing this charter. Full regression: 823/823.

**Disclosed historical sequencing anomaly, not a defect requiring remediation:** unlike `WP-15 BA-01`'s own textbook order (charter → Implementation Authorization → implementation → closure), C-040's own path was: `IRA-C040` drafted (capability-first, no WP number, 2026-08-25) → `TDS-016`/`TDS-017` (technical design, independently reviewed) → explicit Repository Owner Implementation Authorization ("C-040 IMPLEMENTATION AUTHORIZATION") → implementation completed and tested → Part II/Part III readiness reassessments → **this charter, and WP-16's own formal registration, only now.** `ROD-C040-Blocker-Closure-Assessment.md §14` had already anticipated and correctly reasoned that "WP numbering occurs at implementation-authorization time, downstream of readiness closure, not a prerequisite to it" — what was not anticipated is that implementation-authorization and implementation themselves would occur before WP numbering, rather than at the same moment. **This charter does not, and no canonical rule requires it to, undo, re-authorize, or redo any part of the completed implementation.** It formalizes governance recognition of work already correctly authorized and completed, mirroring how `WP-15`'s own charter itself was later corrected in place, non-destructively, when its own registration timing changed (see that charter's own "Registration status correction" preamble) — the same no-silent-fix, no-rewrite discipline is applied here to a larger but structurally identical timing gap.

---

## 25. CBOR Status

Tenant preliminarily passes the `CMD-001 §26.3a` eligibility test (`TDS-016 §13` — independent identity; cross-Business-Activity reference via `EX-C040-15`/Contract 5.3; governed lifecycle). **Formal registration (a registering ADR, mirroring `ADR-006`-class precedent) has not been performed and is not performed by this charter.** Per `WP-04`'s own established precedent (each Business Object registered as part of its own Business Activity's delivery, typically alongside or shortly before Certification), CBOR registration is expected as a downstream WP-16 closure activity — **not a prerequisite to chartering**, consistent with `ROD-C040-Blocker-Closure-Assessment.md §7`'s and this session's own prior post-GREEN transition analysis's identical conclusion.

## 26. `AI-002` / Runtime Authority Holder Status — Disclosed, Not Reopened

Recorded exactly as it currently exists, per explicit instruction:
- `AI-002` (Infrastructure Allocation Authority) — constitutionally established (`ADR-029 §11`); accountability point **unpopulated**.
- `TD-157` — Open — BLOCKED, High severity.
- Fifteen independent Key-2 cases completed across two candidates; the Sarika Rath evidentiary path is concluded and **permanently frozen**.
- No `AI-004` exists.
- `AI-001`'s own runtime `authority_holders` record is also unpopulated (no legitimate `Person` record exists for Ashit Padhi; none fabricated).

**None of this is reopened, modified, or acted upon by this charter.** No candidate search, no Key-2 case, no `AI-004`, no `Person`/`Identity` fabrication, no `authority_holders` row is created here. Per `IRA-C040` Part III §32/§33 (already established, restated not re-derived): this is a Category-C data/environment-readiness finding — it blocks *live production execution* of BA-01, not this charter's own act of chartering, and not `IRA-C040`'s own GREEN classification.

---

## Final Determinations

BA-01's full governing chain — `CAP-001` → `SD-002` → `ADR-024`–`035` → `AI-001`–`003` → `IRA-C040` (accepted, GREEN) → `TDS-016`/`TDS-017` (independently reviewed) → completed, tested implementation (823/823) → `RO-DEC-C040-BA01-01` (Enterprise Experience scope, resolved Backend-only) → Gates 1/2/5 (all PASS, below) — is now complete and internally consistent, independently re-verified in preparing this charter and each of its amendments. No new architecture, business rule, entity, table, API contract element, or authorization mechanism is introduced by this charter beyond what already exists. **No genuinely open Repository Owner decision remains for BA-01's own chartered scope** — §21's own item, the only `D` this charter ever identified, is `D → RESOLVED`.

**This charter does NOT itself:** perform CBOR registration (§25); populate, modify, or reopen `AI-001`/`AI-002` (§26); commit or push anything; or expand BA-01 beyond §19's own boundaries.

**Governance state, as of this closure:** ~~C-040 moves from unchartered to WP-16 — CHARTERED (retroactive). BA-01 is IMPLEMENTATION COMPLETE. It is explicitly not CERTIFIED and not CLOSED — Independent Certification (Gate 1), the mandatory V&V Audit (Gate 2), and the Release Readiness Audit (Gate 5) each remain distinct, future, independently-gated actions, each requiring a fresh-context reviewer per `CLAUDE.md §19.7`'s self-certification prohibition, exactly as every prior Work Package in this repository's own history required.~~ *(Historical, drafting-time statement, preserved per this repository's own no-silent-fix discipline — accurate on 2026-08-26, before Gates 1/2/5 had run. Superseded — see "BA-01 — Closure" immediately below.)*

---

## BA-01 — Closure

**Recorded 2026-08-26, per direct Repository Owner instruction ("C-040 / WP-16 — FORMAL CLOSURE").** This entry is the formal closure record for BA-01/WP-16, mirroring the precedent `WP-15 BA-01`'s own charter established (its own "BA-01 — Implementation Authorization" trailer section, later followed by its `IMP-REPORT-WP-15`'s own closure decision). **It records that all five `CLAUDE.md §19.7b` gates are complete and that WP-16 is closed at the governance-documentation level; it does not itself perform, and is not a substitute for, the separate git-commit action that would finalize this closure in repository history.**

**Closure basis:**
1. Gate 1 — Independent Certification: **PASS WITH OBSERVATIONS** (`CERT-WP-16_Tenant_Establishment.md`).
2. Gate 2 — V&V Audit: **PASS WITH CONDITIONS** (`VV-AUDIT-WP-16_Tenant_Establishment.md`), including four from-scratch runtime probes per `CLAUDE.md §19.7b`'s own method requirement.
3. Gates 3/4 — Remediation / Independent Verification of Remediation: **not triggered** — no defect requiring remediation was found by either gate.
4. Gate 5 — Release Readiness Audit: **PASS** (`RRA-WP-16_Tenant_Establishment_Release_Readiness_Audit.md`) — independently re-verified Gates 1/2 from primary sources, independently re-ran the full suite a third time (823/823, identical), and directly corrected two governance-documentation staleness items (`TD-157`'s "Owning Work Package" field; the Delivery Map's C-040 D-003 line), per this repository's own established Gate 5 precedent. Registered `TD-159`/`TD-160` per `CLAUDE.md §19.8.2`.
5. `IMP-REPORT-WP-16_Tenant_Establishment.md` — the Implementation Report, recording implementation summary, all five gates, Technical Debt, and this same closure decision.

**Decision: BA-01 (Tenant Establishment) is CLOSED — CERTIFIED at the governance-recording level.** All `CLAUDE.md §19.7` Business Activity Completion Gate conditions are satisfied except one: **the accepted implementation has not yet been committed to the repository.** Per this closure task's own explicit change-control boundary, no commit or push was performed as part of this closure recording — that remains a distinct, subsequent action requiring its own explicit Repository Owner authorization.

**Explicit closure-scope boundary, restated per direct instruction:** this closure applies **only** to WP-16/BA-01 (Tenant Establishment: Business Approval → Infrastructure Allocation). It does **not** close, certify, or resolve:
- **C-040 as a whole** — remains `IRA-C040` Part III's own GREEN — Implementation Ready classification, unaffected by this closure.
- **`AI-002`/`TD-157`** — remains constitutionally established, unpopulated, Open — BLOCKED, High severity, Sarika Rath path permanently frozen after 15 cases, no `AI-004`. Not reopened, not touched, not a condition of this closure.
- **Technical Provisioning, migration, offboarding, cross-tenant sharing** — remain future, unchartered scope (§19), unaffected.
- **Future Tenant Administration Enterprise Experience/UI** — remains an open question for any future, separately-chartered Business Activity (§21's own explicit scope limit — `RO-DEC-C040-BA01-01` applies to BA-01 only).
- **CBOR registration for Tenant** — remains genuinely downstream future work (§25), confirmed non-blocking at every gate, not performed by this closure.

**Governance-synchronization performed this pass:** `WPR-001`'s own WP-16 row updated to CLOSED — CERTIFIED (governance-recording), citing all three gate artifacts. `IMP-REPORT-WP-16_Tenant_Establishment.md` created as this Work Package's own Implementation Report, per the same convention every prior closed Work Package in this repository follows.

---

*End of charter. No source code, migration, model, router, service, schema, or test file has been created or modified by this document or by its closure amendment. No ADR, `AI-001`/`AI-002`/`AI-003`, `AI-004`, `TD-157`'s own substantive finding, `TDS-016`, `TDS-017`, `tenant_registry` code, `TenantMiddleware`, or `CBOR-INDEX.md` was modified in preparing this charter or this closure. Nothing was staged, committed, or pushed by this closure. `IRA-C040`, `TDS-016`, `TDS-017`, `ROD-C040-Blocker-Closure-Assessment.md`, `CAP-001`, `SER-001`, `HISTORICAL-SCREEN-REALIZATION-MATRIX.md`, `EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md`, `CERT-WP-16_Tenant_Establishment.md`, `VV-AUDIT-WP-16_Tenant_Establishment.md`, and `RRA-WP-16_Tenant_Establishment_Release_Readiness_Audit.md` were read, not modified, in preparing this closure.*
