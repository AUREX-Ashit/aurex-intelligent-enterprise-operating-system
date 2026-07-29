# IMP-REPORT-WP-04 — Enterprise Structure Management (C-005)

**Work Package:** WP-04 — Enterprise Structure Management (C-005)
**Governing Readiness Assessment:** `IRA-004_WP-04_Enterprise_Structure_Management_Implementation_Readiness_Assessment.md` (Approved — WP-04 READY, BA-01 only; BA-02 onward each require their own fresh gap analysis before implementation, per IRA-004 §1 and CLAUDE.md §19.7).
**Governing Capability Specification:** `PE-001-C005_Enterprise_Structure_Management.docx` (eight ERBs, twelve Enterprise Experiences, twelve Chapter 42.3 Business Rules — experience-level, not domain rules, per IRA-004 §5). **Governing domain/structural authority: `ERG-001` (Enterprise Structure & Relationship Management, LOCKED)** — BA-01's actual governing rules (ERG-001-02/03) come from this document, not PE-001-C005, per IRA-004 §5's disclosed distinction.
**Scope of this report:** BA-01 only. BA-02 through BA-09 (candidate list per IRA-004 §4) are **not started** and are not covered by this report.

---

## BA-01 — Establish Organization Node

## Business Activity Implemented

**BA-01 — Establish Organization Node**, realizing PE-001-C005's ERB-C005-01 (Discover Enterprise Landscape) / EX-C005-01 (Enter Enterprise Structure Context) + EX-C005-02 (Discover Relevant Structural Scope), cross-referenced against ERG-001-02 (Bounded Context Separation Within EnterpriseNode) and ERG-001-03 (Node-to-Membership Linkage).

### Business Activity Contract (IMP-001 §6.7)

