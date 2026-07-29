# Master Data Population Specification (MDP-001)
### Version 1.2 — GOLD STANDARD (Supersedes v1.1)

**Status:** LOCKED
**Purpose:** Execution-level instructions for Claude Code to populate Aurex's platform-seed master data tables at build time, reading directly from the 23 Domain CILs, 7 Industry Extension Packs, and the locked architecture documents (SD-001 v2.0, SD-002 v2.0, SD-003 v2.0, URA-001 v2.1, ERG-001 v2.0).
**Not this document's job:** CMD-001 defines what a table *is* and how it's classified. The Technical Architecture defines the physical schema. This document defines what *data* goes in, from where, and how — the layer CMD-001 and the Technical Architecture deliberately don't cover.
**Every mapping below is verified against the actual locked Technical Architecture schema, not assumed from an earlier unverified table list.**

---

## Changelog from v1.0

v1.0's Critical Correction section checked only 9 of the 40 candidate tables, and used a single failure mode (NOT NULL constraint) that missed a second, equally real failure mode: tables whose schema is nullable but whose actual *purpose* is to record something that already happened (a decision, an anomaly, a scored relationship) — seeding these would fabricate events that never occurred. v1.1 re-checked all 40 tables individually against this two-part test, corrected one factual error from the prior pass (`executive_insight_registry` was wrongly read as having no `organization_id`; it has `NOT NULL`), and closed the arithmetic: 22 clean + 2 conditional + 16 excluded = 40. A second schema defect was also found while validating the BQ-CDE relationship: `kpi_metric_mapping.organization_id` is `NOT NULL`, blocking the one CIL relationship (`04_BQ_CDE_Mapping`) this document had not yet addressed. Both defects (this one and `role_view_configuration`'s deprecated FK) are flagged for a schema fix, not worked around at the data layer.

## Changelog from v1.1

AMD-014 (Master Technical Architecture v6.9) added `domain_registry` — a platform-seeded, tenant-extensible reference/master-data table for Domain (URA-001 §4), closing a completion gap that left `domain_permission_registry.domain_id` referencing no real table. Added as table #41 below (row 41, Critical Correction table) and Section B2a. Arithmetic updated: 23 clean + 2 conditional + 16 excluded = 41.

---

## Critical Correction Before Any Population Work Begins

*(v1.1 — this section replaces two earlier, partially-incorrect passes. The first pass checked 9 tables and missed several NOT NULL constraints. The second pass corrected some of those but introduced a new error (`executive_insight_registry` was wrongly read as having no `organization_id` — it has `NOT NULL`) and never closed the arithmetic. This version is the complete, individually-verified pass across all 40 originally-claimed tables, cross-checked so the count actually closes: 24 + 16 = 40.)*

**Every one of the 40 originally-claimed "Platform Seed" tables was checked individually against its actual `CREATE TABLE` statement.** Two failure modes were found, not one:

1. **Constraint-blocked** — the table has `organization_id NOT NULL`, or a foreign key into tenant-runtime data (a real membership, a real user, a real org hierarchy) that cannot exist before a tenant is onboarded.
2. **Content-blocked** — the schema itself is nullable/global-safe, but the table's actual *purpose* is to record something that happened (a decision made, an anomaly detected, a relationship scored). Seeding these with invented content would mean fabricating an event that never occurred — a false audit-trail entry, not master data. This second failure mode was missed in earlier passes, which checked only the NOT NULL constraint and not what the table is semantically for.

