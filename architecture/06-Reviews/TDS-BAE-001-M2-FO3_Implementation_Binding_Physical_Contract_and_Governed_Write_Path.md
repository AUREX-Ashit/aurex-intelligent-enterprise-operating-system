# TDS-BAE-001-M2-FO3 — Implementation Binding: Physical Contract and Governed Write Path (FO-3)

**Work Package:** `WP-BAE-001`, milestone M2. This is follow-on **FO-3** of `ADR-043 §9`.
**Prepared:** 2026-09-29, by Repository Owner instruction: "Proceed with FO-3 — Physical Binding Contract and Governed Write Path, DESIGN ONLY."
**Status:** ~~**DESIGN COMPLETE — NOT IMPLEMENTED — PENDING REPOSITORY OWNER APPROVAL.**~~ **DESIGN APPROVED — NOT IMPLEMENTED** *(2026-09-29, Repository Owner decisions FQ-1 to FQ-8, §15.A)*.
- ~~Open design questions FQ-1 to FQ-8 (§15) must be decided before this design can be approved as the M2 implementation basis.~~ *(2026-09-29: FQ-1 to FQ-8 are DECIDED, §15.A. The original open-question record in §15 is preserved unchanged. Remaining implementation prerequisites are listed in §15.A.3.)*
- FO-3 approval authorizes no physical implementation (§15.A.4).
- **M2 remains NOT AUTHORIZED and NOT STARTED.**

**This document creates nothing executable.** It contains no `CREATE TABLE`, SQL, migration, ORM model, repository, service, adapter, router or test. Field lists and constraints below are a *design contract* for a future, separately authorized implementation. Every design choice is `[DESIGN — pending approval]` unless it restates a decided source.

---

## 1. Authoritative Baseline (read directly for this design)

| Source | Relied on |
|---|---|
| `ADR-043` (Accepted) | B2: the governed binding is authoritative, realization is subordinate, reconciliation is required (§4.1–§4.4). FO-3 = physical contract, write path and act-to-row enforcement (§9) |
| `Master_Technical_Architecture.md` v7.4, PART K ADDENDUM (AMD-017, commit `867af46`) | K.1–K.9: the concepts, authority model, hosting and tenancy, runtime consumption, reconciliation, write-path separation (K.7), and non-decisions. H.5 records that the physical store is FO-3, and that BAR tables are not recorded in the MTA |
| `IRA-BAE-001-M2 …` §16 (FO-2, DESIGN APPROVED) and §16.L (commit `accc127`) | 16.C conceptual contract; 16.D realization; 16.E adapter; 16.F reconciliation; 16.I failure semantics. OQ-1: no host column. OQ-2: present means bound, no M2 lifecycle. OQ-3: no caching. OQ-4: reconciliation in CI and at host start-up |
| `ROD-BAE-001-M2 …` | K-1 to K-11; the B2 comparison (§5); §0.5 (TD-171 separation) |
| `IMP-001 §6.15.4`, `§6.16.5` | Activity Resolution locates the implementation using BAR; unresolvable activities terminate before execution |
| WP-23 A–C (commit `b0f5a12`): `models/bar_registration.py`, `services/bar_registration_service.py` | BAR identity and registration authority; `registering_act` is a required, non-blank, free-text `String(255)`; identifier `String(20)`; no caller-authority check (TD-171) |
| Existing governed-write and authority mechanisms, verified in code (§3) | `require_platform_admin`, `require_authority_holder` (`AI-001`/`AI-002`), `enforce_approval_authority`, the `tenant_registry` approval pattern, `observability.record_audit`/`publish_event` |
| `TECH-DEBT.md` | TD-157 (AI-002 seat unpopulated); TD-171 (BAR act-to-row); TD-175 (no DB identifier-format CHECK); TD-176 (PostgreSQL unverified) |

## 2. Scope Boundary

| FO-3 defines (design) | FO-3 does not |
|---|---|
| The physical binding data model, constraints and cardinality (§4–§6) | Implement any table, migration, model, repository, service, adapter or test |
| The governed write path (§7) and act-to-row enforcement (§8) | Invent an approval framework or a governance-act registry. Where the repository lacks one, the gap is recorded (§8.3, §15) |
| Governing-act semantics (§9), replacement semantics (§10) and audit (§11) | Introduce a binding lifecycle. OQ-2 stands |
| The physical design's fit with the approved read model (§12) and reconciliation (§13) | Change BAR, `BAR-INDEX.md`, TD-171 or any M2 decision |

## 3. Existing Governance Mechanisms Found (verified in code; evidence for reuse)

| Mechanism | What it actually does | Fit for binding writes |
|---|---|---|
| `require_platform_admin` (`dependencies.py:46`) | A claims-only check (`is_platform_admin`) | Available, but a **claims-only** gate. It records no appointed authority, the weakness TD-171 describes |
| `require_authority_holder(authority_identity)` (`dependencies.py:180`) | A **live database lookup** of the ACTIVE `authority_holders` row for a constitutional authority, compared with the caller's `person_id`; denies when no holder exists | The strongest existing authority-to-write pattern. But the only authorities defined are **`AI-001`** (Dedicated Tenant Establishment Business Governance Authority) and **`AI-002`** (Dedicated Infrastructure Allocation Authority, *unpopulated*, TD-157). **Neither owns Business Activity implementation binding** |
| `enforce_approval_authority` (`dependencies.py:233`, WP-18) | Resolves an **Organization-scoped** `approval_authorities` row via a Membership binding | **Not applicable.** The binding is platform-global (OQ-1; K.3), and this gate is organization-scoped by design |
| `tenant_registry` approval pattern (`TenantEstablishmentService`, router gated by `require_ai002_holder`) | The write is gated by a live authority check; `approved_by_actor_id` is taken from the ACTIVE holder record inside the service (never caller-supplied), with `approved_at` | **The precedent** for binding a verified approver identity to a row atomically. `approved_by_actor_id` is a plain UUID (no FK) |
| Act references: `bar_registration.registering_act`, `authority_holders.appointment_instrument_ref` | Free-text citations of a repository governance document | **Traceability only.** No database object represents a governance act, and nothing verifies a citation (TD-171) |
| `observability.record_audit` / `publish_event` (`AuditStatus` SUCCESS/DENIED/FAILED) | Log-based audit and event stand-ins ("explicitly temporary local substitute"; C-114 is not implemented) | The existing audit mechanism, reused. It is **not durable storage** (§11) |

