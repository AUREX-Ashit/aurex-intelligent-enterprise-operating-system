# ROD-BAE-001-M2 — B2 Binding Infrastructure: Ownership and Scope — Decision Preparation (RD-M2-07, RD-M2-08)

**Work Package:** `WP-BAE-001`, milestone M2 (Business Activity Resolution & BAR Integration).
**Prepared:** 2026-09-29, by Repository Owner instruction ("prepare the GOVERNANCE DECISION PACKAGE required before any M2 implementation can begin"). This follows the §13 B2 readiness assessment of the same date.
**Status:** ~~**READY FOR DECISION — NO OPTION SELECTED.**~~ **DECIDED (2026-09-29, §11): RD-M2-07 = Option B; RD-M2-08 = Option (a).**
- ~~This document prepares two Repository Owner decisions, **RD-M2-07** and **RD-M2-08**. It makes neither. The observations in §6 are recommendations only.~~ *(2026-09-29: both decisions were made by the Repository Owner and are recorded in §11. The preparation in §1–§10 is preserved as the analysis presented for decision.)*
- The decisions authorize **no implementation** (§11.3).
- **M2 remains NOT AUTHORIZED and NOT STARTED.**

**This document creates nothing executable.**
- No table, schema, migration, model, repository, service, adapter, CI job, packaging, test or binding row is created.
- No Charter, ADR, `IRA-BAE-001-M2`, FO-3 design, `WPR-001`, `TECH-DEBT.md` entry or Master Technical Architecture text is modified.
- The §13 checklist is **not** regenerated (§8).

---

## 1. The Decisions

**RD-M2-07 — Ownership and scope of the B2 physical binding infrastructure.**
Which Work Package or milestone owns each component in §4? In particular, is the physical binding store, with its write operation and verification, part of M2 or delivered outside it?

**RD-M2-08 — The infrastructure prerequisites of FQ-6 and FQ-7.**
- FQ-6 needs CI access to the target environment's binding store. FQ-7 needs database-role separation.
- No deployment environment, deployment pipeline, database-role pattern or infrastructure Work Package exists in the repository (§2).
- Who owns these prerequisites, and at what point must they exist?

## 2. The Gap (repository evidence)

| # | Evidence | Source |
|---|---|---|
| G-1 | FO-3's approval authorizes none of these: the binding table, a migration, the binding write service or deployment-time data operation, the adapter, reconciliation, TD-171 work or M2 | FO-3 §15.A.4 (`e7c713b`) |
| G-2 | The M2 checklist forbids "A new table or migration" | `IRA-BAE-001-M2 §13.8`. It was written for M-B, which needed no table (§13.2 FO-2 note) |
| G-3 | The approved M2 boundary excludes the write side. M2 "will not … create, change or retire bindings; define the governed write path" | `IRA-BAE-001-M2 §16.A` (FO-2, approved `accc127`) |
| G-4 | ADR-042 left "the manifest contract, schema, **storage**, or artifact form" to **M2** | `ADR-042 §6` (`RO-M1-03`) |
| G-5 | "each host that runs BAE-routed Business Activities will need its own binding table, migration, host-side adapter and governed write path once implementation is authorized". **No Work Package or milestone is named** | `ADR-043 §6` |
| G-6 | The BAE owns "the governed mapping *BAR-issued Business Activity Identifier → Business Activity implementation/manifest*" | `ADR-042 §3`/`§4.3` (`RO-M1-03`) |
| G-7 | The BAE runs in-process "on its own database session" in each host. Services never access another service's database | `ADR-042 §4.1`, `§6`; `CLAUDE.md §8`; `ADR-043` K-7 |
| G-8 | The Charter's M2 major scope includes "Manifest Resolution". Its M2 exclusions cover BAR writes and BAR schema only | `WP-BAE-001` Charter §10 M2 |
| G-9 | No infrastructure or deployment Work Package exists. `source/infrastructure/` is empty. There is one `DATABASE_URL` and no `GRANT`/`CREATE ROLE` anywhere. CI (`.github/workflows/authservice-ci.yml`) has only a throwaway `postgres:16` service with one user | `WPR-001`; repository search, 2026-09-29 |
| G-10 | BAR's owner is excluded: the binding is "**not** a BAR table" | `ADR-043` K-2; `ADR-042 §7` |

