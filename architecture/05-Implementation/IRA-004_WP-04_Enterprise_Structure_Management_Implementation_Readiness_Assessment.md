# IRA-004 — WP-04 Implementation Readiness Assessment
### Enterprise Structure Management (C-005)

**Status:** Approved — WP-04 READY (BA-01 only; BA-02 onward re-assessed per Business Activity, per the Business Activity Completion Gate, CLAUDE.md §19.7) — pending final sign-off per this document's own Completion Criteria (§20)
**Classification:** Implementation Readiness Assessment (canonical IRA template, per IRA-001/IRA-002/IRA-003)
**Work Package:** WP-04 — Enterprise Structure Management (C-005), per `WPR-001_Work_Package_Roadmap.md` (row to be added upon this IRA's acceptance, per WPR-001 §3's own maintenance rule: "a row is added... only when... it has an accepted IRA assigning it a specific capability")
**Governing capability specification:** `PE-001-C005_Enterprise_Structure_Management.docx` (extracted and read in full — see §2). Eight canonical ERBs (ERB-C005-01 through -08). Twelve Enterprise Experiences (EX-C005-01 through -12). Twelve Chapter 42.3 Business Rules (BR-C005-001 through -012) — **experience-level**, not domain/data rules (see §5's disclosed distinction). No Chapter 5-style numbered Contracts exist in this document; Chapter 41.14–41.19 instead states six named Contracts (Context, Navigation, Collaboration, AI Assistance, Experience Consistency, Context Preservation — see §6).
**Primary Specification (structural/domain authority):** `ERG-001 — Enterprise Structure & Relationship Management (ESRM)` v2.0, Status **LOCKED**. Defines the canonical Enterprise Relationship Graph — EnterpriseNode, EnterpriseRelationship, EnterpriseView, ConsolidationDetermination, NodePermissionAssignment, TraversalPolicy — the concrete domain objects PE-001-C005 explicitly excludes from its own scope (§38.4: "Enterprise structure entities, relationship semantics, hierarchy rules and structural data models — ERG-001").
**Documents reviewed:** CLAUDE.md (§14, §16, §17, §19.1–§19.8), ARCH-000, CAP-001 (§2 Registry, C-005 entry: Primary Specification ERG-001, Status Active, line 56), ERG-001 (read in full — all 12 sections, AD-001 through AD-005, ERG-001-01 through -11), PE-001-C005 (extracted from `docs/Product/PE-001/capabilities/C-005/PE-001-C005_Enterprise_Structure_Management.docx` and read in full — Chapters 38–42, Appendices A–B), IMP-001 (§6 CBAIP — the Business Activity derivation pattern WP-01/02/03 all used), Master Technical Architecture (§C-ERG-001 amendment changelog; `organization_node`, `organization_hierarchy`, `consolidation_determination`, `enterprise_view_registry`, `traversal_policy_registry`, `node_permission_assignment` DDL, Part A/C, RLS chapter), WPR-001 (confirms WP-01/WP-02/WP-03 all `CLOSED — Certified`; confirms no WP currently owns C-005), IRA-001/IRA-002/IRA-003 (precedent format, the BA-01-only implementation-scoping discipline, and the "derived, no canonical BA identifier" disclosure pattern all three already established), CERT-WP-01/CERT-WP-02/CERT-WP-03 (precedent certification discipline), TECH-DEBT.md (**TD-032, the decisive evidentiary item — see §2**), current AuthService repository structure (`models/organization_node.py`, `repositories/organization_node_repository.py` — both already exist, WP-03 BA-01-era, read-only/minimal; `models/membership.py`'s `home_node_id` nullable FK to `organization_nodes.id`).

---

## 1. Scope

This IRA governs **WP-04 — Enterprise Structure Management (C-005)**. Following the identical discipline IRA-001/002/003 established: this document derives a full candidate Business Activity list from PE-001-C005's eight ERBs (§4), but **fully gap-analyzes and authorizes implementation of BA-01 only** ("Establish Organization Node"). BA-02 through the remainder of the candidate list each require their own fresh gap analysis before implementation begins, per the Business Activity Completion Gate (CLAUDE.md §19.7).

This IRA does not implement code, create a migration, or modify architecture. It is itself an assessment artifact.

---

## 2. Capability Summary

- **Primary Capability:** C-005 Enterprise Structure Management (CAP-001 line 56) — Primary Specification **ERG-001**, Status **Active**, Business Intent "Maintain enterprise structure" (verbatim).
- **Decisive evidence this is WP-04, not a speculative choice:** Three independent repository artifacts, each written before this IRA and each unaware of the others, all name C-005 as the next capability:
  1. **IRA-001 §2** (WP-01, Organization Management): "Supporting Capabilities: C-005 Enterprise Structure Management (shares ERG-001 as Primary Spec; WP-01 must respect ERG-001-03's Organization→EnterpriseNode graph-ownership contract without implementing C-005 itself)."
  2. **IRA-003 §4, BA-04** (WP-03, Membership Management): BA-04 (Reconfirm Home-Node Structural Congruence) is recorded **BLOCKED — External Capability Dependency (C-005)**, "remains blocked pending C-005's own future charter."
  3. **TD-032** (`TECH-DEBT.md`, raised in WP-03 BA-01): *"Target Resolution: Enterprise Structure Management (C-005)'s own future 'Establish Organization Node' Business Activity... Resolution Criteria: C-005 is chartered with its own IRA and implements Establish Organization Node."* TD-032 names WP-04's own BA-01 by its exact title before this IRA was drafted.
- **Capability boundary, quoted verbatim (PE-001-C005 §38.4 Out of Scope):** "Enterprise structure entities, relationship semantics, hierarchy rules and structural data models — ERG-001." / "Database, API, event, service, routing, component or screen design." / "Identity, role, permission and authorization policy — URA-001." C-005's own specification is explicitly experience-level only; it "does not specify screens, APIs, services, databases, structural entities, relationship rules, authorization policies, workflow mechanics or state-machine implementation" (§42.15).
- **Structural/domain authority for concrete objects: ERG-001**, not PE-001-C005. This is a material difference from WP-01/03: PE-001-C004/C007 each carried their own domain-level Business Rules and Contracts (e.g., BR-C007-007's home-node anchor rule) directly implementable against a database. PE-001-C005's own Chapter 42.3 Business Rules (BR-C005-001 through -012) are **experience/UX-flow rules** ("Structural Focus SHALL be established before a proposal is shaped"), not domain/persistence rules. The domain rules and concrete entities WP-04 must implement come from **ERG-001** (AD-001–005, ERG-001-01 through -11), not from PE-001-C005. This distinction is disclosed here rather than glossed over — see §5.
- **Runtime Execution Boundary:** Not directly touched by BA-01. NodePermissionAssignment resolution into URA-001-76's precedence chain (ERG-001-10) is a downstream concern of a later Business Activity, not BA-01.
- **Upstream Dependencies (consumed, never redefined):** C-004 (Organization Context — WP-01, closed — `organization_master`/`organizations` already exists), URA-001 (authorization/eligibility, reference only), CAP-001 (capability identity).
- **Downstream Consumers:** C-007 Membership Management (WP-03, closed — BA-04 is directly unblocked by this Work Package's own completion; `memberships.home_node_id` already carries the FK), C-002 Access Management (future — NodePermissionAssignment), C-006 Person Management, C-008 Workspace Management (PE-001-C005 §39.9: "C-005 collaborates with Organization Management... Person and Membership capabilities... Access Management... Workspace Management").
- **Explicitly excluded from this capability (verbatim, §38.4):** Identity/role/permission/authorization policy (URA-001); Business Activity execution/orchestration mechanics (IMP-001); database/API/event/service/routing/component/screen design; capability identity and naming (CAP-001).

---

## 3. Enterprise Reference Blueprints (ERBs)

| ERB | Name | Purpose (verbatim, condensed) | Realizing EXs |
|---|---|---|---|
| ERB-C005-01 | Discover Enterprise Landscape | Establish the enterprise boundary and structural scope relevant to the current enterprise objective. | EX-C005-01, -02 |
| ERB-C005-02 | Understand Structural Position | Build an understandable view of how the active Structural Focus relates to surrounding enterprise context. | EX-C005-03 |
| ERB-C005-03 | Frame Structural Change Intent | Turn an observed structural need into explicit enterprise intent, target outcome and decision context. | EX-C005-04 |
| ERB-C005-04 | Shape Proposed Structural Outcome | Develop the intended structural result while preserving current context for comparison. | EX-C005-05, -06 |
| ERB-C005-05 | Assess Structural Consequence | Understand affected structural context and identify downstream capability implications before review. | EX-C005-07 |
| ERB-C005-06 | Review Structural Outcome | Coordinate contextual review and resolve concerns without losing decision continuity. | EX-C005-08, -09 |
| ERB-C005-07 | Validate Transition Readiness | Confirm that the exact reviewed structural outcome is complete enough to become a resulting enterprise state. | EX-C005-10 |
| ERB-C005-08 | Complete Structural Transition | Complete the structural transition, establish resulting context and prepare downstream continuation. | EX-C005-11, -12 |

All eight independently confirmed by direct docx extraction of `PE-001-C005_Enterprise_Structure_Management.docx` (temporary working extract used for this review only, not committed as a repository artifact, mirroring how IRA-001/003 each extracted their own governing docx without committing the raw extract).

**Structural observation, disclosed rather than glossed over:** unlike PE-001-C004/C007's ERBs (each a concrete lifecycle operation — Establish, Suspend, Retire, Maintain Terms), C-005's eight ERBs describe **one generic structural-change experience journey** (Discover→Orient→Frame Intent→Shape→Assess→Review→Validate→Complete), applicable uniformly to *any* structural change (new node, new relationship, consolidation-method change, retirement). PE-001-C005 §42.16 confirms this is intentional: it is "the reference for depth, ownership discipline, context engineering, lifecycle clarity and traceability — not a content template to be mechanically duplicated," and explicitly states its own ERB/EX names and count are not meant to be copied by future capability specs. This has direct consequences for §4's Business Activity derivation.

---

## 4. Business Activities (derived — no canonical BA identifier exists in PE-001-C005 itself, and no canonical EAC registry exists anywhere in this repository to supply one)

**Methodology note, disclosed rather than glossed over:** Every single EX in PE-001-C005 states, verbatim and without exception: *"Bind to applicable canonical Business Activities in the EAC/IMP-001 authority. No local Business Activity identifier is created."* A repository-wide search (`grep -rn "Enterprise Activity Catalog\|canonical EAC"`) confirms **no "Enterprise Activity Catalog" or "EAC" document exists anywhere in this repository.** This is not unique to C-005 — IRA-001 §2.2 records the identical situation for C-004 ("PE-001-C004 itself records every Business Activity/EAC binding as 'Pending Canonical Binding'"). The precedent WP-01/02/03 all followed, and this IRA follows identically, is to derive concrete Business Activities directly from the capability specification's own EX/ERB text using IMP-001 §6.6's taxonomy (Create/Update/Query/Lifecycle Transition, per Business Object), rather than waiting on a canonical EAC binding that does not exist.

**A second, C-005-specific derivation difficulty (disclosed, not silently resolved):** because C-005's EXs describe a generic experience stage rather than a concrete object operation (§3), they do not map 1:1 onto ERG-001's concrete objects (EnterpriseNode, EnterpriseRelationship, ConsolidationDetermination, EnterpriseView, NodePermissionAssignment). A single "Frame Intent → Shape → Assess → Review → Validate → Complete" journey could, in principle, be instantiated against any of those five objects. This IRA does **not** invent a one-to-one ERG-001-object-to-BA assignment. It records the candidate list below as a derivation aid only, exactly as IRA-003 §4 did ("The count above... is a derivation aid, not a commitment").

| BA | Business Activity | Type | Business Object | Governing ERB/EX | Status |
|---|---|---|---|---|---|
| **BA-01** | **Establish Organization Node** | Create | EnterpriseNode (`organization_node`) | ERB-C005-01 / EX-C005-01, -02, cross-referenced against ERG-001-02/03 | ✅ **Implementation authorized under this IRA — see §9, §10** |
| BA-02 | Understand Structural Position | Query | EnterpriseNode (+ relationships) | ERB-C005-02 / EX-C005-03 | ⏳ Not started |
| BA-03 | Frame Structural Change Intent | Create (transient decision context) | Change Intent Context | ERB-C005-03 / EX-C005-04 | ⏳ Not started — no persisted business object is evident from PE-001-C005 or ERG-001; whether this requires a database table or is satisfied by request-scoped context alone is a question for that BA's own gap analysis, not assumed here |
| BA-04 | Shape / Refine Proposed Structural Outcome | Create / Update (proposal) | Proposed Outcome Context (structural change proposal — over EnterpriseNode, EnterpriseRelationship, or ConsolidationDetermination, per §4's disclosed ambiguity) | ERB-C005-04 / EX-C005-05, -06 | ⏳ Not started |
| BA-05 | Assess Structural Consequence | Query (computed) | Impact/Comparison Context | ERB-C005-05 / EX-C005-07 | ⏳ Not started |
| BA-06 | Review Structural Outcome / Resolve Concerns | Update (review) | Review Context | ERB-C005-06 / EX-C005-08, -09 | ⏳ Not started |
| BA-07 | Validate Transition Readiness | Update (validation) | Validation Context | ERB-C005-07 / EX-C005-10 | ⏳ Not started |
| BA-08 | Complete Structural Transition | Update (lifecycle/state transition) | EnterpriseNode / EnterpriseRelationship (`organization_hierarchy`) / ConsolidationDetermination | ERB-C005-08 / EX-C005-11 | ⏳ Not started |
| BA-09 | Continue from Resulting Structure | Query (context carry-forward) | Resulting Structural Context | ERB-C005-08 / EX-C005-12 | ⏳ Not started — likely (not assumed) candidate for a WP-03 BA-09/BA-11-style "no new production code" disposition, given its own Purpose text ("Transfer resulting structural context to the next Enterprise Experience or Journey") closely parallels EX-C007-13's |

**Not listed as a numbered BA, explicitly flagged instead:** Enterprise View configuration (`enterprise_view_registry`), Traversal Policy configuration (`traversal_policy_registry`), and Node Permission Assignment (`node_permission_assignment`) are all canonically specified in ERG-001 (§6, §9) and Master Technical Architecture, but PE-001-C005's own text treats them as instances of the same generic "structural outcome" rather than naming them as distinct ERBs/EXs. Whether each becomes its own Business Activity, or a parameterized variant of BA-04/BA-08, is **not decided here** — it is a future gap-analysis question, exactly mirroring how IRA-003 §4 left the BA-09/BA-10/BA-11 collapse question open rather than assuming an answer.

**Only BA-01 is fully gap-analyzed and authorized for implementation under this IRA.** The candidate list above (9 items) is a derivation aid, not a commitment.

---

## 5. Business Rules

**Disclosed distinction (the central finding of this IRA):** PE-001-C005 Chapter 42.3 states twelve Business Rules, BR-C005-001 through -012. Read in full, every one of them governs the **experience/UX layer** — proposal/review/validation workflow discipline — not data persistence or domain logic:

**Reverse-check mapping (semantic, not a literal citation PE-001-C005 itself makes — the document does not cross-cite BR↔EX identifiers anywhere in Chapter 42.3, the identical disclosure IRA-003 §5 made for BR-C007):**

| BR | Statement (verbatim, Ch. 42.3) | Layer | Nearest governing EX (semantic) | Future BA (candidate, §4) |
|---|---|---|---|---|
| BR-C005-001 | A governed structural change SHALL have explicit Change Intent Context. | Experience | EX-C005-04 | BA-03 |
| BR-C005-002 | Structural Focus SHALL be established before a proposal is shaped. | Experience | EX-C005-03 / -04 boundary | BA-02 / BA-03 |
| BR-C005-003 | Current structural context SHALL remain distinguishable from Proposed Outcome Context. | Experience | EX-C005-05 | BA-04 |
| BR-C005-004 | Every proposal revision SHALL remain traceable to the change intent that produced it. | Experience | EX-C005-06 | BA-04 |
| BR-C005-005 | Material proposal revision SHALL invalidate prior validation readiness. | Experience | EX-C005-10 | BA-07 |
| BR-C005-006 | Review SHALL identify the exact proposal revision under review. | Experience | EX-C005-08 | BA-06 |
| BR-C005-007 | Unresolved review concerns SHALL prevent completion unless the governing decision mechanism records an accepted exception. | Experience | EX-C005-09 / -11 | BA-06 / BA-08 |
| BR-C005-008 | C-005 SHALL identify downstream capability implications but SHALL not execute outcomes owned by those capabilities. | Experience (boundary discipline) | EX-C005-07 | BA-05 |
| BR-C005-009 | Completion SHALL produce Resulting Structural Context. | Experience | EX-C005-11 | BA-08 |
| BR-C005-010 | Exiting without completion SHALL not represent a proposal as resulting enterprise structure. | Experience | All stages (cross-cutting exit path) | BA-03 through BA-08 |
| BR-C005-011 | AI-generated observations SHALL be distinguishable from authoritative structural context. | Experience (AI governance) | **All twelve EXs** (cross-cutting — mirrors BR-C007-012's identical universal disposition) | All BAs |
| BR-C005-012 | Context re-establishment SHALL be explicit whenever enterprise or Structural Focus changes materially. | Experience | EX-C005-01 / -02 | BA-01 / BA-02 |

**Reverse check — every EX has at least one semantically-mapped BR:** EX-01/02 (BR-012), EX-03 (BR-002), EX-04 (BR-001/002), EX-05 (BR-003), EX-06 (BR-004), EX-07 (BR-008), EX-08 (BR-006), EX-09 (BR-007), EX-10 (BR-005), EX-11 (BR-007/009), EX-12 (no EX-specific BR — mirrors EX-C007-13's identical gap in IRA-003 §5, disclosed there and here rather than invented). All twelve EXs additionally carry BR-011 (universal AI-observation rule).

**None of BR-C005-001 through -010 governs BA-01 (Establish Organization Node) as a minimal, direct Create operation** — they govern the full propose→review→validate→complete workflow (BA-03 through BA-08), not the base act of creating an EnterpriseNode row. **BR-C005-011 (AI-observation distinguishability) is universal in principle but satisfied by absence for BA-01**, mirroring WP-01/02/03's own identical disposition for their own AI-assistance rules — BA-01 introduces no AI-assisted feature. **BR-C005-012 (explicit re-establishment on material context change) touches BA-01/BA-02's own context-entry discipline only at the margin** — it governs the *experience* of re-orienting Structural Focus, not the data shape BA-01's Create operation persists; it imposes no additional field, validation, or business rule on BA-01's own implementation. This is disclosed explicitly, not silently assumed: **BA-01, as scoped in this IRA, is a deliberately minimal interim slice that does not yet implement BR-C005-001 through -010's governed-transition discipline.** This mirrors precisely how WP-01's ADR-005 adopted an interim lifecycle model rather than SD-002's full metadata-driven state machine, and how WP-03's BA-06 disclosed a minimal "always reject, Pending Canonical Binding" disposition rather than inventing a lifecycle matrix. The full governed-transition workflow is deferred to BA-03 through BA-08's own future gap analyses.

**BA-01's actual governing rules come from ERG-001, not PE-001-C005:**

| Rule | Statement (verbatim/paraphrased, ERG-001) | Basis |
|---|---|---|
| ERG-001-02 | EnterpriseNode carries a stable, shared identity reference consumed by four independently-governed extension contexts (Structural Identity, Authorization, Financial Consolidation, Reporting Views); a change in one context must never require a change to another's data. | Governs `organization_node`'s own column boundaries — BA-01 must not conflate Structural Identity fields with Authorization/Consolidation/Reporting-View fields |
| ERG-001-03 | Every EnterpriseNode that can serve as a membership's organizational home must be addressable and resolvable at the time a Membership is created; the ERG rejects a Membership creation request referencing a node outside the organization's graph or a non-ACTIVE node. | Directly governs BA-01's required output shape — the row BA-01 creates is exactly what `memberships.home_node_id` (already FK'd, WP-03 BA-01) must be able to reference |
| Master Technical Architecture, `organization_node` DDL | Canonical ~20+ column shape (node_code, node_name, node_type, parent_node_id self-reference note — though hierarchy is separated per the schema's own comment — legal_entity_name, business_unit, sector, geography_id, materiality/risk scores, lifecycle state, etc.) | The canonical target shape BA-01 extends toward; not all columns are BA-01's own scope (§9) |

---

## 6. Contracts

**Disclosed structural difference from IRA-001/002/003:** PE-001-C005 contains **no Chapter 5-style numbered Contracts** (5.1, 5.2, etc.) the way PE-001-C004/C007 did. Instead, Chapter 41.14–41.19 states six named, unnumbered Contracts:

| Contract | Title (verbatim) | Disposition for WP-04 |
|---|---|---|
| §41.14 | C-005 Context Contract | Governs the full proposal/review/validation workflow (BA-03 through BA-08) — not BA-01 as minimally scoped here |
| §41.15 | C-005 Navigation Contract | Cross-cutting UX; no dedicated BA — mirrors WP-02/03's own disposition for their own navigation-style contracts |
| §41.16 | C-005 Collaboration Contract | Cross-cutting; "Most C-005 experiences" involve review/collaboration — relevant to BA-06, not BA-01 |
| §41.17 | C-005 AI Assistance Contract | Satisfied by absence unless a specific BA introduces AI assistance — none currently does, mirroring WP-01/02/03's own identical disposition for their own AI contracts |
| §41.18 | C-005 Experience Consistency Contract | Cross-cutting; satisfied by construction if every BA reuses the same establish/update/audit/event pattern WP-01/02/03 already proved |
| §41.19 | C-005 Context Preservation Contract | Governs BA-02/BA-09 (context read-back / carry-forward) — not BA-01 |

**None of the six Contracts specifically governs BA-01 (Establish Organization Node) as a minimal Create operation** — the same disclosed finding as §5. BA-01's actual governing authority is ERG-001-02/03 (§5) and Master Technical Architecture's DDL, exactly as it was for WP-03's own BA-01 (which built `organization_node`'s minimal predecessor for the identical reason — see §7).

---

## 7. Required Business Objects

- **EnterpriseNode / `organization_node`** — **partially exists.** WP-03 BA-01 already created a **minimal subset** (`models/organization_node.py`, table `organization_nodes`): `id`, `node_code`, `node_name`, `node_type` (free-text), `active_flag`, `created_at`, `updated_at`. The canonical Master Technical Architecture DDL specifies ~20 further columns (legal_entity_name, business_unit, sector, geography_id, materiality/risk scores, lifecycle state beyond a boolean flag, etc.) explicitly deferred by WP-03's own module docstring: "the remaining canonical columns are deferred, not silently omitted." **This Work Package's first task is to extend, not create, this object** — see §10.
- **EnterpriseRelationship / `organization_hierarchy`** — **does not exist.** Confirmed by direct grep across `Backend/Services/AuthService` — zero matches. Canonically specified (ERG-001 §5, Master Technical Architecture DDL) but not yet built by any Work Package. Out of BA-01's own scope (§9).
- **ConsolidationDetermination / `consolidation_determination`** — **does not exist.** Canonically specified (ERG-001-08, Master Technical Architecture DDL). Out of BA-01's own scope.
- **EnterpriseView / `enterprise_view_registry`** — **does not exist.** Canonically specified (ERG-001-06). Out of BA-01's own scope.
- **TraversalPolicy / `traversal_policy_registry`** — **does not exist.** Canonically specified (ERG-001-04). Out of BA-01's own scope.
- **NodePermissionAssignment / `node_permission_assignment`** — **does not exist.** Canonically specified (ERG-001-10). Out of BA-01's own scope; also has a direct URA-001-76 authorization-precedence dependency that a future BA must resolve, not BA-01.
- **Organization** — already exists (WP-01, closed); EnterpriseNode's own governing organization for tenancy purposes.
- **Membership** — already exists (WP-03, closed); `home_node_id` FK already points at `organization_nodes.id`, awaiting a real establish path (TD-032).

No new object *type* beyond `organization_node`'s own extension is required for BA-01. The remaining five ERG-001 objects are real, future WP-04 work (BA-02 onward), not invented here.

---

## 8. Existing Reusable Implementation (from WP-00 through WP-03)

| Component | Source | Reuse for WP-04 |
|---|---|---|
| `models/organization_node.py` (`OrganizationNode`) | WP-03 BA-01 | **Direct extension target** — BA-01 adds the canonical columns Master Technical Architecture specifies and this table currently lacks (§10) |
| `repositories/organization_node_repository.py` (`OrganizationNodeRepository`) | WP-03 BA-01 | **Direct extension target** — currently read-only (inherited `get_by_id()` only, explicit module docstring: "No establish()-style write path is added here"); BA-01 adds the create path |
| `record_audit()` / `publish_event()` (`observability.py`) | WP-00/WP-01 | Direct reuse, no change |
| `BaseRepository[T]` | WP-00/WP-01 | Already the base class of `OrganizationNodeRepository`; BA-01 adds a `create()`-path method following the same pattern WP-03 IRA-003 §13 used for `MembershipRepository` |
| Tenant middleware pattern | WP-01 | Reuse as-is; confirm whether EnterpriseNode is tenant-scoped via its owning Organization (likely yes, mirroring `organization_nodes`' existing FK-free but Organization-adjacent design — to be confirmed at BA-01 implementation time) |
| `require_platform_admin` | WP-01/02/03 | Reuse as the same disclosed interim gate; inherits the same ADR-002-dependent limitation WP-02/03 already logged (TD-021–025, TD-042) — not new debt |
| Establish→Version→Deprecate/Retire Business Activity shape (IMP-001 §6 CBAIP) | WP-01, WP-02, WP-03 | Directly reusable for BA-01 (Establish) |
| Pydantic schema pattern (`schemas/*.py`) | WP-01/02/03 | Direct reuse |
| SQLite-in-memory test fixture (`tests/conftest.py`) | WP-00/01/02/03 | Direct reuse, no new test infrastructure |
| `memberships.home_node_id` (nullable FK to `organization_nodes.id`) | WP-03 BA-01 | The exact consumer BA-01 unblocks — TD-032's own resolution criterion |

---

## 9. Architecture Validation

**Performed now, per this Work Package's own governance instruction, mirroring IRA-003 §9's discipline:**

- **`organization_node` already exists, but only as a minimal 6-column subset** (`id`, `node_code`, `node_name`, `node_type`, `active_flag`, `created_at`/`updated_at`). Confirmed by direct file read (`models/organization_node.py`). This is not a fresh Create — it is an **Extend**, per CLAUDE.md §19.5's Reuse→Configure→Extend→Compose→Create discipline. No new table is required for BA-01; the existing `organization_nodes` table gains additional canonical columns.
- **`organization_hierarchy`, `consolidation_determination`, `enterprise_view_registry`, `traversal_policy_registry`, `node_permission_assignment` do not exist** — confirmed by direct grep across `Backend/Services/AuthService`, zero matches for any of the five. This is not a constitutional gap — ERG-001 §5, §7, §9, and Master Technical Architecture's DDL fully and unambiguously specify all five. **They are out of BA-01's own scope** (§4, §7) and are not created under this IRA.
- **Disposition:** BA-01 (Establish Organization Node) is a normal Implementation Gap (category C, per §10), resolved by extending the existing minimal `organization_node`/`OrganizationNode`/`OrganizationNodeRepository` trio with a create path and the canonical columns needed to satisfy ERG-001-02/03 (§5), not by building a new object from scratch.
- **BA-01's own gap analysis must resolve exactly which of Master Technical Architecture's ~20+ `organization_node` columns are in scope.** Mirroring WP-01's ADR-004 precedent (`organizations` vs. `organization_master` — a deliberately minimal subset, not the full canonical shape, with the remainder explicitly deferred): this IRA does **not** decide the exact column list here. That is BA-01's own first implementation decision, to be disclosed in BA-01's own Business Activity Contract (IMP-001 §6.7), not assumed by this readiness assessment.
- **IMP-001 §13.17–13.25 (Runtime Component Engineering) — confirmed not applicable**, for the identical reason IRA-003 §9 recorded for WP-03: C-005 is Business-Activity-shaped (§6 CBAIP), not a new RTA-001 Runtime Component. No new Runtime Component is required.
- **NodePermissionAssignment's URA-001-76 authorization-precedence dependency (ERG-001-10) is confirmed not a BA-01 concern.** BA-01 only establishes the EnterpriseNode identity object; permission-scope resolution is a later Business Activity's own gap analysis (§4).

---

## 10. Gap Analysis (per Business Activity, category A–E)

| BA | Category | Reasoning |
|---|---|---|
| BA-01 — Establish Organization Node | **C** (Architecture requires completion — implementation-level) | Extend existing minimal `organization_node`/`OrganizationNodeRepository` with canonical columns (subset, per §9) and a create path; direct unblock of WP-03's own TD-032 |
| BA-02 — Understand Structural Position | **B** (Existing implementation can be reused) | `OrganizationNodeRepository`'s inherited `get_by_id()`/query methods are a direct starting point once BA-01 exists |
| BA-03 — Frame Structural Change Intent | **D** (Governance clarification required) | No persisted business object is evident from either PE-001-C005 or ERG-001; whether this is a database concept at all is undetermined — not resolved here |
| BA-04 — Shape/Refine Proposed Structural Outcome | **D** | Depends on §4's disclosed ambiguity (which ERG-001 object a "proposal" attaches to) — not resolved here |
| BA-05 — Assess Structural Consequence | **D** | Depends on BA-04's own resolution first |
| BA-06 — Review Structural Outcome | **B** (likely, pending BA-04) | Mirrors WP-01/02/03's own review/audit patterns once a proposal object exists |
| BA-07 — Validate Transition Readiness | **B** (likely, pending BA-04/BA-06) | Mirrors WP-01/02/03's own validation patterns |
| BA-08 — Complete Structural Transition | **C** | Requires `organization_hierarchy`/`consolidation_determination` — genuinely new tables, category C exactly as BA-01 is for `organization_node` |
| BA-09 — Continue from Resulting Structure | **B** (likely, pending BA-08) | Mirrors WP-03 BA-09/BA-11's own "no new production code, existing response shapes suffice" disposition — not assumed, to be confirmed at that BA's own gap analysis |
| *(cross-cutting)* `node_permission_assignment` / URA-001-76 integration | **D** (Governance clarification required) | Requires C-002 (Access Management, no WP yet) coordination — explicitly out of WP-04's own BA-01 scope, recorded as a Governance Backlog Item (§17) |

**No Business Activity meets category E (genuine STOP condition).**

---

## 11. Required Migrations

- **BA-01:** Extend `organization_nodes` — add the canonical columns Master Technical Architecture's DDL specifies that BA-01's own gap analysis determines are in scope (§9) — e.g., `legal_entity_name`, structural-identity fields per ERG-001-02's "Structural Identity" extension context. Single new migration, chained onto the existing head (`d4f8e2a6c1b9`), following the exact chaining discipline WP-01/02/03 all used.
- **BA-02 onward:** None currently anticipated beyond BA-01's own migration — to be confirmed at each BA's own gap analysis, not assumed here. BA-08 will require new tables (`organization_hierarchy` at minimum) when its own turn comes.

---

## 12. Required APIs

- **BA-01:** `POST /organization-nodes` (Establish) — not yet drafted; this IRA identifies it as the anticipated endpoint, at the same level of specificity IRA-002/003 used for their own BA-01. This IRA does not itself authorize drafting — that remains a separate approval step at BA-01 implementation time.
- **BA-02 onward:** Not enumerated here, mirroring IRA-002/003's own precedent of not speculating on later BAs' endpoint shapes in advance.

---

## 13. Required Repositories

- **BA-01:** Extend `OrganizationNodeRepository` with a `create()`-path method (currently read-only via inherited `get_by_id()` only). Reuse `BaseRepository[OrganizationNode]` — already the base class.
- **BA-02 onward:** No new repository class anticipated for BA-02; a new repository will be required once BA-08 introduces `organization_hierarchy` and later `consolidation_determination`.

---

## 14. Required Services

- **BA-01:** New `OrganizationNodeService` (does not exist today) — `establish()` following the identical existence-check → business-rule-check → mutate → audit → publish-event shape WP-01/02/03 all used.
- **BA-02 onward:** Extend the same `OrganizationNodeService`, mirroring WP-01/02/03's single-service-per-object-type discipline, until BA-08 introduces objects requiring their own service.

---

## 15. Required Schemas

- **BA-01:** `schemas/organization_node.py` — `EstablishOrganizationNodeRequest`, `OrganizationNodeResponse`. Reuse the exact Pydantic pattern WP-01/02/03 all used; no new validation framework.

---

## 16. Governance Observation — Cross-Reference to WP-03's Own TD-032

Per TD-032's own recorded text (raised in WP-03 BA-01, `TECH-DEBT.md`): **"Resolution Criteria: C-005 is chartered with its own IRA and implements Establish Organization Node; `home_node_id`'s nullability is then explicitly revisited (tightened or reaffirmed) as part of that or a subsequent WP-03 Business Activity."** This IRA is the chartering step TD-032 anticipated. TD-032 itself is **not closed by this IRA** — it remains open until BA-01 actually implements Establish Organization Node and a subsequent decision revisits `memberships.home_node_id`'s nullability. This IRA records the charter; it does not itself resolve TD-032.

---

## 17. Governance Backlog Item — Node Permission Assignment / Access Management Coordination (Explicitly Out of WP-04's BA-01 Scope)

ERG-001-10 states that NodePermissionAssignment "resolves into URA-001's existing precedence chain" and requires coordination with C-002 (Access Management) and C-003 (Role & Permission Management, WP-02, closed). **C-002 currently has no Work Package, no IRA, and no implementation anywhere in this repository** (confirmed via CAP-001 §2 and WPR-001 §2 — no row exists for C-002). This means a future WP-04 Business Activity implementing `node_permission_assignment` will face the same class of external-capability blocker WP-03's own BA-04 faced with C-005 itself. This is recorded here as a **Governance Backlog Item**, explicitly outside BA-01's scope, not gap-analyzed for implementation here, and not assigned a committed BA number in §4 beyond the disclosed candidate placeholder.

---

## 18. Test Strategy

Same discipline as IRA-001/002/003: IMP-TEST-001 (Business Activity Contract tests) as the primary layer, IMP-TEST-002 (Authorization Boundary tests, constrained by the same `require_platform_admin` interim-gate disposition WP-01/02/03 all established). New `test_organization_node_service.py` (unit) and `test_organization_node_api.py` (API/integration), using the existing `tests/conftest.py` SQLite-in-memory fixture — no new test infrastructure. BA-01's own test suite must additionally cover whatever canonical-column subset §9/§11 resolves, and should include a regression test confirming `memberships.home_node_id` can now be populated end-to-end (closing the observable half of TD-032, though not tightening its nullability — see §16).

---

## 19. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| BA-01's canonical-column-subset decision (§9, §11) is made carelessly, without disclosure | Medium | This IRA explicitly flags it as BA-01's first required decision, mirroring IRA-001/003's own precedent for comparable items |
| PE-001-C005's experience-level Business Rules/Contracts (§5, §6) are mistaken for BA-01's own governing rules, causing over-scoped implementation (the full propose/review/validate workflow) when only a minimal Establish is authorized | Medium | Explicitly disclosed in §5/§6 as **not** governing BA-01 as scoped; BA-03 through BA-08 are where that discipline actually applies |
| The ERG-001-object-to-BA mapping ambiguity (§4, BA-03/BA-04) is silently resolved by assumption at a later BA's own gap analysis rather than being explicitly re-examined | Low | Recorded explicitly here; future BA gap analyses should cite this section rather than re-discover the ambiguity |
| `node_permission_assignment`'s C-002 dependency (§17) is later mistaken for WP-04's own BA-01 responsibility | Low | Recorded explicitly as a Governance Backlog Item, out of BA-01's scope |
| Same `PLATFORM_ADMIN`-only interim authorization gate WP-01/02/03 all carried forward recurs a fourth time | Low (disclosed, consistent pattern) | Inherited, not new; to be logged as its own TD entry at BA-01's own Independent Review, exactly as WP-02/03 both did |
| TD-032 is mistakenly marked Closed upon this IRA's acceptance, before BA-01 is actually implemented | Low | §16 explicitly states this IRA charters but does not close TD-032 |

---

## 20. Technical Debt Carried Forward

- **TD-032** (WP-03) — "Target Resolution: Enterprise Structure Management (C-005)'s own future 'Establish Organization Node' Business Activity." **This IRA is that charter; TD-032 remains Open until BA-01 is actually implemented and `home_node_id`'s nullability is explicitly revisited** (§16). Not closed by this IRA.
- **ADR-002** (Proposed, not Accepted) — the same unresolved authorization-catalog question WP-01/02/03 all carried; WP-04's own `require_platform_admin` reuse (§8) will inherit it identically, not newly.
- **TD-021–025, TD-042** (WP-01/02/03) — the recurring `PLATFORM_ADMIN`-only interim gate; WP-04 inherits this pattern, to be logged as its own TD entry at BA-01's own Independent Review rather than treated as newly discovered.

---

## Completion Criteria

This IRA is complete when:
- BA-01 has a full Business Activity Contract per IMP-001 §6.7 (Business Intent, Input/Output Contract, Business Rules, Validation Rules, Authorization Rules, Domain Events, Audit Requirements, Tests) — **drafted at BA-01 implementation time, not here.**
- ERG-001-02 and ERG-001-03 (BA-01's actual governing rules, per §5) are satisfied and tested.
- The canonical-column-subset disposition (§9, §11) is explicitly disclosed, not silently assumed.
- No new database table is created beyond `organization_nodes`' own extension (§9, §11) — `organization_hierarchy` and the other four ERG-001 objects remain out of scope.
- The Node Permission Assignment / C-002 coordination gap (§17) remains excluded from WP-04's BA-01 implementation and is not silently absorbed.
- TD-032 is referenced, not silently closed (§16, §20).
- ADR-002's live status and BA-01's own disposition relative to it are disclosed, mirroring IRA-001/002/003's own precedent exactly.

**Governing document status:** This IRA does not create any ADR or AMD, does not modify architecture, does not implement BA-01, and does not resolve ADR-002, TD-032, or the Node Permission Assignment/C-002 coordination question. It records BA-01's scope, the one architectural decision BA-01 itself must make and disclose (§9), and the point at which each later Business Activity will require its own fresh gap analysis — exactly the discipline IRA-001, IRA-002, and IRA-003 all already established and CLAUDE.md §19.7 requires.

---

*End of IRA-004.*
