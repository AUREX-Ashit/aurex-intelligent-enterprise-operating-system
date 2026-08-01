# VV-AUDIT-WP-09 — Independent Verification & Validation Audit: Workspace Management (C-008)

**Work Package:** WP-09 — Workspace Management (C-008)
**Commits audited:** `90544cb` (BA-01), `6ce9bd3` (BA-02), `d648150` (BA-03)
**Reviewer:** Independent, fresh-context reviewer — second reviewer, distinct from `CERT-WP-09`'s own reviewer, no prior WP-09 involvement
**Gate:** 2 of 5 (`CLAUDE.md §19.7b`) — a broader, more exhaustive mandate than Gate 1, per this document's own method requirement (from-scratch runtime probes per defect class, not adapted from the existing test suite)
**Determination:** Remediation required before Gate 5 — see Finding 2 below

---

## Independent Re-Verification

Full regression suite re-run: 716/716 passing (at time of this audit). `alembic heads` — single head, `b1d6f4c8a3e7`. `tsc --noEmit` — 0 errors. All commits verified to contain the content their own messages describe.

## Requirements Traceability Matrix (6 ERBs / 11 EXs) and Business Rule Conformance (BR-C008-01 through 07)

Both built fresh from an independent primary-source extraction. `IRA-009 §4.8`'s own 3-of-6 ERB exclusion independently confirmed accurate — no entry/switch/re-entry code exists anywhere in WP-09. `BR-C008-01a`, `BR-C008-02`, `BR-C008-06`, `BR-C008-07` conform. `BR-C008-03/04/05` not applicable at this scope (governed transitions excluded). See Finding 1 below for the one non-conformance found.

## Finding 1 — BA-02 Never Requests an Access Evaluation Outcome (re-derived from Gate 1, severity determined)

Independently re-extracted `ERB-C008-06`/`EX-C008-10` and Contract 5.3's own closing sentence — confirmed Gate 1's reading: Access Evaluation Outcome is named unconditionally for this EX, and Contract 5.3 states a change to Access context "SHALL be surfaced through ERB-C008-06/EX-C008-10 and SHALL NOT be silently absorbed into continued participation." A from-scratch runtime probe (seeded an ACTIVE Membership with an associated `DENIED`/`INVALIDATED` `AccessEvaluationOutcome` row, called both the service layer and `POST /workspaces/refresh-status` directly) empirically confirmed the endpoint reports `CURRENT` regardless.

**Severity: Medium — deferrable Technical Debt, not `CLAUDE.md §19.8.5`-class.** Calibrated directly against `TD-103`'s own precedent (WP-08, identical shape): no HTTP status diverges from spec, no referentially-invalid data, no access actually granted or bypassed (`BR-C008-07` establishes this status is never an authorization envelope), no UI consumer currently depends on it. Root cause is `TD-111` (no production `TierResolver` anywhere). **Registered as `TD-112`.**

## Finding 2 — Cross-Tenant Membership Status Disclosure via `classify-handoff-rejection`

**Disagrees with Gate 1's own recommendation to defer this as Technical Debt.** A from-scratch, two-tenant runtime probe (Organization A/Person A/Membership A and an unrelated Organization B/Person B/Membership B, no shared row) confirmed: an authenticated caller in Tenant A, supplying Tenant B's own `membership_id`, received HTTP 200 and correctly distinguished Tenant B's own Membership status change (`ACTIVE` → `SUSPENDED`) purely from the response's `classification` field — with no relationship between the tenants and no ownership/tenant check anywhere in the request path (`middleware/tenant.py` exempts `/workspaces` entirely; `BaseRepository.get_by_id()` is a bare primary-key lookup).

Gate 1's own WP-08 comparator does not hold: WP-08's `identity_id` lookup is safe specifically because `Identity`/`Person` carry no `organization_id` column anywhere (no tenant boundary exists to cross) — `Membership` is the opposite case, and `middleware/tenant.py`'s own commentary repeatedly states Membership is organization-scoped data. The correct comparator is `VV-AUDIT-WP-05`'s own Finding F-02 (an unscoped foreign-ID lookup disclosing another tenant's Approval Authority data) — rated High, non-deferrable. The one difference (a two-value status vs. a name/id) is not a principled basis for a lower severity under `CLAUDE.md §19.8.7`'s own text ("even if no exploit is currently known").

**Severity: High — `CLAUDE.md §19.8.5`-class — non-deferrable.** Remediation required before Gate 5, with independent re-verification (Gate 4) including a negative control against the pre-fix code.

## Harness/Fixture Production-Parity Checklist

FK enforcement is off in the SQLite test harness by default (repository-wide, pre-existing gap) — no WP-09-specific data-integrity risk, since no BA writes to any FK-bound table. BA-01 correctly has cross-organization tests (`test_resolve_candidates_spans_multiple_organizations`, `test_get_candidates_only_returns_the_callers_own_memberships`). **No multi-organization/cross-tenant test existed anywhere for BA-02 or BA-03 at the time of this audit** — the same root cause `VV-AUDIT-WP-05` names for its own F-02, and exactly the missing test class that would have caught Finding 2 before certification.

## Determination

Finding 2 is `CLAUDE.md §19.8.5`-class and must be remediated and independently re-verified before WP-09's certified status can stand. Finding 1 is genuine, deferrable Technical Debt (`TD-112`). No other `§19.8.5`-class defect found across the RTM/BR sweep or harness-parity checklist.

---

*End of VV-AUDIT-WP-09. See `RRA-WP-09_Workspace_Management_Release_Readiness_Audit.md` (Gate 5) for confirmation that Finding 2's own remediation was independently verified (Gate 4) before this Work Package's closure.*
