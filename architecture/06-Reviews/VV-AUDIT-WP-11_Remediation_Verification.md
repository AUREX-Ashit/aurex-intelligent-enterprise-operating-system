# VV-AUDIT-WP-11 — Remediation Re-Verification: Enterprise Search (C-093)

**Work Package:** WP-11 — Enterprise Search (C-093)
**Finding remediated:** `VV-AUDIT-WP-11_Enterprise_Search.md` Finding 1 (High, `CLAUDE.md §19.8.5`-class, blocking) — no uniqueness constraint on `(organization_id, index_name)` in `vector_index_registry`; `VectorIndexRegistryRepository.get_by_name_for_caller`'s own `.scalar_one_or_none()` raises unhandled `sqlalchemy.exc.MultipleResultsFound` (bare `500`) once a caller establishes two active indexes of the same name in the same scope, breaking both BA-02 (`POST /search/query`) and BA-03 (`POST /search/content`) for that name thereafter.
**Reviewer:** Independent, fresh-context reviewer — no prior involvement in WP-11's implementation, `CERT-WP-11` (Gate 1), `VV-AUDIT-WP-11` (Gate 2), or the remediation itself.
**Gate:** 4 of 5 (`CLAUDE.md §19.7b`) — required regardless of the finding's own severity, per this repository's own established precedent (`VV-AUDIT-WP-05_Remediation_Verification.md`, `VV-AUDIT-WP-09_Remediation_Verification.md`).
**Determination:** **REMEDIATION VERIFIED — CONFIRMED. WP-11 may proceed to Gate 5.**

---

## 1. What Changed (independently read, not accepted from the implementing session's own description)

State at time of review: both files untracked (`??` in `git status`) — WP-11 has never been committed, so there is no prior commit to `git diff`/`git stash` against. The negative control (below) was therefore obtained by manually reconstructing the pre-fix state from the post-fix working tree (removing exactly the added method and the added check), not by `git stash` against history, since no such history exists yet for these two files.

- `Backend/Services/AIService/repositories/search_repository.py` — one new method added to `VectorIndexRegistryRepository`: `get_active_by_exact_scope(organization_id, index_name)`. It selects `VectorIndexRegistryModel` filtered by `index_name`, `active_flag.is_(True)`, and `organization_id == organization_id` when `organization_id is not None`, else `organization_id.is_(None)` — an **exact**-scope match (including exact `NULL` for platform-wide), distinct from `get_by_name_for_caller`'s own caller-visibility `OR NULL` fallback. Returns via `.scalar_one_or_none()` — safe here because the method's own job is to prove at most one row exists in the exact scope before a second one is created, not to resolve an already-possibly-ambiguous set.
- `Backend/Services/AIService/services/search_index_service.py` — `SearchIndexConfigurationService.establish()` now calls `get_active_by_exact_scope(target_organization_id, request.index_name)` before `index_repo.create(...)`, and raises `HTTPException(409, ...)` with a scope-described detail message if a row is already found. No schema change, no new migration, no new architecture — matches Gate 2's own suggested remediation shape exactly ("the smallest-scope fix... is application-level: reject a second active establishment... returning a handled 409 Conflict... a physical UNIQUE index is an available but not mandatory option").

This is a narrowly-scoped, application-level guard consistent with `CLAUDE.md §19.5`'s Reuse → Configure → Extend → Compose → Create discipline — it extends the existing repository/service pair rather than introducing a new table, migration, or endpoint.

## 2. Negative Control (this gate's own central requirement)

Per `CLAUDE.md §19.7b`, re-reading code and re-running the existing suite alone is insufficient — the probe/test must be shown to actually detect the original defect. Both files were manually reverted to their pre-fix state (the new `get_active_by_exact_scope` method removed from `search_repository.py`; the pre-`create()` existence check and its `HTTPException` removed from `search_index_service.py`), reproducing exactly what Gate 2's own diff description said existed before remediation. Two independent probes were run against this reconstructed pre-fix code, then the fix was restored and both re-run:

**Probe A — Gate 2's own from-scratch runtime probe (`tests/_vv_probe_wp11.py`, Probe 2).**
- Pre-fix: `P2a` (establishing two indexes of the same name under the same org) returned `201`/`201` — nothing rejected the duplicate. `P2b` and `P2c` **FAILED**: `POST /search/content` and `POST /search/query` against the ambiguous name both raised `sqlalchemy.exc.MultipleResultsFound` unhandled out of the ASGI app — the exact crash Finding 1 described. Log output: `"Exception raised during request processing: Multiple rows were found when one or none was required"`, `exception_type: MultipleResultsFound`, for both endpoints. **This independently reproduces the original defect.**
- Post-fix (fix restored): `P2b`/`P2c` now **PASS** (handled responses, no exception). `P2a` now reports its own assertion as "failed" only because its assertion text describes the *pre-fix* symptom ("establishing a second index... is accepted") — the actual observed behavior is `first=201 second=409`, i.e., the fix correctly rejects the second establishment. This is expected, correct behavior, not a regression; the probe script itself was written to document Gate 2's own finding and was not updated for the fix (consistent with `VV-AUDIT-WP-11`'s own note that the probe script is "retained... not a certified regression test").

**Probe B — the new regression test (`tests/test_search_api.py::test_establish_duplicate_index_name_in_same_scope_is_rejected_with_409`).**
- Pre-fix: `pytest tests/test_search_api.py -k duplicate_index_name -v` → **FAILED** (`assert 201 == 409`) — the test genuinely detects the pre-fix defect, not a tautology.
- Post-fix: same command → **PASSED**, along with `test_establish_same_index_name_across_platform_wide_and_tenant_scopes_is_allowed` (also PASSED).

Both probes independently confirm: (1) the pre-fix code really did crash exactly as Finding 1 described, and (2) the post-fix code closes that specific failure mode.

## 3. Post-Fix Full Regression Confirmation

Full `AIService` suite re-run independently, post-fix, from `Backend/Services/AIService`:

```
33 passed, 6 warnings, 0 failed
```

This is 33 (30 Gate-1/Gate-2-confirmed baseline + the 2 new WP-11 remediation tests + 1 already counted — see note below) with **zero regressions** to any pre-existing test, including the full Mandatory Tenant-Isolation checklist (`CLAUDE.md §21.4`) suite, `test_search_unit.py`, `test_authentication.py`, and `test_ai.py`. (Gate 2 recorded 31 passed at its own time of review, itself already 1 more than Gate 1's 30, reflecting the Implementation Report's Addendum; this gate's 33 reflects the 2 additional remediation tests added on top of that baseline — arithmetic independently checked against `test_search_api.py`'s own current test count, 17 collected in that file.)

## 4. Independent Scope Assessment (not just "the probe passes")

**Platform-wide vs. tenant-dedicated scoping, verified directly, not just via the test's name.** `get_active_by_exact_scope`'s own `organization_id == organization_id if organization_id is not None else organization_id.is_(None)` branch means:
- Two different organizations establishing the identical `index_name` are in different exact scopes (`org_a` vs. `org_b`, both non-`NULL` and unequal) — both succeed. Independently confirmed: Probe A's `P1a` (two-organization, identical-name adversarial probe) still passes `201`/`201` after the fix, unaffected — the fix does not over-broadly reject across tenants.
- The same organization establishing both a tenant-dedicated (`organization_id = org_a`) and a platform-wide (`organization_id = NULL`) index of the identical name are in different exact scopes — both succeed. Independently confirmed by directly reading `test_establish_same_index_name_across_platform_wide_and_tenant_scopes_is_allowed` (not merely trusting its name): it establishes `"scope-distinct-name"` tenant-dedicated for `ORG_A`, then establishes the identical name with `platform_wide: True` for the same caller, and asserts `201` on the second call. Re-run independently: **PASSED**.
- A genuine duplicate within the *same* exact scope (same org, same name, not platform-wide) is correctly rejected with `409`, and — the stronger check Gate 2's own regression test performs beyond the establish path alone — content registration and search against the resulting single, unambiguous index continue to work normally afterward (`registered["chunk_count"] == 1`, one search result). Independently confirmed: **PASSED**.

