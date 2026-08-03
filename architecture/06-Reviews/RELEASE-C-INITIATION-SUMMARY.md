# Release C Initiation & WP-11 Planning — Summary

**Type:** Planning-only governance summary, per Repository Owner Instruction "Release C Initiation & WP-11 Planning" (2026-08-03). **No code, API, or architecture change is authorized by this document or the pass it summarizes. WP-11 implementation has not begun.**

---

## 1. Release C Initiation

Release B (Milestone 1, "The Configured Enterprise") is CLOSED, CERTIFIED, and release-ready — `RELEASE-B-INTEGRATION-SE009-EDR1-READINESS.md`, EDR-1 READY. Release C (Milestone 2, "The Intelligent Enterprise," `PRODUCT-MILESTONE-ROADMAP.md §3`) is hereby initiated at the **planning** stage only: WP-11 is chartered and its Implementation Readiness Assessment is drafted; neither is authorized to proceed to implementation without a further, separate Repository Owner instruction, mirroring `WP-10`'s own two-step chartering→authorization precedent.

---

## 2. Evidence for Selecting WP-11 = C-093 Enterprise Search

Per Repository Owner Instruction Phase 1, using only repository evidence (Product Milestone Roadmap, Architecture Evolution Roadmap, Architecture Evolution Implementation Programme, `WP-REG-001`, `WPR-001`, `CAP-001`):

| Candidate | Governing Documents | Dependencies | Roadmap Order | Recommendation |
|---|---|---|---|---|
| **C-093 Enterprise Search** | `CAP-001` (Active, D-005); `EIA-001 Vol. I` (Access Pattern discipline); `Master_Technical_Architecture.md` AMD-012 (LOCKED schema: `vector_index_registry`, `document_chunk_registry`); `TD-109` (assigns registry-reconciliation execution to WP-11); `SER-001 SE-024`/`SE-026` | Real code already exists (`RAGEngine`, provider abstractions) behind two clean interfaces; schema fully specified and LOCKED; critical-path `R4` dependency now confirmed resolved (`AMD-015`) | `ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md` `R17`/`R28`, Release C, first D-005 item on the critical path to Executive Cognition (R23/R24) | **Selected.** Reuse-first: only candidate with real, substantial existing code and a fully-specified, zero-conflict physical schema to build against. |
| **C-090 Enterprise Discovery** | `CAP-001` (Active, D-005); `HISTORICAL-SCREEN-REALIZATION-MATRIX.md` (`F1_Enterprise_Understanding_Center.html`, EVOLVE CONCEPT, verbatim-linked to LOCKED `Complete_Blueprint.md` Q1–Q12 text) | No equivalent code exists anywhere; structurally more demanding (multi-document synthesis, contradiction detection) than a first, proving Work Package should attempt | Also named in `SER-001 SE-024`'s umbrella text as an alternative; `R17` names both as eligible | **Not selected this cycle** — disclosed, not dropped. Real, evidence-grounded future business case (`F1`) preserved for a later charter. |
| **C-092 Knowledge Graph Management** | `CAP-001` (Active, D-005); `SER-001 SE-025` (lists "WP-11 (part of)") | Requires Neo4j Aura — zero driver, connection code, or configuration exists anywhere in this repository (confirmed by direct search) | `R17`/`R28` reference it alongside C-093, but as a distinct, larger scope | **Reclassified out of WP-11's own scope** during charter drafting — a hard external-infrastructure gap distinct in kind from C-093's own (interface exists, only the concrete provider is stubbed). `SER-001 SE-024`'s own umbrella text names only "C-090 or C-093," never C-092, as the charter target. |

**Selection: WP-11 = C-093 Enterprise Search.** Full five-point evidence basis recorded in `WP-11_Enterprise_Search.md §0`.

---

## 3. WP-11 Charter

`architecture/05-Implementation/WP-11_Enterprise_Search.md` — CHARTERED. Scope: C-093 Enterprise Search, `Backend/Services/AIService` (existing service, reused). Two governed halves named by the charter (index configuration, query execution); `IRA-011` (§4) exercises the charter's own delegation and finalizes three Business Activities. Out of scope: C-090, C-092, real embedding/vector-search provider (no credentials available), Multi-Agent orchestration (`SE-027`), frontend UI beyond what `IRA-011`'s own Plan B determines. No architecture change proposed — every table this Work Package writes to is already LOCKED and canonical (AMD-012).

