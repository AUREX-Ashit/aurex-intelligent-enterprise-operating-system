# CERT-WP-12 — Independent Certification: AI Conversation Management (C-094)

**Work Package:** WP-12 — AI Conversation Management (C-094)
**Business Activities:** BA-01 (Establish and Manage Conversation Lifecycle), BA-02 (Execute Interaction), BA-03 (Retrieve Conversation)
**State certified:** repository at commit `79d8bca` (`master`) — the four-commit sequence `86af6e6` (IRA-012/TDS-012), `fd69366` (backend), `2a07427` (frontend), `79d8bca` (IMP-REPORT-WP-12)
**Reviewer:** Independent, fresh-context reviewer — no prior involvement in WP-12's implementation
**Gate:** 1 of 5 (`CLAUDE.md §19.7b`)
**Determination:** **CERTIFIED WITH FINDINGS (non-blocking)** — no `CLAUDE.md §19.8.5`-class defect found; two Medium and two Low findings recorded below, none security-, tenant-isolation-, or data-integrity-class.

---

## Scope and Method

This certification re-derives every material claim in `IMP-REPORT-WP-12_AI_Conversation_Management.md` from primary sources — the report's own prose is not accepted on trust. Specifically performed:

- Full read of `IRA-012_WP-12_AI_Conversation_Management_Implementation_Readiness_Assessment.md` and `TDS-012_WP-12_AI_Conversation_Management_Technical_Design.md` (both in full), and `IMP-REPORT-WP-12_AI_Conversation_Management.md` (in full).
- Full read of every new/modified backend file: `models/conversation.py`, `repositories/conversation_repository.py`, `routers/conversation.py`, `schemas/conversation.py`, `services/conversation_service.py`, `services/conversation_state_resolver.py`, `services/interaction_service.py`, `services/interaction_state_assembler.py`, `observability.py`, `middleware/tenant.py`, `main.py` (diff only), the Alembic migration (`2026_08_07_0300-b7f2a9c4e8d1_conversation_management_registries.py`), `tests/test_conversation.py` (in full), `dependencies.py`.
- Full read of every new frontend file: `source/frontend/src/features/conversation/**`, `src/components/ui/ProgressiveDisclosure.tsx`, `src/components/ui/EvidencePanel.tsx`, `src/services/conversation-api.ts`, `src/types/conversation.ts`, `src/config/admin-navigation.ts` (diff), `src/app/platform-admin/(workspace)/ai-conversation/page.tsx`.
- Direct read of governing constitutional text: `RTA-001 §13.15a` (AI Session Management), `SD-001 §16` (`SD-001-113`–`121`), `CMD-001 §24.4`/`§24.4a`/`§26.3a`, `IMP-001 §13.26–53` and `§10.3`/`§10.4` (`IMP-FE-004`), `ADR-020` (including its Clarifications), `CBOR-INDEX.md`.
- Independent re-run of the full `AIService` test suite.
- Independent re-run of `alembic upgrade head` / `alembic downgrade base` against a fresh SQLite database, with direct `PRAGMA table_info`/`PRAGMA foreign_key_list` schema inspection after upgrade, then cleanup; independent re-run of `alembic heads`.
- Independent re-run of `npx tsc --noEmit`, `npx eslint` (scoped to every new/changed WP-12 file), and a full `npx next build`.
- `git show --stat` on each of the four WP-12 commits and `git status --short` at the repository root, to independently confirm commit-boundary cleanliness.
- Direct grep of `tests/test_conversation.py` for concurrency-probe coverage (`concurrent`/`gather`/`race`) against `TDS-012 §9`'s own explicit testing commitment.

## Governing Documents Reviewed

