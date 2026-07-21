# Technical Debt Register

**Governing rule:** CLAUDE.md §19.8 (Technical Debt Management)
**Scope:** Repository-wide — not scoped to a single Work Package or Business Activity.

---

## Purpose

This register captures non-blocking engineering observations raised during Independent Review that:

- do not justify failing Independent Review,
- do not require an Architecture Decision Record (ADR),
- do not require immediate remediation,
- are intentionally deferred to a future Business Activity, Work Package, or release.

Per CLAUDE.md §19.8.2, Technical Debt SHALL NOT exist solely within Independent Review reports, implementation reports, commit messages, or chat history — it is recorded here.

Per CLAUDE.md §19.8.3, once an item is recorded here, future Independent Reviews reference its ID instead of repeating the full observation, e.g.:

> Observation: Tracked as TD-001. No additional discussion required.

Per CLAUDE.md §19.8.5, Technical Debt SHALL NOT be used to defer architectural, security, data integrity, or tenant-isolation defects, failing tests, build failures, broken functionality, or mandatory compliance requirements. Every item below was accepted through Independent Review as non-blocking before being recorded.

---

## Register

| ID | Description | Raised In | Category | Priority | Planned Resolution | Status | Owner |
|---|---|---|---|---|---|---|---|
| TD-001 | Add a dedicated `TenantMiddleware` test asserting the `/organizations/*` prefix-match behavior directly (currently only exercised incidentally via each endpoint's own tests). | BA-02 | Testing | Low | BA-05 (resolved: `tests/test_tenant_middleware.py`) | Closed | AuthService (Backend) |
| TD-002 | Add a test asserting `updated_at` actually advances after `PUT /organizations/{id}` (Update Organization Profile). | BA-04 | Testing | Low | WP-01 Closure | Open | AuthService (Backend) |
| TD-003 | Evaluate optimistic concurrency support (e.g. a version/`ETag` field) for Organization writes — current behavior is last-write-wins on concurrent updates, undocumented as a formal decision. | BA-04 | Concurrency | Medium | WP-02 | Open | AuthService (Backend) |
| TD-004 | `ck_organizations_status` CHECK constraint exists in the Alembic migration but is not declared on the ORM model (`models/organization.py`) — model/migration drift; no test exercises the constraint directly. | BA-01 | Data Integrity | Low | WP-01 Closure | Open | AuthService (Backend) |
| TD-005 | Add a dedicated test for the concurrent-duplicate-`organization_code` race branch (the `IntegrityError` handler in `OrganizationService.establish()`) — currently only the sequential pre-check path is tested. | BA-01 | Testing | Low | WP-01 Closure | Open | AuthService (Backend) |
| TD-006 | Audit/event emission in `OrganizationService.establish()` happens after `session.flush()` but before the outer transaction commits — a post-flush commit failure would emit a false-success audit/event signal. Low severity given the interim, log-only observability mechanism. | BA-01 | Observability | Low | WP-01 Closure | Open | AuthService (Backend) |
| TD-007 | `useSearchOrganizations.ts` re-fetches on every keystroke with no debounce and no `AbortController`/staleness guard — an out-of-order network response could briefly overwrite the grid with stale results. | BA-03 | Concurrency | Low | Future frontend hardening pass (not addressed in BA-05, which was scoped backend-only) | Open | Platform Admin (Frontend) |
| TD-008 | Search/List's `SUSPENDED` status-filter tests only assert an empty result set (no Activate/Suspend Business Activity yet produces a `SUSPENDED` row) — true inclusion/exclusion against a mixed-status dataset is not yet provable. | BA-03 | Testing | Low | BA-05 / BA-06 (resolved: `test_search_status_filter_correctly_includes_and_excludes_mixed_statuses` and `test_search_organizations_status_filter_includes_and_excludes_mixed_statuses`) | Closed | AuthService (Backend) |
| TD-009 | The Organization Management grid fully remounts (`key={gridRefreshKey}`) after a successful Create or Update, resetting the user's active search text/status filter/sort/page instead of preserving them. | BA-03 | UX | Low | Future UX polish pass | Open | Platform Admin (Frontend) |
| TD-010 | The AuthService backend test suite requires `JWT_SECRET_KEY`/`JWT_ALGORITHM` set out-of-band with no fixture or `.env.example` documenting it, tripping up fresh reviewers and CI runs. | BA-01 | Developer Experience | Low | WP-01 Closure | Open | AuthService (Backend) |
| TD-011 | `organization_code`/lifecycle-`status` immutability on Update Organization Profile rests entirely on `OrganizationService.update_profile()`'s explicit field whitelist — `BaseRepository.update()` itself has no allowlist and will `setattr` whatever keys it is given. Safe today; a latent risk if `update_profile()` is ever refactored to pass a full `model_dump()`. | BA-04 | Maintainability | Low | Revisit if `BaseRepository.update()` is refactored, or at WP-01 Closure | Open | AuthService (Backend) |
| TD-012 | `Organization.is_active` (legacy WP-00 boolean column) is never updated by any lifecycle transition — `establish()` leaves it at its `True` default and `activate()` only touches `status`. Once BA-06 Suspend lands and sets `status="SUSPENDED"`, `is_active` will silently keep reading `True` for a suspended organization, a real (not hypothetical) data inconsistency between two columns that both claim to represent lifecycle state. | BA-05 | Data Integrity | Medium | BA-06 (resolved: `suspend()`/`activate()` now sync `is_active` to `False`/`True` alongside `status`; see `test_suspend_and_activate_keep_is_active_in_sync_with_status` and `test_suspend_then_activate_round_trip_keeps_is_active_in_sync`) | Closed | AuthService (Backend) |

---

## Maintenance

- New entries are appended with the next sequential `TD-NNN` ID.
- When an item is resolved, update its `Status` to `Closed` and record the resolving Business Activity or Work Package in `Planned Resolution` (do not delete closed rows — they remain part of the audit trail).
- This register is reviewed and updated during Independent Review of any Business Activity that touches an area with an open, related entry.
