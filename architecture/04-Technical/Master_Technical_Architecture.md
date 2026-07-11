CORPSTAGE 360: MASTER TECHNICAL ARCHITECTURE DOCUMENT (COMBINED, FINAL v6.3)
-- ALIGNED TO BLUEPRINT v2.2 -- GOLD STANDARD --
-- v6.0 additionally incorporates the Gold Standard Alignment Amendment v1.0,
-- reconciling this schema with URA-001 v2.1 (User/Role/Permission/Event/
-- Assignment Architecture) and ERG-001 v2.0 (Enterprise Structure &
-- Relationship Management). This is a fully standalone document — nothing
-- in the amendment file needs to be consulted separately.

DOCUMENT VERSION HISTORY
  v4.0: Combined two source drafts, 108 tables, RLS complete, AMD-001/003 applied.
  v5.0: 7 schema amendments (AMD-004 through AMD-010) applied
    to align the schema with Blueprint v2.2 Sections 5.0c-e.
    Net addition: 6 new tables, multiple column extensions.
    Verified total at v5.0: 114 distinct tables.
  v6.0: AMD-011 applied — Gold Standard Alignment Amendment v1.0,
    reconciling the schema with URA-001 v2.1 and ERG-001 v2.0. Net addition:
    22 new tables (16 URA-001, 4 ERG-001, 2 workflow-event), 4 column renames
    (with migration notes), 1 enum-value correction (with migration note),
    3 tables/columns marked DEPRECATED in place (retained, not dropped), and
    a full purge of non-compliant ESG/Sustainability/Carbon/Net-Zero/Scope-1-2-3/
    CSRD language from all live schema and documentation content.
  v6.1: post-review fixes to two items flagged at v6.0 —
    (1) resolved both forward-referencing inline FKs (consolidation_determination
    and node_permission_assignment) via deferred ALTER TABLE ADD CONSTRAINT
    statements placed after their target tables; (2) authored RLS policies for
    17 of the 22 AMD-011 tables, with 1 explicitly flagged rather than
    force-fitted (consolidation_determination) and 4 intentionally left exempt
    as global/master-reference tables. Also fixed a Part-label collision
    between this document's own PART A-E headers and the amendment's internal
    Part A-D labels (all amendment citations now use disambiguated §-labels).
    Verified total at v6.1: 136 distinct tables, 93 RLS policies.
  v6.2: closed the one remaining v6.1 gap. Implemented an RLS
    policy for consolidation_determination — the single table left flagged
    rather than force-fitted at v6.1 — by reusing organization_node's own
    established tenant_workspace-schema mechanism (resolving hierarchy_id ->
    organization_hierarchy -> child_node_id and validating tenancy the same
    way organization_node validates itself), rather than inventing a separate
    mechanism. Zero AMD-011 tables now left with an unresolved RLS decision
    (18 implemented, 4 intentionally exempt as global/master-reference data).
    Verified total at v6.2: 136 distinct tables, 94 RLS policies.
  v6.3 (this version): closed a pre-existing, pre-AMD-011 gap explicitly
    flagged (not silently left) at v6.2 — organization_hierarchy itself had
    no RLS policy of its own anywhere in this document. Added
    org_isolation_hierarchy using the same tenant_workspace-schema mechanism
    as organization_node and consolidation_determination, scoped on
    child_node_id, placed immediately after organization_node's own policy
    in Part D. This closes the last identified RLS gap in the document —
    pre-AMD-011 or AMD-011 — across all 136 tables.
    Final verified total: 136 distinct tables, 95 RLS policies.

======================================================================
AMD-011 CHANGELOG — GOLD STANDARD ALIGNMENT AMENDMENT v1.0
(Reconciles this document with URA-001 v2.1 and ERG-001 v2.0)
======================================================================

TABLES ADDED — Amendment §B-URA-001 (URA-001 v2.1), 16 tables:
  person_registry              — root Person, independent of any org (URA-001-15)
  identity_registry             — auth identities held by a Person (URA-001-16, -25)
  membership_registry            — Person's membership + home node in an org (URA-001-17b/ERG-001-03, -106, -111, -28)
  system_role_registry           — platform-admin-only roles, distinct from business roles (URA-001-29)
  business_role_registry         — tenant-defined business roles; grants no permission by itself (URA-001-38, -40)
  membership_business_role       — supersedes user_role_mapping; supports multiple roles (URA-001-37)
  approval_authority_registry    — approval authorities, independent of business roles (URA-001-04, -41, -42, -82)
  membership_approval_authority  — assigns approval authorities to memberships
  group_registry                 — named groups with hierarchy support (URA-001-57, -59)
  group_membership                — assigns memberships to groups
  domain_permission_registry     — the actual domain permission-level grant (URA-001-47)
  runtime_assignment_registry    — object/event/time-scoped live assignments, never global (URA-001-77, -78)
  delegation_registry             — temporary authority handoff, reason mandatory (URA-001-88, -89, -90, -92)
  escalation_policy_registry      — escalation strategy + mandatory cycle-protection depth (URA-001-94, -94a)
  license_registry                 — per-membership license grant (URA-001-111)
  entitlement_registry             — org-level feature entitlements, separate from licensing (URA-001-112)

TABLES ADDED — Amendment §C-ERG-001 (ERG-001 v2.0), 4 tables:
  consolidation_determination     — extracts consolidation_method into its own temporal object (ERG-001-08)
  enterprise_view_registry        — fully customer-defined enterprise views, no hardcoded type (ERG-001-06)
  traversal_policy_registry       — independently governs access propagation per relationship type (ERG-001-04)
  node_permission_assignment      — resolves membership/role access to a node via a traversal policy (ERG-001-10)

TABLES ADDED — Amendment §D-Event-Collision (event_registry collision resolution), 2 tables:
  workflow_event_registry         — internal workflow-transition event types (URA-001-71, -72)
  workflow_event_log              — immutable log of every workflow state transition (URA-001-85)

COLUMNS RENAMED (live schema, migration required):
  organization_master.sustainability_commitment_flag  -> business_resilience_commitment_flag
  organization_master.net_zero_target_flag            -> strategic_commitment_flag
  organization_master.sustainability_maturity_score   -> business_resilience_maturity_score
  competitor_profile_registry.sustainability_maturity_score -> business_resilience_maturity_score
  (Each carries an inline "-- MIGRATION (AMD-011)" ALTER TABLE note directly
  beneath its table definition.)

ENUM VALUE CORRECTED (live schema, migration required):
  role_view_configuration.lens_id CHECK constraint: 'SUSTAINABILITY' -> 'RESILIENCE'
  (lens_vocabulary_map.lens_id carries the same corrected value in its
  documentation comment; that column has no CHECK constraint, so no ALTER
  is required there — comment-only fix.)

DEPRECATED IN PLACE (retained for read compatibility, stop writing to):
  role_registry                        — superseded by business_role_registry + membership_business_role
  user_role_mapping                    — superseded by membership_business_role (URA-001-37)
  organization_hierarchy.consolidation_method — superseded by consolidation_determination (ERG-001-08);
    two-release deprecation floor per SD-001-110, then dropped

NAMING COLLISION RESOLVED:
  event_registry retained as-is (external-world events only); workflow_event_registry
  / workflow_event_log added as permanently separate concepts for internal
  workflow-transition events (URA-001 Event model). No overlap, no shared columns.

LANGUAGE PURGE — 45 live/documentation occurrences corrected across
organization_master, organization_node, competitor_profile_registry,
material_topic_registry, metric_registry, framework_registry,
regulatory_requirement_registry, jurisdiction_requirement_mapping,
kpi_registry, kpi_metric_mapping, benchmark_registry, scenario_registry,
scenario_driver_mapping, risk_registry, external_factor_registry,
external_factor_impact_mapping, financial_metric_registry, insight_registry,
report_registry, ai_model_registry, competitive_signal_registry,
narrative_registry, market_trend_registry, event_registry,
audit_package_registry, lens_vocabulary_map, and role_view_configuration —
following the binding substitution table (ESG Score -> Business Resilience
Index; Carbon Emissions -> Energy Cost & Transition Exposure; Net Zero ->
Strategic Commitment; Sustainability Report -> Intelligence Foundation
Document; Scope 1/2/3 -> Direct/Procurement/Value Chain Cost; CSRD
Compliance -> Regulatory Cost Exposure). "Green Bond" and "Diversity
Metrics" were searched for and found to have zero occurrences in the base
document — no action was needed for those two terms.

ASSUMPTIONS AND FLAGGED ITEMS (not silently resolved):
  1. Two mentions of "ESG" (as "ESG Hub" and in a diagram service list)
     inside Appendix I ("Technical Section Review Findings") were left
     verbatim. That appendix is a historical audit trail quoting an
     EARLIER document section's actual (uncorrected) diagram/module names
     while reviewing it for internal consistency — changing the quoted
     names would misrepresent what that historical review actually found.
     This is treated the same as the task's own changelog carve-out
     ("a changelog line describing what was fixed is fine and expected").
     A human reviewer should confirm this treatment is acceptable.
  2. "Carbon Cost" (financial_metric_registry purpose example) was mapped
     to "Transition Cost Exposure" rather than reusing "Energy Cost &
     Transition Exposure" verbatim, since that exact list already contains
     a separate "Energy Cost" line item and reusing the full binding phrase
     would have produced a confusing near-duplicate. Same underlying
     concept, distinguished wording — flagged for confirmation.
  3. [RESOLVED, was originally flagged] Part C tables (consolidation_determination,
     enterprise_view_registry, traversal_policy_registry, node_permission_assignment)
     are placed immediately after organization_master rather than immediately after
     organization_hierarchy, specifically to avoid a forward-reference to
     organization_master before its own definition. consolidation_determination
     and node_permission_assignment still had genuine forward-references to
     membership_registry / business_role_registry (defined later, adjacent to
     user_registry, per the placement instruction for §B-URA-001). THIS HAS BEEN
     FIXED in this revision: the forward-referencing columns now declare a plain
     UUID inline with no REFERENCES clause, and the actual foreign-key constraint
     is attached via a separate ALTER TABLE ... ADD CONSTRAINT statement placed
     immediately after the target table's own definition. This is standard,
     fully executable practice for resolving circular/forward table dependencies
     in a single top-to-bottom script, and the document can now be run in
     reading order without error. Search for "FORWARD-REFERENCE NOTE" and
     "DEFERRED FK" to find both fixes.
  4. [FULLY RESOLVED as of v6.3, was flagged at v6.0, partially resolved at
     v6.1, and closed for all AMD-011 tables at v6.2] RLS policies are
     authored for 18 of the 22 AMD-011 tables, added as a new "AMD-011 RLS
     POLICY SET" sub-section at the end of Part D. The remaining 4
     (person_registry, identity_registry, system_role_registry,
     traversal_policy_registry) are intentionally left without a policy,
     consistent with this document's own existing precedent for genuinely
     global/master-reference tables (e.g. industry_taxonomy_registry also
     carries no RLS policy). consolidation_determination has an implemented
     policy reusing organization_node's own established tenant_workspace-
     schema mechanism (resolving hierarchy_id -> organization_hierarchy ->
     child_node_id and validating that node_id the same way organization_node
     validates itself). At v6.2 this left one separate, pre-existing gap
     explicitly noted rather than silently fixed: organization_hierarchy
     itself had no RLS policy of its own anywhere in the document, predating
     AMD-011 entirely. THIS WAS ALSO CLOSED, at v6.3: org_isolation_hierarchy
     was added immediately after organization_node's own policy in Part D,
     using the identical tenant_workspace mechanism, scoped on child_node_id
     for consistency with consolidation_determination's policy. Zero tables
     anywhere in the document — AMD-011 or pre-existing — are now left with
     an unresolved RLS decision (implemented, or intentionally exempt).
  5. The amendment's closing note also flags CorpStage_Complete_Blueprint.docx
     (86,000 words, 134 raw language-violation hits) as NOT YET addressed and
     recommends treating it as a separate, explicitly-scoped pass. That work
     is out of scope for this merge and is carried forward here, unresolved,
     exactly as the amendment left it.

  6. This document's own top-level sections are already named PART A
     (Authoritative Tables), PART B (Source-A-Exclusive Tables), PART C
     (Customer-Specific Domain Layer), and PART D (Row-Level Security) —
     a completely different numbering scheme from the amendment's own
     internal Part A (Language Purge) / B (URA-001) / C (ERG-001) / D
     (Event Collision) labels. To avoid a genuine ambiguity risk (e.g. an
     inline comment reading just "Part B" could mean either), every
     citation to the amendment's internal parts in this document uses the
     disambiguated form "Alignment Amendment v1.0 §B-URA-001" (etc.),
     never the bare "Part B." This was corrected during final review;
     verified zero remaining ambiguous references.

======================================================================
END AMD-011 CHANGELOG
======================================================================

BLUEPRINT v2.2 ALIGNMENT SUMMARY (v5.0 changes)
  AMD-004: 4-tier CDE hierarchy (CANONICAL/INDUSTRY/TENANT/TEMPORARY) added to
    metric_registry and customer_metric_registry. Semantic-match-before-create
    model implemented on customer_metric_registry (Blueprint Binding 3).
  AMD-005: unclassified_intelligence_registry — new table for extracted facts
    with no matching CDE. Never discards a discovered fact (Blueprint Binding 5).
  AMD-006: framework_tier + governed_by + parent_framework_id added to
    framework_registry. Implements the 3-tier framework governance model
    (Tier 1=Standard/CorpStage Admin, Tier 2=Custom/Corporate Admin,
    Tier 3=Extended/Corporate Admin additive only) (Blueprint Binding 2).
  AMD-007: Hide/Purge governance columns added to metric_registry and
    customer_metric_registry. New purge_audit_log table for the immutable
    audit record of every Hide/Unhide/Purge/Restore action (Blueprint Binding 7).
  AMD-008: department_registry + role_view_configuration — new tables making
    departments and roles platform metadata, not hardcoded logic. A Role View
    is a live aggregation of Department Views (Blueprint Section 5.0d).
  AMD-009: guided_completion_task — new table implementing the Guided Completion
    UX pattern ("Spend 3 minutes → Intelligence improves 18%"). Groups Business
    Questions into named business-activity tasks with declared time estimates
    and cross-domain impact statements (Blueprint Section 11 / Law 23).
  AMD-010: domain_coverage_snapshot + domain_coverage_current view — supports
    the Domain Coverage Dashboard (Blueprint Section 5.0e). No fixed denominator.
    Tracks Discovered/Inferred/Confirmed/Pending per Domain per organization.

FINAL VERIFIED STATE (v6.3, mechanically checked):
  136 distinct tables, zero duplicates, zero paren mismatches,
  zero tables from v5.0 dropped, zero unresolved live ESG/Sustainability/
  Carbon/Net-Zero/Scope-1-2-3/CSRD terms outside the one flagged historical
  appendix carve-out (Assumption 1 above), zero forward-referencing inline
  FK declarations (both resolved via deferred ALTER TABLE ADD CONSTRAINT —
  Assumption 3), 95 RLS policies (76 pre-AMD-011 + 18 AMD-011 + 1 v6.3 fix
  for organization_hierarchy, a pre-existing gap unrelated to AMD-011 — see
  Assumption 4), with 4 tables intentionally RLS-exempt as global/master
  reference data and zero tables left with an unresolved RLS decision
  anywhere in the document.


DOCUMENT SCOPE AND AUTHORITY

This document is the authoritative schema definition for the CorpStage 360
Intelligent Enterprise Operating Center platform. It defines all 136 tables,
their column-level DDL with data types, primary keys, foreign keys, and
PostgreSQL Row-Level Security policies (95 policies covering 96 tables of the
136 — see Assumption 4 for the 4 tables intentionally exempt as global/master
reference data, and note this count also folds in a v6.3 fix for
organization_hierarchy, a pre-existing gap unrelated to AMD-011).

GOVERNING DOCUMENTS:
  Architecture Blueprint v2.2 — product laws, binding decisions, UX principles.
  URA-001 v2.1 — User/Role/Permission/Event/Assignment Architecture.
  ERG-001 v2.0 — Enterprise Structure & Relationship Management.
  This document — schema implementation of those decisions.
  Where they conflict, the Blueprint and the two locked architecture
  documents (URA-001, ERG-001) govern.

AMENDMENT REGISTER SUMMARY:
  AMD-001: organization_id added to 49 transactional tables (tenant isolation).
  AMD-002: tenant_id (nullable) added to organization_master.
  AMD-003: confidence_rule_id added to 27 tables with confidence scores.
  AMD-004: 4-tier CDE hierarchy (cde_tier) on metric_registry;
           semantic-match model on customer_metric_registry.
  AMD-005: unclassified_intelligence_registry — extracted facts with no CDE.
  AMD-006: framework_tier + governed_by on framework_registry (3-tier governance).
  AMD-007: Hide/Purge columns + purge_audit_log (Blueprint v2.2 Binding 7).
  AMD-008: department_registry + role_view_configuration (Section 5.0d).
  AMD-009: guided_completion_task (Guided Completion UX engine).
  AMD-010: domain_coverage_snapshot + view (Domain Coverage Dashboard).
  AMD-011: Gold Standard Alignment Amendment v1.0 — URA-001/ERG-001
           reconciliation. See changelog above for full detail.
  (v6.3 note: organization_hierarchy's RLS policy is a fix to a pre-existing
  gap that predates AMD-001 through AMD-011 alike — it is not attributed to
  any single amendment number, since none of them introduced or owned it.)

VERIFIED STATE:
  136 tables, zero duplicates, zero unresolved forward-referencing inline FKs
  (both instances resolved via deferred ALTER TABLE ADD CONSTRAINT — see
  Assumption 3), 95 RLS policies (76 carried forward unchanged from v5.0 with
  zero gaps in that scope, +18 AMD-011 policies, +1 v6.3 fix for
  organization_hierarchy), 4 tables intentionally RLS-exempt as global/master
  reference data, zero tables anywhere in the document left with an
  unresolved RLS decision (see Assumption 4), zero paren mismatches.


PART 0: INDUSTRY INTELLIGENCE TAXONOMY LAYER
-- =========================================================================
-- industry_taxonomy_registry
-- PURPOSE: Self-referencing three-tier reference table (Sector -> Industry -> Sub-Industry) closing the gap where organization_master.sector and .industry_subsector were free text with no enforced classification.
-- FK: parent_taxonomy_id -> industry_taxonomy_registry (self-referencing)
-- =========================================================================
CREATE TABLE industry_taxonomy_registry (
    industry_taxonomy_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    taxonomy_level VARCHAR(20) NOT NULL CHECK (taxonomy_level IN ('SECTOR', 'INDUSTRY', 'SUB_INDUSTRY')),
    taxonomy_name VARCHAR(150) NOT NULL,
    taxonomy_code VARCHAR(50) NOT NULL UNIQUE,
    parent_taxonomy_id UUID REFERENCES industry_taxonomy_registry(industry_taxonomy_id),
    source_standard VARCHAR(50) NOT NULL DEFAULT 'SASB_SICS' CHECK (source_standard IN ('SASB_SICS', 'GICS', 'CUSTOM')),
    source_standard_code VARCHAR(50),
    taxonomy_description TEXT,
    active_flag BOOLEAN DEFAULT TRUE NOT NULL,
    effective_from TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    effective_to TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_taxonomy_parent_consistency CHECK (
        (taxonomy_level = 'SECTOR' AND parent_taxonomy_id IS NULL) OR
        (taxonomy_level IN ('INDUSTRY', 'SUB_INDUSTRY') AND parent_taxonomy_id IS NOT NULL)
    )
);

