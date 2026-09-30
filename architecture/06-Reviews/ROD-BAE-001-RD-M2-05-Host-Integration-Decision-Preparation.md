# ROD-BAE-001 — RD-M2-05 Host Integration (B2 M2) — Decision Preparation

**Work Package:** `WP-BAE-001`, milestone M2 (Business Activity Resolution & BAR Integration).
**Prepared:** 2026-09-30, by Repository Owner instruction ("Prepare the RD-M2-05 Host Integration Decision Package").
**Status:** ~~**READY FOR DECISION — NO OPTION SELECTED.**~~ **DECIDED — RD-M2-05** *(2026-09-30, Repository Owner; §21)*: OQ-05-1 = H-A; OQ-05-2 = fail closed at start-up; OQ-05-3 = explicit dependency provisioning; OQ-05-4 = M2 may extend CI for M2 verification; OQ-05-5 = interim reuse of the WP-13 path helper.
- *(2026-09-30: the preparation in §1–§20 is preserved as the analysis presented for decision.)*
- The evidence (§3, §4) is sufficient to establish the host, the lifecycle hook and the CI boundary.
- A recommendation is given in §9. It is **not** a decision. *(2026-09-30: the Repository Owner selected H-A; §21.)*
- Five open questions (§18) accompany the decision.

**Nothing is authorized.** **M2 remains NOT AUTHORIZED / NOT STARTED. M2-P remains CHARTERED / NOT AUTHORIZED / NOT STARTED.**

This document creates nothing executable: no code, package, start-up hook, adapter, realization, migration, test, CI change or packaging. It modifies no ADR, Master Technical Architecture text, IRA, Charter, `WPR-001` entry or `TECH-DEBT.md` entry.

---

## 1. Decision Statement

**RD-M2-05 — Host integration.** Where, and through which existing boundary and lifecycle hook, is B2 M2 hosted? It must be hosted so that:
- the read-only `BindingSource` adapter reads the M2-P binding store;
- start-up reconciliation runs at an authoritative host boundary;
- FO-2/FO-3 reconciliation semantics are implementable without inventing an integration point;
- M2 stays read-only.

RD-M2-05 was **selected in principle** on 2026-09-25 (`IRA-BAE-001-M2 §0`): "an additive AuthService integration boundary, proposed as `Backend/Services/AuthService/bae_integration/` … subject to the detailed M2 implementation design". The regenerated §13 (`66f0aed`) leaves open:
- the detailed design;
- the TD-165 import or packaging choice;
- the start-up wiring point (§13.1, §13.4, §13.8, §13.9).

This package prepares that detail.

## 2. Current Status

*(2026-09-30: superseded by §21. RD-M2-05 is DECIDED. The text below records the status at preparation.)*

**READY FOR DECISION.** Every fact the decision needs was verified in code and configuration (§3). No stop condition applies:
- the host is established (§4);
- no option requires reopening FO-2 or FO-3, changing RD-M2-07 ownership, or changing the B2 authority model;
- no irreconcilable contradiction was found.

One behaviour is not specified by FO-2/FO-3: start-up when the binding store itself is unreadable (§11). It is presented as an open question within RD-M2-05's detail (OQ-05-2), not as a reopening.

## 3. Evidence Reviewed (read directly, 2026-09-30)