| # | Table | Verdict | Reason |
|---|---|---|---|
| 1 | `industry_taxonomy_registry` | ✅ Seed | No org_id |
| 2 | `traversal_policy_registry` | ✅ Seed | No org_id |
| 3 | `enterprise_view_registry` | ✅ Seed | org_id nullable, global templates only |
| 4 | `consolidation_determination` | ❌ Excluded | FK to tenant-specific `organization_hierarchy` |
| 5 | `system_role_registry` | ✅ Seed | No org_id — 5 fixed rows |
| 6 | `business_role_registry` | ✅ Seed | org_id nullable, `NULL = global` per its own column comment |
| 7 | `domain_permission_registry` | ❌ Excluded | FK to `membership_registry` |
| 8 | `approval_authority_registry` | ✅ Seed | org_id nullable, global templates only |
| 9 | `entitlement_registry` | ✅ Seed | org_id nullable, global catalog only |
| 10 | `license_registry` | ❌ Excluded | FK to `membership_registry` |
| 11 | `framework_registry` | ✅ Seed | No org_id |
| 12 | `regulatory_requirement_registry` | ✅ Seed | No org_id |
| 13 | `material_topic_registry` | ✅ Seed | No org_id |
| 14 | `metric_registry` | ✅ Seed | No org_id |
| 15 | `kpi_registry` | ✅ Seed | No org_id |
| 16 | `benchmark_registry` | ✅ Seed | No org_id |
| 17 | `financial_metric_registry` | ✅ Seed | No org_id |
| 18 | `confidence_scoring_registry` | ✅ Seed | No org_id |
| 19 | `workflow_registry` | ✅ Seed | No org_id |
| 20 | `event_registry` | ❌ Excluded | `organization_id NOT NULL` |
| 21 | `notification_template_registry` | ✅ Seed | No org_id |
| 22 | `llm_prompt_registry` | ⚠️ Seed-eligible | Schema permits, but **no content source exists** — see note below |
| 23 | `predictive_model_registry` | ✅ Seed | No org_id, catalog of model types only |
| 24 | `anomaly_detection_registry` | ❌ Excluded | `organization_id NOT NULL` |
| 25 | `recommendation_registry` | ❌ Excluded | FK into operational `executive_insight_registry` |
| 26 | `trust_scoring_registry` | ❌ Excluded | `organization_id NOT NULL` |
| 27 | `enterprise_knowledge_graph_registry` | ❌ Excluded | No org_id column, but stores real graph edges between real entities — no legitimate content pre-operation |
| 28 | `architecture_version_registry` | ✅ Seed | No org_id — one row for this locked build |
| 29 | `architecture_health_registry` | ❌ Excluded | No org_id column, but content is computed at runtime |
| 30 | `screen_registry` | ✅ Seed | No org_id |
| 31 | `enterprise_configuration_registry` | ✅ Seed | No org_id, genuine global default values |
| 32 | `role_view_configuration` | ⚠️ Seed-eligible | org_id nullable, but **`role_id` FK points to deprecated `role_registry`** — blocked until repointed to `business_role_registry` |
| 33 | `api_credential_registry` | ✅ Seed | org_id nullable — internal-service rows only, never customer credentials |
| 34 | `customer_domain_registry` | ❌ Excluded | `organization_id NOT NULL` |
| 35 | `audit_package_registry` | ❌ Excluded | org_id nullable, but `requested_by_user_id` makes the content inherently post-onboarding |
| 36 | `orchestration_trigger_registry` | ✅ Seed | No org_id — global trigger definitions only |
| 37 | `cross_domain_relationship_registry` | ❌ Excluded | No org_id column, but stores real scored relationships — no legitimate content pre-operation |
| 38 | `executive_insight_registry` | ❌ Excluded | `organization_id NOT NULL` |
| 39 | `strategic_intent_registry` | ❌ Excluded | org_id nullable, but content is inherently one real company's board/CEO statement — no legitimate global row |
| 40 | `decision_traceability_registry` | ❌ Excluded | `organization_id NOT NULL` |
| 41 | `domain_registry` | ✅ Seed | org_id nullable, `NULL = platform-default` per AMD-014/URA-001-43, mirrors `business_role_registry`'s own convention |

**Verified count: 23 tables cleanly seedable today, 2 conditionally seedable (`llm_prompt_registry` pending a content source, `role_view_configuration` pending the FK fix), 16 excluded. 23 + 2 + 16 = 41 — arithmetic closes.**

