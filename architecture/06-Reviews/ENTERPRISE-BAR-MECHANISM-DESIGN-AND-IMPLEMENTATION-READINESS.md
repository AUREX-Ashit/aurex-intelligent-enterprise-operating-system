# Enterprise Business Activity Registry (BAR) — Mechanism Design and Implementation-Readiness Package

**Type:** Design + Implementation Preparation. Not implementation. Every design element below is traced either to a governing source (`SD-002`, `COM-001`, `PLT-001`, `GRC-001`, `RTA-001`, `IMP-001 §6.22`) or to one of the eight Repository Owner decisions now recorded in `ROD-ENTERPRISE-BAR-Decision-Preparation.md` (D1–D8, D4 moot). Where this document proposes an implementation-level detail no source or decision already fixes (e.g., the exact identifier sequence, the physical file/table shape), it is labeled **[IMPLEMENTATION DESIGN — not constitutional text]**, distinct from decided governance.

**Prepared:** 2026-09-20, per direct Repository Owner instruction, as the first platform-level BAR design stage following the enterprise BAR governance decision chain's own completion (D1–D7, all recorded at that time). **Updated 2026-09-22**, per direct Repository Owner instruction, to synchronize this document with D8 (`ROD-ENTERPRISE-BAR-Decision-Preparation.md §0g`, recorded 2026-09-21), a further decision this document's own §21/§22 (Open Issue 1) itself surfaced during the original design pass. This update is a narrow documentation synchronization only — it does not redesign BAR, does not reopen D1–D7, and does not begin implementation.

**Governing decision baseline (re-verified, not re-litigated):** `ROD-ENTERPRISE-BAR-Decision-Preparation.md §0`/`§0b`/`§0c`/`§0d`/`§0e`/`§0f`/`§0g` — D1 Establish; D2 LOCKED-minimum scope (cataloguing/registration, canonical identity, execution-time gate, discovery-exclusivity); D3 retroactive registration for all 21 existing rows; D4 moot; D5 BAR is identifier authority, assigned at BAR registration; D6 no `IMP-001 §6.22` amendment; D7 separate BAR registration index, distinct from `WPR-001`; **D8 — a transitional execution gate: existing Business Activities continue executing during a governed retroactive-registration transition; only newly introduced/future Business Activities are gated immediately upon BAR becoming operational; all 21 existing rows remain subject to D3's own registration obligation, undischarged until performed; no permanent exemption; no transition duration, deadline, or cutover mechanism has been fixed.** **This document does not reopen any of D1–D8** — no source conflict was discovered during design, or during this synchronization pass, that would require it (§24 below).

**Classification key:** `[LOCKED]`/`[ACTIVE]`/`[FACT]`/`[PRECEDENT]`/`[INFERENCE]` — as established throughout the ROD chain. `[IMPLEMENTATION DESIGN]` — a design choice this document makes because no source or decision fixes it, clearly distinguished from governance.

---

## 1. Executive Summary

This document answers: *what exactly must AUREX build to satisfy D1–D8, what existing capabilities require retrofit, and what is the controlled implementation sequence* — at design depth sufficient for engineering to begin after a separate future implementation authorization. It does not create code, schema, APIs, migrations, tests, or the actual `BAR-INDEX.md`/database artifact; it does not register any Business Activity or assign any identifier; it does not modify `WPR-001`, `CBOR-INDEX.md`, any constitutional document, or `C-024 D10`.

**Bottom line:** BAR is a small, four-responsibility mechanism (identity, cataloguing, execution gate, discovery) with its own separate registration index (per D7), linked to — never merging with — `WPR-001` (Work Package governance) and `CBOR-INDEX.md` (Business Object governance). The 21 existing Business Activities require a retroactive backfill exercise that does not reopen any certification, and — per D8 — continue executing uninterrupted throughout that transition; only newly introduced/future Business Activities are gated immediately. C-024 BA-01 remains untouched, `D10` remains scoped to it alone, and BA-01 would only interact with the future BAR mechanism once it is actually implemented — a future contingency, not created here.

---

## 2. Governance Baseline D1–D8 (re-confirmed against source, not re-derived; updated 2026-09-22 to add D8)

| Decision | Outcome | Governing record |
|---|---|---|
| D1 | Establish a canonical enterprise BAR | `ROD-ENTERPRISE-BAR §0` |
| D2 | LOCKED-minimum scope: cataloguing/registration, canonical identity, execution-time gate, discovery-exclusivity | `ROD-ENTERPRISE-BAR §0b` |
| D3 | Registration applies retroactively to all 21 existing rows | `ROD-ENTERPRISE-BAR §0c` |
| D4 | Moot (contingent on D1 Option B, not selected) | `ROD-ENTERPRISE-BAR §0` |
| D5 | BAR is the canonical identifier authority; assignment at BAR registration | `ROD-ENTERPRISE-BAR §0d` |
| D6 | No `IMP-001 §6.22` amendment required | `ROD-ENTERPRISE-BAR §0e` |
| D7 | BAR maintains its own separate registration index, distinct from `WPR-001` | `ROD-ENTERPRISE-BAR §0f` |
| D8 | Transitional execution gate — existing Business Activities continue executing during a governed retroactive-registration transition; future Business Activities are gated immediately; no permanent exemption; no transition duration/deadline/cutover mechanism fixed | `ROD-ENTERPRISE-BAR §0g` |

**No conflict was found between D1–D8 and the LOCKED sources during this design pass, or during this synchronization update** — this design implements exactly what was decided; it does not need to, and does not, revisit any of the eight questions. **D8 was not one of the original seven `§14` questions** — it emerged directly from this document's own §21 (Open Issue 1) and was resolved by the Repository Owner as a further decision in the same class, recorded at `ROD-ENTERPRISE-BAR §0g`.

---

## 3. BAR Responsibility Boundary

| Responsibility | BAR | `IMP-001` | `WPR-001` | CBOR | Other |
|---|---|---|---|---|---|
| Business Activity registration/cataloguing | **Owns** (D2) | Describes methodology only (`§6.22.2`) | No role | No role | — |
| Canonical Business Activity identity (`BA-NNNNNN`) | **Owns, issues** (D2, D5) | Format cross-reference only (`§6.22.1b`) | No role | No role — Business Object identity is CBOR's own, separate namespace | `SD-002-004` (format) |
| Registration state (minimal: exists/registered) | **Owns** (D2) | `§6.22.9`'s fuller status lifecycle is NOT adopted (D2/D6) | No role | No role | — |
| Execution-time gating | **Owns** (D2, `COM-001-005`/`PLT-001-004`/`GRC-001-008`) | Restates the gate (`§6.22.7`/`§6.22.15`) | No role | No role | — |
| Discovery (exclusive, via Registry) | **Owns** (D2, `RTA-001 §6.6`) | Restates (`§6.22.8`) | No role | No role | `RTA-001` (Runtime Execution Architecture context) |
| Work Package → Capability governance | **No role** | No role | **Owns** (`WPR-001 §1`) | No role | — |
| Charter content (design-time BA scope) | **No role** | Owns methodology (`§6.7` BAC, `§6.14` CBAM) | No role | No role | Charter (per-WP artifact) |
| Business Object registration | **No role** | No role | No role | **Owns** (`CMD-001 §26`) | — |
| General authorization policy | **No role** — reuses existing mechanism (§13) | No role | No role | No role | `Backend/Runtime/AuthorizationEngine` |
| Validation checklist, version/dependency management, governance workflow, observability (broader `§6.22`) | **Not adopted** (D2/D6) | Remains `IMP-001`'s own broader methodology, unamended | No role | No role | Future extension only if separately decided |

**BAR does not silently absorb** Work Package governance, Charter governance, capability governance, Business Object governance, CBOR, general authorization policy, or the broader `§6.22` responsibilities not included in D2 — each row above states this explicitly, per the anti-scope-drift instruction governing this task.

---

## 4. BAR Registration Model

**Mandatory fields (directly required by D2/D5/D7):**

