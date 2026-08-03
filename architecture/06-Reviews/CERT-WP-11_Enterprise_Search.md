# CERT-WP-11 — Independent Certification: Enterprise Search (C-093)

**Work Package:** WP-11 — Enterprise Search (C-093)
**Business Activities:** BA-01 (Establish Enterprise Search Index Configuration), BA-02 (Execute Enterprise Search), BA-03 (Register Enterprise Search Content)
**Platform Prerequisite (consumed, not re-certified here):** AIService Authentication Bootstrap (`IRA-011 §4.4`/§14) — separately authorized and completed before BA-01/02/03 began; this review independently re-confirms it still functions as BA-01/02/03's own foundation, per instruction, but does not re-litigate its own separate authorization.
**State certified:** working tree at time of review (BA-01/02/03 + Frontend "Implementation Complete," not yet committed, per `IMP-REPORT-WP-11_Enterprise_Search.md`)
**Reviewer:** Independent, fresh-context reviewer — no prior involvement in WP-11's implementation
**Gate:** 1 of 5 (`CLAUDE.md §19.7b`)
**Determination:** **CERTIFIED WITH OBSERVATIONS** — no blocking finding; four non-blocking observations recorded below (three Low, one Medium), none security-, tenant-isolation-, or data-integrity-class per `CLAUDE.md §19.8.5`.

---

## Scope and Method

This certification re-derives every material claim in `IMP-REPORT-WP-11_Enterprise_Search.md` from primary sources — it does not accept the report's own prose on trust. Specifically performed:

- Full read of the governing charter (`WP-11_Enterprise_Search.md`), the accepted readiness assessment (`IRA-011_WP-11_Enterprise_Search_Implementation_Readiness_Assessment.md`, all 14 sections), and the Implementation Report.
- Full read of every new/modified backend file: `models/search.py`, `dependencies.py`, `repositories/search_repository.py`, `routers/search.py`, `schemas/search.py`, `services/search_index_service.py`, `services/content_registration_service.py`, `services/search_execution_service.py`, `services/vector_provider.py` (`DocumentChunkRegistryVectorProvider`), `services/rag_engine.py` (pre-existing, confirmed literally reused), `services/embedding_provider.py` (pre-existing), `middleware/tenant.py`, `main.py`, `models/__init__.py`, `routers/__init__.py`, the Alembic chain (`alembic.ini`, `alembic/env.py`, the migration file), `tests/test_search_api.py`, `tests/test_search_unit.py`, `tests/conftest.py`.
- Full read of every new/modified frontend file: `src/features/search/**`, `src/services/search-api.ts`, `src/types/search.ts`, `src/lib/api-client.ts`, `src/lib/config.ts`, `src/app/platform-admin/(workspace)/enterprise-intelligence/page.tsx`, and cross-checked component reuse against `src/components/ui/`.
- Direct line-by-line comparison of `models/search.py`/the Alembic migration against `Master_Technical_Architecture.md` AMD-012's own `CREATE TABLE` text for `vector_index_registry` (lines 3208–3218), `evidence_registry` (lines 2323–2341), `document_chunk_registry` (lines 3189–3201).
- Independent re-run of the full `AIService` test suite.
- Independent re-run of `alembic upgrade head` / `alembic downgrade base` against a fresh SQLite database, with direct schema inspection (`sqlite_master`) after upgrade and table-list inspection after downgrade, then cleanup.
- Independent re-run of `alembic heads` (single head, no branching).
- Independent re-run of `npx tsc --noEmit`, `npx eslint` (scoped to every new/changed frontend file), and a full `npx next build`.
- `git status` / targeted `git diff` at the repository root, cross-checked against the Implementation Report's own "Documents Created / Modified" list.
- Direct comparison of `AIService/dependencies.py`'s claim-decoding logic against `AuthService/services/auth_service.py`'s real `decode_access_token`/`create_access_token` (claim shape, secret/algorithm resolution) to independently confirm token interoperability, not merely accept the report's own "mirrors AuthService" claim.
- Direct read of `TECH-DEBT.md` entries `TD-109`, `TD-123`, `TD-124`, `TD-125`, `TD-126`, `TD-107` (amendment).