**A second schema defect, found while validating the BQ-CDE relationship (added as Section A2a below): `kpi_metric_mapping.organization_id` is `NOT NULL`.** This table is the junction between `kpi_registry` (BQs) and `metric_registry` (CDEs) — both of which are correctly global, seedable tables. But the mapping *between* them cannot be seeded as global rows, because the column forces a real organization. This means the CIL's canonical BQ→CDE relationships (e.g., "What was total cost of delivery?" mapping to Transportation/Packaging/Distribution Cost — true for every tenant, per One Truth Multiple Views) cannot be represented once, globally — every tenant would have to independently recreate the same universal mapping. **This is a schema-level fix required before Section A2a can execute, flagged the same way as the `role_view_configuration` FK block — not worked around at the data layer.**

---

## Global Execution Rules (apply to every table below)

1. **Source precedence, when two sources could inform the same field:** CIL > Architecture Document > International Standard > Platform Default. If a CIL and an architecture document both describe the same entity, the CIL wins for business content (metrics, KPIs, materiality); the architecture document wins for structural/behavioral fields (permission levels, event codes).
2. **Language purge is enforced at population time, not assumed pre-clean.** Every text field sourced from a CIL or document must pass through the binding substitution table before insert (ESG Score → Business Resilience Index, Carbon Emissions → Energy Cost & Transition Exposure, Net Zero → Strategic Commitment, Green Bond → Financial Obligation with Performance Condition, Sustainability Report → Intelligence Foundation Document, Scope 1/2/3 → Direct/Procurement/Value Chain Cost, Diversity Metrics → Talent Competitiveness, CSRD Compliance → Regulatory Cost Exposure). This is a mandatory transformation step, run and logged, not a one-time assumption that source content is already clean.
3. **Global-scope rows carry `organization_id = NULL`** (per business_role_registry's own comment convention: "NULL = global"). Never populate a placeholder/dummy organization_id to satisfy a NOT NULL constraint — if a column is NOT NULL and requires a real organization, the table is not in scope for seeding (see the correction above).
4. **IDs are generated, not sourced.** Every `*_id` column uses `gen_random_uuid()` per its column default — population scripts never hardcode UUIDs, so re-runs and environment promotion remain consistent.
5. **`created_at` = population run timestamp, in UTC, for every row.** `active_flag = TRUE` for every seeded row unless the table's own business logic requires otherwise (e.g., a deprecated framework version seeded for historical reference).
6. **Idempotency is mandatory.** Every population script must be safely re-runnable: match on the natural key (`*_code` or `*_name` + scope) before insert; update in place if the source content changed, never insert a duplicate row.
7. **Provenance is recorded, not implied.** Every populated row's source (which CIL, which document, which section/sheet) must be logged in the population run's audit output — this is what makes the seed data itself explainable per L11, not just the platform's runtime behavior.

---

## A. CIL-Sourced Tables (7 tables)

Source: all 23 Domain CIL files (17-sheet Gold Standard format) plus 7 Industry Extension Pack files (12-sheet format).

### A1. `metric_registry`
| Field | Source | Rule |
|---|---|---|
| `metric_name` | CIL sheet `03_CDE_Registry`, column "CDE Name" | Direct copy, post-purge |
| `metric_code` | Derived: `{Domain Prefix}-{CDE ID}` | e.g. `CDE-CR033` from D12 |
| `metric_category` | CIL sheet `01_Intelligence_Areas` mapped to Business Resilience/risk/financial via the IA's stated theme | See Appendix A1 mapping table below |
| `metric_description` | `03_CDE_Registry`, "Domain Ownership Note" (truncated to definition-only sentence) | Post-purge |
| `unit_of_measure` | Inferred from `03_CDE_Registry` "Validation Rule" column (e.g. `TYPE:NUMERIC|MIN:0` → numeric, currency stated → currency) | — |
| `formula_logic` | `03_CDE_Registry`, "Aggregation Rule" column | Direct copy |
| `source_type` | `03_CDE_Registry`, "Source System" column, mapped to `system`/`manual` | `system` if named platform/ERP; `manual` if evidence-catalog sourced |
| `material_topic_id` | Resolve via `01_Intelligence_Areas` name match against `material_topic_registry` (populate A3 first) | FK must resolve — no orphans |
| `benchmark_enabled_flag` | `TRUE` if a corresponding `benchmark_registry` row exists for the same domain | — |
| `evidence_required_flag` | `TRUE` if `05_Evidence_Catalog` has a matching Reliability ≥ 0.85 entry | — |
| `ai_extractable_flag` | `TRUE` if `08_Extraction_Rules` documents a Discover/Extract pattern for this CDE | — |
| `framework_mapping_json` | `09_Framework_Mapping` + `12_Framework_CDE_Detail`, filtered to this CDE ID | JSON array of `{framework, reference}` |

**Validation:** row count should equal 3,643 (total CDEs across 23 CILs) plus IEP-specific CDEs (110), minus any CDE explicitly marked `Purged`/`Archived` in `00_Freeze_Status`. Every row must resolve `material_topic_id`; zero-orphan check is mandatory before commit.

### A2. `kpi_registry`
Source: `02_BQ_Registry` + `10_Executive_Summary` (for executive priority signal). Mapping follows the same pattern as A1: `kpi_code` derived from BQ ID, `kpi_category` from parent Intelligence Area, `calculation_logic` from the BQ's linked CDE aggregation (via `04_BQ_CDE_Mapping`), `executive_priority_level` from whether the BQ appears in `10_Executive_Summary`'s Sacred-Question rows (1 = present, 0 = absent). **Validation:** row count should equal 827 (BQs across 23 CILs) plus 70 (IEP BQs) = 897.

### A2a. `kpi_metric_mapping` — BQ↔CDE relationships — **BLOCKED pending schema fix**
Source: `04_BQ_CDE_Mapping` sheet, every CIL — one row per (BQ, CDE) pair, each BQ mapping to 3–9 CDEs per the Gold Standard range rule already enforced in every locked CIL. **This table cannot be populated as written**, because `kpi_metric_mapping.organization_id` is `NOT NULL`, forcing every canonical, tenant-independent relationship (true for all tenants, per SD-002-014 One Truth Multiple Views) to be artificially duplicated per organization instead of stored once, globally. **Required schema fix before this section executes:** make `organization_id` nullable on `kpi_metric_mapping`, consistent with `kpi_registry` and `metric_registry` themselves. Once fixed: `contribution_weight` and `formula_sequence` derive from the CIL's aggregation rule ordering; `dependency_type` = `required` for every mapped pair (the Gold Standard range rule already guarantees no optional/orphan mappings survive CIL lock). **Validation:** every `metric_registry` row must resolve to at least one `kpi_metric_mapping` row and vice versa — zero-orphan check, identical in spirit to the CIL's own BQ-CDE range validation.

### A3. `material_topic_registry`
Source: `01_Intelligence_Areas` sheet, one row per Intelligence Area per domain (230 IAs total: 23 domains × 10 IAs each). `financial_materiality_score` and `impact_materiality_score` derive from the IA's stated BIR (Business Intelligence Requirement) criticality language — not invented, mapped from the existing `06_Confidence_Rules` weighting already present in each CIL. `framework_materiality_json` pulls from `09_Framework_Mapping`. **Populate this table before A1/A2**, since both reference it via FK.

### A4. `framework_registry`
Source: the union of every distinct framework named across all 23 CILs' `09_Framework_Mapping` sheets (IFRS, national/regional regulatory frameworks, GRI, ISSB, BRSR, CSRD, TCFD, SASB, and others) plus each IEP's sector-specific framework additions. **Note:** these are real external framework names, legitimately populated as reference data — not a language-purge violation, consistent with the precedent set in Blueprint v2.3's gated Regulatory & Framework Detail Lens. This table is backend reference data a Compliance persona queries; it does not render on an executive screen. `framework_status` defaults to `'confirmed'` for anything appearing in 3+ CILs, `'detected'` otherwise.

### A5. `regulatory_requirement_registry`
Source: `09_Framework_Mapping` + `12_Framework_CDE_Detail`, one row per distinct (framework, requirement) pair. `mandatory_flag` from the CIL's "Mandatory" column. `domain_category` from the owning domain's name.

### A6. `benchmark_registry`
Source: `05_Evidence_Catalog` rows explicitly tagged as external/peer data sources (not internal system-of-record). `benchmark_type` = `sector` if sourced from an IEP; `peer`/`internal` otherwise, per the evidence source's own stated category.

### A7. `industry_taxonomy_registry`
Source: each of the 7 IEP's `01_Sector_Profile` sheet (SASB SICS Sector/Sub-Industry codes) plus each domain CIL's stated industry applicability. `taxonomy_level` = `SECTOR` for the 7 top-level IEP sectors, `SUB_INDUSTRY` for each IEP's named sub-industries (per `source_standard = 'SASB_SICS'`). **Validation:** the `chk_taxonomy_parent_consistency` constraint must pass — every SUB_INDUSTRY row requires a resolved `parent_taxonomy_id` to its SECTOR row; populate sectors first.

---

## B. Identity & Access Tables (URA-001 v2.1-sourced, global scope only)

### B1. `system_role_registry`
Source: URA-001-29, verbatim. Exactly 5 rows: `AUREX_ADMIN`, `CORPORATE_ADMIN`, `USER_ADMIN`, `SECURITY_ADMIN`, `DOMAIN_ADMIN`. Fixed, stable — this table's content will not change based on CIL updates.

### B2. `business_role_registry` (global rows only)
Source: URA-001-30's named examples (CEO, CFO, COO, CHRO, CSO, CISO, Company Secretary, Finance Manager, Plant Head, Board Member) — populate with `organization_id = NULL`. Tenant-specific custom roles (URA-001-38) are created during onboarding, not seeded here.

### B2a. `domain_registry` (platform-default rows only)
Source: URA-001-43, verbatim — 7 platform-default domains: Finance, HR, Risk, Supply Chain, Cyber Security, Legal, Business Resilience. Populate with `organization_id = NULL`, `parent_domain_id = NULL` (top-level rows only; URA-001-44's sub-domain examples — Accounting, Treasury, Taxation under Finance — are illustrative, not a fixed canonical set, so sub-domain rows are a tenant-configuration action, not seeded here). Tenant-added domains (URA-001-43's "organizations may add domains such as Innovation, Manufacturing Excellence, or Investor Relations") are created during onboarding/configuration, not seeded here.

### B3. `approval_authority_registry` (global templates only)
Source: URA-001-41's named examples (Annual Report Approver, Financial Statement Approver, Board Resolution Approver, Policy Approver) with `organization_id = NULL`, `approval_strategy` defaulted per URA-001-42's stated norm for each (SEQUENTIAL for Annual Report Approver, per URA-001-67's worked example).

### B4. `group_registry` (global templates only)
Source: URA-001-57's named examples (Board Committee, Audit Committee, Finance Leadership Team, Risk Committee) as global templates, `organization_id = NULL`. Real tenant groups are created during onboarding.

### B5. `entitlement_registry` (global catalog only)
Source: URA-001-112's named examples (`IFRS_ENABLED`, `AI_DISCOVERY_ENABLED`, `SUPPLIER_PORTAL_ENABLED`) as the entitlement catalog, `organization_id = NULL`. Which entitlements a tenant actually holds is assigned at onboarding, not seeded here.

---

## C. Interaction & Workflow Tables (SD-003/URA-001-sourced)

### C1. `workflow_registry`
Source: URA-001-83's named workflow templates (e.g., Annual Report: Prepare → Finance Review → CFO Signoff → CEO Approval → Board Approval → Publish) plus SD-003 Section 6/7's governed sequences. `workflow_category` from the template's domain. `approval_level_count` counted from the named sequence steps.

### C2. `event_registry` — external-world events only
**Important distinction, already resolved in the Technical Architecture integration:** this table is scoped to external-world events (`event_category`: climate/regulatory/market), per URA-001 v2.1's Part D resolution. **Do not populate this table with URA-001's internal workflow events** (ENTER/APPROVE/ESCALATE) — those belong in `workflow_event_registry` (below), which is a distinct table this document's earlier draft correctly kept separate. Source for this table: `enterprise_view_registry`'s external-factor mappings and the CILs' `05_Evidence_Catalog` rows tagged as market/regulatory event sources.

### C3. `workflow_event_registry`
Source: URA-001-71's named events (ENTER, REVIEW, APPROVE, REJECT, ASSIGN, DELEGATE, ESCALATE, PUBLISH) at `scope_type = 'GLOBAL'`, `organization_id = NULL`. Company- and domain-scoped events (BOARD_APPROVAL, CFO_SIGNOFF) are created during tenant onboarding against this global template set, not seeded as tenant rows here.

### C4. `escalation_policy_registry` (global templates only)
Source: URA-001-94's four strategy types as default templates, `organization_id = NULL`, `max_depth = 5` per URA-001-94a's stated default. Tenant-specific escalation policies are configured during onboarding.

---

## D. Enterprise Structure Tables (ERG-001 v2.0-sourced, global scope only)

### D1. `enterprise_view_registry` (global templates only)
Source: ERG-001-06's explicit statement that no view type is hardcoded — populate only genuinely generic, reusable templates (Legal, Financial, Operating, Management view *shapes*, not tenant content), `organization_id = NULL`. **Do not seed an "ESG View" or any framework-named view** — this is the exact defect ERG-001 v2.0 was built to eliminate; a Regulatory & Resilience Reporting View template is acceptable as one configurable instance, never as a hardcoded named citizen.

### D2. `traversal_policy_registry`
Source: ERG-001-04's named relationship types (OWNS, SUPPORTS, SUPPLIES_TO, JOINT_VENTURE_WITH, etc.) with `propagates_access = FALSE` (NODE_ONLY) by default for every row, per ERG-001-04's stated default — a new relationship type is never access-propagating until a Security Admin explicitly configures otherwise.

---

## E. Screen & Navigation Tables (SD-001 v2.0-sourced, global scope only)

### E1. `screen_registry`
Source: SD-001 v2.0's 39 screens (Blueprint's "39 Screens" framework), Sections 6–8. `screen_layer`: `LAYER_1` for Operational Intelligence screens, `LAYER_2` for the 12 Sacred screens, `LAYER_3` for Exchange & Reporting screens. `is_sacred_12 = TRUE` for exactly 12 rows (enforced by the existing `trg_sacred_12_cap` trigger — population must respect this, not attempt to bypass it). `allows_guided_completion = FALSE` for every Sacred 12 row (enforced by `trg_sacred_12_cap`; population script should set this explicitly rather than rely on the trigger to catch an omission). `journey` from SD-001's Two Journeys framework.

**Validation:** insert order matters — the trigger rejects a 13th `is_sacred_12 = TRUE` row, so populate all 39 rows in one transaction and verify exactly 12 have the flag set before commit.

### E2. `role_view_configuration` (global defaults only)
**Blocked pending the FK fix noted above.** Once `role_id` is repointed to `business_role_registry`, populate default lens assignments per business role (e.g., CFO → `EXECUTIVE` lens) from URA-001 v2.1's persona descriptions.

---

## F. AI & Confidence Infrastructure Tables (Platform Defaults, global scope only)

### F1. `confidence_scoring_registry`
Source: SD-001-011's disclosed confidence formula (Reliability × 0.40 + Freshness × 0.25 + Corroboration × 0.20 + Completeness × 0.15), applied as the `DATA` confidence_type row. Additional rows for `MODEL`, `EVIDENCE`, `NARRATIVE`, `COMPOSITE` types per the same weighting philosophy, thresholds at `green=90/amber=70/red=50` per this table's own column defaults.

### F2. `llm_prompt_registry`
Source: platform default prompt templates (Daily Brief, Board Narrative, Risk Summary, Extraction) — these are engineering artifacts, not CIL-derived; populate from the platform's own prompt engineering specification (outside this document's source set — flag to the engineering team if no such spec exists yet, do not invent prompt content here).

