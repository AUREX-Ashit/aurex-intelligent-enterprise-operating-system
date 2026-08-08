# ADR-016 — Authorization Runtime Consolidation

**Status:** Accepted
**Classification:** Architecture Governance / Runtime Consolidation
**Decided by:** Repository owner (architecture governance authority), same decision-authority pattern `ADR-006` through `ADR-015` already established.
**Affected Documents:** None edited by this ADR. Formalizes, retroactively, the repository-owner decision already recorded in prose at `IRA-RTA-001 §5` (resolving `IRA-005 §10.2 item 3` as Option 2), and separately authorizes the repository consolidation action performed alongside this ADR (§3 below).
**Affected Code:** `Backend/Services/AuthService/{routers,schemas,services,tests}/authorization_engine*.py` (removed), `Backend/Services/AuthService/main.py` (reverted), `Backend/Services/AuthService/middleware/tenant.py` (reverted).

---

## 1. Context

Two Authorization Engine implementations existed simultaneously in this repository's working tree:

1. **An unauthorized "candidate" implementation** at `Backend/Services/AuthService/{routers,schemas,services,tests}/authorization_engine*.py`, wired into `main.py` (`app.include_router(authorization_engine.router, prefix="/authorization", ...)`) and `middleware/tenant.py` (a tenant-isolation exemption). This code was built before any Runtime Work Package existed to authorize it, self-labeled `"WP-RTA-001 Business Activity: BA-02"` — an identity that, at the time, corresponded to no real chartered artifact. It was independently reviewed (`architecture/06-Reviews/AUTHORIZATION_ENGINE_CONSTITUTIONAL_RESPONSE.md`) and classified **PARTIAL REUSE**: architecturally sound in its precedence-evaluation algorithm and honest-disclosure discipline, but built in direct violation of `ADR-015`'s own "no implementation is authorized" clause and `IRA-005 §10.2 item 3`'s explicit "do not begin" instruction, and resting on a fabricated Work Package/IRA identity.
2. **The now-properly-chartered `WP-RTA-001`** (`IRA-RTA-001`, `WP-RTA-001_Authorization_Runtime_Engine.md`), implemented at `Backend/Runtime/AuthorizationEngine/` across six milestones (M1–M6), independently certified `CERTIFIED WITH CONDITIONS` by a fresh-context reviewer (per `CLAUDE.md §19.7`), 106/106 tests passing.

The independent certification's own Non-Conformity 1 (High, Blocking) found that the first implementation was never removed or reconciled once the second was authorized and completed — both existed side by side, uncommitted, with the certification-facing governance documents disclosing neither the first implementation's continued presence nor its relationship to the second.

## 2. Decision

1. **`WP-RTA-001` (`Backend/Runtime/AuthorizationEngine/`) is confirmed as the single, authoritative Authorization Runtime for this repository.** This formalizes, retroactively and without re-litigation, the decision already recorded in prose at `IRA-RTA-001 §5` — resolving `IRA-005 §10.2 item 3` as **Option 2**: a dedicated Runtime Work Package, separate from any Business Capability Work Package (WP-05 or otherwise), owning no Business Object and performing no Business Activity (`IRA-RTA-001 §9`).
2. **The unauthorized candidate implementation is retired, not reconciled.** Per the independent certification's own recommendation, the repository owner selects removal (not the alternative "formally reconcile it" path) — the candidate code's algorithmic content is not carried forward; `AuthorizationAdapter`/`AuthorizationRequest` (`Backend/Runtime/AuthorizationEngine/adapters/`) remains the sole integration seam any future Business Activity uses.
3. **No new implementation is authorized by this ADR.** `WP-RTA-001` itself remains unmodified (M1–M6, as independently certified). This ADR does not charter `WP-05` or any other Work Package's own implementation.

## 3. Consequences

**Removed** (obsolete, unauthorized, never had constitutional standing per `AUTHORIZATION_ENGINE_CONSTITUTIONAL_RESPONSE.md`'s own F-01/F-02 findings):
- `Backend/Services/AuthService/routers/authorization_engine.py`
- `Backend/Services/AuthService/schemas/authorization_engine.py`
- `Backend/Services/AuthService/services/authorization_engine_service.py`
- `Backend/Services/AuthService/tests/test_authorization_engine_api.py`
- `Backend/Services/AuthService/tests/test_authorization_engine_service.py`

**Reverted to their pre-candidate, committed state** (confirmed via `git diff --stat` showing zero remaining diff against `HEAD` for both files):
- `Backend/Services/AuthService/main.py` — the `authorization_engine` import and its `app.include_router(...)` registration removed.
- `Backend/Services/AuthService/middleware/tenant.py` — the `/authorization/evaluate` tenant-exemption comment block and path condition removed.

**Confirmed unaffected:**
- `Backend/Runtime/AuthorizationEngine/` (the authorized `WP-RTA-001` package) — not touched by this consolidation.
- Every other `Backend/Services/AuthService` router, model, service, and test — confirmed by `pytest --collect-only`: 572 tests collect cleanly with zero import errors after removal.

**Result:** exactly one Authorization Engine / Authorization Runtime implementation now exists anywhere in this repository — `Backend/Runtime/AuthorizationEngine/`, owned by `WP-RTA-001`, integrated exclusively through `AuthorizationAdapter`.

**This ADR resolves the independent certification's Blocking Condition 1** (`CERT-WP-RTA-001`, Non-Conformity 1) and, by formalizing the `IRA-RTA-001 §5` decision, **also resolves Blocking Condition 2** (the missing ADR for that decision) in the same governance pass.

## 4. Status

**Accepted.**
