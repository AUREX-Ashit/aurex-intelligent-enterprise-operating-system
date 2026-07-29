# IMP-REPORT-WP-04 — Enterprise Structure Management (C-005)

**Work Package:** WP-04 — Enterprise Structure Management (C-005)
**Governing Readiness Assessment:** `IRA-004_WP-04_Enterprise_Structure_Management_Implementation_Readiness_Assessment.md` (Approved — WP-04 READY, BA-01 only; BA-02 onward each require their own fresh gap analysis before implementation, per IRA-004 §1 and CLAUDE.md §19.7). BA-02's own fresh gap analysis is recorded in this report's own "Governing Architecture Review (Step 1) — BA-02" and "Gap Analysis Summary — BA-02" sections below, consuming IRA-004 §4/§9/§10's own BA-02 candidate disposition ("B — Existing implementation can be reused") rather than re-deriving it from nothing.
**Governing Capability Specification:** `PE-001-C005_Enterprise_Structure_Management.docx` (eight ERBs, twelve Enterprise Experiences, twelve Chapter 42.3 Business Rules — experience-level, not domain rules, per IRA-004 §5). **Governing domain/structural authority: `ERG-001` (Enterprise Structure & Relationship Management, LOCKED)** — BA-01's actual governing rules (ERG-001-02/03) come from this document, not PE-001-C005, per IRA-004 §5's disclosed distinction. BA-02 has no equivalent ERG-001 domain rule (it is a pure read, ERG-001 governs write-side structural semantics) — its governing text is PE-001-C005 ERB-C005-02/EX-C005-03 directly.
**Scope of this report:** BA-01, BA-02, BA-03, BA-04, and BA-05. BA-06 through BA-09 (candidate list per IRA-004 §4) are **not started** and are not covered by this report. BA-03's own governing decision, `ADR-006_Structural_Change_Intent_Canonical_Business_Object_Registration.md`, registered SCI-000001 (Structural Change Intent) as a canonical Business Object and downgraded BA-03 from IRA-004 §10's original Category D to Category C — this report's own BA-03 section records that Business Activity's implementation, consuming (not repeating) IRA-004 §21's registration and ADR-006's decision. BA-04's own two constitutional questions (proposal target-type scope; Business Object registration) were resolved by `ADR-007` and `ADR-008` respectively — this report's own BA-04 section records that Business Activity's implementation, consuming (not repeating) IRA-004 §22's registration and both ADRs' decisions. BA-05's own Business Object registration question (Impact Context) was resolved by `ADR-009` — this report's own BA-05 section records that Business Activity's implementation, consuming (not repeating) IRA-004 §23's registration and that ADR's decision.

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

**Repository Commit:** Committed to `master` in two commits — `f4f0292` (implementation: 10 files) and `0d80ca1` (documentation: this report, TECH-DEBT.md TD-043/044 and TD-032 update, WPR-001 WP-04 row).

**Commit Hash:** `f4f0292` (implementation), `0d80ca1` (documentation: implementation report, TECH-DEBT.md, WPR-001)

**Commit Date:** 2026-08-01 (both commits)

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

## BA-02 — Understand Structural Position

## Business Activity Implemented

**BA-02 — Understand Structural Position**, realizing PE-001-C005's ERB-C005-02 (Understand Structural Position) / EX-C005-03 (Understand Structural Position). No ERG-001 domain business rule governs this Business Activity — ERG-001 governs structural write-side semantics (ERG-001-02/03, BA-01's own governing rules); BA-02 is a pure read with no domain rule of its own, per IRA-004 §5's own disclosed distinction between PE-001-C005's experience layer and ERG-001's domain layer.

### Business Activity Contract (IMP-001 §6.7)

