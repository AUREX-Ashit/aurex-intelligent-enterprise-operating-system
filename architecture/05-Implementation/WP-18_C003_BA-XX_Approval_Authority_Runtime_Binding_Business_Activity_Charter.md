# WP-18 — C-003 (Role & Permission Management) — Bind and Resolve Approval Authority — Business Activity Charter

**Work Package:** WP-18 — the next unclaimed Work Package number, verified directly this pass against `WPR-001` (highest row: `WP-17`, C-023, CHARTERED — implementation not yet authorized; no `WP-18` row, reference, or reservation exists anywhere in `WPR-001`). `WP-REG-001` was also checked and found stale (last updated 2026-08-08, predating `WP-13` through `WP-17`) — `WPR-001` is treated as the current authoritative source per its own status as this repository's "single, authoritative source for Work Package → Capability assignment" (`WPR-001 §1`).
**Business Activity:** BA — Bind and Resolve Approval Authority (working title; no closer canonical term found in `URA-001` or repository precedent — disclosed, not invented as if canonical, §1).
**Capability:** C-003 — Role & Permission Management (`CAP-001` line 68, Primary Specification `URA-001`, Active). Verified directly, not assumed: `approval_authority_registry` and `membership_registry` are both C-003/C-007-adjacent constructs already hosted in `AuthService` under WP-02's own certified ownership; `membership_approval_authority` (the binding object this BA implements) is additive schema to the same C-003-owned registry, per `TDS-018 §4.2`.
**Status:** ~~**CHARTERED — IMPLEMENTATION AUTHORIZED, IMPLEMENTATION COMPLETE, NOT YET CERTIFIED.** *(Updated this pass — historically accurate at drafting time, this line originally read "IMPLEMENTATION NOT YET AUTHORIZED, NOT YET COMPLETE, NOT CERTIFIED"; superseded once the Repository Owner explicitly granted Implementation Authorization and implementation was subsequently completed, per `IMP-REPORT-WP-18_Approval_Authority_Runtime_Binding.md §1`/`§2`. A Gate 1 Independent Certification was attempted and returned NOT CERTIFIED solely because this reconciliation had not yet occurred — no code, security, or design defect was found. Certification remains not yet achieved.)*~~ *(The struck-through line above was accurate between 2026-08-29 and 2026-08-30 and is preserved as the historical record.)* **CLOSED — CERTIFIED — RELEASE-READY (governance-recording complete; repository commit outstanding), 2026-08-30.** All five `CLAUDE.md §19.7b` gates are complete: Gate 1 Independent Certification — PASS WITH OBSERVATIONS (`CERT-WP-18_Approval_Authority_Runtime_Binding.md`); Gate 2 V&V Audit — PASS WITH OBSERVATIONS (`VV-AUDIT-WP-18_Approval_Authority_Runtime_Binding.md`); Gates 3/4 not triggered (no remediation required); Gate 5 Release Readiness Audit — PASS (`RRA-WP-18_Approval_Authority_Runtime_Binding.md`). The formal Repository Owner Closure Decision is recorded at `IMP-REPORT-WP-18_Approval_Authority_Runtime_Binding.md §7` (2026-08-30). Five non-material observations (`VV-O1`–`VV-O5`) are disclosed and accepted for release; none is a `CLAUDE.md §19.8.5`-class defect. **This closure does not authorize, begin, or certify any C-023 or `WP-17` work — C-023 remains 🔴 RED — Not Implementation Ready; `WP-17` remains CHARTERED — IMPLEMENTATION NOT YET AUTHORIZED, NOT YET COMPLETE, NOT CERTIFIED; neither is changed by this closure.** This charter formalizes `TDS-018_C003_Approval_Authority_Runtime_Binding_Technical_Design.md` (design-only, independently reviewed — no material defect) into the charter-level structure `WP-14 BA-04`, `WP-15 BA-01`, `WP-16 BA-01`, and `WP-17 BA-01` each already established as real, repeated repository precedent.
**Prepared under:** direct Repository Owner instruction ("TDS-018 — Charter the Repository-Wide Approval Authority Runtime Binding Work Package"), following `TDS-018`'s own independently-confirmed "SUFFICIENT FOR BA/WP CHARTERING" status.

**A note on document type, disclosed rather than assumed (mirrors `WP-14 BA-04`'s, `WP-15 BA-01`'s, `WP-16 BA-01`'s, and `WP-17 BA-01`'s own identical disclosure):** this repository's own established convention charters at the Work Package level, with per-Business-Activity charter detail specified inside the governing IRA. This charter departs from that convention for the same reason its four predecessors did — per direct Repository Owner instruction — with one further, genuinely disclosed difference from all four: **no accepted IRA governs this Work Package** (§0 below explains why, and the precedent relied on).