**The contradiction.**
- Ownership of the mapping is decided: it is the BAE (G-6). ADR-042 assigned storage to M2 (G-4).
- But the later, approved FO-2 boundary excludes the binding write path from M2 (G-3), and §13.8 excludes tables (G-2).
- FO-3 authorizes no physical work (G-1), and ADR-043 names no owner (G-5).
- So no current document authorizes or assigns the store, the write operation, CI act verification or reconciliation.
- G-4 and G-3 must be reconciled by an RO decision, not by assumption.

## 3. Fixed Constraints (decided; not reopened)

| ID | Constraint | Source |
|---|---|---|
| F-1 | BAR is the canonical Business Activity identity and registration authority. The BAE never registers or issues identity | D2, D5; `ADR-043 §4.1`, K-2 |
| F-2 | The BAE never writes the binding. Binding creation is a governed, reviewed deployment-time data operation, with no runtime write path | FQ-1 (c); FO-2 §16.A; MTA K.7(c) |
| F-3 | The binding row has no actor or approver field | IP-3 (FO-3 §15.B) |
| F-4 | Act-to-row verification is a CI citation check against repository documents, with no act registry | FQ-2 (a) |
| F-5 | Create-only. Many-to-one reference. There is no lifecycle, caching, host column or tenant column | FQ-3, FQ-4, OQ-1 to OQ-3 |
| F-6 | CI reconciliation reads the target store. Start-up reconciliation fails closed per identifier (`REALIZATION_UNAVAILABLE`) | FQ-6, OQ-4 |
| F-7 | Database-role separation is **required** and may not be silently weakened | FQ-7 |
| F-8 | One store per hosting service, in that service's own database | K-7; `ADR-042 §4.1` |
| F-9 | TD-171 is separate from the B2 binding mechanism and stays OPEN | FO-3 §16; `IRA §16.H` |
| F-10 | FQ-5 is deferred under `RO-M1-11`, so there is no cross-service BAR read | FQ-5 |
| F-11 | M2 returns an opaque handle and never invokes it. M5 owns invocation and transactions | RD-M2-06; FO-2 §16.G |
| F-12 | The BAE core stays persistence-free. Host adapters are injected | K-10; M1 boundary tests |

## 4. Components to Allocate

| C | Component | Nature |
|---|---|---|
| C1 | Binding table, schema and migration (first host: AuthService, under RD-M2-05) | Host persistence, write-side structure |
| C2 | Governed deployment-time binding write operation | Write side (F-2) |
| C3 | CI governing-act citation verification | Governance verification (F-4) |
| C4 | CI reconciliation against the target binding store | Deployment verification (F-6). Needs target-environment access |
| C5 | Host start-up reconciliation (per identifier, fail-closed) | Read-only runtime check. Needs the realization type (FO-2 §16.D) |
| C6 | Database-role separation (write role vs read-only adapter role) | Infrastructure plus migration/grant specification (F-7) |
| C7 | M2 read-only `BindingSource` port and host adapter | Read side. Already inside the approved M2 boundary (FO-2 §16.A, §16.E) |

## 5. Options

| Option | Allocation | For (evidence) | Against (evidence) |
|---|---|---|---|
| **A** — All in M2 | C1 to C7 in M2. §13.8 is replaced | ADR-042 §6 assigned storage to M2 (G-4). Mapping ownership is the BAE's (G-6) | It contradicts approved FO-2 §16.A, which keeps the write path out of M2 (G-3); moving C2 in would need FO-2 reopened. It places C4/C6, which are blocked on non-existent infrastructure (G-9), inside M2, so M2 cannot pass its own completion gate until infrastructure exists. It mixes a write-side, schema-bearing deliverable with a read-only resolution milestone under one `§19.7` gate |
| **B** — Separate WP-BAE-001 milestone before M2 | A new WP-BAE-001 milestone (working label **"M2-P"**, name to be fixed by the RO) owns C1, C2, C3 and the in-repository part of C6. M2 owns C5 and C7. C4 and the provisioning part of C6 go to RD-M2-08 | Ownership stays with the decided owner (G-6, `RO-M1-03`). FO-2 §16.A's read-only M2 boundary is preserved (G-3). §13.8's "no new table or migration" stays valid **for M2**. The store is physically in the host's own database and migration chain (G-7, F-8) under the RD-M2-05 host boundary. Every milestone already requires its own `§19` checklist and `§19.7` gate (Charter §10, §13) | It needs a Charter §10 amendment (a new milestone) and a `WPR-001` update. ADR-042 §6's "storage (M2)" needs a dated reconciliation note |
| **C** — An existing host or service Work Package | C1 to C3 assigned to a Work Package already working in AuthService (for example WP-13) | Code lands in AuthService either way | No existing Work Package owns Business Activity resolution. WP-13 is Authorization Runtime Integration, so this would couple unrelated domains (`CLAUDE.md §8`). It would split the mapping away from its decided owner (`RO-M1-03`), contrary to "one capability, one owner" |
| **D** — A new dedicated Work Package | A new Work Package owns C1 to C4 and C6. WP-BAE-001 M2 consumes it | Clean isolation of the write side | It creates a second owner for a mapping `RO-M1-03` already assigns to the BAE. It adds a Charter, IRA and five-gate closure for a single-host store. It gains no separation that Option B does not already give inside the rightful owner |
| **E** — A governed platform binding-store owner, plus a BAE M2 consumer | An owner separate from the BAE holds C1 to C4 and C6. M2 holds C5 and C7 | It matches the write/read separation in K.7 | **No such owner exists in the repository.** Designating one would invent a new ownership construct (`CLAUDE.md §21`). Option B already achieves the write/read split *within* the decided owner |