| Evidence | Finding |
|---|---|
| Search of `Backend/Services/**/*.py` (excluding venvs) for `BusinessActivityEngine`, `AuthorizationEngine`, `runtime_engine_path`, `bar_registration` | **Only AuthService** references a runtime engine or BAR (11 files). AIService, IngestionService, ReportingService and TenantService reference none |
| Search of `Backend/**/*.py` for `business_activity_engine` outside `Backend/Runtime/BusinessActivityEngine/` | **No importer.** BAE M1 is not integrated into any host |
| `Backend/Services/AuthService/bae_integration/` | **Does not exist** |
| `Backend/Services/AuthService/authz_integration/` (`runtime_engine_path.py`, `domain_permission_resolver.py`) | The WP-13 precedent for hosting a runtime component in AuthService. `ensure_on_path()` inserts `Backend/Runtime/AuthorizationEngine` into `sys.path` ("a disclosed, pragmatic interim measure", TD-165-class). It is used by `dependencies.py:131` (`enforce_domain_permission`), which composes the engine per call |
| `Backend/Runtime/BusinessActivityEngine/business_activity_engine/engine.py`, `ports.py`, `pytest.ini` | `BusinessActivityEngine(registration_source, …, manifest_resolver=None)` is constructed by its caller. The core imports AuthorizationEngine's `adapters` and `authorization` packages. Its own tests run with `pythonpath = . ../AuthorizationEngine`. **A host needs both runtime roots importable** |
| `Backend/Services/AuthService/main.py:19–30` | The **only** start-up hook: a FastAPI `lifespan` that runs `await db_manager.initialize()` before `yield` and `await db_manager.close()` after. There is no other start-up, composition or bootstrap registration in the process |
| `Backend/Services/AuthService/models/database.py:24–52` | `initialize()` creates the async engine and sessionmaker lazily. It opens no connection. The URL comes from `config.settings` (`DATABASE_URL` env var, else `Config/platform-config.yaml`) |
| `Backend/Services/AuthService/routers/health.py` | `/health` (liveness: `SELECT 1`) and `/ready` (readiness: DB reachable and `BootstrapService.is_bootstrapped()`), each on a per-request session. There is no start-up state or reconciliation in either |
| Search for existing start-up reconciliation | **None exists.** The only "reconciliation" hits are the unrelated `person_reconciliation_decisions` (C-006) |
| `Backend/Services/AuthService/tests/conftest.py` | The `client` fixture uses `with TestClient(app)`, so **every TestClient test enters the lifespan**. Sessions are overridden only for `db_manager.get_session` dependencies. A lifespan-time read would use the **configured** database, not the test SQLite |
| `.github/workflows/authservice-ci.yml` | **Test job:** `pytest tests/` on SQLite; no `DATABASE_URL`; no database service. **Bootstrap job:** ephemeral `postgres:16`, `alembic upgrade head`, bootstrap twice, then `uvicorn main:app` polled on `/ready`. It is the only CI job that starts the real process against PostgreSQL. **BAE and AuthorizationEngine suites are not run by CI.** There is no deployment job and no target environment |
| `Config/platform-config.yaml` `database:` comments | Local development uses a superuser. A non-superuser `auth_service_user` is intended but not yet granted. **No read-only role exists** (relevant to FQ-7) |
| `IRA-BAE-001-M2` §0 (RD-M2-05), §12, §13 (`66f0aed`, `3303237`), §14, §16.A–§16.I, §16.L | The decision in principle; tenant placement; the B2 checklist; the approved M2 design |
| `ADR-042` (`RO-M1-01` in-process, own database session; `RO-M1-03`; §6 addendum), `ADR-043` (K-7, K-10; §12 addendum) | The BAE runs in-process in each host. The binding store is per host. Adapters are injected. The core stays persistence-free |
| MTA v7.4 PART K (K.3–K.5, K.7) | Per-host store; adapter consumption; reconciliation at CI **and** host start-up; the write/read split |
| `TDS-BAE-001-M2-FO3 …` §4–§6, §12–§14, §15.A (FQ-6, FQ-7) | The store M2 reads; fail-closed per identifier; role separation required |
| `ROD-BAE-001-M2-Binding-Infrastructure-Ownership-Decision-Preparation.md` §11 | RD-M2-07 (M2-P owns C1–C3; M2 owns C5, C7); RD-M2-08 (infrastructure prerequisite) |
| `WP-BAE-001` Charter §10 (M2-P, M2), §17; `WPR-001` WP-BAE-001 row | Milestone scope; no authorization |
| `IMP-001 §6.15.4`, `§6.16.3`, `§6.16.5`; `RTA-001 §6.6` | Resolution through BAR; termination before execution; no implementation-specific discovery |
| `TECH-DEBT.md` TD-165, TD-170, TD-171, TD-175, TD-176; `RO-M1-11` | See §16 |

## 4. Actual Host / Integration Landscape

