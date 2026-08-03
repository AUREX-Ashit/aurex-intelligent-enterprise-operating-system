# WP-11 — Enterprise Search (C-093)

**Document ID:** WP-11 Charter
**Work Package:** WP-11
**Capability:** C-093 — Enterprise Search ("Discover enterprise information," `CAP-001`, Active, D-005)
**Release:** Release C = [WP-11] — Milestone 2, "The Intelligent Enterprise" (`PRODUCT-MILESTONE-ROADMAP.md §3`)
**Prepared By:** Engineering Governance session (Claude Code), under Repository Owner Instruction "Release C Initiation & WP-11 Planning"
**Date:** 2026-08-03
**Status:** CHARTERED — `IRA-011` drafted (see `IRA-011_WP-11_Enterprise_Search_Implementation_Readiness_Assessment.md`), pending Repository Owner acceptance and a separate, future Repository Owner implementation authorization (mirrors WP-10's own two-step chartering→implementation-authorization precedent). **No code, API, or architecture change is authorized by this document.**

**Post-charter correction (`IRA-011`, 2026-08-03):** `IRA-011` independently re-verified this charter's own §0 evidence and found it accurate in every material respect, plus three additional, previously-undisclosed gaps materially affecting scope — `AIService` has zero authentication anywhere (more severe than the `CERT-WP-10`/`VV-AUDIT-WP-09` disclosure class), no Alembic migration chain exists (correcting §9's own incorrect assumption that one does), and `document_chunk_registry`'s `NOT NULL` FK to the wholly-unimplemented `evidence_registry` means this charter's own two Business Activities cannot produce real, queryable content without a third. `IRA-011` resolves this by adding **BA-03 — Register Enterprise Search Content** (narrow, no ingestion pipeline) and, originally, folding the authentication/migration prerequisites into BA-01. See `IRA-011 §4`/§5 for full reasoning; this charter's own §3/§9 below are superseded by `IRA-011`'s own determination, per this charter's own §3 delegation ("Final Business Activity numbering... remain IRA-011's own determination").

**Second correction (`IRA-011 §4.4`, Repository Owner Instruction "Final planning validation before IRA-011 acceptance," 2026-08-03):** the AIService authentication gap is **re-classified as a mandatory platform prerequisite, NOT part of WP-11's own Business Capability scope** — it is not a fourth Business Activity, and it is not folded into BA-01 either. It must be completed and independently verified before BA-01/02/03 implementation begins, but it carries no Business Activity number and does not expand this charter's own §2 Scope (unchanged — see §2's own added confirmation below and §5 Dependencies). The Alembic-chain prerequisite is unaffected by this second correction — it remains genuinely produced as part of BA-01's own first migration, distinct in kind from the authentication prerequisite. See `IRA-011 §4.4`'s own correction for the full evidentiary basis (`CMD-001 §26.3a` Step 1 failure, `WP-00`/`WP-RTA-001` precedent, the defect's own pre-existing and broader-than-WP-11 scope, `TD-106`/`TD-107`'s own Platform ownership).

---

## 0. Capability Selection — Evidence and Reasoning

`SER-001 SE-024` (the umbrella Strategic Enhancement for WP-11) names the choice as **"C-090 Enterprise Discovery or C-093 Enterprise Search"** — deliberately left open, "chosen to prove the charter→IRA pattern for D-005 before broader Enterprise Intelligence work." Per Repository Owner Instruction "Release C Initiation & WP-11 Planning" Objective 2, this charter resolves that choice to **C-093 Enterprise Search**, on the following repository evidence:

1. **Existing, substantial, real code already exists for C-093's own domain.** `Backend/Services/AIService` contains a working `RAGEngine` (`services/rag_engine.py`) that already implements the exact query → embed → search → evidence-cited-assembly pattern C-093 requires, behind two clean abstraction interfaces (`EmbeddingProvider`, `VectorProvider`) and a persisted configuration model (`RAGConfigModel`/`rag_configs`). **No equivalent code exists anywhere in the repository for C-090.** Choosing C-093 is the Reuse-first choice (`CLAUDE.md §19.5`'s Reuse → Configure → Extend → Compose → Create order), not a preference asserted without evidence.
2. **A concrete, already-registered Technical Debt item already assigns this exact work to WP-11.** `TD-109`: "Migrate `AIService`'s own RAG/retrieval code from `rag_configs` onto `vector_index_registry` when WP-11 (first Enterprise Intelligence Work Package) is implemented." This is a standing, pre-existing obligation that only makes sense against C-093's own retrieval domain.
3. **The canonical physical schema is already fully specified and LOCKED**, ready to build against without any architecture change: `Master_Technical_Architecture.md` (AMD-012) defines `vector_index_registry` and `document_chunk_registry`, owned by an explicitly-named "Retrieval Service" component boundary, with RLS policies already specified. No equivalent schema depth exists for a C-090-specific "Enterprise Discovery" data model.
4. **Milestone 2's own Expected Demonstration Scenarios** (`PRODUCT-MILESTONE-ROADMAP.md §3`) — "Ask a natural-language question across enterprise knowledge and receive an evidence-cited answer" — map directly onto Search/Retrieval, which is structurally what `RAGEngine.build_context()` already does today (with fake data).
5. **`SER-001 §5`'s own only two concrete (non-umbrella) D-005 sub-enhancements — `SE-025` and `SE-026` — both target C-092/C-093, never C-090 specifically.** No Strategic Enhancement anywhere names a C-090-specific deliverable.