**RD-M2-08 options** (for C4 and the provisioning part of C6):
- **(a)** The C1 to C3 owner specifies the in-repository parts: role grants in the host migration, and the CI job definition. Provisioning of the target environment and the second database credential is recorded as an **external operational prerequisite**. It must exist before the **first governed binding write to any deployed environment**, not before M2 code. If provisioning proves infeasible, the constraint is recorded under FQ-7 without weakening it.
- **(b)** A separate, future infrastructure Work Package owns provisioning of the target environment, credentials and pipeline. Charters for C4 and C6 wait for it.
- **(c)** Defer C4 and C6 provisioning to M7 (first real consumer), with the constraint recorded, and hold every deployed binding write until then.

## 6. Observations (for the Repository Owner; not a selection)

1. **Option B is the smallest allocation consistent with every fixed constraint and every approved design.**
   - It keeps the mapping with its decided owner (`RO-M1-03`).
   - It keeps M2 read-only, as approved (FO-2 §16.A).
   - It keeps §13.8 valid for M2.
   - It places the store in the host's own database (F-8).
   - It needs no new owner or Work Package.
   - Options C, D and E each create or displace an owner. Option A reopens FO-2 §16.A.
2. **C5 (start-up reconciliation) fits M2, not M2-P.** It is read-only and needs the realization type M2 delivers (FO-2 §16.D). C7 is already M2 (FO-2 §16.E).
3. **C4 and C6 provisioning cannot be allocated from repository evidence alone** (G-9). RD-M2-08 is therefore a genuine RO decision.
   - Option (a) is the smallest that preserves FQ-6/FQ-7 without blocking resolution code indefinitely.
   - That rests on one fact: M2 binds no real capability activity (`IRA §13.8`), so no deployed binding exists for CI to reconcile until the first governed write.
4. **Under B, M2 depends on M2-P passing its own `§19.7` completion gate.** M2's host adapter and tests need the real table.
5. **None of RD-M2-07 or RD-M2-08 affects TD-171** (F-9). TD-171 remains a separate prerequisite to M2 authorization.

## 7. What a Decision Does Not Authorize

Selecting any option authorizes **no implementation**. In particular it does not authorize:
- M2-P or M2 implementation, the table, a migration, a write operation, a CI job, reconciliation, database roles or credentials;
- any binding row or real Business Activity binding;
- any BAR change or BAR registration;
- any TD-171 or TD-176 work, or closure of any debt item.

Each milestone needs its own `CLAUDE.md §19` checklist and an explicit Repository Owner implementation authorization naming its scope (Charter §10, §17).

## 8. Effect on §13 and on M2 Authorization

**§13.8.**
- Under B (or C, D, E), "A new table or migration" **remains valid for M2**. It should get a dated note that the store is delivered by its owner (M2-P under B).
- Under A, the line must be replaced by the exact store scope, and FO-2 §16.A must be reopened for C2.

**M2 authorization** cannot be requested until all of the following hold:
- RD-M2-07 and RD-M2-08 are decided and their documents reconciled (§9);
- RD-M2-05's detailed design and the TD-165 choice are decided;
- TD-171 is closed, or an RO decision is recorded;
- TD-176 PostgreSQL evidence exists;
- the TD-170 entry is committed;
- under B, M2-P is complete through `§19.7`;
- §13 is regenerated for B2;
- the authorization names an AuthService-only scope, unless `RO-M1-11` is resolved.