`IRA-012_WP-12_AI_Conversation_Management_Implementation_Readiness_Assessment.md` (full); `TDS-012_WP-12_AI_Conversation_Management_Technical_Design.md` (full); `IMP-REPORT-WP-12_AI_Conversation_Management.md` (full); `RTA-001 §13.15a`; `SD-001 §16` (`SD-001-113`–`121`); `CMD-001 §24.4`/`§24.4a`/`§26.3a`/`§26.4`; `ADR-020` (full, including Clarifications 1–4); `IMP-001 §13.26–53`, `§10.3`/`§10.4`; `CBOR-INDEX.md`; `CLAUDE.md §16`, `§19` (all subsections), `§20`, `§21` (`§21.3`, `§21.4`); `CERT-WP-11_Enterprise_Search.md` (format/rigor precedent).

---

## Point-by-Point Findings

### 1. Backend tests actually run and pass

**Checked:** ran the real suite myself; did not trust the report's "55/55" claim.

**Command run (after diagnosing an environment-only import issue — see note below):**
```
cd Backend/Services/AIService
PYTHONCASEOK=1 py -m pytest -v
```
**Actual output (tail):** `======================= 55 passed, 6 warnings in 6.62s ========================`, matching every test name enumerated in the report (52 pre-existing/BA-01–03 + 3 new authorization-boundary tests).

**Note (not a WP-12 defect):** without `PYTHONCASEOK=1`, `pytest` fails at collection with `ModuleNotFoundError: No module named 'config'` — the on-disk package is `Config/` (capital C) but every import site (`main.py`, `dependencies.py`, etc.) imports lowercase `config.settings`. Confirmed via `git show fd69366 -- Backend/Services/AIService/main.py` that WP-12's own diff to `main.py` only adds the router import/registration (2 lines) — the `config.settings` import line is untouched, pre-existing since before WP-12. This is a pre-existing, environment-specific (Windows case-sensitive-import) condition, not introduced by this Work Package, and the task's own instructions already anticipated it (`PYTHONCASEOK=1`).

**Conclusion: Pass.**

### 2. Schema conformance (TDS-012 §4)

**Checked:** direct column-by-column comparison of `models/conversation.py` and the Alembic migration against `TDS-012 §4`'s own `CREATE TABLE`-equivalent text, plus direct `PRAGMA table_info`/`PRAGMA foreign_key_list` inspection of the actual database produced by `alembic upgrade head`.

**Result:** all three tables (`conversation_registry`, `interaction_registry`, `interaction_prompt_execution`) match TDS-012 §4 column-for-column, including both `CHECK` constraints, the `UNIQUE(conversation_id, sequence_number)` constraint, and both `ForeignKeyConstraint`s (`ondelete='CASCADE'` on both), independently confirmed present in the actual SQLite schema after migration.

**One deviation found:** `TDS-012 §4` specifies `interaction_registry.confidence_score` as `NUMERIC NULL`. Both `models/conversation.py` (`Mapped[int | None] = mapped_column(Integer, ...)`) and the migration (`sa.Column('confidence_score', sa.Integer(), ...)`) implement it as `Integer`, not `NUMERIC`. Currently inert — the field is always written `None` (`TD-133`, disclosed placeholder) — but a future real confidence score with fractional precision (e.g., a `0.87` probability, as opposed to an integer percentage) cannot be stored as `NUMERIC` designed without a follow-on migration.

**Conclusion: Finding (Low)** — schema type deviation from the approved Technical Design, currently without functional impact. Recommend recording as new Technical Debt (not currently in `TECH-DEBT.md`'s `TD-129`–`TD-133` range) or correcting before a real Reasoning Engine (`TD-133`'s own resolution) begins writing this column.

### 3. API contract conformance (TDS-012 §5)

**Checked:** direct read of `routers/conversation.py` against `TDS-012 §5`'s table.

**Result:** all four endpoints match exactly — `POST /conversations` (201), `POST /conversations/{id}/close`, `POST /conversations/{id}/interactions` (201, 409 against Closed, 404 against unknown/cross-tenant), `GET /conversations/{id}/interactions` (200). Every response composes `confidence_score`/`evidence_reference` fields per `TDS-012 §5`'s own requirement, confirmed in `schemas/conversation.py::InteractionResponse`. No new API convention introduced.

