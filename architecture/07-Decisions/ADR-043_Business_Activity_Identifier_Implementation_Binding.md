# ADR-043 — Business Activity Identifier → Implementation Binding (RD-M2-02): Governed Persistent Binding Registry (Option B2)

**Status:** Accepted
**Classification:** Architecture Governance / Runtime Component contract form (`CLAUDE.md §16`, `§18`, `§19`)
**Decided by:** Repository owner (architecture governance authority), 2026-09-28, by the instruction "Select OPTION B2 for RD-M2-02 — Identifier Implementation Binding … Create the required ADR". It responds to `architecture/06-Reviews/ROD-BAE-001-M2-Identifier-Implementation-Binding-Decision-Preparation.md` (prepared 2026-09-25; reassessed **READY FOR DECISION** 2026-09-28, §0 there).
**Affected Documents:**
- `ROD-BAE-001-M2-…` records the selection and links here.
- `IRA-BAE-001-M2 …` §0 and §13.1 reflect that RD-M2-02 is decided.
- `ADR-042` is **not** modified; this ADR fixes the form `ADR-042 §4.3` left open.
- `RTA-001`, `IMP-001`, `CMD-001`, the `WP-BAE-001` Charter, the WP-23 Charter, `BAR-INDEX.md` and the Master Technical Architecture are **not** modified. The Master Technical Architecture amendment this decision requires is identified in §9 and **not performed**.

**Affected Code:** None. No table, migration, model, repository, service, adapter, resolver, binding row, test or BAE runtime file is created or modified.

---

## 0. Nature of This Record

This ADR **records** a Repository Owner selection that has already been made: RD-M2-02 = Option **B2**. It creates no policy beyond that selection and the constraints the selection inherits from already-decided sources (§4.4).

An ADR is required because the decision is an architectural addition. It creates a new canonical element (the implementation reference, §4.2) and a new governed store (`CLAUDE.md §18`, `§19`). Every RD-M2-02 option carried this requirement (`ROD-BAE-001-M2 §6`, `§0.4`).

**This ADR does not authorize WP-BAE-001 M2 implementation** or any other implementation (§7).

## 1. Context

- `ADR-042 §4.3` (`RO-M1-03`) makes the Business Activity Engine (BAE) the owner, at runtime, of resolving a BAR-issued Business Activity Identifier (`BA-NNNNNN`, D5) to its implementation or manifest. It requires "an **explicit, governed manifest/registry contract**", and it "does not define that contract, its schema, its storage, or its form".
- `IRA-BAE-001-M2 §3.2` (B-2) found that no governed source binds an identifier to executable code. RD-M2-02 was opened to fix that form.
- The decision preparation (`ROD-BAE-001-M2`) compared four options against fixed constraints K-1 to K-11: A, B1, B2 and C.
- It was reassessed on 2026-09-28 after WP-23 A–C were committed (`b0f5a12e84a9a3f7d9622bcbea4cee87b934be85`) and reconciled (`bae8350b89771c48ad0b9acd57c829cdb62be615`). Its verdict was **READY FOR DECISION** (`§0.4`).

## 2. Problem

What is the authoritative, governed mechanism by which a BAR-issued Business Activity Identifier is bound to the executable implementation the BAE will run (`ROD-BAE-001-M2 §1`)?

Whatever holds this mapping *is* the authoritative runtime link between canonical identity and executable code. That fixes who may add or change it, where its truth lives, and how it is audited.

No canonical attribute for an implementation reference exists. Checked sources:
- CBAM v1/v2 (`IMP-001 §6.14`, `§6.29.6`);
- `RTA-001 §6.7`;
- `ONT-001-041` and `PLT-001-038`, which are reference-only delegation clauses;
- the Master Technical Architecture, whose only Business Activity link is `ai_tool_registry.invokes_business_activity_id`, a tool → Business Activity pointer.