**C-090 Enterprise Discovery is not selected this cycle — explicitly disclosed, not silently dropped.** `HISTORICAL-SCREEN-REALIZATION-MATRIX.md` items `F1_Enterprise_Understanding_Center.html` (EVOLVE CONCEPT, owning capability C-090, verbatim-linked to already-LOCKED `Complete_Blueprint.md` Q1–Q12 executive-question text) and `I1_Intelligence_Center.html` (EVOLVE CONCEPT, C-090/091/093) both carry real, evidence-grounded Business Intent and Executive Experience value for a **future** C-090 charter — neither concept is retired or lost by this decision; both remain available EVOLVE CONCEPTs for whichever future Work Package eventually charters C-090. F1/I1's own described capability (multi-document synthesis, contradiction detection, confidence-gap routing) is also structurally more demanding of real AI infrastructure than C-093's own minimum-viable query/retrieve/cite loop — consistent with the Roadmap's own explicit framing of WP-11 as "the proving Work Package," the narrower, lower-risk choice is the correct first D-005 charter.

**`C-092 Knowledge Graph Management` is also not chartered as WP-11's own scope**, despite `SER-001 SE-025` listing it as "WP-11 (part of)" — reclassified during this charter's own drafting, per `IRA-011 §4a`'s Strategic Enhancement Review: `SE-024`'s own umbrella text names only "C-090 or C-093," never C-092, as the charter target; a genuine Knowledge Graph *build* requires Neo4j Aura (`Master_Technical_Architecture.md` I.9/7D.13), for which **zero driver, connection code, or configuration exists anywhere in this repository** (`grep -ri "neo4j"` across `Backend/` returns no results) — a hard external-infrastructure gap this Work Package cannot close, distinct in kind from C-093's own gap (an abstraction interface already exists; only its concrete provider is stubbed). See §4 (Out of Scope) and `IRA-011 §6` for the full disclosure.

---

## 1. Purpose / Business Objective

Prove that Enterprise Search — a real, tenant-scoped, evidence-cited retrieval capability — can be resolved and maintained for a specific enterprise, replacing the `AzureSearchStubProvider`'s own hardcoded, query-independent fake results with a real persistence layer and a real orchestration path, per `PRODUCT-MILESTONE-ROADMAP.md §3` Milestone 2's own Business Objective ("Prove AUREX can understand enterprise data, not just administer enterprise structure").