**No existing runtime authority owns Business Activity implementation binding, and no canonical, database-backed governance-act model exists.** Both are open questions (FQ-1, FQ-2), not invented here.

## 4. A — Physical Binding Entity (minimum)

One store per hosting service (K.3, OQ-1). A row present means bound (OQ-2).

| # | Field (logical name) | Type (design) | Null | Basis |
|---|---|---|---|---|
| 1 | `id` | UUID, primary key, system-assigned | No | The repository-wide surrogate-key convention (`bar_registration.id`, `tenant_registry.id`). It is an internal handle only, never the Business Activity Identifier |
| 2 | `business_activity_identifier` | String, max 20 (as `bar_identifier_ledger.identifier`) | No | The BAR-issued `BA-NNNNNN` key of the binding (16.C) |
| 3 | `implementation_reference` | Opaque string, bounded length (**FQ-8** fixes the bound; *2026-09-29: FQ-8 DECIDED — fixed during implementation design, §15.A*) | No | ADR-043 §4.2; K.1. Never parsed, imported or executed. *Not unique (FQ-4 DECIDED many-to-one, §15.A)* |
| 4 | `governing_act` | String, max 255 (as `bar_registration.registering_act`) | No | A citation of the governance act authorizing the row (16.C; §9) |
| ~~5~~ | ~~`approved_by_actor_id`~~ | ~~UUID (no FK)~~ | ~~No~~ | **Withdrawn 2026-09-29 (IP-3 resolved, §15.B). The field is not part of the binding row.** *Original text:* The verified identity of the authority that executed the governed write, ~~taken from the authority check~~ and **never caller-supplied** (the `tenant_registry.approved_by_actor_id` precedent; §7, §8). No FK, because a non-AuthService host cannot reference AuthService's persons (K.3; `RO-M1-11`). *2026-09-29: under FQ-1 (c) there is no runtime authority check to derive this value from. Its source under a governed deployment-time data operation is an open implementation prerequisite, IP-3 (§15.A.3). It is not invented here* |
| 6 | `bound_at` | Timestamp with time zone, system-assigned | No | When the binding became effective (16.C, §11). Never caller-supplied |

**Deliberately excluded,** per the approved decisions:
- a hosting-service column (OQ-1);
- a tenant or organization column (K.3, OQ-1);
- a status, lifecycle, effective-to, version or superseded-by column (OQ-2);
- an `updated_at` column (see §10);
- any BAR registration field, such as reference, owning capability or registration status (K-2, K.2).

~~**Why the field set is `approved_by_actor_id` plus `governing_act`, and not the citation alone.** The citation says *which* act; the approver says *who executed* it under a verified authority. §8 explains why neither alone is enforcement.~~

*2026-09-29 (IP-3, §15.B):* the minimum binding row is `id`, `business_activity_identifier`, `implementation_reference`, `governing_act` and `bound_at`.
- The row records **which act** authorized it (`governing_act`, verified in CI under FQ-2) and **when** it became effective (`bound_at`).
- It records no actor identity, so it never claims that a runtime authorization check occurred.
- Who approved is carried by the governing act itself. Who executed the deployment-time operation is carried by the existing audit mechanism (§11, §15.B).

## 5. B — Identity and Foreign-Key Model

**Decision (design): no foreign key to `bar_registration` or to `bar_identifier_ledger`.**
- BAR lives in AuthService's private database. A binding store in any other hosting service cannot reference it, and a design that allowed an FK only in AuthService would make the contract host-dependent (K.3; `RO-M1-11`; 16.C).
- The authorities stay separate. Registration is checked at **run time** (16.B step 2b) and at **write time** by application logic (§7 step 3), never by a cross-authority constraint.

**Integrity boundary:**
- The binding store enforces its own integrity: non-null fields, uniqueness (§6), and field-shape checks (§6).
- BAR registration of the identifier is verified by the governed write path at write time (application level), and again by the BAE at every resolution (2b). A binding for an identifier later found unregistered is inert, because 2b stops first.
- For a non-AuthService host, the write-time BAR check depends on cross-service BAR read access (`RO-M1-11`, deferred): **FQ-5**. *(2026-09-29: FQ-5 DECIDED — DEFERRED under `RO-M1-11`. No cross-service BAR-read mechanism is designed here, §15.A.)*

## 6. C — Uniqueness and Cardinality

