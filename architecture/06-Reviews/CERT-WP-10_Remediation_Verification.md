# CERT-WP-10 — Independent Verification of Remediation: Configuration Management (C-041)

**Work Package:** WP-10 — Configuration Management (C-041)
**Finding remediated:** `CERT-WP-10_Configuration_Management.md` Finding B-1 (High, blocking) — `GET /configuration` trusted the client-supplied `X-Tenant-ID` header with no verification against the caller's own JWT `organization_id` claim or Membership, allowing any authenticated Person, including one with no relationship whatsoever to the target Organization, to read that Organization's Configuration.
**Reviewer:** Independent, fresh-context reviewer — no prior involvement in WP-10's implementation, in `CERT-WP-10`'s own Gate 1 Certification, or in the remediation itself.
**Gate:** 4 of 5 (`CLAUDE.md §19.7b`) — Independent Verification of Remediation, required regardless of the finding's own severity, per this repository's established precedent (`VV-AUDIT-WP-05_Remediation_Verification.md`, `VV-AUDIT-WP-09_Remediation_Verification.md`).
**Determination:** **REMEDIATION VERIFIED**

---

## What Was Reviewed

- `CERT-WP-10_Configuration_Management.md` in full (Finding B-1's own probe, reasoning, and recommended remediation shape).
- Current state of `Backend/Services/AuthService/dependencies.py` (new `require_matching_tenant_or_platform_admin` dependency) and `Backend/Services/AuthService/routers/configuration.py` (its wiring into `resolve_configuration`).
- The three new tests in `Backend/Services/AuthService/tests/test_configuration_api.py`: `test_resolve_rejects_mismatched_tenant_for_non_admin`, `test_resolve_allows_platform_admin_to_view_a_different_tenant`, and `TestConfigurationTenantIsolation::test_outsider_with_no_relationship_to_org_cannot_resolve_its_configuration`.
- `Backend/Services/AuthService/middleware/tenant.py` (`get_current_tenant()` and the `TenantMiddleware` that populates the `ContextVar` it reads).

None of these files are yet committed to git (`git status --short` confirms `dependencies.py` modified and `routers/configuration.py` / `tests/test_configuration_api.py` untracked, consistent with `IMP-REPORT-WP-10`'s own "not yet committed" state at the time of `CERT-WP-10`) — the negative control below was therefore performed via direct, temporary file edit rather than a git checkout of a prior commit.

---

## Negative Control (this gate's own central requirement)

Per `CLAUDE.md §19.7b`: "the reviewer SHALL also run a negative control — the same probe executed against the pre-fix code... to confirm the probe actually reproduces the original defect."

**Method.** `routers/configuration.py`'s `resolve_configuration` was temporarily reverted (via `Edit`) from `Depends(require_matching_tenant_or_platform_admin)` back to `Depends(get_current_claims)` — its exact pre-remediation state — and the import line adjusted accordingly. The two negative-control-relevant new tests were then run against this reverted code:

```
JWT_SECRET_KEY=test-secret ./venv/Scripts/python.exe -m pytest \
  tests/test_configuration_api.py::test_resolve_rejects_mismatched_tenant_for_non_admin \
  tests/test_configuration_api.py::TestConfigurationTenantIsolation::test_outsider_with_no_relationship_to_org_cannot_resolve_its_configuration \
  -v
```

**Result: both tests FAILED**, as required to prove the probe is genuine and not trivially true:

- `test_resolve_rejects_mismatched_tenant_for_non_admin`: `assert response.status_code == 403` → actual `200`.
- `TestConfigurationTenantIsolation::test_outsider_with_no_relationship_to_org_cannot_resolve_its_configuration`: `assert response.status_code == 403` → actual `200`, with the response body containing Organization A's own established `theme_class = BOARDROOM` override, disclosed to an "Outsider" caller whose own JWT `organization_id` claim names neither Organization A nor Organization B. This is byte-for-byte the same defect shape `CERT-WP-10` Finding B-1 originally reproduced (Organization B's `BRANDING`/`logo_url` override disclosed to an unrelated caller).

This confirms the two tests are a genuine, non-trivial reproduction of Finding B-1, not an assertion that would pass regardless of the fix.

**Restoration.** The temporary edit was then reverted: the import line restored to `from dependencies import require_matching_tenant_or_platform_admin, require_platform_admin` and `resolve_configuration`'s claims dependency restored to `Depends(require_matching_tenant_or_platform_admin)`. Independently re-confirmed by direct grep of the file afterward — no `get_current_claims` reference and no stray edit markers remain in `routers/configuration.py`; the fixed state is exactly as the implementing session left it.

## Post-Fix Confirmation

With the fix restored, the same two tests plus the two "does the fix still allow legitimate access" tests were re-run:

```
tests/test_configuration_api.py::test_resolve_rejects_mismatched_tenant_for_non_admin PASSED
tests/test_configuration_api.py::TestConfigurationTenantIsolation::test_outsider_with_no_relationship_to_org_cannot_resolve_its_configuration PASSED
tests/test_configuration_api.py::test_resolve_allows_platform_admin_to_view_a_different_tenant PASSED
tests/test_configuration_api.py::test_resolve_is_open_to_any_authenticated_caller_not_only_platform_admin PASSED
```

All four pass. Read together with the negative control above, this satisfies `CLAUDE.md §19.7b`'s own method requirement: the probe fails against the pre-fix code and passes against the post-fix code, and the fix does not collaterally block the endpoint's own legitimate callers.

## Correctness of `require_matching_tenant_or_platform_admin` (Independent Judgment)

Read directly in `dependencies.py`:

```python
async def require_matching_tenant_or_platform_admin(
    claims: Annotated[dict, Depends(get_current_claims)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant)],
) -> dict:
    if claims.get("role_code") == PLATFORM_ADMIN_ROLE_CODE:
        return claims
    if claims.get("organization_id") != str(tenant_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, ...)
    return claims
```

This is correct against the endpoint's own stated Business Intent ("every caller resolves their own tenant's Configuration; `PLATFORM_ADMIN` may still view any tenant"):

- `PLATFORM_ADMIN` short-circuits first and is never subject to the tenant-match check — matches the endpoint's own original administrator-oversight design, which `CERT-WP-10` explicitly found correct-in-intent and not part of Finding B-1.
- For every other caller, the comparison is against `claims.get("organization_id")` — a value carried in the caller's own signed JWT, not attacker-controlled — compared with `str(tenant_id)`, the value `get_current_tenant()` resolved from the `X-Tenant-ID` header via `TenantMiddleware`. A mismatch is rejected with 403 before any repository query runs. This closes exactly the gap Finding B-1 identified: the header is no longer trusted on its own.
- No bypass path exists: there is no code path in `resolve_configuration` (`routers/configuration.py`) that reaches `resolution_service.resolve(...)` other than through this dependency — `claims` and `organization_id` for the actual resolution call are both sourced from the same request's dependency graph, not recomputed independently afterward.

`test_resolve_is_open_to_any_authenticated_caller_not_only_platform_admin` (an `ESG_MANAGER`-role caller resolving their own tenant) and `test_resolve_allows_platform_admin_to_view_a_different_tenant` (a `PLATFORM_ADMIN` caller with a different `organization_id` claim than the `X-Tenant-ID` requested) both pass in the fixed state, confirming the dependency does not over-restrict: legitimate self-tenant access and legitimate administrator cross-tenant access are both preserved.

## Full Regression Suite

`JWT_SECRET_KEY=test-secret ./venv/Scripts/python.exe -m pytest tests/ -q` in the fixed (post-remediation, post-negative-control-revert) state: **743 passed, 0 failed, 52 warnings** (585.95s). This is 3 more than `CERT-WP-10`'s own independently-confirmed 740, consistent exactly with the 3 new tests the remediation added (`test_resolve_rejects_mismatched_tenant_for_non_admin`, `test_resolve_allows_platform_admin_to_view_a_different_tenant`, `TestConfigurationTenantIsolation::test_outsider_with_no_relationship_to_org_cannot_resolve_its_configuration`). No regression anywhere else in the suite.

## New-Defect Check: Import Cycle / Double Evaluation

`dependencies.py` imports `get_current_tenant` from `middleware.tenant` (line 24) — a new import for this module, added by the remediation. Checked directly for risk:

- **Circular import:** `middleware/tenant.py` imports only `uuid`, `contextvars`, `starlette.middleware.base`, and `fastapi` — it does not import `dependencies.py`, `routers/configuration.py`, or anything that transitively imports either. The import is strictly one-directional (`dependencies.py` → `middleware.tenant`); no cycle exists. `main.py` imports `middleware.tenant.TenantMiddleware` directly and `routers.configuration` (which itself imports both `dependencies` and `middleware.tenant`) — both resolve cleanly, confirmed by the test suite above actually running (a circular import would fail at collection, not merely at runtime).
- **Double evaluation / divergence risk:** `get_current_tenant()` is called twice in `resolve_configuration`'s dependency graph — once as `tenant_id` inside `require_matching_tenant_or_platform_admin` (`dependencies.py:57`), once directly as `organization_id` in `resolve_configuration` itself (`routers/configuration.py:69`). Two independent reasons this cannot diverge within a single request: (1) FastAPI's dependency resolution caches a dependency's result per request by callable identity by default (`use_cache=True` is the default and not overridden anywhere in this codebase — confirmed by grep, zero `use_cache` occurrences), so the second call site reuses the first call's cached result rather than re-invoking the function; (2) even disregarding caching, `get_current_tenant()` is a pure, synchronous read of a `ContextVar` (`tenant_context`) that `TenantMiddleware.dispatch()` sets exactly once, before the route handler and all its dependencies run, and does not mutate again until teardown (`finally: tenant_context.reset(token)`, after the response is built) — there is no code path between the two evaluations that could change the `ContextVar`'s value. Both call sites are therefore guaranteed to observe the identical `tenant_id`/`organization_id`, whether or not FastAPI's caching is relied upon.

No new defect found in this area.

## New-Defect Check: `POST /configuration` and `GET /configuration/entries` Unaffected

Read directly in `routers/configuration.py`, current state:

- `establish_configuration` (`POST /configuration`, BA-02): `claims: Annotated[dict, Depends(require_platform_admin)]` — unchanged, still `PLATFORM_ADMIN`-gated.
- `list_configuration_entries` (`GET /configuration/entries`, BA-02): `claims: Annotated[dict, Depends(require_platform_admin)]` — unchanged, still `PLATFORM_ADMIN`-gated.

Only `resolve_configuration` (`GET /configuration`, BA-01) was touched by the remediation — its claims dependency changed from `get_current_claims` to `require_matching_tenant_or_platform_admin`, and its docstring/`description=` text updated to describe the new guarantee. No other route in the file was modified. This matches `CERT-WP-10`'s own scoping of Finding B-1 to the resolve path only, and confirms the remediation did not silently touch the two endpoints it wasn't meant to change.

---

## Verdict

**REMEDIATION VERIFIED.**

- The negative control confirms the two governing tests genuinely reproduce Finding B-1 against the pre-fix code (both failed, returning 200 where 403 was required — one of them disclosing another Organization's actual Configuration override to an unrelated caller) and both pass against the post-fix code.
- `require_matching_tenant_or_platform_admin`'s own logic is independently confirmed correct: it closes the disclosure for non-admin callers while preserving both a normal caller's own-tenant access and `PLATFORM_ADMIN`'s cross-tenant access, exactly matching BA-01's stated Business Intent.
- No new defect was found: no import cycle, no double-evaluation/divergence risk in the two `get_current_tenant()` call sites, and `POST /configuration` / `GET /configuration/entries` are confirmed untouched and still `PLATFORM_ADMIN`-gated.
- Full regression suite: **743 passed, 0 failed** — exactly `CERT-WP-10`'s own 740 plus the 3 new tests this remediation added, with no regression elsewhere.
- The repository has been left in the fixed state: `routers/configuration.py`'s `resolve_configuration` uses `require_matching_tenant_or_platform_admin`, with no stray temporary-revert artifacts remaining (independently re-confirmed by direct grep after the negative-control revert was undone).

Finding B-1 is genuinely closed. No `CLAUDE.md §19.8.5`-class defect survives in the fix itself. **Gate 4 passes** — WP-10 may proceed to Gate 2 (V&V Audit), which SHALL also carry forward `CERT-WP-10`'s own Findings G2-1 (Medium, concurrent-write race on Configuration uniqueness) and G2-2 (Low, no action required), per `CERT-WP-10`'s own Recommendation §2.

---

*End of CERT-WP-10_Remediation_Verification. This gate is strictly scoped to Finding B-1's remediation — it does not perform the full Gate 2 V&V Audit, which remains a separate, later step per `CLAUDE.md §19.7b`.*
