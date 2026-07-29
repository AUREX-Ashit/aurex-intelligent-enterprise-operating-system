# CERT-WP-01A — Independent Certification (Corrective)

## Organization Management (C-004) — Constitutional Correction

**Certification Type:** Independent Corrective Certification (CLAUDE.md §19.7, "Independent Certification" — applied to a corrective sub-package, same discipline as an original WP-level certification)
**Work Package:** WP-01A — Organization Management Constitutional Correction (C-004), corrective sub-package of WP-01
**Replaces (for BA-01/BA-01B/BA-01C only):** `CERT-WP-01_Organization_Management.md`. That certification's findings for BA-02 through BA-07 are **not superseded** and remain the certified record for those Business Activities — this document does not re-review or re-certify them.
**Certifying party:** Independent certifier, fresh-context, no participation in this correction's implementation. Performed per CLAUDE.md's explicit prohibition on self-certification.
**Date:** 2026-07-29
**Inputs certified against:** `IRA-001A_WP-01_Organization_Establishment_Activation_Correction.md`, `IMP-REPORT-WP-01_Organization_Management.md`'s IRA-001A section, `TECH-DEBT.md` (TD-046–TD-049), the canonical `PE-001-C004_Organization_Management.docx`, actual source code, actual test execution, actual migration state, actual git history, and `CERT-WP-01_Organization_Management.md` itself (the certification being partially replaced).

---

## 1. Executive Summary

This corrective certification covers exactly three Business Activities: **BA-01 (amended) — Establish Organization Identity**, **BA-01B (new) — Verify Organization Domain Claim**, and **BA-01C (new) — Activate Organization, first-time**. BA-02 through BA-07 are unaffected by this correction and remain certified under CERT-WP-01's own original findings — confirmed by direct diff: none of their service methods, routers, or business logic changed.

**CERT-WP-01's own Finding A** stated that ERB-C004-02/ERB-C004-03's absence was "not a functional defect — nothing in the implemented code is internally inconsistent or broken," and classified it as a documentation/traceability defect in IRA-001/IMP-REPORT-WP-01. **This certification does not accept that classification.** Independent re-derivation from PE-001-C004's own unconditional text — BR-C004-01 ("An Organization SHALL NOT be treated as valid before governed activation"), BR-C004-08 ("An Organization Anchor Context SHALL NOT be treated as... an Authoritative Organization Context... under any circumstance"), and Contract 5.4 ("Prior to activation, no Organization exists in this sense") — establishes that `establish()`'s original behavior (writing `status=ACTIVE` unconditionally, with no distinguishable governed-activation act) was a genuine, unconditional Business Rule non-conformance, present in code that existed at CERT-WP-01's own certification time, not merely an inaccurate claim about which ERBs a document says are realized. CLAUDE.md §19.8.5 does not permit deferring an architectural/Business-Rule non-conformance of this kind via Technical Debt registration alone, which is the disposition CERT-WP-01's own Recommendation 2 pointed toward.

Independent re-verification of the correction itself confirms:

- **469/469 backend tests pass** (re-run independently), **exactly one Alembic head** (`e5c1a9f4b7d2`), and a **linear, purely-additive migration chain** (the new migration alters no existing table).
- `establish()` no longer writes to `organizations` under any circumstance — confirmed by direct grep (`organization_repo.create` appears exactly once in `organization_service.py`, inside `activate_establishment`).
- `activate_establishment()`'s precondition gate (a `VERIFIED` domain claim or an explicit, non-whitespace `no_domain_activation_reason`) has no bypass path — traced by hand through every branch.
- BA-02 (`get_details()`) and BA-03 (`search()`) reference the new `organization_establishment_attempts` construct nowhere — confirmed by grep and full diff review; their behavior is unchanged.
- No file outside this correction's own change set references `organization_establishment_attempts` — the exact leak this correction exists to prevent does not exist anywhere in the repository.
- Every Technical Debt item this correction raises (TD-046–TD-049) is genuinely registered in `TECH-DEBT.md`, not left in review prose.

