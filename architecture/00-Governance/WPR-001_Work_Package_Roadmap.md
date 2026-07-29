# WPR-001 — Work Package Roadmap

**Document ID:** WPR-001
**Document Name:** Work Package Roadmap
**Type:** Governance Registry (not a Constitutional Document under ARCH-000 §12 — this is an implementation-sequencing record, analogous in authority scope to an ADR, not a Layer-1 architecture specification)
**Owner:** Repository Owner / Engineering Governance
**Status:** Active
**Dependencies:** CAP-001 (capability identity), ARCH-000 (layering), CLAUDE.md §19.7 (Business Activity Completion Gate)

---

## 1. Purpose

Before this document existed, no repository artifact defined which Work Package (WP-NN) implements which PE-001 capability (C-XXX). Every IRA (Implementation Readiness Assessment) to date had to *infer* this mapping from cross-references scattered across Technical Debt entries, certification reports, and prior IRAs — a traceability gap identified during the WP-03 Readiness Assessment.

**This document is the single, authoritative source for Work Package → Capability assignment.** Future IRAs SHALL cite this document for WP ownership rather than inferring it. This document does not itself approve or authorize implementation of any WP it lists — approval remains governed by CLAUDE.md §19 (Implementation Start Checklist) and, where applicable, an accepted IRA.

---

## 2. Roadmap

| WP | Capability | Capability Name | Status | Governing IRA | Certification |
|---|---|---|---|---|---|
| **WP-00** | — (Platform Bootstrap; no PE-001 capability) | Idempotent seeding of canonical Roles/Permissions, demonstration Organization, Platform Administrator identity; config-driven feature flags; liveness/readiness endpoints; interim observability. | Committed (`d5150ab`) | None — predates the IRA/CERT governance process (introduced starting WP-01) | None — no CERT-WP-00 exists; not required, since no capability-specific ERB/EX/BR was implemented |
| **WP-00A** | — (Repository Baseline Stabilization; no PE-001 capability) | IC-001 certification remediation and repository hygiene: production seed-data safeguard, stale doc/test correction, dead-code removal, CI/Docker path fixes. | Committed (`d5150ab`, same commit as WP-00) | None — same reason as WP-00 | None |
| **WP-01** | C-004 | Organization Management | **CLOSED — Certified, with IRA-001A constitutional correction applied** (BA-01 amended, BA-01B/BA-01C added — see `IRA-001A_WP-01_Organization_Establishment_Activation_Correction.md`. Corrects a BR-C004-01/BR-C004-08/Contract 5.4 non-conformance in BA-01's original `establish()` behavior, found by this repository's own constitutional-governance investigation to have existed since WP-01's own certification time. BA-02 through BA-07 unaffected — re-verified, not re-certified. Raises TD-046 through TD-049) | `IRA-001_WP-01_Organization_Management_Implementation_Readiness_Assessment.md` + `IRA-001A_WP-01_Organization_Establishment_Activation_Correction.md` | `CERT-WP-01_Organization_Management.md` — PASS WITH OBSERVATIONS (original, BA-02–BA-07) + `CERT-WP-01A_Organization_Management_Correction.md` (corrective, BA-01/BA-01B/BA-01C) |
| **WP-02** | C-003 | Role & Permission Management | **CLOSED — Certified** | `IRA-002_WP-02_Role_Permission_Management_Implementation_Readiness_Assessment.md` | `CERT-WP-02_Role_Permission_Management.md` — PASS WITH OBSERVATIONS |
| **WP-03** | C-007 | Membership Management | **CLOSED — Certified** (9 of 11 Business Activities Complete and Independently Reviewed — BA-01, BA-02, BA-03, BA-06, BA-07, BA-08, BA-09, BA-10, BA-11; **BA-04 formally BLOCKED — External Capability Dependency (C-005)**; **BA-05 formally BLOCKED — Governance Decision Required**, per Contract 5.3's own prohibition on inventing a standing-transition matrix. Every Business Activity IRA-003 identified reached a final, documented disposition — COMPLETE or BLOCKED — satisfying the Work Package Completion Gate; re-opening BA-04/BA-05 is a future, separately-scoped action contingent on external events, not outstanding WP-03 work) | `IRA-003_WP-03_Membership_Management_Implementation_Readiness_Assessment.md` | `CERT-WP-03_Membership_Management.md` — PASS WITH OBSERVATIONS |
| **WP-04** | C-005 | Enterprise Structure Management | **IN PROGRESS** (4 of 9 candidate Business Activities implemented and independently reviewed — BA-01 Establish Organization Node, BA-02 Understand Structural Position, BA-03 Frame Structural Change Intent, BA-04 Shape/Refine Proposed Structural Outcome. BA-05 through BA-09 (IRA-004 §4's candidate list) each require their own fresh gap analysis before implementation, per CLAUDE.md §19.7. BA-01 half-resolves WP-03's own TD-032; does not unblock WP-03 BA-04, per IMP-REPORT-WP-04's own disclosed finding. BA-02 raises TD-045 — relationship traversal deferred to `organization_hierarchy`'s own future Business Activity. BA-03 registers SCI-000001 (Structural Change Intent) as a canonical Business Object — see `ADR-006` — and raises TD-051/TD-052. BA-04 scopes proposals to EnterpriseNode only for v1 (`ADR-007`), registers POC-000001 (Proposed Outcome Context) as a canonical Business Object (`ADR-008`), introduces this repository's first append-only revision model, and raises TD-053 through TD-056, all deferred to BA-05's own future gap analysis) | `IRA-004_WP-04_Enterprise_Structure_Management_Implementation_Readiness_Assessment.md` + `ADR-006_Structural_Change_Intent_Canonical_Business_Object_Registration.md` + `ADR-007_BA-04_Phase-1_Proposal_Target_Scope.md` + `ADR-008_Proposed_Outcome_Context_Canonical_Business_Object_Registration.md` | None yet — Work Package not yet closed |

No Work Package beyond WP-04 currently has constitutional ownership anywhere in this repository. A stray informal reference to "WP-06" exists in `Backend/Services/AuthService/docs/RUNBOOK_BOOTSTRAP.md` (an operational runbook, not a governance document), written before WP-01's actual capability assignment was decided and never corrected — it is **not** treated as a roadmap commitment and is explicitly excluded here per this document's own no-invention rule (§3).

---

## 3. Maintenance Rule

- A row is added to §2 only when a Work Package is either (a) actually committed to the repository (WP-00/WP-00A precedent), or (b) has an accepted IRA assigning it a specific capability.
- **No future WP may be added speculatively.** If a document elsewhere in the repository casually mentions a future WP number without it being backed by an accepted IRA or a real commit, that mention is non-authoritative and SHALL NOT be copied into this table until it is properly assigned.
- When a WP's status changes (e.g., IRA-003 accepted, WP-03 implementation begins, WP-03 certified), this table SHALL be updated in the same governance pass that produces the triggering artifact.
- This document does not redefine CAP-001's capability registry, ARCH-000's layering, or any Business Activity's own scope — it records sequencing and ownership only.

---

*End of WPR-001.*
