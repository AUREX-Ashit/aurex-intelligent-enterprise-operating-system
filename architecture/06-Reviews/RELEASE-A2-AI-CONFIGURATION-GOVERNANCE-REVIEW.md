# Release A2 — AI Configuration Governance Review

**Type:** Focused architectural validation (read-only; no implementation, no architecture, no capability created)
**Scope:** Validates whether Release A2's two remaining governance decisions (R4, R5) are still correct after all architectural evolution completed this programme — not a repository-wide review, not a redesign.
**Inputs used, no new research performed:** `ARCHITECTURE-EVOLUTION-STRATEGIC-ROADMAP.md`, `ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md`, `PRODUCT-MILESTONE-ROADMAP.md`, ARCH-000, RTA-001, PE-001, SD-001, DS-001, IMP-001, CAP-001, CLAUDE.md, plus this session's own prior full read of `architecture/06-Reviews/ENTERPRISE-AI-ARCHITECTURE-AUDIT.md` (the pre-existing, authoritative source for this exact domain, already cited throughout the Strategic Roadmap — reused, not re-derived).

---

## Contents

1. [R4 Review](#1-r4-review)
2. [AI Configuration Architecture](#2-ai-configuration-architecture)
3. [Existing Registries](#3-existing-registries)
4. [Impact Analysis](#4-impact-analysis)
5. [R5 Validation](#5-r5-validation)
6. [Recommendation](#6-recommendation)

---

## 1. R4 Review

**R4 as documented** (Implementation Programme §2): "Reconcile `llm_prompt_registry` vs `reasoning_engine_registry` — Duplicate schema-level concept, neither migrated; a decision, not a build." Classified Release A2 (Architecture Governance): blocked on a Repository Owner decision, no Locked document involved, no ADR required once decided.

**Original evidence source:** `ENTERPRISE-AI-ARCHITECTURE-AUDIT.md` §4 (Architecture Ownership Matrix): *"Prompt/Model configuration mechanism | Master Technical Architecture | **Duplicate** — `llm_prompt_registry` (pre-AMD-012, Azure-OpenAI-specific) and `reasoning_engine_registry` (AMD-013, vendor-neutral) both govern 'which AI configuration answers this request,' with no document stating which supersedes, complements, or is scoped apart from the other."*

**Is this still valid? Yes — independently re-confirmed, not assumed.** Neither registry has been migrated, modified, or reconciled by any work completed during this programme (Release A1 touched ARCH-000, CLAUDE.md, and `TECH-DEBT.md` only — Master Technical Architecture was not touched). The duplicate is exactly as documented, unchanged.

**What R4's original framing left open, and what this pass adds:** R4 as written only says "a decision, not a build" — it does not recommend *which* registry should win. Re-examining the evidence already gathered this session yields a concrete answer:

- `reasoning_engine_registry` (AMD-013) is explicitly vendor-neutral by design — `ENTERPRISE-AI-ARCHITECTURE-AUDIT.md` §5 quotes its own governing rationale verbatim: *"the Enterprise Operating System's engineering architecture shall remain independent of any specific AI vendor, LLM vendor"* — **correction, per Release A2's own independent verification pass:** this quote's actual source is Master Technical Architecture's own AMD-013 Phase 1A "Execution Capability" note, not RTA-001 §13.9b as originally attributed here; RTA-001 §13.9b makes a related but textually distinct vendor-neutrality statement of its own. This matches CLAUDE.md's own stated technology posture and every other AI-runtime decision this repository has made (Agent Framework: "Final as a deliberate non-selection," MCP: deliberate neutrality — both already established, unretracted findings).
- `llm_prompt_registry` (pre-AMD-012) hardcodes `azure_openai_model` as a column — it structurally cannot represent a non-Azure-OpenAI provider without a schema change. It **predates** the vendor-neutral design and was, per the audit's own Technology Decision Register, *"never reconciled with it."*

**Repository evidence therefore supports a specific recommendation, not just "flag for decision":** `reasoning_engine_registry` is the architecturally-aligned survivor; `llm_prompt_registry` should be deprecated or explicitly scoped to a narrower, disclosed legacy purpose. This is a refinement of R4, not a reversal of it — see §6.

---

## 2. AI Configuration Architecture

**Question:** does the platform now require a single canonical AI Configuration Meta-Model spanning Enterprise AI Providers, LLM selection, embedding models, Vector DB selection, Knowledge Retrieval configuration, Prompt management/templates, Reasoning engines, AI runtimes, Tool registry, MCP servers, AI policies, AI governance, AI observability, AI cost controls, Enterprise AI preferences, and Enterprise AI feature flags?

**Answer: No — not supported by repository evidence, and would actively work against this repository's own governing principles.**

DOC-000 §2 states the layering rule this repository already enforces: *"Each layer consumes the layer above it and never redefines it."* ARCH-000's own Architectural Principle 1 (cited at DOC-000 §7): each concern has exactly one owner. The sixteen items above do not all live in one layer today, and evidence shows they *should not*:

| Item | Correct existing layer/owner | Evidence |
|---|---|---|
| Enterprise AI Providers, LLM selection, embedding models — **as an enterprise-facing configuration choice** ("which vendor does *this* enterprise use") | **CMD-001 §12** (Configuration Categories — explicitly includes an "AI Configuration" category: Embedding Model, LLM Selection, Prompt Strategy), resolved through the same Tenant/Enterprise Scope Hierarchy as every other C-041 facet | Already established this session (Implementation Programme §3, R16 mapping) |
| Vector Database selection, Knowledge Retrieval configuration | **Master Technical Architecture** (`vector_index_registry`) + **RTA-001 §13.7** (Context Assembly) | `ENTERPRISE-AI-ARCHITECTURE-AUDIT.md` §2.1/§2.8 — rated Final/Tentative, single-owner, not duplicated |
| Prompt management, Prompt templates | **RTA-001 §13.8** (Prompt Orchestration) governs the principle; Master Technical Architecture owns the physical mechanism — **this is the one genuine duplicate**, R4 | See §1 above |
| Reasoning engines, AI runtimes | **RTA-001 §13** in full (Clean ownership per the audit's own §4 Ownership Matrix) | Unchanged |
| Tool registry | **RTA-001 §13.9a** (Tool Selection) + `ai_tool_registry` (Master Technical Architecture) | Clean; already confirmed this session |
| MCP servers | **Deliberately not owned anywhere** — a considered vendor-neutrality stance (RTA-001 §13.9b names MCP only as a possible future extension seam), not a gap | Already established, unretracted finding |
| AI policies, AI governance | **ARCH-000 §7c** (Ownership Map) | Being incrementally corrected via the ARM-001 precedent and Release A1 — the correct owner, not a candidate for merging elsewhere |
| AI observability | **RTA-001 §17** (Observability Runtime, its own canonical Runtime Law) | A distinct, already-complete architectural home, discovered this session |
| AI cost controls | **RTA-001 §13.14** (telemetry) + `evidence_fusion_registry.cost_incurred_units` | Architecturally defined, correctly scoped to the runtime layer, not implemented yet — not evidence of missing ownership |
| Enterprise AI preferences | **C-042 Preference & Personalization** (CAP-001, Planned) | Already the correct, registered, if-unspecified capability home |
| Enterprise AI feature flags | **The existing `FeatureFlagService`** (`Backend/Services/AuthService`) — YAML-driven, per-organization allowlist, already Fully Implemented | AI-specific flags are additional entries in an *already-built* mechanism, not a reason to build a new one |

**This table itself is the answer to Phase 2's question.** Fourteen of sixteen items already have a single, correctly-scoped, non-duplicated owner spread deliberately across four different architectural layers (Constitutional/CMD-001, Runtime/RTA-001, Engineering/Master Technical Architecture, Governance/ARCH-000) — collapsing them into one model would not fix anything; it would take fourteen concerns that are correctly separated today and force them under one roof, the opposite of "one entity, one definition." Only prompt/model configuration (R4) is a genuine same-layer duplicate requiring reconciliation, and Enterprise AI preferences (C-042) is Planned-but-unspecified, not duplicated or ownerless.

**Precedent already validates this conclusion.** `ENTERPRISE-AI-ARCHITECTURE-AUDIT.md` §2.5 rates `ai_model_registry` (for predictive/forecasting models) as *"a **separate** registry... correctly scoped apart, not a duplicate"* from `reasoning_engine_registry` (for LLMs) — this repository has already, independently, drawn the line between "these two AI-adjacent registries should stay separate" in one case. The same discipline applies here: most of Phase 2's sixteen items are `ai_model_registry`-shaped (correctly separate), not `llm_prompt_registry`/`reasoning_engine_registry`-shaped (genuinely duplicated).

---

## 3. Existing Registries

Every AI-related registry this session has evidence for, with ownership/overlap assessed directly (not invented):

| Registry | Owns | Overlaps with | Missing responsibility | Canonicalize? |
|---|---|---|---|---|
| `llm_prompt_registry` | Prompt storage (pre-AMD-012, Azure-specific) | **`reasoning_engine_registry`** — both answer "which AI configuration serves this request" | N/A | No — deprecate or narrow (§1) |
| `reasoning_engine_registry` | Multi-LLM/model selection (AMD-013, vendor-neutral) | `llm_prompt_registry` (above) | No default model row designated (separate, already-disclosed gap, not an ownership problem) | **Yes** — recommended canonical survivor |
| `ai_tool_registry` / `agent_tool_grant` | Tool registration and per-agent grants | None found | Not yet migrated | Correct as-is; extend, don't merge |
| `agent_registry` | Agent type registration (11 types) | None found | Not yet migrated | Correct as-is |
| `discovery_provider_registry` / `discovery_strategy_registry` | Enterprise Discovery provider/strategy config | None found | Not yet migrated | Correct as-is |
| `evidence_fusion_registry` | Evidence Fusion (7 dimensions), cost/latency telemetry | None found | Not yet migrated | Correct as-is |
| `confidence_scoring_registry` | Confidence scoring; reused as the `governing_policy_id` target for AI policy/agent governance | None found — a deliberate reuse, not a duplicate (already noted in ARCH-000 §7c's own "AI policy boundaries" row) | Not yet migrated | Correct as-is |
| `vector_index_registry` | Vector DB/embedding index configuration, retrieval mode | **`rag_configs`** (below) — new finding, this pass | Embedding *model* not named at the architecture layer (pre-existing, disclosed gap) | **Yes** — recommended canonical survivor over `rag_configs` |
| `rag_configs` (`AIService/models/rag.py`, `RAGConfigModel`) | Chunk size/overlap/semantic-search-enabled, keyed by `tenant_id` | **`vector_index_registry`** — both configure retrieval/indexing behavior | N/A | **New finding this pass:** a second, smaller-scale duplicate of the same shape as R4 — `rag_configs` lives on the non-canonical `tenant_id` model (already flagged elsewhere this session as a duplicate of canonical `Organization`), is unmigrated, and overlaps `vector_index_registry`'s own territory. Not part of R4's original scope; recommend tracking as a related, separately-scoped follow-on (§6) |
| `ai_model_registry` | Predictive/forecasting models (risk, financial, anomaly) | None — audit already confirmed this is correctly separate from `reasoning_engine_registry` | N/A | Correct as-is; cited above as the precedent for *not* over-merging |

**No registry should become "canonical" in the sense of absorbing the others.** The evidence supports exactly two narrow reconciliations (`llm_prompt_registry`→`reasoning_engine_registry`, and the newly-surfaced `rag_configs`→`vector_index_registry`), not a single canonical AI registry. Extending existing architecture (migrating the surviving registries, deprecating the losing ones) is sufficient — nothing here requires inventing new architecture.

---

## 4. Impact Analysis

| Future work | Impact |
|---|---|
| **Release B / WP-09** (Workspace Management) | None — does not touch AI configuration. |
| **Release B / WP-10** (Configuration Management, includes AI Configuration facet) | **Clarifying, not blocking.** WP-10's own AI Configuration facet (already mapped to CMD-001 §12 in the Implementation Programme) should resolve to `reasoning_engine_registry`-shaped settings once R4 is decided — this sharpens what WP-10 will build against; it does not change WP-10's scope or delay its charter. |
| **WP-11** (first Enterprise Intelligence Work Package) | **Directly benefits.** R4 already sits on the Implementation Programme's own hard critical path to WP-11 (§8: "R17 depends on R3 and R4"). This review's concrete recommendation (§6) removes the remaining ambiguity, rather than leaving WP-11's own future IRA to re-litigate the same open question. |
| **Enterprise Intelligence (D-005 generally)** | Same as WP-11 — no structural change, faster path to the same already-planned destination. |
| **Executive Cognition (C-094/C-095)** | Indirect only — gated behind WP-11 regardless (Implementation Programme §8); this review does not change that gate. |
| **Enterprise Configuration (C-041)** | WP-10's AI Configuration facet clarified, as above. |
| **Enterprise Administration** | No impact — outside this review's scope entirely. |

**No release, Work Package, or capability boundary changes as a result of this review.** This confirms Phase 4's own question directly: the AI Configuration architecture has *not* evolved in a way that restructures future work — it has evolved (via this session's own accumulated research) to the point where R4's open decision can be answered with evidence instead of left blank.

---

## 5. R5 Validation

**R5:** canonical platform-identity naming — "Enterprise Operating System" (ARCH-000, CLAUDE.md, RTA-001) vs. "Intelligent Enterprise Operating Center" (Complete_Blueprint, exclusively).

**Should this now be finalized?** No new evidence from Phases 1–4 bears on this question at all — R4 is a technical schema duplicate; R5 is a branding/platform-identity naming choice. They are unrelated concerns that happen to share a release wave for process reasons (both are Release A2: decision-blocked, no Locked document), not for substantive reasons. Re-confirming rather than assuming: neither name is technically "more correct" — both are used extensively, deliberately, and non-accidentally in their respective documents (ARCH-000 §2 is literally titled "Enterprise Operating System Philosophy"; Complete_Blueprint's own Platform Identity section uses "Intelligent Enterprise Operating Center" six times, exclusively). This is not evidence one term is stale or superseded — it is evidence of two documents making an independent, deliberate, unreconciled choice.

**Recommendation: remains deferred, unchanged from the prior finding.** This is a pure Repository Owner naming decision — no repository evidence resolves it, and no amount of further architectural research would; it is not the kind of question evidence answers. Finalizing it now, absent a Repository Owner decision, would be inventing a resolution rather than validating one, which this exercise's own instructions explicitly prohibit ("Do NOT assume the answer").

---

## 6. Recommendation

**Option 2 — Refine Release A2 before implementation.**

Not Option 1 (proceed exactly as planned): R4's original framing ("a decision, not a build," no recommended direction) is less useful than it could be — this review adds a concrete, evidence-based direction (`reasoning_engine_registry` canonical) that R4 alone did not provide, and surfaces one adjacent finding (`rag_configs` vs `vector_index_registry`) that R4's original scope never covered at all.

Not Option 3 (replace R4 with a canonical AI Configuration Meta-Model decision): directly contradicted by evidence — §2's table shows fourteen of sixteen candidate concerns already have single, correctly-separated owners across this repository's own deliberate layering; a meta-model would violate CLAUDE.md's own "one entity, one definition" principle and DOC-000's own layering rule, not fulfill it. This would be inventing unnecessary architecture, which Phase 3's own instruction explicitly warns against.

**Refinement, concretely:**

1. **R4 (Release A2) is refined, not replaced:** recommend `reasoning_engine_registry` as the canonical prompt/model configuration mechanism; recommend `llm_prompt_registry` be deprecated or explicitly narrowed to a disclosed legacy purpose. This is still a Repository Owner decision to confirm (the evidence supports a direction, it does not self-execute), but it is no longer an open-ended one.
2. **A new, related item is disclosed, not silently added to R4's scope:** `rag_configs` (AIService) vs. `vector_index_registry` (Master Technical Architecture) is a second, smaller duplicate of the same shape, discovered during this validation pass. Recommend tracking it as its own Technical Debt entry and a candidate for a future, separately-scoped reconciliation — bundling it into R4 now would quietly expand Release A2's own approved scope, which this exercise's own instructions prohibit ("Do NOT modify implementation... Do NOT implement Release A2").
3. **R5 is validated and reaffirmed unchanged:** remains a pure Repository Owner naming decision, appropriately deferred, not resolvable by further evidence.

No architecture was modified. No capability was created. No implementation occurred. Release A2 itself has not begun.

---

*Focused architectural validation · no repository files were modified other than this report · no implementation, architecture, or capability change occurred · Aurex Enterprise Operating System*