One **inherited, not newly introduced** finding is reconfirmed: **TD-047**, `MembershipService.establish()` (WP-03) deriving Organization existence via direct repository access rather than any C-004-owned resolution authority (BR-C004-03). This predates IRA-001A (WP-03 was built 2026-07-29, after WP-01's own certification) and is correctly out of this correction's ownership — `membership_service.py` was not touched. It does not block this certification; it is WP-03's own open item, disclosed here for completeness since it bears directly on the same Business Rule this correction exists to satisfy.

## 2. Certification Decision

**CERTIFIED – PASS WITH OBSERVATIONS**

---

## 3. Scope Reviewed

**Governance documents:**
- `CLAUDE.md` §14, §16, §17, §19.1–§19.8 (full)
- `architecture/05-Implementation/IRA-001A_WP-01_Organization_Establishment_Activation_Correction.md` (full)
- `architecture/05-Implementation/IMP-REPORT-WP-01_Organization_Management.md`'s IRA-001A section (the BA-02–BA-07 sections above it were not re-reviewed — already certified under CERT-WP-01)
- `architecture/06-Reviews/TECH-DEBT.md` (TD-046–TD-049 in full, plus re-confirming TD-001–TD-045 were not altered)
- `docs/Product/PE-001/capabilities/C-004/PE-001-C004_Organization_Management.docx` — re-extracted and re-read against BR-C004-01, BR-C004-02, BR-C004-08, BR-C004-09, Contract 5.1, 5.2, 5.4, ERB-C004-01/02/03, EX-C004-01 through EX-C004-04, §1.16–§1.18, §9.6, §9.7
- `architecture/06-Reviews/CERT-WP-01_Organization_Management.md` (full — the certification being partially replaced, its Finding A specifically re-derived against primary text rather than accepted)
- `architecture/07-Decisions/ADR-003/004/005` (re-confirmed unaffected — none required amendment; the new table is purely additive, the same disposition class ADR-004 already pre-authorizes)

**Source code read in full:**
- `Backend/Services/AuthService/models/organization_establishment_attempt.py`
- `Backend/Services/AuthService/services/organization_service.py` (all methods, including the five unmodified ones)
- `Backend/Services/AuthService/routers/organization.py`, `routers/organization_establishment_attempt.py`
- `Backend/Services/AuthService/repositories/organization_establishment_attempt_repository.py`
- `Backend/Services/AuthService/alembic/versions/2026_08_02_0900-e5c1a9f4b7d2_organization_establishment_attempt.py`
- `Backend/Services/AuthService/middleware/tenant.py`, `main.py`
- `Backend/Services/AuthService/tests/test_organization_service.py`, `tests/test_organization_api.py` (both in full)

**Commands actually executed (not assumed):**
- `pytest -q` (with `JWT_SECRET_KEY` set) → **469 passed, 0 failed**
- `alembic heads` → one head (`e5c1a9f4b7d2`)
- `python -c "from main import app; app.openapi()"` → 60 paths, generated successfully
- `python -c "import yaml; yaml.safe_load(...)"` against both `organization-api.yaml` and `organization-establishment-attempt-api.yaml` → valid
- `git status`, `git diff --stat`, targeted `grep` across the full `Backend/Services/AuthService` tree

---

## 4. Findings

### 4.1 Architecture

- **No architecture redefinition beyond what IRA-001A itself scoped and disclosed.** One new table (`organization_establishment_attempts`), purely additive — confirmed by reading the migration's `upgrade()` in full: only `create_table`/`create_foreign_key`/`create_check_constraint`/`create_index`, no `ALTER`/`DROP` touching any existing table.
- **`organizations`' own shape is untouched** — confirmed `models/organization.py` has an empty diff.
- **ADR-003/004/005 honored, not re-litigated** — the new table's additive nature falls squarely within ADR-004's own pre-authorized pattern ("Future work packages that need a deferred field extend the table additively; this ADR pre-authorizes that pattern rather than requiring a new ADR each time").
- **BR-C004-08 satisfied by construction, re-verified directly:** grepped the entire `Backend/Services/AuthService` tree for `organization_establishment_attempt` — the only files referencing it are the new/modified files themselves. No stray query anywhere else could return an Anchor row and represent it as an Organization.

### 4.2 Business Activities (BA-01 amended, BA-01B, BA-01C)

- **`establish()` (BA-01, amended):** read in full (`organization_service.py:89-180`). Writes only via `organization_establishment_attempt_repo.create`; the pre-check now correctly queries both `organizations.get_by_code()` and the new repository's own `get_by_code()`, closing the shared-namespace requirement (BR-C004-01's own "one Anchor per establishment thread" implies no code collision across either table). `IntegrityError` handling mirrors the original establish()'s own proven pattern.
- **`verify_domain_claim()` (BA-01B):** read in full. Correctly rejects 404 (not found), 409 (already activated), 409 (no domain was claimed — nothing to verify). Records `VERIFIED`/`UNVERIFIED` as a distinct, audited fact (`VERIFY_ORGANIZATION_DOMAIN_CLAIM` audit action, `ORGANIZATION_DOMAIN_CLAIM_VERIFICATION_RECORDED` event) — satisfies BR-C004-02/BR-C004-09's requirement that the decision be recorded, not merely proven (proof-of-control itself is disclosed as out of scope, TD-046).
- **`activate_establishment()` (BA-01C):** read in full and traced by hand. Gate at lines 322-341 (post-fix): requires `has_verified_domain` or a non-empty-after-`.strip()` `no_domain_activation_reason`; no branch reaches `organization_repo.create` (line 349) without satisfying one of these. On success, creates the Organization (identical shape to the original `establish()`'s own create call), links `activated_organization_id`, and — critically — the Anchor row is **not** deleted, satisfying PE-001-C004 §1.17's "preserved in lineage" requirement. Distinct audit action (`ACTIVATE_ORGANIZATION_ESTABLISHMENT`) and event (`ORGANIZATION_ACTIVATED_FIRST_TIME`) from BA-05's own `ACTIVATE_ORGANIZATION`/`ORGANIZATION_ACTIVATED` — confirmed by direct string comparison, no collision.
- **BA-02 through BA-07 — confirmed unaffected, not merely claimed:** diffed every one of their own methods (`get_details`, `search`, `update_profile`, `activate`, `suspend`, `retire`) against the pre-correction blob — zero behavioral difference, only pre-existing docstrings/module-level comments updated for accuracy.

### 4.3 Testing

- **469 passed, 0 failed** — re-run independently, matching the report's claim exactly.
- BA-01's own tests confirmed to assert `len(organizations) == 0` after `establish()` alone (service test) and `"status" not in body` on the establish API response — genuinely proving no Organization is created, not merely renamed assertions.
- BA-01B/BA-01C tests cover 404/409/precondition-not-met/whitespace-only-reason paths, not only the happy path.
- BA-02 through BA-07's own test bodies confirmed byte-for-byte unchanged from before this correction (only their setup fixtures were migrated to a new `_establish_and_activate` helper).

### 4.4 Documentation

- `organization-api.yaml` and the new `organization-establishment-attempt-api.yaml` both validated and confirmed to match the actual routers.
- IRA-001A's own claims (test counts, migration description, BA table) checked out against actual code and test execution, after this certification's own review corrected two documentation defects the correction's own Independent Review had already found and fixed in the same pass (a premature "Independent Review completed" claim, and a whitespace-only-reason gap) — re-verified here as genuinely resolved, not re-discovered.

### 4.5 Technical Debt

- **TD-046, TD-048, TD-049** — genuinely new, genuinely registered, correctly scoped to this correction's own disclosed limitations (no real domain-verification mechanism; BA-02 doesn't realize EX-C004-05's typed contract; frontend now calls a removed endpoint).
- **TD-047** — an inherited WP-03 finding, correctly disclosed rather than fixed inline (out of this correction's ownership boundary), and correctly not re-attributed to WP-01A as if it were a new defect this correction introduced.
- No item was found in review prose without a corresponding register entry, consistent with §19.8.2.

### 4.6 Repository

- **Working tree confirmed to touch only the expected file set** — `git diff --stat` shows exactly the model, migration, repository, schema, and router files (new); `organization_service.py`, `routers/organization.py`, `main.py`, `middleware/tenant.py`, `models/__init__.py`, `schemas/organization.py`, both test files, `organization-api.yaml`, `README.md`, `TECH-DEBT.md`, `WPR-001`, `IMP-REPORT-WP-01`, and the new `organization-establishment-attempt-api.yaml` + `IRA-001A` doc (modified/new). No WP-02/03/04 file was touched.
- Pre-existing, unrelated uncommitted files (`CLAUDE.md`, `ARM-001_Implementation_Report.md`, and the untracked AR-001/AAR-001-track documents plus one stray scratch file, `_PE-001-C005_ba02_check.txt`) confirmed unrelated to this correction and not staged with it.

---

## 5. Risks

| # | Risk | Severity | In WP-01A's boundary? | Status |
|---|---|---|---|---|
| 1 | TD-046 — BA-01B has no real proof-of-control mechanism behind its verification decision. | Low | Yes | Open, deferred until a real domain-trust consumer exists |
| 2 | TD-047 — `MembershipService` (WP-03) bypasses C-004's resolution authority, no status check. | Medium | No — WP-03's own file | Open, correctly out of this correction's remediation scope; needs WP-03's own governance action |
| 3 | TD-048 — BA-02 doesn't realize EX-C004-05's typed validity contract. | Low | Yes | Open, deferred until a real consumer needs it |
| 4 | TD-049 — Frontend Establish Organization flow now 404s until updated. | Medium | Yes (disclosure), No (remediation — backend-only scope) | Open, real and immediate, correctly disclosed rather than silently left for discovery |

None of the above is a data-integrity, tenant-isolation, or build-breaking defect within WP-01A's own boundary that CLAUDE.md §19.8.5 would require remediating before this completion gate; TD-047 is real and Medium severity but is not this correction's own defect to fix.

---

## 6. Recommendations

1. No further action is required before BA-01/BA-01B/BA-01C are considered closed under CLAUDE.md §19.7.
2. **TD-047's ownership should be formally escalated to WP-03's own governance** — this certification cannot assign WP-03 work, only flag it.
3. **TD-049 (frontend) should be scheduled** before the existing Organization Management UI is presented to a real user, to avoid a live 404 on the Establish flow.
4. This certification, together with CERT-WP-01 (for BA-02–BA-07), constitutes WP-01's complete, current certification record. WPR-001 has been updated to cite both.

---

## 7. Remediation Plan

No remediation is required to lift this certification above PASS WITH OBSERVATIONS. If the repository owner elects to act on §6:

| Item | Owner | Fix type | Suggested timing |
|---|---|---|---|
| Escalate TD-047 to WP-03 governance | Repository owner / governance | Planning decision | Before WP-03's own next Business Activity or amendment |
| Schedule TD-049 (frontend update) | Platform Admin (Frontend) | Implementation | Before the Establish Organization UI flow is next relied upon |

This certification does not implement any of the above — per its own scope, it is a review-and-report activity only. No production code, test file, or configuration was modified during this certification.