**Governing basis, stated explicitly:** `CAP-001` (C-003 registration, line 68) → `URA-001-41`/`-42`/`-61`/`-62`/`-82` (Approval Authority, primary domain specification) → `Master_Technical_Architecture.md` (canonical, unimplemented `membership_approval_authority` schema) → `TDS-018_C003_Approval_Authority_Runtime_Binding_Technical_Design.md` (Technical Design, independently reviewed, no material defect) → this charter. **No implementation exists at any point in this chain.**

---

## 0. Governing-Document Basis — Disclosed Departure from the Usual IRA-First Sequence

`WPR-001 §3`'s own Maintenance Rule states a row is added to its roadmap table "only when a Work Package is either (a) actually committed to the repository..., or (b) has an accepted IRA assigning it a specific capability." **Neither condition is literally satisfied here** — this Work Package has not been committed, and no IRA (`IRA-018`, or any IRA assigning this specific runtime-binding scope to C-003) has been drafted or accepted. This is disclosed plainly, not glossed over.

**The precedent relied on instead: `WP-13`.** `WPR-001`'s own §2 table already contains a standing, un-reopened exception of the identical shape — `WP-13` ("Authorization Runtime Integration"), whose own "Governing IRA" cell reads verbatim: *"— (no new IRA; this is platform-wide adoption of already-certified architecture, not new capability work)."* `WP-13` was added, and remains, in `WPR-001`'s own main roadmap table without an IRA, on exactly the reasoning this Work Package also satisfies: it is repository-wide/platform-wide infrastructure implementing an already-canonically-specified construct (`WP-13`: the already-certified `Backend/Runtime/AuthorizationEngine`; this Work Package: the already-specified `membership_approval_authority` table, `Master_Technical_Architecture.md` lines 1318–1329), not a new PE-001 capability experience requiring its own Business-Activity-readiness assessment.

**One disclosed difference from `WP-13`, not hidden:** `WP-13` used capability field `— (Runtime)`, since its own work is not cleanly attributable to one PE-001 capability. This Work Package instead uses `C-003` directly, per the Repository Owner's own explicit instruction (§2 of the governing task) and `TDS-018`'s own explicit self-declaration as C-003-owned (`membership_approval_authority` is additive schema to C-003's own `approval_authority_registry`). This is a judgment call, made transparently: the underlying reasoning (repository-wide infrastructure, no new capability-experience work, no IRA required) is identical to `WP-13`'s own; only the capability-attribution field differs, because unlike `WP-13`'s own cross-cutting Runtime Engine, this construct has one clear, undisputed owning capability.

**If this reading is judged incorrect, this charter should be treated as provisional pending an explicit Repository Owner confirmation or correction — not as a silently-settled interpretation.**

---

## Classification Key

Mirrors `WP-15 BA-01`'s, `WP-16 BA-01`'s, and `WP-17 BA-01`'s own key exactly:
- **A** — already determined by governing documents
- **B** — determined by repository precedent
- **C** — an implementation detail
- **D** — requires a Repository Owner decision, genuinely open
- **D → RESOLVED** — was **D**, now resolved by a recorded decision

---

## 1. Business Activity Identity — [A/B]

Working title: **"Bind and Resolve Approval Authority."** Verified against repository precedent before use, per the governing task's own explicit instruction: no closer canonical term exists in `URA-001` or elsewhere — `URA-001-41`/`-42` name the `approval_authorities` policy object itself but no canonical name for *binding an actor to it*. This title is descriptive, not a claim of canonical status — Category B (repository-precedent-shaped naming, mirroring how `WP-06`'s own charter titled itself "Domain Permission Read APIs," a descriptive scope title, not a `PE-001`-sourced EX name), not Category A.

Governed physical Business Object: `membership_approval_authority` (`Master_Technical_Architecture.md` lines 1318–1329, `TDS-018 §5`/`§19`) — a new, additive, C-003-owned join table. Write path — creates/supersedes/closes a binding record. Read/resolution path — the runtime resolver contract `TDS-018 §29.2`/`§29.4` designs (not yet built; `§29.2` is the current, amended, authoritative algorithm — `§10`'s own original text is superseded and preserved only as historical record, `TDS-018 §10`'s own note).

## 2. Business Intent — [A]

Realize `TDS-018`'s own central design conclusion (`TDS-018 §5`–`§7`): make the already-certified, Organization-scoped `approval_authorities` mechanism (`URA-001-41`, `WP-02` BA-03) actually enforceable at runtime, by implementing the canonical `membership_approval_authority` binding and a resolver that determines, for a given caller and a given Approval Authority, `ALLOW` or `DENY` (`TDS-018 §17`, §20). This closes a repository-wide gap `TDS-018 §4` independently reconfirmed exists for every capability that has ever established an `approval_authorities` row, not only C-023.

## 3. Trigger — [A]

