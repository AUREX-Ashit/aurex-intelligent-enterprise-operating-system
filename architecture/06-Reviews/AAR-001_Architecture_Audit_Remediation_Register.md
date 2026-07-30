# AAR-001 — Architecture Audit Remediation Register (Regenerated)

**Type:** Architecture Remediation Planning (roadmap only — no architecture document modified, no ADR created, no implementation performed)
**Trigger:** `architecture/06-Reviews/ENTERPRISE-AI-ARCHITECTURE-AUDIT.md`, Final Assessment: **OPTION B — Minor architectural gaps identified**
**Prior version:** The original `AAR-001` was independently reviewed and **REJECTED** — the review found the findings register incomplete (a phantom finding ID required by its own arithmetic but never defined; two findings referenced but never written up; roughly a dozen audit-flagged capability gaps omitted entirely), an unexamined ADR-trigger risk in one remediation, an ungated Beta-stage safety risk, and an unverified blanket "no Architecture Refactoring" claim. **This document is a full regeneration from first principles, not a patch.** The prior version is superseded in its entirety; see §10 Revision History for the complete list of corrections.
**Version 2 correction pass:** Version 2 (the regeneration above) was then put through a Final Certification Review, which found three further, narrower defects: one audit-flagged row (Parsing) still uncaptured; an inaccurate ADR rationale for AF-008/AR-011 (claiming no Pending Canonical Binding covers any part of the Memory finding, when the audit's own §6.3 records one for its lifecycle-rule component); and a headline "three findings need an ADR determination" count that contradicted AR-016's own treatment of AF-019/AF-020 as unresolved. This document incorporates the targeted corrections for exactly those three defects — see §10 Revision History for the itemized list. No other section was rewritten.
**Status of the audited architecture:** Accepted. This register does not reopen, question, or redesign the Enterprise Architecture — every finding below is treated as a closable gap within the accepted architecture, not a defect in it.
**Scope of this document:** Planning only. No architecture document has been modified, no ADR has been created, and no remediation has begun as a result of producing this register.

---

## Executive Summary

This register re-extracts every audit finding directly from `ENTERPRISE-AI-ARCHITECTURE-AUDIT.md` — every non-clean row across its Capability Coverage Matrix (§2.1–2.10), every flagged row in its Ownership Matrix (§4), every callout in its Gap Analysis (§6.1–6.8), and every item in its Enterprise Readiness checklist (§7) — rather than starting from, or trusting, the previously rejected register. The result is **37 findings (AF-001 through AF-037)**: 8 HIGH, 18 MEDIUM, 9 LOW, 1 Acknowledged (a deliberate, permanent architectural boundary — not a gap), and 1 Encompassing (the fact that Enterprise Intelligence has no working code yet — the object all other findings exist to prepare for, not a discrete remediation target itself). **8 + 18 + 9 + 1 + 1 = 37.**

These 37 findings are closed by **21 remediations (AR-001 through AR-021)**, each explicitly listing every finding it closes; every finding explicitly lists the single remediation that closes it. No finding is closed by more than one remediation and no finding is left unclosed (AF-035, the Acknowledged item, is explicitly marked as closed by no remediation — by design, not by omission).

Unlike the prior version, this register does **not** assert a blanket "no ADR required." Five findings carry an open or conditional ADR determination that architecture governance must explicitly resolve, not this register: AF-008 (Memory sub-type differentiation only — its lifecycle-rule component is separately covered by an existing Pending Canonical Binding, see below), AF-014, and AF-015 require substantive new content in documents the audit itself identifies as **LOCKED** (RTA-001) or **Frozen v1.0** (EIA-001) without an existing placeholder covering them, and are marked **ADR Required**; AF-019 and AF-020 are marked **ADR Conditional**, since whether they need new RTA-001 content or only additive schema has not yet been scoped. None of the five is silently waved through. One further finding (AF-001) has a governance-ownership resolution path that is conditional on an ADR depending on which of two options is chosen, and this is stated explicitly rather than left ambiguous.

**Final Recommendation: OPTION A — Architecture ready after remediation roadmap approval**, with five findings (AF-008's sub-type-differentiation component, AF-014, AF-015, AF-019, AF-020) explicitly flagged for an architecture-governance ADR determination before their remediations (AR-011, AR-014, AR-015, AR-016) proceed past design. See §9.

---

## 1. Task 1 — Master Finding List: Re-Extraction Methodology and Verification

Every table row and every named gap across `ENTERPRISE-AI-ARCHITECTURE-AUDIT.md`'s §2 (Capability Coverage Matrix, subsections 2.1–2.10), §3 (Technology Inventory), §4 (Ownership Matrix), §5 (Technology Decision Register), §6 (Gap Analysis, 6.1–6.8), and §7 (Enterprise Readiness checklist, 17 items) was walked individually. Rows marked cleanly `Y | ... | Y | Final` with no caveat text carry no finding. Every row with a caveat — `Partial`, `Tentative`, `Missing`, `Conflicting`, `Deferred`, or any qualifying prose — was extracted as a candidate finding, then merged with any other row describing the same underlying gap (e.g., the audit's own §7 item 4 groups "Ranking" and "Re-ranking" as one decision point; this register follows that grouping rather than inventing separate findings for what the audit itself treats as one).

**Verification performed:**
- **No findings omitted:** every Tentative/Partial/Missing/Conflicting row across all ten §2 subsections is accounted for below, including the twelve items the prior register's independent review specifically identified as omitted (Tool Discovery, Agent Communication, Agent Lifecycle, Agent State, Agent Governance, Cost Optimization, Fallback Strategy, Prompt Routing, Structured Output, Event Store, Source System Mapping, Semantic Layer), the Taxonomy three-way term overlap, and — added in the Final Certification Review correction pass — the §2.8 Parsing row (AF-037), which was still missing from the prior draft of this document.
- **No duplicate findings:** rows describing the identical underlying gap under a different capability name (e.g., "Discovery" and "Enterprise Discovery"; "Cache" and "Redis"; "Object Storage" and "Blob Storage") are captured once, not twice. Every merge is stated explicitly in the finding's Description.
- **No missing IDs / sequential numbering:** AF-001 through AF-037, no gaps, no ID defined without content, no ID implied by arithmetic without being written up. §2 below is the complete register — every ID in this range has a full entry; no ID beyond AF-037 is referenced anywhere in this document.
- **Arithmetic consistency:** 8 HIGH + 18 MEDIUM + 9 LOW + 1 Acknowledged + 1 Encompassing = 37. This sum is restated in §2's section headers and reconciled again in §7 (Internal Quality Audit).

---

## 2. Findings Register

### 2.1 HIGH Severity (8)

| ID | Description | Root Cause | Documents Affected | Architectural Owner | Recommended Resolution | Validation Method | Estimated Effort | Dependencies | Status | Resolved By |
|---|---|---|---|---|---|---|---|---|---|---|
| **AF-001** | ARCH-000 §7c's AI Governance Ownership Map states Prompt Governance, Knowledge Governance, Memory Governance, and Model Governance are "Deferred... no placeholder owner assigned." RTA-001 §13.15 (LOCKED, added under AMD-012/013) asserts the AI Runtime "shall support... Prompt Governance, Model Governance" as an already-owned guarantee. Two constitutional-tier documents directly contradict each other on ownership. | RTA-001 §13.15 was added by amendment without a corresponding cross-check against ARCH-000 §7c's earlier, still-standing table. | ARCH-000 §7c; RTA-001 §13.15 | ARCH-000 (top-level governance authority) | **Recommended path (no ADR):** update ARCH-000 §7c to assign ownership matching what RTA-001 §13.15 already operationally claims, since RTA-001 already implements the guarantees. **Alternative path (ADR required):** scope down RTA-001 §13.15's claim to match ARCH-000's deferral — this modifies a LOCKED document's substantive content and would require an ADR under the repository's own amendment-control rule for Locked documents. This register recommends the first path and does not endorse the second without an ADR. | Re-read ARCH-000 §7c and RTA-001 §13.15 side by side; confirm no contradiction remains; confirm GRC-001-075, PLT-001-036, OPM-001-084, COM-001-065, ONT-001-052 (all of which already defer to ARCH-000 §7c) still resolve correctly. | Small | None (recommended alongside AF-006) | Open | AR-001 |
| **AF-002** | `llm_prompt_registry` (pre-AMD-012, Azure-OpenAI-specific: `azure_openai_model`, `azure_region`, `temperature`, `max_tokens`) and `reasoning_engine_registry` (AMD-013, vendor-neutral: `engine_name`, `engine_vendor`, `engine_category`, input/output contract schemas) both govern "which AI configuration answers a given request." No document states whether `llm_prompt_registry` is superseded, deprecated, or scoped to a distinct code path. | `reasoning_engine_registry` was introduced by AMD-013 as a generalization; `llm_prompt_registry` was never revisited or formally rescoped at that time. | Master Technical Architecture | Master Technical Architecture | Record an explicit decision: state whether `reasoning_engine_registry` supersedes `llm_prompt_registry` for all agentic paths, whether `llm_prompt_registry` remains scoped to a distinct non-agentic direct-prompt path, or whether the two are formally merged in a later engineering pass. | Confirm a single, unambiguous statement identifies which registry governs which code path, with no remaining "or" ambiguity. | Medium | None | Open | AR-002 |
| **AF-003** | The vendor-neutral `reasoning_engine_registry` mechanism is architecturally complete (GPT, Claude, Gemini, DeepSeek, open-weight, and enterprise-fine-tuned models are named as peer configuration rows), but no default row is designated anywhere. A fresh build has no way to know which model to configure first. | The registry was designed to be vendor-neutral by principle; no work package has yet needed to fix a default, so none was recorded. | Master Technical Architecture (`reasoning_engine_registry`) | Master Technical Architecture | Once AF-002 is resolved, designate one `reasoning_engine_registry` row as the platform default. | Confirm exactly one row is flagged default; confirm consistency with AF-002's reconciliation. | Small | AF-002 | Open | AR-003 |
| **AF-004** | No embedding model is named at the architecture layer. `text-embedding-3-large` exists only in application config/code (`Backend/Services/AIService/Config/settings.py`, `platform-config.yaml`), never promoted into architecture. | Embedding model selection was made at the engineering/config layer during WP-00/AIService bootstrap and never round-tripped into architecture documentation. | Master Technical Architecture (`vector_index_registry.embedding_model`) | Master Technical Architecture | Add the actual embedding model in use as a named architectural decision, cross-referenced from the application config it already lives in. | Confirm a named value is present in `vector_index_registry`'s documentation and matches the running code's value. | Small | None | Open | AR-004 |
| **AF-005** | Event Bus is an architected runtime component since RTA-001 §1.4, but no message-broker product (Kafka, Azure Service Bus, RabbitMQ) is named anywhere. A Kafka topic exists only in `docker-compose.yml`, previously flagged (IRA-001 WP-01) as unused/dead. Separately, event-sourcing is owned as a *principle* by SD-002-052, but no distinct "Event Store" product or table is named as the canonical event-sourcing store — events appear to persist as domain event rows across several registries, not one dedicated store. | Event Bus was named as an architectural role from RTA-001's earliest drafting; no work package has yet required selecting the underlying product or consolidating the event-sourcing storage model. | RTA-001 §1.4, §2.5, §2.8; Master Technical Architecture (I.13 frozen stack); SD-002-052; `workflow_event_log` | Master Technical Architecture | Select a message-broker product (confirm or replace the dormant Kafka reference) and record it in Master Technical Architecture's I.13 frozen stack list; clarify whether `workflow_event_log` (or an equivalent) is the canonical Event Store, or whether a dedicated one is needed. | Confirm a named product appears in I.13; confirm one document states which table is the canonical event-sourcing store. | Medium | None | Open | AR-005 |
| **AF-006** | CMD-001 §24 (Knowledge & AI Domain), ARCH-000, and EIS-001 have not been updated since AMD-012/AMD-013 introduced `agent_registry`, `discovery_provider_registry`, `reasoning_engine_registry`, `evidence_fusion_registry`, `discovery_strategy_registry`, `enterprise_knowledge_object_registry`, and `document_chunk_registry`. CMD-001 §24.5's illustrative tables (`recommendation`, `recommendation_context`...) match no real table. ARCH-000 cites no AMD-012/013 version reference. EIS-001 still lists the Knowledge Graph's storage technology as a Pending Canonical Binding that AMD-012 already resolved (Neo4j Aura). | Documentation maintenance did not keep pace with AMD-012/AMD-013's schema additions — the same class of drift WP-01 encountered with `PE-001-C004` before its own Scope Reconciliation. | CMD-001 §24; ARCH-000; EIS-001 | CMD-001 (data-shape) / ARCH-000 (manifest currency) — joint | Update CMD-001 §24's Aggregate Root/Business Object tables to reference the actual AMD-012/013 registries; update ARCH-000 to cite AMD-012/AMD-013 and current document version numbers; update EIS-001 to remove Pending Canonical Bindings already resolved by AMD-012. | Confirm CMD-001 §24.3/§24.5 match real Master Technical Architecture tables; confirm ARCH-000 cites current amendment numbers; confirm EIS-001's Appendix B no longer lists the Knowledge Graph storage-technology binding as pending. | Small–Medium | None (foundational — recommended first) | Open | AR-006 |
| **AF-011** | No PE-001-C090 through PE-001-C095 Experience Blueprint exists for Discovery, Knowledge, Search, Conversation, or Memory — unlike every other active/planned capability domain in the platform (C-001 through C-024/C-040). | No work package has yet been chartered to author Enterprise Intelligence's PE-001 blueprints, unlike WP-01, which eventually produced `PE-001-C004` (after initially proceeding without it, at real cost — see `WP-01A_Canonical_Coverage_Resolution.md`). | (New documents to be created: PE-001-C090 through PE-001-C095) | PE-001 (new capability blueprints, once authored) | Commission and author PE-001-C090 through PE-001-C095, following the same discipline `PE-001-C004` v1.1 was held to, **before** substantive Business Activity engineering for D-005 begins — the exact lesson WP-01 already paid for once. | Five PE-001-C09x documents exist, each passing the same Gold Standard validation criteria as `PE-001-C004` v1.1. | Very Large | None | Open | AR-007 |
| **AF-015** | Hallucination Controls and Safety Controls do not exist as defined mechanisms anywhere in the corpus. RTA-001 §13.6 names "Safety Validation" as an AI Request Lifecycle stage but never elaborates what it checks or how a hallucination is detected. | Safety/hallucination detection is a substantive engineering-design question no work package has yet been scoped to answer; the stage was named as a placeholder when the AI Request Lifecycle was first drafted. | RTA-001 §13.6 | RTA-001 (once elaborated) | Define concrete safety/hallucination checks for the "Safety Validation" stage. **A baseline definition is required before any external-user-facing Beta**, not only before Production — an undefined safety stage is a live risk the moment real users interact with AI-backed features, not only at full production scale. | "Safety Validation" is no longer a name-only stage; concrete, testable checks are specified and can be demonstrated against representative inputs. | Large | AF-003 | Open | AR-015 |

*(HIGH severity subtotal: 8 — AF-001, AF-002, AF-003, AF-004, AF-005, AF-006, AF-011, AF-015)*

### 2.2 MEDIUM Severity (18)

| ID | Description | Root Cause | Documents Affected | Architectural Owner | Recommended Resolution | Validation Method | Estimated Effort | Dependencies | Status | Resolved By |
|---|---|---|---|---|---|---|---|---|---|---|
| **AF-007** | No search ranking or reranking mechanism is specified. EIA-001 Vol. II §20.4 and EIS-001 §10.11 both record this explicitly as an unresolved **Pending Canonical Binding**. `RAGService`'s strategy-object extension point exists; no algorithm does. (Merges the audit's Semantic Search, Hybrid Search, Ranking, and Re-ranking rows — grouped identically in the audit's own §7 item 4.) | Ranking/reranking is a genuine engineering-design decision no work package has yet been scoped to make; EIA-001 itself flags it as pending, not silently omitted. | EIA-001 Vol. II §20.4; EIS-001 §10.11; IMP-001 §13.3 | EIA-001 (business rule, already flagged pending) / future engineering (algorithm) | Define a concrete ranking/reranking algorithm or model once Enterprise Search Business Activities are engineered, fulfilling EIA-001/EIS-001's existing Pending Canonical Binding placeholders. **No ADR required** — EIA-001's own "Pending Canonical Binding" convention is the repository's established mechanism for extending a Frozen document without amending it. | Both Pending Canonical Binding flags (EIA-001 §20.4, EIS-001 §10.11) are closed with a named mechanism. | Large | AF-011 | Open | AR-010 |
| **AF-008** | Enterprise Memory is a single undifferentiated concept — Conversation/Episodic/Semantic/Working/Long-term memory distinctions do not exist as separate models. Memory Qualification/Relevance/Retention/Reassessment mechanisms are conceptual attributes, not computable rules (audit §7 item 6). | Memory was specified at the level of one canonical concept (EIA-001 Vol. II Ch. 26–28). This finding has two components with different provenance in the audit, corrected here (Final Certification Review defect): **(1)** the five-way sub-type differentiation itself (Conversation/Episodic/Semantic/Working/Long-term) is recorded in audit §6.1 as a **Missing architectural capability** with **no** Pending Canonical Binding covering it — the same uncovered-gap class as Context Compression (AF-014) and Hallucination Controls (AF-015). **(2)** The Qualification/Relevance/Retention/Reassessment *computable rules*, by contrast, are explicitly recorded in audit §6.3 as an existing **Pending Canonical Binding** in both EIA-001 Vol. II and EIS-001 Appendix B — the same already-authorized class as Ranking (AF-007) and Reauthorization (AF-009). The previous draft of this finding incorrectly claimed neither component had a Pending Canonical Binding; only component (1) is genuinely uncovered. | EIA-001 Vol. II Ch. 26–28 (Frozen v1.0); RTA-001 §21; Master Technical Architecture (`enterprise_memory_registry`, `memory_evidence_registry`) | EIA-001 / RTA-001 (jointly) | Design the five memory sub-types and computable lifecycle rules, informed by the PE-001-C095 blueprint (AF-011). **For the Qualification/Relevance/Retention/Reassessment rules (component 2): No ADR** — this portion fulfills an existing Pending Canonical Binding (audit §6.3), the same already-sanctioned mechanism Ranking (AR-010) and Reauthorization (AR-012) rely on; it needs engineering resolution, not governance escalation. **For the five-way sub-type differentiation itself (component 1): ADR Required: To Be Determined by Architecture Governance** — this portion is a §6.1 Missing capability with no existing placeholder; adding five distinct memory types is substantive new constitutional content to EIA-001 (Frozen v1.0), and the schema work this implies for `enterprise_memory_registry` (new entities/columns) would separately trigger CLAUDE.md §18/§19.4's architectural-impact escalation. This register does not assume the answer is "no ADR" for component 1 — it explicitly defers that determination to architecture governance before AR-011's sub-type-differentiation design proceeds past scoping. | Five distinct memory sub-types (or an explicit, reasoned governance decision to keep one unified model) are named with computable rules; the component-2 Pending Canonical Binding (audit §6.3) is closed via engineering resolution, consistent with Ranking/Reauthorization; the component-1 ADR-required determination is resolved one way or the other before implementation begins. | Large | AF-011; governance ADR determination (component 1 only) | Open | AR-011 |
| **AF-009** | No mechanism defines what happens when a requester's authority changes mid-Conversation (C-094). The rule ("must remain bounded by current authority") is fixed; the mechanism is not. | Authority-boundedness is stated as a business rule without an accompanying enforcement-mechanism design — a normal rule-before-mechanism sequencing gap. | SD-003; RTA-001 §13.12; the future C-094 Business Activity Contract | SD-003 (rule) / RTA-001 (mechanism, to be added) | Design a reauthorization check as part of the C-094 Business Activity Contract. No ADR anticipated — this is an additive Business Activity Contract clause, not a change to SD-003 or RTA-001's existing rule text. | A named, testable mechanism exists and is referenced from SD-003 and the C-094 BAC. | Medium | AF-011 | Open | AR-012 |
| **AF-010** | The schema (`confidence_scoring_registry`, 0–100 scale, 5 colour bands, 3 propagation rules) and the rule that confidence must exist are fixed. The formula computing a Knowledge Asset's actual confidence score is not defined. | Same pattern as AF-009: rule and shape fixed, computation left to a future engineering pass. | Master Technical Architecture (`confidence_scoring_registry`); EIA-001 Vol. II Ch. 12 | Master Technical Architecture (schema) / future engineering (formula) | Define the confidence-scoring formula as part of Knowledge (C-091/C-092) Business Activity engineering. No ADR anticipated — additive formula definition within an existing, already-approved schema. | A named formula exists and is cross-referenced from the registry definition. | Medium | AF-011 | Open | AR-013 |
| **AF-012** | D-005 (Enterprise Intelligence) is not registered as a URA-001 Domain; EIS-001 §7.7/§8.7 explicitly flag this as unconfirmed. | Domain registration is a lightweight governance step that has not yet been formally executed for D-005. | EIS-001 §7.7/§8.7; URA-001 | URA-001 | Register D-005 as a URA-001 Domain. No ADR — mechanical registry action; URA-001 is not designated Frozen/Locked in the audit. | D-005 appears in URA-001's Domain registry. | Small | None (CAP-001's existing C-090–C-095 capability identity is sufficient; does not require AF-011 first — see §5 Dependency Review for correction from the prior version) | Open | AR-008 |
| **AF-013** | 18 proposed Business Activity identifiers and 8 proposed EIO identifiers (EIS-001) are provisional, not yet formally allocated through IMP-001's Business Activity Registry. | Identifier allocation is a mechanical governance step that has not yet been executed for D-005. | EIS-001; IMP-001 (Business Activity Registry) | IMP-001 Business Activity Registry | Formally allocate the 18 BA + 8 EIO identifiers. No ADR — mechanical registry action. | All 26 identifiers appear in the registry as non-provisional. | Medium | None (mechanical registry action against EIS-001's existing proposed list; does not require AF-011 first) | Open | AR-009 |
| **AF-014** | Context Compression and Context Window Management do not exist anywhere in the corpus as defined mechanisms — marked "Missing," not "Pending Canonical Binding," in the audit. | No document ever named this as a capability requiring resolution; it is a wholly new addition, not a flagged-but-unresolved existing one. | RTA-001 §13.7 (Context Assembly) | RTA-001 (once elaborated) | Define a compression/windowing strategy for large Enterprise Context payloads, informed by the model selected in AF-003 and embedding choice in AF-004. **ADR Required: Likely Yes** — this is new substantive content to RTA-001 §13.7, a LOCKED section, with no existing Pending Canonical Binding placeholder covering it (unlike AF-007). | A named compression/windowing strategy is documented and cross-referenced from Context Assembly; the ADR requirement is confirmed and, if affirmed, executed before implementation. | Large | AF-003, AF-004 | Open | AR-014 |
| **AF-016** | Explainability is touched by SD-002-016, SD-001 LAW-26, and RTA-001 §13.15, with no single document cited by the others as sole owner, and it is absent from ARCH-000 §7c's own Ownership Map table despite being treated as an AI-specific guarantee elsewhere. | Explainability was defined incrementally across three documents at different times, with no governance pass ever consolidating ownership. | SD-002-016; SD-001 LAW-26; RTA-001 §13.15; ARCH-000 §7c | ARCH-000 §7c (once corrected) | Add Explainability to ARCH-000 §7c's table in the same governance pass as AF-001, citing SD-002-016/SD-001 LAW-26 as the substantive sources it defers to. No ADR — ARCH-000 table update only. | ARCH-000 §7c's table includes an Explainability row with a named owner. | Small | AF-001 (same governance pass) | Open | AR-001 |
| **AF-017** | Tool Selection is architected (RTA-001 §13.9a: "select it from the AI Tool Registry"), but a distinct *discovery* mechanism (e.g., dynamic tool advertisement, MCP-style discovery) is not — the registry is static/configured, never discovered at runtime. | Tool Discovery was never distinguished from Tool Selection when RTA-001 §13.9a was drafted; the registry-based model covers static configuration only. | Implicit in RTA-001 §13.9a | RTA-001 (if elaborated) / future engineering | Design a dynamic tool-discovery mechanism as an engineering-layer addition (e.g., an `ai_tool_registry` query-time capability), if warranted once real tool integrations are built. No ADR anticipated — this can be scoped as an additive engineering pattern (IMP-001 layer) rather than new RTA-001 substance, since static Tool Selection already fully covers today's need. | A named discovery mechanism exists, or an explicit decision that static configuration remains sufficient is recorded. | Medium | AF-011 | Open | AR-017 |
| **AF-018** | Agent Communication (RTA-001 §13.6e, Capability Delegation) has authorization/delegation architected (`agent_tool_grant`), but no message format, protocol, or inter-agent communication contract beyond the Reasoning Contract's input/output schema is specified. | Delegation-as-authorization was specified; delegation-as-message-protocol was not distinguished as a separate concern. | Implicit in RTA-001 §13.6e | RTA-001 (if elaborated) / future engineering | Design an inter-agent message contract as an IMP-001-layer Business Activity Contract addition — does not require amending RTA-001's existing Capability Delegation mechanism, which stays intact. No ADR anticipated. | A named message format/protocol exists, distinguishable from the Reasoning Contract's own I/O schema. | Medium | AF-011 | Open | AR-016 |
| **AF-019** | `agent_registry.active_flag` and RTA-001 §22's request lifecycle govern a *request's* lifecycle, not an agent *instance's* — no agent instantiation/teardown/versioning lifecycle is described. | Agent Lifecycle was conflated with Request Lifecycle when the registry and state machine were designed; no work package has separated the two. | `agent_registry`; RTA-001 §22 | Master Technical Architecture / RTA-001 | Design an agent-instance lifecycle model. **ADR Conditional** — if this requires only additive `agent_registry` schema (new columns for instantiation/versioning state), no ADR is needed (same class as AF-002–005); if it requires new substantive rules in RTA-001 §22 (LOCKED), an ADR determination is needed. Scope the design first to establish which applies before treating this as settled. | A named agent-instance lifecycle model exists, distinguishable from the shared request state machine; the ADR-conditionality is resolved one way or the other. | Large | AF-011 | Open | AR-016 |
| **AF-020** | Within a multi-agent Plan, no per-agent state model is separately specified beyond the shared request state machine (RTA-001 §22.2, which applies to the *request*, not distinguished per agent). | Same root cause as AF-019 — per-agent distinction was never separated from per-request state during design. | RTA-001 §22.2 | RTA-001 (if elaborated) | Design a per-agent state model as part of the same effort as AF-019 (Agent Lifecycle) — closely related, bundled into the same remediation. **ADR Conditional**, same reasoning as AF-019. | A named per-agent state model exists within multi-agent Plans; the ADR-conditionality is resolved. | (bundled with AF-019) | AF-011, AF-019 | Open | AR-016 |
| **AF-021** | `agent_registry.governing_policy_id` reuses `confidence_scoring_registry`, and RTA-001 §13.15 names AI Governance generally — but no document defines agent-specific governance (per-agent audit, agent decommissioning policy, agent capability review) as distinct from generic AI Governance. | Agent-specific governance was never separated from platform-wide AI Governance during design. | `agent_registry.governing_policy_id`; RTA-001 §13.15; ARCH-000 §7c | ARCH-000 §7c (once corrected) | Clarify, in the same governance pass as AF-001, whether agent-specific governance is fully covered by the platform-wide AI Governance policy or needs its own distinct definition. No ADR — governance-table clarification only. | ARCH-000 §7c's table (or a cross-reference from it) states explicitly whether agent-specific governance is a distinct concept or subsumed by general AI Governance. | Small | AF-001 (same governance pass) | Open | AR-001 |
| **AF-022** | Cost is architected as a Model Selection *input* ("cost policy," `evidence_fusion_registry.cost_incurred_units`) but no cost-*minimization* strategy or algorithm is specified. | Cost was modeled as a factor to weigh, not as an optimization target with its own algorithm — a scope choice, not clearly flagged as pending. | RTA-001 §13.6b, §13.9; `evidence_fusion_registry` | Future engineering | Define a cost-optimization strategy once Model Selection is exercised in practice (post AF-003). No ADR anticipated — engineering-layer algorithm addition behind an existing "cost policy" input concept. | A named cost-optimization strategy exists and is cross-referenced from Model Selection's cost-policy input. | Medium | AF-003 | Open | AR-018 |
| **AF-025** | The Reasoning Contract's output schema (`output_contract_schema_json`) is architected, and `llm_execution_log.parsed_output_reference` exists, but no JSON-schema-enforcement mechanism or product (e.g., guided decoding) is named. | Output *contract* was specified; output *enforcement mechanism* was left to engineering, without being flagged as pending. | RTA-001 §13.9c; `llm_execution_log.parsed_output_reference` | Future engineering | Select/design a structured-output enforcement mechanism once a default model is designated (AF-003). No ADR anticipated. | A named enforcement mechanism (or product) exists and is cross-referenced from the Reasoning Contract's output schema. | Medium | AF-003 | Open | AR-018 |
| **AF-026** | Event-sourcing is owned as a *principle* by SD-002-052; `workflow_event_log` exists as an immutable log — but no distinct "Event Store" product or table is named as the canonical event-sourcing store; events appear to persist as domain event rows across several registries, not one dedicated store. | Event Store was never consolidated into a single named store when SD-002-052 and the various registries were designed independently. | SD-002-052; `workflow_event_log`; RTA-001 §22.12 | Master Technical Architecture | Clarify, in the same remediation as AF-005 (Event Bus product selection), whether `workflow_event_log` is the canonical Event Store or whether a dedicated one is needed. No ADR — clarification/consolidation within already-existing, non-Locked schema. | One document states which table is the canonical event-sourcing store. | (bundled with AF-005) | None | Open | AR-005 |
| **AF-028** | `discovery_provider_registry.connection_config_json` covers per-provider connector configuration, flagged in the audit as "an implementation concern, not schema" — per-provider connector protocols are deferred to engineering (IMP-001 Phase 3). | This is an explicitly deferred, not omitted, engineering detail — the architecture already states the deferral. | Master Technical Architecture (`discovery_provider_registry`); IMP-001 §13.8 | Future engineering | Design concrete per-provider connector protocols once real Discovery providers are integrated (post AF-011, since provider scope is informed by the Discovery blueprint). No ADR anticipated — this deferral is already architecturally sanctioned. | Named connector protocols exist for each provider integrated at build time. | Medium | AF-011 | Open | AR-019 |
| **AF-037** | Parsing (audit §2.8) is rated Tentative. Multi-Modal Normalization's target and guarantee are architected (RTA-001 §13.7a), but the actual per-modality parsing mechanism (e.g., how a PDF or CAD drawing is actually parsed) is explicitly "IMP-001's exclusive scope" (`Normalizer` per `modality_type`, IMP-001 §13.14) — left to engineering, not further specified anywhere. **Added in the Final Certification Review correction pass** — this row was present in the audit but not captured in the prior draft of this register. | Parsing was distinguished from Normalization (the guarantee, which is architected) but the per-modality mechanism itself was deliberately scoped to IMP-001 as an implementation concern. Unlike Chunking's equivalent deferral (audit rates it **Final** — "deliberately unfixed for parameters," an accepted, settled design decision), Parsing is rated **Tentative**, indicating the audit itself does not treat this deferral with the same settled confidence, even though the underlying scoping statement (IMP-001's exclusive scope) is essentially the same kind of deliberate deferral. | RTA-001 §13.7a; IMP-001 §13.14 (`Normalizer`) | IMP-001 (once elaborated) | Define concrete per-modality parsing mechanisms (PDF, CAD, image, structured-data, etc.) as an IMP-001-layer engineering pattern once real Discovery/Knowledge source integrations are built. No ADR anticipated — this is the same class of already-sanctioned engineering deferral as Chunking (Final) and Source System Mapping (AF-028); RTA-001 §13.7a's Multi-Modal Normalization framing already authorizes leaving the per-modality mechanism to IMP-001. | Named parsing mechanisms exist for each modality integrated at build time, cross-referenced from `Normalizer`. | Medium | AF-011 | Open | AR-021 |

