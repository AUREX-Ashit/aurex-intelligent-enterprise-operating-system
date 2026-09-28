# ROD-BAE-001-M2 — Business Activity Identifier → Implementation Binding: Decision Preparation (RD-M2-02)

**Work Package:** `WP-BAE-001`, milestone M2 (Business Activity Resolution & BAR Integration)
**Prepared:** 2026-09-25, per the Repository Owner's RD-M2-02 instruction (`IRA-BAE-001-M2 §0`): "Prepare a narrow decision artifact … Do not select an option. Do not implement any option."
**Status:** ~~**DECISION PREPARATION — NO OPTION SELECTED.** No ADR is created.~~ `ADR-042` is not modified. No code, schema, migration, manifest, binding, registry, file format or test is created. ~~*(Updated 2026-09-28, §0: **READY FOR DECISION** — still no option selected; RD-M2-02 remains OPEN.)*~~ *(Updated 2026-09-28, §0.6.)* **DECIDED — Option B2 (governed persistent binding registry), by the Repository Owner. Recorded in `ADR-043_Business_Activity_Identifier_Implementation_Binding.md`.** The analysis in §0–§7 is preserved as presented for decision. No implementation is authorized.

---

## 0. Decision-Readiness Reassessment (2026-09-28)

**Performed** by Repository Owner instruction: "Proceed only with the RD-M2-02 decision-preparation step … Determine whether the previously open RD-M2-02 decision … can now be resolved based on the current committed repository state. Do NOT begin M2 implementation." The reassessment was made against HEAD `bae8350b89771c48ad0b9acd57c829cdb62be615`. §1–§7 below are preserved as prepared on 2026-09-25, apart from two dated annotations (§3 and §6).

### 0.1 The question (unchanged, §1)

What is the authoritative, governed mechanism by which a BAR-issued Business Activity Identifier (`BA-NNNNNN`) is bound to the executable implementation the Business Activity Engine will run? The documented options are unchanged (§4):
- **A:** host-service start-up binding table;
- **B:** governed registry, in two forms: **B1** documented (+ realization) and **B2** persistent (+ realization);
- **C:** capability-contributed, BAE-owned fail-fast registry.

No option is added.

### 0.2 Evidence now available

**1. WP-23 A–C is committed and accepted.**
- Commit `b0f5a12e84a9a3f7d9622bcbea4cee87b934be85`; acceptance record `IRA-WP-23-AC §0.2`; C-4 reconciliation `bae8350`.
- The `bar_registration` evidence row in §3 was "untracked, unverified" when written. It is now committed and independently verified (Gates 1–5), and `BarRegistrationRepository.get_by_identifier` exists at HEAD.
- The persistent-registry precedent cited for B2 is therefore now valid repository evidence.

**2. The WP-23 authority question that §6 said "may inform this one" is decided.**
- It was RD-23-03, Option D (layered), recorded in `ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md §0`:
  - the governance record (the registering act) is the authority;
  - the runtime record (`bar_registration`) is subordinate, and a row is not proof of authorization;
  - `BAR-INDEX.md` is a catalogue;
  - reconciliation is required but has **no implemented mechanism** (TD-171).
- The repository therefore now has a decided precedent for a governed-record-plus-runtime-realization arrangement, structurally comparable to B-with-realization. It also has direct evidence of that arrangement's cost: the reconciliation gap recorded as TD-171.
- This is evidence for the Repository Owner. It is **not** a selection, and this document still does not link the two decisions.

**3. The canonical physical-realization owner was checked** (not examined in the 2026-09-25 preparation):
- `ONT-001-041` and `PLT-001-038` ("Implementation Reference", both LOCKED) are reference-only delegation clauses. They assign *physical realization* of ontology relationships and platform constructs to `CMD-001` and `architecture/04-Technical/Master_Technical_Architecture.md`. Neither defines an identifier → implementation attribute.
- The Master Technical Architecture contains no Business Activity → implementation binding. Its only Business Activity link is `ai_tool_registry.invokes_business_activity_id`, a tool → Business Activity cross-registry reference with no FK. It does not bind to code.
- **K-6 therefore still holds**, now verified against every canonical source that could own it.
- *Observation for the Repository Owner (outside RD-M2-02):* that column is typed `UUID`, while the canonical BAR identifier is the string `BA-NNNNNN`.
- *Consequence for option B2 only:* a new binding table would also require a Master Technical Architecture amendment, in addition to the ADR (`CLAUDE.md §18`).