Two triggers, both already recorded, neither invented here: (1) `IRA-C023 §19.13` Decision 1 (Option B, "Reuse the Existing Approval Authority Mechanism") named this mechanism family as C-023's own future Commit Authority basis, and `TDS-C023 §7.7`/`§29` found no runtime enforcement exists for it anywhere; (2) `TDS-018 §1`/`§4` independently confirmed this gap is repository-wide, not C-023-specific — any future capability establishing an `approval_authorities` row shares the identical unmet need. This Work Package's own trigger is the second, broader finding — it is chartered as C-003-owned infrastructure, not as a C-023 deliverable (§7 below).

## 4. Actor / Persona — [A/C]

The resolver's own caller is any authenticated Membership attempting an action gated by an `approval_authorities` row (e.g., a future C-023 Commit Authority caller, §7). No specific persona is named by `URA-001` for this binding/resolution act itself — Category C, an implementation detail resolved by whichever future consuming capability's own persona vocabulary applies (e.g., `PE-001-C023 §1.11`'s "Entitlement/License Steward"/"Decision Participant" for C-023's own eventual consumption, unchanged, not resolved here).

## 5. Preconditions — [A]

A currently-`ACTIVE` `approval_authorities` row must exist for the target Organization/`authority_name` (`ApprovalAuthority.status`, certified, `WP-02` BA-03/07/08, unchanged). The caller must hold a currently-valid Membership in that same Organization (`WP-03` BA-01, certified, unchanged). Neither precondition is created, altered, or relaxed by this charter.

## 6. Input Contract — [C]

Per `TDS-018 §20`: target Organization identifier, required `authority_name`, caller's verified claims (`person_id`, `organization_id`), resolved `membership_id`. Precise request/response schema shape is an implementation detail, not fixed by this charter.

## 7. Business Rules — [A]

**Carried forward from `TDS-018 §29.2`/`§29.3` — the current, amended, authoritative algorithm — not from `TDS-018`'s own original `§10`/`§11`, which are superseded and preserved only as historical record.** Corrected this pass to align with `TDS-018`'s own independently-reviewed amendment (no material defect found), following the identical High-severity false-`ALLOW` finding a WP-18 implementation-readiness review surfaced: the original list below (as it stood before this correction) never gated on `approval_strategy`, meaning a `MAJORITY`/`ALL`/`SEQUENTIAL`-configured row could have been satisfied by a single qualifying binding. The corrected sequence, in order, not reinterpreted:

(1) resolve the authority — no `ACTIVE` row → deny; a row exists but is `SUPERSEDED`/`DEPRECATED`/`RETIRED` → deny; (2) validate configuration — a structurally malformed row (e.g., `MAJORITY` with no threshold) → deny, never defaulted, **evaluated before any caller-specific step and before the strategy check below, so it cannot be bypassed by a qualifying binding**; (3) **inspect `approval_strategy` — if not `ANY_ONE`, deny.** `MAJORITY` → deny. `ALL` → deny. `SEQUENTIAL` → deny. **No counting, quorum, or sequencing semantics for these three strategies are invented anywhere in this charter or in `TDS-018`** — they remain genuinely unresolved (`TDS-018 §9`/`§29.5`), this rule only ensures they cannot silently authorize; (4) caller Organization mismatch → deny; (5) no currently-effective `membership_approval_authority` binding for the caller → deny; (6) caller's own Membership not currently valid → deny; (7) only when steps 1–6 all pass, for an `ANY_ONE`-strategy row, does exactly one qualifying binding authorize (`TDS-018 §29.2` step 7/8); (8) no `PLATFORM_ADMIN`/`AUREX_ADMIN`/Role/Group bypass exists at any branch (`TDS-018 §29.3`/`§18`, unchanged).

## 8. Persistence Target — [A]

`membership_approval_authority`, exact canonical shape per `Master_Technical_Architecture.md` lines 1318–1329 and `TDS-018 §19`: `membership_id`, `approval_authority_id`, `effective_from`, `effective_to`, composite PK `(membership_id, approval_authority_id, effective_from)`. **Not created by this charter** — implementation remains future work (§18 below).

## 9. State / Lifecycle Transition — [A]

A binding is "deactivated" by setting `effective_to`, never hard-deleted — `TDS-018 §19`'s own recommended consistency choice, mirroring every other SD-002-011-shaped table in this codebase (`ApprovalAuthority`, `DelegationPolicy`, `RuntimeAssignmentPolicy`, `AuthorityHolder`). No status column beyond the temporal window, per the canonical schema's own minimal shape.

## 10. Authorization — [D → not yet resolved by this charter]

**Two items remain genuinely open, carried forward from `TDS-018` without resolution, per the governing task's own explicit "preserve open items" instruction:**
1. **Engine-tier (Option A) vs. direct-dependency (Option B) integration** (`TDS-018 §12`/§13) — Option B (a direct FastAPI dependency, mirroring `require_authority_holder`) is `TDS-018`'s own **recommended near-term direction**, carried forward here as the design basis, but **not decided or implemented by this charter**. Option A (a concrete M5 `ApprovalAuthorityResolver` inside `Backend/Runtime/AuthorizationEngine`) remains the architecturally correct long-term home, per `TDS-018 §12`'s own disclosure, revisited only once M2–M4 exist.
2. **Cross-Organization binding enforcement mechanism** (`TDS-018 §7`/§19) — service-layer validation vs. database trigger, not chosen.