The source is `ROD-BAE-001-M2 §2` (K-6) and `§0.2` item 3.

## 3. Decision

**RD-M2-02 = Option B2: a governed database table holds the authoritative binding from a BAR-issued Business Activity Identifier to its implementation. A code-side realization is subordinate to it, and a reconciliation mechanism is required between the two.**

## 4. Decision Details

### 4.1 Authority relationship

| Layer | Record | Authority |
|---|---|---|
| Canonical identity | BAR (`bar_registration` / `bar_identifier_ledger`; D2, D5) | The `BA-NNNNNN` identifier is the canonical Business Activity identity. BAR registration is consulted **first**; a binding never implies registration (`ROD-BAE-001-M2 §5`, "Relationship to BAR") |
| **Binding (authoritative)** | The **governed binding table** (B2) | **Authoritative** for which implementation an identifier is bound to. It is created or changed only by a governance act; the governed write path and its own authorization are a required part of the design (`ROD-BAE-001-M2 §5`, B2 "Authority") |
| Realization (subordinate) | The code-side realization (B-with-realization, `ROD-BAE-001-M2 §4`) | **Subordinate.** It turns a governed binding into the executable object. It is never itself proof of a binding, and it must conform to the governed record |
| Consumer | The BAE resolver (`ADR-042 §4.3`, K-1) | The BAE owns resolution. It reads the governed binding through a host-side adapter (K-10) and resolves only after the BAR registration check |

This follows the layered-authority precedent the Repository Owner established for BAR in RD-23-03 (`ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md §0`): a governed record is authoritative, runtime realization is subordinate, and reconciliation is required.

### 4.2 The new implementation-reference element (conceptual only)

**Implementation reference:** the governed value, held in the binding table against a `BA-NNNNNN` identifier, that identifies the executable implementation bound to that Business Activity. Constraints:
- It is **opaque to M2**, which resolves it and never invokes it. The invocation contract belongs to M5 (RD-M2-06, K-8).
- It is **new canonical vocabulary** (K-6). This ADR defines it only at the conceptual level; its physical representation, column set and schema are **not** defined here.
- It is **not** a BAR attribute and is never held in BAR tables (K-2).

### 4.3 Reconciliation (required)

The authoritative binding and its code-side realization must be reconciled: a realization entry without a governed binding, or a governed binding without a realization, must be detectable. `ROD-BAE-001-M2 §4` names the matched variant: "a mandatory consistency test proves they match". The concrete mechanism is **not** defined by this ADR.

A related unresolved gap exists for BAR itself, TD-171 (no act-to-row enforcement or reconciliation for `bar_registration`). It is recorded here as a precedent to avoid, not as part of this decision.

### 4.4 Constraints B2 inherits (already decided; restated, not added)

| # | Constraint as it applies to B2 | Source |
|---|---|---|
| K-2 | The binding table is **not** a BAR table. It holds no registration state and issues no identifier. This keeps BAR's scope unexpanded, consistent with `ADR-042 §7` | `ROD-BAE-001-M2 §2`, `§5`–`§6` |
| K-3 / K-10 | The stored implementation reference is **never** turned into code by dynamic import or discovery, and never by filesystem, decorator, module or route scanning. Realization is an explicit code-side table matched to the governed record. The BAE core imports no persistence, so a host-side adapter reads the table | `ADR-042 §4.3`; `RTA-001 §6.6`; `ROD-BAE-001-M2 §4`, `§5` |
| K-4 / K-5 | The binding is an explicit, governed contract, and is never derived from implementation | `ADR-042 §4.3`; `IMP-001 §6.29.2` |
| K-7 | The BAE runs in-process in each hosting service. A binding table and migration are therefore required **per hosting service**, and cross-host placement interacts with the deferred `RO-M1-11` | `ADR-042 §4.1`, `§6`; `ROD-BAE-001-M2 §5` |
| K-9 | Resolution is organization-independent. The table is platform-global (no `organization_id`), like `bar_registration`. `CLAUDE.md §21.4` must be re-checked if any write endpoint is added | RD-M2-03; `ROD-BAE-001-M2 §5` |
| Discipline | Fail-fast on duplicates, identifier mismatch and missing reference; resolution strictly after the BAR check; no import-time registration | `ROD-BAE-001-M2 §6` |

