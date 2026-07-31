# VV-AUDIT-WP-05 — Remediation Re-Verification

## Independent Re-Verification of the F-01 / F-02 Correction to Work Package WP-05 (Access Management, C-002)

**Document ID:** VV-AUDIT-WP-05-RV
**Document Type:** Independent Remediation Re-Verification — narrowly scoped. **Not** a repeat of `VV-AUDIT-WP-05_Access_Management.md`'s full 14-phase audit, and **not** a new certification of WP-05.
**Subject:** the correction described in `architecture/05-Implementation/IMP-REPORT-WP-05_Access_Management.md` §"Correction (VV-AUDIT-WP-05, 2026-07-31)" (lines 107–131)
**Re-verification date:** 2026-07-31
**Working tree state at re-verification:** `master`, five WP-05 source/test files **modified but uncommitted** (`git status` confirmed — see §2.1). The correction is *not* in any commit; it exists only in the working tree.

**Reviewer posture:** Independent. No involvement in WP-05's design, implementation, original certification (`CERT-WP-05`), the V&V audit that found F-01/F-02 (`VV-AUDIT-WP-05`), or the remediation now being re-verified. Every claim in `IMP-REPORT-WP-05`'s Correction section was treated as an unproven hypothesis and re-derived against actual source, actual test execution, and purpose-built probes written from scratch for this re-verification.

---

## 1. Determination

### **CONFIRMED WITH OBSERVATIONS.**

Both High-severity, `CLAUDE.md §19.8.5`-class defects are **genuinely fixed**. The fixes were verified structurally (by reading the code), behaviourally (by 24 independent probe checks written from scratch, not adapted from the existing suite), and by a **negative control** proving those same probes reproduce both original defects when run against the pre-fix code extracted from `git HEAD`. The full AuthService suite passes at **608/608** with zero regressions, independently re-executed.

Four minor, non-blocking observations are recorded in §7. **None blocks restoring `CLOSED — CERTIFIED`**; all are documentation-level and one is incidental to WP-05 entirely.

---

## 2. Method

### 2.1 Working-tree state independently confirmed

```
$ git status --short
 M Backend/Services/AuthService/repositories/access_evaluation_outcome_repository.py
 M Backend/Services/AuthService/routers/access_evaluation.py
 M Backend/Services/AuthService/services/access_evaluation_service.py
 M Backend/Services/AuthService/tests/test_access_evaluation_api.py
 M Backend/Services/AuthService/tests/test_access_evaluation_service.py
 M architecture/00-Governance/DOC-000_Documentation_Catalogue.md
 M architecture/00-Governance/WP-REG-001_Enterprise_Work_Package_Register.md
 M architecture/00-Governance/WPR-001_Work_Package_Roadmap.md
 M architecture/05-Implementation/IMP-REPORT-WP-05_Access_Management.md
 M architecture/06-Reviews/CERT-WP-05_Access_Management.md
 M architecture/06-Reviews/TECH-DEBT.md
?? architecture/06-Reviews/VV-AUDIT-WP-05_Access_Management.md
```

`IMP-REPORT-WP-05` line 195's claim ("Not yet committed … remain staged in the working tree") is **accurate**.

```
$ git diff HEAD --stat -- Backend/Services/AuthService/
 .../access_evaluation_outcome_repository.py        |  28 ++-
 .../AuthService/routers/access_evaluation.py       |  10 +-
 .../services/access_evaluation_service.py          |  52 +++--
 .../tests/test_access_evaluation_api.py            | 210 +++++++++++++++------
 .../tests/test_access_evaluation_service.py        | 203 ++++++++++++++++----
 5 files changed, 385 insertions(+), 118 deletions(-)
```

The production-code change is small and localized — 90 changed lines across three files, of which the substantive logic change is roughly 20 lines. No model, migration, schema, `main.py`, or `middleware/tenant.py` change accompanies it, consistent with the claim that no new migration was required.

### 2.2 What was executed