Neither item blocks chartering (`TDS-018 §24`'s own governance determination: both Category C, ordinary implementation-design choices, not Repository Owner decisions) — both are explicitly **not resolved** by this charter and remain open for the implementing session.

## 11. Organization / Membership Boundary — [A]

Enforced at the two independent points `TDS-018 §18` already designs: RLS on `membership_approval_authority` itself (canonical, via `membership_registry.organization_id`), and the resolver's own explicit caller-Organization-vs-target-Organization match check (`TDS-018 §29.2` step 4, renumbered by the amendment — originally step 2, unchanged in substance). The third layer — a bind-time, service-level guard preventing a cross-Organization binding row from ever being created — is named as a required future implementation item (`TDS-018 §7`/§19), **not built by this charter**.

## 12. Events / Outcomes — [C]

A future implementation should `record_audit`/`publish_event` on bind/supersede/close (mirroring `ApprovalAuthorityService.establish()`/`create_new_version()`'s own existing pattern, `TDS-018 §21`) and on every resolution outcome (`AUTHORIZED`/denied-with-reason). Precise event names/payloads are an implementation detail, not fixed here.

## 13. Error / Rejection Conditions — [A]

**Corrected this pass — `TDS-018 §29.4` (amended) supersedes `§20`'s own original seven-label list, adding one label.** Exactly the eight diagnostic reasons `TDS-018 §29.4` now designs: `NO_AUTHORITY_CONFIGURED`, `INACTIVE_AUTHORITY`, `INVALID_CONFIGURATION`, **`UNSUPPORTED_STRATEGY`** (new — `approval_strategy` is not `ANY_ONE`), `INVALID_SCOPE`, `NO_ELIGIBLE_ACTOR`, `INACTIVE_MEMBERSHIP`, `AUTHORIZED`. Outer decision reuses the existing `AuthorizationDecision` (`RTA-001 S11.8`, `authorization/models.py`) — `ALLOW`/`DENY` only, no new status enum invented (`TDS-018 §20`/`§29.4`'s own explicit reuse-over-invention discipline, carried forward unchanged).

## 14. Idempotency Expectations — [C]

Not designed by `TDS-018` in further detail beyond the composite-PK shape (`§19`); an implementation-time concern for the binding-creation service, not resolved here.

## 15. Audit / Observability Expectations — [A]

Reuses `observability.py`'s existing `record_audit`/`publish_event`/`AuditStatus` convention exactly, per `TDS-018 §21` — no new audit subsystem. Full detail (exact `action` names, metadata shape) remains a future implementation item.

## 16. Dependencies — [A]

`C-003`/`WP-02`'s own certified `approval_authorities`/`ApprovalAuthorityService` (unmodified, reused as-is). `C-007`/`WP-03`'s own certified `memberships` (unmodified, reused as-is). `Master_Technical_Architecture.md`'s own canonical schema specification (source of truth for the new table's own shape — not altered by this charter). `TDS-018`'s own design in full. **Not a dependency of, and does not depend on, C-023, `TDS-C023`, or `WP-17`** — the relationship runs the other direction (§7 below).

## 17. Acceptance Criteria — [D → not yet resolved by this charter]

Not yet specified in implementation-testable detail — a future implementation-time task, per `TDS-018 §26`'s own sequencing (schema → binding service → resolver → Engine integration decision → audit → tests → consumer integration → Implementation Authorization).

## 18. Test Obligations — [D, NOT YET SATISFIED]

**Corrected this pass to align with `TDS-018 §29.6` (amended) — the two new obligations below (strategy-rejection, and confirming malformed configuration cannot be bypassed) did not appear in this section's own original text.** None exist yet. A future implementation must, at minimum, cover every branch `TDS-018 §29.2`/`§29.3` names (all eight `§13` reasons above), specifically including, per `TDS-018 §29.6`:

- `ANY_ONE` + one valid, currently-effective binding → `AUTHORIZED`.
- `MAJORITY` + one valid binding → `DENY`/`UNSUPPORTED_STRATEGY`, never `AUTHORIZED`.
- `ALL` + one valid binding → `DENY`/`UNSUPPORTED_STRATEGY`, never `AUTHORIZED`.
- `SEQUENTIAL` + one valid binding → `DENY`/`UNSUPPORTED_STRATEGY`, never `AUTHORIZED`.
- A malformed configuration (e.g., `MAJORITY` with a NULL threshold) → `DENY`/`INVALID_CONFIGURATION`, never reachable via a qualifying binding.
- `NO_AUTHORITY_CONFIGURED`, `INACTIVE_AUTHORITY`, `INVALID_SCOPE`, `NO_ELIGIBLE_ACTOR`, `INACTIVE_MEMBERSHIP` rejection cases.