1. **Where BAE M1 integrates today:** nowhere. The package exists and is tested in isolation. No host imports it.
2. **The process that will host BAE M2:** **AuthService.** It is the only service holding BAR (`bar_registration`, D2/D5). It is the only service already hosting a runtime component (WP-13). RD-M2-05 named it in principle. `RO-M1-11` defers any cross-service BAR read, so no other host can verify registration in M2.
3. **`bae_integration/`:** does not exist. `authz_integration/` is the structural precedent.
4. **Start-up path:** `main.py` `lifespan` → `db_manager.initialize()` → serve → `db_manager.close()`.
5. **Composition:** there is no application-level composition root or DI container. Runtime components are composed **per call** at the point of use (`dependencies.py::enforce_domain_permission`).
6. **Health/readiness:** `routers/health.py` (`/health`, `/ready`), per-request and stateless.
7. **CI start-up:** only the bootstrap job starts the process (uvicorn), against an ephemeral PostgreSQL. The test job starts the app only through `TestClient`.
8. **Existing start-up reconciliation:** none.
9. **Host:** AuthService. No new BAE host is needed or evidenced.
10. **Architecture permits it:** yes. An additive package under AuthService plus a minimal lifespan call reopens no approved decision. RD-M2-05 (a) anticipated the package, and §13 requires RD-M2-05 to name the wiring point.

## 5. Current M1 Integration Boundary

- The M1 core (`Backend/Runtime/BusinessActivityEngine/`) is persistence-free (boundary tests).
- It exposes ports: `RegistrationSource.is_registered -> bool`, and `ManifestResolver` with `UnimplementedManifestResolver`.
- It has no host adapter, import path, composition or start-up participation.
- Its only external import is the AuthorizationEngine package (M1 stage 4).

## 6. Candidate Options (derived from evidence)

| Option | Host / package | Start-up reconciliation point | TD-165 mechanism |
|---|---|---|---|
| **H-A** | AuthService, new `bae_integration/` package (mirrors `authz_integration/`) | **FastAPI `lifespan` in `main.py`:** one call into `bae_integration` after `await db_manager.initialize()` and before `yield` | Interim path helper in `bae_integration/`, reusing `authz_integration.runtime_engine_path.ensure_on_path()` for the AuthorizationEngine root (the WP-13 precedent) |
| **H-B** | As H-A | **Lazy, at BAE composition** inside `bae_integration` (when a caller first builds the engine). `main.py` unchanged | As H-A |
| **H-C** | As H-A | As H-A (lifespan) | **Formal packaging:** a `pyproject.toml` for both Runtime components, installed editable into AuthService (`requirements` and CI install change) |
| **H-D** | Defer the host adapter (RD-M2-05 original option (c)), or a new dedicated BAE host service | — | — |

`/ready` participation (reporting reconciliation state through `routers/health.py`) was considered as a variant and is **not** offered as an option:
- a per-identifier failure must not take the whole host out of service (FQ-6);
- nothing in FO-2 or FO-3 asks for a readiness signal.

## 7. Decision Criteria

1. Reuses an existing host boundary rather than inventing one (`CLAUDE.md §19.5`, Reuse → … → Create).
2. Start-up reconciliation actually runs at host start-up in a deployed process (OQ-4, FQ-6, K.5).
3. M2 stays read-only against BAR and the binding store (RD-M2-07, K-2, K.7).
4. The BAE core stays persistence-free, with adapters injected by the host (K-10).
5. Minimal change to existing AuthService modules (§13.8).
6. No change to certified components (WP-RTA-001 `AuthorizationEngine`) without governance.
7. It does not break the existing test harness or CI.
8. It stays within `RO-M1-11`: AuthService only.

## 8. Findings, RD-M2-05.1 to RD-M2-05.9

**RD-M2-05.1 Host:** **AuthService**, in-process (`RO-M1-01`). Evidence: §4 items 2 and 9.

