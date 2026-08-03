# IRA-011 — WP-11 Enterprise Search (C-093) — Implementation Readiness Assessment

**Document ID:** IRA-011
**Work Package:** WP-11
**Capability:** C-093 — Enterprise Search ("Discover enterprise information," `CAP-001`, Active, D-005)
**Governing Specification:** No dedicated `PE-001-C093` capability specification exists (confirmed by direct search, `docs/Product/PE-001/capabilities/` contains specifications through C-040 only — same absence `WP-11_Enterprise_Search.md §14` already disclosed). This IRA is grounded directly in `EIA-001 Volume I §5.1.6/§6.3/§8/§9` (Enterprise Intelligence meta-model — Access Pattern discipline, Enterprise Context scoping) and `Master_Technical_Architecture.md` AMD-012 (`vector_index_registry`, `document_chunk_registry`, `evidence_registry` — LOCKED physical schema), mirroring `IRA-010`'s own precedent of grounding a Gap Analysis in Locked/Active constitutional text when no dedicated capability docx exists.
**Status:** DRAFTED — Plan A (BA-01/02/03)/Plan B pending Repository Owner acceptance and a separate implementation authorization; the AIService Authentication Bootstrap platform prerequisite (§4.4/§14) is separately authorized (Repository Owner Instruction "Platform Prerequisites," 2026-08-03) and **COMPLETE**. **No Business Activity code, API, or architecture change is authorized by this document.**
**Prepared By:** Engineering Governance session (Claude Code), under Repository Owner Instruction "Release C Initiation & WP-11 Planning"
**Date:** 2026-08-03

---

## 1. Purpose

Determines whether, and at what scope, WP-11 (chartered `WP-11_Enterprise_Search.md`) may proceed to implementation, per `CLAUDE.md §19`/`§20`/`§21`. Per the charter's own §3, this IRA is the authority that finalizes Business Activity numbering, contracts, and any splitting/merging the charter itself deliberately left open. This IRA produces **two** implementation plans — **Plan A** (Business Capability Implementation, §5) and **Plan B** (Enterprise Experience Implementation, §7) — neither of which designs screens or writes code; both are planning determinations only. This IRA also performs the three pre-Business-Activity reviews `CLAUDE.md §21.3` requires: Strategic Enhancement Review (§4a), Historical Screen Review (§4b), Executive Cognition Review (§4c).