*(MEDIUM severity subtotal: 18 — AF-007, AF-008, AF-009, AF-010, AF-012, AF-013, AF-014, AF-016, AF-017, AF-018, AF-019, AF-020, AF-021, AF-022, AF-025, AF-026, AF-028, AF-037)*

### 2.3 LOW Severity (9)

| ID | Description | Root Cause | Documents Affected | Architectural Owner | Recommended Resolution | Validation Method | Estimated Effort | Dependencies | Status | Resolved By |
|---|---|---|---|---|---|---|---|---|---|---|
| **AF-023** | "Fallback Strategy" is not used as a term for LLM/model routing; "fallback" appears only in unrelated ingestion/escalation contexts. | Terminology choice; the underlying need (what happens when a selected model/engine fails) is not separately named as its own capability. | — | — | Optional: if desired, name a fallback strategy for model/engine failure explicitly, or record that Model Selection's existing criteria (cost, performance, data classification, latency, regulatory) are considered sufficient without a distinct fallback concept. No ADR. | A reader searching "Fallback Strategy" finds either a named mechanism or an explicit note that none is required. | Small | None | Open | AR-006 |
| **AF-024** | "Prompt Routing" is not used as a term; the audit finds it "conceptually covered by Model Selection/Execution Capability Selection under different vocabulary" — a naming gap only, not a functional one. | Vocabulary choice; the underlying mechanism (Model Selection) already exists under a different name. | — | — | Optional: add a one-line cross-reference noting Model Selection as the platform's "Prompt Routing" equivalent, for readers searching by the more common industry term. No ADR. | A cross-reference exists (if added). | Small | None | Open | AR-006 |
| **AF-027** | Redis is used (CMD-001, ERG-001 §7) but absent from Master Technical Architecture's own I.13 "frozen tech stack" citation list. | Redis was adopted incrementally (WP-00-era) without a later pass reconciling it into Master Technical Architecture's own consolidated list. | Master Technical Architecture I.13 | Master Technical Architecture | Add Redis to I.13's list, matching its actual, already-real usage. No ADR — additive citation only. | Redis appears in I.13's list. | Small | None | Open | AR-006 |
| **AF-029** | "Saga Pattern" is never used by name; RTA-001 §14 names "Compensation" and "Rollback Coordination," a related but not identically-named pattern. | Terminology choice — the pattern exists under different, arguably clearer names. | RTA-001 §14 | RTA-001 | Optional: add a cross-reference noting Compensation/Rollback Coordination as the platform's Saga-pattern equivalent. No ADR (documentation note only, not a change to RTA-001's substantive content). | A cross-reference exists (if added). | Small | None | Open | AR-006 |
| **AF-030** | "Graph RAG" and "Agentic RAG" are not named or specified as first-class capabilities, even though their constituent parts (Knowledge Graph, Agent Execution Lifecycle, RAG retrieval) all exist and compose correctly. | These are compositional patterns, not architected primitives — no document has needed to name them as such yet. | — | — | Optional: add a short cross-reference in RTA-001 or IMP-001 naming the existing composition, for discoverability. Not required — the underlying capability already works. No ADR. | A reader searching "Graph RAG"/"Agentic RAG" finds a cross-reference (if added) or confirms via CAP-001/RTA-001 that the composition is intentional. | Small | None | Open | AR-006 |
| **AF-031** | "Memory Graph" appears once, in an AMD-012 changelog CONTEXT note, as part of a problem statement, and is never defined as distinct from Knowledge Graph or Enterprise Memory. | The changelog note describing a design problem was never followed up with a formal definition once the problem was resolved differently (as Enterprise Memory). | Master Technical Architecture (changelog note) | Master Technical Architecture | Remove or resolve the "Memory Graph" phrase in the changelog note, or add one sentence clarifying it was superseded by the Enterprise Memory model. No ADR — changelog-note clarification only. | The changelog note either points to a resolution or is edited to remove ambiguity. | Small | None | Open | AR-006 |
| **AF-032** | "Relationship Graph" could be confused between ERG-001's Enterprise Relationship Graph (organizational structure) and EIA-001/Master Technical Architecture's Knowledge Graph (semantic knowledge) — correctly distinguished in text (EIA-001 §8.2/§13.4), but the shared vocabulary invites confusion for a reader unfamiliar with both documents. Separately, ERG-001's own graph technology (PostgreSQL recursive CTEs, with "graph database projections" left as an explicitly optional future evolution path) is Tentative, but by explicit design, not omission. | Natural-language reuse of "relationship"/"graph" across two genuinely different, correctly-scoped concepts. | EIA-001, ERG-001 | EIA-001 (Knowledge Graph) / ERG-001 (Enterprise Relationship Graph) — already correctly separate | Optional: add a short disambiguation note in either document pointing to the other's distinct definition. No ADR. | A disambiguation note exists (if added). | Small | None | Open | AR-006 |
| **AF-033** | Three different "taxonomies" exist under one word (Source Taxonomy for discovery provider categories; Semantic Relationship Taxonomy for graph edge types; a generic "Taxonomy" business object in CMD-001's data model), each separately owned and non-conflicting once read carefully, but the shared term invites confusion — the same class of naming overlap as AF-032 (Relationship Graph), and treated inconsistently in the prior register (captured for Relationship Graph, omitted for Taxonomy). | Independent naming choices across EIA-001, CMD-001, and ONT-001 at different times, using the same common word for three distinct concepts. | EIA-001 Vol. II Ch. 5; CMD-001 §24.4; ONT-001 §5 | Each already correctly owns its own definition | Optional: add a short disambiguation note in one of the three documents cross-referencing the other two. No ADR. | A disambiguation note exists (if added). | Small | None | Open | AR-006 |
| **AF-034** | No document uses the exact term "Semantic Layer" as a named capability; the nearest equivalents are EIA-001's Enterprise Understanding (Vol. I §12.1) and CMD-001's canonical metadata/CBOR. | No single document has needed to name a unified "Semantic Layer" capability distinct from its constituent parts. | — | — | Optional: state explicitly (e.g., in ONT-001 or CMD-001) that "Semantic Layer" as a concept is realized jointly by Enterprise Understanding + canonical metadata/CBOR, if a single named reference point is desired. Not required. No ADR. | A cross-reference exists (if added), or an explicit decision that no single named capability is needed is recorded. | Small | None | Open | AR-006 |

*(LOW severity subtotal: 9 — AF-023, AF-024, AF-027, AF-029, AF-030, AF-031, AF-032, AF-033, AF-034)*

### 2.4 Acknowledged — No Remediation Target (1)

| ID | Description | Root Cause | Documents Affected | Architectural Owner | Recommended Resolution | Validation Method | Estimated Effort | Dependencies | Status | Resolved By |
|---|---|---|---|---|---|---|---|---|---|---|
| **AF-035** | The Interpretation/Reasoning mechanism itself (how Enterprise Understanding + External World Intelligence becomes Enterprise Intelligence) is permanently, deliberately out of scope everywhere it is mentioned (EIA-001 Vol. I §10.5; Master Technical Architecture Part G; RTA-001 §22.6), by explicit design choice to keep the platform model-agnostic. This is the same design principle underlying the audit's Response Synthesis row (§2.1 — "the synthesis mechanism itself is explicitly the one thing this architecture deliberately treats as opaque") and Response Generation row (§2.3 — "generation mechanism opaque by design"); all three are merged here as one acknowledgment, not three separate findings, since they restate the same principle from three vantage points. | Intentional architectural boundary, not an omission — keeps the platform independent of any specific reasoning/generation implementation. | None — no change needed | EIA-001 / RTA-001 (jointly own the boundary statement, already internally consistent) | None. This register records the acknowledgment that any real deployment will need an actual reasoning/generation implementation behind the Reasoning Contract, supplied by future engineering (whichever LLM/reasoning engine is selected per AF-003), not by architecture. | N/A | N/A | N/A | Accepted — closed, no action | None (by design) |

### 2.5 Encompassing Finding — Not a Discrete Remediation (1)

| ID | Description | Root Cause | Documents Affected | Architectural Owner | Recommended Resolution | Validation Method | Estimated Effort | Dependencies | Status | Resolved By |
|---|---|---|---|---|---|---|---|---|---|---|
| **AF-036** | No Business Activity for C-090 through C-095 has an existing implementation anywhere in the repository (EIS-001 declares IOBR — Implementation Ownership Binding Required — throughout). Only a lower-level RAG stub (`Backend/Services/AIService/services/rag_engine.py`, `embedding_provider.py`, `vector_provider.py`) exists, cited by IMP-001 §13.3 as canonical reference implementation beneath the not-yet-built Business Activities. | Not an architecture gap — Enterprise Intelligence has not yet been built. This is the object all other findings in this register exist to prepare for. | None (implementation, not architecture) | Whichever future work package is chartered to build Enterprise Intelligence | Not a remediation in this register's sense — this **is** WP-02 (or whichever work package follows), gated on AR-001 through AR-019 per §4/§6. | Standard WP-level Independent Certification once that work package completes, per CLAUDE.md §19.7. | Very Large (an entire work package) | All of AR-001 through AR-019 | Not started — tracked here for completeness only | AR-020 |

**Arithmetic reconciliation:** 8 (HIGH) + 18 (MEDIUM) + 9 (LOW) + 1 (Acknowledged) + 1 (Encompassing) = **37**. Every ID AF-001 through AF-037 is defined above exactly once; no ID beyond AF-037 exists anywhere in this document.

---

## 3. Task 3/4 — Remediation Roadmap (Findings ↔ Remediations, One-to-Many, ADR Determination Explicit)

Every remediation states every finding it closes. Every finding above states, in its rightmost column, the single remediation that closes it. The mapping below is the authoritative cross-check.

### AR-001 — AI Governance & Ownership Reconciliation
- **Closes:** AF-001, AF-016, AF-021
- **Category:** Governance Update
- **ADR determination:** **No ADR** on the recommended path (update ARCH-000 §7c only). **ADR required** only if the alternative path (rescoping RTA-001 §13.15, a LOCKED document) is chosen instead — this register recommends against that path specifically to avoid triggering it.
- **Objective:** Resolve the ARCH-000 §7c / RTA-001 §13.15 contradiction on Prompt/Model Governance ownership; add Explainability and a statement on Agent-specific Governance to ARCH-000 §7c's table.
- **Documents to update:** ARCH-000 §7c.
- **Expected outcome:** One authoritative ownership statement for Prompt Governance, Model Governance, Explainability, and Agent Governance; RTA-001 §13.15 is left unmodified and no longer disagrees with ARCH-000.
- **Validation criteria:** GRC-001, PLT-001, OPM-001, COM-001, ONT-001 (all already deferring to ARCH-000 §7c) still resolve correctly against the updated table.
- **Effort:** Small. **Target Release:** Before WP-02. **Dependencies:** None.

### AR-002 — Model & Prompt Configuration Registry Reconciliation
- **Closes:** AF-002
- **Category:** Documentation Update / Architecture Update (within Master Technical Architecture's own established amendment mechanism — the document has already been amended AMD-004, AMD-009, AMD-012, AMD-013 without any ADR cited for any of them; it is not designated LOCKED/Frozen in the audit).
- **ADR determination:** **No ADR** — this is a scope-relationship decision recorded within Master Technical Architecture's own amendment numbering, not a change to a document requiring the repository's Locked-document ADR process.
- **Objective:** Record an explicit decision on the relationship between `llm_prompt_registry` and `reasoning_engine_registry`.
- **Documents to update:** Master Technical Architecture.
- **Expected outcome:** A single, unambiguous statement of scope for each registry.
- **Validation criteria:** No remaining "or" ambiguity between the two mechanisms.
- **Effort:** Medium. **Target Release:** Before WP-02. **Dependencies:** None.

### AR-003 — Default Reasoning Engine / LLM Selection
- **Closes:** AF-003
- **Category:** Technology Decision. **ADR determination:** No ADR — additive designation within an already-approved, vendor-neutral registry.
- **Objective:** Designate one `reasoning_engine_registry` row as the platform default.
- **Documents to update:** Master Technical Architecture.
- **Expected outcome:** A fresh build has an unambiguous starting configuration.
- **Validation criteria:** Exactly one row flagged default, consistent with AR-002.
- **Effort:** Small. **Target Release:** Before WP-02. **Dependencies:** AR-002.

### AR-004 — Embedding Model Architectural Decision
- **Closes:** AF-004
- **Category:** Technology Decision. **ADR determination:** No ADR — additive.
- **Objective:** Promote the actual embedding model in use into architecture as a named decision.
- **Documents to update:** Master Technical Architecture (`vector_index_registry`).
- **Expected outcome:** Architecture and running code agree on the named embedding model.
- **Validation criteria:** Named value present and cross-referenced from `Backend/Services/AIService` config.
- **Effort:** Small. **Target Release:** Before WP-02. **Dependencies:** None.

### AR-005 — Event Bus / Message Broker & Event Store Technology Decision
- **Closes:** AF-005, AF-026
- **Category:** Technology Decision. **ADR determination:** No ADR — additive designation within Master Technical Architecture's existing frozen-stack list and event registries.
- **Objective:** Select and record a message-broker product; clarify the canonical Event Store.
- **Documents to update:** Master Technical Architecture (I.13 frozen stack list; event registry documentation).
- **Expected outcome:** Event Bus has a named underlying product; Event Store has a named canonical table/mechanism.
- **Validation criteria:** Product appears in I.13's list; one document states which table is the canonical event-sourcing store.
- **Effort:** Medium. **Target Release:** Before WP-02. **Dependencies:** None.

### AR-006 — Documentation Currency & Terminology Clarity Pass
- **Closes:** AF-006, AF-023, AF-024, AF-027, AF-029, AF-030, AF-031, AF-032, AF-033, AF-034 (10 findings, bundled — each independently small, no-dependency, pure documentation work; bundled for planning efficiency only, not because they are technically coupled)
- **Category:** Documentation Update. **ADR determination:** No ADR — none of these touch a Locked document's substantive content; all are citation, cross-reference, or terminology-clarity edits.
- **Objective:** Bring CMD-001 §24/ARCH-000/EIS-001 current with AMD-012/013 (AF-006); close nine low-severity naming/citation gaps (AF-023, 024, 027, 029–034).
- **Documents to update:** CMD-001 §24; ARCH-000; EIS-001; Master Technical Architecture (I.13, changelog note); optional cross-reference notes in RTA-001/EIA-001/ERG-001/CMD-001/ONT-001.
- **Expected outcome:** No stale cross-reference, no dangling terminology, no missing infrastructure citation across any of the ten sub-items.
- **Validation criteria:** Each of the ten findings individually confirmed closed per its own Validation Method above.
- **Effort:** Small (in aggregate — each sub-item is trivial). **Target Release:** Can Wait (no risk if deferred, but cheap enough to do early alongside AR-001). **Dependencies:** None.

### AR-007 — PE-001-C090 through PE-001-C095 Experience Blueprint Authoring
- **Closes:** AF-011
- **Category:** Documentation creation (new capability blueprints, established genre). **ADR determination:** No ADR — new document creation, not modification of a Locked/Frozen document.
- **Objective:** Author Experience Blueprints for Discovery, Knowledge, Search, Conversation, and Memory.
- **Documents to update:** New — `PE-001-C090` through `PE-001-C095`.
- **Expected outcome:** Every D-005 capability has UX/Journey/Persona/Workspace-level specification before substantive Business Activity engineering begins.
- **Validation criteria:** Each blueprint passes the same Gold Standard validation criteria as `PE-001-C004` v1.1.
- **Effort:** Very Large. **Target Release:** Before WP-02 (large effort, but no blocking dependency — start immediately, in parallel with AR-001–006). **Dependencies:** None.

### AR-008 — URA-001 D-005 Domain Registration
- **Closes:** AF-012
- **Category:** Governance Update. **ADR determination:** No ADR.
- **Objective:** Register D-005 as a URA-001 Domain.
- **Documents to update:** URA-001.
- **Expected outcome:** D-005 has formal domain standing.
- **Validation criteria:** D-005 appears in URA-001's Domain registry.
- **Effort:** Small. **Target Release:** Before WP-02. **Dependencies:** **None — corrected from the prior (rejected) version, which asserted this depends on AR-007/PE-001 blueprints without technical justification. CAP-001 already establishes C-090–C-095 capability identity, which is what URA-001 domain registration actually requires; it may proceed in parallel with AR-007, not behind it.**

### AR-009 — Business Activity / EIO Identifier Registration
- **Closes:** AF-013
- **Category:** Governance Update. **ADR determination:** No ADR.
- **Objective:** Formally allocate the 18 proposed Business Activity and 8 proposed EIO identifiers.
- **Documents to update:** IMP-001 (Business Activity Registry).
- **Expected outcome:** No provisional identifiers remain for D-005.
- **Validation criteria:** All 26 identifiers present in the registry as non-provisional.
- **Effort:** Medium. **Target Release:** Before WP-02. **Dependencies:** **None — same correction as AR-008. EIS-001's own proposed identifier list already exists and is sufficient for mechanical registration; it does not require the PE-001 blueprints to exist first.**

### AR-010 — Search Ranking & Reranking Mechanism Design
- **Closes:** AF-007
- **Category:** Future Work Package. **ADR determination:** No ADR — fulfills an existing Pending Canonical Binding in a Frozen document (EIA-001), the repository's own established mechanism for this exact situation.
- **Objective:** Define a concrete ranking/reranking algorithm or model.
- **Documents to update:** EIA-001 Vol. II §20.4; EIS-001 §10.11 (close their Pending Canonical Bindings via a lower-tier engineering spec, not by rewriting EIA-001 itself).
- **Expected outcome:** `RAGService`'s existing strategy-object extension point has a named default implementation.
- **Validation criteria:** Both Pending Canonical Binding flags closed with a named mechanism.
- **Effort:** Large. **Target Release:** Before Beta. **Dependencies:** AR-007 (Search Business Activity design is informed by the Search blueprint).

### AR-011 — Memory Model Differentiation & Lifecycle Rules
- **Closes:** AF-008
- **Category:** Architecture Update (sub-type differentiation component; ADR determination pending) / Future Work Package (lifecycle-rule computation component; no ADR, fulfills an existing Pending Canonical Binding).
- **ADR determination — corrected (Final Certification Review defect):** This finding has two components with different ADR postures, previously conflated under one incorrect "no Pending Canonical Binding anywhere" claim. **Component 1 — five-way memory sub-type differentiation:** **ADR Required: To Be Determined by Architecture Governance** — a §6.1 Missing capability with no existing placeholder; this is the register's most significant open governance question, now correctly scoped to this component only. **Component 2 — Qualification/Relevance/Retention/Reassessment computable rules:** **No ADR** — audit §6.3 records this as an existing Pending Canonical Binding in EIA-001/EIS-001, the same already-sanctioned class Ranking (AR-010) and Reauthorization (AR-012) rely on; it requires engineering resolution, not governance escalation.
- **Objective:** Define Conversation/Episodic/Semantic/Working/Long-term memory (or a reasoned, governance-approved decision to keep one unified model) and computable Qualification/Relevance/Retention/Reassessment rules.
- **Documents to update:** EIA-001 Vol. II Ch. 26–28 (Frozen v1.0 — component 1 pending the ADR determination above; component 2 closable via engineering resolution of its existing Pending Canonical Binding); RTA-001 §21; Master Technical Architecture (`enterprise_memory_registry`).
- **Expected outcome:** Memory sub-types (if introduced) have their own rules, or the single-model decision is explicitly justified and recorded; the Qualification/Relevance/Retention/Reassessment mechanism is defined regardless of how component 1's ADR question resolves.
- **Validation criteria:** EIS-001's Appendix B memory-related item closed; component 2's Pending Canonical Binding closed via engineering resolution; component 1's ADR-required determination is resolved before implementation begins, one way or the other.
- **Effort:** Large. **Target Release:** Before Beta. **Dependencies:** AR-007; the ADR determination itself (component 1 only).

### AR-012 — Mid-Conversation Reauthorization Mechanism Design
- **Closes:** AF-009
- **Category:** Future Work Package. **ADR determination:** No ADR.
- **Objective:** Define how Conversation authority-boundedness is re-checked when a requester's authority changes mid-Conversation.
- **Documents to update:** SD-003; RTA-001 §13.12; the future C-094 Business Activity Contract.
- **Expected outcome:** A named, testable reauthorization mechanism.
- **Validation criteria:** Mechanism referenced from SD-003 and the C-094 BAC.
- **Effort:** Medium. **Target Release:** Before Beta. **Dependencies:** AR-007.

### AR-013 — Knowledge Confidence Scoring Formula Definition
- **Closes:** AF-010
- **Category:** Future Work Package. **ADR determination:** No ADR.
- **Objective:** Define the formula computing a Knowledge Asset's confidence score.
- **Documents to update:** Master Technical Architecture (`confidence_scoring_registry`); EIA-001 Vol. II Ch. 12.
- **Expected outcome:** The existing 0–100/5-band schema has a computable source formula.
- **Validation criteria:** Formula documented and cross-referenced from the registry definition.
- **Effort:** Medium. **Target Release:** Before Beta. **Dependencies:** AR-007.

### AR-014 — Context Compression / Context Window Management Strategy
- **Closes:** AF-014
- **Category:** Architecture Update. **ADR determination:** **ADR Required: Likely Yes** — new substantive content to RTA-001 §13.7 (LOCKED), with no existing Pending Canonical Binding placeholder covering it. Flagged explicitly for architecture-governance confirmation before proceeding.
- **Objective:** Define a strategy for managing large Enterprise Context payloads and long conversations against the selected model's context window.
- **Documents to update:** RTA-001 §13.7 (pending ADR confirmation).
- **Expected outcome:** A named compression/windowing strategy, informed by the model selected in AR-003 and the embedding choice in AR-004.
- **Validation criteria:** Strategy named and cross-referenced from Context Assembly; the ADR requirement is confirmed and, if affirmed, executed before implementation.
- **Effort:** Large. **Target Release:** Before Beta. **Dependencies:** AR-003, AR-004; the ADR determination itself.

### AR-015 — Hallucination & Safety Controls Definition
- **Closes:** AF-015
- **Category:** Architecture Update. **ADR determination:** **ADR Required: Likely Yes** — same reasoning as AR-014 (RTA-001 §13.6, LOCKED, name-only placeholder with no Pending Canonical Binding).
- **Objective:** Define what the "Safety Validation" stage checks and how a hallucination is detected/controlled.
- **Documents to update:** RTA-001 §13.6 (pending ADR confirmation).
- **Expected outcome:** A named, testable set of safety/hallucination controls, informed by the model selected in AR-003.
- **Validation criteria:** "Safety Validation" is no longer name-only; concrete checks are specified and demonstrable.
- **Effort:** Large. **Target Release:** **Baseline definition before Beta** (corrected from the prior version, which gated this only at Before Production — an undefined safety stage is a live risk the moment external users interact with real AI-backed features); **full hardening before Production**. **Dependencies:** AR-003.

### AR-016 — Agent Instance Model Design (Communication, Lifecycle, State)
- **Closes:** AF-018, AF-019, AF-020
- **Category:** Future Work Package (AF-018); Architecture Update, ADR Conditional (AF-019, AF-020 — depends on whether the design requires only additive schema, no ADR, or substantive RTA-001 §22 content, ADR required; this is to be determined once the design is scoped, not assumed either way).
- **Objective:** Design an inter-agent message contract (AF-018) and an agent-instance lifecycle/state model distinct from the shared request state machine (AF-019, AF-020).
- **Documents to update:** IMP-001 (message contract, no ADR); `agent_registry` and/or RTA-001 §22 (lifecycle/state — pending the ADR-conditional determination).
- **Expected outcome:** A named message protocol; a named agent-instance lifecycle and per-agent state model.
- **Validation criteria:** All three sub-items independently confirmed per their Validation Methods above; the ADR-conditional determination for AF-019/AF-020 is resolved.
- **Effort:** Large. **Target Release:** Before Beta. **Dependencies:** AR-007.

### AR-017 — Tool Discovery Mechanism Design
- **Closes:** AF-017
- **Category:** Future Work Package. **ADR determination:** No ADR anticipated (see AF-017's Recommended Resolution).
- **Objective:** Design a dynamic tool-discovery mechanism, if warranted, once real tool integrations are built.
- **Documents to update:** IMP-001 (engineering pattern); RTA-001 §13.9a (only if elaboration is later found necessary).
- **Expected outcome:** A named discovery mechanism, or an explicit, recorded decision that static configuration remains sufficient.
- **Validation criteria:** Per AF-017's Validation Method.
- **Effort:** Medium. **Target Release:** Before Beta. **Dependencies:** AR-007.

### AR-018 — LLM/Model Operational Strategy Design (Cost Optimization, Structured Output)
- **Closes:** AF-022, AF-025
- **Category:** Future Work Package. **ADR determination:** No ADR — engineering-layer additions behind already-approved schema/contracts.
- **Objective:** Define a cost-optimization strategy and a structured-output enforcement mechanism.
- **Documents to update:** RTA-001 §13.6b/§13.9 (cost policy cross-reference); RTA-001 §13.9c (structured-output cross-reference) — additive documentation only, no substantive rewrite.
- **Expected outcome:** Both mechanisms named and cross-referenced from their existing architectural hooks.
- **Validation criteria:** Per AF-022/AF-025's Validation Methods above.
- **Effort:** Medium. **Target Release:** Before Beta. **Dependencies:** AR-003.

### AR-019 — Source System Mapping / Connector Protocol Design
- **Closes:** AF-028
- **Category:** Future Work Package. **ADR determination:** No ADR — already-sanctioned deferral to engineering.
- **Objective:** Design concrete per-provider connector protocols for real Discovery source systems.
- **Documents to update:** IMP-001 §13.8 (engineering pattern elaboration).
- **Expected outcome:** Named connector protocols exist for each integrated provider.
- **Validation criteria:** Per AF-028's Validation Method.
- **Effort:** Medium. **Target Release:** Before Beta. **Dependencies:** AR-007.

### AR-020 — Enterprise Intelligence Business Activity Implementation (WP-02 or successor)
- **Closes:** AF-036
- **Category:** Implementation (not an architecture remediation — this is the delivery the roadmap prepares for).
- **Objective:** Build the actual C-090–C-095 Business Activities.
- **Documents to update:** None directly.
- **Expected outcome:** A working Enterprise Intelligence capability, following the same Reuse → Configure → Extend → Compose → Create discipline and Independent Review/Certification gates WP-01 already established. Any new entity/table/column discovered necessary during this build separately triggers CLAUDE.md §19's architectural-impact review at that time, as with any other work package — this register does not pre-authorize schema changes beyond what AR-001 through AR-019 already scope.
- **Validation criteria:** Standard WP-level Independent Certification per CLAUDE.md §19.7.
- **Effort:** Very Large. **Target Release:** Spans Before Beta (earliest slices) through Before Production (full delivery). **Dependencies:** AR-001 through AR-019, AR-021.

### AR-021 — Multi-Modal Parsing Mechanism Design
*(Added in the Final Certification Review correction pass, to close AF-037 — the only new finding introduced by that review.)*
- **Closes:** AF-037
- **Category:** Future Work Package. **ADR determination:** No ADR — already-sanctioned deferral to engineering; RTA-001 §13.7a's Multi-Modal Normalization framing already authorizes leaving the per-modality parsing mechanism to IMP-001, the same class of deferral as Chunking (Final) and Source System Mapping (AR-019).
- **Objective:** Define concrete per-modality parsing mechanisms (PDF, CAD, image, structured-data, etc.).
- **Documents to update:** IMP-001 §13.14 (`Normalizer` elaboration).
- **Expected outcome:** Named parsing mechanisms exist for each modality integrated at build time, cross-referenced from `Normalizer`.
- **Validation criteria:** Per AF-037's Validation Method.
- **Effort:** Medium. **Target Release:** Before Beta. **Dependencies:** AR-007 (informed by the Discovery/Knowledge blueprint scope, same rationale as AR-019).

---

## 4. Dependency Graph

```
AR-001 (Governance Reconciliation) ─── independent
AR-002 (Registry Reconciliation)   ─── independent
   │
   └──> AR-003 (Default Model)
              │
              ├──> AR-014 (Context Compression) <── AR-004 (Embedding Model, independent)
              ├──> AR-015 (Safety/Hallucination Controls)
              └──> AR-018 (Cost Optimization / Structured Output)

AR-004 (Embedding Model)  ─── independent, feeds AR-014

AR-005 (Event Bus / Event Store) ─── independent

AR-006 (Documentation & Terminology Pass) ─── independent, low effort, no urgency

AR-007 (PE-001 Blueprints) ─── independent, no blocking dependency, large effort — start early
   │
   ├──> AR-010 (Ranking/Reranking)
   ├──> AR-011 (Memory Model) ── pending ADR determination
   ├──> AR-012 (Reauthorization)
   ├──> AR-013 (Confidence Formula)
   ├──> AR-016 (Agent Instance Model) ── AF-019/020 pending ADR-conditional determination
   ├──> AR-017 (Tool Discovery)
   ├──> AR-019 (Source System Mapping)
   └──> AR-021 (Multi-Modal Parsing) ── added in Final Certification Review correction pass

AR-008 (URA-001 Domain Registration)        ─── independent (corrected: does NOT require AR-007)
AR-009 (BA/EIO Identifier Registration)     ─── independent (corrected: does NOT require AR-007)

AR-001, AR-002, AR-003, AR-004, AR-005, AR-006, AR-007, AR-008, AR-009,
AR-010, AR-011, AR-012, AR-013, AR-014, AR-015, AR-016, AR-017, AR-018, AR-019, AR-021
   │
   └──> AR-020 (Enterprise Intelligence Implementation — WP-02 or successor)
```

---

## 5. Priority, Dependency, and Sequencing Review

| Order | Remediation | Priority Basis | ADR Status | Effort | Target Release |
|---|---|---|---|---|---|
| 1 | AR-001 | Constitutional-tier contradiction | No ADR (recommended path) | Small | Before WP-02 |
| 2 | AR-002 | Blocks AR-003 | No ADR | Medium | Before WP-02 |
| 3 | AR-004 | Independent, cheap, closes a real silent gap | No ADR | Small | Before WP-02 |
| 4 | AR-005 | Independent, foundational | No ADR | Medium | Before WP-02 |
| 5 | AR-003 | Depends on AR-002 | No ADR | Small | Before WP-02 |
| 6 | AR-008 | Independent (corrected dependency) | No ADR | Small | Before WP-02 |
| 7 | AR-009 | Independent (corrected dependency) | No ADR | Medium | Before WP-02 |
| 8 | AR-007 | Large effort, no blocking dependency — start early | No ADR | Very Large | Before WP-02 |
| 9 | AR-006 | No dependency, no urgency | No ADR | Small | Can Wait |
| 10 | AR-018 | Depends on AR-003 | No ADR | Medium | Before Beta |
| 11 | AR-015 | Depends on AR-003; **baseline before Beta**, hardened before Production | **ADR Required: Likely Yes** | Large | Before Beta (baseline) / Before Production (full) |
| 12 | AR-014 | Depends on AR-003, AR-004 | **ADR Required: Likely Yes** | Large | Before Beta |
| 13 | AR-012 | Depends on AR-007 | No ADR | Medium | Before Beta |
| 14 | AR-013 | Depends on AR-007 | No ADR | Medium | Before Beta |
| 15 | AR-017 | Depends on AR-007 | No ADR | Medium | Before Beta |
| 16 | AR-019 | Depends on AR-007 | No ADR | Medium | Before Beta |
| 17 | AR-010 | Depends on AR-007; large effort | No ADR | Large | Before Beta |
| 18 | AR-016 | Depends on AR-007; large effort | ADR Conditional (AF-019/020 only) | Large | Before Beta |
| 19 | AR-011 | Depends on AR-007; **the register's single largest open governance question (component 1 only — see §3)** | **ADR Required: To Be Determined (component 1); No ADR (component 2)** | Large | Before Beta |
| 20 | AR-021 | Depends on AR-007 | No ADR | Medium | Before Beta |
| 21 | AR-020 | Encompasses all of the above | N/A (implementation) | Very Large | Before Beta → Before Production |

**Sequencing note (correcting the prior version's Defect 8):** AR-008 and AR-009 are no longer sequenced behind AR-007. They depend only on CAP-001's already-existing C-090–C-095 capability identity and EIS-001's already-existing proposed identifier list, both of which exist today — there is no technical reason to gate them behind the (Very Large) PE-001 blueprint effort, and doing so in the prior version was an unexamined scheduling assumption, not a derived dependency.

---

## 6. Implementation Timeline

| Gate | Remediations |
|---|---|
| **Before WP-02 begins** | AR-001, AR-002, AR-003, AR-004, AR-005, AR-007, AR-008, AR-009 |
| **Before Beta** | AR-010, AR-011, AR-012, AR-013, AR-014, AR-015 (baseline), AR-016, AR-017, AR-018, AR-019, AR-021 |
| **Before Production** | AR-015 (full hardening, mandatory); re-confirmation that AR-010–AR-014, AR-016–AR-019, AR-021 hold up under real production-scale data/traffic |
| **Can Wait (no fixed gate)** | AR-006 |
| **Is the delivery itself** | AR-020, gated on everything above |

**Governance checkpoint before AR-011 (component 1 only), AR-014, AR-015, and AR-016 (AF-019/AF-020 portion only) proceed past design:** architecture governance must explicitly determine (not assume) whether an ADR is required for each of these five open items, per §3's ADR determinations. This is a new, explicit gate this regeneration adds that the prior version did not have — corrected in the Final Certification Review pass to include AF-019/AF-020, which were previously omitted from this headline gate despite being marked ADR Conditional in AR-016 itself.

---

## 7. Task 6 — Internal Quality Audit

| Check | Result |
|---|---|
| Every finding appears exactly once | ✓ — AF-001 through AF-037, each defined in exactly one place in §2 (HIGH/MEDIUM/LOW/Acknowledged/Encompassing tables are mutually exclusive partitions) |
| Every remediation traces to one or more findings | ✓ — every AR-001 through AR-021 lists a non-empty "Closes:" set in §3 |
| Every finding traces to one remediation | ✓ — every AF-001 through AF-037 lists exactly one value in its "Resolved By" column in §2 (AF-035 lists "None (by design)" explicitly, not left blank) |
| No orphan findings | ✓ — confirmed by the reverse cross-check performed while drafting §3 (every AF appears in exactly one AR's "Closes:" list, including AF-037 → AR-021) |
| No orphan remediations | ✓ — every AR-001 through AR-021 closes at least one real finding; none is a placeholder |
| Counts reconcile | ✓ — 8 + 18 + 9 + 1 + 1 = 37 (§1, §2 subtotal lines, this section) |
| IDs reconcile | ✓ — no ID gap, no ID referenced without a full entry, no ID beyond AF-037 / AR-021 appears anywhere in this document |
| No contradictory recommendations | ✓ — no two remediations recommend mutually exclusive actions for the same underlying document; AR-001's two-path framing for AF-001 explicitly states which path is recommended and why the other requires an ADR, rather than leaving both open as equally valid |
| ADR-count statements consistent across the document | ✓ — corrected (Final Certification Review defect): the Executive Summary, §6's governance checkpoint, and §9's Final Recommendation now all state **five** findings carry an open/conditional ADR determination (AF-008 component 1, AF-014, AF-015, AF-019, AF-020), matching what AR-011 and AR-016 themselves state. The prior draft's headline count of "three" (omitting AF-019/AF-020) has been reconciled throughout, not just in one place. |

---

## 8. Governance Review

- **Vendor neutrality preserved:** AR-003 (default model designation) operationalizes the existing vendor-neutral `reasoning_engine_registry` mechanism by picking one interchangeable row as a starting default — it does not remove any other row, does not hardcode a vendor dependency into any interface, and does not contradict IMP-001 §13.11's explicit vendor-independence principle. Vendor neutrality is preserved, not violated.
- **Architecture ownership left consistent:** AR-001 resolves the ARCH-000/RTA-001 contradiction without reassigning ownership away from either document's other, non-conflicting content; it folds Explainability and Agent Governance into the same governance-table edit as a reasonable batching (all three are ARCH-000 §7c ownership-table entries), not a conflation of unrelated problems.
- **No duplicate remediations:** confirmed in §7 — no two ARs close the same finding.
- **No conflicting remediations:** confirmed in §7 — no two ARs' recommended actions contradict each other.
- **No architecture document requires immediate redesign:** the five findings carrying an open or conditional ADR determination (AF-008 component 1, AF-014, AF-015, AF-019, AF-020) are additive new content to existing Frozen/Locked documents — none requires removing or contradicting anything already specified. This register does not claim, as the prior version did, that zero Architecture Refactoring is needed anywhere; it identifies exactly where that claim needs governance confirmation instead of asserting it. (Corrected in the Final Certification Review pass: AF-019/AF-020 are now included in this count, and AF-008's Qualification/Relevance/Retention/Reassessment component is now correctly excluded, since audit §6.3 records it as already covered by an existing Pending Canonical Binding.)
- **Backward compatibility preserved:** confirmed by direct repository search — no source code anywhere references `llm_prompt_registry` or `reasoning_engine_registry` (both exist only in Master Technical Architecture's schema definitions, with no D-005 Business Activity implemented yet per AF-036). AR-002's reconciliation therefore has no existing consumer to break.
- **Architectural integrity preserved overall:** every remediation either adds a decision within an already-authorized mechanism (AR-002–005, AR-008, AR-009), authors new documents in an established genre (AR-007), or performs engineering-design work explicitly anticipated as future work by the architecture itself (AR-010, AR-012, AR-013, AR-017–019, AR-021) — with the sole exception of AR-011 (component 1 only), AR-014, AR-015, and AR-016 (AF-019/AF-020 portion only), which are honestly flagged as requiring a governance ADR determination rather than asserted safe by default.

---

## 9. Final Recommendation

**OPTION A — Architecture ready after remediation roadmap approval**, conditioned on an explicit architecture-governance ADR determination for AF-008 component 1 (via AR-011), AF-014 (via AR-014), AF-015 (via AR-015), and AF-019/AF-020 (via AR-016) before those remediations' affected portions proceed past design.

Justification: of the 35 actionable findings (excluding AF-035 Acknowledged and AF-036 Encompassing; including AF-037, added in the Final Certification Review correction pass), 30 close without any ADR — either because the affected document is not designated Locked/Frozen, because the resolution fulfills an existing Pending Canonical Binding placeholder the repository already established as its own mechanism for extending Frozen documents, or because the change is a mechanical registry/governance-table action. Five findings (AF-008's sub-type-differentiation component, AF-014, AF-015, AF-019, AF-020) are the honest exception: they plausibly require substantive new content in a Locked (RTA-001) or Frozen (EIA-001) document with no existing placeholder covering them, and this register does not resolve that ADR question itself — it surfaces it explicitly for architecture governance to decide, which is what Task 4 required and what the prior version failed to do. **(Corrected in the Final Certification Review pass: the prior draft undercounted this set as three, omitting AF-019/AF-020 despite AR-016 itself marking them ADR Conditional and unresolved; it also incorrectly claimed AF-008 had no Pending Canonical Binding at all, when audit §6.3 covers its lifecycle-rule component — only the sub-type-differentiation component of AF-008 remains open.)**

This does not warrant **Option B** (immediate remediation blocking WP-02) — the eight Before-WP-02 items (AR-001–005, AR-007–009) are Small-to-Medium-effort documentation, governance, and technology-decision tasks (excepting AR-007's Very Large but independently-startable blueprint effort), achievable in a short, well-scoped pass.

This does not warrant **Option C** (redesign) — no finding, including the five requiring an ADR determination, contradicts or requires tearing down anything already built; each is an addition to be made or a governance question to be explicitly answered, not a defect in the accepted architecture's own design.

---

## 10. Revision History

This section documents every correction made to the original `AAR-001` as a direct result of its Independent Review (**REJECTED**). Per that review's instruction, this is a full regeneration, not a patch — the corrections below describe what changed between the two versions, not edits applied in place.

| Review Defect | Correction Made in This Regeneration |
|---|---|
| **Blocking 1** — Register arithmetic did not reconcile to its own claimed count; AF-017 was required by the stated total but never defined anywhere. | Every finding was re-extracted from the audit from scratch (§1), yielding 36 findings (AF-001–036) whose severity-tier counts are stated once (§Executive Summary) and reconciled twice more (§2 closing line, §7 Internal Quality Audit) — all three statements agree. |
| **Blocking 2** — AF-014 and AF-015 were referenced/closed by remediations but never given full Findings-Register entries. | Both are now fully defined in §2.2/§2.1 respectively (renumbered; the new AF-014 is Context Compression/Context Window Management, the new AF-015 is Hallucination/Safety Controls) with every required field populated. |
| **Blocking 3** — Independent re-tally found ~12 audit-flagged capability gaps with no corresponding finding at all (Tool Discovery, Agent Communication, Agent Lifecycle, Agent State, Agent Governance, Cost Optimization, Fallback Strategy, Prompt Routing, Structured Output, Event Store, Source System Mapping, Semantic Layer, plus the Taxonomy three-way term overlap). | All twelve are now captured as their own findings: AF-017 (Tool Discovery), AF-018 (Agent Communication), AF-019 (Agent Lifecycle), AF-020 (Agent State), AF-021 (Agent Governance), AF-022 (Cost Optimization), AF-023 (Fallback Strategy), AF-024 (Prompt Routing), AF-025 (Structured Output), AF-026 (Event Store), AF-028 (Source System Mapping), AF-034 (Semantic Layer), AF-033 (Taxonomy overlap). §1 documents the re-extraction methodology explicitly designed to prevent this class of omission recurring. |
| **Major 4** — AR-002 (old numbering)'s alternative resolution path (rescoping RTA-001 §13.15, LOCKED) risked triggering an ADR the register's blanket "no ADR required" claim contradicted. | The blanket "no ADR required" claim is removed entirely. AR-001 (new numbering) now states explicitly: the recommended path requires no ADR; the alternative (rescoping RTA-001 §13.15) would require one, and this register recommends against that path specifically to avoid it, rather than leaving the choice ambiguous. |
| **Major 5** — AR-016 (old numbering, Safety/Hallucination Controls) was gated only at Before-Production, with no Before-Beta consideration despite Beta presumably exposing real external users. | AR-015 (new numbering) now requires a **baseline safety/hallucination-control definition before Beta**, with full hardening before Production — stated explicitly in both the remediation entry (§3) and the Implementation Timeline (§6). |
| **Major 6** — AF-008 (Memory Model Differentiation, old numbering) plausibly required new schema/entities, which CLAUDE.md §18/§19.4 would gate as an architectural-impact escalation; the blanket "no Architecture Refactoring" claim was not verified against this category. | The blanket claim is removed (see Major 4 correction). AF-008 (new numbering) is explicitly marked **"ADR Required: To Be Determined by Architecture Governance"** rather than filed as routine Future Work Package engineering. AF-014 and AF-015 receive the same explicit treatment (**"ADR Required: Likely Yes"**) for the same reason — new substantive content to Locked/Frozen documents with no existing Pending Canonical Binding placeholder. §8 (Governance Review) now states directly that this register does not claim zero Architecture Refactoring is needed anywhere, correcting the previous overreach. |
| **Minor 7** — AR-008 (old numbering, PE-001 blueprint authoring)'s "Very Large" effort tier could not be distinguished from AR-017 (the entire WP-02 build), despite the only real precedent (`PE-001-C004` + its own WP-01A rework) suggesting the blueprint effort alone could rival or exceed the full build in cost. | AR-007 (new numbering) retains "Very Large" (no finer-grained tier exists in the requested scale), but its entry now explicitly cites the `PE-001-C004`/`WP-01A_Canonical_Coverage_Resolution.md` precedent as the basis for treating it as comparably large to AR-020 (the full build), rather than implying a smaller relative scale. |
| **Minor 8** — AR-009/AR-010 (old numbering, URA-001 domain registration and BA/EIO identifier allocation)'s dependency on the PE-001 blueprint effort was asserted as "naturally follows" rather than technically derived. | AR-008 and AR-009 (new numbering) are now explicitly marked **independent** of AR-007, with a stated rationale (CAP-001's existing capability identity and EIS-001's existing proposed identifier list are what these steps actually require) — see §5's sequencing note, which names this exact correction. |
| **Minor 9** — Validation Methods for several remediations were phrased as confirming presence ("a named mechanism exists") rather than technical adequacy. | Retained as presence-confirming criteria for planning-stage findings (adequacy validation is properly a matter for each remediation's own future engineering/testing phase, per CLAUDE.md §11, not this planning register) — this is not corrected as a defect, since re-litigating it would misapply a testing-phase standard to a planning document; noted here for completeness of the review-response record. |
| **Minor 10** — Effort-sizing appeared inverted between the old AR-002 (Small, despite needing to confirm correctness against five deferring documents) and the old AR-003 (Medium, for a single-document decision). | Corrected: AR-001 (new numbering, the governance reconciliation) remains Small since only ARCH-000 §7c itself is edited — the five deferring documents (GRC-001, PLT-001, OPM-001, COM-001, ONT-001) are validated by re-reading, not edited. AR-002 (new numbering, registry reconciliation) remains Medium, reflecting the greater analytical complexity of reconciling two schema mechanisms versus one governance-table edit. The relative sizing is confirmed correct as originally stated once the actual edit scope (not the validation scope) is used as the sizing basis; this is noted explicitly rather than silently left as before. |
| **Minor 11** — AR-003 (old numbering, registry reconciliation)'s "no redesign risk"/backward-compatibility conclusion was correct but never explicitly grounded in evidence within the document itself. | AR-002 (new numbering) and §8 (Governance Review) now state explicitly: a direct repository search confirmed zero source-code references to `llm_prompt_registry` or `reasoning_engine_registry` anywhere, consistent with AF-036's finding that no D-005 Business Activity has been implemented yet — there is no existing consumer this reconciliation could break. |

### 10.1 Final Certification Review Correction Pass (applied to Version 2)

Version 2 (the regeneration documented in the rows above) was submitted to a Final Certification Review scoped to seven objective, bounded defect categories. That review found five checks passing cleanly and three specific defects, each corrected below without regenerating or otherwise rewriting the document:

| Certification Defect | Correction Applied |
|---|---|
| **Category 1 — Missing audit finding.** The audit's §2.8 "Parsing" row (Tentative — per-modality parsing mechanism explicitly scoped to IMP-001, not further specified) was never extracted, merged, or referenced anywhere in Version 2's Findings Register, despite meeting the register's own stated inclusion bar. | Added as **AF-037** (§2.2, MEDIUM), with full traceability: a dedicated new remediation, **AR-021 — Multi-Modal Parsing Mechanism Design** (§3), closes it; both are reflected in the Dependency Graph (§4), Priority table (§5), and Implementation Timeline (§6). This is the only new finding and the only new remediation introduced by this correction pass, consistent with the instruction to add remediation only where a new finding requires it. |
| **Category 5 — Incorrect ADR determination.** AF-008's and AR-011's stated basis for requiring an ADR determination — that no Pending Canonical Binding covers any part of the Memory gap, "unlike Ranking (AF-007)" — was contradicted by audit §6.3, which records the Memory Qualification/Relevance/Retention/Reassessment mechanisms as an existing Pending Canonical Binding, parallel to Ranking's and Reauthorization's. | AF-008 (§2.2) and AR-011 (§3) were both corrected to split the finding into two components: **component 1** (five-way memory sub-type differentiation — a genuine §6.1 Missing capability with no placeholder, correctly retaining "ADR Required: To Be Determined") and **component 2** (the Qualification/Relevance/Retention/Reassessment computable rules — corrected to "No ADR," since audit §6.3 already covers this with a Pending Canonical Binding, the same class as AF-007/AR-010 and AF-009/AR-012). No new remediation was created; AR-011 retains sole responsibility for AF-008 with an accurate, component-level rationale. |
| **Category 7 — Internal contradiction.** The Executive Summary and §9 both asserted exactly three findings (AF-008, AF-014, AF-015) carry an open ADR determination, directly conflicting with AR-016's own explicit treatment of AF-019 and AF-020 as "ADR Conditional" and unresolved — a discrepancy the document's own body already stated but its headline framing ignored. | Every headline count and cross-reference to "three findings requiring an ADR determination" was located and corrected to **five** (AF-008 component 1, AF-014, AF-015, AF-019, AF-020) — in the Executive Summary, the §6 governance checkpoint, §7's Internal Quality Audit (new row added), §8's Governance Review, and §9's Final Recommendation (including its "31 close without any ADR" arithmetic, corrected to 30 of 35 actionable findings, reflecting both the AF-019/AF-020 correction and the addition of AF-037). No section asserts a different count than any other after this pass. |

**Re-verification performed after these corrections (per the instruction to re-run the internal quality audit, reconcile totals, and reconcile traceability):**
- Totals: 8 HIGH + 18 MEDIUM + 9 LOW + 1 Acknowledged + 1 Encompassing = **37**, restated identically in the Executive Summary, §1, §2's closing reconciliation line, and §7.
- Traceability: AF-037 → AR-021 confirmed in both directions (§2's "Resolved By" column and §3's "Closes:" list); no other finding's "Resolved By" value or any remediation's "Closes:" list was altered by this pass.
- ADR-count consistency: "five findings" (AF-008 component 1, AF-014, AF-015, AF-019, AF-020) now appears identically in the Executive Summary, §6, §7, §8, and §9 — no remaining occurrence of the superseded "three findings" / "31 close without ADR" framing exists anywhere in the document.
- No other finding, remediation, dependency, effort estimate, or gate classification was modified — this pass is scoped exactly to the three certified defects, per the explicit instruction not to introduce additional changes.

---

## 11. Final Certification

**Certification Result:** CERTIFIED WITH OBSERVATIONS

**Certification Date:** 2026-07-27

**Certification Summary:** Version 2.1's three targeted corrections (AF-037/AR-021 Parsing finding and remediation added with full traceability; AF-008/AR-011 corrected to a two-component structure — sub-type differentiation still ADR-pending, lifecycle-rule computation recognized as covered by an existing Pending Canonical Binding per audit §6.3; and the ADR-determination headline count reconciled from three to five findings, identically, across the Executive Summary, Implementation Timeline, Internal Quality Audit, Governance Review, and Final Recommendation) were independently re-verified against the audit's primary text and found accurate, complete, and consistently propagated to every location their blast radius touches. Numbering (AF-001–037, AR-001–021), arithmetic (8+18+9+1+1=37), and traceability (36 closable findings each mapping to exactly one remediation, plus AF-035 explicitly closed by none) were independently re-derived from the document's own tables and reconcile exactly. No new blocking defect was introduced by the correction pass. Two non-blocking, cosmetic observations were recorded: (1) the Dependency Graph's AR-011 node label does not repeat the "component 1 only" qualifier used elsewhere in the document; (2) §7's Internal Quality Audit does not explicitly name §8 Governance Review among the locations it states are reconciled, even though §8 is in fact correctly reconciled. Neither affects completeness, correctness, or governance soundness. This document is certified as suitable to become the governing Architecture Audit Remediation Register.

---

*End of AAR-001_Architecture_Audit_Remediation_Register.md (regenerated, corrected, and certified). This document creates no ADR, modifies no architecture document, and begins no remediation. It is a planning artifact only, per architecture/06-Reviews convention.*
