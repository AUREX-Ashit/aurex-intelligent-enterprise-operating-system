# IRA-C066 — Evidence Management (C-066) — Implementation Readiness Assessment

**Document ID naming note (established fact + repository rule, stated up front):** every prior IRA in this repository is named `IRA-0XX_WP-0X_...` — WP-number-first. This document is deliberately named **capability-first, with no WP number**, because `WPR-001` §3 (Maintenance Rule) states explicitly: *"No future WP may be added speculatively. If a document elsewhere in the repository casually mentions a future WP number without it being backed by an accepted IRA or a real commit, that mention is non-authoritative and SHALL NOT be copied into this table until it is properly assigned."* No WP number exists for C-066 anywhere in `WP-REG-001` or `WPR-001` as of this document's own drafting. Assigning one here — before this IRA is even accepted — would itself violate that rule. A WP number is assigned only once this IRA (or a successor) is accepted and `WPR-001`/`WP-REG-001` are updated to record it, mirroring how every existing WP number first appears in those two registers, never invented inside an IRA in advance of them.

**Remediation provenance (2026-08-24):** this revision addresses **Finding 1** of the independent Repository Owner Review of this IRA's own original draft — the omission of `CLAUDE.md §21.3`'s three mandatory reviews (Strategic Enhancement, Historical Screen, Executive Cognition), including the specific unclassified `SE-051` gap that review identified — and separately corrects two non-blocking citation/cross-reference defects that same review found (§3.1, §16, §21.3 reviews below). No prior finding, discrepancy, or Repository Owner decision recorded in this document's own original draft has been removed or silently altered by this remediation; §6a/§6b/§6c below are new. This remediation was performed by the same session that authored the original IRA and is **not independently certified** — a fresh independent review of this updated document remains the required next step before any TDS or implementation authorization (§18).

**Repository Owner authorization basis for this document:** Repository Owner instruction, this session, explicitly scoped to "begin the governed IRA/readiness process" for C-066 only — not implementation, not a TDS, not a WP charter.

**Acceptance provenance (2026-08-24):** this revision further records that the Repository Owner has since reviewed and **accepted** this IRA, per a separate, explicit Repository Owner Instruction ("C-066 IRA Acceptance → Technical Design Preparation"), authorizing progression to the governed Technical Design stage only (§18 records this in full). Acceptance does not itself assign a WP number, charter BA-01, or authorize implementation — each remains a distinct, not-yet-performed governance step, per §18. `TDS-015_C066_BA-01_Understand_Evidence_Context_Technical_Design.md` was subsequently authored on this basis, independently reviewed (verdict: PASS WITH CONDITIONS), and remediated against that review's findings.

---

## 1. Executive Summary

**(Established fact.)** C-066 Evidence Management is `CAP-001`-registered (Active, Domain D-004 Enterprise Operations, owning specification `SD-002` §6 "Evidence & Source Intelligence Rules," rules `SD-002-040` through `SD-002-050`). No Business Activity has ever been chartered against C-066. No IRA has ever existed for it. A physical table directly relevant to C-066's own subject matter — `evidence_registry` — already exists, is populated in production by two other, already-closed Work Packages (WP-11, WP-14), and is tenant-scoped and tested. **No read/query capability exists against it anywhere in this repository.** This is the one clean, bounded, evidence-backed gap this assessment identifies as C-066's own genuine minimum first increment — directly analogous in shape to `IRA-006`/WP-06's own "Read APIs against an already-existing table" precedent, though this assessment does not assume that shape is automatically correct without first tracing it from `SD-002` §6's own rules (§7 below).

**Readiness verdict (§17): READY, at a minimum scope — one candidate Business Activity, backend-only, zero new schema.** **IRA Acceptance: GRANTED, 2026-08-24**, per Repository Owner Instruction "C-066 IRA Acceptance → Technical Design Preparation" (§18 records this in full, including the precise, distinct boundary between IRA acceptance, WP assignment, BA authorization, and implementation authorization — none of the latter three is granted by this acceptance).

---

## 2. Capability Analysis

**(Established fact, `CAP-001` line 75, direct read.)**

| Field | Value |
|---|---|
| Capability ID | C-066 |
| Capability Name | Evidence Management |
| Description | "Manage enterprise evidence." |
| Domain | D-004 — Enterprise Operations (C-060–C-089) |
| Owning Specification | `SD-002` |
| Status | Active |