**Conclusion: Pass.**

### 4. Security/Authorization conformance (TDS-012 §8)

**Checked:** direct code read of `routers/conversation.py`'s dependency wiring, not just test names.

**Result:** `establish_conversation`, `close_conversation`, and `execute_interaction` each depend on `Annotated[dict, Depends(require_platform_admin)]`; `list_interactions` depends only on `Annotated[dict, Depends(get_current_claims)]`. `require_platform_admin` (`dependencies.py`) 403s unless `claims.get("role_code") == "PLATFORM_ADMIN"`. Independently confirmed by direct code read, not merely by the three `..._requires_platform_admin` tests passing (which were also independently re-run and confirmed passing).

**Conclusion: Pass.**

### 5. Audit wiring conformance (TDS-012 §8)

**Checked:** direct read of `services/conversation_service.py` and `services/interaction_service.py` for every state-changing path.

**Result:** `ConversationService.establish()` calls `record_audit(..., AuditStatus.SUCCESS)`; `close()` calls `record_audit` on both the not-found `DENIED` path and the invalid-transition `DENIED` path, and again on the `SUCCESS` path. `InteractionService.execute()` calls `record_audit(..., AuditStatus.DENIED)` when the Conversation-open gate raises, `record_audit(..., AuditStatus.FAILED)` in the `except Exception` branch around `complete()`, and `record_audit(..., AuditStatus.SUCCESS)` on the normal path. `list_for_conversation` (BA-03, a read path) does not call `record_audit` — correctly so: `TDS-012 §8` only commits BA-01/BA-02 *state changes* to audit wiring, and BA-03 is read-only.

**Conclusion: Pass.**

### 6. Mandatory Tenant-Isolation Test Checklist (CLAUDE.md §21.4)

**Checked:** full read of `tests/test_conversation.py`, not just test-name counting.

**Result:**
- **(a)** `_ORG_A`/`_ORG_B` are two distinct, hardcoded UUIDs, no shared row; every token is minted per-organization via `_token()`.
- **(b)** `test_caller_in_org_a_cannot_close_org_bs_conversation` and `test_org_a_cannot_retrieve_org_bs_conversation_interactions` both genuinely construct a Conversation under one Organization and attempt cross-tenant access from the other, asserting `404` (not `403` — existence itself undisclosed, correctly reasoned).
- **(c)** `test_unrelated_tenants_conversation_id_is_rejected_not_accepted` (BA-01 close) and `test_org_a_cannot_execute_interaction_against_org_bs_conversation` (BA-02 execute) both supply a real, existing, unrelated tenant's own `conversation_id` verbatim and assert `404`, not silent scoping or a fabricated empty result — the genuine probe `§21.4(c)` requires.
- Independently confirmed the *mechanism*, not just the tests: `ConversationRepository.get_by_id_for_caller` filters by `conversation_id == X AND organization_id == caller` in one query — never an unscoped lookup by id alone; `InteractionRepository.list_for_conversation` filters the same way.
- **Incidental defect, independently re-verified as fixed:** the report claims `InteractionService.list_for_conversation` (BA-03) initially leaked a `200`/empty-list response for a cross-tenant `conversation_id` instead of `404`, fixed by gating on `ConversationService.require_exists()` first. Direct code read confirms the fix is present (`interaction_service.py` line 121: `await self.conversation_service.require_exists(...)` precedes the interaction query) and `test_org_a_cannot_retrieve_org_bs_conversation_interactions` passes against the current code.

**Conclusion: Pass** — exceeds the minimum checklist (covers BA-01 and BA-02/BA-03, not just one Business Activity).

### 7. Structural Memory exclusion (ADR-020 Decision 4)

**Checked:** direct read of `services/interaction_state_assembler.py`'s import graph and `test_state_assembler_has_no_memory_dependency`.

