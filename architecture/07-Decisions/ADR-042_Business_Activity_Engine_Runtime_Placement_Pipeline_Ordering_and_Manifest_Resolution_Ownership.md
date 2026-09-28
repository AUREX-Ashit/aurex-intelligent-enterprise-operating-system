# ADR-042 — Business Activity Engine: Runtime Placement, Execution-Pipeline Ordering Authority, and Manifest Resolution Ownership

**Status:** Accepted
**Classification:** Architecture Governance / Runtime Component Placement and Canonical-Authority Disposition (`CLAUDE.md §16`, `§18`, `§19`)
**Decided by:** Repository owner (architecture governance authority), 2026-09-24, in the "RO DECISION PACKAGE — WP-BAE-001 M1 ARCHITECTURAL DISPOSITION" (decisions `RO-M1-01`, `RO-M1-02`, `RO-M1-03`), responding to the decision questions raised by `IRA-BAE-001-M1_Runtime_Contract_and_Gap_Analysis.md §14.2`. This ADR was separately authorized on 2026-09-24 ("RO DECISION: AUTHORIZE ADR FOR WP-BAE-001 M1 ARCHITECTURAL DECISIONS").
**Affected Documents:** None amended by this ADR. `RTA-001` (LOCKED), `IMP-001`, the `WP-BAE-001` Charter, `IRA-BAE-001`, `IRA-BAE-001-M1`, the WP-23 Charter, `ROD-ENTERPRISE-BAR-Decision-Preparation.md`, `BAR-INDEX.md`, and `WP-RTA-001` are read-only evidentiary sources. None is modified by this ADR. The `RTA-001` corrections this ADR makes necessary are identified in §9 and **not performed**.
**Affected Code:** None. `Backend/Runtime/BusinessActivityEngine/` is **not created**. No module, class, schema, migration, API, route, test, manifest, or execution-state table is created or modified.

---

## 0. Nature of This Record

This ADR **records** three architectural dispositions that the Repository Owner has **already approved** (`RO-M1-01`, `RO-M1-02`, `RO-M1-03`). It creates no policy beyond them.

It exists because `CLAUDE.md §19` provides that architecture "SHALL NOT evolve during implementation unless explicitly approved through the existing Architecture Decision Record (ADR) process." Two of the three decisions depart from text in the LOCKED `RTA-001`, and the third fixes the location of a new Runtime Component. `IRA-BAE-001-M1 §16` (Condition 1) accordingly identified ADR formalization as required before the `RTA-001` correction pass.

**This ADR does not authorize BAE implementation.** It does not authorize the M1 skeleton or any later milestone. Implementation authorization remains a separate Repository Owner act under `WP-BAE-001 §17`.

## 1. Context

- `IMP-001 §6.15`–`§6.19` specify the Business Activity Engine (BAE) as the mandatory, platform-wide execution path for every Business Activity. No BAE exists in this repository (`BAR-WP23-WORKSTREAM-D-BUSINESS-ACTIVITY-ENGINE-PREREQUISITE-INVESTIGATION.md §2`–`§7`).
- The Repository Owner selected Option B, a separately chartered runtime Work Package (investigation `§0`). This produced `IRA-BAE-001` and the `WP-BAE-001` Charter, registered in `WPR-001 §2a`.
- M1 of `WP-BAE-001` (Runtime Contract / Architecture Baseline) was authorized as analysis and design only. It produced `IRA-BAE-001-M1_Runtime_Contract_and_Gap_Analysis.md`, which mapped `IMP-001 §6.15`–`§6.19` against the repository.
- Its cross-check (§14) found conflicts between `IMP-001` and the LOCKED `RTA-001`, and between both of those and the enterprise BAR decisions (D2/D6). `IRA-BAE-001 §11` had also left module placement open.
- The Repository Owner disposed of all twelve M1 decision questions on 2026-09-24 (`IRA-BAE-001-M1 §0`). M1 concluded **COMPLETE WITH CONDITIONS** (`§16`).