| Activity | Evidence location |
|---|---|
| Full AuthService suite re-run | §5 |
| WP-05 suite re-run and test-count verification | §5 |
| Independent probe suite (24 checks), written from scratch | §3.2, §4.2, §6 |
| **Negative control** — same probes against pre-fix `HEAD` code | §3.3, §4.3 |
| Full read of `evaluate()`, `get_active_domain_approval_authority()`, all five router handlers | §3.1, §4.1, §6.1 |
| Full read of `git diff HEAD` for the three production files | §6 |
| Read of the existing regression tests' own code (not just their names) | §3.4, §4.4, §6.3 |
| Governance-document spot-check | §7 |

The probe suite deliberately builds its **own** engines, sessions, and seed data and imports nothing from `Backend/Services/AuthService/tests/`. This matters: `VV-AUDIT-WP-05 §9.5` established that the existing fixtures were themselves the blind spot that let both defects reach a certified state, so re-verifying through those same fixtures would beg the question.

---

## 3. F-01 — Orphan foreign key on the UNRESOLVED branch

### 3.1 Structural verification (code read)

`Backend/Services/AuthService/services/access_evaluation_service.py`, `evaluate()`, lines 66–193. The branch order is now:

| Lines | Behaviour |
|---|---|
| 98–110 | Domain does not exist → `record_audit(...DENIED)` → **404**. Pre-existing, unchanged. |
| **112–124** | **Membership does not exist → `record_audit(...DENIED)` → 404. New (F-01 fix).** |
| 126–149 | Membership exists **and** `membership_status != "ACTIVE"` → create `UNRESOLVED`, flush, audit, publish, return. |
| 151–177 | Organization-scoped Approval Authority found → create `DEFERRED`, flush, audit, publish, return. |
| 179–193 | Otherwise → `record_audit(...DENIED)` → **501**. |

**The critical structural property holds:** the `return`-less `raise HTTPException(404)` at line 121–124 precedes the *only* two `self.outcome_repo.create(...)` call sites in the entire repository (lines 128 and 155). There is **no** `try`/`except IntegrityError` anywhere in the file, and none is needed — the bad write is never attempted rather than being attempted and caught. This is the audit's Recommendation R-01 option (a), implemented as specified.

The UNRESOLVED branch's guard is now `if membership.membership_status != "ACTIVE":` (line 126), evaluated only on a `membership` object already proven non-`None`. Its payload's `"membership_id": request.membership_id` (line 130) is therefore always an id that resolves to a real `memberships` row. **The row-write-under-invalid-FK scenario is structurally unreachable**, not merely untested.

### 3.2 Independent probe — FK enforcement ON

Probe written from scratch (`rv_probe.py`, probe 1). Own engine; `PRAGMA foreign_keys=ON` installed via `sqlalchemy.event.listens_for(engine.sync_engine, "connect")`, exactly as `VV-AUDIT-WP-05 §9.6` did. The pragma was **asserted in effect**, not assumed.

```
=== PROBE 1 (F-01): FK enforcement ON, unknown membership_id ===
[PASS] 1a PRAGMA foreign_keys is ON
        PRAGMA foreign_keys = 1
[PASS] 1b unknown membership_id -> HTTP 404 (not IntegrityError, not 201)
        raised=('HTTPException', 404, "No membership found with id 'bf7845b3-...-c76384e5a99b'.")
[PASS] 1c no access_evaluation_outcomes row written
        row count before=0 after=0
[PASS] 1d UNRESOLVED still produced for real non-ACTIVE membership under FK ON
        outcome_type=UNRESOLVED membership_id=9c663654-... reason="Membership standing is not
        ACTIVE (current standing: 'SUSPENDED')."
[PASS] 1e persisted outcome's membership_id resolves to a real Membership
        rows=1 membership resolved=True
[PASS] 1f DEFERRED branch still works under FK ON (same-org authority)
        outcome_type=DEFERRED approval_authority_id=da7964e0-...
[PASS] 1g unknown domain -> 404
        status=404
```

Checks `1c` and `1e` go beyond what the in-suite regression test asserts: `1c` counts rows in `access_evaluation_outcomes` directly (confirming the *absence* of a write, not merely the presence of a 404), and `1e` resolves the persisted row's `membership_id` back to a live `Membership` object.

### 3.3 Negative control — the probe against pre-fix code

