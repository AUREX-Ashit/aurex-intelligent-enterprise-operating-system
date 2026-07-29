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
| BA-03 | Frame Structural Change Intent | Create (governed decision record) | Structural Change Intent (`SCI-000001`, registered §21) | ERB-C005-03 / EX-C005-04 | ⏳ Not started — Business Object registered (§21); persistence mechanism, endpoint shape, and service/repository design remain undetermined and are that BA's own future implementation-readiness gap analysis, not assumed here |
| BA-04 | Shape / Refine Proposed Structural Outcome | Create / Update (proposal) | Proposed Outcome Context (`POC-000001`, registered §22) — **v1 scoped to EnterpriseNode-targeted proposals only, per ADR-007**; EnterpriseRelationship/ConsolidationDetermination-targeted proposals explicitly deferred, not eliminated (ADR-007 point 3) | ERB-C005-04 / EX-C005-05, -06 | ⏳ Not started — target-type ambiguity resolved (ADR-007); Business Object registered (`POC-000001`, §22); own implementation-readiness gap analysis still required |
| BA-05 | Assess Structural Consequence | Query (computed) | Impact Context (`IMC-000001`, registered §23) | ERB-C005-05 / EX-C005-07 | ⏳ Not started — Business Object registered (`IMC-000001`, §23); own implementation-readiness gap analysis still required |
| BA-06 | Review Structural Outcome / Resolve Concerns | Update (review) | Review Context (`RVC-000001`, registered §25) | ERB-C005-06 / EX-C005-08, -09 | ⏳ Not started — Business Object registered (`RVC-000001`, §25); own implementation-readiness gap analysis still required |
| BA-07 | Validate Transition Readiness | Update (validation) | Validation Context (`VLC-000001`, registered §26) | ERB-C005-07 / EX-C005-10 | ⏳ Not started — Business Object registered (`VLC-000001`, §26); own implementation-readiness gap analysis still required |
| BA-08 | Complete Structural Transition | Update (lifecycle/state transition) | Resulting Structural Context (`RSC-000001`, registered §27) — **the actual ERG-001 domain object(s) a completion mutates (EnterpriseNode / EnterpriseRelationship (`organization_hierarchy`) / ConsolidationDetermination) remain a separate, explicitly undecided implementation question**, disclosed in §27's own "Explicitly Not Decided" subsection, not resolved by this row | ERB-C005-08 / EX-C005-11 | ⏳ Not started — Business Object registered (`RSC-000001`, §27); own implementation-readiness gap analysis, including the ERG-001-mutation-scope question, still required |
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

**Addendum (post-BA-02):** this section's scope is ERG-001's own structural/domain objects only. A sixth object, **Structural Change Intent** — a PE-001-C005 experience-layer construct, not an ERG-001 domain object — has since been identified and formally registered per SD-002 §2/CMD-001 §26.3; see §21. It governs BA-03, not BA-01/BA-02.

**Addendum (post-ADR-007):** a seventh object, **Proposed Outcome Context** — likewise a PE-001-C005 experience-layer construct, not an ERG-001 domain object — has since been identified and formally registered per SD-002 §2/CMD-001 §26.3; see §22. It governs BA-04, not BA-01/BA-02/BA-03.

**Addendum (post-BA-04):** an eighth object, **Impact Context** — likewise a PE-001-C005 experience-layer construct, not an ERG-001 domain object — has since been identified and formally registered per SD-002 §2/CMD-001 §26.3; see §23. It governs BA-05, not BA-01 through BA-04.

**Addendum (post-BA-05):** Structural Change Intent, Proposed Outcome Context, and Impact Context are recognized, per `ADR-010`, as three stages of one canonical Structural Context Lifecycle pattern (§24) — not three independent discoveries. A ninth object, **Review Context** — the pattern's fourth stage — has since been registered per that pattern and CMD-001 §26.3, citing `ADR-010` for eligibility rather than re-deriving it; see §25. It governs BA-06, not BA-01 through BA-05. Validation Context and Resulting Structural Context (the pattern's fifth and sixth stages) remain unregistered.