## 2. Problem / Conflict Identified by M1

**2.1 Module placement (`IRA-BAE-001-M1 §12`; `IRA-BAE-001 §11`).** No source fixed where the BAE lives. Four placements were compared factually:
- P1: `Backend/Runtime/BusinessActivityEngine/`, in-process
- P2: embedded in AuthService
- P3: `Backend/Shared/`
- P4: a standalone network service

Creating a new top-level Runtime Component location is a new architectural artifact under `CLAUDE.md §18`/`§19.4`.

**2.2 Execution-pipeline ordering (`IRA-BAE-001-M1 §14.1`, `X-01`).** The sources give different stage sequences:
- `IMP-001 §6.16.3` `[ACTIVE]`: a 16-stage sequence (Request Reception → Activity Resolution → Execution Context Initialization → Authorization Evaluation → Input Contract Validation → Business Validation → Metadata Resolution → Workflow Resolution → Business Rule Execution → Persistence Coordination → Transaction Commit → Domain Event Publication → Notification Processing → Audit Recording → AI Assistance Hooks → Response Generation).
- `RTA-001 §6.5` `[LOCKED]`: a different 16-stage sequence (Runtime Request → Activity Discovery → Manifest Resolution → Business Activity Context → Authorization → Metadata Resolution → Enterprise Context Resolution → Business Rule Execution → Business Object Persistence → Transaction Commit → Domain Event Publication → Workflow Continuation → Knowledge Graph Update → Audit Recording → Observability → Response).
- `IMP-001 §6.15.5` gives a third ordering.
- The `WP-BAE-001` Charter (§9) and `IRA-BAE-001` (§4) give a fourth, hybrid list.

**2.3 Manifest Resolution ownership (`IRA-BAE-001-M1 §14.1`, `X-02`, `X-03`).**
- `RTA-001 §3.6` `[LOCKED]` lists "Manifest resolution" among BAR's primary responsibilities, and `RTA-001 §6.4` `[LOCKED]` assigns "Manifest Resolution — Business Activity Registry".
- The enterprise BAR decisions D2 and D6 (`ROD-ENTERPRISE-BAR-Decision-Preparation.md §0b`, `§0e`) scope BAR to four LOCKED-minimum responsibilities. They exclude manifest, version, execution-policy, and implementation-mapping metadata.
- The `WP-BAE-001` Charter (M2) places Manifest Resolution in the BAE.
- `IMP-001 §6.15.4` requires the BAE to "Locate the Business Activity implementation." `RTA-001 §6.6` `[LOCKED]` forbids discovery "through implementation-specific mechanisms."
- No source stated where the identifier-to-implementation binding lives.

## 3. Decision

The Repository Owner's decisions `RO-M1-01`, `RO-M1-02`, and `RO-M1-03`, recorded without reinterpretation:

1. **`RO-M1-01`:** The canonical BAE runtime module is `Backend/Runtime/BusinessActivityEngine/`. The BAE executes **in-process within the hosting service**, not as a standalone service.
2. **`RO-M1-02`:** `IMP-001 §6.16` is the **canonical execution-pipeline ordering authority** for the BAE. Where `RTA-001` conflicts with `IMP-001` on pipeline ordering, the BAE follows `IMP-001 §6.16`.
3. **`RO-M1-03`:** The **BAE owns runtime Manifest Resolution** and the governed mapping *BAR-issued Business Activity Identifier → Business Activity implementation/manifest*. BAR remains the canonical Business Activity registration and identifier authority. The BAE must not discover Business Activities through filesystem scanning, decorators, arbitrary module scanning, FastAPI route discovery, or implementation heuristics. The detailed manifest contract remains an M2 design concern.

## 4. Decision Details

### 4.1 `RO-M1-01` — Runtime placement