This is also the first Work Package chartered in D-005 (Enterprise Intelligence) — its own success or failure through the full `CLAUDE.md §19.7b` five-gate sequence is the proving ground the Architecture Evolution Implementation Programme's own critical path (`R17 → R23/R24 → Executive Cognition`) depends on before any further D-005 or Executive Cognition capability may be chartered.

---

## 2. Scope

- **Capability:** C-093 Enterprise Search.
- **System of Record:** `Backend/Services/AIService` (existing service — reused, not created; already owns `RAGEngine`, `EmbeddingProvider`, `VectorProvider`, and the non-canonical `rag_configs` this Work Package migrates off of).
- **Canonical schema:** `vector_index_registry`, `document_chunk_registry` (`Master_Technical_Architecture.md` AMD-012, LOCKED) — the "Retrieval Service" component boundary.
- Two candidate Business Activities (§3), spanning the establish/configure half and the execute/query half — the same two-Business-Activity shape `IRA-010`'s own WP-10 precedent used, for the same reason (`SD-002-077`'s metadata-driven object pattern: one governed configuration object, one resolution/execution path against it).
- **Scope confirmation (`IRA-011 §4.4`, second correction, 2026-08-03): unchanged by the AIService authentication finding.** That gap is a platform prerequisite (§5 Dependencies), not a capability addition — C-093's own chartered Business Capability scope remains exactly what this section already states.

---

## 3. Business Activities (candidate — confirmed by `IRA-011`)

- **BA-01 — Establish Enterprise Search Index Configuration.** Writes a real, tenant-scoped `vector_index_registry` row (index name, embedding model, retrieval mode, refresh cadence) — the governed configuration object every search executes against. Resolves `TD-109` by using the canonical table from this Work Package's own first commit, never writing to `rag_configs`.
- **BA-02 — Execute Enterprise Search.** The query path: embeds the caller's own query text, searches the caller's own tenant-scoped `vector_index_registry`-configured index via `document_chunk_registry`, returns evidence-cited results (source, score, locator) — reusing `RAGEngine.build_context()`'s own existing orchestration shape rather than re-implementing it.

Final Business Activity numbering, contracts, and any splitting/merging remain `IRA-011`'s own determination — this charter names the two governed halves, not a locked BA list. **`IRA-011 §4.2`/§5 exercises this delegation and adds a third: BA-03 — Register Enterprise Search Content** (narrow — a caller-supplied text passage only, no ingestion pipeline), required because `document_chunk_registry`'s own `NOT NULL` FK to `evidence_registry` (itself wholly unimplemented anywhere in this repository) leaves BA-02's query path with no way to become genuinely real without it.

---

## 4. Out of Scope