**Corrected during this same pass** (see charter's own inline corrections): the charter's original §9 Technical Assumption that an `AIService` Alembic chain already exists was found incorrect (none exists anywhere in that service); the charter's original §5 Dependencies disclosed only `R6` as a residual risk and did not explicitly re-verify `R4`'s own hard critical-path status — now independently re-verified closed (§4 below).

---

## 4. IRA-011

`architecture/05-Implementation/IRA-011_WP-11_Enterprise_Search_Implementation_Readiness_Assessment.md` — **DRAFTED, READY (at the scope below), pending Repository Owner acceptance.**

**Independently re-verified:** the Implementation Programme's own critical-path statement — "do not start R17 [WP-11] before R3 and R4 have closed" — is satisfied. `R3` closed via Release A1; `R4` (the `llm_prompt_registry`/`reasoning_engine_registry` reconciliation, "the single highest-leverage decision in the programme") is closed via the `AMD-015` CHANGELOG (`Master_Technical_Architecture.md` lines 630–682), applied by Repository Owner decision per `IMP-REPORT-RELEASE-A2_Governance.md` (2026-08-01). `R6` remains open, disclosed as a non-blocking soft dependency (both the charter and `IRA-011` mitigate it by reading `Master_Technical_Architecture.md`'s own primary schema text directly rather than `CMD-001 §24`'s potentially-stale summary).

**Three previously-undisclosed gaps found and resolved within IRA-011's own scope determination:**

1. **`AIService` has zero authentication anywhere** — every existing router trusts an unverified, client-supplied tenant header, a more severe instance of the exact defect class `CERT-WP-10` Finding B-1 and `VV-AUDIT-WP-09` Finding 2 already found and remediated elsewhere in this repository. **Reclassified** (Repository Owner Instruction "Final planning validation before IRA-011 acceptance," 2026-08-03, `IRA-011 §4.4` second correction): this is a **mandatory platform prerequisite gating BA-01/02/03, not part of WP-11's own Business Capability scope** — not folded into BA-01, not a fourth Business Activity, carries no WP-11 traceability. Evidence: fails `CMD-001 §26.3a` Step 1 (no independent business identity); direct precedent in `WP-00`/`WP-00A` (Platform Bootstrap, no owning `PE-001` capability) and `WP-RTA-001` (Runtime Work Package, consumed by but not produced within a Business Capability WP); the defect pre-dates and is broader than WP-11 (`AIService`'s own pre-existing `extraction.py`/`validation.py`/`scoring.py` endpoints share it, untouched by this charter); `TD-106`/`TD-107` are already classified "Backend/Shared (Platform)" in `TECH-DEBT.md`, not capability-owned. Resolution path unchanged: a real JWT claims-verification dependency, reusing `AIService`'s own already-declared-but-unused `jwt_secret_key`/`jwt_algorithm` settings (`CLAUDE.md §19.8.5` — a security/tenant-isolation weakness may not be deferred as Technical Debt), recommended bundled with the `TD-107` fix (`Backend/Shared/Security/jwt_manager.py`'s own broken import) so the Shared `JWTManager` is consumed rather than `AuthService`'s local decode logic duplicated a second time — one of two items still requiring explicit Repository Owner confirmation (§4 of `IRA-011`).
2. **`AIService` has no Alembic migration chain** — contradicted the charter's own §9 assumption. Unaffected by the above reclassification: bootstrapping one remains in-scope, mandatory prerequisite work genuinely produced within BA-01's own first migration (mirroring `AuthService`'s own established pattern), not new architecture.
3. **`document_chunk_registry.evidence_id` is a `NOT NULL` FK to `evidence_registry`, which has zero implementation anywhere in this repository** — the charter's own two Business Activities had no way to produce real, queryable content. Resolved: `IRA-011` adds **BA-03 — Register Enterprise Search Content**, a deliberately narrow content-registration path (caller-supplied text only, no ingestion pipeline, no Discovery Provider, no chunking-algorithm decision) — the minimum addition making BA-02's own query path genuinely real rather than permanently empty, reasoned by the same `CLAUDE.md §19.5` minimum-scope discipline the Repository's own WP-04 BA-08 precedent established.

**Final scope: READY** — C-093's own Business Capability scope is BA-01 (Establish Enterprise Search Index Configuration, including the Alembic-chain prerequisite it genuinely produces), BA-02 (Execute Enterprise Search), BA-03 (Register Enterprise Search Content, new). The AIService Authentication Bootstrap is tracked separately, as a platform prerequisite gating the start of BA-01/02/03, not as WP-11 capability scope. No new canonical Business Object (`vector_index_registry`/`document_chunk_registry`/`evidence_registry` are already LOCKED, AMD-012). No constitutional blocker for the in-scope portion.

---

## 5. Strategic Enhancement Allocation

`SER-001` updated in this pass:

- **`SE-024`** (WP-11 umbrella): Capability column resolved from "C-090 or C-093" to **C-093** (charter §0). Dependencies column updated — `R4` (AI-config registry duplication) marked **resolved**; `R6` (Knowledge Governance) remains open, disclosed non-blocking. Status remains **Deferred** (charter/IRA drafted, not yet implemented).
- **`SE-025`** (Knowledge Graph, C-092): unchanged, Deferred — confirmed Not Applicable to WP-11's own chartered scope (§0/§4 of the charter; reclassified out during drafting).
- **`SE-026`** (Semantic Search real implementation, C-093/C-092): unchanged, Deferred — this is WP-11's own core deliverable; realized by Plan A (BA-01/02/03) once implemented.
- **`SE-027`** (Multi-Agent orchestration): unchanged, Deferred, confirmed Not Applicable — `RAGEngine`'s own design has no agent-delegation dependency.

---

## 6. Enterprise Experience Allocation

Per `CLAUDE.md §20.3`/`§21.3`, `IRA-011 §7` (Plan B): the existing `enterprise-intelligence` nav slot (`/platform-admin/enterprise-intelligence`, currently a `PlaceholderPage`, confirmed by direct read of `admin-navigation.ts`) is reused for BA-01/BA-03's own admin establish/register UI — no new nav item invented for that half. BA-02's own persona-facing query surface has no existing nav slot (the existing one is administration-scoped); its exact placement is deliberately left undecided by this planning pass, to be determined at implementation time against `DS-001`'s own navigation guidance, per `CLAUDE.md §19.1`'s prohibition on inventing a pattern `DS-001` does not define.

---

## 7. Executive Experience Allocation

Per `IRA-011 §4c`: WP-11 advances genuine, if narrow, Executive Cognition — the platform's first "ask a question, get a cited answer" experience (`PRODUCT-MILESTONE-ROADMAP.md §3`, Milestone 2's own Executive Value statement), distinct from WP-10's own Discover-stage-only advance. No dedicated Executive screen is chartered. Genuine Executive Cognition capability (C-094 AI Conversation Management) remains correctly gated behind WP-11's own successful five-gate closure, per `EIA-001 Vol. I`'s own Access → Converse layering and the Implementation Programme's own R23/R24 gating.