**4. Unchanged and still valid:**
- the certified `ResolverRegistry` precedent (`Backend/Runtime/AuthorizationEngine/authorization/registry.py:24`; used at `Backend/Services/AuthService/dependencies.py:140`), relevant to A and C;
- the `CBOR-INDEX.md` / `BAR-INDEX.md` governed-index precedent (B1);
- the `admin-navigation.ts` "documented, temporary deviation" precedent (A and C under K-4/K-5).

### 0.3 Evidence still unavailable, and whether it blocks the decision

| Missing item | Blocks the RD-M2-02 decision? | Why |
|---|---|---|
| A canonical implementation-reference attribute (K-6) | **No** | Its absence is the *reason* for the decision, not an input to it. Every option creates this element as new vocabulary through an ADR (§6) |
| Any CBAM instance | No | It is a consequence of choosing B1 (an `IMP-001` CBAM amendment, §5); it is not needed to choose |
| The M5 invocation contract | No | RD-M2-06 fixes M2 to an opaque, never-invoked reference; §5 records no option-distinguishing M5 effect beyond B1's possible future reuse of CBAM sections |
| A first consumer and hosting decision (M7; `RO-M1-11`) | No | It affects deployment detail (per-host tables under B2), not the choice of mechanism |
| Workstreams D–H (BAR discovery, execution gate, retroactive registration) | No | None of them bears on how an identifier binds to code. K-2 keeps BAR out of the binding in every option |
| PostgreSQL/asyncpg verification (TD-176) | No | It bears only on B2's eventual persistence behaviour, not on the choice |

### 0.4 Readiness determination

**READY FOR DECISION.**
- All repository evidence the options depend on is now available. The dependency this document itself named (the WP-23 authority question) is resolved.
- What remains is the governance judgment §1 identifies: how K-4 ("explicit, governed contract") and K-5 ("never derived from implementation") are to be satisfied. Only the Repository Owner can make it.
- The decision requires:
  1. an explicit Repository Owner selection among A, B1, B2 and C;
  2. an ADR recording it and naming the new implementation-reference element (K-6). Every option is an architectural change under `CLAUDE.md §18`/`§19` (§6), and would need its own authorization.

**This reassessment selects no option, ranks none, creates no ADR, modifies no `ADR-042`, and authorizes nothing.**

### 0.5 Separate M2 constraint surfaced (not part of RD-M2-02)

RD-M2-03 and RD-M2-04 make M2's Activity Resolution consume `bar_registration` registration state, and terminate execution when an activity is not registered. **TD-171's hard condition** says act-to-row enforcement and reconciliation must exist **before `bar_registration` is used to decide whether a Business Activity may execute** (`TECH-DEBT.md`; `IRA-WP-23-AC §0.2`).
- An M2 that consults `bar_registration` for eligibility would therefore fall within TD-171's condition.
- This does not affect the RD-M2-02 choice. It is a prerequisite the Repository Owner must address before any M2 implementation authorization.
- RD-M2-01 (WP-23 A–C closed, committed and verified; stale statements reconciled) now appears satisfied by `b0f5a12`/`bae8350`. Recording that in `IRA-BAE-001-M2 §0` is outside this task and was not done.

**M2 remains NOT AUTHORIZED and NOT STARTED. WP-23 remains OPEN; Workstreams D–H are not implemented; TD-171 remains OPEN.**

### 0.6 Repository Owner Decision Record — RD-M2-02 (2026-09-28)

**Recorded** by direct Repository Owner instruction: "Select OPTION B2 for RD-M2-02 — Identifier Implementation Binding." The decision is recorded as stated and is not reinterpreted.

**Decision: Option B2.** A governed database table holds the **authoritative** binding from a BAR-issued Business Activity Identifier to its implementation. The code-side realization (B-with-realization, §4) is **subordinate**, and a **reconciliation** mechanism between the two is required.

**Recorded in ADR-043:** `architecture/07-Decisions/ADR-043_Business_Activity_Identifier_Implementation_Binding.md` (Accepted). It holds:
- the authority relationship (§4.1);
- the conceptual implementation-reference element (§4.2);
- the reconciliation requirement (§4.3);
- the inherited constraints K-2, K-3/K-10, K-4/K-5, K-7 and K-9 (§4.4);
- the rationale and the rejected alternatives (§5);
- the non-authorizations (§7);
- the follow-on work (§9).

**Repository Owner rationale, summarized from ADR-043 §5:**
- `BA-NNNNNN` is the canonical identity.
- The binding is an architectural authority relationship.
- A persisted governed record is durable and queryable across restarts, deployments and instances.
- It follows the RD-23-03 layered-authority precedent.
- No canonical identifier-to-implementation attribute exists (K-6), so this is a genuine addition.