**Result:** the module's only import is `from repositories.conversation_repository import InteractionRepository` — no Memory-related repository or model is imported or reachable. The test inspects `dir(interaction_state_assembler_module)` for any symbol containing `"memory"` (case-insensitive) — a genuine structural check of the actual import graph, not a vacuous or docstring-only assertion. Independently re-run, passes.

**Conclusion: Pass.**

### 8. Frontend vertical slice (CLAUDE.md §20.3/§20.7)

**Checked:** direct existence and content read of every named path.

**Result:** all confirmed present and real:
- `source/frontend/src/features/conversation/components/{ConversationalExperienceScreen,ConversationTurnComposer,ConversationTurnList}.tsx`, `state/useConversationManagement.ts` — all real, wired to real state machines, no TODO/mock markers.
- `source/frontend/src/services/conversation-api.ts` — calls `apiClient.post`/`apiClient.get` against `appConfig.aiServiceUrl` for all four endpoints; no mocked response.
- `source/frontend/src/types/conversation.ts` — field-for-field identical to `schemas/conversation.py` (`ConversationResponse`, `ExecuteInteractionRequest`, `InteractionResponse`, `InteractionListResponse`), confirmed by direct side-by-side read.
- `source/frontend/src/config/admin-navigation.ts` — new `ai-conversation` entry present (`href: "/platform-admin/ai-conversation"`).
- `source/frontend/src/app/platform-admin/(workspace)/ai-conversation/page.tsx` — real route, renders `ConversationalExperienceScreen`.

**Conclusion: Pass.**

### 9. Progressive Disclosure / Evidence Panel contract conformance (IMP-FE-004, SD-001-020/021)

**Checked:** direct read of `ProgressiveDisclosure.tsx` and `EvidencePanel.tsx`, and `IMP-001 §10.3` (`IMP-FE-004`)'s own wording.

**Result:** `ProgressiveDisclosureProps` declares `summary`, `details`, `evidence`, `auditHistory` all as required (non-optional) `ReactNode` props — matching `IMP-FE-004`'s own text exactly ("four distinct render states ... as a required prop interface ... not ... an ad-hoc pattern"; "a widget missing one of the four states is an incomplete implementation"). `EvidencePanel` imports and renders `<ProgressiveDisclosure summary={...} details={...} evidence={...} auditHistory={...} />` — genuine composition, not a reimplementation of tab/level state.

**Conclusion: Pass.**

### 10. Implementation Quality Baseline states (CLAUDE.md §20.6)

**Checked:** direct read of the actual JSX conditionals, not the report's claim.

**Result:** loading (`LoadingState` while `establishing`/`idle` in `ConversationalExperienceScreen`; `LoadingState` while `idle`/`loading` in `ConversationTurnList`), empty (`ConversationTurnList`'s explicit "No turns yet" message for a genuinely empty `interactions` array, not a fabricated result), validation (`ConversationTurnComposer`'s client-side empty-input check before submit, `invalid`/`FormError` wiring), error (`FormBanner tone="danger"` on `conversationState.status === "error"` and `executeState.status === "execute-error"`), confirmation (`FormBanner tone="success"` on `executed`, `notify("Conversation closed.", "success")` on close) — all against real state produced by real API calls, no hardcoded demonstration data.

**Conclusion: Pass.**

### 11. Frontend build

**Checked:** independently ran (after `npm install`, since `node_modules` was absent):
```
npx tsc --noEmit         → clean, zero errors/output
npx eslint <every new/changed WP-12 file>  → exit code 0, clean
npx next build           → "✓ Compiled successfully", 39/39 routes generated,
                            /platform-admin/ai-conversation present in the route list
```
**Conclusion: Pass.**

### 12. Technical Debt Register integrity (TD-129–TD-133)

**Checked:** direct read of each entry against what the code actually does.