## 9. Documents to Reconcile After the Decision (not edited here)

*(2026-09-29: the reconciliation performed after the decision is listed in §11.4.)*

| Document | Required reconciliation |
|---|---|
| `WP-BAE-001` Charter §10, §17 | Under B: add the M2-P milestone (objective, scope C1–C3 and C6-spec, dependencies, verification, exclusions); add a dated note on the M2 scope ("Manifest Resolution" consumes the store); update §17 status lines. Under A: amend the M2 scope and exclusions |
| `WPR-001` WP-BAE-001 row | Record the milestone structure and status |
| `ADR-042 §6`, `ADR-043 §6` | Dated addenda naming the owner of "storage" and "each host … will need its own binding table …". Not a change of decision |
| `IRA-BAE-001-M2` header, §13, §15, §16.J, §16.K | Point the FO-3 status at `e7c713b`; change "not committed yet" to `867af46`; add rows for RD-M2-07, RD-M2-08, TD-176, the TD-170 commit and M2-P completion; regenerate §13 (IRA §13 structure proposal prepared with this package) |
| `TDS-BAE-001-M2-FO3 …` §15.A.3, §17 | Name the owner of IP-4, IP-5 and IP-6, and of the physical implementation |
| `Master_Technical_Architecture.md` PART K | No change now. A physical entry follows implementation authorization (FO-3 §17) |
| `TECH-DEBT.md` | No closure. Commit of TD-170 only by separate authorization |

## 10. Traceability

`ADR-042` (`RO-M1-01`, `RO-M1-03`, §4.1, §6, §7); `ADR-043` (§4, K-2, K-7, K-10, §6, §7); `IRA-BAE-001-M2` §0, §13, §16.A, §16.D–§16.G, §16.K, §16.L; `TDS-BAE-001-M2-FO3` §15.A, §15.B, §17; MTA v7.4 PART K (K.3, K.5, K.7); `WP-BAE-001` Charter §10, §13, §17; `WPR-001`; `CLAUDE.md §8`, §18, §19, §21; `.github/workflows/authservice-ci.yml`; TD-165, TD-170, TD-171, TD-175, TD-176; `RO-M1-11`.

## 11. Repository Owner Decision Record (2026-09-29)

**Recorded** by direct Repository Owner instruction ("Record the Repository Owner decisions for RD-M2-07 and RD-M2-08"). Each decision is recorded as stated and is not reinterpreted.

### 11.1 RD-M2-07 — Ownership: **DECIDED — Option B**

**A separate pre-M2 milestone within WP-BAE-001 owns the B2 physical binding infrastructure.**

**Milestone name: `M2-P` — Governed Implementation Binding Store.**
- The repository has no precedent for inserting a milestone, and renumbering M1–M7 would break the M2/M5 references in `ADR-042`, `ADR-043`, `IRA-BAE-001-M2`, FO-2, FO-3 and `TECH-DEBT.md`.
- `M2-P` collides with no existing identifier, so the working label is adopted as the milestone identifier.

**The decision:**
- WP-BAE-001 remains the owner of the BAR-identifier → implementation mapping (`RO-M1-03`).
- The physical binding infrastructure is implemented in `M2-P`.
- **M2 remains a read-only consumer/resolver.** It does not create, modify, retire or write binding rows.
- Approved FO-2 §16.A is **not** reopened or weakened.

