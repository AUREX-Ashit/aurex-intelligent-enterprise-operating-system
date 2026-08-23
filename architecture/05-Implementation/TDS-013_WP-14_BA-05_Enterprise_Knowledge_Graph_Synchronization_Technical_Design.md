# TDS-013 — WP-14 BA-05 (C-092 Knowledge Graph Management) — Synchronize Enterprise Knowledge Graph — Technical Design Specification

**Document ID:** TDS-013
**Work Package:** WP-14
**Business Activity:** BA-05 — Synchronize Enterprise Knowledge Graph
**Basis:** `IRA-014_WP-14_Enterprise_Intelligence_Foundation_Implementation_Readiness_Assessment.md` §6 BA-05, §11 (Classification B — architecturally unblocked, Technical Design required before implementation)
**Governing constitutional authority (unchanged, cited not restated):** `ADR-023` (Enterprise Knowledge Graph Relationship Tenant Boundary), `Master_Technical_Architecture.md` AMD-016, `RTA-001 §12` (Knowledge Graph Runtime, full), `SD-002-108`/`109`/`111`/`013`, `ONT-001`, `CLAUDE.md §21.4` (Mandatory Tenant-Isolation Test Checklist)
**Status:** Technical Design — implementation NOT yet authorized. This document determines a mechanism; it does not authorize building it (§26).
**Reconciliation pass (this update):** integrates `§26a`'s three Repository Owner decisions (`RO-DEC-WP14-BA05-01`/`02`/`03`) into the main-body sections they each affect (§7–§9, §16–§17, §20, §24–§25), so the document carries one internally coherent current design position rather than a main body that still reads as open alongside a later addendum that reads as decided. No design element is added, removed, or altered by this pass beyond what §26a itself already recorded — this is integration, not new Technical Design. Superseded main-body language is marked, not deleted, per this repository's own no-silent-fix discipline (`ADR-017`/`METH-002`). This pass does **not** authorize BA-05 implementation and is **not** itself the fresh, independent Technical Design Authorization Review §26a/§26 both require — that review remains a separate, subsequent action performed by a reviewer with no involvement in this reconciliation.

---

## 1. Purpose and Scope

Determines **how** `ADR-023`'s four approved business rules (BR-1–BR-4) are enforced when BA-05 is implemented — the mechanism, not the decision. `ADR-023` and `AMD-016` already answer *what* the tenant boundary is and *that* `enterprise_knowledge_graph_registry.organization_id` represents it (§9). This document answers *where in the execution path* each rule is evaluated, *which components* perform the evaluation, and *what happens* on every failure path a synchronization attempt can take.

**In scope:** the Relationship Resolution mechanism for BA-05's own minimum chartered scope — the relational registry (`enterprise_knowledge_graph_registry`), triggered by BA-04's own Knowledge Asset `ACCEPTED` transition (`IRA-014 §6` BA-05 Dependencies row), per `RTA-001 §12.7`'s pipeline.

**Out of scope, explicitly:**
- The live Neo4j Aura graph write (`graph_engine_reference` population) — disclosed, deferred, unchanged from `IRA-014 §5.5`/`§5.6`.
- `cross_domain_relationship_registry` — outside `ADR-023` and outside BA-05 (`ADR-023 §6`).
- Redesigning the Knowledge Graph Runtime's own pipeline, entity list, or relationship-kind vocabulary (`RTA-001 §12.7`–`§12.9`) — this document places new logic *inside* the existing pipeline stages, it does not add, remove, or reorder stages.
- A new authorization model — §14 determines which *existing* mechanism applies to which of BA-05's two access shapes; it invents neither.
- BA-01 through BA-04's own Technical Design — unaffected, unchanged (`IRA-014 §11` items 1–2 remain open for those BAs independently).

## 2. Governing Decisions and References

| Document | What it settles, for this design |
|---|---|
| `ADR-023` | The tenant boundary is Organization; `organization_id` is nullable, never independently asserted, derived from/validated against the relationship's own two endpoints; BR-1–BR-4; authorization reuses `WP-10`'s pattern, not WP-13's; RTA-001 gets a minimal clarification only. |
| `AMD-016` | The physical column (`organization_id UUID REFERENCES organization_master(organization_id)`, nullable, indexed, RLS-governed) and BR-1–BR-4 as column documentation, enforcement mechanism explicitly deferred to Technical Design — this document. |
| `RTA-001 §12.9` (as amended) | *"Relationship Resolution shall validate the tenant boundary of both endpoints before persistence... never inferred after the fact."* Names the exact pipeline stage this design's tenant-boundary logic occupies. |
| `IRA-014 §6` BA-05, §11 | BA-05's own execution shape (event-triggered, no mandatory caller-facing establish endpoint; optional read endpoint); the two remaining open items this design must resolve or explicitly leave open (hosting service, BR-1–BR-4 enforcement mechanism). |
| `SD-002-108`/`109`/`111` | Tenant boundary is non-optional and non-inferable at query time (`108`); isolation is a storage/retrieval guarantee, not solely an access-control feature (`109` — directly grounds §22's RLS backstop); cross-tenant sharing requires an explicit mechanism that does not exist (`111` — grounds BR-4's default-reject). |

## 3. BA-05 Business Intent

Unchanged from `IRA-014 §6` BA-05: *"Resolve canonical entities and create semantic relationships in the Knowledge Graph's own relational registry, triggered by governed business outcomes."* Realizes `RTA-001 §12.7`'s pipeline against `enterprise_knowledge_graph_registry`. This design adds no new business intent — it operationalizes the existing one under the now-resolved tenant-boundary constraint.

## 4. BR-1–BR-4 (verbatim from `ADR-023 §5.3`, reproduced for this document's own traceability, not restated as a new decision)

- **BR-1:** if both endpoints are Organization-scoped, their `organization_id` values MUST match; a mismatch MUST reject the relationship — never silently reconciled.
- **BR-2:** if exactly one endpoint is Organization-scoped, the relationship inherits that endpoint's `organization_id`.
- **BR-3:** if neither endpoint is Organization-scoped (both platform-wide/Global), `organization_id` remains `NULL`.
- **BR-4:** cross-organization relationships are rejected unless and until an explicit, named, audited cross-tenant sharing mechanism exists (`SD-002-111`) — not built by this design.

**Relationship between BR-1 and BR-4, stated explicitly (not stated this precisely in `ADR-023` itself):** BR-4 is not a separate enforcement mechanism from BR-1 — it is BR-1's own mismatch outcome, named from the cross-organization angle. Any pair of endpoints resolving to two different, non-`NULL` `organization_id` values is simultaneously a BR-1 mismatch *and* a BR-4 cross-organization relationship; one derivation check enforces both. §10/§13 design this as a single mechanism.

## 5. Existing Architecture Components (Reuse Inventory, `CLAUDE.md §19.2`)

Directly inspected in the actual repository, not assumed:

| Component | Location | Reuse role |
|---|---|---|
| `enterprise_knowledge_graph_registry` (AMD-012/016) | `Master_Technical_Architecture.md` (line ~3134) | The target table — read/write directly, no new table. |
| `DatabaseSessionManager` / `db_manager` | `Backend/Services/AuthService/models/database.py` (pattern; AIService carries its own equivalent) | Session lifecycle: `async with sessionmaker() as session: ... await session.commit()` on success, `rollback()` on exception — reused verbatim for BA-05's own transaction (§15). |
| `require_matching_tenant_or_platform_admin`, `require_platform_admin` | `Backend/Services/AuthService/dependencies.py` | The exact WP-10 pattern `ADR-023 §5` item 5 names — reused for the optional read endpoint only (§14). |
| `Backend/Shared/Events` (`EventFactory`, `EventSubscriber`, `CloudEvent`, `EventContext`) | `Backend/Shared/Events/*.py` | The platform's own real Domain Event framework — CloudEvents envelope, tenant-carrying context, DLQ routing on handler failure. **Corrected from this document's own earlier draft:** this was previously described as "currently non-importable platform-wide." Directly re-verified for this correction: `TD-105` (`TECH-DEBT.md`) is **Closed**, resolved by Release A1 Foundation Repairs (2026-08-01) — `Backend/aurex/backend/shared/events/__init__.py` redirects `__path__` to this same `Backend/Shared/Events` directory, making `aurex.backend.shared.events.*` resolve correctly. Empirically re-confirmed by direct import (`EventPublisher`, `CloudEvent`, `EventRegistry`, `EventSubscriber` all resolve). **BA-05 should use this real framework directly — no local substitute and no new event architecture are required.** |
| `AzureServiceBusStub` (`EventPublisher`) | `Backend/Services/IngestionService/services/event_publisher.py` | The existing precedent for *how* a Domain Event gets published — currently a dry-run stub (`published_history`, no live broker call), not live infrastructure. |
| `organization_id` as "logical, not physical, FK" pattern | `Backend/Services/AIService/models/search.py` (module docstring + `vector_index_registry`/other model columns) | The exact precedent this design reuses for `enterprise_knowledge_graph_registry.organization_id` once hosted outside `AuthService`'s own database (§20). |
| `two_orgs` fixture pattern | `Backend/Services/AuthService/tests/test_delegation_policy_authorization_retrofit_api.py` (and siblings) | The Mandatory Tenant-Isolation Test Checklist pattern — two unrelated Organizations, no shared row — reused for BR-1/BR-4 test design (§21). |
| `AuditStatus`/`CorrelationContext` observability pattern | `Backend/Services/AuthService/observability.py` | **Correction:** previously listed as BA-05's own reuse target for rejection/audit logging, "until the shared framework is fixed." `TD-105` is now Closed (see the `Backend/Shared/Events` row above) — the real `Backend/Shared/Events`/`Backend/Shared/Logging` framework is importable and available directly. This local, explicitly-temporary substitute (still unmigrated by `AuthService` itself, per `TD-108`, Open) is **no longer BA-05's own reuse target** — BA-05 is a new component with nothing to migrate, so it should use the real framework from the outset (§23). |
| `confidence_scoring_registry` | `Master_Technical_Architecture.md` AMD-003 | Already FK'd from `enterprise_knowledge_graph_registry.confidence_rule_id` — reused, not reinvented, for Evidence/Confidence population (`IRA-014 §6` BA-05 Evidence/provenance row). |

## 6. Current-State Analysis

Verified directly, not assumed: **zero code exists** for any part of this pipeline. `grep` across `Backend/` for `knowledge_graph`, `KnowledgeGraph`, and `enterprise_knowledge_graph_registry` returns no matches. No Entity Resolution, Relationship Resolution, or Knowledge Graph Engine component exists in any service. This matches `IRA-014 §1`'s own finding ("Zero code — this Work Package is the first to implement any of it") exactly — confirmed independently in this pass, not accepted on trust. Every component named "new" in §11 below is therefore genuinely new, not an oversight of something already built.

## 7. Target Architecture

