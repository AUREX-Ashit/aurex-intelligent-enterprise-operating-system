# IRA-001A — WP-01 Constitutional Correction: Organization Identity Establishment & Activation

### Organization Management (C-004)

**Status:** Approved — Implemented, Developer-Validated, and Independently Reviewed (APPROVED WITH OBSERVATIONS; see §9)
**Classification:** Implementation Readiness Assessment — Corrective (same genre as IRA-001, scoped to a constitutional non-conformance correction, not a new capability increment)
**Work Package:** WP-01A — corrective sub-package of WP-01 (C-004), not a new Work Package number
**Supersedes (partially):** IRA-001's own BA-01 Business Activity Contract only — IRA-001's BA-02 through BA-07 contracts remain in force, unmodified, unreferenced by this document
**Trigger:** This repository's own constitutional-interpretation, behavioral-compliance-assessment, and historical-governance-validity investigation chain established that `OrganizationService.establish()` violated BR-C004-01 and Contract 5.4 (PE-001-C004) using code that existed at WP-01's own certification time (2026-07-23 self-reported, per CERT-WP-01) — not merely a documentation-accuracy gap, as CERT-WP-01's own Finding A originally classified it.

---

## 1. Objective

Close the BR-C004-01/BR-C004-08/Contract 5.4 non-conformance identified against BA-01's `establish()` without disturbing any already-certified, unaffected Business Activity (BA-02 through BA-07).

## 2. Scope

**In scope:** BA-01 (amended), BA-01B (new, ERB-C004-02), BA-01C (new, ERB-C004-03).
**Out of scope:** BA-02 through BA-07 (no change — confirmed zero modification to their own service methods, routers, or business logic). Membership's (WP-03) own BR-C004-03 gap — `MembershipService.establish()` derives Organization existence via direct repository access rather than a C-004-owned resolution authority — is a cross-capability finding, not owned by this corrective package; recorded as Technical Debt (§8) for WP-03's own governance to receive. Any change to already-persisted Organization rows — this correction is forward-only; no historical `organizations` row is retrofitted with a synthetic Anchor.

## 3. Documents Reviewed

CLAUDE.md, PE-001-C004 (full), CAP-001, ERG-001, IMP-001 §6.3–6.7, ADR-003/004/005, IRA-001 (the baseline being corrected), IMP-REPORT-WP-01, CERT-WP-01, WPR-001, and this repository's own constitutional-interpretation / behavioral-compliance-assessment / historical-governance-validity / architectural-decision investigation reports (produced in this same governance track, not committed as separate artifacts — their conclusions are incorporated directly into this IRA and into IMP-REPORT-WP-01's IRA-001A section).

## 4. Architectural Realization (approved, per the preceding architectural-decision investigation)