| Field | Purpose | Source | Label |
|---|---|---|---|
| Business Activity Identifier | Canonical identity (`BA-NNNNNN`) | `SD-002-004`, D5 | Mandatory |
| Registration status (registered / not registered — a two-state minimum, not `§6.22.9`'s six-state model) | Discharges the execution gate (`COM-001-005`) | D2 | Mandatory |
| Business Activity reference (name/description, informal, human-readable) | Human traceability | `[IMPLEMENTATION DESIGN]` | Mandatory |
| Owning Capability (`C-XXX`) | Traceability to `CAP-001` | `[FACT]`, existing pattern (every CBOR entry carries this) | Mandatory |
| Owning Work Package (`WP-NN`) | Linkage to `WPR-001`, without merging registries (D7) | D7 | Mandatory |
| Registering act reference (the ADR/RO-authorized act that performed registration) | Governance traceability, mirroring the CBOR pattern | `[PRECEDENT]`, `ADR-039`/`-040`/`-041` | Mandatory |
| Registration timestamp | Governance history | `[IMPLEMENTATION DESIGN]` | Mandatory |
| Retroactive flag (registered via D3's backfill vs. prospectively) | Distinguishes the 21-row historical population from future registrations, for audit clarity only | `[IMPLEMENTATION DESIGN]`, informed by D3 | Recommended, not LOCKED |

**Explicitly excluded from the mandatory model (belongs to `§6.22`'s broader, not-adopted scope, per D2/D6):** Business Domain/Object/Type classification beyond the owning-capability reference; Execution/Security/Workflow/Events/AI/Runtime attribute groups (`§6.22.6`); status lifecycle beyond registered/not-registered (`§6.22.9`); version history (`§6.22.10`); dependency tracking (`§6.22.11`); governance-workflow-as-Business-Activity (`§6.22.12`); observability metrics (`§6.22.13`).

**Charter linkage:** referenced, not duplicated — the registration record points to the Charter (where one exists) as its own design-time source; it does not re-host BAC/CBAM content.

**Uniqueness / immutability:** the identifier, once assigned, is permanent and never reused — mirroring `SD-002-004`'s own "globally unique, permanent identifier" requirement, and the CBOR precedent's own practice (no CBOR identifier has ever been reassigned or reused in this repository).

**Relationship to existing governance records:** the registration record is additive — it does not replace or duplicate `IMP-REPORT-WP-XX`, the Charter, `WPR-001`'s own row, or any CBOR entry; it cross-references them.

**Optional future extension, explicitly not built now:** any of `§6.22`'s broader attribute categories, if a future decision (revisiting D2, which this document does not do) ever expands scope.

**Unresolved (flagged, not designed here):** the exact retroactive-registration sequencing for the 21 rows (single omnibus act vs. per-row) — already flagged as open in D3.10/D5.10 and not resolved by this design pass either, since it is an execution-planning question for §11/§18 below, not a data-model question.

---

## 5. Business Activity Identifier Model

**Governance already fixed:** format is `PREFIX-NNNNNN` (`SD-002-004`); BAR is the issuing authority, at BAR registration (D5).

**`[IMPLEMENTATION DESIGN — not constitutional text]` Proposed concrete format:** `BA-NNNNNN`, six-digit zero-padded sequential number, starting at `BA-000001`.

**Justification against repository convention:**
- The prefix `BA` is not invented — it is the **exact prefix already used in the illustrative example** cited independently, three times, in constitutional/methodology text: `SD-002-004`, `CMD-001 §26.4a`, and `IMP-001 §6.22.1b` all use `BA-000089` as their own worked example of a Business Activity identifier. Adopting `BA` as the actual prefix is the most direct, lowest-invention reading of that already-telegraphed convention — this document does not invent a new prefix where the constitutional text already implies one.
- The six-digit, zero-padded, sequential pattern mirrors every existing CBOR identifier in this repository (`OFR-000001`, `CAC-000001`, `BIA-000001`, `AEO-000001`, `CFG-000001`, and the six `SCI`/`POC`/`IMC`/`RVC`/`VLC`/`RSC`-000001 entries) — the only actually-established identifier-formatting convention this repository has, per `SD-002-004`'s own shared `PREFIX-NNNNNN` rule across both Business Objects and Business Activities.
- Starting at `000001` (not, e.g., resuming some other counter) mirrors how each CBOR namespace independently starts its own sequence at `000001`.

**Explicitly not reused, per this task's own instruction:** WP numbers; `BIA-000001` (a Business Object identifier, structurally unrelated); the literal string "BAR" as an identifier; arbitrary capability IDs (`C-XXX`) — none of these becomes, or contributes to, a `BA-NNNNNN` value.

**Design supports:**
- **Uniqueness** — a single sequential counter, one namespace, mirroring the CBOR pattern's own collision-freedom (each CBOR ADR explicitly collision-checks against `CBOR-INDEX.md` before registering — `ADR-041`'s own Self-Review: "Identifier collision-checked against `CBOR-INDEX.md` and repository-wide"). The future BAR index would perform the equivalent check against itself.
- **Stability** — permanent once assigned, per `SD-002-004`.
- **Human traceability** — six digits is legible at the current and reasonably projected future scale (21 existing + an unbounded but modestly-growing future population, consistent with the CBOR namespace's own current scale of ten entries after several Work Packages).
- **Machine use** — a fixed-width, regex-matchable token (`^BA-\d{6}$`), consistent with every other `PREFIX-NNNNNN` identifier already in the repository.
- **Retroactive registration of the 21 existing rows** — each would receive the next sequential `BA-NNNNNN` value at its own registration act; this document does not decide the assignment *order* among the 21 (an execution-planning detail, §11).
- **Future registration** — the same counter continues forward.

**No actual identifier is assigned by this document.**

---

## 6. BAR Registration Index Model (per D7 — separate from `WPR-001`)

**`[IMPLEMENTATION DESIGN]`, informed by the CBOR precedent (structural template only, per D7.7/D5.7's own anti-analogy discipline):**

- **Initial authoritative representation:** a Markdown governance index, structurally mirroring `CBOR-INDEX.md` — i.e., `BAR-INDEX.md` (not created by this document), living in `architecture/00-Governance/` alongside `CBOR-INDEX.md` and `WPR-001`, per that directory's own established role as the home for living, frequently-amended cross-Work-Package indexes (`CBOR-INDEX.md §5`'s own relocation note: "this index lives in `architecture/00-Governance/`... because it is a living, frequently-amended cross-Work-Package index... not LOCKED constitutional text" — the identical reasoning applies to a future BAR index).
- **Whether a database-backed registry is also needed:** not decided here — this is an execution-gate/discovery *runtime* question (§9/§10 below), not a *governance-record* question. The Markdown index is the authoritative governance record (mirroring CBOR); whether a database table also exists as the *runtime* mechanism `IMP-001 §6.22.3`/`RTA-001 §6.6` describe (for actual discovery/execution-gate enforcement at runtime) is a downstream engineering decision within Workstream C/D (§18), not fixed now. **Both is the most likely eventual shape** — a governance index for human/audit traceability (mirroring CBOR-INDEX's own role: "a pointer to it," `CBOR-INDEX.md §1`) plus a runtime-queryable store for the Engine's own actual discovery/gating queries — but this document does not commit to that shape as a decision, only names it as the most plausible outcome given the existing platform pattern.
- **Canonical registration record:** each row = one Business Activity, containing the fields in §4 above.
- **Authority:** the index is a pointer to each registering act (mirroring `CBOR-INDEX.md §1`: "this index does not itself register anything. Each entry's registering ADR remains the authoritative registration record; this index is a pointer to it") — the same authority model applies here: the future registering act (§18, Workstream C) is authoritative; the index is a cross-Work-Package summary of those acts, not a competing source of truth.
- **Relationship to `WPR-001`:** linked by the `Owning Work Package` field (§4); `WPR-001` is not modified, extended, or merged (D7, re-confirmed).
- **Relationship to Charter:** linked by reference; Charter content is not duplicated into the index.
- **Relationship to capability:** linked by the `Owning Capability` field; `CAP-001` is not modified.
- **Relationship to Business Activity Identifier:** the index is the record where each identifier (§5) is written down, per BAR's own issuing role (D5).
- **Registration state:** the minimal two-state model from §4 (registered / not-registered) — sufficient for the execution gate; no fuller lifecycle is adopted (D2/D6).
- **Historical traceability:** each entry cites its own registering act, mirroring CBOR's own "pointer, not source of truth" convention.

~~**`BAR-INDEX.md` is not created by this document** — its logical shape is designed; its physical creation is a future implementation action (§18, Workstream A).~~ *(Superseded 2026-09-22 — `BAR-INDEX.md` has since been built, per `WP-23_Enterprise_BAR_Mechanism_Implementation_Charter.md` Workstream A, exactly to the shape this section designs. It contains zero actual registrations. Historical text preserved, struck through, per this document's own no-silent-fix discipline.)*

---

## 7. `WPR-001` Relationship

Logical chain: **BAR record ↔ Business Activity ↔ Charter ↔ Work Package ↔ Capability.**

- BAR record cross-references its own Work Package via the `Owning Work Package` field (§4).
- `WPR-001`'s own row for that Work Package is **not modified** to carry BAR information — the linkage is one-directional-by-reference from the BAR index toward `WPR-001`, not a bidirectional merge.
- `WPR-001` continues to be queried for WP-level facts (Capability, Status, Governing IRA, Certification); the BAR index is queried for BA-level facts (identity, registration state).
- **No `WPR-001` structural change is proposed, designed, or performed by this document**, consistent with D7's own explicit "do not turn `WPR-001` into the BAR registry" instruction.

---

## 8. CBOR Relationship

- Business Object Identifier (CBOR, `CMD-001 §26`) and Business Activity Identifier (BAR, `SD-002-004`/D5) are **two structurally independent namespaces** (`ONT-001 §2`, re-confirmed throughout D5–D7).
- `C-024`'s own `BIA-000001` (Billing Arrangement, a Business Object) remains **completely separate** from whatever future `BA-NNNNNN` identifier BA-01 (a Business Activity) eventually receives — no shared sequence, no shared prefix logic, no cross-reference implying equivalence.
- `CBOR-INDEX.md` is **not modified** by this document.
- A future BA registration record (§4) may cross-reference a related CBOR entry (e.g., BA-01's own future record could note `BIA-000001` as "the Business Object this Business Activity acts upon") — a reference, never a merge, mirroring how `WP-22_C024_BA-01...Charter.md` and `ADR-041` already coexist as two related-but-distinct artifacts today.

---

## 9. Discovery Architecture

**Logical contract (design-level, no runtime code):**

- The Business Activity Engine (a component this repository has already named, `RTA-001 §3.5`, but not yet built for Business Activities generally — only the narrower Authorization Engine exists, per `WP-RTA-001`) obtains its list of discoverable, executable Business Activities **exclusively** by querying the BAR registration record (`IMP-001 §6.22.8`, `RTA-001 §6.6`, both re-confirmed LOCKED-reinforcing).
- **Implementation scanning or naming-convention-based discovery is explicitly excluded** — `RTA-001 §6.6`'s own verbatim text: "Business Activities shall never be discovered through implementation-specific mechanisms." No future engineering pass may substitute a code-scanning or naming-heuristic discovery path for a BAR-registry query.
- **An unregistered Business Activity is not discoverable through BAR** — by construction, since discovery only enumerates BAR's own registered population; this is the same mechanism that produces the execution gate's own practical effect (§10), not a separate rule. **Per D8 (`ROD-ENTERPRISE-BAR §0g`, transitional gate):** this discovery-exclusivity rule applies fully and immediately to newly introduced/future Business Activities. For the 21 existing rows (D3), it applies once each is individually, retroactively registered — until then, each continues to be invoked through its own existing, pre-BAR mechanism (its current direct route), exactly as today, unaffected by BAR's own discovery-exclusivity requirement. This is not a second, separate discovery path invented for the transition — it is simply the fact that BAR-mediated discovery, and the whole Business Activity Engine it depends on, does not yet exist for any Business Activity today; D8 confirms that its future rollout does not retroactively cut off an existing Business Activity's own current invocation path before that Activity is itself onboarded (registered) into the new mechanism.
- **Relationship to future agent/runtime execution:** unresolved by any source (re-confirmed, D2.6/D6.4) — if a future AI agent orchestrator ever needs to discover Business Activities dynamically, it would query the same BAR mechanism, not a separate path; no agent-specific discovery mechanism is designed here, since none is currently required (no agent-invoked Business Activity exists yet, per the investigation's own §10 finding, re-confirmed unchanged).
- **No specific runtime framework is invented** — this repository has not yet built the Business Activity Engine for general use (only the narrower Authorization Engine, `Backend/Runtime/AuthorizationEngine`, exists); this design does not presuppose a framework choice beyond "queries BAR," consistent with not inventing unsupported runtime architecture.

---

## 10. Execution-Time Registration Gate Architecture

**Logical contract:**

- A Business Activity **must** have a `registered` state in BAR before it becomes eligible for execution (`COM-001-005`/`PLT-001-004`/`GRC-001-008`, `IMP-001 §6.22.7`/`§6.22.15`, all re-confirmed).
- BAR (specifically, its registration-state field, §4) is the **sole authoritative source** for whether a given Business Activity is execution-eligible — no other artifact (Charter, `WPR-001`, CBOR) may substitute as the authority for this specific fact.
- **Temporal reach — D8 (`ROD-ENTERPRISE-BAR §0g`), decided, not this document's own invention:** this gate applies **immediately** to newly introduced/future Business Activities, from the moment BAR becomes operational. It does **not** apply to any of D3's 21 existing rows until each is individually, retroactively registered — those rows continue executing uninterrupted in the interim, per a governed transition, not a permanent exemption. All 21 remain fully subject to D3's own registration obligation, undischarged until performed. No transition duration, deadline, or specific cutover mechanism has been fixed by D8, and none is invented here — the *eventual* enforcement mechanism for closing the transition (e.g., per-row cutover as each registers, vs. a single future date for all remaining unregistered rows) remains open, future implementation-planning work (§21, Open Issue 5).
- **Denial behavior, at the design level only:** when a Business Activity is invoked without a `registered` BAR state, execution must fail/deny — the exact mechanism (HTTP status code, exception type) is **not specified here**, per this task's own instruction not to invent detailed API behavior unless required and supported by existing platform convention; this repository's existing convention (e.g., `require_platform_admin`'s own 403-style denial pattern) would be the natural template for a future engineering pass, not committed to here.
- **No hidden bypass** — a Business Activity callable via a hard-coded route or an activity name matched by convention, without a corresponding BAR `registered` entry, is not source-compliant; this design does not create, and explicitly forecloses, such a bypass path.

**Explicit distinctions (per this task's own instruction — these are not the same thing):**
- **Registration eligibility** — whether a Business Activity *may* be registered (a governance/data-completeness question: does it have the fields §4 requires).
- **Discovery** — whether the Engine *can find* a Business Activity to consider executing (§9) — logically downstream of registration.
- **Execution authorization (the BAR gate)** — whether a *registered* Business Activity is *currently eligible to run at all* (this section) — a platform-level gate, binary, tied to registration state alone.
- **Ordinary business authorization** — whether *this specific caller* may invoke *this specific* (already execution-eligible) Business Activity right now (e.g., `require_platform_admin`, tenant-isolation checks, per-endpoint permission logic) — a **separate, existing mechanism this design reuses, not replaces** (§13).

These four are sequential, independent checks — a Business Activity can be discoverable but not execution-eligible (unregistered), or execution-eligible but denied to a specific caller (ordinary authorization failure) — the BAR gate does not subsume the latter, and ordinary authorization does not subsume the former.

---

## 11. Retroactive Registration Strategy — the 21 Existing Business Activities

**Execution during this transition, per D8 (`ROD-ENTERPRISE-BAR §0g`), decided:** every row below continues executing exactly as it does today, uninterrupted, for the entire duration of its own retroactive-registration exercise. Registration status changes only the future eligibility gate's own eventual reach for that row (§10) — it is not itself the mechanism that stops or starts execution during the transition. All 21 remain fully subject to the registration obligation below; D8 governs only the execution consequence in the interim, not whether registration itself is required.

**Full implementation-preparation inventory (re-confirmed from `ROD-ENTERPRISE-BAR §D3.4`, no new data invented; table unchanged from the original design pass):**

| # | Capability | WP | BA | Charter | Impl. status | Cert. status | Existing identity evidence | BAR dependency | Unresolved data |
|---|---|---|---|---|---|---|---|---|---|
| 1 | C-004 | WP-01 | BA-01–08 (informal) | Predates convention | IMPLEMENTED | CLOSED — CERTIFIED | `IMP-REPORT-WP-01` | Identity + registration record per informal BA label | Which of the 8 informal labels map 1:1 to a distinct future `BA-NNNNNN` — needs RO/governance confirmation at registration time |
| 2 | C-003 | WP-02, WP-06 | Various (informal) | Predates convention | IMPLEMENTED | CLOSED — CERTIFIED | `IMP-REPORT-WP-02`/`-06` | Same | Same |
| 3 | C-007 | WP-03 | BA-01,02,03,06–11 (9 of 11) | Predates convention | PARTIAL | CERTIFIED (partial) | `IMP-REPORT-WP-03` | Identity + record per completed BA only (BA-04/05 BLOCKED, excluded) | Whether BLOCKED BAs (04/05) register at all — flagged, not decided here |
| 4 | C-005 | WP-04 | BA-01–09 | Predates convention | IMPLEMENTED (9/9) | CLOSED — CERTIFIED | `IMP-REPORT-WP-04` | Identity + record, 9 entries | None beyond standard confirmation |
| 5 | C-002 | WP-05 | BA-01–06 | Predates convention | IMPLEMENTED (min. scope) | CLOSED — CERTIFIED | `IMP-REPORT-WP-05` | Identity + record | Whether the minimum-scope-only BAs register as-is or await fuller scope — flagged |
| 6 | C-006 | WP-07 | (informal) | Predates convention | IMPLEMENTED | CLOSED — CERTIFIED | `WPR-001` row | Identity + record | None |
| 7 | C-001 | WP-08 | (informal) | Predates convention | IMPLEMENTED | CLOSED — CERTIFIED | `WPR-001` row | Identity + record | None |
| 8 | C-008 | WP-09 | (informal) | Predates convention | IMPLEMENTED | CLOSED — CERTIFIED | `WPR-001` row | Identity + record | None |
| 9 | C-041 | WP-10 | (informal) | Predates convention | IMPLEMENTED | CLOSED — CERTIFIED | `IMP-REPORT-WP-10` | Identity + record | None |
| 10 | C-093 | WP-11 | BA-01/02/03 | Predates convention | IMPLEMENTED — PARTIAL (stub) | CLOSED — CERTIFIED | `IMP-REPORT-WP-11` | Identity + record | Whether stub-backed BAs register identically to fully-backed ones — flagged, likely yes (registration ≠ implementation completeness) |
| 11 | C-094 | WP-12 | BA-01/02/03 | Predates convention | IMPLEMENTED — PARTIAL (stub) | CLOSED — CERTIFIED WITH FINDINGS | `IMP-REPORT-WP-12` | Identity + record | Same |
| 12 | — | WP-13 | Not decomposed into BAs | N/A | IN PROGRESS | Not certified | `WPR-001` row | **Not part of the 21 — excluded**, per D3.4's own finding (cross-cutting infra, not a chartered BA) | N/A |
| 13 | C-090/091/092 | WP-14 | BA-01–05 | Predates convention | IMPLEMENTED | CLOSED — CERTIFIED | `IMP-REPORT-WP-14` | Identity + record, 5 entries | None |
| 14 | C-066 | WP-15 | BA-01 | Predates convention | IMPLEMENTED | CLOSED — CERTIFIED | `IMP-REPORT-WP-15` | Identity + record | None |
| 15 | C-040 | WP-16 | BA-01 | `WP-16` Charter | IMPLEMENTATION COMPLETE | CLOSED — CERTIFIED | `IMP-REPORT-WP-16` | Identity + record | None |
| 16 | C-023 | WP-17 | BA-01 | `WP-17` Charter | IMPLEMENTED | Gate 1 PASSED (per R9) | `WPR-001` row | Identity + record | Full 5-gate closure not independently re-verified beyond the R9 note (pre-existing, unrelated finding, not created by this document) |
| 17 | C-003 (runtime binding) | WP-18 | Repo-wide infra, backend-only | `WP-18` Charter | IMPLEMENTATION COMPLETE | CLOSED — CERTIFIED — RELEASE-READY | `IMP-REPORT-WP-18` | Identity + record | Whether infra-only, non-capability-scoped work should register as a "Business Activity" at all in the same sense as capability BAs — flagged, not decided here |
| 18 | C-132 | WP-19 | BA-01 | `WP-19` Charter | IMPLEMENTATION COMPLETE | FORMALLY CLOSED — CERTIFIED — RELEASE-READY | `WPR-001` row | Identity + record | None |
| 19 | C-021 | WP-20 | BA-01 | `WP-20` Charter | IMPLEMENTED | CLOSED — CERTIFIED — RELEASE-READY | `ADR-037` | Identity + record, layered on `ADR-037`'s own existing BAR deferral (not reopened) | None |
| 20 | C-022 | WP-21 | BA-01 | `WP-21` Charter | IMPLEMENTATION COMPLETE | CLOSED — CERTIFIED — RELEASE-READY | `ADR-040`, `ROD-C022-B` | Identity + record, layered on `ROD-C022-B D10` (not reopened) | None |
| 21 | C-024 | WP-22 | BA-01 | `WP-22` Charter | **NOT STARTED** | Not certified | `ROD-C024-BAR` | **Not registered now** — NOT STARTED, outside the "already-implemented" population; governed prospectively (§14) | D10 preserved (§14) |

**Can this be performed from existing repository evidence, or does it require manual RO/governance confirmation?** Mixed — rows with a single, unambiguous BA per WP (7, 8, 9, 14, 15, 16, 18, 19, 20; row 21 excluded from the exercise entirely) can be sourced directly from existing `IMP-REPORT`/`WPR-001`/Charter records without further confirmation. Rows with multiple informal BAs per WP (1, 2, 4, 5, 10, 11, 13) require an explicit RO/governance confirmation step to map each informal ordinal label to a distinct future identifier (flagged in the table, not resolved here — this is exactly the kind of "unresolved data" this task's own Step 8 asked to be surfaced, not invented). Row 3 (WP-03) requires a decision on whether its BLOCKED BAs (04/05) are included. Row 17 (WP-18) requires a decision on whether infra-only work registers as a Business Activity in the same sense as capability BAs.

**No registration, identifier assignment, or data reconstruction is performed by this document** — the table above is analysis, not action.

---

## 12. Existing (19 Closed/Certified) Business Activity Impact

- **Does retroactive registration require reopening implementation/certification status?** No — registration is a new, additive governance act (creating a BAR entry, per §4/§6), not a re-execution of any gate `CLAUDE.md §19.7b` already passed. It is **governance metadata retrofit only** — the same class of act CBOR's own registrations (`OFR-000001`, `CAC-000001`, `BIA-000001`, etc.) already performed for already-implemented, already-certified constructs without reopening any WP's own certification.
- **Does execution eligibility change?** ~~In principle, yes, per the LOCKED gate's own literal text (`COM-001-005`) — but D3.11's own unresolved question (whether the gate applies retroactively to already-executing BAs, or only prospectively) remains genuinely open and is not resolved by this design document; this design does not invent a grandfathering rule to answer it. This is the single most significant open item this design surfaces (§21).~~ *(Resolved 2026-09-21 by D8 — `ROD-ENTERPRISE-BAR §0g` — historical text preserved above, struck through, per this document's own no-silent-fix discipline.)* **No — not during the transition.** D8 (Option B, transitional gate) decided that execution eligibility for the 19 already-certified rows (and WP-20/WP-21) does **not** change until each is individually registered; they continue executing exactly as today. Only newly introduced/future Business Activities are subject to the eligibility gate immediately.
- **Is additional verification needed?** Only the RO/governance confirmations flagged in §11's own table (multi-BA mapping, BLOCKED-BA treatment, infra-BA treatment) — no additional testing or re-certification of the underlying implementation is implied.
- **Is an explicit transition decision still missing?** ~~Yes — precisely the execution-gate-retroactivity question above, and the retroactive-registration *sequencing*...~~ *(Partially resolved 2026-09-21 by D8.)* The execution-gate-retroactivity question itself is now decided (D8, transitional gate). **What remains open:** the retroactive-registration *sequencing* (single omnibus act vs. per-row, order) and the *eventual enforcement mechanism* for closing the D8 transition (D8 itself fixed no duration, deadline, or cutover point) — both flagged as open in §21, Open Issue 5, and not resolved here.
- **No certified WP is reopened. No certification record is modified.**

---

## 13. C-024 Impact

- **`D10` (BAR DEFERRED FOR BA-01 ONLY):** unchanged. This design does not convert it into registration-now, implementation authorization, or an enterprise exemption.
- **`BIA-000001`, WP-22, Charter:** unaffected.
- **Implementation status:** remains NOT STARTED.
- **How the enterprise BAR design interacts with BA-01 once implementation later begins:** once BA-01 is actually implemented (a future, separately authorized act), it would follow the same registration model (§4), identifier model (§5), and index (§6) this document designs for every other future Business Activity — at that point, `D10`'s own deferral would need to be revisited by whoever authorizes that implementation (a future act, not this document), consistent with `D10 §0`'s own text: "the `COM-001-060` execution-time obligation remains outstanding... deferred pending a future enterprise-level BAR-mechanism decision" — which this document's own D1–D7 chain *is* that future decision, now made, but BA-01's own case-by-case application of it remains a separate future act.
- **No actual conflict was found between this design and `D10`.** `D10` gates only C-024 BA-01's own *decision record*; it does not forbid this document from designing the enterprise mechanism `D10` itself anticipated. **No STOP condition applies; `D10` is not changed.**

---

## 14. Security / Authority Model

| Function | Authority | Reuses existing mechanism? |
|---|---|---|
| Who can create/register a Business Activity | The Repository Owner-authorized registering act (mirroring the CBOR-ADR pattern, §4) | Yes — the same governance-act pattern already used for `OFR-000001`/`CAC-000001`/`BIA-000001` |
| Who can modify registration state | The same registering-act authority, for any future state change | Same pattern |
| Who can consume registry information (read) | Any implementer/reviewer, mirroring `CBOR-INDEX.md`'s own open-read pattern (a "living document" any future IRA/WP consults, per its own §1 Purpose) | Yes |
| Who can execute a Business Activity | Ordinary business authorization (existing, per-endpoint mechanism — `require_platform_admin` and peers, or the `Backend/Runtime/AuthorizationEngine` where already integrated per WP-13) | Yes — **no new authorization architecture is created**; the BAR gate (§10) is a precondition layered in front of, not a replacement for, this existing mechanism |

**Registration authority, execution authorization, and business-user authorization are kept explicitly distinct** (§10's own four-way distinction, restated here for the authority dimension specifically) — a single caller class (Repository Owner / governance act) controls registration; a separate, already-existing mechanism controls execution authorization per caller.

---

## 15. Audit / Traceability

**Minimum required, per existing enterprise governance (not a new audit platform):**

- **Registration event** — when a Business Activity was registered, and by which act (§4's own `Registering act reference` and `Registration timestamp` fields).
- **Registration authority** — which governance act (ADR-equivalent) performed it (same field).
- **Identifier creation** — implicit in the registration event; no separate audit trail is proposed beyond the registration record itself.
- **Registration state change** — if the minimal two-state model (§4) ever needs a "deregistered/retired" transition (§16), that transition would need the same registering-act-authority pattern; not built now, since retirement is out of current scope (§16).
- **Execution-gate evidence** — reuses the existing `record_audit`/`publish_event` pattern already used throughout `AuthService`/`AIService` for every certified Business Activity to date (`[FACT]`, re-confirmed unchanged from the investigation's own §10 finding) — **no new audit mechanism is created**; a gate-denial event would be recorded the same way any other denied-authorization event already is.

**This does not reproduce the broader C-114 (Audit & Assurance) capability** — C-114 is a distinct, not-yet-implemented capability for cross-capability audit-trail querying/assurance/certification tracking as its own product (per the census artifacts' own explicit distinction, re-confirmed); BAR's own audit need is the narrow, per-registration-event trail described above, using the mechanism every other Business Activity already uses, not a new enterprise audit platform.

---

## 16. Failure / Edge Cases

| Case | Design-level handling |
|---|---|
| Duplicate registration attempt | Rejected at the registering act — collision-checked against the BAR index before registering, mirroring `ADR-041`'s own "Identifier collision-checked against `CBOR-INDEX.md`" practice |
| Identifier collision | Structurally prevented by a single sequential counter (§5); if ever detected, the registering act is invalid and must be corrected before proceeding — no automatic resolution invented |
| Invalid Business Activity reference (e.g., no corresponding Charter/`IMP-REPORT`) | Registration should not proceed without the mandatory fields (§4) resolvable from existing governance artifacts; flagged as a pre-registration data-completeness check, not a runtime error |
| Missing Work Package linkage | Same — a mandatory field (§4); registration blocked until resolved |
| Missing Charter linkage | Charter linkage is referenced where one exists (§4) — for the pre-2026 informal-Charter-convention rows (§11), the `IMP-REPORT-WP-XX` substitutes; not a blocking condition, since several already-certified WPs (1–15) predate the formal Charter convention |
| Already-implemented Business Activity | Explicitly the normal case for 18 of the 21 retroactive rows (§11) — registration is designed to accommodate this, not treat it as exceptional |
| Already-certified Business Activity | Same — registration does not reopen certification (§12) |
| Unregistered activity execution attempt | For a **future/new** Business Activity: denied per the execution gate (§10), immediately, once BAR is operational; exact denial mechanism not specified (design-level only). For one of D3's **21 existing** rows, before its own registration completes: **permitted**, per D8's own transitional gate (§10, §11) — this is not a "denial exception," it is the designed default state during the governed transition |
| Deregistration/retirement | **Explicitly out of current scope** — D2's own decided minimum does not include the fuller `§6.22.9` status lifecycle; if a future need arises, it would require revisiting D2 (not decided here) |
| Conflicting source records (e.g., `IMP-REPORT` and Charter disagree on BA count for a given WP) | Flagged as a pre-registration data-quality issue requiring the same RO/governance confirmation step already identified for the multi-BA rows in §11 — not resolved by this document, since resolving a specific historical discrepancy is a future, case-by-case act |

**Where the design requires a future governance decision, it is flagged in the relevant section above (§11, §12, §16) rather than resolved here**, consistent with this task's own instruction not to invent unsupported business-lifecycle semantics.

---

## 17. Existing Repository Gap — What Would Need to Be Created or Modified

| Category | Gap |
|---|---|
| BAR registration index/registry | ~~Does not exist — `BAR-INDEX.md` (§6) not yet created~~ *(Resolved 2026-09-22, Workstream A — `architecture/00-Governance/BAR-INDEX.md` built; zero registrations; Workstreams B–H remain not built)* |
| Business Activity Identifier support | No `BA-NNNNNN` namespace/counter exists anywhere |
| Registration service/mechanism | No registering-act tooling or convention exists yet for Business Activities (the CBOR-ADR pattern exists for Business Objects only) |
| Discovery integration | No Business Activity Engine exists generally (only the narrower Authorization Engine, `WP-RTA-001`) |
| Execution-gate integration | No gate currently checks BAR registration anywhere in `AuthService`/`AIService` |
| Retroactive registration tooling/data | No tooling exists to perform the §11 backfill; the data itself exists (in `IMP-REPORT`/`WPR-001`/Charters) but is not yet consolidated into a BAR-shaped record |
| Governance documentation | `IMP-001 §6.22.1b` could optionally be updated at a future D6 revisit (not performed here, since D6 = no amendment) to name `BA` as the adopted prefix once actually assigned |
| Tests | No BAR-specific test suite exists |
| Observability/audit hooks | Reuses existing `record_audit`/`publish_event` (§15) — no net-new hook category, only new call sites once the gate exists |

**None of these is created by this document.**

---

## 18. Implementation Architecture (design depth only — no code, schema, API, migrations, or runtime classes)

**Logical components:**
1. **BAR Registration Index** (§6) — the governance record (Markdown, `architecture/00-Governance/BAR-INDEX.md`, **built 2026-09-22, Workstream A, zero registrations**), plus, per the most plausible eventual shape, a runtime-queryable store for Engine use (not yet built).
2. **Business Activity Identifier Issuer** — a component (or convention) that assigns the next sequential `BA-NNNNNN` value (§5) at registration time.
3. **Registering Act mechanism** — the governed process (mirroring an ADR) by which a Business Activity is actually registered.
4. **Discovery Interface** — the query surface the (not-yet-built) Business Activity Engine would use against the BAR index (§9).
5. **Execution Gate** — the check layered in front of ordinary business authorization (§10, §14).

**Data flow (design-level):** Charter/`IMP-REPORT` (design-time source) → Registering Act (governance act, consults §4's mandatory fields) → BAR Registration Index (persists the record, issues the identifier per §5) → Discovery Interface (Engine queries the index) → Execution Gate (checks registration state before allowing ordinary authorization to proceed) → ordinary business authorization (existing mechanism, unchanged) → execution.

**Registration flow:** propose (cite Charter/`IMP-REPORT`/WP) → validate mandatory fields present → collision-check the next identifier → record in the index → (optionally) propagate to a runtime store.

**Discovery flow:** Engine queries the index (or its runtime store) by Activity Identifier / Capability / Domain — never by code inspection or naming convention (§9).

**Execution-gate flow:** on invocation attempt, check registration state in the index/runtime store → if registered, proceed to ordinary authorization → if not registered, apply D8's own transitional policy (§10): for a Business Activity newly introduced after BAR became operational, deny (mechanism unspecified, §10); for one of D3's 21 pre-existing rows still awaiting its own registration, permit execution to proceed as today, per the governed transition — this distinction (new-and-unregistered vs. pre-existing-and-not-yet-transitioned) is itself part of the gate's own logical design, not an afterthought bolted onto it.

**Retroactive registration flow:** for each of the 21 rows (§11), resolve unresolved data (multi-BA mapping, BLOCKED/infra treatment) → perform the registering act → record in the index — sequencing (batch vs. per-row) not fixed here.

**Relationships to `WPR-001`/Charter/CBOR:** by reference only (§7, §8) — no merge, no duplication of authoritative content.

**Integration points:** `AuthService`/`AIService` (wherever a Business Activity's own endpoint currently exists) would eventually need the execution gate layered in; no such integration is performed by this document.

**Security boundary:** registration authority vs. execution authorization vs. business-user authorization, kept distinct (§10, §14).

**Failure handling:** per §16.

**Test strategy (design-level, no tests created):** unit-level — identifier uniqueness/format validation, registration-record field completeness; integration-level — discovery correctly excludes unregistered activities, execution gate correctly denies unregistered activities and correctly permits registered ones, retroactive registration does not alter any existing certification artifact; per `CLAUDE.md §21.4`'s own Mandatory Tenant-Isolation Test Checklist, if and when the BAR mechanism's own runtime store carries any tenant-scoped data (currently, per D2's own scope, it does not appear to — BAR is platform-global metadata about Business Activities, not tenant data — flagged for confirmation at actual implementation time, not resolved here).

**Migration/backfill strategy:** the §11 retroactive-registration exercise itself, performed as a governance act (or a small number of acts) after the unresolved data points (§11's own table) are confirmed — not a database migration in the schema sense unless/until a runtime store (§6) is actually built.

**Rollout/transition approach:** prospective registration (new Business Activities) can begin as soon as the mechanism exists; retroactive registration (the 21 rows) can proceed independently and does not need to wait for or block prospective registration, since the two are logically independent acts using the same mechanism.

---

## 19. Implementation Work Breakdown

| Workstream | Deliverable | Dependencies | Test expectations | Gate | Rollback/containment |
|---|---|---|---|---|---|
| **A. BAR registry/index** | `BAR-INDEX.md` created, per §6's own shape — **IMPLEMENTED 2026-09-22, `architecture/00-Governance/BAR-INDEX.md`, READY FOR INDEPENDENT VERIFICATION; zero actual registrations** | D7 (decided) | Structural validation (row shape matches §4) — self-verified against D1–D9/the Charter, per this Workstream's own closing statement; independent verification still pending | Independent reviewer confirms shape matches this design | Low risk — a new file, additive |
| **B. Business Activity Identifier** | Issuer mechanism/convention for `BA-NNNNNN` (§5) — **IMPLEMENTED 2026-09-22: `models/bar_identifier_ledger.py`, `repositories/bar_identifier_repository.py`, `services/bar_identifier_service.py`, migration `a7b8c9d0e1f2` (`AuthService`), reusing the certified `[RO DECISION]` O1 application-level monotonic-allocator pattern (`MAX(suffix)+1`, UNIQUE-constraint backstop, allocate-and-retry) rather than a PostgreSQL SEQUENCE; ~~READY FOR INDEPENDENT VERIFICATION~~ *(synchronized 2026-09-28, Gate 5 C-2, `RRA-WP-23-AC` ST-13: independently verified at Gates 1, 2 and 4; Gate 5 PASS WITH CONDITIONS; ~~not yet accepted or committed~~ C-3 addendum, 2026-09-28: **accepted** (`IRA-WP-23-AC §0.2`) and committed with that record; not certified)*; zero identifiers issued to any of the 21 existing rows or to C-024 BA-01** | Workstream A | Uniqueness/format tests — **9/9 targeted tests passing** (format, deterministic sequencing, uniqueness across 25 issuances, a forced UNIQUE-collision retry, allocation-exhausted error handling, no `BAR-INDEX.md` mutation, no registration-field leakage); genuine multi-session async-concurrency testing against this repository's own SQLite test harness was attempted and found unreliable (disclosed in the test suite itself, mirroring `OfferingDefinitionService.establish`'s own identical, already-accepted `pragma: no cover` limitation) — ~~atomicity is instead proven deterministically via the forced-collision test~~ *(corrected 2026-09-28, ST-13: that test never actually collides (Gate 1 CERT-F-05, TD-172). Genuine-collision retry and atomicity were proven by the Gate 3 tests in `tests/test_bar_transaction_safety.py` and by independent probes at Gates 2, 4 and 5)* | Independent reviewer confirms no collision with any existing identifier namespace | Low risk |
| **C. Registration mechanism** | Registering-act convention (mirroring CBOR-ADR pattern) — **IMPLEMENTED 2026-09-22: `models/bar_registration.py`, `repositories/bar_registration_repository.py`, `services/bar_registration_service.py`, migration `b8c9d0e1f2a3` (`AuthService`), FK-linked to the Workstream B ledger for identifier integrity, UNIQUE-constrained on `(owning_work_package, business_activity_reference)` for duplicate protection; ~~READY FOR INDEPENDENT VERIFICATION~~ *(synchronized 2026-09-28, ST-13: independently verified at Gates 1, 2 and 4, including the Gate 3 remediation of VV-F-01/VV-F-02; Gate 5 PASS WITH CONDITIONS; ~~not yet accepted or committed~~ C-3 addendum, 2026-09-28: **accepted** (`IRA-WP-23-AC §0.2`) and committed with that record; not certified)*; zero real Business Activities registered — every test registration uses synthetic `WP-TEST-*` data, never any of the 21 existing rows or C-024/WP-22** | Workstreams A, B | Governance-artifact review (does the act properly cite Charter/`IMP-REPORT`/WP) — **13/13 targeted tests passing** (mandatory-field persistence, duplicate protection via a real DB constraint plus a friendlier-error pre-check, ~~a forced identifier collision retried across both the ledger and registration inserts together,~~ *(corrected 2026-09-28, ST-13: that test never actually collides (CERT-F-05, TD-172); genuine-collision retry across both inserts is proven by the Gate 3 tests and by independent probes at Gates 2, 4 and 5)*, allocation-exhausted leaves no partial state, no `BAR-INDEX.md` mutation); the identifier-issuance-plus-registration atomicity is achieved by sharing one session/transaction across both repositories (enforced defensively in the service's own constructor), not by composing two independently-committing service calls | Repository Owner authorization per act | ~~Low risk — governance-only, no runtime~~ *(Correction 2026-09-25, RD-23-04; see the note below this table:)* Low risk — additive; includes the runtime registration store (not a runtime consumer, gate or discovery path) |
| **D. Discovery integration** | Engine query surface against the index/store (§9), scoped per D8: excludes unregistered future BAs; does not intercept the 21 existing rows' own current invocation path until each individually cuts over (§19a) | Workstreams A–C; depends on whether/when a general Business Activity Engine is built (currently only the narrower Authorization Engine exists) — a genuine engineering dependency, not a governance blocker (D8 resolved the governance question, `ROD-ENTERPRISE-BAR §0g`; §19a resolved the cutover-mechanism implementation-planning question) | Discovery excludes unregistered *future* activities; verified to leave each not-yet-cutover existing row's own current route untouched | Independent V&V per `CLAUDE.md §19.7b` | Moderate — ~~first actual runtime component~~ *(Correction 2026-09-25, RD-23-04:)* first runtime **consumer** component (Business Activity Engine / discovery integration; **not implemented**); contain by feature-flagging discovery-gated paths |
| **E. Execution gate** | Gate layered in front of existing authorization (§10, §14), implementing D8's own transitional policy per §19a's own per-BA cutover mechanism (immediate for future BAs; deferred, per individual row, for each of the 21 existing rows until *that row's own* §19a.5 flow completes) | Workstream D; the D8 governance question is resolved (`ROD-ENTERPRISE-BAR §0g`) and the cutover mechanism is now specified (§19a — per-BA, no new RO decision required) — remaining dependencies are ordinary engineering ones: building the per-row state tracking (§19a.6) and verification checks (§19a.8) | Gate denies unregistered *future* activities, permits activities that have individually completed §19a.5's own cutover flow, and does not deny any not-yet-cutover existing row, without breaking existing authorization behavior | Full regression suite must pass; independent V&V | Moderate — touches every existing Business Activity's own execution path, but D8's own transitional default plus §19a's own per-row independence (a failure or delay on one row does not affect the other 20, §19a.7) removes the highest-risk failure mode this workstream previously carried |
| **F. Retroactive 21-BA registration** | All 21 rows individually registered per §19a.5's own per-BA cutover flow (minus row 21/C-024, which stays prospective, §19a.9); 14 of 21 rows have no unresolved data and can proceed immediately, 7 require the §11-flagged confirmation first (§19a.5) | Workstreams A–C; the 7 rows' own §11/§21 data confirmations | Verify no certification record was altered; verify each cutover row independently satisfies §19a.8's own six criteria before being marked Registered (BAR-Gated) | Independent reviewer confirms no reopening of any WP's own certification, per-row | Low risk — additive, per-row governance records; a single row's own failure (§19a.7) does not affect the other 20, and is reversible by removing that one entry |
| **G. Governance/test/assurance** | Test suite (§18), audit-hook wiring (§15), optional `IMP-001 §6.22.1b` update flagged for a future D6 revisit | Workstreams A–F | Per `CLAUDE.md §19.7b`'s own five-gate sequence | Same gate sequence | Low risk |
| **H. C-024 integration readiness** | No action now — BA-01 remains prospective (§13); this workstream exists only to confirm, at the time BA-01 is actually implemented, that it follows Workstreams A–C's own established mechanism | D10 (unchanged) | N/A until BA-01 implementation is separately authorized | A future, separate governance act | N/A |

*(Correction note, 2026-09-25 — Repository Owner decision **RD-23-04**, resolving Gate 1 finding CERT-F-01. Recorded in `IRA-WP-23-AC_BAR_Workstreams_A-C_Closure_Readiness.md §0`; the same correction is applied to WP-23 Charter §21. The original wording of rows C and D is preserved above, struck through.)*
- **Ratification.** The runtime construction already performed under Workstreams B and C is ratified as within this design's boundary. §6 had delegated the runtime-store question to Workstreams C/D. Workstream C accordingly includes the runtime BAR registration store and mechanism already built.
- **Workstream D** remains the Business Activity Engine / discovery integration, the first runtime *consumer*, and is **not implemented**.
- **RD-23-03's layered authority model remains authoritative:** the registering act is the governance authority; `bar_registration` is the runtime record; `BAR-INDEX.md` is the governance catalogue; reconciliation remains required.
- **No additional Workstream D or E behaviour, registration, gating or new runtime behaviour is authorized** by this correction.

**If a new Work Package is required to execute Workstreams A–G, that requirement is identified here — it is not silently created.** This document does not register a new WP; a future Repository Owner decision would need to charter one (or fold the work into an existing/upcoming WP), per `CLAUDE.md §21`'s own Standard Work Package Lifecycle. **See §19a below for the specific Work Package question, resolved as far as this implementation-planning stage can resolve it.**

---

## 19a. Transition Cutover Mechanism (added 2026-09-22, implementation-planning determination — not a new enterprise governance decision)

### 19a.1 — D8 Baseline (restated, not altered)

D8 (`ROD-ENTERPRISE-BAR §0g`): existing Business Activities continue executing during a governed transition; only newly introduced/future Business Activities are gated immediately once BAR is operational; all 21 existing rows remain subject to D3's own registration obligation, undischarged until performed; no permanent exemption; no transition duration, deadline, or cutover mechanism was fixed by D8 itself — that determination was explicitly left to this stage.

### 19a.2 — Cutover Problem Statement

By what concrete operational mechanism does an individual existing Business Activity move from "continues executing under D8's own transitional treatment" to "BAR-registered, subject to the normal execution gate"? This is an implementation-planning question about *how* D3+D8 are executed, not a re-opening of *whether* they apply — D3 and D8 are treated as fixed inputs throughout this section.

### 19a.3 — Options Considered

**OPTION A — Per-BA cutover.** Each existing Business Activity is independently: (1) data-validated against §11's own mandatory fields, (2) registered in BAR, (3) assigned its own identifier by BAR at that registration act (D5), (4) verified, (5) moved from transitional treatment to normal BAR-gated execution — the moment its own registration completes, independent of every other row's own progress.

**OPTION B — Single enterprise cutover.** All 21 rows are prepared and validated first; the complete population is registered/activated together; one controlled switch moves every row from transitional treatment to BAR-gated execution simultaneously.

**No third, materially distinct mechanism was found in the repository's own architecture or evidence** — a "batched-by-capability" or "batched-by-Work-Package" variant would be a partitioning of Option B (grouping some, not all, rows into one cutover event) rather than a materially different mechanism; not manufactured as a separate option here.

### 19a.4 — Evidence and Constraints (why this does not require a new Repository Owner decision)

**Per the governing instruction for this task, escalation to a new RO decision is warranted only if an actual LOCKED requirement or already-decided governance boundary prevents choosing the mechanism at implementation level. None was found — instead, the already-decided text itself points to Option A:**

- `COM-001-005` (`[LOCKED]`), re-read again for this section: *"No commercial Business Activity shall be executed until registered in the BAR."* The obligation's own grammatical subject is singular — **one** Business Activity, gated on **its own** registration — not a population-wide condition requiring every member of a cohort to be ready before any one of them is gated. Nothing in this text, or in `PLT-001-004`/`GRC-001-008`'s identical formula, ties one Business Activity's own gate to another's own registration status.
- `D5` (`ROD-ENTERPRISE-BAR §0d`, `[RO DECISION]`, already made, not reopened here): the identifier is "assigned **at BAR registration**" — a per-registration-event trigger, not a batch trigger. Re-reading D5's own text confirms no population-wide gating concept exists anywhere in that decision.
- `D8`'s own recorded text (`ROD-ENTERPRISE-BAR §0g`, re-read again for this section): the transition ends for a given row "until **each is individually, retroactively registered**" — D8's own decision record already uses individual-row language, not cohort language. This is not this document's own invention; it is the already-decided text's own framing, re-confirmed by direct re-reading, not paraphrased differently now to fit a preferred answer.
- `§11`'s own inventory (this document) already shows most of the 21 rows (14 of 21 — see §11) have no unresolved data at all; only 7 rows carry a flagged confirmation item (multi-BA mapping, BLOCKED-BA treatment, infra-BA treatment). A single-cutover mechanism would force the 14 already-ready rows to wait on the 7 that are not — a consequence no LOCKED text, and no D1–D8 decision, requires.

**Conclusion: Option A (per-BA cutover) is the selected mechanism.** This is stated as an engineering/implementation-planning determination, grounded directly in D3/D5/D8's own already-decided text, not as a new `§14`-or-`D8`-class Repository Owner decision — no new RO decision is created or required for this determination.

**Evaluated against the required criteria (Option A vs. Option B, technical characteristics only):**

| Criterion | Option A (per-BA) | Option B (single cutover) |
|---|---|---|
| Operational continuity | High — no row's own cutover is held hostage to another's own readiness | Lower — a single lagging row (e.g., one of the 7 flagged in §11) blocks all 21 |
| Dependency on complete data | None — each row proceeds independently once its own data is confirmed | Full — requires all 21 rows' data resolved before any cutover occurs |
| Partial-failure handling | Contained to the one failing row (§19a.7) | A single failure can stall the entire population's own cutover |
| Rollback/containment | Per-row — removing or correcting one entry does not affect the other 20 | Population-wide — a rollback affects all 21 simultaneously |
| Effect on WP-20/C-021, WP-21/C-022 | Each proceeds on its own confirmed-ready timeline (§11: no unresolved data for either) | Both would wait on the 7 flagged rows regardless of their own readiness |
| Effect on WP-22/C-024 | Not applicable — BA-01 is not part of the 21 (§19a.9) | Same — not applicable |
| Observability | Each row's own transition state is independently trackable | Only a single population-wide state is meaningful until cutover |
| Verification | Per-row acceptance criteria (§19a.10) evaluated independently | Requires all 21 rows to pass verification before any row's own gate activates |
| Recovery after failed registration | Retry the single affected row; the other 20 are unaffected | Retry blocks the entire population's own cutover until resolved |
| Compatibility with D8 | Direct — D8's own text already uses "each... individually" language | Requires reading D8's own "individually" language as merely descriptive, not operative — a strained reading |
| Complexity | Lower — no cross-row synchronization/coordination logic needed | Higher — requires coordinating readiness across all 21 rows before any cutover |
| Executable without reopening certification | Yes — identical to Option A/B either way (§12, unaffected by cutover mechanism choice) | Same |

No subjective label beyond these named technical characteristics is applied; Option A is not called "better" in the abstract — it is selected because it satisfies every listed criterion at least as well as Option B, and strictly better on operational continuity, partial-failure containment, and direct textual compatibility with D5/D8's own already-decided per-row framing.

### 19a.5 — 21-BA Transition Flow (Option A, applied to the actual inventory)

For each of the 21 rows in §11's own table:
1. Confirm the row's own mandatory data (§4) is resolvable from existing governance artifacts (`IMP-REPORT`/`WPR-001`/Charter) — **14 of 21 rows already satisfy this with no confirmation needed** (rows 4, 6, 7, 8, 9, 13, 14, 15, 16, 18, 19, 20, per §11's own "Unresolved data: None" column); 7 rows require the specific confirmation already flagged in §11 (rows 1, 2, 3, 5, 10, 11, 17) before *their own* registration can proceed — this does not block the 14 ready rows.
2. Perform that row's own registering act (Workstream C).
3. BAR assigns that row's own `BA-NNNNNN` identifier at that act (D5, Workstream B).
4. Record the entry in the BAR index (Workstream A).
5. Verify per §19a.10's own criteria.
6. That row's own execution now proceeds under the normal BAR execution gate (Workstream E) — it exits transitional treatment individually, without waiting for or affecting any other row.

**Row 21 (C-024/WP-22) is excluded from this flow entirely** — it is NOT STARTED, not part of the transitional-execution population D8 governs (§19a.9).

### 19a.6 — Registration/Cutover State Model (minimum states only, per this task's own instruction not to invent unneeded business lifecycle)

Three states are needed, and no more — this does **not** reintroduce `IMP-001 §6.22.9`'s own six-state lifecycle, which D2/D6 already excluded from BAR's decided scope:

| State | Meaning | Kind |
|---|---|---|
| **Not Registered (Transitional)** | The row's current, actual state today — executes via its own existing route, unaffected by the future gate, per D8 | **Governance state** — this is exactly D2's own two-state "not registered" value (§4); D8 supplies the execution consequence attached to it |
| **Registration Pending** | An operational, internal tracking convenience for the cutover exercise itself (e.g., "data confirmed, registering act not yet performed") | **Operational transition state only** — not a BAR registration-record field, not a business lifecycle state, exists purely to track the exercise's own progress across the 21 rows |
| **Registered (BAR-Gated)** | The row's registering act has completed; identifier assigned; BAR index entry exists; normal execution gate now applies | **Governance state** — exactly D2's own two-state "registered" value (§4) |

**No new Business Activity business-lifecycle state is created.** "Registration Pending" is scaffolding for the cutover exercise's own project tracking, not a value ever written into the BAR registration record's own `Registration status` field (§4), which remains binary.

### 19a.7 — Failure / Partial-Completion Handling

| Scenario | Handling |
|---|---|
| 18 of 21 register successfully; 3 fail data validation | The 18 successful rows proceed to BAR-Gated individually (§19a.5); the 3 failing rows remain in Not Registered (Transitional) — still executing under D8, not exempted, not blocked, simply not yet advanced |
| One BAR identifier assignment fails (e.g., a collision, per §16) | That single row's own registering act is corrected and retried (§16); it does not affect any other row's own already-completed or in-progress registration |
| A source record conflicts (e.g., `IMP-REPORT` and Charter disagree) | That row remains in Not Registered (Transitional) pending the same RO/governance confirmation step already identified in §11/§16 for conflicting records — not resolved by this section, consistent with "do not invent missing mappings" |
| A previously certified BA cannot be reconstructed cleanly | Same — remains Transitional until the underlying data question is resolved; its own certified status and continued execution are unaffected either way (§12) |

**No incomplete row silently becomes permanently exempt.** Every row remaining in Not Registered (Transitional) is, by construction, still fully subject to D3's own registration obligation and D8's own transitional (not exempt) framing — this section does not invent a new governance exemption for rows that fail or stall; it only confirms that Option A's own per-row independence prevents one row's own failure from freezing the other 20's own progress.

### 19a.8 — Verification / Cutover Criteria (per-row, minimum, no unnecessary business requirements added)

A row moves from Registration Pending to Registered (BAR-Gated) only when all of the following hold:
1. A BAR registration entry exists for that row in the index (§6).
2. A canonical `BA-NNNNNN` identifier has been assigned to it (§5).
3. The mandatory registration data (§4) is present and internally consistent (no conflicting source records, §16).
4. The row is discoverable through the BAR-mediated discovery path (§9) — confirming the discovery integration itself recognizes the new entry.
5. The execution-gate check (§10) can be evaluated for that row and correctly returns "eligible."
6. Verification evidence (the registering act's own record, §14/§15) exists and is retrievable.

No additional business requirement (e.g., a fresh manual sign-off beyond the registering act itself, or a waiting period) is added beyond these six criteria, consistent with this task's own instruction not to create unnecessary business requirements.

### 19a.9 — C-024 Treatment

C-024 BA-01 is **not** part of the 21-row transitional population this section governs — it is NOT STARTED, not currently executing (§11, row 21; §13). `D10` (`ROD-C024-BAR §0`, deferred, C-024 BA-01 only) is unaffected, unaltered, and not reinterpreted by this section. No identifier is assigned to BA-01. No registration occurs for BA-01. The Charter is unchanged. Once BA-01 is actually implemented (a future, separately authorized act), it would be a **future** Business Activity relative to whenever BAR goes live, gated immediately under D8's own future-BA branch — it would use the same registering-act mechanism (Option A's own per-BA flow, §19a.5) as any other future Business Activity, not the transition-cutover mechanism this section designs for the 21 pre-existing rows specifically.

### 19a.10 — Future-BA Treatment (D8 preserved, no bypass created)

Any Business Activity introduced after BAR becomes operational must be BAR-registered before execution — immediately, per D8's own future-BA branch, with no transitional treatment of any kind. The cutover mechanism this section designs (§19a.3–§19a.8) applies **only** to D3's own 21-row existing population; it creates no permanent bypass, no new exemption class, and no precedent for treating any future Business Activity as "transitional."

### 19a.11 — Remaining Implementation Dependencies

- The 7 rows' own data-confirmation items (§11/§21 Issues 2–4) — genuine prerequisites for *those specific rows'* own registration, not for the cutover mechanism itself, which is now fully specified.
- Workstreams A–E's own actual engineering build (§18/§19) — the mechanism is designed; it is not yet built.
- Whether/when the general Business Activity Engine is built (Workstream D's own dependency, unaffected by this section).
- A new Work Package decision (§19a.12 below).

### 19a.12 — Work Package Question (identified, not executed)

`WPR-001`'s own current structure (highest registered: `WP-22`, re-confirmed by direct inspection for this section) contains no existing Work Package whose own chartered scope covers building the enterprise BAR mechanism — every existing WP is either a specific capability's own Business Activity (WP-01–WP-12, WP-14–WP-22) or a narrowly-scoped cross-cutting runtime effort (`WP-13` Authorization Runtime Integration, `WP-RTA-001` Authorization Runtime Engine), neither of which charters a Business-Activity-Registry-building effort. **A new Work Package genuinely appears to be required**, following the same precedent `WP-13`/`WP-RTA-001` already established for cross-cutting, non-single-capability platform mechanisms:

- **Purpose:** build the enterprise BAR mechanism per Workstreams A–H (§18/§19).
- **Scope:** BAR registration index (A), Business Activity Identifier issuance (B), registration mechanism (C), discovery integration (D), execution gate (E), retroactive 21-BA registration/cutover per §19a (F), governance/test/assurance (G), C-024 integration readiness confirmation only (H).
- **Proposed next-number candidate:** `WP-23` — the next sequential, unassigned number following `WP-22`, the current highest registered entry in `WPR-001`. This is a candidate identification only, not a reservation or registration.
- **Why needed:** no existing WP's own charter covers this cross-cutting, multi-capability mechanism; `CLAUDE.md §21`'s own Standard Work Package Lifecycle requires a Charter + IRA before implementation begins for work of this shape, mirroring exactly how `WP-13` and `WP-RTA-001` were each separately chartered for their own cross-cutting runtime work rather than folded into any single capability's own WP.

**This is an identification only. No WP is registered, reserved, or chartered by this section.** A future Repository Owner decision would need to authorize it, per `CLAUDE.md §21`.

---

## 20. Test Strategy

Covered inline per workstream (§18/§19). Summary: unit tests for identifier format/uniqueness and registration-record completeness; integration tests for discovery-exclusion and execution-gate behavior; regression tests confirming no existing certified Business Activity's own execution path breaks; a tenant-isolation checklist item flagged for confirmation (not currently expected to apply, since BAR is platform-global metadata, not tenant-scoped data) per `CLAUDE.md §21.4`.

---

## 21. Open Issues (explicit, not silently resolved; updated 2026-09-22)

1. ~~**Execution-gate retroactivity** (§12) — does the gate apply to the 21 existing Business Activities' own *continued* execution before they are individually registered, or only once registered, or only to future Business Activities? This is the single most consequential open question this design surfaces — Workstream E (§19) cannot be safely built without an answer.~~ **RESOLVED 2026-09-21 — see D8 (`ROD-ENTERPRISE-BAR §0g`).** A transitional gate applies: the 21 existing rows continue executing until individually registered; future Business Activities are gated immediately. Historical text preserved above, struck through, per this document's own no-silent-fix discipline.
2. **Multi-BA mapping for informal Charters** (§11, rows 1/2/4/5/10/11) — which informal ordinal labels become distinct `BA-NNNNNN` identifiers, requiring RO/governance confirmation. *(Still open.)*
3. **BLOCKED-BA treatment** (§11, row 3, WP-03 BA-04/05) — register or exclude. *(Still open.)*
4. **Infra-only-BA treatment** (§11, row 17, WP-18) — whether repository-wide infrastructure work registers as a Business Activity in the same sense as capability-scoped ones. *(Still open.)*
5. ~~**Retroactive-registration sequencing and D8 transition cutover mechanism** (§11/§18, Workstream F; §10, §19 Workstream E) — single omnibus act vs. per-row registration ordering, and the eventual enforcement mechanism for closing D8's own transition — D8 itself fixed no duration, deadline, or cutover mechanism.~~ **RESOLVED 2026-09-22 — see §19a.** Per-BA cutover selected as an implementation-planning determination (not a new Repository Owner decision), grounded directly in `COM-001-005`/D5/D8's own already-decided per-row text (§19a.4). Each of the 21 rows transitions independently upon completing its own registering act; no population-wide waiting condition exists. Historical text preserved above, struck through, per this document's own no-silent-fix discipline.
6. **Runtime-store necessity and timing** (§6, §18 Workstream D) — whether/when a database-backed store is built alongside the Markdown index, and how it relates to the still-unbuilt general Business Activity Engine. *(Still open.)*
7. **New Work Package requirement** (§19, §19a.12) — whether Workstreams A–G need a new, separately chartered WP. *(Still open as a formal chartering action — but the requirement itself is now identified, with a proposed next-number candidate `WP-23`, per §19a.12; only the Repository Owner's own act of chartering it remains, not a design question.)*

**Issues 1 and 5 are resolved (D8, §19a respectively). Issues 2–4 remain open, unchanged by this synchronization pass. Issue 6 remains open. Issue 7 is now precisely identified (§19a.12) though the chartering act itself remains a future Repository Owner step — none of the remaining items is resolved by this document; each requires either an ordinary data-confirmation/chartering step or a future engineering-planning pass, and none is answered by assumption here.**

---

## 22. Implementation Readiness (reassessed 2026-09-22, following D8 and §19a's cutover-mechanism determination)

**Classification: READY WITH CONDITIONS — no remaining governance question; only ordinary implementation-planning/administrative steps remain.**

All eight enterprise BAR decisions (D1–D8) are recorded, and the one implementation-planning ambiguity the original design surfaced (the transition cutover mechanism) is now fully specified (§19a) without requiring a new Repository Owner decision — Option A (per-BA cutover) was selected as an engineering determination grounded directly in D3/D5/D8's own already-decided text.

Workstreams A, B, C, F, and G (registry, identifier, registration mechanism, per-BA retroactive cutover, governance/test scaffolding) are ready to support a future implementation authorization **without further governance decisions**, once the 7 rows' own §11/§21 data-confirmation items (Issues 2–4) are resolved — and, per §19a.5, the other 14 rows have no such dependency and can proceed independently.

**Workstreams D and E (discovery, execution gate) are no longer blocked by any open governance or cutover-mechanism question** — D8 resolved the temporal-reach policy; §19a resolved the mechanism by which that policy is operationally executed. **Genuine remaining conditions, distinct from both now-resolved questions:**
- whether/when a general Business Activity Engine is built at all (Workstream D's own engineering dependency, unaffected by D8/§19a);
- building the per-row state tracking (§19a.6) and verification checks (§19a.8) that implement the now-specified cutover mechanism;
- full regression testing confirming the gate's own new-vs-existing, per-row distinction is correctly implemented before production rollout;
- the 7 rows' own data confirmations (§11/§21 Issues 2–4) — a condition on completing *those specific rows'* own cutover, not on building the mechanism itself, which applies uniformly to all 21.

**The one remaining item that is not purely engineering detail: a Work Package must be chartered before implementation begins**, per `CLAUDE.md §19`'s own Implementation Start Checklist — this is not a design gap (the design, including the cutover mechanism, is complete) but the ordinary procedural gate every prior Work Package in this repository has passed through. §19a.12 identifies the requirement and a candidate number (`WP-23`); it does not charter it.

**No new governance decision is manufactured** — every remaining item listed above is either ordinary engineering work, ordinary data confirmation, or the standard WP-chartering procedure already required for every prior Work Package; none is elevated to a `§14`-, `D8`-, or `D9`-class enterprise decision.

Workstream H (C-024 integration readiness) requires no action until BA-01's own implementation is separately authorized.

---

## 23. Traceability to D1–D8

| Design element | Decision(s) traced to |
|---|---|
| §3 (responsibility boundary), §4 (registration model) | D2 |
| §5 (identifier model) | D5, `SD-002-004` |
| §6 (index model), §7 (`WPR-001` relationship) | D7 |
| §11 (retroactive strategy) | D3 |
| §9 (discovery) | D2, `RTA-001 §6.6`, D8 (transitional carve-out) |
| §10 (execution gate) | D2, `COM-001-005`/`PLT-001-004`/`GRC-001-008`, D8 (temporal reach) |
| §17 (`§6.22.1b` future-update flag only, no amendment now) | D6 |
| §13 (C-024 impact) | `C-024 D10`, unchanged |
| §1 (establishment premise) | D1 |
| §12, §16, §18 (execution-gate temporal reach, existing-vs-future distinction), §19 Workstreams D/E, §21 Issue 1 (resolved), §22 (readiness reassessment) | D8 |
| §19a (transition cutover mechanism), §19 Workstreams D/E/F (updated), §21 Issue 5 (resolved), §21 Issue 7 (identified), §22 (reassessed) | Implementation-planning determination grounded in D3/D5/D8 — not a new enterprise decision |
| D4 | Moot — no design element traces to it |

---

## 24. Self-Review (updated 2026-09-22 following the D8 synchronization pass and the §19a cutover-mechanism determination)

- **D1–D8 were re-confirmed against source before this update, not assumed** (§1, §2). **Confirmed.**
- **No settled decision was reopened or re-litigated** — D8's own recording, and D1–D7 before it, are treated as decided input, not revisited; no source conflict was discovered during design, the D8 synchronization pass, or the §19a cutover-mechanism determination that would require reopening any of D1–D8. **Confirmed.**
- **Every current (non-struck-through) statement in this document is consistent with D8 and §19a** — the prior "execution-gate retroactivity is unresolved" language (§12, §16, §18, §19 Workstream E, §21 Issue 1, §22) and the prior "cutover mechanism is unresolved" language (§19 Workstream E/F, §21 Issue 5, §22) were each searched for and updated, with original wording preserved only in struck-through, explicitly-dated historical form. **Confirmed, per direct re-check of every section listed.**
- **D3 still requires all 21 existing rows to eventually register** — unchanged by this update (§11's own table is byte-for-byte the same as the original design pass). **Confirmed.**
- **Existing Business Activities continue executing during the transition; future Business Activities are gated immediately; no permanent exemption was introduced; no deadline/cutover date was invented** — each stated explicitly in §10/§11/§12/§16/§18/§19a/§21/§22. **Confirmed.**
- **The per-BA cutover mechanism (§19a) was selected as an engineering/implementation-planning determination, not a new Repository Owner decision** — grounded directly in `COM-001-005`'s own singular-subject text, D5's own per-registration-event trigger, and D8's own "each... individually" language, each re-read and cited, not paraphrased to fit a preferred answer (§19a.4). **Confirmed.**
- **The known unresolved 21-BA data items (multi-BA mapping, BLOCKED-BA treatment, infra-BA treatment) are preserved exactly, not silently resolved** — §19a.5 explicitly separates the 14 ready rows from the 7 flagged ones without inventing any missing mapping. **Confirmed.**
- **Partial-completion/failure handling exists and does not create a new exemption** — §19a.7 confirms every stalled or failed row remains in Not Registered (Transitional), still fully subject to D3, never silently exempted. **Confirmed.**
- **Workstreams D, E, and F are no longer shown as blocked by either the D8 governance question or the cutover-mechanism question** — §19's own rows for D/E/F were rewritten to reflect §19a's own resolution, while their genuine remaining engineering dependencies (Engine build timing, per-row state-tracking/verification build-out, regression testing, the 7 rows' own data confirmations) are preserved, not silently dropped. **Confirmed.**
- **The new-Work-Package requirement is identified (§19a.12, candidate `WP-23`) but not executed** — no WP was registered, reserved, or chartered. **Confirmed.**
- **No new governance decision was manufactured** — the remaining engineering/administrative details named in §19a.11/§21/§22 are implementation-planning or ordinary-chartering work, not elevated to `§14`-, `D8`-, or `D9`-class decisions. **Confirmed.**
- **The design implements exactly the D2-decided minimum scope** — §3's own boundary matrix explicitly excludes every broader `§6.22` responsibility not adopted. **Confirmed.**
- **BAR is confirmed as the canonical identifier authority (D5)**, and identifiers are assigned at BAR registration (§5) — no earlier assignment point is designed. **Confirmed.**
- **All 21 rows of D3's retroactive population are represented** (§11), with unresolved data explicitly flagged, not invented. **Confirmed.**
- **A separate BAR registration index is preserved** (§6, §7) — `WPR-001` is not modified or merged. **Confirmed.**
- **`WPR-001` remains WP-governance-only; CBOR remains Business-Object governance** (§7, §8). **Confirmed.**
- **D6's no-amendment decision is preserved** — `IMP-001` is not modified; only a future, separate D6-revisit is flagged as optional (§17), not performed. **Confirmed.**
- **`C-024 D10` remains unchanged** — no registration, identifier assignment, or Charter change occurred for BA-01 (§13). **Confirmed.**
- **No Business Activity Identifier was assigned; no Business Activity was registered; no BAR implementation (code/schema/API/migration/test/frontend) occurred.** **Confirmed.**
- **Anti-scope-drift check:** BAR was not designed as an ERP, CRM, general workflow engine, broad authorization platform, general audit platform, `WPR-001` replacement, CBOR replacement, or a full `§6.22` implementation — §3's own boundary matrix and §14/§15's own "reuse existing mechanism" findings confirm this throughout. **Confirmed.**

*End of Enterprise BAR Mechanism Design and Implementation-Readiness Package, synchronized 2026-09-22 to reflect D8, the §19a transition-cutover-mechanism determination, `WP-23`'s own chartering/registration, and Workstreams A, B, and C's own implementation. `COM-001`, `CMD-001`, `IMP-001`, `SD-002`, `PLT-001`, `GRC-001`, `RTA-001`, `CLAUDE.md`, `WPR-001`, `CBOR-INDEX.md`, and all eight D1–D8 decision records were read, not modified. **`BAR-INDEX.md` (Workstream A), the `bar_identifier_ledger` model/repository/service/migration (Workstream B), and the `bar_registration` model/repository/service/migration (Workstream C, `AuthService`) have all been built — 2026-09-22 — with zero real Business Activities registered and zero identifiers issued to any of the 21 existing rows or to C-024 BA-01.** No API or execution-runtime component (Workstreams D/E) was created. `C-024 D10` unchanged, scoped only to C-024 BA-01. D8 (`ROD-ENTERPRISE-BAR §0g`) resolved Open Issue 1 — a transitional gate. §19a resolved Open Issue 5 — per-BA cutover. Implementation readiness: Workstreams A, B, and C — IMPLEMENTED, READY FOR INDEPENDENT VERIFICATION; Workstream F ready pending ordinary data confirmation for 7 of 21 rows (Open Issues 2–4); Workstreams D/E ready pending genuine engineering dependencies (Engine build timing, per-row tracking/verification build-out, regression testing — Open Issue 6); Workstream H requires no action until C-024 BA-01's own future implementation. Nothing staged, committed, or pushed.*