**Alternatives not selected** (still documented in §4–§5 above; reasons in ADR-043 §5.1):
- **A:** the binding would depend on host start-up state.
- **B1:** a governed record plus a separate code-side table, without a stronger persistent system-of-record boundary.
- **C:** a different, capability-authored and code-held authority model. ADR-043 notes that the BAE owns resolution in every option (K-1).

**Required follow-on (ADR-043 §9, not performed):**
- **FO-1:** the Master Technical Architecture amendment for the new governed table (§0.2 item 3).
- **FO-2:** the M2 detailed design re-done for B2.
- **FO-3:** the physical definition of the implementation reference.

**Unchanged and separate:**
- The PostgreSQL/asyncpg verification limitation (TD-176 for BAR A–C) remains an implementation and verification matter and will also apply to the binding table.
- **TD-171 remains OPEN** and unresolved. It is separate from this decision (§0.5).
- **M2 remains NOT AUTHORIZED and NOT STARTED.**

---

## 1. The Decision

**Question.** What is the authoritative, governed mechanism by which a BAR-issued Business Activity Identifier (`BA-NNNNNN`) is bound to the executable implementation the Business Activity Engine will run?

**Why it is a decision, not a detail.** The Repository Owner's own reasoning (`IRA-BAE-001-M2 §0`, RD-M2-02): whatever holds this mapping *is* the authoritative runtime mapping between canonical identity and executable code. That fixes who may add or change it, where its truth lives, and how it is audited.

## 2. Fixed Constraints (already decided; not reopened)

| # | Constraint | Source |
|---|---|---|
| K-1 | The **BAE owns** runtime Manifest Resolution and the identifier → implementation/manifest mapping | `ADR-042 §3`/`§4.3` (`RO-M1-03`) |
| K-2 | BAR remains the registration and identifier authority. **BAR scope is not expanded**, so the binding cannot be a BAR column or a BAR responsibility | `ADR-042 §7`; D2, D5, D6 |
| K-3 | No filesystem scanning, decorators, arbitrary module scanning, FastAPI route discovery or implementation heuristics | `ADR-042 §4.3`; `RTA-001 §6.6` `[LOCKED]`; `IMP-001 §6.22.8` ("never … through implementation scanning or naming conventions") |
| K-4 | The mapping must use an **explicit, governed manifest/registry contract** | `ADR-042 §4.3` |
| K-5 | "The Manifest shall never be derived from implementation"; "The CBAM is owned by the Business Architecture. The Business Activity Engine consumes the CBAM" | `IMP-001 §6.29.2`, `§6.29.3` |
| K-6 | **No canonical attribute for an implementation reference exists.** CBAM v1/v2 (`§6.14`, `§6.29.6`) and `RTA-001 §6.7` list none, and no CBAM instance exists in the repository | `IRA-BAE-001-M2 §3.2` (B-2) |
| K-7 | The BAE runs **in-process in each hosting service** (`RO-M1-01`); cross-service BAR access is deferred (`RO-M1-11`) | `ADR-042 §4.1`, `§6` |
| K-8 | M2 resolves an **opaque reference and never invokes it**; the invocation contract belongs to M5 | RD-M2-06 |
| K-9 | Resolution is **organization-independent** | RD-M2-03 |
| K-10 | The BAE core imports no persistence, BAR, `importlib`, `pkgutil`, `os`, `glob` or `sys` (M1 package-boundary tests) | `tests/test_package_boundary.py` (committed, `94c99a1`) |
| K-11 | The 21 existing Business Activities keep executing through direct routing until each migrates (D8); no binding is required for them | D8; Charter §5 |

**Consequence of K-6 for every option.** Whatever option is chosen, the "implementation reference" element is **new canonical vocabulary**: no source defines it. That is the root reason RD-M2-02 is a decision.

## 3. Repository Evidence for Candidate Mechanisms

