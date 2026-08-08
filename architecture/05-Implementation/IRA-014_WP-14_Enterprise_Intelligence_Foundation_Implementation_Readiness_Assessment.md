# IRA-014 — WP-14 Enterprise Intelligence Foundation (C-090/C-091/C-092) — Implementation Readiness Assessment

**Document ID:** IRA-014
**Work Package:** WP-14
**Capability:** C-090 Enterprise Discovery, C-091 Knowledge Management, C-092 Knowledge Graph Management (`CAP-001` D-005, all Active) — plus the explicitly chartered, implementation-ready elements of the Enterprise Intelligence Convergence Lifecycle
**Governing Specification:** No dedicated `PE-001-C090`/`C091`/`C092` capability specification exists (same finding `IRA-011 §0`/`IRA-012` each independently confirmed for `C-093`/`C-094`, unchanged since). This IRA is grounded directly in `EIA-001` Volumes I & II (`docs/Product/Architecture/EIA-001/*.docx`, extracted and read in full), `RTA-001 §12` (Knowledge Graph Runtime, full) and `§13.9c` (Reasoning Contract), `Complete_Blueprint.md §5.0c` (CDE/BQ Bindings, all eight read directly), `Master_Technical_Architecture.md` AMD-004/005/012/013 (LOCKED physical schema), `ONT-001`, and `SD-002 §§3–6`.
**Status:** DRAFTED — pending Repository Owner review and a separate implementation authorization, per the two-step chartering-then-authorization precedent `WP-10`/`WP-11`/`WP-12` each established. **No Business Activity code, API, or architecture change is authorized by this document.** **Amended following a focused authorization review (this pass):** BA-01 through BA-04 are confirmed implementation-ready subject to their documented interim `PLATFORM_ADMIN` gate; **BA-05 is Classification C — STOP** — a tenant-isolation representation gap in `enterprise_knowledge_graph_registry`'s own LOCKED schema, not an authorization-persona question `PLATFORM_ADMIN` resolves (§6 BA-05, §11).
**Prepared By:** Engineering Governance session (Claude Code), under Repository Owner Instruction "Resume WP-14 — Enterprise Intelligence Foundation" / "Produce IRA-014"
**Date:** 2026-08-09

---

## 1. Purpose

Determines whether, and at what scope, WP-14 (`C-090`/`C-091`/`C-092` Enterprise Intelligence Foundation, plus the chartered Convergence Lifecycle elements) may proceed to implementation, per `CLAUDE.md §19`/`§20`/`§21`. This IRA produces **two** implementation plans — **Plan A** (Business Capability Implementation, §6) and **Plan B** (Enterprise Experience Implementation, §9) — neither of which designs screens or writes code; both are planning determinations only. This IRA also performs the three pre-Business-Activity reviews `CLAUDE.md §21.3` requires: Strategic Enhancement Review (§5a), Historical Screen Review (§5b), Executive Cognition Review (§5c).

**This IRA's central finding, stated up front:** the constitutional foundation for `C-090`/`C-091`/`C-092` and the chartered Convergence Lifecycle elements is complete, LOCKED, and internally consistent — independently re-verified against `RTA-001 §12` (full text, all 18 subsections), `Complete_Blueprint.md §5.0c` (all eight Bindings, full text), and `Master_Technical_Architecture.md`'s own `CREATE TABLE` statements (not summaries) in this pass, not accepted on trust from the charter's own prose. Every physical table WP-14 needs already exists, LOCKED: `discovery_provider_registry` (AMD-013), `unclassified_intelligence_registry` (AMD-005), `customer_metric_registry`'s Binding-3 rework (AMD-004: `semantic_match_attempted_flag`, `convergence_count`, `promotion_decision`), `knowledge_asset_registry` and `enterprise_knowledge_graph_registry` (AMD-012). **One structural finding materially shapes authorization design (§10):** none of these five tables carries a `domain_id` column. **Amended finding:** four (`discovery_provider_registry`, `unclassified_intelligence_registry`, `customer_metric_registry`, `knowledge_asset_registry`) are `organization_id`-scoped only; the fifth, `enterprise_knowledge_graph_registry`, carries **no tenant-boundary column of any kind** — a materially different, more serious gap than the other four share (§6 BA-05, §11). WP-13's own Authorization Runtime Engine integration (the ADMIN-level DomainPermission grant mechanism proven across `domain_permission.py`/`approval_authority.py`/`delegation_policy.py`) has no anchor to attach to here — the same structural absence `TD-025` (Runtime Assignment Policy) already documented for an unrelated resource. WP-14 therefore correctly falls back to the interim `PLATFORM_ADMIN`-only gate every Work Package used at inception, disclosed as new Technical Debt (§13), not an authorization gap this IRA invents a workaround for. **This absence of a `domain_id` column does not, by itself, make `PLATFORM_ADMIN` constitutionally correct** — it is justified for BA-01 through BA-04 only because two already-certified, independently-reviewed repository precedents (`WP-10`'s own `establish_configuration`, `WP-11`'s own `register_content`) govern the identical resource shape (organization-scoped only, no Domain anchor, a write/establish action) and reach the same interim conclusion, not because a missing column automatically implies a missing-persona-only gap. **A focused authorization review of BA-01 through BA-05, performed after this IRA's own first draft, found that this reasoning does not extend to BA-05**: `enterprise_knowledge_graph_registry` carries no tenant-boundary column of any kind, which `PLATFORM_ADMIN` does not resolve (§6 BA-05, §11).

---

## 2. Governing Documents Reviewed

- `CAP-001_Enterprise_Capability_Registry.md` — `C-090`/`C-091`/`C-092` registration, verbatim: "Understand enterprise context" / "Curate enterprise knowledge" / "Maintain semantic relationships," all Active, D-005, owned by `EIA-001`.
- `EIA-001` Volume I & II (`docs/Product/Architecture/EIA-001/*.docx`) — read in full. §7.2 (meta-model: Source → Discovery → Signal → Knowledge Management → Knowledge Asset → Knowledge Graph → Relationship → Enterprise Understanding), §12.1/§12.2 (Enterprise Understanding / Enterprise Context definitions), §5.1.6 ("Search and Conversation Are Access Patterns, Not Sources"), Vol. II §31.5 (capability-level architecture confirmed complete for all six D-005 capabilities), Vol. II Ch. 5–6 (Source Taxonomy, Connector Architecture).
- `RTA-001 §12` (Knowledge Graph Runtime) — full text, all 18 subsections read directly: Purpose/Principle/Runtime Position (§12.1–12.3), Runtime Responsibilities/Knowledge Sources/Construction (§12.4–12.6), Graph Synchronization Pipeline (§12.7), Entity Resolution (§12.8), Relationship Resolution (§12.9), Semantic Enrichment/Inference/AI Collaboration (§12.10–12.12), Graph Query Runtime/Runtime Collaboration (§12.13–12.14), Knowledge Observability/Governance (§12.15–12.16), Relationship with ERG-001/CMD-001 (§12.17), Architectural Guarantees (§12.18).
- `RTA-001 §13.9c` (Reasoning Contract Execution) — the Semantic Matching invocation mechanism the charter names: input assembled strictly per a declared `input_contract_schema_json`, output validated against `output_contract_schema_json` before any downstream use; defines no reasoning algorithm.
- `Complete_Blueprint.md §5.0c` (Node Applicability & Framework Governance, binding) — all eight Bindings read directly, not summarized: Binding 1 (Node Applicability), Binding 2 (Framework Tiers), **Binding 3** (semantic match before create; Corporate-Scoped default; convergence-triggered promotion, Aurex Admin decision, never automatic), Binding 4 (framework onboarding), **Binding 5** (Unclassified Intelligence Registry — the exact three-way Governance Manager decision: map to existing CDE / confirm genuinely new and create, Corporate-Scoped by default / mark not relevant and discard), Bindings 6–8 (ownership, hiding, framework completeness).
- `Master_Technical_Architecture.md` — `CREATE TABLE` statements read directly (not paraphrased) for `discovery_provider_registry` (line 3244), `enterprise_knowledge_object_registry` (3267), `knowledge_asset_registry` (3169), `enterprise_knowledge_graph_registry` (3147), `document_chunk_registry`/`vector_index_registry` (3189/3208, WP-11 precedent), `unclassified_intelligence_registry` (5389), and the `customer_metric_registry`/`metric_registry` AMD-004 rework (`ALTER TABLE`, 5334–5377) implementing Binding 3's semantic-match/convergence/promotion model in full (`cde_tier`, `semantic_match_attempted_flag`, `semantic_match_result_metric_id`, `semantic_match_score`, `convergence_count`, `promotion_requested_flag`, `promotion_decision`).
- `SD-002_Universal_Business_Object_Rules.md` §§3–6 — CDE rules (`SD-002-021`–`028`, incl. `SD-002-024` Discovery Method Visibility, `SD-002-025` Confidence Composition — evidence quality is one of five contributing factors), BQ rules (`§4`), Business Activity rules (`§5`), Evidence & Source Intelligence rules (`§6`, incl. `SD-002-040` Evidence as First-Class Object, `SD-002-041` No CDE Without Evidence Capability, `SD-002-042` recognized evidence source classes, `SD-002-043` granular evidence references) — all read directly.
- `ONT-001_Enterprise_Ontology_Architecture.md` — the semantic relationship-kind vocabulary (Classification/Specialization/Composition/Aggregation/Association/Reference) `RTA-001 §12.10`'s Semantic Enrichment and Ontology Validation consume.
- `CMD-001_Canonical_Data_Model.md §24`/`§26` — Knowledge & AI Domain (Ontology Aggregate Root named, not itself defined — `ONT-001` completes it); `§26.3a` Business Object Eligibility criteria.
- `SER-001_Strategic_Enhancement_Register.md` — `SE-024` (WP-11 umbrella; "C-090 disclosed, not selected this cycle" — the direct textual precedent naming WP-14 as C-090's own eventual home), `SE-025` (Knowledge Graph real build, Deferred, "Part of SE-024," "Zero graph database exists anywhere in the running system"), `SE-026` (Search, Implemented — not this Work Package's concern), `SE-027` (Multi-Agent orchestration, Deferred, cross-cutting, unaffected by this scope).
- `HISTORICAL-SCREEN-REALIZATION-MATRIX.md` — `F1_Enterprise_Understanding_Center.html` and `I1_Intelligence_Center.html`, both EVOLVE CONCEPT, both mapped to `C-090` (`I1` also to `C-091`/`C-093`), read directly (§7b below).
- `EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md` — the Access→Understand→Decide layering and its explicit statement that Decide-stage Executive experience is "genuinely gated on Enterprise Intelligence capabilities (`C-090+`) existing" (§7c below).
- `WP-REG-001 §5`/`§6`, `WPR-001 §2` — WP-14's own charter text (Repository Owner Instruction "Implementation Replanning Approval," and the separate "Enterprise Intelligence Convergence Constitutional Design Workshop" instruction the Convergence Lifecycle elements trace to), read verbatim, not paraphrased from memory.
- `Backend/Runtime/AuthorizationEngine/` and `Backend/Services/AuthService/routers/domain_permission.py`/`approval_authority.py`/`delegation_policy.py` — WP-13's own committed, tested Authorization Runtime Engine integration, read directly to determine applicability (§10).
- Existing repository source, read directly: full search of `Backend/` for any `discovery`, `knowledge`, `unclassified_intelligence`, `enterprise_knowledge_graph` implementation (none found); `AIService/alembic/versions/` (two migrations, WP-11/WP-12 only); `source/frontend/src/config/admin-navigation.ts` (nav slot survey, §9).
- `CANONICAL-ENTERPRISE-SEARCH-ARCHITECTURE-SPECIFICATION.md` — an uncommitted reconstruction (not itself authoritative), consulted for its own disclosed-gaps list and cross-reference map; every citation from it re-verified against the primary source directly in this pass, not taken on its own word.