A probe that passes against the fix proves nothing unless it also **fails** against the defect. The pre-fix sources were extracted read-only (`git show HEAD:...` into the scratchpad, working tree untouched) and loaded as standalone modules:

```
=== NEGATIVE CONTROL 1 (F-01) against PRE-FIX HEAD code, FK enforcement ON ===
  PRAGMA foreign_keys = 1
  RESULT: pre-fix code raised IntegrityError -> DEFECT REPRODUCED
          (sqlite3.IntegrityError) FOREIGN KEY constraint failed
```

This exactly reproduces `VV-AUDIT-WP-05 §9.6`'s original finding, from an independently written probe. The probe is therefore demonstrably capable of detecting F-01, and its passing against the working-tree code is meaningful evidence.

### 3.4 The in-suite regression test, read rather than trusted

`tests/test_access_evaluation_service.py:228–293`, `test_evaluate_unknown_membership_writes_no_row_under_foreign_key_enforcement`. Read line by line. It does what its name claims: it creates its own `create_async_engine("sqlite+aiosqlite:///:memory:")`, registers a real `@event.listens_for(engine.sync_engine, "connect")` pragma listener (`:241–245`), seeds through that engine's own session factory, asserts 404 (`:268–270`), and then additionally proves the DEFERRED path still works under FK enforcement (`:272–289`). It is a genuine test, not a name-only one.

Two minor notes (Observation O-3, §7): it does not itself assert a zero row count despite `writes_no_row` in its name — it infers this from the 404. My probe check `1c` closes that gap independently. It also declares an unused `seeded_membership_and_domain` fixture parameter (`:229`).

### 3.5 The structural test-seeding problem is also resolved

`VV-AUDIT-WP-05 §1.3` observed that **16 of 29 tests** were seeded through the production-impossible phantom-membership path. Both suites now seed via a genuinely-existing `SUSPENDED` Membership: `tests/test_access_evaluation_service.py:56–81` (`_seed_unresolved_outcome`) and `tests/test_access_evaluation_api.py:104–130` (`seeded_unresolved_outcome_id`, `membership_status="SUSPENDED"` at `:124`). Downstream BA-02/03/04 tests therefore now exercise a production-reachable state.

**F-01: FIXED. Verified structurally, behaviourally, and by negative control.**

---

## 4. F-02 — Cross-organization Approval Authority selection

### 4.1 Structural verification (code read)

`Backend/Services/AuthService/repositories/access_evaluation_outcome_repository.py:17–49`:

- Signature is now `get_active_domain_approval_authority(self, domain_id: uuid.UUID, organization_id: uuid.UUID)` (`:17–19`). `organization_id` is **positional and required** — not optional with a `None` default, so no caller can silently omit it and reintroduce the defect. The type annotation is `uuid.UUID`, not `uuid.UUID | None`.
- `ApprovalAuthority.organization_id == organization_id` is in the `WHERE` clause (`:43`), alongside the pre-existing `domain_id` (`:42`), `scope_type == "DOMAIN"` (`:44`), and `status == "ACTIVE"` (`:45`) filters — all four retained.
- `.order_by(ApprovalAuthority.created_at, ApprovalAuthority.id)` added (`:47`), replacing the previously-unordered `.first()` (audit F-02 item 3).

`services/access_evaluation_service.py:151–153` passes `membership.organization_id` — the *requesting Membership's own* organization, read from the Membership object already loaded and proven non-`None` at `:112`. It is not taken from the request body, from a header, or from the Domain, so it cannot be caller-influenced.

A repository-wide grep confirms exactly **two** references to this method — its definition and that single call site — so no other caller exists that could have been left on a stale signature:

```
$ grep -rn "get_active_domain_approval_authority" --include=*.py Backend/
Backend/Services/AuthService/repositories/access_evaluation_outcome_repository.py:17
Backend/Services/AuthService/services/access_evaluation_service.py:151
```

### 4.2 Independent two-organization probe

Constructed from scratch: Organization A, Organization B, a platform-shared `Domain` with `organization_id is None` (asserted, so the probe genuinely exercises the shared-reference-data condition the defect depended on), a Membership in Org A, and an ACTIVE DOMAIN-scoped `ApprovalAuthority` named `"TENANT-B CONFIDENTIAL APPROVAL BOARD"` owned by Org B against that same Domain.