**Result:** `TD-129` (PLATFORM_ADMIN-only write gate) — accurate, matches §4 above. `TD-130` (Progressive Disclosure/Evidence Panel narrow scope) — accurate; both components are genuinely built to the general `IMP-FE-004` contract (§9 above), not feature-locked in a way that would block a future rollout. `TD-131` (no streaming) — accurate, matches `TDS-012 §6`'s own disclosed one-turn-per-Interaction choice. `TD-132` (no Memory compaction, unbounded prior turns) — accurate; see also the note under "Additional Findings," Finding D below. `TD-133` (no real Reasoning Engine wired, 100% of BA-02 executions are a disclosed placeholder) — accurate and honestly stated; rated Medium, and independently judged **not** a `§19.8.5`-class "broken functionality" defect, because the placeholder is loudly disclosed to the caller (`output_reference` states its own placeholder nature; `confidence_score` is `None`, never fabricated) rather than silently masquerading as a real answer — the same distinguishing test `CLAUDE.md §19.8.7`'s own `TD-070` example applies (silent no-op vs. disclosed non-op). None of the five entries is a security, tenant-isolation, or data-integrity defect, a failing test, or a build failure in disguise.

**Conclusion: Pass**, with one caveat: this register is **incomplete** — see Findings A and B below, neither of which is currently recorded anywhere in `TECH-DEBT.md`.

### 13. Repository cleanliness

**Checked:** `git status --short` (clean, working tree matches `master` at `79d8bca`) and `git show --stat` on each of the four commits.