**These negative tests establish only that unsupported strategies and malformed rows cannot accidentally authorize — they must not define, simulate, or approximate how `ALL`/`MAJORITY`/`SEQUENTIAL` would eventually count votes or sequence approvers** (`TDS-018 §29.5`, unresolved, not invented here). Additionally, per this repository's own Mandatory Tenant-Isolation Test Checklist (`CLAUDE.md §21.4`) — two distinct Organizations, a caller-cannot-read-across-Organizations probe, and an explicit unrelated-tenant-identifier-acceptance probe, none of which exist today.

## 19. Out-of-Scope Boundaries — [A]

Explicitly excluded from this Work Package, per the governing task's own exhaustive list, each independently re-confirmed against `TDS-018`:

- **C-023 License/Entitlement implementation** — no C-023 code, schema, or migration of any kind.
- **`ERB-C023-05`** — not implemented; this WP builds the mechanism a future `ERB-C023-05` implementation would consume, never the ERB itself.
- **License lifecycle, License Consumption, License Allocation, Entitlement Catalog, Subscription semantics, Billing, `C-020`/`C-025`** — all C-023-specific, none touched.
- **Frontend/UI** — none, at any layer; this is backend infrastructure only.
- **`AuthorityHolder` replacement** — explicitly rejected as unsuitable for reuse (`TDS-018 §14`); coexists, unmodified.
- **Group infrastructure** — investigated and found non-canonical for this binding (`TDS-018 §15`); not created.
- **`PLATFORM_ADMIN`/`AUREX_ADMIN` policy redesign** — `ADR-002 §17a`'s own separate, unresolved bypass-scope question is untouched, not reopened, not resolved.
- **Unrelated authorization redesign** — no change to `require_platform_admin`, `require_matching_tenant_or_platform_admin`, `require_domain_permission`, or `require_authority_holder`.
- **Modification of certified Approval Authority CRUD behavior** — `TDS-018` requires none, and none is authorized; `ApprovalAuthorityService`/`ApprovalAuthorityRepository`/router/schema remain exactly as certified.
- **Unrelated Runtime Authorization Engine redesign** — no change to `engine.py`, `tier_resolvers.py`, `models.py`, or any M2–M6 milestone; `TDS-018 §12`'s own Option A remains a named future possibility, not built or scaffolded.

## 20. Implementation Readiness Classification — TDS Sufficiency Acceptance

**`TDS-018_C003_Approval_Authority_Runtime_Binding_Technical_Design.md` is hereby formally accepted as the governing Technical Design for this Business Activity.** `TDS-018` has undergone its original independent review (`§28`, no material defect found) and a subsequent independent review of the `§29` resolver-algorithm amendment (`§30`, no material defect remaining from that amendment review). **This is a chartering-sufficiency acceptance, not an implementation-readiness acceptance — the two are deliberately not conflated anywhere in this charter**, mirroring `WP-17 §20`'s own identical discipline, itself mirroring `IRA-C023`'s own established distinction between "governance decisions resolved" and "implementation readiness achieved." Acceptance of `TDS-018` for chartering does not itself authorize implementation (§24 below).

## 21. Enterprise Experience Scope Decision — `CLAUDE.md §20.3`

**Infrastructure-only, per this Work Package's own charter — no Enterprise Experience is chartered.** This is backend, repository-wide infrastructure with no operable screen, no persona-facing journey, and no `PE-001-Cxxx` Capability Experience of its own — `TDS-018`'s own scope (§2) never designs a frontend, and none is designed here. Per `CLAUDE.md §20.3`'s own carve-out ("a Work Package's own charter explicitly designates it infrastructure-only... or a specific Business Activity within it explicitly backend-only"), this Work Package is explicitly designated **backend-only** by this charter — mirroring `WP-13`'s own identical treatment as infrastructure with no PE-001-scoped Enterprise Experience component. Any future consuming capability (e.g., C-023) remains responsible for its own, separately-chartered Enterprise Experience scope decision (`WP-17 §21`, unaffected, unreopened).

## 22. Repository Owner Decisions Recorded

**None new.** This charter records no fresh Repository Owner decision — `TDS-018 §24` independently determined every open implementation-design item (Engine-tier vs. direct-dependency integration; cross-Organization enforcement mechanism) is Category C, not Category D, and this charter does not elevate either to a decision requiring adjudication. The one pre-existing, related decision this Work Package's own existence depends on — `IRA-C023 §19.13` Decision 1 (Option B) — is **not reopened, altered, or reinterpreted** by this charter; it is cited as this Work Package's own originating trigger only (§3).

## 23. Temporal / Subscription Semantics