```
=== PROBE 2 (F-02): two-organization cross-tenant Approval Authority ===
[PASS] 2a repository lookup for Org A returns None while only Org B holds an authority
        selected=None
[PASS] 2b Org A membership -> HTTP 501, never DEFERRED to Org B's authority
        result=HTTP 501
[PASS] 2c no row persisted and Org B's authority name never leaks
        rows before=0 after=0; leak of 'TENANT-B' in response = False
[PASS] 2d same-org DEFERRED branch still correct after the fix
        outcome_type=DEFERRED aa_id=eef11925-... (org_a aa=eef11925-..., org_b aa=907b04dd-...)
        reason="Governed by Approval Authority 'ORG-A OWN BOARD' (eef11925-...); resolution
        pending approval."
[PASS] 2e Org B membership defers to Org B's own authority (no over-narrowing)
        outcome_type=DEFERRED aa_id=907b04dd-... expected=907b04dd-...
[PASS] 2f RETIRED authority in own org is not selected (status filter intact)
        selected=None
[PASS] 2g GLOBAL-scoped authority in own org is not selected (scope filter intact)
        selected=None
```

Checks `2d`, `2e`, `2f` and `2g` exist specifically to test for **over-narrowing** — the most likely way a tenant-isolation fix introduces a new defect. They confirm the fix isolates rather than disables: Org A's own authority is still selected for Org A (`2d`), Org B's own authority is still selected for Org B (`2e`), and the pre-existing `status`/`scope_type` filters are untouched (`2f`, `2g`).

### 4.3 Negative control

```
=== NEGATIVE CONTROL 2 (F-02) against PRE-FIX HEAD code, two organizations ===
  Membership organization_id : 09a3dd1c-9dd4-42c9-a09e-95c5b55680b6 (Org A)
  Selected AA organization_id: 7271e506-b796-4518-bc29-24f7f0979da0 (Org B)
  outcome_type               : DEFERRED
  approval_authority_id      : 1b65c0dd-f9be-437d-9e48-7532120a6de9
  reason (persisted+returned): Governed by Approval Authority 'TENANT-B CONFIDENTIAL
                               APPROVAL BOARD' (1b65c0dd-...); resolution pending approval.
  CROSS-TENANT LEAK          : True
```

Byte-for-byte the shape of `VV-AUDIT-WP-05 §8.6`'s original finding, reproduced by an independently written probe against the pre-fix code, and **not** reproduced against the corrected code.

### 4.4 Determinism

`VV-AUDIT-WP-05 §8.6` item 3 recorded the unordered `.first()` as a third distinct defect. Probe 3 seeds four ACTIVE, same-org, same-domain authorities with `created_at` values deliberately inserted in reverse order:

```
=== PROBE 3: deterministic ORDER BY on multiple ACTIVE same-org authorities ===
[PASS] 3a selection is stable across repeated calls
        distinct selections=1
[PASS] 3b selection is the earliest created_at (deterministic ORDER BY)
        selected=6c991089-... earliest=6c991089-... (Board 3)
```

Selection is stable across five consecutive calls and resolves to the genuinely-earliest `created_at`, not to insertion order.

**F-02: FIXED, including the determinism sub-finding. Verified structurally, behaviourally, and by negative control. No over-narrowing.**

---

## 5. Regression — full suite

Executed independently, from `Backend\Services\AuthService`, with `JWT_SECRET_KEY=ci-test-secret-key-not-for-production`:

```
$ venv/Scripts/python.exe -m pytest tests/ -q
608 passed, 47 warnings in 254.03s (0:04:14)
```

**608 passed, 0 failed, 0 errors, 0 skipped.** This independently confirms `IMP-REPORT-WP-05` line 165's claim of 608/608. The 47 warnings are all pre-existing `HTTP_422_UNPROCESSABLE_ENTITY` deprecation warnings from Starlette/FastAPI across WP-02/WP-03 files, unrelated to this correction.

WP-05's own two files, and their collected counts:

```
$ pytest tests/test_access_evaluation_service.py tests/test_access_evaluation_api.py -q
36 passed, 2 warnings in 22.07s

$ pytest tests/test_access_evaluation_service.py --collect-only -q   → 17 tests collected
$ pytest tests/test_access_evaluation_api.py     --collect-only -q   → 19 tests collected
```

**17 unit + 19 API = 36**, exactly as `IMP-REPORT-WP-05` line 164 and `WP-REG-001` line 92 both state.

---

## 6. No new defect introduced

The full `git diff HEAD` for the three production files was read. It contains **no** change beyond the three fixes and their docstrings.

### 6.1 F-03 — audit actor attribution (checked as briefed)

All five handlers in `routers/access_evaluation.py` now pass the authenticated caller's own claim:

| Line | Handler | Call |
|---|---|---|
| 88 | `evaluate_access` | `service.evaluate(request, actor_id=claims.get("person_id"))` |
| 114 | `preserve_access_evaluation_outcome` | `service.preserve(outcome_id, actor_id=claims.get("person_id"))` |
| 136 | `expire_access_evaluation_outcome` | `service.expire(outcome_id, actor_id=claims.get("person_id"))` |
| 166 | `detect_access_context_change` | `service.detect_context_change(outcome_id, request, actor_id=claims.get("person_id"))` |
| 190 | `resolve_access_handoff_rejection` | `service.resolve_handoff_rejection(outcome_id, request, actor_id=claims.get("person_id"))` |

The diff shows all five were previously without it. This matches the 51-occurrence convention across the service's other 15 routers that `VV-AUDIT-WP-05 §8.8` documented. Independently probed end-to-end against the real emitted log record:

```
=== PROBE 5 (F-03): actor_id threading ===
[PASS] 5a actor_id reaches the emitted audit record
        records=1; contains actor=True; contains SYSTEM=False
```

The `actor_id or "SYSTEM"` fallback is retained in the service (correctly — it remains the right default for a genuinely system-initiated call), but it is no longer reached from the API surface.

### 6.2 Previously-correct behaviour preserved

Independently re-confirmed, all under FK enforcement ON:

| Behaviour | Probe | Result |
|---|---|---|
| Unknown Domain → 404 (evaluated first) | 1g | 404 |
| Real non-ACTIVE Membership → UNRESOLVED | 1d, 4a | `UNRESOLVED` / `CREATED` |
| Same-org authority → DEFERRED, correct `approval_authority_id` | 1f, 2d | correct authority |
| No governing authority → 501, never a fabricated decision | 2b | 501 |
| BA-02 `CREATED → PRESERVED` | 4b | `PRESERVED` |
| BA-02 double-preserve → 409 | 4c | 409 |
| BA-02 expire on non-PRESERVED → 409 | 4g | 409 |
| BA-03 invalidates a live outcome | 4e | `invalidated=True`, `re_evaluation_required=True` |
| BA-04 live outcome → `CAPABILITY_SCOPED_INSUFFICIENCY`, preserved | 4d | correct |
| BA-04 non-live outcome → `INTEGRITY_SIGNAL`, routed to BA-01 | 4f | correct |

BA-02, BA-03 and BA-04 are **untouched by the diff** (their service methods appear nowhere in it beyond the `actor_id` parameter that was already present in their signatures), and probe 4 confirms all three still function correctly against an outcome created through the *corrected* BA-01 path.

### 6.3 Regression tests read, not trusted

- `test_access_evaluation_service.py:103–121` — asserts 404 for a phantom `membership_id`. Genuine.
- `test_access_evaluation_service.py:168–205` — seeds a real second Organization and an Org-B authority against the same Domain, asserts 501 and that `"ORG-B"` does not appear in the detail. Genuine.
- `test_access_evaluation_api.py:145–157` — API-layer 404 for unknown membership. Genuine.
- `test_access_evaluation_api.py:177–190` — API-layer cross-org case, asserts 501 and `"ORG-B" not in response.text`. Genuine.
- `test_access_evaluation_api.py:249–272` — parses the real emitted JSON audit records from `caplog` and asserts every one carries the token's `person_id` and none carries `"SYSTEM"`. Genuine, and stronger than a mere call-argument assertion.