**Corrected by this reconciliation pass (was aspirational at original drafting, now real):** the publish step below previously named only a generic "Domain Event," since no producing increment existed at drafting time (§26a's own original finding). It is now the concrete, delivered, CLOSED — CERTIFIED `KnowledgeAssetAcceptedEvent` (`aurex.aiservice.knowledge_asset.accepted` v`1.0.0`, `TDS-014 §8`, `Backend/Services/AIService/events/knowledge_asset_events.py`), produced by the BA-04 Increment (F-01) `RO-DEC-WP14-BA05-01` names, committed `4c86813`. **Delivery is best-effort with no automatic retry** (`RO-DEC-BA04-INC-007`, `TDS-014 §9`/§19/§21) — a publish failure is logged only; it does not roll back the already-committed `ACCEPTED` state and does not requeue itself. If the event is never delivered, BA-05 simply does not execute for that transition — an explicitly accepted limitation of the BA-04 Increment, not a BA-05 design defect (see §24 item 8, new).

```
BA-04 (Knowledge Asset -> ACCEPTED)
        │  transaction commit
        ▼
  KnowledgeAssetAcceptedEvent published, best-effort, no retry
  (aurex.aiservice.knowledge_asset.accepted v1.0.0 — TDS-014 §8;
   RTA-001 §12.3/§12.6; Backend/Shared/Events; RO-DEC-BA04-INC-007)
        │
        ▼
  KnowledgeGraphSyncHandler                              (NEW — event subscriber registration)
        │  Knowledge Event Processing (§12.7)
        ▼
  RelationshipResolutionService                          (NEW — orchestrator)
        │
        ├─► EntityOwnershipResolver.resolve(entity_type, entity_id)   (NEW, §11)
        │        for source AND target independently
        │
        ├─► BR-1/BR-2/BR-3/BR-4 derivation                (§10, in-memory, no write yet)
        │        reject ──────────────────────────────────► DLQ + audit log, no persistence
        │
        ├─► Ontology Validation (relationship_type ∈ RTA-001 §12.9 named set)
        │        reject ──────────────────────────────────► DLQ + audit log, no persistence
        │
        ▼
  EnterpriseKnowledgeGraphRepository.insert(...)          (NEW — thin repository)
        │  single transaction, db_manager pattern (§15)
        ▼
  enterprise_knowledge_graph_registry row persisted        (organization_id correctly derived)
        │
        ▼
  Knowledge Observability telemetry (§12.15) — best-effort, non-transactional
```

Optional, separate, caller-facing path (not mandatory for BA-05's own minimum scope, `IRA-014 §6` BA-05 Frontend/UX row):

```
Caller ──► GET /knowledge-graph/relationships
              │  require_matching_tenant_or_platform_admin  (existing, §14)
              ▼
        Repository read, scoped by RLS (§13) + caller's own organization_id
```

## 8. End-to-End BA-05 Execution Flow

1. BA-04's own `KnowledgeAssetService` (Increment F-01, `TDS-014`, CLOSED — CERTIFIED, commit `4c86813`) transitions a Knowledge Asset to `ACCEPTED` and commits — **this is now the repository's actual, delivered behavior, not a target state** (corrected by this reconciliation pass; see §7).
2. After commit (never before — `RTA-001 §12.6`; independently re-verified in `knowledge_asset_service.py` — the publish attempt strictly follows `claim_transition()`'s own internal commit), a best-effort attempt is made to publish `KnowledgeAssetAcceptedEvent` naming the accepted Knowledge Asset. Delivery is not guaranteed (`RO-DEC-BA04-INC-007`, §24 item 8) — this step may not occur for a given transition even though step 1 always succeeds.
3. `KnowledgeGraphSyncHandler` (a registered `EventSubscriber` handler, §11), if the event is delivered, decodes the envelope and maps it to the one relationship tuple `RO-DEC-WP14-BA05-02` decides for this trigger — **RESOLVED, no longer an open item (was §24 Open Question 3):** `(source_entity_type=KNOWLEDGE_ASSET, source_entity_id=<accepted Knowledge Asset id>, relationship_type=Governed By, target_entity_type=ORGANIZATION, target_entity_id=<the Knowledge Asset's own persisted organization_id>)`. No CDE relationship and no source-ingestion-owner relationship is produced by this trigger (`RO-DEC-WP14-BA05-02`'s own explicit exclusions) — either remains future, separately authorized scope.
4. For each candidate tuple, `RelationshipResolutionService` performs Entity Resolution (§9) for both endpoints, then Relationship Resolution (§10) to derive/validate `organization_id`.
5. On success: Ontology Validation (relationship_type membership check), then a single-transaction insert via `EnterpriseKnowledgeGraphRepository` (§15).
6. On any rejection (§16): no row is persisted; the originating event is routed to the existing DLQ mechanism (`EventSubscriber.route_to_dead_letter_queue`) and a structured rejection record is logged (§23) — the triggering BA-04 transaction is never affected (`RTA-001 §12.3`: "shall never delay Business Activity completion" — already committed by step 1).
7. `graph_engine_reference` remains `NULL` — the live Neo4j write is out of scope (§1).

## 9. Tenant Boundary Resolution

**Where determined:** inside Entity Resolution (`RTA-001 §12.8`), immediately before Relationship Resolution (`§12.9`) — never at query time, never inferred after persistence, satisfying `SD-002-108` and the `§12.9` clarification directly.

**How source and target are resolved:** via a new `EntityOwnershipResolver` (§11) — a per-`entity_type` strategy that, given `(entity_type, entity_id)`, returns either a resolved `organization_id` (possibly `NULL`, meaning confirmed-Global), or a resolution failure (entity not found / ambiguous). **Minimum scope for this design:** the resolver's own initial strategy set covers only entity types this Work Package itself produces — `discovery_provider_registry`, `unclassified_intelligence_registry`, `customer_metric_registry`/`metric_registry`, `knowledge_asset_registry` (BA-01–BA-04's own tables). `RTA-001 §12.8`'s own full entity list (Organizations, Enterprise Nodes, People, Metrics, Risks, Opportunities, Evidence, Reports, Frameworks, Regulations) is broader than these five tables — most of the remainder are `AuthService`-owned Business Objects outside WP-14's own charter. **This narrowing is disclosed, not silent** — it mirrors `IRA-014 §5.2`'s own precedent (BA-02's `extraction_method` narrowing) exactly: the smallest scope that satisfies BA-05's own chartered trigger (BA-04's Knowledge Asset acceptance) without inventing a general, all-entity-type resolver no governing document specifies. Extending `EntityOwnershipResolver` to the full `§12.8` entity list is future scope, named not silently assumed (§24).

**How each object's Organization boundary is established:** each resolver strategy queries its own entity type's owning table's `organization_id` column directly (same-database read, if BA-05 and its source tables share a hosting service, §20) — never via the polymorphic reference alone, and never cached across requests (a fresh read per resolution, since `SD-002-108` treats a stale/inferred boundary as an invalid state).

**Narrowed by this reconciliation pass, not contradicted:** `RO-DEC-WP14-BA05-02`'s own decided minimum scope (§8 step 3) produces exactly one relationship kind — Knowledge Asset → Organization — for BA-05's currently-authorized trigger. Of the five per-entity-type strategies named above, only two are load-bearing for that one decided relationship: `knowledge_asset_registry` (source) and Organization itself (target — resolved trivially, since `RO-DEC-WP14-BA05-02` defines the target's own `organization_id` as identical to the Knowledge Asset's own persisted `organization_id`, never independently looked up). The other three strategies (`discovery_provider_registry`, `unclassified_intelligence_registry`, `customer_metric_registry`/`metric_registry`) remain named here as this design's own disclosed broader-scope precedent for future trigger wiring (§24 item 7, unchanged) — they are not required to implement the one relationship BA-05's own current minimum scope decides.

## 10. BR-1 Enforcement

After both endpoints resolve (§9): if both resolved `organization_id` values are non-`NULL`, compare them. Equal → proceed, `organization_id` = that shared value. Unequal → **reject before persistence** (§16) — this comparison is also BR-4's own enforcement point (§4). Enforced at the **application/service layer** (`RelationshipResolutionService`, inside the Relationship Resolution pipeline stage) — not achievable by RLS alone, since RLS cannot evaluate a *derived* correctness condition across two polymorphic references (§22).

**Consistency note, this reconciliation pass:** `RO-DEC-WP14-BA05-02`'s own decided Knowledge Asset → Organization relationship (§8 step 3) satisfies BR-1 by construction, not merely by runtime luck — the target's own `organization_id` is defined as identical to the source Knowledge Asset's own persisted `organization_id` (§9), so the comparison in this section always finds equality for that specific relationship. This does not weaken or bypass the general BR-1 mechanism above, which remains the enforcement point for any future relationship kind this design's own broader entity-resolver scope (§9) may eventually produce.

## 11. BR-2 Enforcement

If exactly one endpoint resolves a non-`NULL` `organization_id` and the other resolves `NULL` (confirmed-Global, not unresolved — §12), the relationship inherits the non-`NULL` value. Enforced at the same application/service layer, same pipeline stage, immediately adjacent to BR-1's comparison (they are evaluated by the same function, not two separate mechanisms).

## 12. BR-3 Enforcement

If both endpoints resolve `NULL` (both confirmed-Global), `organization_id` remains `NULL` on the persisted row. **Distinction enforced explicitly, per `SD-002-108`:** a `NULL` resolution here means the resolver strategy positively confirmed the entity is Global (e.g., a `discovery_provider_registry` row with its own `organization_id IS NULL`) — it is never the default outcome when a resolver *cannot determine* an entity's boundary. An unresolvable/ambiguous entity is treated as an Entity Resolution failure (§16), not silently defaulted into a BR-3 `NULL` — this distinction is the one place `ADR-023`'s own nullable design could be mis-implemented as "null means unknown" rather than its actual meaning, "null means confirmed-Global," and this design states the difference explicitly to foreclose that error.

## 13. BR-4 Enforcement

As established in §4/§10: BR-4 is BR-1's own mismatch case, named from the cross-organization angle. No separate mechanism. The one thing BR-4 adds beyond BR-1's bare comparison: the rejection path's own audit/log message (§16, §23) SHALL name the rejection as "cross-organization relationship rejected — no sharing mechanism exists (`SD-002-111`)" specifically when both resolved values are non-`NULL` and unequal, distinct from a generic "entity not found" rejection message — so that a future cross-tenant sharing mechanism (if ever built) has a precise, already-distinguished rejection class to relax, rather than an undifferentiated rejection log.

## 14. Authorization Responsibility

**Determined from existing governing architecture — no new mechanism invented, per the task's own explicit prohibition.**

BA-05 has two structurally distinct access shapes (`IRA-014 §6` BA-05, APIs/services required row), and authorization applies differently to each:

**Write path (event-triggered synchronization, §7–§8):** has no caller-facing endpoint and no external caller — it is invoked exclusively by the internal event-subscription pipeline, itself only reachable from an already-committed, already-authorized originating Business Activity (e.g., BA-04's own `PLATFORM_ADMIN` gate, already enforced before the Knowledge Asset reached `ACCEPTED`). **BA-05 performs no additional caller-authorization check on this path, because there is no caller to authorize** — `ADR-023 §1`'s own distinction applies precisely here: BR-1–BR-4 are a **data/tenant-boundary integrity concern**, not an authorization concern. Conflating the two — e.g., gating the internal handler with `PLATFORM_ADMIN` — would be a category error `ADR-023` itself already forecloses ("`PLATFORM_ADMIN` gates who may call an endpoint, not whether the underlying rows are safely scoped to one tenant").

**Read path (optional `GET /knowledge-graph/relationships`, if built):** a genuine caller-facing endpoint. Reuses `require_matching_tenant_or_platform_admin` (`Backend/Services/AuthService/dependencies.py`, §5) **exactly as `WP-10` established** — the caller's own JWT `organization_id` claim must match the requested tenant scope unless they hold `PLATFORM_ADMIN`. This is precisely the mechanism `ADR-023 §5` item 5 names ("Authorization SHALL subsequently reuse the existing tenant-boundary enforcement pattern already certified at WP-10... not WP-13's Authorization Runtime Engine"). A caller without `PLATFORM_ADMIN` sees rows where `organization_id` is `NULL` (Global) or equals their own tenant — mirroring the RLS policy's own semantics (§22), not a separate rule.

**WP-13's Authorization Runtime Engine (`enforce_domain_permission`) is not used anywhere in BA-05** — confirmed inapplicable by `ADR-023 §4` Option D (category error: Domain-delegation, not Organization-ownership) and by the continuing absence of any `domain_id` column on `enterprise_knowledge_graph_registry` (`IRA-014 §10`, unchanged by `AMD-016`).

## 15. Transaction and Persistence Model

Reuses the existing `DatabaseSessionManager` pattern (§5) in semantics, adapted to an event-handler call site rather than a FastAPI route dependency (no HTTP request exists on this path). **Corrected from this document's own earlier draft:** the earlier sketch referenced `db_manager.session_scope()` — a method that does not exist anywhere in this repository. The actual, directly-verified primitive (`Backend/Services/AuthService/models/database.py:64`) is:

```
async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
    ...
    async with self._sessionmaker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

This is a plain async-generator function shaped for FastAPI's `Depends()` injection — FastAPI's own dependency-injection machinery drives it via the generator protocol, which is why every existing call site in this repository uses it only as `Depends(db_manager.get_session)`. It is **not**, as written, directly usable as `async with db_manager.get_session() as session: ...` at a non-HTTP, non-Depends call site such as `KnowledgeGraphSyncHandler`'s own event handler — calling `get_session()` produces an async generator object, not an async context manager, and a bare `async with` over it fails.

**The commit/rollback/close semantics this design requires are unchanged by this correction** — resolve, validate, and only then persist within one transaction; commit on success; rollback on any exception; always release the session. Reusing `get_session()` at BA-05's own event-handler call site requires one of two small adaptations, **neither implemented by this Technical Design** — left open as an implementation-time detail (§25), not decided here:

- iterate it directly — `async for session in db_manager.get_session(): ...` (a single-iteration loop, since `get_session()` yields exactly once); or
- wrap it as a proper async context manager — `async with contextlib.asynccontextmanager(db_manager.get_session)() as session: ...`.

Either adaptation preserves `get_session()`'s own existing commit/rollback/close semantics verbatim; the choice between them is a small implementation-time detail, not a design decision:

```
# via one of the two adaptations above:
    # 1. Entity Resolution reads (source, target) — read-only, no write yet
    # 2. BR-1/2/3/4 derivation — in-memory, no write yet
    # 3. Ontology Validation — in-memory, no write yet
    # 4. If and only if all three pass: session.add(new_relationship_row)
    #    await session.flush()
    # (commit on successful exit, rollback on exception, session closed on
    #  exit — db_manager.get_session()'s own existing semantics, unchanged)
```

One relationship-resolution attempt = one transaction. A rejection at any point (§16) means **no write is attempted** — there is nothing to roll back; the transaction is a no-op that is simply not committed. Observability telemetry emission (§23) is **outside** this transaction — a best-effort side effect that never causes the relationship write itself to roll back if telemetry emission fails, and never blocks on it (`RTA-001 §12.3`).

## 16. Failure and Rejection Semantics

| Condition | Outcome |
|---|---|
| Source object unknown (Entity Resolution finds no owning row) | Reject before persistence. DLQ + rejection log ("entity not found"). No relationship row created. |
| Target object unknown | Same as above, for the target endpoint. |
| Source and target belong to different Organizations | BR-1/BR-4 reject (§10/§13). DLQ + rejection log, explicitly labeled "cross-organization." Never silently reconciled (`ADR-023 §5.3`). |
| One endpoint has no determinable Organization boundary (ambiguous, not confirmed-Global) | Treated as an Entity Resolution failure (§12), not a BR-3 `NULL` default. Reject. |
| Relationship already present (identical natural key) | Idempotent no-op (§17) — not an error, not a duplicate row. |
| Relationship is invalid (`relationship_type` not in `RTA-001 §12.9`'s named set) | Ontology Validation rejects. DLQ + rejection log. No relationship row created. |
| Caller lacks required authority | Applies only to the optional read path (§14) — `403`, standard FastAPI dependency rejection, no change to write-path semantics. |
| Cross-tenant reference attempted | Identical to "different Organizations" above — one enforcement point (§13). |

No rejection reaches back to the originating Business Activity synchronously — it already committed (§8, step 1) — consistent with `RTA-001 §12.3`'s guarantee.

## 17. Idempotency / Retry / Replay

**Natural key:** `(source_entity_type, source_entity_id, relationship_type, target_entity_type, target_entity_id)`. `organization_id` is deliberately excluded from the natural key — BR-1/BR-2/BR-3 are deterministic derivations, so two resolution attempts against the same natural key always derive the same `organization_id`; including it would be redundant, not additionally safe.

**Recommended mechanism:** check-before-insert within the same transaction (§15) — if a row with the identical natural key already exists, treat the attempt as a no-op and do not insert a second row. This works with **zero schema change** to `AMD-012`/`AMD-016`'s own existing columns, which is why it is recommended over a database-level `UNIQUE` constraint for this design's own minimum scope.

**Disclosed, not decided here:** a `UNIQUE` constraint on the natural key would be a stronger, database-enforced guarantee against concurrent duplicate inserts (the check-before-insert approach has a narrow race window under concurrent event delivery) — but adding one is itself a schema change requiring its own small amendment beyond `AMD-016`'s own scope. Left as an implementation-time choice (§24, Open Question 4), not decided or created by this Technical Design.

**Replay via CloudEvents redrive (DLQ):** `Backend/Shared/Events` is importable and available now (`TD-105` Closed, §5/§24 item 1) — a redriven event re-enters the same pipeline from step 3 (§8) and is naturally idempotent via the same natural-key check — no separate replay-specific logic is required.

## 18. Runtime Integration

Exact placement inside the existing, unmodified `RTA-001 §12.7` pipeline:

```
Business Activity Completed → Domain Event Published → Knowledge Event Processing
   → Entity Resolution [ + organization_id resolution, §9 ]
   → Relationship Resolution [ + BR-1–BR-4 derivation/validation, §10–§13 — REJECTION POINT ]
   → Semantic Enrichment → Ontology Validation [ — SECOND REJECTION POINT, §16 ]
   → Graph Update [ = the persistence step, §15 ]
   → Knowledge Index Refresh
```

No stage is added, removed, or reordered. The tenant-boundary logic occupies the Entity Resolution and Relationship Resolution stages exactly as `RTA-001 §12.9`'s own amended sentence already names ("Relationship Resolution shall validate the tenant boundary of both endpoints before persistence"). This design's own contribution is the concrete mechanism inside those two already-named stages, not a new stage.

## 19. API / Service Contract Implications

**Write path:** no public API contract — an internal event-handler signature only (`KnowledgeGraphSyncHandler.handle(event: BaseEvent) -> None`, following `EventSubscriber`'s own existing `AsyncEventHandler` type, §5).

**Read path (optional, if built):** `GET /knowledge-graph/relationships`, illustrative only per `IRA-014 §6` BA-05's own explicit non-mandatory framing — exact request/response schema is a further implementation-time decision, not fixed here (consistent with `IRA-014 §16`'s own self-review finding that endpoint shapes are illustrative, not architecture).

## 20. Database Implications

**No migration, model, or schema change is created by this Technical Design** (explicit prohibition, honored). The following are **recommendations for the eventual BA-05 migration**, not created now:

- **Hosting service recommendation:** `AIService`, not `AuthService` — **a recommendation only, not a resolved decision; Repository Owner concurrence remains required (§25 item 2) and the decision remains OPEN.** *(This was this document's position at original drafting — superseded by this reconciliation pass; see below.)* **Reconciled by this pass:** `RO-DEC-WP14-BA05-03` (`§26a`) has since approved `AIService` as the confirmed hosting service — Repository Owner concurrence has been given, and the decision is no longer open. This does not alter the recommendation itself or the evidentiary correction immediately below it, only its governance status. Two distinct kinds of evidence must not be conflated here — **corrected from this document's own earlier draft, which conflated them:**
  - **Architectural/schema precedent (shared amendment):** `enterprise_knowledge_graph_registry` shares its own governing amendment (`AMD-012`) with `knowledge_asset_registry`, `document_chunk_registry`, `vector_index_registry`, and `ai_tool_registry` — all four are AMD-012 siblings at the architecture-document level. This is accurate and unchanged.
  - **Actual physical Backend model implementation (directly re-verified for this correction):** of those four siblings, only `vector_index_registry` and `document_chunk_registry` are actually modeled today, in `Backend/Services/AIService/models/search.py`. `knowledge_asset_registry` and `ai_tool_registry` have **no Backend model anywhere in this repository** — consistent with, not contradicting, §6's own "zero code exists" finding. The earlier claim that "all four" are "already modeled in `Backend/Services/AIService/models/`" overstated the physical evidence and is corrected here. No model is invented by this correction — the gap is disclosed, not filled. *(This was this correction's own position as originally drafted — itself inaccurate, corrected by this remediation pass, `F-03` of the independent WP-14/BA-05 Technical Design Authorization Review.)* **Corrected by this remediation pass, directly re-verified by reading the actual source file:** `knowledge_asset_registry` **is** modeled — `Backend/Services/AIService/models/knowledge_asset.py:37` defines `class KnowledgeAssetRegistryModel(Base)` with `__tablename__ = "knowledge_asset_registry"`. Only `ai_tool_registry` has **no Backend model anywhere in this repository** (independently re-confirmed by direct search — zero hits for `ai_tool_registry` as a `__tablename__` anywhere in `Backend/`).
  - **Consequently, the recommendation rests on a 2-of-4 physical sibling-table precedent, not a 4-of-4 one.** This weakens, but does not eliminate, the recommendation's own evidentiary basis — `IRA-014 §11` item 2 independently frames `AIService` as "the more direct precedent" for the Work Package's five new tables generally, on grounds broader than AMD-012 sibling co-location alone. The recommendation itself is unchanged by this correction; the justification stated for it is now accurate. *(The "2-of-4" figure above was itself inaccurate, per the correction immediately above — superseded by this remediation pass.)* **Corrected:** the recommendation actually rests on a **3-of-4** physical sibling-table precedent (`vector_index_registry`, `document_chunk_registry`, `knowledge_asset_registry` — only `ai_tool_registry` unmodeled), a stronger evidentiary basis than previously stated, not a weaker one. This does not change the recommendation itself, which was already correct; it corrects the strength of the evidence stated for it, in the same direction as, not contradicting, this section's own `IRA-014 §11` item 2 citation.
  - **Canonical logical grouping, separately (`Master_Technical_Architecture.md`, PART F ADDENDUM: KNOWLEDGE & INTELLIGENCE SERVICES, AMD-012):** that addendum names a distinct logical component owner, **"Knowledge Graph Service,"** for exactly `enterprise_knowledge_graph_registry` and `knowledge_asset_registry` — separate from "Retrieval Service" (`document_chunk_registry`/`vector_index_registry`) and "Agent Orchestration Service" (`ai_tool_registry`). That addendum states this is "Component design only"; it is not, and is not converted here into, a physical microservice. **No physical service named `Knowledge Graph Service` exists among the repository's five actual services** (`AIService`, `AuthService`, `IngestionService`, `ReportingService`, `TenantService`) — this Technical Design does not create one. Hosting `enterprise_knowledge_graph_registry` inside the physical `AIService` codebase does not itself contradict the logical "Knowledge Graph Service" component boundary, since no physical service currently realizes that boundary at all. This reconciliation is disclosed here for Repository Owner awareness; it does not, by itself, resolve which physical service should host `enterprise_knowledge_graph_registry`, and this document does not treat it as resolved.
  - **Net effect of this correction:** the hosting-service determination remains explicitly OPEN, exactly as before — this correction changes the accuracy and completeness of the evidence presented for the recommendation, not the recommendation, and not the requirement for Repository Owner concurrence. *(True at the time this correction was originally drafted; superseded by this reconciliation pass — `RO-DEC-WP14-BA05-03` (`§26a`) has since approved `AIService` as the confirmed hosting service, and that Repository Owner concurrence has now been given.)* It does not resolve hosting for BA-01–BA-04's own tables either (different amendments, `AMD-013`/`AMD-004`/`AMD-005` — a separate, still-open determination, unaffected by `RO-DEC-WP14-BA05-03`, which concerns only `enterprise_knowledge_graph_registry`).
- **Consequence of that recommendation:** `organization_id UUID REFERENCES organization_master(organization_id)` becomes a **logical, not physical, FK** once `enterprise_knowledge_graph_registry` lives in `AIService`'s own database — `organization_master` lives in `AuthService`'s own database, a separate service boundary (`CLAUDE.md §8`: never access another service's database). This is not a deviation from `AMD-016` — it is the exact, already-established precedent `AIService/models/search.py`'s own module docstring states for every other AMD-012 table's `organization_id` column. The RLS policy itself is unaffected (§22) — RLS evaluates a session-local setting against a locally-stored column value; it requires no cross-database join.
- **Idempotency uniqueness constraint (§17):** a candidate, not decided — deferred to implementation time as its own small amendment if a database-enforced natural-key `UNIQUE` constraint is chosen over check-before-insert.
- **No Alembic migration is created by this document** — unchanged from `ADR-023`/`AMD-016`'s own explicit position; the column already exists at the architecture-document level only.

## 21. Testing and Verification Strategy

Per `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist, applied to BA-05 specifically (reusing the `two_orgs` fixture pattern, §5):

- **BR-1/BR-4:** seed two Organizations (Org A, Org B), a source entity owned by Org A and a target entity owned by Org B — assert the relationship is rejected, no row persisted, DLQ/rejection log recorded.
- **BR-2:** seed one Org-scoped entity and one confirmed-Global entity — assert the relationship inherits the Org-scoped `organization_id`.
- **BR-3:** seed two confirmed-Global entities — assert `organization_id IS NULL` on the persisted row.
- **Ambiguous-boundary distinction (§12):** seed an entity whose owning row cannot be resolved — assert this is treated as an Entity Resolution failure, not a silent `NULL`/BR-3 outcome (the specific mis-implementation risk §12 names).
- **Idempotency (§17):** deliver the identical natural-key tuple twice — assert exactly one row persists.
- **Cross-tenant read-path probe (optional endpoint, if built):** a caller in Org A must never retrieve an Org B-scoped relationship row, per the same `require_matching_tenant_or_platform_admin` pattern `WP-10`'s own test suite already exercises.
- **Bypass probes (§13 design question):** confirm no second code path can insert a row into `enterprise_knowledge_graph_registry` without passing through `RelationshipResolutionService` — a structural/import-graph check (mirroring `VV-AUDIT-WP-12`'s own AST-based structural check precedent, §5's own observability citation), not merely a runtime test.

All of the above are **test design**, not test code — no test file is created by this document (explicit prohibition, honored).

## 22. Security / Tenant-Isolation Analysis

Two independent layers, deliberately not collapsed into one — directly grounded in `SD-002-109`'s own text, quoted precisely in `ADR-023 §2`: *"isolation is a storage and retrieval guarantee, not solely an access-control feature."*

1. **Application/service layer (§10–§13):** the only layer capable of evaluating BR-1/BR-2/BR-3's own *derivation correctness* — comparing two resolved endpoint boundaries requires application logic; RLS cannot traverse the polymorphic `source_entity_id`/`target_entity_id` references to determine what the "correct" `organization_id` should be.
2. **Database/RLS layer (`AMD-016`'s own policy, §5, §20):** `organization_id IS NULL OR organization_id = current_setting('app.organization_id')::uuid` — a **query-time visibility floor**, independent of and in addition to layer 1. Even if layer 1 were bypassed by a future code defect, RLS still prevents a session connected as one tenant from reading or (with an appropriately extended `WITH CHECK` clause, an implementation-time recommendation, not created here) writing another tenant's row. This is the concrete architectural answer to design question 13 ("can any alternate path bypass the controls") for the *database* boundary specifically — a second, independent backstop, not a restatement of layer 1.

**Bypass analysis (design question 13), by path:**
- **Another API path:** none exists — the write path has no public endpoint (§19).
- **Direct service invocation:** `EnterpriseKnowledgeGraphRepository`'s own insert method is the single choke point; any future direct caller still passes through it, and RLS (layer 2) still applies regardless of caller.
- **Background processing / bulk synchronization / future ingestion mechanisms:** any future mechanism MUST route through `RelationshipResolutionService`, never a raw bulk insert — stated here as a binding constraint on future work, not merely a recommendation, since a bulk path bypassing BR-1–BR-4 derivation would defeat `ADR-023` entirely.
- **Retry/replay:** naturally idempotent (§17); replay does not re-open a bypass, since it re-enters the same pipeline from the same entry point.

## 23. Observability / Audit Implications

Reuses `RTA-001 §12.15`'s own named telemetry (Graph Update Duration, Entity Resolution Count, Relationship Creation Count, Synchronization Latency) as the metric vocabulary. **Corrected from this document's own earlier draft:** previously stated that, pending an import-path fix, BA-05 would need `AuthService/observability.py`'s local substitute. `TD-105` is Closed (§5/§24 item 1) — `Backend/Shared/Events`/`Backend/Shared/Logging` are importable and available now. BA-05's own emission SHALL use the real framework directly (`EventFactory`/`EventContext`/`CloudEvent` for event-side telemetry, `Backend/Shared/Logging`'s own `CorrelationContext`/audit vocabulary for structured logging) — no local substitute is needed, since BA-05 is a new component with nothing to migrate away from. Every rejection (§16) is logged with its own specific reason class (entity-not-found, cross-organization, ontology-invalid) so that future analysis can distinguish a tenant-boundary defect from a data-quality gap.

## 24. Technical Debt / Open Questions

Disclosed here, not silently resolved or silently ignored, per `CLAUDE.md §19.8`:

1. **RESOLVED — `Backend/Shared/Events` is importable and available.** Previously stated here as "currently non-importable platform-wide," citing `AuthService/observability.py`'s own module docstring. **Corrected, directly re-verified against the repository:** `TD-105` (`TECH-DEBT.md`) is **Closed**, resolved by Release A1 Foundation Repairs (2026-08-01, commit `81d34b0`) — `Backend/aurex/backend/shared/{config,database,events,logging,security}/__init__.py` are five alias packages redirecting `__path__` to the corresponding real `Backend/Shared/<Component>` directory, without moving, renaming, or duplicating any file. Empirically re-confirmed for this correction by direct import: `EventPublisher`, `CloudEvent`, `EventRegistry`, `EventSubscriber` all resolve correctly; `Backend/Shared/tests/test_aurex_namespace_import.py::test_events_namespace_imports_fully` passes. **BA-05's event-triggered mechanism (§7–§8) has no remaining infrastructure precondition on this point** — it should use the real `EventFactory`/`EventSubscriber`/`CloudEvent`/`EventContext` framework directly (§5), not `AuthService/observability.py`'s local substitute. No new event architecture is required.
2. **The live message-bus transport itself remains a stub** (`AzureServiceBusStub`, `IngestionService/services/event_publisher.py` — dry-run, in-memory `published_history`, no live Azure Service Bus call) — distinct from item 1 above: `Backend/Shared/Events`'s own import path is now resolved (`TD-105` Closed), but a live broker is a separate, further, still-open precondition, unaffected by that fix (mirrors `IRA-014 §5a`'s own `SE-025` disclosure for the live Neo4j write — the same class of infrastructure-maturity gap, not new).
3. **Per-trigger-event-type mapping** (§8, step 3 — which specific `(source_entity_type, relationship_type, target_entity_type)` tuple(s) a given Domain Event, e.g. "Knowledge Asset ACCEPTED," actually implies) is not specified anywhere in governing architecture. `RTA-001 §12.6` lists the *kinds* of updates the Engine may perform but not a concrete mapping table. Left open for implementation-time design — not decided here, since deciding it would require inventing business semantics no governing document states. *(This was this item's position at original drafting — superseded by this reconciliation pass for the one trigger named below; see `§26a`.)* **RESOLVED for BA-05's own one currently-authorized trigger, by `RO-DEC-WP14-BA05-02` (`§26a`):** Knowledge Asset `ACCEPTED` maps to exactly `(source_entity_type=KNOWLEDGE_ASSET, relationship_type=Governed By, target_entity_type=ORGANIZATION)`, per §8 step 3 above. No other trigger event has been mapped — any future trigger beyond this one remains open and still requires its own separate Repository Owner decision; this item's resolution is scoped to the one trigger BA-05's own current minimum scope handles, not a general per-trigger-mapping framework.
4. **Idempotency uniqueness constraint** (§17) — check-before-insert (this design's recommendation) vs. a database `UNIQUE` constraint (stronger, requires its own amendment) — implementation-time choice, not decided here.
5. **`RTA-001 §12.9`'s 12 named relationship kinds are never mapped to `ONT-001`'s own six general relationship categories** (Classification/Specialization/Composition/Aggregation/Association/Reference), despite `ONT-001-020` expecting exactly this classification from the "owning document." **Discovered during this design's own evidence-gathering pass; explicitly out of this design's own mandate** — it concerns Ontology Validation's own semantic completeness (a different pipeline stage, §18), not BR-1–BR-4 tenant-boundary enforcement, and resolving it would mean assigning ontology classifications this document has no authority to assign. **Non-blocking for BA-05's own minimum scope:** `relationship_type` membership in `RTA-001 §12.9`'s own closed 12-value list is independently sufficient for Ontology Validation to function (§16) without the `ONT-001` cross-classification existing yet. Flagged for `RTA-001`'s or `ONT-001`'s own governing authority, not resolved here.
6. **No `updated_at`/version column exists** on `enterprise_knowledge_graph_registry` (`AMD-012`/`AMD-016`) despite `RTA-001 §12.9`'s own text ("Relationships shall remain versioned and auditable") — `active_flag`/`created_at` alone do not fully satisfy "versioned." Not decided or created here; a candidate future amendment, disclosed rather than silently worked around by, e.g., quietly reinterpreting `active_flag` as a version mechanism it was not documented to be.
7. **`EntityOwnershipResolver`'s own minimum scope excludes most of `RTA-001 §12.8`'s named entity list** (§9) — disclosed, narrower-than-full-charter scope, consistent with `IRA-014`'s own established narrowing precedent, not a silent gap.

None of items 1–7 are `CLAUDE.md §19.8.5`-class (architectural, security, data-integrity, or tenant-isolation defects) — BR-1–BR-4 themselves are fully specified and enforceable by this design (§10–§13); items 1–7 concern surrounding infrastructure maturity and semantic completeness, not the tenant-boundary decision itself.

## 25. Implementation Preconditions

Before BA-05 implementation may begin, in addition to standard Business Activity Completion Gate requirements (`CLAUDE.md §19.7`):

1. **RESOLVED, no longer a precondition:** previously stated as requiring `Backend/Shared/Events`'s own import-path defect to be fixed, or adoption of `AuthService/observability.py`'s local-substitute pattern, before implementation could begin. `TD-105` is Closed (§24, item 1) — the import path already resolves, directly re-verified. BA-05's own event-handler registration should use the real `EventFactory`/`EventSubscriber`/`CloudEvent`/`EventContext` framework (§5) from the outset; no local-substitute pattern is needed and none should be built.
2. Hosting-service determination (§20) — `AIService`, per this design's own recommendation — requires Repository Owner concurrence at Implementation Authorization time; this document recommends, it does not decide. *(This was this item's position at original drafting — superseded by this reconciliation pass; see `§26a`.)* **RESOLVED:** `RO-DEC-WP14-BA05-03` (`§26a`) has since given that concurrence and approved `AIService` as the confirmed hosting service. This precondition no longer blocks implementation on that ground.
3. `EntityOwnershipResolver`'s own five initial per-entity-type strategies (§9) require each of BA-01–BA-04's own tables to actually exist (their own migrations) — a same-Work-Package, not external, dependency.
4. The per-trigger-event-type mapping (§24, item 3) must be resolved before `KnowledgeGraphSyncHandler` can be written meaningfully. *(This was this item's position at original drafting — superseded by this reconciliation pass for the one trigger named below; see `§26a`.)* **RESOLVED for that one trigger:** `RO-DEC-WP14-BA05-02` (`§26a`) has since resolved the Knowledge Asset `ACCEPTED` → `(KNOWLEDGE_ASSET, Governed By, ORGANIZATION)` mapping (§8 step 3; §24 item 3), so `KnowledgeGraphSyncHandler` can now be designed against it for that trigger. This precondition remains open for any future additional trigger event, which still requires its own separate Repository Owner decision before it can be handled.

## 26a. Repository Owner Decision Recording (2026-08-16)

**Recorded per direct Repository Owner instruction ("WP-14 — Repository Owner Decision Recording, BA-05 Knowledge Graph Synchronization").** This section records governance **decisions**, not a Technical Design revision — it does not add, remove, or alter any design element §1–§26 above already state; it records which of this document's own previously-OPEN items now have an explicit Repository Owner decision, and which remain open.

An independent WP-14 BA-05 Technical Design Authorization Review (preceding this recording) found this document's own §7–§8 trigger assumption — that BA-04 already transitions a Knowledge Asset to `ACCEPTED` and publishes a Domain Event — does not hold against BA-04's actual, delivered, certified implementation (which provides only `establish()`/`get_by_id()`). A subsequent Repository Owner Decision Package analyzed the available trigger models against `RTA-001 §12.14` and found exactly one architecturally consistent option. The Repository Owner has now decided:

- **`RO-DEC-WP14-BA05-01` (BA-05 trigger model) — APPROVED.** BA-05's trigger shall be a Domain Event BA-04 emits on reaching `ACCEPTED`, produced by a separately authorized **BA-04 Increment** completing this Business Activity's own already-disclosed, deferred transition/event scope (recorded in full in `WP-14_BA-04_Establish_Knowledge_Asset_Business_Activity_Charter.md`, its own new "BA-04 Increment" section). This decision does **not** itself authorize the Increment's implementation, and does **not** decide the Increment's own event name, version, or payload schema — those remain the Increment's own Technical Design items. §7's own diagram and §8's own execution-flow text above are therefore now understood as describing the *intended*, Repository-Owner-approved target state, not (and never claimed by this recording to be) a currently-true fact about the delivered system — a correction this recording makes explicitly rather than silently.
- **`RO-DEC-WP14-BA05-03` (hosting service) — APPROVED.** `AIService`, per §20's own recommendation above, is now the Repository-Owner-confirmed hosting service — no longer merely a recommendation. §20's own evidentiary text is unchanged and remains the record of *why*; this line records *that* it is now decided. Not to be reopened absent a later authoritative architectural conflict.
- **`RO-DEC-WP14-BA05-02` (per-trigger-event-type mapping, §24 item 3) — APPROVED, 2026-08-16.** The Repository Owner has decided the business semantics of the one Knowledge Asset `ACCEPTED` outcome BA-05's own minimum scope handles:

  **Decision:** upon a Knowledge Asset reaching `ACCEPTED`, BA-05 shall establish exactly one governed-ownership relationship between that Knowledge Asset and the Organization that owns it. Acceptance alone shall **not** create a Knowledge Asset→CDE relationship (no authoritative rule establishes that every accepted Knowledge Asset curates a specific CDE) or a Knowledge Asset→source-ingestion-owner relationship (ingestion provenance is distinct from governed enterprise ownership) — either may be established later by another, separately authorized Business Activity once its own business conditions are satisfied, but neither is implied by `ACCEPTED` alone. No live Neo4j relationship is created (`SE-025`, unchanged, out of scope).

  - **Source entity:** the accepted Knowledge Asset.
  - **Target entity:** the Organization identified by the Knowledge Asset's own authoritative, persisted `organization_id` — never a value taken from the triggering event payload as if it were independently authoritative; the Knowledge Asset's own stored tenant ownership is the sole source of truth for the target.
  - **Relationship kind:** `Governed By` — the exact, unmodified `RTA-001 §12.9` vocabulary value (`Owns`, `Reports To`, `Depends On`, `Supports`, `References`, `Controls`, `Measures`, `Influences`, `Linked To`, `Derived From`, `Verified By`, `Governed By` — confirmed as the complete, closed 12-value list by direct re-read of `RTA-001 §12.9`, verbatim, this pass). `RTA-001 §12.9` gives no further per-term definition beyond the name itself; `Governed By`, applied source→target as `Knowledge Asset — Governed By → Organization`, is selected because it reads correctly in the stated direction and matches the Repository Owner's own business-meaning text ("governed enterprise knowledge belonging to the Organization that owns it") almost verbatim. `Owns` was considered and rejected: it is the more obvious lexical candidate for "ownership," but its natural direction is owner→owned (`Organization Owns Knowledge Asset`), the reverse of the Repository Owner's own specified source (Knowledge Asset) → target (Organization) direction — applying it in the specified direction would read backwards ("Knowledge Asset Owns Organization"). `Derived From` was considered and rejected: it is the better semantic fit for ingestion/provenance lineage, which this decision explicitly excludes. The remaining nine values (`Reports To`, `Depends On`, `Supports`, `References`, `Controls`, `Measures`, `Influences`, `Linked To`, `Verified By`) do not plausibly express a governed-ownership relationship. No new relationship kind was created, renamed, or reinterpreted; `RTA-001` is unmodified.
  - **Cardinality:** N:1 — each accepted Knowledge Asset has exactly one owning Organization; one Organization may own many accepted Knowledge Assets. No cardinality assumption is made for any CDE or source-ingestion relationship, since neither is created by this decision.
  - **Tenant rule:** the relationship's own `organization_id` is always the Knowledge Asset's own persisted value; no cross-tenant relationship may be created; an `organization_id` supplied by the triggering event payload is never treated as authoritative on its own.
  - **Idempotency:** exactly one logical relationship per accepted Knowledge Asset; repeated processing of the same `ACCEPTED` outcome must not create a duplicate. The technical mechanism (database `UNIQUE` constraint vs. check-before-insert vs. another approved mechanism) is **not** decided here — unchanged, still an implementation-time choice, `§17`/`§24` item 4.
  - **Evidence/audit:** attributable to the `ACCEPTED` outcome, the Knowledge Asset, the Organization, and the processing context, through the existing BA-05 evidence/audit pattern already designed in `§23` — no new evidence model is introduced. Exact event schema and field-level implementation remain subject to the BA-04 Increment's own Technical Design.
  - **Ontology Validation cross-check (validation only, per this task's own instruction — `ONT-001` is not modified):** `Governed By` is confirmed present in `RTA-001 §12.9`'s own closed list (re-verified above). `ONT-001 §5`'s own six general relationship categories (`ONT-001-010`–`015`: Classification; Specialization/Generalization; Composition; Aggregation; Association; Reference) still carry no formal, document-stated cross-mapping to `RTA-001 §12.9`'s 12 specific kinds — the same gap `§24` item 5 already discloses, unresolved by this decision and not required to be resolved for Ontology Validation to function per `§16`'s own closed-list-membership sufficiency. As an informal, non-binding cross-check only: a Knowledge Asset's governed-ownership relationship to its Organization is "two Concepts meaningfully connected without either being composed of, aggregating, or specializing the other" — `ONT-001-014` Association's own stated definition — suggesting no inconsistency between the two documents for this specific relationship, though this cross-check is advisory only and does not constitute a formal `ONT-001` mapping decision.

  `KnowledgeGraphSyncHandler`'s own concrete logic for this one relationship can now be designed — its exact code, event contract, and payload shape remain subject to the BA-04 Increment / BA-05 implementation-time Technical Design process, not decided here.

**Net effect on `§25` (Implementation Preconditions):** items 2 and 4 are both now resolved in principle by `RO-DEC-WP14-BA05-03`/`RO-DEC-WP14-BA05-02` above. The remaining precondition is the BA-04 Increment `RO-DEC-WP14-BA05-01` names — it must itself be designed, authorized, implemented, and certified before this document's own §7–§8 trigger assumption is actually true of the running system, and a fresh BA-05 Technical Design Authorization review must incorporate all three decisions before implementation is authorized.

**This recording does not change `§26`'s own conclusion below.** BA-05 implementation remains not authorized by this document. All three Repository Owner decisions (`RO-DEC-WP14-BA05-01`/`02`/`03`) are now resolved in principle, but that alone does not authorize implementation: the BA-04 Increment `RO-DEC-WP14-BA05-01` names does not yet exist, and per `CLAUDE.md §19.7`'s own governance discipline, a fresh BA-05 Technical Design Authorization review is required — re-examining this document once it is updated to incorporate these decisions structurally (§7/§8/§20/§24/§25 above still read, in their own original bodies, as they did before this recording; only §26a records what has since been decided) — before implementation may proceed. *(This paragraph's own "does not yet exist" claim was accurate when originally drafted, immediately after this recording (2026-08-16), but is stale and superseded as of the reconciliation and remediation passes made to this document since — corrected immediately below rather than silently: preserved here as the historical record of this section's own original position, per `ADR-017`/`METH-002`'s no-silent-fix discipline.)* **Corrected — `F-02` of the independent WP-14/BA-05 Technical Design Authorization Review, independently re-verified against the repository:** the BA-04 Increment `RO-DEC-WP14-BA05-01` names was subsequently designed (`TDS-014`), authorized, implemented, independently certified (Gate 1 CERTIFIED, Gate 2 V&V PASS, Gate 5 Release Readiness READY WITH CONDITIONS — documentation-only conditions), committed as `4c86813`, and its closure synchronized into governance (`8b3f475`) — consistent with, not contradicting, `§7`'s own statement above ("CLOSED — CERTIFIED... committed `4c86813`"), which was and remains accurate. The BA-04 Increment therefore now exists and is delivered — this no longer reads as a remaining blocker on that specific ground. What remains genuinely open is a fresh BA-05 Technical Design Authorization review of this document as reconciled and remediated (unaffected by this correction, still required, per `CLAUDE.md §19.7`) — not the Increment's own existence.

## 26. Implementation Authorization Boundary

**This document is Technical Design, not implementation authorization.** The distinction, stated explicitly per this task's own requirement:

- **`ADR-023` = constitutional architecture decision** — already Accepted, already committed (`ccb36af`), already pushed. Settles *what* the tenant boundary is.
- **This Technical Design (`TDS-013`) = determines the implementation mechanism** — *how* BR-1–BR-4 are enforced, which components are reused, which are new, where the mechanism sits in the existing runtime pipeline. Settles *how*, on paper only.
- **Implementation Authorization = a separate, future Repository Owner decision** — the same two-step chartering-then-authorization precedent `WP-10`/`WP-11`/`WP-12` each established, and `ADR-023 §6`'s own explicit statement ("does not authorize BA-05 implementation by itself").
- **BA-05 implementation is NOT authorized by this document.** No migration, model, router, service, API, frontend, or test has been created. `git status` at the time of this document's own creation contains no `Backend/` changes (verified, §27 report).

---

*End of TDS-013. No BA-05 implementation, migration, model, router, service, API, frontend, or test has been created or authorized by this document. Per §26a (2026-08-16), the Repository Owner has approved all three outstanding decisions in principle — trigger model (`RO-DEC-WP14-BA05-01`), the Knowledge Asset→Organization `Governed By` relationship mapping (`RO-DEC-WP14-BA05-02`), and hosting service (`RO-DEC-WP14-BA05-03`). ~~BA-05 implementation remains NOT AUTHORIZED: the BA-04 Increment `RO-DEC-WP14-BA05-01` depends on does not yet exist, and a fresh BA-05 Technical Design Authorization review, incorporating these decisions, has not yet been performed.~~ **Corrected by this remediation pass (`F-02`, independent WP-14/BA-05 Technical Design Authorization Review — the preceding sentence was accurate on 2026-08-16 but is stale/superseded, preserved struck through rather than deleted, per `ADR-017`/`METH-002`):** the BA-04 Increment `RO-DEC-WP14-BA05-01` depends on now exists — designed, authorized, implemented, independently certified, and committed as `4c86813` (governance-synchronized `8b3f475`), consistent with §7 above. BA-05 implementation nonetheless remains **NOT AUTHORIZED** by this document: `RO-DEC-WP14-BA05-02`/`03` still require independent evidentiary recording outside this one artifact (remediated separately, in `WP-14_BA-04_Establish_Knowledge_Asset_Business_Activity_Charter.md`), and a fresh BA-05 Technical Design Authorization review of this document as reconciled and remediated has not yet been performed — that review, not the Increment's own existence, is the actual remaining precondition.*