- **Location:** `Backend/Runtime/BusinessActivityEngine/`, alongside `Backend/Runtime/AuthorizationEngine/`.
- **Execution mode:** in-process, as a library executed within whichever service hosts a given Business Activity. It is not a network service.
- **Rationale, as recorded by the Repository Owner:**
  - it is consistent with the existing AuthorizationEngine runtime precedent (`WP-RTA-001`);
  - it lets the BAE own the hosting service's transaction boundary (`IMP-001 §6.19.3`);
  - it avoids cross-service database transaction ownership (`CLAUDE.md §8`; `IMP-001 §6.19.9`);
  - it keeps the BAE a platform runtime rather than placing it inside AuthService (`IMP-001 §6.15.9`, Domain Independence).
- **Not created by this ADR.** The directory, its packaging, and its import mechanism are implementation matters for the M1 skeleton, which is not authorized here.
- **Alternatives not selected:** P2 (embedded in AuthService), P3 (`Backend/Shared/`), P4 (standalone service). The factual comparison is at `IRA-BAE-001-M1 §12`.

### 4.2 `RO-M1-02` — Pipeline ordering authority

- **Scope of the decision:** the *ordering* of BAE execution stages. The BAE executes stages in the `IMP-001 §6.16.3` sequence quoted in §2.2 above. Per `§6.16.3`, "no stage may be bypassed unless explicitly designated as optional by the Business Activity Contract."
- **Precedence rule:** where `RTA-001` (including `§6.5`) conflicts with `IMP-001` on pipeline ordering, `IMP-001 §6.16` governs BAE execution semantics.
- **`RTA-001` is not rewritten by this decision or by this ADR.** Its text stands as LOCKED until a separately authorized correction (§9).
- **What this decision does not settle (recorded, not decided here):** stage *membership* differences that are not ordering conflicts. `RTA-001 §6.5`'s "Knowledge Graph Update" stage has no `§6.16.3` counterpart. `IRA-BAE-001-M1 §14.4` records this as residual item `R-01`, deferred to M5, with the stated default that no such stage is added without a Repository Owner decision. This ADR does not decide `R-01`.

### 4.3 `RO-M1-03` — Manifest Resolution and identifier-to-implementation mapping

- **Owner:** the BAE owns, at runtime, the resolution of a BAR-issued Business Activity Identifier (`BA-NNNNNN`, D5) to its canonical Business Activity implementation/manifest.
- **BAR's role is unchanged:** BAR remains the canonical registration authority (D2) and the canonical identifier authority (D5). BAR does **not** become the runtime owner of implementation-code resolution, and its decided scope is not expanded.
- **Prohibited discovery mechanisms:** filesystem scanning; decorators; arbitrary module scanning; FastAPI route discovery; implementation heuristics. This is consistent with `RTA-001 §6.6` `[LOCKED]` and `IMP-001 §6.22.8` ("never … through implementation scanning or naming conventions").
- **Required mechanism:** the mapping must use an **explicit, governed manifest/registry contract**. This ADR does not define that contract, its schema, its storage, or its form.
- **Deferred to M2:** the minimum manifest contract, and whether a new governed artifact is required (`IRA-BAE-001-M1 §15`, M2 prerequisite 1). `IRA-BAE-001-M1 §14.5` (`D-09`) records, as an M2 input rather than a decision, that `IMP-001 §6.14`/`§6.29` already define the Canonical Business Activity Manifest (CBAM) concept, and that `IMP-001 §6.29.3` states "The Business Activity Engine consumes the CBAM."

## 5. Consequences

- **For `WP-BAE-001`:**
  - Once separately authorized, the M1 skeleton has a fixed location and a fixed canonical stage sequence. These were the two items `IRA-BAE-001-M1` identified as blocking M1 implementation.
  - M2 has a fixed owner for Manifest Resolution and a fixed list of prohibited discovery mechanisms. It still must define the manifest contract itself.