### 6.4 Probe summary

```
TOTAL CHECKS: 24   PASSED: 24   FAILED: 0
```

**No new defect found.**

---

## 7. Observations (non-blocking)

None of the following blocks restoring `CLOSED — CERTIFIED`.

**O-1 — `TECH-DEBT.md` TD-085 contains an incorrect cross-reference.** `architecture/06-Reviews/TECH-DEBT.md:1061` (TD-085 Detailed Entry, Description) reads: *"the audit log (itself anonymized per the now-resolved `TD-086`-class gap, see below)"*. `TD-086` is the `CMD-001 §26.7` Physical Implementation Mapping gap, its Status is **Open**, and it has nothing to do with audit-log anonymization. The anonymization issue is `VV-AUDIT-WP-05` **F-03**, which was fixed directly and correctly never registered as a Technical Debt item (per `CLAUDE.md §19.8.5` it was not deferrable). The sentence should reference F-03, not TD-086. Cosmetic; no register field (Status, Severity, Priority, Owner) is wrong.

**O-2 — `routers/access_evaluation.py:78`'s OpenAPI `404` description is now incomplete.** It reads `404: {"description": "The target Domain does not exist."}`. Since the F-01 fix, `POST /access-evaluations` also returns 404 for an unknown `membership_id` (`services/access_evaluation_service.py:121–124`), which this description does not mention. This is the same *class* of cosmetic OpenAPI gap already registered as `TD-089`, but it is **not covered by** `TD-089`'s own text, which is scoped to the four sub-resource endpoints omitting 400/401/403. Runtime behaviour is correct; only the generated documentation is understated.

**O-3 — the F-01 regression test does not itself assert the row count its name claims.** `tests/test_access_evaluation_service.py:228–293`, `test_evaluate_unknown_membership_writes_no_row_under_foreign_key_enforcement`, asserts 404 and infers "writes no row" from it. It does not query `access_evaluation_outcomes`. The inference is sound given §3.1's structural argument, and this re-verification's probe check `1c` asserts the row count directly and independently, so the property is proven — but the test's own assertion is weaker than its name. The same test also declares an unused `seeded_membership_and_domain` fixture parameter (`:229`), which needlessly instantiates the shared FK-*disabled* engine alongside its own FK-enabled one. Neither issue affects correctness.

**O-4 — incidental, outside WP-05.** `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md:42` (the `WP-RTA-001` row) is internally self-contradictory: it opens *"**CERTIFIED WITH CONDITIONS** — both Blocking Conditions now resolved (`CERT-WP-RTA-001`, `ADR-016`)"* and later in the same cell states *"**Not yet independently reviewed or certified; not committed**"*. This predates and is unrelated to the WP-05 correction; recorded only because it was encountered during §8's spot-check.

---

## 8. Governance-document consistency spot-check

