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
| TD-004 | `ck_organizations_status` CHECK constraint exists in the Alembic migration but is not declared on the ORM model (`models/organization.py`) — model/migration drift; no test exercises the constraint directly. | BA-01 | Data Integrity | Low | BA-07 (resolved: constraint declared on the model via `__table_args__`, widened to include `RETIRED` in lockstep with the Alembic migration `d2d840d224b6`) | Closed | AuthService (Backend) |
| TD-005 | Add a dedicated test for the concurrent-duplicate-`organization_code` race branch (the `IntegrityError` handler in `OrganizationService.establish()`) — currently only the sequential pre-check path is tested. | BA-01 | Testing | Low | WP-01 Closure | Open | AuthService (Backend) |
| TD-006 | Audit/event emission in `OrganizationService.establish()` happens after `session.flush()` but before the outer transaction commits — a post-flush commit failure would emit a false-success audit/event signal. Low severity given the interim, log-only observability mechanism. | BA-01 | Observability | Low | WP-01 Closure | Open | AuthService (Backend) |
| TD-007 | `useSearchOrganizations.ts` re-fetches on every keystroke with no debounce and no `AbortController`/staleness guard — an out-of-order network response could briefly overwrite the grid with stale results. | BA-03 | Concurrency | Low | Future frontend hardening pass (not addressed in BA-05, which was scoped backend-only) | Open | Platform Admin (Frontend) |
| TD-008 | Search/List's `SUSPENDED` status-filter tests only assert an empty result set (no Activate/Suspend Business Activity yet produces a `SUSPENDED` row) — true inclusion/exclusion against a mixed-status dataset is not yet provable. | BA-03 | Testing | Low | BA-05 / BA-06 (resolved: `test_search_status_filter_correctly_includes_and_excludes_mixed_statuses` and `test_search_organizations_status_filter_includes_and_excludes_mixed_statuses`) | Closed | AuthService (Backend) |
| TD-009 | The Organization Management grid fully remounts (`key={gridRefreshKey}`) after a successful Create or Update, resetting the user's active search text/status filter/sort/page instead of preserving them. | BA-03 | UX | Low | Future UX polish pass | Open | Platform Admin (Frontend) |
| TD-010 | The AuthService backend test suite requires `JWT_SECRET_KEY`/`JWT_ALGORITHM` set out-of-band with no fixture or `.env.example` documenting it, tripping up fresh reviewers and CI runs. | BA-01 | Developer Experience | Low | WP-01 Closure | Open | AuthService (Backend) |
| TD-011 | `organization_code`/lifecycle-`status` immutability on Update Organization Profile rests entirely on `OrganizationService.update_profile()`'s explicit field whitelist — `BaseRepository.update()` itself has no allowlist and will `setattr` whatever keys it is given. Safe today; a latent risk if `update_profile()` is ever refactored to pass a full `model_dump()`. | BA-04 | Maintainability | Low | Revisit if `BaseRepository.update()` is refactored, or at WP-01 Closure | Open | AuthService (Backend) |
| TD-012 | `Organization.is_active` (legacy WP-00 boolean column) is never updated by any lifecycle transition — `establish()` leaves it at its `True` default and `activate()` only touches `status`. Once BA-06 Suspend lands and sets `status="SUSPENDED"`, `is_active` will silently keep reading `True` for a suspended organization, a real (not hypothetical) data inconsistency between two columns that both claim to represent lifecycle state. | BA-05 | Data Integrity | Medium | BA-06 (resolved: `suspend()`/`activate()` now sync `is_active` to `False`/`True` alongside `status`; see `test_suspend_and_activate_keep_is_active_in_sync_with_status` and `test_suspend_then_activate_round_trip_keeps_is_active_in_sync`) | Closed | AuthService (Backend) |
| TD-013 | `OrganizationService.update_profile()` (Steward Organization Identity, BA-04) has no status check — it allows updating profile fields regardless of current lifecycle state. PE-001-C004's ERB-C004-05 Entry Context requires "Authoritative Organization Context in **ACTIVE** state" for identity stewardship — a `SUSPENDED` or `RETIRED` organization's profile should not be steward-updatable. Discovered while implementing BA-07's Entry Context checks; not fixed here because it is a behavior change to BA-04's already-accepted, already-independently-reviewed code, out of BA-07's scope. | BA-07 | Data Integrity | Medium | Future BA or WP-01 Closure — requires its own review since it changes already-shipped `PUT /organizations/{id}` behavior | Open | AuthService (Backend) |
| TD-014 | PE-001-C004's ERB-C004-07 describes an optional Organization Continuity Context linking a retired Organization to a successor (EX-C004-13), plus a persisted retirement reason/responsible-authority record. Neither is implemented — no successor-organization relationship exists anywhere in the schema, and the reason/authority is only captured at the same audit-metadata level of rigor as every other lifecycle transition (BA-05/BA-06), not a queryable, durable field. A deliberate, minimal-scope decision consistent with ADR-004's incremental-implementation philosophy, not an oversight. | BA-07 | Data Integrity | Low | Future WP — no successor-organization concept exists yet anywhere to attach a continuity link to | Open | AuthService (Backend) |
| TD-015 | Frontend `types/organization.ts`'s `OrganizationStatus` union (`"ACTIVE" \| "SUSPENDED"`) and `OrganizationSearchGrid.tsx`'s `StatusBadge` tone logic (`status === "ACTIVE" ? "success" : "warning"`) do not recognize the new `RETIRED` value — a retired organization would display with the same "warning" tone as `SUSPENDED`, not a distinct visual treatment. Not fixed here — BA-07 was scoped backend-only, same precedent as BA-05/BA-06. | BA-07 | UX | Low | When Organization Management's frontend is next extended (e.g. alongside the Action Center UI recommendation already carried from BA-06's review) | Open | Platform Admin (Frontend) |
| TD-016 | `services/auth_service.py`'s login/organization-selection flow (`authenticate_user()`) never checks `Organization.status` at all — only `Membership.is_active` is consulted. A person holding an active Membership can still select and authenticate into a `SUSPENDED` or `RETIRED` organization's context; nothing blocks it. Discovered during BA-07's post-implementation Enterprise Lifecycle Consistency Check (full-codebase search for every `Organization`/status consumer outside the Organization Management module). Pre-existing since `SUSPENDED` was introduced (BA-06) — not a new consequence of `RETIRED` specifically — but only surfaced by this check. Cross-cuts AuthService's login flow and Membership/Role & Permission Management, both explicitly excluded from WP-01's scope per IRA-001; not fixed as part of BA-07. | BA-07 (Enterprise Lifecycle Consistency Check) | Security | Medium | Role & Permission Management or Membership Management work package, or a dedicated cross-service hardening pass — requires changes to AuthService's login flow, outside WP-01's declared boundary | Open | AuthService (Backend) |
| TD-017 | `OrganizationRepository.get_by_code()` has no status filter, so `establish()`'s duplicate-code check correctly rejects reusing a `RETIRED` organization's `organization_code` for a new organization — architecturally correct continuity behavior — but no test in either test file exercises this scenario. Discovered during BA-07's Independent Review. Low risk since the code path itself is correct, but a future refactor of `get_by_code()`/`establish()` could silently reintroduce a reuse bug with nothing to catch it. | BA-07 (Independent Review) | Testing | Low | WP-01 Closure — e.g. `test_establish_rejects_reusing_a_retired_organizations_code` | Open | AuthService (Backend) |
| TD-018 | `record_audit()` is called before `publish_event()` in every write-path Business Activity (`establish()`, `update_profile()`, `activate()`, `suspend()`, `retire()`), while IMP-001 §6.3 states the canonical Business Activity Lifecycle order as Business Object Update → **Domain Event Publication → Audit Recording** — the implemented order is reversed. Inherited unchanged since BA-01; flagged as a non-blocking observation at BA-05's Independent Review and again at BA-06's ("now spans 4+ Business Activities and is growing"), but never previously given its own tracked register entry — found to exist only in review-report prose during BA-07's Independent Review audit of this register, in violation of CLAUDE.md §19.8.2. Needs a single reconciling decision: either amend IMP-001 §6.3 to reflect the actually-implemented and already-accepted order, or reorder the code to match the documented order. | BA-05 (first flagged; formally registered after BA-07's audit) | Observability | Low | WP-01 Closure (single reconciling decision) | Open | AuthService (Backend) |
| TD-019 | No "Action Center" UI (or equivalent) has been built for any of Organization Management's three lifecycle actions (Reactivate, Suspend, Retire) — all three remain backend-only, callable only via direct API. IRA-001 §5's UI Impact Matrix named "Action Center" as a DS-001 pattern not yet built; deferring it was reasonable while only one lifecycle action existed (BA-05), but BA-06's Independent Review noted the justification weakens once multiple actions exist and recommended explicitly scheduling this UI before WP-01 closure rather than continuing to implicitly re-defer it BA-by-BA. Distinct from TD-015 (which is narrower — only about `RETIRED` not rendering with a distinct `StatusBadge` tone in the existing Search grid). Never previously given its own tracked register entry — same §19.8.2 gap as TD-018. | BA-05 (deferral first noted); BA-06 (scheduling recommended); formally registered after BA-07's audit | UX | Low | Before WP-01 Closure, or an explicit deferral decision to WP-02 if not built by then | Open | Platform Admin (Frontend) |
| TD-020 | `activate()`, `suspend()`, and `retire()` are three near-identical copy-paste-with-reversal methods (404 → status guard(s) → mutate → audit → event), differing only in target status/audit-action-name/event-name. BA-06's Independent Review judged a shared `_transition()` helper "a reasonable candidate only if a third lifecycle transition is ever added" — BA-07's `retire()` is that third transition, meeting the stated condition, but no refactor was performed and this was not revisited at BA-07's own Independent Review. Not a defect: three call sites of a well-understood, consistently-tested pattern remain independently readable and auditable. Never previously given its own tracked register entry — same §19.8.2 gap as TD-018/TD-019. | BA-06 (conditional recommendation); condition met at BA-07; formally registered after BA-07's audit | Maintainability | Low | WP-01 Closure, or if a fourth lifecycle transition is ever added | Open | AuthService (Backend) |
| TD-021 | BA-01 (Establish Business or System Role, WP-02/C-003) gates both Business Role and System Role establishment on the existing `PLATFORM_ADMIN` role claim only — PE-001-C003's BR-C003-08 requires confirmed, type-specific defining authority (Corporate Admin for Business Roles; Security Admin or User Admin for System Roles), none of which exist as distinct, enforceable claims today. Disclosed and reasoned in `dependencies.require_platform_admin`'s docstring, IRA-001 §2.7, and IRA-002 §2.7/§4; never previously given its own tracked register entry — same §19.8.2 gap as TD-018/TD-019/TD-020, this time found directly by BA-01's Independent Review rather than a self-audit. See detailed entry below the table for full fields. | BA-01 (Independent Review) | Security | Low | ADR-002 acceptance, followed by persona-specific authorization dependencies (WP-02, future Business Activity) | Open | AuthService (Backend) |
| TD-022 | BA-02 (Establish Domain Permission, WP-02/C-003) gates establishment on the existing `PLATFORM_ADMIN` role claim only — PE-001-C003's EX-C003-02 requires confirmed Domain Owner or Domain Admin authority (URA-001-45/46) for the target Domain, and no such relationship exists anywhere in the schema (Domain, AMD-014, was deliberately built as ownership-free reference data). Disclosed in `DomainPermissionService.establish()`'s module docstring and the router/OpenAPI descriptions; same class of gap as TD-021, found directly by BA-02's Independent Review. See detailed entry below the table for full fields. | BA-02 (Independent Review) | Security | Low | A Domain Owner/Domain Admin authority model (future, separately-scoped Business Activity or architecture amendment), followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for this endpoint | Open | AuthService (Backend) |
| TD-023 | BA-03 (Establish Approval Authority, WP-02/C-003) gates establishment on the existing `PLATFORM_ADMIN` role claim only — PE-001-C003's EX-C003-03 requires confirmed Corporate Admin (URA-001-32) or Domain Owner (URA-001-45) authority, and neither exists as a distinct, enforceable claim today (Corporate Admin: same ADR-002 catalog-mismatch gap as TD-021; Domain Owner: same Domain-is-ownership-free gap as TD-022). Disclosed in `ApprovalAuthorityService.establish()`'s module docstring and the router/OpenAPI descriptions; same class of gap as TD-021/TD-022, found directly by BA-03's Independent Review. See detailed entry below the table for full fields. | BA-03 (Independent Review) | Security | Low | ADR-002 acceptance and/or a Domain Owner/Domain Admin authority model (future, separately-scoped Business Activity or architecture amendment), followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for this endpoint | Open | AuthService (Backend) |
| TD-024 | BA-04 (Establish Delegation Policy, WP-02/C-003) gates establishment on the existing `PLATFORM_ADMIN` role claim only — PE-001-C003's EX-C003-04 requires confirmed Corporate Admin (URA-001-32) or Domain Owner (URA-001-45) authority, and neither exists as a distinct, enforceable claim today — the same two already-tracked root causes as TD-021 (ADR-002 catalog mismatch) and TD-022 (Domain-is-ownership-free). Disclosed in `DelegationPolicyService.establish()`'s module docstring and the router/OpenAPI descriptions; same class of gap as TD-021/TD-022/TD-023, found directly by BA-04's Independent Review. See detailed entry below the table for full fields. | BA-04 (Independent Review) | Security | Low | ADR-002 acceptance and/or a Domain Owner/Domain Admin authority model (future, separately-scoped Business Activity or architecture amendment), followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for this endpoint | Open | AuthService (Backend) |
| TD-025 | BA-05 (Establish Runtime Assignment Policy, WP-02/C-003) gates establishment on the existing `PLATFORM_ADMIN` role claim only — PE-001-C003's EX-C003-05 requires confirmed Corporate Admin (URA-001-32) or Domain Admin authority, and neither exists as a distinct, enforceable claim today — the same two already-tracked root causes as TD-021 (ADR-002 catalog mismatch) and TD-022 (Domain-is-ownership-free). Disclosed in `RuntimeAssignmentPolicyService.establish()`'s module docstring and the router/OpenAPI descriptions; same class of gap as TD-021/TD-022/TD-023/TD-024, found directly by BA-05's Independent Review. See detailed entry below the table for full fields. | BA-05 (Independent Review) | Security | Low | ADR-002 acceptance and/or a Domain Owner/Domain Admin authority model (future, separately-scoped Business Activity or architecture amendment), followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for this endpoint | Open | AuthService (Backend) |
| TD-026 | BA-07 (Version and Re-effective-Date Authorization Policy Object, WP-02/C-003) implements SD-002-011's Approval Reference property as a nullable, free-text column on all five authorization policy objects, never validated against a real Approval Authority record or workflow. This is a deliberate simplification, not an oversight: C-003 itself must never execute an approval workflow (Contract 5.3, Runtime Execution Boundary), and no runtime mechanism exists anywhere in this codebase to resolve/execute an Approval Authority's own approval_strategy against a specific decision — that remains C-002/RTA-001 §11's exclusive concern, not yet built. Validating approval_reference against a real record would require inventing that missing runtime mechanism, which is out of BA-07's scope. | BA-07 | Data Integrity | Low | A future Approval Authority resolution/execution capability (C-002/RTA-001 §11, not yet scoped), after which approval_reference could be validated against a real, resolved approval outcome | Open | AuthService (Backend) |
| TD-027 | BA-07's `create_new_version()` has no protection against a concurrent double-amendment race for four of the five object types (Domain Permission, Approval Authority, Delegation Policy, Runtime Assignment Policy) — two concurrent requests against the same target id could both read the same ACTIVE row and both successfully insert a new ACTIVE row, leaving two ACTIVE versions coexisting for one policy chain. Role's own equivalent race is closed (its `role_code`-scoped partial unique index rejects the second concurrent insert, caught as a clean 409), but no comparable natural-key constraint exists on the other four tables to catch the same race. Found directly by BA-07's Independent Review, not self-identified. Low likelihood given every write path is PLATFORM_ADMIN-gated, low-traffic, and administrative. | BA-07 (Independent Review) | Data Integrity | Low | Add a per-type mechanism (e.g., a partial unique index on (organization_id or anchor column, status='ACTIVE') mirroring Role's own fix, or optimistic-locking on the superseded row) for the remaining four types | Open | AuthService (Backend) |
| TD-028 | BA-08's `has_active_dependents()` pre-retirement dependency check (BR-C003-04) is real only for Role, which queries the AuthService-implemented `memberships` table. For the other four object types (Domain Permission, Approval Authority, Delegation Policy, Runtime Assignment Policy), the check always returns `False` — not because no dependency exists, but because each type's real canonical dependent (`membership_approval_authority`, `delegation_registry`, `runtime_assignment_registry`; Domain Permission has no dependent at all in this schema) is not yet implemented in AuthService, the same already-tracked root cause as TD-023/TD-024/TD-025/TD-027. Retirement of these four types therefore always passes this specific check today, regardless of real-world usage. | BA-08 | Data Integrity | Medium | Implement each missing dependent table in AuthService, then extend the corresponding `has_active_dependents()` to a real query, mirroring RoleRepository's own implementation | Open | AuthService (Backend) |
| TD-029 | BA-08's `deprecate()`/`retire()` each require the target object's current status to be exactly ACTIVE, for all five object types. Consequence: once an object is moved to DEPRECATED, no existing code path can ever move it to RETIRED (or back to ACTIVE) — it is permanently stuck in the Hidden state pending a future Restore Business Activity. Neither EX-C003-08 nor BR-C003-04 mandates or forbids a DEPRECATED → RETIRED transition; this is an implementation choice (deprecate/retire modeled as two independent branches from ACTIVE, not a chain), not a contract violation, but it diverges from the WP-01 precedent this Business Activity otherwise mirrors closely (`OrganizationService.retire()` accepts entry from ACTIVE **or** SUSPENDED). Found directly by BA-08's Independent Review. | BA-08 (Independent Review) | Data Integrity | Low | Decide, at BA-09/Restore scoping time, whether DEPRECATED → RETIRED should become a legal transition (mirroring OrganizationService.retire()'s own SUSPENDED-or-ACTIVE entry) or remains intentionally excluded | Open | AuthService (Backend) |
| TD-030 | BA-09's `resolve_conflict()` records an ACCEPTED_BREAK resolution purely as an audit-trail statement (Contract 5.6's own "affirmative accepted break stated by the proposing authority") — it does not itself flip BA-08's `has_active_dependents()` to False, because doing so would require either writing to the dependent's own table (crossing Contract 5.1's C-007 boundary for Membership) or introducing a new "accepted break" persisted flag BA-08's own check would need to consult (which would mean modifying BA-08's already-shipped code, out of this Business Activity's scope). Consequence: after an ACCEPTED_BREAK resolution, a subsequent call to BA-08's deprecate()/retire() for the same object is still blocked by the same dependent, until it naturally resolves (expires) or is genuinely reassigned via the dependent's own capability. EX-C003-09's own promise of "a cleared path for ERB-C003-02 to proceed" is therefore only fully realized for REASSIGNMENT_CONFIRMED/NATURAL_EXPIRY_CONFIRMED resolutions where the underlying data has genuinely changed — not yet for ACCEPTED_BREAK. | BA-09 | Data Integrity | Medium | Design a mechanism (e.g., a short-lived accepted-break record BA-08's own check consults) that lets an explicit ACCEPTED_BREAK resolution actually clear BA-08's gate, without BA-09 writing to any C-007-owned table | Open | AuthService (Backend) |
| TD-031 | BA-01 (Establish Membership Context, WP-03/C-007) gates establishment on the existing `PLATFORM_ADMIN` role claim only — PE-001-C007's EX-C007-02 names Membership Steward/Membership Sponsor as its Participating Personas, neither of which exists as a distinct, enforceable claim today. Same class of gap as TD-021 through TD-025, found directly by BA-01's Independent Review. See detailed entry below the table for full fields. | BA-01 (Independent Review) | Security | Low | A Membership Steward/Sponsor persona authority model (future, separately-scoped Business Activity or architecture amendment), followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for this endpoint | Open | AuthService (Backend) |
| TD-032 | `Membership.home_node_id` (BA-01, WP-03/C-007) is nullable, though URA-001-17b/ERG-001-03 specify it NOT NULL. **Half-resolved by WP-04 BA-01** (Establish Organization Node, IRA-004): a governed write path for `organization_nodes` now exists (`POST /organization-nodes`), closing the "no establish path" half. `home_node_id`'s nullability itself has not yet been tightened or reaffirmed — remains Open for that reason. See detailed entry below the table for full fields. | BA-01 (WP-03); resolving half by WP-04 BA-01 | Data Integrity | Medium | `home_node_id` nullability to be explicitly revisited (tightened or reaffirmed) — a future, separately-scoped decision | Open | AuthService (Backend) |
| TD-033 | `EstablishMembershipRequest.role_id` is required, though PE-001-C007 states verbatim "C-007 does not assign or remove Roles or Permissions" (§1.4/1.8/5.9/5.10) — this is an inherited WP-00-era schema coupling (`memberships.role_id` is NOT NULL), not a canonical requirement of BA-01 itself. BA-01 does not resolve this tension; it discloses it. See detailed entry below the table for full fields. | BA-01 | Architecture | Low | A repository-owner/architecture governance decision on whether `memberships.role_id`'s NOT NULL constraint is relaxed, reassigned to a later Business Activity's own write path, or affirmed as a correct joint Establish-time act | Open | AuthService (Backend) |
| TD-034 | BA-02 (Understand Membership Context, WP-03/C-007) gates `GET /memberships/{id}` on the existing `PLATFORM_ADMIN` role claim only — PE-001-C007's EX-C007-03 names Membership Sponsor/Steward/Downstream Capability Consumer/Executive as its Participating Personas, none of which exists as a distinct, enforceable claim today. Same class of gap as TD-021 through TD-025/TD-031, found directly during BA-02 implementation. See detailed entry below the table for full fields. | BA-02 | Security | Low | A persona-specific authorization model covering Membership Sponsor/Steward/Downstream Capability Consumer/Executive (future, separately-scoped Business Activity or architecture amendment), followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for this endpoint | Open | AuthService (Backend) |
| TD-035 | BA-03 (Maintain Membership Terms, WP-03/C-007) gates `POST /memberships/{id}/terms` on the existing `PLATFORM_ADMIN` role claim only — PE-001-C007's EX-C007-04/EX-C007-05 name Membership Steward/Sponsor as their Participating Personas, neither of which exists as a distinct, enforceable claim today. Same class of gap as TD-021 through TD-025/TD-031/TD-034, found directly during BA-03 implementation. See detailed entry below the table for full fields. | BA-03 | Security | Low | A Membership Steward/Sponsor persona authority model (future, separately-scoped Business Activity or architecture amendment), followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for this endpoint | Open | AuthService (Backend) |
| TD-036 | BA-06 (Reactivate Membership, WP-03/C-007) gates `POST /memberships/{id}/reactivate` on the existing `PLATFORM_ADMIN` role claim only — PE-001-C007's EX-C007-08 names Membership Steward/Sponsor as its Participating Personas, neither of which exists as a distinct, enforceable claim today. Same class of gap as TD-021 through TD-025/TD-031/TD-034/TD-035, found directly during BA-06 implementation. See detailed entry below the table for full fields. | BA-06 | Security | Low | A Membership Steward/Sponsor persona authority model (future, separately-scoped Business Activity or architecture amendment), followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for this endpoint | Open | AuthService (Backend) |
| TD-037 | BA-06's `reactivate()` can never currently produce a successful outcome — PE-001-C007's Contract 5.3 and BR-C007-014 require an established canonical authority permitting a specific non-active-standing-to-ACTIVE transition before one may be applied, and none exists anywhere in this repository (the same root cause as BA-05's own BLOCKED — Governance Decision Required disposition). Every call is rejected with 409, citing Pending Canonical Binding. Not a defect — the literal, correct, complete implementation of BR-C007-014 for today's canonical state — but disclosed prominently since it is the single most consequential fact about this Business Activity's current behavior. See detailed entry below the table for full fields. | BA-06 | Architecture | Medium | A governance decision (most naturally a future ADR, mirroring ADR-005's own precedent) establishing which Membership standing transitions are permitted — the same resolution BA-05 itself is waiting on | Open | AuthService (Backend) |
| TD-038 | BA-01's `establish()` does not route an inactive existing Membership to a governed reactivation determination (EX-C007-08/BA-06) — per PE-001-C007's own §6.3 "Existing Membership found" exception text, recognition should route an inactive existing Membership to reactivation consideration rather than a blanket duplicate rejection. `establish()` currently rejects any existing Membership (active or not) uniformly with 409. Disclosed as a scope boundary versus already-shipped, already-reviewed BA-01 code — not modified here, per this repository's own discipline against revisiting an earlier Business Activity's already-accepted logic without a separately-scoped decision. See detailed entry below the table for full fields. | BA-06 | Architecture | Low | A separately-scoped Business Activity or amendment to `establish()`'s own routing logic, decided and reviewed independently of BA-06 | Open | AuthService (Backend) |
| TD-039 | BA-07 (Surface Multi-Organization Membership Awareness, WP-03/C-007) gates `GET /memberships/multi-organization-awareness` on the existing `PLATFORM_ADMIN` role claim only — PE-001-C007's EX-C007-09 names Membership Sponsor/Steward/Platform Oversight Participant as its Participating Personas, none of which exist as a distinct, enforceable claim today. Same class of gap as TD-021 through TD-025/TD-031/TD-034/TD-035/TD-036, found directly during BA-07 implementation. See detailed entry below the table for full fields. | BA-07 | Security | Low | A Membership Sponsor/Steward/Platform Oversight Participant persona authority model (future, separately-scoped Business Activity or architecture amendment), followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for this endpoint | Open | AuthService (Backend) |
| TD-040 | No explicit, named, audited cross-tenant sharing agreement mechanism exists anywhere in this repository — Contract 5.4 and URA-001-17a both name this as the sole exception path to existence-only cross-tenant Membership visibility. BA-07's `surface_multi_organization_awareness()` therefore always returns the most-restrictive, existence-only default (BR-C007-008), which is the complete, correct behavior for the only case that exists today (no agreement) — not a defect, but disclosed as a known future extension point. See detailed entry below the table for full fields. | BA-07 | Architecture | Low | A cross-tenant sharing agreement registry/model (future, separately-scoped Business Activity or architecture amendment), after which `surface_multi_organization_awareness()` could consult it before defaulting to existence-only | Open | AuthService (Backend) |
| TD-041 | BA-08 (Present Person's Own Cross-Organization Membership View, WP-03/C-007) implements only EX-C007-10's own "Membership Subject views their own portfolio" trigger. Its second Participating Persona, "Platform Oversight Participant where an authorized aggregator is involved," is not implemented — no distinct aggregator claim exists anywhere in this codebase, and standing `PLATFORM_ADMIN` in for it (the usual WP-03 interim-gate pattern) would let any platform admin read any Person's complete cross-tenant Membership detail, a materially larger exposure than any prior Business Activity permits. Deliberately excluded, not silently deferred. See detailed entry below the table for full fields. | BA-08 | Security | Medium | An authorized-aggregator persona authority model (future, separately-scoped Business Activity or architecture amendment) with its own scoped, audited authorization dependency — never a bare `PLATFORM_ADMIN` stand-in given the exposure involved | Open | AuthService (Backend) |
| TD-042 | BA-10 (Hand Off Membership Context to a Dependent Capability, WP-03/C-007) gates `POST /memberships/{id}/hand-off` on the existing `PLATFORM_ADMIN` role claim only — PE-001-C007's EX-C007-12 names Membership Steward/Downstream Capability Consumer as its Participating Personas, neither of which exists as a distinct, enforceable claim today. Additionally, two of the three dependent capabilities Contract 5.10 names — Access Management (C-002) and Workspace Management (C-008) — are registered Active in CAP-001 but have no Work Package anywhere in this repository; only C-003 (Role & Permission Management, WP-02) is real. This does not block BA-10, since C-007 never calls into any dependent capability's own API (the caller reports the outcome, mirroring WP-02 BA-10's own precedent), but is disclosed as a real gap in what "hand-off" can mean in practice for C-002/C-008 today. See detailed entry below the table for full fields. | BA-10 | Security | Low | A Membership Steward/Downstream Capability Consumer persona authority model (future, separately-scoped Business Activity or architecture amendment), followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for this endpoint; separately, C-002/C-008's own future Work Packages would let a hand-off to them mean more than a caller-reported record | Open | AuthService (Backend) |
| TD-043 | BA-01 (Establish Organization Node, WP-04/C-005) persists only the Structural Identity subset of Master Technical Architecture's canonical `organization_node` DDL (`legal_entity_name`, `business_unit`, `sector`, `operational_status`, `effective_from`, `effective_to`). `geography_id` (no `geography_registry` table exists anywhere in this repository), `parent_available_flag` (naturally derived once `organization_hierarchy` exists — BA-08's own future scope), and the materiality/risk/scenario/passport scores (`strategic_importance_score`, `risk_criticality_score`, `reporting_currency`, `benchmark_group`, `scenario_sensitive_flag`, `external_dependency_flag`, `entity_materiality_score`, `data_readiness_score`, `external_data_retrieval_flag`, `passport_shareable_flag`) are deferred — disclosed in IRA-004 §9/§11, not silently omitted. See detailed entry below the table for full fields. | BA-01 | Data Integrity | Low | Enterprise Structure Management's own later Business Activities (BA-04/BA-05/BA-08 candidates, IRA-004 §4) as each concrete need for a deferred column is identified — not invented ahead of a real consumer, mirroring WP-01 ADR-004's own precedent | Open | AuthService (Backend) |
| TD-044 | BA-01 (Establish Organization Node, WP-04/C-005) adds `operational_status` (free-text, e.g. ACTIVE/INACTIVE/DIVESTED per Master Technical Architecture's own DDL comment) as an independent column alongside the pre-existing `active_flag` (boolean, WP-03 BA-01) — the two are not reconciled into one authoritative lifecycle field. `establish()` leaves `active_flag` at its model default and accepts `operational_status` as an optional, independently-supplied value. | BA-01 | Data Integrity | Low | A future Business Activity introducing real lifecycle transitions for OrganizationNode (mirroring WP-01's activate()/suspend()/retire()) should resolve which of the two fields is authoritative, or how they stay in sync, before either is relied upon for a governed transition | Open | AuthService (Backend) |
| TD-045 | BA-02 (Understand Structural Position, WP-04/C-005) realizes only the single-node half of EX-C005-03's own Purpose ("understand surrounding structural context and position... relationships") — `GET /organization-nodes/{id}` returns one node's own Structural Identity fields only. Traversing "surrounding relationships" per ERB-C005-02 requires `organization_hierarchy`, which does not exist yet (IRA-004 §7/§9 confirm it is out of BA-01's and BA-02's own scope, real future WP-04 work). Same disclosed-scoping-decision class as TD-043. See detailed entry below the table for full fields. | BA-02 | Architecture | Low | Enterprise Structure Management's own later Business Activity that introduces `organization_hierarchy` (BA-08 candidate per IRA-004 §4) — not invented ahead of a real consumer, mirroring TD-043's own precedent | Open | AuthService (Backend) |
| TD-046 | BA-01B (Verify Organization Domain Claim, WP-01A/C-004, IRA-001A) records a verification *decision* (`verified: bool`, caller-supplied) as a distinct, audited, traceable act, but has no real proof-of-control mechanism (DNS TXT record, email token, etc.) behind it — the decision is trusted as reported, not independently confirmed. PE-001-C004's own governed no-domain activation path licenses proceeding without real domain verification entirely, so no WP-01A Business Activity requires one to reach Fully Implemented constitutional status; disclosed, not silently omitted. See detailed entry below the table for full fields. | BA-01B | Security | Low | A real proof-of-control mechanism (future, separately-scoped Business Activity) once a genuine domain-trust consumer exists (e.g. C-001/URA-001 SSO domain-based provisioning) | Open | AuthService (Backend) |
| TD-047 | `MembershipService.establish()` (WP-03/C-007, pre-existing since 2026-07-29, not introduced by IRA-001A) derives Organization existence via direct `organization_repo.get_by_id()` repository access, bypassing any C-004-owned resolution authority (BR-C004-03: "Organization existence and validity SHALL be resolved exclusively through EX-C004-05; no dependent capability SHALL derive it independently"). No `.status` check is applied either, so a SUSPENDED or RETIRED organization is equally consumable. Out of IRA-001A's own ownership (C-004, not C-007) — `membership_service.py` was not modified by this correction. See detailed entry below the table for full fields. | IRA-001A (found during WP-01's own constitutional-correction review; not a WP-01A defect, a WP-03 one) | Security | Medium | A WP-03-owned amendment to `MembershipService.establish()` — either calling a C-004-owned resolve method with a status check, or an explicit WP-03 governance decision to accept the current direct-access pattern | Open | AuthService (Backend) |
| TD-048 | BA-02 (`OrganizationService.get_details()`, WP-01/C-004) does not itself realize EX-C004-05's typed Organization Validity Context contract (`ACTIVE`/`SUSPENDED`/`RETIRED`/`NOT_FOUND` as a first-class resolution outcome) — it returns full Organization details or a 404, regardless of status, which is a superset a caller must interpret themselves rather than a purpose-built validity resolution. No current dependent capability needs the narrower contract; not built speculatively ahead of a real consumer. | IRA-001A (found during the correction's own gap analysis of BA-02's relationship to ERB-C004-04/EX-C004-05) | Architecture | Low | A future Business Activity or capability that genuinely needs a typed validity-only resolution (as opposed to full details) — not invented ahead of that need | Open | AuthService (Backend) |
| TD-049 | Frontend consumers of Organization Establishment (`source/frontend/src/features/organization/components/OrganizationManagementScreen.tsx`, `state/useEstablishOrganization.ts`, `services/organization-api.ts`) still call the removed `POST /organizations` endpoint and assume BA-01's original synchronous-ACTIVE-establishment response contract — IRA-001A is backend-only, the same scope precedent BA-05/BA-06/BA-07 each established. Establishing an organization through the existing UI will now fail (404) until the frontend is updated to the two-step establish-then-activate flow. | IRA-001A | UX | Medium | **Resolved:** `services/organization-api.ts`'s `establishOrganization()` now performs both calls internally, preserving its existing `Promise<OrganizationResponse>` contract — no other frontend file required a change. See TD-050 for a partial-failure edge case surfaced by this fix. | Closed | Platform Admin (Frontend) |
| TD-050 | The frontend's `establishOrganization()` (`source/frontend/src/services/organization-api.ts`, TD-049's own resolution) performs two sequential backend calls (create attempt, then activate). If the first succeeds but the second fails for a non-409 reason (network drop, timeout, backend restart), the `organization_establishment_attempts` row is orphaned — un-activated, with no user-visible way to discover, retry-activate, or delete it. Because `organization_code` is unique across both `organizations` and `organization_establishment_attempts`, the obvious user recovery (retry with the same code) then fails with a misleading "already exists" 409, since the modal doesn't clear the code field on error. | Independent Review of TD-049's resolution | UX | Low | A proper fix (idempotent retry-by-code, an attempt list/cleanup affordance, or reusing an existing un-activated attempt on retry) requires backend/UX design beyond a minimal wrapper fix — deliberately not built here to avoid the orchestration-surfacing redesign this task was scoped to avoid. Revisit if this is ever observed in practice. | Open | Platform Admin (Frontend) |
| TD-051 | `StructuralChangeIntent` (SCI-000001, WP-04 BA-03) has no `GET` read endpoint — only `POST /structural-change-intents` (create) exists. EX-C005-05's own Required/Consumed Context names "Change Intent Context" as something a later experience must retrieve, but BA-03 (Type: Create, IRA-004 §4) was not scoped to include a read path; the create response body is the only current way to obtain a framed intent's fields. | BA-03 implementation (self-identified during this Business Activity's own gap analysis, IRA-004 §21's own "Explicitly Not Decided" disclosure) | Architecture | Low | BA-04 (Shape Structural Proposal)'s own future gap analysis — decide there whether it needs a dedicated `GET /structural-change-intents/{id}` or only an internal repository-level lookup. | Open | AuthService (Backend) |
| TD-052 | `StructuralChangeIntent.status` is constrained (CheckConstraint) to IRA-004 §21's full registered Lifecycle Model (CREATED, MODIFIED, SUPERSEDED, ABANDONED, WITHDRAWN, ARCHIVED), but BA-03's own code only ever writes CREATED — no code path anywhere in this repository sets any other value. | BA-03 implementation (self-identified, mirroring BA-01's own disclosed minimal-slice precedent, IRA-004 §5) | Architecture | Low | BA-04 through BA-08's own future gap analyses, as each realizes the lifecycle transition its own stage implies (MODIFIED/SUPERSEDED at BA-04/BA-06, WITHDRAWN per §43.3's exception path, ARCHIVED at eventual retirement). | Open | AuthService (Backend) |
| TD-053 | `StructuralProposal.status` is constrained to IRA-004 §22's own registered Lifecycle Model (CREATED, SUPERSEDED, VALIDATED, ARCHIVED), but BA-04's own code only ever writes CREATED and SUPERSEDED — VALIDATED (BR-C005-005's readiness marker) and ARCHIVED are never reached. | BA-04 implementation (self-identified, mirroring TD-052's own identical class for SCI-000001) | Architecture | Low | BA-07 (Validate Transition Readiness)'s own future gap analysis decides how readiness is represented (a status value here, a separate column, or a separate table); a future retirement/cleanup path would reach ARCHIVED. | Open | AuthService (Backend) |
| TD-054 | "Initial Comparison Context" (EX-C005-05's own Produced Context, alongside Proposed Outcome Context) is not persisted or computed anywhere by BA-04 — `StructuralProposalResponse` returns only the proposal itself. | BA-04 implementation (self-identified; Comparison Context fails the Cross-Experience Reference Test — named only within EX-C005-05's own text — so it is not itself a registered Business Object, but PE-001-C005 does not specify what is compared, and inventing a diff representation was judged out of BA-04's own minimal scope) | Architecture | Low | A future refinement of BA-04, or a dedicated future Business Activity, once a concrete comparison representation is actually needed by a caller. | Open | AuthService (Backend) |
| TD-055 | No `GET` read endpoint exists for Proposed Outcome Context — only `POST /structural-proposals` (Shape) and `POST /structural-proposals/{proposal_id}/revisions` (Refine) exist. Mirrors TD-051's identical disposition for Structural Change Intent. | BA-04 implementation (self-identified, IRA-004 §4's own "Create / Update" typing for BA-04 — no Query type listed) | Architecture | Low | BA-05 (Assess Structural Consequence)'s own future gap analysis decides whether it needs a dedicated `GET` endpoint or an internal repository-level lookup only. | Open | AuthService (Backend) |
| TD-056 | `structural_proposals` has no unique constraint spanning `(proposal_id, revision_number)`. Two concurrent `POST /structural-proposals/{proposal_id}/revisions` calls against the same proposal could both read the same current revision and both insert a row with the same `revision_number`, silently producing two "revision 2" rows instead of a detected conflict. | BA-04 implementation (self-identified, the same class of gap TD-005/TD-006 already recorded for WP-01's own concurrent-duplicate race) | Concurrency | Low | Add a unique constraint on `(proposal_id, revision_number)` and a dedicated concurrency test, mirroring TD-005's own resolution pattern for `organizations.organization_code`. | Open | AuthService (Backend) |
| TD-057 | `ImpactAssessment.status` is constrained to IRA-004 §23's own registered Lifecycle Model (CREATED, INVALIDATED, ARCHIVED), but BA-05's own code only ever writes CREATED — INVALIDATED and ARCHIVED are never reached. | BA-05 implementation (self-identified, mirroring TD-052/TD-053's own identical class) | Architecture | Low | Setting INVALIDATED requires reaching into BA-04's own `refine_proposal()` flow (the event that triggers invalidation per EX-C005-07's own Invalidated Context) — deliberately out of BA-05's own scope ("implement only what BA-05 owns"). A future cross-cutting mechanism or BA-06's own gap analysis decides how invalidation is actually triggered. | Open | AuthService (Backend) |
| TD-058 | No `GET` read endpoint exists for Impact Context — only `POST /impact-assessments` exists. Mirrors TD-051/TD-055's identical disposition for Structural Change Intent / Proposed Outcome Context. | BA-05 implementation (self-identified, IRA-004 §4's own typing — no dedicated read endpoint scoped for this Business Activity) | Architecture | Low | BA-06 (Review Structural Outcome)'s own future gap analysis decides whether it needs a dedicated `GET` endpoint or an internal repository-level lookup only. | Open | AuthService (Backend) |
| TD-059 | `POST /impact-assessments` does not verify that the referenced `structural_proposal_id` is still the current (non-`SUPERSEDED`) revision of its own proposal lineage — an assessment can be created against a revision a later Refine call has already superseded. | BA-05 implementation (self-identified during this Business Activity's own gap analysis; EX-C005-07's own Trigger text — "A coherent proposed structural outcome exists" — does not explicitly require currency, so this was not assumed either way) | Architecture | Low | A future revisit of BA-05 (or BA-06's own review-readiness gap analysis) decides whether assessing a superseded revision should be rejected, allowed with a warning, or remains permitted as historical analysis. | Open | AuthService (Backend) |
| TD-060 | `StructuralReview.concerns` (RVC-000001, WP-04 BA-06) is a single Text field. §41.16's own Collaboration Contract text — "Review concerns SHALL preserve author, decision context and unresolved/resolved status by reference to owning mechanisms" — arguably implies structured, per-concern tracking (individual author, individual resolved/unresolved status), not one free-text field. | BA-06 implementation (self-identified during this Business Activity's own gap analysis) | Architecture | Low | A future revisit of BA-06 introduces a dedicated per-concern child table once a real consumer needs individually-tracked concerns rather than a single review-level text field. | Open | AuthService (Backend) |
| TD-061 | No `GET` read endpoint exists for Review Context — only `POST /structural-reviews` (create) and `POST /structural-reviews/{id}/resolve-concerns` exist. Mirrors TD-051/TD-055/TD-058's identical disposition for the other Structural Context Lifecycle objects. | BA-06 implementation (self-identified, IRA-004 §4's own "Update (review)" typing — no dedicated read endpoint scoped for this Business Activity) | Architecture | Low | BA-07 (Validate Transition Readiness)'s own future gap analysis decides whether it needs a dedicated `GET` endpoint or an internal repository-level lookup only. | Open | AuthService (Backend) |
| TD-062 | `StructuralReview.status` is constrained to IRA-004 §25's own registered Lifecycle Model (CREATED, CONCERNS_RESOLVED, INVALIDATED, ARCHIVED), but BA-06's own code only ever writes CREATED and CONCERNS_RESOLVED — INVALIDATED and ARCHIVED are never reached. | BA-06 implementation (self-identified, mirroring TD-052/TD-053/TD-057's own identical class) | Architecture | Low | Setting INVALIDATED requires reaching into BA-04's own `refine_proposal()` flow (the event that triggers invalidation per GS-INV-007) — deliberately out of BA-06's own scope ("implement only what BA-06 owns"), the same disposition already recorded for Impact Context (TD-057). | Open | AuthService (Backend) |
| TD-063 | `POST /structural-reviews` and `POST /structural-reviews/{id}/resolve-concerns` do not verify that the referenced proposal revision is still current (non-`SUPERSEDED`) — mirrors TD-059's identical gap for Impact Context, now also present for Review Context. | BA-06 implementation (self-identified, same disclosed-not-assumed disposition as TD-059) | Architecture | Low | A future revisit of BA-06 (or BA-07's own readiness gap analysis) decides whether reviewing/resolving against a superseded revision should be rejected, allowed with a warning, or remains permitted. | Open | AuthService (Backend) |
| TD-064 | No `GET` read endpoint exists for Validation Context — only `POST /structural-validations` exists. Mirrors TD-051/TD-055/TD-058/TD-061's identical disposition for the other Structural Context Lifecycle objects. | BA-07 implementation (self-identified, IRA-004 §4's own "Update (validation)" typing — no dedicated read endpoint scoped for this Business Activity) | Architecture | Low | BA-08 (Complete Structural Transition)'s own future gap analysis decides whether it needs a dedicated `GET` endpoint or an internal repository-level lookup only. | Open | AuthService (Backend) |
| TD-065 | `StructuralValidation.status` is constrained to IRA-004 §26's own registered Lifecycle Model (CREATED, INVALIDATED, ARCHIVED), but BA-07's own code only ever writes CREATED — INVALIDATED and ARCHIVED are never reached. | BA-07 implementation (self-identified, mirroring TD-052/TD-053/TD-057/TD-062's own identical class) | Architecture | Low | Setting INVALIDATED requires reaching into BA-04's own `refine_proposal()` flow (the event that triggers invalidation per GS-INV-007) — deliberately out of BA-07's own scope, the same disposition already recorded for Impact Context (TD-057) and Review Context (TD-062). | Open | AuthService (Backend) |
| TD-066 | `POST /structural-validations` enforces only BR-C005-007 (review concerns resolved) as its readiness gate. EX-C005-10's own AI Assistance clause — "AI MAY identify missing context or apparent inconsistencies" — alludes to further readiness criteria beyond concern-resolution that are not implemented. | BA-07 implementation (self-identified during this Business Activity's own gap analysis, directly against EX-C005-10's own text) | Architecture | Low | A future revisit of BA-07, once a concrete additional readiness criterion (e.g., missing required context, structural inconsistency detection) is actually needed by a real caller — not invented speculatively ahead of that need. | Open | AuthService (Backend) |
| TD-067 | `POST /structural-validations` does not verify that the referenced `structural_proposal_id` is still the current (non-`SUPERSEDED`) revision of its own proposal lineage — mirrors TD-059/TD-063's identical gap for Impact Context and Review Context, now also present for Validation Context. | BA-07 implementation (self-identified, same disclosed-not-assumed disposition as TD-059/TD-063) | Architecture | Low | A future revisit of BA-07 (or BA-08's own readiness gap analysis) decides whether validating against a superseded revision should be rejected, allowed with a warning, or remains permitted — ideally resolved once for TD-059/TD-063/TD-067 together. | Open | AuthService (Backend) |
| TD-068 | No `GET` read endpoint exists for Resulting Structural Context — only `POST /structural-completions` exists. Mirrors TD-051/TD-055/TD-058/TD-061/TD-064's identical disposition for the other Structural Context Lifecycle objects. | BA-08 implementation (self-identified, IRA-004 §4's own typing — no dedicated read endpoint scoped for this Business Activity) | Architecture | Low | **Resolved:** BA-09 (Continue from Resulting Structure) adds `GET /structural-completions/{completion_id}` — `StructuralCompletionService.get_details()`, reusing the existing response shape verbatim, no new table/repository/service. | Closed | AuthService (Backend) |
| TD-069 | `StructuralCompletion.status` is constrained to IRA-004 §27's own registered Lifecycle Model (CREATED, ARCHIVED), but BA-08's own code only ever writes CREATED — ARCHIVED is never reached. | BA-08 implementation (self-identified, mirroring TD-052/TD-053/TD-057/TD-062/TD-065's own identical class) | Architecture | Low | A future retirement/archival path reaches ARCHIVED once a real consumer needs it. | Open | AuthService (Backend) |
| TD-070 | **BA-08 ("Complete Structural Transition") records that a governed structural transition has been completed (`RSC-000001`) but performs no actual ERG-001 structural mutation.** `organization_nodes` is never modified, and `organization_hierarchy`/`consolidation_determination` are never created. A caller can complete an entire Structural Change Intent → Proposal → Review → Validation → Completion chain, and the enterprise's own real structural data (the `OrganizationNode` the proposal targeted) is byte-for-byte unchanged afterward — verified directly by this Business Activity's own tests (`test_complete_structural_transition_does_not_mutate_organization_node`, both service- and API-level). | BA-08 implementation (deliberate, mandatory scope decision — Option A, per this Business Activity's own readiness assessment and explicit implementation instruction) | Architecture | **High** | No canonical document in this repository (PE-001-C005, ERG-001, Master Technical Architecture) specifies a structured representation from which a real structural mutation could be deterministically derived from a `StructuralProposal`'s own free-text `proposed_outcome_description` (TD-054's own identical gap). Resolution requires, at minimum: (1) a governance decision on what a "structural change" is represented as in data (a structured patch/diff schema, not free text); (2) the actual ERG-001 write-path capability (`organization_hierarchy`, `consolidation_determination` — neither exists anywhere in this repository); (3) a mechanism connecting a completed `RSC-000001` row to that write path. This is real, substantial future work, likely spanning multiple future Business Activities or its own governance decision — not invented speculatively here. | Open | AuthService (Backend) |
| TD-071 | `Backend/Shared/`'s `aurex.backend.shared.*` import path (used by every module in `Backend/Shared/Logging`, `Backend/Shared/Events`, and `Backend/Shared/Security`) does not resolve — no `aurex` package exists anywhere in this repository (no `setup.py`/`pyproject.toml`, no matching directory structure); importing any of these modules raises `ModuleNotFoundError` immediately. Pre-existing since WP-00; previously disclosed only inline in a code comment (`Backend/Services/AuthService/observability.py`), never formally registered here, itself a `CLAUDE.md §19.8.2` gap (Technical Debt shall not exist solely in comments). Directly relevant to `WP-RTA-001`: this is why Milestone M1 placed the new Authorization Runtime Engine module under `Backend/Runtime/AuthorizationEngine/` rather than `Backend/Shared/`, after directly confirming the breakage rather than assuming WP-00's own comment was still accurate. | WP-RTA-001 M1 (formally registered here; originally disclosed at WP-00) | Developer Experience | Medium | A platform-wide fix (adding a real `aurex` namespace package, or removing the dead import convention repository-wide) spanning AIService, IngestionService, ReportingService, TenantService, and AuthService — out of any single Work Package's own scope, per WP-00's own original disclosure | Open | Platform (Backend) |
| TD-072 | `AuthorizationContext` (`Backend/Runtime/AuthorizationEngine/authorization/models.py`, WP-RTA-001 M1) models Roles/Permissions/Assignments/Delegations/Approval Authorities as opaque `tuple[str, ...]` identifier collections rather than richer typed objects — a deliberate M1 simplification, since no concrete `TierResolver` exists yet (M5) to define what shape each tier actually needs to consume. | WP-RTA-001 M1 | Architecture | Low | Revisit the `AuthorizationContext` field shapes once WP-RTA-001 M5 designs its first concrete `TierResolver` and its own real data needs are known | Open | WP-RTA-001 (Runtime) |
| TD-073 | `EvaluationPipeline`/`ResolverOrchestrator` (`Backend/Runtime/AuthorizationEngine/authorization/{pipeline,orchestrator}.py`, WP-RTA-001 M3) validate their `registry` constructor argument only against `None` (`PipelineConfigurationError`) — a `registry` of the wrong type (not a `ResolverRegistry`) would instead fail with a less clear error deeper inside `ResolverOrchestrator`/`ResolverRegistry.build()`, rather than a clear, immediate configuration error at the pipeline's own boundary. | WP-RTA-001 M3 (self-identified) | Developer Experience | Low | Add an explicit `isinstance(registry, ResolverRegistry)` check (or equivalent structural check) once a second, real caller of `EvaluationPipeline` exists to justify the stricter validation | Open | WP-RTA-001 (Runtime) |
| TD-074 | `AuthorizationRequest` (`Backend/Runtime/AuthorizationEngine/adapters/authorization_adapter.py`, WP-RTA-001 M4) is field-for-field identical to `AuthorizationContext` — `AuthorizationAdapter.build_context()` performs only a direct 1:1 mapping, no real translation logic, because no Business Activity caller exists yet (explicitly out of M4's own scope) to reveal what its own natural request vocabulary actually looks like. The architectural seam (a distinct type, one translation point) is real; the translation itself is not yet exercising that seam's full value. | WP-RTA-001 M4 (self-identified) | Architecture | Low | Revisit `AuthorizationRequest`'s own shape once a real Business Activity (most likely WP-05 BA-01, per `IRA-RTA-001 §6`) is integrated and its own caller-side vocabulary is known | Open | WP-RTA-001 (Runtime) |
| TD-075 | `EvaluationPipeline._notify_safely()` (`Backend/Runtime/AuthorizationEngine/authorization/pipeline.py`, WP-RTA-001 M5) isolates an observer callback's own exception (catch-and-discard) so it can never affect the real evaluation outcome — but provides no visibility mechanism of its own for a failing observer, since no logging/metrics/tracing backend is available this milestone (explicitly out of scope). A silently-broken observer (e.g. a misconfigured `RuntimeObservabilityCollector`) would fail invisibly. | WP-RTA-001 M5 (self-identified) | Observability | Medium | Add a minimal, backend-agnostic way to surface an isolated observer failure (e.g. a bounded in-memory `EvaluationPipeline.observer_failures` log) once a real backend integration (a future, separately-scoped milestone) exists to consume it | Open | WP-RTA-001 (Runtime) |
| TD-076 | `EnterpriseScopeValidator` (`Backend/Runtime/AuthorizationEngine/authorization/scope_validator.py`, WP-RTA-001 M5) performs structural validation only (presence/non-blank checks on `organization_id`/`enterprise_scope`) — it never verifies `enterprise_scope` actually names a real, existing node under `organization_id` in ERG-001's own structure, since that would require repository/persistence access explicitly out of this milestone's scope. A syntactically well-formed but semantically nonexistent scope value currently passes validation. | WP-RTA-001 M5 (self-identified) | Data Integrity | Low | Extend `EnterpriseScopeValidator` to consult a real ERG-001-backed repository once this Work Package (or a consuming Business Activity) is authorized to access persistence — not before, per `IRA-RTA-001 §7`'s own exclusion of database access from this Work Package | Open | WP-RTA-001 (Runtime) |
| TD-077 | `EnterpriseScopeValidator.validate()` (WP-RTA-001 M5) runs once, before `AuthorizationEngine.evaluate()` begins — `RTA-001 §11.7`'s own canonical Authorization Resolution Pipeline instead places Enterprise Scope Validation between Delegation Evaluation and Approval Authority Evaluation, inside the five-tier precedence walk. Threading validation into that exact position would require modifying `AuthorizationEngine`'s own M1 evaluation loop, which this milestone's instruction prohibited redesigning. The substantive guarantee (authorization is never evaluated against an unvalidated Enterprise Context) is preserved either way; only the literal step ordering differs from §11.7's own text. | WP-RTA-001 M5 (self-identified) | Architecture | Low | Revisit whether the pre-evaluation placement remains acceptable once M6 begins threading real Delegation/Approval-Authority resolution into the pipeline, or whether §11.7's exact ordering needs to be honored at that point | Open | WP-RTA-001 (Runtime) |
| TD-078 | `PipelineObserver` (M3) is a passive, after-the-fact notification seam — every method returns `None` and is called either before evaluation starts or after it has already completed/failed. M6's Extension Point Validation (`tests/test_extension_points.py`) confirmed this is sufficient for Metrics, Tracing, Audit, and read-side Persistence recording, but **not** for Caching, which must intercept *before* `AuthorizationEngine` runs to short-circuit evaluation entirely — structurally impossible through `PipelineObserver` alone. A proof-of-concept wrapper pattern (composing around `EvaluationPipeline`, still zero `AuthorizationEngine` changes) was demonstrated test-only, not shipped as production code, per M6's own "Do NOT implement... Authorization caching implementation" exclusion. | WP-RTA-001 M6 (self-identified, Extension Point Validation) | Architecture | Low | Design and implement a real Caching wrapper around `EvaluationPipeline` in the originally-planned M6 Caching sub-item (per `WP-RTA-001`'s own charter-synchronization pass — note this Work Package's M6 is titled differently in practice; caching remains a distinct, not-yet-scheduled future increment) | Open | WP-RTA-001 (Runtime) |
| TD-079 | BA-01 through BA-04 (WP-05/C-002, Access Management) gate every `/access-evaluations` endpoint on the existing `PLATFORM_ADMIN` role claim only — PE-001-C002 names no distinct, enforceable persona claim for Access Evaluation actions today, the same class of gap as TD-021 through TD-025/TD-031/TD-034/TD-035/TD-036/TD-039/TD-042. See detailed entry below the table for full fields. | BA-01 through BA-04 (self-identified, IRA-005 §12) | Security | Low | A persona-specific authorization model for C-002 (future, separately-scoped Business Activity or architecture amendment), followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for these endpoints | Open | AuthService (Backend) |
| TD-080 | No `GET` read endpoint exists for Access Evaluation Outcome — only `POST /access-evaluations` (create) and its four sub-resource action endpoints (`preserve`, `expire`, `context-change`, `handoff-rejection`) exist. Mirrors TD-051/TD-055/TD-058/TD-061/TD-064's identical disposition for the Structural Context Lifecycle objects. | BA-01 implementation (self-identified, IRA-005 §12's own authorized scope — no Query-type Business Activity chartered) | Architecture | Low | A future, separately-scoped WP-05 Business Activity, once a real caller needs to resolve an Access Evaluation Outcome by id independently of the response already returned by whichever action created or transitioned it | Open | AuthService (Backend) |
| TD-081 | `test_access_evaluation_api.py` (WP-05) exercised only one branch of several two-branch service behaviors at the API layer: BA-04's `handoff-rejection` endpoint was tested only for the live-outcome (`CAPABILITY_SCOPED_INSUFFICIENCY`) classification, not the invalidated-outcome (`INTEGRITY_SIGNAL`) classification; BA-02's `expire` endpoint was tested for the double-preserve 409 but not the expire-without-preserve 409; BA-03's `context-change` endpoint was tested only for the invalidating path, not its own 409 rejection of a non-live outcome. All of these branches were already fully covered at the unit (service) layer in `test_access_evaluation_service.py`. | Independent Review (CERT-WP-05) | Testing | Low | **Resolved:** the three missing branch-level API assertions (`test_expire_rejects_outcome_that_was_never_preserved`, `test_context_change_rejects_non_live_outcome`, `test_handoff_rejection_classifies_invalidated_outcome_as_integrity_signal`) were added to `test_access_evaluation_api.py`; 14/14 API tests pass, 601/601 full suite passes | Closed | AuthService (Backend) |
| TD-082 | BA-02's own "Bound" / `EX-C002-06`'s Scope Boundary is not modelled — no execution-scope identifier, no expiry timestamp, and no automatic expiry exist; expiry is manual/caller-invoked only. See detailed entry below the table for full fields. | VV-AUDIT-WP-05 F-08 | Architecture | Medium | A future, separately-scoped Business Activity or architecture decision introduces a real execution-scope concept and/or an automatic expiry trigger | Open | AuthService (Backend) |
| TD-083 | BA-03 performs no real detection — invalidation is driven entirely by an unvalidated caller-supplied `changed_fact` string, never re-checked against Membership/Domain/Approval Authority state. See detailed entry below the table for full fields. | VV-AUDIT-WP-05 F-09 | Business Rule Compliance | Medium | A future Business Activity implementing the excluded re-resolution path would naturally also supply real detection | Open | AuthService (Backend) |
| TD-084 | `AccessEvaluationValidityStatus.SUPERSEDED` is declared but permanently unreachable by any WP-05 code path — same class as WP-04's TD-052/057/062/065/069. See detailed entry below the table for full fields. | VV-AUDIT-WP-05 F-11 | Architecture | Low | A future Work Package performing a real fresh-evaluation supersession | Open | AuthService (Backend) |
| TD-085 | `IRA-005 §11`'s "Full history retained" is only partially met — transitions overwrite `validity_status`/`reason` in place; no prior-state row or version history exists. See detailed entry below the table for full fields. | VV-AUDIT-WP-05 F-12 | Data Integrity | Low | A future transition/version history mechanism, if a real consumer needs to query prior states | Open | AuthService (Backend) |
| TD-086 | `CMD-001 §26.7` Physical Implementation Mapping for `AEO-000001` was never updated to record the now-known table/APIs/events WP-05 supplied. See detailed entry below the table for full fields. | VV-AUDIT-WP-05 F-13 | Documentation | Low | Update `CMD-001 §26.7` (or equivalent) to record the now-known Physical Implementation Mapping | Open | AuthService (Backend) |
| TD-087 | Dependent capability hand-off rejections (BA-04) are never persisted — no queryable record exists beyond the audit log and the synchronous API response. See detailed entry below the table for full fields. | VV-AUDIT-WP-05 F-15 | Data Integrity | Low | A dedicated persisted record, if a real future consumer needs queryable hand-off-rejection history | Open | AuthService (Backend) |
| TD-088 | `approval_authority_id` foreign key column is not indexed — immaterial at current volumes. See detailed entry below the table for full fields. | VV-AUDIT-WP-05 F-19 | Performance | Low | Add an index if table volume or `approval_authorities` mutation frequency ever make this material | Open | AuthService (Backend) |
| TD-089 | Four of five `/access-evaluations` routes omit 400/401/403 from their OpenAPI `responses` maps — cosmetic only, all codes are correctly enforced at runtime. See detailed entry below the table for full fields. | VV-AUDIT-WP-05 F-21 | Documentation | Low | Add 400/401/403 to the four sub-resource endpoints' `responses` maps | Open | AuthService (Backend) |
| TD-090 | BA-01 (Understand Domain Permission Context, WP-06/C-003) gates both new read endpoints (`GET /domain-permissions/{id}`, `GET /domain-permissions`) on the existing `PLATFORM_ADMIN` role claim only — PE-001-C003 v1.1's `EX-C003-11` extends Contract 5.1 to the same defining-authority personas (Domain Owner/Domain Admin, URA-001-45/46) already gapped by `TD-022`, not to `PLATFORM_ADMIN` specifically. Same root cause as `TD-022`, anticipated in `IRA-006 §10.2` before implementation began, not discovered after the fact. See detailed entry below the table for full fields. | BA-01 implementation (self-identified, `IRA-006 §10.2`) | Security | Low | Resolved by the same future Domain Owner/Domain Admin authority model `TD-022` already awaits, applied to these two endpoints in the same pass | Open | AuthService (Backend) |
| TD-091 | `GET /domain-permissions` (`DomainPermissionRepository.search()`, WP-06/C-003) returns every matching row with no `limit`/`skip`/pagination of any kind — omitting every filter returns literally every `DomainPermission` row, including historical `SUPERSEDED` versions. An in-repository precedent for exactly this situation already exists (`OrganizationRepository.search()`, WP-01, caps `limit` at 100 via `Query(ge=1, le=100)` and returns a total count) and was not applied; the omission was undisclosed in `IRA-006`/`IMP-REPORT-WP-06`. See detailed entry below the table for full fields. | `CERT-WP-06` §4.6 (Independent Certification) | Performance | Medium | Add `skip`/`limit` query parameters to `GET /domain-permissions`, mirroring `OrganizationRepository.search()`'s own pattern, before this endpoint is relied upon at production scale or by a downstream capability | Open | AuthService (Backend) |

---

### TD-021 — Detailed Entry

- **Title:** PLATFORM_ADMIN-Only Authorization Gate for Role & Permission Management (BR-C003-08 Persona-Specific Defining Authority Deferred)
- **Category:** Security / Authorization Granularity
- **Description:** BA-01 (Establish Business or System Role, WP-02/C-003) gates both Business Role and System Role establishment on the existing `PLATFORM_ADMIN` role claim only (`dependencies.require_platform_admin`, reused unchanged from WP-01). PE-001-C003's BR-C003-08 requires confirmed, type-specific defining authority — Corporate Admin for Business Roles; Security Admin or User Admin for System Roles — none of which exist as distinct, enforceable claims anywhere in the platform today.
- **Root Cause:** ADR-002 (AuthService Seed Role Catalog Reconciliation) remains **Proposed, not Accepted**. The canonical role catalog URA-001/MDP-001 specify (`AUREX_ADMIN`, `CORPORATE_ADMIN`, `SECURITY_ADMIN`, `USER_ADMIN`, `DOMAIN_ADMIN`) does not match the actually-seeded catalog (`PLATFORM_ADMIN`, `ORG_ADMIN`, `ESG_MANAGER`, `AUDITOR`, `SUPPLIER_ADMIN`, `BOARD_MEMBER`), so no persona-specific claim can be issued or checked until architecture governance resolves which option (A/B/C) applies.
- **Impact:** Any authenticated `PLATFORM_ADMIN` can establish either a Business Role or a System Role, regardless of whether URA-001 would actually confer that specific defining authority to a Corporate Admin versus a Security Admin versus a User Admin. No privilege-escalation risk beyond what `PLATFORM_ADMIN` already holds platform-wide today, but BR-C003-08's persona differentiation is not enforced.
- **Severity:** Low — a disclosed, deliberate simplification, the same class of gap WP-01 already established precedent for (IRA-001 §2.7), not a silent gap or a broken invariant; confirmed non-blocking by Independent Review.
- **Status:** Open
- **Target Resolution:** ADR-002 acceptance, followed by implementation of persona-specific authorization dependencies (e.g. `require_corporate_admin`, `require_security_admin`, `require_user_admin`) before any Business Activity that requires differentiated defining authority.
- **Owning Work Package:** WP-02 — Role & Permission Management (C-003)
- **Related Business Activity:** BA-01 — Establish Business or System Role
- **Source:** Independent Review of BA-01 (`IMP-REPORT-WP-02_Role_Permission_Management.md`, Finding Minor-1)
- **Resolution Criteria:** ADR-002 is Accepted; a persona-specific authorization dependency exists and is enforced for at least Business Role (Corporate Admin) and System Role (Security Admin/User Admin) establishment; BA-01's endpoint (and any subsequent Business Activity requiring type-specific authority) is updated to require the correct persona-specific claim instead of `PLATFORM_ADMIN` alone; a test exists asserting the correct persona-specific claim is required and an unauthorized persona is rejected.

---

### TD-022 — Detailed Entry

- **Title:** PLATFORM_ADMIN-Only Authorization Gate for Establish Domain Permission (URA-001-45/46 Domain Owner/Domain Admin Authority Not Yet Modeled)
- **Category:** Security / Authorization Granularity
- **Description:** BA-02 (Establish Domain Permission, WP-02/C-003) gates establishment on the existing `PLATFORM_ADMIN` role claim only (`dependencies.require_platform_admin`, reused unchanged from WP-01/BA-01). PE-001-C003's EX-C003-02 requires confirmed Domain Owner or Domain Admin authority (URA-001-45/46) for the specific target Domain, distinct from platform-wide administration.
- **Root Cause:** Domain (AMD-014, `models/domain.py`/`domain_registry`) was deliberately implemented as ownership-free reference/master data — no Domain Owner/Domain Admin relationship exists anywhere in the schema, by explicit prior architectural decision (Domain architecture is frozen; reopening it to add an ownership relationship is out of BA-02's scope). There is therefore no data anywhere from which a Domain-specific defining authority could be confirmed today.
- **Impact:** Any authenticated `PLATFORM_ADMIN` can establish a Domain Permission for any Domain, regardless of whether URA-001 would actually confer that specific defining authority to a particular Domain Owner or Domain Admin. No privilege-escalation risk beyond what `PLATFORM_ADMIN` already holds platform-wide today (same risk profile as TD-021), but URA-001-45/46's per-Domain authority differentiation is not enforced.
- **Severity:** Low — a disclosed, deliberate simplification, the same class of gap as TD-021, confirmed non-blocking by Independent Review.
- **Status:** Open
- **Target Resolution:** A Domain Owner/Domain Admin authority model (a future, separately-scoped architecture amendment or Business Activity — not implied or scheduled by this entry), followed by a persona-specific authorization dependency (e.g. `require_domain_owner_or_admin`) replacing `PLATFORM_ADMIN` for this endpoint.
- **Owning Work Package:** WP-02 — Role & Permission Management (C-003)
- **Related Business Activity:** BA-02 — Establish Domain Permission
- **Source:** Independent Review of BA-02 (`IMP-REPORT-WP-02_Role_Permission_Management.md`)
- **Resolution Criteria:** A Domain Owner/Domain Admin authority model exists and is queryable; a persona-specific authorization dependency exists and is enforced for Establish Domain Permission; a test exists asserting the correct Domain-specific authority is required and an unauthorized caller is rejected.

---

### TD-023 — Detailed Entry

- **Title:** PLATFORM_ADMIN-Only Authorization Gate for Establish Approval Authority (URA-001-32/45 Corporate Admin/Domain Owner Authority Not Yet Modeled)
- **Category:** Security / Authorization Granularity
- **Description:** BA-03 (Establish Approval Authority, WP-02/C-003) gates establishment on the existing `PLATFORM_ADMIN` role claim only (`dependencies.require_platform_admin`, reused unchanged from WP-01/BA-01/BA-02). PE-001-C003's EX-C003-03 requires confirmed Corporate Admin authority (Global/Company-scoped authorities, URA-001-32) or Domain Owner authority (Domain-scoped authorities, URA-001-45), neither of which exists as a distinct, enforceable claim today.
- **Root Cause:** Two independent, pre-existing gaps compound here: (1) Corporate Admin has no distinct claim in the actually-seeded role catalog, the same ADR-002 catalog-mismatch gap TD-021 already tracks; (2) Domain Owner authority has no data to confirm against, the same Domain-is-ownership-free gap TD-022 already tracks (Domain, AMD-014, was deliberately built as ownership-free reference/master data; reopening it is out of BA-03's scope). BA-03 does not introduce a new authority gap — it is the third Business Activity to encounter one of these two already-tracked root causes.
- **Impact:** Any authenticated `PLATFORM_ADMIN` can establish an Approval Authority of any scope for any Organization/Domain, regardless of whether URA-001 would actually confer that specific defining authority to a particular Corporate Admin or Domain Owner. No privilege-escalation risk beyond what `PLATFORM_ADMIN` already holds platform-wide today (same risk profile as TD-021/TD-022), but URA-001-32/45's persona differentiation is not enforced.
- **Severity:** Low — a disclosed, deliberate simplification, the same class of gap as TD-021/TD-022, confirmed non-blocking by Independent Review.
- **Status:** Open
- **Target Resolution:** ADR-002 acceptance (for Corporate Admin) and/or a Domain Owner/Domain Admin authority model (for Domain-scoped authorities) — both future, separately-scoped efforts, not implied or scheduled by this entry — followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for this endpoint.
- **Owning Work Package:** WP-02 — Role & Permission Management (C-003)
- **Related Business Activity:** BA-03 — Establish Approval Authority
- **Source:** Independent Review of BA-03 (`IMP-REPORT-WP-02_Role_Permission_Management.md`)
- **Resolution Criteria:** ADR-002 is Accepted and/or a Domain Owner/Domain Admin authority model exists and is queryable; a persona-specific authorization dependency exists and is enforced for Establish Approval Authority, differentiated by scope_type; a test exists asserting the correct persona-specific authority is required per scope and an unauthorized caller is rejected.

---

### TD-024 — Detailed Entry

- **Title:** PLATFORM_ADMIN-Only Authorization Gate for Establish Delegation Policy (URA-001-32/45 Corporate Admin/Domain Owner Authority Not Yet Modeled)
- **Category:** Security / Authorization Granularity
- **Description:** BA-04 (Establish Delegation Policy, WP-02/C-003) gates establishment on the existing `PLATFORM_ADMIN` role claim only (`dependencies.require_platform_admin`, reused unchanged from WP-01/BA-01/BA-02/BA-03). PE-001-C003's EX-C003-04 requires confirmed Corporate Admin authority (URA-001-32) or Domain Owner authority (URA-001-45), neither of which exists as a distinct, enforceable claim today.
- **Root Cause:** The identical two independent, pre-existing gaps already tracked by TD-021 and TD-022 compound here, exactly as they did for TD-023: (1) Corporate Admin has no distinct claim in the actually-seeded role catalog (ADR-002 remains Proposed, not Accepted); (2) Domain Owner authority has no data to confirm against (Domain, AMD-014, is deliberately ownership-free reference data; reopening it is out of BA-04's scope). BA-04 does not introduce a new authority gap — it is the fourth Business Activity to encounter one of these two already-tracked root causes.
- **Impact:** Any authenticated `PLATFORM_ADMIN` can establish a Delegation Policy of any scope for any Organization/Domain, regardless of whether URA-001 would actually confer that specific defining authority to a particular Corporate Admin or Domain Owner. No privilege-escalation risk beyond what `PLATFORM_ADMIN` already holds platform-wide today (same risk profile as TD-021/TD-022/TD-023), but URA-001-32/45's persona differentiation is not enforced.
- **Severity:** Low — a disclosed, deliberate simplification, the same class of gap as TD-021/TD-022/TD-023, confirmed non-blocking by Independent Review.
- **Status:** Open
- **Target Resolution:** ADR-002 acceptance (for Corporate Admin) and/or a Domain Owner/Domain Admin authority model (for Domain-scoped policies) — both future, separately-scoped efforts, not implied or scheduled by this entry — followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for this endpoint.
- **Owning Work Package:** WP-02 — Role & Permission Management (C-003)
- **Related Business Activity:** BA-04 — Establish Delegation Policy
- **Source:** Independent Review of BA-04 (`IMP-REPORT-WP-02_Role_Permission_Management.md`)
- **Resolution Criteria:** ADR-002 is Accepted and/or a Domain Owner/Domain Admin authority model exists and is queryable; a persona-specific authorization dependency exists and is enforced for Establish Delegation Policy, differentiated by scope_type; a test exists asserting the correct persona-specific authority is required per scope and an unauthorized caller is rejected.

---

### TD-025 — Detailed Entry

- **Title:** PLATFORM_ADMIN-Only Authorization Gate for Establish Runtime Assignment Policy (URA-001-32/45 Corporate Admin/Domain Admin Authority Not Yet Modeled)
- **Category:** Security / Authorization Granularity
- **Description:** BA-05 (Establish Runtime Assignment Policy, WP-02/C-003) gates establishment on the existing `PLATFORM_ADMIN` role claim only (`dependencies.require_platform_admin`, reused unchanged from WP-01/BA-01/BA-02/BA-03/BA-04). PE-001-C003's EX-C003-05 requires confirmed Corporate Admin or Domain Admin authority, neither of which exists as a distinct, enforceable claim today.
- **Root Cause:** The identical two independent, pre-existing gaps already tracked by TD-021 and TD-022 compound here, exactly as they did for TD-023/TD-024: (1) Corporate Admin has no distinct claim in the actually-seeded role catalog (ADR-002 remains Proposed, not Accepted); (2) Domain Admin authority has no data to confirm against (Domain, AMD-014, is deliberately ownership-free reference data; reopening it is out of BA-05's scope). BA-05 does not introduce a new authority gap — it is the fifth Business Activity to encounter one of these two already-tracked root causes.
- **Impact:** Any authenticated `PLATFORM_ADMIN` can establish a Runtime Assignment Policy for any Organization, regardless of whether URA-001 would actually confer that specific defining authority to a particular Corporate Admin or Domain Admin. No privilege-escalation risk beyond what `PLATFORM_ADMIN` already holds platform-wide today (same risk profile as TD-021/TD-022/TD-023/TD-024), but URA-001-32/45's persona differentiation is not enforced.
- **Severity:** Low — a disclosed, deliberate simplification, the same class of gap as TD-021/TD-022/TD-023/TD-024, confirmed non-blocking by Independent Review.
- **Status:** Open
- **Target Resolution:** ADR-002 acceptance (for Corporate Admin) and/or a Domain Owner/Domain Admin authority model (for Domain-scoped policies) — both future, separately-scoped efforts, not implied or scheduled by this entry — followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for this endpoint.
- **Owning Work Package:** WP-02 — Role & Permission Management (C-003)
- **Related Business Activity:** BA-05 — Establish Runtime Assignment Policy
- **Source:** Independent Review of BA-05 (`IMP-REPORT-WP-02_Role_Permission_Management.md`)
- **Resolution Criteria:** ADR-002 is Accepted and/or a Domain Owner/Domain Admin authority model exists and is queryable; a persona-specific authorization dependency exists and is enforced for Establish Runtime Assignment Policy; a test exists asserting the correct persona-specific authority is required and an unauthorized caller is rejected.

---

### TD-026 — Detailed Entry

- **Title:** Approval Reference Is Free-Text, Not Validated Against a Real Approval Authority Record or Workflow
- **Category:** Data Integrity
- **Description:** BA-07's Version and Re-effective-Date Business Activity implements SD-002-011's Approval Reference universal temporal property as a nullable `String(255)` column on all five authorization policy objects (`roles`, `domain_permissions`, `approval_authorities`, `delegation_policies`, `runtime_assignment_policies`). A caller may supply any string; nothing checks it against an actual `approval_authorities` row or a resolved approval outcome.
- **Root Cause:** Two structural facts make real validation impossible today, not merely undone: (1) Contract 5.3 (Runtime Execution Boundary) forbids C-003 from ever evaluating or executing an approval workflow itself — "C-003 SHALL NEVER evaluate, compute, or imply the evaluation of whether a specific governed request is currently permitted"; (2) no runtime mechanism anywhere in this codebase resolves an Approval Authority's own `approval_strategy` (ANY_ONE/ALL/MAJORITY/SEQUENTIAL) against a specific decision to produce an actual approval outcome to reference — that remains RTA-001 §11's Authorization Runtime, not yet built (see the Runtime Engineering Methodology governance work, IMP-001 §13.17-13.25).
- **Impact:** `approval_reference` is currently documentation/audit-trail metadata only — useful for a human-supplied note, not machine-verifiable provenance. No data-integrity risk beyond that: it never gates or authorizes anything, and no Business Rule depends on its content being valid.
- **Severity:** Low — disclosed, deliberate, and consistent with Contract 5.3's own boundary; confirmed non-blocking by Independent Review.
- **Status:** Open
- **Target Resolution:** A future Approval Authority resolution/execution capability (C-002/RTA-001 §11) that can produce a real, resolved approval outcome for this column to reference. Not scheduled by this entry.
- **Owning Work Package:** WP-02 — Role & Permission Management (C-003)
- **Related Business Activity:** BA-07 — Version and Re-effective-Date Authorization Policy Object
- **Source:** BA-07 implementation (self-identified; disclosed in the RCC-equivalent field description and this report rather than found only during review)
- **Resolution Criteria:** An Approval Authority resolution/execution mechanism exists; `approval_reference` (or a successor field) is validated against a real, resolved approval outcome at write time; a test exists asserting an invalid/unresolved reference is rejected.

---

### TD-027 — Detailed Entry

- **Title:** No Concurrent-Double-Amendment Race Protection for Four of BA-07's Five Object Types
- **Category:** Data Integrity / Concurrency
- **Description:** `create_new_version()` reads the current ACTIVE row, then inserts a new ACTIVE row referencing it via `supersedes_id`. For Role, a concurrent second call against the same target is caught by the `role_code`-scoped partial unique index (`ix_roles_role_code_active_unique`) and surfaces as a clean 409. Domain Permission, Approval Authority, Delegation Policy, and Runtime Assignment Policy have no comparable natural-key constraint, so a genuine concurrent race could leave two ACTIVE rows for the same policy chain.
- **Root Cause:** Role uniquely has a caller-supplied natural key (`role_code`) to scope a partial unique index against; the other four types have no equivalent single natural key distinguishing one policy chain from another at the database level.
- **Impact:** Low likelihood — every version-amendment endpoint is `PLATFORM_ADMIN`-gated, administrative, and low-traffic, the same risk profile as TD-003's own accepted "last-write-wins" concurrency gap for Organization profile updates.
- **Severity:** Low — disclosed, found by Independent Review, comparable in class to TD-003 and TD-006's own accepted concurrency simplifications.
- **Status:** Open
- **Target Resolution:** A per-type mechanism closing the same race Role's fix already closes — e.g. a partial unique index scoped to each type's own natural anchor plus `status='ACTIVE'`, or optimistic-locking on the row being superseded.
- **Owning Work Package:** WP-02 — Role & Permission Management (C-003)
- **Related Business Activity:** BA-07 — Version and Re-effective-Date Authorization Policy Object
- **Source:** Independent Review of BA-07 (`IMP-REPORT-WP-02_Role_Permission_Management.md`)
- **Resolution Criteria:** Each of the four remaining types has a mechanism that rejects a concurrent double-amendment with a clean 409; a test exists per type asserting the race is caught, not silently allowed to produce two coexisting ACTIVE rows.

---

### TD-028 — Detailed Entry

- **Title:** BA-08's Dependency Check Is Vacuous for Four of Five Object Types
- **Category:** Data Integrity
- **Description:** `deprecate()`/`retire()` call `<Type>Repository.has_active_dependents(id)` before allowing a status transition, per BR-C003-04's "SHALL occur only once... confirms no active dependency remains unresolved." For Role, this queries the real, AuthService-implemented `memberships` table and genuinely blocks retirement of a Role with an active Membership. For Domain Permission, Approval Authority, Delegation Policy, and Runtime Assignment Policy, the method is a stub returning `False` unconditionally.
- **Root Cause:** Each of the four types' real canonical dependent does not exist in AuthService today: `membership_approval_authority` (Approval Authority) and `delegation_registry`/`runtime_assignment_registry` (Delegation Policy/Runtime Assignment Policy, both already named in BA-04's and BA-05's own module docstrings as canonical-but-not-implemented) have no model or migration anywhere in this codebase. Domain Permission has no dependent at all in the reviewed schema — that one is architecturally, not incompletely, vacuous.
- **Impact:** Retiring an Approval Authority, Delegation Policy, or Runtime Assignment Policy that is genuinely relied upon (once its real dependent table exists) would succeed today with no check catching it — a silent violation of BR-C003-04 waiting for its precondition (the dependent table) to become true. Not yet exploitable, since nothing depends on these objects anywhere in the running system today, but the gap is real, not merely theoretical, and grows more consequential as WP-02 and adjacent capabilities mature.
- **Severity:** Medium — higher than TD-023/024/025/027's own Low severity, because this gap concerns data-integrity/dependency-safety directly (BR-C003-04 itself), not an authorization-persona simplification.
- **Status:** Open
- **Target Resolution:** Implement `membership_approval_authority`, `delegation_registry`, and `runtime_assignment_registry` in AuthService (each already has a complete canonical definition in Master Technical Architecture), then extend each type's `has_active_dependents()` from a stub to a real query mirroring `RoleRepository.has_active_dependents()`'s own shape.
- **Owning Work Package:** WP-02 — Role & Permission Management (C-003)
- **Related Business Activity:** BA-08 — Deprecate or Retire Authorization Policy Object
- **Source:** BA-08 implementation (self-identified and disclosed in each stub `has_active_dependents()`'s own docstring, not found only during review)
- **Resolution Criteria:** Each of the three missing dependent tables is implemented; each corresponding `has_active_dependents()` performs a real query; a test exists per type asserting retirement is rejected when a genuine active dependent exists.

---

### TD-029 — Detailed Entry

- **Title:** DEPRECATED Is a Dead End — No Transition to RETIRED (or Back to ACTIVE) Exists
- **Category:** Data Integrity
- **Description:** `deprecate()` and `retire()` both require `status == ACTIVE` as their precondition, identically across all five object types. Once an object reaches DEPRECATED, no code path — including `retire()` itself — can move it further, since `retire()` also demands ACTIVE.
- **Root Cause:** BA-08 modeled Deprecate and Retire as two independent branches from ACTIVE, per EX-C003-08's own Purpose text ("Moves the object to a Deprecated/Retired lifecycle state"), rather than a chain (ACTIVE → DEPRECATED → RETIRED). Neither EX-C003-08 nor BR-C003-04 specifies which shape is required.
- **Impact:** An object correctly moved to DEPRECATED (Hidden, restorable per URA-001-127) has no way to progress to RETIRED (Archived) short of a future code change — a real, if currently cosmetic, gap versus the WP-01 precedent this Business Activity otherwise mirrors closely: `OrganizationService.retire()` accepts entry from ACTIVE **or** SUSPENDED, treating its intermediate state as a valid retirement starting point.
- **Severity:** Low — no data-integrity or business-rule violation; a modeling choice with no canonical instruction pointing either way, surfaced by Independent Review before it could compound with future Restore (BA-09-adjacent) work.
- **Status:** Open
- **Target Resolution:** Decide, when Restore or further lifecycle work is scoped, whether `retire()` should also accept a DEPRECATED source status (mirroring `OrganizationService.retire()`'s own ACTIVE-or-SUSPENDED entry) — a small, additive change to an existing precondition, not a redesign.
- **Owning Work Package:** WP-02 — Role & Permission Management (C-003)
- **Related Business Activity:** BA-08 — Deprecate or Retire Authorization Policy Object
- **Source:** Independent Review of BA-08 (`IMP-REPORT-WP-02_Role_Permission_Management.md`)
- **Resolution Criteria:** A decision is recorded on whether DEPRECATED → RETIRED is a legal transition; if yes, `retire()` is extended to accept it across all five types with a test confirming the transition.

---

### TD-030 — Detailed Entry

- **Title:** ACCEPTED_BREAK Resolution Does Not Yet Clear BA-08's Own Dependency Gate
- **Category:** Data Integrity
- **Description:** BA-09's `resolve_conflict()` supports three resolution modes per Contract 5.6 (`REASSIGNMENT_CONFIRMED`, `NATURAL_EXPIRY_CONFIRMED`, `ACCEPTED_BREAK`). Only `ACCEPTED_BREAK` is purely a governance statement with no corresponding data change — it is recorded via `record_audit`/`publish_event` and nothing else. The other two modes naturally "clear" on re-check because the underlying dependent's own state has genuinely changed (via its own capability, e.g. Membership Management/C-007). `ACCEPTED_BREAK` has nothing to change, so `detect_conflicts()` — and therefore BA-08's own `has_active_dependents()`, which it composes — still finds the same dependent afterward.
- **Root Cause:** Two boundaries this Business Activity was instructed to respect prevent a stronger fix: (1) Contract 5.1 forbids C-003 from writing to Membership or any other dependent's own record; (2) the instruction not to revisit BA-01 through BA-08 forbids modifying `has_active_dependents()`'s own logic to consult a new "accepted break" state.
- **Impact:** An explicit, audited `ACCEPTED_BREAK` decision does not yet translate into an actual cleared path for BA-08's deprecate()/retire() to proceed — the proposing authority's statement is preserved and inspectable, but functionally inert against BA-08's own gate today.
- **Severity:** Medium — this is EX-C003-09's own central promise ("a cleared path for ERB-C003-02 to proceed") only partially realized; not a data-integrity violation, but a real gap between the capability's stated purpose and its current effect for this one resolution mode.
- **Status:** Open
- **Target Resolution:** A future, explicitly-scoped design — e.g., a short-lived, auditable "accepted break" record that BA-08's own `has_active_dependents()` is extended to consult (a deliberate, disclosed modification to BA-08, not an incidental one) — without BA-09 ever writing to a C-007-owned table.
- **Owning Work Package:** WP-02 — Role & Permission Management (C-003)
- **Related Business Activity:** BA-09 — Detect and Resolve Authorization Policy Dependency Conflict
- **Source:** BA-09 implementation (self-identified and disclosed in `resolve_conflict()`'s own docstring, not found only during review)
- **Resolution Criteria:** An ACCEPTED_BREAK resolution, once recorded, results in a subsequent BA-08 deprecate()/retire() call succeeding for that specific, named dependent; a test exists confirming this end-to-end.

---

### TD-031 — Detailed Entry

- **Title:** PLATFORM_ADMIN-Only Authorization Gate for Membership Management (EX-C007-02 Persona-Specific Defining Authority Deferred)
- **Category:** Security / Authorization Granularity
- **Description:** BA-01 (Establish Membership Context, WP-03/C-007) gates Membership establishment on the existing `PLATFORM_ADMIN` role claim only (`dependencies.require_platform_admin`, reused unchanged from WP-01/WP-02). PE-001-C007's EX-C007-02 names "Membership Steward"/"Membership Sponsor" as its Participating Personas, neither of which exists as a distinct, enforceable claim anywhere in the platform today.
- **Root Cause:** No Membership Steward/Sponsor persona claim has ever been modeled in this codebase — the same unresolved-authorization-catalog class of gap ADR-002 already names for WP-02 (TD-021), now recurring for a different capability's own personas.
- **Impact:** Any authenticated `PLATFORM_ADMIN` can establish a Membership for any Person/Organization pair, regardless of whether URA-001 would actually confer that specific defining authority to a Membership Steward or Sponsor. No privilege-escalation risk beyond what `PLATFORM_ADMIN` already holds platform-wide today; EX-C007-02's persona differentiation is simply not enforced.
- **Severity:** Low — a disclosed, deliberate simplification, the same class WP-01/WP-02 already established precedent for, not a silent gap; confirmed non-blocking by Independent Review.
- **Status:** Open
- **Target Resolution:** A Membership Steward/Sponsor persona authority model (future, separately-scoped Business Activity or architecture amendment), followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for `POST /memberships`.
- **Owning Work Package:** WP-03 — Membership Management (C-007)
- **Related Business Activity:** BA-01 — Establish Membership Context
- **Source:** BA-01 implementation (self-identified and disclosed in `MembershipService.establish()`'s own module docstring and the router's OpenAPI description; confirmed non-blocking by Independent Review)
- **Resolution Criteria:** A Membership Steward/Sponsor persona authority model exists and `POST /memberships` is gated on it instead of `PLATFORM_ADMIN`; a test exists confirming a caller lacking that persona is rejected once the real gate replaces today's interim one.

---

### TD-032 — Detailed Entry

- **Title:** `home_node_id` Is Nullable and `organization_nodes` Has No Establish Path
- **Category:** Data Integrity
- **Description:** BA-01 adds `Membership.home_node_id` as a nullable foreign key to a new, minimal `organization_nodes` table, though URA-001-17b/ERG-001-03 specify every Membership's home-node anchor as NOT NULL. When a caller supplies a `home_node_id`, BA-01 validates it references a real, active `OrganizationNode` (BR-C007-002/007) — but no Business Activity anywhere in the platform yet establishes an `OrganizationNode` row through a governed write path, so a caller cannot always supply one.
- **Root Cause:** MDP-001 explicitly excludes `organization_node` from build-time seeding ("populate exclusively through real tenant onboarding and real business operation"), and no capability currently owns an "Establish Organization Node" Business Activity — Enterprise Structure Management (C-005), the capability ERG-001-02/03 assigns this object to, has no IRA yet.
- **Impact:** A Membership can be established today with `home_node_id = NULL`, diverging from the canonical NOT NULL shape. This is disclosed, not silent, and does not violate BR-C007-002/007 (which govern a *supplied* candidate's validity, not whether one must be supplied) — but the gap is real and will need closing once C-005 exists.
- **Severity:** Medium — higher than TD-031's own Low severity, because this concerns a canonical NOT NULL constraint intentionally not enforced, not an authorization-persona simplification.
- **Status:** Open — **half-resolved.** WP-04 (Enterprise Structure Management, C-005) is now chartered (IRA-004) and BA-01 (Establish Organization Node) is implemented (`OrganizationNodeService.establish()`, `POST /organization-nodes`) — a governed write path for `organization_nodes` now exists, closing this entry's own "no Establish path" half. `home_node_id`'s nullability itself has **not** been tightened or reaffirmed — that explicit decision remains open, and is no longer a WP-03 Business Activity's own responsibility (WP-03 is `CLOSED — Certified`, WPR-001) but a future decision for either a subsequent WP-04 Business Activity or a dedicated remediation item.
- **Target Resolution:** ~~Enterprise Structure Management (C-005)'s own future "Establish Organization Node" Business Activity~~ — **done** (WP-04 BA-01). Remaining: `home_node_id`'s nullability must still be explicitly revisited (tightened to NOT NULL on newly-established Memberships, or reaffirmed nullable) — recorded as a future, separately-scoped decision, not assumed here.
- **Owning Work Package:** WP-03 — Membership Management (C-007); the "Establish Organization Node" half of this entry's resolution is credited to WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-01 — Establish Membership Context (WP-03); WP-04 BA-01 — Establish Organization Node (the resolving Business Activity)
- **Source:** BA-01 implementation (self-identified in IRA-003 §9 and `models/organization_node.py`'s own module docstring, not found only during review); status updated during WP-04 BA-01's own implementation
- **Resolution Criteria:** ~~C-005 is chartered with its own IRA and implements Establish Organization Node~~ — **satisfied.** Remaining: `home_node_id`'s nullability is explicitly revisited (tightened or reaffirmed) — this half keeps the entry Open.

---

### TD-033 — Detailed Entry

- **Title:** `role_id` Required on Membership Despite C-007's Own "Does Not Assign Roles" Boundary
- **Category:** Architecture
- **Description:** `EstablishMembershipRequest.role_id` is a required field, though PE-001-C007 states verbatim, reaffirmed at four separate points in its own text (§1.4/1.8/5.9/5.10): "C-007 does not assign or remove Roles or Permissions." Requiring `role_id` at Membership establishment reads, on its surface, as C-007 performing a Role-assignment act.
- **Root Cause:** `memberships.role_id` was declared NOT NULL in WP-00's bootstrap-era schema (predating the current IRA/capability-boundary governance process entirely) to support the login/JWT-claim-building flow. BA-01 inherits this existing column shape; it does not introduce or widen the coupling.
- **Impact:** No functional or data-integrity defect — `MembershipService.establish()` only ever writes to `memberships`, never to `roles`, `role_permissions`, or any Role/Permission table, so BR-C003-02-equivalent separation is preserved in practice. The tension is between the API's required field and the capability's own declared boundary, not in the code's actual behavior.
- **Severity:** Low — disclosed at design time (schema/service module docstrings, IRA-003 §17's own Governance Backlog Item), not discovered as a defect.
- **Status:** Open
- **Target Resolution:** A repository-owner/architecture governance decision on whether `memberships.role_id`'s NOT NULL constraint should be relaxed once C-003's own Membership-anchored Role-assignment path exists (see TD-028), reassigned to a later Business Activity's own write path, or affirmed as a correct joint Establish-time act that does not actually violate the boundary.
- **Owning Work Package:** WP-03 — Membership Management (C-007)
- **Related Business Activity:** BA-01 — Establish Membership Context
- **Source:** BA-01 implementation (self-identified in `schemas/membership.py`'s own module docstring and IRA-003 §17's own Governance Backlog Item, not found only during review)
- **Resolution Criteria:** A governance decision is recorded (an ADR, or an update to WPR-001/IRA-003) on `role_id`'s required status; `schemas/membership.py`'s own docstring is updated to reference that decision instead of disclosing an open tension.

---

### TD-034 — Detailed Entry

- **Title:** PLATFORM_ADMIN-Only Authorization Gate for Understand Membership Context (EX-C007-03 Persona-Specific Defining Authority Deferred)
- **Category:** Security / Authorization Granularity
- **Description:** BA-02 (Understand Membership Context, WP-03/C-007) gates `GET /memberships/{membership_id}` on the existing `PLATFORM_ADMIN` role claim only (`dependencies.require_platform_admin`, reused unchanged from BA-01). PE-001-C007's EX-C007-03 names Membership Sponsor, Membership Steward, Downstream Capability Consumer, and Executive as its Participating Personas, none of which exist as a distinct, enforceable claim anywhere in the platform today.
- **Root Cause:** The same unresolved-authorization-catalog gap ADR-002 already names for WP-02 (TD-021) and BA-01 already recorded for its own personas (TD-031) — no Membership Sponsor/Steward/Downstream Capability Consumer/Executive persona claim has ever been modeled in this codebase.
- **Impact:** Any authenticated `PLATFORM_ADMIN` can read any Membership's authoritative context and computed authority consequence, regardless of whether URA-001/EX-C007-03 would actually confer read access to that specific Sponsor/Steward/Consumer/Executive persona for that Membership. No privilege-escalation risk beyond what `PLATFORM_ADMIN` already holds platform-wide today; EX-C007-03's persona differentiation is simply not enforced. Same risk profile as TD-031.
- **Severity:** Low — a disclosed, deliberate simplification, the same class WP-01/WP-02/BA-01 already established precedent for, not a silent gap.
- **Status:** Open
- **Target Resolution:** A Membership Sponsor/Steward/Downstream Capability Consumer/Executive persona authority model (future, separately-scoped Business Activity or architecture amendment), followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for `GET /memberships/{membership_id}`.
- **Owning Work Package:** WP-03 — Membership Management (C-007)
- **Related Business Activity:** BA-02 — Understand Membership Context
- **Source:** BA-02 implementation (self-identified and disclosed in the router's own OpenAPI description and `membership-api.yaml`, not found only during review)
- **Resolution Criteria:** A persona-specific authorization model exists and `GET /memberships/{membership_id}` is gated on it instead of `PLATFORM_ADMIN`; a test exists confirming a caller lacking the correct persona is rejected once the real gate replaces today's interim one.

---

### TD-035 — Detailed Entry

- **Title:** PLATFORM_ADMIN-Only Authorization Gate for Maintain Membership Terms (EX-C007-04/05 Persona-Specific Defining Authority Deferred)
- **Category:** Security / Authorization Granularity
- **Description:** BA-03 (Maintain Membership Terms, WP-03/C-007) gates `POST /memberships/{membership_id}/terms` on the existing `PLATFORM_ADMIN` role claim only (`dependencies.require_platform_admin`, reused unchanged from BA-01/BA-02). PE-001-C007's EX-C007-04 (Resolve Conflicting Membership Terms) and EX-C007-05 (Change Membership Terms) both name Membership Steward/Sponsor as their Participating Personas, neither of which exists as a distinct, enforceable claim anywhere in the platform today.
- **Root Cause:** The same unresolved-authorization-catalog gap ADR-002 already names for WP-02 (TD-021) and BA-01/BA-02 already recorded for their own personas (TD-031/TD-034) — no Membership Steward/Sponsor persona claim has ever been modeled in this codebase.
- **Impact:** Any authenticated `PLATFORM_ADMIN` can change any Membership's terms, regardless of whether URA-001/EX-C007-04/05 would actually confer that specific defining authority to a Membership Steward or Sponsor. No privilege-escalation risk beyond what `PLATFORM_ADMIN` already holds platform-wide today; EX-C007-04/05's persona differentiation is simply not enforced. Same risk profile as TD-031/TD-034.
- **Severity:** Low — a disclosed, deliberate simplification, the same class WP-01/WP-02/BA-01/BA-02 already established precedent for, not a silent gap.
- **Status:** Open
- **Target Resolution:** A Membership Steward/Sponsor persona authority model (future, separately-scoped Business Activity or architecture amendment), followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for `POST /memberships/{membership_id}/terms`.
- **Owning Work Package:** WP-03 — Membership Management (C-007)
- **Related Business Activity:** BA-03 — Maintain Membership Terms
- **Source:** BA-03 implementation (self-identified and disclosed in the router's own OpenAPI description and `membership-api.yaml`, not found only during review)
- **Resolution Criteria:** A persona-specific authorization model exists and `POST /memberships/{membership_id}/terms` is gated on it instead of `PLATFORM_ADMIN`; a test exists confirming a caller lacking the correct persona is rejected once the real gate replaces today's interim one.

---

### TD-036 — Detailed Entry

- **Title:** PLATFORM_ADMIN-Only Authorization Gate for Reactivate Membership (EX-C007-08 Persona-Specific Defining Authority Deferred)
- **Category:** Security / Authorization Granularity
- **Description:** BA-06 (Reactivate Membership, WP-03/C-007) gates `POST /memberships/{membership_id}/reactivate` on the existing `PLATFORM_ADMIN` role claim only (`dependencies.require_platform_admin`, reused unchanged from BA-01/BA-02/BA-03). PE-001-C007's EX-C007-08 names Membership Steward/Sponsor as its Participating Personas, neither of which exists as a distinct, enforceable claim anywhere in the platform today.
- **Root Cause:** The same unresolved-authorization-catalog gap ADR-002 already names for WP-02 (TD-021) and BA-01/BA-02/BA-03 already recorded for their own personas (TD-031/TD-034/TD-035) — no Membership Steward/Sponsor persona claim has ever been modeled in this codebase.
- **Impact:** Any authenticated `PLATFORM_ADMIN` can attempt to reactivate any Membership, regardless of whether URA-001/EX-C007-08 would actually confer that specific defining authority to a Membership Steward or Sponsor. No privilege-escalation risk beyond what `PLATFORM_ADMIN` already holds platform-wide today — and no reactivation can currently succeed regardless of caller (TD-037) — but EX-C007-08's persona differentiation is simply not enforced.
- **Severity:** Low — a disclosed, deliberate simplification, the same class WP-01/WP-02/BA-01/BA-02/BA-03 already established precedent for, not a silent gap.
- **Status:** Open
- **Target Resolution:** A Membership Steward/Sponsor persona authority model (future, separately-scoped Business Activity or architecture amendment), followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for `POST /memberships/{membership_id}/reactivate`.
- **Owning Work Package:** WP-03 — Membership Management (C-007)
- **Related Business Activity:** BA-06 — Reactivate Membership
- **Source:** BA-06 implementation (self-identified and disclosed in the router's own OpenAPI description and `membership-api.yaml`, not found only during review)
- **Resolution Criteria:** A persona-specific authorization model exists and `POST /memberships/{membership_id}/reactivate` is gated on it instead of `PLATFORM_ADMIN`; a test exists confirming a caller lacking the correct persona is rejected once the real gate replaces today's interim one.

---

### TD-037 — Detailed Entry

- **Title:** No Reactivation Can Currently Succeed — No Canonical Authority Establishes a Permitted Standing-to-ACTIVE Transition
- **Category:** Architecture
- **Description:** BA-06's `MembershipService.reactivate()` implements BR-C007-014 and PE-001-C007's Contract 5.3 literally: a reactivation SHALL NOT be applied where no canonical authority establishes that the current standing may transition to active, and the outcome SHALL instead be explicit and unresolved or rejected. No ADR or other canonical document anywhere in this repository establishes that SUSPENDED, DEACTIVATED, or ARCHIVED may transition to ACTIVE — the identical root cause underlying BA-05's own BLOCKED — Governance Decision Required disposition. Consequently, every call to `POST /memberships/{membership_id}/reactivate` is rejected with 409, and `membership_status` is never mutated by this method, for any input, by any caller.
- **Root Cause:** URA-001-20 establishes the four canonical Membership standing states (active, suspended, deactivated, archived) but no source-to-target transition matrix; Contract 5.3 explicitly forbids C-007 from inventing one absent an explicit canonical authority. No such authority has been recorded anywhere in this repository (all five existing ADRs reviewed; none address it).
- **Impact:** None functionally adverse — this is the literal, correct, complete implementation of BR-C007-014 for today's canonical state, not a defect or a placeholder. The practical consequence is that BA-06's endpoint currently has no reachable success path; its value today is limited to (a) correctly rejecting every attempt per governed business rule, and (b) recording genuine reactivation demand in the audit trail for whoever makes the future governance decision this entry names.
- **Severity:** Medium — higher than a routine authorization-persona gap (TD-036's own class), because this concerns whether an entire Business Activity's primary success path is reachable, not merely how finely its authorization is scoped.
- **Status:** Open
- **Target Resolution:** A governance decision (most naturally a future ADR, mirroring `ADR-005`'s own interim-model precedent) explicitly establishing which Membership standing transitions are permitted — the same resolution BA-05 (TD-associated disposition, see IRA-003 §4's own BA-05 row) is itself waiting on. Once recorded, `reactivate()`'s own permission check is the sole, disclosed extension point requiring modification — not a redesign.
- **Owning Work Package:** WP-03 — Membership Management (C-007)
- **Related Business Activity:** BA-06 — Reactivate Membership
- **Source:** BA-06 implementation (self-identified during this Business Activity's own gap analysis, confirmed against PE-001-C007's primary text directly, not found only during review)
- **Resolution Criteria:** A governance decision is recorded establishing at least one permitted non-active-standing-to-ACTIVE transition; `reactivate()`'s permission check is updated to consult it; a test exists confirming a genuinely permitted reactivation succeeds and correctly mutates `membership_status`.

---

### TD-038 — Detailed Entry

- **Title:** `establish()` Does Not Route an Inactive Existing Membership to Reactivation Consideration
- **Category:** Architecture
- **Description:** PE-001-C007's own §6.3 ("Existing Membership found") states that Recognition (EX-C007-01) routes an active existing Membership to Understand or conflict classification, "and an inactive existing Membership to EX-C007-08 for a governed reactivation determination — never an assumed reactivation." BA-01's `MembershipService.establish()` does not currently perform this routing: it rejects **any** existing Membership for the same (person_id, organization_id) pair — active or not — uniformly with 409 "already exists" (BR-C007-001's own recognition discipline, as BA-01 itself implements it).
- **Root Cause:** BA-01 was implemented and independently reviewed before BA-06 (Reactivate Membership) existed to route to; its own duplicate-prevention check was correctly scoped to what existed at the time. Adding the routing now would mean modifying BA-01's own already-shipped, already-certified `establish()` method from within BA-06's implementation — a different Business Activity's own code, out of BA-06's declared scope, and the same discipline WP-02's TD-030 already established (a later Business Activity does not silently modify an earlier one's already-accepted logic without a separately-scoped decision to do so).
- **Impact:** A caller attempting to establish a Membership for a pair that already has a non-active (SUSPENDED/DEACTIVATED/ARCHIVED) Membership record receives a flat 409 "already exists" from `establish()`, rather than being routed toward BA-06's own reactivation-consideration endpoint. Since BA-06 itself cannot currently produce a successful reactivation either (TD-037), this gap has no practical consequence today beyond an imprecise error message — but it is real and should not be conflated with "BA-06 is complete."
- **Severity:** Low — a disclosed scope boundary between two Business Activities' own responsibilities, not a functional defect in either.
- **Status:** Open
- **Target Resolution:** A separately-scoped Business Activity or explicitly-reviewed amendment to `establish()`'s own duplicate-check branch, routing an inactive existing Membership to a reactivation-consideration outcome (e.g., a 409 naming the existing Membership's id and directing the caller to `POST /memberships/{id}/reactivate`) instead of a generic "already exists" 409 — decided and reviewed independently of BA-06.
- **Owning Work Package:** WP-03 — Membership Management (C-007)
- **Related Business Activity:** BA-06 — Reactivate Membership (found during its own gap analysis; the change itself belongs to BA-01's own code)
- **Source:** BA-06 implementation (self-identified during this Business Activity's own gap analysis, confirmed directly against PE-001-C007's §6.3 text)
- **Resolution Criteria:** `establish()`'s duplicate-check branch distinguishes an active existing Membership from an inactive one, routing the latter toward reactivation consideration; a test exists confirming this routing; the change is independently reviewed as its own scoped amendment to BA-01's code, not bundled silently into another Business Activity.

---

### TD-039 — Detailed Entry

- **Title:** PLATFORM_ADMIN-Only Authorization Gate for Surface Multi-Organization Membership Awareness (EX-C007-09 Persona-Specific Defining Authority Deferred)
- **Category:** Security / Authorization Granularity
- **Description:** BA-07 (Surface Multi-Organization Membership Awareness, WP-03/C-007) gates `GET /memberships/multi-organization-awareness` on the existing `PLATFORM_ADMIN` role claim only (`dependencies.require_platform_admin`, reused unchanged from BA-01/BA-02/BA-03/BA-06). PE-001-C007's EX-C007-09 names Membership Sponsor, Membership Steward, and Platform Oversight Participant as its Participating Personas, none of which exist as a distinct, enforceable claim anywhere in the platform today.
- **Root Cause:** The same unresolved-authorization-catalog gap ADR-002 already names for WP-02 (TD-021) and BA-01/BA-02/BA-03/BA-06 already recorded for their own personas (TD-031/TD-034/TD-035/TD-036) — no Membership Sponsor/Steward/Platform Oversight Participant persona claim has ever been modeled in this codebase.
- **Impact:** Any authenticated `PLATFORM_ADMIN` can query whether a given Person holds Memberships in other Organizations, regardless of whether URA-001/EX-C007-09 would actually confer that specific defining authority to a Membership Sponsor, Steward, or Platform Oversight Participant. No privilege-escalation risk beyond what `PLATFORM_ADMIN` already holds platform-wide today, and the response itself is already existence-only (BR-C007-008, TD-040) regardless of caller — EX-C007-09's persona differentiation is simply not enforced.
- **Severity:** Low — a disclosed, deliberate simplification, the same class WP-01/WP-02/BA-01/BA-02/BA-03/BA-06 already established precedent for, not a silent gap.
- **Status:** Open
- **Target Resolution:** A Membership Sponsor/Steward/Platform Oversight Participant persona authority model (future, separately-scoped Business Activity or architecture amendment), followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for `GET /memberships/multi-organization-awareness`.
- **Owning Work Package:** WP-03 — Membership Management (C-007)
- **Related Business Activity:** BA-07 — Surface Multi-Organization Membership Awareness
- **Source:** BA-07 implementation (self-identified and disclosed in the router's own OpenAPI description and `membership-api.yaml`); this detailed entry itself added during the WP-03 Independent Certification (CERT-WP-03) after the summary table row's own "See detailed entry below the table" claim was found, upon independent verification, not to be true — a genuine §19.8.2 registration-hygiene gap, corrected here.
- **Resolution Criteria:** A persona-specific authorization model exists and `GET /memberships/multi-organization-awareness` is gated on it instead of `PLATFORM_ADMIN`; a test exists confirming a caller lacking the correct persona is rejected once the real gate replaces today's interim one.

---

### TD-040 — Detailed Entry

- **Title:** No Cross-Tenant Sharing Agreement Mechanism Exists Anywhere in This Repository
- **Category:** Architecture
- **Description:** PE-001-C007's Contract 5.4 and URA-001-17a both name an "explicit, named, audited cross-tenant sharing agreement" as the sole exception path that would entitle an establishing Organization to more than an existence-only signal of a Person's Memberships elsewhere. No such mechanism — registry, table, model, or API — exists anywhere in this codebase. BA-07's `surface_multi_organization_awareness()` therefore always returns the most-restrictive, existence-only default (BR-C007-008), unconditionally, for every caller and every Organization pair.
- **Root Cause:** No capability in this repository has ever been chartered to define or implement a cross-tenant sharing agreement construct; it is named only as an exception clause within URA-001-17a/Contract 5.4's own restriction, not as a Business Object any Work Package has yet owned.
- **Impact:** None adverse today — the always-existence-only default is the complete, correct, and safest behavior for the only case that currently exists (no agreement is ever present to consult). The impact is purely one of missing future functionality: if a genuine cross-tenant sharing agreement is ever chartered, `surface_multi_organization_awareness()` would need to be extended to consult it before defaulting to existence-only.
- **Severity:** Low — a disclosed, deliberate non-delivery of an exception path with no canonical owner yet, not a defect in the default path itself, which is already fully correct.
- **Status:** Open
- **Target Resolution:** A cross-tenant sharing agreement registry/model (future, separately-scoped Business Activity or architecture amendment, requiring its own governing capability and canonical specification), after which `surface_multi_organization_awareness()` could be extended to consult it before defaulting to existence-only.
- **Owning Work Package:** WP-03 — Membership Management (C-007)
- **Related Business Activity:** BA-07 — Surface Multi-Organization Membership Awareness
- **Source:** BA-07 implementation (self-identified during this Business Activity's own gap analysis, confirmed directly against Contract 5.4 and URA-001-17a); this detailed entry itself added during the WP-03 Independent Certification (CERT-WP-03) for the same registration-hygiene reason as TD-039 (above).
- **Resolution Criteria:** A cross-tenant sharing agreement model exists and is queryable; `surface_multi_organization_awareness()` is extended to consult it before defaulting to existence-only; a test exists confirming a Person with an active sharing agreement correctly receives expanded visibility while one without still receives only the existence-only signal.

---

### TD-041 — Detailed Entry

- **Title:** EX-C007-10's Own "Authorized Aggregator" Persona Is Not Implemented (Deliberately Excluded, Not Deferred)
- **Category:** Security / Authorization Granularity
- **Description:** BA-08 (Present Person's Own Cross-Organization Membership View, WP-03/C-007) implements `GET /memberships/my-portfolio` gated on `get_current_claims` (any authenticated caller), returning only the caller's own complete Membership portfolio — `person_id` is taken exclusively from the caller's own verified JWT claims, never a query or path parameter. EX-C007-10 names a second Participating Persona, "Platform Oversight Participant where an authorized aggregator is involved," intended to let an authorized party view a *different* Person's own portfolio on their behalf. This path is not implemented.
- **Root Cause:** No distinct "authorized aggregator" claim exists anywhere in this codebase (the same unresolved-authorization-catalog gap ADR-002 already names for WP-02). Unlike every prior WP-03 Business Activity's own persona simplification (TD-031/034/035/036/039), standing the existing `PLATFORM_ADMIN` claim in for this specific persona was considered and rejected: `PLATFORM_ADMIN` is a platform-wide administrative claim with no canonical text anywhere granting it a blanket cross-tenant-visibility right, and every prior WP-03 Business Activity's own worst-case exposure under that interim gate was bounded (a single Organization's own administrative action, or an existence-only signal). Allowing `PLATFORM_ADMIN` to read *any* Person's *complete* cross-tenant Membership detail here would be a categorically larger exposure than any of those.
- **Impact:** No aggregator-assisted portfolio view exists today. A Membership Subject can always see their own portfolio (BR-C007-009 fully satisfied); an authorized third-party aggregator (e.g., a support/compliance role acting on a Person's behalf) has no endpoint to use. This is a functionality gap, not a security exposure — the exposure that a naive implementation could have introduced was avoided by not building the path at all.
- **Severity:** Medium — higher than a routine persona-authorization gap (TD-031/034/035/036/039's own Low severity), because the naive resolution (reusing `PLATFORM_ADMIN`) would itself have been a security regression, not merely an authorization-granularity simplification.
- **Status:** Open
- **Target Resolution:** An authorized-aggregator persona authority model (future, separately-scoped Business Activity or architecture amendment) with its own scoped, audited authorization dependency (e.g., `require_membership_aggregator`) — never a bare `PLATFORM_ADMIN` stand-in, given the exposure a blanket cross-tenant grant would create.
- **Owning Work Package:** WP-03 — Membership Management (C-007)
- **Related Business Activity:** BA-08 — Present Person's Own Cross-Organization Membership View
- **Source:** BA-08 implementation (self-identified during this Business Activity's own gap analysis, confirmed directly against PE-001-C007's EX-C007-10 text and Contract 5.4)
- **Resolution Criteria:** An authorized-aggregator persona authority model exists and is queryable; a persona-specific, audited authorization dependency exists for a "view another Person's portfolio" endpoint, distinct from `PLATFORM_ADMIN`; a test exists confirming an unauthorized caller (including a bare `PLATFORM_ADMIN`, absent the new persona) is rejected.

---

### TD-042 — Detailed Entry

- **Title:** PLATFORM_ADMIN-Only Authorization Gate for Hand Off Membership Context; Access Management (C-002) and Workspace Management (C-008) Have No Implementation to Hand Off To
- **Category:** Security / Authorization Granularity; Architecture
- **Description:** BA-10 (Hand Off Membership Context to a Dependent Capability, WP-03/C-007) gates `POST /memberships/{membership_id}/hand-off` on the existing `PLATFORM_ADMIN` role claim only. PE-001-C007's EX-C007-12 names Membership Steward/Downstream Capability Consumer as its Participating Personas, neither of which exists as a distinct, enforceable claim today. Separately, Contract 5.10 names exactly three dependent capabilities a hand-off may address: Role & Permission Management (C-003), Access Management (C-002), and Workspace Management (C-008). Only C-003 (WP-02) has any implementation anywhere in this repository; C-002 and C-008 are both registered Active in CAP-001 (lines 53/59) but have no Work Package (WPR-001 §2/§3).
- **Root Cause:** The persona gap is the same unresolved-authorization-catalog issue ADR-002 already names for WP-02, recurring for C-007's own personas (same class as TD-031/034/035/036/039). The C-002/C-008 gap is structural: neither capability has been chartered with its own IRA or implementation, the same class of missing-prerequisite finding as BA-04's own BLOCKED disposition (C-005) — but unlike BA-04, this does not block BA-10 itself, because C-007 never calls into any dependent capability's own API for this Business Activity (Contract 5.10's own "acceptance or rejection SHALL be explicit; C-007 SHALL NOT assume acceptance from silence" is satisfied by the caller reporting an already-resolved outcome, mirroring WP-02 BA-10's own `classify_handoff_rejection()` precedent, which itself accepts `reporting_capability="C-002"` as a plain string with no live integration behind it either).
- **Impact:** Any authenticated `PLATFORM_ADMIN` can report a hand-off outcome for any Membership to any of the three named capabilities, regardless of whether a genuine Membership Steward/Downstream Capability Consumer authorized it. No privilege-escalation risk beyond what `PLATFORM_ADMIN` already holds platform-wide today. Separately, a hand-off reported to C-002 or C-008 today can only ever mean "a caller asserts this outcome occurred" — there is no real capability on the other end to independently corroborate it, the same disclosed limitation WP-02's own analogous field already carries for C-002.
- **Severity:** Low — both aspects are disclosed, deliberate simplifications consistent with established precedent (persona gate: TD-031 and class; missing dependent capability: TD-032/BA-04's own class), not silent gaps, and neither is a security exposure beyond what `PLATFORM_ADMIN` already holds.
- **Status:** Open
- **Target Resolution:** A Membership Steward/Downstream Capability Consumer persona authority model (future, separately-scoped Business Activity or architecture amendment), followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for this endpoint. Separately, and independently, C-002's and C-008's own future Work Packages (each requiring their own IRA) would let a hand-off to them mean more than a caller-reported record.
- **Owning Work Package:** WP-03 — Membership Management (C-007)
- **Related Business Activity:** BA-10 — Hand Off Membership Context to a Dependent Capability
- **Source:** BA-10 implementation (self-identified during this Business Activity's own gap analysis, confirmed directly against PE-001-C007's Contract 5.10 text, CAP-001's own capability registry, and WPR-001's own roadmap)
- **Resolution Criteria:** A persona-specific authorization model exists and `POST /memberships/{membership_id}/hand-off` is gated on it instead of `PLATFORM_ADMIN`; separately, if/when C-002 or C-008 are chartered with their own Work Package, a decision is recorded on whether BA-10's own hand-off mechanism should be extended to a real integration for that capability specifically.

---

### TD-043 — Detailed Entry

- **Title:** `organization_nodes` Persists Only a Structural Identity Subset of the Canonical `organization_node` DDL
- **Category:** Data Integrity
- **Description:** BA-01 (Establish Organization Node, WP-04/C-005) extends `organization_nodes` with `legal_entity_name`, `business_unit`, `sector`, `operational_status`, `effective_from`, `effective_to` — the Structural Identity subset of Master Technical Architecture's canonical `organization_node` DDL (ERG-001-02's own "Structural Identity" extension context). Ten further canonical columns are not implemented: `geography_id`, `parent_available_flag`, `strategic_importance_score`, `risk_criticality_score`, `reporting_currency`, `benchmark_group`, `scenario_sensitive_flag`, `external_dependency_flag`, `entity_materiality_score`, `data_readiness_score`, `external_data_retrieval_flag`, `passport_shareable_flag`.
- **Root Cause:** `geography_id` has no `geography_registry` (or equivalent) target table anywhere in this repository to reference — adding it now would be an unconstrained, dangling UUID column with no real consumer. `parent_available_flag` is naturally derived once `organization_hierarchy` exists (BA-08's own future scope, IRA-004 §4) rather than a fact BA-01 can compute today. The materiality/risk/scenario/passport scores belong to a different, independently-governed bounded context per ERG-001-02's own "four independently-governed extension contexts" principle (Structural Identity, Authorization, Financial Consolidation, Reporting Views) — none of C-005's own ERBs/EXs (PE-001-C005) name them, and no capability in this repository currently claims them.
- **Impact:** `OrganizationNode` rows established under BA-01 cannot yet carry geography, hierarchy-readiness, or materiality/risk/scenario/passport data. This is disclosed, not silent — IRA-004 §9/§11 recorded this exact scoping decision before implementation began, mirroring WP-01 ADR-004's own precedent for `organizations` vs. `organization_master`.
- **Severity:** Low — no current Business Activity, test, or consumer requires any of the ten deferred columns; deferring them avoids inventing unconstrained columns or a bounded-context boundary violation (ERG-001-02) ahead of a real need.
- **Status:** Open
- **Target Resolution:** Enterprise Structure Management's own later Business Activities (BA-04/BA-05/BA-08 candidates per IRA-004 §4) as each concrete need for a deferred column is identified — not invented ahead of a real consumer.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-01 — Establish Organization Node
- **Source:** BA-01 implementation (self-identified during this Business Activity's own gap analysis, confirmed directly against Master Technical Architecture's `organization_node` DDL and ERG-001-02's bounded-context principle)
- **Resolution Criteria:** A future Business Activity identifies a real consumer for one of the ten deferred columns and extends `organization_nodes` accordingly, in the same additive, non-breaking style this migration (`a9f3d6e2c8b4`) used.

---

### TD-044 — Detailed Entry

- **Title:** `operational_status` and `active_flag` Are Independent, Unreconciled Lifecycle Signals on `organization_nodes`
- **Category:** Data Integrity
- **Description:** BA-01 (Establish Organization Node, WP-04/C-005) adds `operational_status` (free-text, e.g. `ACTIVE`/`INACTIVE`/`DIVESTED` per Master Technical Architecture's own DDL comment) as an independent column alongside the pre-existing `active_flag` (boolean, WP-03 BA-01). `establish()` leaves `active_flag` at its model default (`True`) and persists `operational_status` as an optional, independently-supplied value with no cross-validation between the two.
- **Root Cause:** The canonical DDL itself specifies both columns without stating their relationship — the same class of pre-existing ambiguity WP-01's own `organizations.status`/`is_active` pair carried before TD-012 resolved it. No Business Activity yet performs a governed lifecycle transition on `OrganizationNode` (BA-08, Complete Structural Transition, is the earliest candidate, per IRA-004 §4/§10), so there is no transition logic yet to reveal which field, if either, should be authoritative.
- **Impact:** A caller could establish a node with `active_flag=True` (the only value BA-01 allows, since establish() never accepts a caller-supplied `active_flag`) but `operational_status="DIVESTED"`, an internally inconsistent combination. No current code path reads `operational_status` to gate any decision, so this is a data-shape inconsistency risk, not yet a functional defect.
- **Severity:** Low — disclosed at establishment time, not discovered later; no governed transition currently depends on either field's consistency.
- **Status:** Open
- **Target Resolution:** A future Business Activity introducing real lifecycle transitions for `OrganizationNode` (mirroring WP-01's `activate()`/`suspend()`/`retire()`, TD-012's own resolution pattern) should resolve which field is authoritative, or how the two stay in sync, before either is relied upon for a governed transition.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-01 — Establish Organization Node
- **Source:** BA-01 implementation (self-identified during this Business Activity's own gap analysis, drawing the direct parallel to WP-01's own TD-012)
- **Resolution Criteria:** A governed lifecycle transition Business Activity for `OrganizationNode` exists and explicitly states which of `active_flag`/`operational_status` is authoritative, or how both are kept consistent.

---

### TD-045 — Detailed Entry

- **Title:** `GET /organization-nodes/{id}` Realizes Only the Single-Node Half of EX-C005-03's Purpose — No "Surrounding Relationships" Traversal
- **Category:** Architecture
- **Description:** BA-02 (Understand Structural Position, WP-04/C-005) implements `OrganizationNodeService.get_details()` / `GET /organization-nodes/{id}`, returning a single `OrganizationNode`'s own Structural Identity fields (the same six columns BA-01 established, plus the base identity columns). PE-001-C005's EX-C005-03 Purpose text states "understand surrounding structural context and position" and ERB-C005-02's Purpose states "how the active Structural Focus relates to surrounding enterprise context" — both describe relationship traversal, not single-record retrieval alone.
- **Root Cause:** `organization_hierarchy` (the ERG-001-specified table that would carry parent/child or other structural relationships between `organization_node` rows) does not exist anywhere in this repository — confirmed by direct grep, zero matches. IRA-004 §7/§9 already disclosed this as real, future WP-04 work (BA-08 candidate, "Complete Structural Transition"), not BA-01's or BA-02's own scope.
- **Impact:** A caller of `GET /organization-nodes/{id}` today receives orientation about the node itself but no relationship context (parent node, child nodes, or any other structural linkage) — EX-C005-03's own "surrounding" half of its Purpose is not yet realized by any endpoint. Not a defect against BA-02's own minimal Query scope (IRA-004 §4 records BA-02 as `Query` over `EnterpriseNode (+ relationships)`, with the parenthetical itself flagging relationships as the not-yet-covered part), but a real, disclosed capability gap versus the full PE-001-C005 experience text.
- **Severity:** Low — no current Business Activity, test, or consumer requires relationship traversal; deferring it avoids inventing `organization_hierarchy` (a new table, an architectural-impact-assessment-triggering change per CLAUDE.md §19.4) ahead of a real, scoped Business Activity for it.
- **Status:** Open
- **Target Resolution:** A future Business Activity that introduces `organization_hierarchy` (BA-08, Complete Structural Transition, is the earliest named candidate per IRA-004 §4) and extends `GET /organization-nodes/{id}` (or a dedicated relationships endpoint) to traverse it.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-02 — Understand Structural Position
- **Source:** BA-02 implementation (self-identified during this Business Activity's own gap analysis, drawing directly on IRA-004 §4's own "(+ relationships)" annotation and EX-C005-03's Purpose text)
- **Resolution Criteria:** `organization_hierarchy` exists and a Business Activity explicitly traverses it to satisfy EX-C005-03's "surrounding structural context" Purpose.

---

### TD-046 — Detailed Entry

- **Title:** BA-01B (Verify Organization Domain Claim) Has No Real Proof-of-Control Mechanism
- **Category:** Security
- **Description:** BA-01B (Verify Organization Domain Claim, WP-01A/C-004, IRA-001A) records a verification outcome (`verified: bool`) supplied directly by the caller — an authorized, audited, traceable act satisfying BR-C004-02/BR-C004-09's literal requirement that verification be a recorded decision, never a silent default. It does not itself independently confirm domain control (no DNS TXT record check, no email-token proof-of-control flow).
- **Root Cause:** PE-001-C004's own "governed no-domain activation path" explicitly licenses proceeding without any real domain verification at all — the specification treats the *distinctness and traceability* of the verification decision as the constitutional requirement, not the cryptographic strength of the proof behind it. No real proof-of-control mechanism exists anywhere in this repository to reuse.
- **Impact:** A caller with PLATFORM_ADMIN access can mark any claimed domain "VERIFIED" without independent confirmation. No current dependent capability (C-001/URA-001 SSO domain-based provisioning) yet consumes this fact for trust decisions, so the exposure is currently theoretical, not active.
- **Severity:** Low — disclosed at implementation time; no current consumer trusts this fact for anything security-relevant.
- **Status:** Open
- **Target Resolution:** A real proof-of-control mechanism, built as its own future, separately-scoped Business Activity once C-001/URA-001's SSO domain-based provisioning (or any other genuine domain-trust consumer) actually exists.
- **Owning Work Package:** WP-01A — Organization Management Constitutional Correction (C-004)
- **Related Business Activity:** BA-01B — Verify Organization Domain Claim
- **Source:** BA-01B implementation (self-identified during IRA-001A's own gap analysis, drawing directly on PE-001-C004's own no-domain-path licensing text)
- **Resolution Criteria:** A named proof-of-control mechanism exists and is exercised by BA-01B before marking a domain claim VERIFIED.

---

### TD-047 — Detailed Entry

- **Title:** `MembershipService.establish()` (WP-03) Derives Organization Existence Independently, Bypassing C-004's Resolution Authority
- **Category:** Security
- **Description:** `MembershipService.establish()` (`Backend/Services/AuthService/services/membership_service.py`, WP-03/C-007, created 2026-07-29) calls `self.organization_repo.get_by_id(request.organization_id)` directly — a raw repository call, not any C-004-owned resolution method — and checks only `organization is None`. BR-C004-03 states: "Organization existence and validity SHALL be resolved exclusively through EX-C004-05; no dependent capability SHALL derive it independently."
- **Root Cause:** WP-03 was implemented independently of C-004's own constitutional text; the direct-repository-access pattern mirrors WP-03's own established pattern for its other FK checks (role, person) without a distinct C-004 resolution contract to call instead at the time.
- **Impact:** No `.status` check is applied at all — a `SUSPENDED` or `RETIRED` Organization is equally consumable for new Membership creation as an `ACTIVE` one, and the resolution bypasses whatever future EX-C004-05-conformant contract C-004 might define (TD-048).
- **Severity:** Medium — a real, currently-exploitable gap (not merely theoretical), pre-existing since WP-03's own implementation and not introduced by IRA-001A.
- **Status:** Open
- **Target Resolution:** A WP-03-owned amendment to `MembershipService.establish()`, either calling a genuine C-004 resolution method with a status check, or an explicit WP-03 governance decision to formally accept the current direct-access pattern with its own disclosed rationale.
- **Owning Work Package:** WP-03 — Membership Management (C-007) — **not WP-01A**; IRA-001A does not modify `membership_service.py`.
- **Related Business Activity:** WP-03 BA-01 — Establish Membership Context
- **Source:** IRA-001A's own gap analysis (found while verifying BR-C004-03 conformance across the codebase during the C-004 constitutional correction; a WP-03 finding surfaced by WP-01A's review, not a WP-01A defect)
- **Resolution Criteria:** `MembershipService.establish()` resolves Organization validity through a C-004-owned contract that includes a status check, or WP-03 governance formally accepts the current pattern.

---

### TD-048 — Detailed Entry

- **Title:** BA-02 (`get_details()`) Does Not Realize EX-C004-05's Typed Organization Validity Context Contract
- **Category:** Architecture
- **Description:** PE-001-C004's EX-C004-05 specifies a Produced Context of "Organization Validity Context (ACTIVE, SUSPENDED, RETIRED, or NOT_FOUND)." `OrganizationService.get_details()` (BA-02) returns either full Organization details (200) or a 404 — a superset response a caller must interpret to derive validity, not a purpose-built validity-only resolution matching EX-C004-05's own typed contract.
- **Root Cause:** BA-02 was originally scoped as "View Organization Details" (a read/display concern), not explicitly bound to EX-C004-05's resolution contract; no dependent capability has yet needed the narrower, typed resolution.
- **Impact:** Low today — every current caller (BA-02's own API consumers) wants full details anyway. Becomes relevant only if/when a dependent capability needs a lightweight, typed existence/validity check without the full detail payload (which would also naturally provide the single, authoritative resolution point BR-C004-03/TD-047 needs).
- **Severity:** Low — no current consumer requires the narrower contract.
- **Status:** Open
- **Target Resolution:** A future Business Activity or capability need that requires a typed, validity-only resolution — not invented speculatively ahead of that need.
- **Owning Work Package:** WP-01A — Organization Management Constitutional Correction (C-004)
- **Related Business Activity:** BA-02 — Resolve Organization Details (pre-existing, unmodified by IRA-001A)
- **Source:** IRA-001A's own gap analysis (found while reviewing whether any existing endpoint already realizes EX-C004-05)
- **Resolution Criteria:** A Business Activity or endpoint exists that returns EX-C004-05's own typed `ACTIVE`/`SUSPENDED`/`RETIRED`/`NOT_FOUND` resolution as its primary contract.

---

### TD-049 — Detailed Entry

- **Title:** Frontend Organization-Establishment UI Calls the Removed `POST /organizations` Endpoint
- **Category:** UX
- **Description:** `source/frontend/src/features/organization/components/OrganizationManagementScreen.tsx`, `state/useEstablishOrganization.ts`, and `services/organization-api.ts` all call `POST /organizations` and assume BA-01's original synchronous-ACTIVE-establishment response — that endpoint no longer exists after IRA-001A's correction (relocated to `POST /organization-establishment-attempts`, followed by a distinct activation step).
- **Root Cause:** IRA-001A is explicitly scoped backend-only, the same precedent BA-05/BA-06/BA-07 each established for their own WP-01 scope — no canonical document requires this correction to also update the frontend, and doing so was judged out of the constitutional-correction's own minimal scope.
- **Impact:** Establishing a new Organization through the existing Platform Administrator UI will now fail (404 Not Found) until the frontend is updated — a real, user-facing regression for that one flow, not merely a latent gap. Every other Organization Management UI flow (View, Search, Update, Activate, Suspend, Retire) is unaffected.
- **Severity:** Medium — real, immediate breakage of one existing UI flow, correctly disclosed rather than silently left for a user to discover.
- **Status:** Open
- **Target Resolution:** A frontend follow-up pass updating the Establish Organization UI flow to the new two-step `POST /organization-establishment-attempts` → `POST /organization-establishment-attempts/{id}/activate` sequence.
- **Owning Work Package:** WP-01A — Organization Management Constitutional Correction (C-004) (frontend remediation itself may be picked up by any future WP-01-adjacent frontend pass)
- **Related Business Activity:** BA-01 (amended) — Establish Organization Identity
- **Source:** IRA-001A's own disclosure (self-identified during the correction's own scope-boundary review, consistent with every prior WP-01 scope-reduction decision being explicitly disclosed rather than silently left for discovery)
- **Resolution Criteria:** The frontend Establish Organization flow successfully creates and activates an Organization through the new two-step API.

---

### TD-051 — Detailed Entry

- **Title:** No `GET` Read Endpoint Exists for Structural Change Intent
- **Category:** Architecture
- **Description:** WP-04 BA-03 (Frame Structural Change Intent, SCI-000001) implements `POST /structural-change-intents` only. EX-C005-05's own Required/Consumed Context ("Change Intent Context and current structural context") establishes that a later, independently-invoked experience must retrieve a previously-framed intent by identity — but IRA-004 §4 scopes BA-03 as `Type: Create` only, mirroring BA-01/BA-02's own precedent of a create-then-read split across two separate Business Activities.
- **Root Cause:** The BA-03 readiness assessment explicitly left "whether BA-03 also needs its own read endpoint" undecided, deferring it as BA-03's own first disclosed implementation decision rather than assuming an answer. This implementation makes the minimal choice (create only), consistent with "do not absorb BA-04 functionality."
- **Impact:** None today — no Business Activity yet consumes a previously-framed Structural Change Intent. Becomes real friction only once BA-04 (Shape Structural Proposal) is implemented and needs to resolve a Change Intent Context by id.
- **Severity:** Low — no current consumer exists; the create response already returns every field a caller needs immediately after framing.
- **Status:** Open
- **Target Resolution:** BA-04's own future implementation-readiness gap analysis decides whether a dedicated `GET /structural-change-intents/{id}` is required, or whether an internal (non-HTTP) repository lookup suffices for that Business Activity's own service-layer needs.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-03 — Frame Structural Change Intent
- **Source:** BA-03 implementation (self-identified during this Business Activity's own gap analysis)
- **Resolution Criteria:** A read path for Structural Change Intent exists, if and only if BA-04's own gap analysis determines one is required.

---

### TD-052 — Detailed Entry

- **Title:** Structural Change Intent Lifecycle Transitions Beyond CREATED Are Not Implemented
- **Category:** Architecture
- **Description:** `StructuralChangeIntent.status` (`models/structural_change_intent.py`) is constrained to IRA-004 §21's full registered Lifecycle Model — CREATED, MODIFIED, SUPERSEDED, ABANDONED, WITHDRAWN, ARCHIVED — but BA-03's own service (`StructuralChangeIntentService.frame_change_intent()`) only ever persists CREATED. No code path anywhere in this repository sets any other value.
- **Root Cause:** BA-03, as scoped in IRA-004 §4 ("Create (governed decision record)"), realizes only ERB-C005-03/EX-C005-04 (Frame). MODIFIED corresponds to intent revision, SUPERSEDED/ABANDONED to EX-C005-04's own Invalidated Context, and WITHDRAWN to PE-001-C005 §43.3's distinct exception path — each belongs to a later stage of the C-005 journey (BA-04 revision, BA-06/BA-07 review/validation-triggered invalidation, or an explicit withdrawal action), not to the initial Frame act.
- **Impact:** None today — mirrors BA-01's own identical, already-accepted disposition of not implementing BR-C005-001 through -010's full governed-transition workflow (IRA-004 §5). The CheckConstraint documents SCI-000001's actual registered lifecycle so the schema is not narrower than the Business Object's own constitution, but no transition logic exists yet.
- **Severity:** Low — consistent with, not a departure from, this Work Package's established minimal-slice discipline.
- **Status:** Open
- **Target Resolution:** BA-04 through BA-08's own future gap analyses, each realizing the lifecycle transition its own stage implies.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-03 — Frame Structural Change Intent
- **Source:** BA-03 implementation (self-identified, mirroring IRA-004 §5's own precedent disclosure for BA-01)
- **Resolution Criteria:** Each of MODIFIED/SUPERSEDED/ABANDONED/WITHDRAWN/ARCHIVED has a real, tested code path once the Business Activity that owns that transition is implemented.

---

### TD-053 — Detailed Entry

- **Title:** Proposed Outcome Context Lifecycle Transitions Beyond CREATED/SUPERSEDED Are Not Implemented
- **Category:** Architecture
- **Description:** `StructuralProposal.status` (`models/structural_proposal.py`) is constrained to IRA-004 §22's full registered Lifecycle Model — CREATED, SUPERSEDED, VALIDATED, ARCHIVED — but BA-04's own service (`StructuralProposalService`) only ever writes CREATED (Shape/Refine) and SUPERSEDED (a revision closed by a later Refine). No code path sets VALIDATED or ARCHIVED.
- **Root Cause:** BA-04, as scoped in IRA-004 §4 ("Create / Update (proposal)"), realizes only ERB-C005-04/EX-C005-05/-06 (Shape, Refine). VALIDATED corresponds to BR-C005-005's own readiness marker, owned by the future BA-07 (Validate Transition Readiness); ARCHIVED is a terminal state reachable only after a full completion/retirement path exists.
- **Impact:** None today — mirrors BA-03's own identical, already-accepted disposition (TD-052) of not implementing every registered lifecycle value in its own first Business Activity.
- **Severity:** Low — consistent with, not a departure from, this Work Package's established minimal-slice discipline.
- **Status:** Open
- **Target Resolution:** BA-07's own future gap analysis decides how readiness is represented (a status value on this same table, a separate column, or a separate table) before writing VALIDATED; a future retirement path reaches ARCHIVED.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-04 — Shape / Refine Proposed Structural Outcome
- **Source:** BA-04 implementation (self-identified, mirroring TD-052's own precedent disclosure for SCI-000001)
- **Resolution Criteria:** VALIDATED and ARCHIVED each have a real, tested code path once the Business Activity that owns that transition is implemented.

---

### TD-054 — Detailed Entry

- **Title:** "Initial Comparison Context" Is Not Persisted or Computed by BA-04
- **Category:** Architecture
- **Description:** EX-C005-05's own Produced Context is "Proposed Outcome Context **and initial Comparison Context**." BA-04 implements only the former — `StructuralProposalResponse` carries no comparison/diff information between the current authoritative structural context and the proposed outcome.
- **Root Cause:** Comparison Context was checked against the Cross-Experience Reference Test during BA-04's own implementation-readiness assessment and found to fail it (named only within EX-C005-05's own text, never required by a later Enterprise Experience) — it is therefore not itself a registered Business Object requiring CBOR registration. However, PE-001-C005's own text does not specify what is compared or how, so building any concrete diff representation now would be inventing a mechanism beyond BA-04's own disclosed minimal scope.
- **Impact:** None today — no test, endpoint, or consumer expects comparison output; EX-C005-05's own Produced Context is only partially realized, disclosed rather than silently claimed complete.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** A future refinement of BA-04 (or a dedicated future Business Activity) once a concrete comparison representation is actually needed by a real caller — not invented speculatively ahead of that need.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-04 — Shape / Refine Proposed Structural Outcome
- **Source:** BA-04 implementation (self-identified during this Business Activity's own gap analysis)
- **Resolution Criteria:** A comparison/diff representation exists and is returned alongside Proposed Outcome Context, once its shape is deliberately decided rather than assumed.

---

### TD-055 — Detailed Entry

- **Title:** No `GET` Read Endpoint Exists for Proposed Outcome Context
- **Category:** Architecture
- **Description:** BA-04 implements `POST /structural-proposals` (Shape) and `POST /structural-proposals/{proposal_id}/revisions` (Refine) only. No endpoint retrieves an existing proposal or its current/full revision history.
- **Root Cause:** IRA-004 §4 types BA-04 as `Create / Update (proposal)` only — no `Query` type is listed, the identical scoping precedent TD-051 already established for BA-03/Structural Change Intent.
- **Impact:** None today — the Shape/Refine response bodies already return every field a caller needs immediately after each call. Becomes real friction once BA-05 (Assess Structural Consequence) needs to resolve a proposal by id independently.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** BA-05's own future implementation-readiness gap analysis decides whether a dedicated `GET /structural-proposals/{proposal_id}` (current revision, or full history) is required, or whether an internal repository-level lookup suffices.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-04 — Shape / Refine Proposed Structural Outcome
- **Source:** BA-04 implementation (self-identified, mirroring TD-051's own identical precedent)
- **Resolution Criteria:** A read path for Proposed Outcome Context exists, if and only if BA-05's own gap analysis determines one is required.

---

### TD-056 — Detailed Entry

- **Title:** Concurrent Refine Calls Can Race on `revision_number`
- **Category:** Concurrency
- **Description:** `structural_proposals` has no unique constraint spanning `(proposal_id, revision_number)`. `StructuralProposalService.refine_proposal()` reads the current revision, then inserts a new row with `revision_number + 1` — two concurrent calls against the same `proposal_id` could both read the same current revision and both insert a row claiming the same `revision_number`, producing two rows with identical `(proposal_id, revision_number)` instead of a detected 409-class conflict.
- **Root Cause:** No optimistic-concurrency or unique-constraint guard was added for the revision-increment path — the same class of gap TD-005/TD-006 already recorded for WP-01's own concurrent-duplicate-`organization_code` race, not a newly-invented category of risk.
- **Impact:** Low today — `PLATFORM_ADMIN`-only access makes simultaneous Refine calls against the same proposal unlikely in practice; no test or consumer currently depends on `revision_number` uniqueness being enforced at the database level.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** Add a unique constraint on `(proposal_id, revision_number)` plus a dedicated concurrency test asserting the second concurrent Refine call receives a conflict response rather than silently succeeding, mirroring TD-005's own resolution pattern.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-04 — Shape / Refine Proposed Structural Outcome
- **Source:** BA-04 implementation (self-identified during this Business Activity's own gap analysis)
- **Resolution Criteria:** A concurrent second Refine call against the same current revision receives a deterministic conflict response, not a silent duplicate `revision_number`.

---

### TD-057 — Detailed Entry

- **Title:** Impact Context Lifecycle Transitions Beyond CREATED Are Not Implemented
- **Category:** Architecture
- **Description:** `ImpactAssessment.status` (`models/impact_assessment.py`) is constrained to IRA-004 §23's full registered Lifecycle Model — CREATED, INVALIDATED, ARCHIVED — but BA-05's own service (`ImpactAssessmentService`) only ever writes CREATED.
- **Root Cause:** EX-C005-07's own Invalidated Context ("Impact observations invalidated by material proposal revision") ties invalidation to an event owned by BA-04 (`refine_proposal()`), not BA-05. Implementing it would require BA-05's own code to reach into BA-04's already-implemented, already-reviewed flow — explicitly out of scope ("implement only what BA-05 owns").
- **Impact:** None today — mirrors BA-03/BA-04's own identical, already-accepted disposition (TD-052/TD-053) of not implementing every registered lifecycle value in a Business Activity's own first pass.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** A future cross-cutting mechanism (e.g., BA-04's `refine_proposal()` itself invalidating dependent Impact Context rows) or BA-06's own gap analysis, once review readiness actually depends on this distinction.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-05 — Assess Structural Consequence
- **Source:** BA-05 implementation (self-identified, mirroring TD-052/TD-053's own precedent)
- **Resolution Criteria:** INVALIDATED and ARCHIVED each have a real, tested code path once the mechanism that owns each transition is implemented.

---

### TD-058 — Detailed Entry

- **Title:** No `GET` Read Endpoint Exists for Impact Context
- **Category:** Architecture
- **Description:** BA-05 implements `POST /impact-assessments` only. No endpoint retrieves an existing assessment by id or lists assessments for a given proposal.
- **Root Cause:** Mirrors TD-051/TD-055's identical scoping precedent — no read path was scoped for this Business Activity's own first pass.
- **Impact:** None today — the create response already returns every field a caller needs immediately after assessment. Becomes real friction once BA-06 (Review Proposed Structural Outcome) needs to resolve an assessment by id independently.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** BA-06's own future implementation-readiness gap analysis decides whether a dedicated `GET /impact-assessments/{id}` (or a proposal-scoped list) is required.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-05 — Assess Structural Consequence
- **Source:** BA-05 implementation (self-identified, mirroring TD-051/TD-055's own identical precedent)
- **Resolution Criteria:** A read path for Impact Context exists, if and only if BA-06's own gap analysis determines one is required.

---

### TD-059 — Detailed Entry

- **Title:** Assess Structural Consequence Does Not Verify the Referenced Proposal Revision Is Still Current
- **Category:** Architecture
- **Description:** `POST /impact-assessments` accepts any existing `structural_proposal_id`, including a revision a later `Refine` call has already marked `SUPERSEDED`. No check compares the referenced revision against its own lineage's current revision.
- **Root Cause:** EX-C005-07's own Trigger text ("A coherent proposed structural outcome exists") does not explicitly require the assessed revision be the current one, so BA-05's own implementation neither assumed nor enforced currency either way — a disclosed, deliberate non-decision rather than a silent gap.
- **Impact:** Low today — no consumer currently depends on assessments only existing against current revisions; a caller could in principle assess a stale revision, producing an Impact Context that is itself immediately stale.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** A future revisit of BA-05, or BA-06's own review-readiness gap analysis, decides whether assessing a superseded revision should be rejected (409-class), allowed with a warning, or remains permitted as legitimate historical analysis.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-05 — Assess Structural Consequence
- **Source:** BA-05 implementation (self-identified during this Business Activity's own gap analysis)
- **Resolution Criteria:** A deliberate decision (not silence) governs whether superseded-revision assessment is permitted, and that decision is enforced and tested.

---

### TD-060 — Detailed Entry

- **Title:** Review Context Concerns Are a Single Text Field, Not Structured Per-Concern Records
- **Category:** Architecture
- **Description:** `StructuralReview.concerns` (`models/structural_review.py`) is one Text column, appended to (never overwritten) by `resolve_concerns()`. §41.16's own Collaboration Contract text — "Review concerns SHALL preserve author, decision context and unresolved/resolved status by reference to owning mechanisms" — describes concerns with per-item structure (an author, a context, an individually-tracked status), which a single free-text field cannot represent.
- **Root Cause:** Building a dedicated per-concern child table (author, timestamp, individual resolved/unresolved status) ahead of any real, identified consumer needing that granularity would be speculative schema design, the same class of over-building ADR-004's own Rationale already rejected for WP-01's Organization schema. BA-06's own v1 scope is deliberately minimal, mirroring every prior Business Activity in this Work Package.
- **Impact:** None today — no test, endpoint, or consumer requires per-concern granularity; the single-field representation satisfies BR-C005-007's own literal text ("Unresolved review concerns SHALL prevent completion...") since the whole review's own status already gates completion via `CONCERNS_RESOLVED`.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** A future revisit of BA-06 (or a dedicated future Business Activity) introduces structured per-concern tracking once a real consumer — e.g., a collaboration/messaging integration — actually needs individually-addressable concerns.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-06 — Review Proposed Structural Outcome / Resolve Structural Review Concerns
- **Source:** BA-06 implementation (self-identified during this Business Activity's own gap analysis, directly against §41.16's own text)
- **Resolution Criteria:** Individual concerns can be authored, addressed, and independently marked resolved/unresolved without renegotiating the single-field representation.

---

### TD-061 — Detailed Entry

- **Title:** No `GET` Read Endpoint Exists for Review Context
- **Category:** Architecture
- **Description:** BA-06 implements `POST /structural-reviews` and `POST /structural-reviews/{id}/resolve-concerns` only. No endpoint retrieves an existing review by id or lists reviews for a given proposal.
- **Root Cause:** Mirrors TD-051/TD-055/TD-058's identical scoping precedent — no read path was scoped for this Business Activity's own first pass; IRA-004 §4 types BA-06 as "Update (review)," not "Query."
- **Impact:** None today — both create and resolve responses already return every field a caller needs immediately. Becomes real friction once BA-07 (Validate Transition Readiness) needs to resolve a review by id independently.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** BA-07's own future implementation-readiness gap analysis decides whether a dedicated `GET /structural-reviews/{id}` is required.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-06 — Review Proposed Structural Outcome / Resolve Structural Review Concerns
- **Source:** BA-06 implementation (self-identified, mirroring TD-051/TD-055/TD-058's own identical precedent)
- **Resolution Criteria:** A read path for Review Context exists, if and only if BA-07's own gap analysis determines one is required.

---

### TD-062 — Detailed Entry

- **Title:** Review Context Lifecycle Transitions Beyond CREATED/CONCERNS_RESOLVED Are Not Implemented
- **Category:** Architecture
- **Description:** `StructuralReview.status` (`models/structural_review.py`) is constrained to IRA-004 §25's full registered Lifecycle Model — CREATED, CONCERNS_RESOLVED, INVALIDATED, ARCHIVED — but BA-06's own service only ever writes CREATED and CONCERNS_RESOLVED.
- **Root Cause:** EX-C005-08's own Invalidated Context ("Prior review position if the reviewed revision changes materially") ties invalidation to an event owned by BA-04 (`refine_proposal()`), not BA-06 — the identical root cause already disclosed for Impact Context (TD-057).
- **Impact:** None today — mirrors BA-03/BA-04/BA-05's own identical, already-accepted disposition (TD-052/053/057) of not implementing every registered lifecycle value in a Business Activity's own first pass.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** A future cross-cutting mechanism (e.g., BA-04's `refine_proposal()` itself invalidating dependent Review Context rows, alongside Impact Context per TD-057) or BA-07's own gap analysis.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-06 — Review Proposed Structural Outcome / Resolve Structural Review Concerns
- **Source:** BA-06 implementation (self-identified, mirroring TD-052/053/057's own precedent)
- **Resolution Criteria:** INVALIDATED and ARCHIVED each have a real, tested code path once the mechanism that owns each transition is implemented.

---

### TD-063 — Detailed Entry

- **Title:** Review Creation and Concern Resolution Do Not Verify the Referenced Proposal Revision Is Still Current
- **Category:** Architecture
- **Description:** Neither `POST /structural-reviews` nor `POST /structural-reviews/{id}/resolve-concerns` checks whether the referenced `structural_proposal_id` is still the current (non-`SUPERSEDED`) revision of its own lineage.
- **Root Cause:** Identical to TD-059 (Impact Context) — PE-001-C005's own text does not explicitly require currency for either EX-C005-08 or EX-C005-09, so this was disclosed rather than assumed either way, consistent with TD-059's own precedent applied to a second object.
- **Impact:** Low today — no consumer currently depends on reviews only existing against current revisions.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** A future revisit of BA-06, or BA-07's own gap analysis, decides whether reviewing/resolving against a superseded revision should be rejected, allowed with a warning, or remains permitted — the same decision TD-059 already defers for Impact Context, ideally resolved once for both objects together.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-06 — Review Proposed Structural Outcome / Resolve Structural Review Concerns
- **Source:** BA-06 implementation (self-identified, mirroring TD-059's own precedent)
- **Resolution Criteria:** A deliberate decision (not silence) governs whether superseded-revision review/resolution is permitted, and that decision is enforced and tested — ideally applied consistently to both TD-059 and TD-063 at once.

---

### TD-064 — Detailed Entry

- **Title:** No `GET` Read Endpoint Exists for Validation Context
- **Category:** Architecture
- **Description:** BA-07 implements `POST /structural-validations` only. No endpoint retrieves an existing validation by id or lists validations for a given proposal.
- **Root Cause:** Mirrors TD-051/TD-055/TD-058/TD-061's identical scoping precedent — no read path was scoped for this Business Activity's own first pass; IRA-004 §4 types BA-07 as "Update (validation)," not "Query."
- **Impact:** None today — the create response already returns every field a caller needs immediately. Becomes real friction once BA-08 (Complete Structural Transition) needs to resolve a validation by id independently.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** BA-08's own future implementation-readiness gap analysis decides whether a dedicated `GET /structural-validations/{id}` is required.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-07 — Validate Transition Readiness
- **Source:** BA-07 implementation (self-identified, mirroring TD-051/055/058/061's own identical precedent)
- **Resolution Criteria:** A read path for Validation Context exists, if and only if BA-08's own gap analysis determines one is required.

---

### TD-065 — Detailed Entry

- **Title:** Validation Context Lifecycle Transitions Beyond CREATED Are Not Implemented
- **Category:** Architecture
- **Description:** `StructuralValidation.status` (`models/structural_validation.py`) is constrained to IRA-004 §26's full registered Lifecycle Model — CREATED, INVALIDATED, ARCHIVED — but BA-07's own service only ever writes CREATED.
- **Root Cause:** EX-C005-10's own Invalidated Context ("Readiness when proposal or material enterprise context changes") ties invalidation to an event owned by BA-04 (`refine_proposal()`), not BA-07 — the identical root cause already disclosed for Impact Context (TD-057) and Review Context (TD-062).
- **Impact:** None today — mirrors BA-03/BA-04/BA-05/BA-06's own identical, already-accepted disposition (TD-052/053/057/062) of not implementing every registered lifecycle value in a Business Activity's own first pass.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** A future cross-cutting mechanism (e.g., BA-04's `refine_proposal()` itself invalidating dependent Impact/Review/Validation Context rows together) or BA-08's own gap analysis.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-07 — Validate Transition Readiness
- **Source:** BA-07 implementation (self-identified, mirroring TD-052/053/057/062's own precedent)
- **Resolution Criteria:** INVALIDATED and ARCHIVED each have a real, tested code path once the mechanism that owns each transition is implemented.

---

### TD-066 — Detailed Entry

- **Title:** Only BR-C005-007 Is Enforced as a Readiness Gate — Other Potential Readiness Criteria Are Not Implemented
- **Category:** Architecture
- **Description:** `POST /structural-validations` hard-enforces exactly one readiness criterion: the referenced review must be `CONCERNS_RESOLVED` (BR-C005-007). EX-C005-10's own AI Assistance clause — "AI MAY identify missing context or apparent inconsistencies" — implies validation readiness could depend on further criteria (completeness of required context, structural inconsistency detection) that this Business Activity does not evaluate.
- **Root Cause:** BR-C005-007 is the only readiness criterion PE-001-C005 states as a Business Rule (a SHALL); "missing context" and "apparent inconsistencies" are named only within an advisory AI Assistance clause, not as enforceable rules — building enforcement for them now would be inventing business rules PE-001-C005 itself does not state, beyond this Business Activity's own minimal, disclosed scope.
- **Impact:** None today — no test, endpoint, or consumer requires additional readiness criteria; BR-C005-007 is the only rule this repository's own governing text makes mandatory.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** A future revisit of BA-07 once a concrete additional readiness criterion is elevated from advisory AI guidance to an actual enforceable Business Rule by a future PE-001-C005 revision or ADR.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-07 — Validate Transition Readiness
- **Source:** BA-07 implementation (self-identified during this Business Activity's own gap analysis, directly against EX-C005-10's own text)
- **Resolution Criteria:** A deliberate decision (not silence) governs whether any further readiness criterion becomes enforceable, and if so, is implemented and tested.

---

### TD-067 — Detailed Entry

- **Title:** Validation Does Not Verify the Referenced Proposal Revision Is Still Current
- **Category:** Architecture
- **Description:** `POST /structural-validations` does not check whether the referenced `structural_proposal_id` is still the current (non-`SUPERSEDED`) revision of its own lineage.
- **Root Cause:** Identical to TD-059 (Impact Context) and TD-063 (Review Context) — PE-001-C005's own text does not explicitly require currency for EX-C005-10, so this was disclosed rather than assumed either way, consistent with precedent applied to a third object.
- **Impact:** Low today — no consumer currently depends on validations only existing against current revisions.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** A future revisit of BA-07, or BA-08's own gap analysis, decides whether validating against a superseded revision should be rejected, allowed with a warning, or remains permitted — ideally resolved once for TD-059/TD-063/TD-067 together.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-07 — Validate Transition Readiness
- **Source:** BA-07 implementation (self-identified, mirroring TD-059/TD-063's own precedent)
- **Resolution Criteria:** A deliberate decision (not silence) governs whether superseded-revision validation is permitted, and that decision is enforced and tested.

---

### TD-068 — Detailed Entry

- **Title:** No `GET` Read Endpoint Exists for Resulting Structural Context
- **Category:** Architecture
- **Description:** BA-08 implements `POST /structural-completions` only. No endpoint retrieves an existing completion by id.
- **Root Cause:** Mirrors TD-051/TD-055/TD-058/TD-061/TD-064's identical scoping precedent — no read path was scoped for this Business Activity's own first pass.
- **Impact:** None today — the create response already returns every field a caller needs immediately. Was real friction once BA-09 (Continue from Resulting Structure) needed to resolve a completion by id — now resolved.
- **Severity:** Low.
- **Status:** **Closed** (resolved by BA-09)
- **Target Resolution:** ~~BA-09's own future implementation-readiness gap analysis decides whether a dedicated `GET /structural-completions/{id}` is required.~~ **Resolved:** BA-09's own readiness assessment confirmed one was required (EX-C005-12's own "transfer resulting structural context to the next Enterprise Experience or Journey"); implemented as `GET /structural-completions/{completion_id}` → `StructuralCompletionService.get_details()`, reusing the existing `StructuralCompletionResponse` shape verbatim — no new table, repository, or service class.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-08 — Complete Structural Transition (raised); BA-09 — Continue from Resulting Structure (resolved)
- **Source:** BA-08 implementation (self-identified, mirroring TD-051/055/058/061/064's own identical precedent)
- **Resolution Criteria:** ~~A read path for Resulting Structural Context exists, if and only if BA-09's own gap analysis determines one is required.~~ Met — `GET /structural-completions/{completion_id}` exists and is tested (`test_get_structural_completion_returns_details_for_platform_admin` and 6 further API/authorization tests).

---

### TD-069 — Detailed Entry

- **Title:** Resulting Structural Context Lifecycle Transition Beyond CREATED Is Not Implemented
- **Category:** Architecture
- **Description:** `StructuralCompletion.status` (`models/structural_completion.py`) is constrained to IRA-004 §27's registered Lifecycle Model — CREATED, ARCHIVED — but BA-08's own service only ever writes CREATED.
- **Root Cause:** No retirement/archival mechanism exists anywhere in this repository yet; ARCHIVED is SD-002-008's own generic terminal state, not something PE-001-C005 itself triggers.
- **Impact:** None today — mirrors every prior Business Activity's own identical, already-accepted disposition (TD-052/053/057/062/065).
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** A future retirement/archival path, once a real consumer needs it.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-08 — Complete Structural Transition
- **Source:** BA-08 implementation (self-identified, mirroring TD-052/053/057/062/065's own precedent)
- **Resolution Criteria:** ARCHIVED has a real, tested code path once the mechanism that owns that transition is implemented.

---

### TD-070 — Detailed Entry

- **Title:** Completing a Structural Transition Performs No Actual ERG-001 Structural Mutation
- **Category:** Architecture
- **Description:** BA-08 ("Complete Structural Transition") creates a `StructuralCompletion` (`RSC-000001`) row recording that a governed decision chain — Structural Change Intent → Proposed Outcome → Review → Validation — has reached completion. It does **not** modify `organization_nodes`, and does **not** create `organization_hierarchy` or `consolidation_determination`. The enterprise's own real structural data (the `OrganizationNode` a proposal targeted) is provably unchanged after "completion" — directly verified by this Business Activity's own tests, which assert the target node's `node_name`/`operational_status`/`active_flag` are byte-for-byte identical before and after completion, at both the service and API layers.
- **Root Cause:** No canonical document in this repository (PE-001-C005, ERG-001, Master Technical Architecture) specifies a structured representation from which a real structural mutation could be deterministically derived from a `StructuralProposal`'s own free-text `proposed_outcome_description` — the same upstream gap TD-054 already disclosed for Comparison Context. PE-001-C005 §38.4 itself explicitly places database/mutation mechanics outside C-005's own scope. Building a mutation mechanism now would require inventing both a change-representation schema and the write logic itself — an unauthorized architectural addition (CLAUDE.md §18/§19.4), not an implementation detail. This was evaluated explicitly during BA-08's own readiness assessment (Option A vs. B vs. C) and Option A — no mutation — was the only option requiring no invention.
- **Impact:** **Significant, and disclosed prominently rather than left implicit.** The entire WP-04 Structural Context Lifecycle (BA-03 through BA-08) currently produces a complete, governed, auditable *decision record* — but the enterprise's actual structural data (`organization_nodes`, and the still-nonexistent `organization_hierarchy`/`consolidation_determination`) is never touched by any code path in this repository. A caller who runs the full chain to "completion" has not changed anything about the real enterprise structure. This also means WP-03's own TD-032 (`memberships.home_node_id` nullability) remains unaffected by WP-04's own completion, since no new `OrganizationNode` state is ever produced by a completed transition.
- **Severity:** **High** — this is the central, load-bearing gap of the entire Structural Context Lifecycle as currently implemented; every other Technical Debt item raised across BA-03 through BA-08 is comparatively minor next to this one.
- **Status:** Open
- **Target Resolution:** Real resolution requires, at minimum: (1) a governance decision on how a "structural change" is represented as structured data (not free text) — likely its own ADR; (2) the actual ERG-001 write-path capability, including `organization_hierarchy` and `consolidation_determination`, neither of which exists anywhere in this repository; (3) a mechanism connecting a completed `RSC-000001` row to that write path, satisfying GS-INV-012's own exact-revision traceability requirement. This is substantial, multi-Business-Activity (or multi-Work-Package) future work — not invented speculatively here.
- **Owning Work Package:** WP-04 — Enterprise Structure Management (C-005)
- **Related Business Activity:** BA-08 — Complete Structural Transition
- **Source:** BA-08 implementation (mandatory disclosure, per this Business Activity's own explicit instruction and readiness assessment)
- **Resolution Criteria:** Completing a structural transition produces a real, verifiable change to the enterprise's own structural data, not only a C-005 experience-layer completion record.

---

### TD-079 — Detailed Entry

- **Title:** PLATFORM_ADMIN-Only Authorization Gate for Access Management (No C-002 Persona Claim Exists)
- **Category:** Security / Authorization Granularity
- **Description:** BA-01 through BA-04 (WP-05/C-002, Access Management) gate every `/access-evaluations` endpoint — `evaluate_access`, `preserve_access_evaluation_outcome`, `expire_access_evaluation_outcome`, `detect_access_context_change`, `resolve_access_handoff_rejection` — on the existing `PLATFORM_ADMIN` role claim only (`dependencies.require_platform_admin`, reused unchanged from WP-01 through WP-04).
- **Root Cause:** The same root cause already tracked by TD-021 through TD-025/TD-031/TD-034/TD-035/TD-036/TD-039/TD-042: no persona-specific, enforceable claim exists anywhere in the platform's seeded role catalog for any capability-specific participant (here, whoever PE-001-C002 would name as its own Access Evaluation participant), pending ADR-002 acceptance.
- **Impact:** Any authenticated `PLATFORM_ADMIN` can evaluate, preserve, expire, invalidate, or classify a hand-off rejection for any Access Evaluation Outcome, regardless of whether a narrower persona would be the architecturally correct actor. No privilege-escalation risk beyond what `PLATFORM_ADMIN` already holds platform-wide today.
- **Severity:** Low — a disclosed, deliberate simplification, the identical class of gap already accepted as non-blocking for every prior Work Package (TD-021 being the first instance); confirmed non-blocking here for the same reason.
- **Status:** Open
- **Target Resolution:** ADR-002 acceptance and/or a C-002-specific persona authority model (future, separately-scoped Business Activity or architecture amendment), followed by a persona-specific authorization dependency replacing `PLATFORM_ADMIN` for these five endpoints.
- **Owning Work Package:** WP-05 — Access Management (C-002)
- **Related Business Activity:** BA-01 through BA-04
- **Source:** BA-01 through BA-04 implementation (self-identified, mirroring TD-021's own precedent, per IRA-005 §12)
- **Resolution Criteria:** ADR-002 is Accepted and/or a C-002 persona authority model exists; a persona-specific authorization dependency exists and is enforced for `/access-evaluations`; a test exists asserting the correct persona-specific claim is required and an unauthorized persona is rejected.

---

### TD-080 — Detailed Entry

- **Title:** No `GET` Read Endpoint Exists for Access Evaluation Outcome
- **Category:** Architecture
- **Description:** WP-05 BA-01 through BA-04 implement `POST /access-evaluations` (create) and four sub-resource action endpoints (`preserve`, `expire`, `context-change`, `handoff-rejection`) only — no `GET /access-evaluations/{id}` exists. Every action's own response already returns the outcome's full current state, but no caller can resolve an outcome by id independently of the action that most recently touched it.
- **Root Cause:** IRA-005 §12 charters exactly four Business Activities (BA-01, BA-02, BA-04 in full; BA-03 classification-only) — none of them is a dedicated Query-type activity, mirroring the identical disposition IRA-004 left open for Structural Change Intent (TD-051), Proposed Outcome Context (TD-055), Impact Context (TD-058), Review Context (TD-061), and Validation Context (TD-064), all resolved the same way (deferred, not silently assumed).
- **Impact:** None today — every existing caller obtains the outcome's current state directly from whichever action's own response it just invoked. Becomes real friction only once a future capability needs to resolve a previously-created outcome by id without itself having just performed an action on it.
- **Severity:** Low — no current consumer exists; every implemented action already returns the full outcome state its own caller needs.
- **Status:** Open
- **Target Resolution:** A future, separately-scoped WP-05 Business Activity (or amendment) adds `GET /access-evaluations/{id}` once a real caller needs it, mirroring TD-068's own resolution precedent (`GET /structural-completions/{id}`, added by a later Business Activity once BA-09 needed it).
- **Owning Work Package:** WP-05 — Access Management (C-002)
- **Related Business Activity:** BA-01 — Evaluate Access for a Governed Request
- **Source:** BA-01 implementation (self-identified during this Business Activity's own gap analysis, IRA-005 §12's own authorized scope)
- **Resolution Criteria:** A read path for Access Evaluation Outcome exists, if and only if a future Business Activity's own gap analysis determines one is required.

---

### TD-081 — Detailed Entry

- **Title:** API-Layer Test Coverage Narrower Than Unit-Layer for Several Two-Branch Behaviors
- **Category:** Testing
- **Description:** `test_access_evaluation_api.py` originally exercised only one branch of several two-branch service behaviors: BA-04's `handoff-rejection` endpoint was tested only for the live-outcome classification; BA-02's `expire` endpoint was tested for the double-preserve 409 but not the expire-without-preserve 409; BA-03's `context-change` endpoint was tested only for its invalidating path. All three branches were already fully covered at the unit layer.
- **Root Cause:** The API test suite was written to exercise the happy path and the most obvious negative path per endpoint, without a systematic cross-check against the unit suite's own branch coverage.
- **Impact:** None on correctness — every omitted branch was independently proven correct at the unit layer. A narrow, self-contained API-layer coverage gap.
- **Severity:** Low — per `CLAUDE.md §19.8.7`, a non-critical testing-completeness gap with no effect on correctness, security, or another capability's ability to depend on this one (this field was missing from the original entry — VV-AUDIT-WP-05 F-10).
- **Status:** **Resolved and Closed.** The three missing branch-level API assertions (`test_expire_rejects_outcome_that_was_never_preserved`, `test_context_change_rejects_non_live_outcome`, `test_handoff_rejection_classifies_invalidated_outcome_as_integrity_signal`) were added to `test_access_evaluation_api.py`; 14/14 API tests passed and 601/601 full suite passed at closure. Genuineness of this closure was independently re-verified by `VV-AUDIT-WP-05` §13.3 (all three named tests located and individually executed, confirmed passing) — the one caveat recorded there (F-06) is a process observation that the remediation was authored and self-attested by the implementing session rather than reviewed by a second party before closure, not a doubt about whether the tests actually exist or pass.
- **Owning Work Package:** WP-05 — Access Management (C-002)
- **Related Business Activity:** BA-02, BA-03, BA-04
- **Source:** Independent Review (`CERT-WP-05`); severity gap found by `VV-AUDIT-WP-05` F-10
- **Resolution Criteria:** Met — see Status.

---

### TD-082 — Detailed Entry

- **Title:** BA-02's "Bound" / EX-C002-06's Scope Boundary Is Not Modelled — Expiry Is Manual-Only, No Object/Event/Time Scoping Exists
- **Category:** Architecture
- **Description:** BA-02's own name is "Preserve and **Bound** Access Evaluation Outcome Validity"; `EX-C002-06` is "Expire ... **at Scope Boundary**"; `IRA-005 §11` states validity is "Object Scoped, Event Scoped, and Time Scoped to the single governed execution it was produced for." No execution-scope identifier, no expiry timestamp, and no automatic expiry exist anywhere in the schema or code — an outcome remains `PRESERVED` indefinitely until a caller explicitly calls `expire()`.
- **Root Cause:** Building real Object/Event/Time scoping would require either a new architectural component (a scheduler) or a new concept (an execution-scope identifier) neither of which is documented anywhere in `IRA-005` or `ADR-015` — inventing one was correctly declined as an unauthorized architectural addition (`CLAUDE.md §18`), consistent with `services/access_evaluation_service.py`'s own documented reasoning for why expiry is caller-invoked only.
- **Impact:** What is implemented is a valid, minimum-scope manual status flip; the gap is that nothing currently *causes* expiry to be called at the actual boundary of a governed execution — that trigger does not exist anywhere in this repository yet.
- **Severity:** Medium — per `CLAUDE.md §19.8.7`, an internal completeness/robustness concern expected to require resolution before this capability is exercised at production scale or depended on by a downstream capability, but not itself a defeat of BA-02's stated Business Intent for its own authorized (manual) scope, and not a security/tenant-isolation boundary.
- **Status:** Open
- **Target Resolution:** A future, separately-scoped Business Activity or architecture decision introduces a real execution-scope concept and/or a caller (e.g. the governed execution's own completion handler) that invokes `expire()` automatically at the correct boundary.
- **Owning Work Package:** WP-05 — Access Management (C-002)
- **Related Business Activity:** BA-02 — Preserve and Bound Access Evaluation Outcome Validity
- **Source:** `VV-AUDIT-WP-05` F-08 (previously disclosed only in a code docstring, `services/access_evaluation_service.py:210-217`, in violation of `CLAUDE.md §19.8.2`)
- **Resolution Criteria:** A real execution-scope identifier and/or an automatic trigger at the governed execution's own boundary exists, tested, and documented.

---

### TD-083 — Detailed Entry

- **Title:** BA-03 Performs No Detection — Invalidation Is Driven Entirely by an Unvalidated Caller-Supplied String
- **Category:** Business Rule Compliance
- **Description:** The Business Activity is named "**Detect** and Resolve Access Context Change." `changed_fact` (the request body's sole field) is validated only for length (1–500 characters) and is never checked against Membership, Domain, or Approval Authority state. Any live outcome is invalidated purely on the caller's own assertion.
- **Root Cause:** Real detection would require re-reading the governing authorities (Membership standing, Domain state, Approval Authority state) and comparing against the state captured at evaluation time — a "re-resolve to determine same-or-different" mechanism `IRA-005 §12` explicitly places out of this Work Package's own authorized scope (it re-enters BA-01's own excluded branches). What is implemented is the classification/detection portion's only non-excluded behavior: trusting a reported change and invalidating.
- **Impact:** Any caller with `PLATFORM_ADMIN` access can invalidate any live outcome by asserting an arbitrary string, whether or not the asserted fact is true. No downstream consequence beyond invalidation exists yet (no automatic re-evaluation is triggered), so the practical impact is bounded, but the gap between the Business Activity's own name and its behavior is real.
- **Severity:** Medium — per `CLAUDE.md §19.8.7`, an internal completeness concern (the endpoint does less than its own name implies) that does not itself defeat BA-03's authorized classification-only scope and does not weaken a security/tenant-isolation boundary (the caller must still be `PLATFORM_ADMIN`), but should be resolved before this capability is relied upon by a downstream consumer expecting genuine fact-verification.
- **Status:** Open
- **Target Resolution:** A future, separately-scoped Business Activity implementing the excluded "re-resolve to a fresh determination" path (which necessarily requires the same authorities BA-01 itself consults) would naturally also supply real detection; not built speculatively ahead of that need.
- **Owning Work Package:** WP-05 — Access Management (C-002)
- **Related Business Activity:** BA-03 — Detect and Resolve Access Context Change
- **Source:** `VV-AUDIT-WP-05` F-09 (previously disclosed only in a code docstring, `services/access_evaluation_service.py:256-260`, in violation of `CLAUDE.md §19.8.2`)
- **Resolution Criteria:** `changed_fact` (or its replacement) is verified against a real, re-read authority before an outcome is invalidated.

---

### TD-084 — Detailed Entry

- **Title:** `AccessEvaluationValidityStatus.SUPERSEDED` Is Permanently Unreachable
- **Category:** Architecture
- **Description:** No code path in WP-05 writes `SUPERSEDED`. This is correct given the authorized scope — reaching it would require a fresh BA-01 re-evaluation producing a new record, itself gated by the same Permitted/Denied exclusion — and the model's own docstring says so.
- **Root Cause:** Same class of gap as `TD-052`/`TD-057`/`TD-062`/`TD-065`/`TD-069` (WP-04): the full registered Lifecycle Model is declared for schema correctness even though this Work Package's own authorized scope writes only a subset.
- **Impact:** None — declared for schema completeness only, not a functional gap.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** A future, separately-scoped Work Package or Business Activity that performs a real fresh-evaluation supersession, once BA-01's Permitted/Denied branches are ever authorized.
- **Owning Work Package:** WP-05 — Access Management (C-002)
- **Related Business Activity:** BA-01 — Evaluate Access for a Governed Request
- **Source:** `VV-AUDIT-WP-05` F-11 (previously disclosed only in a code docstring, `models/access_evaluation_outcome.py:38`, in violation of `CLAUDE.md §19.8.2` — WP-04's five equivalent cases each received a register entry; this one did not)
- **Resolution Criteria:** Either `SUPERSEDED` becomes reachable by a future Business Activity, or this entry is affirmed as a permanent, intentional gap at that Work Package's own closure.

---

### TD-085 — Detailed Entry

- **Title:** "Full History Retained" Is Only Partially Met — Transitions Overwrite Prior State In Place
- **Category:** Data Integrity
- **Description:** `IRA-005 §11` states the Versioning Policy is "Full history retained for audit and traceability." `preserve()`/`expire()`/`detect_context_change()` each overwrite `validity_status` in place; `detect_context_change()` additionally rewrites `reason` by string concatenation. No prior-state row, version column, or transition table exists — the audit log (previously anonymized per the now-resolved `VV-AUDIT-WP-05` F-03 gap — record_audit's actor_id, unrelated to TD-086) is the only remaining history.
- **Root Cause:** No versioning/history mechanism (a transition table, a version column, or an event-sourced reconstruction) was built — this Work Package's own minimum scope did not charter one, and inventing one would be a new architectural component (`CLAUDE.md §18`).
- **Impact:** The current `validity_status`/`reason` is always correct, but the specific prior value at each transition cannot be queried from the outcome row itself once overwritten.
- **Severity:** Low — a completeness gap in an audit-trail nicety, not a correctness defect (the audit log, once actor attribution is fixed, still records each transition's occurrence and its actor).
- **Status:** Open
- **Target Resolution:** A future, separately-scoped Business Activity or architecture decision introduces a transition/version history table, if a real consumer needs to query prior states rather than only the current one.
- **Owning Work Package:** WP-05 — Access Management (C-002)
- **Related Business Activity:** BA-02, BA-03
- **Source:** `VV-AUDIT-WP-05` F-12
- **Resolution Criteria:** A real prior-state history mechanism exists, if and only if a future gap analysis determines one is required.

---

### TD-086 — Detailed Entry

- **Title:** `CMD-001 §26.7` Physical Implementation Mapping for `AEO-000001` Was Never Recorded
- **Category:** Documentation / Repository Governance
- **Description:** `ADR-015`'s "Explicitly Not Decided" section and `IRA-005:289` both record `AEO-000001`'s Physical Tables/APIs/Events as Pending. WP-05 has since supplied all three (one table, five endpoints, five Domain Event types), but no document was updated to record them — `AEO-000001`'s registration still reads as having no physical realization.
- **Root Cause:** Recording the Physical Implementation Mapping back into `CMD-001 §26.7` (or an equivalent register) was not included in this Work Package's own "Documents Updated" list at implementation time.
- **Impact:** A reader consulting `CMD-001 §26.7` or `ADR-015` alone, without also reading `IMP-REPORT-WP-05`, would not learn that `AEO-000001` now has a real physical mapping.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** Update `CMD-001 §26.7` (or the equivalent Canonical Business Object register) to record `access_evaluation_outcomes`, the five `/access-evaluations` endpoints, and the five Domain Event types as `AEO-000001`'s now-known Physical Implementation Mapping.
- **Owning Work Package:** WP-05 — Access Management (C-002)
- **Related Business Activity:** All (BA-01 through BA-04)
- **Source:** `VV-AUDIT-WP-05` F-13
- **Resolution Criteria:** `CMD-001 §26.7` (or equivalent) reflects the actual, now-known Physical Implementation Mapping.

---

### TD-087 — Detailed Entry

- **Title:** Dependent Capability Hand-off Rejections Are Never Persisted
- **Category:** Data Integrity
- **Description:** BA-04's `resolve_handoff_rejection()` mutates no row and creates no row — the rejection exists only as an audit log line and a synchronous API response. No queryable record of any dependent capability's rejection exists after the response is returned.
- **Root Cause:** No governing document (`IRA-005`, `ADR-015`) requires persistence of a hand-off rejection as its own record; the classification-and-respond behavior implemented is a complete, minimal realization of `BR-C002-05`/Contract 5.6 as stated.
- **Impact:** None against any stated requirement — this is a disclosed design choice, not a violation. A future capability wanting to query "how many hand-off rejections has this outcome received" would find no data to query.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** If a future consumer needs a queryable history of hand-off rejections, a dedicated persisted record (mirroring `AccessEvaluationOutcome`'s own shape) would need its own gap analysis and authorization — not built speculatively ahead of that need.
- **Owning Work Package:** WP-05 — Access Management (C-002)
- **Related Business Activity:** BA-04 — Resolve Dependent Capability Access Hand-off Rejection
- **Source:** `VV-AUDIT-WP-05` F-15
- **Resolution Criteria:** N/A unless a real future consumer is identified.

---

### TD-088 — Detailed Entry

- **Title:** `approval_authority_id` Foreign Key Column Is Not Indexed
- **Category:** Performance
- **Description:** `access_evaluation_outcomes.approval_authority_id` carries a foreign key to `approval_authorities.id` but no index. PostgreSQL does not auto-index FK child columns, so a `DELETE`/`UPDATE` against `approval_authorities` performs a sequential scan of `access_evaluation_outcomes` to check for referencing rows.
- **Root Cause:** Only the two columns actually used for lookups (`membership_id`, `domain_id`) were indexed at implementation time; `approval_authority_id` is written but never independently queried by any current code path.
- **Impact:** Immaterial at current table volumes; would become a real concern only at a scale where `approval_authorities` deletes/updates are frequent and `access_evaluation_outcomes` is large.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** Add `ix_access_evaluation_outcomes_approval_authority_id` in a future migration if table volumes or `approval_authorities` mutation frequency ever make this material.
- **Owning Work Package:** WP-05 — Access Management (C-002)
- **Related Business Activity:** BA-01 — Evaluate Access for a Governed Request
- **Source:** `VV-AUDIT-WP-05` F-19
- **Resolution Criteria:** Index added if and when volume/frequency justifies it.

---

### TD-089 — Detailed Entry

- **Title:** Four of Five `/access-evaluations` Routes Omit 400/401/403 From Their OpenAPI `responses` Maps
- **Category:** Documentation
- **Description:** All five endpoints can return 400 (missing/malformed Authorization header), 401 (invalid/expired token), and 403 (non-`PLATFORM_ADMIN`) via the shared `require_platform_admin` dependency. Only `POST /access-evaluations` documents these in its `responses` map; the four sub-resource action endpoints (`preserve`, `expire`, `context-change`, `handoff-rejection`) do not.
- **Root Cause:** The `responses` map for each sub-resource endpoint was written to document only that endpoint's own distinctive outcomes (200/404/409), omitting the shared-dependency codes already documented once on the first endpoint.
- **Impact:** Purely cosmetic — the codes are real and correctly enforced at runtime (confirmed by test); only the generated OpenAPI/Swagger documentation under-describes four of the five endpoints.
- **Severity:** Low.
- **Status:** Open
- **Target Resolution:** Add 400/401/403 to the `responses` map of the four sub-resource endpoints, mirroring `POST /access-evaluations`'s own map.
- **Owning Work Package:** WP-05 — Access Management (C-002)
- **Related Business Activity:** BA-02, BA-03, BA-04
- **Source:** `VV-AUDIT-WP-05` F-21
- **Resolution Criteria:** All five endpoints' `responses` maps document 400/401/403.

---

### TD-090 — Detailed Entry

- **Title:** PLATFORM_ADMIN-Only Authorization Gate for Understand Domain Permission Context (URA-001-45/46 Domain Owner/Domain Admin Authority Not Yet Modeled)
- **Category:** Security / Authorization Granularity
- **Description:** BA-01 (Understand Domain Permission Context, WP-06/C-003) gates both `GET /domain-permissions/{id}` and `GET /domain-permissions` on the existing `PLATFORM_ADMIN` role claim only (`dependencies.require_platform_admin`, reused unchanged from WP-02). PE-001-C003 v1.1's `EX-C003-11` and its Contract 5.1 extension confer the same viewing authority to "the same defining-authority personas confirmed under this Contract to establish, version, deprecate, or retire" a Domain Permission — i.e., Domain Owner/Domain Admin authority (URA-001-45/46) for the target Domain — not to `PLATFORM_ADMIN` specifically.
- **Root Cause:** Identical to `TD-022`: Domain (AMD-014, `models/domain.py`/`domain_registry`) is deliberately ownership-free reference/master data — no Domain Owner/Domain Admin relationship exists anywhere in the schema from which a Domain-specific defining authority could be confirmed. `EX-C003-11` was added at Version 1.1 precisely to complete `ERB-C003-01`'s Discover/Understand lifecycle stages, but its own Contract 5.1 extension text explicitly ties viewing authority to the same not-yet-modeled personas as the write-side Business Activities.
- **Impact:** Any authenticated `PLATFORM_ADMIN` can view any Domain Permission's current state or search across all Domain Permissions, regardless of whether URA-001 would actually confer that specific viewing authority to a particular Domain Owner or Domain Admin. No privilege-escalation risk beyond what `PLATFORM_ADMIN` already holds platform-wide today (same risk profile as `TD-022`), but URA-001-45/46's per-Domain authority differentiation is not enforced for the read side either.
- **Severity:** Low — a disclosed, deliberate simplification anticipated before implementation (`IRA-006 §10.2`), the same class of gap as `TD-022`, not a silent gap or a broken invariant.
- **Status:** Open
- **Target Resolution:** The same future Domain Owner/Domain Admin authority model `TD-022` already awaits, followed by a persona-specific authorization dependency (e.g. `require_domain_owner_or_admin`) replacing `PLATFORM_ADMIN` for both endpoints in the same remediation pass as `TD-022`'s own write-side endpoint.
- **Owning Work Package:** WP-06 — Domain Permission Read APIs (C-003)
- **Related Business Activity:** BA-01 — Understand Domain Permission Context
- **Source:** Self-identified during WP-06 implementation, anticipated in `IRA-006 §10.2`; Resolution Criteria amended per `VV-AUDIT-WP-06` F-02 (see below)
- **Resolution Criteria:** A Domain Owner/Domain Admin authority model exists and is queryable; a persona-specific authorization dependency exists and is enforced for both `GET /domain-permissions/{id}` and `GET /domain-permissions`, resolved in the same pass as `TD-022`; **`DomainPermissionRepository.search()`/`get_by_id()` themselves also gain domain/organization-scoping logic in the same remediation pass — not merely a narrower `Depends()`** (per `VV-AUDIT-WP-06` F-02: neither method performs any query-level scoping today, relying entirely on the coarse role check; a dependency-only swap would leave a caller newly confirmed for one Domain still able to retrieve every other Domain's Domain Permissions, reproducing the shape of `VV-AUDIT-WP-05`'s own F-02 cross-tenant finding); a test exists asserting the correct Domain-specific authority is required, an unauthorized caller is rejected, and a caller scoped to one Domain cannot retrieve another Domain's Domain Permissions via either endpoint.

---

### TD-091 — Detailed Entry

- **Title:** `GET /domain-permissions` Returns an Unbounded Result Set (No Pagination, Unlike the `OrganizationRepository.search()` Precedent)
- **Category:** Performance
- **Description:** `DomainPermissionRepository.search()` (WP-06/C-003, BA-01) builds a `select(DomainPermission)` query with zero, one, two, or three optional `.where()` clauses (`domain_id`, `membership_id`, `status`) and always returns every matching row — there is no `limit`, `skip`, or pagination mechanism of any kind. Omitting every filter (the documented, intended behavior for "no criterion supplied returns every Domain Permission") returns literally every row in the `domain_permissions` table, including historical `SUPERSEDED` versions.
- **Root Cause:** `OrganizationRepository.search()` (WP-01, `repositories/organization_repository.py`) already establishes an in-repository pagination pattern — `skip`/`limit` parameters, the router capping `limit` at 100 via `Query(ge=1, le=100)`, and a `(page_of_results, total_count)` return shape — but `DomainPermissionRepository.search()` does not follow it. Neither `IRA-006` nor `IMP-REPORT-WP-06_Domain_Permission_Read_APIs.md` discusses or discloses this omission anywhere; it was found only by `CERT-WP-06`'s independent certification pass (§4.6), not self-identified during implementation.
- **Impact:** At current and near-term data volumes (Domain Permission rows are created one at a time via `POST /domain-permissions`, `PLATFORM_ADMIN`-gated, at the same low, deliberate volume every other WP-02 authorization-policy object type shares), no practical effect. At production scale, or if a downstream capability relies on this endpoint for a large Organization, an unbounded query could return a very large result set in a single response, with no way for a caller to page through it. Mitigated by the endpoint being `PLATFORM_ADMIN`-gated, administrative, and by every other list-returning endpoint in this AuthService instance except `OrganizationRepository.search()` sharing the same unbounded pattern (e.g. `GET /domains`) — this is not a WP-06-specific regression relative to the rest of the codebase, only relative to the one precedent that exists for it.
- **Severity:** Medium — per `CLAUDE.md §19.8.7`'s rubric: an internal completeness/robustness concern that does not defeat `EX-C003-11`'s own stated Business Intent and does not touch a security or tenant-isolation boundary, but is reasonably expected to require resolution before this endpoint is exercised at production scale or relied upon by a downstream capability.
- **Status:** Open
- **Target Resolution:** Add `skip`/`limit` query parameters to `GET /domain-permissions` and thread them through `DomainPermissionService.search()`/`DomainPermissionRepository.search()`, mirroring `OrganizationRepository.search()`'s own pattern (capped `limit`, returned total count), before this endpoint is relied upon at production scale or by a downstream capability.
- **Owning Work Package:** WP-06 — Domain Permission Read APIs (C-003)
- **Related Business Activity:** BA-01 — Understand Domain Permission Context
- **Source:** `CERT-WP-06_Domain_Permission_Read_APIs.md` §4.6 (Independent Certification); Resolution Criteria amended per `VV-AUDIT-WP-06` F-03 (see below)
- **Resolution Criteria:** `GET /domain-permissions` accepts `skip`/`limit` query parameters, caps `limit` at a bounded maximum, and returns a total count alongside the page of results; **`DomainPermissionRepository.search()`'s query gains a deterministic `ORDER BY` clause in the same pass** (per `VV-AUDIT-WP-06` F-03: the query has none today, which is harmless while unpaginated but would make paging non-deterministic once `skip`/`limit` are added — a row could appear on two different pages, or none, across two calls); a test exists asserting the cap is enforced and pagination behaves correctly and deterministically across a result set larger than one page.

---

## Maintenance

- New entries are appended with the next sequential `TD-NNN` ID.
- When an item is resolved, update its `Status` to `Closed` and record the resolving Business Activity or Work Package in `Planned Resolution` (do not delete closed rows — they remain part of the audit trail).
- This register is reviewed and updated during Independent Review of any Business Activity that touches an area with an open, related entry.