- **For `RTA-001`:** its `§6.5` ordering text and its `§3.6`/`§6.4` assignment of Manifest Resolution to BAR are now inconsistent with a recorded Repository Owner decision. This is a disclosed, uncorrected inconsistency pending the §9 correction pass. Until corrected, a reader of `RTA-001` alone would reach a conclusion this ADR supersedes for BAE purposes. This ADR is the governing record in that interval.
- **For hosting services:** a service that hosts BAE-routed Business Activities executes the BAE in its own process and on its own database session. Cross-service BAR access for a non-AuthService host is not decided here (`RO-M1-11`, deferred; §6).
- **For existing Business Activities:** none. Every existing Business Activity continues to execute by direct FastAPI routing. Migration onto the BAE remains each capability's own future, separately scoped decision (`WP-BAE-001 §5`).
- **No code consequence** arises from this ADR alone.

## 6. Explicit Non-Decisions and Deferred Matters

This ADR does **not** decide, authorize, or alter any of the following:

- **Implementation:** any BAE implementation, including the M1 skeleton, M2–M7, or creation of `Backend/Runtime/BusinessActivityEngine/`.
- **Manifest contract:** the manifest contract, schema, storage, or artifact form (M2, `RO-M1-03`); whether a new governed artifact is required (M2). *(Reconciliation 2026-09-29: see the addendum at the end of this ADR.)*
- **Registration gate:** the BAE ↔ WP-23 Workstream E interface (`RO-M1-04`, M2). It is not recorded in this ADR.
- **Resolution verification:** the per-datum authoritative-source analysis for Activity Resolution (`RO-M1-05`, M2).
- **Other M1 dispositions:** `RO-M1-04` through `RO-M1-12` are recorded at `IRA-BAE-001-M1 §0`. None of them is formalized by this ADR.
- **State and audit:** durable execution state (`RO-M1-07`, M5/M6); the state-transition set (`RO-M1-08`, M5/M6; `IRA-BAE-001-M1 §11.2` U-01–U-10); audit timing (`RO-M1-09`, M5).
- **Platform services:** their treatment (`RO-M1-10`).
- **Cross-service BAR access:** `RO-M1-11`, deferred until a first consumer is selected.
- **Knowledge Graph Update:** stage membership (`R-01`, M5).
- **Other BAR-assigned responsibilities in `RTA-001 §3.6`:** "Version resolution", "Execution policy lookup", and "Dependency resolution" are also assigned to BAR there and exceed D2's decided scope. This ADR records only the Manifest Resolution consequence of `RO-M1-03` and takes no position on those three items.
- **The outstanding stale-document correction pass** listed at `IRA-BAE-001-M1 §16` Condition 2 (`IRA-BAE-001`, the investigation, Charter §9/IRA §4 stage list, Charter "No milestone has begun" wording). It is not performed.
- **Any amendment** of the `WP-BAE-001` Charter's scope or milestones, `IMP-001`, or `RTA-001`.

## 7. Relationship to BAR and WP-23

- **BAR authority is unchanged.** D1–D9 (`ROD-ENTERPRISE-BAR-Decision-Preparation.md`) are neither reopened nor reinterpreted. BAR remains the canonical Business Activity registration authority (D2) and identifier authority (D5), with its decided four-responsibility scope (D2/D6).
- **BAR scope is not expanded.** `RO-M1-03` places implementation/manifest resolution in the BAE precisely so that BAR does not acquire it.
- **BAR A–C are unchanged.** `bar_identifier_ledger`, `bar_registration`, and their repositories, services, migrations, and tests are not modified. `BAR-INDEX.md` is unchanged. No Business Activity is registered. No `BA-NNNNNN` identifier is assigned. C-024 BA-01 remains unregistered.
- **WP-23 Workstream D/E scope is unchanged.** The WP-23 Charter is not amended.
  - Workstream D remains deferred, dependent on `WP-BAE-001` (investigation `§0`).
  - Workstream E remains responsible for the BAR-side execution-gate mechanism/authority. That is recorded separately as `RO-M1-04` and is not decided by this ADR.