**New defect check — TOCTOU / check-then-insert race.** `establish()` performs `get_active_by_exact_scope()` then, if no row is found, `index_repo.create()` as two separate statements with no `SELECT ... FOR UPDATE`, no database-level `UNIQUE` constraint, and no explicit transaction isolation beyond SQLAlchemy's own session defaults. Two genuinely concurrent `POST /search/index-configurations` calls for the identical `(organization_id, index_name)` could both pass the check before either commits, reintroducing the exact duplicate-row state Finding 1 was about — this time only under real request concurrency, not the fully sequential, single-caller reachability Finding 1 itself was rated High for.

Assessed against this repository's own calibration for this defect class, `TD-118` (`architecture/06-Reviews/TECH-DEBT.md`): `TD-118` covers the materially identical shape — a check-then-insert `establish()` on a `PLATFORM_ADMIN`-gated, low-concurrency configuration-establishment endpoint, with no DB-level uniqueness constraint, rated **Medium** and accepted as deferrable specifically because "no HTTP status diverges from spec, no referentially-invalid data, and `PLATFORM_ADMIN`-only, low-concurrency establish traffic makes a real race unlikely today." `POST /search/index-configurations` is confirmed (`TD-124`, `routers/search.py`) to be `PLATFORM_ADMIN`-gated with the same low-concurrency establish-traffic profile. Gate 2's own suggested remediation shape explicitly anticipated and accepted this: "a physical UNIQUE index is an available but not mandatory option; the minimum fix does not require one." My own independent judgment concurs with that calibration: this residual race window does **not** rise to Finding 1's own blocking severity — it does not defeat BA-01's Business Intent under the traffic pattern this endpoint actually has, it produces no cross-tenant leakage (the exact-scope match still correctly isolates by organization even under a race), and it is a narrower, harder-to-trigger variant of the exact gap `TD-118` already established as Medium/deferrable precedent for. It is not, however, literally zero-risk, and is not yet recorded anywhere in `TECH-DEBT.md` for WP-11. **Recommendation, not a Gate 4 blocker:** register a new Technical Debt entry (next available ID) at Gate 5 or WP-11 closure, mirroring `TD-118`'s own text and severity shape, rather than leaving this residual gap undisclosed.

## 5. Context From Gates 1/2 (not re-litigated here)

`CERT-WP-11` (Gate 1) certified WITH OBSERVATIONS (four non-blocking: three Low, one Medium — `active_flag` default, `TD-127`-eligible, RAG double-query `TD-126`, chunking placeholder `TD-125`, persona-gating `TD-124`). `VV-AUDIT-WP-11` (Gate 2) found Finding 1 (this gate's own subject, now remediated) and Finding 2 (Low, `active_flag` default deviation, `TD-127`-eligible, not blocking). Neither is re-verified again here — this gate's focus is exclusively the Finding 1 remediation and whether it introduces anything new, per `CLAUDE.md §19.7b`'s own Gate 4 scope.

## 6. Determination

Both negative controls (Gate 2's own from-scratch probe and the new regression test) independently confirmed the pre-fix code crashes exactly as Finding 1 described, and both confirmed the post-fix code closes that specific failure mode with no observed regression across the full 33-test suite. The fix is correctly scoped — platform-wide and tenant-dedicated scopes remain independently nameable, cross-tenant isolation is preserved, and the fix follows Gate 2's own suggested minimum-scope remediation shape. One residual, non-blocking concurrency gap (check-then-insert race, no DB-level uniqueness constraint) was independently identified and assessed against this repository's own `TD-118` precedent as Medium/deferrable, not a new blocking defect — recommended for Technical Debt registration at Gate 5/closure, not a reason to withhold this gate's own verification.

**No `CLAUDE.md §19.8.5`-class defect survives in the fix itself. Gate 4 passes. WP-11 may proceed to Gate 5 (Release Readiness Audit).**

---

*End of VV-AUDIT-WP-11_Remediation_Verification. See Gate 5 (Release Readiness Audit) for final release-readiness confirmation, including governance-document accuracy and the recommended new Technical Debt registration for the residual concurrency gap noted in §4, before WP-11 closure.*
