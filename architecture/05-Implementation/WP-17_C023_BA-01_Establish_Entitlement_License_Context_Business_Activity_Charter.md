# WP-17 — BA-01 (C-023 Licensing & Entitlement) — Establish Entitlement/License Context (Administrative) — Business Activity Charter

**Work Package:** WP-17 — the next unclaimed Work Package number, verified directly this pass against `WPR-001` (highest Business Capability row: `WP-16`, C-040, CLOSED — CERTIFIED; no `WP-17` row, reference, or reservation exists anywhere in `WPR-001`, `WP-REG-001`, or any other governance register checked this session).
**Business Activity:** BA-01 — Establish Entitlement/License Context (Administrative)
**Capability:** C-023 Licensing & Entitlement (`CAP-001` line 77, Domain D-002 Commercial & Subscription, Primary Specification `URA-001`, Active)
**Status:** **CHARTERED — IMPLEMENTATION NOT YET AUTHORIZED, NOT YET COMPLETE, NOT CERTIFIED.** This charter formalizes the already-accepted `IRA-C023` (RED — Not Implementation Ready, unchanged by this charter), its own six formally-resolved Repository Owner decisions (`§18.13`/`§19.13`/`§20.12`/`§21.12`/`§22.13`/`§23.13`), and the already-independently-reviewed `TDS-C023_Licensing_and_Entitlement_Minimum_BA.md` (twice independently reviewed: once for accuracy, `TDS-C023 §27`; once for chartering sufficiency, verdict **TDS SUFFICIENT FOR BA CHARTERING**) into the charter-level structure this repository's own precedent (`WP-14 BA-04`, `WP-15 BA-01`, `WP-16 BA-01`) established. **Unlike `WP-16`'s own disclosed sequencing anomaly (implementation before charter), this charter follows the normal order — Technical Design → Charter → Implementation Authorization → Implementation — none of the later stages have occurred.**
**Prepared under:** direct Repository Owner instruction ("C-023 — Charter the Minimum-Scope Business Activity"), 2026-08-29, following the TDS's own confirmed chartering-sufficiency verdict.