## 8. Relationship to AuthorizationEngine / WP-RTA-001

- **AuthorizationEngine authority is unchanged.** `Backend/Runtime/AuthorizationEngine` remains the sole authority for runtime authorization decisions (`RTA-001 §11.2`). The BAE constructs `AuthorizationContext` and invokes the engine (`RTA-001 §11.5`/`§11.13`); it never evaluates precedence.
- **`RO-M1-01` places the BAE alongside the AuthorizationEngine** under `Backend/Runtime/`, as a peer Runtime Component. The AuthorizationEngine is not absorbed, extended, or re-scoped.
- **`WP-RTA-001` is not reopened.** Its certification (`CERT-WP-RTA-001`, CERTIFIED WITH CONDITIONS; `ADR-016`) and its Responsibility Boundary row ("Authorization Context Construction — Business Activity Engine") stand as written.
- **Pipeline position.** Under `RO-M1-02`, Authorization Evaluation is the fourth stage of the `IMP-001 §6.16.3` sequence, after Execution Context Initialization and before Input Contract Validation. It completes before any business processing (`IMP-001 §6.16.7`).

## 9. Required Follow-Up Corrections (identified, NOT performed)

This ADR does not modify `RTA-001`. The following `RTA-001` corrections are required to align its LOCKED text with the decisions recorded here. Each needs separate Repository Owner authorization before it is applied. They are reproduced from `IRA-BAE-001-M1 §14.3`.

| ID | `RTA-001` location | Correction required | Decision it reflects |
|---|---|---|---|
| **RC-01** | `§6.5` Runtime Execution Lifecycle | State that BAE execution ordering is governed by `IMP-001 §6.16.3`, or align the sequence to it. Any stage-membership change (e.g. Knowledge Graph Update, `R-01`) requires its own decision | `RO-M1-02` |
| **RC-02** | `§3.6` BAR primary responsibilities | Remove or re-qualify "Manifest resolution" as a BAR responsibility; runtime Manifest Resolution belongs to the BAE | `RO-M1-03` |
| **RC-03** | `§6.4` Runtime Responsibilities table | "Manifest Resolution — Business Activity Registry" → "Manifest Resolution — Business Activity Engine" | `RO-M1-03` |

A related non-`RTA-001` item is outside this ADR's scope and is recorded only: the hybrid stage list in `WP-BAE-001` Charter §9 and `IRA-BAE-001 §4` (`IRA-BAE-001-M1 §14.3`, RC-04). It belongs to the separately pending stale-document correction pass.

**Governance-index impact:** none required. Following the established convention (`ADR-036 §Consequences`), this ADR self-registers by filename in `architecture/07-Decisions/` and adds no `DOC-000` row.

## 10. Traceability