## Governing Documents Reviewed

`WP-11_Enterprise_Search.md` (charter, full); `IRA-011_WP-11_Enterprise_Search_Implementation_Readiness_Assessment.md` (full, all 14 sections); `IMP-REPORT-WP-11_Enterprise_Search.md` (full); `Master_Technical_Architecture.md` AMD-012 (`evidence_registry`, `document_chunk_registry`, `vector_index_registry`, read directly at their primary line ranges); `TECH-DEBT.md` (`TD-107`, `TD-109`, `TD-123`–`TD-126`); `CLAUDE.md` §16, §19 (all subsections), §20, §21 (§21.3, §21.4); `CERT-WP-10_Configuration_Management.md` (format/rigor precedent).

---

## Independently Re-Verified as Correct

### Schema conformance (AMD-012, LOCKED)

`models/search.py`'s three SQLAlchemy models and the Alembic migration (`alembic/versions/2026_08_03_1200-d4a9c1e7f3b5_enterprise_search_registries.py`) were compared column-by-column against AMD-012's own `CREATE TABLE` text. **No column added, removed, retyped, or renamed** beyond what AMD-012 already specifies, for all three tables. Cross-service FKs (`organization_id → organization_master`, `evidence_registry.confidence_rule_id → confidence_scoring_registry`) are correctly declared as plain, non-FK columns with a documented rationale (`AuthService`'s own database is a separate service boundary, `CLAUDE.md §8`) — the intra-service FKs AMD-012 itself specifies (`document_chunk_registry.evidence_id → evidence_registry`, `.vector_index_id → vector_index_registry`) are real, physical `ForeignKeyConstraint`s in both the model and the migration, with the `ondelete` behavior (`CASCADE`, `SET NULL`) AMD-012 does not itself constrain but which is a reasonable, disclosed implementation choice.

### Migration, independently run

`AUREX_DATABASE_URL="sqlite+aiosqlite:///cert_test.db" python -m alembic upgrade head` succeeded from a clean state; direct `sqlite_master` inspection confirmed all three tables present with the exact column set, the `retrieval_mode` `CHECK` constraint, and both `document_chunk_registry` foreign keys. `alembic downgrade base` succeeded, leaving only `alembic_version`. `alembic heads` returns a single head (`d4a9c1e7f3b5`), no branching. Test artifact deleted after verification — no stray file left in the working tree (confirmed by `git status` afterward).

### Test suite, independently re-run

`PYTHONCASEOK=1 python -m pytest -v` from `Backend/Services/AIService`: **30 passed, 0 failed** — matching the claimed figure exactly (3 pre-existing `test_ai.py` + 8 `test_authentication.py` + 14 `test_search_api.py` + 5 `test_search_unit.py`). Zero regressions to the pre-existing suite.

### Mandatory Tenant-Isolation Test Checklist (`CLAUDE.md §21.4`)

Independently judged the shipped tests against what the checklist actually requires (not merely that tests with plausible names exist — the same standard `CERT-WP-10`'s own Finding B-1 applied and found wanting elsewhere):

- **(a) Two distinct, unrelated Organizations, no shared row.** `ORG_A`/`ORG_B` are independent `uuid4()` values; every test token is minted per-organization via `_token()`, carrying that organization's own `organization_id` claim — no synthetic shared identity reused across organizations (the exact shortfall `CERT-WP-10` Finding B-1 found in WP-10's own shipped suite). Confirmed by direct read.
- **(b) A caller in one Organization cannot retrieve or infer another's data.** `test_tenant_isolation_index_listing_never_leaks_another_organizations_dedicated_index` and `test_tenant_isolation_content_registered_under_shared_platform_index_stays_org_scoped` both independently confirmed to exercise a genuine cross-organization read attempt (not a same-organization re-query) and correctly assert the leak does not occur.
- **(c) Explicit probe of an unrelated tenant's own identifier.** `test_tenant_isolation_probe_unrelated_tenant_index_name_is_not_accepted` — Org B supplies Org A's own private `index_name` string verbatim; asserts 404, not silent scoping. This is the caller-supplied, non-claims-derived identifier `§21.4(c)` requires be probed, and it is a genuine probe (Org A's index is real, registered, and contains content — not merely absent).

Independently confirmed the *mechanism*, not just the tests: `VectorIndexRegistryRepository.get_by_name_for_caller`/`get_default_for_caller`/`get_by_id_for_caller` all filter by `organization_id == caller OR organization_id IS NULL` — never an unscoped lookup by name or id alone. `DocumentChunkRegistryRepository.list_for_index` filters by both `vector_index_id` AND `organization_id` together — so even a platform-wide (shared) index's own chunks remain organization-scoped at the content layer, independent of the index row's own visibility. `DocumentChunkRegistryVectorProvider` additionally re-applies `organization_id` scoping inside the vector-search call itself (constructed once per request from the caller's own verified claim in `routers/search.py::get_search_service`) — a genuine second, independent check, not a single point of trust. This is real structural scoping, not a bolted-on check that could be bypassed by a different code path.

### PLATFORM_ADMIN gating

Confirmed directly in `routers/search.py`: `establish_index_configuration` and `register_content` both depend on `require_platform_admin`; `list_index_configurations` and `execute_search` depend only on `get_current_claims` (any authenticated caller). `require_platform_admin` (`dependencies.py`) checks `claims.get("role_code") != "PLATFORM_ADMIN"` and 403s otherwise — independently confirmed by the two `..._requires_platform_admin` tests passing with a `MEMBER`-role token receiving 403, and by direct code read (not merely trusting the test names).

### Authentication interoperability (re-verifying the platform prerequisite's own foundation, per instruction)

Directly compared `AIService/dependencies.py::decode_access_token` against `AuthService/services/auth_service.py`'s real `decode_access_token`/`create_access_token`. Claim shape (`person_id`, `identity_id`, `organization_id`, `membership_id`, `role_code`, `exp`, `type`) is identical on both sides. Secret resolution: `AuthService` reads `JWT_SECRET_KEY` only (`config.py` line 183); `AIService` reads `AUREX_JWT_SECRET_KEY` first, falling back to `JWT_SECRET_KEY` (`config/settings.py` line 158) — so a deployment setting only `JWT_SECRET_KEY` (as `AuthService` requires) is correctly picked up by both services identically. Algorithm defaults to `HS256` in both. A real `AuthService`-issued token would genuinely verify in `AIService` as claimed — this is not a parallel, look-alike mechanism.

### RAGEngine reuse

`services/rag_engine.py` (pre-existing, unmodified — confirmed absent from `git status`) is called literally and unmodified by `SearchExecutionService.execute()`, with only its constructor arguments (`embedder`, `vector_db`) substituted for real implementations. The claimed "reused, not reimplemented" is accurate.

### Frontend — build, types, lint

`npx tsc --noEmit`: clean, zero errors. `npx eslint` scoped to every new/changed WP-11 file: clean, zero problems. `npx next build`: succeeds, `/platform-admin/enterprise-intelligence` compiles and prerenders alongside all other existing routes, zero regressions — matches the claimed "38/38 routes."

### Design System component reuse

`Button`, `Card`/`CardTitle`/`CardDescription`, `Form` family (`FormField`/`FormLabel`/`FormBanner`/`FormHelperText`), `Input`, `LoadingState`, `Spinner`, `StatusBadge`, `Table` family — every one independently confirmed to exist as a real, pre-existing file under `src/components/ui/`, not invented. No new component, token, or theme introduced.

### Five mandatory UI states (`CLAUDE.md §20.6`)

Independently confirmed in `SearchIndexSection.tsx`/`RegisterContentSection.tsx`/`ExecuteSearchSection.tsx`, wired to real state machines (`useSearchManagement.ts`), not hardcoded: loading (`LoadingState` on the index list; `Spinner` in-button during establish/register/search), empty (explicit "No search index has been established yet" / honest backend-supplied `message` on a content-less search — never a fabricated result), validation (required fields, submit disabled while invalid or in flight), error (`FormBanner tone="danger"`, with Retry on the list load), confirmation (`FormBanner tone="success"` on establish/register). A successful search's own results list functions as BA-02's confirmation state — a reasonable interpretation for a query surface, consistent with `CERT-WP-10`'s own acceptance of an analogous read-path interpretation.

### Business Object Eligibility (`CMD-001 §26.3a`)

Independently confirmed **not required**, for the reason `IRA-011 §6` states: `vector_index_registry`/`document_chunk_registry`/`evidence_registry` are already canonical, LOCKED, AMD-012-registered constructs — the eligibility test governs newly-discovered candidate constructs, not tables the physical architecture has already specified. `CBOR-INDEX.md` was checked directly and contains no reference to any of the three tables — consistent with this determination, not an oversight.

### Change surface / governance-document accuracy

`git status --porcelain` at the repository root and scoped to `Backend/Services/AIService` was independently checked against the Implementation Report's own "Documents Created / Modified" list. Every backend and frontend file the report names is present in the actual diff; no unexplained WP-11-scoped file appears outside that list. `WP-REG-001`, `WPR-001`, `DOC-000`, and `SER-001` are also modified (see Observation 1, below — these are accurate but not itemized in the report's own list). Unrelated, concurrent working-tree material (`Backend/Runtime/`, `WP-RTA-001`-family documents, `design/`, `historical-ui-tree.txt`, `RELEASE-C-INITIATION-SUMMARY.md`) is present but belongs to separate, disclosed work outside WP-11's own scope — the same "present but not evaluated by this certification" treatment `CERT-WP-10` applied to analogous concurrent artifacts in its own review. `WP-REG-001`/`WPR-001` were independently read in full for their WP-11 rows and correctly state "Implementation Complete — awaiting Gate 1" throughout, never prematurely claiming certification or closure.

### TECH-DEBT.md entries

`TD-109`: **Closed**, correctly attributes resolution to WP-11, and independently confirmed true — `SearchExecutionService` resolves against `vector_index_registry`, not `rag_configs`; `rag_configs`/`RAGConfigModel` untouched by any WP-11 code path (confirmed by `grep` — no WP-11 file imports `models.rag`). `TD-123`: **Closed**, and the described `SyntaxError` fix in `schemas/extraction.py` was confirmed present and correct (`whistleblower_hotline_active`, no stray space). `TD-124`/`TD-125`/`TD-126`: all **Open**, all **Low**, all accurately described against what the code actually does (interim `PLATFORM_ADMIN` gate; fixed-size, non-configurable chunking; a disclosed double-query in `SearchExecutionService.execute()`, independently confirmed by direct read — `build_context()` is called once for its side-effect-free string, then `search_index()` is called again for structured results). Severity ratings independently checked against `CLAUDE.md §19.8.7`'s rubric and found correctly Low in all three cases — none defeats BA-01/02/03's own Business Intent, none touches a security or tenant boundary. `TD-107`'s amendment (JWTManager incompatibility finding) was independently spot-checked against `Backend/Shared/Security/jwt_manager.py` and found accurate — `JWTManager.create_token()`'s claim shape genuinely does not match `AuthService`'s real claims.

---

## Observations (Non-Blocking)

None of the following is a `CLAUDE.md §19.8.5`-class defect (security, tenant-isolation, data-integrity, failing test, or build failure) — each is eligible for Technical Debt tracking rather than blocking this gate, per §19.8.5's own governance.

### Observation 1 (Low) — Implementation Report's own "Documents Created / Modified" list omits four governance-register updates that actually occurred

`git diff --stat` confirms `architecture/00-Governance/DOC-000_Documentation_Catalogue.md`, `WP-REG-001_Enterprise_Work_Package_Register.md`, `WPR-001_Work_Package_Roadmap.md`, and `architecture/06-Reviews/SER-001_Strategic_Enhancement_Register.md` are all genuinely modified as part of this Work Package's own governance-synchronization pass, but none appears in `IMP-REPORT-WP-11_Enterprise_Search.md`'s own "Documents Created / Modified" section (which lists only Backend, Frontend, and `TECH-DEBT.md` + itself). The content of all four diffs was independently read and found accurate (no staleness, no premature closure claim) — this is a completeness gap in the report's own itemization, not an accuracy defect in the registers themselves. Recommend the Implementation Report's own list be corrected to include these four files for a complete audit trail, at Gate 2 or Gate 5.

### Observation 2 (Medium) — Establishing a `vector_index_registry` row with any `embedding_dimension` other than 1536 silently makes BA-03 (content registration) permanently fail for that index

`services/embedding_provider.py::get_embedding_provider()` (pre-existing, unmodified by WP-11) always constructs `AzureEmbeddingStubProvider(model_name=settings.embedding_model)` — the `dimensions` parameter is never passed, so it always defaults to `1536`, regardless of `settings.embedding_model` or any per-index configuration. `ContentRegistrationService.register()` (new, WP-11) then compares the stub's always-1536-dimension output against `index.embedding_dimension` and raises `422` on any mismatch (`services/content_registration_service.py` lines 84–92) — this is real, functioning validation, not decorative, exactly as the Implementation Report claims. However, `SearchIndexSection.tsx`'s own establish form exposes `embedding_dimension` as a freely-editable number input (defaulting to `"1536"`, but not constrained to it) — a caller who establishes an index with, e.g., `768` or `3072` (both plausible, real embedding-model dimensions) will find every subsequent BA-03 registration attempt against that index fails with a 422 the UI surfaces only as a generic error banner, with no indication that `1536` is the only value the current stub actually supports. This is a genuine interaction between a pre-existing stub (not itself new) and WP-11's own new validation logic (which is new), not previously disclosed anywhere as its own risk — the general "no real embedding provider" exclusion (`IRA-011 §4.6`) discloses that ranking/relevance is stubbed, but not that a specific, easily-triggered configuration choice silently breaks BA-03 end-to-end. Per `CLAUDE.md §19.8.7`, rated Medium: an internal completeness/robustness concern that does not defeat BA-01/02/03's stated Business Intent when the documented default (1536) is used, but is expected to surface in real use once any Repository Owner or demo user changes that field. Recommend either constraining the establish form to the stub's actual supported dimension, or passing the index's own configured dimension through to the embedding provider, as a Technical Debt item.

### Observation 3 (Low) — `VectorIndexRegistryRepository.get_by_id_for_caller` is unused dead code

Defined with correct tenant-scoping logic (mirrors `get_by_name_for_caller`'s own scoping exactly) but no service or router in this Work Package calls it — confirmed by repository-wide `grep`, zero call sites beyond its own definition. Not a defect (the scoping it implements is correct, should a future caller need id-based resolution), but worth removing or wiring up rather than left as an unreferenced method, per `CLAUDE.md §10`'s "remove dead code."

### Observation 4 (Low) — `RegisterContentSection.tsx`'s text-passage field is a raw `<textarea>`, not a Design System component

No `Textarea` component exists yet under `src/components/ui/` (confirmed by directory listing) — there is genuinely nothing to reuse, so this is not a "should have reused an existing component and didn't" defect. The raw element's own Tailwind classes (`border-border`, `bg-surface`, `text-foreground`) partially mirror `Input.tsx`'s own token usage but omit `Input`'s focus-ring, transition, and disabled-cursor treatment — a minor visual/interaction inconsistency against the rest of the same form. Worth a Technical Debt entry once a canonical `Textarea` DS-001 component exists to reuse instead.

---

## Recommendation

**Proceed to Gate 2 (V&V Audit).** No finding in this review is `§19.8.5`-class or otherwise blocking. Carry Observations 1–4 into the V&V Audit's own mandate: Observation 2 (Medium) as a candidate new Technical Debt entry (or an immediate, low-cost fix — either the establish-form constraint or threading the index's own dimension into the embedding provider call would resolve it without new architecture); Observations 1, 3, 4 (Low) as documentation/cleanup items, not requiring rework before Gate 2 proceeds.

All other aspects of this Work Package — AMD-012 schema conformance (zero deviation), Alembic migration correctness and reversibility, tenant isolation (structural, not bolted-on, independently probed at every layer), authentication interoperability with real `AuthService`-issued tokens, `RAGEngine` reuse, Business Object Eligibility determination, backend/frontend test and build results, Enterprise Experience wiring against real DS-001 components, and governance-register accuracy — are independently confirmed sound and require no rework.

---

*End of CERT-WP-11. Gate 2 (V&V Audit) may proceed on the current code.*