**A note on document type, disclosed rather than assumed (mirrors `WP-14 BA-04`'s, `WP-15 BA-01`'s, and `WP-16 BA-01`'s own identical disclosure):** this repository's own established convention charters at the Work Package level, with per-Business-Activity charter detail specified inside the governing IRA. `WP-14 BA-04`, `WP-15 BA-01`, and `WP-16 BA-01` each departed from that convention, per direct Repository Owner instruction, establishing a Business-Activity-level charter as real, repeated repository precedent. This document follows that same shape, again per direct instruction.

**Governing basis for BA-01, stated explicitly:** `CAP-001` (C-023 registration) → `URA-001 §8` (`URA-001-105`–`119`, primary domain specification) → `PE-001-C023` v1.1 (Gold-Standard Enterprise Experience specification, Publication Ready) → `IRA-C023` (RED — Not Implementation Ready; §18–§23, six-decision governance cycle, all resolved) → `TDS-C023_Licensing_and_Entitlement_Minimum_BA.md` (Technical Design, twice independently reviewed) → this charter. **No implementation exists at any point in this chain.**

---

## Classification Key

Mirrors `WP-15 BA-01`'s and `WP-16 BA-01`'s own key exactly:
- **A** — already determined by governing documents
- **B** — determined by repository precedent
- **C** — an implementation detail
- **D** — requires a Repository Owner decision, genuinely open
- **D → RESOLVED** — was **D**, now resolved by a recorded decision

---

## 1. Business Activity Identity — [A]

BA-01, WP-17, Capability C-023 Licensing & Entitlement (`CAP-001` D-002, Active). Governed physical Business Object: a new C-023-owned License/Entitlement governance-layer record (working name `entitlement_license_registry`, `TDS-C023 §6.3` item 2 — a design recommendation, not yet built). Write path — establishes exactly one Authoritative Entitlement Context and/or Authoritative License Context per anchor, per the administrative (non-source-hand-off) trigger `PE-001-C023 §4.5`/`EX-C023-04` already defines.

## 2. Business Intent — [A]

Verbatim basis, `CAP-001`: *"Manage entitlements."* Realized, at this BA's own minimum scope, per `PE-001-C023 §1.1`: *"establishes... the authoritative right of an Organization (optionally Domain-scoped) to use a defined capability — an Entitlement — and the authoritative right of a specific Membership to hold a defined user-license type — a License."* BA-01 realizes only the narrowest slice of this — the administrative establish (continuing) outcome of `ERB-C023-01`/`ERB-C023-03`/`ERB-C023-05` (`EX-C023-04`, `EX-C023-11`), per `IRA-C023 §20.12`'s (Decision 2) own Minimum Scope Now authorization.

## 3. Trigger — [A]

Caller-invoked, administrative — no `C-020`/`C-025` source hand-off required (`PE-001-C023 §4.5`'s own conditional trigger: "a business reason to establish one arises, **often from** a newly-received Entitlement Source Reference" — not exclusively). Realizes the `IRA-C023 §21.6`-disclosed severable path, independent of any Subscription or Contract event.

## 4. Actor / Persona — [A]

Narrative Participating Personas per `PE-001-C023 §1.11`/`§3.6`: "Entitlement/License Steward" and "Entitlement/License Decision Participant" — **explicitly disclaimed by `PE-001-C023` itself as not yet resolved authorization roles.** The actual authorization gate is the resolved Commit Authority (`TDS-C023 §7`, Decision 1) — an `approval_authorities` instance, `COMPANY`-scoped, per Organization, per `URA-001-41` (`C-003`/`WP-02`) — **not yet established as a real, populated row for any Organization**, and its own accountability-point binding (`TDS-C023 §7.5`) remains an explicitly undesigned, disclosed open item (§21 below).

## 5. Preconditions — [A]

- The target Organization (`C-004`, `organizations` row) and/or Membership (`C-007`, `memberships` row) must already exist.
- No existing current Authoritative Entitlement Context (per Entitlement Anchor) or Authoritative License Context (per Membership Anchor) already exists for the target anchor — the uniqueness invariant `PE-001-C023 §1.16` itself already states (`INV-C023-09`/`INV-C023-10`, `TDS-C023 §15`).
- A currently-`ACTIVE` `approval_authorities` row for the target Organization, `authority_name = "Entitlement/License Commit Authority"`, must exist and the caller must satisfy its resolved strategy — ~~**this precondition cannot be satisfied by any Organization today**, since no such row has ever been established and the accountability-point binding mechanism (`TDS-C023 §7.5`) is itself undesigned (disclosed, §21)~~ *(reconciled 2026-08-30 — see the reconciliation note at the end of this charter. The **binding mechanism now exists and is certified**: `membership_approval_authority` (a Membership→Approval Authority binding — the canonical mechanism, not the Group route `TDS-C023 §7.5` speculated about) plus `resolve_approval_authority()` / `require_approval_authority()`, delivered by WP-18/`TDS-018`, CLOSED — CERTIFIED — RELEASE-READY. What is still true: **no C-023 `approval_authorities` row and no binding row has yet been established for any Organization** — creating them, via the now-certified `ApprovalAuthorityService.establish()` and `MembershipApprovalAuthorityService.bind()`, is C-023's own implementation work under this BA, not yet authorized.)*
- For an Entitlement establishment specifically: the target Entitlement Type must already be recognized/catalogued — this BA never creates a new global Entitlement Type (`IRA-C023 §21.12`, Decision 3, unchanged).

## 6. Input Contract — [C]

Design-level only, per `TDS-C023 §17.1` — not yet a frozen API contract (no router/schema exists): target Organization and/or Membership reference; Entitlement type (already-recognized only) and/or License type; `effective_from`/`effective_to` (optional, independent business dates, `TDS-C023 §10.1`, never derived from any Subscription date, `§10.2`). **The actual request/response schema is implementation work, not performed by this charter.**

## 7. Business Rules — [A]

- Exactly one current Authoritative Entitlement Context may exist per Entitlement Anchor; exactly one current Authoritative License Context may exist per Membership Anchor (`INV-C023-09`/`-10`, `PE-001-C023 §1.16`).
- An Entitlement Source Reference (Subscription/Contract/administrative grant) is never itself treated as an authoritative Entitlement or License fact — authority arises only through this BA's own governed Commit (`BR-C023-02`, `INV-C023-06`).
- `membership.license_type` (`C-007`, live, unchanged) is referenced by value at establish time and **never written to, duplicated, migrated, deprecated, or redefined** by this Business Activity (`IRA-C023 §18.13`, Decision 6; `TDS-C023 §6.3` item 11 — "the single most important design constraint").
- No Entitlement Consumption, Allocation, or Global Entitlement Type/Feature Catalog entry is created, modified, or governed by this Business Activity (`IRA-C023 §21.12`/`§22.13`, Decisions 3 and 4, both deferred, neither reopened).
- AI assistance remains advisory, explainable, and non-authoritative throughout — never establishes, activates, suspends, or revokes an Entitlement or License (`BR-C023-09`, unchanged).

## 8. Persistence Target — [D → not yet resolved by this charter]

A new C-023-owned registry (working name `entitlement_license_registry`, `TDS-C023 §6.3` item 2) — **design recommendation only; no table exists; which microservice hosts it remains an explicitly open question** (`TDS-C023 §6.3`, no canonical assignment exists anywhere). **This charter does not create, authorize, or assign this table.** Resolving the service-hosting question is implementation-design work carried forward from the TDS (`TDS-C023 §24` item 1), not performed here.

## 9. State / Lifecycle Transition — [A]

`(none) → ACTIVE` (continuing/establish outcome) only, per `EX-C023-11`. This Business Activity never produces `SUSPENDED` or `REVOKED` (terminal) outcomes — `EX-C023-12`/`EX-C023-13` and the change-of-existing-grant path remain explicitly out of scope (§19 below), consistent with `TDS-C023 §4`'s own narrowing of Decision 2's "administrative establishment" to the establish outcome specifically.

## 10. Authorization — [D → not yet resolved by this charter]

Per `IRA-C023 §19.13` (Decision 1): the Commit Authority mechanism is `URA-001-41`'s Approval Authority concept (`approval_authorities`, `C-003`/`WP-02`) — **governance-mechanism selection only.** Per `TDS-C023 §7`/`§9`: the specific instance design, resolution logic, and failure semantics are designed; ~~**the runtime-enforcement dependency does not exist anywhere in this codebase, for any capability** (independently re-confirmed twice this session, most recently via a fresh `dependencies.py` grep)~~ *(struck 2026-08-30 — reconciled below)*. No `PLATFORM_ADMIN`/`AUREX_ADMIN` bypass is used or permitted (`IRA-C023 §19.5`/`§7.8`, unchanged). ~~**This Business Activity cannot be exercised by any caller until this runtime-enforcement work is separately designed and built** — a repository-wide, not C-023-specific, gap (`TDS-C023 §19.4-A`, unchanged).~~ *(struck 2026-08-30 — reconciled below.)*

> **Reconciliation note — 2026-08-30 (post-WP-18).** The struck statements above were accurate when written. The **repository-wide runtime-enforcement dependency now exists and is independently certified** — designed as `TDS-018`, built and closed as **WP-18** (`membership_approval_authority`, `resolve_approval_authority()`, `require_approval_authority()` / `enforce_approval_authority()`; fail-closed; no admin bypass), **CLOSED — CERTIFIED — RELEASE-READY** through all five `CLAUDE.md §19.7b` gates (`CERT-WP-18`, `VV-AUDIT-WP-18`, `RRA-WP-18`, RO Closure `IMP-REPORT-WP-18 §7`). C-023 is a future consumer of this repository-wide C-003 infrastructure. **This BA still cannot be exercised** — but now only because C-023's own work is unbuilt and unauthorized: the specific C-023 `approval_authorities` instance and `membership_approval_authority` binding row(s) have not been established, the `entitlement_license_registry` schema/service does not exist, and **no Implementation Authorization has been granted**. This section remains `[D → not yet resolved by this charter]` for those reasons, not because the enforcement mechanism is missing. The C-023 **service-hosting question (§8) remains an open `[D]` Repository Owner decision.**


## 11. Organization / Membership Boundary — [A]

Entitlement is anchored to the Organization (optionally Domain-scoped); License is anchored to the Membership, itself keyed to an Organization (`§7.4`, `TDS-C023`). Not a platform-wide, pre-Organization concern the way `C-040`'s `AI-001`/`AI-002` were (`IRA-C023 §7`, corrected, unchanged) — every Commit Authority instance is Organization-scoped (`approval_authorities.organization_id NOT NULL`). Tenant-container semantics beyond `WP-16`'s own minimal `(none)→PROVISIONED` fact are not required by this BA's own primary anchors (`IRA-C023 §13`, Gate 4, conditional pass, unchanged, not reopened by this charter).

## 12. Events / Outcomes — [C]

Design-level only, per `TDS-C023 §14`/`§16` — `record_audit()`/`publish_event()` calls mirroring `MembershipService.establish()`'s own already-certified shape are the designed pattern; **no actual event name, payload, or code exists.** `URA-001-119` names five canonical entitlement-change events (`ENTITLEMENT_ENABLED`/`DISABLED`, `TRIAL_STARTED`/`EXPIRED`, `LICENSE_UPGRADED`) as the eventual vocabulary this BA's own establish outcome should align to — not yet implemented.

## 13. Error / Rejection Conditions — [C]

Design-level only, per `TDS-C023 §14`/`§17.1` (not yet implemented): target Organization/Membership not found → 404; duplicate current Authoritative context for the anchor → 409; Commit Authority not satisfied (no `ACTIVE` `approval_authorities` row, or caller not in the accountability-point Group) → 403; Entitlement Type not already recognized → rejected (exact status code not yet designed, since no catalog-lookup mechanism exists yet, `IRA-C023 §21.6`).

## 14. Idempotency Expectations — [A]

Design-level, reusing an already-certified pattern (`TDS-C023 §15`): the same pre-check-then-create-then-catch-`IntegrityError` shape `MembershipService.establish()` and every prior `WP-0X` Business Activity in this codebase already uses. **Not yet implemented** — no code, no test exists.

## 15. Audit / Observability Expectations — [C]

Design-level only, per `TDS-C023 §16`: initiating `person_id`; the specific `approval_authorities` row (and, once designed, Group/accountability point) that authorized the action; affected Organization/Membership; License/Entitlement anchor and type established; `effective_from`/`effective_to`; resulting status; correlation identifier; on failure, the specific rejection reason. **Not yet implemented.**

## 16. Dependencies — [A]

Reclassified per `TDS-C023 §18`, unchanged, not reopened: `C-004`/`C-007` — already satisfied, closed, certified. `approval_authorities` (`C-003`, existing, certified data model) — selected mechanism, its own runtime enforcement is a repository-wide, not-yet-built gap. `C-020`/`C-025` — required only for a future, differently-scoped BA (the source-hand-off path), **not this BA**. `C-021`/`C-024` — informational/reference only, no direct exchange. `C-040` — `WP-16`'s own minimal delivered scope suffices; no further Tenant work required. `C-041`/`C-150` — **not evidenced anywhere in `PE-001-C023`'s own text** (confirmed by direct full-text search, twice, this session) — no dependency asserted. No dependency on any unchartered capability beyond the already-disclosed, non-blocking `C-020`/`C-025` future-scope items.

## 17. Acceptance Criteria — [D → not yet resolved by this charter]

**Cannot yet be stated as a testable, implementation-level criterion** — no code exists to test. The design-level acceptance criterion, per `TDS-C023 §14`/`§17`: a caller satisfying the resolved Commit Authority can establish exactly one current Authoritative Entitlement and/or License Context per anchor, atomically, correctly rejecting every duplicate/unauthorized/missing-anchor/unrecognized-type case with the correct status code. **This becomes testable only once Implementation Authorization is separately granted and the ~~runtime-enforcement/~~schema/service work is built.** *(Reconciled 2026-08-30: the runtime-enforcement portion of that work is no longer outstanding — it was delivered and certified as WP-18/`TDS-018`. The C-023 `entitlement_license_registry` schema/service, the C-023 authority instance and its binding, and the two frontend items remain unbuilt and unauthorized; this section stays `[D]` for those reasons.)*

## 18. Test Obligations — [D, NOT YET SATISFIED]

**No test exists.** A future implementing session must, at minimum, satisfy `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist (two distinct, unrelated Organizations, cross-Organization visibility probe, foreign-identifier-acceptance probe) and `TDS-C023 §21`'s own designed V&V expectations (a negative control proving the runtime-enforcement contract denies by default, mirroring `test_role_claim_does_not_substitute_for_ai002_holder`'s own precedent; a concurrent-establish race test, mirroring `MembershipService.establish()`'s own existing coverage). **None of this C-023 test coverage exists today.** *(Reconciled 2026-08-30: the runtime-enforcement contract that the negative control must exercise now exists and is itself independently certified — WP-18/`TDS-018` shipped that exact class of negative control, `VV-AUDIT-WP-18` probe P4. This BA's own tests, against C-023's own not-yet-built schema/service, remain entirely unwritten and this section stays `[D, NOT YET SATISFIED]`.)*

## 19. Out-of-Scope Boundaries — [A]

- `C-020` source hand-off consumption (`EX-C023-02`) and `C-025` consumption — `IRA-C023 §20.12`, Decision 2.
- License Consumption and Allocation implementation, and any authority assignment for either — `IRA-C023 §22.13`, Decision 4, deferred, not reopened.
- Global Entitlement Type/Feature Catalog administration, and any authority assignment for it — `IRA-C023 §21.12`, Decision 3, deferred, not reopened.
- Technical Provisioning, migration, offboarding, cross-tenant sharing — never in any C-023 scope framing to date.
- Full License Administration UI, Consumption dashboards, Allocation dashboards, Catalog administration UI, Subscription administration UI, Billing UI — `IRA-C023 §23.13`, Decision 5, exactly two frontend items authorized (§20 below), nothing beyond.
- Commercial/billing workflows beyond the minimum construct — `TDS-C023 §5`-D, out of scope entirely for this design.
- Full Tenant Administration beyond `WP-16`'s own already-delivered minimal scope — unaffected, unchanged.
- Suspend/revoke/reactivate outcomes of `ERB-C023-05` (`EX-C023-12`/`-13`) — this BA realizes the establish (continuing) outcome only (§9 above); a future, separately-scoped increment, not assumed here.
- Any future C-023 capability not explicitly named in this charter.

## 20. Implementation Readiness Classification — TDS Sufficiency Acceptance

**`TDS-C023_Licensing_and_Entitlement_Minimum_BA.md` is hereby formally accepted as the governing Technical Design for this Business Activity.** Result, per its own twice-independently-reviewed verdict: **TDS SUFFICIENT FOR BA CHARTERING.** Acceptance is a governance act recognizing the TDS's own already-independently-confirmed conclusion — it does not alter `IRA-C023`'s own RED classification, which remains unchanged, unreopened, and controlling for implementation readiness. **This is a chartering-sufficiency acceptance, not an implementation-readiness acceptance — the two are deliberately not conflated anywhere in this charter**, mirroring `IRA-C023`'s own repeated distinction between "governance decisions resolved" and "implementation readiness achieved."

## 21. Enterprise Experience Scope Decision — `CLAUDE.md §20.3` [D → RESOLVED, `IRA-C023 §23.13`]

**RESOLVED, Option B: Minimal Frontend.** Per `IRA-C023 §23.13` (Decision 5): this Business Activity's own Enterprise Experience is limited to exactly two items — (1) Establish License/Entitlement; (2) display the resulting establishment/status outcome (`TDS-C023 §17`). **No full administration console, Consumption dashboard, Allocation UI, Catalog administration UI, billing UI, or subscription administration UI is authorized by this charter.** No frontend code exists — this remains implementation work, not performed here.

**Scope of this decision, stated explicitly, mirroring `WP-16 §21`'s own convention:**
- Applies only to BA-01/WP-17's own current chartered scope. It is a scope decision for this Business Activity, not a constitutional prohibition on Enterprise Experience for C-023 generally.
- Does not mean C-023 can never have a fuller frontend, or that future Enterprise Experience work for Consumption/Allocation/Catalog is cancelled — a future, separately-chartered Business Activity remains fully possible and is not foreclosed.
- Does not expand BA-01's own scope (§19) — every excluded item there remains excluded, unaffected by this decision.

## 22. Repository Owner Decisions Recorded (summary — full text: `IRA-C023_Licensing_and_Entitlement_Implementation_Readiness_Assessment.md §18.13/§19.13/§20.12/§21.12/§22.13/§23.13`)

| Decision | Disposition |
|---|---|
| 1 — Commit Authority | RESOLVED, Option B — Reuse the Existing Approval Authority Mechanism (`§19.13`). Mechanism category only; instance/accountability-point/runtime enforcement remain unbuilt (§10/§21 above). |
| 2 — Minimum-scope BA vs. `C-020`/`C-025` wait | RESOLVED, Option A — Minimum Scope Now (`§20.12`). This charter's own scope directly implements that resolution. |
| 3 — Global Entitlement Type/Feature Catalog governance authority | RESOLVED (deferral), Option A — Defer with a Recorded Trigger (`§21.12`). Not reopened by this charter; not part of this BA (§19 above). |
| 4 — License Consumption/Allocation authority | RESOLVED (deferral), Option A — Defer with a Recorded Trigger (`§22.13`). Not reopened by this charter; not part of this BA (§19 above). |
| 5 — Enterprise Experience/frontend scope | RESOLVED, Option B — Minimal Frontend (`§23.13`). Directly implemented at §21 above. |
| 6 — `membership.license_type` vs. C-023 License ownership | RESOLVED, Option B — Split Ownership (`§18.13`). Directly implemented at §7 above (`membership.license_type` referenced, never written/duplicated). |

**No decision above is reopened, altered, or reinterpreted by this charter.**

## 23. Temporal / Subscription Semantics — Preserved as Pending Canonical Binding

Per `TDS-C023 §10.2` (unchanged, not reopened by this charter): whether License duration should align with Subscription duration, whether a License can outlive a Subscription, and what happens on Subscription renewal or termination are **not established by any canonical source** and remain marked **Pending Canonical Binding / Future Governance Decision.** This charter does **not** invent Subscription-aligned expiry, automatic extension, or automatic revocation tied to any Subscription event. `effective_from`/`effective_to` are independent, Commit-time business dates (`TDS-C023 §10.1`), unaffected by this open question, since this BA's own administrative-establishment path never invokes a Subscription at all (`§3` above).

## 24. Implementation Status and Sequencing Disclosure

**No implementation exists.** No production code, schema, migration, router, service, repository, model, or frontend component has been created for C-023 at any point, in this charter or any prior C-023 governance artifact. **Gates 1, 2, and 5 (`CLAUDE.md §19.7b`) have not been dispatched.** This charter does not authorize Implementation — a separate, explicit Repository Owner act (§20's own "TDS Sufficiency Acceptance" is not that act; mirrors `TDS-016`'s/`TDS-017`'s own explicit "does not authorize implementation" disclaimer, carried forward here for the charter itself).

## 25. CBOR Status

**Not assessed by this charter.** Whether the new C-023-owned License/Entitlement governance-layer construct (`§8`) is eligible for Canonical Business Object Registration (`CMD-001 §26.3a`) has not been evaluated — this is disclosed as not-yet-performed future work, mirroring `WP-16`'s own identical disclosure for Tenant CBOR eligibility ("preliminarily eligible, not yet performed... a downstream closure activity, not a chartering prerequisite"), not silently assumed either way.

## 26. Decisions 3 and 4 — Deferred, Not Reopened, Disclosed as Future Governance Triggers

Restated here for chartering-level clarity, not reinterpreted: **Decision 3**'s own recorded trigger (`§21.12`) — "when implementation of the Global Entitlement Type/Feature Catalog becomes necessary for a C-023 Business Activity or another formally chartered capability that requires creation, modification, or governance of global Entitlement Types/Feature definitions" — is **not** fired by this charter; this BA only ever references an already-recognized Entitlement Type, never creates one. **Decision 4**'s own recorded trigger (`§22.13`) — "when implementation of License Consumption and/or Allocation becomes necessary for a formally chartered C-023 Business Activity or another formally chartered capability that requires authoritative recording, enforcement, or governance of License consumption/allocation" — is **not** fired by this charter; this BA establishes, but never tracks consumption or allocation of, a License or Entitlement. **Neither authority is assigned, exercised, or implied by this charter.**

---

## Final Determinations

**This charter does NOT itself:** perform CBOR registration (§25); populate an `approval_authorities` row or any accountability-point binding (§10/§21); build runtime authorization; create the `entitlement_license_registry` table or any migration; write production code, tests, or frontend; resolve Decisions 3 or 4 (§26); resolve the service-hosting question (§8); grant Implementation Authorization (§24); commit or push anything.

**Explicitly preserved, unchanged by this charter:**
- `IRA-C023` remains **🔴 RED — Not Implementation Ready** — unaffected by this charter, which addresses chartering sufficiency only.
- `C-020`/`C-025` remain unmodified, unchartered, and non-prerequisite for this BA.
- `C-040`/`WP-16` remain untouched — `C-040` remains GREEN; `WP-16`/BA-01 remains CLOSED — CERTIFIED.
- `C-114` remains untouched — GAP-4 remains DEFERRED, Option A.
- `AI-002`/`TD-157`/the Sarika Rath evidence path remain untouched — no genuine C-023 dependency on any of them was found at any point in this governance cycle.
- `membership.license_type` (`C-007`/`WP-03`) remains unmodified, unmigrated, undeprecated, and its ownership unchanged.
- `PE-001-C023`, `PE-001-C007`, `URA-001`, `CAP-001` remain unmodified.

**Final state, per direct instruction:** **BA CHARTERED. IMPLEMENTATION NOT YET AUTHORIZED, NOT YET COMPLETE. NOT CERTIFIED.**

---

## Change Control

**Files created:** this document — `architecture/05-Implementation/WP-17_C023_BA-01_Establish_Entitlement_License_Context_Business_Activity_Charter.md`.
**Files modified:** `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md` — one new `WP-17` row added to §2, per `WPR-001 §3`'s own Maintenance Rule (b) ("a row is added to §2 only when... a Work Package... has an accepted IRA assigning it a specific capability" — `IRA-C023` was formally accepted, satisfying this condition), mirroring the identical addition pattern `WP-15`/`WP-16` each already established. No other row in `WPR-001` was altered.
**Not modified:** production code, schema, migrations, frontend, `PE-001-C023`, `PE-001-C007`, `URA-001`, `CAP-001`, `SER-001`, `TD-157`, any C-040/WP-16 artifact, `C-114`, `AI-001`/`AI-002`/`AI-003`/`AI-004`, any unrelated ADR, any unrelated certified WP artifact.

**Governance-reconciliation pass — 2026-08-30 (post-WP-18, R3), per direct Repository Owner instruction ("Reconcile R2 and R3 stale governance statements against WP-18 completion").** Strikethrough-preserve, nothing erased. Sections reconciled in this charter: **§5** (the "cannot be satisfied by any Organization today … the accountability-point binding mechanism … is itself undesigned" precondition — struck; note added that the binding mechanism now exists and is certified as WP-18, while no C-023 authority/binding row has yet been established), **§10** (the "runtime-enforcement dependency does not exist anywhere in this codebase, for any capability" and "cannot be exercised by any caller until this runtime-enforcement work is separately designed and built" statements — struck; reconciliation note added: the dependency now exists (WP-18/`TDS-018`, CLOSED — CERTIFIED — RELEASE-READY), and §10 stays `[D]` only because C-023's own instance/binding/registry/service work is unbuilt and unauthorized), **§17** (the "runtime-enforcement/schema/service work … is built" phrase narrowed — runtime-enforcement portion struck as delivered, schema/service/frontend still outstanding), **§18** (annotated — the runtime-enforcement contract the negative control exercises now exists and is certified; C-023's own tests remain unwritten). **Not changed by this pass:** any of C-023 Decisions 1–6; `TDS-018`; any WP-18 certification artifact; the charter's own scope (§19), its Final Determinations, or its `Status` line. **WP-17 is not marked implemented, certified, or implementation-authorized — it remains CHARTERED — IMPLEMENTATION NOT YET AUTHORIZED, NOT YET COMPLETE, NOT CERTIFIED.** The **service-hosting question (§8) remains an open `[D]` Repository Owner decision — not resolved by this pass.** Companion R2 reconciliation in the same pass: `TDS-C023 §7.7`/`§7.9`/`§9`/`§24`/`§25`/`§29.8`. Companion R3 reconciliation: `IRA-C023 §16` and the `WPR-001` WP-17 row. No production code, schema, migration, test, or frontend was created or modified; nothing was staged, committed, or pushed.