---

## 8. Governance Updates Made in This Pass

- `architecture/05-Implementation/WP-11_Enterprise_Search.md` — status annotation added (IRA-011 drafted); §3 (BA-03 addition), §5 (R4 resolution correction), §9 (Alembic assumption correction) each amended with an inline correction note, source text preserved per this repository's own "no existing content removed or redefined" discipline.
- `architecture/05-Implementation/IRA-011_WP-11_Enterprise_Search_Implementation_Readiness_Assessment.md` — created (this pass's primary artifact).
- `architecture/06-Reviews/SER-001_Strategic_Enhancement_Register.md` — `SE-024` row updated (§5 above).
- `architecture/00-Governance/DOC-000_Documentation_Catalogue.md` — "IRA Reports" family row updated to include `IRA-011` (Drafted, not yet Accepted); total document count unchanged (folded into the existing family row, per every prior Work Package's own mid-implementation precedent).
- `architecture/06-Reviews/RELEASE-C-INITIATION-SUMMARY.md` — created (this document).

**Not updated, per this pass's own no-invention rule and each register's own Maintenance Rule:** `WPR-001` (no row added — a row is added only once a Work Package is committed or has an *accepted* IRA, `WPR-001 §3`; `IRA-011` is drafted, not accepted) and `WP-REG-001` §8 (Pending/Future Work Packages — same "accepted IRA only" rule, `WP-REG-001 §8`'s own text). No architecture, methodology, or capability document was modified.

---

## 9. Repository Files Created / Modified

**Created:**
- `architecture/05-Implementation/WP-11_Enterprise_Search.md` *(pre-existing in the working tree at the start of this pass, untracked — reviewed, independently verified, and corrected in place; not newly authored by this pass)*
- `architecture/05-Implementation/IRA-011_WP-11_Enterprise_Search_Implementation_Readiness_Assessment.md`
- `architecture/06-Reviews/RELEASE-C-INITIATION-SUMMARY.md`

**Modified:**
- `architecture/06-Reviews/SER-001_Strategic_Enhancement_Register.md` (`SE-024` row)
- `architecture/00-Governance/DOC-000_Documentation_Catalogue.md` (IRA Reports family row)
- `architecture/05-Implementation/IRA-011_WP-11_Enterprise_Search_Implementation_Readiness_Assessment.md` — amended (not newly authored — see below), per Repository Owner Instruction "Final planning validation before IRA-011 acceptance" (2026-08-03): §4.4, §4.7, §5, §8, §11 corrected to reclassify the AIService authentication gap as a mandatory platform prerequisite gating BA-01/02/03, not part of WP-11's own Business Capability scope. §1's own central finding annotated with a forward pointer to this correction; no original analysis removed, per this repository's own "no existing content removed or redefined" discipline.
- `architecture/05-Implementation/WP-11_Enterprise_Search.md` — amended with a second correction note (header), a §2 Scope confirmation (unchanged), and a new §5 Dependencies entry for the reclassified prerequisite.

**Not modified:** `WPR-001_Work_Package_Roadmap.md`, `WP-REG-001_Enterprise_Work_Package_Register.md` — both correctly withhold a WP-11 entry pending Repository Owner acceptance of `IRA-011`, per their own respective Maintenance Rules. No architecture, methodology, or capability document was modified in either pass.

None of the above files are yet committed to the repository (git status: untracked/modified in the working tree only) — commit timing is a Repository Owner decision, not performed by this planning-only pass.

---

## Platform Prerequisite: Implemented (Repository Owner Instruction "Platform Prerequisites," 2026-08-03)

The Repository Owner authorized implementation of "mandatory platform prerequisites identified and approved in IRA-011 where those prerequisites are required to enable WP-11," explicitly scoped to no Business Capability expansion, no new Business Activities, minimum-necessary implementation only. The **AIService Authentication Bootstrap** (§8 above) was built under this authorization — `Backend/Services/AIService/dependencies.py` (new), 8 passing unit tests, full `AIService` suite 11/11 (zero regressions). Item 1a below (`TD-107` bundling) is resolved as part of this same implementation pass — evidence gathered while building the dependency showed `JWTManager`'s own claim shape and secret-env-var name are both incompatible with `AuthService`'s real, live tokens, so `TD-107` was **not** bundled; the dependency instead mirrors `AuthService`'s own local decode pattern directly. One incidental, unrelated, pre-existing defect (`TD-123`, a `SyntaxError` blocking `AIService`'s entire application from starting) was found and fixed to make verification possible; both are recorded in `TECH-DEBT.md` and `IRA-011 §14`. Full record: `IRA-011 §13`/§14.

---

## STOP — Awaiting Repository Owner Decision

Per the governing instruction: **WP-11's Business Capability scope (BA-01/02/03) is NOT implemented.** Only the platform prerequisite above was built, under its own distinct, explicit authorization. One Repository Owner decision remains outstanding before Business Activity implementation may begin:

1. **`IRA-011` acceptance of Plan A (BA-01/02/03)/Plan B** — including confirmation of the authentication prerequisite's own reclassification as a platform prerequisite (this pass's own finding, `IRA-011 §4.4`) — specifically, that it requires no separate charter, IRA, or Work Package number of its own, mirroring how `R3`/`R4`-class reconciliation work gates a Work Package without itself being one. *(The `TD-107` bundling question, previously listed here, is resolved — see above.)*
2. **A separate "WP-11 Implementation Authorization" instruction**, mirroring `WP-10`'s own two-step precedent, required after `IRA-011` acceptance before BA-01, BA-02, or BA-03 implementation begins.

*End of Release C Initiation Summary.*