**This IRA's central finding, stated up front:** the charter's own evidence (§0 of `WP-11_Enterprise_Search.md`) is independently re-confirmed accurate in every material respect this pass checked, including the critical-path dependency the charter's own §5 did not explicitly re-verify — `R4` (Release A2, "the single highest-leverage decision in the programme" per `ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md §8`) is in fact **already resolved** (`AMD-015` CHANGELOG, `Master_Technical_Architecture.md` lines 630–682, confirmed by Repository Owner decision per `IMP-REPORT-RELEASE-A2_Governance.md`, 2026-08-01) — R17/WP-11's own stated critical-path gate ("do not start R17 before [R3 and R4 close]") is therefore satisfied, not merely assumed. Independent of that confirmation, this pass found **three additional, previously-undisclosed gaps** that materially affect scope: (a) `Backend/Services/AIService` has **zero authentication anywhere** — every existing router trusts an unverified client-supplied header, a materially larger version of the exact defect class `CERT-WP-10` Finding B-1 and `VV-AUDIT-WP-09` Finding 2 already found and remediated elsewhere in this repository; (b) `AIService` has **no Alembic migration chain at all** (contradicting the charter's own §9 Technical Assumption that one exists to extend); (c) `document_chunk_registry`'s own `evidence_id` column is a `NOT NULL` foreign key to `evidence_registry`, which has **zero implementation anywhere in this repository** — the charter's own two Business Activities (index configuration + query) have no way to produce real, queryable content without a third, narrowly-scoped content-registration path. See §4 for full reasoning; §5 resolves (c) by adding **BA-03**. (b) is scoped as a mandatory, non-deferrable cross-cutting prerequisite within BA-01, per `CLAUDE.md §19.8.5`. **(a) is corrected below** — a subsequent Repository Owner planning-validation pass (2026-08-03, "Final planning validation before IRA-011 acceptance") determined the AIService authentication gap is a **mandatory platform prerequisite gating BA-01/02/03, not part of WP-11's own Business Capability scope** — see §4.4's own correction for the full evidentiary basis. This does not change the underlying technical finding or its non-deferrable status, only where it is tracked.

---

## 2. Governing Documents Reviewed

- `CAP-001_Enterprise_Capability_Registry.md` (C-093 registration, verbatim: "Discover enterprise information," Active, D-005) — full text of the D-005 row block read directly.
- `EIA-001_Volume_I_Enterprise_Intelligence_Foundations.docx` (`word/document.xml`, extracted and read directly — no dedicated PE-001-C093 exists, so this is the only constitutional-tier document naming C-093's own behavioral constraints). Key findings used below: §5.1.6 ("Search and Conversation Are Access Patterns, Not Sources" — C-093 may never become an independent source of Enterprise Understanding); the Access layer definition (Chapter 8: "C-093 Enterprise Search... Expose Enterprise Understanding, scoped through Enterprise Context, for direct query and AI-mediated interaction"); the "Query Surface" term (owning capability C-093: "the conceptual means by which Enterprise Understanding, scoped by Enterprise Context, is made discoverable and retrievable"); the explicit statement that "EIA-001 does not define its own authorization model" for C-090–C-095 (Chapter 9) — authorization is inherited, not invented, by whichever capability actually resolves Enterprise Context; and the document's own explicit Out of Scope for this volume ("Enterprise Search internals... RAG implementation, vector databases, embeddings... are reserved for later EIA-001 volumes" — confirming no later, more specific EIA-001 volume exists yet either, per direct directory listing of `docs/Product/Architecture/EIA-001/` showing only Volumes I and II, II being "Enterprise Intelligence Fabric," not Search-specific).
- `Master_Technical_Architecture.md` — AMD-012 physical schema (`evidence_registry` lines 2319–2335, `document_chunk_registry` lines 3185–3201, `vector_index_registry` lines 3203–3218, `ai_tool_registry` lines 3220–3236), RLS policies (lines 4508–4514), and the AMD-015 CHANGELOG (lines 629–682, `reasoning_engine_registry` confirmed canonical over `llm_prompt_registry`, closing R4) — all read directly.
- `WP-11_Enterprise_Search.md` (charter) — full text read directly; every evidentiary claim in its §0 independently spot-checked against primary sources (below), not accepted on trust.
- `SER-001_Strategic_Enhancement_Register.md` (`SE-024` through `SE-027`, `SE-037`/`SE-038` — the D-005/WP-11 cluster).
- `HISTORICAL-SCREEN-REALIZATION-MATRIX.md` (`F1_Enterprise_Understanding_Center.html`, `I1_Intelligence_Center.html` — both EVOLVE CONCEPT, C-090/C-092/C-093, correctly excluded from this charter's own scope per its §0).
- `TECH-DEBT.md` (`TD-109` — `rag_configs`/`vector_index_registry` reconciliation, execution assigned to WP-11; `TD-111` — no production `TierResolver` exists for any tier, cross-referenced for BA-02's own authorization posture).
- `ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md` (`R17`, `R27`, `R28`, and the R3/R4 critical-path chain, §8/§9) and `RELEASE-A2-AI-CONFIGURATION-GOVERNANCE-REVIEW.md` (R4's own resolution direction, independently re-confirmed against the now-applied `AMD-015` CHANGELOG).
- Existing repository source, read directly: `Backend/Services/AIService/` in full — `main.py`, `middleware/tenant.py`, `models/database.py`, `models/rag.py`, `services/rag_engine.py`, `services/vector_provider.py`, `services/embedding_provider.py`, `routers/extraction.py` (representative of the existing router pattern); `Backend/Services/AuthService/dependencies.py` (`get_current_claims`, `require_platform_admin`, `require_matching_tenant_or_platform_admin` — the reuse target for BA-01/02/03's own authentication, per §4 below); `Backend/Shared/Security/jwt_manager.py` and `TECH-DEBT.md TD-107` (confirms the shared JWT manager is currently unreachable/broken, not a viable direct-reuse target without a separate fix); `source/frontend/src/config/admin-navigation.ts` (confirms the existing `enterprise-intelligence` nav slot, currently a `PlaceholderPage`).

---

## 3. Existing Asset Discovery (Reuse Before Creating, `CLAUDE.md §19.2`)

| Asset | Location | Status |
|---|---|---|
| `RAGEngine.build_context()` | `Backend/Services/AIService/services/rag_engine.py` | Exists. Real orchestration shape (embed → search → assemble evidence-cited references) already matches C-093's own query pattern exactly. Reused, not reimplemented, by BA-02. |
| `EmbeddingProvider` / `VectorProvider` abstractions | `Backend/Services/AIService/services/embedding_provider.py` / `vector_provider.py` | Exist as clean ABCs with stub concrete implementations (`AzureEmbeddingStubProvider`, `AzureSearchStubProvider`). Reused as the abstraction layer; concrete providers remain stubbed (charter §4, unchanged — no credentials available). |
| `vector_index_registry` / `document_chunk_registry` / `evidence_registry` | `Master_Technical_Architecture.md` AMD-012 | Fully specified, LOCKED, canonical. **Zero implementation anywhere** — no SQLAlchemy model, no Alembic migration, no service, confirmed by repository-wide search. This is the real target Plan A builds against. |
| `rag_configs` (`RAGConfigModel`) | `Backend/Services/AIService/models/rag.py` | Exists, non-canonical (`TD-109`). Migrated away from, not extended, by BA-01. |
| AIService authentication | — | **NOT FOUND anywhere.** Every existing router (`extraction.py`, and by the same pattern `validation.py`/`scoring.py`) reads `request.state.tenant_id` — set by `TenantHeaderMiddleware` from a raw, unverified client-supplied header — with no JWT decoding, no `Authorization` header requirement, no claims verification of any kind. `jwt_secret_key`/`jwt_algorithm` are declared in `Config/settings.py` but never consumed anywhere in the service. Confirmed by repository-wide search for `get_current_claims`/`jwt`/`decode` usage in `AIService`'s own router/service code — zero hits beyond the unused settings declaration. |
| AIService Alembic chain | — | **NOT FOUND anywhere.** No `alembic.ini`, no `alembic/` directory, confirmed by direct listing — contradicts the charter's own §9 Technical Assumption ("added to `AIService`'s own Alembic migration chain, mirroring `rag_configs`' current (unmigrated) table"), which incorrectly presupposed a chain already exists. `models/database.py`'s own `init_db()` uses `Base.metadata.create_all()` — a dev-only, non-versioned schema bootstrap, the same class of gap `AuthService` itself did not have even at WP-00. |
| `AuthService/dependencies.py` (`get_current_claims`, `require_platform_admin`, `require_matching_tenant_or_platform_admin`) | `Backend/Services/AuthService/dependencies.py` | Exists, real, already battle-tested (used by every WP-01–WP-10 endpoint; `require_matching_tenant_or_platform_admin` specifically is `CERT-WP-10`'s own Finding B-1 remediation). **Not directly importable by `AIService`** — a separate FastAPI process/service, no cross-service Python import exists or is architecturally intended (`CLAUDE.md §8`: services communicate through APIs or events, never shared code coupling across service boundaries for business logic — though a shared *security primitive* is a distinct question from shared *business logic*, addressed in §4 below). |
| `Backend/Shared/Security/jwt_manager.py` | `Backend/Shared` (platform framework) | Exists, but **currently broken** — `TD-107`: an `ImportError` (`MissingRequiredValueError` does not exist where imported from), unreachable, unfixed, disclosed as Open/Medium. Not a currently-viable direct-reuse target without first resolving `TD-107` (out of this charter's own scope unless separately bundled — see §4). |
| `source/frontend/src/config/admin-navigation.ts` | `source/frontend/src/config/` | Exists. An `enterprise-intelligence` nav slot/route (`/platform-admin/enterprise-intelligence`) already exists, currently rendering a `PlaceholderPage` — the same "existing nav slot, currently placeholder" precedent `IRA-010 §7` found for `system-configuration`. |

**Conclusion:** per `CLAUDE.md §2`/`§19.5` (Reuse → Configure → Extend → Compose → Create), Plan A reuses `RAGEngine` and the provider abstractions wholesale, builds the canonical schema fresh (zero prior implementation, as anticipated by the charter), and must additionally build — as prerequisite, in-scope, non-deferrable cross-cutting work, not new architecture — an Alembic chain and a real authentication dependency for `AIService`, both of which extend an already-established platform pattern (`AuthService`'s own precedent) to a service that has simply never adopted it. Plan B extends the existing `enterprise-intelligence` nav slot rather than inventing a new one.

---

## 4. Gap Analysis

### 4a. Strategic Enhancement Review (`CLAUDE.md §21.3`)

Per `SER-001`, every enhancement relevant to C-093/WP-11 is classified below:

| SE | Enhancement | Disposition for WP-11 |
|---|---|---|
| `SE-024` | WP-11 umbrella (C-090 or C-093) | **Partially Implemented** — resolved to C-093 by the charter (§0); this IRA authorizes Plan A/B implementation; remains Deferred in `SER-001`'s own status field until WP-11 actually closes, per this register's own convention of not marking a status Implemented ahead of certification |
| `SE-025` | Knowledge Graph real build (C-092, Neo4j Aura) | **Not Applicable to this Work Package** — confirmed excluded by the charter §0/§4 (zero Neo4j infrastructure exists; hard external-dependency gap distinct in kind from C-093's own stubbed-provider gap); remains Deferred in `SER-001` |
| `SE-026` | Semantic Search real implementation | **Partially Implemented** — this is C-093's own core deliverable; Plan A (§5) realizes the persistence/orchestration/tenant-scoping layers for real, the concrete embedding/vector-search *provider* remains stubbed (external credentials, disclosed, unchanged from charter §4) |
| `SE-027` | Multi-Agent orchestration build-out | **Not Applicable to this Work Package** — confirmed excluded by the charter §4 (`RAGEngine`'s own design has no agent-delegation dependency); remains Deferred |
| `SE-037` | C-094 AI Conversation Management charter | **Not Applicable** — explicitly gated behind WP-11's own successful closure, not itself in scope |
| `SE-038` | C-095 Enterprise Memory charter | **Not Applicable** — same gating, additionally contingent on an `ARCH-000 §7c` deferral-lift decision not before this IRA |

No `SER-001` item names a C-093-specific deliverable this Gap Analysis has not already accounted for.

### 4b. Historical Screen Review (`CLAUDE.md §21.3`)

`HISTORICAL-SCREEN-REALIZATION-MATRIX.md §1`/§2 names exactly two EVOLVE CONCEPT screens touching C-093's own domain: `F1_Enterprise_Understanding_Center.html` (owning capability C-090, not C-093) and `I1_Intelligence_Center.html` (C-090/091/093, a routing/triage hub, not a search-execution screen). **Neither maps to WP-11's own chartered scope** — `F1` is explicitly C-090-owned (excluded by the charter §0/§4) and `I1` is a governance/routing concept (confidence-gap triage, "Connect a system" flow) structurally distinct from C-093's own minimum-viable query/retrieve/cite loop this Work Package charters. Both remain available EVOLVE CONCEPTs for a future C-090 charter, per the charter's own §0 disclosure — unaffected, not resurrected, by this IRA. No historical screen concept exists for a plain search/query interface specifically; Plan B (§7) is therefore not constrained or informed by historical precedent, only by `DS-001`/`SD-001`/`PE-001` directly.

### 4c. Executive Cognition Review (`CLAUDE.md §21.3`)

Per `PRODUCT-MILESTONE-ROADMAP.md §3` (Milestone 2, "The Intelligent Enterprise"): WP-11 is explicitly named as the proving Work Package for the platform's first Enterprise Intelligence experience — "the first tangible experience of 'the system finds things for me.'" This is a genuine, if narrow, advance in Executive-facing cognition support (an Executive persona can ask a question and receive an evidence-cited answer, not merely browse an administered structure) — distinct from WP-10's own Discover-stage-only advance (`IRA-010 §4c`). No dedicated Executive screen is chartered by WP-11 itself (Plan B, §7, reuses/extends existing admin navigation and a narrow query surface); genuine Executive Cognition capability (C-094 AI Conversation Management) remains correctly gated behind this Work Package's own successful closure, per `EIA-001 Volume I`'s own layering (Access → Converse) and the Implementation Programme's own critical-path statement (R23/R24 depend on R17 succeeding).

### 4.1 Establish Enterprise Search Index Configuration — **IN SCOPE**

`vector_index_registry` (AMD-012, LOCKED) is fully specified: `index_name`, `embedding_model`, `embedding_dimension`, `retrieval_mode` (SEMANTIC/LEXICAL/HYBRID), `refresh_cadence`, `active_flag`, `organization_id` (nullable — platform-wide vs. tenant-dedicated). A real, buildable, already-specified target with zero existing conflicting implementation (only the non-canonical `rag_configs` sibling, migrated away from per `TD-109`).

**Disposition:** in scope, buildable now — realized as **BA-01**.

### 4.2 Register Enterprise Search Content — **IN SCOPE (new, added by this IRA)**

The charter's own two-Business-Activity shape (index configuration + query) has no path to produce real, queryable data: `document_chunk_registry.evidence_id` is `NOT NULL REFERENCES evidence_registry(evidence_id)` (AMD-012), and `evidence_registry` has **zero implementation anywhere in this repository** — no model, no migration, no service, confirmed by repository-wide search. Building a full document-ingestion/chunking pipeline (file upload, discovery providers, chunking algorithm) is correctly out of scope — that is C-090 Enterprise Discovery's own domain, explicitly excluded by the charter §0/§4, and inventing one here would exceed WP-11's own chartered boundary. But a **narrow, minimum-viable content-registration path** — write one `evidence_registry` row plus one or more `document_chunk_registry` rows for a caller-supplied text passage, embedding it via the already-reused `EmbeddingProvider` abstraction — requires no new architecture (both tables are already LOCKED and fully specified; no discovery-provider, chunking-algorithm, or file-format decision is invented) and is the smallest addition that makes BA-02's own query path genuinely real rather than permanently empty. This mirrors the `CLAUDE.md §19.5` worked example's own discipline (WP-04 BA-08, Option A): the smallest scope that satisfies the governing capability's own Produced Context without inventing a mechanism nowhere documented.

**Disposition:** in scope, narrowly — realized as **BA-03** (new). Excluded: any discovery provider, file upload/parsing, or chunking-algorithm decision — content registration accepts pre-extracted text only, mirroring `evidence_registry.file_reference`'s own column being a reference, not a storage/parsing mechanism.

### 4.3 Execute Enterprise Search — **IN SCOPE**

`RAGEngine.build_context()` already implements the exact orchestration shape required: embed query → search index → assemble evidence-cited references. Reused as-is; only its `index_name: str, VectorProvider` inputs are re-wired to resolve from BA-01's own persisted `vector_index_registry` configuration and to query real (once BA-03 has written any) `document_chunk_registry` rows, rather than the current hardcoded fake results.

**Disposition:** in scope, buildable now — realized as **BA-02**.

### 4.4 AIService Authentication — **IN SCOPE, mandatory, non-deferrable prerequisite**

Per `CLAUDE.md §19.8.5`, a defect that "weakens a security or tenant-isolation boundary, even if no exploit is currently known" cannot be deferred as Technical Debt. `AIService`'s current state — zero authentication, a tenant identity taken verbatim from an unverified client-supplied header — is precisely this class of defect, more severe than `CERT-WP-10` Finding B-1 (which at least required an authenticated caller before trusting an unverified header) or `VV-AUDIT-WP-09` Finding 2 (same shape). Shipping any new WP-11 endpoint into this service without first closing this gap would knowingly build new functionality on top of an already-disclosed, `§19.8.5`-class boundary weakness — the same failure mode `METH-002`/`ADR-017` exist to prevent.

**Resolution path (Reuse → Extend, not invent):** `AIService`'s own `Config/settings.py` already declares `jwt_secret_key`/`jwt_algorithm`/`jwt_expiry_minutes`, unused. The correct fix is a local `get_current_claims`-equivalent dependency in `AIService`, decoding and verifying a Bearer token against the same secret/algorithm/claims shape `AuthService`'s own `decode_access_token`/`get_current_claims` already use (`organization_id`, `person_id`, `role_code`) — the same authentication *model* (`URA-001` Identity/Access), not a new one, simply wired into a service that has never adopted it. **`Backend/Shared/Security/jwt_manager.py` is the architecturally cleaner reuse target but is currently broken (`TD-107`)** — resolving `TD-107` first and then consuming the Shared `JWTManager` avoids duplicating `AuthService`'s own local decode logic a second time (`CLAUDE.md §15.3`, "one implementation"), and `TD-107`'s own registered Resolution Criteria is Small effort. **Recommendation: bundle the `TD-107` fix into WP-11's own implementation** (closing it as part of this Work Package rather than deferring a third time) and consume `Backend.Shared.Security.JWTManager` from `AIService`, rather than duplicating `AuthService`'s local pattern — a Repository Owner confirmation of this specific bundling decision is the one open item this section surfaces, not a full STOP (the fix itself requires no new architecture, per `TD-107`'s own already-registered, already-scoped Resolution Criteria).

**Disposition (original):** in scope, mandatory, realized as a cross-cutting prerequisite within **BA-01**'s own implementation (the first WP-11 endpoint built), applied identically to BA-02/BA-03.

**Correction — Repository Owner Instruction "Final planning validation before IRA-011 acceptance" (2026-08-03):** the disposition above is corrected. Repository evidence establishes this is a **mandatory platform prerequisite, not part of WP-11's own Business Capability scope** — completed and verified before BA-01/02/03 implementation begins, not folded into BA-01 as Business Activity work. Evidence:

1. **`CMD-001 §26.3a` Step 1 (Independent Identity) already fails** for this construct, as this section's own original analysis found ("neither has independent business identity of its own," §4.7). A construct that cannot pass the eligibility test to be recognized as a Business Object/Business Activity of C-093 cannot simultaneously be silently absorbed into an adjacent Business Activity's own scope — the correct disposition is to recognize it as sitting outside the Business Activity layer entirely, not to fold it into the nearest one.
2. **`WP-00`/`WP-00A` precedent** (`WPR-001 §2`): cross-cutting, service-wide infrastructure with no owning `PE-001` capability is tracked as Platform work — "WP-00 | — (Platform Bootstrap; no PE-001 capability)" — never folded into a Business Capability's own Business Activity. Real authentication for a whole service is the same shape: it serves every present and future endpoint in `AIService`, not C-093 specifically.
3. **`WP-RTA-001` precedent** (`WPR-001 §2a`): "Runtime Work Packages are categorically distinct from the Business Capability roadmap... own no Business Object, and perform no Business Activity of any capability... exist to be consumed by one or more Business Capability Work Packages, never the reverse." `AIService` authentication is structurally identical in kind — infrastructure a Business Capability Work Package (WP-11) depends on and consumes, not infrastructure WP-11's own capability work produces or owns.
4. **The defect pre-dates and is broader than WP-11's own chartered scope.** `extraction.py`, `validation.py`, and `scoring.py` — none chartered by WP-11, none touching C-093 — already exhibit the identical zero-authentication gap (§3). This confirms the defect is not created by, or scoped to, C-093's own Business Activities; it is a pre-existing, service-wide platform gap WP-11 happens to be the first Work Package to notice, not one WP-11's own capability work produces.
5. **`TD-106`/`TD-107` (the adjacent, already-registered `Backend/Shared/Security` defects) are both owned by "Backend/Shared (Platform)"** in `TECH-DEBT.md`, not attributed to any capability — confirming this repository's own existing taxonomy already classifies JWT/security-infrastructure defects as Platform-owned, not Business-Capability-owned.

**Revised disposition:** mandatory platform prerequisite. Must be completed and independently verified before BA-01, BA-02, or BA-03 implementation begins. Does **not** expand C-093 Enterprise Search's own chartered Business Capability scope (`WP-11_Enterprise_Search.md §2`, unchanged) and is **not** assigned to, or traceable as, any WP-11 Business Activity. Tracked as a prerequisite completion gate on this IRA's own Entry Criteria for Business Activity implementation (§11) — the same "close the reconciliation before the dependent unit of work begins" discipline §1 already applies to `R3`/`R4` gating WP-11's own chartering, applied one layer down, from Release-level to Business-Activity-level. The resolution path itself (§ above — reuse the same `URA-001` authentication model already used by `AuthService`, recommend bundling the `TD-107` fix) is unchanged; only its tracking layer changes.

### 4.5 AIService Alembic Chain — **IN SCOPE, prerequisite**

No Alembic chain exists anywhere in `AIService` (§3). `vector_index_registry`/`document_chunk_registry`/`evidence_registry` cannot be introduced as real, versioned, production-parity tables via `Base.metadata.create_all()` alone — the same discipline `CLAUDE.md §21.4`'s own harness/fixture production-parity checklist exists to enforce (a dev-only `create_all()` bootstrap does not enforce the same FK/constraint behavior a real migrated schema does). Bootstrapping Alembic for `AIService`, mirroring `AuthService`'s own established `alembic.ini`/`env.py`/`versions/` pattern, is Extend-class work (an already-proven platform pattern applied to a second service), not new architecture.

**Disposition:** in scope, mandatory, realized as a cross-cutting prerequisite within **BA-01**.

### 4.6 Real `EmbeddingProvider`/`VectorProvider` implementation — **EXCLUDED** (unchanged from charter)

Confirmed unchanged: no external AI/vector-service credentials exist anywhere in this development environment (`Config/platform-config.yaml`, `AIService/Config/settings.py` — searched directly). The abstraction interfaces, real persistence, real tenant scoping, and real orchestration become genuinely real (§4.1–4.3); the concrete provider remains the disclosed, deferred external-integration point.

**Disposition:** excluded, per charter §4 — unchanged.

### 4.7 Summary

| Item | Disposition | Realization |
|---|---|---|
| Establish Search Index Configuration | In scope | BA-01 |
| Register Enterprise Search Content (new) | In scope, narrow | BA-03 |
| Execute Enterprise Search | In scope | BA-02 |
| AIService real authentication | **Mandatory platform prerequisite — NOT WP-11 Business Capability scope** (corrected §4.4) | Completed and verified **before** BA-01/02/03 begin; not a Business Activity, not traceable to any BA |
| AIService Alembic chain | In scope, mandatory prerequisite | Within BA-01 |
| Real embedding/vector-search provider | Excluded — no credentials | None this WP |
| C-090 Enterprise Discovery / ingestion pipeline | Excluded — different capability | None this WP |
| C-092 Knowledge Graph (Neo4j) | Excluded — zero infrastructure | None this WP |

**Three Business Activities, not two** — this IRA's own determination, exercised under the charter's own §3 delegation ("Final Business Activity numbering... remain IRA-011's own determination"). One cross-cutting infrastructure prerequisite (the Alembic chain) is mandatory, non-deferrable, and folded into BA-01 (no independent business identity of its own — `CMD-001 §26.3a` Step 1 would fail for it as a standalone candidate, but it is genuinely produced as part of BA-01's own first migration). **AIService authentication is a distinct case, corrected by §4.4**: it is not folded into BA-01 — it is a mandatory platform prerequisite completed *before* any Business Activity begins, tracked outside the Business Activity layer entirely, per the evidence in §4.4's own correction.

---

## 5. PLAN A — Business Capability Implementation

### Prerequisite (must complete and be independently verified before BA-01/02/03 begin — not a Business Activity, §4.4)

**AIService Authentication Bootstrap.** Wires a real `get_current_claims`-equivalent JWT verification dependency into `AIService`, per §4.4's own resolution path — reusing the already-declared `jwt_secret_key`/`jwt_algorithm` settings and the same claims shape (`organization_id`, `person_id`, `role_code`) `AuthService` already verifies, recommended (subject to Repository Owner confirmation) by first closing `TD-107` and consuming `Backend.Shared.Security.JWTManager` rather than duplicating `AuthService`'s local decode logic a second time. This is infrastructure `AIService`'s own pre-existing endpoints (`extraction.py`/`validation.py`/`scoring.py`) also lack and equally need — it is not produced by, or scoped to, C-093's own Business Activities (§4.4's own correction), so it carries no WP-11 Business Activity number and is not itself part of C-093 Enterprise Search's chartered scope (`WP-11_Enterprise_Search.md §2`, unchanged). BA-01/02/03 each *consume* this prerequisite (their own API gating depends on it existing) but none of them *build* it.

### BA-01 — Establish Enterprise Search Index Configuration

- **Domain Model:** `VectorIndexRegistry` (SQLAlchemy model mapping to the canonical `vector_index_registry` table, AMD-012 — no new columns, no deviation from the LOCKED schema).
- **Service:** Creates/updates a tenant-scoped (or platform-wide, `organization_id IS NULL`) index configuration record — index name, embedding model, embedding dimension, retrieval mode, refresh cadence.
- **API:** `POST /search/index-configurations` (establish); `GET /search/index-configurations` (list caller's own tenant + platform-wide rows). Gated by the prerequisite's own `get_current_claims`-equivalent dependency (consumed, not built, by this BA — see above); write path additionally gated by an appropriately-scoped authorization dependency (exact persona — `PLATFORM_ADMIN`-only vs. a narrower tenant-admin persona — determined at implementation time, mirroring `IRA-010 §5`'s own identical deferral, since `PE-001-C093` names no persona at all).
- **Cross-cutting (this BA only, applies platform-wide to BA-02/BA-03):** Alembic chain bootstrapped for `AIService` (§4.5) — the one prerequisite genuinely produced as part of this BA's own first migration, distinct from the authentication prerequisite above, which this BA only consumes.
- **Testing:** Unit (record created/updated correctly; tenant-scoping honored) + API (200/201; 401 unauthenticated — now meaningful, where it was previously unreachable; 403 boundary per the chosen persona gate) + the Mandatory Tenant-Isolation Test Checklist (§10).

### BA-02 — Execute Enterprise Search

- **Service:** Resolves the caller's own applicable `vector_index_registry` row (by name or by default tenant-scoped index), embeds the query text via `EmbeddingProvider`, searches `document_chunk_registry`-backed content via `VectorProvider`, returns evidence-cited results (source, score, locator) — directly reusing `RAGEngine.build_context()`'s own orchestration, re-wired to real persisted configuration instead of a hardcoded index name.
- **API:** `POST /search/query` — request: query text, optional index name, top-k; response: ranked, evidence-cited results (or an honest "no matching references found" empty state — `RAGEngine`'s own existing behavior, reused).
- **Testing:** Unit (query embeds, searches the caller's own tenant-scoped index only, assembles citations correctly) + API (200 with results; 200 with empty-state message when no content registered; 401/403 boundary) + the Mandatory Tenant-Isolation Test Checklist (§10) — a caller in Organization A must never retrieve Organization B's own tenant-dedicated index content.

### BA-03 — Register Enterprise Search Content (new, per §4.2)

- **Domain Model:** `EvidenceRegistry` and `DocumentChunkRegistry` (SQLAlchemy models mapping to the canonical `evidence_registry`/`document_chunk_registry` tables, AMD-012 — no new columns).
- **Service:** Accepts pre-extracted text plus minimal evidence metadata (`evidence_type`, `evidence_source`, `file_reference` as a caller-supplied locator string, not a file upload); writes one `evidence_registry` row; chunks the text (a single, deliberately simple fixed-size chunking pass — not a configurable chunking strategy, per AMD-012's own comment that "chunking strategy itself... is intentionally not specified by this table"); embeds each chunk via `EmbeddingProvider`; writes `document_chunk_registry` rows referencing the caller's own `vector_index_registry` row (BA-01) and the new `evidence_registry` row.
- **API:** `POST /search/content` — request: text, evidence metadata, target index name; response: the created evidence + chunk count. Gated identically to BA-01's write path.
- **Explicitly excluded:** file upload/parsing, any Discovery Provider connection (`discovery_provider_registry`, AMD-013 — C-090's own domain), configurable chunking algorithms. This endpoint accepts text the caller already has, nothing more — the narrowest slice that makes BA-02 genuinely demonstrable, per §4.2.
- **Testing:** Unit (evidence + chunk rows created correctly, correctly linked to the caller's own index) + API (200/201; 401/403 boundary) + the Mandatory Tenant-Isolation Test Checklist (§10) — content registered under Organization A's own tenant-dedicated index must never be retrievable through Organization B's own BA-02 query.

### Cross-cutting

- **Migration:** one new Alembic chain bootstrap (`AIService`, first-ever) plus one migration introducing `evidence_registry`, `document_chunk_registry`, `vector_index_registry` (AMD-012, LOCKED shape) and retiring `rag_configs` from further use (`TD-109` — table dropped or left in place per that entry's own disclosed "no runtime data affected" finding; exact mechanics determined at implementation time).
- **`middleware/tenant.py`:** the existing raw-header tenant mechanism is superseded, for the three new WP-11 endpoints, by the real `organization_id` JWT claim (§4.4) — not removed for the service's own pre-existing endpoints (`extraction.py`/`validation.py`/`scoring.py`), which are unaffected by this Work Package, per `CLAUDE.md §20.1`'s own "does not reopen" precedent applied here to unrelated, already-shipped endpoints outside this charter's scope.

---

## 6. Business Object Eligibility Analysis (`CMD-001 §26.3a`)

**Not required.** `vector_index_registry`, `document_chunk_registry`, and `evidence_registry` are already canonical, LOCKED constructs registered directly in `Master_Technical_Architecture.md` AMD-012 — the eligibility test governs *new* candidate constructs discovered during implementation (`CMD-001 §26.3a`'s own purpose), not tables the physical architecture has already specified and locked. No new construct is introduced by BA-01/02/03 beyond these three already-registered tables. This mirrors the disposition every other Work Package building directly against an already-LOCKED table has reached (e.g., `WP-08`'s reuse of already-canonical Identity/Access constructs) — distinct from `WP-10`'s own `CFG-000001` registration, which was required precisely because no canonical Configuration table existed anywhere before that Work Package.

---

## 7. PLAN B — Enterprise Experience Implementation

Derived only from `PE-001`, `SD-001`, `DS-001`, `IMP-001 §10` — per `CLAUDE.md §20.3`, this plan identifies what is built; it does not itself design a screen.

- **What the user sees:** an admin-facing screen to establish a search index and register content (BA-01/BA-03), and a query surface to ask a question and see evidence-cited results (BA-02).
- **What the Executive sees:** the first real "ask a question, get a cited answer" experience the platform has ever offered (§4c) — narrow (only content explicitly registered through BA-03 is searchable), disclosed as narrow, not oversold as general-purpose enterprise search.
- **Screens realized:** the existing `enterprise-intelligence` nav slot (`/platform-admin/enterprise-intelligence`, currently a `PlaceholderPage`, confirmed by direct read of `admin-navigation.ts`) is reused for BA-01/BA-03's own admin establish/register UI — mirroring `IRA-010 §7`'s own precedent of replacing an existing placeholder rather than inventing a new nav item. **BA-02's own query surface has no existing nav slot** — `enterprise-intelligence` is administration-scoped ("Enterprise Intelligence configuration"), not a persona-facing query tool; a new, minimal nav entry or an in-context query affordance is required. The exact placement (a new top-level nav item vs. a Workspace-scoped surface) is **not decided by this IRA** — determined at implementation time against `DS-001`'s own navigation-pattern guidance, consistent with `CLAUDE.md §19.1`'s prohibition on inventing a navigation pattern `DS-001` does not already define.
- **Design System components used:** `Form`, `Card`, `Button`, `Spinner`, `Menu` (all existing, reused, same set `IRA-010 §7` already used for a structurally similar establish/resolve UI pair).
- **States implemented (`CLAUDE.md §20.6`):** loading, empty (no content registered yet under the resolved index — an honest, disclosed empty state, not a fabricated result), validation (BA-01/BA-03 establish forms), error, confirmation.

---

## 8. Readiness Decision

**READY**, at the scope determined in §4.7/§5: **C-093's own chartered Business Capability scope is exactly two Business Activities of index/query and one of content registration — BA-01 (Establish Enterprise Search Index Configuration, including the Alembic-chain prerequisite it genuinely produces), BA-02 (Execute Enterprise Search), BA-03 (Register Enterprise Search Content, new — the minimum addition that makes BA-02 genuinely real rather than permanently empty).** The AIService Authentication Bootstrap (§4.4, §5) is **not** a fourth item within this scope — it is a mandatory platform prerequisite gating the start of BA-01/02/03 implementation, tracked outside C-093's own Business Capability scope entirely, per §4.4's own correction. Real embedding/vector-search provider, C-090 Enterprise Discovery, and C-092 Knowledge Graph Management excluded — each for a distinct, disclosed, evidence-grounded reason, not a single blanket exclusion.

No constitutional blocker for the scope that IS in bounds. The critical-path dependency the Implementation Programme itself names (R3 + R4 must close before R17/WP-11 begins) is independently confirmed satisfied (§1). No new canonical Business Object (§6). No new architectural component beyond the service/router files Plan A names and their frontend counterparts in Plan B — every piece either already exists (`RAGEngine`, the provider abstractions, `AuthService`'s own JWT pattern to extend) or is already LOCKED, specified architecture (`vector_index_registry`/`document_chunk_registry`/`evidence_registry`) with zero prior implementation to conflict with.

**Two items require explicit Repository Owner confirmation before implementation begins:**
1. Whether to bundle the `TD-107` fix into the authentication prerequisite (recommended, §4.4) or duplicate `AuthService`'s local JWT-decode logic into `AIService` instead. Both are architecturally acceptable; the choice affects only where the fix lives.
2. Acceptance of the authentication prerequisite's own reclassification (§4.4) — a platform prerequisite gating BA-01/02/03, not a WP-11 Business Activity — confirming this does not require a separate charter, IRA, or Work Package number of its own (this IRA's own recommendation: it does not, mirroring how `R3`/`R4`-class reconciliation work gates a Work Package without itself being one).

---

## 9. Anticipated Technical Debt

- **TD-candidate-A** (Medium): the exact write-path persona gate for BA-01/BA-03 (`PLATFORM_ADMIN`-only vs. a narrower persona) is undetermined — no `PE-001-C093` exists to name one, same root cause as `TD-021`-class entries across every prior Work Package.
- **TD-candidate-B** (Low): BA-03's own fixed-size chunking pass is a deliberately simple placeholder for a real chunking strategy — disclosed narrow scope (§4.2), not a defect, but worth tracking once a real ingestion pipeline (C-090) exists.
- **TD-candidate-C** (Low, resolves `TD-109`): once BA-01 migrates `AIService` onto `vector_index_registry`, `rag_configs` becomes fully superseded — closing `TD-109` is this Work Package's own explicit obligation (charter §0 item 2), not new debt.
- **TD-candidate-D** (Medium): BA-02's own query path cannot obtain a real, production `TierResolver`-backed Access Evaluation Outcome (`TD-111`, root cause, unresolved platform-wide) — the same disclosed gap every Work Package since WP-05 has carried; BA-02 is gated by real authentication (§4.4) and real tenant scoping, not by a full Access Evaluation, mirroring `IRA-009`'s/`IRA-010`'s own precedent of proceeding at minimum scope rather than blocking on `TD-111`'s own platform-wide resolution.

(Final Technical Debt IDs assigned at implementation time, per `CLAUDE.md §19.8.2`.)

---

## 10. Testing Strategy

Per `IMP-001 §11`, extended by `CLAUDE.md §21.4`'s own Mandatory Tenant-Isolation Test Checklist: `vector_index_registry`, `document_chunk_registry`, and `evidence_registry` each carry an `organization_id` tenant boundary (nullable for platform-wide rows). BA-01/02/03's own test suites SHALL each include, as a submission gate: (a) at least one test seeding two distinct, unrelated Organizations with no shared row; (b) at least one test confirming a caller in one Organization cannot retrieve or infer another Organization's own tenant-dedicated index configuration, registered content, or query results through any of the three endpoints; (c) an explicit probe of whether an unrelated tenant's own index-name identifier is accepted by BA-02/BA-03 (a caller-supplied, not claims-derived, parameter) — if accepted, the endpoint SHALL be gated before submission, per §21.4(c). Full `AIService` regression suite re-run before closure. Given §4.4's own finding (zero pre-existing authentication anywhere in this service), this Work Package's own test suite is also the **first** to exercise `AIService` under real, verified authentication at all — extra scrutiny is warranted here specifically, mirroring the Roadmap's own "first Work Package in a never-before-chartered domain... not the milestone to compress" judgment (`PRODUCT-MILESTONE-ROADMAP.md §3`).

---

## 11. Entry Criteria

This IRA itself is the entry-criteria gate for **chartering**. Satisfied: charter exists (`WP-11_Enterprise_Search.md`), governing specifications reviewed in full (`EIA-001 Volume I` read directly from primary source in the absence of a dedicated `PE-001-C093`, `Master_Technical_Architecture.md` AMD-012 read directly), existing assets discovered (§3), Gap Analysis complete including the three `§21.3` reviews and three previously-undisclosed gaps (§4.2/§4.4/§4.5), no constitutional blocker for the in-scope portion, critical-path dependency (R3/R4) independently re-verified closed.

**Distinct, additional entry criterion for Business Activity implementation specifically (BA-01/02/03):** the AIService Authentication Bootstrap prerequisite (§4.4, §5) SHALL be complete and independently verified before BA-01, BA-02, or BA-03 implementation begins — a gate on Business Activity work, not on this IRA's own acceptance (the IRA may be accepted while this prerequisite remains outstanding, exactly as an accepted IRA does not itself imply implementation authorization, per §13).

## 12. Exit Criteria

Per `CLAUDE.md §19.7`/`§19.7b`/`§20.7`/`§21`, applied to the scope in §4.7/§8: BA-01/02/03 Implementation Complete; Independent Certification; V&V Audit (remediated and re-verified if any finding, including mandatory tenant-isolation verification per `§21.4` and specific attention to the newly-authenticated `AIService` surface per §10); Release Readiness Audit; end-to-end demonstrability for the in-scope facets only (a persona can register content, then query it, and see a real evidence-cited result); `TD-109` closed; committed. Per `§21.5`, one Repository Owner authorization executes the entire Work Package.

---

## 13. Repository-Owner Authorization

**IRA Acceptance: Not yet granted — awaiting Repository Owner review of the remainder (Plan A BA-01/02/03, Plan B).** Per this Work Package's own charter §13 (mirroring `WP-10`'s own two-step chartering→implementation-authorization precedent), a separate, future "WP-11 Implementation Authorization" instruction remains required before BA-01/02/03 implementation begins.

**Platform Prerequisite Authorization: GRANTED, 2026-08-03**, per Repository Owner Instruction "Platform Prerequisites" — implementation of "mandatory platform prerequisites identified and approved in IRA-011 where those prerequisites are required to enable WP-11," explicitly scoped to not expand Business Capability scope, create new Business Activities, or exceed minimum-necessary implementation, fully documented and traceable to this IRA. This authorized, and only, the AIService Authentication Bootstrap prerequisite (§4.4/§5) — the Alembic-chain prerequisite (§4.5) remains genuinely part of BA-01's own future implementation, not separately authorized here. See §14 for the completed implementation record.

---

## 14. Platform Prerequisite Implementation Record — AIService Authentication Bootstrap (Complete)

**Authorized:** Repository Owner Instruction "Platform Prerequisites," 2026-08-03 (§13). **Scope:** exactly the prerequisite named in §4.4/§5 — no Business Activity, no expansion of C-093's own chartered capability scope, per that instruction's own explicit conditions.

**Implemented:**

- `Backend/Services/AIService/dependencies.py` (new) — `decode_access_token()`/`get_current_claims()`, mirroring `AuthService/services/auth_service.py::decode_access_token` and `AuthService/dependencies.py::get_current_claims` exactly (same library, `python-jose`, already an `AIService` dependency per `requirements.txt`; same settings-resolved secret/algorithm via `AIService`'s own already-declared `jwt_secret_key`/`jwt_algorithm`; same claim shape as `AuthService` actually issues).
- `Backend/Services/AIService/tests/test_authentication.py` (new) — 8 unit tests: valid-token acceptance (asserting the real `AuthService` claim shape decodes correctly), expired-token rejection, wrong-token-type rejection, bad-signature rejection, malformed-token rejection, missing-header rejection, non-Bearer-scheme rejection, end-to-end `get_current_claims` acceptance.

**Refined finding, superseding IRA-011 §4.4's own original recommendation (evidence discovered during implementation, not anticipated at drafting time):** `Backend/Shared/Security/jwt_manager.py`'s `JWTManager` — the "architecturally cleaner reuse target" §4.4 recommended, contingent on fixing `TD-107` — was evaluated directly against `AuthService`'s own real token-issuance code (`services/auth_service.py::create_access_token`) and found **not actually compatible**: `JWTManager.create_token()`'s own claim shape (`sub`, `tenant_id`, `roles`, `permissions`) does not match what `AuthService` issues (`person_id`, `identity_id`, `organization_id`, `membership_id`, `role_code`), and `JWTManager` resolves its secret from a third, distinct environment variable (`AUREX_JWT_SECRET`) neither `AuthService` (`JWT_SECRET_KEY`) nor `AIService` (`AUREX_JWT_SECRET_KEY`/`JWT_SECRET_KEY`) uses. Fixing `TD-107` alone would not have produced a working, interoperable authentication dependency — `JWTManager` cannot verify a real `AuthService`-issued token regardless of the import error, a materially different and larger gap than `TD-107`'s own registered scope. **`TD-107` was therefore NOT bundled into this prerequisite** — it remains Open, amended with this finding (`TECH-DEBT.md`, this same pass). The implemented dependency instead mirrors `AuthService`'s own local pattern directly, per `CLAUDE.md §8`'s service-boundary discipline (no cross-service Python import for business/security logic) — real interoperability with actual, live tokens, not parallel infrastructure that happens to also decode JWTs.

**Incidental defect found and fixed (disclosed as `TD-123`, Closed):** `Backend/Services/AIService/schemas/extraction.py` line 24 contained a `SyntaxError` (a stray space inside a field identifier) that blocked `AIService`'s entire application — and therefore its entire test suite, including this prerequisite's own new tests — from ever loading. Unrelated to WP-11/C-093; a pre-existing defect, never previously exercised because no prior Work Package had run this service's own test suite end-to-end. Fixed (one-character correction, zero semantic ambiguity — every consumer already expected the corrected name) because it blocked verifying this prerequisite works inside the real application, not merely in isolation; disclosed in full per `TECH-DEBT.md TD-123`.

**Verification:** full `AIService` test suite — previously unable to run at all (`TD-123`) — now collects and passes in full: **11/11** (3 pre-existing `tests/test_ai.py` + 8 new `tests/test_authentication.py`), zero regressions, run twice (isolated new-file run, then full-suite run) via `pytest` from `Backend/Services/AIService`.

**Not built, per this prerequisite's own minimum-necessary scope (§4.4):** no authorization/persona-gating dependency (`require_platform_admin`-equivalent — that is BA-01/02/03's own future implementation, per §5); no retrofit of `get_current_claims` onto `AIService`'s own pre-existing, non-WP-11 endpoints (`extraction.py`/`validation.py`/`scoring.py` — untouched, per `CLAUDE.md §20.1`'s own "does not reopen" precedent applied to unrelated, already-shipped endpoints); no Alembic-chain work (§4.5, genuinely BA-01's own scope, not authorized by this instruction).

**Traceability:** `IRA-011 §4.4` (finding and original resolution path) → this §14 (implementation, refined finding, verification) → `TECH-DEBT.md TD-123` (incidental defect, Closed) → `TECH-DEBT.md TD-107` (amended, still Open, unaffected in its own scope) → `WP-11_Enterprise_Search.md §5` (Dependencies, updated to reflect completion).

**Status: COMPLETE.** BA-01/02/03 implementation remains gated on the separate, still-outstanding "WP-11 Implementation Authorization" instruction (§13) — this prerequisite's own completion does not itself authorize Business Activity work.

---

*End of IRA-011. Drafted; awaiting Repository Owner acceptance of Plan A/B and separate WP-11 Implementation Authorization for BA-01/02/03. The AIService Authentication Bootstrap platform prerequisite (§4.4/§14) is implemented and complete, per its own distinct "Platform Prerequisites" authorization (§13) — no Business Activity implementation has been performed under this document.*