**Not applicable.** This Work Package has no temporal/Subscription-alignment surface of its own — `membership_approval_authority`'s own `effective_from`/`effective_to` fields are ordinary binding-validity windows (§9), unrelated to `TDS-C023 §10.2`'s own Subscription-alignment open questions, which remain exactly as recorded there, untouched by this charter.

## 24. Implementation Status and Sequencing Disclosure

**Updated this pass — superseded, not rewritten in place, per this repository's own no-silent-fix convention.** The paragraph immediately below is preserved as the historical record of this charter's own state at drafting time, when it was accurate:

~~No implementation exists. No production code, schema, migration, router, service, repository, model, resolver, or test has been created for this Work Package, in this charter or in `TDS-018`. Gates 1, 2, and 5 (`CLAUDE.md §19.7b`) have not been dispatched. This charter does not authorize Implementation — a separate, explicit Repository Owner act, mirroring `TDS-016`'s/`TDS-017`'s/`TDS-018`'s own explicit "does not authorize implementation" disclaimer, carried forward here for the charter itself.~~

**Current state:** the Repository Owner subsequently and explicitly granted Implementation Authorization for WP-18 (recorded in full at `IMP-REPORT-WP-18_Approval_Authority_Runtime_Binding.md §1`), and implementation was completed exactly within that authorized scope — `TDS-018 §26`'s own derived implementation sequence (schema/binding model → repository/service → resolver → Engine-integration decision (Option B selected, per `TDS-018 §12`'s own recommendation) → audit wiring → tests → Explicit Implementation Authorization) was followed in full; see `IMP-REPORT-WP-18` §2/§3 for the complete file list and implementation detail. **Gates 1, 2, and 5 (`CLAUDE.md §19.7b`) remain not yet passed** — a Gate 1 Independent Certification was attempted and returned NOT CERTIFIED, solely because this charter and `WPR-001` had not yet been reconciled with the authorization and completed implementation at the time of that attempt (no code, security, or design defect was found). This governance-reconciliation pass, together with `IMP-REPORT-WP-18`, exists to resolve that specific gap; it does not itself constitute, claim, or imply certification, and does not re-dispatch Gate 1.

**Superseded 2026-08-30 (formal closure).** The "Gates 1, 2, and 5 (`CLAUDE.md §19.7b`) remain not yet passed" statement immediately above was accurate when written and is preserved as the historical record. All five gates have since completed — Gate 1 PASS WITH OBSERVATIONS (`CERT-WP-18_Approval_Authority_Runtime_Binding.md`), Gate 2 PASS WITH OBSERVATIONS (`VV-AUDIT-WP-18_Approval_Authority_Runtime_Binding.md`), Gates 3/4 not triggered, Gate 5 PASS (`RRA-WP-18_Approval_Authority_Runtime_Binding.md`) — and the Repository Owner has recorded a formal WP-18 Closure Decision at `IMP-REPORT-WP-18 §7`. WP-18 is **CLOSED — CERTIFIED — RELEASE-READY** at the governance-documentation level; the repository commit remains a separate, explicitly-authorized future action. No `Backend/` file, `TDS-018`, `IRA-C023`, `TDS-C023`, `WP-17`, or C-023 artifact is altered by this closure.

## 25. CBOR Status

**Not assessed by this charter.** Whether `membership_approval_authority` is eligible for Canonical Business Object Registration (`CMD-001 §26.3a`) has not been evaluated — disclosed as not-yet-performed future work, mirroring `WP-16`'s and `WP-17`'s own identical disclosure pattern, not silently assumed either way. (Note, disclosed for completeness: `membership_approval_authority` is a join/binding table, not obviously a Canonical Business Object in the sense `CMD-001 §26.3a` targets — this observation is not itself a determination, and the formal assessment remains unperformed.)

## 26. C-023 Dependency Relationship — Consumer, Not Owner

Restated for chartering-level clarity, per the governing task's own explicit requirement: this Work Package is the **infrastructure**; C-023 is a **future consumer**, never the owner. The dependency chain, stated precisely and not reversed:

```text
This Work Package (WP-18, C-003)
        │  builds
        ▼
Approval Authority runtime binding infrastructure (membership_approval_authority + resolver, §8/§10)
        │  once built, may be depended upon by
        ▼
IRA-C023 §19.13 Decision 1 (Option B — already resolved, not reopened)
        │  names
        ▼
A future C-023 Commit Authority (TDS-C023 §7, not built)
        │  would gate
        ▼
A future ERB-C023-05 implementation (not built, not authorized, not part of this charter)
```

**None of Decisions 1, 2, 3, 4, or 6 (`IRA-C023 §19.13`/`§20.12`/`§21.12`/`§22.13`/`§18.13`) is reopened, altered, or reinterpreted by this charter.** Decision 5 (`§23.13`, Minimal Frontend) is likewise untouched — it governs C-023/`WP-17`'s own Enterprise Experience scope, unaffected by this Work Package's own §21 above (a distinct, infrastructure-only scope decision for a different Work Package). **C-023 remains RED — Not Implementation Ready. `WP-17` remains CHARTERED — implementation not yet complete, not yet certified.** Neither status is changed by this charter.