**Option A — a separate, non-authoritative Organization Anchor persistence construct** (`organization_establishment_attempts`), evaluated against four alternatives (a fourth lifecycle status value — constitutionally disqualified by PE-001-C004 §9.6's own drafting history; a single-table authority/visibility flag; a workflow-orchestrated single table; an event-sourced realization) and found to satisfy BR-C004-08 and Contract 5.4's NOT_FOUND requirement **by construction** rather than by read-path filtering discipline, with the smallest reopening footprint (zero already-certified Business Activities touched) and no dependency on platform infrastructure this repository does not have (no Metadata Runtime, Workflow engine, or Event Store exists — confirmed via ADR-005).

## 5. Business Activity Assessment

| BA | Type | Business Object | Domain Event | Canonical ERB | Disposition |
|---|---|---|---|---|---|
| BA-01 (amended) | Create | Organization Establishment Attempt (Organization Anchor Context) | `ORGANIZATION_ANCHOR_ESTABLISHED` (renamed from `ORGANIZATION_ESTABLISHED`, disclosed) | ERB-C004-01 | Amended |
| BA-01B (new) | Update (verification) | Organization Establishment Attempt | `ORGANIZATION_DOMAIN_CLAIM_VERIFICATION_RECORDED` | ERB-C004-02 | New |
| BA-01C (new) | Update (state transition, first-time, terminal for the attempt) | Organization | `ORGANIZATION_ACTIVATED_FIRST_TIME` (distinct from BA-05's `ORGANIZATION_ACTIVATED`) | ERB-C004-03 | New |

## 6. Gap Analysis / Persistence Design Decision

**New table:** `organization_establishment_attempts` — candidate identity fields mirroring the original `EstablishOrganizationRequest` exactly (`organization_code`, `organization_name`, `organization_type`, `description`), plus `primary_domain` (nullable), `domain_verification_status` (`NOT_CLAIMED`/`UNVERIFIED`/`VERIFIED`), `no_domain_activation_reason` (nullable — the governed no-domain decision itself, BR-C004-09), and `activated_organization_id` (nullable FK into `organizations.id`, set only at activation, never consulted by any existence/validity resolution path — PE-001-C004 §1.17's "preserved in lineage").

**Design decision, resolved directly (no separate ADR required):** this is an additive schema change (one new table, no existing column altered or dropped) — the same disposition class ADR-004 pre-authorized for future incremental `organizations` extensions, and consistent with every prior WP-01/02/03/04 migration in this repository's history. No architecture document requires an ADR for a purely additive new table introduced by a Business Activity's own gap analysis.

**BA-02/BA-03 impact:** none. Both continue to query only `organizations`, exactly as before — confirmed directly, no code change to either.

## 7. Real Verification Mechanism — Explicitly Out of Scope

BA-01B (Verify Organization Domain Claim) records a verification *decision* (`verified: bool`, supplied by the caller) as a distinct, authorized, audited, traceable act — satisfying BR-C004-02/BR-C004-09's actual requirement (that verification be a recorded fact, never a silent default). The underlying proof-of-control mechanism (DNS TXT record, email token, etc.) is not built — PE-001-C004's own "governed no-domain activation path" licenses proceeding without real domain verification entirely, so no WP-01A Business Activity requires one to reach Fully Implemented status. Recorded as Technical Debt (§8), not silently omitted.

## 8. Technical Debt Raised

1. **BA-01B's verification decision has no real proof-of-control mechanism behind it** (DNS/email token, etc.) — disclosed above; not required for constitutional conformance, since the no-domain path is fully licensed.
2. **`MembershipService.establish()` (WP-03) derives Organization existence via direct repository access**, not through any C-004-owned resolution authority (BR-C004-03) — pre-existing, not introduced by this correction, but not fixed here either: `membership_service.py` is WP-03's own file, out of WP-01A's ownership. Flagged for WP-03's own governance to receive.
3. **BA-02 (`get_details()`) does not itself distinguish ACTIVE/SUSPENDED/RETIRED/NOT_FOUND as a typed Organization Validity Context** the way EX-C004-05 specifies — it returns full details or 404, regardless of status. No dependent capability currently needs the narrower resolution contract; not built speculatively.
4. **Frontend consumers** (`OrganizationManagementScreen.tsx`, `useEstablishOrganization.ts`, `organization-api.ts`) still assume BA-01's original synchronous-ACTIVE-establishment contract. Out of this correction's scope — backend-only, the same precedent BA-05/BA-06/BA-07 each established for their own scope.
5. **A stray, undisclosed scratch file** (`architecture/05-Implementation/_PE-001-C005_ba02_check.txt`, unrelated PE-001-C005 spec extraction from an earlier, separate investigation) was found untracked in the working tree by this correction's own Independent Review — confirmed unrelated to and untouched by this correction's diff; left as-is, not committed with this change set.

## 9. Completion Criteria

Per CLAUDE.md §19.7's Business Activity Completion Gate, applied per corrective BA:

- ✅ BA-01 (amended): implementation complete, tests rewritten and passing, reviewed.
- ✅ BA-01B (new): implementation complete, tests passing, reviewed.
- ✅ BA-01C (new): implementation complete, tests passing, reviewed.
- ✅ Full AuthService suite: 468/468 passing, zero regressions to BA-02–BA-07 or any other Work Package.
- ✅ Single Alembic head confirmed.
- ✅ Independent Review completed — APPROVED WITH OBSERVATIONS (fresh-context reviewer, full detail recorded in IMP-REPORT-WP-01's IRA-001A section, added in the same documentation pass as this status update).
- ⏳ Committed to repository (see IMP-REPORT-WP-01's IRA-001A section for commit hashes).
- ⏳ CERT-WP-01A issued.

---

*End of IRA-001A. This document does not modify IRA-001 (unchanged, preserved per §19.7's audit-trail discipline) and does not itself reopen or amend CERT-WP-01 — see CERT-WP-01A for that governance act.*