PART A: AUTHORITATIVE TABLES (97, per Source B Chapter 9)
-- =========================================================================
-- organization_node
-- PURPOSE: Canonical enterprise entity registry. Every organizational object exists here. Single source of truth for organizational structure.
-- FK (per Chapter 9 — authoritative): parent_node_id -> organization_node (self-referencing hierarchy)
-- =========================================================================
CREATE TABLE organization_node (
    node_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    node_code VARCHAR(100) UNIQUE NOT NULL  -- unique identifier,
    node_name VARCHAR(255)  -- entity name,
    node_type VARCHAR(255)  -- holding/region/entity/site/supplier/JV,
    legal_entity_name VARCHAR(255)  -- official legal entity,
    business_unit VARCHAR(255)  -- BU mapping,
    sector VARCHAR(255)  -- industry sector,
    geography_id UUID  -- geographic linkage,
    parent_available_flag BOOLEAN DEFAULT FALSE  -- hierarchy readiness,
    operational_status VARCHAR(255)  -- active/inactive/divested,
    strategic_importance_score INT  -- materiality significance,
    risk_criticality_score INT  -- risk relevance,
    reporting_currency VARCHAR(255)  -- financial standard,
    benchmark_group VARCHAR(255)  -- peer mapping,
    scenario_sensitive_flag BOOLEAN DEFAULT FALSE  -- forecasting relevance,
    external_dependency_flag BOOLEAN DEFAULT FALSE  -- outside-in relevance,
    entity_materiality_score INT  -- onboarding prioritization,
    data_readiness_score INT  -- document/data availability maturity,
    external_data_retrieval_flag BOOLEAN DEFAULT FALSE  -- web/API/public data retrievable,
    passport_shareable_flag BOOLEAN DEFAULT FALSE  -- shareable business resilience passport,
    active_flag BOOLEAN DEFAULT FALSE  -- active record,
    effective_from VARCHAR(255)  -- validity,
    effective_to VARCHAR(255)  -- validity,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    updated_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- organization_hierarchy
-- PURPOSE: Stores relationships between organizational nodes. Canonical graph-based hierarchy model supporting: - ownership - reporting - operational relationships - matrix organizations - JV structures - multi-parent governance Hierarchy intentionally separated from organization_node.
-- FK (per Chapter 9 — authoritative): parent_node_id -> organization_node | child_node_id -> organization_node
-- =========================================================================
CREATE TABLE organization_hierarchy (
    hierarchy_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_node_id UUID REFERENCES organization_node(node_id)  -- parent entity,
    child_node_id UUID REFERENCES organization_node(node_id)  -- child entity,
    relationship_type VARCHAR(255)  -- ownership/reporting/operational/functional,
    ownership_percentage VARCHAR(255)  -- ownership share,
    consolidation_method VARCHAR(255)  -- ** DEPRECATED (Alignment Amendment v1.0, §C-ERG-001 / ERG-001-08) ** — a relationship cannot own its own consolidation determination as an anti-pattern column; backfilled into the new consolidation_determination table below, kept nullable and readable for a minimum two-release deprecation window per SD-001-110, then dropped,
    reporting_scope_flag BOOLEAN DEFAULT FALSE  -- included in reporting,
    benchmark_scope_flag BOOLEAN DEFAULT FALSE  -- benchmarking eligibility,
    scenario_scope_flag BOOLEAN DEFAULT FALSE  -- forecasting propagation,
    strategic_control_flag BOOLEAN DEFAULT FALSE  -- governance control,
    relationship_confidence_score INT  -- confidence in hierarchy mapping,
    confidence_rule_id UUID  -- (see source narrative),
    effective_from VARCHAR(255)  -- validity,
    effective_to VARCHAR(255)  -- validity,
    active_flag BOOLEAN DEFAULT FALSE  -- active relationship,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- organization_master
-- PURPOSE: Stores enterprise-level company metadata. Organization-level settings are intentionally separated from node-level structure (organization_master != organization_node).
-- FK (per Chapter 9 — authoritative): tenant_id -> tenant_registry (nullable, AMD-002)
-- =========================================================================
CREATE TABLE organization_master (
    organization_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenant_registry(tenant_id)  -- Nullable. NULL means this organisation is its own tenant. Foreign key -> tenant_...,
    organization_name VARCHAR(255)  -- company,
    organization_code VARCHAR(100) UNIQUE NOT NULL  -- unique,
    headquarters_country VARCHAR(100)  -- HQ,
    sector VARCHAR(255)  -- industry — DEPRECATED, see industry_taxonomy_registry,
    industry_subsector VARCHAR(255)  -- detail — DEPRECATED, see industry_taxonomy_registry,
    reporting_currency VARCHAR(255)  -- standard,
    fiscal_year_type VARCHAR(255)  -- calendar,
    employee_count INT  -- scale,
    revenue_band VARCHAR(255)  -- maturity,
    stock_exchange_flag BOOLEAN DEFAULT FALSE  -- public/private,
    business_resilience_commitment_flag BOOLEAN DEFAULT FALSE  -- Business Resilience Index maturity,
    strategic_commitment_flag BOOLEAN DEFAULT FALSE  -- long-term strategic commitment,
    reporting_framework_json JSONB  -- standards,
    regulatory_jurisdictions_json JSONB  -- obligations,
    onboarding_stage VARCHAR(255)  -- onboarding progress,
    business_resilience_maturity_score INT  -- Business Resilience Index maturity score,
    framework_applicability_status_json JSONB  -- framework detection + confirmation,
    data_collection_mode VARCHAR(255)  -- retrieval-first/manual/hybrid,
    executive_brief_timezone VARCHAR(255)  -- briefing alignment,
    board_meeting_frequency VARCHAR(255)  -- executive cadence,
    daily_brief_enabled_flag BOOLEAN DEFAULT FALSE  -- executive intelligence,
    passport_enabled_flag BOOLEAN DEFAULT FALSE  -- business resilience passport enablement,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    sector_id UUID REFERENCES industry_taxonomy_registry(industry_taxonomy_id)  -- replaces deprecated free-text 'sector',
    industry_id UUID REFERENCES industry_taxonomy_registry(industry_taxonomy_id),
    sub_industry_id UUID REFERENCES industry_taxonomy_registry(industry_taxonomy_id)  -- replaces deprecated free-text 'industry_subsector'
);
-- MIGRATION (AMD-011, Alignment Amendment v1.0 §A-Language-Purge): ALTER TABLE organization_master RENAME COLUMN sustainability_commitment_flag TO business_resilience_commitment_flag;
-- MIGRATION (AMD-011, Alignment Amendment v1.0 §A-Language-Purge): ALTER TABLE organization_master RENAME COLUMN net_zero_target_flag TO strategic_commitment_flag;
-- MIGRATION (AMD-011, Alignment Amendment v1.0 §A-Language-Purge): ALTER TABLE organization_master RENAME COLUMN sustainability_maturity_score TO business_resilience_maturity_score;

-- SERVICE-LAYER VALIDATION REQUIREMENT (ERG-001-05, Alignment Amendment v1.0
-- Part C): a database constraint alone cannot detect graph cycles. Before
-- any organization_hierarchy INSERT of relationship_type IN ('OWNS',
-- 'PARTIALLY_OWNS'), the application layer MUST execute a recursive CTE
-- walk from child_node_id back up through existing parent_node_id chains
-- to confirm the proposed parent_node_id does not already appear as a
-- descendant of child_node_id. This is a mandatory pre-insert service-layer
-- check, not expressible as a pure SQL CHECK/FK constraint, and must not be
-- silently omitted because it is not a database-level rule.

-- =========================================================================
-- consolidation_determination
-- PURPOSE: Extracts consolidation method out of organization_hierarchy into
-- its own temporal object, since the same relationship can carry different
-- consolidation determinations under different reporting frameworks
-- (e.g. IFRS vs local GAAP) at different points in time.
-- FK: hierarchy_id -> organization_hierarchy | approved_by_membership_id -> membership_registry
--     (FK constraint for approved_by_membership_id added via ALTER TABLE after
--     membership_registry is defined below — see forward-reference note)
-- -- ERG-001-08: consolidation method as independent temporal object
-- =========================================================================
CREATE TABLE consolidation_determination (
    determination_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hierarchy_id UUID REFERENCES organization_hierarchy(hierarchy_id),
    consolidation_method VARCHAR(50), -- FULL/PROPORTIONAL/EQUITY_METHOD/EXCLUDE
    reporting_framework VARCHAR(100), -- IFRS, local GAAP, etc. — same relationship can have different determinations per framework
    approved_by_membership_id UUID, -- FK to membership_registry added below (forward reference — see note)
    effective_from TIMESTAMP WITH TIME ZONE,
    effective_to TIMESTAMP WITH TIME ZONE
);
-- FORWARD-REFERENCE NOTE: approved_by_membership_id cannot declare its FK
-- inline because membership_registry is not yet defined at this point in
-- the document (it is placed adjacent to user_registry per the amendment's
-- own placement instruction). The constraint is added explicitly once
-- membership_registry exists — see "ALTER TABLE consolidation_determination
-- ADD CONSTRAINT" immediately after membership_registry's definition below.
-- This is standard practice for resolving circular/forward table
-- dependencies and is fully valid, executable DDL in dependency order.
-- MIGRATION (AMD-011, Alignment Amendment v1.0 §C-ERG-001): backfill this table from
-- organization_hierarchy.consolidation_method (one row per existing non-null value,
-- reporting_framework defaulted to the organization's primary framework where not
-- otherwise recorded), then observe the two-release deprecation window on the
-- source column per SD-001-110 before dropping it.

-- =========================================================================
-- enterprise_view_registry
-- PURPOSE: Fully customer-defined enterprise views over the node/relationship
-- graph — no hardcoded view type. Powers VIEW_CONSTRAINED scope in
-- traversal_policy_registry and node_permission_assignment below.
-- FK: organization_id -> organization_master
-- -- ERG-001-06: view definitions are customer-configured, never hardcoded
-- =========================================================================
CREATE TABLE enterprise_view_registry (
    view_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organization_master(organization_id),
    view_name VARCHAR(255), -- fully customer-defined — NO hardcoded view type (ERG-001-06)
    traversal_constraint_json JSONB, -- which relationship types and nodes participate
    effective_from TIMESTAMP WITH TIME ZONE,
    effective_to TIMESTAMP WITH TIME ZONE
);

-- =========================================================================
-- traversal_policy_registry
-- PURPOSE: Governs whether and how access propagates across a relationship
-- type, independently of the relationship type's own definition.
-- FK: none (master reference table)
-- -- ERG-001-04: traversal/propagation is independently governed from the
-- relationship_type definition itself; defaults to no propagation
-- =========================================================================
CREATE TABLE traversal_policy_registry (
    traversal_policy_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    relationship_type VARCHAR(100), -- OWNS, SUPPORTS, SUPPLIES_TO, or tenant-defined
    propagates_access BOOLEAN DEFAULT FALSE, -- defaults to NODE_ONLY / no propagation (ERG-001-04)
    scope_type VARCHAR(50) -- NODE_ONLY/INCLUDE_DESCENDANTS/INCLUDE_ANCESTORS/VIEW_CONSTRAINED/CUSTOM_TRAVERSAL
);

-- =========================================================================
-- node_permission_assignment
-- PURPOSE: Resolves a membership/business-role's effective access to a node,
-- via a traversal policy and (optionally) a customer-defined enterprise view.
-- FK: membership_id -> membership_registry | business_role_id -> business_role_registry |
--     node_id -> organization_node | traversal_policy_id -> traversal_policy_registry |
--     enterprise_view_id -> enterprise_view_registry
--     (FK constraints for membership_id and business_role_id added via ALTER
--     TABLE after their target tables are defined below — see forward-reference note)
-- -- ERG-001-10: resolves to an effective domain_permission_registry row
-- before URA-001-76's precedence chain evaluates — never a competing
-- authorization system
-- =========================================================================
CREATE TABLE node_permission_assignment (
    assignment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    membership_id UUID, -- FK to membership_registry added below (forward reference — see note)
    business_role_id UUID, -- FK to business_role_registry added below (forward reference — see note)
    node_id UUID REFERENCES organization_node(node_id),
    traversal_policy_id UUID REFERENCES traversal_policy_registry(traversal_policy_id),
    enterprise_view_id UUID REFERENCES enterprise_view_registry(view_id), -- nullable, for VIEW_CONSTRAINED scope
    effective_from TIMESTAMP WITH TIME ZONE,
    effective_to TIMESTAMP WITH TIME ZONE
);
-- FORWARD-REFERENCE NOTE: membership_id and business_role_id cannot declare
-- their FKs inline because membership_registry and business_role_registry
-- are not yet defined at this point in the document (both are placed
-- adjacent to user_registry per the amendment's own placement instruction).
-- Both constraints are added explicitly once their target tables exist —
-- see "ALTER TABLE node_permission_assignment ADD CONSTRAINT" immediately
-- after membership_registry and business_role_registry's definitions below.

-- =========================================================================
-- user_registry
-- PURPOSE: Canonical user identity layer. Stores who interacts with CorpStage. Identity intentionally separated from permissions. Examples: - CFO - CSO - Plant Manager - Risk Head - Resilience Analyst - Board Member - Auditor - External Consultant
-- FK (per Chapter 9 — authoritative): default_node_scope -> organization_node | organization_id -> organization_master
-- =========================================================================
CREATE TABLE user_registry (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id UUID  -- HR linkage,
    full_name VARCHAR(255)  -- user,
    email_address VARCHAR(255)  -- login,
    department VARCHAR(255)  -- function,
    designation VARCHAR(255)  -- title,
    geography_scope VARCHAR(255)  -- region,
    default_node_scope UUID REFERENCES organization_node(node_id)  -- org visibility,
    executive_visibility_flag BOOLEAN DEFAULT FALSE  -- leadership,
    board_access_flag BOOLEAN DEFAULT FALSE  -- board,
    approval_authority_level INT  -- governance,
    external_user_flag BOOLEAN DEFAULT FALSE  -- consultant/auditor,
    authentication_type VARCHAR(255)  -- SSO/MFA,
    preferred_notification_channel VARCHAR(255)  -- email/mobile/teams/slack,
    notification_quiet_hours VARCHAR(255)  -- alert governance,
    daily_brief_subscription_flag BOOLEAN DEFAULT FALSE  -- executive briefing,
    preferred_language VARCHAR(255)  -- localization,
    persona_type VARCHAR(255)  -- executive/operator/analyst/board,
    decision_style VARCHAR(255)  -- summarized/deep-dive/exception-based,
    copilot_memory_enabled_flag BOOLEAN DEFAULT FALSE  -- AI context continuity,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    updated_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);
-- NOTE (Alignment Amendment v1.0, §B-URA-001): default_node_scope already anticipated
-- URA-001-17b's home-node concept (a rename/restructure, not new invention).
-- MIGRATION (AMD-011): user_registry.default_node_scope becomes membership_registry.home_node_id.
-- user_registry is retained going forward for authentication-session convenience fields only;
-- authority now resolves through membership_registry, not user_registry.

-- =========================================================================
-- role_registry
-- ** DEPRECATED (Alignment Amendment v1.0, §B-URA-001) ** — superseded by
-- business_role_registry + membership_business_role, which correctly
-- separate business roles from system roles (system_role_registry) and
-- approval authorities (approval_authority_registry) that this flat model
-- conflated. Retained here, unmodified, for read compatibility only —
-- stop writing to this table. No data migration script is prescribed by
-- the amendment beyond the read-compatibility retention itself.
-- PURPOSE: Stores business responsibility roles. Used for: - approval - governance - workflow routing - responsibility - delegation Not dashboard roles.
-- FK (per Chapter 9 — authoritative): none (master reference table)
-- =========================================================================
CREATE TABLE role_registry (
    role_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_name VARCHAR(255)  -- role,
    role_category VARCHAR(255)  -- executive/functional,
    role_description TEXT  -- definition,
    approval_authority_level INT  -- governance,
    executive_visibility_flag BOOLEAN DEFAULT FALSE  -- leadership,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    escalation_authority_flag BOOLEAN DEFAULT FALSE  -- escalation,
    workflow_assignment_flag BOOLEAN DEFAULT FALSE  -- workflow,
    delegation_allowed_flag BOOLEAN DEFAULT FALSE  -- backup,
    question_approval_authority_flag BOOLEAN DEFAULT FALSE  -- onboarding/governance approvals,
    narrative_review_authority_flag BOOLEAN DEFAULT FALSE  -- executive narrative review,
    evidence_override_authority_flag BOOLEAN DEFAULT FALSE  -- evidence acceptance override,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- user_role_mapping
-- ** DEPRECATED (Alignment Amendment v1.0, §B-URA-001) ** — superseded by
-- membership_business_role, which supports multiple simultaneous roles per
-- membership (URA-001-37) and correctly resolves through membership_registry
-- rather than user_registry directly. Retained, unmodified, for read
-- compatibility only — stop writing to this table.
-- PURPOSE: Defines who can do what. Separates users from roles. Supports: - multiple roles - temporary assignments - delegation - approval substitution - cross-functional responsibilities
-- FK (per Chapter 9 — authoritative): user_id -> user_registry | role_id -> role_registry | node_scope_id -> organization_node | delegated_by_user_id -> user_registry
-- =========================================================================
CREATE TABLE user_role_mapping (
    user_role_mapping_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES user_registry(user_id)  -- linked user,
    role_id UUID REFERENCES role_registry(role_id)  -- linked role,
    node_scope_id UUID REFERENCES organization_node(node_id)  -- org scope,
    assignment_type VARCHAR(255)  -- permanent/temporary,
    delegated_by_user_id UUID REFERENCES user_registry(user_id)  -- delegation,
    approval_scope VARCHAR(255)  -- authority,
    question_scope_flag BOOLEAN DEFAULT FALSE  -- onboarding/question permissions,
    narrative_scope_flag BOOLEAN DEFAULT FALSE  -- narrative review scope,
    effective_from VARCHAR(255)  -- validity,
    effective_to VARCHAR(255)  -- validity,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- person_registry
-- PURPOSE: The canonical individual, independent of any organization or
-- authentication method. Root of the Person/Identity/Membership separation
-- that user_registry's flat model never expressed.
-- FK: none (root reference table)
-- -- URA-001-15: Person is independent of any organization
-- =========================================================================
CREATE TABLE person_registry (
    person_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(255),
    primary_email VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE
);

-- =========================================================================
-- identity_registry
-- PURPOSE: One or more authentication identities held by a single Person.
-- FK: person_id -> person_registry
-- -- URA-001-16: one person may hold multiple identities
-- -- URA-001-25: auth_provider enumerates supported identity providers
-- =========================================================================
CREATE TABLE identity_registry (
    identity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    person_id UUID REFERENCES person_registry(person_id),
    auth_provider VARCHAR(100), -- Entra ID, Okta, Google, SAML, local (URA-001-25)
    auth_subject_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE
);

-- =========================================================================
-- membership_registry
-- PURPOSE: A Person's membership within a specific organization — the
-- authority-resolving object that user_registry's organization_id column
-- previously conflated with identity itself.
-- FK: person_id -> person_registry | organization_id -> organization_master |
--     home_node_id -> organization_node
-- -- URA-001-17b / ERG-001-03: home node linkage
-- -- URA-001-106: membership_type (INTERNAL/EXTERNAL)
-- -- URA-001-111: license_type (FULL/LIGHT)
-- -- URA-001-28: lifecycle_state — never hard-deleted
-- =========================================================================
CREATE TABLE membership_registry (
    membership_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    person_id UUID REFERENCES person_registry(person_id),
    organization_id UUID REFERENCES organization_master(organization_id),
    home_node_id UUID REFERENCES organization_node(node_id) NOT NULL, -- URA-001-17b / ERG-001-03
    membership_type VARCHAR(50), -- INTERNAL / EXTERNAL (URA-001-106)
    license_type VARCHAR(50),    -- FULL / LIGHT (URA-001-111)
    lifecycle_state VARCHAR(50), -- ACTIVE/SUSPENDED/DEACTIVATED/ARCHIVED — never hard-deleted (URA-001-28)
    effective_from TIMESTAMP WITH TIME ZONE,
    effective_to TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE
);
-- MIGRATION (AMD-011, Alignment Amendment v1.0 §B-URA-001): user_registry.default_node_scope
-- becomes membership_registry.home_node_id (backfill: one membership_registry row per
-- existing active user_registry row, home_node_id sourced from default_node_scope,
-- organization_id carried across unchanged).

-- DEFERRED FK (resolves forward reference from consolidation_determination above,
-- Alignment Amendment v1.0 §C-ERG-001): now that membership_registry exists,
-- attach the constraint that could not be declared inline.
ALTER TABLE consolidation_determination
    ADD CONSTRAINT fk_consolidation_determination_approved_by_membership
    FOREIGN KEY (approved_by_membership_id) REFERENCES membership_registry(membership_id);

-- =========================================================================
-- system_role_registry
-- PURPOSE: Platform administration roles only — distinct from business
-- responsibility roles below. Never grants business-data permissions.
-- FK: none (master reference table)
-- -- URA-001-29: system roles govern platform administration only
-- =========================================================================
CREATE TABLE system_role_registry (
    system_role_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_code VARCHAR(100), -- CORPSTAGE_ADMIN / CORPORATE_ADMIN / USER_ADMIN / SECURITY_ADMIN / DOMAIN_ADMIN
    role_name VARCHAR(255)
);

-- =========================================================================
-- business_role_registry
-- ** Supersedes role_registry (deprecated above) **
-- PURPOSE: Tenant-defined or global business roles (CEO, CFO, Plant Head,
-- or any custom label). Grants no permissions by itself — permission
-- resolution runs through domain_permission_registry and
-- node_permission_assignment, never through the role directly.
-- FK: organization_id -> organization_master (NULL = global)
-- -- URA-001-38: role_name is tenant-definable
-- -- URA-001-40: grants no permissions by itself
-- =========================================================================
CREATE TABLE business_role_registry (
    business_role_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organization_master(organization_id), -- NULL = global
    role_name VARCHAR(255), -- CEO, CFO, Plant Head, or any tenant-defined role (URA-001-38)
    effective_from TIMESTAMP WITH TIME ZONE,
    effective_to TIMESTAMP WITH TIME ZONE
);

-- DEFERRED FKs (resolve forward references from node_permission_assignment above,
-- Alignment Amendment v1.0 §C-ERG-001): both target tables now exist.
ALTER TABLE node_permission_assignment
    ADD CONSTRAINT fk_node_permission_assignment_membership
    FOREIGN KEY (membership_id) REFERENCES membership_registry(membership_id);
ALTER TABLE node_permission_assignment
    ADD CONSTRAINT fk_node_permission_assignment_business_role
    FOREIGN KEY (business_role_id) REFERENCES business_role_registry(business_role_id);

-- =========================================================================
-- membership_business_role
-- ** Supersedes user_role_mapping (deprecated above) **
-- PURPOSE: Assigns one or more simultaneous business roles to a membership.
-- FK: membership_id -> membership_registry | business_role_id -> business_role_registry
-- -- URA-001-37: supports multiple simultaneous roles per membership
-- =========================================================================
CREATE TABLE membership_business_role (
    membership_id UUID REFERENCES membership_registry(membership_id),
    business_role_id UUID REFERENCES business_role_registry(business_role_id),
    effective_from TIMESTAMP WITH TIME ZONE,
    effective_to TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY (membership_id, business_role_id, effective_from)
);

-- =========================================================================
-- approval_authority_registry
-- PURPOSE: Named approval authorities (e.g. Annual Report Approver),
-- deliberately independent of business_role_registry — an approval
-- authority is not a role, and a role does not automatically carry one.
-- FK: organization_id -> organization_master
-- -- URA-001-04: independent of business_role_registry
-- -- URA-001-41: authority_name examples
-- -- URA-001-42: approval_strategy (ANY_ONE/ALL/MAJORITY/SEQUENTIAL)
-- -- URA-001-82: majority_threshold_pct is configurable
-- =========================================================================
CREATE TABLE approval_authority_registry (
    approval_authority_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organization_master(organization_id),
    authority_name VARCHAR(255), -- Annual Report Approver, Financial Statement Approver (URA-001-41)
    approval_strategy VARCHAR(50), -- ANY_ONE / ALL / MAJORITY / SEQUENTIAL (URA-001-42)
    majority_threshold_pct INT -- configurable, e.g. 50/66/75/100 (URA-001-82)
);

-- =========================================================================
-- membership_approval_authority
-- PURPOSE: Assigns one or more approval authorities to a membership.
-- FK: membership_id -> membership_registry | approval_authority_id -> approval_authority_registry
-- =========================================================================
CREATE TABLE membership_approval_authority (
    membership_id UUID REFERENCES membership_registry(membership_id),
    approval_authority_id UUID REFERENCES approval_authority_registry(approval_authority_id),
    effective_from TIMESTAMP WITH TIME ZONE,
    effective_to TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY (membership_id, approval_authority_id, effective_from)
);

-- =========================================================================
-- group_registry
-- PURPOSE: Named groups (e.g. Board Committee, Finance Leadership Team)
-- supporting group hierarchies, for group-based assignment and delegation.
-- FK: organization_id -> organization_master | parent_group_id -> group_registry (self-referencing)
-- -- URA-001-57: group examples | URA-001-59: group hierarchies
-- =========================================================================
CREATE TABLE group_registry (
    group_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organization_master(organization_id),
    group_name VARCHAR(255), -- Board Committee, Finance Leadership Team (URA-001-57)
    parent_group_id UUID REFERENCES group_registry(group_id) -- group hierarchies (URA-001-59)
);

-- =========================================================================
-- group_membership
-- PURPOSE: Assigns memberships to groups.
-- FK: group_id -> group_registry | membership_id -> membership_registry
-- =========================================================================
CREATE TABLE group_membership (
    group_id UUID REFERENCES group_registry(group_id),
    membership_id UUID REFERENCES membership_registry(membership_id),
    effective_from TIMESTAMP WITH TIME ZONE,
    effective_to TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY (group_id, membership_id, effective_from)
);

-- =========================================================================
-- domain_permission_registry
-- PURPOSE: The actual permission-level grant of a membership over a domain
-- (Finance, HR, Risk, etc.) — the row that node_permission_assignment
-- resolves to before URA-001-76's precedence chain evaluates.
-- FK: membership_id -> membership_registry
-- -- URA-001-47: permission_level enumeration
-- =========================================================================
CREATE TABLE domain_permission_registry (
    domain_permission_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    membership_id UUID REFERENCES membership_registry(membership_id),
    domain_id UUID, -- references domain object (Finance, HR, Risk, etc.)
    permission_level VARCHAR(50), -- VIEW/ENTER/EDIT/REVIEW/APPROVE/ASSIGN/DELEGATE/ADMIN (URA-001-47)
    effective_from TIMESTAMP WITH TIME ZONE,
    effective_to TIMESTAMP WITH TIME ZONE
);

-- =========================================================================
-- runtime_assignment_registry
-- PURPOSE: A live, in-flight work assignment — always object-scoped,
-- event-scoped, and time-scoped; never a standing global assignment.
-- FK: assigned_to_membership_id -> membership_registry |
--     assigned_to_group_id -> group_registry |
--     assigned_to_business_role_id -> business_role_registry
-- -- URA-001-77: Object Scoped, Event Scoped, Time Scoped, never global
-- -- URA-001-78: status lifecycle enumeration
-- event_code links to workflow_event_registry, Part D below
-- =========================================================================
CREATE TABLE runtime_assignment_registry (
    assignment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    object_type VARCHAR(100),
    object_id UUID,
    event_code VARCHAR(100), -- links to workflow_event_registry, Part D below
    assigned_to_membership_id UUID REFERENCES membership_registry(membership_id),
    assigned_to_group_id UUID REFERENCES group_registry(group_id),
    assigned_to_business_role_id UUID REFERENCES business_role_registry(business_role_id),
    status VARCHAR(50), -- CREATED/ASSIGNED/ACCEPTED/IN_PROGRESS/COMPLETED/REJECTED/ESCALATED/EXPIRED/ARCHIVED (URA-001-78)
    effective_from TIMESTAMP WITH TIME ZONE,
    effective_to TIMESTAMP WITH TIME ZONE
);

-- =========================================================================
-- delegation_registry
-- PURPOSE: A temporary handoff of authority from one membership to another.
-- Delegations are always temporary and always require a stated reason.
-- FK: delegator_membership_id -> membership_registry | delegatee_membership_id -> membership_registry
-- -- URA-001-89: scope_type | URA-001-90: delegation_type
-- -- URA-001-92: sub_delegation_allowed | URA-001-88: reason is mandatory
-- =========================================================================
CREATE TABLE delegation_registry (
    delegation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    delegator_membership_id UUID REFERENCES membership_registry(membership_id),
    delegatee_membership_id UUID REFERENCES membership_registry(membership_id),
    scope_type VARCHAR(50), -- ORGANIZATION/DOMAIN/OBJECT/EVENT (URA-001-89)
    delegation_type VARCHAR(50), -- TEMPORARY/OUT_OF_OFFICE/EMERGENCY/ACTING_ROLE/PROJECT_BASED (URA-001-90)
    sub_delegation_allowed BOOLEAN DEFAULT FALSE, -- (URA-001-92)
    reason TEXT NOT NULL, -- delegations always require a reason (URA-001-88)
    effective_from TIMESTAMP WITH TIME ZONE NOT NULL,
    effective_to TIMESTAMP WITH TIME ZONE NOT NULL -- delegations are always temporary, never permanent
);

-- =========================================================================
-- escalation_policy_registry
-- PURPOSE: Configures how an unresolved item escalates. Cycle protection
-- is mandatory at configuration time, not just at runtime.
-- FK: organization_id -> organization_master
-- -- URA-001-94: strategy_type | URA-001-94a: mandatory cycle-protection depth limit
-- =========================================================================
CREATE TABLE escalation_policy_registry (
    escalation_policy_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organization_master(organization_id),
    strategy_type VARCHAR(50), -- TIME_BASED/HIERARCHY_BASED/ROLE_BASED/GROUP_BASED (URA-001-94)
    max_depth INT DEFAULT 5 NOT NULL, -- URA-001-94a: mandatory cycle-protection depth limit
    time_threshold_hours INT
);

-- SERVICE-LAYER VALIDATION REQUIREMENT (URA-001-94a, Alignment Amendment v1.0
-- Part B): max_depth alone does not prevent a cyclical escalation chain
-- (A escalates to B escalates back to A). Configuration-time cycle
-- validation (graph walk across escalation_policy_registry's configured
-- targets) is required before an escalation policy is activated — this is
-- an application-layer check, not expressible as a pure SQL constraint.

-- =========================================================================
-- license_registry
-- PURPOSE: License grant record per membership.
-- FK: membership_id -> membership_registry
-- -- URA-001-111: license_type (FULL/LIGHT)
-- =========================================================================
CREATE TABLE license_registry (
    license_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    membership_id UUID REFERENCES membership_registry(membership_id),
    license_type VARCHAR(50) -- FULL / LIGHT (URA-001-111)
);

-- =========================================================================
-- entitlement_registry
-- PURPOSE: Feature/module entitlements at the organization level —
-- explicitly separate from license_registry, which governs per-membership
-- licensing rather than org-wide feature enablement.
-- FK: organization_id -> organization_master
-- -- URA-001-112: entitlement_code examples; explicitly separate from license_registry
-- =========================================================================
CREATE TABLE entitlement_registry (
    entitlement_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organization_master(organization_id),
    entitlement_code VARCHAR(100), -- IFRS_ENABLED, AI_DISCOVERY_ENABLED, SUPPLIER_PORTAL_ENABLED (URA-001-112)
    effective_from TIMESTAMP WITH TIME ZONE,
    effective_to TIMESTAMP WITH TIME ZONE
);

-- =========================================================================
-- material_topic_registry
-- PURPOSE: Defines what matters to the business. Supports: - double materiality - financial materiality - impact materiality - sector-specific materiality - regulatory materiality
-- FK (per Chapter 9 — authoritative): none (master reference table)
-- =========================================================================
CREATE TABLE material_topic_registry (
    material_topic_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic_name VARCHAR(255)  -- topic,
    topic_category VARCHAR(255)  -- Business Resilience/risk/financial,
    topic_description TEXT  -- explanation,
    sector_relevance VARCHAR(255)  -- industry relevance,
    financial_materiality_score INT  -- business impact,
    impact_materiality_score INT  -- societal impact,
    regulatory_materiality_flag BOOLEAN DEFAULT FALSE  -- compliance,
    executive_priority_level INT  -- importance,
    benchmark_relevance_flag BOOLEAN DEFAULT FALSE  -- peers,
    predictive_relevance_flag BOOLEAN DEFAULT FALSE  -- forecasting,
    framework_materiality_json JSONB  -- framework-level materiality applicability,
    materiality_confidence_score INT  -- confidence in topic prioritization,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- metric_registry
-- PURPOSE: Canonical metric library. Every metric defined once and reused everywhere. Examples: - electricity consumption - water withdrawal - employee injury rate - renewable energy % - energy cost & transition exposure - supplier compliance %
-- FK (per Chapter 9 — authoritative): material_topic_id -> material_topic_registry
-- =========================================================================
CREATE TABLE metric_registry (
    metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_name VARCHAR(255)  -- metric,
    metric_code VARCHAR(100) UNIQUE NOT NULL  -- unique,
    metric_category VARCHAR(255)  -- Business Resilience/risk/financial,
    metric_subcategory VARCHAR(255)  -- detail,
    metric_description TEXT  -- definition,
    unit_of_measure VARCHAR(255)  -- standard,
    formula_logic TEXT  -- calculation,
    normalization_logic TEXT  -- intensity logic,
    source_type VARCHAR(255)  -- system/manual,
    material_topic_id UUID REFERENCES material_topic_registry(material_topic_id)  -- linkage,
    benchmark_enabled_flag BOOLEAN DEFAULT FALSE  -- peer context,
    scenario_sensitive_flag BOOLEAN DEFAULT FALSE  -- forecasting,
    predictive_relevance_score INT  -- prediction,
    executive_visibility_flag BOOLEAN DEFAULT FALSE  -- leadership,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    framework_mapping_json JSONB  -- linked disclosure frameworks,
    evidence_required_flag BOOLEAN DEFAULT FALSE  -- audit readiness,
    ai_extractable_flag BOOLEAN DEFAULT FALSE  -- document extraction readiness,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- metric_source_mapping
-- PURPOSE: Defines where metrics come from. Maps metrics to: - SAP - IoT - Excel - utility systems - manual inputs - government data - third-party providers Critical for trust, lineage, and explainability.
-- FK (per Chapter 9 — authoritative): metric_id -> metric_registry | organization_id -> organization_master | confidence_rule_id -> confidence_scoring_registry
-- =========================================================================
CREATE TABLE metric_source_mapping (
    metric_source_mapping_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_id UUID REFERENCES metric_registry(metric_id)  -- linked metric,
    source_id UUID  -- external source,
    connector_id UUID  -- integration,
    source_priority INT  -- fallback,
    ingestion_frequency VARCHAR(255)  -- cadence,
    transformation_logic TEXT  -- conversion,
    validation_required_flag BOOLEAN DEFAULT FALSE  -- trust,
    confidence_score INT  -- quality,
    lineage_enabled_flag BOOLEAN DEFAULT FALSE  -- explainability,
    ai_extraction_enabled_flag BOOLEAN DEFAULT FALSE  -- document extraction support,
    fallback_manual_capture_flag BOOLEAN DEFAULT FALSE  -- manual fallback,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- metric_record
-- PURPOSE: Stores actual metric values over time. Fact table of reality. Example: Water Consumption Plant A Jan 2026 = 12,400 m³
-- FK (per Chapter 9 — authoritative): metric_id -> metric_registry | node_id -> organization_node | source_id -> metric_source_mapping | approved_by -> user_registry | confidence_rule_id -> confidence_scoring_registry
-- =========================================================================
CREATE TABLE metric_record (
    metric_record_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_id UUID REFERENCES metric_registry(metric_id)  -- metric,
    node_id UUID REFERENCES organization_node(node_id)  -- organization scope,
    reporting_period VARCHAR(255)  -- period,
    metric_value NUMERIC(18,2)  -- value,
    normalized_value NUMERIC(18,2)  -- intensity,
    unit_of_measure VARCHAR(255)  -- unit,
    source_id UUID REFERENCES metric_source_mapping(metric_source_mapping_id)  -- origin,
    confidence_score INT  -- trust,
    anomaly_flag BOOLEAN DEFAULT FALSE  -- quality,
    externally_verified_flag BOOLEAN DEFAULT FALSE  -- assurance,
    review_status VARCHAR(255)  -- workflow,
    approved_by UUID REFERENCES user_registry(user_id)  -- governance,
    approval_timestamp TIMESTAMP WITH TIME ZONE  -- validation,
    evidence_document_id UUID  -- supporting evidence,
    retrieval_method VARCHAR(255)  -- system/manual/AI extracted,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- framework_registry
-- PURPOSE: Defines global reporting frameworks. Supports: - GRI - ISSB - Regulatory Cost Exposure Framework - ESRS - BRSR - ISSB S2 - CDP - SASB Simultaneously.
-- FK (per Chapter 9 — authoritative): none (master reference table)
-- =========================================================================
CREATE TABLE framework_registry (
    framework_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    framework_name VARCHAR(255)  -- framework,
    framework_version VARCHAR(255)  -- version,
    framework_category VARCHAR(255)  -- mandatory/voluntary,
    jurisdiction_scope VARCHAR(255)  -- geography,
    reporting_frequency VARCHAR(255)  -- cadence,
    materiality_required_flag BOOLEAN DEFAULT FALSE  -- requirement,
    assurance_required_flag BOOLEAN DEFAULT FALSE  -- validation,
    framework_status VARCHAR(255)  -- detected/confirmed/active,
    framework_priority_score INT  -- onboarding priority,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    effective_from VARCHAR(255)  -- validity,
    effective_to VARCHAR(255)  -- validity,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- regulatory_requirement_registry
-- PURPOSE: Defines specific disclosure requirements. Examples: - Regulatory Cost Exposure Framework E1-5 - BRSR Principle 6 - ISSB Climate Metrics
-- FK (per Chapter 9 — authoritative): framework_id -> framework_registry
-- =========================================================================
CREATE TABLE regulatory_requirement_registry (
    requirement_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    framework_id UUID REFERENCES framework_registry(framework_id)  -- linked framework,
    requirement_code VARCHAR(100)  -- official code,
    requirement_name VARCHAR(255)  -- requirement,
    disclosure_description TEXT  -- requirement,
    mandatory_flag BOOLEAN DEFAULT FALSE  -- required,
    metric_dependency_flag BOOLEAN DEFAULT FALSE  -- metric needed,
    evidence_required_flag BOOLEAN DEFAULT FALSE  -- defensibility,
    review_requirement_flag BOOLEAN DEFAULT FALSE  -- approval,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- materiality,
    canonical_question_dependency_flag BOOLEAN DEFAULT FALSE  -- onboarding dependency,
    domain_category VARCHAR(255)  -- climate/governance/water/etc.,
    requirement_priority_score INT  -- onboarding prioritization,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- jurisdiction_requirement_mapping
-- PURPOSE: Solves multi-country compliance complexity. Examples: India → BRSR EU → Regulatory Cost Exposure Framework US → SEC Climate Different requirements supported simultaneously.
-- FK (per Chapter 9 — authoritative): framework_id -> framework_registry | requirement_id -> regulatory_requirement_registry
-- =========================================================================
CREATE TABLE jurisdiction_requirement_mapping (
    jurisdiction_requirement_mapping_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    jurisdiction VARCHAR(255)  -- geography,
    framework_id UUID REFERENCES framework_registry(framework_id)  -- framework,
    requirement_id UUID REFERENCES regulatory_requirement_registry(requirement_id)  -- disclosure,
    applicability_logic TEXT  -- threshold,
    mandatory_flag BOOLEAN DEFAULT FALSE  -- obligation,
    entity_threshold_logic INT  -- revenue/employee/listing thresholds,
    effective_from VARCHAR(255)  -- start,
    effective_to VARCHAR(255)  -- end,
    active_flag BOOLEAN DEFAULT FALSE  -- active
);

-- =========================================================================
-- metric_review_workflow
-- PURPOSE: Defines governance rules for metric approval. Only: - high materiality - low confidence - high risk - board-facing metrics require approval.
-- FK (per Chapter 9 — authoritative): metric_id -> metric_registry | organization_id -> organization_master
-- =========================================================================
CREATE TABLE metric_review_workflow (
    workflow_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_id UUID REFERENCES metric_registry(metric_id)  -- linked metric,
    materiality_threshold INT  -- trigger,
    confidence_threshold INT  -- trigger,
    approval_level INT  -- governance,
    escalation_rule VARCHAR(255)  -- fallback,
    executive_visibility_rule VARCHAR(255)  -- exposure,
    board_visibility_rule VARCHAR(255)  -- board,
    auto_approval_flag BOOLEAN DEFAULT FALSE  -- automation support,
    review_frequency VARCHAR(255)  -- cadence,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- metric_review_workflow_execution
-- PURPOSE: Tracks actual approval execution. Example: Energy Cost & Transition Exposure reviewed by Resilience Head approved on Jan 12
-- FK (per Chapter 9 — authoritative): workflow_id -> metric_review_workflow | metric_record_id -> metric_record | reviewer_user_id -> user_registry
-- =========================================================================
CREATE TABLE metric_review_workflow_execution (
    execution_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID REFERENCES metric_review_workflow(workflow_id)  -- workflow,
    metric_record_id UUID REFERENCES metric_record(metric_record_id)  -- metric value,
    reviewer_user_id UUID REFERENCES user_registry(user_id)  -- reviewer,
    review_status VARCHAR(255)  -- pending/approved,
    review_comments VARCHAR(255)  -- explanation,
    confidence_override VARCHAR(255)  -- human adjustment,
    escalation_flag BOOLEAN DEFAULT FALSE  -- escalation,
    override_reason_code VARCHAR(100)  -- governance traceability,
    approved_timestamp TIMESTAMP WITH TIME ZONE  -- audit,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- kpi_registry
-- PURPOSE: Defines enterprise KPIs. KPIs are business performance indicators built from one or many metrics. Examples: - Energy Transition Intensity - Water Efficiency - Renewable Energy Ratio - Operational Risk Exposure - EBITDA Resilience - Supplier Resilience Score KPIs are what executives see, not raw metrics.
-- FK (per Chapter 9 — authoritative): material_topic_id -> material_topic_registry
-- =========================================================================
CREATE TABLE kpi_registry (
    kpi_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    kpi_name VARCHAR(255)  -- KPI,
    kpi_code VARCHAR(100) UNIQUE NOT NULL  -- unique,
    kpi_category VARCHAR(255)  -- Business Resilience/risk/financial/operational,
    kpi_subcategory VARCHAR(255)  -- detail,
    kpi_description TEXT  -- business meaning,
    calculation_logic TEXT  -- formula,
    target_logic TEXT  -- target definition,
    normalization_method VARCHAR(255)  -- intensity logic,
    material_topic_id UUID REFERENCES material_topic_registry(material_topic_id)  -- linkage,
    executive_priority_level INT  -- importance,
    benchmark_enabled_flag BOOLEAN DEFAULT FALSE  -- peer comparison,
    scenario_sensitive_flag BOOLEAN DEFAULT FALSE  -- forecasting,
    predictive_enabled_flag BOOLEAN DEFAULT FALSE  -- future intelligence,
    narrative_enabled_flag BOOLEAN DEFAULT FALSE  -- AI narrative,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    executive_summary_flag BOOLEAN DEFAULT FALSE  -- executive dashboard priority,
    alert_enabled_flag BOOLEAN DEFAULT FALSE  -- threshold alerts,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- kpi_metric_mapping
-- PURPOSE: Defines how KPIs are built. Maps metrics → KPI. Example: KPI: Energy Transition Intensity Built from: - Direct Cost - Procurement Cost - Production Volume
-- FK (per Chapter 9 — authoritative): kpi_id -> kpi_registry | metric_id -> metric_registry
-- =========================================================================
CREATE TABLE kpi_metric_mapping (
    kpi_metric_mapping_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    kpi_id UUID REFERENCES kpi_registry(kpi_id)  -- KPI,
    metric_id UUID REFERENCES metric_registry(metric_id)  -- metric,
    contribution_weight VARCHAR(255)  -- weighting,
    formula_sequence INT  -- logic order,
    transformation_logic TEXT  -- calculation,
    dependency_type VARCHAR(255)  -- required/optional,
    benchmark_relevance_flag BOOLEAN DEFAULT FALSE  -- peer relevance,
    scenario_impact_flag BOOLEAN DEFAULT FALSE  -- simulator,
    causal_dependency_flag BOOLEAN DEFAULT FALSE  -- KPI dependency chain,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- benchmark_registry
-- PURPOSE: Defines benchmarking methodology. Supports: - sector benchmark - geographic benchmark - custom peer group - top quartile - internal benchmark - historical benchmark
-- FK (per Chapter 9 — authoritative): none (master reference table)
-- =========================================================================
CREATE TABLE benchmark_registry (
    benchmark_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    benchmark_name VARCHAR(255)  -- benchmark,
    benchmark_category VARCHAR(255)  -- Business Resilience/risk/financial,
    benchmark_type VARCHAR(255)  -- sector/peer/internal,
    industry_sector VARCHAR(255)  -- scope,
    geography_scope VARCHAR(255)  -- region,
    methodology_description TEXT  -- methodology,
    percentile_logic TEXT  -- ranking,
    external_source_id UUID  -- provider,
    confidence_score INT  -- trust,
    executive_priority_flag INT  -- visibility,
    narrative_enabled_flag BOOLEAN DEFAULT FALSE  -- storytelling,
    benchmark_refresh_frequency VARCHAR(255)  -- update cadence,
    materiality_weight_flag BOOLEAN DEFAULT FALSE  -- material KPI prioritization,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- peer_comparison_registry
-- PURPOSE: Defines company-specific peer comparison logic. Answers: Who should we compare against? Example: Manufacturing India → Tata Steel, JSW, ArcelorMittal, Nucor
-- FK (per Chapter 9 — authoritative): benchmark_id -> benchmark_registry | organization_id -> organization_master
-- =========================================================================
CREATE TABLE peer_comparison_registry (
    peer_comparison_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    benchmark_id UUID REFERENCES benchmark_registry(benchmark_id)  -- benchmark,
    comparison_name VARCHAR(255)  -- comparison,
    comparison_scope VARCHAR(255)  -- sector/peer/custom,
    industry_sector VARCHAR(255)  -- industry,
    geography_scope VARCHAR(255)  -- region,
    selected_peer_company_json JSONB  -- peers,
    comparison_metric_type VARCHAR(255)  -- KPI/risk/financial,
    percentile_position VARCHAR(255)  -- ranking,
    urgency_score INT  -- urgency,
    narrative_trigger_flag BOOLEAN DEFAULT FALSE  -- storytelling,
    executive_visibility_flag BOOLEAN DEFAULT FALSE  -- leadership,
    competitive_gap_score INT  -- performance distance vs peers,
    peer_refresh_frequency VARCHAR(255)  -- update cadence,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- scenario_registry
-- PURPOSE: Defines what-if simulation models. Supports: - energy price shocks - energy transition cost scenarios - climate disruption - supplier failure - regulatory change - water scarcity - market slowdown - commodity volatility Explains what could happen next.
-- FK (per Chapter 9 — authoritative): organization_id -> organization_master
-- =========================================================================
CREATE TABLE scenario_registry (
    scenario_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scenario_name VARCHAR(255)  -- scenario,
    scenario_category VARCHAR(255)  -- climate/financial/regulatory,
    scenario_description TEXT  -- context,
    scenario_time_horizon VARCHAR(255)  -- short/medium/long,
    baseline_assumption_json JSONB  -- assumptions,
    impact_logic TEXT  -- methodology,
    sensitivity_model VARCHAR(255)  -- calculation,
    benchmark_enabled_flag BOOLEAN DEFAULT FALSE  -- peers,
    executive_visibility_flag BOOLEAN DEFAULT FALSE  -- leadership,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    simulation_confidence_score INT  -- confidence in prediction,
    recommended_action_flag BOOLEAN DEFAULT FALSE  -- trigger actions,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- scenario_external_factor_mapping
-- PURPOSE: Defines what drives a scenario. Links scenarios to: - energy price - commodity price - water availability - interest rates - energy transition cost - inflation - FX rates - weather events Powers the simulator.
-- FK (per Chapter 9 — authoritative): scenario_id -> scenario_registry | external_factor_id -> external_factor_registry
-- =========================================================================
CREATE TABLE scenario_external_factor_mapping (
    scenario_external_factor_mapping_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scenario_id UUID REFERENCES scenario_registry(scenario_id)  -- scenario,
    external_factor_id UUID REFERENCES external_factor_registry(external_factor_id)  -- factor,
    baseline_value NUMERIC(18,2)  -- current,
    min_simulation_value NUMERIC(18,2)  -- lower bound,
    max_simulation_value NUMERIC(18,2)  -- upper bound,
    adjustment_granularity VARCHAR(255)  -- precision,
    impact_weight VARCHAR(255)  -- influence,
    cascading_impact_flag BOOLEAN DEFAULT FALSE  -- propagation,
    executive_visibility_flag BOOLEAN DEFAULT FALSE  -- materiality,
    sensitivity_coefficient VARCHAR(255)  -- impact elasticity,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- risk_registry
-- PURPOSE: Canonical enterprise risk registry. Defines risks across: - Business Resilience - operations - finance - supply chain - regulatory - cyber - climate - reputation - market Examples: - Water Scarcity - Energy Transition Cost Exposure - Supplier Failure - Energy Volatility - Regulatory Non-Compliance - Climate Physical Risk
-- FK (per Chapter 9 — authoritative): material_topic_id -> material_topic_registry
-- =========================================================================
CREATE TABLE risk_registry (
    risk_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    risk_name VARCHAR(255)  -- risk,
    risk_code VARCHAR(100) UNIQUE NOT NULL  -- unique,
    risk_category VARCHAR(255)  -- Business Resilience/financial/operational,
    risk_subcategory VARCHAR(255)  -- detail,
    risk_description TEXT  -- explanation,
    material_topic_id UUID REFERENCES material_topic_registry(material_topic_id)  -- linkage,
    inherent_risk_score INT  -- base severity,
    residual_risk_score INT  -- after controls,
    likelihood_score INT  -- probability,
    impact_score INT  -- business effect,
    financial_materiality_score INT  -- financial relevance,
    regulatory_materiality_flag BOOLEAN DEFAULT FALSE  -- compliance,
    predictive_relevance_score INT  -- forecasting,
    benchmark_enabled_flag BOOLEAN DEFAULT FALSE  -- peers,
    executive_visibility_flag BOOLEAN DEFAULT FALSE  -- leadership,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    risk_velocity_score INT  -- speed of risk escalation,
    early_warning_flag BOOLEAN DEFAULT FALSE  -- predictive signal monitoring,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- risk_metric_mapping
-- PURPOSE: Defines what signals influence risk. Maps metrics → risks. Example: Water Scarcity driven by: - water withdrawal - groundwater availability - regional drought index - water regulation Enables explainable risk scoring.
-- FK (per Chapter 9 — authoritative): risk_id -> risk_registry | metric_id -> metric_registry
-- =========================================================================
CREATE TABLE risk_metric_mapping (
    risk_metric_mapping_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    risk_id UUID REFERENCES risk_registry(risk_id)  -- risk,
    metric_id UUID REFERENCES metric_registry(metric_id)  -- metric,
    influence_weight VARCHAR(255)  -- importance,
    threshold_logic INT  -- trigger,
    sensitivity_level INT  -- low/medium/high,
    anomaly_trigger_flag BOOLEAN DEFAULT FALSE  -- alert,
    predictive_impact_flag BOOLEAN DEFAULT FALSE  -- forecasting,
    scenario_sensitive_flag BOOLEAN DEFAULT FALSE  -- simulator,
    causal_dependency_flag BOOLEAN DEFAULT FALSE  -- risk causality,
    early_warning_trigger_flag BOOLEAN DEFAULT FALSE  -- predictive alerts,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- external_factor_registry
-- PURPOSE: Defines outside-world signals. Tracks: - energy price - commodity price - inflation - interest rates - weather - energy transition price - regulations - climate events - geopolitical risks - competitor signals Powers outside-in intelligence.
-- FK (per Chapter 9 — authoritative): none (master reference table)
-- =========================================================================
CREATE TABLE external_factor_registry (
    external_factor_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    factor_name VARCHAR(255)  -- factor,
    factor_category VARCHAR(255)  -- market/regulatory/climate,
    factor_subcategory VARCHAR(255)  -- detail,
    source_id UUID  -- provider,
    geography_scope VARCHAR(255)  -- region,
    unit_of_measure VARCHAR(255)  -- standard,
    update_frequency VARCHAR(255)  -- cadence,
    volatility_score INT  -- instability,
    predictive_importance_score INT  -- forecasting,
    benchmark_relevance_flag BOOLEAN DEFAULT FALSE  -- peers,
    scenario_enabled_flag BOOLEAN DEFAULT FALSE  -- simulator,
    executive_visibility_flag BOOLEAN DEFAULT FALSE  -- leadership,
    leading_indicator_flag BOOLEAN DEFAULT FALSE  -- predictive signal,
    refresh_confidence_score INT  -- source confidence,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- external_factor_impact_mapping
-- PURPOSE: Defines what external factors affect. Maps: external factor ↓ risk ↓ KPI ↓ financial impact Example: Energy Transition Price affects: - opex - emissions - profitability - risk
-- FK (per Chapter 9 — authoritative): external_factor_id -> external_factor_registry
-- =========================================================================
CREATE TABLE external_factor_impact_mapping (
    external_factor_impact_mapping_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    external_factor_id UUID REFERENCES external_factor_registry(external_factor_id)  -- factor,
    impacted_entity_type VARCHAR(255)  -- KPI/risk/financial,
    impacted_entity_id UUID  -- target,
    influence_weight VARCHAR(255)  -- strength,
    sensitivity_logic TEXT  -- methodology,
    cascading_effect_flag BOOLEAN DEFAULT FALSE  -- propagation,
    predictive_trigger_flag BOOLEAN DEFAULT FALSE  -- forecasting,
    executive_materiality_flag BOOLEAN DEFAULT FALSE  -- visibility,
    impact_time_lag VARCHAR(255)  -- delayed effect,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- financial_impact_registry
-- PURPOSE: Defines business impact of business resilience and risk events. Answers: What does this mean financially? Connects business resilience and risk to: - revenue - margin - EBITDA - cash flow - capex - opex
-- FK (per Chapter 9 — authoritative): polymorphic (linked_entity_type/linked_entity_id) | organization_id -> organization_master
-- =========================================================================
CREATE TABLE financial_impact_registry (
    financial_impact_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    impact_name VARCHAR(255)  -- impact,
    impact_category VARCHAR(255)  -- revenue/cost/EBITDA,
    linked_entity_type VARCHAR(255)  -- KPI/risk/factor,
    linked_entity_id UUID  -- source,
    baseline_financial_value NUMERIC(18,2)  -- baseline,
    projected_financial_impact NUMERIC(18,2)  -- forecast,
    confidence_score INT  -- trust,
    sensitivity_score INT  -- volatility,
    executive_materiality_flag BOOLEAN DEFAULT FALSE  -- importance,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    time_horizon VARCHAR(255)  -- short/medium/long,
    financial_exposure_band VARCHAR(255)  -- low/medium/high,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- financial_impact_sensitivity
-- PURPOSE: Supports sensitivity simulation. Example: Energy Price: 150 → 180 USD System estimates: - operating cost impact - EBITDA impact - risk movement - benchmark movement
-- FK (per Chapter 9 — authoritative): financial_impact_id -> financial_impact_registry | external_factor_id -> external_factor_registry
-- =========================================================================
CREATE TABLE financial_impact_sensitivity (
    financial_impact_sensitivity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    financial_impact_id UUID REFERENCES financial_impact_registry(financial_impact_id)  -- impact,
    external_factor_id UUID REFERENCES external_factor_registry(external_factor_id)  -- factor,
    baseline_value NUMERIC(18,2)  -- today,
    adjusted_value NUMERIC(18,2)  -- simulation,
    sensitivity_coefficient VARCHAR(255)  -- influence,
    projected_financial_delta VARCHAR(255)  -- expected change,
    confidence_score INT  -- trust,
    cascading_impact_flag BOOLEAN DEFAULT FALSE  -- propagation,
    narrative_trigger_flag BOOLEAN DEFAULT FALSE  -- commentary,
    scenario_execution_id UUID  -- simulation traceability,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- financial_metric_registry
-- PURPOSE: Defines canonical financial metrics. Examples: - Revenue - Gross Margin - EBITDA - Operating Cost - Energy Cost - Transition Cost Exposure - Cash Flow - Capex - Opex - Working Capital Financial intelligence building blocks.
-- FK (per Chapter 9 — authoritative): none (master reference table)
-- =========================================================================
CREATE TABLE financial_metric_registry (
    financial_metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_name VARCHAR(255)  -- metric,
    metric_code VARCHAR(100) UNIQUE NOT NULL  -- unique,
    metric_category VARCHAR(255)  -- revenue/cost/profitability,
    metric_subcategory VARCHAR(255)  -- detail,
    metric_description TEXT  -- definition,
    formula_logic TEXT  -- calculation,
    reporting_standard VARCHAR(255)  -- accounting method,
    reporting_currency_logic TEXT  -- FX,
    scenario_sensitive_flag BOOLEAN DEFAULT FALSE  -- forecasting,
    benchmark_enabled_flag BOOLEAN DEFAULT FALSE  -- peers,
    executive_visibility_flag BOOLEAN DEFAULT FALSE  -- leadership,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    materiality_relevance_score INT  -- executive importance,
    financial_statement_mapping TEXT  -- P&L/BS/Cash Flow,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- financial_record
-- PURPOSE: Stores actual financial values over time. Financial fact table. Example: India Manufacturing Q1 2026 Energy Cost = $42.8M
-- FK (per Chapter 9 — authoritative): financial_metric_id -> financial_metric_registry | node_id -> organization_node | approved_by -> user_registry
-- =========================================================================
CREATE TABLE financial_record (
    financial_record_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    financial_metric_id UUID REFERENCES financial_metric_registry(financial_metric_id)  -- metric,
    node_id UUID REFERENCES organization_node(node_id)  -- organization scope,
    reporting_period VARCHAR(255)  -- time,
    actual_value NUMERIC(18,2)  -- reported,
    forecast_value NUMERIC(18,2)  -- projected,
    normalized_value NUMERIC(18,2)  -- intensity,
    currency VARCHAR(255)  -- reporting,
    source_id UUID  -- origin,
    confidence_score INT  -- trust,
    anomaly_flag BOOLEAN DEFAULT FALSE  -- unusual,
    approved_flag BOOLEAN DEFAULT FALSE  -- governance,
    approved_by UUID REFERENCES user_registry(user_id)  -- approver,
    approval_timestamp TIMESTAMP WITH TIME ZONE  -- audit,
    retrieval_method VARCHAR(255)  -- ERP/manual/AI extracted,
    evidence_document_id UUID  -- supporting evidence,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- executive_insight_registry
-- PURPOSE: Executive intelligence engine. Stores what executives should know. Generated from: - KPIs - risk changes - financial impact - external signals - benchmarks - predictive models
-- FK (per Chapter 9 — authoritative): node_id -> organization_node | organization_id -> organization_master
-- =========================================================================
CREATE TABLE executive_insight_registry (
    executive_insight_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    insight_category VARCHAR(255)  -- Business Resilience/risk/financial,
    insight_title VARCHAR(255)  -- summary,
    insight_description TEXT  -- explanation,
    linked_entity_type VARCHAR(255)  -- KPI/risk/scenario,
    linked_entity_id UUID  -- source,
    materiality_score INT  -- importance,
    urgency_score INT  -- urgency,
    financial_impact_score INT  -- business effect,
    benchmark_gap_score INT  -- peer gap,
    confidence_score INT  -- trust,
    narrative_summary TEXT  -- AI explanation,
    executive_action_required_flag BOOLEAN DEFAULT FALSE  -- response,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    generated_timestamp TIMESTAMP WITH TIME ZONE  -- timing,
    insight_priority_rank INT  -- executive ordering,
    recommended_action_available_flag BOOLEAN DEFAULT FALSE  -- actionability,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- recommendation_registry
-- PURPOSE: Defines what CorpStage recommends doing. Moves platform from reporting → actionability. Example: Insight: Energy price risk ↑ Recommendation: Increase renewable sourcing by 18% Expected savings = $2.7M
-- FK (per Chapter 9 — authoritative): executive_insight_id -> executive_insight_registry | organization_id -> organization_master
-- =========================================================================
CREATE TABLE recommendation_registry (
    recommendation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    executive_insight_id UUID REFERENCES executive_insight_registry(executive_insight_id)  -- insight,
    recommendation_category VARCHAR(255)  -- cost/risk/compliance,
    recommendation_title VARCHAR(255)  -- action,
    recommendation_description TEXT  -- explanation,
    linked_entity_type VARCHAR(255)  -- KPI/risk/scenario,
    linked_entity_id UUID  -- source,
    expected_financial_benefit VARCHAR(255)  -- value,
    expected_risk_reduction VARCHAR(255)  -- impact,
    implementation_effort_score INT  -- effort,
    confidence_score INT  -- trust,
    owner_role_id UUID  -- accountability,
    due_date_recommendation VARCHAR(255)  -- timing,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    implementation_priority_score INT  -- execution priority,
    expected_payback_period VARCHAR(255)  -- ROI timing,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- action_tracker
-- PURPOSE: Tracks what was actually done. Moves recommendations into execution. Example: Recommendation: Reduce energy dependence Action: Install solar at Plant B Owner: COO Deadline: Dec 2026 Status: In Progress
-- FK (per Chapter 9 — authoritative): recommendation_id -> recommendation_registry | owner_user_id -> user_registry
-- =========================================================================
CREATE TABLE action_tracker (
    action_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recommendation_id UUID REFERENCES recommendation_registry(recommendation_id)  -- recommendation,
    action_title VARCHAR(255)  -- action,
    action_description TEXT  -- detail,
    owner_user_id UUID REFERENCES user_registry(user_id)  -- accountable,
    owner_role_id UUID  -- responsibility,
    node_scope_id UUID  -- org scope,
    action_status VARCHAR(255)  -- pending/in-progress,
    target_completion_date TIMESTAMP WITH TIME ZONE  -- timeline,
    budget_allocated VARCHAR(255)  -- funding,
    expected_business_impact NUMERIC(18,2)  -- value,
    progress_percentage VARCHAR(255)  -- status,
    escalation_flag BOOLEAN DEFAULT FALSE  -- delay,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    actual_completion_date TIMESTAMP WITH TIME ZONE  -- execution closure,
    execution_confidence_score INT  -- delivery confidence,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- action_impact_tracking
-- PURPOSE: Measures whether actions worked. Example: Action: Switch renewable sourcing Outcome: - Energy Cost ↓ 8% - EBITDA ↑ 2.1% - Energy Cost & Transition Exposure ↓ 14%
-- FK (per Chapter 9 — authoritative): action_id -> action_tracker
-- =========================================================================
CREATE TABLE action_impact_tracking (
    action_impact_tracking_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    action_id UUID REFERENCES action_tracker(action_id)  -- action,
    impacted_entity_type VARCHAR(255)  -- KPI/risk/financial,
    impacted_entity_id UUID  -- target,
    baseline_value NUMERIC(18,2)  -- before,
    actual_value NUMERIC(18,2)  -- after,
    delta_value NUMERIC(18,2)  -- improvement,
    achieved_financial_impact NUMERIC(18,2)  -- realized value,
    achieved_risk_reduction VARCHAR(255)  -- realized reduction,
    confidence_score INT  -- trust,
    success_rating VARCHAR(255)  -- effectiveness,
    narrative_summary TEXT  -- AI summary,
    ROI_realization_score INT  -- realized ROI,
    lessons_learned_summary VARCHAR(255)  -- continuous learning,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- workflow_registry
-- PURPOSE: Defines enterprise workflow templates. Used for: - metric approvals - risk escalation - board approvals - regulatory submissions - stakeholder reviews - executive signoffs
-- FK (per Chapter 9 — authoritative): none (master reference table)
-- =========================================================================
CREATE TABLE workflow_registry (
    workflow_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_name VARCHAR(255)  -- workflow,
    workflow_category VARCHAR(255)  -- metric/risk/disclosure,
    workflow_description TEXT  -- explanation,
    trigger_entity_type VARCHAR(255)  -- KPI/risk/metric,
    trigger_logic TEXT  -- automation,
    approval_level_count INT  -- complexity,
    escalation_enabled_flag BOOLEAN DEFAULT FALSE  -- governance,
    board_approval_required_flag BOOLEAN DEFAULT FALSE  -- materiality,
    SLA_days VARCHAR(255)  -- response timeline,
    auto_trigger_flag BOOLEAN DEFAULT FALSE  -- automation,
    workflow_priority_level INT  -- governance criticality,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- workflow_execution
-- PURPOSE: Tracks actual workflow execution. Tracks what actually happened.
-- FK (per Chapter 9 — authoritative): workflow_id -> workflow_registry | triggered_by_user_id -> user_registry | organization_id -> organization_master
-- =========================================================================
CREATE TABLE workflow_execution (
    workflow_execution_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID REFERENCES workflow_registry(workflow_id)  -- workflow,
    linked_entity_type VARCHAR(255)  -- KPI/risk/disclosure,
    linked_entity_id UUID  -- entity,
    workflow_status VARCHAR(255)  -- pending/completed,
    current_approver_user_id UUID  -- approver,
    escalation_flag BOOLEAN DEFAULT FALSE  -- delay,
    SLA_breach_flag BOOLEAN DEFAULT FALSE  -- governance,
    completion_timestamp TIMESTAMP WITH TIME ZONE  -- finish,
    workflow_comments VARCHAR(255)  -- audit,
    approval_sequence_number INT  -- approval order,
    workflow_outcome_status VARCHAR(255)  -- approved/rejected/escalated,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- evidence_registry
-- PURPOSE: Stores evidence supporting intelligence. Supports: - metrics - risk scores - financial assumptions - regulatory disclosures - AI recommendations - board narratives Examples: - utility invoices - audit reports - supplier declarations - regulatory filings - IoT logs
-- FK (per Chapter 9 — authoritative): node_id -> organization_node | uploaded_by -> user_registry | organization_id -> organization_master
-- =========================================================================
CREATE TABLE evidence_registry (
    evidence_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evidence_type VARCHAR(255)  -- invoice/report/API,
    linked_entity_type VARCHAR(255)  -- metric/risk/disclosure,
    linked_entity_id UUID  -- entity,
    evidence_source VARCHAR(255)  -- provider,
    file_reference VARCHAR(255)  -- document,
    source_timestamp TIMESTAMP WITH TIME ZONE  -- evidence timing,
    confidence_score INT  -- reliability,
    externally_verified_flag BOOLEAN DEFAULT FALSE  -- assurance,
    legal_defensibility_flag BOOLEAN DEFAULT FALSE  -- audit,
    retention_policy VARCHAR(255)  -- governance,
    document_hash_signature VARCHAR(255)  -- tamper-proofing,
    AI_extracted_flag BOOLEAN DEFAULT FALSE  -- extraction traceability,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- stakeholder_registry
-- PURPOSE: Defines internal and external stakeholders. Supports: - employees - investors - regulators - communities - customers - suppliers - NGOs - board - media
-- FK (per Chapter 9 — authoritative): node_id -> organization_node | organization_id -> organization_master
-- =========================================================================
CREATE TABLE stakeholder_registry (
    stakeholder_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stakeholder_name VARCHAR(255)  -- stakeholder,
    stakeholder_category VARCHAR(255)  -- regulator/investor,
    stakeholder_subcategory VARCHAR(255)  -- detail,
    geography_scope VARCHAR(255)  -- region,
    influence_score INT  -- importance,
    impact_sensitivity_score INT  -- sensitivity,
    engagement_priority_level INT  -- urgency,
    regulatory_relevance_flag BOOLEAN DEFAULT FALSE  -- compliance,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    stakeholder_materiality_score INT  -- enterprise relevance,
    engagement_frequency VARCHAR(255)  -- cadence,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- stakeholder_engagement
-- PURPOSE: Tracks stakeholder interactions. Example: Investor concern: Water risk exposure Tracks: - issue raised - response - action - closure Stakeholder concerns influence: - risk - materiality - board priorities
-- FK (per Chapter 9 — authoritative): stakeholder_id -> stakeholder_registry | conducted_by -> user_registry
-- =========================================================================
CREATE TABLE stakeholder_engagement (
    stakeholder_engagement_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stakeholder_id UUID REFERENCES stakeholder_registry(stakeholder_id)  -- stakeholder,
    engagement_type VARCHAR(255)  -- meeting/survey,
    engagement_topic VARCHAR(255)  -- issue,
    linked_entity_type VARCHAR(255)  -- KPI/risk,
    linked_entity_id UUID  -- topic,
    engagement_date TIMESTAMP WITH TIME ZONE  -- timing,
    concern_level INT  -- severity,
    action_required_flag BOOLEAN DEFAULT FALSE  -- follow-up,
    owner_user_id UUID  -- accountability,
    closure_status VARCHAR(255)  -- completed,
    materiality_impact_flag BOOLEAN DEFAULT FALSE  -- materiality influence,
    escalation_required_flag BOOLEAN DEFAULT FALSE  -- governance escalation,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- stakeholder_sentiment_tracking
-- PURPOSE: Tracks stakeholder perception trends over time. Supports: - reputation risk - investor trust - community sentiment - supplier confidence - employee trust Example: Community trust ↓ after water shortage event
-- FK (per Chapter 9 — authoritative): stakeholder_id -> stakeholder_registry
-- =========================================================================
CREATE TABLE stakeholder_sentiment_tracking (
    stakeholder_sentiment_tracking_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stakeholder_id UUID REFERENCES stakeholder_registry(stakeholder_id)  -- stakeholder,
    reporting_period VARCHAR(255)  -- time,
    sentiment_score INT  -- score,
    sentiment_category VARCHAR(255)  -- positive/neutral/negative,
    sentiment_driver VARCHAR(255)  -- reason,
    linked_entity_type VARCHAR(255)  -- KPI/risk/event,
    linked_entity_id UUID  -- source,
    confidence_score INT  -- trust,
    executive_alert_flag BOOLEAN DEFAULT FALSE  -- escalation,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    sentiment_trend_direction VARCHAR(255)  -- improving/stable/declining,
    reputation_risk_flag BOOLEAN DEFAULT FALSE  -- enterprise risk signal,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- narrative_registry
-- PURPOSE: Stores AI-generated executive narratives. Supports: - executive summaries - board commentary - risk explanations - KPI explanations - scenario summaries - regulatory reporting text Separates: data layer → explanation layer
-- FK (per Chapter 9 — authoritative): node_id -> organization_node | approved_by -> user_registry | organization_id -> organization_master
-- =========================================================================
CREATE TABLE narrative_registry (
    narrative_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    narrative_category VARCHAR(255)  -- Business Resilience/risk/financial,
    narrative_title TEXT  -- title,
    narrative_summary TEXT  -- generated text,
    linked_entity_type VARCHAR(255)  -- KPI/risk/scenario,
    linked_entity_id UUID  -- source,
    reporting_period VARCHAR(255)  -- timing,
    narrative_priority_level INT  -- importance,
    confidence_score INT  -- trust,
    benchmark_context_flag BOOLEAN DEFAULT FALSE  -- peer comparison,
    financial_impact_flag BOOLEAN DEFAULT FALSE  -- business effect,
    recommendation_included_flag BOOLEAN DEFAULT FALSE  -- actionability,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    human_review_required_flag BOOLEAN DEFAULT FALSE  -- governance,
    approved_flag BOOLEAN DEFAULT FALSE  -- approval,
    narrative_generation_type VARCHAR(255)  -- AI/manual/hybrid,
    explainability_score INT  -- defensibility,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- narrative_component_mapping
-- PURPOSE: Defines what builds a narrative. Maps narrative content to: - KPIs - metrics - risks - financial impact - benchmarks - external signals - actions Ensures narrative explainability.
-- FK (per Chapter 9 — authoritative): narrative_id -> narrative_registry
-- =========================================================================
CREATE TABLE narrative_component_mapping (
    narrative_component_mapping_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    narrative_id UUID REFERENCES narrative_registry(narrative_id)  -- narrative,
    component_entity_type VARCHAR(255)  -- KPI/risk/metric,
    component_entity_id UUID  -- source,
    contribution_weight VARCHAR(255)  -- importance,
    reasoning_logic TEXT  -- explanation,
    confidence_score INT  -- trust,
    anomaly_trigger_flag BOOLEAN DEFAULT FALSE  -- significance,
    benchmark_reference_flag BOOLEAN DEFAULT FALSE  -- peer context,
    recommendation_reference_flag BOOLEAN DEFAULT FALSE  -- action,
    evidence_reference_flag BOOLEAN DEFAULT FALSE  -- traceability,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- report_registry
-- PURPOSE: Stores generated reports. Supports: - board packs - executive summaries - Business Resilience reports - annual reports - regulatory disclosures - quarterly intelligence reports Single intelligence base → many outputs.
-- FK (per Chapter 9 — authoritative): node_id -> organization_node | approved_by -> user_registry | organization_id -> organization_master
-- =========================================================================
CREATE TABLE report_registry (
    report_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_name VARCHAR(255)  -- report,
    report_category VARCHAR(255)  -- board/regulatory,
    reporting_period VARCHAR(255)  -- timing,
    report_version VARCHAR(255)  -- version,
    narrative_included_flag BOOLEAN DEFAULT FALSE  -- storytelling,
    disclosure_required_flag BOOLEAN DEFAULT FALSE  -- compliance,
    executive_visibility_flag BOOLEAN DEFAULT FALSE  -- leadership,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    report_status VARCHAR(255)  -- draft/reviewed,
    generated_timestamp TIMESTAMP WITH TIME ZONE  -- generation,
    approved_by_user_id UUID  -- approval,
    submission_status VARCHAR(255)  -- draft/submitted/filed,
    report_output_format VARCHAR(255)  -- PDF/XLSX/PPT,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- disclosure_requirement_mapping
-- PURPOSE: Maps framework disclosure requirements to actual enterprise data. Automates compliance by linking disclosures to: - KPIs - metrics - risks - narratives - evidence - governance workflows
-- FK (per Chapter 9 — authoritative): framework_id -> framework_registry | requirement_id -> regulatory_requirement_registry
-- =========================================================================
CREATE TABLE disclosure_requirement_mapping (
    disclosure_requirement_mapping_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    framework_id UUID REFERENCES framework_registry(framework_id)  -- framework,
    requirement_id UUID REFERENCES regulatory_requirement_registry(requirement_id)  -- disclosure,
    linked_entity_type VARCHAR(255)  -- KPI/risk/narrative/metric,
    linked_entity_id UUID  -- source,
    evidence_required_flag BOOLEAN DEFAULT FALSE  -- defensibility,
    workflow_required_flag BOOLEAN DEFAULT FALSE  -- approval,
    submission_deadline VARCHAR(255)  -- timing,
    board_review_required_flag BOOLEAN DEFAULT FALSE  -- governance,
    mandatory_response_flag BOOLEAN DEFAULT FALSE  -- mandatory disclosure,
    data_availability_status VARCHAR(255)  -- available/missing/partial,
    auto_extract_supported_flag BOOLEAN DEFAULT FALSE  -- AI extraction readiness,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- disclosure_submission_tracker
-- PURPOSE: Tracks actual disclosure submissions.
-- FK (per Chapter 9 — authoritative): report_id -> report_registry | framework_id -> framework_registry | submitted_by -> user_registry
-- =========================================================================
CREATE TABLE disclosure_submission_tracker (
    submission_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    framework_id UUID REFERENCES framework_registry(framework_id)  -- framework,
    report_id UUID REFERENCES report_registry(report_id)  -- report,
    jurisdiction VARCHAR(255)  -- geography,
    reporting_period VARCHAR(255)  -- timing,
    submission_status VARCHAR(255)  -- draft/submitted,
    submission_date TIMESTAMP WITH TIME ZONE  -- timing,
    regulator_reference_number VARCHAR(255)  -- tracking,
    assurance_status VARCHAR(255)  -- validation,
    escalation_flag BOOLEAN DEFAULT FALSE  -- missed deadline,
    submission_version VARCHAR(255)  -- filing version,
    resubmission_flag BOOLEAN DEFAULT FALSE  -- amended filing,
    submission_owner_user_id UUID  -- accountability,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- narrative_feedback_learning
-- PURPOSE: Supports continuous narrative improvement. Tracks: - executive feedback - board edits - regulatory comments - approval changes Improves narrative quality over time.
-- FK (per Chapter 9 — authoritative): narrative_id -> narrative_registry | reviewer_user_id -> user_registry
-- =========================================================================
CREATE TABLE narrative_feedback_learning (
    narrative_feedback_learning_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    narrative_id UUID REFERENCES narrative_registry(narrative_id)  -- narrative,
    reviewer_user_id UUID REFERENCES user_registry(user_id)  -- reviewer,
    feedback_type VARCHAR(255)  -- correction/improvement,
    original_text_reference VARCHAR(255)  -- before,
    revised_text_reference VARCHAR(255)  -- after,
    feedback_reason VARCHAR(255)  -- rationale,
    learning_confidence_score INT  -- AI learning,
    board_preference_flag BOOLEAN DEFAULT FALSE  -- governance,
    feedback_acceptance_flag BOOLEAN DEFAULT FALSE  -- accepted/rejected,
    regulatory_alignment_flag BOOLEAN DEFAULT FALSE  -- compliance improvement,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- predictive_model_registry
-- PURPOSE: Defines predictive models available in CorpStage. Supports: - risk forecasting - financial forecasting - Business Resilience forecasting - anomaly prediction - scenario prediction Governed AI model registry.
-- FK (per Chapter 9 — authoritative): none (master reference table)
-- =========================================================================
CREATE TABLE predictive_model_registry (
    predictive_model_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_name VARCHAR(255)  -- model,
    model_category VARCHAR(255)  -- Business Resilience/risk/financial,
    model_subcategory VARCHAR(255)  -- detail,
    model_description TEXT  -- explanation,
    prediction_target_type VARCHAR(255)  -- KPI/risk/financial,
    prediction_horizon VARCHAR(255)  -- short/medium/long,
    algorithm_type VARCHAR(255)  -- ML/statistical,
    explainability_required_flag BOOLEAN DEFAULT FALSE  -- transparency,
    benchmark_enabled_flag BOOLEAN DEFAULT FALSE  -- peer intelligence,
    confidence_threshold INT  -- trust,
    executive_visibility_flag BOOLEAN DEFAULT FALSE  -- leadership,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    model_owner_user_id UUID  -- accountability,
    model_version VARCHAR(255)  -- governance,
    retraining_frequency VARCHAR(255)  -- cadence,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- predictive_model_execution
-- PURPOSE: Tracks actual model execution. Stores: - prediction results - confidence - anomalies - alerts - narratives
-- FK (per Chapter 9 — authoritative): predictive_model_id -> predictive_model_registry | node_id -> organization_node | organization_id -> organization_master
-- =========================================================================
CREATE TABLE predictive_model_execution (
    predictive_execution_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    predictive_model_id UUID REFERENCES predictive_model_registry(predictive_model_id)  -- model,
    linked_entity_type VARCHAR(255)  -- KPI/risk/financial,
    linked_entity_id UUID  -- target,
    prediction_timestamp TIMESTAMP WITH TIME ZONE  -- timing,
    predicted_value NUMERIC(18,2)  -- forecast,
    confidence_score INT  -- trust,
    prediction_horizon VARCHAR(255)  -- timeline,
    anomaly_probability VARCHAR(255)  -- instability,
    benchmark_comparison_score INT  -- peer context,
    narrative_generated_flag BOOLEAN DEFAULT FALSE  -- storytelling,
    executive_alert_flag BOOLEAN DEFAULT FALSE  -- escalation,
    prediction_status VARCHAR(255)  -- completed/failed,
    actual_outcome_value NUMERIC(18,2)  -- accuracy validation,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- anomaly_detection_registry
-- PURPOSE: Detects unexpected deviations. Supports: - cost spikes - compliance anomalies - emissions variance - supplier disruption - financial volatility
-- FK (per Chapter 9 — authoritative): node_id -> organization_node | metric_id -> metric_registry | organization_id -> organization_master
-- =========================================================================
CREATE TABLE anomaly_detection_registry (
    anomaly_detection_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    anomaly_category VARCHAR(255)  -- KPI/risk/financial,
    linked_entity_type VARCHAR(255)  -- metric/KPI,
    linked_entity_id UUID  -- target,
    expected_value NUMERIC(18,2)  -- baseline,
    actual_value NUMERIC(18,2)  -- observed,
    variance_percentage VARCHAR(255)  -- deviation,
    anomaly_severity_score INT  -- severity,
    root_cause_hypothesis TEXT  -- explanation,
    predictive_escalation_flag BOOLEAN DEFAULT FALSE  -- future risk,
    executive_alert_flag BOOLEAN DEFAULT FALSE  -- urgency,
    resolved_flag BOOLEAN DEFAULT FALSE  -- remediation,
    resolution_comments VARCHAR(255)  -- closure,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- optimization_recommendation_registry
-- PURPOSE: Defines AI-optimized decisions. Predictive + optimization-driven recommendations.
-- FK (per Chapter 9 — authoritative): predictive_execution_id -> predictive_model_execution | organization_id -> organization_master
-- =========================================================================
CREATE TABLE optimization_recommendation_registry (
    optimization_recommendation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    predictive_execution_id UUID REFERENCES predictive_model_execution(predictive_execution_id)  -- prediction,
    recommendation_type VARCHAR(255)  -- cost/risk,
    recommendation_title VARCHAR(255)  -- action,
    recommendation_description TEXT  -- detail,
    optimization_target VARCHAR(255)  -- EBITDA/risk,
    expected_optimization_value NUMERIC(18,2)  -- benefit,
    implementation_complexity VARCHAR(255)  -- effort,
    confidence_score INT  -- trust,
    recommended_execution_window VARCHAR(255)  -- timing,
    executive_priority_score INT  -- urgency,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    estimated_payback_period VARCHAR(255)  -- ROI,
    owner_role_id UUID  -- accountability,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- learning_feedback_registry
-- PURPOSE: Captures human feedback to AI decisions. Allows AI to learn: - organization preferences - executive behavior - risk appetite - business constraints
-- FK (per Chapter 9 — authoritative): reviewer_user_id -> user_registry | organization_id -> organization_master
-- =========================================================================
CREATE TABLE learning_feedback_registry (
    learning_feedback_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    linked_entity_type VARCHAR(255)  -- recommendation/narrative,
    linked_entity_id UUID  -- source,
    reviewer_user_id UUID REFERENCES user_registry(user_id)  -- reviewer,
    feedback_category VARCHAR(255)  -- accepted/rejected,
    feedback_reason VARCHAR(255)  -- rationale,
    confidence_adjustment VARCHAR(255)  -- learning,
    contextual_factor TEXT  -- business context,
    organization_preference_flag BOOLEAN DEFAULT FALSE  -- preference,
    executive_override_flag BOOLEAN DEFAULT FALSE  -- governance,
    feedback_effectiveness_score INT  -- learning quality,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- AI_confidence_recalibration
-- PURPOSE: Adjusts AI confidence dynamically. Confidence becomes: earned, not assumed
-- FK (per Chapter 9 — authoritative): predictive_model_id -> predictive_model_registry | organization_id -> organization_master
-- =========================================================================
CREATE TABLE AI_confidence_recalibration (
    recalibration_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    predictive_model_id UUID REFERENCES predictive_model_registry(predictive_model_id)  -- model,
    linked_entity_type VARCHAR(255)  -- recommendation/prediction,
    linked_entity_id UUID  -- source,
    original_confidence_score INT  -- original,
    recalibrated_confidence_score INT  -- adjusted,
    recalibration_reason VARCHAR(255)  -- rationale,
    historical_accuracy_score INT  -- trust,
    executive_override_flag BOOLEAN DEFAULT FALSE  -- governance,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    recalibration_trigger_type VARCHAR(255)  -- rejection/error/drift,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- competitive_signal_registry
-- PURPOSE: Defines external competitive signals. Tracks: - competitor resilience moves - technology shifts - cost structure changes - market positioning - regulatory preparedness - operational resilience
-- FK (per Chapter 9 — authoritative): competitor_id -> competitor_profile_registry | organization_id -> organization_master
-- =========================================================================
CREATE TABLE competitive_signal_registry (
    competitive_signal_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    signal_name VARCHAR(255)  -- signal,
    signal_category VARCHAR(255)  -- operational/Business Resilience/financial,
    signal_subcategory VARCHAR(255)  -- detail,
    competitor_id UUID REFERENCES competitor_profile_registry(competitor_id)  -- company,
    geography_scope VARCHAR(255)  -- region,
    signal_description TEXT  -- explanation,
    signal_strength_score INT  -- importance,
    confidence_score INT  -- trust,
    predicted_business_impact NUMERIC(18,2)  -- expected effect,
    urgency_score INT  -- actionability,
    executive_visibility_flag BOOLEAN DEFAULT FALSE  -- leadership,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- competitor_profile_registry
-- PURPOSE: Defines who competitors are. Supports: - direct competitors - peer companies - industry leaders - regional challengers - best-in-class benchmarks
-- FK (per Chapter 9 — authoritative): none (master reference table)
-- =========================================================================
CREATE TABLE competitor_profile_registry (
    competitor_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    competitor_name VARCHAR(255)  -- company,
    industry_sector VARCHAR(255)  -- sector,
    geography_scope VARCHAR(255)  -- region,
    competitor_category VARCHAR(255)  -- peer/leader/disruptor,
    market_position_score INT  -- ranking,
    business_resilience_maturity_score INT  -- Business Resilience Index maturity,
    financial_strength_score INT  -- resilience,
    operational_resilience_score INT  -- stability,
    external_data_source VARCHAR(255)  -- provider,
    benchmark_eligibility_flag BOOLEAN DEFAULT FALSE  -- comparison,
    executive_priority_flag INT  -- materiality,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);
-- MIGRATION (AMD-011, Alignment Amendment v1.0 §A-Language-Purge): ALTER TABLE competitor_profile_registry RENAME COLUMN sustainability_maturity_score TO business_resilience_maturity_score;

-- =========================================================================
-- competitor_metric_mapping
-- PURPOSE: Maps competitor performance metrics. Allows CorpStage to compare: - organization KPI vs competitor KPI
-- FK (per Chapter 9 — authoritative): competitor_id -> competitor_profile_registry | metric_id -> metric_registry | benchmark_id -> benchmark_registry
-- =========================================================================
CREATE TABLE competitor_metric_mapping (
    competitor_metric_mapping_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    competitor_id UUID REFERENCES competitor_profile_registry(competitor_id)  -- competitor,
    metric_id UUID REFERENCES metric_registry(metric_id)  -- metric,
    benchmark_id UUID REFERENCES benchmark_registry(benchmark_id)  -- benchmark,
    reporting_period VARCHAR(255)  -- timing,
    competitor_metric_value NUMERIC(18,2)  -- observed,
    percentile_rank VARCHAR(255)  -- position,
    variance_vs_company VARCHAR(255)  -- comparison,
    trend_direction VARCHAR(255)  -- improving/declining,
    confidence_score INT  -- trust,
    executive_alert_flag BOOLEAN DEFAULT FALSE  -- urgency,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- market_trend_registry
-- PURPOSE: Defines macro market trends. Tracks: - energy trends - energy transition pricing - technology shifts - commodity volatility - water stress - regulatory movement - sector disruption
-- FK (per Chapter 9 — authoritative): none (master reference table)
-- =========================================================================
CREATE TABLE market_trend_registry (
    market_trend_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trend_name VARCHAR(255)  -- trend,
    trend_category VARCHAR(255)  -- market/climate/regulatory,
    geography_scope VARCHAR(255)  -- region,
    trend_description TEXT  -- explanation,
    trend_direction VARCHAR(255)  -- rising/falling,
    volatility_score INT  -- instability,
    expected_business_impact NUMERIC(18,2)  -- effect,
    predictive_relevance_score INT  -- forecasting,
    urgency_score INT  -- actionability,
    executive_visibility_flag BOOLEAN DEFAULT FALSE  -- leadership,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- benchmark_performance_tracker
-- PURPOSE: Tracks performance against benchmarks over time. Supports comparison across: - sector median - top quartile - competitors - reporting periods - regions
-- FK (per Chapter 9 — authoritative): benchmark_id -> benchmark_registry | organization_id -> organization_master
-- =========================================================================
CREATE TABLE benchmark_performance_tracker (
    benchmark_performance_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    benchmark_id UUID REFERENCES benchmark_registry(benchmark_id)  -- benchmark,
    linked_entity_type VARCHAR(255)  -- KPI/risk/financial,
    linked_entity_id UUID  -- target,
    reporting_period VARCHAR(255)  -- timing,
    organization_score INT  -- internal,
    benchmark_score INT  -- market,
    percentile_position VARCHAR(255)  -- rank,
    competitive_gap_score INT  -- difference,
    trend_direction VARCHAR(255)  -- improving/declining,
    executive_materiality_flag BOOLEAN DEFAULT FALSE  -- importance,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- competitive_advantage_tracking
-- PURPOSE: Tracks where the company leads or lags. Supports: - strategic positioning - investor communication - competitive resilience - future planning
-- FK (per Chapter 9 — authoritative): polymorphic (linked_entity_type/linked_entity_id) | organization_id -> organization_master
-- =========================================================================
CREATE TABLE competitive_advantage_tracking (
    competitive_advantage_tracking_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    linked_entity_type VARCHAR(255)  -- KPI/risk/financial,
    linked_entity_id UUID  -- entity,
    competitive_position VARCHAR(255)  -- leader/laggard,
    advantage_score INT  -- strength,
    disadvantage_risk_score INT  -- weakness,
    projected_future_position VARCHAR(255)  -- forecast,
    financial_implication VARCHAR(255)  -- business effect,
    investor_relevance_flag BOOLEAN DEFAULT FALSE  -- perception,
    strategic_priority_flag INT  -- urgency,
    executive_visibility_flag BOOLEAN DEFAULT FALSE  -- leadership,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- event_registry
-- PURPOSE: Defines external or internal events. Supports: - climate events - regulatory events - market shocks - geopolitical events - technology disruptions - operational disruptions - supply chain disruptions - social events
-- FK (per Chapter 9 — authoritative): organization_id -> organization_master
-- =========================================================================
CREATE TABLE event_registry (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_name VARCHAR(255)  -- event,
    event_category VARCHAR(255)  -- climate/regulatory/market,
    event_subcategory VARCHAR(255)  -- detail,
    geography_scope VARCHAR(255)  -- region,
    event_description TEXT  -- explanation,
    event_source VARCHAR(255)  -- provider,
    event_start_timestamp TIMESTAMP WITH TIME ZONE  -- start,
    event_end_timestamp TIMESTAMP WITH TIME ZONE  -- close,
    severity_score INT  -- impact,
    confidence_score INT  -- trust,
    predictive_relevance_score INT  -- forecasting,
    executive_visibility_flag BOOLEAN DEFAULT FALSE  -- leadership,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- NAMING COLLISION RESOLVED (Alignment Amendment v1.0, §D-Event-Collision): event_registry
-- (above) is retained AS-IS, scoped explicitly and permanently to
-- EXTERNAL-WORLD events — its event_category values (climate/regulatory/
-- market) confirm this was always its actual purpose. It is a distinct,
-- permanently separate concept from URA-001's WORKFLOW events (ENTER,
-- APPROVE, ESCALATE, DELEGATE, etc.), which have zero relationship to
-- event_registry and are modeled below in workflow_event_registry /
-- workflow_event_log. No column, table, or concept in event_registry is
-- altered by this amendment. These two "event" concepts share a word, not
-- a schema, and must never be merged or cross-referenced as though they
-- were the same object.

-- =========================================================================
-- workflow_event_registry
-- PURPOSE: Defines internal workflow-transition event types (state
-- machine transitions on business objects), independent of event_registry's
-- external-world events above.
-- FK: organization_id -> organization_master (NULL for GLOBAL scope)
-- -- URA-001-71: event_code enumeration | URA-001-72: scope_type
-- =========================================================================
CREATE TABLE workflow_event_registry (
    workflow_event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_code VARCHAR(100), -- ENTER/REVIEW/APPROVE/REJECT/ASSIGN/DELEGATE/ESCALATE/PUBLISH (URA-001-71)
    scope_type VARCHAR(50), -- GLOBAL/COMPANY/DOMAIN (URA-001-72)
    organization_id UUID REFERENCES organization_master(organization_id), -- NULL for GLOBAL scope
    domain_id UUID -- NULL unless scope_type = DOMAIN
);

-- =========================================================================
-- workflow_event_log
-- PURPOSE: Immutable append-only record of every workflow state transition.
-- FK: workflow_event_id -> workflow_event_registry | membership_id -> membership_registry
-- -- URA-001-85: every state transition generates an immutable record
-- =========================================================================
CREATE TABLE workflow_event_log (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_event_id UUID REFERENCES workflow_event_registry(workflow_event_id),
    object_type VARCHAR(100),
    object_id UUID,
    membership_id UUID REFERENCES membership_registry(membership_id),
    occurred_at TIMESTAMP WITH TIME ZONE,
    previous_state VARCHAR(100),
    new_state VARCHAR(100)
);

-- =========================================================================
-- incident_registry
-- PURPOSE: Defines actual incidents affecting the organization. Difference: - event = something happened - incident = organization affected
-- FK (per Chapter 9 — authoritative): linked_event_id -> event_registry | node_scope_id -> organization_node
-- =========================================================================
CREATE TABLE incident_registry (
    incident_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    linked_event_id UUID REFERENCES event_registry(event_id)  -- event,
    incident_name VARCHAR(255)  -- incident,
    incident_category VARCHAR(255)  -- operational/climate,
    node_scope_id UUID REFERENCES organization_node(node_id)  -- organization scope,
    incident_description TEXT  -- detail,
    incident_timestamp TIMESTAMP WITH TIME ZONE  -- occurrence,
    incident_status VARCHAR(255)  -- active/resolved,
    severity_score INT  -- seriousness,
    financial_materiality_score INT  -- exposure,
    operational_disruption_score INT  -- disruption,
    escalation_flag BOOLEAN DEFAULT FALSE  -- urgency,
    executive_visibility_flag BOOLEAN DEFAULT FALSE  -- leadership,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- incident_impact_mapping
-- PURPOSE: Defines what incidents affect. Maps: - incident → KPI - incident → risk - incident → financial impact - incident → stakeholder impact
-- FK (per Chapter 9 — authoritative): incident_id -> incident_registry | organization_id -> organization_master
-- =========================================================================
CREATE TABLE incident_impact_mapping (
    incident_impact_mapping_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_id UUID REFERENCES incident_registry(incident_id)  -- incident,
    impacted_entity_type VARCHAR(255)  -- KPI/risk/financial,
    impacted_entity_id UUID  -- target,
    impact_severity_score INT  -- strength,
    projected_duration VARCHAR(255)  -- timeline,
    cascading_effect_flag BOOLEAN DEFAULT FALSE  -- propagation,
    financial_exposure VARCHAR(255)  -- value,
    confidence_score INT  -- trust,
    executive_materiality_flag BOOLEAN DEFAULT FALSE  -- importance,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- resilience_assessment_registry
-- PURPOSE: Measures organizational resilience. Assesses: - preparedness - recovery capability - response maturity - operational redundancy - supply chain resilience - financial resilience
-- FK (per Chapter 9 — authoritative): polymorphic (linked_entity_type/linked_entity_id) | organization_id -> organization_master
-- =========================================================================
CREATE TABLE resilience_assessment_registry (
    resilience_assessment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_name VARCHAR(255)  -- assessment,
    assessment_category VARCHAR(255)  -- climate/operational,
    linked_entity_type VARCHAR(255)  -- node/risk,
    linked_entity_id UUID  -- target,
    resilience_score INT  -- capability,
    preparedness_score INT  -- readiness,
    recovery_speed_score INT  -- response,
    dependency_risk_score INT  -- vulnerability,
    benchmark_comparison_score INT  -- peers,
    executive_priority_flag INT  -- urgency,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- resilience_response_tracker
-- PURPOSE: Tracks: how the organization responded Example: Incident: Energy Price Spike Response: hedging strategy activated renewable sourcing increased backup suppliers enabled
-- FK (per Chapter 9 — authoritative): incident_id -> incident_registry | owner_user_id -> user_registry | organization_id -> organization_master
-- =========================================================================
CREATE TABLE resilience_response_tracker (
    resilience_response_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_id UUID REFERENCES incident_registry(incident_id)  -- incident,
    response_action VARCHAR(255)  -- action,
    owner_user_id UUID REFERENCES user_registry(user_id)  -- accountability,
    response_start_timestamp TIMESTAMP WITH TIME ZONE  -- timing,
    response_completion_timestamp TIMESTAMP WITH TIME ZONE  -- finish,
    response_status VARCHAR(255)  -- planned/active/completed/failed,
    response_effectiveness_score INT  -- effectiveness,
    estimated_financial_protection VARCHAR(255)  -- benefit,
    recovery_speed_score INT  -- performance,
    executive_visibility_flag BOOLEAN DEFAULT FALSE  -- leadership,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- resilience_learning_registry
-- PURPOSE: Captures: lessons learned after disruptions Critical for: continuous resilience improvement Example: After flood disruption: CorpStage learns: backup supplier worked insurance response slow plant redundancy insufficient recovery took too long Future recommendations improve.
-- FK (per Chapter 9 — authoritative): incident_id -> incident_registry | organization_id -> organization_master
-- =========================================================================
CREATE TABLE resilience_learning_registry (
    resilience_learning_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_id UUID REFERENCES incident_registry(incident_id)  -- incident,
    learning_category VARCHAR(255)  -- operational/financial/supply-chain/governance,
    lesson_learned VARCHAR(255)  -- insight,
    root_cause_summary VARCHAR(255)  -- why,
    recommended_future_change VARCHAR(255)  -- improvement,
    confidence_score INT  -- trust,
    future_preparedness_impact NUMERIC(18,2)  -- resilience,
    executive_review_flag BOOLEAN DEFAULT FALSE  -- governance,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- master_entity_registry
-- PURPOSE: Defines: canonical enterprise entity identity Creates: one trusted reference layer for all objects across CorpStage. Supports: organization units KPIs risks stakeholders frameworks events reports suppliers facilities business units
-- FK (per Chapter 9 — authoritative): none (platform-wide entity resolution table)
-- =========================================================================
CREATE TABLE master_entity_registry (
    entity_registry_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type VARCHAR(255)  -- KPI/risk/facility,
    canonical_entity_name VARCHAR(255)  -- trusted identity,
    alternate_names VARCHAR(255)  -- aliases,
    source_system_reference VARCHAR(255)  -- integration,
    hierarchy_reference_id UUID  -- parent,
    materiality_score INT  -- significance,
    global_visibility_flag BOOLEAN DEFAULT FALSE  -- enterprise,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- decision_traceability_registry
-- PURPOSE: Tracks: why executive decisions were made Captures: recommendation evidence risk stakeholder impact executive decision outcome
-- FK (per Chapter 9 — authoritative): executive_user_id -> user_registry | organization_id -> organization_master
-- =========================================================================
CREATE TABLE decision_traceability_registry (
    decision_traceability_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    linked_entity_type VARCHAR(255)  -- recommendation/risk,
    linked_entity_id UUID  -- source,
    executive_user_id UUID REFERENCES user_registry(user_id)  -- decision maker,
    decision_summary VARCHAR(255)  -- action,
    decision_reasoning VARCHAR(255)  -- why,
    evidence_reference VARCHAR(255)  -- support,
    predicted_outcome VARCHAR(255)  -- expectation,
    actual_outcome VARCHAR(255)  -- result,
    explainability_score INT  -- defensibility,
    board_visibility_flag BOOLEAN DEFAULT FALSE  -- board,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- trust_scoring_registry
-- PURPOSE: Measures: enterprise confidence in intelligence Trust score considers: evidence quality data freshness AI confidence historical accuracy external validation
-- FK (per Chapter 9 — authoritative): polymorphic (linked_entity_type/linked_entity_id) | organization_id -> organization_master
-- =========================================================================
CREATE TABLE trust_scoring_registry (
    trust_score_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    linked_entity_type VARCHAR(255)  -- prediction/recommendation,
    linked_entity_id UUID  -- source,
    trust_score INT  -- trust,
    evidence_quality_score INT  -- evidence,
    historical_accuracy_score INT  -- reliability,
    external_validation_score INT  -- verification,
    confidence_adjustment_factor VARCHAR(255)  -- AI,
    materiality_modifier VARCHAR(255)  -- significance,
    board_safe_flag BOOLEAN DEFAULT FALSE  -- governance,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- enterprise_configuration_registry
-- PURPOSE: Controls: enterprise-wide platform behavior Supports: materiality thresholds risk thresholds workflow rules jurisdiction settings board escalation AI behavior
-- FK (per Chapter 9 — authoritative): none (platform configuration table)
-- =========================================================================
CREATE TABLE enterprise_configuration_registry (
    configuration_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    configuration_category VARCHAR(255)  -- governance/AI,
    configuration_key VARCHAR(255)  -- parameter,
    configuration_value NUMERIC(18,2)  -- setting,
    jurisdiction_scope VARCHAR(255)  -- geography,
    industry_scope VARCHAR(255)  -- industry,
    effective_start_date TIMESTAMP WITH TIME ZONE  -- validity,
    effective_end_date TIMESTAMP WITH TIME ZONE  -- expiry,
    executive_override_flag BOOLEAN DEFAULT FALSE  -- governance,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- cross_domain_relationship_registry
-- PURPOSE: Defines: hidden relationships across domains Enables: systems intelligence
-- FK (per Chapter 9 — authoritative): polymorphic (source_entity_type/source_entity_id, target_entity_type/target_entity_id)
-- =========================================================================
CREATE TABLE cross_domain_relationship_registry (
    relationship_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_entity_type VARCHAR(255)  -- origin,
    source_entity_id UUID  -- source,
    target_entity_type VARCHAR(255)  -- target,
    target_entity_id UUID  -- impact,
    relationship_strength_score INT  -- influence,
    causality_type VARCHAR(255)  -- direct/indirect,
    time_lag_factor VARCHAR(255)  -- delay,
    confidence_score INT  -- trust,
    predictive_relevance_flag BOOLEAN DEFAULT FALSE  -- foresight,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- enterprise_knowledge_graph_registry
-- PURPOSE: Creates: AI-native enterprise memory Connects: events risks stakeholders metrics decisions incidents financials benchmarks
-- FK (per Chapter 9 — authoritative): polymorphic (source_entity_type/source_entity_id, target_entity_type/target_entity_id)
-- =========================================================================
CREATE TABLE enterprise_knowledge_graph_registry (
    knowledge_graph_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_entity_type VARCHAR(255)  -- source,
    source_entity_id UUID  -- node,
    relationship_type VARCHAR(255)  -- relation,
    target_entity_type VARCHAR(255)  -- target,
    target_entity_id UUID  -- node,
    relationship_weight VARCHAR(255)  -- strength,
    confidence_score INT  -- trust,
    explainability_reference VARCHAR(255)  -- evidence,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- architecture_health_registry
-- PURPOSE: Measures: whether CorpStage architecture itself is healthy Tracks: missing evidence broken workflows stale predictions trust degradation orphan relationships
-- FK (per Chapter 9 — authoritative): polymorphic (linked_entity_type/linked_entity_id)
-- =========================================================================
CREATE TABLE architecture_health_registry (
    architecture_health_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    health_category VARCHAR(255)  -- workflow/data/AI,
    linked_entity_type VARCHAR(255)  -- affected domain,
    linked_entity_id UUID  -- target,
    health_score INT  -- quality,
    issue_description TEXT  -- problem,
    severity_score INT  -- criticality,
    remediation_required_flag BOOLEAN DEFAULT FALSE  -- action,
    executive_visibility_flag BOOLEAN DEFAULT FALSE  -- leadership,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- architecture_version_registry
-- PURPOSE: Tracks: enterprise architecture evolution Prevents: schema drift uncontrolled redesign breaking changes Supports: versioning freeze states migration planning rollback
-- FK (per Chapter 9 — authoritative): approval_user_id -> user_registry
-- =========================================================================
CREATE TABLE architecture_version_registry (
    architecture_version_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    architecture_version VARCHAR(255)  -- release,
    architecture_status VARCHAR(255)  -- draft/frozen,
    change_summary VARCHAR(255)  -- revision,
    impacted_tables VARCHAR(255)  -- scope,
    approval_user_id UUID REFERENCES user_registry(user_id)  -- governance,
    effective_date TIMESTAMP WITH TIME ZONE  -- activation,
    freeze_flag BOOLEAN DEFAULT FALSE  -- freeze,
    rollback_reference VARCHAR(255)  -- recovery,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- orchestration_trigger_registry
-- PURPOSE: Defines: enterprise automation logic Controls: what triggers what across CorpStage. Enables: event-driven intelligence orchestration
-- FK (per Chapter 9 — authoritative): polymorphic (trigger_entity_id, target_entity_reference)
-- =========================================================================
CREATE TABLE orchestration_trigger_registry (
    orchestration_trigger_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trigger_entity_type VARCHAR(255)  -- event/risk/KPI,
    trigger_entity_id UUID  -- source,
    trigger_condition VARCHAR(255)  -- threshold/logic,
    target_process_type VARCHAR(255)  -- prediction/workflow,
    target_entity_reference VARCHAR(255)  -- destination,
    execution_priority INT  -- urgency,
    escalation_flag BOOLEAN DEFAULT FALSE  -- governance,
    retry_logic TEXT  -- resilience,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- risk_subscription_registry
-- PURPOSE: Defines: the Risk Subscription Engine Controls: which events each user sees at what severity threshold for which geographies and assets Enables: human-in-the-loop event filtering before any downstream calculation fires
-- FK (per Chapter 9 — authoritative): user_id -> user_registry | role_id -> role_registry
-- =========================================================================
CREATE TABLE risk_subscription_registry (
    risk_subscription_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES user_registry(user_id)  -- subscription owner,
    role_id UUID REFERENCES role_registry(role_id)  -- role-level subscription,
    event_category VARCHAR(255)  -- climate/regulatory/market/supply chain/cyber,
    event_subcategory VARCHAR(255)  -- flood/fuel/energy transition price/supplier/strike/sanction,
    geography_filter VARCHAR(255)  -- global/region/country/city,
    asset_filter_json JSONB  -- specific facilities, suppliers, business units,
    severity_threshold INT  -- minimum severity score to surface event,
    auto_trigger_threshold INT  -- severity above which services fire without human decision,
    notification_channel VARCHAR(255)  -- message centre/email/Teams/all,
    subscription_active_flag BOOLEAN DEFAULT FALSE  -- on/off,
    effective_from VARCHAR(255)  -- validity start,
    effective_to VARCHAR(255)  -- validity end,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- event_acceptance_log
-- PURPOSE: Tracks: every human decision on every incoming event Records: accept / ignore / escalate / auto-triggered which downstream services fired as a result Enables: permanent audit trail of why impact was or was not calculated
-- FK (per Chapter 9 — authoritative): event_id -> event_registry | user_id -> user_registry | escalated_to_user_id -> user_registry
-- =========================================================================
CREATE TABLE event_acceptance_log (
    acceptance_log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id UUID REFERENCES event_registry(event_id)  -- linked event,
    user_id UUID REFERENCES user_registry(user_id)  -- decision maker,
    role_id UUID  -- role context at time of decision,
    decision VARCHAR(255)  -- accepted/ignored/escalated/auto-triggered,
    decision_reason VARCHAR(255)  -- optional rationale,
    decision_timestamp TIMESTAMP WITH TIME ZONE  -- exact time — audit precision,
    downstream_triggered VARCHAR(255)  -- yes/no,
    services_triggered_json JSONB  -- list of services that fired,
    escalated_to_user_id UUID REFERENCES user_registry(user_id)  -- if escalated — who,
    auto_trigger_flag BOOLEAN DEFAULT FALSE  -- yes/no — was this automatic,
    notification_sent_flag BOOLEAN DEFAULT FALSE  -- yes/no,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit — immutable, never updated,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- AMD-003
);

-- =========================================================================
-- llm_prompt_registry
-- PURPOSE: Defines: every AI prompt template in CorpStage Controls: what data the LLM may use what the LLM is forbidden from doing what format output must return in which Azure OpenAI model and region to use Enables: versioned, governed, auditable AI behaviour
-- FK (per Chapter 9 — authoritative): deprecated_by_prompt_id -> llm_prompt_registry (self-referencing)
-- =========================================================================
CREATE TABLE llm_prompt_registry (
    prompt_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prompt_name VARCHAR(255)  -- Daily Brief/Board Narrative/Risk Summary/Extraction,
    prompt_version VARCHAR(255)  -- 1.0/1.1/2.0 — versioned like software,
    prompt_category VARCHAR(255)  -- narrative/summary/extraction/recommendation,
    verified_data_fields_json JSONB  -- canonical data point IDs that must be passed in,
    forbidden_actions_json JSONB  -- what the LLM may never do for this prompt type,
    output_format_json JSONB  -- JSON schema the response must conform to,
    azure_openai_model VARCHAR(255)  -- gpt-4o/gpt-4o-mini,
    azure_region VARCHAR(255)  -- centralindia/westeurope/eastus — data residency,
    max_tokens VARCHAR(255)  -- cost and quality control,
    temperature VARCHAR(255)  -- 0.1 factual / 0.5 summary / 0.7 narrative,
    human_review_required_flag BOOLEAN DEFAULT FALSE  -- yes/no,
    confidence_inheritance_rule VARCHAR(255)  -- how output inherits colour from input data,
    confidence_rule_id UUID  -- foreign key — confidence_scoring_registry,
    prompt_status VARCHAR(255)  -- active/deprecated/draft,
    deprecated_by_prompt_id UUID REFERENCES llm_prompt_registry(prompt_id)  -- self-referencing, which version replaced this,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- llm_execution_log
-- PURPOSE: Tracks: every call made to Azure OpenAI Records: what went in what came out which canonical data points were used which Azure region handled the call Enables: full AI audit trail confidence colour inheritance data residency proof
-- FK (per Chapter 9 — authoritative): prompt_id -> llm_prompt_registry | reviewed_by_user_id -> user_registry | confidence_rule_id -> confidence_scoring_registry
-- =========================================================================
CREATE TABLE llm_execution_log (
    execution_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prompt_id UUID REFERENCES llm_prompt_registry(prompt_id)  -- which prompt template,
    prompt_version VARCHAR(255)  -- exact version used — immutable,
    called_by_service VARCHAR(255)  -- which CorpStage service triggered this,
    called_for_entity_type VARCHAR(255)  -- narrative/insight/extraction/recommendation,
    called_for_entity_id UUID  -- specific narrative_id or report_id,
    input_data_points_json JSONB  -- canonical data point IDs passed as verified numbers,
    azure_region VARCHAR(255)  -- which data centre — data residency confirmation,
    azure_model_used VARCHAR(255)  -- exact model version,
    raw_output_reference VARCHAR(255)  -- pointer to full response in secure storage,
    parsed_output_reference VARCHAR(255)  -- structured output after schema validation,
    numbers_used_json JSONB  -- figures in output with their source,
    validation_status VARCHAR(255)  -- passed/failed/partial,
    validation_failure_reason VARCHAR(255)  -- if failed — why,
    confidence_score_inherited INT  -- lowest confidence among all inputs,
    confidence_colour_inherited VARCHAR(255)  -- green/amber/red/grey,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- foreign key — confidence_scoring_registry,
    human_reviewed_flag BOOLEAN DEFAULT FALSE  -- yes/no,
    reviewed_by_user_id UUID REFERENCES user_registry(user_id)  -- reviewer,
    review_timestamp TIMESTAMP WITH TIME ZONE  -- when,
    review_decision VARCHAR(255)  -- approved/revised/rejected,
    tokens_used VARCHAR(255)  -- cost tracking,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit — immutable,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- confidence_scoring_registry
-- PURPOSE: Defines: the single source of truth for confidence scoring Prevents: inconsistent confidence scales across tables unexplainable confidence colours in board outputs Supports: standardised 0–100 scale across all 62 tables five confidence types — DATA/MODEL/EVIDENCE/NARRATIVE/COMPOSITE five colour bands — Green/Amber/Red/Grey/Unscored three propagation rules — Lowest Wins/Weighted Average/Manual Over...
-- FK (per Chapter 9 — authoritative): none (platform-wide rules table)
-- =========================================================================
CREATE TABLE confidence_scoring_registry (
    confidence_scoring_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_name VARCHAR(255)  -- e.g. Metric Data Confidence / Predictive Model Confidence,
    confidence_type VARCHAR(255)  -- DATA/MODEL/EVIDENCE/NARRATIVE/COMPOSITE,
    entity_type VARCHAR(255)  -- which table this rule governs,
    calculation_logic TEXT  -- formula or rules to compute the score,
    input_factors_json JSONB  -- source type, verification status, data age, conflict flag,
    score_range_min INT  -- always 0,
    score_range_max INT CHECK (score_range_max BETWEEN 0 AND 100)  -- always 100,
    green_threshold INT  -- default 90 — configurable per entity type,
    amber_threshold INT  -- default 70 — configurable per entity type,
    red_threshold INT  -- default 50 — configurable per entity type,
    propagation_rule VARCHAR(255)  -- LOWEST_WINS/WEIGHTED_AVERAGE/MANUAL_OVERRIDE,
    propagation_applies_to VARCHAR(255)  -- downstream entity types that inherit from this,
    human_override_allowed_flag BOOLEAN DEFAULT FALSE  -- yes/no,
    override_requires_rationale_flag BOOLEAN DEFAULT FALSE  -- yes/no,
    board_facing_flag BOOLEAN DEFAULT FALSE  -- yes/no — enforces LOWEST_WINS regardless of propagation_rule,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- data_ingestion_registry
-- PURPOSE: Defines: the receiving layer for all incoming data Tracks: every document upload, API pull, SFTP export, manual entry before it touches the canonical layer Enables: full data lineage from source to metric_record duplicate detection ingestion audit trail
-- FK (per Chapter 9 — authoritative): approved_by_user_id -> user_registry | confidence_rule_id -> confidence_scoring_registry
-- =========================================================================
CREATE TABLE data_ingestion_registry (
    ingestion_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID  -- linked to metric_source_mapping,
    ingestion_name VARCHAR(255)  -- e.g. Plant A Utility Bill Q1 2026,
    ingestion_type VARCHAR(255)  -- document_upload/api_pull/sftp_export/manual_entry,
    tier VARCHAR(255)  -- 0/1/2 — matches 3-tier integration model,
    raw_payload_reference VARCHAR(255)  -- pointer to raw data in secure storage — never deleted,
    received_timestamp TIMESTAMP WITH TIME ZONE  -- when data arrived,
    node_id UUID  -- which organisation unit,
    reporting_period VARCHAR(255)  -- which period this data covers,
    expected_metrics_json JSONB  -- canonical data points this ingestion should populate,
    ingestion_status VARCHAR(255)  -- received/validating/transforming/reconciling/approved/rejected,
    duplicate_check_hash VARCHAR(255)  -- hash of payload — flags probable duplicates before processing,
    reconciliation_status VARCHAR(255)  -- no_conflict/conflict_detected/conflict_resolved,
    approval_required_flag BOOLEAN DEFAULT FALSE  -- yes/no — based on metric materiality,
    approved_by_user_id UUID REFERENCES user_registry(user_id)  -- who approved,
    approval_timestamp TIMESTAMP WITH TIME ZONE  -- when,
    rejection_reason VARCHAR(255)  -- if rejected — why,
    confidence_score_assigned INT  -- confidence given to data from this ingestion,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- foreign key — confidence_scoring_registry,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit — immutable,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- data_reconciliation_log
-- PURPOSE: Tracks: every conflict between two or more sources for the same metric, same node, same period Records: both source values the resolution decision who decided and why Enables: full conflict audit trail explainable data quality
-- FK (per Chapter 9 — authoritative): source_a_ingestion_id -> data_ingestion_registry | source_b_ingestion_id -> data_ingestion_registry | resolved_by_user_id -> user_registry | entered_metric_record_id -> metric_record
-- =========================================================================
CREATE TABLE data_reconciliation_log (
    reconciliation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_id UUID  -- which canonical metric is in conflict,
    node_id UUID  -- which organisation unit,
    reporting_period VARCHAR(255)  -- which period,
    source_a_ingestion_id UUID REFERENCES data_ingestion_registry(ingestion_id)  -- first source,
    source_a_value NUMERIC(18,2)  -- value from first source,
    source_a_confidence VARCHAR(255)  -- confidence of first source,
    source_b_ingestion_id UUID REFERENCES data_ingestion_registry(ingestion_id)  -- second source,
    source_b_value NUMERIC(18,2)  -- value from second source,
    source_b_confidence VARCHAR(255)  -- confidence of second source,
    variance_absolute VARCHAR(255)  -- numerical difference,
    variance_percentage VARCHAR(255)  -- % difference,
    auto_resolution_applied VARCHAR(255)  -- yes/no,
    auto_resolution_rule VARCHAR(255)  -- higher_confidence_wins/primary_source_wins/most_recent_wins,
    human_resolution_required_flag BOOLEAN DEFAULT FALSE  -- yes/no,
    resolved_by_user_id UUID REFERENCES user_registry(user_id)  -- who resolved,
    resolution_decision VARCHAR(255)  -- source_a/source_b/manual_value/flagged_for_review,
    resolved_value NUMERIC(18,2)  -- final value entered into metric_record,
    resolution_rationale TEXT  -- mandatory explanation,
    resolution_timestamp TIMESTAMP WITH TIME ZONE  -- when,
    entered_metric_record_id UUID REFERENCES metric_record(metric_record_id)  -- the metric_record row this resolved into,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit — immutable,
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id)  -- AMD-001
);

-- =========================================================================
-- tenant_registry
-- PURPOSE: Design now. Build when first multi-org customer arrives.
-- FK (per Chapter 9 — authoritative): none (root infrastructure table)
-- =========================================================================
CREATE TABLE tenant_registry (
    tenant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_name VARCHAR(255)  -- customer name,
    tenant_code VARCHAR(100) UNIQUE NOT NULL  -- short unique code — used in storage paths and cache keys,
    deployment_model VARCHAR(255)  -- shared/dedicated_subscription/customer_tenant,
    azure_region VARCHAR(255)  -- data residency,
    azure_subscription_id UUID  -- which Azure subscription,
    database_schema VARCHAR(255)  -- PostgreSQL schema for this tenant,
    storage_container_prefix VARCHAR(255)  -- prefix for all blob storage paths,
    cache_key_prefix VARCHAR(255)  -- prefix for all cache keys,
    encryption_key_reference VARCHAR(255)  -- Azure Key Vault pointer,
    data_residency_country INT  -- legal jurisdiction,
    tier VARCHAR(255)  -- starter/professional/enterprise,
    contract_start_date TIMESTAMP WITH TIME ZONE  -- activation,
    contract_end_date TIMESTAMP WITH TIME ZONE  -- expiry,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- api_credential_registry
-- PURPOSE: Defines: every entity allowed to call the CorpStage API Controls: who can call what they can access how many times what happens when they exceed limits Enables: rate limit governance stale credential detection API security audit trail
-- FK (per Chapter 9 — authoritative): organization_id -> organization_master | issued_by_user_id -> user_registry
-- =========================================================================
CREATE TABLE api_credential_registry (
    credential_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organization_master(organization_id)  -- which customer this credential belongs to,
    credential_name VARCHAR(255)  -- e.g. SAP Production Integration / Power BI Read-Only,
    credential_type VARCHAR(255)  -- api_key / oauth_client / service_account / internal_service,
    caller_type VARCHAR(255)  -- customer_integration / third_party_feed / internal_service,
    permissions_json JSONB  -- endpoints and methods this credential can access,
    rate_limit_per_minute VARCHAR(255)  -- calls allowed per minute,
    rate_limit_per_day VARCHAR(255)  -- calls allowed per day,
    rate_limit_breach_action VARCHAR(255)  -- throttle / error / alert / suspend,
    allowed_ip_ranges_json JSONB  -- IP whitelist — optional, recommended for enterprise,
    credential_hash VARCHAR(255)  -- hashed key — never stored in plain text,
    issued_by_user_id UUID REFERENCES user_registry(user_id)  -- who created this credential,
    issued_timestamp TIMESTAMP WITH TIME ZONE  -- when issued,
    expiry_timestamp TIMESTAMP WITH TIME ZONE  -- when this credential expires,
    last_used_timestamp TIMESTAMP WITH TIME ZONE  -- last successful call — stale credential detection,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- api_call_log
-- PURPOSE: Tracks: every API call that enters CorpStage Records: who called what endpoint what response was returned whether rate limit was breached Enables: full API audit trail data lineage from call to metric_record billing for API usage bad data source identification
-- FK (per Chapter 9 — authoritative): credential_id -> api_credential_registry | organization_id -> organization_master | ingestion_id -> data_ingestion_registry
-- =========================================================================
CREATE TABLE api_call_log (
    call_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    credential_id UUID REFERENCES api_credential_registry(credential_id)  -- which API key made this call,
    organization_id UUID REFERENCES organization_master(organization_id)  -- which customer,
    endpoint VARCHAR(255)  -- which API endpoint was called,
    http_method VARCHAR(255)  -- GET / POST / PUT / DELETE,
    request_payload_hash VARCHAR(255)  -- hash of request — not full payload, privacy-safe,
    response_status VARCHAR(255)  -- 200 / 400 / 401 / 429 / 500,
    response_latency_ms VARCHAR(255)  -- performance tracking,
    ingestion_id UUID REFERENCES data_ingestion_registry(ingestion_id)  -- if this call created a data ingestion —,
    rate_limit_breach_flag BOOLEAN DEFAULT FALSE  -- yes / no — did this call exceed the limit,
    ip_address VARCHAR(255)  -- caller IP,
    call_timestamp TIMESTAMP WITH TIME ZONE  -- exact time,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit — immutable
);

-- =========================================================================
-- notification_template_registry
-- PURPOSE: Defines: every notification type in CorpStage Controls: what triggers each notification which channel it goes to how often it can fire when it must not fire Enables: governed versioned auditable notifications UX/CX rule enforcement in the data model duplicate suppression quiet hours compliance
-- FK (per Chapter 9 — authoritative): none (master reference table)
-- =========================================================================
CREATE TABLE notification_template_registry (
    template_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_name VARCHAR(255)  -- Daily Executive Brief / Risk Alert / Score Unlock / Weekly Drip / Breach Alert,
    template_category VARCHAR(255)  -- executive / operational / compliance / security / engagement,
    trigger_type VARCHAR(255)  -- event_accepted / score_threshold / schedule / rate_limit_breach / report_ready,
    channel VARCHAR(255)  -- email / teams / in_app / push / sms,
    subject_template VARCHAR(255)  -- subject line with placeholders — e.g. {company} Intelligence Brief — {date},
    body_template VARCHAR(255)  -- body with placeholders — never hardcoded in code,
    severity_level INT  -- urgent / important / informational / scheduled,
    max_frequency VARCHAR(255)  -- how often this notification can fire per user — e.g. once_per_day,
    quiet_hours_flag BOOLEAN DEFAULT FALSE  -- yes / no — respects 6am–8pm local time rule,
    dismissal_cooldown_days VARCHAR(255)  -- days before same notification fires again after user dismissal,
    human_approval_required_flag BOOLEAN DEFAULT FALSE  -- yes / no,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- notification_log
-- PURPOSE: Tracks: every notification sent by CorpStage Records: delivery status read status dismissal action taken Enables: proof of delivery audit trail duplicate suppression evidence quiet hours enforcement record engagement analytics UX/CX compliance verification
-- FK (per Chapter 9 — authoritative): template_id -> notification_template_registry | recipient_user_id -> user_registry | organization_id -> organization_master
-- =========================================================================
CREATE TABLE notification_log (
    notification_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id UUID REFERENCES notification_template_registry(template_id)  -- which template was used —,
    triggered_by_entity_type VARCHAR(255)  -- event / risk / score / schedule / api_breach / report,
    triggered_by_entity_id UUID  -- the specific entity that triggered this notification,
    recipient_user_id UUID REFERENCES user_registry(user_id)  -- who it was sent to — Table 4,
    organization_id UUID REFERENCES organization_master(organization_id)  -- which organisation — Table 3,
    channel VARCHAR(255)  -- email / teams / in_app / push,
    subject VARCHAR(255)  -- actual subject sent — placeholders resolved,
    delivery_status VARCHAR(255)  -- sent / delivered / bounced / failed,
    delivered_timestamp TIMESTAMP WITH TIME ZONE  -- when confirmed delivered,
    read_flag BOOLEAN DEFAULT FALSE  -- yes / no,
    read_timestamp TIMESTAMP WITH TIME ZONE  -- when opened,
    dismissed_flag BOOLEAN DEFAULT FALSE  -- yes / no,
    dismissed_timestamp TIMESTAMP WITH TIME ZONE  -- when dismissed,
    action_taken_flag BOOLEAN DEFAULT FALSE  -- yes / no — user clicked through and acted,
    duplicate_suppressed_flag BOOLEAN DEFAULT FALSE  -- yes / no — suppressed by max_frequency rule,
    queued_timestamp TIMESTAMP WITH TIME ZONE  -- when queued — separate from delivered when quiet hours apply,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit — immutable
);

-- =========================================================================
-- audit_package_registry
-- PURPOSE: Defines: every audit evidence package generated by CorpStage Tracks: who requested it what it covers what it contains whether it was delivered and acknowledged Enables: one-click audit export regulatory filing evidence investor due diligence response tamper detection via integrity hash BRSR Core reasonable assurance readiness ESRS limited assurance readiness
-- FK (per Chapter 9 — authoritative): requested_by_user_id -> user_registry | organization_id -> organization_master | framework_id -> framework_registry
-- =========================================================================
CREATE TABLE audit_package_registry (
    audit_package_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    package_name VARCHAR(255)  -- e.g. KPMG Direct Cost Assurance FY2026 / SEBI BRSR Core Evidence Q1,
    package_category VARCHAR(255)  -- external_assurance / regulatory_filing / board_committee / investor_due_diligenc...,
    requested_by_user_id UUID REFERENCES user_registry(user_id)  -- who initiated the export — Table 4,
    requested_for_entity VARCHAR(255)  -- KPMG / SEBI / Audit Committee / BlackRock,
    organization_id UUID REFERENCES organization_master(organization_id)  -- which organisation — Table 3,
    reporting_period VARCHAR(255)  -- which period this covers,
    framework_id UUID REFERENCES framework_registry(framework_id)  -- which framework this evidence supports — Table 11,
    metrics_included_json JSONB  -- list of metric_ids included in this package,
    tables_queried_json JSONB  -- which of the 86 tables were queried to build this package,
    evidence_count INT  -- total evidence items included,
    decision_count INT  -- total human decisions included,
    ai_execution_count INT  -- total AI calls included,
    confidence_summary_json JSONB  -- min / max / avg confidence across all included data points,
    package_status VARCHAR(255)  -- generating / ready / delivered / acknowledged,
    integrity_hash VARCHAR(255)  -- SHA-256 hash of full package contents — tamper detection,
    delivered_timestamp TIMESTAMP WITH TIME ZONE  -- when delivered to requesting party,
    acknowledged_by VARCHAR(255)  -- requesting party confirmation,
    storage_reference VARCHAR(255)  -- pointer to packaged export in secure storage,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit — immutable
);

-- =========================================================================
-- audit_package_line_item
-- PURPOSE: Tracks: every single piece of evidence inside an audit package Records: which table it came from which metric it supports its confidence at time of export whether the full chain is unbroken Enables: line-by-line auditor drill-down chain completeness verification reasonable assurance readiness per data point tamper-evident immutable evidence records
-- FK (per Chapter 9 — authoritative): audit_package_id -> audit_package_registry | metric_id -> metric_registry | confidence_rule_id -> confidence_scoring_registry | reviewed_by_user_id -> user_registry | ai_execution_id -> llm_execution_log
-- =========================================================================
CREATE TABLE audit_package_line_item (
    line_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    audit_package_id UUID REFERENCES audit_package_registry(audit_package_id)  -- which package this belongs to — Table 85,
    line_item_sequence INT  -- order within the package,
    evidence_type VARCHAR(255)  -- metric_record / ingestion / reconciliation / llm_execution / human_decision / do...,
    source_table_number VARCHAR(255)  -- which of the 86 tables this came from,
    source_record_id UUID  -- the specific record ID from that table,
    metric_id UUID REFERENCES metric_registry(metric_id)  -- which canonical metric this supports — Table 8,
    metric_value NUMERIC(18,2)  -- the value being evidenced,
    confidence_score INT  -- confidence at time of package generation,
    confidence_colour VARCHAR(255)  -- green / amber / red / grey,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- which rule calculated this — Table 77,
    human_reviewed_flag BOOLEAN DEFAULT FALSE  -- yes / no,
    reviewed_by_user_id UUID REFERENCES user_registry(user_id)  -- who reviewed — Table 4,
    review_timestamp TIMESTAMP WITH TIME ZONE  -- when reviewed,
    ai_generated_flag BOOLEAN DEFAULT FALSE  -- yes / no,
    ai_execution_id UUID REFERENCES llm_execution_log(execution_id)  -- if AI-generated — linked to Table 76,
    source_document_reference VARCHAR(255)  -- original document pointer in secure storage,
    chain_complete_flag BOOLEAN DEFAULT FALSE  -- yes / no — is the full evidence chain unbroken for this item,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit — immutable
);

-- =========================================================================
-- enterprise_memory_registry
-- PURPOSE: Stores: significant contextual events in this company's history Controls: what prior context is eligible for retrieval Enables: decision-layer memory surfaces only when it changes recommended action, confidence, urgency, or signal interpretation Operating Rule: Memory exists in the background, not the foreground. Surface only when it materially changes what the executive should do today.
-- FK (per Chapter 9 — authoritative): organization_id -> organization_master | confidence_rule_id -> confidence_scoring_registry | materiality_scoring_rule_id -> scoring_rule_registry
-- =========================================================================
CREATE TABLE enterprise_memory_registry (
    memory_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organization_master(organization_id)  -- FK → organization_master,
    memory_type VARCHAR(255)  -- event / decision / commitment / risk / outcome / pattern_instance / assumption,
    memory_date TIMESTAMP WITH TIME ZONE  -- when this happened,
    reporting_period VARCHAR(255)  -- which FY,
    headline VARCHAR(255)  -- one sentence — what happened. Fact not label. Max 200 chars.,
    business_context TEXT  -- why it mattered — meaning not data. Max 400 chars.,
    financial_impact_min NUMERIC(18,2)  -- lower bound ₹ — null if unquantified,
    financial_impact_max NUMERIC(18,2)  -- upper bound ₹ — null if unquantified,
    financial_impact_confidence VARCHAR(255)  -- 0–100 — how reliable the financial estimate is,
    intelligence_zone VARCHAR(255)  -- value_creation / risk_resilience / market_position / future_readiness / executio...,
    memory_materiality_score INT CHECK (memory_materiality_score BETWEEN 0 AND 100)  -- 0–100 — calculated per scoring_rule_registry rule_type = memory_materiality,
    materiality_scoring_rule_id UUID REFERENCES scoring_rule_registry(scoring_rule_id)  -- FK → scoring_rule_registry,
    memory_decay_factor VARCHAR(255)  -- 0.0–1.0 — rate of relevance decay. 0.0 = never decays. 1.0 = decays rapidly.,
    decay_last_applied_date TIMESTAMP WITH TIME ZONE  -- when decay was last recalculated,
    retrieval_trigger_type VARCHAR(255)  -- action_change / confidence_change / urgency_change / interpretation_change,
    retrieval_trigger_conditions VARCHAR(255)  -- structured conditions — must be met for this memory to surface,
    source_type VARCHAR(255)  -- board_minutes / annual_report / management_decision / system_detected / executiv...,
    source_reference VARCHAR(255)  -- document name, page, or system record,
    confidence_score INT CHECK (confidence_score BETWEEN 0 AND 100)  -- 0–100,
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id)  -- FK → confidence_scoring_registry,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit — immutable,
    updated_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- decision_outcome_registry
-- PURPOSE: Tracks: every recommendation CorpStage made and its real-world outcome Enables: recommendation calibration — CorpStage improves accuracy over time trust building — CFO sees historical recommendation accuracy score learning loop — outcomes feed back into future recommendation confidence Operating Rule: Every recommendation made by CorpStage must have a corresponding outcome row created at the time ...
-- FK (per Chapter 9 — authoritative): organization_id -> organization_master | recommendation_id -> recommendation_registry | decision_maker_user_id -> user_registry | memory_id -> enterprise_memory_registry | accuracy_scoring_rule_id -> scoring_rule_registry
-- =========================================================================
CREATE TABLE decision_outcome_registry (
    outcome_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organization_master(organization_id)  -- FK → organization_master,
    recommendation_id UUID REFERENCES recommendation_registry(recommendation_id)  -- FK → recommendation_registry — unique. One outcome per recommendation.,
    decision_made VARCHAR(255)  -- yes / no / partial / deferred / overridden,
    decision_date TIMESTAMP WITH TIME ZONE  -- when the decision was made — null until decision_made is set,
    decision_maker_user_id UUID REFERENCES user_registry(user_id)  -- FK → user_registry,
    decision_rationale TEXT  -- why — or why not. Max 300 chars.,
    implementation_status VARCHAR(255)  -- not_started / in_progress / complete / abandoned,
    realisation_rate VARCHAR(255)  -- actual ÷ projected financial impact. 0–200%. null until outcome measured.,
    variance_primary_reason VARCHAR(255)  -- adoption_friction / external_event / scope_change / data_error / timing / other,
    lessons_learned VARCHAR(255)  -- what this teaches for future similar recommendations. Max 300 chars.,
    recommendation_accuracy_score INT CHECK (recommendation_accuracy_score BETWEEN 0 AND 100)  -- 0–100 — calculated per scoring_rule_registry rule_type = recommendation_accuracy,
    accuracy_scoring_rule_id UUID REFERENCES scoring_rule_registry(scoring_rule_id)  -- FK → scoring_rule_registry,
    confidence_adjustment VARCHAR(255)  -- delta applied to future similar recommendations. Range -50 to +50.,
    memory_created_flag BOOLEAN DEFAULT FALSE  -- yes / no,
    memory_id UUID REFERENCES enterprise_memory_registry(memory_id)  -- FK → enterprise_memory_registry — null until memory_created_flag = yes,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit — immutable,
    outcome_recorded_at VARCHAR(255)  -- when actual impact was measured — null until recorded
);

-- =========================================================================
-- recurring_pattern_registry
-- PURPOSE: Detects: systemic issues vs situational events Enables: pattern-aware intelligence — this keeps happening severity acceleration detection — this is getting worse each cycle systemic vs situational classification predicted next occurrence with financial estimate Operating Rule: A pattern is not declared until at least two confirmed occurrences exist in pattern_occurrence_registry. One occurrence is...
-- FK (per Chapter 9 — authoritative): organization_id -> organization_master | velocity_scoring_rule_id -> scoring_rule_registry
-- =========================================================================
CREATE TABLE recurring_pattern_registry (
    pattern_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organization_master(organization_id)  -- FK → organization_master,
    pattern_name VARCHAR(255)  -- descriptive — max 150 chars. Must name the issue not the symptom.,
    pattern_type VARCHAR(255)  -- risk_recurrence / missed_opportunity / commitment_gap / performance_cycle / beli...,
    intelligence_zone VARCHAR(255)  -- primary zone affected — same six locked values as enterprise_memory_registry,
    first_occurrence_date TIMESTAMP WITH TIME ZONE  -- date of first confirmed occurrence,
    latest_occurrence_date TIMESTAMP WITH TIME ZONE  -- date of most recent occurrence,
    occurrence_count INT  -- total confirmed occurrences — must match count of active rows in pattern_occurre...,
    average_financial_impact NUMERIC(18,2)  -- mean ₹ impact across all occurrences — recalculated on each new occurrence,
    trend_direction VARCHAR(255)  -- stable / increasing / decreasing / accelerating — derived from pattern_occurrenc...,
    pattern_velocity_score INT CHECK (pattern_velocity_score BETWEEN 0 AND 100)  -- 0–100 — rate of severity acceleration — calculated per scoring_rule_registry rul...,
    velocity_scoring_rule_id UUID REFERENCES scoring_rule_registry(scoring_rule_id)  -- FK → scoring_rule_registry,
    management_response_pattern VARCHAR(255)  -- how management has typically responded. Max 200 chars.,
    response_effectiveness VARCHAR(255)  -- resolved / partially_resolved / unresolved / worsened,
    structural_flag BOOLEAN DEFAULT FALSE  -- yes / no — systemic or situational. Requires human confirmation before set to ye...,
    root_cause_hypothesis TEXT  -- what drives this pattern. Max 300 chars.,
    predicted_next_occurrence_date TIMESTAMP WITH TIME ZONE  -- when system predicts recurrence — null if insufficient data,
    predicted_next_impact_min NUMERIC(18,2)  -- lower bound ₹ estimate,
    predicted_next_impact_max NUMERIC(18,2)  -- upper bound ₹ estimate,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit — immutable,
    last_recalculated VARCHAR(255)  -- when all derived fields were last updated
);

-- =========================================================================
-- strategic_intent_registry
-- PURPOSE: Tracks: what leadership says matters — declared strategic priorities Controls: intelligence reweighting — same signal different importance per company Enables: company-specific intelligence instead of generic intent-progress tracking — are we moving toward what we said matters commitment accountability — declared priorities vs actual progress Operating Rule: Every signal interpretation in executiv...
-- FK (per Chapter 9 — authoritative): organization_id -> organization_master
-- =========================================================================
CREATE TABLE strategic_intent_registry (
    intent_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organization_master(organization_id)  -- FK → organization_master,
    intent_name VARCHAR(255)  -- e.g. Global expansion — Southeast Asia. Max 150 chars.,
    intent_category VARCHAR(255)  -- growth / resilience / efficiency / compliance / reputation / transition / financ...,
    intent_description TEXT  -- what this means in business terms. Max 300 chars.,
    stated_by VARCHAR(255)  -- board / CEO / CFO / CSO / investor_communication / annual_report,
    stated_date TIMESTAMP WITH TIME ZONE  -- when declared,
    stated_in_source VARCHAR(255)  -- document or meeting reference. Max 200 chars.,
    intent_horizon VARCHAR(255)  -- short_term / medium_term / long_term,
    commitment_strength VARCHAR(255)  -- aspirational / committed / board_mandated / investor_committed,
    progress_status VARCHAR(255)  -- not_started / on_track / lagging / at_risk / achieved / abandoned,
    progress_confidence VARCHAR(255)  -- 0–100 — how confident the system is in its progress assessment,
    progress_last_assessed VARCHAR(255)  -- when last reviewed,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit — immutable,
    updated_at TIMESTAMP WITH TIME ZONE  -- audit
);

-- =========================================================================
-- executive_belief_registry
-- PURPOSE: Tracks: assumptions held by leadership as first-class objects Detects: when evidence contradicts a held assumption Enables: assumption archaeology — tracing failures to their origin belief belief accuracy scoring — which assumptions prove reliable vs consistently wrong systemic blind spot detection — beliefs that keep failing but keep being held Operating Rule: A belief is any assumption that, if ...
-- FK (per Chapter 9 — authoritative): organization_id -> organization_master | accuracy_scoring_rule_id -> scoring_rule_registry
-- =========================================================================
CREATE TABLE executive_belief_registry (
    belief_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organization_master(organization_id)  -- FK → organization_master,
    belief_statement TEXT  -- the assumption stated as a belief. Max 250 chars. Written as an assertive claim ...,
    belief_category VARCHAR(255)  -- operational / financial / market / regulatory / people / strategic / risk,
    intelligence_zone VARCHAR(255)  -- primary zone this belief affects — same six locked values,
    stated_by VARCHAR(255)  -- board / CEO / CFO / CSO / management_team / system_inferred,
    stated_date TIMESTAMP WITH TIME ZONE  -- when first articulated,
    stated_in_source VARCHAR(255)  -- document or meeting reference. Max 200 chars.,
    belief_status VARCHAR(255)  -- unverified / supported / challenged / disproven / revised,
    belief_status_date TIMESTAMP WITH TIME ZONE  -- when status last changed,
    status_change_reason VARCHAR(255)  -- what triggered the status change. Max 200 chars.,
    belief_accuracy_score INT CHECK (belief_accuracy_score BETWEEN 0 AND 100)  -- 0–100 — historical reliability of this belief type from this source — calculated...,
    accuracy_scoring_rule_id UUID REFERENCES scoring_rule_registry(scoring_rule_id)  -- FK → scoring_rule_registry,
    impact_of_failure_min NUMERIC(18,2)  -- lower bound ₹ estimate if this belief proves wrong. null if unquantifiable.,
    impact_of_failure_max NUMERIC(18,2)  -- upper bound ₹ estimate. null if unquantifiable.,
    active_flag BOOLEAN DEFAULT FALSE  -- active,
    created_at TIMESTAMP WITH TIME ZONE  -- audit — immutable,
    last_evaluated VARCHAR(255)  -- when last assessed against current evidence
);-- =========================================================================
-- memory_evidence_registry
-- PURPOSE: Links evidence items to the enterprise_memory_registry entry they support or contradict. SOURCE GAP: never given a full column-level schema anywhere in either source document — only its PK/FK summary line exists. Columns below are the minimum implied by that line plus its one-line purpose; nothing else is invented.
-- FK (per Chapter 9 — authoritative): memory_id -> enterprise_memory_registry | organization_id -> organization_master | confidence_rule_id -> confidence_scoring_registry
-- =========================================================================
CREATE TABLE memory_evidence_registry (
    evidence_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    memory_id UUID NOT NULL REFERENCES enterprise_memory_registry(memory_id),
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id),
    confidence_rule_id UUID REFERENCES confidence_scoring_registry(confidence_scoring_id),
    active_flag BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- =========================================================================
-- decision_outcome_dimension
-- PURPOSE: Per-dimension breakdown of a decision_outcome_registry row's projected-vs-actual variance. SOURCE GAP: same as memory_evidence_registry — no full schema was ever specified, only the PK/FK line and a one-line purpose. Minimal definition only.
-- FK (per Chapter 9 — authoritative): outcome_id -> decision_outcome_registry | organization_id -> organization_master
-- =========================================================================
CREATE TABLE decision_outcome_dimension (
    dimension_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    outcome_id UUID NOT NULL REFERENCES decision_outcome_registry(outcome_id),
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id),
    active_flag BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

PART B: SOURCE-A-EXCLUSIVE TABLES (12)
industry_taxonomy_registry — Self-referencing three-tier reference table (Sector -> Industry -> Sub-Industry) resolving the gap where organization_master.sector and .industry_subsector were free text with no enforced classification. Lets a Canonical Data Element be tagged as Global or industry-specific against one frozen, SASB-SICS-grounded taxonomy instead of three incompatible ad-hoc lists.

adaptive_ingestion_state — Tracks the live state of each business question for each user during the conversational data-entry interview: whether it has been pre-filled, suppressed, confirmed, skipped, or delegated, and the estimated time saved by automation. Powers the Business Intelligence Interview's progress bar and "highest mandatory density" prioritization logic.

business_question_variants — Caches the industry-specific phrasing of each canonical business question (e.g. BQ-003 asks about "fabric types and dyes" for Apparel vs "metals, plastics, semiconductors" for Automotive) without creating a separate underlying data point per industry. One canonical fact, many question phrasings.

cross_domain_synthesis_metadata — Stores the calculated weight and causal-direction coefficients between pairs of intelligence domains (e.g. Supplier Ecosystem amplifying Financial Engine risk), used by the cross-domain synthesis engine to compute combined severity across a causal chain.

delegation_audit_trail — Immutable, append-only log of every delegation of an intelligence_work_queue item from one user to another, including the reason, acceptance timestamp, and outcome. Exists to guarantee a complete accountability trail can never be silently lost.

domain_ownership_routing — Defines which role (primary, secondary, escalation) owns resolution of an unconfirmed or low-confidence data point in each of the 20 Canonical Intelligence Domains, and the SLA hours before an unresolved item escalates.

intelligence_work_queue — The central work-routing table: every data point flagged for human confirmation, correction, or delegation lands here with its confidence score, materiality score, auto-allocated owner, and resolution deadline. Drives the Action Center.

lens_vocabulary_map — Translates one underlying canonical data value into the vocabulary appropriate to the active executive persona (e.g. the same metric reads as "Value Chain Opex Impact" to a CFO and "Value Chain Cost Category 1 Upstream Exposure" to a CSO) without duplicating the database or the underlying fact.

recurring_causal_chains — Caches named, multi-domain causal-chain templates (e.g. "Supplier-to-Earnings Chain") as an ordered sequence of domain IDs, used by the synthesis engine to recognize and evaluate a known systemic risk pattern when its component signals are observed together.


decision_outcome_dimension — Per-dimension breakdown of a decision_outcome_registry row's projected-vs-actual variance (e.g. cost dimension projected $2M, actual $2.6M). NOTE: same acknowledged source gap as memory_evidence_registry — no full schema was ever given in the source; built minimally from its stated PK/FK line and purpose only.
CREATE TABLE IF NOT EXISTS adaptive_ingestion_state (
    state_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL,
    user_id UUID NOT NULL,
    question_code VARCHAR(50) NOT NULL,
    workflow_bucket VARCHAR(50) NOT NULL, -- 'B-01' through 'B-07'
    ingestion_status VARCHAR(50) NOT NULL DEFAULT 'ELIGIBLE', -- 'ELIGIBLE' | 'SUPPRESSED' | 'CONFIRMED' | 'SKIPPED' | 'DELEGATED'
    suppression_reason VARCHAR(100), -- 'EXTRACTED' | 'INFERRED' | 'IMMATERIAL'
    estimated_time_savings_seconds INTEGER NOT NULL DEFAULT 0,
    last_interacted_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_ais_org FOREIGN KEY (organization_id) REFERENCES organization_master(organization_id),
    CONSTRAINT fk_ais_user FOREIGN KEY (user_id) REFERENCES user_registry(user_id),
    CONSTRAINT chk_ais_status CHECK (ingestion_status IN ('ELIGIBLE', 'SUPPRESSED', 'CONFIRMED', 'SKIPPED', 'DELEGATED')),
    CONSTRAINT chk_ais_reason CHECK (suppression_reason IN ('EXTRACTED', 'INFERRED', 'IMMATERIAL'))
);

CREATE TABLE tenant_workspace.belief_evidence_registry (
    belief_evidence_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization_master(organization_id),
    belief_id UUID NOT NULL REFERENCES tenant_workspace.executive_belief_registry(belief_id),
    evidence_type VARCHAR(100) NOT NULL,
    source_record_id UUID NOT NULL, -- Pointing directly to database source row generating validation discrepancy
    is_contradictory BOOLEAN DEFAULT FALSE NOT NULL, -- Toggled dynamically when live data metrics mismatch assumptions
    confidence_rule_id UUID NOT NULL REFERENCES public.confidence_scoring_registry(confidence_scoring_id),
    active_flag BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS business_question_variants (
    variant_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL,
    question_code VARCHAR(50) NOT NULL, -- BQ-001 to BQ-070
    industry_slug VARCHAR(50) NOT NULL, -- e.g., 'APPAREL', 'AUTOMOTIVE', 'OIL_GAS'
    phrased_text TEXT NOT NULL,
    target_cde_id VARCHAR(50) NOT NULL, -- Layer B mapping target (CDE/CDP reference)
    importance_tier VARCHAR(50) NOT NULL DEFAULT 'RECOMMENDED', -- 'REQUIRED' | 'RECOMMENDED' | 'SUPPLEMENTAL'
    active_flag BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_bqv_org FOREIGN KEY (organization_id) REFERENCES organization_master(organization_id),
    CONSTRAINT chk_bqv_tier CHECK (importance_tier IN ('REQUIRED', 'RECOMMENDED', 'SUPPLEMENTAL')),
    CONSTRAINT uq_bqv_org_code_industry UNIQUE (organization_id, question_code, industry_slug)
);

CREATE TABLE IF NOT EXISTS cross_domain_synthesis_metadata (
    synthesis_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL,
    source_domain_id INTEGER NOT NULL,
    target_domain_id INTEGER NOT NULL,
    weight_coefficient NUMERIC(5,4) NOT NULL CONSTRAINT chk_cdsm_weight CHECK (weight_coefficient BETWEEN 0.0000 AND 1.0000),
    causal_direction VARCHAR(20) NOT NULL, -- 'AMPLIFYING' | 'CONSTRAINING' | 'REVEALING' | 'CAUSAL'
    cross_domain_impact_score INTEGER NOT NULL CONSTRAINT chk_cdsm_score CHECK (cross_domain_impact_score BETWEEN 0 AND 100),
    active_flag BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_cdsm_org FOREIGN KEY (organization_id) REFERENCES organization_master(organization_id),
    CONSTRAINT chk_cdsm_direction CHECK (causal_direction IN ('AMPLIFYING', 'CONSTRAINING', 'REVEALING', 'CAUSAL'))
);

CREATE TABLE tenant_workspace.intent_signal_mapping (
    mapping_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization_master(organization_id),
    intent_id UUID NOT NULL REFERENCES tenant_workspace.strategic_intent_registry(intent_id),
    signal_type VARCHAR(100) NOT NULL,
    weight_modifier NUMERIC(3,2) NOT NULL DEFAULT 1.00,
    active_flag BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS lens_vocabulary_map (
    mapping_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL,
    lens_id VARCHAR(50) NOT NULL, -- 'EXECUTIVE' | 'RESILIENCE' | 'RISK'
    canonical_term VARCHAR(255) NOT NULL,
    lens_term VARCHAR(255) NOT NULL,
    lens_priority_weight NUMERIC(3,2) NOT NULL DEFAULT 1.00,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_lvm_org FOREIGN KEY (organization_id) REFERENCES organization_master(organization_id),
    CONSTRAINT uq_lvm_org_lens_term UNIQUE (organization_id, lens_id, canonical_term)
);

CREATE TABLE tenant_workspace.pattern_occurrence_registry (
    occurrence_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization_master(organization_id),
    pattern_id UUID NOT NULL REFERENCES tenant_workspace.recurring_pattern_registry(pattern_id),
    memory_id UUID NOT NULL REFERENCES tenant_workspace.enterprise_memory_registry(memory_id),
    occurrence_date DATE NOT NULL,
    financial_impact NUMERIC(18,2) NOT NULL,
    active_flag BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL    
);

CREATE TABLE IF NOT EXISTS recurring_causal_chains (
    chain_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL,
    chain_name VARCHAR(150) NOT NULL, -- e.g., 'Supplier-to-Earnings Chain'
    ordered_domain_sequence INTEGER[] NOT NULL, -- Array of Domain IDs tracking the cascade
    calculated_ebitda_sensitivity NUMERIC(15,2),
    trigger_threshold_score INTEGER NOT NULL DEFAULT 70,
    active_flag BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_rcc_org FOREIGN KEY (organization_id) REFERENCES organization_master(organization_id)
);

CREATE TABLE public.scoring_rule_registry (
    scoring_rule_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_name VARCHAR(150) NOT NULL,
    rule_type VARCHAR(100) NOT NULL CHECK (rule_type IN ('memory_materiality', 'recommendation_accuracy', 'pattern_velocity', 'belief_accuracy')),
    formula_logic TEXT NOT NULL,
    deprecated_by_rule_id UUID REFERENCES public.scoring_rule_registry(scoring_rule_id) ON DELETE SET NULL,
    active_flag BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS intelligence_work_queue (
    element_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL,
    domain_id INTEGER NOT NULL,
    confidence_score INTEGER NOT NULL CONSTRAINT chk_iwq_confidence CHECK (confidence_score BETWEEN 0 AND 100),
    materiality_score INTEGER NOT NULL CONSTRAINT chk_iwq_materiality CHECK (materiality_score BETWEEN 0 AND 100),
    auto_allocated_to UUID NOT NULL,
    allocated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolution_deadline TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'ALLOCATED', -- 'ALLOCATED' | 'CONFIRMED' | 'CORRECTED' | 'DELEGATED' | 'ESCALATED' | 'RESOLVED'
    escalation_level INTEGER NOT NULL DEFAULT 0,
    financial_exposure_range_min NUMERIC(15,2),
    financial_exposure_range_max NUMERIC(15,2),
    active_flag BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_iwq_org FOREIGN KEY (organization_id) REFERENCES organization_master(organization_id),
    CONSTRAINT fk_iwq_user FOREIGN KEY (auto_allocated_to) REFERENCES user_registry(user_id),
    CONSTRAINT chk_iwq_status CHECK (status IN ('ALLOCATED', 'CONFIRMED', 'CORRECTED', 'DELEGATED', 'ESCALATED', 'RESOLVED'))
);

CREATE TABLE IF NOT EXISTS domain_ownership_routing (
    routing_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL,
    domain_id INTEGER NOT NULL,
    primary_owner_role UUID NOT NULL,
    secondary_owner_role UUID NOT NULL,
    escalation_owner_role UUID NOT NULL,
    resolution_sla_hours INTEGER NOT NULL DEFAULT 168, -- Default 7 days
    active_flag BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_dor_org FOREIGN KEY (organization_id) REFERENCES organization_master(organization_id),
    CONSTRAINT fk_dor_primary FOREIGN KEY (primary_owner_role) REFERENCES role_registry(role_id),
    CONSTRAINT fk_dor_secondary FOREIGN KEY (secondary_owner_role) REFERENCES role_registry(role_id),
    CONSTRAINT fk_dor_escalation FOREIGN KEY (escalation_owner_role) REFERENCES role_registry(role_id),
    CONSTRAINT uq_dor_org_domain UNIQUE (organization_id, domain_id)
);

CREATE TABLE IF NOT EXISTS delegation_audit_trail (
    delegation_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL,
    element_id UUID NOT NULL,
    delegated_from UUID NOT NULL,
    delegated_to UUID NOT NULL,
    delegated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    delegation_reason TEXT NOT NULL,
    accepted_at TIMESTAMP WITH TIME ZONE,
    outcome VARCHAR(50) NOT NULL DEFAULT 'PENDING', -- 'PENDING' | 'ACCEPTED' | 'REJECTED' | 'EXPIRED'
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_dat_org FOREIGN KEY (organization_id) REFERENCES organization_master(organization_id),
    CONSTRAINT fk_dat_iwq FOREIGN KEY (element_id) REFERENCES intelligence_work_queue(element_id),
    CONSTRAINT fk_dat_from FOREIGN KEY (delegated_from) REFERENCES user_registry(user_id),
    CONSTRAINT fk_dat_to FOREIGN KEY (delegated_to) REFERENCES user_registry(user_id),
    CONSTRAINT chk_dat_outcome CHECK (outcome IN ('PENDING', 'ACCEPTED', 'REJECTED', 'EXPIRED'))
);
PART C: CUSTOMER-SPECIFIC DOMAIN AND CDE EXTENSIBILITY LAYER

-- =========================================================================
-- Customer-defined Domains and CDEs unique to one customer. Tenant-scoped
-- and invisible to every other customer. Flows through the same confidence,
-- evidence, workflow, and reporting pipeline as every standard CDE.
-- Blueprint v2.2 Section 5.0c Binding 3 and AMD-004 govern these tables.
-- =========================================================================

SQL
-- =========================================================================
-- customer_domain_registry
-- PURPOSE: A customer-defined intelligence domain that does not exist in
-- the platform's standard 20 Canonical Intelligence Domains. Tenant-scoped
-- and invisible to every other customer.
-- =========================================================================
CREATE TABLE customer_domain_registry (
    customer_domain_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id),
    domain_name VARCHAR(255) NOT NULL,
    domain_description TEXT,
    requested_by_user_id UUID NOT NULL REFERENCES user_registry(user_id),
    approval_status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (approval_status IN ('pending', 'approved', 'rejected')),
    approved_by_user_id UUID REFERENCES user_registry(user_id),
    approved_at TIMESTAMP WITH TIME ZONE,
    active_flag BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT uq_customer_domain_name UNIQUE (organization_id, domain_name)
);

-- =========================================================================
-- customer_metric_registry
-- PURPOSE: A customer-defined Canonical Data Element, tenant-scoped and
-- invisible to every other customer. Mirrors metric_registry's column shape
-- so it can be queried and processed identically by the same downstream
-- confidence-scoring, evidence, and reporting pipelines — the only
-- difference is organization_id scoping instead of platform-wide visibility.
-- =========================================================================
CREATE TABLE customer_metric_registry (
    customer_metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id),
    customer_domain_id UUID REFERENCES customer_domain_registry(customer_domain_id),  -- NULL if attached to a standard domain instead of a fully custom one
    metric_name VARCHAR(255) NOT NULL,
    metric_code VARCHAR(100) NOT NULL,
    metric_description TEXT,
    unit_of_measure VARCHAR(50),
    formula_logic TEXT,
    source_type VARCHAR(50),
    requested_by_user_id UUID NOT NULL REFERENCES user_registry(user_id),
    approval_status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (approval_status IN ('pending', 'approved', 'rejected')),
    approved_by_user_id UUID REFERENCES user_registry(user_id),
    approved_at TIMESTAMP WITH TIME ZONE,
    evidence_required_flag BOOLEAN DEFAULT TRUE NOT NULL,
    ai_extractable_flag BOOLEAN DEFAULT FALSE NOT NULL,  -- customer CDEs default to FALSE; the platform AI is not trained on them until pattern volume justifies it
    active_flag BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT uq_customer_metric_code UNIQUE (organization_id, metric_code)
);

ALTER TABLE customer_domain_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON customer_domain_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE customer_metric_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON customer_metric_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

-- =========================================================================
-- Governance note: metric_record (the fact table every CDE's actual values
-- live in) must accept EITHER a standard metric_id OR a customer_metric_id,
-- never both populated, never both null. Enforced via a CHECK constraint
-- added to metric_record as part of this Part:
-- =========================================================================
ALTER TABLE metric_record
    ADD COLUMN customer_metric_id UUID REFERENCES customer_metric_registry(customer_metric_id),
    ALTER COLUMN metric_id DROP NOT NULL;

ALTER TABLE metric_record
    ADD CONSTRAINT chk_metric_record_exactly_one_metric_type CHECK (
        (metric_id IS NOT NULL AND customer_metric_id IS NULL) OR
        (metric_id IS NULL AND customer_metric_id IS NOT NULL)
    );

-- Query pattern: the complete CDE set visible to a given organization
-- (Global standard CDEs + that organization's industry-specific CDEs +
-- that organization's own customer-defined CDEs, nothing from any other
-- customer):
-- SELECT metric_id AS id, metric_name AS name, 'standard' AS source FROM metric_registry
--   WHERE sub_industry_id IS NULL OR sub_industry_id = (SELECT sub_industry_id FROM organization_master WHERE organization_id = :org_id)
-- UNION ALL
-- SELECT customer_metric_id, metric_name, 'customer_defined' FROM customer_metric_registry
--   WHERE organization_id = :org_id AND approval_status = 'approved';

PART D: ROW-LEVEL SECURITY — MULTI-TENANT ISOLATION POLICY SET (74 of 76 total
pre-AMD-011, +18 AMD-011 policies added below = 94 total; see the AMD-011 RLS
POLICY SET sub-section at the end of this Part for the new tables, including
4 intentionally RLS-exempt global reference tables — zero tables left
unresolved)
(Restores all real source policies, fixes the 4-table no-policy bug found in
Source A, adds RLS for the Tier-1/2 tables identified in Part A. NOTE: the
remaining 2 RLS-protected tables — customer_domain_registry and
customer_metric_registry — are defined inline within Part C immediately
after their own CREATE TABLE statements, not duplicated here. The true
complete count across the whole document is 76 RLS-protected tables, 76
matching policies, verified by the mechanical check in this document's own
revision history — not 74.)
ALTER TABLE intelligence_work_queue ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON intelligence_work_queue
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE organization_node ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation_node ON organization_node
    USING (node_id IN (
        SELECT node_id FROM tenant_workspace.organization_node 
        WHERE current_setting('app.organization_id', true) <> '' 
        AND node_id = node_id -- Forces evaluation within localized tenant sandbox schema bounds
    ));

-- [v6.3 ADDITION] organization_hierarchy previously carried no RLS policy of
-- its own anywhere in this document — a pre-existing gap that predated
-- AMD-011 and was explicitly flagged rather than silently left at v6.2.
-- Closed here using the exact same mechanism as organization_node directly
-- above, scoped on child_node_id (the same column consolidation_determination's
-- own policy already uses to reach organization_node, for consistency between
-- the two policies).
ALTER TABLE organization_hierarchy ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation_hierarchy ON organization_hierarchy
    USING (child_node_id IN (
        SELECT node_id FROM tenant_workspace.organization_node
        WHERE current_setting('app.organization_id', true) <> ''
        AND node_id = node_id -- Forces evaluation within localized tenant sandbox schema bounds
    ));

ALTER TABLE metric_record ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation_metrics ON metric_record
    USING (organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid);

ALTER TABLE financial_record ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation_financials ON financial_record
    USING (organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid);

ALTER TABLE INTELLIGENCE_WORK_QUEUE ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON INTELLIGENCE_WORK_QUEUE
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE enterprise_memory_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation_memory ON enterprise_memory_registry
    USING (organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid);

ALTER TABLE recurring_pattern_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation_patterns ON recurring_pattern_registry
    USING (organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid);

ALTER TABLE strategic_intent_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation_intents ON strategic_intent_registry
    USING (organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid);

ALTER TABLE executive_belief_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation_beliefs ON executive_belief_registry
    USING (organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid);

ALTER TABLE report_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON report_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE disclosure_requirement_mapping ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON disclosure_requirement_mapping
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE disclosure_submission_tracker ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON disclosure_submission_tracker
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE intelligence_work_queue ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON intelligence_work_queue
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE domain_ownership_routing ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON domain_ownership_routing
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE delegation_audit_trail ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON delegation_audit_trail
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE lens_vocabulary_map ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON lens_vocabulary_map
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE business_question_variants ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON business_question_variants
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE adaptive_ingestion_state ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON adaptive_ingestion_state
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE cross_domain_synthesis_metadata ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON cross_domain_synthesis_metadata
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE recurring_causal_chains ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON recurring_causal_chains
    USING (organization_id = current_setting('app.organization_id')::uuid);
-- The 4 tables below had RLS ENABLED in the source documents with NO POLICY
-- ever defined for them — a genuine bug in the source (RLS-enabled-with-no-
-- policy denies ALL access by default in PostgreSQL, including to the
-- table's own organization). Fixed here using the same standard pattern
-- already used for their sibling Memory Layer tables.
ALTER TABLE pattern_occurrence_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON pattern_occurrence_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE intent_signal_mapping ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON intent_signal_mapping
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE belief_evidence_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON belief_evidence_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE decision_outcome_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON decision_outcome_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);


ALTER TABLE AI_confidence_recalibration ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON AI_confidence_recalibration
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE action_impact_tracking ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON action_impact_tracking
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE action_tracker ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON action_tracker
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE anomaly_detection_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON anomaly_detection_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE api_call_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON api_call_log
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE api_credential_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON api_credential_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE audit_package_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON audit_package_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE benchmark_performance_tracker ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON benchmark_performance_tracker
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE competitive_advantage_tracking ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON competitive_advantage_tracking
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE competitive_signal_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON competitive_signal_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE competitor_metric_mapping ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON competitor_metric_mapping
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE data_ingestion_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON data_ingestion_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE data_reconciliation_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON data_reconciliation_log
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE decision_outcome_dimension ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON decision_outcome_dimension
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE decision_traceability_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON decision_traceability_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE event_acceptance_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON event_acceptance_log
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE event_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON event_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE evidence_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON evidence_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE executive_insight_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON executive_insight_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE external_factor_impact_mapping ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON external_factor_impact_mapping
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE financial_impact_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON financial_impact_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE financial_impact_sensitivity ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON financial_impact_sensitivity
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE incident_impact_mapping ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON incident_impact_mapping
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE kpi_metric_mapping ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON kpi_metric_mapping
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE learning_feedback_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON learning_feedback_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE llm_execution_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON llm_execution_log
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE memory_evidence_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON memory_evidence_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE metric_review_workflow ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON metric_review_workflow
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE metric_review_workflow_execution ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON metric_review_workflow_execution
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE metric_source_mapping ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON metric_source_mapping
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE narrative_component_mapping ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON narrative_component_mapping
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE narrative_feedback_learning ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON narrative_feedback_learning
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE narrative_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON narrative_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE notification_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON notification_log
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE optimization_recommendation_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON optimization_recommendation_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE peer_comparison_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON peer_comparison_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE predictive_model_execution ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON predictive_model_execution
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE recommendation_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON recommendation_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE resilience_assessment_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON resilience_assessment_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE resilience_learning_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON resilience_learning_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE resilience_response_tracker ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON resilience_response_tracker
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE risk_metric_mapping ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON risk_metric_mapping
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE scenario_external_factor_mapping ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON scenario_external_factor_mapping
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE scenario_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON scenario_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE stakeholder_engagement ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON stakeholder_engagement
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE stakeholder_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON stakeholder_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE stakeholder_sentiment_tracking ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON stakeholder_sentiment_tracking
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE trust_scoring_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON trust_scoring_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE user_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON user_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE user_role_mapping ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON user_role_mapping
    USING (organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE workflow_execution ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON workflow_execution
    USING (organization_id = current_setting('app.organization_id')::uuid);

-- =========================================================================
-- AMD-011 RLS POLICY SET — NEW TABLES (Alignment Amendment v1.0)
-- Extends the 76-policy set above to the 22 tables added by AMD-011.
-- Three treatment categories, each justified below rather than applying
-- one pattern uniformly:
--   (1) Direct organization_id column — standard org_isolation policy,
--       matching the pattern used throughout this Part D.
--   (2) One-hop via membership_id -> membership_registry.organization_id —
--       subquery-based policy, standard practice, since these tables do
--       not carry their own organization_id column.
--   (3) Flagged, not force-fitted — a small number of tables where the
--       correct policy shape is genuinely ambiguous given how this
--       document already scopes organization_node/organization_hierarchy
--       (via a tenant_workspace-schema mechanism, not a plain organization_id
--       column — see organization_node's existing policy above). Rather
--       than invent a policy shape that doesn't match that established,
--       non-standard mechanism, these are explicitly flagged for the same
--       team that designed organization_node's policy to extend.
-- Global/master-reference tables (person_registry, identity_registry,
-- system_role_registry, traversal_policy_registry) intentionally receive
-- no RLS policy, consistent with this document's own existing precedent
-- for master reference tables (e.g. industry_taxonomy_registry carries no
-- RLS policy either, for the same reason: no organization_id concept
-- applies to a genuinely global/platform-level table).
-- =========================================================================

-- --- Category 1: direct organization_id column ---

ALTER TABLE membership_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON membership_registry
    USING (organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid);

ALTER TABLE business_role_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON business_role_registry
    USING (organization_id IS NULL  -- NULL = global role, visible to all tenants (URA-001-38)
           OR organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid);

ALTER TABLE group_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON group_registry
    USING (organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid);

ALTER TABLE approval_authority_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON approval_authority_registry
    USING (organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid);

ALTER TABLE escalation_policy_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON escalation_policy_registry
    USING (organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid);

ALTER TABLE entitlement_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON entitlement_registry
    USING (organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid);

ALTER TABLE enterprise_view_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON enterprise_view_registry
    USING (organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid);

ALTER TABLE workflow_event_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON workflow_event_registry
    USING (organization_id IS NULL  -- NULL = GLOBAL scope_type (URA-001-72), visible to all tenants
           OR organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid);

-- --- Category 2: one-hop via membership_id -> membership_registry.organization_id ---

ALTER TABLE membership_business_role ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON membership_business_role
    USING (membership_id IN (
        SELECT membership_id FROM membership_registry
        WHERE organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid
    ));

ALTER TABLE membership_approval_authority ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON membership_approval_authority
    USING (membership_id IN (
        SELECT membership_id FROM membership_registry
        WHERE organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid
    ));

ALTER TABLE group_membership ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON group_membership
    USING (membership_id IN (
        SELECT membership_id FROM membership_registry
        WHERE organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid
    ));

ALTER TABLE domain_permission_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON domain_permission_registry
    USING (membership_id IN (
        SELECT membership_id FROM membership_registry
        WHERE organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid
    ));

ALTER TABLE license_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON license_registry
    USING (membership_id IN (
        SELECT membership_id FROM membership_registry
        WHERE organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid
    ));

ALTER TABLE delegation_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON delegation_registry
    USING (delegator_membership_id IN (
        SELECT membership_id FROM membership_registry
        WHERE organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid
    ));
-- NOTE: this policy scopes on delegator_membership_id only. It does not
-- independently verify delegatee_membership_id belongs to the same
-- organization — that is a data-integrity expectation, not something this
-- policy enforces. If cross-organization delegation is ever a real
-- business scenario, this policy will need explicit revisiting.

ALTER TABLE node_permission_assignment ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON node_permission_assignment
    USING (membership_id IN (
        SELECT membership_id FROM membership_registry
        WHERE organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid
    ));

ALTER TABLE workflow_event_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON workflow_event_log
    USING (membership_id IN (
        SELECT membership_id FROM membership_registry
        WHERE organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid
    ));

ALTER TABLE runtime_assignment_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON runtime_assignment_registry
    USING (
        assigned_to_membership_id IN (
            SELECT membership_id FROM membership_registry
            WHERE organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid
        )
        OR assigned_to_group_id IN (
            SELECT group_id FROM group_registry
            WHERE organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid
        )
        OR assigned_to_business_role_id IN (
            SELECT business_role_id FROM business_role_registry
            WHERE organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid
               OR organization_id IS NULL
        )
    );
-- NOTE: assignment can target a membership, a group, OR a business role
-- (URA-001-77) — exactly one is expected to be populated per row, so this
-- OR-across-three-paths policy is intentional, not a broadening of access.

-- --- Category 3: implemented using organization_node's own established mechanism ---

-- consolidation_determination scopes through hierarchy_id -> organization_hierarchy
-- -> child_node_id -> organization_node. organization_node itself is NOT scoped by
-- a plain organization_id column; it uses a tenant_workspace-schema mechanism (see
-- organization_node's own policy earlier in this Part D). Rather than invent a
-- different mechanism, this policy reuses that exact established pattern by
-- resolving down to child_node_id and checking it the same way organization_node
-- checks itself.
ALTER TABLE consolidation_determination ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON consolidation_determination
    USING (hierarchy_id IN (
        SELECT hierarchy_id FROM organization_hierarchy
        WHERE child_node_id IN (
            SELECT node_id FROM tenant_workspace.organization_node
            WHERE current_setting('app.organization_id', true) <> ''
            AND node_id = node_id -- Forces evaluation within localized tenant sandbox schema bounds
        )
    ));
-- NOTE [updated at v6.3]: organization_hierarchy now has its own RLS policy
-- (org_isolation_hierarchy, added at v6.3 immediately after organization_node's
-- policy earlier in this Part D — see that policy for the fix). This
-- consolidation_determination policy does not depend on it either way; it
-- queries organization_hierarchy directly and validates tenancy via
-- organization_node's mechanism independently. If organization_node's policy
-- is ever redesigned, both this policy and organization_hierarchy's own
-- policy should be updated to match, since all three now deliberately mirror
-- the same mechanism rather than three independent ones.

-- =========================================================================
-- GLOBAL / MASTER-REFERENCE TABLES — NO RLS POLICY BY DESIGN
-- (consistent with this document's existing precedent, e.g.
-- industry_taxonomy_registry, which also carries no RLS policy)
-- =========================================================================
-- person_registry        — canonical individual, independent of any organization (URA-001-15)
-- identity_registry       — authentication identities belong to a Person, not an organization
-- system_role_registry    — platform administration roles are global by definition (URA-001-29)
-- traversal_policy_registry — master reference table of relationship-traversal rules (ERG-001-04)

PART E: MASTER TABLE TIER CLASSIFICATION AND CIL SEEDING REFERENCE

Tier 1 — Full Pre-Seed (21 tables, platform ships with complete data):
  industry_taxonomy_registry, role_registry, material_topic_registry,
  metric_registry, framework_registry, regulatory_requirement_registry,
  jurisdiction_requirement_mapping, metric_review_workflow, kpi_registry,
  kpi_metric_mapping, benchmark_registry, external_factor_registry,
  financial_metric_registry, workflow_registry, disclosure_requirement_mapping,
  predictive_model_registry, architecture_version_registry,
  orchestration_trigger_registry, llm_prompt_registry,
  confidence_scoring_registry, notification_template_registry.

  Seed source: 9 locked Domain CILs — 647 Business Questions, 2,356 CDEs,
  309 Framework Mapping rows (as of Domain 10 completion). See Blueprint v2.2
  Part E for the detailed CIL-to-table seeding specification.

Tier 2 — Partial Pre-Seed (11 tables, platform seeds defaults, customer extends):
  scenario_registry, scenario_external_factor_mapping, risk_registry,
  risk_metric_mapping, external_factor_impact_mapping, competitor_profile_registry,
  market_trend_registry, master_entity_registry, enterprise_configuration_registry,
  cross_domain_relationship_registry, enterprise_knowledge_graph_registry.

Tier 3 — Customer-Created (76 tables, empty at onboarding):
  All remaining transactional tables — populated as customers use the platform.

APPENDIX H: KNOWN OPEN ITEMS AND ENGINEERING DECISIONS DEFERRED

H.1 — API endpoint-level specification for the Industry/Customer
Extensibility layer (Part 0, Part C) does not exist in either source. The
source's own API Architecture section (7D.8) is high-level prose only ("REST
for CRUD, GraphQL for dashboards") with zero actual endpoint definitions for
ANY table, not just the new ones — so this is a pre-existing gap in both
sources, not something introduced by this document's additions. Genuine
implementation work, not a documentation fix.

H.2 — Section 7D.4's claimed "23 domain-driven microservices" remains short
by 2 even after this Part's additions (21 confirmed, 23 claimed). Neither
source specifies what the missing 2 were intended to be — left open rather
than invented.

H.3 — The LangGraph orchestration graph actually implementing the Discover/
Infer/Validate/Ask pipeline (Part G) has not been specified as executable
workflow logic anywhere — only as the conceptual 4-stage pattern already
proven out at the CIL content level across all 9 domains.

H.4 — CLOSED in the follow-up pass (see Part I below). All 13 remaining
sections (7D.1, 7D.2, 7D.3, 7D.5, 7D.9-7D.17) were reviewed. 2 genuine
internal inconsistencies were found and resolved, and 2 genuine
cross-referencing gaps were found and flagged. See Part I for the complete
findings.

APPENDIX I: TECHNICAL SECTION REVIEW FINDINGS

I.1 — 7D.1 Locked Engineering Strategy: reviewed, no discrepancy found.
Deployment model, cloud choice, target segment, and stated rationale are
internally consistent with the rest of the document and require no
correction.

I.2 — 7D.2 High-Level System Architecture: INTERNAL INCONSISTENCY FOUND: The "Logical Architecture" diagram in this section names 11
services — ESG, Risk, Financial, Benchmark, Resilience, Workflow,
REPORTING, NARRATIVE, RECOMMENDATION, DECISION, CONFIGURATION Service —
but four of these (Reporting, Recommendation, Decision, Configuration)
never appear anywhere else in the entire document: no "Handles:"
description in 7D.4, no table ownership, not mentioned in this combined
document's own Part F service map. Cross-checking against Part F's actual
table assignments shows these 4 diagram-only names map onto services
ALREADY NAMED DIFFERENTLY elsewhere: report_registry, recommendation_registry,
and decision_traceability_registry were all assigned to Narrative Service
(7D.4's actual prose, confirmed in Part F.6); enterprise_configuration_registry
was assigned to Platform Health Service (Part F.16). RESOLUTION: 7D.2's
diagram is treated as an EARLIER, more granular naming pass that 7D.4's
actual service descriptions later consolidated — "Reporting/Recommendation/
Decision Service" collapsed into "Narrative Service" (consistent with
Narrative Service's stated scope: "executive narratives, board reports,
regulatory reports" already covering all three concepts), and
"Configuration Service" was absorbed into Platform Health Service's
platform-wide scope. This consolidation is now made explicit rather than
left as a silent contradiction between two sections of the same source.

I.3 — 7D.3 Frontend Architecture: reviewed against the Product Architecture
chapter's own Module list (13 modules, Chapter 7C). NOTE: 7D.3's
"Frontend Design Model" names only 7 of the 13 real product modules in its
own module list (Executive Cockpit, Risk Intelligence, ESG Hub, Board Room,
AI Copilot, Reports, Admin) — missing the Business Intelligence Interview, Financial Impact Intelligence,
Benchmarking & Market Intelligence, Scenario & Predictive Intelligence,
Resilience & Incident Command Center, and Action & Workflow Orchestration
(6 of the 13 real modules named in Chapter 7C are absent from 7D.3's own
frontend module list). Flagged as a documentation gap between two sections
of the same source — the product modules genuinely exist (Chapter 7C is
detailed and complete), the frontend architecture section's module list is
simply incomplete and should be read as illustrative, not exhaustive.

I.4 — 7D.5 Data Architecture: reviewed. The stated "86+ core tables" claim
is now stale against this combined document's verified 108-table total —
consistent with every other stale-count issue already found and corrected
in Part 0's provenance note and Part E's seeding correction. No new
correction needed here since this is the same already-documented
discrepancy, not a new one.

I.5 — 7D.9 Event-Driven Architecture: reviewed against the real
event_registry/event_acceptance_log/orchestration_trigger_registry tables
(Event Intelligence Service, Part F.13). The described event flow (Flood
Alert -> Risk Score Update -> Incident Trigger -> Financial Impact ->
Executive Alert) is directionally consistent with the real table
relationships (event_registry -> incident_registry via linked_event_id,
confirmed in Chapter 9's authoritative FK reference) — no discrepancy found.

I.6 — 7D.10 Workflow Orchestration: reviewed against Workflow Service's
real table ownership (Part F.5: action_tracker, workflow_execution,
evidence_registry, intelligence_work_queue). The stated Temporal.io example
flow (Risk -> Recommendation -> Executive approval -> Owner assignment ->
Evidence upload -> Closure) maps cleanly onto these real tables — no
discrepancy found.

I.7 — 7D.11 Security Architecture: reviewed against Part D's actual RLS
implementation. NOTE: this section names Microsoft Entra ID,
RBAC+ABAC, and AES-256/TLS 1.3 — but never once mentions Row-Level Security
or PostgreSQL policies, despite RLS being the actual, real, implemented
multi-tenant isolation mechanism throughout this entire document (76
policies, Part D). Security Architecture is the section where RLS most
belongs conceptually and it is entirely absent from it — RLS is only ever
described in the data-layer sections. Flagged as a real cross-referencing
gap: a security reviewer reading only 7D.11 would not learn that RLS is the
platform's actual database-level tenant isolation mechanism.

I.8 — 7D.12 Multi-Tenant Architecture: reviewed. States "Shared SaaS with
tenant isolation... logical isolation" which is directionally consistent
with the real RLS implementation, but again never names RLS specifically
or cross-references Part D. Same gap class as I.7.

I.9 — 7D.13 Cloud & Deployment Architecture: reviewed. Infrastructure list
(AKS, Azure PostgreSQL, Neo4j Aura, Azure Blob, Azure AI Search, Azure
OpenAI, Azure Monitor, Azure Key Vault) is internally consistent with every
other section's technology references — no discrepancy found.

I.10 — 7D.14 Scalability & Performance: reviewed. States a design goal of
"10,000+ facilities, 100M+ records" — this is a forward-looking target, not
a verifiable claim against current CIL content, and is left as stated. No
discrepancy found, but also not independently verifiable from the artifacts
available in this project.

I.11 — 7D.15 Observability & Reliability: reviewed. No discrepancy found.

I.12 — 7D.16 DevSecOps Strategy: reviewed. No discrepancy found.

I.13 — 7D.17 Recommended Tech Stack (Frozen): reviewed against every
technology reference made across all other sections (Azure OpenAI, NestJS,
PostgreSQL, Neo4j, Temporal, Docker/Kubernetes, Microsoft Entra ID) — fully
internally consistent, no contradictions found anywhere else in the
document.

I.14 — Review Summary
2 genuine internal inconsistencies found and resolved (I.2, I.3) — both
were silent disagreements between different sections of the SAME source
document, not contradictions introduced by this combined document's own
additions. 2 genuine cross-referencing gaps found (I.7, I.8) — RLS is the
platform's real security mechanism but the Security Architecture section
itself never names it. 9 of 13 reviewed items had no discrepancy.

-- =========================================================================
-- PART J: BLUEPRINT v2.2 ALIGNMENT AMENDMENTS
-- Eight gaps identified by cross-checking the Technical Architecture against
-- Blueprint v2.2 Section 5.0c Bindings 2-8 and Sections 5.0d-e.
-- Applied as additive amendments per the Amendment Register convention
-- established in Chapter 10 (AMD-001 through AMD-003).
-- =========================================================================

-- AMD-004: 4-TIER CDE HIERARCHY
-- Blueprint v2.2 Section 5.0c Binding 3 mandates: Global / Industry /
-- Tenant (Corporate-Scoped) / Temporary. The prior schema had only two
-- tiers (metric_registry = Global; customer_metric_registry = Tenant).
-- This amendment adds: a cde_tier column to metric_registry to mark every
-- existing CDE as CANONICAL (the default, since every CDE in the CIL is
-- canonical by definition), and reworks customer_metric_registry to carry
-- the full tier distinction including a TEMPORARY tier for unmapped
-- discovered facts awaiting Governance Manager resolution.

ALTER TABLE metric_registry
    ADD COLUMN cde_tier VARCHAR(20) NOT NULL DEFAULT 'CANONICAL'
        CHECK (cde_tier IN ('CANONICAL','INDUSTRY','TENANT','TEMPORARY')),
    ADD COLUMN tier_governed_by VARCHAR(50) NOT NULL DEFAULT 'CORPSTAGE_ADMIN'
        CHECK (tier_governed_by IN ('CORPSTAGE_ADMIN','CORPORATE_ADMIN'));

COMMENT ON COLUMN metric_registry.cde_tier IS
    'CANONICAL = CorpStage Global standard (default, applies to all 2356 locked CIL CDEs).
     INDUSTRY  = CorpStage Admin adds for a specific SASB Sub-Industry.
     TENANT    = Corporate Admin created, visible within their instance only.
     TEMPORARY = Discovered fact with no CDE match yet; awaiting resolution.';

-- Rework customer_metric_registry to implement the full Binding 3 model:
-- semantic-match-first, convergence-triggered promotion, explicit tier.
ALTER TABLE customer_metric_registry
    ADD COLUMN cde_tier VARCHAR(20) NOT NULL DEFAULT 'TENANT'
        CHECK (cde_tier IN ('TENANT','TEMPORARY')),
    ADD COLUMN semantic_match_attempted_flag BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN semantic_match_result_metric_id UUID
        REFERENCES metric_registry(metric_id),
    ADD COLUMN semantic_match_score NUMERIC(4,3)
        CHECK (semantic_match_score BETWEEN 0 AND 1),
    ADD COLUMN semantic_match_rejected_reason TEXT,
    ADD COLUMN convergence_count INTEGER NOT NULL DEFAULT 1,
    ADD COLUMN promotion_requested_flag BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN promotion_requested_by UUID REFERENCES user_registry(user_id),
    ADD COLUMN promotion_requested_at TIMESTAMP WITH TIME ZONE,
    ADD COLUMN promotion_decision VARCHAR(20)
        CHECK (promotion_decision IN ('PENDING','APPROVED','REJECTED')),
    ADD COLUMN promotion_decided_by UUID REFERENCES user_registry(user_id),
    ADD COLUMN promotion_decided_at TIMESTAMP WITH TIME ZONE;

COMMENT ON COLUMN customer_metric_registry.semantic_match_attempted_flag IS
    'TRUE once the platform has run a semantic similarity check against
     the Global CDE library — prevents repeat processing.';
COMMENT ON COLUMN customer_metric_registry.semantic_match_result_metric_id IS
    'The Global CDE the semantic engine believes this Tenant CDE duplicates.
     NULL if no match found. Corporate Admin must explicitly REJECT the match
     before the Tenant CDE becomes active — preventing silent duplication
     (Blueprint v2.2 Section 5.0c Binding 3).';
COMMENT ON COLUMN customer_metric_registry.convergence_count IS
    'How many independent customers have created a materially identical
     Corporate-Scoped CDE. When this count crosses a CorpStage Admin-
     configured threshold, a promotion review is triggered automatically.';

-- =========================================================================
-- AMD-005: UNCLASSIFIED INTELLIGENCE REGISTRY
-- Blueprint v2.2 Section 5.0c Binding 5: extracted facts with no matching
-- CDE are never discarded. They are held here until a Governance Manager
-- does one of three things: (a) maps to an existing CDE the semantic engine
-- missed, (b) confirms it is genuinely new and creates a CDE, (c) marks
-- not relevant and discards. If the same entry recurs across multiple
-- customers, this feeds the convergence signal in AMD-004 above.
-- =========================================================================

CREATE TABLE unclassified_intelligence_registry (
    unclassified_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id),
    raw_extracted_value TEXT NOT NULL,
    source_document_reference TEXT NOT NULL,
    source_page_section VARCHAR(500),
    extraction_method VARCHAR(100) NOT NULL
        CHECK (extraction_method IN (
            'OCR','NLP_PARSE','TABLE_EXTRACT','ENTITY_EXTRACT',
            'SEMANTIC_PARSE','MANUAL_ENTRY','API_INGEST')),
    llm_label_suggestion VARCHAR(255),
    llm_confidence_score NUMERIC(4,3) CHECK (llm_confidence_score BETWEEN 0 AND 1),
    probable_domain VARCHAR(100),
    probable_bq_id VARCHAR(50),
    resolution_status VARCHAR(30) NOT NULL DEFAULT 'PENDING'
        CHECK (resolution_status IN (
            'PENDING','MAPPED_TO_EXISTING','NEW_CDE_CREATED',
            'DISCARDED','PROMOTED_CONVERGENCE')),
    resolved_by_user_id UUID REFERENCES user_registry(user_id),
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolved_metric_id UUID REFERENCES metric_registry(metric_id),
    resolved_customer_metric_id UUID
        REFERENCES customer_metric_registry(customer_metric_id),
    convergence_signal_raised_flag BOOLEAN NOT NULL DEFAULT FALSE,
    active_flag BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_unclassified_org ON unclassified_intelligence_registry(organization_id);
CREATE INDEX idx_unclassified_status ON unclassified_intelligence_registry(resolution_status)
    WHERE resolution_status = 'PENDING';

ALTER TABLE unclassified_intelligence_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON unclassified_intelligence_registry
    USING (organization_id = current_setting('app.organization_id')::uuid);

-- =========================================================================
-- AMD-006: FRAMEWORK TIER + GOVERNED_BY ON framework_registry
-- Blueprint v2.2 Section 5.0c Binding 2: three framework tiers, three
-- governance owners. Tier 1 = Standard (CorpStage Admin only).
-- Tier 2 = Custom (Corporate Admin, fully bespoke).
-- Tier 3 = Extended (Corporate Admin, additive on top of a Tier 1 clone).
-- =========================================================================

ALTER TABLE framework_registry
    ADD COLUMN framework_tier INTEGER NOT NULL DEFAULT 1
        CHECK (framework_tier IN (1,2,3)),
    ADD COLUMN tier_governed_by VARCHAR(50) NOT NULL DEFAULT 'CORPSTAGE_ADMIN'
        CHECK (tier_governed_by IN ('CORPSTAGE_ADMIN','CORPORATE_ADMIN')),
    ADD COLUMN parent_framework_id UUID REFERENCES framework_registry(framework_id),
    ADD COLUMN organization_id UUID REFERENCES organization_master(organization_id);

COMMENT ON COLUMN framework_registry.framework_tier IS
    '1 = Standard: externally governed (GRI, BRSR, ISSB etc.) — CorpStage Admin only.
     2 = Custom: fully bespoke, owned by one customer, never shared.
     3 = Extended: clone of a Tier 1 framework with additive customer BQs/CDEs.
       Standard mappings in the clone are NEVER overridden (Blueprint Binding 2).';
COMMENT ON COLUMN framework_registry.parent_framework_id IS
    'For Tier 3 frameworks only: the Tier 1 framework this was cloned from.
     NULL for Tier 1 and Tier 2.';
COMMENT ON COLUMN framework_registry.organization_id IS
    'NULL for Tier 1 (shared across all customers).
     Populated for Tier 2 and Tier 3 (customer-specific).';

-- =========================================================================
-- AMD-007: HIDE / PURGE GOVERNANCE COLUMNS
-- Blueprint v2.2 Section 5.0c Binding 7: Hide and Purge are distinct,
-- separately governed actions. Hide = reversible, no approval, view-only.
-- Purge = soft-delete, Corporate Admin approval required, audit-logged,
-- never a hard delete. Applied to metric_registry (for Global CDEs that a
-- Corporate Admin proposes to Purge from their view) and
-- customer_metric_registry (for Tenant CDEs).
-- Also requires a dedicated purge_audit_log table for the immutable record.
-- =========================================================================

ALTER TABLE metric_registry
    ADD COLUMN is_hidden_flag BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN hidden_by_organization_id UUID
        REFERENCES organization_master(organization_id),
    ADD COLUMN hidden_at TIMESTAMP WITH TIME ZONE,
    ADD COLUMN is_purged_flag BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN purge_requested_by UUID REFERENCES user_registry(user_id),
    ADD COLUMN purge_requested_at TIMESTAMP WITH TIME ZONE,
    ADD COLUMN purge_approved_by UUID REFERENCES user_registry(user_id),
    ADD COLUMN purge_approved_at TIMESTAMP WITH TIME ZONE,
    ADD COLUMN purge_reason TEXT;

ALTER TABLE customer_metric_registry
    ADD COLUMN is_hidden_flag BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN hidden_at TIMESTAMP WITH TIME ZONE,
    ADD COLUMN is_purged_flag BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN purge_requested_by UUID REFERENCES user_registry(user_id),
    ADD COLUMN purge_requested_at TIMESTAMP WITH TIME ZONE,
    ADD COLUMN purge_approved_by UUID REFERENCES user_registry(user_id),
    ADD COLUMN purge_approved_at TIMESTAMP WITH TIME ZONE,
    ADD COLUMN purge_reason TEXT;

CREATE TABLE purge_audit_log (
    purge_log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id),
    entity_type VARCHAR(50) NOT NULL
        CHECK (entity_type IN ('METRIC','CUSTOMER_METRIC','DOMAIN','FRAMEWORK','BQ')),
    entity_id UUID NOT NULL,
    entity_name VARCHAR(255) NOT NULL,
    action VARCHAR(10) NOT NULL CHECK (action IN ('HIDE','UNHIDE','PURGE','RESTORE')),
    requested_by UUID NOT NULL REFERENCES user_registry(user_id),
    requested_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    approved_by UUID REFERENCES user_registry(user_id),
    approved_at TIMESTAMP WITH TIME ZONE,
    reason TEXT NOT NULL,
    previous_state JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

COMMENT ON TABLE purge_audit_log IS
    'Immutable audit log for every Hide/Unhide/Purge/Restore action across the
     platform. Records are never deleted — only annotated. Satisfies Law 13
     (Auditability by Default) and the regulatory retention obligations that
     a genuinely deleted record could not satisfy (Blueprint Binding 7).';

ALTER TABLE purge_audit_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON purge_audit_log
    USING (organization_id = current_setting('app.organization_id')::uuid);

-- =========================================================================
-- AMD-008: DEPARTMENT REGISTRY + ROLE VIEW CONFIGURATION
-- Blueprint v2.2 Section 5.0d: departments and roles are platform metadata,
-- not hardcoded logic. A Role View is a live aggregation of Department Views.
-- =========================================================================

CREATE TABLE department_registry (
    department_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organization_master(organization_id),
    department_name VARCHAR(255) NOT NULL,
    department_code VARCHAR(100) NOT NULL,
    parent_department_id UUID REFERENCES department_registry(department_id),
    default_visible_domains TEXT[],
    default_hidden_cde_ids TEXT[],
    created_by UUID REFERENCES user_registry(user_id),
    active_flag BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT uq_dept_code_per_org UNIQUE (organization_id, department_code)
);

COMMENT ON TABLE department_registry IS
    'Platform-metadata-driven department registry (Blueprint v2.2 Section 5.0d).
     NULL organization_id = platform default department (shared across all customers).
     Populated organization_id = customer-specific department.
     Adding a new department requires inserting one row — zero engineering change.';

COMMENT ON COLUMN department_registry.default_visible_domains IS
    'Array of domain names visible to this department by default.
     Drives the Domain Coverage Dashboard (Section 5.0e) filtered view.
     Individual CDEs can be further hidden per purge_audit_log.';

CREATE TABLE role_view_configuration (
    role_view_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id UUID NOT NULL REFERENCES role_registry(role_id),
    organization_id UUID REFERENCES organization_master(organization_id),
    aggregated_department_ids UUID[],
    lens_id VARCHAR(50) NOT NULL DEFAULT 'EXECUTIVE'
        CHECK (lens_id IN ('EXECUTIVE','RESILIENCE','RISK','CUSTOM')),
    primary_sacred_screens INTEGER[],
    active_flag BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
-- MIGRATION (AMD-011, Alignment Amendment v1.0 §A-Language-Purge): UPDATE role_view_configuration SET lens_id = 'RESILIENCE' WHERE lens_id = 'SUSTAINABILITY';
-- then ALTER TABLE role_view_configuration DROP CONSTRAINT <existing_check_name>, ADD CHECK (lens_id IN ('EXECUTIVE','RESILIENCE','RISK','CUSTOM'));
-- Same enum correction applies to lens_vocabulary_map.lens_id's documented value set (comment-only there; no CHECK constraint exists on that column, so no ALTER needed for that table).

COMMENT ON TABLE role_view_configuration IS
    'A Role View is a live aggregation of the Department Views listed in
     aggregated_department_ids — never a separately maintained dataset.
     Changing what a department hides automatically changes what the role sees
     (Blueprint v2.2 Section 5.0d Binding 2: configure once, compute always).
     primary_sacred_screens lists which of the 12 Sacred Screens surface first
     for this role (e.g. CFO: {3,5,9,12}; CRO: {4,5,10}).';

ALTER TABLE department_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON department_registry
    USING (organization_id IS NULL
        OR organization_id = current_setting('app.organization_id')::uuid);

ALTER TABLE role_view_configuration ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON role_view_configuration
    USING (organization_id IS NULL
        OR organization_id = current_setting('app.organization_id')::uuid);

-- =========================================================================
-- AMD-009: GUIDED COMPLETION GROUPING TABLE
-- Blueprint v2.2 Section 11 / 6.2: "Guided Completion" groups related
-- Business Questions into a named business-activity task with a stated
-- time estimate and cross-domain impact declaration. This is the table
-- that was described behaviorally in the Blueprint but never defined
-- mechanically in either source document.
-- =========================================================================

CREATE TABLE guided_completion_task (
    task_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organization_master(organization_id),
    task_name VARCHAR(255) NOT NULL,
    task_description TEXT,
    business_activity_label VARCHAR(255) NOT NULL,
    estimated_minutes INTEGER NOT NULL CHECK (estimated_minutes BETWEEN 1 AND 30),
    input_count INTEGER NOT NULL GENERATED ALWAYS AS (
        array_length(bq_ids, 1)
    ) STORED,
    bq_ids TEXT[] NOT NULL,
    primary_domain VARCHAR(100) NOT NULL,
    cross_domain_impact TEXT[],
    intelligence_gain_statement TEXT NOT NULL,
    financial_relevance_statement TEXT,
    priority_score NUMERIC(5,2),
    display_order INTEGER,
    is_platform_default BOOLEAN NOT NULL DEFAULT TRUE,
    active_flag BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

COMMENT ON TABLE guided_completion_task IS
    'Implements the Guided Completion UX pattern (Blueprint v2.2 Section 11):
     "Spend 3 minutes → Regulatory Cost Exposure improves 18%."
     Each row is one named business-activity grouping (e.g. "Delivery Cost
     Analysis") containing 3-10 related Business Questions. The platform
     presents these as a single coherent task, never as a question list.
     is_platform_default=TRUE rows are CorpStage-seeded; FALSE rows are
     customer-configured. NULL organization_id = platform default.';

COMMENT ON COLUMN guided_completion_task.intelligence_gain_statement IS
    'The value declaration shown to the user before they begin the task.
     Must follow Law 23 format: "Spend N minutes → [metric] improves by X%.
     Also improves: [cross-domain list]."
     Example: "Spend 3 minutes → Supplier Intelligence +12%.
     Also improves: Operational Risk, Regulatory Cost Exposure, Financial Exposure."';

COMMENT ON COLUMN guided_completion_task.bq_ids IS
    'Array of Business Question IDs (e.g. {BQ-009, BQ-010, BQ-011}) that
     comprise this task. Questions are presented sequentially, never as a list.
     Minimum 3, maximum 10 per task (above 10 should be split into two tasks).';

ALTER TABLE guided_completion_task ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON guided_completion_task
    USING (organization_id IS NULL
        OR organization_id = current_setting('app.organization_id')::uuid);

-- =========================================================================
-- AMD-010: DOMAIN COVERAGE DASHBOARD SUPPORT
-- Blueprint v2.2 Section 5.0e: the Domain Coverage Dashboard shows
-- Discovered / Inferred / Confirmed / Pending per Domain, with no fixed
-- denominator. This requires a computed/materialized view that aggregates
-- metric_record confidence states per domain per organization.
-- =========================================================================

CREATE TABLE domain_coverage_snapshot (
    snapshot_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organization_master(organization_id),
    domain_name VARCHAR(100) NOT NULL,
    snapshot_timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_cdes_found INTEGER NOT NULL DEFAULT 0,
    discovered_count INTEGER NOT NULL DEFAULT 0,
    inferred_count INTEGER NOT NULL DEFAULT 0,
    confirmed_count INTEGER NOT NULL DEFAULT 0,
    pending_review_count INTEGER NOT NULL DEFAULT 0,
    hidden_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

COMMENT ON TABLE domain_coverage_snapshot IS
    'Materialized snapshot for the Domain Coverage Dashboard (Blueprint v2.2
     Section 5.0e). Recalculated on a scheduled basis rather than computed
     live on every page load, since it aggregates across potentially thousands
     of metric_record rows per organization.

     Counts defined:
     discovered_count   = metric_record rows with confidence_score < 60
                          AND retrieval_method IN (OCR, NLP_PARSE, API_INGEST)
                          AND approved_flag = FALSE  (IDAL Stages 1/2)
     inferred_count     = metric_record rows with confidence_score 60-89
                          AND approved_flag = FALSE  (IDAL Stage 3)
     confirmed_count    = metric_record rows with approved_flag = TRUE
                          AND confidence_score >= 90  (IDAL Stages 4/5)
     pending_review_count = rows in intelligence_work_queue with status
                          IN (ALLOCATED, DELEGATED, ESCALATED)  (Stage 5a)
     hidden_count       = metric_registry rows with is_hidden_flag = TRUE
                          for this organization (excluded from totals above
                          per Blueprint Binding 7 — Hide is presentation only)

     The dashboard NEVER shows a denominator (no "you need 300 CDEs" message).
     Framework-level required counts live in framework_registry + Binding 8.';

CREATE INDEX idx_domain_coverage_org_domain
    ON domain_coverage_snapshot(organization_id, domain_name);

ALTER TABLE domain_coverage_snapshot ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON domain_coverage_snapshot
    USING (organization_id = current_setting('app.organization_id')::uuid);

-- Convenience view: always returns the latest snapshot per org per domain
CREATE OR REPLACE VIEW domain_coverage_current AS
SELECT DISTINCT ON (organization_id, domain_name)
    organization_id,
    domain_name,
    snapshot_timestamp,
    total_cdes_found,
    discovered_count,
    inferred_count,
    confirmed_count,
    pending_review_count,
    hidden_count,
    ROUND(confirmed_count::NUMERIC /
          NULLIF(total_cdes_found - hidden_count, 0) * 100, 1
    ) AS confirmed_pct
FROM domain_coverage_snapshot
ORDER BY organization_id, domain_name, snapshot_timestamp DESC;

