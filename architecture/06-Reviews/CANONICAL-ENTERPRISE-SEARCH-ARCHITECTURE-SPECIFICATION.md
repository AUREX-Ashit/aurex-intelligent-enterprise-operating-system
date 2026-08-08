# The Canonical Enterprise Search Architecture Specification

**Type:** Reconstruction, not proposal. Every claim below is traced to an existing repository document; nothing here is newly designed. Where the repository does not yet answer a question this specification's own structure raises, that is stated as a disclosed gap, per the same discipline every prior consolidation exercise in this repository (`ENTERPRISE-AI-ARCHITECTURE-AUDIT.md`, `AI-CONFIGURATION-TRACEABILITY-MATRIX.md`) has followed.

---

## 1. Business Objective

Enterprise Search (`C-093`) exists to answer one question a traditional enterprise search index cannot: not merely *where is this document*, but *what does the enterprise actually know, and how confident are we in it*. `EIA-001 Volume I §5.1.6` states the governing constraint directly — **"Search and Conversation Are Access Patterns, Not Sources."** Enterprise Search never originates knowledge; it is one of two ways (the other being `C-094` AI Conversation Management) that an already-continuously-formed body of Enterprise Understanding is *accessed*, scoped through Enterprise Context. This is the architecture's central differentiator from conventional enterprise search: a keyword or vector index sits in front of a document store; Enterprise Search sits in front of a **living model of the enterprise itself** — Knowledge Assets and their Relationships, each carrying Confidence, Provenance, and Evidence as first-class properties, never bare text.

## 2. Functional Architecture

No single document states one canonical pipeline end to end — this specification's own contribution is naming, and citing, where each stage actually lives. Four documented flows compose the real picture, at four different altitudes:

- **`EIA-001 Vol. I §7.2`**, the meta-model: `Source → (C-090 Discovery) → Signal → (C-091 Knowledge Management) → Knowledge Asset → (C-092 Knowledge Graph) → Relationship → Enterprise Understanding → (C-093/C-094, scoped by Enterprise Context) → Access`.
- **`Complete_Blueprint.md §7`**, the business-process layer — IDAL, *"Understand → Infer → Confirm → Strengthen Confidence"*: Extract → Retrieve → Infer → Confirm → Correct → Route (unresolved gaps assigned to a domain owner, never left unattended) → Ask (only when extraction, retrieval, inference, and routing have all failed).
- **`Master_Technical_Architecture.md` Part G**, the component layer: **Discover → Explore → Correlate → Reason → Validate**, each a named service node.
- **`IMP-001 §13.14`**, the engineering layer, the most granular: Discovery → Normalization → Knowledge Object generation → Embedding → Retrieval → Evidence creation → Knowledge/Memory update.

`EIA-001 §12.1`/`§12.2` fixes the two governing concepts these flows all feed: **Enterprise Understanding** ("the aggregate of every Knowledge Asset and Relationship... continuously formed, never delivered as a finished artifact") and **Enterprise Context** ("a bounded, situational projection of Enterprise Understanding... derived, not authored"). One explicit, disclosed gap sits at the top of this stack: `EIA-001 §7.2`'s own **Interpretation** step (Enterprise Understanding → Enterprise Intelligence) is stated to have no implementation-ready specification anywhere in the repository yet.

## 3. Technical Architecture

The physical realization is `Master_Technical_Architecture.md` AMD-012 (LOCKED), consumed at runtime by `RTA-001 §13` (the AI Runtime) and engineered by `IMP-001 §13.2–14`:

| Concern | Owning construct | Status |
|---|---|---|
| Document Ingestion | `data_ingestion_registry`, `evidence_registry` — Document Ingestion Service | Specified; `IMP-001 §13.4`'s `ChunkingStrategy` per source type is aspirational — `WP-11`'s own shipped code (`TD-125`) is a disclosed fixed-size placeholder |
| Vector Database | `vector_index_registry` (`retrieval_mode`: SEMANTIC/LEXICAL/HYBRID) | Real, tenant-scoped configuration (`WP-11` `BA-01`); the concrete embedding/vector-search provider remains stubbed — no credentials configured anywhere in this environment |
| Knowledge Graph | `enterprise_knowledge_graph_registry`, `knowledge_asset_registry` — Neo4j Aura, technology-selected | Specified; zero implementation |
| Evidence Store | `evidence_registry`, `document_chunk_registry` | Real (`WP-11`), replacing `AzureSearchStubProvider`'s hardcoded results |
| AI Runtime | `RTA-001 §13`, full Request/Agent Execution Lifecycle, Reasoning Contract | Specified in exhaustive detail; implemented only for the `C-093` slice `WP-11` built |
| Multi-Agent Orchestration | `agent_registry` (11 types), 5 execution strategies (Sequential/Parallel/Hybrid/DynamicGraph/Adaptive), `RTA-001 §13.6d/e` | Architecturally complete, zero code (`SE-027`, confirmed Not Applicable to `WP-11`'s own scope) |
| Multi-LLM Routing | `reasoning_engine_registry`, vendor-neutral Reasoning Contract (`RTA-001 §13.9b/c`) | Specified; no default model named at architecture layer |
| Ranking | — | **Explicitly unresolved.** `EIA-001 Vol. II §20.4`: *"Pending Canonical Binding — the mechanism by which a Search Result is ranked or ordered for relevance is not yet evidenced anywhere in the repository."* `RTA-001 §13.7` does not, on direct inspection, contain reranking logic despite one cross-reference elsewhere claiming it does |
| Confidence | `confidence_scoring_registry` (0–100, five bands) | Specified; `WP-11`'s own live confidence remains hardcoded pending a real model |
| Explainability | `SD-001 LAW-26`, `SD-002-016` | Owned twice over; zero UI implementation anywhere |

## 4. Data Sources

`EIA-001 Vol. II Ch. 5`'s own constitutional taxonomy is deliberately abstract — seven categories only (**Systems of Record, Documents, Conversations, People, External Feeds, Memory Feedback, Machine-Generated Sources**), naming *"categories, not technologies."* The physical enumeration lives one layer down, in `discovery_provider_registry.provider_type` (AMD-013, `Master_Technical_Architecture.md` lines 3244–3252) — roughly thirty concrete sources across three categories:

- **ENTERPRISE:** uploaded documents, SharePoint, OneDrive, Google Drive, Teams, Slack, Confluence, Jira, SAP, Oracle, Salesforce, ServiceNow, SQL databases, data warehouses, enterprise APIs, email, event streams, IoT, sensors, message queues.
- **EXTERNAL:** corporate websites, annual reports, sustainability/intelligence-foundation reports, regulatory filings, government databases, stock-exchange filings, standards bodies, public APIs, internet search, benchmark providers, industry databases.

This table is itself flagged, in its own governing amendment, as an open question requiring human review — connector *protocols* (authentication, pagination, rate limiting) for any of these thirty sources are explicitly deferred to a future implementation phase and confirmed still unbuilt by `WP-11`'s own IRA, which excluded "any Discovery Provider connection" as C-090's domain, not C-093's.

## 5. AI Architecture

`RTA-001 §13.6a`'s **Agent Execution Lifecycle** governs any request a single Inference stage cannot satisfy: Context Assembly → Planning → Task Decomposition → [Execution Capability Selection → Invocation → Result Evaluation, repeated per strategy] → Confidence Evaluation → Safety Validation → Human Review. Every model/reasoning-engine choice resolves through the vendor-neutral **Reasoning Contract** (`§13.9c`) — input assembled strictly per a declared JSON schema, output validated against another before any downstream use; no vendor SDK type ever crosses this boundary. RAG realization (`IMP-001 §13.3`) is a `RAGService` dependency-injected with `EmbeddingProvider`/`VectorProvider` interfaces — `WP-11`'s own `RAGEngine` is the literal, shipped instance, re-wired from a hardcoded stub to real, tenant-scoped `document_chunk_registry` retrieval. Hybrid and structured query remain thin: `retrieval_mode` supports `SEMANTIC`/`LEXICAL`/`HYBRID` as a configuration value, but no document anywhere — confirmed by direct search — defines a "structured query" concept distinct from these three, and `EIA-001 §20` states outright that *"no search algorithm, ranking mechanism, or index technology is prescribed."* Evidence generation and Confidence scoring are architecturally exhaustive (`Evidence Fusion`, seven scored dimensions; `Confidence`, five bands) and functionally real in `WP-11`'s own shipped path, short of the ranking and real-embedding gaps named above.

## 6. CDE Integration — the Core Differentiator

This is the one place this reconstruction must be exact rather than optimistic: **`EIA-001` (both volumes) never once mentions Canonical Data Elements or Business Questions.** The CDE/BQ meta-model is owned entirely by `SD-002 §§3–4` (`SD-002-021`–`033`) and realized physically in `Master_Technical_Architecture.md` AMD-004/005 — a parallel, independently-governed architecture that the Enterprise Search/Discovery documents never cross-reference. The two systems meet at exactly one schema-level joint, not a named architectural pattern: `unclassified_intelligence_registry`, which holds extracted facts carrying `probable_domain`/`probable_bq_id` until a Governance Manager resolves each one to `MAPPED_TO_EXISTING`, `NEW_CDE_CREATED`, `PROMOTED_CONVERGENCE`, or `DISCARDED` — the literal, if unglamorous, bridge from discovered signal to canonical fact. `Complete_Blueprint.md §5.0c`'s eight Bindings govern the business rule: a semantic match against an existing CDE is always attempted before a new one is created (`Binding 3`), Corporate-Scoped by default, promoted only on demonstrated convergence across the same fact appearing repeatedly. `customer_metric_registry.semantic_match_attempted_flag`/`convergence_count`/`promotion_decision` is this rule's own physical trace. **Disclosed gap, not invented bridge:** no document states that a `KnowledgeAsset` (`C-090`'s own output) *becomes* a row in `unclassified_intelligence_registry` — the two registries are adjacent in intent, never joined in text.

## 7. End-to-End Sequence (as documented, not as hypothesized)

```
 Enterprise Sources (discovery_provider_registry: ~30 provider_types)
        │
        ▼
 Discovery  (C-090 · Document Ingestion Service · EIA-001 §7.2)
        │
        ▼
 Extraction / Normalization  (IMP-001 §13.14 · RTA-001 §13.7a Multi-Modal Normalization)
        │
        ▼
 Evidence  (evidence_registry, document_chunk_registry · WP-11, real)
        │
        ├──────────────────────────────┐
        ▼                              ▼
 Knowledge Graph                 Vector Store
 (C-092 · Neo4j Aura ·           (vector_index_registry ·
  specified, zero code)           WP-11, real config / stub provider)
        │                              │
        └──────────────┬───────────────┘
                        ▼
              Enterprise Understanding
         (EIA-001 §12.1 — continuously formed)
                        │
         ╌╌╌╌╌╌╌╌╌╌╌╌╌╌ Interpretation ╌╌╌╌╌╌╌╌╌╌╌╌╌╌   ← disclosed gap, EIA-001 §7.2
                        │                                   (no implementation-ready spec)
                        ▼
              unclassified_intelligence_registry
         (probable_bq_id · resolution_status)  ← the one real CDE bridge
                        │
                        ▼
              CDE Engine (SD-002 §3, AMD-004)  ──▶  Business Question Engine (SD-002 §4)
                        │
                        ▼
              AI Runtime  (RTA-001 §13 · Reasoning Contract · Ask User Gate)
                        │
                        ▼
              Recommendations  (CMD-001 §24.4, registered Business Object)
                        │
                        ▼
              Business Activities  (consumed via C-093/C-094 Access, never authored by them)
```

## 8. Repository Traceability

`EIA-001 Volume I` (§5.1.6, §7.2, §12.1–12.2, Ch. 8–9) · `EIA-001 Volume II` (Ch. 5–6 Source Taxonomy/Connectors, Ch. 20–22 Search/Retrieval/Lifecycle) · `RTA-001 §§13, 13.6a–13.15` · `Master_Technical_Architecture.md` AMD-004/005 (CDE), AMD-012 (Retrieval Service, LOCKED), AMD-013 (Discovery/Agent Orchestration), Part G (Discover-Explore-Correlate-Reason-Validate) · `CMD-001 §24` (Knowledge & AI Domain), `§23` (Connector Framework, generic) · `SD-002 §§3–4` (CDE/BQ), `LAW-26` · `SD-001` (§1.3, `LAW-26`) · `Complete_Blueprint.md §5.0c` (CDE Bindings), `§7` (IDAL) · `IMP-001 §§13.2–14` · `CAP-001` (`D-005`, `C-090`–`C-095`) · `WP-11_Enterprise_Search.md`, `IRA-011`, `CERT-WP-11`, `TECH-DEBT.md` (`TD-125`) · `ENTERPRISE-AI-ARCHITECTURE-AUDIT.md` (independent corroboration of every gap named above).

---

### Disclosed Gaps (not designed here)

Ranking/reranking algorithm (`EIA-001 §20.4`, Pending Canonical Binding) · Connector protocols for any of the ~30 named sources · The EIA-001-to-CDE bridge as a named pattern (only a schema-level join exists) · Interpretation (Enterprise Understanding → Enterprise Intelligence, `EIA-001 §7.2`) · Real embedding/vector-search provider credentials · ESG/financial-statement-specific parsing logic (only a terminology-substitution table exists, not a functional distinction).

*Reconstruction only — no architecture was invented, redesigned, or simplified in producing this document.*