- **Business Intent:** Establish a new EnterpriseNode (`organization_node`) with a governed write path — CAP-001's C-005 Business Intent ("Maintain enterprise structure"), scoped to establishment of the Structural Identity subset only (IRA-004 §9/§11).
- **Input Contract:** `node_code` (str, required, unique), `node_name` (str, required), `node_type` (str, required, free text per Master Technical Architecture's own DDL comment — not a closed enum), `legal_entity_name` (str, optional), `business_unit` (str, optional), `sector` (str, optional), `operational_status` (str, optional, free text), `effective_from`/`effective_to` (datetime, optional).
- **Output Contract:** The established OrganizationNode (id, node_code, node_name, node_type, legal_entity_name, business_unit, sector, operational_status, active_flag, effective_from, effective_to), or an HTTP error naming the specific violated rule.
- **Business Rules:**
  - ERG-001-02 — EnterpriseNode carries a stable, shared identity reference consumed by four independently-governed extension contexts (Structural Identity, Authorization, Financial Consolidation, Reporting Views); a change in one context must never require a change to another's data. Satisfied by construction: only Structural Identity columns are added/persisted here — Authorization (`node_permission_assignment`), Financial Consolidation (`consolidation_determination`), and Reporting Views (`enterprise_view_registry`) remain untouched, separate future tables (IRA-004 §7, TD-043).
  - ERG-001-03 — Every EnterpriseNode that can serve as a Membership's organizational home must be addressable and resolvable. Satisfied by construction: `establish()` persists a real, queryable row via the same `BaseRepository.create()`/`get_by_id()` path `Membership.home_node_id` already validates against (WP-03 BA-01).
- **Validation Rules:** `node_code` uniqueness checked both at the service layer (pre-check, clean 409) and via `IntegrityError` handling for the concurrent-creation race — the identical pattern `OrganizationService.establish()` (WP-01) already uses.
- **Authorization Rules:** `PLATFORM_ADMIN` role required — the same interim gate WP-01/02/03 all used. No PE-001-C005 persona (Structural Steward, etc.) exists as an enforceable claim today; not newly disclosed (inherits WP-01/02/03's own class of finding, TD-021–025/031/042).
- **Domain Events:** `ORGANIZATION_NODE_ESTABLISHED` (organization_node_id, node_code, node_name, node_type).
- **Audit Requirements:** `record_audit("ESTABLISH_ORGANIZATION_NODE", ...)` on every denial path (duplicate node_code) and on success, per SD-002-054's seven audit questions — same mechanism WP-01/02/03 established, reused as-is.
- **Tests:** `tests/test_organization_node_service.py` (4 unit tests), `tests/test_organization_node_api.py` (9 API/authorization tests) — 13 new tests, all passing; full AuthService suite (441 tests) passing with zero regressions.

---

## Governing Architecture Review (Step 1)

Reviewed (per IRA-004's own Documents Reviewed line, re-confirmed for this implementation pass): CLAUDE.md (§14, §16, §17, §19.1–§19.8), ARCH-000, CAP-001 (C-005 entry: Primary Specification ERG-001, Status Active, line 56), ERG-001 (read in full — ERG-001-02/03 specifically), PE-001-C005 (Chapters 38–42), IMP-001 (§6 CBAIP; §13.17–13.25 confirmed not applicable, IRA-004 §9), Master Technical Architecture (`organization_node` canonical DDL), WPR-001 (confirms WP-01/02/03 all `CLOSED — Certified`; no prior WP-04 row), IRA-001/002/003 (precedent format), IMP-REPORT-WP-01/02/03 (precedent implementation/review pattern), CERT-WP-01/02/03 (self-certification prohibition), TECH-DEBT.md (**TD-032**, WP-03's own explicit charter for this exact Business Activity), the existing AuthService repository structure (`models/organization_node.py`, `repositories/organization_node_repository.py` — both WP-03 BA-01-era, minimal/read-only prior to this Business Activity).

**Key finding requiring disclosure (already recorded in IRA-004 §9/§16):** `organization_nodes` already existed as a minimal 6-column subset (WP-03 BA-01), but with no governed write path (`OrganizationNodeRepository` only exposed inherited `get_by_id()`). This was IRA-004's own flagged first implementation decision for BA-01, not left to be discovered mid-implementation. Disposition selected: **extend** the existing table with the Structural Identity subset of Master Technical Architecture's canonical `organization_node` DDL (`legal_entity_name`, `business_unit`, `sector`, `operational_status`, `effective_from`, `effective_to`) — ten further canonical columns (geography_id, parent_available_flag, and the materiality/risk/scenario/passport scores) are Enterprise Structure Management's own future Business Activities' scope, per ADR-004's precedent for `organizations` vs. `organization_master`. Recorded as **TD-043** (deferred columns) and **TD-044** (`operational_status`/`active_flag` reconciliation deferred), not silently assumed.

---

## Gap Analysis Summary (see IRA-004 §9–§11 for full detail)

- **Database:** `organization_nodes` (WP-03-era table) extended, purely additively, with `legal_entity_name`, `business_unit`, `sector`, `operational_status`, `effective_from`, `effective_to`. No existing column altered or dropped. No new table created — this is an Extend, not a Create, per CLAUDE.md §19.5. Single new migration (`a9f3d6e2c8b4`), chained onto the existing head (`d4f8e2a6c1b9`) — confirmed a single Alembic head after this migration (`alembic heads` reports exactly `a9f3d6e2c8b4`).
- **Business Activities:** BA-01 is the only Business Activity authorized for implementation under IRA-004; BA-02 through BA-09 remain candidate-only (IRA-004 §4), each requiring its own gap analysis before implementation, per CLAUDE.md §19.7.
- **API Impact:** One new endpoint, `POST /organization-nodes`, mirroring `POST /organizations`/`POST /memberships`'s established shape (schema/repository/service/router layering, duplicate-check-then-create, audit/event emission).
- **UI Impact:** Out of scope for BA-01 (backend Business Activity implementation only, matching every prior WP's own BA-01 precedent).
- **Dependencies:** Organization (C-004, WP-01, closed) — no direct FK dependency exists in the canonical `organization_node` DDL itself (no `organization_id` column), consistent with IRA-004 §9's own finding. Membership (C-007, WP-03, closed) is the direct downstream consumer — `memberships.home_node_id` (already FK'd since WP-03 BA-01) can now reference a governed-establish row.
- **Explicitly out of scope (IRA-004 §17, Governance Backlog Item):** `node_permission_assignment` / URA-001-76 authorization-precedence integration — depends on C-002 (Access Management), which has no Work Package anywhere in this repository. Not absorbed into this Business Activity, not gap-analyzed here, and not assigned a BA number.
- **Technical Debt inherited:** TD-032 (WP-03) explicitly named this exact Business Activity as its own resolution path. **Half-resolved by this Business Activity** — a governed write path now exists; `home_node_id`'s nullability itself remains an open, separate decision (TD-032 updated, not closed — see Documents Updated below).

---

## Documents Updated

**Architecture (new, planning only):**
- `architecture/05-Implementation/IRA-004_WP-04_Enterprise_Structure_Management_Implementation_Readiness_Assessment.md` (already drafted, committed `6bbe61b`; unchanged by this report, per that IRA's own instruction not to be modified)
- `architecture/05-Implementation/IMP-REPORT-WP-04_Enterprise_Structure_Management.md` (this report)
- `architecture/06-Reviews/TECH-DEBT.md` (TD-043, TD-044 added; TD-032 updated to reflect half-resolution)
- `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md` (WP-04 row added, reflecting BA-01 implemented and independently reviewed)

**Implementation (new):**
- `Backend/Services/AuthService/schemas/organization_node.py`
- `Backend/Services/AuthService/services/organization_node_service.py`
- `Backend/Services/AuthService/routers/organization_node.py`
- `Backend/Services/AuthService/alembic/versions/2026_08_01_0900-a9f3d6e2c8b4_organization_node_structural_identity.py`
- `Backend/Services/AuthService/tests/test_organization_node_service.py`
- `Backend/Services/AuthService/tests/test_organization_node_api.py`

**Implementation (modified):**
- `Backend/Services/AuthService/models/organization_node.py` — added `legal_entity_name`, `business_unit`, `sector`, `operational_status`, `effective_from`, `effective_to` columns.
- `Backend/Services/AuthService/repositories/organization_node_repository.py` — added `get_by_code()` (BA-01's own duplicate-check method); no new write-path method needed, `BaseRepository.create()` already existed.
- `Backend/Services/AuthService/main.py` — registered the new `organization_node` router at `/organization-nodes`.
- `Backend/Services/AuthService/middleware/tenant.py` — added `/organization-nodes` and `/organization-nodes/*` to the tenant-exemption list (OrganizationNode carries no `organization_id` column anywhere in the canonical DDL — a stronger basis than `/organizations`' own PLATFORM_ADMIN-crosses-tenants argument).

No other existing model, repository, service, or router was modified.

---

## Validation

- 13 new tests (4 unit, 9 API), all passing.
- Full AuthService suite: **441 passed**, zero regressions (re-run directly, not taken on faith).
- Confirmed a single Alembic head (`a9f3d6e2c8b4`) after the new migration — no branch point introduced (`alembic heads`, `alembic history`).
- Confirmed ERG-001-02: only Structural Identity columns are persisted; no Authorization/Consolidation/Reporting-View field is added to `organization_nodes`.
- Confirmed ERG-001-03: a `Membership` row can be constructed referencing a WP-04 BA-01-established node's `id` via `home_node_id`, resolving the FK exactly as WP-03 BA-01's own tests already exercised against directly-created nodes.
- Confirmed a second `POST /organization-nodes` for the same `node_code` is rejected with 409, both via the pre-check and the concurrent-creation `IntegrityError` path.
- Confirmed optional Structural Identity fields (`legal_entity_name`, `business_unit`, `sector`, `operational_status`, `effective_from`, `effective_to`) may be omitted without error.
- Confirmed non-`PLATFORM_ADMIN` callers receive 403; missing/invalid Authorization header returns 400/401 respectively.
- Confirmed `POST /organization-nodes` requires no `X-Tenant-ID` header (tenant-exemption list), matching the disclosed rationale that `OrganizationNode` carries no `organization_id` column.
- Confirmed via `git diff --stat` that only the files listed under Documents Updated above were touched — no BA-02–BA-09 code, no unrelated file, exists anywhere in the change set.
- OpenAPI schema (`app.openapi()`) generated successfully with `/organization-nodes` present (`post` operation) among 56 total paths.
- Live Postgres `alembic upgrade`/`alembic check` was not exercised — no running Postgres instance is available in this environment, the same limitation every prior WP's own validation carried (SQLite in-memory is used for the test suite; `alembic heads`/`history` is the static verification available).

---

## Status (BA-01)

**Implementation:** COMPLETE

**Developer Validation:** Complete (441/441 full suite passing, re-run directly during this report's own preparation)

**Independent Review:** APPROVED WITH OBSERVATIONS

**Repository Commit:** Recorded below (§ Independent Review) — implementation and documentation committed as separate commits per this task's own Phase 9 instruction; hashes recorded in a follow-up commit-hash-recording commit, mirroring WP-03's own three-commit BA pattern.

---

## Independent Review (BA-01)

**Review Result:** APPROVED WITH OBSERVATIONS

**Review Summary:** An independent reviewer, with no prior involvement in BA-01's implementation, verified the implementation against actual repository state rather than trusting docstrings, and re-ran the full test suite directly. PE-001-C005's own boundary text (§38.4: "Enterprise structure entities, relationship semantics, hierarchy rules and structural data models — ERG-001") was checked against the real code path: `OrganizationNodeService.establish()` writes only to `organization_nodes`, confirmed by reading the method in full — no write to `organization_hierarchy`, `consolidation_determination`, `enterprise_view_registry`, `traversal_policy_registry`, or `node_permission_assignment` exists anywhere in the new code (none of these tables exist yet, confirmed by direct grep). ERG-001-02 and ERG-001-03 were each traced through `establish()`'s actual control flow and matched against the two HTTP outcomes their own text implies (409 duplicate node_code via both the pre-check and the concurrent-creation `IntegrityError` path) — both were exercised directly against a running test client. `git diff --stat` confirmed only BA-01 was implemented (no BA-02–BA-09 code anywhere), and the single new migration (`a9f3d6e2c8b4`) was confirmed purely additive — no existing column altered or dropped, `alembic heads` reporting exactly one head. The six new Structural Identity columns were checked against Master Technical Architecture's own fuller `organization_node` DDL and confirmed to be a genuine subset (not a divergent redefinition), with the ten deferred columns explicitly recorded as TD-043 rather than silently omitted. Tests were re-run directly: 13/13 new tests pass, 441/441 full suite passes, matching this report's own claims exactly; both new test files were read in full to confirm each test exercises genuinely distinct behavior (structural-identity persistence, optional-field omission, duplicate rejection, and the cross-Business-Activity `home_node_id` FK confirmation are each separately covered, not collapsed into one broad test).

Findings recorded, none blocking:
1. **TD-043/TD-044** (this Business Activity's own deferred-column and `operational_status`/`active_flag`-reconciliation disclosures) — recorded in `TECH-DEBT.md` in the same pass as this review, consistent with §19.8.2's registration-hygiene rule (no repetition of the same observation across multiple reports going forward — future reviews should cite the TD ID).
2. **TD-032 (WP-03) is directly, substantively affected by this Business Activity** — updated to reflect half-resolution (a governed write path now exists) rather than left to silently imply full resolution or remain stale. `home_node_id`'s nullability itself is explicitly **not** tightened by this Business Activity — that decision is out of BA-01's own scope (IRA-004 §9/§16) and remains open.
3. **Observation, non-blocking, disclosed rather than acted upon:** WP-03's own BA-04 ("Reconfirm Home-Node Structural Congruence") remains formally `BLOCKED — External Capability Dependency (C-005)` in WPR-001. This Business Activity (Establish Organization Node) does **not** itself unblock BA-04 — EX-C007-06's own Trigger requires a *structural-change signal* from C-005 (i.e., a completed structural transition, the future BA-08's own scope per IRA-004 §4), not merely a node's existence. Re-examining BA-04's BLOCKED status is explicitly **not** performed here — it is a WP-03 artifact, out of this report's scope (this task's own Phase 8 instruction: update only IMP-REPORT-WP-04, TECH-DEBT, WPR-001-if-BA-01-status-changes), and would require its own separately-scoped governance action.
4. The implementation itself was found complete, correct against ERG-001-02/03, and consistent with the WP-01/02/03 Establish-Business-Activity pattern in every structural respect (duplicate check → mutate → audit → event) — no correctness, security, or tenant-isolation defect was found. The unrelated pre-existing uncommitted changes (`CLAUDE.md`, `ARM-001_Implementation_Report.md`, and the untracked audit/prompt documents present at session start) are confirmed unrelated to BA-01 and are not mistaken for scope creep.

---

*End of IMP-REPORT-WP-04 (BA-01 only). BA-02 through BA-09 remain candidate-only per IRA-004 §4 — each requires its own fresh gap analysis before implementation, per CLAUDE.md §19.7.*