---

## 3. Existing Asset Discovery (Reuse Before Creating, `CLAUDE.md §19.2`)

| Asset | Location | Status |
|---|---|---|
| `EIA-001 §7.2` meta-model (Source → Discovery → Signal → Knowledge Mgmt → Knowledge Asset → Knowledge Graph → Relationship → Enterprise Understanding) | `EIA-001` | Fully specified, constitutional. Zero code. |
| `RTA-001 §12` Knowledge Graph Runtime (full, 18 subsections) | `RTA-001` | Fully specified, constitutional. Zero code — this Work Package is the first to implement any of it. |
| `Complete_Blueprint.md §5.0c` Bindings 3/5 (semantic match, Unclassified Intelligence, convergence/promotion) | `Complete_Blueprint.md` | Fully specified, LOCKED, binding. Zero code. |
| `discovery_provider_registry` (AMD-013) | `Master_Technical_Architecture.md` | LOCKED physical schema, real (30 `provider_type` values, `connection_config_json`, `credential_id` reusing existing `api_credential_registry`). Zero rows anywhere in a running system. |
| `unclassified_intelligence_registry` (AMD-005) | `Master_Technical_Architecture.md` | LOCKED physical schema, real, RLS policy already specified. Zero rows — `WP-REG-001`'s own charter text confirms "unpopulated by any prior WP." |
| `customer_metric_registry`/`metric_registry` Binding-3 rework (AMD-004) | `Master_Technical_Architecture.md` | LOCKED physical schema, real (`semantic_match_attempted_flag`, `convergence_count`, `promotion_decision` all present as actual columns, independently verified — not merely charter-cited). Zero rows exercising this path. |
| `knowledge_asset_registry` / `enterprise_knowledge_graph_registry` (AMD-012) | `Master_Technical_Architecture.md` | LOCKED physical schema, real. `enterprise_knowledge_graph_registry`'s own governing comment states explicitly it **is** the Postgres-side relational index/RLS audit trail of the Knowledge Graph, **not** the primary store — Neo4j Aura is. Zero rows; zero Neo4j infrastructure anywhere (confirmed by `WP-11`'s own IRA exclusion: "C-090/C-092 excluded — different capability / zero Neo4j infrastructure"). |
| `RTA-001 §13.9c` Reasoning Contract | `RTA-001` | Fully specified, constitutional, already the mechanism `WP-11`'s own `RAGEngine`/Reasoning Engine selection uses conceptually — reused, not reinvented, for Semantic Matching. |
| `confidence_scoring_registry` (AMD-003) | `Master_Technical_Architecture.md` | Real, already the FK target on `knowledge_asset_registry`/`enterprise_knowledge_graph_registry`/`unclassified_intelligence_registry`'s own sibling tables — reused, not duplicated. |
| `evidence_registry`/`document_chunk_registry` | `Master_Technical_Architecture.md`, real, built by WP-11 | **Exists, real, already built.** `SD-002-041`'s Evidence-capability obligation is satisfied by binding to this existing registry, not a new one. |
| `AIService` real authentication, Alembic chain | `Backend/Services/AIService/` | **Exists, real, already built by WP-11**, extended by WP-12. WP-14 extends the same chain — does not bootstrap a second one. |
| WP-13 Authorization Runtime Engine (ADMIN-level DomainPermission grant) | `Backend/Runtime/AuthorizationEngine`, `AuthService/dependencies.py::enforce_domain_permission` | **Exists, real, fully proven** across five endpoints. **Not applicable to WP-14's own resources** — none of the five tables above carries a `domain_id` column (§10). |
| `source/frontend/src/config/admin-navigation.ts` `enterprise-intelligence` slot | `source/frontend/src/config/` | Exists, but **already occupied** — reused by `WP-11` for `EnterpriseSearchScreen`. Not a free slot for WP-14 (§9). |

**Conclusion:** per `CLAUDE.md §2`/`§19.5` (Reuse → Configure → Extend → Compose → Create), WP-14 implements `RTA-001 §12` and `Complete_Blueprint.md §5.0c`'s own already-fully-specified constructs for the first time — necessary and expected, mirroring `IRA-011`/`IRA-012`'s own identical finding for their own governing runtimes. No new table, column, or constraint is proposed anywhere in this IRA. The one genuine structural gap (no `domain_id` anchor for authorization) is disclosed, not worked around (§10).

---

## 4. Existing Asset Discovery — Cross-Reference to WP-13

Verified directly (`CLAUDE.md` instruction #11): WP-13's Authorization Runtime integration surface (`a180ca4`) and its full `domain_permission.py`/`approval_authority.py` (DOMAIN scope)/`delegation_policy.py` (DOMAIN scope) retrofit are committed and pushed to `origin/main` (`fdc203a`…`909ba08`, `TD-022`/`090`/`137`/`138`/`139` Closed, `TD-023`/`024` partially resolved). `enforce_domain_permission()` is available for reuse by any resource carrying a `domain_id` anchor. **No WP-14 resource carries one** (§1, §10) — this IRA does not recreate authorization logic; it correctly identifies that WP-13's own mechanism has no attachment point here, and names the resulting gap as ordinary, disclosed Technical Debt (§13), the same class every capability before WP-13 carried at its own inception.

---

## 5. Gap Analysis

### 5a. Strategic Enhancement Review (`CLAUDE.md §21.3`)

| SE | Enhancement | Disposition for WP-14 |
|---|---|---|
| `SE-024` | WP-11 umbrella — "C-090 Enterprise Discovery or C-093 Enterprise Search," resolved to C-093 for WP-11, **"C-090 disclosed, not selected this cycle."** | **Realized by this Work Package** — WP-14 is the deferred continuation `SE-024` itself named, not a new enhancement. |
| `SE-025` | Knowledge Graph real build (Neo4j Aura). "Zero graph database exists anywhere in the running system." | **Partially addressed by this Work Package, disclosed, not fully closed** — WP-14 builds the real, LOCKED relational registry (`enterprise_knowledge_graph_registry`) and the Entity/Relationship Resolution logic that populates it; the live Neo4j Aura connection (`graph_engine_reference` population) remains the disclosed, deferred external-integration point, mirroring `WP-11`'s own embedding-provider-credentials deferral exactly (`SE-026`'s own precedent). |
| `SE-026` | Semantic Search real implementation. | **Not this Work Package's concern** — already Implemented at `WP-11`'s own authorized scope; unaffected. |
| `SE-027` | Multi-Agent orchestration. | **Not this Work Package's concern** — cross-cutting runtime, remains Deferred, unaffected. |