| Rule | Level | Basis |
|---|---|---|
| **One binding per Business Activity Identifier per host store:** `business_activity_identifier` UNIQUE | Database constraint | 16.C, K.3: "at most one current binding per identifier per hosting service"; this is what makes resolution deterministic |
| `id` primary key | Database | Convention |
| `implementation_reference` **not** unique | — | The approved reconciliation model counts a realization entry as aligned when "referenced by **at least one** binding" (16.F, K.5), which permits more than one identifier to bind to one reference. Making it unique would add a cardinality the approved design does not state. ~~**FQ-4** asks the RO whether 1:1 is required~~ *2026-09-29, FQ-4 DECIDED: many-to-one. No UNIQUE on `implementation_reference`. The Business Activity Identifier stays unique within the binding store. §15.A* |
| Non-blank `implementation_reference` and `governing_act` | Database CHECK (non-empty after trim) plus application validation | 16.C integrity expectations |
| Identifier shape `BA-\d{6}` | Application validation; a database CHECK is **recommended** but must be dialect-portable, since SQLite test harness and PostgreSQL production differ (TD-175, TD-176) | 16.C; BAR's own TD-175 gap is not repeated silently. See FQ-8 *(DECIDED 2026-09-29: fixed during implementation design, validated against both SQLite and PostgreSQL, §15.A)* |

There is no composite key and no ordering or version cardinality. Ambiguous bindings are therefore structurally impossible: a second row for the same identifier is rejected by the UNIQUE constraint.

## 7. D — Governed Write Path

**The only way a binding row comes into existence** (K.7(b)):

1. **Governing act.** The Repository Owner issues a governance act naming the exact `business_activity_identifier`, `implementation_reference` and hosting service (§9). *Who may request one:* anyone may propose; only the Repository Owner decides, consistent with every existing registering act and ADR in this repository.
2. **Execution request.** An executor submits the act citation, identifier and reference to the host's **binding write service**. This is a host-side service, not the BAE core, which stays persistence-free and never writes bindings (K.4, K.7(c)).
3. **Pre-write checks** (application level, all before any insert):
   - ~~the executor passes the **binding-write authority check**. *Which* authority is **FQ-1** (§15); the evidenced options are listed there;~~ *2026-09-29, FQ-1 DECIDED (c): there is no runtime authority check. The operation is permitted only as a governed, reviewed deployment-time data operation citing the act, executed under the binding-write database role (FQ-7). §15.A*;
   - the identifier is well-formed and **BAR-registered** (a read-only BAR lookup; FQ-5 for non-AuthService hosts; *2026-09-29: FQ-5 DEFERRED under `RO-M1-11`. Complete write-time BAR verification cannot be claimed for a non-AuthService host until the governed cross-service mechanism exists, §15.A*);
   - no binding exists for the identifier (a friendly pre-check; the UNIQUE constraint is the real backstop);
   - the act citation is non-blank and well-formed (§9);
   - the implementation reference is non-blank.
4. **Persist.** One transaction inserts the row. ~~`approved_by_actor_id` is taken from the **verified authority record** returned by step 3, never from the request (the `tenant_registry` precedent).~~ ~~*(2026-09-29: the `approved_by_actor_id` source is IP-3, §15.A.3.)*~~ *(2026-09-29, IP-3 resolved, §15.B: no actor identity is written to the row.)* `bound_at` is system-assigned.
5. **Audit.** Emitted after the row is flushed in the same unit of work: `record_audit` SUCCESS and `publish_event` (§11).

**Who persists:** the host's binding write service only, within its hosting service's transaction. There is no runtime write path in the BAE (K.7(c)).

**Exposure:** ~~whether step 2 is reachable through an HTTP route, only through an administrative or deployment-time operation, or through a governed data migration is **FQ-1 / FQ-3**.~~ *2026-09-29, FQ-1 DECIDED (c) and FQ-3 DECIDED create-only: no runtime write path and no HTTP route exist. Bindings are created only by a governed, reviewed deployment-time data operation citing the act. There is no replace operation. §15.A.* None is designed as an API here. No HTTP semantics are invented.

## 8. E — Act-to-Row Enforcement

### 8.1 What "enforcement" must mean here

A row must not be able to exist unless:
- (i) a governing act authorized it;
- (ii) an authorized executor carried it out;
- (iii) the row's recorded act ~~and approver are~~ *is* the one actually used.

*2026-09-29 (FQ-1 (c), FQ-2 (a), IP-3 §15.B):*
- (i) is met by the governing act, whose existence and correspondence are verified in CI.
- (ii) is met by the review of the governed deployment-time data operation, and by the binding-write database role (FQ-7). It is not met by a runtime check.
- (iii) is met by the CI citation check. There is no recorded approver to compare against.

**Storing a citation string satisfies none of these by itself.** That is exactly TD-171's gap for `bar_registration`.

### 8.2 Enforcement design (layered; what can be enforced with existing mechanisms)

| Layer | Mechanism | Enforces |
|---|---|---|
| Database | NOT NULL on `governing_act`, ~~`approved_by_actor_id`~~ and `bound_at`; non-blank CHECK on `governing_act`; UNIQUE on the identifier *(2026-09-29: `approved_by_actor_id` withdrawn, IP-3 §15.B)* | A row cannot exist *without* an act citation ~~, a recorded approver~~ or a timestamp, and cannot duplicate an identifier |
| Application (write service) | The single governed write path (§7). ~~The authority check (FQ-1) runs **in the same transaction** as the insert. `approved_by_actor_id` is derived from the verified authority record.~~ *(2026-09-29, FQ-1 DECIDED (c): no runtime authority check. Authorization is the governed act plus review of the deployment-time data operation. Execution is limited by the binding-write database role (FQ-7). ~~The `approved_by_actor_id` source is IP-3.~~ No actor identity is written to the row; the executing actor goes to `record_audit` (IP-3 resolved, §15.B).)* Every failure raises **before** or **rolls back** the insert. Audit SUCCESS is only after a successful flush | ~~A row is created only by a verified authority, recording that authority's identity.~~ *(2026-09-29: a row is created only by the governed, reviewed data operation under the binding-write role.)* A failed or denied attempt leaves no row |
| Transaction boundary | ~~Authority lookup →~~ BAR check → insert → flush *(2026-09-29: no runtime authority lookup under FQ-1 (c))*, all in one unit of work. Any exception rolls back the whole unit. There is no partial row and no SUCCESS audit | Atomicity: act ~~, approver~~ and row cannot diverge within one write *(2026-09-29: IP-3 §15.B)* |
| Database access control ~~(recommended)~~ **(REQUIRED — FQ-7 DECIDED 2026-09-29, §15.A)** | Restrict INSERT, UPDATE and DELETE on the binding store to the write service's database role; the BAE adapter's role gets SELECT only | It closes the "write around the service" path. **The repository has no established database-role separation pattern that I could verify.** Recorded as **FQ-7**, not assumed. *If implementation finds the existing infrastructure cannot support this cleanly, the constraint is recorded, and the decision is not silently weakened (IP-4)* |