- **C-090 Enterprise Discovery** — not selected this cycle; disclosed in §0, not silently dropped. `F1`/`I1`'s own historical Enterprise/Executive Experience value is preserved for a future charter.
- **C-092 Knowledge Graph Management (Neo4j-backed graph build/traversal)** — zero Neo4j infrastructure exists anywhere in this repository; a hard external-dependency gap. Reclassified out of `SE-024`'s own umbrella scope, per §0.
- **A real (non-stub) `EmbeddingProvider`/`VectorProvider` implementation** — requires external AI/vector-service credentials (Azure AI Search, OpenAI/equivalent embedding API, or similar) this development environment does not have configured anywhere (no such credentials appear in `Config/platform-config.yaml` or any service's own `Config/settings.py`). The **abstraction interfaces, real persistence layer, real tenant scoping, and real orchestration** become genuinely real; the concrete embedding/vector-search **provider** implementation remains an explicitly disclosed, deferred external-integration point — the same class of disclosed gap `TD-111` already established for the Access Evaluation `TierResolver` (the mechanism is registered and real; the resolver behind it is a named, tracked dependency, not silently faked as complete).
- **`SE-027` Multi-Agent orchestration** (`RTA-001 §13.6d/e`) — a large, separate, cross-cutting concern; `RAGEngine`'s own existing design has no agent-delegation dependency, confirming it is not a Search prerequisite. Remains Deferred, `SER-001`-tracked, unaffected by this charter.
- **`SE-028` through `SE-035`** (prompt management, AI policy engine, AI confidence, evidence fusion, AI cost tracking, tool governance, observability build-out, AI audit wiring) — all `Unassigned WP` in `SER-001`, not chartered here.
- **`C-090`/`C-092`/`C-094`/`C-095`** as future capability charters — `C-094`/`C-095` remain explicitly gated behind this Work Package's own successful five-gate closure, per the Architecture Evolution Implementation Programme's own critical path.
- Frontend UI for browsing/searching (a screen consuming this capability) is addressed by `IRA-011`'s own Plan B — not assumed complete by this charter.

---

## 5. Dependencies

- **`TD-109`** (Open, Medium) — this Work Package's own obligation to resolve, not a blocker on chartering it.
- **`R6` (Release A3, soft dependency)** — `CMD-001 §24`'s own Knowledge & AI Domain text does not yet reference the AMD-012/013 registries these capabilities actually use; a documentation-staleness risk, not a proven hard block (`ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md §159`/`205`: "WP-11 could technically be chartered without it... resolving R6 before WP-11's own IRA is drafted avoids that IRA re-discovering the same staleness"). R6 itself requires the formal Locked-document ADR/recertification process (`CMD-001` is LOCKED) — this charter does **not** perform R6; `IRA-011` discloses the residual risk directly rather than silently building against possibly-stale documentation-only text.
- **`R4` (Release A2, hard critical-path dependency) — confirmed CLOSED, per `IRA-011 §1`/§2.** The Implementation Programme's own critical path states "do not start R17 [WP-11] before R3 and R4 have closed." Independently re-verified during `IRA-011` drafting: `R4` (the `llm_prompt_registry`/`reasoning_engine_registry` reconciliation) is resolved — `Master_Technical_Architecture.md`'s own `AMD-015` CHANGELOG confirms `reasoning_engine_registry` as canonical, applied by Repository Owner decision per `IMP-REPORT-RELEASE-A2_Governance.md` (2026-08-01); `R3` closed via Release A1. This charter's own original drafting did not explicitly re-verify this hard dependency (only `R6`, a soft one) — recorded here as a correction, not a new blocker: the critical path is satisfied, not merely assumed.
- **No dependency on `TD-111`** (Access Evaluation `TierResolver`) — C-093 performs no governed authorization-adjacent transition.
- **No dependency on Release A1/A2** — both already closed; no open item from either blocks this charter.
- **AIService Authentication Bootstrap (mandatory platform prerequisite, not C-093 Business Capability scope) — `IRA-011 §4.4`, second correction. STATUS: COMPLETE**, per Repository Owner Instruction "Platform Prerequisites" (2026-08-03). `Backend/Services/AIService` had zero authentication anywhere (§ post-charter correction, above); real JWT claims verification is now implemented (`Backend/Services/AIService/dependencies.py`, 8 passing unit tests, `IRA-011 §14`) and independently verified — BA-01/02/03 may consume it once implementation of those Business Activities is itself separately authorized. This was infrastructure `AIService`'s own pre-existing, non-WP-11 endpoints also lacked — evidenced as platform-owned, not capability-owned, by direct analogy to `WP-00`/`WP-00A` (Platform Bootstrap, no `PE-001` capability) and `WP-RTA-001` (Runtime Work Package, consumed by but not produced within any one Business Capability Work Package), and by `TD-106`/`TD-107`'s own existing "Backend/Shared (Platform)" ownership classification in `TECH-DEBT.md`. Full reasoning and implementation record: `IRA-011 §4.4`/§14.

---

## 6. Enterprise Experience Requirement (`CLAUDE.md §20`/`§21`)

Per `CLAUDE.md §20.3`, WP-11 SHALL deliver both the Business Capability and the Enterprise Experience halves for each Business Activity it charters, unless explicitly designated backend-only — no such designation is made here; `IRA-011 §7` (Plan B) determines the actual frontend scope.

---

## 7. Deliverables / Acceptance Criteria

Determined in full by `IRA-011`'s own Plan A/Plan B — this charter names the governed scope (§3), not the implementation detail.

---

## 8. Risks

- **External-provider unavailability** (§4) — the single largest risk to this Work Package's own "real, not fake" ambition. `IRA-011` SHALL disclose a minimum-scope path that is genuinely real (persistence, tenant-scoping, orchestration) without requiring credentials this environment cannot provide.
- **`R6`'s own documentation-staleness risk** (§5) — mitigated by `IRA-011` reading `Master_Technical_Architecture.md`'s own primary schema text directly, not `CMD-001 §24`'s potentially-stale summary.
- **First-ever D-005 charter** — no prior Work Package in this domain to pattern-match against beyond WP-10's own general two-BA shape; extra care warranted in `IRA-011`'s own Gap Analysis, per the Roadmap's own "not the milestone to compress on schedule pressure" judgment.

---

## 9. Technical Assumptions

- `Backend/Services/AIService` remains the implementing service — no new service is proposed.
- `vector_index_registry`/`document_chunk_registry` are added to `AIService`'s own Alembic migration chain — **corrected by `IRA-011 §3`/§4.5**: no such chain currently exists anywhere in `AIService` (this assumption incorrectly presupposed one); bootstrapping it (mirroring `AuthService`'s own established pattern) is itself in-scope, prerequisite work, not a pre-existing extension point.
- Tenant scoping follows the same `organization_id`-based RLS pattern `Master_Technical_Architecture.md` already specifies for these tables (nullable for platform-wide shared indices, set for tenant-dedicated ones).