| Evidence | What it shows | Relevance |
|---|---|---|
| `Backend/Runtime/AuthorizationEngine/authorization/registry.py` `ResolverRegistry` (certified, `WP-RTA-001`); used at `AuthService/dependencies.py:140` | An explicit, fluent, **fail-fast** in-code registry (a duplicate registration raises), assembled by the **host at its composition point**, mapping a key to a runtime object | Direct precedent for **Option A** and **Option C** |
| `CBOR-INDEX.md`, `BAR-INDEX.md` | Governed Markdown registries in `architecture/00-Governance/`, amended only by a registering act, and pointers to that act | Precedent for the documented form of **Option B** |
| `bar_registration` table (WP-23 C, ~~**untracked, unverified**~~ *(2026-09-28: committed `b0f5a12`, independently verified, accepted)*) | A persistent registry table in AuthService | Precedent for the persistent form of **Option B**, ~~but not yet committed or verified (`IRA-WP-23-AC …`). Its own authority relative to `BAR-INDEX.md` is unresolved there~~ *(2026-09-28, §0.2: now committed and verified; its authority is decided by RD-23-03 (layered; runtime record subordinate to the registering act), with reconciliation unimplemented, TD-171)* |
| `source/frontend/src/config/admin-navigation.ts` | Static code configuration substituting for required navigation metadata (`SD-001-018`), recorded **as "a documented, temporary deviation … not a silent violation"** | Shows this repository treats code-held configuration in place of required metadata as a **governance deviation** requiring disclosure. Bears on A and C under K-4 and K-5 |
| `AuthService/main.py` explicit `include_router` list | Explicit composition of executable units, with no discovery | Composition precedent only; it is not an identifier registry |
| `screen_registry` (cited in `CLAUDE.md §20.6`, IMP-FE-001) | **Does not exist** in `Backend/` or `database/` (`IRA-BAE-001-M1 §5` row 8) | Not usable evidence |

No other identifier → code registry exists in the repository.

## 4. Options

**A. Host-service start-up binding table.** Each hosting service's composition root constructs one immutable table `{BA-NNNNNN → implementation reference (+ minimum manifest identity)}` and passes it to a BAE-owned, content-free resolver.

**B. Governed persistent or documented binding registry.** The authoritative mapping lives outside executable code, as a governed record amended by a registering-act-style governance act. Two forms:
- **B1, documented:** a governed Markdown or structured index, or CBAM instance files listed in one index, under `architecture/`.
- **B2, persistent:** a governed database table in the host.

Either form still needs a code-side way to turn a textual reference into the executable object. That is either a dynamic import by name (prohibited in the BAE core by K-10, and close to K-3), or a code-side table matched to the record. The matched variant is examined as **B-with-realization**: the record is authoritative, a code-side table realizes it, and a mandatory consistency test proves they match.

**C. Capability-contributed, BAE-owned fail-fast registry (the `ResolverRegistry` pattern).** The BAE ships an explicit registry type modelled on the certified `ResolverRegistry`. Each capability contributes its own bindings through an explicit call at the host's composition point; there is no central hand-maintained table. It differs from A in *who authors each entry*: the owning capability, not the host wiring. It is **closely related to A** and shares A's source-of-truth characteristics. It is listed separately because the repository provides direct, certified precedent for its shape.

## 5. Comparison