| C | Component | Owner |
|---|---|---|
| C1 | Physical binding table, schema and migration | **M2-P** |
| C2 | Governed deployment-time binding write operation | **M2-P** |
| C3 | CI governing-act citation verification | **M2-P** |
| C4 | CI reconciliation against the target binding store | **Infrastructure prerequisite, RD-M2-08** |
| C5 | Host start-up reconciliation | **M2** (part of M2's read-only resolution behaviour) |
| C6 | Database-role provisioning | **Infrastructure prerequisite, RD-M2-08.** FQ-7 remains REQUIRED |
| C7 | `BindingSource` port and read-only host adapter | **M2** |

**Preserved:**
- BAR remains the canonical identity authority. The BAE never writes BAR registration.
- TD-171 remains completely separate.
- FQ-5 remains deferred under `RO-M1-11`.
- M5 remains responsible for invocation and transaction semantics.

### 11.2 RD-M2-08 — Infrastructure: **DECIDED — Option (a)**

The required infrastructure provisioning is an **external operational prerequisite**. It must exist **before the first governed binding write is performed against a deployed environment**.
- Target-store access for CI reconciliation (C4) must be provided by deployment/infrastructure provisioning.
- Database-role separation (FQ-7) **remains REQUIRED**. The write-service role and the read-only adapter role must be provisionable.
- **The absence of infrastructure must not cause FQ-7 to be weakened.**
- **The absence of a target environment must not be disguised as successful CI reconciliation.** CI must not claim target-store reconciliation until the target store actually exists and is accessible.
- No new infrastructure Work Package is created to satisfy this decision.
- Provisioning is not implemented now. **RD-M2-08 does not authorize production infrastructure changes.**

### 11.3 What these decisions authorize, and what they do not

**They authorize** the allocation of ownership above and the governance reconciliation in §11.4. Nothing else.

**They do not authorize:**
- `M2-P` implementation, the binding table, a migration, the write operation, a CI job or reconciliation;
- infrastructure provisioning, database roles or credentials;
- any binding row;
- M2 implementation;
- any BAR change;
- TD-171 work.

**They do not close** TD-170, TD-171, TD-165 or TD-176. They do not satisfy FQ-6 or FQ-7: their infrastructure and implementation evidence remains **OUTSTANDING**. `M2-P` and M2 each need their own `CLAUDE.md §19` checklist and an explicit Repository Owner implementation authorization naming its scope (Charter §10, §17).

### 11.4 Reconciliation performed (2026-09-29; dated addenda only, historical wording preserved)

| Document | Reconciliation |
|---|---|
| `WP-BAE-001` Charter §10, §16, §17 | `M2-P` milestone added before M2. M2 note: read-only consumer; C5 and C7 in M2. Status and closure lines annotated |
| `WPR-001` WP-BAE-001 row | `M2-P` recorded as chartered, not authorized, not started. M2 unchanged |
| `IRA-BAE-001-M2` header, §0, §13 (status, §13.1, §13.8), §15, §16 status, §16.J, §16.K | RD-M2-07/08 DECIDED. The governance decision is distinguished from outstanding implementation and authorization. Full §13 regeneration is recorded as the **next** governance task |
| `ADR-042 §6`, `ADR-043 §6` | Dated reconciliation addenda. The original decisions are unchanged |
| `TDS-BAE-001-M2-FO3` §17 | A traceability pointer to the physical-implementation owner. The design and FQ-1 to FQ-8 are unchanged |
| Master Technical Architecture | **Not changed.** PART K names no Work Package or milestone, so no ownership terminology became stale |
| `TECH-DEBT.md` | **Not changed.** No item was closed |
| §13 full B2 regeneration | **Not performed.** It is the next governance task, after RD-M2-07/08 and before any M2 authorization |

### 11.5 Readiness after these decisions

| Item | State |
|---|---|
| RD-M2-07 | **DECIDED** (Option B; `M2-P`) |
| RD-M2-08 | **DECIDED** (Option (a)) |
| FO-1 | DONE |
| FO-2 | DESIGN APPROVED |
| FO-3 | DESIGN APPROVED / NOT IMPLEMENTED |
| FQ-1 to FQ-8 | DECIDED |
| IP-3 | SATISFIED |
| `M2-P` | CHARTERED — NOT AUTHORIZED / NOT STARTED |
| TD-171 | OPEN / unresolved |
| TD-170 | OUTSTANDING (the register entry is uncommitted) |
| TD-165 | OUTSTANDING; ~~a governance decision is still required (RD-M2-05)~~ *(2026-09-30: RD-M2-05 is DECIDED (`ROD-BAE-001-RD-M2-05-Host-Integration-Decision-Preparation.md` §21); OQ-05-5 selected the interim WP-13 path helper. The RD-M2-05 governance decision is no longer outstanding. TD-165 itself remains OPEN, and formal packaging needs its own future decision)* |
| TD-176 | OUTSTANDING |
| FQ-7 implementation evidence | OUTSTANDING |
| FQ-6 target-store infrastructure | OUTSTANDING |
| §13 B2 regeneration | OUTSTANDING (next governance task) |
| **M2** | **NOT AUTHORIZED / NOT STARTED** |

*~~End of decision preparation. READY FOR DECISION. M2 remains NOT AUTHORIZED and NOT STARTED.~~ End of decision record. DECIDED 2026-09-29 (RD-M2-07 = B; RD-M2-08 = (a)). No implementation authorized. M2 remains NOT AUTHORIZED and NOT STARTED.*