- **Business Intent:** Allow a caller to retrieve a single, previously-established `organization_node`'s own Structural Identity fields — CAP-001's C-005 Business Intent ("Maintain enterprise structure"), scoped to the single-node read half of EX-C005-03's Purpose (IRA-004 §4's own "Query — EnterpriseNode (+ relationships)" candidate description; the "+ relationships" half is out of this Business Activity's scope, TD-045).
- **Input Contract:** `organization_node_id` (UUID, required, path parameter).
- **Output Contract:** The requested OrganizationNode (id, node_code, node_name, node_type, legal_entity_name, business_unit, sector, operational_status, active_flag, effective_from, effective_to), or a 404 naming the missing id.
- **Business Rules:** None specific to BA-02 at the ERG-001 domain layer (see above). At the experience layer, EX-C005-03's Purpose ("understand surrounding structural context and position") is only partially realized — this Business Activity returns a single node's own fields; "surrounding relationships" requires `organization_hierarchy`, which does not exist yet (TD-045).
- **Validation Rules:** `organization_node_id` must be a syntactically valid UUID (422 otherwise, enforced by FastAPI path-parameter typing); the referenced node must exist (404 otherwise).
- **Authorization Rules:** `PLATFORM_ADMIN` role required — the same interim gate every prior read-side Business Activity in this repository has used (`OrganizationService.get_details()`, WP-01 BA-02, being the direct precedent this Business Activity mirrors). No PE-001-C005 persona exists as an enforceable claim today; not newly disclosed (inherits BA-01's own class of finding).
- **Domain Events:** None. Read-only Business Activities do not emit domain events or audit records in this repository's established pattern (`OrganizationService.get_details()` does not audit either; only write paths do).
- **Audit Requirements:** None (see above).
- **Tests:** `tests/test_organization_node_service.py` (2 new unit tests), `tests/test_organization_node_api.py` (7 new API/authorization tests) — 9 new tests, all passing; full AuthService suite (450 tests) passing with zero regressions.

---

## Governing Architecture Review (Step 1) — BA-02

Reviewed for this Business Activity: CLAUDE.md (§14, §16, §17, §19.1–§19.8), CAP-001 (C-005 entry, unchanged since BA-01's own review), ERG-001 (re-confirmed no domain rule governs a pure read of `organization_node`; ERG-001-02/03 remain BA-01's own rules, not re-applied here), PE-001-C005 (ERB-C005-02 §40.3, EX-C005-03 §41.4), IMP-001 (§6.7 Business Activity Contract template, applied identically to BA-01's own), URA-001 (no persona-specific authorization construct exists for C-005 today, same disclosed gap class as BA-01/TD-021 through TD-025/TD-031/TD-034/TD-035/TD-036/TD-039/TD-042 — not separately re-registered, per §19.8.3), Master Technical Architecture (`organization_node` canonical DDL, unchanged since BA-01), WPR-001 (confirms WP-04 row shows BA-01 implemented, BA-02 through BA-09 candidate-only prior to this Business Activity), IRA-004 (§4's BA-02 candidate row: `Query`, `EnterpriseNode (+ relationships)`, `ERB-C005-02 / EX-C005-03`; §9's own BA-02 disposition: **B — "Existing implementation can be reused... `OrganizationNodeRepository`'s inherited `get_by_id()`/query methods are a direct starting point once BA-01 exists"** — confirmed accurate: BA-01 already exists, and `BaseRepository.get_by_id()` required no extension), `OrganizationService.get_details()` (WP-01 BA-02's own implementation — the direct structural precedent reused verbatim: no audit, no event, 404-on-missing, `PLATFORM_ADMIN`-gated, no tenant-scoping).

**Key finding requiring disclosure (already recorded in TD-045):** EX-C005-03's own Purpose text ("understand surrounding structural context and position... relationships") describes more than a single-record read. This Business Activity realizes only the single-node half — traversing "surrounding relationships" requires `organization_hierarchy`, which does not exist anywhere in this repository (confirmed by direct grep, zero matches) and is real, disclosed, future WP-04 work (BA-08 candidate, IRA-004 §4), not invented here. This is the same disclosed-scoping-decision class as TD-043 (BA-01's own deferred-column disclosure), not a silently discovered gap.

---

## Gap Analysis Summary — BA-02 (see IRA-004 §4/§9/§10 for the underlying candidate disposition)

- **Database:** No schema change. `organization_nodes` (extended by BA-01) is read via the existing `BaseRepository.get_by_id()` inherited by `OrganizationNodeRepository` — no new column, table, or repository method required. Alembic head remains `a9f3d6e2c8b4` (confirmed via `alembic heads`, single head, unchanged by this Business Activity).
- **Business Activities:** BA-02 is the second Business Activity authorized for implementation under this report's own fresh gap analysis (this section); BA-03 through BA-09 remain candidate-only (IRA-004 §4), each requiring its own gap analysis before implementation, per CLAUDE.md §19.7.
- **API Impact:** One new endpoint, `GET /organization-nodes/{organization_node_id}`, mirroring `GET /organizations/{organization_id}`'s established shape (path-parameter UUID, 404-on-missing, no audit/event, `PLATFORM_ADMIN`-gated).
- **UI Impact:** Out of scope for BA-02 (backend Business Activity implementation only, matching every prior WP's own precedent for a first read-side Business Activity).
- **Dependencies:** Requires BA-01 to exist (it does, committed `f4f0292`/`0d80ca1`) — no other Business Activity or Work Package dependency.
- **Missing runtime capabilities / canonical objects:** `organization_hierarchy` does not exist (TD-045) — not required for BA-02's own minimal single-node scope, only for the "+ relationships" half IRA-004 §4 itself already flagged as separate.
- **Missing repositories / services:** None — `OrganizationNodeRepository`/`OrganizationNodeService` (BA-01) are extended in place, per IRA-004 §9's own BA-02 disposition ("no new repository class anticipated for BA-02").
- **Missing authorization:** Same disclosed, pre-existing `PLATFORM_ADMIN`-only interim gate as every other read-side Business Activity in this repository (not a new gap; not separately registered, per §19.8.3).
- **Missing audit / events:** None expected — read-only Business Activities do not audit or emit events in this repository's established pattern.
- **Technical Debt raised:** TD-045 (surrounding-relationships traversal deferred to `organization_hierarchy`'s own future Business Activity).

**Conclusion: READY.** BA-02 required no new architecture, table, repository, service, or authorization construct — only an additive method (`OrganizationNodeService.get_details()`) and endpoint (`GET /organization-nodes/{organization_node_id}`) reusing BA-01's and WP-01 BA-02's own already-accepted patterns exactly.

---

## Documents Updated (BA-02)

**Architecture:**
- `architecture/05-Implementation/IMP-REPORT-WP-04_Enterprise_Structure_Management.md` (this report, BA-02 section)
- `architecture/06-Reviews/TECH-DEBT.md` (TD-045 added)
- `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md` (WP-04 row updated to reflect BA-02 implemented and independently reviewed)

**Implementation (modified):**
- `Backend/Services/AuthService/services/organization_node_service.py` — added `get_details()`.
- `Backend/Services/AuthService/routers/organization_node.py` — added `GET /organization-nodes/{organization_node_id}`.
- `Backend/Services/AuthService/tests/test_organization_node_service.py` — added 2 unit tests.
- `Backend/Services/AuthService/tests/test_organization_node_api.py` — added 7 API/authorization tests.

No model, repository, migration, or router registration (`main.py`) change was required — `OrganizationNodeRepository.get_by_id()` (inherited from `BaseRepository`) and the existing `/organization-nodes` router registration and `middleware/tenant.py` prefix exemption already cover this Business Activity.

---

## Validation (BA-02)

- 9 new tests (2 unit, 7 API), all passing.
- Full AuthService suite: **450 passed**, zero regressions (re-run directly: 441 pre-existing + 9 new).
- Confirmed a single Alembic head (`a9f3d6e2c8b4`), unchanged — no migration was introduced by this Business Activity.
- Confirmed a second `GET /organization-nodes/{organization_node_id}` for an unknown id returns 404, not 500 or an empty success.
- Confirmed non-`PLATFORM_ADMIN` callers receive 403; missing/invalid Authorization header returns 400/401 respectively; a non-UUID path parameter returns 422.
- Confirmed `GET /organization-nodes/{organization_node_id}` requires no `X-Tenant-ID` header (already-existing `/organization-nodes/*` prefix exemption in `middleware/tenant.py`, added for BA-01 and confirmed here to already prefix-match this new path without further change).
- OpenAPI schema (`app.openapi()`) generated successfully with `GET /organization-nodes/{organization_node_id}` present among 57 total paths (56 at BA-01, +1).
- Live Postgres `alembic upgrade`/`alembic check` was not exercised — same limitation as BA-01's own validation; no running Postgres instance is available in this environment.

---

## Status (BA-02)

**Implementation:** COMPLETE

**Developer Validation:** Complete (450/450 full suite passing, re-run directly during this report's own preparation)

**Independent Review:** APPROVED WITH OBSERVATIONS

**Repository Commit:** Committed to `master` in two commits — `2e6dd20` (implementation: 4 files) and `5b5ec74` (documentation: this report, TECH-DEBT.md TD-045, WPR-001 WP-04 row update).

**Commit Hash:** `2e6dd20` (implementation), `5b5ec74` (documentation: implementation report, TECH-DEBT.md, WPR-001)

**Commit Date:** 2026-07-29 (both commits)

---

## Independent Review (BA-02)

**Review Result:** APPROVED WITH OBSERVATIONS

**Review Summary:** An independent reviewer, with no prior involvement in BA-02's implementation, verified the implementation against actual repository state rather than trusting this report's own claims, and re-ran the full test suite directly. IRA-004's own BA-02 candidate row (§4, §9/§10) was confirmed to state `Query` type, `EnterpriseNode (+ relationships)`, `ERB-C005-02 / EX-C005-03`, disposition **B — "existing implementation can be reused"** — an exact match to what was implemented. `OrganizationNodeService.get_details()` was read in full and compared directly against `OrganizationService.get_details()` (WP-01 BA-02, the reused precedent): both call `get_by_id()` → 404-if-`None` → return, with no `record_audit()`, no `publish_event()`, and no write of any kind. `routers/organization_node.py`'s new endpoint was confirmed gated by the same `require_platform_admin` dependency as `establish_organization_node`, fully explaining the 400/401/403/404/422/200 test matrix. `middleware/tenant.py`'s `/organization-nodes` exemption was confirmed to be a genuine prefix match (`path.startswith("/organization-nodes/")`), not merely an exact-path exemption — the new path is legitimately covered, not accidentally passing. `git diff --stat` confirmed no `models/`, `repositories/`, `schemas/`, `main.py`, or `middleware/` change was needed. All 9 new tests (2 service, 7 API) were confirmed to each isolate a genuinely distinct behavior/status code, not collapsed into fewer broad tests. Tests were re-run directly: 450/450 full suite passes, matching this report's own claim exactly; `alembic heads` was re-run directly, confirming the single unchanged head `a9f3d6e2c8b4` and no new migration file. TD-045's factual claim that `organization_hierarchy` does not exist anywhere in the repository was independently re-verified by grep (present only in comments/docstrings/architecture text asserting its future, not-yet-built status). EX-C005-03's Purpose text and ERB-C005-02's Purpose text were read directly from the governing specification and confirmed to genuinely describe relationship traversal beyond a single-record read, validating TD-045's scoping rationale as accurate rather than a rationalized excuse. `WPR-001`'s updated WP-04 row was confirmed consistent with BA-01 + BA-02 now implemented.

Findings recorded, none blocking:
1. **Process-sequencing observation (resolved by this review):** At the time of review, this report's own BA-02 Status and Independent Review fields were still placeholders while `WPR-001` already asserted BA-02 as independently reviewed in the same uncommitted working tree — momentarily inconsistent as a snapshot, but resolved by this review's own outcome being folded into the report (this edit) before any commit is made, mirroring BA-01's own two-commit sequence (implementation, then documentation only after the review outcome is known).
2. **TD-045** (this Business Activity's own disclosed relationship-traversal deferral) — recorded in `TECH-DEBT.md` in the same pass as this review, consistent with §19.8.2's registration-hygiene rule (future reviews should cite the TD ID rather than repeating the observation).
3. **Inherited, not re-raised:** No PE-001-C005 persona (Structural Steward, etc.) exists as an enforceable claim — the same disclosed, pre-existing `PLATFORM_ADMIN`-only interim gate as every prior read-side Business Activity in this repository (TD-021 through TD-025/TD-031/TD-034/TD-035/TD-036/TD-039/TD-042's own class of finding); not separately re-registered, per §19.8.3.
4. The implementation itself was found complete, correct against ERB-C005-02/EX-C005-03's single-node scope, and consistent with the WP-01 BA-02 read-side Business Activity pattern in every structural respect (get-by-id → 404-if-missing → return, no audit, no event) — no correctness, security, or tenant-isolation defect was found. The unrelated pre-existing uncommitted/untracked documents present at session start (`CLAUDE.md`, `ARM-001_Implementation_Report.md`, and the AR-001/AAR-001 governance-audit-track documents) were confirmed unrelated to BA-02 and are not mistaken for scope creep.

---

## BA-03 — Frame Structural Change Intent

## Business Activity Implemented

**BA-03 — Frame Structural Change Intent**, realizing PE-001-C005's ERB-C005-03 (Frame Structural Change Intent) / EX-C005-04 (Frame Structural Change Intent). Realizes SCI-000001 (Structural Change Intent), the canonical Business Object registered by `ADR-006`/IRA-004 §21. No ERG-001 domain business rule governs this Business Activity — Structural Change Intent is a PE-001-C005-native experience-layer construct, not an ERG-001 structural/domain object (ADR-006's own Aggregate Root finding), the same disclosed layer distinction IRA-004 §5 already drew between PE-001-C005's experience rules and ERG-001's domain rules.

### Business Activity Contract (IMP-001 §6.7)

- **Business Intent:** Allow a caller to record explicit enterprise decision context — business rationale, target structural outcome, and decision boundary — before a structural change may be proposed (ERB-C005-03's own Purpose, verbatim: "Turn an observed structural need into explicit enterprise intent, target outcome and decision context"; BR-C005-001: "A governed structural change SHALL have explicit Change Intent Context").
- **Input Contract:** `change_rationale` (str, required — EX-C005-04's own Required/Consumed Context: "recognized change need"), `target_outcome` (str, required — EX-C005-04's own Produced Context), `decision_boundary` (str, optional — EX-C005-04's own Produced Context, not marked mandatory by its own text).
- **Output Contract:** The framed StructuralChangeIntent (id, change_rationale, target_outcome, decision_boundary, status, created_at, updated_at), or a 422 naming the missing/invalid field.
- **Business Rules:**
  - BR-C005-001 — A governed structural change SHALL have explicit Change Intent Context. Satisfied by construction: this is the only path that creates a `StructuralChangeIntent` row, and `change_rationale`/`target_outcome` are both required (schema validation).
  - BR-C005-002 — Structural Focus SHALL be established before a proposal is shaped. Not directly enforced by BA-03 (no hard dependency on a prior BA-02 call is checked) — EX-C005-04's own Required Context is "Structural Understanding Context and recognized change need" at the experience level, not a database-enforceable precondition; the same disclosed-not-enforced disposition BA-01/BA-02 already established for the PE-001-C005 experience layer generally (IRA-004 §5).
- **Validation Rules:** `change_rationale`/`target_outcome` must be non-empty (422 otherwise, Pydantic `min_length=1`). No duplicate-check exists — EX-C005-04's own text names no unique business key for a Change Intent Context (a deliberate, disclosed difference from BA-01's `node_code`-based duplicate check).
- **Authorization Rules:** `PLATFORM_ADMIN` role required — the same interim gate BA-01/BA-02 and every prior Work Package used. No PE-001-C005 persona (Structural Steward) exists as an enforceable claim today; not newly disclosed (inherits the same TD-021–025/031/034/035/036/039/042/045 class of finding).
- **Domain Events:** `STRUCTURAL_CHANGE_INTENT_FRAMED` (structural_change_intent_id, status).
- **Audit Requirements:** `record_audit("FRAME_STRUCTURAL_CHANGE_INTENT", ...)` on success, per SD-002-054's seven audit questions — same mechanism BA-01/BA-02 established, reused as-is.
- **Tests:** `tests/test_structural_change_intent_service.py` (4 unit tests), `tests/test_structural_change_intent_api.py` (9 API/authorization tests) — 13 new tests, all passing; full AuthService suite (482 tests) passing with zero regressions.

---

## Governing Architecture Review (Step 1) — BA-03

Reviewed for this Business Activity: CLAUDE.md (§14, §16, §17, §19.1–§19.8), SD-002 (§2, Universal Business Object Blueprint — the basis of SCI-000001's own registration), CMD-001 (§26.3–§26.7, Canonical Business Object Register), `ADR-006` (Accepted — registers SCI-000001, downgrades BA-03 to Category C, does not itself authorize implementation), IRA-004 (§4/§9/§10/§21 — BA-03's own candidate disposition and the full CBOR registration entry), PE-001-C005 (ERB-C005-03 §40.4, EX-C005-04 §41.5 and EX-C005-05 §41.6, re-extracted verbatim from `_PE-001-C005_ba02_check.txt` during this Business Activity's own readiness assessment), `OrganizationNodeService`/`OrganizationNodeRepository`/`OrganizationNodeRepository` (BA-01/BA-02, the direct Establish-Business-Activity structural precedent), `OrganizationEstablishmentAttempt` (WP-01A, evaluated and found only a partial structural analog — see below), `BaseRepository[T]`, `observability.py`, `dependencies.require_platform_admin`, `middleware/tenant.py`'s exemption pattern.

**Key finding requiring disclosure (already recorded in the BA-03 readiness assessment):** EX-C005-04's own Required Context is "Structural Understanding Context and recognized change need" — not a bound reference to a specific EnterpriseNode/EnterpriseRelationship row. The `DERIVED_FROM` relationship IRA-004 §21 records as Pending Canonical Binding is confirmed, by direct comparison against EX-C005-05's own Required Context ("Change Intent Context **and current structural context**"), to be BA-04's resolution responsibility, not a BA-03 precondition. `StructuralChangeIntent` therefore carries no FK to `organization_nodes` or any future `organization_hierarchy` row — binding a structural target here would absorb BA-04's own scope, which this Business Activity deliberately does not do.

**Second finding:** `OrganizationEstablishmentAttempt` (WP-01A) was evaluated as a candidate reuse template ("governed intermediate decision object with its own table") and found only a partial analog: that object is deliberately never exposed through any read path, while SCI-000001 is designed to be read by a later, independently-invoked BA-04 (EX-C005-05's own Required/Consumed Context names it explicitly). No read endpoint is added by BA-03 itself (TD-051) — BA-03's own scope is `Create` only (IRA-004 §4).

---

## Gap Analysis Summary — BA-03 (see the BA-03 readiness assessment and IRA-004 §21 for the underlying disposition)

- **Database:** New table, `structural_change_intents` — a genuine Create, not an Extend (no existing table maps to SCI-000001, confirmed by IRA-004 §21's own Aggregate Root finding). Single new migration (`f7a2d9c4e6b1`), chained onto the existing head (`e5c1a9f4b7d2`); `alembic heads` confirms exactly one head after this migration.
- **Business Activities:** BA-03 is the third Business Activity authorized for implementation under this report's own fresh gap analysis (this section, consuming ADR-006's Category C reclassification); BA-04 through BA-09 remain candidate-only (IRA-004 §4), each requiring its own gap analysis before implementation, per CLAUDE.md §19.7.
- **API Impact:** One new endpoint, `POST /structural-change-intents` (Frame), mirroring the established Establish-Business-Activity shape (schema/repository/service/router layering, create-then-audit-then-event) minus the duplicate-check step (no natural unique key exists for this object — disclosed, not silently copied from BA-01).
- **UI Impact:** Out of scope for BA-03 (backend Business Activity implementation only, matching every prior WP's own precedent).
- **Dependencies:** BA-02 (satisfied — implemented, committed). No dependency on BA-04–BA-09.
- **Missing runtime capabilities / canonical objects:** None required beyond the new table itself — `BaseRepository[T]`, `observability.py`, `require_platform_admin`, and the Pydantic schema pattern are all directly reusable.
- **Missing repositories / services:** `StructuralChangeIntentRepository`/`StructuralChangeIntentService` — new, mirroring `OrganizationNodeRepository`/`OrganizationNodeService`'s own minimal shape.
- **Missing authorization:** Same disclosed, pre-existing `PLATFORM_ADMIN`-only interim gate as every other write-side Business Activity in this repository (not a new gap; not separately registered, per §19.8.3).
- **Missing audit / events:** None — both are implemented (`FRAME_STRUCTURAL_CHANGE_INTENT` audit action, `STRUCTURAL_CHANGE_INTENT_FRAMED` event).
- **Technical Debt raised:** TD-051 (no read endpoint yet — deferred to BA-04's own gap analysis), TD-052 (lifecycle transitions beyond CREATED not implemented — deferred to BA-04 through BA-08's own future gap analyses).

**Conclusion: READY, implemented.** BA-03 required one new table and three new thin wrapper layers (repository/service/router), all following directly reusable patterns — no new architecture, permission, or event mechanism was introduced.

---

## Documents Updated (BA-03)

**Architecture:**
- `architecture/05-Implementation/IMP-REPORT-WP-04_Enterprise_Structure_Management.md` (this report, BA-03 section)
- `architecture/06-Reviews/TECH-DEBT.md` (TD-051, TD-052 added)
- `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md` (WP-04 row updated to reflect BA-03 implemented and independently reviewed)

**Implementation (new):**
- `Backend/Services/AuthService/models/structural_change_intent.py`
- `Backend/Services/AuthService/repositories/structural_change_intent_repository.py`
- `Backend/Services/AuthService/schemas/structural_change_intent.py`
- `Backend/Services/AuthService/services/structural_change_intent_service.py`
- `Backend/Services/AuthService/routers/structural_change_intent.py`
- `Backend/Services/AuthService/alembic/versions/2026_08_03_0900-f7a2d9c4e6b1_structural_change_intent.py`
- `Backend/Services/AuthService/tests/test_structural_change_intent_service.py`
- `Backend/Services/AuthService/tests/test_structural_change_intent_api.py`

**Implementation (modified):**
- `Backend/Services/AuthService/main.py` — registered the new `structural_change_intent` router at `/structural-change-intents`.
- `Backend/Services/AuthService/middleware/tenant.py` — added `/structural-change-intents` and `/structural-change-intents/*` to the tenant-exemption list (`StructuralChangeIntent` carries no `organization_id` column, the same basis `/organization-nodes`' own exemption documents).

No other existing model, repository, service, or router was modified.

---

## Validation (BA-03)

- 13 new tests (4 unit, 9 API), all passing.
- Full AuthService suite: **482 passed**, zero regressions (re-run directly: 469 pre-existing + 13 new).
- Confirmed a single Alembic head (`f7a2d9c4e6b1`) after the new migration (`alembic heads`, `alembic history` — chained onto `e5c1a9f4b7d2`, no branch point introduced).
- Confirmed BR-C005-001: every successful `POST /structural-change-intents` call persists a real, identity-bearing row; `change_rationale`/`target_outcome` cannot be empty (422).
- Confirmed `decision_boundary` may be omitted without error.
- Confirmed two structurally-identical requests each create their own distinct row (no 409/deduplication) — the disclosed, deliberate difference from BA-01's own duplicate-check pattern.
- Confirmed non-`PLATFORM_ADMIN` callers receive 403; missing/invalid Authorization header returns 400/401 respectively.
- Confirmed `POST /structural-change-intents` requires no `X-Tenant-ID` header (tenant-exemption list).
- Confirmed via `git status`/`git diff --stat` that only the files listed under Documents Updated above were touched — no BA-04–BA-09 code, no structural-target/EnterpriseNode FK, and no lifecycle-transition code exists anywhere in the change set.
- OpenAPI schema (`app.openapi()`) generated successfully with `POST /structural-change-intents` present (single `post` operation) among 61 total paths — recounted directly against the current repository state, not assumed from BA-02's own (pre-WP-01A/pre-rebrand) figure.
- Live Postgres `alembic upgrade`/`alembic check` was not exercised — `alembic check` was attempted and failed only with a connection-refused error (no running Postgres instance available in this environment), the same limitation every prior WP's own validation carried; static verification (`alembic heads`/`history`) was performed instead.

---

## Status (BA-03)

**Implementation:** COMPLETE

**Developer Validation:** Complete (482/482 full suite passing, re-run directly during this report's own preparation)

**Independent Review:** APPROVED WITH OBSERVATIONS

**Repository Commit:** Committed to `master` in two commits — `e411aa5` (implementation: 10 files) and `62df1c7` (documentation: this report, TECH-DEBT.md TD-051/052, WPR-001 WP-04 row).

**Commit Hash:** `e411aa5` (implementation), `62df1c7` (documentation: implementation report, TECH-DEBT.md, WPR-001)

**Commit Date:** 2026-07-29 (both commits)

---

## Independent Review (BA-03)

**Review Result:** APPROVED WITH OBSERVATIONS

**Review Summary:** An independent reviewer, with no prior involvement in BA-03's implementation, verified the implementation against actual repository state rather than trusting this report's own claims, and re-ran the full test suite directly. ADR-006's own text was re-confirmed to authorize registration only, not implementation — this Business Activity's own gap analysis (this report, above) was performed fresh rather than assumed satisfied by the registration alone, satisfying CLAUDE.md §19.7's Business Activity Completion Gate. EX-C005-04 and EX-C005-05 were both re-extracted directly from `_PE-001-C005_ba02_check.txt` and compared side-by-side: EX-C005-04's Required Context ("Structural Understanding Context and recognized change need") was confirmed to name no structural target, while EX-C005-05's Required Context ("Change Intent Context and current structural context") was confirmed to be the first point at which a structural target is required — validating the decision not to add an EnterpriseNode/EnterpriseRelationship FK to `StructuralChangeIntent` as a textually-grounded reading, not a convenient assumption. `git status`/`git diff --stat` confirmed no BA-04–BA-09 code, no structural-target FK, and no lifecycle-transition code (MODIFIED/SUPERSEDED/ABANDONED/WITHDRAWN/ARCHIVED) exists anywhere in the change set — matching BA-03's own disclosed minimal-CREATED-only scope. The CheckConstraint on `status` was confirmed to match IRA-004 §21's own registered Lifecycle Model exactly (six values), with TD-052 recorded for the five unreachable-by-BA-03 values rather than silently left undocumented. `OrganizationEstablishmentAttempt` was independently re-compared against `StructuralChangeIntent` and confirmed to be only a partial analog (write-only vs. read-later), validating the report's own disclosed reasoning for not copying that pattern's own read-exclusion. Tests were re-run directly: 13/13 new tests pass, 482/482 full suite passes, matching this report's own claims exactly; both new test files were read in full to confirm each test isolates a genuinely distinct behavior (creation, default status, optional-field omission, no-deduplication, and the full authorization/tenant-exemption matrix are each separately covered).

Findings recorded, none blocking:
1. **TD-051** (no read endpoint yet for Structural Change Intent) — recorded in `TECH-DEBT.md` in the same pass as this review, consistent with §19.8.2's registration-hygiene rule.
2. **TD-052** (lifecycle transitions beyond CREATED not implemented) — recorded in `TECH-DEBT.md` in the same pass as this review, mirroring BA-01's own already-accepted minimal-slice disposition (IRA-004 §5) rather than a newly discovered gap class.
3. **Observation, non-blocking:** BR-C005-002 (Structural Focus established before framing) is disclosed as not database-enforced by BA-03 (experience-level guidance, not a persisted precondition) — consistent with how BA-01/BA-02 already treated PE-001-C005's own experience-layer Business Rules (IRA-004 §5). Not acted upon further here; no dependent capability currently requires enforcement.
4. **Inherited, not re-raised:** No PE-001-C005 persona (Structural Steward, etc.) exists as an enforceable claim — the same disclosed, pre-existing `PLATFORM_ADMIN`-only interim gate as every prior write-side Business Activity in this repository; not separately re-registered, per §19.8.3.
5. The implementation itself was found complete, correct against BR-C005-001 and EX-C005-04's own Required/Produced Context, and consistent with the established Establish-Business-Activity pattern in every structural respect except the deliberately-disclosed absence of a duplicate check — no correctness, security, tenant-isolation, or scope-creep (BA-04 absorption) defect was found.

---

## BA-04 — Shape / Refine Proposed Structural Outcome

## Business Activity Implemented

**BA-04 — Shape / Refine Proposed Structural Outcome**, realizing PE-001-C005's ERB-C005-04 (Shape Proposed Structural Outcome) / EX-C005-05 (Shape Structural Proposal) and EX-C005-06 (Refine Structural Proposal). Realizes POC-000001 (Proposed Outcome Context), the canonical Business Object registered by `ADR-008`/IRA-004 §22. Proposal target scoped to EnterpriseNode only for v1, per `ADR-007`. No ERG-001 domain business rule governs this Business Activity — Proposed Outcome Context, like Structural Change Intent, is a PE-001-C005-native experience-layer construct, not an ERG-001 domain object.

### Business Activity Contract (IMP-001 §6.7)

- **Business Intent:** Allow a caller to develop an intended structural result against an existing Structural Change Intent and EnterpriseNode target, and to iteratively refine it while preserving every prior revision (ERB-C005-04's own Purpose, verbatim: "Develop the intended structural result while preserving current context for comparison").
- **Input Contract (Shape):** `structural_change_intent_id` (UUID, required — must reference an existing `StructuralChangeIntent`), `target_organization_node_id` (UUID, required — must reference an existing `OrganizationNode`, ADR-007's v1 scope), `proposed_outcome_description` (str, required).
- **Input Contract (Refine):** `proposal_id` (UUID, path parameter — identifies the lineage), `proposed_outcome_description` (str, required — the only field a revision may change; `structural_change_intent_id`/`target_organization_node_id` are copied forward unchanged, per BR-C005-004).
- **Output Contract:** The shaped/refined revision (id, proposal_id, revision_number, structural_change_intent_id, target_organization_node_id, proposed_outcome_description, status, created_at, updated_at), or a 404 naming the missing reference.
- **Business Rules:**
  - BR-C005-003 — Current structural context SHALL remain distinguishable from Proposed Outcome Context. Satisfied by construction: `StructuralProposal` is its own table/object, never conflated with `OrganizationNode`.
  - BR-C005-004 — Every proposal revision SHALL remain traceable to the change intent that produced it. Satisfied by construction: `structural_change_intent_id` is copied forward, unchanged, across every revision in a lineage; Refine's own schema does not accept a different value.
  - §41.14 (C-005 Context Contract) — "A material proposal revision SHALL invalidate readiness and dependent impact/review conclusions that no longer apply" (BR-C005-005). Not enforced by this Business Activity: no readiness marker is implemented yet (TD-053) — there is nothing to invalidate.
- **Validation Rules:** `structural_change_intent_id` and `target_organization_node_id` must reference existing rows (404 otherwise, mirroring ERG-001-03's "must be addressable and resolvable" discipline already applied to `Membership.home_node_id`); `proposal_id` (Refine) must reference an existing proposal lineage (404 otherwise). No duplicate-check on Shape — Proposed Outcome Context has no natural business key, the same disclosed difference BA-03 already established.
- **Authorization Rules:** `PLATFORM_ADMIN` role required — the same interim gate every prior write-side Business Activity in this repository has used.
- **Domain Events:** `STRUCTURAL_PROPOSAL_SHAPED` (proposal_id, revision_id, revision_number), `STRUCTURAL_PROPOSAL_REFINED` (proposal_id, revision_id, revision_number, superseded_revision_id).
- **Audit Requirements:** `record_audit("SHAPE_STRUCTURAL_PROPOSAL", ...)` and `record_audit("REFINE_STRUCTURAL_PROPOSAL", ...)` on success, per SD-002-054's seven audit questions.
- **Tests:** `tests/test_structural_proposal_service.py` (6 unit tests), `tests/test_structural_proposal_api.py` (12 API/authorization tests) — 18 new tests, all passing; full AuthService suite (500 tests) passing with zero regressions.

---

## Governing Architecture Review (Step 1) — BA-04

Reviewed for this Business Activity: CLAUDE.md (§14, §16, §17, §19.1–§19.8), SD-002 (§2), CMD-001 (§26.3–§26.7), `ADR-007` (Accepted — EnterpriseNode-only v1 proposal-target scope), `ADR-008` (Accepted — registers POC-000001), IRA-004 (§4/§9/§10/§22 — BA-04's own candidate disposition, readiness assessment, and full CBOR registration entry), PE-001-C005 (ERB-C005-04 §40.5, EX-C005-05 §41.6, EX-C005-06 §41.7, and §41.14's C-005 Context Contract, re-extracted verbatim from `_PE-001-C005_ba02_check.txt` during BA-04's own readiness assessment), `StructuralChangeIntentRepository`/`OrganizationNodeRepository` (BA-01/BA-03, reused directly to validate BA-04's two FK inputs), `BaseRepository[T]`, `observability.py`, `dependencies.require_platform_admin`, `middleware/tenant.py`'s exemption pattern.

**Key finding requiring disclosure (already recorded in the BA-04 readiness assessment):** this repository has no existing precedent for a revision/versioning write path — every prior write-side Business Activity (BA-01, BA-03) is a single-state create-or-read. BA-04 introduces an **append-only revision model**: `proposal_id` (stable lineage identity, equal to `id` for revision 1) plus `revision_number` (incrementing per Refine), with each row's own substantive content (`proposed_outcome_description`) never altered after insert — only `status` transitions (CREATED → SUPERSEDED), satisfying POC-000001's own registered Versioning Policy ("Full version history retained; superseded revisions preserved in traceability, never physically deleted").

**Second finding:** "initial Comparison Context" (EX-C005-05's own Produced Context, alongside Proposed Outcome Context) was re-checked against the Cross-Experience Reference Test during BA-04's own readiness assessment and found not to qualify as a registered Business Object (named only within EX-C005-05's own text). It is not persisted or computed by this Business Activity — TD-054, not silently omitted.

---

## Gap Analysis Summary — BA-04 (see the BA-04 readiness assessment and IRA-004 §22 for the underlying disposition)

- **Database:** New table, `structural_proposals` — a genuine Create (POC-000001 is its own Aggregate Root, IRA-004 §22). FKs to `structural_change_intents.id` and `organization_nodes.id`. Single new migration (`a3c6f8e1d5b2`), chained onto the existing head (`f7a2d9c4e6b1`); `alembic heads` confirms exactly one head after this migration.
- **Business Activities:** BA-04 is the fourth Business Activity authorized for implementation under this report's own fresh gap analysis (this section, consuming ADR-007's and ADR-008's reclassifications); BA-05 through BA-09 remain candidate-only (IRA-004 §4).
- **API Impact:** Two new endpoints — `POST /structural-proposals` (Shape) and `POST /structural-proposals/{proposal_id}/revisions` (Refine). The Refine endpoint is deliberately a `POST`-a-new-revision-resource shape, not `PUT`/`PATCH`, since it literally inserts a new row rather than mutating one in place — a disclosed naming decision, not an accident of convenience.
- **UI Impact:** Out of scope for BA-04 (backend Business Activity implementation only).
- **Dependencies:** BA-01 and BA-03 (both satisfied — `organization_nodes` and `structural_change_intents` both exist). No dependency on BA-05–BA-09.
- **Missing runtime capabilities / canonical objects:** None required beyond the new table — every repository/service/audit/event mechanism reused directly.
- **Missing repositories / services:** `StructuralProposalRepository` (new, adds `get_current_revision()` beyond the inherited `BaseRepository` methods — no natural-key lookup applies here) / `StructuralProposalService` (new).
- **Missing authorization:** Same disclosed, pre-existing `PLATFORM_ADMIN`-only interim gate as every other write-side Business Activity in this repository.
- **Missing audit / events:** None — both implemented for Shape and Refine separately.
- **Technical Debt raised:** TD-053 (lifecycle transitions beyond CREATED/SUPERSEDED not implemented), TD-054 (Comparison Context not persisted), TD-055 (no read endpoint — mirrors TD-051), TD-056 (no unique constraint on `(proposal_id, revision_number)` — a concurrent-revision race, mirroring TD-005/TD-006's own class).

**Conclusion: READY, implemented.** BA-04 required one new table, two new thin wrapper layers (repository/service), one new router with two endpoints, and one genuinely new pattern (append-only revisions) — no new architecture, permission, or event mechanism otherwise.

---

## Documents Updated (BA-04)

**Architecture:**
- `architecture/05-Implementation/IMP-REPORT-WP-04_Enterprise_Structure_Management.md` (this report, BA-04 section)
- `architecture/06-Reviews/TECH-DEBT.md` (TD-053, TD-054, TD-055, TD-056 added)
- `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md` (WP-04 row updated to reflect BA-04 implemented and independently reviewed)

**Implementation (new):**
- `Backend/Services/AuthService/models/structural_proposal.py`
- `Backend/Services/AuthService/repositories/structural_proposal_repository.py`
- `Backend/Services/AuthService/schemas/structural_proposal.py`
- `Backend/Services/AuthService/services/structural_proposal_service.py`
- `Backend/Services/AuthService/routers/structural_proposal.py`
- `Backend/Services/AuthService/alembic/versions/2026_08_04_0900-a3c6f8e1d5b2_structural_proposal.py`
- `Backend/Services/AuthService/tests/test_structural_proposal_service.py`
- `Backend/Services/AuthService/tests/test_structural_proposal_api.py`

**Implementation (modified):**
- `Backend/Services/AuthService/main.py` — registered the new `structural_proposal` router at `/structural-proposals`.
- `Backend/Services/AuthService/middleware/tenant.py` — added `/structural-proposals` and `/structural-proposals/*` to the tenant-exemption list.

No other existing model, repository, service, or router was modified.

---

## Validation (BA-04)

- 18 new tests (6 unit, 12 API), all passing.
- Full AuthService suite: **500 passed**, zero regressions (re-run directly: 482 pre-existing + 18 new).
- Confirmed a single Alembic head (`a3c6f8e1d5b2`) after the new migration, chained onto `f7a2d9c4e6b1`.
- Confirmed BR-C005-003/004: `StructuralProposal` is its own table; `structural_change_intent_id`/`target_organization_node_id` are copied forward unchanged across a 3-revision chain (tested directly).
- Confirmed the append-only property directly: after Refine, the prior revision's own `proposed_outcome_description` is unchanged and its `status` is `SUPERSEDED`; the new revision carries the new description at `status=CREATED`.
- Confirmed Shape/Refine each reject an unknown FK reference with 404, not 500 or a silently-created orphan row.
- Confirmed non-`PLATFORM_ADMIN` callers receive 403; missing/invalid Authorization header returns 400/401 respectively.
- Confirmed both endpoints require no `X-Tenant-ID` header (tenant-exemption list).
- Confirmed via `git status`/`git diff --stat` that only the files listed under Documents Updated above were touched — no BA-05–BA-09 code and no Comparison Context/validation-readiness code exists anywhere in the change set.
- OpenAPI schema (`app.openapi()`) generated successfully with both `POST /structural-proposals` and `POST /structural-proposals/{proposal_id}/revisions` present among 63 total paths.
- Live Postgres `alembic upgrade`/`alembic check` was not exercised — `alembic check` was attempted and failed only with a connection-refused error (no running Postgres instance available in this environment), the same limitation every prior Business Activity's validation carried.

---

## Status (BA-04)

**Implementation:** COMPLETE

**Developer Validation:** Complete (500/500 full suite passing, re-run directly during this report's own preparation)

**Independent Review:** APPROVED WITH OBSERVATIONS

**Repository Commit:** Committed to `master` in two commits — `17cba1e` (implementation: 10 files) and `c60cf97` (documentation: this report, TECH-DEBT.md TD-053–056, WPR-001 WP-04 row).

**Commit Hash:** `17cba1e` (implementation), `c60cf97` (documentation: implementation report, TECH-DEBT.md, WPR-001)

**Commit Date:** 2026-07-29 (both commits)

---

## Independent Review (BA-04)

**Review Result:** APPROVED WITH OBSERVATIONS

**Review Summary:** An independent reviewer, with no prior involvement in BA-04's implementation, verified the implementation against actual repository state rather than trusting this report's own claims, and re-ran the full test suite directly. `ADR-007`'s own EnterpriseNode-only v1 scope and `ADR-008`'s own POC-000001 registration were each re-confirmed Accepted and unamended by this implementation — this Business Activity consumes both decisions rather than re-litigating them. The append-only revision model was independently traced through `StructuralProposalService.refine_proposal()`'s actual control flow: the current revision is read via `get_current_revision()` (ordered by `revision_number` descending), its own `status` is set to `SUPERSEDED` (a status transition, confirmed by direct inspection to be the only field changed on that row — `proposed_outcome_description` is never reassigned), and a genuinely new row is inserted for the next revision. A three-revision chain was independently exercised (`test_refine_proposal_operates_on_the_current_revision_after_multiple_refinements`) and confirmed both earlier revisions end in `SUPERSEDED`, not just the immediately-prior one. `git diff --stat` confirmed no BA-05–BA-09 code exists anywhere in the change set, and that Comparison Context/validation-readiness code was genuinely absent (not merely untested) — consistent with TD-054/TD-053's own disclosures. The `id`-population defect found and fixed during this Business Activity's own development (assigning `proposal_id = proposal.id` before the ORM's Python-side `default=uuid.uuid4` had been evaluated, which would have silently persisted `proposal_id = NULL` had the `NOT NULL` constraint not caught it at flush) was independently re-verified fixed: `structural_proposal_service.py` now generates the id explicitly via `uuid4()` before insertion rather than reading it back from an unflushed object. Tests were re-run directly: 18/18 new tests pass, 500/500 full suite passes, matching this report's own claims exactly.

Findings recorded, none blocking:
1. **TD-053** (lifecycle transitions beyond CREATED/SUPERSEDED not implemented) — recorded in `TECH-DEBT.md`, mirroring TD-052's own precedent class for SCI-000001.
2. **TD-054** (Comparison Context not persisted) — recorded in `TECH-DEBT.md`; independently re-verified that Comparison Context genuinely fails the Cross-Experience Reference Test (grep confirms it is named only within EX-C005-05's own text) rather than being a rationalized omission.
3. **TD-055** (no read endpoint) — recorded in `TECH-DEBT.md`, mirroring TD-051's own identical precedent; independently confirmed IRA-004 §4 types BA-04 as `Create / Update` only, with no `Query` type listed, supporting the scoping decision as textually grounded rather than convenient.
4. **TD-056** (no unique constraint on `(proposal_id, revision_number)`, a concurrency race) — recorded in `TECH-DEBT.md` as a newly-identified, genuine gap (not previously disclosed anywhere prior to this Business Activity's own implementation) — the same class of finding TD-005/TD-006 already established for WP-01, not a novel category of risk to this repository.
5. **Inherited, not re-raised:** No PE-001-C005 persona (Structural Steward, etc.) exists as an enforceable claim — the same disclosed, pre-existing `PLATFORM_ADMIN`-only interim gate as every prior write-side Business Activity in this repository.
6. The implementation itself was found complete, correct against BR-C005-003/004 and EX-C005-05/-06's own Required/Produced Context, and consistent with this repository's established audit/event pattern in every respect except the deliberately-new append-only revision mechanism (itself found correct) — no correctness, security, tenant-isolation, or scope-creep (BA-05 absorption) defect was found beyond the id-population defect already caught and fixed during development, not left for independent review to discover.

---

## BA-05 — Assess Structural Consequence

## Business Activity Implemented

**BA-05 — Assess Structural Consequence**, realizing PE-001-C005's ERB-C005-05 (Assess Structural Consequence) / EX-C005-07. Realizes IMC-000001 (Impact Context), the canonical Business Object registered by `ADR-009`/IRA-004 §23. No ERG-001 domain business rule governs this Business Activity — Impact Context, like Structural Change Intent and Proposed Outcome Context, is a PE-001-C005-native experience-layer construct, not an ERG-001 domain object.

### Business Activity Contract (IMP-001 §6.7)

- **Business Intent:** Allow a caller to record computed impact and uncertainty context — affected structural areas, known/uncertain consequences, and identified downstream capability implications — for one specific proposal revision, prior to review (ERB-C005-05's own Purpose, verbatim: "Understand affected structural context and identify downstream capability implications before review").
- **Input Contract:** `structural_proposal_id` (UUID, required — must reference an existing `StructuralProposal` revision), `impact_description` (str, required), `uncertainty_notes` (str, optional), `downstream_implications` (str, optional).
- **Output Contract:** The persisted assessment (id, structural_proposal_id, impact_description, uncertainty_notes, downstream_implications, status, created_at, updated_at), or a 404 naming the missing proposal.
- **Business Rules:**
  - BR-C005-008 — C-005 SHALL identify downstream capability implications but SHALL not execute outcomes owned by those capabilities. Satisfied by construction: `downstream_implications` is a free-text identification field only; no downstream capability API is called, no event beyond `STRUCTURAL_CONSEQUENCE_ASSESSED` is published.
- **Validation Rules:** `structural_proposal_id` must reference an existing row (404 otherwise); `impact_description` must be non-empty (422 otherwise). No check that the referenced revision is still current/non-`SUPERSEDED` (TD-059, disclosed rather than assumed either way). No duplicate-check — Impact Context has no natural business key, the same disclosed difference already established for SCI-000001/POC-000001.
- **Authorization Rules:** `PLATFORM_ADMIN` role required — the same interim gate every prior write-side Business Activity in this repository has used.
- **Domain Events:** `STRUCTURAL_CONSEQUENCE_ASSESSED` (impact_assessment_id, structural_proposal_id).
- **Audit Requirements:** `record_audit("ASSESS_STRUCTURAL_CONSEQUENCE", ...)` on success.
- **Tests:** `tests/test_impact_assessment_service.py` (4 unit tests), `tests/test_impact_assessment_api.py` (9 API/authorization tests) — 13 new tests, all passing; full AuthService suite (513 tests) passing with zero regressions.

---

## Governing Architecture Review (Step 1) — BA-05

Reviewed for this Business Activity: CLAUDE.md (§14, §16, §17, §19.1–§19.8), SD-002 (§2), CMD-001 (§26.3–§26.7), `ADR-009` (Accepted — registers IMC-000001), IRA-004 (§4/§9/§10/§23 — BA-05's own candidate disposition, readiness assessment, and full CBOR registration entry), PE-001-C005 (ERB-C005-05 §40.6, EX-C005-07 §41.8, and Chapter 42's own "Impact Context is mandatory for review readiness" text), `StructuralProposalRepository` (BA-04, reused directly to validate BA-05's own single FK input), `BaseRepository[T]`, `observability.py`, `dependencies.require_platform_admin`, `middleware/tenant.py`'s exemption pattern.

**Key finding requiring disclosure (already recorded in the BA-05 constitutional-alignment task):** IRA-004 §4 types BA-05 as "Query (computed)" at the Business Activity level (it reads a proposal and computes an assessment; no existing structural data is mutated) — but the assessment itself is a registered, persisted Business Object (IMC-000001), so this implementation's own router uses `POST` (create), not a contradiction between the "Query" typing and a write-shaped endpoint.

**Second finding:** setting `ImpactAssessment.status` to `INVALIDATED` (EX-C005-07's own Invalidated Context: "Impact observations invalidated by material proposal revision") would require reaching into BA-04's own, already-implemented and independently-reviewed `refine_proposal()` flow. Deliberately not done here — "implement only what BA-05 owns" — recorded as TD-057, not silently assumed satisfied.

---

## Gap Analysis Summary — BA-05 (see IRA-004 §23 for the underlying disposition)

- **Database:** New table, `impact_assessments` — a genuine Create (IMC-000001 is its own Aggregate Root, IRA-004 §23). FK to `structural_proposals.id` (one specific revision). Single new migration (`b8e4d1a7c3f9`), chained onto the existing head (`a3c6f8e1d5b2`); `alembic heads` confirms exactly one head after this migration.
- **Business Activities:** BA-05 is the fifth Business Activity authorized for implementation under this report's own fresh gap analysis (this section, consuming ADR-009's reclassification); BA-06 through BA-09 remain candidate-only (IRA-004 §4).
- **API Impact:** One new endpoint, `POST /impact-assessments`, mirroring the established create-then-audit-then-event shape (BA-03's own precedent) minus a duplicate-check.
- **UI Impact:** Out of scope for BA-05 (backend Business Activity implementation only).
- **Dependencies:** BA-04 (satisfied — `structural_proposals` exists). No dependency on BA-06–BA-09.
- **Missing runtime capabilities / canonical objects:** None required beyond the new table — every repository/service/audit/event mechanism reused directly.
- **Missing repositories / services:** `ImpactAssessmentRepository`/`ImpactAssessmentService` (new, minimal — no natural-key lookup, mirroring `StructuralChangeIntentRepository`'s own shape).
- **Missing authorization:** Same disclosed, pre-existing `PLATFORM_ADMIN`-only interim gate.
- **Missing audit / events:** None — both implemented.
- **Technical Debt raised:** TD-057 (lifecycle transitions beyond CREATED not implemented — mirrors TD-052/TD-053), TD-058 (no read endpoint — mirrors TD-051/TD-055), TD-059 (no check that the referenced revision is still current).

**Conclusion: READY, implemented.** BA-05 required one new table and two new thin wrapper layers (repository/service) plus a router — no new architecture, permission, or event mechanism.

---

## Documents Updated (BA-05)

**Architecture:**
- `architecture/05-Implementation/IMP-REPORT-WP-04_Enterprise_Structure_Management.md` (this report, BA-05 section)
- `architecture/06-Reviews/TECH-DEBT.md` (TD-057, TD-058, TD-059 added)
- `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md` (WP-04 row updated to reflect BA-05 implemented and independently reviewed)

**Implementation (new):**
- `Backend/Services/AuthService/models/impact_assessment.py`
- `Backend/Services/AuthService/repositories/impact_assessment_repository.py`
- `Backend/Services/AuthService/schemas/impact_assessment.py`
- `Backend/Services/AuthService/services/impact_assessment_service.py`
- `Backend/Services/AuthService/routers/impact_assessment.py`
- `Backend/Services/AuthService/alembic/versions/2026_08_05_0900-b8e4d1a7c3f9_impact_assessment.py`
- `Backend/Services/AuthService/tests/test_impact_assessment_service.py`
- `Backend/Services/AuthService/tests/test_impact_assessment_api.py`

**Implementation (modified):**
- `Backend/Services/AuthService/main.py` — registered the new `impact_assessment` router at `/impact-assessments`.
- `Backend/Services/AuthService/middleware/tenant.py` — added `/impact-assessments` and `/impact-assessments/*` to the tenant-exemption list.

No other existing model, repository, service, or router was modified.

---

## Validation (BA-05)

- 13 new tests (4 unit, 9 API), all passing.
- Full AuthService suite: **513 passed**, zero regressions (re-run directly: 500 pre-existing + 13 new).
- Confirmed a single Alembic head (`b8e4d1a7c3f9`) after the new migration, chained onto `a3c6f8e1d5b2`.
- Confirmed BR-C005-008: `downstream_implications` is persisted as identification only; no downstream capability endpoint is called anywhere in the code path.
- Confirmed `POST /impact-assessments` rejects an unknown `structural_proposal_id` with 404, not 500 or a silently-created orphan row.
- Confirmed optional fields (`uncertainty_notes`, `downstream_implications`) may be omitted without error.
- Confirmed two assessments against the same proposal each create their own distinct row (no deduplication).
- Confirmed non-`PLATFORM_ADMIN` callers receive 403; missing/invalid Authorization header returns 400/401 respectively.
- Confirmed the endpoint requires no `X-Tenant-ID` header (tenant-exemption list).
- Confirmed via `git status`/`git diff --stat` that only the files listed under Documents Updated above were touched — no BA-06–BA-09 code and no invalidation/cross-BA-04-coupling code exists anywhere in the change set.
- OpenAPI schema (`app.openapi()`) generated successfully with `POST /impact-assessments` present among 64 total paths.
- Live Postgres `alembic upgrade`/`alembic check` was not exercised — `alembic check` was attempted and failed only with a connection-refused error (no running Postgres instance available in this environment), the same limitation every prior Business Activity's validation carried.

---

## Status (BA-05)

**Implementation:** COMPLETE

**Developer Validation:** Complete (513/513 full suite passing, re-run directly during this report's own preparation)

**Independent Review:** APPROVED WITH OBSERVATIONS

**Repository Commit:** recorded below, Documents Updated section, upon commit.

**Commit Hash:** *(recorded in a follow-up commit-hash-recording commit, per this Work Package's own established 3-commit convention)*

**Commit Date:** 2026-07-29

---

## Independent Review (BA-05)

**Review Result:** APPROVED WITH OBSERVATIONS

**Review Summary:** An independent reviewer, with no prior involvement in BA-05's implementation, verified the implementation against actual repository state rather than trusting this report's own claims, and re-ran the full test suite directly. `ADR-009`'s own IMC-000001 registration was re-confirmed Accepted and unamended by this implementation. `ImpactAssessmentService.assess_structural_consequence()` was read in full and confirmed to reuse `StructuralProposalRepository.get_by_id()` directly rather than re-implementing a lookup, and to persist `downstream_implications` as plain text with no call of any kind to a downstream-capability API — satisfying BR-C005-008's own "identify but do not execute" boundary by construction, not merely by convention. `git diff --stat` confirmed no BA-06–BA-09 code exists anywhere in the change set, and specifically that no change was made to `services/structural_proposal_service.py` (BA-04) — confirming TD-057's own disclosure that invalidation-on-revision was deliberately not implemented, rather than silently attempted and failing. The "Query (computed) type but POST verb" apparent tension was independently checked against BA-03's own identical precedent (a Create-typed Business Activity using POST) and found consistent, not a new inconsistency. Tests were re-run directly: 13/13 new tests pass, 513/513 full suite passes, matching this report's own claims exactly; both new test files were read in full to confirm each test isolates a genuinely distinct behavior (creation, optional-field omission, unknown-FK rejection, no-deduplication, and the full authorization/tenant-exemption/validation matrix are each separately covered).

Findings recorded, none blocking:
1. **TD-057** (lifecycle transitions beyond CREATED not implemented) — recorded in `TECH-DEBT.md`, mirroring TD-052/TD-053's own precedent class.
2. **TD-058** (no read endpoint) — recorded in `TECH-DEBT.md`, mirroring TD-051/TD-055's own identical precedent.
3. **TD-059** (no currency check against the proposal's own current revision) — recorded in `TECH-DEBT.md` as a genuinely new observation (not previously disclosed anywhere prior to this Business Activity); independently confirmed EX-C005-07's own Trigger text does not resolve the question either way, so this is a disclosed open design choice, not a defect being excused.
4. **Inherited, not re-raised:** No PE-001-C005 persona exists as an enforceable claim — the same disclosed, pre-existing `PLATFORM_ADMIN`-only interim gate as every prior write-side Business Activity in this repository.
5. The implementation itself was found complete, correct against BR-C005-008 and EX-C005-07's own Required/Produced Context, and consistent with this repository's established audit/event pattern — no correctness, security, tenant-isolation, or scope-creep (BA-06 absorption, or reaching into BA-04's own code) defect was found.

---

*End of IMP-REPORT-WP-04 (BA-01 through BA-05). BA-06 through BA-09 remain candidate-only per IRA-004 §4 — each requires its own fresh gap analysis before implementation, per CLAUDE.md §19.7.*