**(Established fact, `SD-002` §6, full text read directly — not paraphrased from a prior session's summary.)** `SD-002` §6 opens with a formalization note (per `ARP-001 WP-5`): *"this section's Evidence, confidence, and source rules are the foundation Enterprise Intelligence reasoning builds on. `EIA-001` Vol. II §12's Knowledge Asset model — Provenance, Confidence, Freshness, Authority, Lineage — extends these rules into the Enterprise Intelligence domain specifically; it does not define a competing Evidence concept."* This directly cross-references and subordinates to `SD-002` §6 the exact Evidence-adjacent language already used by WP-14's own `TDS-013`/`IRA-014` — confirming C-066/`SD-002` §6 is the single upstream authority Evidence-adjacent work in this repository already answers to, not a new or competing concept.

The ten rules, verbatim in substance (full text read, `SD-002_Universal_Business_Object_Rules.md` lines 257–299):
- **SD-002-040**: Evidence is a first-class Business Object (identity, ownership, versioning, relationships, confidence, events, audit, lifecycle — inheriting §2 in full), not a file attachment.
- **SD-002-041**: No CDE exists without Evidence capability ("No Evidence, No Trust") — capability must be universal; not every CDE must have evidence attached at all times.
- **SD-002-042**: Evidence may originate from any recognized source class (document, enterprise, public, human, AI), each with its own reliability weighting.
- **SD-002-043**: Evidence supports granular references (document/page/section/table/cell) where the source format permits.
- **SD-002-044**: Evidence is reusable across objects — duplicating the same evidence record per consuming object is a modeling error.
- **SD-002-045**: Evidence confidence is independently scored, distinct from and contributing to any CDE's own confidence.
- **SD-002-046**: Evidence preserves immutable original sources; AI enrichment is additive metadata only.
- **SD-002-047**: Evidence supports multi-modal formats (document, image, audio, video, structured data).
- **SD-002-048**: Evidence retention has a governed floor — minimum 7 years or the applicable statutory minimum, whichever is longer; may be raised, never lowered without documented governance approval.
- **SD-002-049**: Cross-object data lineage is explicit — a number in a Report traces backward through its Activity, CDEs, and each CDE's own evidence as one continuous chain.
- **SD-002-050**: Evidence is human-governed — AI may discover/classify/summarize/recommend; only humans approve/reject/override/archive.

**(Established fact.)** `SD-002` §2 (`SD-002-004` through `SD-002-020`) is the Universal Business Object Model every subtype, including Evidence, inherits "in full" per §6's own text. This is the same aspirational, full canonical blueprint (registered identity via a Canonical Business Object Register, full event-sourcing, bulk operations, full extensibility) that **no Business Object anywhere in this repository has ever implemented literally in full** — every certified WP to date (WP-01 through WP-14) implements a disclosed, narrower, LOCKED-schema subset, not the complete aspirational model. This assessment treats that same established repository pattern as governing here too (§8), not as a new standard C-066 alone must meet in full.

---

## 3. Existing Asset Discovery (`CLAUDE.md §19.2`, `IMP-001 §6.2a`)

**(Established fact, direct repository inspection — not accepted from any prior session's summary.)**

### 3.1 Physical schema

`evidence_registry` exists (`Master_Technical_Architecture.md` lines 2342–2350+), a **pre-existing base-schema table**, not an AMD amendment (no AMD number governs its own creation — distinguished explicitly from `AMD-012`'s own siblings). Its architecture-document header: *"Stores evidence supporting intelligence. Supports: metrics, risk scores, financial assumptions, regulatory disclosures, AI recommendations, board narratives. Examples: utility invoices, audit reports, supplier declarations, regulatory filings, IoT logs."* FK per Chapter 9: `node_id -> organization_node`, `uploaded_by -> user_registry`, `organization_id -> organization_master` (the last already realized; the first two are **not** present in the actual physical Backend model at all — a distinct gap from §3.4's own RLS finding below; recorded as its own item at §16 item 5).

### 3.2 Physical Backend model (`Backend/Services/AIService/models/search.py:70–105`)

`EvidenceRegistryModel`, table `evidence_registry`, columns: `evidence_id` (PK), `evidence_type`, `linked_entity_type`, `linked_entity_id`, `evidence_source`, `file_reference`, `source_timestamp`, `confidence_score`, `externally_verified_flag`, `legal_defensibility_flag`, `retention_policy`, `document_hash_signature`, `ai_extracted_flag`, `active_flag`, `created_at`, `organization_id` (`NOT NULL`, indexed). The model's own docstring: *"WP-11 BA-03 (Register Enterprise Search Content) writes this table — narrowly: a caller-supplied text passage's own evidence record, not a real document-ingestion/discovery pipeline (`IRA-011 §4.2`, C-090's own future domain)."*

**(Discrepancy, recorded not resolved):** this docstring names **C-090** (Enterprise Discovery, realized by WP-14) as the "future domain" for a real document-ingestion pipeline into this table — not C-066. Independently checked: WP-14's own BA-01/BA-02 write to `discovery_provider_registry`/`unclassified_intelligence_registry`, never to `evidence_registry` — so no actual overlap exists in delivered code, but the docstring's own framing suggests whoever wrote it in 2026-08 did not clearly anticipate C-066 as `evidence_registry`'s own eventual capability owner. Flagged for Repository Owner awareness (§16), not resolved here.

### 3.3 Existing write paths (`Backend/Services/AIService/repositories/search_repository.py:134–188`)

Exactly two write methods exist on `EvidenceRegistryRepository`, both already delivered and certified under **other** capabilities:
- `create()` — WP-11 BA-03 (Register Enterprise Search Content, **C-093**), unmodified since.
- `create_linked()` — WP-14 BA-03 (Resolve Enterprise Intelligence Candidate, **C-090/C-091**), added explicitly to satisfy `SD-002-041` "using already-real infrastructure, no new schema" (method's own docstring).

**No `get_by_id`, `list`, `search`, or any other read/query method exists anywhere against `EvidenceRegistryModel`** — confirmed by direct, complete read of `EvidenceRegistryRepository`'s own class body; it contains exactly the two write methods above and nothing else.

### 3.4 RLS — documented, not physically enforced (parallel to BA-05's own `TD-150`)

`Master_Technical_Architecture.md` lines 4520–4522 document: `ALTER TABLE evidence_registry ENABLE ROW LEVEL SECURITY; CREATE POLICY org_isolation ON evidence_registry USING (organization_id = current_setting('app.organization_id')::uuid);` — **but no AIService Alembic migration creates this policy** (independently re-confirmed by the same class of check already performed three times this session for BA-05's own `TD-150`: zero `CREATE POLICY`/`ENABLE ROW LEVEL SECURITY` in `Backend/Services/AIService/alembic/versions/*.py`). This is the identical repository-wide pattern already disclosed for `enterprise_knowledge_graph_registry`, `knowledge_asset_registry`, and every other AMD-012-era table — not a C-066-specific gap.

### 3.5 Logical service ownership is contested across three service boundaries — none physically real

`Master_Technical_Architecture.md`'s own PART F component addendum assigns `evidence_registry` to **three different logical services** in three different places: "Document Ingestion Service" (line 5055–5056, "Owns: `data_ingestion_registry`, `evidence_registry`"), the "Retrieval Service" boundary description (line 4980, referencing it as a stored-document source alongside `data_ingestion_registry`), and "Workflow Service" (lines 5328–5331, listing `evidence_registry` among its "real table ownership" alongside `action_tracker`/`workflow_execution`/`intelligence_work_queue`). **None of these three named logical services physically exists as a distinct microservice anywhere in this repository** (the actual five physical services are `AIService`, `AuthService`, `IngestionService`, `ReportingService`, `TenantService` — the same closed set BA-05's own `TDS-013 §20` already established). `evidence_registry` is physically hosted in `AIService` today, exactly the same "logical component vs. physical hosting service" distinction `TDS-013`/`RO-DEC-WP14-BA05-03` already resolved for `enterprise_knowledge_graph_registry`. **Discrepancy, recorded not resolved:** three different, mutually non-exclusive logical-ownership claims exist for the same table, none reconciled anywhere. This does not block hosting a first C-066 BA in `AIService` (the physical status quo, zero migration required) — it is flagged as a documentation-consistency item for Repository Owner awareness (§16), the same class of gap `TDS-013 §20` already carried and disclosed for BA-05 before its own hosting question was separately settled by `RO-DEC-WP14-BA05-03`.

### 3.6 `SE-031` — a distinct, unimplemented, unrelated table (resolves objective #4)

`SER-001` line 75: *"`SE-031` | AI Evidence Fusion table — seven fixed dimensions (Coverage/Quality/Diversity/Freshness/Consistency/Confidence/Cost+Latency); table does not exist in any migration... Target: Release C | Status: Unassigned... Deferred."* Independently traced to its own named physical table, `evidence_fusion_registry` (`Master_Technical_Architecture.md` lines 3393–3410+, `AMD-013`) — a genuinely distinct table from `evidence_registry`, with its own PK (`evidence_fusion_id`) and its own purpose (AI-output confidence/sufficiency scoring across fused evidence, not evidence storage itself). Independently confirmed **zero Backend model exists anywhere for `evidence_fusion_registry`** (direct repository-wide search, zero hits).

**Conclusion (established fact + direct inference):** `SE-031` is **not** the correct SER boundary for a first C-066 increment built around the already-real `evidence_registry` table — it targets a wholly different, wholly unimplemented table, for a materially different purpose (AI-fusion scoring, not evidence storage/retrieval). A minimum C-066 charter scoped to `evidence_registry`'s own retrieval gap (§3.3) **does not touch `SE-031` at all.** `SE-031` remains a distinct, separately-deferred future enhancement, unaffected by anything this assessment proposes.

### 3.7 No `PE-001-C066` or capability-specific Experience spec exists

**(Established fact.)** Direct filesystem search for `PE-001-C066`, `PE-001*Evidence*`, or any capability-specific Experience document naming C-066: zero hits. C-066 is governed only by `SD-002` §6's own general Business Object rules — the same posture `C-093`/`C-090`/`C-091`/`C-092` each had before their own first Technical Design (none of them had a dedicated `PE-001-Cxxx` file either; `SD-001`/`IRA-014`/`TDS-013` governed instead). Not a blocker; recorded as the baseline this assessment works from.

### 3.8 Existing IRA/BA/authorization history for C-066

**(Established fact.)** None — confirmed by direct search (`IRA-C066`, `IRA-066`, or any BA decomposition naming C-066): zero prior hits anywhere in `architecture/`, `WP-REG-001`, or `WPR-001`.

---

## 4. What Must NOT Be Duplicated — Explicit Reuse-vs-New-Scope Boundary

**(Established fact + explicit governance discipline, per the Repository Owner's own instruction not to treat existing infrastructure as capability completion.)**

WP-11's `create()` and WP-14's `create_linked()` write paths are **not C-066's own implementation** — they are **C-093's** (Enterprise Search) and **C-090/C-091's** (Enterprise Discovery/Knowledge Management) own respective consumption of a shared, pre-existing Business Object, exactly as `SD-002-044` itself requires ("Evidence Is Reusable Across Objects... one evidence record may support many CDEs simultaneously"). Neither WP-11 nor WP-14 was ever chartered against C-066; neither delivered any Business Activity whose own stated business outcome is "manage enterprise evidence" as its own end (both used Evidence instrumentally, in service of Search content registration and Intelligence Candidate resolution respectively). **A first C-066 BA MUST NOT re-implement, modify, or re-certify either existing write path** — both remain the sole province of their own already-closed, already-certified Work Packages, and any C-066 charter that touched them would itself violate `CLAUDE.md §8` (service/capability boundary discipline) by reopening already-closed, unrelated capability work.

What genuinely remains unimplemented and would belong to a first C-066 BA specifically: **read/query access to the Evidence a caller's own Organization already owns** — the one capability gap directly evidenced in §3.3, touching no other capability's own delivered scope.

---

## 5. Business Object Eligibility Analysis (`CMD-001 §26.3a`)

**(Established fact + direct inference.)** Not applicable in the "new Business Object" sense — Evidence is already a registered concept (`SD-002` §6, physically realized as `evidence_registry`, already reused by two closed WPs). No new Canonical Business Object is proposed by this assessment. `evidence_registry`'s own registration/ownership provenance remains with `AMD-012`'s general schema-authority framing (§3.1); this assessment neither creates nor re-registers it.

---

## 6. Gap Analysis (`IMP-001 §6.2b`, category A–E — mirroring `IRA-006 §7`'s own applied framework)

### 6a. Strategic Enhancement Review (`CLAUDE.md §21.3`) — added in remediation of independent-review Finding 1

Per `SER-001`, every enhancement relevant to C-066 is classified below (repository-wide search performed for "C-066," "Evidence," and `evidence_registry`, not limited to entries already suspected relevant):

| SE | Enhancement | Disposition for C-066 |
|---|---|---|
| `SE-031` | AI Evidence Fusion table (`evidence_fusion_registry`, `AMD-013`) | **Not Applicable** to this assessment's proposed minimum scope — targets a distinct, wholly unimplemented table for AI-fusion scoring, not evidence storage/retrieval (§3.6, unchanged finding). Remains Deferred in `SER-001`'s own status field, unaffected by this IRA. |
| `SE-051` | Retention policies (general, tenant/category-configurable, 7-year constitutional floor for audit-relevant evidence) — `SD-002-048`/`053`/`058`/`081` | See dedicated classification immediately below (resolves the independent review's specific Finding 1 request). |
| `SE-001`/`SE-007`/`SE-008` | Progressive Disclosure / Evidence Panel / AI-transparency sequencing — a UI component pattern named "Evidence," unrelated to the `evidence_registry` Business Object | **Not Applicable** — a distinct, cross-cutting Design System concept (already delivered by WP-12), sharing only the word "Evidence," not the Business Object or `SD-002` §6's own rules. Named here only to foreclose a plausible naming confusion between "Evidence Panel" (UI widget) and "Evidence" (Business Object) — no substantive relationship to C-066 exists. |
| `SE-030` | AI confidence — real, non-stub computation (`RTA-001 §13.11`) | **Not Applicable** — governs the *computation* of confidence scores platform-wide, not Evidence storage/retrieval. `evidence_registry.confidence_score` is a column BA-01 (§7) would expose read access to as-is; correctly *populating* it is `SE-030`'s own separate, cross-cutting, already-Deferred concern, not something a read-only BA touches. |

No other `SER-001` entry names C-066, `evidence_registry`, or Evidence-as-a-Business-Object specifically (confirmed by direct full-register search).

**`SE-051` — dedicated classification (resolves the independent review's Finding 1 request precisely):**

**Classification: NOT APPLICABLE to BA-01's own proposed minimum scope — with an explicit, disclosed CONSTRAINT recorded for C-066's own broader, future scope.**

- **Architectural relevance (established fact):** Genuine — `SE-051`'s own Governing Doc column names `SD-002-048` directly, one of C-066's own ten governing rules (§2), specifically the 7-year retention-floor rule for evidence.
- **Requirement of BA-01 specifically (direct inference):** No. BA-01 (§7) is read-only — it does not create, mutate, delete, or purge any `evidence_registry` row. Retention-floor *enforcement* is a lifecycle-management/write-path concern; a pure read endpoint has no operational dependency on whether purge/retention enforcement exists or not.
- **Dependency vs. constraint (direct inference):** Not a dependency — BA-01 does not require `SE-051` to be built first, and nothing about it changes if `SE-051` remains unbuilt indefinitely. It is instead a disclosed *constraint on C-066's own eventual full scope*: any future C-066 Business Activity that writes, deletes, or purges Evidence would need to account for `SD-002-048`'s own retention floor, and `SE-051` remains the tracked mechanism for building that enforcement.
- **Deferred status (established fact):** Confirmed directly — `SER-001` (`SE-051` row): Status `Deferred`, Planned Release `Unscheduled`, Planned WP `Unassigned`.
- **Blocks implementation of BA-01? (direct inference):** No — BA-01's own minimum scope has zero operational dependency on retention-floor enforcement existing. Not a condition of this IRA's own readiness verdict (§17, unchanged).

### 6b. Historical Screen Review (`CLAUDE.md §21.3`) — added in remediation of independent-review Finding 1

`HISTORICAL-SCREEN-REALIZATION-MATRIX.md` (line 29) names exactly one EVOLVE CONCEPT screen touching Evidence-adjacent subject matter: `F1_Enterprise_Understanding_Center.html` — "Synthesize uploaded enterprise documents into confidence-scored, routable executive intelligence... Evidence-first, AI-assisted enterprise understanding." **This screen is explicitly scoped to C-090 Enterprise Discovery**, per its own matrix entry ("No chartered Work Package exists yet (C-090 Enterprise Discovery, Active, unchartered)") — a document-ingestion/synthesis concept, not an Evidence-record read/query concept, and not C-066-owned. No historical screen concept exists anywhere in the matrix specifically for a plain Evidence-record retrieval/understand interface — the shape BA-01 (§7) proposes. Plan B (Enterprise Experience, §9, undecided) is therefore not constrained or informed by historical screen precedent — only by `SD-001`/`PE-001` directly, mirroring `IRA-011 §4b`'s own identical finding for its own analogous case (no historical screen exists for WP-11's own plain query surface either).

No prior Technical Debt entry or gate finding names `evidence_registry`, C-066, or a read-path gap against this table specifically (confirmed by search of `TECH-DEBT.md` — the only relevant hits are the repository-wide RLS-disclosure pattern already noted at §3.4, `TD-150`'s own class, not a distinct C-066 debt item). `IMP-REPORT-WP-06`/`CERT-WP-06` (the "Read APIs against an already-existing table" precedent this assessment's own §7/§17 rely on) is independently re-confirmed here as the directly relevant historical shape-precedent; no historical decision found anywhere that would constrain, prohibit, or reinterpret that shape for C-066.

### 6c. Executive Cognition Review (`CLAUDE.md §21.3`) — added in remediation of independent-review Finding 1

`EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md` (lines 21–25, 45, 49) states genuine Executive **Decide**-stage cognition support "requires real Evidence/Confidence (`SD-002 §6`)... gated on Enterprise Intelligence capabilities (C-090+) existing," and separately names `SE-030`/`SE-031` (confidence computation, evidence-fusion scoring) — not `evidence_registry`'s own existence, which already exists — as the properties that specific gate depends on. That same document's own **Understand**-stage principle (line 21: "Evidence-first presentation of whatever data already exists — governed by `PE-001` Chapter 23, applicable to any capability") is the directly relevant standard for BA-01: a plain "what Evidence does my Organization already have, and what does it say" read capability is squarely an Understand-stage Executive-cognition function, not a Decide-stage one — it makes no claim to AI-assisted decision support, confidence computation, or synthesis, and correctly attempts none of these.

**Assessed against BA-01 (§7) specifically:**
- **Business/user question enabled:** "What Evidence exists for [an entity my Organization owns], and what are its own properties (source, confidence, verification status, provenance)?" — a genuine Understand-stage question, not merely infrastructure exposure for its own sake.
- **Consumer:** any Organization-scoped caller needing to inspect Evidence already registered against their own data — not yet a named Executive persona specifically, since no `PE-001-C066` exists (§3.7) to name one; this remains a proposed, not decided, consumer model.
- **Outcome:** direct visibility into a Business Object that today has **zero read access anywhere in the platform** (§3.3, unchanged finding) — closing a real, narrow, precisely-bounded capability gap, not merely exposing a table for exposure's own sake.
- **Meaningful at capability level?** Yes, narrowly — the *first* realization of C-066 as a capability any caller can actually interact with, mirroring the same "first conforming/first realized minimum" precedent already accepted for WP-06 (Domain Permission's own first Understand capability) and WP-11 BA-01 (Search's own first Establish capability).
- **Too technical/narrow to qualify as a genuine Business Activity?** No — `SD-002-054`'s own seven-question audit standard (Who/What/Why/When/How/Using Which Evidence/Under Which Policy) is itself constitutional-text evidence that "being able to answer questions about Evidence" is already treated as a first-class governance concern in this repository, not a merely-technical convenience.
- **Backend-only defensible, or is Enterprise Experience required for BA-01 to be meaningful?** Backend-only is defensible — a caller (human operator or another internal service) obtains the full value of BA-01 via API alone; nothing in `PE-001` Chapter 23's own text requires a dedicated screen for every Understand-stage capability to be meaningful, and `IRA-011 §4b`'s own precedent (a query surface delivered without a dedicated Executive screen) already established this exact pattern as acceptable for a first increment. This does **not** resolve §14 item 2 (backend-only vs. Enterprise Experience) as a decided fact — it remains an explicit Repository Owner scope decision, not self-selected by this review; it establishes only that backend-only scope would not itself make BA-01 meaningless.

**Conclusion:** BA-01 delivers a coherent, if narrow, Understand-stage Executive-cognition outcome — not merely infrastructure exposure — and does not structurally require Enterprise Experience to be meaningful at its own proposed minimum scope. §14 item 2 remains open as a Repository Owner scope decision, not resolved by this review.

---

| Candidate BA | Category | Reasoning |
|---|---|---|
| BA-01 — Understand Evidence Context (proposed, §7) | **C** (Architecture requires completion — implementation-level only) | No governance question, no missing Business Object, no missing table. `EvidenceRegistryModel`, `organization_id`-scoped tenant boundary, and the already-certified `require_platform_admin`/`require_matching_tenant_or_platform_admin` authorization pattern all already exist and are directly reusable. The only implementation-level design decision (exact filter/query shape) is an ordinary API design question, not a constitutional one — the same conclusion `IRA-006 §7` reached for the structurally identical WP-06 case. |

**Constitutional-vs-Implementation blocker distinction applied (same framework `IRA-006`/`ADR-014`/`METH-001` already establish):** no question here determines Business Object eligibility or requires a new entity, table, API, service boundary, or business rule not already authorized by `SD-002` §6/§2. Every open question is "how much of the already-real table's own read access to build now" — an Implementation Blocker class question, not a Constitutional one.

---

## 7. Candidate Business Activities (Proposed Scope — NOT authorized by this document)

**(Proposed scope, explicitly not yet authorized.)** Derived from `SD-002` §6's own rules and §3's own gap finding, **not assumed from the WP-06 precedent's shape alone** (per the Repository Owner's own explicit caution):

### BA-01 (candidate) — Understand Evidence Context

- **Business Intent:** retrieve the current governed state of an Evidence record — by identity, or by a filtered criterion (`linked_entity_type`/`linked_entity_id`, `evidence_source`, `evidence_type`) — without establishing, mutating, or altering any object returned. Directly realizes `SD-002-040`'s own "first-class... governed object" framing for the read side, and `SD-002-044`'s "reusable across objects" principle by making that reuse queryable for the first time (today, reuse only happens via internal FK joins inside other WPs' own repository code — §3.3 — never a caller-facing capability).
- **Input contract (proposed):** single-item branch, `evidence_id` (UUID, path parameter); list branch, `linked_entity_type`/`linked_entity_id`/`evidence_source`/`organization_id`-implicit filters (all independently optional, mirroring `IRA-006`'s own BA-01 shape).
- **Output contract (proposed):** a `EvidenceResponse` schema (new, minimal — direct field mapping of the existing model, no new derived data).
- **Business rules:** read-only — no `evidence_registry` row created, mutated, or transitioned. Never returns another Organization's own row.
- **Validation rules:** standard path/query-parameter type coercion only.
- **Authorization (proposed, to be confirmed at Technical Design, not decided here):** `require_matching_tenant_or_platform_admin` (the `WP-10`-established pattern `ADR-023 §5` item 5 already names as this repository's own default for a read path against an `organization_id`-scoped table) — **not** `require_platform_admin`-only, since Evidence is inherently a broadly-consumed, cross-capability object (§3.3's own two existing consumer capabilities), unlike a narrowly-administered configuration object. This is a proposed default, not a Repository Owner decision recorded here (§16).
- **Idempotency:** naturally idempotent — pure read, no side effect.
- **AI Assistance:** none — `SD-002-050` reserves evidence governance actions (approve/reject/override/archive) to humans; a read-only BA touches none of those actions.
- **Domain Events:** none published — a read has nothing to announce, the same basis `OrganizationService.get_details()`/`IRA-006`'s own BA-01 already established.
- **Audit Requirements:** none — mirrors the identical precedent `IRA-006`'s own BA-01 recorded for the structurally identical case (a pure read produces no state change for `SD-002-054`'s seven audit questions to describe).

**No second candidate BA is proposed at this time.** `SD-002-048` (retention floor) and `SD-002-049` (cross-object lineage) are real, LOCKED rules this table's own current schema does not yet fully evidence enforcement of (§8) — but neither requires a *new* Business Activity to satisfy at minimum scope; both are more precisely Technical Debt or future-increment candidates (§14), not blockers to a first read-only BA.

---

## 8. Schema Readiness — Does `evidence_registry` Need Modification? (resolves objective #7)

**(Direct inference from §2's own rule text against §3.2's own physical columns — no assumption.)**

| `SD-002` §6 rule | Physical column present today | Assessment |
|---|---|---|
| SD-002-040 (first-class object) | Own table, own PK | Satisfied structurally |
| SD-002-042 (source class) | `evidence_source` (string, unconstrained) | Satisfied at basic level; no enum/CHECK constraint restricts values — not a blocker for a read-only BA |
| SD-002-043 (granular refs) | `file_reference` (string) | Partial — no explicit page/section/table/cell decomposition column exists on `evidence_registry` itself (contrast: `document_chunk_registry.chunk_locator` explicitly carries "page/section/table/cell reference, per SD-002-043," `Master_Technical_Architecture.md:3250` — that granularity already lives one join away, on the chunk table, not duplicated here) |
| SD-002-044 (reusable across objects) | `linked_entity_type`/`linked_entity_id` (singular pair) + `document_chunk_registry.evidence_id` FK (many-to-one) | Satisfied — reuse already happens structurally (many chunks may cite one evidence row); a read-only BA does not need to add anything to expose this |
| SD-002-045 (independently scored confidence) | `confidence_score` (int, nullable) | Satisfied |
| SD-002-046 (immutable original + additive enrichment) | `document_hash_signature`, `ai_extracted_flag` | Partially evidenced (integrity-hash column exists); no enforcement mechanism (e.g., an update-trigger or application-layer immutability guard) is evidenced — **not** required for a read-only BA either way |
| SD-002-047 (multi-modal formats) | `evidence_type`, `evidence_source` (both unconstrained strings) | Satisfied at basic level |
| SD-002-048 (retention floor) | `retention_policy` (string, nullable, no default, no CHECK) | **Gap** — no physical floor is enforced; disclosed as Technical Debt (§14), not a blocker for a read-only BA |
| SD-002-049 (cross-object lineage) | Not evidenced — no lineage/chain table or column | **Gap** — genuinely unimplemented anywhere in this repository for any object type, not specific to C-066; disclosed as Technical Debt (§14), out of a minimum first BA's own scope |
| SD-002-050 (human-governed) | `externally_verified_flag`, `legal_defensibility_flag` | Partially evidenced (verification-tracking columns exist); no formal approval-workflow beyond flags |

**Conclusion: `evidence_registry` can be reused for the proposed BA-01 (§7) without any architectural modification.** Every gap identified above is either (a) irrelevant to a read-only BA's own scope, or (b) a genuine, pre-existing, repository-wide maturity gap unrelated to and not created by C-066 (mirrors `TD-150`'s own class of finding for BA-05). **No new migration, column, or table is required for BA-01 (proposed).**

---

## 9. API / Service / Enterprise Experience Requirements (resolves objectives #8, partial #5)

**(Proposed scope.)** Two new `GET` endpoints under a new `/evidence` prefix (or equivalent — exact routing is a Technical Design item, not decided here): `GET /evidence/{evidence_id}` (single-item) and `GET /evidence` (filtered list), directly mirroring `IRA-006`'s own delivered BA-01 shape. **No new repository model or migration.** One new repository method (`get_by_id`/`search` or equivalent) and one new schema class (`EvidenceResponse`) — an Extend, not a Create, per `CLAUDE.md §19.5`.

**Enterprise Experience:** **not established** whether a frontend is required for a minimum scope. `CLAUDE.md §20.3` permits a Business Activity to be explicitly chartered backend-only, with the same disclosed-exception discipline BA-05 (WP-14) already used ("BA-05 alone is the disclosed exception" to WP-14's own otherwise-universal Frontend/UX requirement, per `IRA-014 §16`'s own Self-Review). Whether C-066's own first BA should be backend-only or paired with a minimal read-only screen is a **Repository Owner decision required** (§16), not decided here — this assessment does not assume either answer.

---

## 10. Authorization and Tenant-Isolation Requirements (resolves objective #9)

**(Proposed scope + direct precedent citation.)** `evidence_registry.organization_id` is `NOT NULL` (§3.2) — every row is strictly Organization-scoped, unlike `enterprise_knowledge_graph_registry`'s own nullable/Global-permitting design. The already-certified `require_matching_tenant_or_platform_admin` pattern (`WP-10`, reused by BA-05's own optional read-path design per `ADR-023 §5` item 5) is the closest direct precedent for a caller-facing read endpoint against a strictly-tenant-scoped table — proposed as BA-01's own default (§7), not decided here. No `domain_id` column exists on `evidence_registry` (confirmed, §3.2's own full column list) — the `WP-13`/`enforce_domain_permission` mechanism has no attachment point here, the same conclusion already reached for every WP-14 Business Activity (`IRA-014 §10`/§11).

Mandatory Tenant-Isolation Test Checklist (`CLAUDE.md §21.4`) would apply in full to any C-066 BA touching `organization_id`-scoped reads: (a) two distinct, unrelated Organizations seeded, no shared row; (b) a caller in one Organization cannot retrieve another Organization's own Evidence row; (c) an unrelated Organization's `evidence_id` supplied explicitly must be rejected (404, not disclosed), the same probe class `TD-142`'s own BA-01 precedent already exercises.

---

## 11. Testing Strategy (proposed, mirrors `IRA-006`'s own delivered shape)

Unit tests against the new repository method (existence/filtering behavior) and API tests against the two new endpoints (200/404/403/400 paths, tenant-isolation probes per §10). No new test framework, no new fixture pattern — the existing `tests/conftest.py`/`two_orgs` pattern (already reused by every WP-11 through WP-14 Business Activity) applies directly.

---

## 12. Dependencies and Preconditions (resolves objective #11)

None outstanding. `evidence_registry` (pre-existing), `organization_master` (pre-existing, cross-service logical FK, already-established pattern), and `require_matching_tenant_or_platform_admin` (`AuthService/dependencies.py`, pre-existing) are all already real, tested, and certified. No dependency on `WP-13`'s own blocked retrofit scope (no `domain_id` anchor exists on this table, §10). No dependency on `SE-031` (§3.6). No dependency on any currently-open Technical Debt item blocking a read-only BA specifically.

---

## 13. Anticipated Technical Debt (mirrors `IRA-006 §10.2`'s own precedent for disclosing debt at IRA time, not silently deferring it)

If BA-01 (§7) is authorized and implemented substantially as proposed, the following Technical Debt would be anticipated, each mirroring an already-accepted precedent class elsewhere in this repository:

1. **No physical RLS enforcement on `evidence_registry`** (§3.4) — same class as `TD-150` (BA-05), repository-wide, not C-066-specific.
2. **No retention-floor enforcement mechanism** (`SD-002-048`, §8) — `retention_policy` is a free-text column with no CHECK/default tied to the 7-year constitutional floor.
3. **No cross-object lineage mechanism** (`SD-002-049`, §8) — genuinely unimplemented for any object type in this repository, not created or worsened by a minimum C-066 BA.
4. **Interim `PLATFORM_ADMIN`-adjacent authorization gap**, if `require_matching_tenant_or_platform_admin`'s own persona granularity does not fully match `SD-002-050`'s own "human-governed" framing once a richer persona model exists — the same class of gap `TD-090`/`TD-113` etc. already disclose repository-wide.

None of these is `CLAUDE.md §19.8.5`-class (none defeats read-only BA-01's own stated Business Intent, none weakens an existing tenant-isolation boundary — `organization_id NOT NULL` already exists and would be enforced at the application layer exactly as every other WP-11-through-WP-14 read path already does).

---

## 14. Unresolved Repository Owner Decisions (resolves objective #12 — recorded explicitly, not resolved here)

1. **Whether `evidence_registry`'s own hosting-service ambiguity (§3.5 — three conflicting logical-ownership claims: Document Ingestion Service, Retrieval Service, Workflow Service, none physically real) should be formally reconciled** before or independently of C-066's own first BA. This assessment does not require reconciliation to proceed at minimum scope (physical hosting in `AIService` is the status quo, zero migration), but flags it as an open documentation-consistency question.
2. **Whether BA-01 (§7) should be backend-only or should include a minimal Enterprise Experience** (§9) — `CLAUDE.md §20.3`'s disclosed-exception path is available but not self-selecting; this is a scope decision, not an implementation-level one.
3. **Whether `require_matching_tenant_or_platform_admin` (proposed, §10) is the correct authorization pattern**, or whether a narrower/broader persona model is intended for Evidence specifically, given `SD-002-050`'s own human-governance framing may eventually warrant a distinct Evidence-reviewer persona not yet modeled anywhere in this repository.
4. **The `evidence_registry` model docstring's own "C-090's own future domain" framing** (§3.2) for real document-ingestion — whether this should be corrected to reflect C-066 ownership, left as-is, or reconciled some other way. Not corrected by this assessment (read-only investigation).

---

## 15. Business Object Registration

**Not applicable**, mirroring `IRA-006 §11`'s own precedent exactly — no new Canonical Business Object is produced by a minimum C-066 charter. `Evidence`/`evidence_registry` remains owned by its own pre-existing, pre-AMD-012 registration.

---

## 16. Discrepancies Recorded (not silently resolved)

1. `EvidenceRegistryModel`'s own docstring names C-090, not C-066, as `evidence_registry`'s own "future domain" for real document ingestion (§3.2).
2. `Master_Technical_Architecture.md` assigns `evidence_registry` to three different, mutually unreconciled logical services (§3.5), none of which physically exists.
3. Physical RLS for `evidence_registry` is documented (`Master_Technical_Architecture.md:4520–4522`) but not implemented in any migration (§3.4) — same class as `TD-150`, not unique to C-066.
4. No `PE-001-C066` or capability-specific Experience document exists (§3.7) — C-066 is governed by `SD-002` §6 alone, the same posture several already-certified capabilities had before their own first Technical Design.
5. **(Added in remediation of independent-review Finding 1's own cross-reference defect.)** `Master_Technical_Architecture.md`'s own architecture-level schema for `evidence_registry` names two further foreign keys — `node_id -> organization_node` and `uploaded_by -> user_registry` (§3.1) — that are **absent from the actual physical Backend model entirely** (`EvidenceRegistryModel`, §3.2 — not merely unenforced, as with item 3 above, but not present as columns at all). This is a distinct class of gap from item 3's own RLS-not-enforced finding, not the same one; §3.1's own cross-reference has been corrected to point here rather than to §3.4.

None of these five items is treated as resolved by this assessment. None blocks the readiness verdict below (§17), since none touches BA-01's own minimum, read-only, zero-new-schema scope — a read-only BA-01 exposes only columns already physically present, per §8.

---

## 17. Readiness Decision (resolves objective #14)

**C-066 is READY for a minimum-scope Technical Design/chartering process, bounded strictly to BA-01 — Understand Evidence Context (§7), read-only, zero new migration, zero new table, reusing `evidence_registry` exactly as it exists today.** Every dependency this minimum scope needs already exists, correctly, in this repository (§12). The gap this assessment identifies (§3.3: no read/query capability exists anywhere against `evidence_registry`) is genuine, precisely bounded, and does not require inventing any new Business Object, table, or business rule — it requires only the same class of additive extension `IRA-006`/WP-06 already delivered successfully for a structurally identical situation.

**This readiness verdict does NOT extend to:** `SE-031`/`evidence_fusion_registry` (§3.6, a wholly separate, unimplemented future enhancement); any write-path change to `evidence_registry` (§4, remains WP-11/WP-14's own exclusive province); retention-floor enforcement, cross-object lineage, or any other `SD-002` §6 rule beyond what a read-only BA-01 touches (§13); or any Enterprise Experience/frontend component (§9, undecided).

---

## 18. Repository-Owner Authorization to Begin — ACCEPTANCE RECORDED

**IRA Acceptance: GRANTED, 2026-08-24**, per Repository Owner Instruction "C-066 IRA Acceptance → Technical Design Preparation." Per `CLAUDE.md §19.1`'s own no-self-authorization discipline, this acceptance was not self-granted by this document — it was granted by a separate, explicit Repository Owner decision, recorded here, mirroring the `IRA Acceptance: GRANTED, <date>, per Repository Owner Instruction "<name>"` convention this repository already established (`IRA-009`, `IRA-010`).

**What this acceptance grants, precisely:**
- This IRA is accepted **as written**, at its own proposed BA-01 minimum scope (§7) — no expansion or narrowing of that scope was directed.
- Authorization to proceed to the governed Technical Design stage for BA-01 — realized as `TDS-015_C066_BA-01_Understand_Evidence_Context_Technical_Design.md`, which has since been independently reviewed (verdict: PASS WITH CONDITIONS) and remediated against that review's findings.

**What this acceptance does NOT grant — each remains a separate, distinct, not-yet-performed governance step:**
- **WP assignment.** No WP number is assigned by this acceptance. Per `WPR-001` §3's own Maintenance Rule, a WP number becomes assignable once "backed by an accepted IRA" — this acceptance now satisfies that precondition — but assignment itself is a distinct governance act (a `WPR-001`/`WP-REG-001` register update), not automatic upon acceptance, and has not been performed. As of this recording, no WP-15 or any other WP number exists anywhere in `WPR-001` or `WP-REG-001` for C-066.
- **BA-01 chartering/authorization.** BA-01 remains a *candidate* Business Activity (§7). No charter document exists for it (contrast the `WP-14 BA-04` charter precedent). Chartering requires its own separate Repository Owner action.
- **Implementation authorization.** Not granted by this acceptance. `TDS-015` §23 records this explicitly and independently.

**Resolution status of the four unresolved decisions in §14, as of this acceptance:** none was resolved by the acceptance decision itself — the Repository Owner accepted this IRA with all four items still open, exactly as §14 originally disclosed them. `TDS-015` §21 carries these four forward, plus one further item raised by `TDS-015`'s own independent review (the `PLATFORM_ADMIN` list-endpoint question, `TDS-015` §21 item 5) — none of the five is resolved by this acceptance.

**No WP is created by this acceptance. No BA is authorized by this acceptance. No implementation may begin on the basis of this acceptance alone.**

---

*End of IRA-C066. No implementation, migration, model, router, service, API, frontend, or test has been created or authorized by this document. No other governance document (`CAP-001`, `SD-002`, `SER-001`, `WP-REG-001`, `WPR-001`, `Master_Technical_Architecture.md`, the Master Delivery Map) was modified in the preparation of this assessment.*