### F3. `predictive_model_registry`
Source: model catalog entries for each domain CIL that has a stated predictive capability (check each CIL's `01_Intelligence_Areas` for forward-looking BIRs). Populate as a catalog of model *types* available, not trained model instances (those are operational).

### F4. `notification_template_registry`
Source: SD-003's notification/attention laws (Section 8) — the five example templates already named in the Technical Architecture's own column comments (Daily Executive Brief, Risk Alert, Score Unlock, Weekly Drip, Breach Alert) as the starting catalog.

### F5. `architecture_version_registry` / `architecture_health_registry` / `enterprise_configuration_registry` / `orchestration_trigger_registry`
These four are platform self-description tables. Seed one row in `architecture_version_registry` representing this locked build (all six documents at their current versions). The other three seed with baseline/default configuration only — do not populate `architecture_health_registry` with scores (those are computed at runtime, operational) or `orchestration_trigger_registry` with tenant-specific triggers (global trigger *definitions* only).

### F6. `api_credential_registry` (internal service credentials only)
Populate only `organization_id = NULL` rows for internal platform services (e.g., the AI orchestration service's own service account). Customer integration credentials are created during onboarding — never seed a customer-facing API key.

---

## G. Explicitly Excluded — Do Not Populate at Seed Time

**The 16 tables verified as constraint- or content-blocked in the Critical Correction table above** (`consolidation_determination`, `domain_permission_registry`, `license_registry`, `event_registry`, `anomaly_detection_registry`, `recommendation_registry`, `trust_scoring_registry`, `enterprise_knowledge_graph_registry`, `architecture_health_registry`, `customer_domain_registry`, `audit_package_registry`, `cross_domain_relationship_registry`, `executive_insight_registry`, `strategic_intent_registry`, `decision_traceability_registry`, and `kpi_metric_mapping` pending its schema fix) — plus the remaining tenant/operational tables from the original 84-table list never claimed as seedable in the first place (`organization_master`, `organization_node`, `organization_hierarchy`, `tenant_registry`, `department_registry`, `person_registry`, `user_registry`, `identity_registry`, `membership_registry`, `membership_business_role`, `membership_approval_authority`, `group_membership`, `runtime_assignment_registry`, `delegation_registry`, `escalation_policy_registry` beyond its global templates, `evidence_registry`, `stakeholder_registry`, `narrative_registry`, `report_registry`, `scenario_registry`, `risk_registry`, `financial_impact_registry`, `competitive_signal_registry`, `competitor_profile_registry`, `market_trend_registry`, `incident_registry`, `resilience_assessment_registry`, `resilience_learning_registry`, `master_entity_registry`, `enterprise_memory_registry`, `decision_outcome_registry`, `recurring_pattern_registry`, `executive_belief_registry`, `memory_evidence_registry`, `customer_metric_registry`, `unclassified_intelligence_registry`, `data_ingestion_registry`, `risk_subscription_registry`) — all correctly excluded. Claude Code must not populate any of these at build time; they populate exclusively through real tenant onboarding and real business operation, per Discover First, Ask Later.

---

## Freeze Statement

This specification governs the initial seed population of **23 cleanly-seedable platform-scoped tables**, verified individually against the actual locked schema (not the earlier unverified 40-table assumption), plus the fixed 5-row `system_role_registry` already counted within that 23 (and, per AMD-014, the 7-row `domain_registry` also counted within that 23). **Two tables are conditionally seedable pending a schema fix, not yet ready:** `role_view_configuration` (repoint `role_id` from deprecated `role_registry` to `business_role_registry`) and `kpi_metric_mapping` (make `organization_id` nullable, so the CIL's canonical BQ↔CDE relationships can be stored once, globally, rather than duplicated per tenant). `llm_prompt_registry` is schema-ready but has no content source yet — flagged for engineering, not fabricated here. Every field mapping above traces to a named CIL sheet, a named principle in SD-001/002/003/URA-001/ERG-001, or is explicitly flagged as needing an engineering-owned source rather than invented.