---

## Final Determinations

**This charter does NOT itself:** implement `membership_approval_authority` (model, migration, repository, service); implement the runtime resolver or any `require_approval_authority`-shaped dependency; decide Option A vs. Option B (§10); modify `approval_authorities`, `memberships`, `authority_holders`, `dependencies.py`, or `Backend/Runtime/AuthorizationEngine`; create Group infrastructure; implement any part of C-023; create a C-023 authority holder or License/Entitlement record; modify `WP-17`, `IRA-C023`, or `TDS-C023`; grant Implementation Authorization (§24); resolve `ALL`/`MAJORITY`/`SEQUENTIAL` semantics; commit or push anything.

**Explicitly preserved, unchanged by this charter:**
- `TDS-018` remains a Technical Design — implementation authorization for WP-18 did not come from `TDS-018` or from this charter itself; it came from a separate, explicit, subsequent Repository Owner act, recorded at `IMP-REPORT-WP-18 §1` (updated this pass — originally this bullet read "implementation NOT authorized by it, and not authorized by this charter either," accurate before that act occurred).
- `C-023` remains **🔴 RED — Not Implementation Ready** — unaffected by this charter.
- `WP-17` remains **CHARTERED — IMPLEMENTATION NOT YET AUTHORIZED, NOT YET COMPLETE, NOT CERTIFIED** — untouched.
- `IRA-C023`'s six Repository Owner Decisions (1–6) remain exactly as recorded — none reopened.
- `C-040`/`WP-16` remain untouched — `C-040` remains GREEN; `WP-16`/BA-01 remains CLOSED — CERTIFIED.
- `AI-002`/`TD-157`/the Sarika Rath evidence path remain untouched.
- `approval_authorities`, `memberships`, `authority_holders`, `dependencies.py`, `Backend/Runtime/AuthorizationEngine` remain unmodified.
- `CAP-001`, `URA-001`, `Master_Technical_Architecture.md` remain unmodified.