**RD-M2-05.2 Integration location:** a new, additive `Backend/Services/AuthService/bae_integration/` package, owning:
- the `RegistrationSource` adapter over `BarRegistrationRepository.get_by_identifier`;
- the `BindingSource` read-only adapter over M2-P's store;
- the explicit realization construction (the host's composition of reference → object);
- the start-up reconciliation entry point;
- the M2 BAE import path.

M2-P's store, migration, write operation and CI act-citation check are **not** placed here (§10).

**RD-M2-05.3 Start-up reconciliation:**
- It runs from the host start-up hook (H-A) through a single `bae_integration` function.
- It reads the store through the read-only adapter on a `db_manager` session, and compares it with the realization keys.
- It records the set of identifiers whose binding has no realization. The host-composed resolver consults that set and returns `EXECUTION_FAILED` / `REALIZATION_UNAVAILABLE` for those identifiers only. The process continues.
- It writes nothing to BAR or the store, imports nothing dynamically, and makes no authority check.
- Because no BAE execution path is exposed by AuthService in M2 (no router invokes the BAE; the first consumer is M7), completing reconciliation inside the lifespan, before `yield`, necessarily precedes any future execution path.

**RD-M2-05.4 Lifecycle:**
- The authoritative point is **application lifespan start-up** (`main.py` `lifespan`, after `db_manager.initialize()`, before `yield`). It is the only start-up hook the process has.
- Process start-up has no separate hook. Dependency composition is per-call and lazy (§4 item 5). There is no explicit BAE initialization today.
- Under H-B, reconciliation would never run in a deployed M2 process, because nothing composes the BAE at M2. That fails criterion 2.

**RD-M2-05.5 CI:**
- **Pre-deployment reconciliation against the target store is not available.** There is no deployment job and no target environment (RD-M2-08; FQ-6 OUTSTANDING). Nothing may claim it.
- The **bootstrap job** already starts `uvicorn main:app` on an ephemeral PostgreSQL after `alembic upgrade head`. Under H-A it would exercise start-up reconciliation against an **ephemeral** store: PostgreSQL start-up evidence, relevant to TD-176, but **not** target-store reconciliation, and it must never be reported as such.
- Adding BAE or AuthorizationEngine suites, or any reconciliation step, to CI changes `.github/workflows/authservice-ci.yml`. That is a CI change **outside M2's §13.4 file list**, and needs a decision (OQ-05-4).

**RD-M2-05.6 Service boundary:** a **new integration package under the existing host** (AuthService). RD-M2-05's in-principle selection already covers it. No new host, and no governance decision beyond RD-M2-05's detail, is needed. A new BAE host service (H-D) has no repository basis and would contradict `RO-M1-01`.

**RD-M2-05.7 M2-P boundary:** unchanged from RD-M2-07; see §10. H-A needs M2-P to supply a readable model or query surface for the store (the §13.9 stop condition if it does not).

**RD-M2-05.8 AuthService start-up constraint:**
- **Yes.** The `main.py` `lifespan` is the correct wiring point. It is the only start-up boundary. It already owns database-resource initialization, which reconciliation depends on. It runs in every real process (uvicorn, including the CI bootstrap job).
- Wiring requires **modifying an existing AuthService module (`main.py`)**. §13.8 and §13.9 allow this only for the RD-M2-05-approved wiring point, which this decision would name.
- **Constraint:** the lifespan also runs in every `TestClient` test, and in the CI test job there is no database behind the configured URL. The start-up read would therefore meet an unreachable store in the test harness. OQ-05-2 and OQ-05-3 must be decided so this is handled explicitly and fails closed, not by silently skipping.

**RD-M2-05.9 Minimum change (future, not authorized):**
- one new package, `bae_integration/`;
- one call site in `main.py` `lifespan`;
- no change to `dependencies.py`, routers, `health.py`, `authz_integration/`, `models/`, `repositories/` (read-only reuse only), BAR files or `AuthorizationEngine`;
- no application-wide DI container or refactor.

## 9. Recommended Option (not a decision)

**H-A** is recommended. It is the only option that meets all eight criteria:
- it reuses the existing host, the existing package precedent, and the only existing start-up hook;
- it runs reconciliation at real host start-up;
- it keeps the change to one additive package and one lifespan call;
- it leaves certified `AuthorizationEngine` packaging untouched (the TD-165 interim, as WP-13 did).

H-C remains available if the Repository Owner prefers to resolve TD-165 fully now. Its consequences are in §15.

## 10. Boundary: M2 / M2-P / Infrastructure (unchanged from RD-M2-07 and RD-M2-08)

| Area | Owns |
|---|---|
| **M2** (`bae_integration/` plus the BAE core) | Typed `RegistrationSource` adapter. Read-only `BindingSource` adapter. Realization construction. Start-up reconciliation and the per-identifier fail-closed set. Runtime resolution (stage 2). The opaque `ResolvedBusinessActivity` handle. The M2/M5 boundary (never invoke) |
| **M2-P** | The physical binding table, schema and migration (AuthService migration chain). The governed deployment-time write operation. CI governing-act citation verification. The in-repository role-separation specification |
| **Infrastructure (RD-M2-08)** | Database roles and credentials: a read-only adapter role and a write role (FQ-7). Target-environment binding-store access for CI reconciliation (FQ-6). Any deployment pipeline |

H-A shifts no responsibility between these.

## 11. Start-up Reconciliation Boundary

- **Runs:** in `lifespan`, after `db_manager.initialize()`, before `yield`, as a single `bae_integration` call.
- **Reads:** the binding store (through the read-only adapter) and the host's realization keys.
- **Writes:** nothing. No BAR access is needed for binding↔realization reconciliation (the §16.F states).
- **Produces:**
  - aligned: resolvable;
  - binding without realization: that identifier fails closed (`REALIZATION_UNAVAILABLE`), and the host continues;
  - realization without binding: a reported orphan (log via the existing `observability` stand-ins);
  - disagreement: rejected at realization construction, or `MALFORMED_BINDING_RESPONSE` at run time.
- *(2026-09-30: decided by OQ-05-2, §21.1. An unreadable store makes AuthService start-up fail. The options below are preserved.)* **Not specified by FO-2/FO-3 (OQ-05-2):** the behaviour when the store is **unreadable at start-up** (connection failure, missing table). This is not one of the four §16.F states. At run time the approved answer is `BINDING_SOURCE_UNAVAILABLE`, raised and never converted. The start-up answer must be decided: fail every identifier closed and continue, or abort start-up. It must never be treated as "aligned" or as "no bindings".

## 12. CI Reconciliation Boundary and Infrastructure Dependency

- **Target-store CI reconciliation (C4, FQ-6):** **not available.** It depends on the RD-M2-08 external prerequisite. It is required before the first governed binding write to a deployed environment. It is not an M2 deliverable.
- **What the repository can do today:** the bootstrap job's uvicorn start-up (H-A) would run start-up reconciliation against an ephemeral, migrated PostgreSQL store. This is useful TD-176-class evidence. It is reported only as "start-up reconciliation on an ephemeral store".
- **Workflow change:** any CI workflow change needs OQ-05-4.

## 13. Files a Future Implementation Would Touch (knowable now; not authorized)

| File | Role |
|---|---|
| `Backend/Services/AuthService/bae_integration/` *(new package; module names fixed at M2 implementation design)* | Import path (TD-165 interim); registration adapter; binding adapter; realization construction; start-up reconciliation entry point |
| `Backend/Services/AuthService/main.py` | **One call** in `lifespan` after `db_manager.initialize()` (the RD-M2-05 wiring point) |
| `Backend/Runtime/BusinessActivityEngine/business_activity_engine/` (`ports.py`, `engine.py`, `results.py`, `__init__.py`, plus new realization/reconciliation modules) | Per §13.4 A |
| Tests | Per §13.4 A and §13.6 |

Under H-C only: `pyproject.toml` for both Runtime components, AuthService `requirements.txt`, and CI install steps.

## 14. Files That Must NOT Be Touched

- `Backend/Services/AuthService/dependencies.py`;
- `routers/**`, including `health.py` (no `/ready` change);
- `authz_integration/**` (imported, never modified);
- `models/**`, `repositories/**`, `services/**` (BAR read reuse only);
- every BAR A–C file and migration; `BAR-INDEX.md`;
- `Backend/Runtime/AuthorizationEngine/**` (under H-A);
- all M2-P files;
- `alembic/**` (M2 adds no migration);
- `.github/workflows/**`, unless OQ-05-4 authorizes a change;
- `Config/platform-config.yaml`; infrastructure.

## 15. Governance Consequences per Option

| Option | Consequence |
|---|---|
| **H-A** | Names `main.py` `lifespan` as the approved wiring point, satisfying the §13.1 RD-M2-05 box's detail. TD-165 stays **Open** (the interim path helper, as WP-13). Needs OQ-05-2 and OQ-05-3. No ADR, FO or ownership change |
| **H-B** | No `main.py` change. But start-up reconciliation would not run at host start-up in M2 (OQ-4, FQ-6, K.5 unmet in any deployed process) unless another start-up trigger is added, which would mean inventing one. It would need a Repository Owner ruling that "start-up" may mean "first composition", which amounts to reinterpreting OQ-4 |
| **H-C** | As H-A, plus it **resolves TD-165**. It changes the packaging of the certified `WP-RTA-001` `AuthorizationEngine`, AuthService dependencies and CI install. A broader change, touching a certified component, that needs explicit authorization |
| **H-D** | Leaves M2's "real query against BAR" objective unmet (RD-M2-05 (c)), or creates a new host with no basis, contradicting `RO-M1-01` and `RO-M1-11`. It would need a new architectural decision |

## 16. Dependencies

| Item | Relation to RD-M2-05 |
|---|---|
| TD-165 | Chosen here: H-A keeps it Open (interim), H-C resolves it |
| TD-170 | Unaffected. It must still be committed before M2 authorization (§13.1) |
| TD-171 | Unaffected. It remains an M2 authorization prerequisite. H-A reads BAR registration only as FO-2 already designs |
| TD-175 | Unaffected |
| TD-176 | H-A's lifespan call gives a natural PostgreSQL start-up venue (the bootstrap job). Adapter-level PostgreSQL tests (T-18) still need a venue (OQ-05-4) |
| FQ-6 | Target-store CI reconciliation remains an RD-M2-08 prerequisite. H-A does not satisfy it |
| FQ-7 | The read-only adapter role is still unprovisioned. `platform-config.yaml` shows local superuser use and an ungranted `auth_service_user`. The adapter must be able to run under a separate read-only role; T-17 stays OUTSTANDING evidence |
| `RO-M1-11` | AuthService only; no cross-service BAR read |

## 17. Traceability

| Source | Applied in |
|---|---|
| `ADR-042` (`RO-M1-01` in-process on the host's own session; `RO-M1-03`; §6 addendum) | §4, §8 (05.1, 05.6) |
| `ADR-043` (K-7 per-host store; K-10 injected adapters; §12 addendum) | §8 (05.2), §10 |
| MTA v7.4 PART K (K.3, K.4, K.5 reconciliation at CI and start-up, K.7) | §8 (05.3–05.5), §11, §12 |
| FO-2 (`IRA-BAE-001-M2` §16.A, §16.D–§16.F, §16.I, §16.L OQ-3, OQ-4) | §8, §11 |
| FO-3 (`TDS-BAE-001-M2-FO3` §12–§14; FQ-6, FQ-7) | §11, §12, §16 |
| RD-M2-07, RD-M2-08 (`ROD-BAE-001-M2-Binding-Infrastructure-Ownership …` §11) | §10, §12 |
| §13 (`66f0aed`, `3303237`): §13.1 RD-M2-05 box; §13.4 wiring-point row; §13.8; §13.9 | §1, §8 (05.8), §13, §14 |

## 18. Open Questions for the Repository Owner

*(2026-09-30: all five are decided; §21. The table is preserved as presented.)*

| ID | Question | Evidenced options |
|---|---|---|
| **OQ-05-1** | Host option | H-A (recommended), H-B, H-C, H-D (§6, §15) |
| **OQ-05-2** | Start-up behaviour when the binding store is unreadable (not a §16.F state) | (i) Record every identifier as fail-closed (`BINDING_SOURCE_UNAVAILABLE`) and continue start-up. (ii) Abort start-up. Treating it as "no bindings" is excluded by §16.E/§16.I |
| **OQ-05-3** | Test-harness treatment of the lifespan call. Every `TestClient` test enters the lifespan, and the CI test job has no database | (i) Tests supply the reconciliation's session and realization explicitly, as they already override `db_manager.get_session`, so the lifespan call is exercised deterministically. (ii) The lifespan call follows OQ-05-2 against the unreachable configured database. Silently skipping reconciliation in tests is excluded |
| **OQ-05-4** | CI scope for M2 | (i) No workflow change in M2: BAE/PostgreSQL evidence produced outside CI and recorded. (ii) Authorize an M2 change to `authservice-ci.yml` to run the BAE suite and PostgreSQL-backed M2 tests. Target-store reconciliation stays with RD-M2-08 either way |
| **OQ-05-5** | TD-165 | Interim path helper (H-A, TD-165 stays Open) or formal packaging (H-C, TD-165 resolved) |

## 19. Decision Options (compact)

| Option | Host | Wiring point | TD-165 | Start-up at host start-up | Existing-module change | Recommended |
|---|---|---|---|---|---|---|
| H-A | AuthService, `bae_integration/` | `main.py` `lifespan` | Interim (Open) | Yes | `main.py` (one call) | **Yes** |
| H-B | AuthService, `bae_integration/` | Lazy composition | Interim (Open) | **No** in M2 | None | No |
| H-C | AuthService, `bae_integration/` | `main.py` `lifespan` | Packaging (resolved) | Yes | `main.py`, `requirements.txt`, CI, AuthorizationEngine packaging | Alternative |
| H-D | Deferred or new host | — | — | — | — | No |

## 20. Readiness Statement

~~**RD-M2-05: READY FOR DECISION — NO OPTION SELECTED.**~~ *(2026-09-30: **DECIDED**; §21.4.)* Deciding it (OQ-05-1 to OQ-05-5) would complete the RD-M2-05 prerequisite and the §13.1 box's detail. It would **not** authorize M2.

Deciding RD-M2-05 leaves every other §13.1 prerequisite unchanged:
- M2-P is CHARTERED / NOT AUTHORIZED / NOT STARTED;
- TD-171 is OPEN;
- TD-170, TD-176, FQ-6 and FQ-7 are OUTSTANDING;
- §13 is PREPARED / NOT APPROVED.

**M2 remains NOT AUTHORIZED / NOT STARTED.**

**Integrity:** only this document was created. Nothing was staged, committed or pushed.

## 21. Repository Owner Decision Record (2026-09-30)

**Recorded** by direct Repository Owner instruction ("Record the Repository Owner decisions for RD-M2-05"). Each decision is recorded as stated and is not reinterpreted. **Governance only:**
- no `bae_integration/` package, `main.py` change, CI change, test, TD entry, ADR or Master Technical Architecture change is made;
- M2 is not authorized.

### 21.1 Decisions

| OQ | Selected | Decision (as recorded) | Rationale | Implementation consequence (future, not authorized) | Out of scope |
|---|---|---|---|---|---|
| **OQ-05-1** Host | **H-A** | AuthService is the canonical BAE M2 runtime host. The BAE runs in-process. Future M2 integration uses a new additive `bae_integration/` package, modelled on the existing `authz_integration/` precedent. The FastAPI `lifespan` in `Backend/Services/AuthService/main.py` is the start-up integration boundary. H-C is **not** selected | Only AuthService holds BAR and hosts a runtime component. The lifespan is the process's only start-up hook (§3, §4, §8) | A new `bae_integration/` package; one call in `main.py` `lifespan` after `db_manager.initialize()` (§13, §8 RD-M2-05.9) | WP-13 is not reopened. No change to `dependencies.py`, routers, `health.py`, `authz_integration/**` or `AuthorizationEngine` (§14) |
| **OQ-05-2** Unreadable binding store | **Fail closed at start-up** | If the M2-P binding store cannot be read during mandatory start-up reconciliation, **AuthService start-up fails**. An unreadable store must **never** be interpreted as an empty binding set. If the store reads successfully but a particular implementation cannot be resolved, `REALIZATION_UNAVAILABLE` is retained for that identifier | It preserves the fail-closed discipline of §16.E/§16.I, so an unreadable authority is never read as "no bindings" | Start-up reconciliation raises on a store-read failure, and the lifespan does not reach `yield`. Per-identifier realization failures stay per-identifier | No additional runtime state is invented. **FO-2 and FO-3 are not reopened.** This resolves the RD-M2-05 question only |
| **OQ-05-3** Test harness | **Explicit dependency provisioning** | M2 tests must explicitly provide the required database/session and realization dependencies. Production start-up behaviour must not be weakened or silently bypassed because the current SQLite `TestClient` suite has no database. Tests covering start-up reconciliation must use an appropriate database-backed setup | It keeps OQ-05-2 intact in production. The existing harness enters the lifespan in every `TestClient` test (§3) | M2's test design supplies these dependencies to the lifespan call and to the reconciliation tests | Not implemented now. No change to `tests/` or `conftest.py` in this decision |
| **OQ-05-4** CI | **M2 may extend CI for required M2 verification** | M2 implementation may later extend the existing CI workflow where required to verify M2. Such changes are limited to M2 verification. The current throwaway-PostgreSQL bootstrap job is **not** target-environment reconciliation | The BAE suite and PostgreSQL-backed M2 tests are not run by CI today (§3) | A later M2 change to `.github/workflows/authservice-ci.yml`, limited to M2 verification, within M2's authorized scope | FQ-6 stays an external infrastructure/deployment prerequisite for target-store reconciliation (RD-M2-08). CI is not modified now |
| **OQ-05-5** TD-165 | **Interim reuse of the WP-13 path helper** | M2 may temporarily reuse WP-13's existing `authz_integration.runtime_engine_path.ensure_on_path()`. M2 must not modify the certified AuthorizationEngine implementation to resolve TD-165. **TD-165 remains OPEN** | It follows the disclosed WP-13 interim precedent and avoids changing a certified component | `bae_integration/` provides the BAE import path and reuses `ensure_on_path()` for the AuthorizationEngine root | Formal packaging, or refactoring AuthorizationEngine runtime-path management, needs a separate decision. `TECH-DEBT.md` is unchanged |

### 21.2 Resulting boundaries

| Area | Owns |
|---|---|
| **M2** (`bae_integration/` plus the BAE core) | The read-only `RegistrationSource`; the read-only `BindingSource`; the host adapter; the realization; start-up reconciliation (lifespan, OQ-05-2); runtime resolution; the opaque resolved handle |
| **M2-P** | The binding store; its schema and migration; the governed deployment-time binding write; CI governing-act citation verification |
| **Infrastructure (RD-M2-08)** | Database-role provisioning (FQ-7); target binding-store access (FQ-6) |

### 21.3 Recorded facts

- `bae_integration/` does not yet exist.
- No start-up reconciliation exists today.
- The AuthService `lifespan` is the future integration point.

### 21.4 State after this decision

| Item | State |
|---|---|
| RD-M2-05 | **DECIDED** (H-A; OQ-05-1 to OQ-05-5) |
| M2 | **NOT AUTHORIZED / NOT STARTED** |
| M2-P | CHARTERED / NOT AUTHORIZED / NOT STARTED |
| §13 | PREPARED / NOT APPROVED |
| TD-171 | OPEN |
| TD-165 | OPEN (interim path helper) |
| TD-170, TD-176, FQ-6, FQ-7 | OUTSTANDING |

Deciding RD-M2-05 does not authorize M2.

### 21.5 Traceability

| Source | Decision link |
|---|---|
| `ADR-042` (`RO-M1-01` in-process, own session; `RO-M1-03`) | OQ-05-1 (AuthService, in-process) |
| `ADR-043` (K-7 per-host store; K-10 injected adapters) | OQ-05-1, OQ-05-2 (per-host store read by an injected adapter) |
| AMD-017 (MTA v7.4 PART K: K.4, K.5 start-up reconciliation, K.7) | OQ-05-1 (lifespan is the start-up point), OQ-05-2 |
| FO-2 (`IRA-BAE-001-M2` §16.E, §16.F, §16.I, §16.L OQ-4) | OQ-05-2 (fail-closed; `REALIZATION_UNAVAILABLE` retained; not reopened) |
| FO-3 (`TDS-BAE-001-M2-FO3` §12–§14; FQ-6, FQ-7) | OQ-05-2, OQ-05-4 |
| RD-M2-07 | §21.2 (M2-P ownership unchanged) |
| RD-M2-08 | OQ-05-4 (target-store reconciliation stays external); §21.2 |
| §13 (`66f0aed`, `3303237`): §13.1 RD-M2-05 box, §13.4 wiring-point row, §13.8, §13.9 | OQ-05-1 names `main.py` `lifespan` as the approved wiring point |
| TD-165 | OQ-05-5 (remains OPEN) |
| FQ-6 | OQ-05-4 (external prerequisite) |
| FQ-7 | §21.2 (infrastructure); T-17 evidence outstanding |

### 21.6 Compact decision table

| OQ | Decision |
|---|---|
| OQ-05-1 | H-A: AuthService, in-process; `bae_integration/`; `main.py` `lifespan` |
| OQ-05-2 | Unreadable store at start-up means start-up fails; never read as empty; `REALIZATION_UNAVAILABLE` per identifier retained |
| OQ-05-3 | Tests provision the session and realization explicitly; production start-up is not weakened |
| OQ-05-4 | M2 may extend CI, only for M2 verification; the throwaway PostgreSQL is not target reconciliation; FQ-6 external |
| OQ-05-5 | Interim reuse of `ensure_on_path()`; no AuthorizationEngine change; TD-165 OPEN |

*~~End of decision preparation.~~ End of decision record. RD-M2-05 DECIDED (2026-09-30). No implementation authorized. M2 remains NOT AUTHORIZED / NOT STARTED.*