| Document | Checked | Result |
|---|---|---|
| `WP-REG-001` | §§ lines 13, 68–74, 92, 101–105, 124, 136, 154–158, 171–180 | **Consistent.** WP-05 recorded as *Certified — Remediation Applied, Re-Verification Pending* in every location, never as Closed. Excluded from the Closed count (6), the Certified count (5), the completed-BA count (36/38 = 94.7%), and removed from the Closed table (line 124) with an explicit reason. Test count 608/608 and 36 tests stated consistently. Lifecycle-history row at line 158 accurately records the transition *Certified (Closed) → Certified — Remediation Applied, Re-Verification Pending* with its cause. |
| `WPR-001` | lines 30, 44 | **Consistent.** WP-05 row records the same qualified status, states that `CERT-WP-05` was "superseded in substance" by `VV-AUDIT-WP-05`, describes F-01/F-02 accurately (including that F-01 manifests as HTTP 500 on PostgreSQL and F-02 as a cross-tenant disclosure), and correctly conditions the return to `CLOSED — CERTIFIED` on a further independent reviewer. 608/608 and 36 tests match. Line 44's WP-05 cross-reference is likewise consistent. (See O-4 for an unrelated defect elsewhere in this file.) |
| `TECH-DEBT.md` | TD-079 – TD-089, summary table lines 109–119 + Detailed Entries lines 956–1140 | **Consistent, with O-1.** All eleven entries carry the six `CLAUDE.md §19.8.2` mandatory fields plus a `§19.8.7` Severity. `TD-081` now has a Detailed Entry with `Severity: Low` (F-10 addressed) and Status `Closed`. `TD-082`–`TD-089` are Open with correct `VV-AUDIT-WP-05` F-08/F-09/F-11/F-12/F-13/F-15/F-19/F-21 sourcing. Correctly, **neither F-01 nor F-02 appears in the register** — both were `§19.8.5`-ineligible for deferral and were remediated directly, exactly as `IMP-REPORT-WP-05` line 120 states. `TD-081`'s "601/601 at closure" is a historical statement about its own closure date and is not in conflict with the current 608. |
| `DOC-000` | lines 252, 259, 265 | **Consistent.** Certification Reports index now lists `CERT-WP-05` (7 issued: 6 PASS WITH OBSERVATIONS + 1 CERTIFIED WITH CONDITIONS — arithmetic checks out), with a note that `CERT-WP-05` did not survive re-verification. `VV-AUDIT-WP-05` has its own row (line 259) correctly typed as a V&V Audit distinct from certification. Implementation Reports row (line 265) correctly reads "6 issued (4 Closed, 1 Certified-conditions-resolved, 1 under correction per `VV-AUDIT-WP-05`)". F-05 is addressed. |
| `IMP-REPORT-WP-05` | Correction section, lines 107–131; Validation, lines 162–177; Status, lines 181–195 | **Accurate.** Every substantive claim in the Correction section was independently re-derived and holds: the 404-before-INSERT shape, the organization-scoped lookup with deterministic ordering, the five `actor_id` threadings, 36 tests, 608/608, and the uncommitted working-tree state. Line 122's refusal to self-certify the remediation, and the resulting *Re-Verification Pending* status, are correct process under `CLAUDE.md §19.7` — and this document is that re-verification. |

---

## 9. Conclusion and recommendation

Both `CLAUDE.md §19.8.5`-class defects are genuinely and completely remediated:

- **F-01** — the invalid-FK write is now **structurally unreachable**, not merely caught. Confirmed under real SQLite foreign-key enforcement by an independent probe, and confirmed by negative control to be a real change in behaviour rather than a probe artifact.
- **F-02** — the Approval Authority lookup is now organization-scoped with a required (non-defaultable) parameter and a deterministic ordering. Confirmed by an independent two-organization probe that also proves the fix does not over-narrow: same-organization DEFERRED still works for both organizations, and the pre-existing `status`/`scope_type` filters remain intact.
- **F-03** — actor attribution reaches every audit record; verified against the real emitted log output.

No regression: **608/608** independently re-executed. No new defect found in the diff. The four observations in §7 are documentation-level and non-blocking; O-1 and O-2 are worth a one-line correction whenever `TECH-DEBT.md` and the router's OpenAPI map are next touched, and O-4 is outside WP-05 entirely.

**Recommendation: WP-05's `CLOSED — CERTIFIED` status may be restored** in `WP-REG-001` and `WPR-001`, subject to the repository owner's own commit decision (the correction remains uncommitted — `IMP-REPORT-WP-05` line 195). This satisfies `VV-AUDIT-WP-05` Recommendation R-03 and `CLAUDE.md §19.7`'s fresh-context reviewer requirement.

### Statement of independence

This re-verification was performed by a reviewer with no involvement in WP-05's design, implementation, original certification, the V&V audit, or the remediation. Every conclusion above rests on source code read in full, tests executed and their output recorded verbatim, and probes written from scratch and validated by negative control against the pre-fix code. No claim was accepted from `IMP-REPORT-WP-05`, `CERT-WP-05`, or `VV-AUDIT-WP-05` without independent re-derivation. No repository file was modified by this re-verification other than this report; nothing was committed.

---

**Document status:** Complete
**Determination:** **CONFIRMED WITH OBSERVATIONS**
**Independent checks executed:** 24 probe checks + 2 negative controls + 608 suite tests, 0 failures