No `SER-001` item names a Convergence-Lifecycle-specific deliverable this Gap Analysis has not already accounted for; the Convergence elements trace to the separate "Enterprise Intelligence Convergence Constitutional Design Workshop" instruction, not to an existing `SER-001` row — consistent with `WPR-001 §2`'s own citation.

### 5b. Historical Screen Review (`CLAUDE.md §21.3`)

Two entries in `HISTORICAL-SCREEN-REALIZATION-MATRIX.md` are directly relevant, both already classified **EVOLVE CONCEPT**, both explicitly named as awaiting exactly this Work Package:

- **`F1_Enterprise_Understanding_Center.html`** — maps to `C-090`. Its own governing text: *"Confidence-gap surfacing with 'who should confirm this' routing... Auto-extraction, contradiction detection, per-item confirmation routing... No chartered Work Package exists yet (C-090 Enterprise Discovery, Active, unchartered) — this is a real, evidenced future business case."* This is a direct historical precedent for BA-02/BA-03's own candidate-intake-and-resolution shape (§6).
- **`I1_Intelligence_Center.html`** — maps to `C-090`/`C-091`/`C-093`. Its own governing text: *"Unclassified-item queue with governance routing... Overall confidence scoring, 'Connect a system' flow, audit trail... Only a placeholder navigation slot exists today (enterprise-intelligence route) — no chartered Work Package (C-090/091/093, Active, unchartered)."* This is a direct historical precedent for BA-03's own Governance Manager resolution queue (§6, §9).

Both concepts are historical CorpStage 360 material (pre-AUREX), evolved not resurrected verbatim — per the matrix's own remediated finding, their underlying business intent (evidence-first, confidence-gated discovery-to-resolution) survives independently of their specific historical framing, and neither requires L2 ("Never ESG") correction, since neither is ESG-specific in intent. No new screen concept is invented by this IRA — both are already-evolved concepts this Work Package is the first to actually realize.

### 5c. Executive Cognition Review (`CLAUDE.md §21.3`)

Per `EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md`, read directly: Discover/Understand-stage Executive experience does not require `C-090+` to exist first, but genuine **Decide**-stage Executive experience (`PE-001` Chapter 23) is *"genuinely gated on Enterprise Intelligence capabilities (C-090+) existing"* — real Evidence/Confidence properties `SE-030`/`SE-031` themselves still await. WP-14 is therefore the Work Package that **unblocks** Decide-stage Executive Cognition for the first time, without itself being obligated to build a Decide-stage screen — that remains a future capability's own scope (`C-094`'s eventual maturation, or a future `C-090`-consuming Executive surface), consistent with `IRA-011 §4c`/`IRA-012 §4c`'s own precedent of naming the unblocking without overclaiming the unblocked screen as in-scope.

### 5.1 Establish Discovery Provider Configuration — **IN SCOPE**

`discovery_provider_registry` (AMD-013) is fully specified: `provider_name`, `provider_category` (ENTERPRISE/EXTERNAL/REALTIME), `provider_type` (30 named values, category-consistent), `connection_config_json`, `credential_id` (reusing the pre-existing `api_credential_registry`, never duplicating credential storage), `discovery_cadence`, `governing_policy_id` (reusing `confidence_scoring_registry`), `organization_id`. A real, buildable target with zero existing conflicting implementation — structurally identical in shape to `WP-11 BA-01` (`vector_index_registry` configuration).

**Disposition:** in scope, buildable now, lowest risk — realized as **BA-01**.

### 5.2 Register Enterprise Intelligence Candidate — **IN SCOPE (explicitly named "implementable now" by the charter)**