**Final state, updated this pass (historical: "BA/WP CHARTERED. IMPLEMENTATION NOT YET AUTHORIZED, NOT YET COMPLETE. NOT CERTIFIED." — accurate before the Repository Owner's subsequent Implementation Authorization and the resulting completed implementation, both recorded at `IMP-REPORT-WP-18`):** ~~**BA/WP CHARTERED. IMPLEMENTATION AUTHORIZED. IMPLEMENTATION COMPLETE. NOT YET CERTIFIED** — a Gate 1 Independent Certification was attempted and returned NOT CERTIFIED solely for the governance-documentation gap this pass resolves; no code, security, or design defect was found; Gate 1 is not re-dispatched by this update.~~

**Superseded 2026-08-30 — formal Repository Owner closure. Final state: BA/WP CHARTERED. IMPLEMENTATION AUTHORIZED. IMPLEMENTATION COMPLETE. CERTIFIED — all five `CLAUDE.md §19.7b` gates passed (Gate 1 `CERT-WP-18` PASS WITH OBSERVATIONS; Gate 2 `VV-AUDIT-WP-18` PASS WITH OBSERVATIONS; Gates 3/4 not triggered; Gate 5 `RRA-WP-18` PASS). CLOSED — RELEASE-READY, governance-recording complete; the repository commit finalizing this closure in git history has not been performed and remains a separate, explicitly-authorized action. Repository Owner Closure Decision: `IMP-REPORT-WP-18 §7`, 2026-08-30. C-023 remains 🔴 RED — Not Implementation Ready; `WP-17` remains CHARTERED — NOT IMPLEMENTED, NOT CERTIFIED — neither authorized, begun, or certified by this closure. `VV-O5` and every other disclosed observation remain non-material accepted carry-forwards; `TDS-018` and the implementation are unchanged.**

---

## Change Control

**Files created:** this document — `architecture/05-Implementation/WP-18_C003_BA-XX_Approval_Authority_Runtime_Binding_Business_Activity_Charter.md`. **(Gate 1 governance-reconciliation pass, separately dated below):** `architecture/05-Implementation/IMP-REPORT-WP-18_Approval_Authority_Runtime_Binding.md` — the Implementation Report this Work Package's own §19.7 Certification checklist requires, created alongside this pass's own status corrections.
**Files modified:** `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md` — one new `WP-18` row added to §2, on the disclosed `WP-13`-precedent basis explained at §0 above (no accepted IRA exists; `WPR-001 §3`'s literal (a)/(b) conditions are not met by the letter, but `WP-13`'s own standing, un-reopened exception for "platform-wide adoption of already-certified architecture, not new capability work" is directly on point and cited, not invented). No other row in `WPR-001` was altered. **This pass (alignment with amended `TDS-018`):** `§1`, `§7`, `§11`, `§13`, `§18` of this charter corrected so every reference to the resolver algorithm points to `TDS-018 §29.2`/`§29.3`/`§29.4`/`§29.6` (the current, amended, independently-reviewed algorithm — no material defect found) rather than `TDS-018`'s own original, now-superseded `§10`/`§11`/`§20`. The corrected `§7`/`§13`/`§18` now state explicitly: configuration validation precedes authorization; `approval_strategy` is gated before any caller-specific check; only `ANY_ONE` may currently authorize; `MAJORITY`/`ALL`/`SEQUENTIAL` each fail closed with a distinct `UNSUPPORTED_STRATEGY` reason, with no counting/quorum/sequencing semantics invented for any of them. `WPR-001` was **not** touched by this alignment pass, per the governing instruction's own expectation that it should "normally NOT be required" — the `WP-18` row's own text does not restate the resolver algorithm in enough detail to need correction.
**Not modified:** `TDS-018` itself (only read/cited), `IRA-C023`, `TDS-C023`, `WP-17`, production code, schema, migrations, frontend, `approval_authority.py`, `approval_authority_repository.py`, `approval_authority_service.py`, `membership.py`, `dependencies.py`, `Backend/Runtime/AuthorizationEngine`, `CAP-001`, `URA-001`, any C-040/WP-16 artifact, `C-114`, `AI-001`/`AI-002`/`AI-003`/`AI-004`, any unrelated ADR, any unrelated certified WP artifact. No Repository Owner decision was reopened; `membership_approval_authority` design, Organization isolation, the `AuthorityHolder` distinction, the Group exclusion, the C-023 dependency relationship, Decision 1, Decision 6, the Option A/B integration recommendation, the migration boundary, the audit model, and certification status (still CHARTERED / NOT IMPLEMENTED / NOT CERTIFIED) are all unchanged by this alignment pass.
**Gate 1 governance-reconciliation pass (this pass):** the header Status line, `§24`, and two "Final Determinations" statements were updated — using the strikethrough-preserve convention, not silent rewriting — to reflect the Repository Owner's own subsequent, explicit Implementation Authorization and the resulting completed implementation, both recorded in full at the newly-created `architecture/05-Implementation/IMP-REPORT-WP-18_Approval_Authority_Runtime_Binding.md`. This pass was triggered by a Gate 1 Independent Certification attempt that returned NOT CERTIFIED solely because this reconciliation had not yet occurred (no code, security, or design defect was found by that certifier). This pass does **not** itself certify WP-18, does not re-dispatch Gate 1, does not authorize or touch C-023/`WP-17`, and does not modify any `Backend/` file, migration, test, `TDS-018`, `IRA-C023`, or `TDS-C023`.

**§20 traceability correction (separate, later pass):** `§20`'s own stale review-count sentence — *"Independently reviewed once, with no material defect found (`TDS-018 §28`)"* — was corrected to accurately record both of `TDS-018`'s own independent reviews to date: the original design review (`§28`, no material defect found) and the subsequent, separate independent review of the `§29` resolver-algorithm amendment (`§30`, no material defect remaining from that amendment review). This bullet documents that one-sentence correction only — no other content in `§20`, or elsewhere in this charter, was changed by it; no certification or implementation-readiness claim was introduced or implied.

**Formal closure pass (2026-08-30, per direct Repository Owner instruction "Proceed to the formal Repository Owner closure of WP-18"):** the header **Status** line (§6), the `§24` "Current state" note, and the Final Determinations "Final state" line were updated — strikethrough-preserve, nothing erased — to record that all five `CLAUDE.md §19.7b` gates have completed (Gate 1 `CERT-WP-18_Approval_Authority_Runtime_Binding.md` — PASS WITH OBSERVATIONS; Gate 2 `VV-AUDIT-WP-18_Approval_Authority_Runtime_Binding.md` — PASS WITH OBSERVATIONS; Gates 3/4 not triggered; Gate 5 `RRA-WP-18_Approval_Authority_Runtime_Binding.md` — PASS) and that the Repository Owner has recorded a formal WP-18 Closure Decision at `IMP-REPORT-WP-18_Approval_Authority_Runtime_Binding.md §7`. WP-18 is **CLOSED — CERTIFIED — RELEASE-READY** at the governance-documentation level; the repository commit finalizing this closure in git history has not been performed and remains a separate, explicitly-authorized action (identical to `WP-16`'s own recorded closure state). `TDS-018`, every `Backend/` implementation/migration/test file, `IRA-C023`, `TDS-C023`, `WP-17`, and every C-023 artifact were read for cross-reference only, **not modified**. No `IRA-C023` decision was reopened; `VV-O5` was **not** converted into any design or code change. The only other governance artifacts touched in this closure pass are `IMP-REPORT-WP-18` (new §7 — the Closure Decision itself) and the `WPR-001` WP-18 row (same strikethrough-preserve status update). Nothing was staged, committed, or pushed.