### 8.3 What remains unenforceable (recorded gap, not invented away)

- **Act existence and content verification.** No canonical, database-backed governance-act model exists in this repository (§3). The write path can check that a citation is present and well-formed, and that a verified authority executed the write. It **cannot** verify, at the database or application level, that the cited act exists, is approved, and names this identifier and reference.
- The candidate closures (FQ-2) require either:
  - (a) a canonical act registry, which would be a new governed object needing its own decision; or
  - (b) a CI-time check resolving act citations against repository governance documents (§13).
- ~~**Until FQ-2 is decided, act-to-row enforcement is PARTIAL:** authority-to-row is enforced; act-to-row is traceable but not verified. This is disclosed, not hidden.~~
- *2026-09-29, FQ-2 DECIDED (a), which is closure (b) above, a CI-time check against repository governance documents:*
  - Act-to-row correspondence is **verified in CI**. The cited ADR/ROD-style record must exist in the governed repository and must correspond to the binding's identifier and reference.
  - It is **not** enforced by a database FK. There is no act registry to reference, and none is created.
  - At the database level, enforcement remains limited to NOT NULL, the non-blank citation and database-role separation (FQ-7). This is disclosed, not hidden.

## 9. F — Governing Act Semantics

- **What the act is.** A Repository-Owner-authorized governance record binding one `BA-NNNNNN` identifier to one implementation reference in one hosting service. It mirrors the existing **registering-act convention** (WP-23 Charter §7, "a discrete, Repository-Owner-authorized act … mirroring the CBOR-ADR pattern") and the CBOR-ADR registrations (`ADR-037`/`-040`/`-041`).
- **Can an existing record type authorize it?**
  - Yes, as a *form*: an ADR or ROD-style decision record, or a registering-act-style record, can carry the binding.
  - **No existing record type is designated for bindings.** Whether bindings use ADRs/RODs, BAR-style registering acts, or a new act type (for example a dedicated binding-act series) is **FQ-2**. It is not invented here. *2026-09-29, FQ-2 DECIDED (a): an ADR/ROD-style record per binding, with the citation checked in CI against repository documents. No database-backed act registry and no BAR-style act authority are created. §15.A*
- **Minimum traceability,** whatever the form:
  - a stable act identifier, which becomes the `governing_act` citation;
  - the identifier, the reference and the hosting service;
  - the RO decision date;
  - the act's own location in the repository.

  The `governing_act` field stores the act identifier, never free prose.

## 10. G — Creation, Change and Replacement (no lifecycle; OQ-2 preserved)

| Operation | Design |
|---|---|
| **Initial creation** | §7, the only operation in the minimum write path |
| **Change of implementation reference** | **Not part of the minimum M2 write path.** A change would need its own governing act, and a defined atomic operation that preserves the previous reference, act and approver in the audit trail. Because OQ-2 excludes lifecycle fields and the audit mechanism is non-durable (§11), whether M2 includes a governed **replace** operation is **FQ-3**. No lifecycle column is introduced for it. *2026-09-29, FQ-3 DECIDED: create-only for M2. Any future governed replacement is a separate decision, with explicit audit-preservation semantics. §15.A* |
| **Deletion / unbinding** | **Not available.** OQ-2 decided "no unbinding … in M2". Any removal needs a separate governed decision |
| Replacement attempted without governance | There is no write path for it. A second insert for the same identifier is rejected by UNIQUE (§14) |

## 11. H — Auditability

| Question | Where answered |
|---|---|
| Who caused the binding | ~~`approved_by_actor_id` (row, durable) and~~ `record_audit` `actor_id` (log) *(2026-09-29, IP-3 §15.B: the executing actor is recorded only through the existing audit mechanism. Who approved is carried by the governing act, which is durable in the repository and verified in CI)* |
| Which act authorized it | `governing_act` (row, durable) and audit metadata (log) |
| When it became effective | `bound_at` (row, durable) |
| What reference was bound | `implementation_reference` (row, durable) and audit metadata (log) |
| Denied or failed attempts | `record_audit` with DENIED/FAILED (log only) |

**The existing audit mechanism is reused; no new audit subsystem is created.** `record_audit`/`publish_event` are log-based stand-ins (C-114 is not implemented). The row itself is the durable record of the *current* binding. History of denied attempts, and of any future replacement (FQ-3), exists only in logs. This limitation is recorded; it is not solved here.

## 12. I — Read Path and BAE Boundary (the physical design supports FO-2)