**Result:** `86af6e6` touches only `IRA-012`/`TDS-012` (2 files). `fd69366` touches only 13 backend files plus `TECH-DEBT.md` (14 files, 1301 insertions / 7 deletions — the 7 deletions are the `middleware/tenant.py` bypass-list edit). `2a07427` touches only 10 frontend files. `79d8bca` touches only `IMP-REPORT-WP-12_AI_Conversation_Management.md`. No unrelated repository content (`Backend/Runtime/`, `design/`, `historical-ui-tree.txt`, or any other concurrent working-tree material visible in the session's own `git status` snapshot at task start) was swept into any of the four commits.

**Conclusion: Pass.**

---

## Additional Findings (Beyond the 13-Point Checklist)

Discovered through direct TDS-012-vs-implementation comparison, not called out by the Implementation Report.

### Finding A (Medium) — `ExperienceCompositionResolver`/`ExistingContractRegistry` were never implemented, and the TDS-012 §9 test committed against them was never built

`TDS-012 §3`'s own "Backend Services and Repositories" table lists `ExperienceCompositionResolver` ("Resolves which existing `SD-001` contracts ... compose a given Interaction's own output for presentation," backed by `ExistingContractRegistry`) as a component of this Work Package, owned by `AIService`. `TDS-012 §9`'s Testing Strategy explicitly commits: "`ExperienceCompositionResolver` verified to never resolve by hardcoded capability identity." Neither class exists anywhere in the repository (confirmed by direct inspection of the backend commit's file list and a repository-wide check for the symbol names), and no such test exists in `tests/test_conversation.py`.

In practice, the Evidence Panel/Progressive Disclosure composition is instead performed directly and statically in the frontend (`ConversationTurnList.tsx` unconditionally renders `<EvidencePanel .../>` for every `COMPLETE` Interaction) — a reasonable, working outcome for a first, single-consumer implementation, and not a security or correctness defect. But it is an **undisclosed** deviation from the approved Technical Design: `IRA-012 §4.5`/`§4.6` and `TDS-012 §10` each explicitly enumerate what is excluded from this Work Package's scope, and this component is not among them; `IMP-REPORT-WP-12` does not mention `ExperienceCompositionResolver`, `ExistingContractRegistry`, or the dropped test at all. Per `CLAUDE.md §19.5`'s own discipline ("what it deliberately excludes is disclosed, not hidden"), this scope reduction should have been named and either justified as out-of-scope or recorded as new Technical Debt — it was silently dropped instead.

**Recommendation:** record as new Technical Debt before Gate 2, or build the minimal resolver TDS-012 committed to.

### Finding B (Medium) — `TDS-012 §9`'s committed concurrency probe for `UNIQUE(conversation_id, sequence_number)` was never built, and the underlying race condition is plausible and unhandled

`TDS-012 §9` explicitly commits: "`UNIQUE(conversation_id, sequence_number)` concurrency probe (mirroring `TD-128`'s own recommended follow-up, built in from the start here rather than retrofitted)." A direct grep of `tests/test_conversation.py` for `concurrent`/`gather`/`race` returns zero matches — no such probe exists.

Direct code read of `services/interaction_service.py::execute()` shows `sequence_number = await self.interaction_repo.next_sequence_number(conversation_id)` (a `SELECT MAX(sequence_number)+1`) followed by a separate `create_pending()` insert, with **no** surrounding `try`/`except` — unlike the `complete()` call three lines later, which *is* wrapped. Two concurrent `execute_interaction` calls against the same `Conversation` could both read the same `next_sequence_number()` result before either commits its insert; the second insert would then violate `uq_interaction_registry_conversation_sequence` and raise an unhandled `IntegrityError`, surfacing as an uncaught `500` rather than a graceful `409`/retry. This is exactly the scenario the committed-but-undelivered concurrency probe exists to catch.

**Recommendation:** record as new Technical Debt before Gate 2; the V&V Audit (Gate 2) should include a purpose-built concurrent-request probe against this exact path, per `CLAUDE.md §19.7b`'s own method requirement for empirical, from-scratch probing.

### Finding C (Low) — see Point 2 above (`confidence_score` schema type deviation, `NUMERIC` vs. `Integer`).

### Finding D (Low, informative) — `InteractionStateAssembler`'s prior-turn accumulation is unbounded, in tension with `RTA-001 §13.15a`'s "never an unbounded transcript" wording

`RTA-001 §13.15a` states Interaction State exists as "structured runtime context — never an unbounded transcript." `InteractionStateAssembler.assemble()` accumulates every `COMPLETE` prior Interaction's full `input_reference`/`output_reference` into `prior_inputs`/`prior_outputs` lists with no cap, window, or summarization. This is already disclosed and tracked as `TD-132` ("no compaction/summarization strategy... grow unbounded") — not a new gap — but it is worth stating explicitly for the record that the growth pattern is in literal tension with the constitutional phrase, not merely a future performance concern. No action required beyond `TD-132`'s own existing tracking.

---

## Recommendation

**Proceed to Gate 2 (V&V Audit)**, with Findings A and B carried forward as explicit line items for that gate's own broader mandate — specifically, Gate 2 should (i) confirm both are recorded as new `TECH-DEBT.md` entries (or remediated) before this Work Package's own certified status is treated as final, and (ii) include the purpose-built concurrency probe `CLAUDE.md §19.7b`'s own method requirement calls for, targeting Finding B directly (not adapted from the existing test suite). Neither finding is `§19.8.5`-class (no security, tenant-isolation, or data-integrity defect; no failing test; no build failure; the disclosed placeholder behavior of `TD-133` is honestly surfaced, not broken functionality) and neither blocks this Gate.

All other aspects of this Work Package — schema conformance (one Low-severity type deviation aside), API contract conformance, `PLATFORM_ADMIN` authorization gating, audit wiring, the Mandatory Tenant-Isolation Test Checklist (exceeding its minimum scope), the structural Memory exclusion, the frontend vertical slice and its real API integration, the first conforming Progressive Disclosure/Evidence Panel implementation, all five `CLAUDE.md §20.6` states, backend/frontend test and build results, and commit-boundary cleanliness — are independently confirmed sound and require no rework.

---

*End of CERT-WP-12. Gate 2 (V&V Audit) may proceed on the current code, carrying Findings A and B forward per the Recommendation above.*