`unclassified_intelligence_registry` (AMD-005) is fully specified and the charter's own first-listed Convergence element. `extraction_method`'s own enumeration includes `MANUAL_ENTRY` and `API_INGEST` alongside five automated-extraction values (`OCR`/`NLP_PARSE`/`TABLE_EXTRACT`/`ENTITY_EXTRACT`/`SEMANTIC_PARSE`) — the latter five presuppose a live extraction pipeline over a connected Discovery Provider, which does not exist (§5.1's own disclosed deferral). This Business Activity is therefore correctly scoped to the two extraction methods that require no live connector: a caller directly registers a candidate fact, mirroring `WP-11 BA-03`'s own "Register Enterprise Search Content" precedent (direct API registration standing in for an undone live-connector problem) exactly.

**Disposition:** in scope, narrow (`MANUAL_ENTRY`/`API_INGEST` only) — realized as **BA-02**. Excluded: the five automated `extraction_method` values, which require Discovery Provider connector protocols this Work Package does not build (§5.1).

### 5.3 Resolve Enterprise Intelligence Candidate (Convergence Decision) — **IN SCOPE — the core Convergence deliverable**

`Complete_Blueprint.md §5.0c` Binding 5, read directly: a Governance Manager does *"exactly one of three things: map the entry to an existing CDE the automated semantic match missed; confirm it is genuinely new and create a CDE for it, Corporate-Scoped by default per Binding 3; or mark it not relevant and discard."* This is the literal three-way outcome set the charter names (`MAPPED_TO_EXISTING`/`NEW_CDE_CREATED`/`DISCARDED`) — `resolution_status`'s own fourth value, `PROMOTED_CONVERGENCE`, is a later-lifecycle-stage consequence of convergence tracking crossing a threshold (Binding 3: *"When this count crosses a... configured threshold, a promotion review is triggered automatically"*), not a fourth decision a Governance Manager makes at resolution time — this BA produces the three-way decision only; automatic promotion-review triggering is this BA's own downstream effect, not a manual outcome it asks for.

Semantic Matching precedes the human decision (`RTA-001 §13.9c` Reasoning Contract, existing three-way outcome set only — no new outcome invented, per the charter's own explicit constraint) and populates `customer_metric_registry.semantic_match_attempted_flag`/`semantic_match_result_metric_id`/`semantic_match_score` when a `NEW_CDE_CREATED` path is taken. Evidence binding (`SD-002-041`) and Confidence's evidence-quality factor (`SD-002-025`) are cross-cutting obligations of this same resolution act, not separate Business Activities — `CMD-001 §26.3a` Step 1 (independent business identity) would fail for either as a standalone candidate, the same reasoning `IRA-012 §4.4` already applied to its own Progressive Disclosure/Evidence Panel prerequisite.

**Disposition:** in scope, mandatory, core — realized as **BA-03**, with Evidence/Confidence binding folded in as a cross-cutting requirement of the same Business Activity.

### 5.4 Establish Knowledge Asset — **IN SCOPE, kept structurally distinct from Convergence**

`EIA-001 §7.2`'s own meta-model names Knowledge Asset as `C-091`'s own deliverable — the curated product of a Signal, physically realized by `knowledge_asset_registry` (AMD-012). **Disclosed, not invented:** no document anywhere states that a resolved Convergence candidate *becomes* a Knowledge Asset, or that a Knowledge Asset *becomes* an `unclassified_intelligence_registry` row — the two registries are, in the repository's own words (traced independently to `Master_Technical_Architecture.md`'s own schema comments, not merely the reconstruction's framing), governed by two parallel, independently-owned meta-models (`EIA-001` for Knowledge Assets; `SD-002`/`Complete_Blueprint.md` for CDEs) that meet nowhere in text. This IRA does **not** invent that bridge. BA-04 is therefore built directly against `knowledge_asset_registry`'s own real anchor — `source_ingestion_id` → `data_ingestion_registry` (already real, built by `WP-11`) — independent of BA-02/BA-03's own CDE-resolution path.

**Disposition:** in scope, buildable now — realized as **BA-04**, structurally independent of the Convergence Lifecycle (BA-02/BA-03), consistent with the two meta-models' own documented separation.

### 5.5 Synchronize Enterprise Knowledge Graph — **IN SCOPE, scoped to the relational registry, not the live graph**

`RTA-001 §12.7`'s Graph Synchronization Pipeline (Business Activity Completed → Domain Event → Entity Resolution → Relationship Resolution → Semantic Enrichment → Ontology Validation → Graph Update → Knowledge Index Refresh) is fully specified; the charter's own "requires no new work at all" framing describes the **trigger** (a generic Domain Event subscription, genuinely free), not the Entity Resolution (`§12.8`)/Relationship Resolution (`§12.9`) logic itself, which is real, new engineering work this Business Activity performs. `enterprise_knowledge_graph_registry`'s own governing comment is unambiguous: this table **is** the Postgres-side relational index/audit trail, **not** the Neo4j graph — `graph_engine_reference` remains NULL until a live Neo4j Aura synchronization exists, which this Work Package does not build (zero Neo4j infrastructure anywhere, `WP-11 IRA`'s own confirmed exclusion, unchanged).

**Disposition:** in scope architecturally, scoped narrowly to the relational registry and Entity/Relationship Resolution against it — realized as **BA-05**. Excluded: the live Neo4j Aura write itself (disclosed, deferred external integration, mirroring `WP-11`'s own embedding-provider-credentials deferral, §5.1's own discovery-connector deferral). **"In scope" here is a chartering/architecture-fit determination, not a readiness-to-implement determination** — a focused authorization review found `enterprise_knowledge_graph_registry` carries no tenant-boundary column, a `CLAUDE.md §19.8.5`-class gap; BA-05 is **Classification C — STOP**, not implementation-ready, pending a Repository Owner decision (§6 BA-05's own amended table, §11).

### 5.6 Explicitly Excluded — preserved, not silently implemented

- **`ENRICH_EXISTING`/`PROPOSE_NEW_BUSINESS_QUESTION` as new resolution outcomes** — would modify Binding 5's own locked three-way text (§5.3). Not implemented. Requires a future constitutional amendment to `Complete_Blueprint.md §5.0c` itself, a Repository Owner decision this IRA does not make.
- **Interpretation** (`EIA-001 §7.2`, Enterprise Understanding → Enterprise Intelligence) — confirmed, independently, to have no implementation-ready specification anywhere in the repository (only `SD-001 §1.2`'s own philosophical framing). Not implemented.
- **Intelligence Evaluation** (Intelligence Evolution) — requires an uncharted `CAP-001` capability. Not implemented; no capability is invented here to close this gap.
- **Live Discovery Provider connector protocols** (any of the 30 named `provider_type` values' actual authentication/pagination/rate-limiting mechanics) — `WP-11`'s own IRA already excluded these from `C-093`'s scope as `C-090`'s domain; this IRA confirms they remain out of *this* Work Package's own scope too — connector protocol design is an engineering-layer decision (`IMP-001`) this IRA does not make, and no document anywhere specifies it (§5.1).
- **Live Neo4j Aura graph write** — §5.5.
- **Ranking/reranking algorithm, web-crawling mechanism, document parsing per file modality** — each already independently disclosed as Pending Canonical Binding / engineering-layer / unspecified by `WP-11`'s own closure and the `CANONICAL-ENTERPRISE-SEARCH-ARCHITECTURE-SPECIFICATION.md` reconstruction; none is `C-090`/`C-091`/`C-092`'s own obligation to close, and none is closed here.

### 5.7 Summary

| Item | Disposition | Realization |
|---|---|---|
| Establish Discovery Provider Configuration | In scope | BA-01 |
| Register Enterprise Intelligence Candidate | In scope, narrow (`MANUAL_ENTRY`/`API_INGEST` only) | BA-02 |
| Resolve Enterprise Intelligence Candidate (Semantic Matching, 3-way decision, convergence tracking, Evidence/Confidence binding) | In scope, mandatory, core | BA-03 |
| Establish Knowledge Asset | In scope, structurally independent of Convergence | BA-04 |
| Synchronize Enterprise Knowledge Graph (relational registry only) | In scope architecturally — **not implementation-ready, Classification C, §6/§11** | BA-05 |
| `ENRICH_EXISTING`/`PROPOSE_NEW_BUSINESS_QUESTION` | Excluded | None this WP |
| Interpretation | Excluded | None this WP |
| Intelligence Evaluation | Excluded | None this WP |
| Live Discovery Provider connectors | Excluded | None this WP |
| Live Neo4j Aura graph write | Excluded | None this WP |

**Five Business Activities** — one more than `WP-11`/`WP-12`'s own three-BA shape, proportionate to covering three chartered capabilities (`C-090`/`C-091`/`C-092`) plus the Convergence Lifecycle's own core deliverable, not micro-BA inflation (each BA carries independent business identity per `CMD-001 §26.3a`, verified individually above).

---

## 6. PLAN A — Business Capability Implementation

### BA-01 — Establish Discovery Provider Configuration

| Field | Content |
|---|---|
| **BA ID** | BA-01 |
| **Business Capability** | C-090 Enterprise Discovery |
| **Business Objective** | Register a governed configuration for one Enterprise Intelligence discovery source, without requiring a live connection to it. |
| **Business Intent** | Realize `discovery_provider_registry`'s own purpose: replace the implicit single-source assumption with a typed, extensible provider registry, per the governing law that the platform shall not assume uploaded documents represent complete enterprise knowledge. |
| **Participating Personas** | No `PE-001-C090` names one. Interim: `PLATFORM_ADMIN` only (§10). |
| **Business Objects** | `discovery_provider_registry` row (AMD-013) — not a new canonical object, an existing LOCKED registry (§7). |
| **Business Rules** | `provider_type` must be category-consistent with `provider_category` (DB CHECK, AMD-013); credentials are never stored in `connection_config_json` — only via `credential_id`, reusing `api_credential_registry`. |
| **APIs/services required** | `POST /discovery-providers` (establish); `GET /discovery-providers` (list, tenant-scoped). No live connector service. |
| **Frontend/UX required** | Admin config screen — establish/list, per §9. |
| **Authorization requirements** | Interim `PLATFORM_ADMIN`-only (§10) — no `domain_id` anchor exists on this table. |
| **Evidence/provenance requirements** | None at establishment — a configuration record, not a knowledge claim. |
| **Dependencies** | `api_credential_registry` (pre-existing, reused); `confidence_scoring_registry` (pre-existing, reused via `governing_policy_id`). None on BA-02–05. |
| **Acceptance criteria** | A caller establishes a provider configuration; it is retrievable, tenant-scoped; `provider_type`/`provider_category` mismatch is rejected (422). |
| **Testing requirements** | Unit + API (200/201, 401/403, 422) + Mandatory Tenant-Isolation Test Checklist (`CLAUDE.md §21.4`) — two Organizations, no shared row, cross-tenant retrieval denied. |
| **Authoritative architecture references** | `Master_Technical_Architecture.md` AMD-013 (`discovery_provider_registry`, line 3244); `EIA-001 Vol. II Ch. 5–6`. |

### BA-02 — Register Enterprise Intelligence Candidate

| Field | Content |
|---|---|
| **BA ID** | BA-02 |
| **Business Capability** | C-090 Enterprise Discovery (feeding the Convergence Lifecycle intake) |
| **Business Objective** | Capture a raw extracted fact with no matching CDE, rather than discarding it or forcing it into the nearest wrong CDE. |
| **Business Intent** | Realize `Complete_Blueprint.md §5.0c` Binding 5's own opening guarantee: *"An extracted fact with no matching CDE is never discarded."* |
| **Participating Personas** | No `PE-001-C090` names one. Interim: `PLATFORM_ADMIN` only (§10), pending a genuine submitting-persona determination. |
| **Business Objects** | `unclassified_intelligence_registry` row (AMD-005). |
| **Business Rules** | `extraction_method` restricted to `MANUAL_ENTRY`/`API_INGEST` for this BA (§5.2); `resolution_status` always begins `PENDING` (DB default); `raw_extracted_value`/`source_document_reference` mandatory (NOT NULL, AMD-005). |
| **APIs/services required** | `POST /intelligence-candidates` (register). |
| **Frontend/UX required** | A registration form (or the `F1`/`I1`-precedented intake surface, §5b/§9) — not decided by this IRA. |
| **Authorization requirements** | Interim `PLATFORM_ADMIN`-only (§10) — no `domain_id` anchor. |
| **Evidence/provenance requirements** | `source_document_reference`/`source_page_section` mandatory per Binding 5's own text; where the source is an existing `evidence_registry` document, the reference SHOULD resolve to it (reuse, not duplication) — exact binding mechanism determined at Technical Design. |
| **Dependencies** | None on BA-01 (`unclassified_intelligence_registry` carries no `discovery_provider_id` FK — independently verified, §7). Feeds BA-03. |
| **Acceptance criteria** | A caller registers a candidate; it persists with `resolution_status='PENDING'`; an automated `extraction_method` value is rejected (422) with a clear reason. |
| **Testing requirements** | Unit + API (200/201, 401/403, 422 for excluded `extraction_method` values) + Mandatory Tenant-Isolation Test Checklist. |
| **Authoritative architecture references** | `Master_Technical_Architecture.md` AMD-005 (`unclassified_intelligence_registry`, line 5389); `Complete_Blueprint.md §5.0c` Binding 5. |

### BA-03 — Resolve Enterprise Intelligence Candidate (Convergence Decision)

| Field | Content |
|---|---|
| **BA ID** | BA-03 |
| **Business Capability** | Convergence Lifecycle (spans C-090 intake and the CDE/BQ meta-model `SD-002`/`Complete_Blueprint.md` own) |
| **Business Objective** | Resolve a pending candidate to exactly one of three outcomes, with Semantic Matching attempted first, and every outcome carrying real Evidence and Confidence. |
| **Business Intent** | Realize Binding 5's own three-way Governance Manager decision, Binding 3's semantic-match-before-create rule, `SD-002-041` (Evidence capability universal), and `SD-002-025`'s evidence-quality confidence factor. |
| **Participating Personas** | Binding 5 names "a Governance Manager" for the three-way resolution decision this BA performs; its own textual context (Category 5/6 routing — personal-document warnings, "belongs to a different organisation" warnings, confidentiality notifications) confirms it operates within a single Organization, not platform-wide. Binding 3 separately names "Aurex Admin" for the *out-of-scope* promotion decision (Corporate-Scoped → Global, §5.3, not built by this BA) — **clarification, not a scope change:** "Aurex Admin" names the platform operator itself, which aligns semantically with `PLATFORM_ADMIN` directly, not merely as an interim stand-in for a missing persona. This does not extend BA-03's own scope to include promotion, and no new persona is introduced by this observation. No enforceable claim for "Governance Manager" exists in the seeded role catalog (same `ADR-002` root cause `TD-021`-class entries already track). Interim, for the resolution decision this BA actually performs: `PLATFORM_ADMIN` only. |
| **Business Objects** | `unclassified_intelligence_registry` (updated); `customer_metric_registry` (new row, `NEW_CDE_CREATED` path only) or `metric_registry` (referenced, `MAPPED_TO_EXISTING` path). |
| **Business Rules** | Exactly one of `MAPPED_TO_EXISTING`/`NEW_CDE_CREATED`/`DISCARDED` per resolution (Binding 5); Semantic Matching always attempted before `NEW_CDE_CREATED` (Binding 3); a net-new CDE defaults `cde_tier='TENANT'`, Corporate-Scoped (Binding 3) — Global promotion is a separate, later, Aurex-Admin-only act (`promotion_decision`), never automatic; `SD-002-041` — the resulting CDE (new or mapped-to) must carry an evidence relationship. |
| **APIs/services required** | `POST /intelligence-candidates/{id}/resolve` — request: one of the three outcomes + supporting data (target `metric_id` for `MAPPED_TO_EXISTING`; new CDE fields for `NEW_CDE_CREATED`); invokes Semantic Matching (`RTA-001 §13.9c` Reasoning Contract call) before persisting a `NEW_CDE_CREATED` outcome. |
| **Frontend/UX required** | A resolution queue — directly precedented by `I1_Intelligence_Center.html`'s own "Unclassified-item queue with governance routing... Overall confidence scoring" (§5b). |
| **Authorization requirements** | Interim `PLATFORM_ADMIN`-only (§10). |
| **Evidence/provenance requirements** | Mandatory — `SD-002-041`; binds to `evidence_registry` (reused, real, `WP-11`) via the candidate's own `source_document_reference`. |
| **Dependencies** | BA-02 (candidate must exist). Feeds BA-04 only if the resolving caller separately chooses to curate a Knowledge Asset (§5.4 — not automatic). Convergence tracking (`convergence_count` increment, cross-tenant "materially same" comparison) is **flagged, not resolved by this IRA** — no document anywhere specifies the actual matching algorithm for "materially identical... across independent customers" (Binding 3's own text names the business rule, not the mechanism); this is a genuine Technical Design-phase open item (§8), not silently assumed. |
| **Acceptance criteria** | A `PENDING` candidate resolves to exactly one of three states; `NEW_CDE_CREATED` always carries a Semantic Matching attempt record; every resolved outcome carries an Evidence reference and a Confidence score with evidence-quality as a named factor. |
| **Testing requirements** | Unit (all three outcome paths; Semantic Matching invoked before `NEW_CDE_CREATED`; a `DISCARDED` outcome never creates a CDE) + API (200, 401/403, 409 for an already-resolved candidate) + Mandatory Tenant-Isolation Test Checklist — a `NEW_CDE_CREATED` outcome in Organization A must never become visible or matchable from Organization B except through the explicitly-designed convergence-signal path, itself gated to Aurex-Admin-only review (never automatic promotion). |
| **Authoritative architecture references** | `Complete_Blueprint.md §5.0c` Bindings 3 & 5 (full text); `Master_Technical_Architecture.md` AMD-004 (`customer_metric_registry` rework) & AMD-005; `RTA-001 §13.9c`; `SD-002-025`, `SD-002-041`–`043`. |

### BA-04 — Establish Knowledge Asset

| Field | Content |
|---|---|
| **BA ID** | BA-04 |
| **Business Capability** | C-091 Knowledge Management |
| **Business Objective** | Curate a Signal into a governed Knowledge Asset, carrying Provenance from first existence, per `EIA-001`'s own invariant. |
| **Business Intent** | Realize `EIA-001 Vol. I §7`'s Knowledge Asset concept: "a curated, governed unit of knowledge produced from one or more Signals." |
| **Participating Personas** | No `PE-001-C091` names one. Interim: `PLATFORM_ADMIN` only. |
| **Business Objects** | `knowledge_asset_registry` row (AMD-012). |
| **Business Rules** | `curation_status` begins `PROPOSED` (DB default; EIA-001 Vol. II §13 Knowledge Validation states: PROPOSED/VALIDATED/ACCEPTED/REJECTED/SUPERSEDED); `provenance_reference` mandatory — *"no Knowledge Asset without Provenance"* (EIA-001 Vol. I §7.3 invariant, independently re-verified, not restated from the reconstruction); `freshness_last_confirmed_at` — *"Freshness Decays Unless Renewed"* (EIA-001 Vol. II §17.5), read-path/staleness mechanics determined at Technical Design. |
| **APIs/services required** | `POST /knowledge-assets` (establish, `PROPOSED`); a status-transition endpoint (`PROPOSED`→`VALIDATED`/`ACCEPTED`/`REJECTED`) — exact transition shape (single generic endpoint vs. named actions, mirroring `OrganizationService.activate()`/`suspend()`'s own precedent) determined at Technical Design. |
| **Frontend/UX required** | Establish + status view, per §9. |
| **Authorization requirements** | Interim `PLATFORM_ADMIN`-only (§10). |
| **Evidence/provenance requirements** | Mandatory at establishment (`provenance_reference`) — this BA's own defining rule. |
| **Dependencies** | `source_ingestion_id` → `data_ingestion_registry` (pre-existing, real, `WP-11`) — reused, not duplicated. Structurally independent of BA-02/BA-03 (§5.4). |
| **Acceptance criteria** | A Knowledge Asset establishes in `PROPOSED` state with mandatory Provenance; a Knowledge Asset with no Provenance is rejected (422). |
| **Testing requirements** | Unit (Provenance mandatory; `curation_status` transitions correctly bounded) + API (200/201, 401/403, 422) + Mandatory Tenant-Isolation Test Checklist. |
| **Authoritative architecture references** | `Master_Technical_Architecture.md` AMD-012 (`knowledge_asset_registry`, line 3169); `EIA-001 Vol. I §7`, `Vol. II §13`, `§17.5`. |

### BA-05 — Synchronize Enterprise Knowledge Graph — **Classification C — STOP, not implementation-ready (amended)**

**Amendment (post-draft authorization review):** `enterprise_knowledge_graph_registry`'s own `CREATE TABLE` (line 3147, re-verified a second time for this amendment) carries **no `organization_id` column** — unlike every other table this Work Package touches. `source_entity_id`/`target_entity_id` are **untyped, polymorphic references** (`source_entity_type VARCHAR`/`source_entity_id UUID`, no declared foreign key of any kind) — nothing in the schema itself ties either end of a relationship row to a specific owning table, let alone guarantees both ends belong to the same Organization. Tenant ownership is therefore **only transitively inferable** — by resolving `source_entity_id`/`target_entity_id` against whichever table they happen to point to (`knowledge_asset_registry`, `metric_registry`/`customer_metric_registry`, etc., each of which *does* carry `organization_id`) — and is **not schema-enforced** at this table's own level. **This is a tenant-isolation representation gap, not merely a testing concern**: a query or write path that infers scope only by following these untyped references, without a rigorously designed and independently-verified dual-entity organization-match check on every access path, is exactly the shape of defect `VV-AUDIT-WP-05`'s own F-02 and `TD-113` already found elsewhere in this repository — `CLAUDE.md §19.8.5`-class, non-deferrable, not something a `PLATFORM_ADMIN` gate on top of it resolves. Gating the caller does not answer whether the underlying rows can be correctly scoped to one tenant at all.

| Field | Content |
|---|---|
| **BA ID** | BA-05 |
| **Business Capability** | C-092 Knowledge Graph Management |
| **Business Objective** | Resolve canonical entities and create semantic relationships in the Knowledge Graph's own relational registry, triggered by governed business outcomes. |
| **Business Intent** | Realize `RTA-001 §12.7`'s Graph Synchronization Pipeline: Entity Resolution → Relationship Resolution → Semantic Enrichment → Ontology Validation → Graph Update, against `enterprise_knowledge_graph_registry`. |
| **Participating Personas** | `RTA-001 §12`'s own model is asynchronous/system-triggered, not a named human persona for the synchronization act itself (§12.3: "shall never delay Business Activity completion"). A read/query surface may have a persona; none named by any governing document. **Not the operative question for this BA** — see Authorization requirements below. |
| **Business Objects** | `enterprise_knowledge_graph_registry` row(s) (AMD-012) — the relational index/audit trail, not the Neo4j graph itself (§5.5). **Carries no `organization_id` column and no typed foreign key on either `source_entity_id` or `target_entity_id` — only polymorphic type/id pairs.** Tenant ownership is transitively inferable from the referenced entities only, never schema-enforced on this table itself (amendment, above). |
| **Business Rules** | Triggered by a Domain Event following a governed outcome (e.g. BA-04's own Knowledge Asset `ACCEPTED` transition), per `§12.7`/`§12.14` — never by direct invocation of this BA in place of the originating Business Activity; Entity Resolution must resolve against the named entity list (`§12.8`: Organizations, People, Metrics, Risks, etc.); Relationship Resolution restricted to the named relationship-kind vocabulary (`§12.9`: Owns/Reports To/Depends On/etc.), validated against `ONT-001`'s own six relationship kinds (Ontology Validation, `§12.7`); `graph_engine_reference` remains NULL — no live Neo4j write (§5.5). |
| **APIs/services required** | No caller-facing establish endpoint — an event-triggered synchronization service (`RTA-001 §12.14`: "triggered by Domain Events rather than direct Business Activity invocation"). A read/query endpoint (`GET /knowledge-graph/relationships`) may be added for observability, per `§12.13`; not mandatory for this BA's own minimum scope. **Neither path may be implemented until the tenant-boundary representation decision below is made**, regardless of which persona or gate would front it. |
| **Frontend/UX required** | None mandatory for the synchronization act itself (a backend/system Business Activity, per `§12.3`'s own asynchronous design) — an optional read-only graph/relationship view is a Plan B candidate, not required to satisfy this BA's own vertical slice (§9's own explicit-exception discussion). |
| **Authorization requirements** | **Classification C — STOP.** This is not an authorization-persona gap `PLATFORM_ADMIN` closes. The underlying question is whether `enterprise_knowledge_graph_registry` rows can be correctly scoped to a single Organization at all, given the schema finding above. `PLATFORM_ADMIN`-gating a manual/read endpoint would restrict *who* may call it without resolving *whether the data returned is safely tenant-scoped* — the two are independent questions, and only the second is genuinely unresolved here. **Do not treat `PLATFORM_ADMIN` as sufficient to close this finding.** |
| **Evidence/provenance requirements** | `explainability_reference`/`confidence_score` columns already exist on `enterprise_knowledge_graph_registry` (AMD-012) — populated from the triggering Business Activity's own Evidence/Confidence, reused not reinvented. |
| **Dependencies** | Fires from BA-04 (Knowledge Asset acceptance) and, per `§12.4`'s own generic design, any other governed Business Activity's Domain Event — this BA's own minimum scope wires the BA-04 trigger only; broader cross-capability wiring is future work, disclosed not built here. **Additionally and newly blocking: the Repository Owner tenant-boundary decision above (§11).** |
| **Acceptance criteria** | A `BA-04` Knowledge Asset reaching `ACCEPTED` produces a corresponding `enterprise_knowledge_graph_registry` entry with resolved entity/relationship type, `graph_engine_reference` NULL, without delaying the triggering Business Activity's own completion (`§12.3`). **Not achievable, and not to be attempted, until the tenant-boundary representation decision is made** — no acceptance criterion here supersedes that gate. |
| **Testing requirements** | Unit (synchronization is asynchronous — triggering BA completes before graph update; Entity/Relationship Resolution restricted to the named vocabularies; Ontology Validation rejects an unrecognized relationship kind) + Mandatory Tenant-Isolation Test Checklist. **This checklist cannot be satisfied as a mechanical exercise for this BA specifically** — "a graph entry from Organization A never resolves against or is visible to Organization B" presupposes a tenant-scoping mechanism that does not yet exist on this table; writing the test is not possible until the Repository Owner's own tenant-boundary decision (§11) supplies one. |
| **Authoritative architecture references** | `RTA-001 §12` (full — `§12.3`, `§12.4`, `§12.7`–`§12.9`, `§12.13`–`§12.14`); `Master_Technical_Architecture.md` AMD-012 (`enterprise_knowledge_graph_registry`, line 3147 — re-verified for this amendment); `ONT-001`. |

### Cross-cutting

- **Migrations:** new Alembic migrations extending the appropriate existing service's chain (`AuthService` for `discovery_provider_registry`/`unclassified_intelligence_registry`/`customer_metric_registry`-adjacent tables if hosted there, or `AIService` if hosted there — **hosting-service determination is an open item**, §8) — exact table shape mirrors the LOCKED `Master_Technical_Architecture.md` definitions verbatim, per `CLAUDE.md §12` (no parallel schema).
- **Authorization:** interim `PLATFORM_ADMIN`-only across **BA-01 through BA-04** (§10) — new Technical Debt, not a WP-13 mechanism reuse (no `domain_id` anchor exists on any of the five tables). **BA-05 is excluded from this line** — its own gap is not resolved by `PLATFORM_ADMIN` or any authorization gate (§11, BA-05's own table above).

---

## 7. Business Object Eligibility Analysis (`CMD-001 §26.3a`)

Unlike `IRA-012`'s own open question for Conversation/Interaction (no LOCKED physical schema existed at all), **every Business Object this IRA proposes already has a LOCKED physical schema** in `Master_Technical_Architecture.md` — `discovery_provider_registry` (AMD-013), `unclassified_intelligence_registry` (AMD-005), `customer_metric_registry`/`metric_registry` (AMD-004 rework), `knowledge_asset_registry`/`enterprise_knowledge_graph_registry` (AMD-012). No `CMD-001 §26.3a` eligibility determination is required — these are not candidate *new* canonical objects; they are already-canonical, already-registered objects this Work Package is the first to populate. This mirrors `IRA-011 §6`'s own finding (eligibility analysis unnecessary against already-LOCKED tables), not `IRA-012`'s own open item.

---

## 8. CDE/BQ Evolution & Enrichment Obligation

Per `CLAUDE.md §21`'s own governing instruction (currently an uncommitted `CLAUDE.md` diff, not staged or modified by this IRA per explicit instruction, but constitutionally active per the system's own override framing): every completed Business Activity is an opportunity to enrich the Enterprise Operating System, and every newly discovered/approved CDE or Business Question SHALL be evaluated for whether it enables a new capability, recommendation, KPI, dashboard, agent, or workflow — with the authoritative owning document updated within the same Work Package where an existing owner is found, or a STOP-and-report where none exists.

**Not yet exercised — no CDE or Business Question has been approved by any WP-14 Business Activity, since none is implemented.** This obligation is recorded here as a **standing gate on BA-03's own Business Activity Completion** (`CLAUDE.md §19.7`), not deferred or silently dropped: every `NEW_CDE_CREATED` or `PROMOTED_CONVERGENCE` outcome BA-03 produces, once implemented, SHALL be evaluated at that time against `GRC-001` (KPI, C-110), `SD-001`/`DS-001` (dashboard/widget marketplace, already engineered per `EIX-DISCOVERY.md §6` row 5), `RTA-001 §13.9a` (Tool Registry, for agent-consumability), and `CAP-001` (new capability) — enriching whichever of these already-existing owners applies, never inventing a new one, consistent with `EIX-DISCOVERY.md`'s own independent finding that no CDE/BQ-adjacent construct in this repository currently lacks a constitutional owner.

---

## 9. PLAN B — Enterprise Experience Implementation

Derived only from `SD-001`, `PE-001`, `DS-001`, `HISTORICAL-SCREEN-REALIZATION-MATRIX.md`'s own `F1`/`I1` precedents — per `CLAUDE.md §20.3`, this plan identifies what is built; it does not itself design a screen.

- **What the user sees:** an admin/governance surface — establish a Discovery Provider configuration (BA-01); register or review a candidate fact (BA-02); a resolution queue with confidence scoring, directly precedented by `I1`'s own "Unclassified-item queue with governance routing... Overall confidence scoring" (BA-03); a Knowledge Asset establish/status view (BA-04). BA-05 is system-triggered, no mandatory screen (§6, BA-05's own row).
- **Screens realized:** **no free nav slot exists for `C-090`/`C-091`/`C-092`** — the historically-associated `enterprise-intelligence` slot is already occupied by `WP-11`'s own `EnterpriseSearchScreen` (confirmed by direct read of `admin-navigation.ts`, §3). A new nav entry, or an extension of the existing `enterprise-intelligence` administration surface into a multi-tab/multi-section screen, is **not decided by this IRA** — determined at implementation time against `SD-001-115`'s own confirmation that nav placement remains each capability's own CRB/ERB decision, per `PE-001 §13.5`'s existing delegation (same deferral `IRA-012 §7` already used for `C-094`).
- **Design System components used:** existing `Form`, `Card`, `Button`, `Spinner`, `Table` (reused, same set every prior IRA has used); Progressive Disclosure/Evidence Panel (`SD-001-021`/`SD-001-020`) — now real, first built by `WP-12` — reused, not rebuilt, for BA-03's own Evidence/Confidence display.
- **States implemented (`CLAUDE.md §20.6`):** loading, empty (no candidates pending resolution — an honest, disclosed empty state, directly relevant to BA-03's own queue), validation, error, confirmation.

---

## 10. Authorization Requirements & WP-13 Dependency Verification

**Verified, per instruction #11:** WP-13's Authorization Runtime Engine integration is real, committed, and available (`Backend/Runtime/AuthorizationEngine`, `AuthService/dependencies.py::enforce_domain_permission`). **Not recreated here.** **Not applicable to any WP-14 resource:** `discovery_provider_registry`, `unclassified_intelligence_registry`, `customer_metric_registry`, `knowledge_asset_registry`, and `enterprise_knowledge_graph_registry` are each `organization_id`-scoped only — none carries a `domain_id` column (independently verified against each table's own `CREATE TABLE`/`ALTER TABLE` statement, §2). This is the identical structural absence `TD-025` (Runtime Assignment Policy) already documents for an unrelated resource in WP-13's own closed assessment.

**Resulting disposition for BA-01 through BA-04:** the absence of a `domain_id` column establishes only that WP-13's own mechanism has no attachment point — it does not, by itself, establish that `PLATFORM_ADMIN` is the constitutionally correct gate. That second conclusion rests on independent evidence: `routers/configuration.py::establish_configuration` (`WP-10`, `CLOSED — CERTIFIED`, two independent review gates) and `AIService/routers/search.py::register_content` (`WP-11`, `CLOSED — CERTIFIED`) each govern the identical resource shape — Organization-scoped only, no Domain anchor, a write/establish action — and each was independently, already certified using exactly this interim gate, with the `WP-10` endpoint's own docstring stating verbatim: *"Gated by PLATFORM_ADMIN — no Tenant Admin authority model exists yet."* This is a reused, already-adjudicated precedent, not a fresh assumption. Every WP-14 Business Activity that matches this resource shape therefore gates on the interim `PLATFORM_ADMIN`-only pattern, the same starting posture every Work Package before WP-13's own retrofit used — not a regression, not an invented mechanism. This SHALL be recorded as new Technical Debt at implementation time (§12), following the exact `TD-021`-class disclosure discipline this repository has used at every prior Work Package's own inception.

**BA-05 is explicitly excluded from this disposition.** A focused authorization review (this amendment) found that `enterprise_knowledge_graph_registry` — unlike `discovery_provider_registry`, `unclassified_intelligence_registry`, `customer_metric_registry`, and `knowledge_asset_registry` — carries no `organization_id` column at all, not merely no `domain_id`. No precedent cited above (or found anywhere in this repository) certifies an authorization pattern for a resource with no tenant-boundary column whatsoever; `PLATFORM_ADMIN` governs *who* may call an endpoint, not *whether the underlying rows are safely scoped to one tenant*, and cannot substitute for the missing answer to the second question. See §6 BA-05's own amended table and §11.

---

## 11. Readiness Decision

**Amended following a focused authorization review of BA-01 through BA-05 (this pass).** The five Business Activities in §6 no longer share one uniform readiness conclusion:

**BA-01 through BA-04 — READY**, with two open items requiring resolution before Technical Design (not blocking, per the same disclosure discipline `IRA-012 §6`/§8 already established):

1. **Convergence-matching algorithm (§6, BA-03):** Binding 3 names the business rule ("materially identical" CDE recurrence across independent customers triggers a promotion signal) but no document specifies the actual cross-tenant comparison mechanism. Technical Design must determine this — not resolved, and not invented, by this IRA.
2. **Hosting service (§6, Cross-cutting):** whether the five new tables are hosted in `AuthService` or `AIService` (or a new service) is not decided by any governing document surveyed. `AIService` is the more direct precedent (already hosts `WP-11`/`WP-12`'s own AI-adjacent registries); `AuthService` already hosts the tenant/organization anchor these tables reference. A Technical Design determination, not an architecture question.

No constitutional blocker exists for BA-01–04's own in-scope portion. `RTA-001 §12`, `Complete_Blueprint.md §5.0c`, and `EIA-001 §7.2` are each independently re-verified complete and internally consistent for what this scope requires. `ENRICH_EXISTING`/`PROPOSE_NEW_BUSINESS_QUESTION`, Interpretation, Intelligence Evaluation, live Discovery Provider connectors, and the live Neo4j Aura write are each excluded for a distinct, disclosed, evidence-grounded reason (§5.6), not a blanket exclusion. Their own `PLATFORM_ADMIN` interim gate is justified by direct, already-certified repository precedent, not merely by the absence of a `domain_id` column (§10) — the distinction matters, and is why BA-05 below reaches a different conclusion from the same starting observation ("no `domain_id`").

**BA-05 — Classification C — STOP. Not implementation-ready; a distinct, unresolved readiness item, not a Technical Design open item like the two above.**

`enterprise_knowledge_graph_registry`'s own LOCKED schema carries no `organization_id` column and no typed foreign key on either `source_entity_id` or `target_entity_id` — only untyped polymorphic references (§6, BA-05's own amended table). Tenant ownership is transitively inferable from the referenced entities only, never schema-enforced on this table itself. This is a `CLAUDE.md §19.8.5`-class tenant-isolation representation gap, not an authorization-persona gap: **`PLATFORM_ADMIN` does not resolve it** — gating who may call an endpoint says nothing about whether the rows an endpoint returns or writes are safely scoped to one tenant. BA-05 SHALL NOT proceed to Technical Design or implementation until the Repository Owner determines how `enterprise_knowledge_graph_registry`'s own tenant boundary is represented and enforced — most plausibly a specified, mandatory dual-entity organization-match verification rule (confirming `source_entity_id`'s and `target_entity_id`'s own owning rows share the caller's own `organization_id` before any read or write), but the specific mechanism is a Repository Owner/architecture determination this IRA does not make. This finding does not affect BA-01 through BA-04's own independent readiness (§6, no BA-05 dependency exists for any of them).

---

## 12. Anticipated Technical Debt

- **TD-candidate-I** (Low, `TD-021`-class): interim `PLATFORM_ADMIN`-only gate across **BA-01 through BA-04** — no `domain_id` anchor exists on any of these four resources for WP-13's own mechanism to attach to (§10); no `PE-001-C090`/`091`/`092` exists to name a persona either. Same root cause and same severity class as every prior Work Package's own inception-time entry.
- **BA-05's own tenant-isolation representation gap (§6, §11) is deliberately NOT listed as an ordinary TD-candidate here** — per `CLAUDE.md §19.8.5`, tenant-isolation defects SHALL NOT be deferred as ordinary Technical Debt. It is a blocking, unresolved readiness item (§11), to be recorded (if the Repository Owner's own eventual decision leaves any residual, non-blocking aspect open) only after that decision is made, not before.
- **TD-candidate-J** (Medium): convergence cross-tenant matching algorithm undetermined (§11 item 1) — Binding 3 names the rule, not the mechanism.
- **TD-candidate-K** (Low): live Discovery Provider connector protocols remain unbuilt for all 30 `provider_type` values — same disclosed gap `WP-11`'s own IRA already carried forward, still open, not this Work Package's obligation to close in full (BA-01 builds configuration only).
- **TD-candidate-L** (Low): live Neo4j Aura synchronization remains unbuilt — `graph_engine_reference` stays NULL platform-wide; `enterprise_knowledge_graph_registry` is real and populated, the traversable graph itself is not (§5.5, `SE-025`'s own precedent).
- **TD-candidate-M** (Low): the EIA-001-to-CDE bridge (whether/how a Knowledge Asset and a resolved Convergence candidate ever relate) remains undocumented, deliberately not invented by this IRA (§5.4) — a future architecture question, not an implementation oversight.

(Final Technical Debt IDs assigned at implementation time, per `CLAUDE.md §19.8.2`.)

---

## 13. Testing Strategy

Per `IMP-001 §11` and `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist: **four of the five tables** (`discovery_provider_registry`, `unclassified_intelligence_registry`, `customer_metric_registry`, `knowledge_asset_registry`) carry a direct `organization_id` tenant boundary; `enterprise_knowledge_graph_registry` (BA-05) does not (§6, §11 — amended finding). BA-01 through BA-04's own test suites SHALL each include, as a submission gate: (a) at least one test seeding two distinct, unrelated Organizations with no shared row; (b) at least one test confirming a caller in one Organization cannot retrieve or infer another Organization's own Discovery Provider, candidate, CDE resolution, or Knowledge Asset; (c) an explicit probe of whether a caller-supplied (not claims-derived) foreign identifier is accepted by any id-scoped endpoint — if accepted, the endpoint SHALL be gated before submission, not left for a future audit to discover. In addition: BA-03's own Semantic Matching path tested to confirm it is genuinely invoked (not bypassed) before any `NEW_CDE_CREATED` outcome persists. **BA-05 is excluded from this testing strategy until its own tenant-boundary representation is decided (§11)** — a Mandatory Tenant-Isolation Test Checklist cannot be meaningfully written against a table with no tenant-scoping mechanism to test; writing one prematurely would create false assurance, not real verification. Full relevant service regression suite re-run before closure of each in-scope Business Activity, per `CLAUDE.md §19.7`.

---

## 14. Entry Criteria

This IRA itself is the entry-criteria gate for chartering. Satisfied for **BA-01 through BA-04**: governing constitutional documents reviewed in full (`EIA-001`, `RTA-001 §12`/`§13.9c`, `Complete_Blueprint.md §5.0c`, `Master_Technical_Architecture.md`'s own physical schema, `SD-002 §§3–6`, `ONT-001`), existing assets discovered (§3–4), Gap Analysis complete including the three `§21.3` reviews (§5a–5c), no constitutional blocker for the in-scope portion (§11), Business Object eligibility confirmed unnecessary (§7, already-LOCKED schema). **Not yet satisfied for BA-01–04, required before Technical Design:** the two open items in §11 (convergence-matching algorithm; hosting service). **Not satisfied for BA-05, and not a Technical Design-phase item:** the tenant-isolation representation gap (§6, §11) is an entry-criteria blocker — BA-05 does not clear this IRA's own entry gate at all until the Repository Owner's decision is made.

## 15. Exit Criteria

Per `CLAUDE.md §19.7`/`§19.7b`/`§20.7`/`§21`, applied to the scope in §5.7/§11: **BA-01 through BA-04** Implementation Complete; Independent Certification; V&V Audit (including mandatory tenant-isolation verification per `§21.4`); Release Readiness Audit; end-to-end demonstrability for the in-scope facets only (a persona can configure a Discovery Provider, register a candidate fact, see it resolved with real Evidence/Confidence, and see a resulting Knowledge Asset — with live connectors honestly absent, not stubbed as present). **BA-05 is excluded from this exit-criteria sequence until the Repository Owner's own tenant-boundary decision (§11) is made and a corresponding IRA-014 amendment (or successor document) restores it to READY.** Per `§21.5`, one Repository Owner authorization executes a Work Package's own in-scope Business Activities — BA-05's own later authorization, once unblocked, is not assumed to be automatic or bundled with BA-01–04's own authorization.

---

## 16. Self-Review (pre-finalization, per instruction #17)

- **Missing responsibility?** None found — all three chartered capabilities (`C-090`/`091`/`092`) and every explicitly-named Convergence element (candidate intake, Semantic Matching, convergence tracking, Governance Manager decision, Evidence binding, Confidence evidence-quality factor, Graph synchronization) map to at least one BA (§5.7).
- **Duplicated ownership?** None — each BA's own Business Object is already singly-owned by an existing LOCKED table (§7); no second document or table claims the same responsibility.
- **Over-engineering?** Reconsidered and narrowed twice during drafting: (a) considered a sixth BA for convergence *promotion* (Aurex-Admin-only Global-CDE decision) as distinct from resolution — rejected, since `Binding 3`'s own text frames it as a later, separately-triggered review, not part of BA-03's own minimum scope, and no immediate business need is demonstrated for building it now; (b) considered folding BA-05 into BA-03 as purely cross-cutting — rejected, since `C-092` is one of the three explicitly chartered capabilities requiring its own vertical slice (`CLAUDE.md §20.3`), and Entity/Relationship Resolution is real, distinct engineering work, not a trivial side-effect.
- **Unnecessary Business Activities?** None — five BAs against three capabilities plus one cross-cutting Convergence core is proportionate (`WP-11`/`WP-12` each needed three for one capability apiece).
- **Incorrect architectural ownership?** Checked explicitly: Knowledge Asset (BA-04) kept independent of CDE resolution (BA-03) specifically because no document joins them (§5.4) — the one place this IRA could most easily have invented a bridge, and did not.
- **Backend-only scope accidentally introduced?** Checked against `CLAUDE.md §20.3`/§20.4 — BA-01 through BA-04 each specify Frontend/UX requirements (§6); BA-05 is the one exception, explicitly justified by `RTA-001 §12.3`'s own asynchronous, system-triggered design (not a convenience exclusion) — the same class of evidence-based backend-only justification `§20.3` itself requires before excluding a vertical slice.
- **Any implementation detail incorrectly elevated into architecture?** Checked — API endpoint shapes (§6) are stated as illustrative, not fixed; exact request/response schemas, the CMS-Design-time hosting-service decision (§11), and the convergence-matching algorithm (§11) are all explicitly left open for Technical Design, not decided here.

---

## 17. Repository-Owner Authorization

**IRA Acceptance: Not yet granted — awaiting Repository Owner review**, including explicit resolution of the two open items this IRA surfaces for BA-01–04 (§11: convergence-matching algorithm; hosting service) **and the separate, blocking BA-05 tenant-boundary decision (§11)**. Per the two-step chartering-then-authorization precedent `WP-10`/`WP-11`/`WP-12` each established, a separate, future "WP-14 Implementation Authorization" instruction remains required before BA-01 implementation begins.

**BA-01 through BA-04 — Classification B, permitted to proceed on the existing interim `PLATFORM_ADMIN` pattern once authorized**, with `WP-10`'s own `establish_configuration` and `WP-11`'s own `register_content` retained explicitly as the governing precedents (§10) — not a fresh interim decision this IRA invents, an application of two already-certified ones.

**BA-05 — Classification C, blocked**, pending the Repository Owner's own determination of how `enterprise_knowledge_graph_registry`'s tenant boundary is represented and enforced (§6, §11). BA-05 SHALL NOT be scheduled for Technical Design or implementation as part of any "WP-14 Implementation Authorization" instruction that does not separately address this finding — bundling it with BA-01–04's own authorization would authorize implementation of a Business Activity this IRA does not certify as ready.

**Recommended starting Business Activity: BA-01 — Establish Discovery Provider Configuration.**

**Why BA-01, not BA-02 (candidate intake), despite BA-02 having zero technical dependency on BA-01 either (independently verified, §6):** every prior Work Package in this repository — including the two most directly cited as WP-14's own precedent, `WP-11` and `WP-12` — began with a pure configuration/establishment Business Activity, not a content- or data-bearing one, and only reached data registration later (`WP-11 BA-03`, third in sequence). BA-02 touches `unclassified_intelligence_registry`, the single table this Work Package's own two independently-owned meta-models (`EIA-001` and `SD-002`/`Complete_Blueprint.md`) meet at — the most architecturally sensitive point in the whole chartered scope (§5.4's own disclosed non-bridge). Starting there first, ahead of the lowest-risk, most-precedented configuration shape, would front-load risk into the part of the scope requiring the most care, for no technical necessity. BA-01 carries the same risk profile as every prior Work Package's own proven first Business Activity: a tenant-scoped configuration record against an already-LOCKED table, zero external dependency, immediately demonstrable end to end.

---

*End of IRA-014. No Business Activity code, API, database migration, or architecture change has been implemented or authorized by this document.*