| Actor | Role | Physical touch point |
|---|---|---|
| BAR (`bar_registration`) | Identity and registration authority | Read-only by the BAE adapter (2b) and by the write service (§7 step 3) |
| Binding store | Implementation-binding authority | Written only by the governed write service; read-only by the BAE adapter (`BindingSource`, 2c) using `business_activity_identifier` equality; no cache (OQ-3) |
| BAE | Resolution authority | No persistence; consumes adapter ports; realization keyed by `implementation_reference` (16.D) |
| Host adapter | Read-only boundary | SELECT only. It raises on failure and never converts a failure into "no binding" (16.E) |
| M2 | Resolution only | Returns an opaque handle; never invokes |
| M5 | Invocation | Out of scope |

The UNIQUE identifier column guarantees that the adapter's lookup returns zero or one row. More than one row is impossible by constraint, so 16.I's "more than one current row" case becomes structurally unreachable, and stays in 16.I only as a defensive malformed-response check.

## 13. J — Reconciliation (OQ-4; design, not implemented)

| Check point | Compares | Input source |
|---|---|---|
| **Pre-deployment/CI** | The bindings that *will* be live against the build's realization keys | CI has no access to a production database. The binding set must come either from (a) a pre-deployment step with read access to the target environment's binding store, or (b) the governing acts in the repository, which would also give CI-time act-to-row verification (§8.3). **FQ-6** *2026-09-29, FQ-6 DECIDED: (a), a read of the target environment's binding store, is the authoritative CI binding input. CI act-citation verification is a separate check under FQ-2. §15.A* |
| **Host start-up** | Rows in the host's binding store against the host's realization keys | The host's own store (read-only) and the realization |

| State | CI result | Start-up result |
|---|---|---|
| Aligned | pass | pass |
| Binding without realization | **fail** (block deployment) | **fail closed**. ~~Whether start-up aborts the host or marks the identifier unresolvable is **FQ-6**; in either case,~~ *2026-09-29, FQ-6 DECIDED: fail closed **per identifier**, and the host is not aborted. The affected identifier becomes unresolved/unavailable and is never invoked;* resolution returns `REALIZATION_UNAVAILABLE` (16.I) |
| Realization without binding | reported orphan (not a failure) | reported orphan |
| Malformed or conflicting binding (blank field, bad identifier shape, citation not resolvable when act checking is adopted) | **fail** | **fail closed** (`MALFORMED_BINDING_RESPONSE` at resolution) |

The check reads only. It never writes a binding and never invokes a Business Activity.

## 14. K and L — Security, Multi-Tenancy and Failure Semantics

**Security and multi-tenancy:**
- The store is platform-global, with no tenant or organization column (K.3).
- Neither the write service nor the adapter accepts organization or tenant input.
- ~~Caller claims are used **only** for the write-authority check (FQ-1), never to select or filter bindings.~~ *2026-09-29, FQ-1 DECIDED (c): there is no runtime write path, so no caller claims participate in binding writes. Claims are never used to select or filter bindings.*
- A caller-supplied tenant identity cannot influence resolution, because the lookup key is the identifier alone.
- `CLAUDE.md §21.4` must be re-applied if any write endpoint is exposed (FQ-1/FQ-3). *(2026-09-29: none is exposed under FQ-1 (c) and FQ-3 create-only. §21.4 applies again if a later governed decision adds one.)*

**Failure semantics** (design level; no HTTP semantics invented):

| Case | Detected at | Behaviour |
|---|---|---|
| Duplicate binding for an identifier | Pre-check, then UNIQUE backstop | Rejected, no retry. Audit DENIED. No row change |
| Duplicate implementation reference | — | **Permitted** under the approved many-to-one reading (§6). ~~If FQ-4 selects 1:1, it becomes a UNIQUE rejection~~ *(FQ-4 DECIDED many-to-one, 2026-09-29)* |
| Missing or blank governing act | Validation, then NOT NULL/CHECK backstop | Rejected before insert. Audit DENIED |
| Unauthorized executor | ~~Authority check (step 3)~~ *2026-09-29: database-role separation (FQ-7); no runtime authority check exists under FQ-1 (c)* | ~~Rejected before any write. Audit DENIED~~ *A write attempted without the binding-write role is refused by the database. No row is created* |
| Invalid act-to-row relationship (act not naming this identifier/reference) | ~~**Not detectable today** (§8.3). Detectable once FQ-2 is decided, at write time or in CI~~ *2026-09-29, FQ-2 DECIDED (a): detected by CI citation verification against repository documents (§8.3)* | ~~Recorded gap~~ *CI failure: deployment blocked. Not a database constraint* |
| Unregistered BAR identifier | BAR check (step 3) | Rejected. Audit DENIED |
| Replacement without governance | No such operation exists; a second insert hits UNIQUE | Rejected |
| Transaction failure (database, session) | Any step | Full rollback, no partial row, no SUCCESS audit. The error is raised, never retried as a different operation |

## 15. Open FO-3 Design Questions (to be decided by the Repository Owner; none is decided here)

*2026-09-29: all eight are now DECIDED; see §15.A. The table below is preserved unchanged as the original open-question record.*