Determinism: B2 "depends on a database read per resolution or a cached snapshot; needs a defined refresh rule" (`ROD-BAE-001-M2 §5`). The refresh rule is a required implementation-design decision and is not fixed here.

## 5. Rationale (as recorded by the Repository Owner)

1. The BAR identifier `BA-NNNNNN` is the canonical Business Activity identity.
2. The implementation binding is an architectural authority relationship, not merely a start-up or runtime convenience.
3. A persisted, governed database record provides durable, queryable authority across process restarts, deployments and runtime instances.
4. RD-23-03 already established the relevant layered-authority precedent: the governing act or record is authoritative, runtime realization is subordinate, and reconciliation is required.
5. B2 therefore follows an existing architectural authority pattern rather than introducing a second canonical implementation-reference mechanism.
6. The existing architecture sources were checked, and no canonical identifier-to-implementation attribute exists. This is therefore a genuine architectural addition (§2).

### 5.1 Alternatives considered and not selected

| Option | Summary (`ROD-BAE-001-M2 §4`) | Reason not selected (Repository Owner) |
|---|---|---|
| **A** — host-service start-up binding table | An immutable table built in each host's composition root | It makes the binding depend on host-service start-up state rather than a durable, governed enterprise record |
| **B1** — governed documented registry (+ realization) | A governed Markdown or structured index (or CBAM instance files), realized by a code-side table and a consistency test | It introduces a governed record plus a separate code-side table that must be reconciled, without giving the binding a stronger persistent system-of-record boundary. It would also most likely need an `IMP-001` CBAM amendment (`ROD-BAE-001-M2 §5`) |
| **C** — capability-contributed, BAE-owned fail-fast registry | The BAE ships a registry type modelled on `ResolverRegistry`; each capability contributes its own entries in code at composition | It creates a different authority and ownership model from the layered enterprise-governance model already established: canonical content is distributed across capabilities and held in executable code. *Clarifying note: under `ADR-042 §4.3` (K-1) the BAE owns identifier-to-implementation resolution in **every** option, including B2. What distinguishes C, per `ROD-BAE-001-M2 §4`/`§5`, is capability-authored, code-held content rather than a single governed record* |

## 6. Consequences

- **For WP-BAE-001 M2:**
  - The binding form is decided.
  - The M-B / composition-root design text in `IRA-BAE-001-M2 §7` and `§13.2`–`§13.4` (proposed files such as `binding.py`, and the "no table, no migration" statements) **no longer reflects the decided form**. The M2 detailed design must be redone for B2 before any M2 implementation authorization.
  - M2 still requires its own explicit authorization.
