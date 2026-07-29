# IRA-001 — WP-01 Implementation Readiness Assessment
### Organization Management (C-004)

**Status:** Approved — WP-01 READY
**Classification:** Implementation Readiness Assessment (canonical IRA template — see "Future Reuse" at the end of this document)
**Work Package:** WP-01 — Organization Management (C-004)
**Approved scope (revised per §15 WP-01 Scope Reconciliation):** Organization identity establishment, resolution, search/listing, identity stewardship, suspension/reactivation, and retirement — realizing PE-001-C004's seven canonical ERBs. Explicitly excludes Role & Permission Management, Membership Management, and Workspace Management (subsequent work packages). Configuration and Audit History are **removed** from WP-01's scope — see §15; they were never canonical C-004 Business Activities.
**Documents reviewed:** CLAUDE.md, ARCH-000, CAP-001 (§2 Registry, C-004 entry), ERG-001, URA-001 (§2, Organization-relevant principles), CMD-001 (§17 Enterprise Domain), Master Technical Architecture (Part A, `organization_master`/`organization_node`/`organization_hierarchy` DDL + RLS chapter), RTA-001 (§4.13, runtime execution chain), IMP-001 (§1.7, §6.3–6.7 Business Activity Lifecycle/Contract), SD-001 (§5 Layout Templates, §7 Screen Anatomy), SD-002 (§7 Event/Lifecycle/Audit Rules), DS-001 (Component Catalogue, Ch.13), GRC-001 (§ Scope/Audit cross-reference), WP-00 Certification Report, WP-00A Completion Report, current repository structure and git status, PE-001 Enterprise Experience Blueprint (Ch.13–15), **`PE-001-C004_Organization_Management.docx` (extracted and reviewed in full — see §15; this is the authoritative Capability Experience Specification for C-004, previously unreadable, now the governing document for this IRA's Business Activity list).**

---

## 1. Executive Summary

WP-01 is **READY** to begin implementation.

The assessment identified several architectural decisions that required explicit governance approval before implementation commenced. These decisions have now been approved and recorded as Architecture Decision Records:

- **ADR-003** — Organization Management Implementation Ownership
- **ADR-004** — Organization Canonical Schema Scope
- **ADR-005** — Organization Lifecycle (interim model)

They are implementation governance decisions rather than architectural blockers and therefore do not prevent implementation.

---

## 2. Readiness Assessment

### 2.1 Capability Assessment
- **Primary Capability:** C-004 Organization Management (CAP-001 §2, line 55) — Primary Specification **ERG-001**, Domain D-001 Enterprise Foundation, Status Active.
- **Supporting Capabilities:** C-005 Enterprise Structure Management (shares ERG-001 as Primary Spec; WP-01 must respect ERG-001-03's Organization→EnterpriseNode graph-ownership contract without implementing C-005 itself). C-114 Audit & Assurance (SD-002 §7 — every lifecycle transition WP-01 produces must satisfy SD-002-054's seven audit questions).
- **Dependent Capabilities:** C-001/C-002/C-006/C-007 (Identity/Access/Person/Membership, URA-001) — WP-00's `Membership.organization_id` FK and `home_node_id` contract (URA-001-17b) already depend on Organization existing; WP-01 must not break this.
- **Future Capabilities (explicitly excluded per approved scope):** C-003 Role & Permission Management, C-007 Membership Management (full surface), Workspace Management.

#### Recorded Architectural Decisions (summary)

The following findings were identified during this assessment as requiring an explicit governance call. They are now resolved and recorded as ADRs — they are not implementation blockers.

| Finding | Resolution |
|---|---|
| Service ownership ambiguity (AuthService vs. TenantService) | **ADR-003 — Recorded.** |
| Canonical schema gap (7 columns vs. ~25-column `organization_master`) | **ADR-004 — Recorded.** |
| No lifecycle state model / no Metadata Runtime | **ADR-005 — Recorded.** |

Full ADR text and traceability: §12 and §13.

### 2.2 Business Activity Assessment (revised per §15 WP-01 Scope Reconciliation)
Per IMP-001 §1.7 ("Business Activities Over CRUD"), none of the following may be exposed as raw REST CRUD — each needs a full Business Activity Contract (§6.7): Business Intent, Input/Output Contract, Business Rules, Validation Rules, Authorization Rules, Metadata Dependencies, Domain Events, Audit Requirements, Tests.

This table originally listed 8 Business Activities, including "Configure Organization" and "View Organization Audit History," proposed before `PE-001-C004` (the authoritative Capability Experience Specification for C-004) could be read. Now that it has been (§15), the table below is the corrected, canonical-ERB-mapped list of 7 Business Activities.

| Business Activity | Type (§6.6 taxonomy) | Business Object | Domain Event | Canonical ERB (PE-001-C004) | Status |
|---|---|---|---|---|---|
| BA-01 — Establish Organization Identity | Create | Organization | `ORGANIZATION_ESTABLISHED` | ERB-C004-01 | ✅ Complete |
| BA-02 — Resolve Organization Details | Query | Organization | none | ERB-C004-04 | ✅ Complete |
| BA-03 — Search & List Organizations | Query (read-side) | Organization | none | Platform Administrator operational capability (no direct ERB — reasonable admin tooling, not a canonical Enterprise Experience) | ✅ Complete |
| BA-04 — Steward Organization Identity | Update | Organization | `ORGANIZATION_PROFILE_UPDATED` | ERB-C004-05 | ✅ Complete |
| BA-05 — Reactivate Suspended Organization | Update (state transition) | Organization | `ORGANIZATION_ACTIVATED` | ERB-C004-06 / EX-C004-09 | ✅ Complete |
| BA-06 — Suspend Organization | Update (state transition) | Organization | `ORGANIZATION_SUSPENDED` | ERB-C004-06 / EX-C004-08 | ✅ Complete |
| BA-07 — Retire Organization & Preserve Continuity | Update (state transition, terminal) | Organization | `ORGANIZATION_RETIRED` | ERB-C004-07 | ⏳ Planned |

**Removed** (never canonical C-004 Business Activities — see §15): ~~Configure Organization~~, ~~View Organization Audit History~~.

None of the Domain Event names above are canonically pre-defined anywhere (RTA-001 §4.13 gives examples like `EVIDENCE_VERIFIED`/`REPORT_PUBLISHED`, not Organization-specific ones; PE-001-C004 itself records every Business Activity/EAC binding as "Pending Canonical Binding") — they are proposed here for planning purposes only, consistent with SD-002-053 ("Event Types Are Tenant-Configurable Metadata... new event types require no application deployment, only a metadata record"), which again presumes the Metadata Runtime addressed by ADR-005.

**Business Rules / States / Lifecycle:** SD-002-051 mandates lifecycle be metadata-driven, tenant-configurable, version-controlled. No metadata-driven lifecycle state machine for Organization exists in any canonical document — resolved by ADR-005 (interim model). PE-001-C004 defines a **third lifecycle state, `RETIRED`** (terminal, irreversible), in addition to the `ACTIVE`/`SUSPENDED` pair ADR-005 already scoped as WP-01's interim model — `RETIRED` is BA-07's scope, not yet implemented.

### 2.3 Architecture Impact
See Architecture Impact Matrix (§4).

### 2.4 Backend Impact
See Backend Impact Matrix (§6).

### 2.5 Frontend Impact
See UI Impact Matrix (§5). Headline: **no DS-001/SD-001 gap** — Master-Detail layout template (SD-001 §5) + Guided Completion for the create flow, composed from existing/extendable DS-001-named components, following the `features/person/` precedent exactly (state hook + components + services/*-api.ts + types/*.ts). The blocker identified was backend readiness, not frontend architecture — and backend readiness is now resolved by ADR-003/ADR-004.

### 2.6 Database Impact
See Database Impact Matrix (§7).

### 2.7 Security Assessment
- **Authentication:** N/A — Organization Management endpoints ride on AuthService's existing JWT bearer auth (unchanged).
- **Authorization:** Explicitly out of WP-01 scope (Role & Permission Management is a separate WP), **but** every Business Activity above requires "Authorization Rules" per IMP-001 §6.4 — this creates a soft dependency: WP-01 cannot ship Activate/Suspend/Update endpoints with real authorization checks until *some* permission model is callable. Minimum viable resolution: gate on the existing `is_system_role`/`PLATFORM_ADMIN` role seeded in WP-00 (already exists), explicitly deferring fine-grained Domain Permission checks (VIEW/EDIT/APPROVE per URA-001 §4) to the Role & Permission Management work package. This must be a stated, approved simplification, not a silent gap (see Implementation Guardrails, §12).
- **Roles/Permissions:** Not implemented by WP-01. WP-01 must not invent role/permission logic.
- **Feature Flags:** WP-00's `FeatureFlagService` is reusable as-is (interim mechanism, already flagged as such per IC-001 E1) — e.g. `ff_organization_management_v1` gating rollout is consistent with existing pattern.
- **Audit:** SD-002 §7 (owned by C-114) is the binding requirement — every Organization lifecycle transition needs an immutable, seven-question-answering audit record. WP-00's `observability.py` (`record_audit`) is the only currently-usable mechanism (same documented "temporary local stand-in" status as WP-00) — reusable, not a new build.
- **Encryption:** No Organization field identified in either candidate schema (current or canonical `organization_master`) requires field-level encryption; standard transport/at-rest DB encryption applies (unchanged from AuthService baseline).

### 2.8 Integration Assessment
- **External Systems:** None identified for C-004 specifically.
- **Internal Services:** TenantService overlap resolved by ADR-003 (TenantService remains scaffolding, untouched by WP-01). Membership (WP-00, AuthService) already FK-depends on `organizations.id` — must not be broken.
- **Events/Queues:** `docker-compose.yml` declares a Kafka topic `aurex.tenant.provisioning` that nothing in the codebase currently publishes or consumes — not a WP-01 dependency, but worth noting as a likely-related, currently-dead integration point.
- **Notifications/Search/AI:** None identified as in-scope for C-004's approved WP-01 boundary.

### 2.9 Vertical Slice Assessment
A complete slice (DB → Backend → API → Frontend → Business Activity → Tests → Observability → Docs) is achievable in principle — WP-00 proved this pattern works end-to-end for Bootstrap. With ADR-003/004/005 recorded, the slice is no longer blocked upstream.

### 2.10 Testing Strategy
Per IMP-001 §11 (already applied in WP-00): IMP-TEST-001 (Business Activity Contract tests) as primary layer, IMP-TEST-002 (Authorization Boundary tests) — constrained by §2.7's authorization simplification, IMP-TEST-003 (idempotency, if any seed/provisioning logic is added). Standard unit/integration/contract tests per the existing `tests/conftest.py` SQLite-in-memory pattern. Every Business Activity shall include Unit Tests, Integration Tests, and Business Activity Tests per the Implementation Guardrails (§12).

### 2.11 Deployment Assessment
- **Migration:** New Alembic revision(s) needed, scoped per ADR-004. IMP-CICD-001's 2-release deprecation floor applies if any existing `organizations` columns are renamed/removed.
- **Rollback:** Additive columns/tables are safely reversible; the ADR-005 lifecycle-state migration (adding a status column) is additive and low-risk.
- **Feature Flags:** Reuse WP-00's mechanism (see §2.7).
- **Backward Compatibility:** Must not break WP-00's `Membership.organization_id` FK or bootstrap seeding (`DEMO_ORGANIZATION`).
- **Monitoring/Operational Readiness:** Extend WP-00's `/ready` pattern and `observability.py` — reuse, not rebuild.

### 2.12 Risks
See Risk Register (§8).

### 2.13 Implementation Plan
See §9.

### 2.14 Work Breakdown
See §9 (folded in — phase-level breakdown is more useful than a raw file/module count at this stage).

### 2.15 Success Criteria
- Every Business Activity in §2.2 has a full BAC per IMP-001 §6.7.
- Every lifecycle transition produces a Domain Event and an audit record (SD-002-054's seven questions answered).
- Tenant isolation (RLS or equivalent) is explicit and tested, not assumed.
- DS-001/SD-001 compliance: Master-Detail + Guided Completion, composed only from named DS-001 components.
- Zero new architecture invented silently; every governance decision is recorded as an ADR before its dependent code is written.
- Every Business Activity is independently certifiable (see Implementation Guardrails, §12).

---

## 3. Architecture Impact Matrix

| Component | Current State | WP-01 Impact | Decision Needed First? |
|---|---|---|---|
| Owning microservice | Ambiguous (AuthService real model vs. TenantService branded-but-mocked) | Determines everything below | **Architectural Decision Recorded (ADR-003)** |
| `organizations` table (AuthService) | 7 columns, live, migrated | Extended per approved subset | **Architectural Decision Recorded (ADR-004)** |
| `organization_master` (canonical, Master Technical Architecture) | Defined on paper only, not implemented anywhere | Reference target; full shape not built by WP-01 | **Architectural Decision Recorded (ADR-004)** |
| `Tenant`/`TenantConfig`/`TenantUser` (TenantService) | Mocked, no migrations, no real DB | Untouched by WP-01 | **Architectural Decision Recorded (ADR-003)** |
| Metadata Runtime (RTA-001 §9, SD-002-051) | Does not exist anywhere in repo | Interim model used instead | **Architectural Decision Recorded (ADR-005)** |
| Event Bus / Domain Event publication | `observability.py` `publish_event()` (log-only stand-in) | Reusable as interim, same as WP-00 | No — reuse existing interim |
| RLS on Organization's own table | Absent in canonical DDL (`organization_master`) and in AuthService's actual table | Must confirm intended model | Open — non-blocking implementation task (§11) |
| `BaseRepository` | No `update()` method | Needs extension | No — mechanical |
| `middleware/tenant.py` | Dead code (WP-00 finding, unresolved) | Any real `/organizations` endpoints would be the first live routes subject to it | No — surfaces the pre-existing dead-code issue for the first time in practice |

## 4. Business Activity Matrix

See §2.2 (Business Activities, Types, Events, canonical ERB mapping). Business Rules/Validation Rules per activity are now traceable to `PE-001-C004`'s ERB/EX definitions (§15) rather than pending that document's review.

## 5. UI Impact Matrix (revised per §15 — Configuration and Audit History rows removed, never canonical)

| Screen/Component | SD-001 Pattern | DS-001 Components (existing in `ui/`) | DS-001 Components (named, not yet built) |
|---|---|---|---|
| Organization List | Master-Detail (list side) | Table, Card, Button, Breadcrumb | Filter Bar, Bulk Action Row, Saved View Selector, Pagination |
| Organization Detail | Master-Detail (detail side) + Progressive Disclosure | Card, StatusBadge, Modal | Action Center |
| Establish Organization | Guided Completion | Form, Input, Button, Spinner | Select, Stepper |
| Activate/Suspend | Action Center action | Modal, Button, StatusBadge | Action Center |
| Retire (BA-07, planned) | Action Center action (irreversible — requires explicit confirmation per PE-001-C004 §1.7 "Explainable governance") | Modal, Button, StatusBadge | Action Center |
| Existing placeholder routes | — | `/organization` (App), `/platform-admin/organizations` (Admin) — two separate placeholder routes already exist; one to be selected (§11) |

No DS-001 gap-escalation is required — missing components are named in DS-001's catalogue and buildable as shared `ui/` additions (per DS-001-230A, not capability-scoped), following the `features/person/` precedent exactly.

## 6. Backend Impact Matrix

| Layer | New | Modified |
|---|---|---|
| Model | Extended per ADR-004's approved subset | `models/organization.py` |
| Repository | `organization_repository.py` | `base_repository.py` (add `update()`) |
| Schema (Pydantic) | `schemas/organization.py` (Create/Update/Response/List/AuditEntry DTOs) | — |
| Router | `routers/organization.py` | `main.py` (register router), `routers/__init__.py` |
| Service | `services/organization_service.py` (Business Activity orchestration, mirroring `bootstrap_service.py`'s structure) | `services/__init__.py` |
| Migration | New Alembic revision(s), scoped per ADR-004 | — |
| Tests | `tests/test_organization_service.py`, `tests/test_organization_api.py` | — |
| Observability | — | Reuse `observability.py` as-is |

## 7. Database Impact Matrix

| Change | Notes |
|---|---|
| New columns on `organizations` | Scoped per ADR-004's approved subset (Lifecycle, CRUD, Profile, Search, Validation) — "Configuration" removed from ADR-004's originally-cited areas per §15; no Organization Configuration Business Activity is canonical |
| Lifecycle/status column | Per ADR-005's interim `ACTIVE`/`SUSPENDED` model |
| Index on searchable fields (name, code — code already indexed) | Additive, low-risk |
| Constraints | Unique `organization_code` already exists; no new constraint conflicts identified |
| RLS | Needs explicit confirmation of intended model (§11, non-blocking) |
| Seed data | WP-00's `DEMO_ORGANIZATION` remains valid; MDP-001 governs any further seed rows |

## 8. Risk Register

| # | Risk | Type | Severity | Status |
|---|---|---|---|---|
| 1 | Building Organization CRUD in AuthService while TenantService's README/branding claims the same capability | Architecture | — | **Resolved by ADR (ADR-003).** |
| 2 | Building against the current 7-column `organizations` table vs. the canonical 25-column `organization_master` shape | Architecture/Delivery | — | **Resolved by ADR (ADR-004).** |
| 3 | Implementing "activation/suspension" as a bare boolean, silently contradicting SD-002-051's metadata-driven lifecycle mandate | Architecture/Compliance | — | **Resolved by ADR (ADR-005).** |
| 4 | Designing UI/business rules without having read PE-001-C004 (capability-specific experience spec) | Delivery/Compliance | **Major** | **Resolved.** PE-001-C004 read in full during the WP-01 Scope Reconciliation (§15); two Business Activities (Configure, Audit History) were found to have no canonical basis and were removed; one canonical ERB (Retire) was found unplanned and added as BA-07. |
| 5 | RLS gap on the tenant-boundary-defining table itself, shipped without confirming whether that's intentional | Security | **Major** | Open — non-blocking implementation task |
| 6 | Authorization simplification (PLATFORM_ADMIN-only gating) shipped without being flagged as a deliberate, temporary scope reduction | Security/Compliance | **Minor** | Open — mitigated by Implementation Guardrails (§12) |
| 7 | Two existing placeholder routes (`/organization`, `/platform-admin/organizations`) both getting built out independently | Delivery | **Minor** | Open — non-blocking implementation task |
| 8 | `middleware/tenant.py`'s dead-code exemption pattern (WP-00 finding) becomes live and untested for the first time in this same work package | Technical | **Minor** | Open — mitigated by testing strategy (§2.10) |

## 9. Implementation Plan (phased, each phase a working vertical slice — no Big Bang) — revised per §15

**Phase 0 — Decisions (no code):** ✅ Complete. ADR-003, ADR-004, ADR-005 recorded.

**Phase 1 — Read-side vertical slice:** ✅ Complete. BA-02 Resolve Organization Details, BA-03 Search & List Organizations.

**Phase 2 — Establish Organization:** ✅ Complete. BA-01 Establish Organization Identity.

**Phase 3 — Lifecycle:** ✅ Complete. BA-05 Reactivate Suspended Organization, BA-06 Suspend Organization (per ADR-005's interim model; audit and Domain Event on every transition, per the established `record_audit`/`publish_event` pattern).

**Phase 4 — Identity Stewardship:** ✅ Complete. BA-04 Steward Organization Identity. ("Configuration" removed from this phase's original scope per §15 — never canonical.)

**Phase 5 — Retire:** ⏳ Planned. BA-07 Retire Organization & Preserve Continuity (ERB-C004-07) — the sole remaining Business Activity. ("Audit History & Search/Listing polish" removed from this phase's original scope per §15 — Search & Listing already delivered as BA-03 in Phase 1; Audit History was never canonical.)

Each phase ships a demonstrable, tested, documented increment — consistent with CLAUDE.md §5 ("Never skip validation") and IMP-001's Business Activity Contract-per-activity structure.

## 10. Recommended Implementation Sequence (revised per §15)

1. Phase 1 (read-side) — ✅ complete, proved the foundation.
2. Phase 2 (Establish) — ✅ complete.
3. Phase 3 (Lifecycle: Suspend/Reactivate) — ✅ complete, implements ADR-005's interim model.
4. Phase 4 (Identity Stewardship) — ✅ complete.
5. Phase 5 (Retire) — ⏳ the sole remaining phase; BA-07 Retire Organization & Preserve Continuity, per PE-001-C004's ERB-C004-07.

## 11. Recorded Architectural Decisions

The following governance decisions have been approved. They are informational — they do not block implementation.

- **ADR-003** — Organization implementation owner is AuthService; TenantService remains scaffolding; future service extraction occurs after the Modular Monolith phase.
- **ADR-004** — WP-01 implements the approved Organization subset (Lifecycle, CRUD, Profile, Configuration, Search, Validation); the complete canonical Organization model in Master Technical Architecture remains unchanged and is implemented incrementally by future work packages.
- **ADR-005** — The metadata-driven lifecycle defined by SD-002 remains the target architecture; until the Metadata Runtime exists, WP-01 implements an interim lifecycle model (e.g. `ACTIVE`/`SUSPENDED`) with clearly documented extension points, following the same interim implementation strategy already approved during WP-00.

### Remaining non-blocking implementation tasks

- ~~Read `PE-001-C004_Organization_Management.docx`...~~ **Resolved** — read in full during the WP-01 Scope Reconciliation (§15); a `.md` conversion is still a reasonable follow-up (matching CAP-001's precedent) but no longer blocks anything (Risk #4 closed).
- Confirm RLS intent on the Organization table before real data crosses environments beyond local dev (Risk #5).
- Select one of the two existing placeholder routes (`/organization` vs. `/platform-admin/organizations`) as WP-01's UI target (Risk #7).

---

## 12. Implementation Guardrails

The following constraints shall govern WP-01 implementation.

- Implement only the approved WP-01 scope.
- Do not introduce Identity Management.
- Do not introduce Membership Management.
- Do not introduce Workspace Management.
- Do not introduce Licensing.
- Do not introduce Role or Permission Management.
- Do not redesign platform architecture during implementation.
- Follow the Business Activity methodology defined in IMP-001.
- Do not duplicate business logic across services.
- Use only documented interim implementations with clear extension points.
- Maintain backward compatibility with the approved architecture.
- Every Business Activity shall include:
  - Unit Tests
  - Integration Tests
  - Business Activity Tests
  - Documentation
- Every implementation shall be independently certifiable.

## 13. Architecture Decision Traceability

| ADR | Description | Used By |
|---|---|---|
| ADR-003 | Organization implementation ownership | WP-01 |
| ADR-004 | Canonical Organization schema scope | WP-01 |
| ADR-005 | Interim lifecycle model | WP-01 |

This table establishes traceability between Architecture Decision Records and Work Packages and is a standard section of all future Implementation Readiness Assessments.

## 14. Final Recommendation

**OPTION A — WP-01 READY**

**Overall Assessment**

| Area | Status |
|---|---|
| Architecture | READY |
| Engineering Standards | READY |
| Repository | READY |
| Platform Foundation | READY |
| Business Activities | READY |
| Testing Strategy | READY |
| Documentation Strategy | READY |
| Dependencies | READY |

No architectural blockers remain. The assessment identified several architectural decisions that have now been formally approved and recorded. These decisions ensure that WP-01 proceeds in full alignment with:

- Master Technical Architecture
- IMP-001
- Engineering Architecture
- Modular Monolith implementation strategy
- WP-00 implementation approach

WP-01 may now proceed through the approved implementation lifecycle:

Implementation Readiness Assessment → Implementation → Implementation Report → Independent Certification → Remediation → Re-Certification → Commit

---

## 15. WP-01 Scope Reconciliation

**Date:** 2026-07-21
**Trigger:** Before starting the originally-planned BA-07 (Configure Organization), a governing-canonical-asset review (CLAUDE.md §19.1) surfaced that `PE-001-C004_Organization_Management.docx` — flagged in this IRA's header as unreviewed, and in Risk #4 (§8) as a Major, Open risk — had never actually been read. It was `.docx`-only and unreadable by available file tools; its raw text was extracted directly from the archive and read in full (1461 paragraphs) before any further implementation proceeded.

**Findings:**

- `PE-001-C004` is the authoritative Capability Experience Specification for C-004 (Gold Standard, v1.1) and became the governing document for Organization Management's Business Activity scope once read.
- It defines exactly seven Enterprise Experience Blueprints (ERB-C004-01 through -07) and a three-state lifecycle (`ACTIVE`/`SUSPENDED`/**`RETIRED`**) — not the two-state `ACTIVE`/`SUSPENDED` pair ADR-005 scoped as WP-01's interim model.
- This IRA's original §2.2 Business Activity table (8 items) was drafted before `PE-001-C004` could be read and was self-labeled "proposed here for planning purposes only" — not itself a canonical source.
- **Configuration** and **Audit History** — 2 of the original 8 planned Business Activities — have **no corresponding ERB, EX, or scope clause anywhere in `PE-001-C004`** (confirmed by full-text search of the extracted document). ADR-004 independently and separately already deferred every configuration-flavored canonical field (`reporting_framework_json`, `board_meeting_frequency`, `daily_brief_enabled_flag`, etc.) to future work packages pending an actual consumer — reinforcing that WP-01 never had a genuine need for Configuration. Audit History's underlying concern (auditability) is already satisfied cross-cuttingly by `observability.py`'s `record_audit()` calls in every implemented Business Activity, consistent with SD-002-054 and C-114 Audit & Assurance — a platform-wide concern, not a distinct C-004 Enterprise Experience.
- **ERB-C004-07 (Retire Organization & Preserve Continuity)** — a real, fully-specified canonical ERB with its own `RETIRED` terminal lifecycle state — had **no corresponding Business Activity anywhere in this IRA's original plan**. This is the gap in the opposite direction: real canonical scope with no implementation plan.
- Two Business Activities were renamed for precision against canonical terminology: "Activate Organization" → **"Reactivate Suspended Organization"** (it implements ERB-C004-06/EX-C004-09, a reversible reactivation of an already-established Organization — not ERB-C004-03/EX-C004-04's distinct "Activate Organization," which means completing first-time establishment); "Establish Organization" → "Establish Organization Identity" and "Update Organization Profile" → "Steward Organization Identity" and "View Organization Details" → "Resolve Organization Details," aligning naming with ERB-C004-01/05/04 respectively without changing any implemented behavior, API, or Domain Event name.

**Resolution:**

- IRA-001's §2.2 Business Activity table is corrected to 7 canonical-ERB-mapped Business Activities (§2.2, above).
- Configuration and Audit History are removed — they were never canonical C-004 Business Activities.
- BA-07 is now **Retire Organization & Preserve Continuity** (ERB-C004-07), replacing the two removed items — the sole remaining planned Business Activity.
- **No architecture changed.** No entity, table, column, service boundary, or permission tier was added, removed, or redefined by this reconciliation.
- **No implementation was discarded.** BA-01 through BA-06 are unchanged in the codebase; only their names and canonical cross-references in planning documents were corrected. No commit was reverted, no code was rewritten.
- **No ADR was required.** This is not two canonical authorities in genuine conflict — it is a planning document's self-flagged, provisional content (this IRA's §2.2, explicitly written before `PE-001-C004` could be reviewed) being superseded by the actual canonical Capability Specification once read, exactly the outcome this IRA's own Risk #4 anticipated. There was no architectural tradeoff to adjudicate, only a plan to correct.
- This is a **planning correction**, not an architectural change, per CLAUDE.md §16's canonical authority resolution: `PE-001-C004` (the governing Capability Specification) takes precedence over this IRA's provisional Business Activity list wherever they conflict.

**Cross-reference:** The corresponding update to `IMP-REPORT-WP-01_Organization_Management.md` records the same reconciliation against the implementation report's dashboard and Business Activity sections.

---

## Future Reuse

This Implementation Readiness Assessment establishes the canonical IRA structure for future work packages.

Future assessments (IRA-002, IRA-003, etc.) shall follow the same structure unless superseded by enterprise engineering standards.

The standard IRA sections shall be:

1. Executive Summary
2. Capability Assessment
3. Business Activity Assessment
4. Architecture Impact
5. UI Impact
6. Backend Impact
7. Database Impact
8. Security Assessment
9. Integration Assessment
10. Testing Strategy
11. Risk Register
12. Implementation Plan
13. Work Breakdown
14. Success Criteria
15. Recorded Architectural Decisions
16. Implementation Guardrails
17. ADR Traceability
18. Final Recommendation