| ID | Question | Evidenced options (not invented) | Why it matters |
|---|---|---|---|
| **FQ-1** | Which runtime authority executes binding writes? | (a) `require_platform_admin`: claims-only, the weakest option, and the same fail-open class as TD-171; (b) a constitutional authority seat on the `authority_holders` / `require_authority_holder` pattern, which needs a **new authority identity** (constitutional work, not FO-3); (c) no runtime write path: bindings are written only by a governed, reviewed deployment-time data operation citing the act | It defines authority-to-row enforcement (§8.2) and whether any write endpoint exists |
| **FQ-2** | What is the governing act, and how is its existence verified? | (a) An ADR/ROD-style record per binding, with the citation checked in CI against repository documents; (b) a BAR-style registering act; (c) a new canonical act registry (a new governed object, needing its own decision) | Without it, act-to-row enforcement stays partial (§8.3) |
| **FQ-3** | Does M2's write path include a governed **replace**, or create-only? | Create-only (minimum); create plus a governed atomic replace (needs a defined audit-preservation rule) | OQ-2 excludes lifecycle; replacement semantics are otherwise undefined |
| **FQ-4** | Must `implementation_reference` be unique (1:1)? | Many-to-one (as the approved reconciliation wording implies); 1:1 (add UNIQUE) | Cardinality; reconciliation states |
| **FQ-5** | How does a non-AuthService host verify BAR registration at write time? | Deferred with `RO-M1-11` | The write-time BAR check (§7 step 3) |
| **FQ-6** | What input does CI reconciliation use, and what does start-up do on failure? | CI: target-environment store read, or governing acts in the repository. Start-up: abort the host, or fail closed per identifier | OQ-4 realization (§13) |
| **FQ-7** | Is database-role separation (write-service role vs read-only adapter role) required? | Required; or not (application-only enforcement) | Closes "write around the service" (§8.2). No established repository pattern was verified |
| **FQ-8** | Physical bounds: the implementation-reference length, and a portable identifier-shape CHECK | Fixed at implementation design | TD-175 / TD-176 portability |

## 15.A Repository Owner Decisions on FQ-1 to FQ-8 (2026-09-29)

*Recorded by Repository Owner instruction ("Record the following Repository Owner decisions for FO-3 FQ-1 through FQ-8", 2026-09-29; design-only governance update).*
- The open-question record in §15 above is preserved unchanged as the historical record.
- Earlier wording that these decisions overtake is struck through, with dated addenda, in §0 (the header), §4, §5, §6, §7, §8.2, §8.3, §9, §10, §13, §14, §16 and §19.

### 15.A.1 Decisions

| FQ | Status | Decision | Rationale (as given by the RO) | Deferred dependency | Affected FO-3 sections |
|---|---|---|---|---|---|
| **FQ-1** Runtime binding-write authority | **DECIDED** | **Option (c):** "No runtime write path: bindings are written only by a governed, reviewed deployment-time data operation citing the act." | Do not introduce a new constitutional authority seat. Do not use claims-only `require_platform_admin` as the binding-write authority. Avoid reproducing the fail-open authority class identified alongside TD-171. Binding creation is a governed data operation, not a normal runtime Business Activity endpoint. The BAE does not own or perform binding writes | None. Consequence: the source of `approved_by_actor_id` ~~is open as IP-3 (§15.A.3)~~ *was open as IP-3. Resolved 2026-09-29 by withdrawing the field (§15.B). The FQ-1 decision is unchanged* | §4 (field 5), §7, §8.2, §14 |
| **FQ-2** Governing act | **DECIDED** | **Option (a):** "An ADR/ROD-style record per binding, with the citation checked in CI against repository documents." | Reuse the existing AUREX governance mechanism. Do not create a new canonical database-backed act registry. Do not create a second BAR-style identity/registration authority. CI verification establishes that the cited governance act exists in the governed repository and corresponds to the binding. Physical act-to-row enforcement stays constrained by the repository-governed nature of the act; no database FK to a non-existent act registry is claimed | None | §8.3, §9, §14, §16 |
| **FQ-3** Replacement | **DECIDED** | **CREATE-ONLY FOR M2.** No governed replace operation is part of the M2/FO-3 implementation | OQ-2 established present-equals-bound with no lifecycle. Introducing replacement now would silently create lifecycle semantics. A future governed replacement requirement must be a separate decision with explicit audit-preservation semantics | Any future replacement is a separate governed decision | §7, §10, §11, §14 |
| **FQ-4** Implementation-reference cardinality | **DECIDED** | **MANY-TO-ONE.** Multiple BAR identifiers may reference the same opaque implementation reference. **No UNIQUE on `implementation_reference`.** The BAR identifier remains unique within the binding store | Consistent with the approved FO-2 reconciliation model. The implementation reference identifies a realization, not a unique Business Activity | None | §4 (field 3), §6, §14 |
| **FQ-5** Non-AuthService BAR verification | **DECIDED — DEFERRED UNDER `RO-M1-11`** | No cross-service BAR-read mechanism is invented in FO-3 | `RO-M1-11` already governs this deferred issue. FO-3 records the dependency and boundary but does not solve it. Binding creation cannot claim complete write-time BAR verification until the governed cross-service mechanism exists | **`RO-M1-11`** (IP-2) | §5, §7 step 3 |
| **FQ-6** Reconciliation input / start-up failure | **DECIDED** | **CI:** a read of the target environment's binding store is the authoritative binding input for reconciliation. **Host start-up:** fail closed **per identifier**, rather than aborting the entire host | CI validates the actual governed binding state intended for the target environment. Host start-up detects deployment/runtime mismatch. One invalid Business Activity realization must not unnecessarily terminate the entire hosting service. The affected identifier becomes unresolved/unavailable. FO-2's `REALIZATION_UNAVAILABLE` semantics are preserved. The Business Activity is not invoked when reconciliation fails | CI access to the target environment's binding store (IP-5) | §13 |
| **FQ-7** Database role separation | **DECIDED** | **REQUIRED.** The binding-write service database role and the BAE read-only adapter/database role are separated | Prevents "write around the service". Adds a database-level enforcement boundary in addition to application authorization. The read-only adapter must not possess binding-write privileges. If implementation reveals that the existing infrastructure cannot support this cleanly, the implementation constraint is recorded; the decision is not silently weakened | Infrastructure support is unverified (IP-4) | §8.2, §14 |
| **FQ-8** Physical bounds / portability | **DECIDED** | **FIX DURING IMPLEMENTATION DESIGN.** Explicit implementation-time bounds are defined for the `implementation_reference` length and for portable `BA-NNNNNN` identifier validation. The implementation must validate against both the repository's SQLite test environment and the PostgreSQL production target | FO-3 sets no numeric length, because no existing authoritative platform constraint establishes one. FQ-8 is not turned into another architecture decision | Implementation design (IP-6); TD-175, TD-176 | §4 (field 3), §6 |