| Dimension | A. Host start-up table | B1. Documented registry (+ realization) | B2. Persistent DB registry (+ realization) | C. Capability-contributed registry |
|---|---|---|---|---|
| **Authority** (who may change the mapping) | Whoever changes the host's composition code, through normal code review | A governance act, as with BAR/CBOR registering acts | A governance act writing the row; the write path needs its own authorization | Each owning capability, for its own entries, through code review |
| **Lifecycle** | Exists from process start to process end; changes only by deployment | Document lifecycle (draft → approved → amended); realization changes by deployment | Row lifecycle (insert, amend); realization changes by deployment | As A |
| **Source of truth** | Executable code | The governed document; code must conform | The database row; code must conform | Executable code, distributed across capabilities |
| **Adding / removing a BA** | Edit the host table and redeploy | Governance act amends the record, then the realization is updated and redeployed; the consistency test fails until both agree | Governance act writes the row, then realization and redeploy; drift is detectable only at run time or by test | The capability adds or removes its contribution and redeploys |
| **Determinism** | Full: immutable, built once, duplicates rejected | Full at run time (the realization); record-to-code agreement is proven by test, not by construction | Depends on a database read per resolution or a cached snapshot; needs a defined refresh rule | Full, provided contribution order cannot change the outcome (fail-fast on duplicates, as `ResolverRegistry` does) |
| **Testability** | High: pure, in-memory | High for the realization; the record needs a parser or checker, which is new tooling | Needs a database fixture; FK and uniqueness parity with production (`§19.7b` checklist) | High: pure, in-memory; precedent tests exist in `AuthorizationEngine` |
| **Tenant implications** | None if the table is global; K-9 holds by construction | None; the record is global | A table must be declared platform-global (no `organization_id`), like `bar_registration`; `§21.4` must be re-checked if any write endpoint is added | As A |
| **Deployment implications** | Each host carries only its own bindings; no migration | Records live in the repository; hosts deploy the realization; no migration | New table and migration **per hosting service** (K-7), plus a governed write path; cross-host placement interacts with `RO-M1-11` | As A; each host composes the contributions of the capabilities it hosts |
| **Relationship to BAR** | Independent. BAR is consulted first; a binding never implies registration | Independent. Could cite the BAR identifier and registering act, but must not duplicate BAR fields (K-2) | Independent. Must not become a second registration store: no registration state, no identifier issuance (K-2) | As A |
| **Relationship to BAE** | The BAE owns the resolver *type*; the host owns the *content* | The BAE owns the resolver and consumes the realization; the record is the governed contract K-4 names | The BAE owns the resolver, but the table is host persistence. The BAE core cannot read it (K-10), so a host adapter is needed | The BAE owns the registry type and its fail-fast rules; capabilities own the content |
| **New ADR / constitutional change?** | **Yes, at least an ADR.** It must rule that a code-held table satisfies K-4's "governed" contract despite K-5, and must name the new implementation-reference element (K-6). Absent that ruling it would stand as a disclosed deviation, as the `admin-navigation.ts` precedent shows | **Yes.** An ADR, plus most likely an `IMP-001` CBAM amendment adding an implementation-reference attribute (K-6) if the record is a CBAM instance; a new governed artifact type and location | **Yes.** An ADR; a new table (`CLAUDE.md §18`); a governed write path; per-host placement | **Yes, as A.** An ADR ruling on K-4/K-5 and naming the element; it also fixes distributed authorship as policy |
| **Introduces discovery / scanning?** | No | No, if every entry is index-listed. A reference turned into code by dynamic import would conflict with K-3/K-10; realization by a code table avoids that | No, if realized by a code table. Dynamic import by stored name would conflict with K-3/K-10 | No, provided contributions are explicit calls at composition, **never** import-time side effects or decorators |
| **Effect on M5 invocation** | None directly (K-8). The referenced object must later satisfy the M5 invocation contract; a type mismatch surfaces at composition or at M5 | Same; the record may later also hold M5-relevant manifest data (transaction policy and so on), which favours B1 if M5 consumes CBAM sections (`§6.29.12`) | Same as B1, with M5 reading host persistence | As A |

## 6. Observations (for the Repository Owner; not a selection)

- **Every option needs an ADR.** K-6 means the implementation-reference element is new vocabulary in every case, and `CLAUDE.md §18`/`§19` require architecture to change only through an ADR.
- **A and C are the smallest to build.** They sit closest to certified repository precedent (`ResolverRegistry`) and leave K-4/K-5 conformance as an explicit ruling rather than something structurally guaranteed.
- **B1 is the only option in which the source of truth is a governed, non-code artifact.** That is the reading of K-4/K-5 most literally faithful to `§6.29.2`/`§6.29.3`. It costs a CBAM amendment and a mandatory record-to-code consistency test.
- **B2 adds a table and a write path in every hosting service.** It also overlaps BAR's persistence role, which is the pattern `ADR-042 §7` exists to avoid.
- **Whichever option is chosen, three disciplines apply.** Fail-fast construction (duplicates, identifier mismatch, missing reference); resolution strictly *after* the BAR check; and an explicit prohibition on import-time registration and dynamic import.
- **Interaction with WP-23 A–C.** Under RD-M2-01, WP-23 A–C closure precedes M2. The unresolved authority question inside WP-23 A–C (`BAR-INDEX.md` versus the `bar_registration` table; see `IRA-WP-23-AC …`) is the same kind of question as B1 versus B2 here: documented record versus persistent table. Deciding the WP-23 question first may inform this one. This document does not link the two decisions. *(2026-09-28: the WP-23 question is decided (RD-23-03, Option D, layered); see §0.2 item 2. The decisions remain unlinked.)*

## 7. What This Document Does Not Do

- It selects no option and records no ranking.
- It creates no ADR and does not modify `ADR-042`.
- It amends no `IMP-001`, `RTA-001`, Charter, BAR or WP-23 artifact.
- It creates no code, manifest, binding, registry, table, migration or test.
- It registers no Business Activity and assigns no identifier.
- Nothing is staged, committed or pushed.

---

~~**RD-M2-02 — OPEN — RO decision required.** *(2026-09-28: READY FOR DECISION, §0.4. No option is selected.)*~~

**RD-M2-02 — DECIDED (2026-09-28) — Option B2, governed persistent binding registry (§0.6; `ADR-043`). M2 is NOT AUTHORIZED.**