- **For hosting services:** each host that runs BAE-routed Business Activities will need its own binding table, migration, host-side adapter and governed write path once implementation is authorized (K-7, K-10).
- **For BAR / WP-23:** none. BAR scope, `bar_registration`, `BAR-INDEX.md` and Workstreams D–H are unchanged (K-2).
- **Verification:** PostgreSQL/asyncpg behaviour of any new persistent store remains unverified in this environment. This is recorded as an implementation and verification matter (TD-176's scope is BAR A–C, but the same limitation will apply to the binding table).
- **No code consequence** arises from this ADR alone.

## 7. Explicit Non-Decisions / What This ADR Does NOT Authorize

This ADR does **not** authorize or decide any of the following:
- **Implementation:** WP-BAE-001 M2 or any other milestone. M2 remains **NOT AUTHORIZED and NOT STARTED**.
- **Artifacts:** creation of the binding table, any migration, model, repository, service, host adapter, resolver, realization table, reconciliation check, binding row or test.
- **Physical design:** the schema, column set, physical form of the implementation reference, refresh rule, governed write path, or its authorization.
- **BAR changes:** any change to BAR registration code, BAR tables or `BAR-INDEX.md`; any Business Activity registration or identifier assignment.
- **TD-171:** any change to TD-171, which remains **OPEN**. Its hard condition, that act-to-row enforcement must exist before `bar_registration` decides whether a Business Activity may execute, is separate from this decision and unresolved (`ROD-BAE-001-M2 §0.5`).
- **Other open items:** WP-23 Workstreams D–H, the M5 invocation contract (RD-M2-06), `RO-M1-11` cross-service BAR access, or the M2 detailed design.
- **Amendments:** any amendment of `ADR-042`, `RTA-001`, `IMP-001`, `CMD-001` or the Master Technical Architecture.

## 8. Relationship to Existing Decisions

- **`ADR-042`:** consistent with and complementary to it. This ADR supplies the "explicit, governed manifest/registry contract" form that `§4.3` required but left undefined. The ownership (`RO-M1-03`) and prohibited-discovery list are unchanged.
- **RD-23-03 (`ROD-WP-23-AC …`):** the layered-authority precedent this decision follows (§4.1). The two decisions govern different records: BAR registration versus implementation binding.
- **RD-M2-03 / RD-M2-04 / RD-M2-06 (`IRA-BAE-001-M2 §0`):** unchanged. Organization-independence, BAE consumption of BAR registration state, and resolve-don't-invoke all apply to B2.

## 9. Required Follow-On Work (identified, NOT performed)

| ID | Item | Why | Authorization |
|---|---|---|---|
| **FO-1** | **Master Technical Architecture amendment** recording the governed binding table, platform-global and per hosting service | `CLAUDE.md §18` (new table). The Master Technical Architecture is the canonical owner of physical realization (`ONT-001-041`, `PLT-001-038`; `ROD-BAE-001-M2 §0.2` item 3) | Separate Repository Owner authorization |
| **FO-2** | M2 detailed design re-done for B2: the binding table, host adapter, realization, reconciliation, refresh rule and governed write path | §6 | Part of a future M2 authorization |
| **FO-3** | Physical definition of the implementation-reference element | §4.2 | With FO-1/FO-2 |

**Governance-index impact:** none required. Following the established convention (`ADR-036 §Consequences`, `ADR-042 §9`), this ADR self-registers by filename in `architecture/07-Decisions/` and adds no `DOC-000` row.

## 10. Traceability

| Source | Role |
|---|---|
| `ROD-BAE-001-M2-Identifier-Implementation-Binding-Decision-Preparation.md` | Options, constraints K-1 to K-11, comparison, readiness reassessment (§0) |
| `IRA-BAE-001-M2_Business_Activity_Resolution_and_BAR_Integration_Readiness.md` | RD-M2-02 origin (§0), B-2 finding (§3.2) |
| `ADR-042` §4.3, §6, §7 | Ownership, the governed-contract requirement, BAR scope |
| `ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md §0` | RD-23-03 layered-authority precedent |
| `IMP-001 §6.14`, `§6.29.2`, `§6.29.6`; `RTA-001 §6.6`, `§6.7`; `ONT-001-041`; `PLT-001-038`; Master Technical Architecture | K-3 to K-6 sources |
| `TECH-DEBT.md` TD-171, TD-176 | Separate open items referenced, not changed |
| Commits `b0f5a12e84a9a3f7d9622bcbea4cee87b934be85`, `bae8350b89771c48ad0b9acd57c829cdb62be615` | Repository state at decision |

## 11. Status / Approval

**Accepted**, recording the Repository Owner's RD-M2-02 selection of Option B2 (2026-09-28). No implementation is authorized. Nothing is staged, committed or pushed by the creation of this ADR.