### 15.A.2 Distinctions preserved

- **FQ-2 has four separate steps; none substitutes for another:**
  1. **Act citation:** the row's `governing_act` names an ADR/ROD-style record.
  2. **CI verification:** a CI check confirms that the cited record exists in the governed repository and corresponds to the binding's identifier and reference.
  3. **Row creation:** the governed, reviewed deployment-time data operation under the binding-write database role (FQ-1 (c), FQ-7).
  4. **Runtime resolution:** read-only BAE consumption through the adapter, which never writes (§12).
- **Binding write ≠ BAE runtime resolution** (K.7(b)/(c)). The BAE neither owns nor performs binding writes.
- **FO-3 act-to-row enforcement ≠ TD-171 BAR execution-eligibility enforcement** (§16). TD-171 remains OPEN and unchanged.

### 15.A.3 Remaining implementation prerequisites (none authorized by this approval)

| ID | Prerequisite | Source |
|---|---|---|
| IP-1 | **TD-171** resolved or otherwise governed, as a separate prerequisite to any M2 implementation authorization | `IRA-BAE-001-M2 §16.H`; §16 |
| IP-2 | A governed cross-service BAR-read mechanism under **`RO-M1-11`**. Until it exists, complete write-time BAR verification cannot be claimed for a binding store in a non-AuthService host | FQ-5 |
| IP-3 | **The source of `approved_by_actor_id` under FQ-1 (c).** The original §4/§7 derivation, "from the authority check", no longer applies, because no runtime authority check exists. How the approving identity is determined for a governed deployment-time data operation, or whether the field is retained, is not settled by FQ-1 to FQ-8. It must be settled by the Repository Owner before implementation design, and is not invented here. **RESOLVED (design) 2026-09-29, §15.B:** `approved_by_actor_id` is withdrawn from the binding row | Consequence of FQ-1 |
| IP-4 | Verification that the infrastructure supports separate binding-write and read-only database roles. If it does not, the constraint is recorded and FQ-7 is not weakened | FQ-7 |
| IP-5 | CI access to the target environment's binding store, as the reconciliation input. CI act-citation verification, as a separate check | FQ-6, FQ-2 |
| IP-6 | Implementation-design bounds: the `implementation_reference` length and portable `BA-NNNNNN` validation, tested on SQLite and PostgreSQL | FQ-8; TD-175, TD-176 |
| IP-7 | The §13 B2 implementation checklist, which is **OUTSTANDING** and is not regenerated here | `IRA-BAE-001-M2 §13` |
| IP-8 | A separate Repository Owner authorization of M2 implementation | CLAUDE.md §18/§19.4 |

### 15.A.4 What FO-3 approval does NOT authorize

FO-3 approval authorizes none of the following:
- the physical binding table;
- any migration;
- the binding write service or the deployment-time data operation;
- the adapter;
- the reconciliation implementation (CI or start-up);
- any TD-171 implementation;
- M2 implementation.

Each needs its own separate authorization. **M2 remains NOT AUTHORIZED / NOT STARTED.**

## 15.B IP-3 Resolution — Treatment of `approved_by_actor_id` (2026-09-29)

*Recorded by Repository Owner instruction to resolve IP-3 without introducing a new authority model or a runtime authorization mechanism. FQ-1 to FQ-8 are not reopened.*

**Resolution (design).** `approved_by_actor_id` is **withdrawn** from the binding row. The minimum row is `id`, `business_activity_identifier`, `implementation_reference`, `governing_act` and `bound_at` (§4).

**Why the field cannot stay.**
- Under FQ-1 (c), no runtime authority check exists, so no verified actor record exists to derive the value from.
- Populating it from the operation's own input would make it caller-supplied. §4 prohibited that from the start.
- Populating it with a fixed or system value would make the row falsely imply that a verified approver was recorded.
- Either way, the row would claim an authorization it did not check. Removing the field is the only treatment that stays truthful without inventing a mechanism.

**Where accountability is represented instead (existing mechanisms only):**

| Question | Represented by | Existing mechanism |
|---|---|---|
| Who approved the binding | The **governing act** (an ADR/ROD-style Repository Owner decision record), cited in `governing_act` | The repository governance-record convention (FQ-2 (a)) |
| Does the approval exist, and does it name this binding | **CI verification** of the citation against repository documents | FQ-2 (a); IP-5 |
| Who executed the deployment-time row creation | `record_audit` `actor_id` (the executing identity supplied to the operation, or `"SYSTEM"`), with `governing_act` in the audit metadata | `observability.record_audit`. This is exactly how `BarRegistrationService` records its actor (`actor_id or "SYSTEM"`) |
| When the binding became effective | `bound_at` on the row | — |
| How resolution consumes it | A read-only BAE adapter that never writes (§12) | FO-2 16.E |