**Addendum (post-BA-06):** a tenth object, **Validation Context** — the Structural Context Lifecycle's fifth stage — has since been registered per `ADR-010` and CMD-001 §26.3, independently re-confirmed (not merely assumed) during BA-07's own implementation-readiness assessment; see §26. It governs BA-07, not BA-01 through BA-06. Resulting Structural Context (the pattern's sixth and final stage) remains unregistered.

**Addendum (post-BA-07):** an eleventh object, **Resulting Structural Context** — the Structural Context Lifecycle's sixth and final stage — has since been registered per `ADR-010` and CMD-001 §26.3, independently re-confirmed during BA-08's own implementation-readiness assessment on the most literal cross-Business-Activity evidence of any of the six stages; see §27. It governs BA-08, not BA-01 through BA-07. **The Structural Context Lifecycle pattern is now fully registered end-to-end** (SCI-000001 → POC-000001 → IMC-000001 → RVC-000001 → VLC-000001 → RSC-000001); no further pattern member remains outstanding. Whether BA-08 must also mutate real ERG-001 structural data (EnterpriseNode / `organization_hierarchy` / `consolidation_determination`) to actually complete a transition is a separate, explicitly undecided implementation question — see §27's own "Explicitly Not Decided" subsection — not itself a Structural Context Lifecycle pattern member.

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
| BA-03 — Frame Structural Change Intent | **C** (Architecture requires completion — implementation-level; downgraded from D) | **Constitutional question resolved (§21, ADR-006):** Structural Change Intent is a registered canonical Business Object (`SCI-000001`) per SD-002 §2/CMD-001 §26.3 — not an undetermined concept. What remains is ordinary implementation-level gap analysis (persistence mechanism, endpoint shape, service/repository design) — the same class of work BA-01 itself required, not a governance blocker. This reclassification does not authorize implementation; BA-03's own fresh gap analysis is still required per CLAUDE.md §19.7 before any code is written. |
| BA-04 — Shape/Refine Proposed Structural Outcome | **C** (Architecture requires completion — implementation-level; downgraded from D) | **Both constitutional questions resolved.** Target-type ambiguity resolved (ADR-007): BA-04 v1 is scoped to EnterpriseNode-targeted proposals only — a phased implementation decision, not an architectural one; ERG-001 remains unamended. EnterpriseRelationship/ConsolidationDetermination-targeted proposals remain deferred to their own future Business Activities. **Business Object registration resolved:** "Proposed Outcome Context" satisfied SD-002 §2's Universal Business Object Blueprint and the Cross-Experience Reference Test (BA-05/BA-06/BA-07 each name it as Required/Consumed Context under three separate ERBs) and is now registered as `POC-000001` (§22, `ADR-008`). Neither reclassification authorizes implementation; BA-04's own fresh implementation-readiness gap analysis (persistence mechanism, endpoint shape, service/repository design) is still required per CLAUDE.md §19.7. |
| BA-05 — Assess Structural Consequence | **C** (Architecture requires completion — implementation-level; downgraded from D) | **BA-04 dependency satisfied** (implemented, `17cba1e`/`c60cf97`/`b3adb6e`). **Business Object registration resolved:** "Impact Context" satisfied SD-002 §2's Universal Business Object Blueprint and the Cross-Experience Reference Test (BA-06/BA-07 each name it as Required/Consumed Context under two separate ERBs) and is now registered as `IMC-000001` (§23, `ADR-009`). This reclassification does not authorize implementation; BA-05's own fresh implementation-readiness gap analysis is still required per CLAUDE.md §19.7. |
| BA-06 — Review Structural Outcome | **C** (Architecture requires completion — implementation-level; superseding the prior "B, likely" placeholder) | **BA-04/BA-05 dependencies satisfied** (both implemented). **Business Object registration resolved:** "Review Context" is registered as `RVC-000001` (§25, `ADR-011`), citing `ADR-010`'s own Structural Context Lifecycle pattern for eligibility rather than re-deriving it. This reclassification does not authorize implementation; BA-06's own fresh implementation-readiness gap analysis (including EX-C005-09's own disclosed ambiguity, §25) is still required per CLAUDE.md §19.7. |
| BA-07 — Validate Transition Readiness | **C** (Architecture requires completion — implementation-level; superseding the prior "B, likely" placeholder) | **BA-04/BA-05/BA-06 dependencies satisfied** (all implemented). **Business Object registration resolved:** "Validation Context" is registered as `VLC-000001` (§26, `ADR-012`), citing `ADR-010`'s own Structural Context Lifecycle pattern for eligibility, independently re-confirmed rather than merely assumed. This reclassification does not authorize implementation; BA-07's own fresh implementation-readiness gap analysis is still required per CLAUDE.md §19.7. |
| BA-08 — Complete Structural Transition | **C** (Architecture requires completion — implementation-level; superseding the prior pre-`ADR-010` disposition) | **BA-07 dependency satisfied** (implemented). **Business Object registration resolved:** "Resulting Structural Context" is registered as `RSC-000001` (§27, `ADR-013`), citing `ADR-010`'s own Structural Context Lifecycle pattern for eligibility, independently re-confirmed rather than merely assumed. **Separately disclosed, not resolved:** whether/how BA-08 actually mutates ERG-001 structural data (`organization_hierarchy`/`consolidation_determination` genuinely do not exist yet; every `StructuralProposal` carries only free text, no structured change-representation exists upstream) is BA-08's own future implementation-readiness gap analysis's question. This reclassification does not authorize implementation. |
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

## 21. Business Object Registration — Structural Change Intent

**Trigger:** This repository's own architectural-decision analysis (governance track, not a separate committed artifact) concluded that "Change Intent Context" (PE-001-C005, ERB-C005-03/EX-C005-04) satisfies SD-002 Section 2's Universal Business Object Blueprint — independent identity, business meaning, ownership, governance, business state, references, traceability, versioned history, and relationships — and is not a transient request-scoped value. This section performs the registration CMD-001 §26.3 requires ("No Business Object shall be implemented until it has been registered in the Canonical Business Object Register") **before** BA-03's own implementation-readiness gap analysis can proceed. This section does not authorize implementation.

**Governing decision:** `ADR-006_Structural_Change_Intent_Canonical_Business_Object_Registration.md` records the governance decision authorizing this registration, following the same pattern ADR-005 already established (a governance decision surfacing during a Work Package's own readiness-assessment review, formalized as its own ADR). CMD-001 is **LOCKED** (v1.3, GOLD STANDARD) — this registration exercises CMD-001 §26.3's own existing registration mechanism; it does not amend CMD-001's text, rules, or structure, and therefore does not itself require a Locked-document amendment ADR for CMD-001. The full registration entry is recorded here, in IRA-004, as WP-04/C-005's own implementation-readiness record — **disclosed as a Governance Backlog Item, not a silent resolution:** whether WP-04-registered objects should eventually be consolidated into CMD-001 §26 itself (a separate, future amendment to CMD-001) is not decided by this registration or by ADR-006.

### Registration Entry

| Attribute (CMD-001 §26.4) | Value |
|---|---|
| **Business Object Identifier** | `SCI-000001` |
| **Canonical Name** | Structural Change Intent |
| **Business Description** | The explicit enterprise decision context — business rationale, target structural outcome, and decision boundary — that must exist before a structural change may be proposed. Prevents structural work from beginning as an isolated edit (ERB-C005-03's own Purpose and Business Intent, verbatim). |
| **Business Domain** | Enterprise Structure Management (C-005) |
| **Aggregate Root** | Structural Change Intent itself — not a sub-object of EnterpriseNode/EnterpriseRelationship. It is the enterprise decision that precedes and governs an eventual change to one of those objects; PE-001-C005's own Context Model treats it as a top-level Context construct, not an attribute of the object it will eventually target. |
| **Business Owner** | Structural Steward (ERB-C005-03 Participating Personas); Structural Decision Participant contributes decision intent. |
| **Data Steward** | Pending Canonical Binding — no persona-to-URA-001-role binding exists yet for any C-005 persona (the same disclosed gap class as TD-021 through TD-025/TD-031/TD-034/TD-035/TD-036/TD-039/TD-042/TD-045; not newly discovered here, not separately registered per CLAUDE.md §19.8.3). |
| **Primary Data Category** | Transaction — a mutable, versioned, governed decision record, distinct from a pure immutable Event log entry (though it produces events per SD-002-009 once implemented). |
| **System of Record** | Pending — not yet determined. Deciding this is implementation-layer work (which service, which persistence mechanism) explicitly reserved for BA-03's own future implementation-readiness gap analysis, not this registration. |
| **Lifecycle Model** | SD-002-008's default lifecycle, distributed across C-005's own experience stages: **CREATED** (BA-03/EX-C005-04) → **MODIFIED** (revision within Frame Intent, before Shape Outcome) → **SUPERSEDED** or **ABANDONED** (EX-C005-04's own Invalidated Context text, verbatim: "Superseded or abandoned intent statements") → **WITHDRAWN** (a distinct, more specific closure condition from PE-001-C005 §43.3's own exception-semantics table: "Change intent withdrawn → Close Change Intent Context as withdrawn; preserve decision rationale and return to the last valid Structural Understanding Context") → **ARCHIVED** (SD-002-008's terminal state; not addressed in PE-001-C005's own text but not foreclosed by it). Review/Approval states apply to the downstream Proposed Outcome Context (ERB-C005-06), not to the intent itself. |
| **Versioning Policy** | Full version history retained; superseded revisions preserved in traceability, never physically deleted (EX-C005-04's own Invalidated Context text; SD-002-009/-010). |
| **Effective Dating** | Supported — inherited automatically from SD-002-011's universal temporal model (Effective From/To, Version, Status, Approval Reference); not a distinctive design choice for this object. |
| **Metadata Schema** | Pending — no implementation exists yet. |
| **Security Classification** | Internal — enterprise-internal structural decision data, consistent with every other C-005 construct. |
| **AI Context** | "Represents the enterprise's explicit rationale and target outcome for a proposed structural change, prior to a Proposed Outcome Context being shaped." EX-C005-04's own AI Assistance clause, quoted exactly: *"AI MAY help articulate intent, detect ambiguity and suggest questions. It SHALL not invent business rationale."* |
| **Status** | Draft — this registration entry is newly created; no separate CBOR-entry-approval governance step is defined anywhere in this repository, so no higher status is claimed. Subject to the Independent Review this task's own Phase 5 performs. |

### Relationship Mapping (CMD-001 §26.5)

| Structural Change Intent | Relationship | Target |
|---|---|---|
| Structural Change Intent | `CONSUMES` | Structural Understanding Context (EX-C005-03's own Produced Context, BA-02) |
| Structural Change Intent | `PRECEDES` | Proposed Outcome Context (EX-C005-05's own Produced Context, BA-04 candidate) — confirmed by EX-C005-05's own Required/Consumed Context: "Change Intent Context and current structural context" |
| Structural Change Intent | `DERIVED_FROM` | EnterpriseNode / EnterpriseRelationship — **Pending Canonical Binding**. §4's own disclosed ambiguity (which ERG-001 object a "proposal" ultimately attaches to) is unresolved and is **not** resolved by this registration; it remains BA-04's own open question. |

**Addendum (post-ADR-007):** BA-04's own *implementation-phasing* scope (which ERG-001 object BA-04 v1 supports as a proposal target — EnterpriseNode only) has since been decided by `ADR-007`. This is distinct from, and does not resolve, this table's own `DERIVED_FROM` relationship: SCI-000001's own definition remains generic and Pending Canonical Binding, exactly as recorded above — ADR-007 governs BA-04's implementation scope, not Structural Change Intent's own registered relationships. This section is otherwise unamended by ADR-007.

### Business Activity Mapping (CMD-001 §26.6)

- **Consumes:** BA-02 — Understand Structural Position
- **Produces:** BA-03 — Frame Structural Change Intent (itself)
- **Supports:** BA-04 — Shape/Refine Proposed Structural Outcome (candidate, not yet chartered)

### Governing References

- **Governing Business Activities:** BA-03 (create), BA-04 (consumes, candidate)
- **Governing Enterprise Experiences:** EX-C005-04 (Frame Structural Change Intent, produces); EX-C005-05 (Shape Structural Proposal, consumes)
- **Governing Business Rules:** BR-C005-001 ("A governed structural change SHALL have explicit Change Intent Context"), BR-C005-002 (Structural Focus boundary, BA-02/BA-03)

### Explicitly Not Decided by This Registration

- **Physical Implementation Mapping (CMD-001 §26.7)** — Physical Tables, APIs, Events Published/Consumed, Reports, Search Indexes, Knowledge Graph Nodes, AI Embeddings: **all Pending.** No database table, migration, API, or code is authorized or implied by this registration. Determining these remains BA-03's own future implementation-readiness gap analysis, per CLAUDE.md §19.4's Architectural Impact Assessment discipline.
- **Business Object Quality Score (CMD-001 §26.8)** — not scored; scoring an object with no implementation yet would be premature.
- **Whether BA-03 is now READY for implementation** — this registration resolves the *constitutional* question (Category D, "is this a database concept at all") but does not itself perform BA-03's own implementation-readiness gap analysis (persistence mechanism, endpoint shape, service/repository design), which remains a separate, future step per CLAUDE.md §19.7.

---

## 22. Business Object Registration — Proposed Outcome Context

**Trigger:** An Architectural Decision Report (governance track, not a separate committed artifact) applied SD-002 §2's Universal Business Object Blueprint and the Cross-Experience Reference Test to "Proposed Outcome Context" (PE-001-C005, ERB-C005-04/EX-C005-05, BA-04's own produced object) and found it satisfies both — more decisively than SCI-000001's own case: it is named, in one paraphrase or another ("proposal," "coherent proposal," "reviewed proposal"), as Required/Consumed Context by **three** separately-invoked Enterprise Experiences governed by **three different ERBs** (EX-C005-07/ERB-C005-05, EX-C005-08/ERB-C005-06, EX-C005-10/ERB-C005-07), not merely one. This section performs the registration CMD-001 §26.3 requires ("No Business Object shall be implemented until it has been registered in the Canonical Business Object Register") **before** BA-04's own implementation-readiness gap analysis can proceed. This section does not authorize implementation.

**Governing decision:** `ADR-008_Proposed_Outcome_Context_Canonical_Business_Object_Registration.md` records the governance decision authorizing this registration, following the identical pattern ADR-006 already established for SCI-000001. CMD-001 remains **LOCKED** (v1.3, GOLD STANDARD) — this registration exercises CMD-001 §26.3's own existing registration mechanism; it does not amend CMD-001's text, rules, or structure. The full registration entry is recorded here, in IRA-004, as WP-04/C-005's own implementation-readiness record — the same Governance Backlog Item already disclosed at §21 (whether WP-04-registered objects should eventually be consolidated into CMD-001 §26 itself) applies identically here and is not re-disclosed.

### Registration Entry

| Attribute (CMD-001 §26.4) | Value |
|---|---|
| **Business Object Identifier** | `POC-000001` |
| **Canonical Name** | Proposed Outcome Context |
| **Business Description** | The intended structural result, developed while the current structural context is retained for comparison — EX-C005-05's own Purpose, verbatim: "Create a proposed structural outcome while retaining current context." Business Value, verbatim: "Makes intended enterprise arrangement explicit while protecting authority of current structure." |
| **Business Domain** | Enterprise Structure Management (C-005) |
| **Aggregate Root** | Proposed Outcome Context itself — not a sub-object of Structural Change Intent (SCI-000001) or of the ERG-001 object it targets. It is related to both (see Relationship Mapping) but is independently identified, revised, and versioned across BA-04 through BA-07's own experience stages — the same top-level-Context-construct disposition ADR-006/§21 already established for SCI-000001. |
| **Business Owner** | Structural Steward (Participating Persona, EX-C005-05 through EX-C005-10, without exception); Structural Reviewer and Structural Decision Participant contribute at the review/validation stages (EX-C005-08/-09/-10). |
| **Data Steward** | Pending Canonical Binding — same disclosed gap class already recorded for SCI-000001 (§21) and TD-021 through TD-025/TD-031/TD-034/TD-035/TD-036/TD-039/TD-042/TD-045; not separately re-registered, per CLAUDE.md §19.8.3. |
| **Primary Data Category** | Transaction — a mutable, versioned, governed decision record, the same classification as SCI-000001. |
| **System of Record** | Pending — not yet determined; reserved for BA-04's own future implementation-readiness gap analysis, not this registration. |
| **Lifecycle Model** | SD-002-008's default lifecycle, distributed across C-005's own experience stages: **CREATED** (BA-04/EX-C005-05, Produced Context: "Proposed Outcome Context and initial Comparison Context") → **REVISED** (BA-04/EX-C005-06, Purpose: "Produce a coherent proposal revision suitable for assessment") → **SUPERSEDED** on revision (EX-C005-05's own Invalidated Context, verbatim: "Superseded proposal revisions are closed but retained in traceability") → a distinct, revocable **readiness marker**, VALIDATED (EX-C005-10's own Produced Context: "Validation Context and readiness result"), which BR-C005-005 states is itself invalidated by a subsequent material revision ("Material proposal revision SHALL invalidate prior validation readiness") — a readiness state layered on top of, not replacing, the CREATED/REVISED/SUPERSEDED sequence → **ARCHIVED** (SD-002-008's terminal state; not addressed in PE-001-C005's own text but not foreclosed by it). Distinct from, and layered against, Impact Context (EX-C005-07), Review Context (EX-C005-08/-09), and Validation Context (EX-C005-10) — each of those is its own produced context, not a renamed state of Proposed Outcome Context itself; only the proposal's own CREATED/REVISED/SUPERSEDED/readiness states are recorded here, not invented for the related context objects. |
| **Versioning Policy** | Full version history retained; superseded revisions preserved in traceability, never physically deleted (EX-C005-05's own Invalidated Context text; BR-C005-004: "Every proposal revision SHALL remain traceable to the change intent that produced it"; SD-002-009/-010). |
| **Effective Dating** | Supported — inherited automatically from SD-002-011's universal temporal model; not a distinctive design choice for this object. |
| **Metadata Schema** | Pending — no implementation exists yet. |
| **Security Classification** | Internal — enterprise-internal structural decision data, consistent with SCI-000001 and every other C-005 construct. |
| **AI Context** | "Represents the intended structural outcome, and its successive revisions, developed against a specific Structural Change Intent while the current structural context is preserved for comparison." EX-C005-05's own AI Assistance clause, quoted exactly: *"AI MAY compare intended outcome with current context. It SHALL not convert a suggestion into a proposal without explicit persona action."* EX-C005-06's own AI Assistance clause, quoted exactly: *"AI MAY summarize proposal-revision differences and explain unresolved coherence concerns."* (EX-C005-08's and EX-C005-09's own AI Assistance clauses govern Review Context, a related but distinct produced context — not quoted here as this object's own AI Context, to avoid conflating the two objects.) |
| **Status** | Draft — newly created registration entry; no separate CBOR-entry-approval governance step is defined anywhere in this repository, so no higher status is claimed. Subject to this task's own Independent Review (Phase 6). |

### Relationship Mapping (CMD-001 §26.5)

| Proposed Outcome Context | Relationship | Target |
|---|---|---|
| Proposed Outcome Context | `DERIVED_FROM` | Structural Change Intent (SCI-000001) — the inverse of §21's own `PRECEDES` entry; confirmed by EX-C005-05's own Required/Consumed Context: "Change Intent Context and current structural context." |
| Proposed Outcome Context | `DERIVED_FROM` | EnterpriseNode — **Bound for BA-04 v1** (not Pending), per `ADR-007`'s own EnterpriseNode-only phase-1 scope decision. EnterpriseRelationship / ConsolidationDetermination binding remains deferred to a future BA-04 extension (ADR-007 point 3) — this registration does not itself widen or narrow ADR-007's own scope decision. |
| Proposed Outcome Context | `PRECEDES` | Impact Context (EX-C005-07's own Produced Context, BA-05 candidate) — confirmed by EX-C005-07's own Required/Consumed Context: "Coherent proposal and current authoritative structural context." |
| Proposed Outcome Context | `PRECEDES` | Review Context (EX-C005-08's own Produced Context, BA-06 candidate) — confirmed by EX-C005-08's own Required/Consumed Context: "Proposal, Impact Context and review purpose." |
| Proposed Outcome Context | `PRECEDES` | Validation Context (EX-C005-10's own Produced Context, BA-07 candidate) — confirmed by EX-C005-10's own Required/Consumed Context: "Reviewed proposal, resolved concerns and Impact Context." |

### Business Activity Mapping (CMD-001 §26.6)

- **Consumes:** BA-03 — Frame Structural Change Intent (SCI-000001)
- **Produces:** BA-04 — Shape / Refine Proposed Structural Outcome (itself)
- **Supports:** BA-05 — Assess Structural Consequence (candidate); BA-06 — Review Structural Outcome / Resolve Concerns (candidate); BA-07 — Validate Transition Readiness (candidate) — none yet chartered.

### Governing References

- **Governing Business Activities:** BA-04 (create/update), BA-05/BA-06/BA-07 (consume, candidates)
- **Governing Enterprise Experiences:** EX-C005-05 (Shape Structural Proposal, produces); EX-C005-06 (Refine Structural Proposal, consumes/produces revision); EX-C005-07 (Assess Structural Consequence, consumes); EX-C005-08 (Review Proposed Structural Outcome, consumes); EX-C005-09 (Resolve Structural Review Concerns, consumes/produces revision); EX-C005-10 (Validate Structural Transition Readiness, consumes)
- **Governing Business Rules:** BR-C005-003 (current structural context SHALL remain distinguishable from Proposed Outcome Context), BR-C005-004 (traceability to originating Change Intent), BR-C005-005 (material revision invalidates prior validation readiness), BR-C005-006 (review SHALL identify the exact revision under review), BR-C005-007 (unresolved concerns block completion absent a recorded exception)

### Explicitly Not Decided by This Registration

- **Physical Implementation Mapping (CMD-001 §26.7)** — Physical Tables, APIs, Events Published/Consumed, Reports, Search Indexes, Knowledge Graph Nodes, AI Embeddings: **all Pending.** No database table, migration, API, or code is authorized or implied by this registration. Determining these remains BA-04's own future implementation-readiness gap analysis, per CLAUDE.md §19.4's Architectural Impact Assessment discipline.
- **Business Object Quality Score (CMD-001 §26.8)** — not scored; scoring an object with no implementation yet would be premature.
- **Whether BA-04 is now READY for implementation** — this registration resolves the *constitutional* question (does this concept qualify as a Business Object requiring registration) but does not itself perform BA-04's own implementation-readiness gap analysis (persistence mechanism, endpoint shape, service/repository design), which remains a separate, future step per CLAUDE.md §19.7. ADR-007's own EnterpriseNode-only v1 scope decision is unaffected and unchanged by this registration.

---

## 23. Business Object Registration — Impact Context

**Trigger:** BA-05's own implementation-readiness assessment applied the identical SD-002 §2 Universal Business Object Blueprint test and Cross-Experience Reference Test already used for SCI-000001 (§21) and POC-000001 (§22) to "Impact Context" (PE-001-C005, ERB-C005-05/EX-C005-07, BA-05's own produced object) and found it qualifies: it is named as Required/Consumed Context by **two** separately-invoked Enterprise Experiences governed by two different ERBs — EX-C005-08 (ERB-C005-06, BA-06: "Proposal, Impact Context and review purpose") and EX-C005-10 (ERB-C005-07, BA-07: "Reviewed proposal, resolved concerns and Impact Context") — the same class of decisive evidence already accepted twice in this Work Package. Chapter 42's own text independently corroborates this: "Impact Context is mandatory for review readiness unless a canonical journey records a traceable exception," treating it as a standing, referenceable artifact, not a transient computation. This section performs the registration CMD-001 §26.3 requires **before** BA-05's own implementation-readiness gap analysis can proceed. This section does not authorize implementation.

**Governing decision:** `ADR-009_Impact_Context_Canonical_Business_Object_Registration.md` records the governance decision authorizing this registration, following the identical pattern ADR-006 and ADR-008 already established. CMD-001 remains **LOCKED** — this registration exercises CMD-001 §26.3's own existing registration mechanism; it does not amend CMD-001's text, rules, or structure.

### Registration Entry

| Attribute (CMD-001 §26.4) | Value |
|---|---|
| **Business Object Identifier** | `IMC-000001` |
| **Canonical Name** | Impact Context |
| **Business Description** | The computed impact and uncertainty context — affected structural areas, known/uncertain consequences, and downstream capability implications — created for a specific coherent proposal revision, prior to review. EX-C005-07's own Purpose, verbatim: "Create impact and uncertainty context for review." Business Value, verbatim: "Improves decision quality by exposing affected context and uncertainty before review." |
| **Business Domain** | Enterprise Structure Management (C-005) |
| **Aggregate Root** | Impact Context itself — not a sub-object of Proposed Outcome Context (POC-000001). It is computed *about* a specific proposal revision but is independently identified, retrieved, and invalidated across BA-06/BA-07's own later experience stages — the same top-level-Context-construct disposition already established for SCI-000001/POC-000001. |
| **Business Owner** | Structural Steward, Structural Reviewer (Participating Personas, EX-C005-07). |
| **Data Steward** | Pending Canonical Binding — same disclosed gap class already recorded for SCI-000001 (§21) and POC-000001 (§22). |
| **Primary Data Category** | Transaction — a computed, versioned, governed decision-support record tied to a specific proposal revision, the same classification already applied to SCI-000001/POC-000001, notwithstanding its "Query (computed)" Business Activity type (IRA-004 §4) — computed does not mean transient, per the Cross-Experience Reference Test finding above. |
| **System of Record** | Pending — reserved for BA-05's own future implementation-readiness gap analysis. |
| **Lifecycle Model** | SD-002-008's default lifecycle: **CREATED** (BA-05/EX-C005-07, Produced Context: "Impact Context, known/uncertain consequence context and downstream implications") → **INVALIDATED** (EX-C005-07's own Invalidated Context, verbatim: "Impact observations invalidated by material proposal revision") → **ARCHIVED** (SD-002-008's terminal state; not addressed in PE-001-C005's own text but not foreclosed by it). Unlike Proposed Outcome Context, no REVISED/SUPERSEDED pair is registered here — PE-001-C005's own text describes a material proposal revision *invalidating* the prior Impact Context outright (implying a fresh Impact Context is computed against the new revision), not a refinement of the same one; whether BA-05's own future implementation actually creates a new row per computation or reuses one is not decided by this registration. |
| **Versioning Policy** | Full history retained; invalidated Impact Context entries preserved in traceability, never physically deleted, the same SD-002-009/-010 disclosure already applied to SCI-000001/POC-000001. |
| **Effective Dating** | Supported — inherited automatically from SD-002-011's universal temporal model; not a distinctive design choice for this object. |
| **Metadata Schema** | Pending — no implementation exists yet. |
| **Security Classification** | Internal — consistent with SCI-000001/POC-000001 and every other C-005 construct. |
| **AI Context** | "Represents the computed impact, uncertainty and downstream capability implications of a specific proposal revision, prior to review." EX-C005-07's own AI Assistance clause, quoted exactly: *"AI MAY identify possible affected context and downstream implications. Confidence and evidence basis SHALL be visible."* |
| **Status** | Draft — newly created registration entry; no separate CBOR-entry-approval governance step is defined anywhere in this repository. Subject to this task's own Independent Review (Phase 6). |

### Relationship Mapping (CMD-001 §26.5)

| Impact Context | Relationship | Target |
|---|---|---|
| Impact Context | `DERIVED_FROM` | Proposed Outcome Context (POC-000001) — confirmed by EX-C005-07's own Required/Consumed Context: "Coherent proposal and current authoritative structural context." |
| Impact Context | `PRECEDES` | Review Context (EX-C005-08's own Produced Context, BA-06 candidate) — confirmed by EX-C005-08's own Required/Consumed Context: "Proposal, Impact Context and review purpose." |
| Impact Context | `PRECEDES` | Validation Context (EX-C005-10's own Produced Context, BA-07 candidate) — confirmed by EX-C005-10's own Required/Consumed Context: "Reviewed proposal, resolved concerns and Impact Context." |

### Business Activity Mapping (CMD-001 §26.6)

- **Consumes:** BA-04 — Shape / Refine Proposed Structural Outcome (POC-000001)
- **Produces:** BA-05 — Assess Structural Consequence (itself)
- **Supports:** BA-06 — Review Structural Outcome / Resolve Concerns (candidate); BA-07 — Validate Transition Readiness (candidate) — neither yet chartered.

### Governing References

- **Governing Business Activities:** BA-05 (create/compute), BA-06/BA-07 (consume, candidates)
- **Governing Enterprise Experiences:** EX-C005-07 (Assess Structural Consequence, produces); EX-C005-08 (Review Proposed Structural Outcome, consumes); EX-C005-10 (Validate Structural Transition Readiness, consumes)
- **Governing Business Rules:** BR-C005-008 ("C-005 SHALL identify downstream capability implications but SHALL not execute outcomes owned by those capabilities")

### Explicitly Not Decided by This Registration

- **Physical Implementation Mapping (CMD-001 §26.7)** — Physical Tables, APIs, Events Published/Consumed, Reports, Search Indexes, Knowledge Graph Nodes, AI Embeddings: **all Pending.** No database table, migration, API, or code is authorized or implied by this registration. Determining these remains BA-05's own future implementation-readiness gap analysis.
- **Business Object Quality Score (CMD-001 §26.8)** — not scored.
- **Whether BA-05 is now READY for implementation** — this registration resolves the *constitutional* question only; BA-05's own fresh implementation-readiness gap analysis (persistence mechanism, one-row-per-computation vs. reuse, endpoint shape, service/repository design) remains a separate, future step per CLAUDE.md §19.7.
- **Whether "Review Context" (BA-06) and "Validation Context" (BA-07) themselves require CBOR registration** — each is that future Business Activity's own eligibility question, not decided or assumed here.

---

## 24. Canonical Pattern — The Structural Context Lifecycle

**Trigger:** BA-06's own implementation-readiness assessment identified Review Context as a fourth candidate Business Object. Before repeating SCI-000001/POC-000001/IMC-000001's own individual discovery-and-registration cycle a third time, a fresh review of PE-001-C005 Chapter 38 (not previously consulted by any Business Activity's own readiness assessment in this Work Package) found the pattern already explicitly declared: **§38.15 ("C-005 Context Model")**, **§38.17 ("Context Transitions")**, and Chapter 43's **GS-INV-003 through GS-INV-012** governance invariants.

**Governing decision:** `ADR-010_Structural_Context_Lifecycle_Canonical_Pattern.md` recognizes this pattern. **This section records that recognition. It registers no Business Object and authorizes no implementation.**

### The Structural Context Lifecycle (PE-001-C005 §38.15/§38.17)

Six substantive Context stages, in sequence, per §38.17's own transition semantics:

| Stage | Context (§38.15) | Rule (§38.15, verbatim) | Governing EX (produces) | CBOR Status |
|---|---|---|---|---|
| 1 | Change Intent Context | "Created before a governed proposal." | EX-C005-04 | `SCI-000001` — **registered, §21 (ADR-006)** |
| 2 | Proposed Outcome Context | "Never represented as current authoritative structure." | EX-C005-05 | `POC-000001` — **registered, §22 (ADR-008)** |
| 3 | Comparison / Impact Context | "Preserved during assessment and review." | EX-C005-07 | `IMC-000001` — **registered, §23 (ADR-009)** |
| 4 | Review Context | "Preserved through resolution and validation." | EX-C005-08 (BA-06) | **Not registered — candidate only, per this ADR's own Decision point 2** |
| 5 | Validation Context | "Invalidated by material proposal change." | EX-C005-10 (BA-07 candidate) | **Not registered — candidate only** |
| 6 | Resulting Structural Context | "Structural context produced by successful completion." | EX-C005-11 (BA-08 candidate) | **Not registered — candidate only** |

Excluded from the substantive six (per §38.15's own table, ADR-010's own Decision): **Enterprise Context, Structural Focus, Journey Intent, Navigation Context** — cross-cutting session/request-scoped context, not persisted Business Objects (Structural Focus additionally resolves to an ERG-001 EnterpriseNode, itself outside the CBOR/SD-002 §2 registration process by this Work Package's own established precedent, IRA-004 §7's addenda).

### Governing Invariants (PE-001-C005 Chapter 43, verbatim)

- **GS-INV-003** — "A governed structural proposal SHALL NOT exist without explicit Change Intent Context."
- **GS-INV-004** — "Current authoritative structural context and Proposed Outcome Context SHALL remain semantically and experientially distinct."
- **GS-INV-005** — "Every proposal revision SHALL preserve lineage to the Change Intent Context and the proposal revision it supersedes, where applicable."
- **GS-INV-006** — "Impact, Review and Validation Context SHALL identify the exact proposal revision to which they apply."
- **GS-INV-007** — "A material proposal revision SHALL invalidate dependent readiness and SHALL trigger reassessment of affected impact or review context."
- **GS-INV-008** — "Resulting Structural Context SHALL be created only after successful completion of the validated structural transition."
- **GS-INV-012** — "Completion SHALL identify the exact validated proposal revision from which Resulting Structural Context was produced."

### Ownership and Lifecycle Semantics (per-stage, §41's own Participating Personas)

Structural Steward participates throughout every stage. Structural Decision Participant joins from Frame Intent onward. Structural Reviewer joins from Assess/Review onward. Each stage's own Invalidated Context (§41.5–§41.12) establishes a real, event-generating lifecycle transition — not merely a data update — consistent with SD-002-008/-009 across all six stages, already implemented identically for stages 1–3 (SCI-000001/POC-000001/IMC-000001 each carry a CheckConstraint-declared status enum matching their own registered Lifecycle Model, per §21/§22/§23).

### Relationship to Enterprise Experiences

Each stage is produced by exactly one EX (table above) and consumed, per §38.17's own transition table, by the immediately following stage's EX — the same `PRECEDES`/`DERIVED_FROM`/`CONSUMES` relationship vocabulary already used in §21/§22/§23's own Relationship Mapping tables. Stages 4–6 (Review, Validation, Resulting Structural Context) will each receive their own full Relationship Mapping only at their own future registration.

### Explicitly Not Decided by This Section

- **Review Context, Validation Context, and Resulting Structural Context are not registered by this section.** No Business Object Identifier, Aggregate Root, Owner, or Lifecycle Model is assigned to any of them here. Each requires its own future registration entry (mirroring §21/§22/§23's own format), which may cite this section and `ADR-010` for the eligibility question but must still independently supply its own CMD-001 §26.4 attributes.
- **Whether BA-06 may now implement Review Context** — no. This section records a pattern, not a registration; CMD-001 §26.3's registration-precedes-implementation rule still applies per-object.
- **Whether Enterprise Context / Structural Focus / Journey Intent / Navigation Context require their own CBOR registration** — this section's own analysis found they do not (cross-cutting session/request-scoped context, per §38.15's own "Mandatory throughout" / "Preserved until explicitly changed" framing, distinct from the six substantive, domain-specific stages) — not re-examined further here.

---

## 25. Business Object Registration — Review Context

**Trigger:** Per `ADR-010`'s own Decision point 4, this registration cites the Structural Context Lifecycle pattern (§24) for the eligibility question rather than re-deriving SD-002 §2's Universal Business Object Blueprint from first principles. Review Context is the fourth of the pattern's six substantive stages (§24's own table), produced by ERB-C005-06/EX-C005-08. This section performs the registration CMD-001 §26.3 requires **before** BA-06's own implementation-readiness gap analysis can proceed. This section does not authorize implementation.

**Governing decision:** `ADR-011_Review_Context_Canonical_Business_Object_Registration.md` records the governance decision authorizing this registration. CMD-001 remains **LOCKED** — this registration exercises CMD-001 §26.3's own existing registration mechanism.

### Registration Entry

| Attribute (CMD-001 §26.4) | Value |
|---|---|
| **Business Object Identifier** | `RVC-000001` |
| **Canonical Name** | Review Context |
| **Business Description** | The review position, concerns, decisions, and unresolved issues recorded against one specific proposal revision. §38.15's own Meaning, verbatim: "Review purpose, concerns, decisions and unresolved issues." EX-C005-08's own Purpose, verbatim: "Create a contextual review position and concerns." Business Value, verbatim: "Makes review a continuation of the enterprise decision rather than a detached approval task." |
| **Business Domain** | Enterprise Structure Management (C-005) |
| **Aggregate Root** | Review Context itself — per `ADR-010` point 5, not merged with Proposed Outcome Context (POC-000001) or Impact Context (IMC-000001); its own independently-identified object, related to both (see Relationship Mapping). |
| **Business Owner** | Structural Reviewer (primary reviewing persona); Structural Decision Participant and Structural Steward also participate (EX-C005-08 Participating Personas). |
| **Data Steward** | Pending Canonical Binding — same disclosed gap class already recorded for SCI-000001/POC-000001/IMC-000001 (§21/§22/§23). |
| **Primary Data Category** | Transaction — a mutable, versioned, governed decision record, the same classification already applied to every other Structural Context Lifecycle member. |
| **System of Record** | Pending — reserved for BA-06's own future implementation-readiness gap analysis. |
| **Lifecycle Model** | SD-002-008's default lifecycle: **CREATED** (BA-06/EX-C005-08, Produced Context: "Review Context, review position and contextual concerns") → **CONCERNS_RESOLVED** (BA-06/EX-C005-09, one of its own two Produced Context alternatives, verbatim: "Resolved concern context...") → **INVALIDATED** (EX-C005-08's own Invalidated Context, verbatim: "Prior review position if the reviewed revision changes materially"; corroborated by GS-INV-007) → **ARCHIVED** (SD-002-008's terminal state; not addressed in PE-001-C005's own text but not foreclosed by it). **Explicitly not decided here:** EX-C005-09's own text offers a second, alternate Produced Context — "...or revised proposal context" — which may mean concern-resolution instead invokes BA-04's already-implemented Refine mechanism (a new `StructuralProposal` revision) rather than transitioning Review Context itself to a distinct state. This ambiguity is carried forward, not resolved, from BA-06's own original candidate-identification finding — it is BA-06's own future implementation-readiness gap analysis's question. |
| **Versioning Policy** | Full version history retained; per GS-INV-006, each Review Context instance identifies "the exact proposal revision to which it applies" — implying one Review Context per assessed proposal revision, the same per-revision scoping already implemented for Impact Context (IMC-000001's own `structural_proposal_id` FK to one specific revision, not a lineage). Not decided as a firm implementation commitment here — reserved for BA-06's own gap analysis. |
| **Effective Dating** | Supported — inherited automatically from SD-002-011's universal temporal model; not a distinctive design choice for this object. |
| **Metadata Schema** | Pending — no implementation exists yet. |
| **Security Classification** | Internal — consistent with every other Structural Context Lifecycle member. |
| **AI Context** | "Represents the review position, concerns, and decision continuity recorded against one specific proposal revision, prior to validation." EX-C005-08's own AI Assistance clause, quoted exactly: *"AI MAY summarize proposal, impact and review history. It SHALL not issue the review decision."* EX-C005-09's own AI Assistance clause, quoted exactly: *"AI MAY group concerns and explain revision impact. It SHALL preserve the original concern and not rewrite it as resolved."* |
| **Status** | Draft — newly created registration entry; no separate CBOR-entry-approval governance step is defined anywhere in this repository. Subject to this task's own Independent Review (Phase 4). |

### Relationship Mapping (CMD-001 §26.5)

| Review Context | Relationship | Target |
|---|---|---|
| Review Context | `DERIVED_FROM` | Proposed Outcome Context (POC-000001) and Impact Context (IMC-000001) — confirmed by EX-C005-08's own Required/Consumed Context: "Proposal, Impact Context and review purpose." |
| Review Context | `PRECEDES` | Validation Context (EX-C005-10's own Produced Context, BA-07 candidate) — confirmed by EX-C005-10's own Required/Consumed Context: "Reviewed proposal, resolved concerns and Impact Context." |

### Business Activity Mapping (CMD-001 §26.6)

- **Consumes:** BA-04 — Shape / Refine Proposed Structural Outcome (POC-000001); BA-05 — Assess Structural Consequence (IMC-000001)
- **Produces:** BA-06 — Review Structural Outcome / Resolve Concerns (itself)
- **Supports:** BA-07 — Validate Transition Readiness (candidate, not yet chartered)

### Governing References

- **Governing Business Activities:** BA-06 (create/update), BA-07 (consume, candidate)
- **Governing Enterprise Experiences:** EX-C005-08 (Review Proposed Structural Outcome, produces); EX-C005-09 (Resolve Structural Review Concerns, consumes/produces resolution)
- **Governing Business Rules:** BR-C005-006 ("Review SHALL identify the exact proposal revision under review"), BR-C005-007 ("Unresolved review concerns SHALL prevent completion unless the governing decision mechanism records an accepted exception")
- **Governing Invariants (PE-001-C005 Chapter 43):** GS-INV-006, GS-INV-007

### Explicitly Not Decided by This Registration

- **Physical Implementation Mapping (CMD-001 §26.7)** — Physical Tables, APIs, Events Published/Consumed, Reports, Search Indexes, Knowledge Graph Nodes, AI Embeddings: **all Pending.** No database table, migration, API, or code is authorized or implied by this registration. Determining these remains BA-06's own future implementation-readiness gap analysis.
- **Business Object Quality Score (CMD-001 §26.8)** — not scored.
- **Whether BA-06 is now READY for implementation** — this registration resolves the *constitutional* question only; BA-06's own fresh implementation-readiness gap analysis (persistence mechanism, exact lifecycle representation, endpoint shape, service/repository design, and EX-C005-09's own disclosed ambiguity) remains a separate, future step per CLAUDE.md §19.7.
- **Whether "Validation Context" (BA-07) and "Resulting Structural Context" (BA-08) themselves require their own registration** — each is that future Business Activity's own eligibility question; `ADR-010`'s pattern recognition already establishes they qualify in principle, but neither is registered by this section.

---

## 26. Business Object Registration — Validation Context

**Trigger:** BA-07's own implementation-readiness assessment independently re-confirmed — not merely assumed from precedent — that Validation Context, the Structural Context Lifecycle's fifth stage, satisfies SD-002 §2 and the Cross-Experience Reference Test, citing `ADR-010`'s own pattern recognition for the general eligibility question per that ADR's Decision point 4. This section performs the registration CMD-001 §26.3 requires **before** BA-07's own implementation-readiness gap analysis can proceed. This section does not authorize implementation.

**Governing decision:** `ADR-012_Validation_Context_Canonical_Business_Object_Registration.md` records the governance decision authorizing this registration. CMD-001 remains **LOCKED** — this registration exercises CMD-001 §26.3's own existing registration mechanism.

### Registration Entry

| Attribute (CMD-001 §26.4) | Value |
|---|---|
| **Business Object Identifier** | `VLC-000001` |
| **Canonical Name** | Validation Context |
| **Business Description** | The readiness of one specific, exactly-identified reviewed proposal revision to become the resulting enterprise state. §38.15's own Meaning, verbatim: "Readiness of the exact reviewed proposal revision." EX-C005-10's own Purpose, verbatim: "Establish validated readiness or explicit return context." Business Value, verbatim: "Ensures completion applies to the exact proposal reviewed and found ready." |
| **Business Domain** | Enterprise Structure Management (C-005) |
| **Aggregate Root** | Validation Context itself — per `ADR-010` point 5, not merged with Proposed Outcome Context (POC-000001), Impact Context (IMC-000001), or Review Context (RVC-000001); its own independently-identified object, related to all three (see Relationship Mapping). |
| **Business Owner** | Structural Steward; Structural Reviewer and Structural Decision Participant also participate (EX-C005-10 Participating Personas). |
| **Data Steward** | Pending Canonical Binding — same disclosed gap class already recorded for SCI-000001/POC-000001/IMC-000001/RVC-000001 (§21/§22/§23/§25). |
| **Primary Data Category** | Transaction — a governed decision record, the same classification already applied to every other Structural Context Lifecycle member. |
| **System of Record** | Pending — reserved for BA-07's own future implementation-readiness gap analysis. |
| **Lifecycle Model** | SD-002-008's default lifecycle: **CREATED** (BA-07/EX-C005-10, Produced Context: "Validation Context and readiness result") → **INVALIDATED** (EX-C005-10's own Invalidated Context, verbatim: "Readiness when proposal or material enterprise context changes"; corroborated by BR-C005-005 and GS-INV-007) → **ARCHIVED** (SD-002-008's terminal state; not addressed in PE-001-C005's own text but not foreclosed by it). **Explicitly not decided here:** EX-C005-10's own Exit Context (§40.8) offers two outcomes — "Validated Transition Context **or** explicit return-to-resolution context" — whether the readiness result (ready vs. return-to-resolution) is a field on this object or governs whether a row is created at all is BA-07's own future implementation-readiness gap analysis's question, not resolved here. |
| **Versioning Policy** | Full version history retained; per GS-INV-006, each Validation Context instance identifies "the exact proposal revision to which it applies" — the same per-revision scoping already implemented for Impact Context and Review Context. |
| **Effective Dating** | Supported — inherited automatically from SD-002-011's universal temporal model; not a distinctive design choice for this object. |
| **Metadata Schema** | Pending — no implementation exists yet. |
| **Security Classification** | Internal — consistent with every other Structural Context Lifecycle member. |
| **AI Context** | "Represents whether the exact reviewed proposal revision is ready to become the resulting enterprise state." EX-C005-10's own AI Assistance clause, quoted exactly: *"AI MAY identify missing context or apparent inconsistencies. Validation authority remains with the governed experience."* |
| **Status** | Draft — newly created registration entry; no separate CBOR-entry-approval governance step is defined anywhere in this repository. Subject to this task's own Independent Review (Phase 4). |

### Relationship Mapping (CMD-001 §26.5)

| Validation Context | Relationship | Target |
|---|---|---|
| Validation Context | `DERIVED_FROM` | Proposed Outcome Context (POC-000001) — confirmed by EX-C005-10's own Required/Consumed Context: "Reviewed proposal, resolved concerns and Impact Context." |
| Validation Context | `DERIVED_FROM` | Review Context (RVC-000001) — confirmed by the same Required/Consumed Context ("resolved concerns"). |
| Validation Context | `DERIVED_FROM` | Impact Context (IMC-000001) — confirmed by the same Required/Consumed Context ("Impact Context"). |
| Validation Context | `PRECEDES` | Resulting Structural Context (BA-08 candidate, not yet registered) — confirmed by §40.9's own Entry Context ("Validated Transition Context") and GS-INV-008 ("Resulting Structural Context SHALL be created only after successful completion of the validated structural transition"). |

### Business Activity Mapping (CMD-001 §26.6)

- **Consumes:** BA-04 — Shape/Refine Proposed Structural Outcome (POC-000001); BA-05 — Assess Structural Consequence (IMC-000001); BA-06 — Review/Resolve Structural Review Concerns (RVC-000001)
- **Produces:** BA-07 — Validate Transition Readiness (itself)
- **Supports:** BA-08 — Complete Structural Transition (candidate, not yet chartered)

### Governing References

- **Governing Business Activities:** BA-07 (create), BA-08 (consume, candidate)
- **Governing Enterprise Experiences:** EX-C005-10 (Validate Structural Transition Readiness, produces)
- **Governing Business Rules:** BR-C005-005 ("Material proposal revision SHALL invalidate prior validation readiness")
- **Governing Invariants (PE-001-C005 Chapter 43):** GS-INV-006, GS-INV-007, GS-INV-008, GS-INV-012

### Explicitly Not Decided by This Registration

- **Physical Implementation Mapping (CMD-001 §26.7)** — Physical Tables, APIs, Events Published/Consumed, Reports, Search Indexes, Knowledge Graph Nodes, AI Embeddings: **all Pending.** No database table, migration, API, or code is authorized or implied by this registration. Determining these remains BA-07's own future implementation-readiness gap analysis.
- **Business Object Quality Score (CMD-001 §26.8)** — not scored.
- **Whether BA-07 is now READY for implementation** — this registration resolves the *constitutional* question only; BA-07's own fresh implementation-readiness gap analysis (persistence mechanism, readiness-result representation, endpoint shape, service/repository design) remains a separate, future step per CLAUDE.md §19.7.
- **Whether "Resulting Structural Context" (BA-08) itself requires its own registration** — that future Business Activity's own eligibility question; `ADR-010`'s pattern recognition already establishes it qualifies in principle as the pattern's sixth and final stage, but it is not registered by this section.

---

## 27. Business Object Registration — Resulting Structural Context

**Trigger:** BA-08's own implementation-readiness assessment independently re-confirmed — not merely assumed from precedent — that Resulting Structural Context, the Structural Context Lifecycle's sixth and final stage, satisfies SD-002 §2 and the Cross-Experience Reference Test on the most literal textual evidence of any of the six stages, citing `ADR-010`'s own pattern recognition for the general eligibility question per that ADR's Decision point 4. This section performs the registration CMD-001 §26.3 requires **before** BA-08's own implementation-readiness gap analysis can proceed. This section does not authorize implementation.

**Governing decision:** `ADR-013_Resulting_Structural_Context_Canonical_Business_Object_Registration.md` records the governance decision authorizing this registration. CMD-001 remains **LOCKED** — this registration exercises CMD-001 §26.3's own existing registration mechanism.

### Registration Entry

| Attribute (CMD-001 §26.4) | Value |
|---|---|
| **Business Object Identifier** | `RSC-000001` |
| **Canonical Name** | Resulting Structural Context |
| **Business Description** | The structural context produced by a successfully completed transition — the closure of a validated proposal into a recognizable resulting enterprise state. §38.15's own Meaning, verbatim: "Structural context produced by successful completion." EX-C005-11's own Purpose, verbatim: "Establish Resulting Structural Context and completed Enterprise Transition." Business Value, verbatim: "Creates a recognizable resulting enterprise state and closes the structural decision coherently." |
| **Business Domain** | Enterprise Structure Management (C-005) |
| **Aggregate Root** | Resulting Structural Context itself — per `ADR-010` point 5, not merged with Validation Context (VLC-000001) or any earlier stage; its own independently-identified object, related to Validation Context (see Relationship Mapping). |
| **Business Owner** | Structural Steward; eligible decision participant by reference to URA-001 (EX-C005-11 Participating Personas, verbatim: "Structural Steward and eligible decision participant by reference to URA-001"). |
| **Data Steward** | Pending Canonical Binding — same disclosed gap class already recorded for SCI-000001/POC-000001/IMC-000001/RVC-000001/VLC-000001 (§21/§22/§23/§25/§26). |
| **Primary Data Category** | Transaction — a governed completion record, the same classification already applied to every other Structural Context Lifecycle member. |
| **System of Record** | Pending — reserved for BA-08's own future implementation-readiness gap analysis. |
| **Lifecycle Model** | SD-002-008's default lifecycle: **CREATED** (BA-08/EX-C005-11, Produced Context: "Resulting Structural Context and completion outcome") → **ARCHIVED** (SD-002-008's terminal state; not addressed in PE-001-C005's own text but not foreclosed by it). **Deliberately no INVALIDATED transition** — unlike its five siblings, EX-C005-11's own Invalidated Context text ("Transient proposal/review context closes as completed") describes the *prior* stages' contexts closing as a *result* of this stage's own completion, not Resulting Structural Context's own state being invalidated by a later material revision. This object represents a terminal, successfully-completed outcome; PE-001-C005's own text gives it no revision-invalidation semantics the way every earlier stage has — a disclosed, deliberate difference, not an oversight. |
| **Versioning Policy** | Full version history retained; per GS-INV-012, "Completion SHALL identify the exact validated proposal revision from which Resulting Structural Context was produced" — exact traceability to one specific `StructuralValidation`, the same per-revision scoping already implemented for Impact Context, Review Context, and Validation Context. |
| **Effective Dating** | Supported — inherited automatically from SD-002-011's universal temporal model; not a distinctive design choice for this object. |
| **Metadata Schema** | Pending — no implementation exists yet. |
| **Security Classification** | Internal — consistent with every other Structural Context Lifecycle member. |
| **AI Context** | "Represents the resulting enterprise structural state produced by a successfully completed, validated transition." EX-C005-11's own AI Assistance clause, quoted exactly: *"AI MAY explain completion outcome and Resulting Structural Context. It SHALL not independently complete the transition."* |
| **Status** | Draft — newly created registration entry; no separate CBOR-entry-approval governance step is defined anywhere in this repository. Subject to this task's own Independent Review (Phase 4). |

### Relationship Mapping (CMD-001 §26.5)

| Resulting Structural Context | Relationship | Target |
|---|---|---|
| Resulting Structural Context | `DERIVED_FROM` | Validation Context (VLC-000001) — confirmed by EX-C005-11's own Required/Consumed Context: "Validated Transition Context." |
| Resulting Structural Context | `PRECEDES` | Downstream Continuation Context (§40.9's own Exit Context; EX-C005-12's own Produced Context, BA-09 candidate) — confirmed by EX-C005-12's own Required/Consumed Context: "Resulting Structural Context and next enterprise objective." Whether Downstream Continuation Context itself requires CBOR registration is **not decided here** — BA-09's own future eligibility question. |

### Business Activity Mapping (CMD-001 §26.6)

- **Consumes:** BA-07 — Validate Transition Readiness (VLC-000001)
- **Produces:** BA-08 — Complete Structural Transition (itself)
- **Supports:** BA-09 — Continue from Resulting Structure (candidate, not yet chartered)

### Governing References

- **Governing Business Activities:** BA-08 (create), BA-09 (consume, candidate)
- **Governing Enterprise Experiences:** EX-C005-11 (Complete Structural Transition, produces); EX-C005-12 (Continue from Resulting Structure, consumes, candidate)
- **Governing Business Rules:** BR-C005-009 ("Completion SHALL produce Resulting Structural Context"), BR-C005-010 ("Exiting without completion SHALL not represent a proposal as resulting enterprise structure" — cross-cutting, BA-03 through BA-08)
- **Governing Invariants (PE-001-C005 Chapter 43):** GS-INV-008, GS-INV-012

### Explicitly Not Decided by This Registration

- **Physical Implementation Mapping (CMD-001 §26.7)** — Physical Tables, APIs, Events Published/Consumed, Reports, Search Indexes, Knowledge Graph Nodes, AI Embeddings: **all Pending.** No database table, migration, API, or code is authorized or implied by this registration. Determining these remains BA-08's own future implementation-readiness gap analysis.
- **Business Object Quality Score (CMD-001 §26.8)** — not scored.
- **Whether BA-08 is now READY for implementation** — this registration resolves the *constitutional* question only. BA-08's own fresh implementation-readiness gap analysis remains a separate, future step per CLAUDE.md §19.7 — **including the ERG-001-mutation-scope question BA-08's own readiness assessment separately disclosed** (whether/how completion actually mutates `organization_nodes` or any future `organization_hierarchy`/`consolidation_determination` table, given no structured change-representation exists anywhere upstream in the pipeline). This registration covers the C-005 experience-layer completion record only, not any ERG-001 domain mutation mechanism.
- **Whether "Downstream Continuation Context" (BA-09) itself requires its own registration** — that future Business Activity's own eligibility question, not decided or assumed here.

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