| Source | Role |
|---|---|
| `architecture/06-Reviews/IRA-BAE-001-M1_Runtime_Contract_and_Gap_Analysis.md` §0, §12, §14.1 (`X-01`, `X-02`, `X-03`), §14.3, §14.4, §16 | Records the Repository Owner decisions; placement comparison; conflict findings; `RTA-001` correction list; residual `R-01`; Condition 1 (ADR formalization) |
| `architecture/05-Implementation/WP-BAE-001_Business_Activity_Engine_Charter.md` §4, §5, §7, §8, §9, §10 (M1, M2), §17 | Work Package scope; exclusions; BAR/AuthorizationEngine relationships; M2's Manifest Resolution scope; implementation-authorization status |
| `architecture/05-Implementation/IRA-BAE-001_Business_Activity_Engine_Implementation_Readiness_Assessment.md` §9, §11 | Business responsibilities; placement originally deferred |
| `architecture/06-Reviews/BAR-WP23-WORKSTREAM-D-BUSINESS-ACTIVITY-ENGINE-PREREQUISITE-INVESTIGATION.md` §0, §4, §10 | Option B decision; responsibility table; Workstream D dependency |
| `architecture/03-Engineering/IMP-001_Implementation_Playbook.md` §6.15.3, §6.15.4, §6.15.9, §6.16.3, §6.16.5, §6.16.7, §6.19.3, §6.19.9, §6.22.8, §6.29.3 | Canonical ordering (`RO-M1-02`); Activity Resolution; domain independence and transaction ownership (`RO-M1-01`); discovery exclusivity and CBAM consumption (`RO-M1-03`) |
| `architecture/02-Constitutional/RTA-001 - Runtime Architecture and Execution.md` `[LOCKED]` §3.5, §3.6, §6.4, §6.5, §6.6, §11.2, §11.5, §11.13 | Conflicting ordering and ownership text; discovery prohibition; authorization relationship |
| `architecture/06-Reviews/ROD-ENTERPRISE-BAR-Decision-Preparation.md` §0b (D2), §0d (D5), §0e (D6) | BAR scope and identifier authority, unchanged |
| `architecture/05-Implementation/WP-23_Enterprise_BAR_Mechanism_Implementation_Charter.md` §8, §9 | Workstream D/E, unchanged |
| `architecture/05-Implementation/WP-RTA-001_Authorization_Runtime_Engine.md`; `architecture/07-Decisions/ADR-016_Authorization_Runtime_Consolidation.md` | AuthorizationEngine precedent and authority, unchanged |
| `CLAUDE.md` §8, §16, §18, §19 | Service boundaries; canonical-authority conflict handling; change control; ADR requirement |

## 11. Status / Approval

**Accepted.** The three decisions recorded in §3 were approved by the Repository Owner on 2026-09-24 (`RO-M1-01`, `RO-M1-02`, `RO-M1-03`; `IRA-BAE-001-M1 §0`). Creation of this ADR was separately authorized on 2026-09-24.

This ADR partially satisfies `IRA-BAE-001-M1 §16` Condition 1 (ADR formalization). The `RTA-001` correction pass (§9, RC-01–RC-03) that the same condition anticipates remains outstanding and is not performed. `IRA-BAE-001-M1` itself is not edited by this ADR; its Condition 1 text continues to describe the pre-ADR state until a later documentation update.


## Reconciliation Addendum (2026-09-29)

*The decisions recorded above are unchanged. This addendum only reconciles later decisions against §6.*
- §6 left the manifest contract, schema, **storage** and artifact form to M2.
- For the physical implementation boundary of the B2 identifier → implementation binding, that deferral is now resolved by later approved decisions:
  - `ADR-043` (RD-M2-02 = B2);
  - FO-2, approved (`IRA-BAE-001-M2 §16.A`), which keeps M2 read-only;
  - FO-3, design approved (`TDS-BAE-001-M2-FO3 …`);
  - RD-M2-07 (`ROD-BAE-001-M2-Binding-Infrastructure-Ownership-Decision-Preparation.md` §11).
- Under RD-M2-07, the physical binding storage (table, schema, migration), its governed write operation and CI act-citation verification belong to WP-BAE-001 milestone **M2-P**. M2 is the read-only consumer.
- `RO-M1-03` (BAE ownership of the mapping) is unchanged. M2-P is a WP-BAE-001 milestone.

---

*End of ADR-042. Records `RO-M1-01` (BAE at `Backend/Runtime/BusinessActivityEngine/`, in-process), `RO-M1-02` (`IMP-001 §6.16` is the BAE pipeline-ordering authority over `RTA-001`), and `RO-M1-03` (the BAE owns runtime Manifest Resolution; BAR authority unchanged; implementation-specific discovery prohibited; manifest contract deferred to M2). No implementation authorized. `RTA-001` not yet corrected. BAR, WP-23 Workstreams D/E, the AuthorizationEngine, and C-024 are unchanged. Nothing staged, committed, or pushed.*