---

## 10. Architecture Impact

**None proposed.** Every table this Work Package writes to is already LOCKED, canonical, and fully specified (`Master_Technical_Architecture.md` AMD-012). No new capability, entity, API pattern, or design-system component is proposed. `IRA-011 §6` performs the `CMD-001 §26.3a` Business Object Eligibility determination for any new construct at implementation time, mirroring `WP-10`'s own precedent.

---

## 11. Testing Strategy

Determined by `IRA-011` — mirrors this repository's own established pattern (service-layer + API-layer tests, the Mandatory Tenant-Isolation Test Checklist per `CLAUDE.md §21.4` for both `vector_index_registry` and `document_chunk_registry`, both of which carry an organization/tenant boundary).

---

## 12. Exit Criteria

`IRA-011` accepted; both Business Activities implemented per its own authorized scope; full `CLAUDE.md §19.7b` five-gate closure complete; `SER-001` updated; WP-11 CLOSED — CERTIFIED.

---

## 13. Repository Authority

Chartered per Repository Owner Instruction "Release C Initiation & WP-11 Planning," 2026-08-03. **Implementation is explicitly NOT authorized by this instruction or this charter** — a separate, future "WP-11 Implementation Authorization" instruction is required, mirroring `WP-10`'s own two-step precedent (`IRA-010` accepted under a planning-only instruction; implementation separately authorized afterward).

---

## 14. Governing Documents

`CAP-001` (C-093 registration), `Master_Technical_Architecture.md` (AMD-012, canonical schema), `EIA-001` Volumes I/II (Enterprise Intelligence Architecture — referenced, not independently re-read in full for this charter; `IRA-011` reads the specific sections its own Gap Analysis requires), `SER-001 §5` (`SE-024`/`SE-025`/`SE-026`), `HISTORICAL-SCREEN-REALIZATION-MATRIX.md` (`F1`/`I1`), `ARCHITECTURE-EVOLUTION-STRATEGIC-ROADMAP.md`, `ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md` (`R17`/`R28`), `PRODUCT-MILESTONE-ROADMAP.md §3` (Milestone 2), `TECH-DEBT.md` (`TD-109`), `CLAUDE.md §19`/`§20`/`§21`. No dedicated `PE-001-C093` capability specification exists — confirmed by direct search; `IRA-011`'s own Gap Analysis identifies the governing basis in its absence, mirroring `IRA-010`'s own precedent for `PE-001-C041`.