**Repository evidence that this is the established pattern:**
- `bar_registration` (WP-23 Workstream C; model `models/bar_registration.py`; migration `b8c9d0e1f2a3`) is the closest precedent: a governed, act-cited registration with no runtime authority check (TD-171). Its row carries `registering_act` and `registered_at`, and **no actor or approver column**. The actor appears only in `record_audit`.
- `authority_holders` likewise records the governing instrument (`appointment_instrument_ref`) and carries no appointing-actor column.
- The `tenant_registry.approved_by_actor_id` precedent, cited in the original §4, applies only to a **runtime, authority-gated** write (`require_ai002_holder`). FQ-1 (c) excludes that class of write, so it no longer applies to bindings.

**What this does not introduce:**
- no authority seat, authority registry, act registry or runtime authorization dependency;
- no TD-171 logic and no BAR execution eligibility.

**The four steps stay distinct:**
1. **Governing-act citation:** `governing_act`.
2. **CI verification:** FQ-2 (a).
3. **Deployment-time row creation:** FQ-1 (c) under the binding-write database role (FQ-7), with audit via `record_audit`.
4. **Runtime resolution:** read-only; the BAE never writes (§12).

**Disclosed limitation (unchanged, §11).** The executing actor is recorded only in the log-based `record_audit` stand-in (C-114 is not implemented), which is not durable storage. The durable accountability record is the governing act in the repository, together with the operation's review. This is the same limitation `bar_registration` already carries. It is disclosed, not solved here.

**IP-3 status: RESOLVED (design).**

## 16. M — FO-3 / TD-171 Boundary

| | FO-3 (this document) | TD-171 |
|---|---|---|
| Record | The implementation-binding store | `bar_registration` (BAR) |
| Concern | Act-to-row enforcement for **bindings** | Act-to-row enforcement and reconciliation for **BAR registration and execution eligibility** |
| Status | ~~Designed (partial enforcement; FQ-1, FQ-2 open)~~ *Design approved 2026-09-29 (FQ-1 to FQ-8 decided, §15.A); not implemented* | **OPEN**, unchanged |

They share a root cause, the absence of a canonical governance-act model, and FQ-2's eventual answer may inform TD-171. *(2026-09-29: FQ-2 is decided for **bindings only**. That decision neither applies to nor resolves `bar_registration` / TD-171.)* **FO-3 act-to-row enforcement ≠ TD-171 BAR execution-eligibility enforcement. They are not combined, and nothing here resolves or closes TD-171.** TD-171 remains a separate prerequisite to any M2 implementation authorization (`IRA-BAE-001-M2 §16.H`).

## 17. N — Physical Implementation Deferred

- No `CREATE TABLE`, SQL, migration, ORM model, repository, service, adapter, router or test is created by this document.
- The table name is not fixed here. It is to be chosen at implementation design and recorded in the MTA under AMD-017's concept.
- The MTA itself is not amended by FO-3: AMD-017 records the concept, and a physical MTA entry follows implementation authorization.

## 18. Traceability

| Source | Where applied |
|---|---|
| RD-M2-02 / `ADR-043` §4.1–§4.4, §9 | §4, §6, §7, §8, §12 |
| AMD-017 (MTA v7.4 PART K) K.1–K.9, H.5 | §4 (concepts), §5 (hosting), §7 (K.7 write-path separation), §13 (K.5), §17 |
| FO-2 `IRA-BAE-001-M2 §16`, §16.L (OQ-1 to OQ-4) | §4 exclusions, §6, §10, §12, §13 |
| `IMP-001 §6.15.4`, `§6.16.5` | §12 (resolution via BAR; terminate if unresolved) |
| WP-23 A–C (`b0f5a12`) | §5 (no FK; runtime and write-time BAR checks), §16 |
| `bar_registration` row/audit pattern (`models/bar_registration.py`, `BarRegistrationService` `record_audit` actor), `authority_holders.appointment_instrument_ref` | §15.B (IP-3) |
| TD-157, TD-171, TD-175, TD-176 | §3, §6, §8.3, §16, FQ-8 |
| `require_platform_admin`, `require_authority_holder`, `enforce_approval_authority`, `tenant_registry` approval pattern, `record_audit`/`publish_event` | §3, §7, §8, §11, FQ-1 |

## 19. Readiness

| Item | State |
|---|---|
| **FO-3** | ~~**DESIGN COMPLETE — NOT IMPLEMENTED — pending RO approval** (FQ-1 to FQ-8 open; act-to-row enforcement partial until FQ-1/FQ-2)~~ **DESIGN APPROVED / NOT IMPLEMENTED** (2026-09-29, §15.A; implementation prerequisites §15.A.3; non-authorizations §15.A.4) |
| **FQ-1 to FQ-8** | **DECIDED** (2026-09-29, §15.A; FQ-5 deferred under `RO-M1-11`) |
| **IP-3** (`approved_by_actor_id`) | **RESOLVED (design)**: field withdrawn (2026-09-29, §15.B). The other IP items in §15.A.3 remain implementation prerequisites |
| **FO-1** | **DONE** (AMD-017, MTA v7.4, commit `867af46`) |
| **FO-2** | **DESIGN APPROVED** (`accc127`) |
| **TD-171** | **OPEN** |
| **§13 B2 checklist** | **OUTSTANDING** |
| **M2** | **NOT AUTHORIZED / NOT STARTED** |

**Integrity:**
- No code, table, migration, schema, model, repository, service, adapter or test was created or modified.
- BAR (WP-23 A–C), `BAR-INDEX.md`, ADR-043, the ROD and the MTA are unchanged by this document.
- TD-170 and TD-171 are unchanged.
- Nothing was staged, committed or pushed.
- *2026-09-29:* recording the FQ-1 to FQ-8 decisions (§15.A) changed only this document. No code, schema, BAR A–C file, TD-171 entry or the §13 checklist was changed, and nothing was staged, committed or pushed.
