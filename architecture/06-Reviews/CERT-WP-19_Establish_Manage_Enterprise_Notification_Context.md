# CERT-WP-19 — Independent Certification (Gate 1 of 5) — Establish / Manage Enterprise Notification Context (C-132, BA-01)

**Work Package:** WP-19
**Capability:** C-132 — Enterprise Notifications (`CAP-001` line 105, Domain D-007 "Collaboration & Engagement", owning specification `SD-003`, Active — capability-wide status **🟡 AMBER**, `IRA-C132`, unchanged and not reclassified by this certification)
**Business Activity:** BA-01 — Establish / Manage Enterprise Notification Context
**Gate:** `CLAUDE.md §19.7b` **Gate 1 — Independent Certification** (gate 1 of 5). Gate 2 (V&V Audit), Gates 3–4 (remediation + verification, triggered only if a later gate finds a defect), and Gate 5 (Release Readiness Audit) are separate, later, independently-staffed gates and are **NOT** performed or recorded here.

**Reviewer independence statement:** The Gate 1 review recorded in this document was performed across **two** genuinely independent, fresh-context reviewers, neither with any prior involvement in the WP-19 implementation. The **first** reviewer (2026-09-05) produced the original ❌ FAIL determination below. After the resulting finding (F-1) was remediated by the implementing session, a **second, distinct** fresh-context reviewer (2026-09-06), with **no** involvement in the implementation, the first Gate 1 review, or the F-1 remediation, independently re-reviewed the corrected implementation — including a purpose-built negative control against a reconstructed pre-fix build — and produced the ✅ PASS determination below. Every material claim in both determinations was re-derived from primary sources (files opened, commands run, from-scratch runtime probes). No prior report's conclusion was accepted on trust.

**State certified:** `git rev-parse HEAD` → `17a07bf` (`main`). All WP-19 work is uncommitted in the working tree (nothing staged, nothing committed, nothing pushed). This certification isolates the **WP-19 change set only** — 9 new + 2 modified backend files, 2 new + 1 modified frontend files, this document, `IMP-REPORT-WP-19`, and the additive `WPR-001` WP-19 row / `WP-19` charter status updates. The working tree also carries a large body of pre-existing, unrelated C-040 / ROD / ADR-027…035 / `IRA-C114` / `Sarika_consent.png` / `Master_Platform_Capability_Delivery_Map.xlsx` / `CLAUDE.md` / `CAP-001` / `SER-001` / `CANONICAL-ENTERPRISE-SEARCH…` / `ADR-002` noise that is **not** part of WP-19 and was verified by both reviewers to carry no WP-19 content.

---

## CURRENT CERTIFICATION STATE (2026-09-06) — ✅ GATE 1 PASSED (second attempt — fresh independent re-review after F-1 remediation)

**This document records two Gate 1 Independent Certification attempts.**

- The **first attempt (2026-09-05)** returned **❌ FAIL** on one material, HIGH-severity, certification-blocking finding — **F-1**, a tenant-isolation defect in `POST /notifications` (an authenticated caller from Organization A could forge `X-Tenant-ID = Organization B` together with an Organization B `membership_id` and create a Notification in Organization B; reproduced at runtime, HTTP 201, persisted, visible to the Organization B recipient). The first-attempt determination and its findings are preserved verbatim in the section **"## DETERMINATION (first attempt — 2026-09-05 — ❌ FAIL — historical, preserved)"** below. This is a historical fact and is **not** deleted, overwritten, or rewritten.

- **F-1 was remediated** by the implementing session under a dedicated Repository Owner remediation authorization (2026-09-06). The fix is a single-mechanism dependency swap: `POST /notifications` (`routers/notification.py::establish_notification`) now takes its `claims` from the **pre-existing** `require_matching_tenant_or_platform_admin` dependency (`dependencies.py`) instead of `get_current_claims` — the exact mechanism WP-10 introduced to close `CERT-WP-10` Finding B-1, the identical root cause. No new authorization mechanism was written; `dependencies.py` and `middleware/tenant.py` are byte-identical to `HEAD`; the service-layer recipient-vs-`X-Tenant-ID` check is unchanged. Full remediation record: `IMP-REPORT-WP-19 §13`.

- The **second attempt (2026-09-06)** — a fresh, independent Gate 1 re-review by a reviewer uninvolved in the implementation, the first Gate 1 review, or the F-1 remediation — returned **✅ PASS**, scoped to WP-19 / C-132 BA-01. That determination is recorded in the section **"## GATE 1 RE-REVIEW (second attempt — 2026-09-06 — ✅ PASS)"** below and is the **current Gate 1 state of record**.

**Governance sequence, recorded explicitly:**

> Gate 1 — Original Independent Review — **❌ FAIL — F-1 (HIGH, tenant isolation)**
> → F-1 remediation (implementing session, RO-authorized, `IMP-REPORT-WP-19 §13`)
> → Fresh Independent Gate 1 Re-Review — **✅ PASS**

**Current status:** ~~WP-19 / C-132 BA-01 = IMPLEMENTATION AUTHORIZED — IMPLEMENTATION COMPLETE — **GATE 1 PASSED** — **GATE 2 (V&V Audit) NOT RUN** — Gate 3 NOT RUN — Gate 4 NOT RUN — **GATE 5 (Release Readiness) NOT RUN** — Formal closure NOT COMPLETE — Certification NOT COMPLETE — Release readiness NOT ESTABLISHED.~~ *(Superseded 2026-09-08 — a fresh independent Gate 2 V&V Audit has since been performed and PASSED; see the note immediately below.)* ~~WP-19 / C-132 BA-01 = IMPLEMENTATION AUTHORIZED — IMPLEMENTATION COMPLETE — **GATE 1 PASSED** — **GATE 2 V&V PASSED** (fresh independent audit, 2026-09-08; result of record: `IMP-REPORT-WP-19 §15` — 24 PASS / 0 PARTIAL / 0 FAIL RTM, 0 material findings, 8 non-material observations, F-1 negative control confirming the pre-fix defect and its closure) — **GATE 3 NOT TRIGGERED** — **GATE 4 NOT TRIGGERED** (Gate 2 found no material defect requiring remediation) — **GATE 5 (Release Readiness) PENDING / NOT RUN** — Formal closure NOT COMPLETE — Certification NOT COMPLETE — Release readiness NOT ESTABLISHED.~~ *(Superseded 2026-09-09 — a fresh independent Gate 5 Release Readiness Audit has since been performed and PASSED, and WP-19 / BA-01 has been formally closed; see the note immediately below.)* WP-19 / C-132 BA-01 = IMPLEMENTATION COMPLETE — **GATE 1 PASSED** — **GATE 2 V&V PASSED** — **GATES 3/4 NOT TRIGGERED** — **GATE 5 RELEASE READINESS PASSED** (fresh independent audit, 2026-09-09; result of record: `IMP-REPORT-WP-19 §16` — 0 material findings, release isolation CLEAN, explicit 19-path release allowlist produced; own from-scratch F-1 probe + negative control 11/11, own E2E + list-cap + CHECK/FK probe 21/21, 25/25 targeted + 901/901 regression re-run, single Alembic head `d4e5f6a7b8c9`, clean frontend `tsc`/`eslint`/`next build`) — **FORMALLY CLOSED — CERTIFIED — RELEASE-READY** (`IMP-REPORT-WP-19 §17`, 2026-09-09; all five `CLAUDE.md §19.7b` gates complete; governance-recording complete; **repository commit outstanding — a separate, explicitly-authorized action**, mirroring `WP-16`/`WP-17`/`WP-18`). **This closure applies to WP-19 / C-132 BA-01 only — it does NOT close C-132 as a capability.** C-132 capability-wide status remains **🟡 AMBER** (`IRA-C132`, unchanged — not reclassified; no capability-wide C-132 completion is claimed; all deferred C-132 scope — delivery channels, real event bus, `SD-003-226`, C-131/C-133 integration — remains deferred). C-023 / WP-17 / WP-18 untouched. **This document (`CERT-WP-19`) remains the Gate 1 record of record; the Gate 2 V&V result of record is `IMP-REPORT-WP-19 §15`; the Gate 5 + formal-closure result of record is `IMP-REPORT-WP-19 §16`/`§17`. The two Gate 1 NOT-CERTIFIED / FAIL attempts and the full gate history remain preserved verbatim as historical record.**

---

## DETERMINATION (first attempt — 2026-09-05 — ❌ FAIL — historical, preserved)

### ❌ FAIL — one material finding.

**F-1 — Cross-tenant Notification injection on `POST /notifications` — HIGH — certification-blocking.**

- **Root cause.** `POST /notifications` (`routers/notification.py::establish_notification`, as originally submitted) depended only on `get_current_tenant` + `get_current_claims`. It never verified that the authenticated caller was authorized to act for `X-Tenant-ID`. `middleware/tenant.py::get_current_tenant()` returns any well-formed UUID the caller supplies. `NotificationEstablishmentService.establish()` validated `membership.organization_id == target_organization_id` (recipient-vs-header) but was never passed `caller_person_id`, so it could not bind the caller to the tenant. The only guard tied two caller-controlled values (`X-Tenant-ID` and body `membership_id`) to each other.
- **Reproduced at runtime by the first reviewer.** An authenticated caller whose own Organization was Org A supplied `X-Tenant-ID` = Org B and `membership_id` = an Org B Membership → **HTTP 201**, row persisted, visible in the Org B recipient's `GET /notifications`.
- **Rules violated.** `CLAUDE.md §21.4(c)` (a foreign-object identifier not derived from the caller's claims "SHALL be gated before submission"); `§19.8.5` (tenant-isolation defects may not be deferred); `WP-19` charter §11 / `TDS-C132 §11`. Direct repository precedent: `CERT-WP-10` Finding B-1 — identical root cause, certification-blocking, fixed with `require_matching_tenant_or_platform_admin`.
- **Severity.** HIGH (`CLAUDE.md §19.8.7` — "weakens a security or tenant-isolation boundary, even if no exploit is currently known").

**Everything else verified sound by the first reviewer** (schema/migration field-by-field vs `TDS-C132 §6.6`; recipient-facing isolation; lifecycle + idempotency; audit wiring; frontend extension; 22/22 targeted, 898/898 regression; single additive Alembic head; clean `tsc`/`eslint`/`next build`; BA scope not expanded; no STOP-and-report bypassed; C-132 remained 🟡 AMBER; C-023/WP-17/WP-18 untouched). Seven non-material observations (N-1…N-7) were recorded — see the re-review section for their carried-forward disposition.

This ❌ FAIL determination is preserved as the historical record of the first attempt and is not rewritten.

---

## GATE 1 RE-REVIEW (second attempt — 2026-09-06 — ✅ PASS)

A fresh, independent Gate 1 re-review reviewer — no involvement in the WP-19 implementation, the first Gate 1 review, or the F-1 remediation — independently inspected the corrected implementation and the full governance chain (`ROD-C132` → `IRA-C132` → `TDS-C132` → `WPR-001` → `WP-19` charter → `IMP-REPORT-WP-19`), and independently executed the test and probe suite.

### ✅ PASS — scoped to WP-19 / C-132 BA-01. Zero material findings.

### F-1 closure — independently verified with a working negative control

| Forged-`X-Tenant-ID` attack: Org A caller (JWT org = A), `X-Tenant-ID` = Org B, body `membership_id` = an Org B Membership | Reconstructed **pre-fix** build (one dependency line reverted, run in a throwaway app) | **Fixed** code (real `main.app`) |
|---|---|---|
| HTTP status | **201 Created** | **403 Forbidden** |
| `c132_notification` rows created | **+1, persisted with the Org B membership** | **0** (row count unchanged) |
| Visible in the Org B recipient's `GET /notifications` | **Yes (count 1)** | **No (`[]`)** |

The probe genuinely reproduces the original F-1 defect against a faithful pre-fix reconstruction and confirms the fix closes it. The repo file was not edited to build the reconstruction; no `git stash` was used.

### Critical checks — all held (independently observed)

- **Caller-vs-header binding proven** (not merely membership-vs-header): forged `X-Tenant-ID` + a **random / never-resolved** `membership_id` → **HTTP 403 at the tenant-authority dependency, before any recipient lookup**, carrying the dependency's own message ("X-Tenant-ID must match your own Organization, unless you hold PLATFORM_ADMIN.").
- **PLATFORM_ADMIN positive control:** a `PLATFORM_ADMIN` whose own `organization_id` claim ≠ `X-Tenant-ID`, establishing for a recipient **in** `X-Tenant-ID` → **HTTP 201** (consistent with the WP-10 / `CERT-WP-10` Finding B-1 precedent).
- **PLATFORM_ADMIN negative control:** the same `PLATFORM_ADMIN` establishing for a recipient Membership in a **third** Organization → **HTTP 403** (the unchanged service-layer recipient-vs-`X-Tenant-ID` check still runs and still denies).
- **Valid same-tenant establish:** Org A caller + `X-Tenant-ID` = Org A + Org A `membership_id` → **HTTP 201**, `status = "UNREAD"`.
- **Recipient-facing isolation intact:** cross-tenant `GET /notifications/{id}` → **404**; cross-tenant `POST /notifications/{id}/acknowledge` → **404** and the target row stays `UNREAD`; a different recipient in the **same** Organization → **404** on read and acknowledge (anti-enumeration, never 403).
- **Acknowledge idempotency intact:** acknowledge twice → both **200**, `status = ACKNOWLEDGED`, `acknowledged_at` unchanged at the DB level, exactly one row.

### Schema / migration — field-by-field faithful to `TDS-C132 §6.6`

`membership_id` FK → `memberships.id`, NOT NULL, indexed (recipient + tenant anchor; no duplicated `organization_id`); `severity` `CheckConstraint` closed set `success/info/warning/danger`; `status` `CheckConstraint` closed set `UNREAD/ACKNOWLEDGED`; `source_type` NOT NULL + `source_id` nullable, **not** a foreign key; `what_happened` NOT NULL; `why_it_matters`/`what_happens_next` nullable; `created_at` NOT NULL; `acknowledged_at` nullable; **no uniqueness constraint**; migration **additive only** (one `create_table` + two `create_index`, no `ALTER`); `down_revision = c3d4e5f6a7b8` (WP-17). `alembic heads` → **`d4e5f6a7b8c9`**, single, non-branching. Model and migration agree. (`updated_at` nullable column beyond §6.6 = established AuthService convention; non-material.)

### API / service / audit / frontend — conformant

Exactly the four authorized routes (`POST /notifications`, `GET /notifications`, `GET /notifications/{id}`, `POST /notifications/{id}/acknowledge`), no others. Input validation (`severity` `Literal` → 422; empty `what_happened` → 422; empty `source_type` → 422); unknown `membership_id` → 404; missing `Authorization` / `X-Tenant-ID` → 400. `record_audit` `ESTABLISH_NOTIFICATION`/`SUCCESS` and `ACKNOWLEDGE_NOTIFICATION`/`SUCCESS`; `DENIED` on establish rejections; uses `observability.record_audit` / `publish_event` (the pre-existing structured-log stand-ins, **not** a real broker); Notification rows are **not** conflated with Audit Events. `NotificationCenter.tsx` **extends** the existing panel shell (not a rewrite) with real `apiClient` integration and loading / error / empty / list states, an unread count, per-item acknowledge, DS-001 Chapter 21 composition (What Happened / Why It Matters / What Happens Next) + four-value severity, token-only styling; no mock data, no new route, no new component/token/theme. Only the three authorized frontend files touched.

### Scope & architecture — conformant

Verified **absent** from the delivered change set: cross-service DB access; cross-service API fan-in; event bus / concrete `EventSubscriber` / broker; new `NotificationService`; delivery-provider infra; email/SMS/push/webhook; C-133 integration; C-131 implementation; `SD-003-226` interruption-ceiling/digest; notification preferences/config UI; new routes/screens. The F-1 remediation introduced no new architecture (Reuse-tier fix per `CLAUDE.md §19.5`). No `§18`/`§19.4` STOP-and-report was bypassed.

### Governance — consistent

Original Gate 1 FAIL preserved as historical fact in `IMP-REPORT-WP-19 §12`; the F-1 remediation recorded in `IMP-REPORT-WP-19 §13`; **no governance document claimed a Gate 1 pass** prior to this recording pass; `IRA-C132` still **🟡 AMBER** (not upgraded); `CAP-001` line 105 unchanged; the delivery-map C-132 row unchanged (under-claims); C-023 / WP-17 / WP-18 artifacts untouched.

### Independently executed by the re-review reviewer

| Command | Observed result |
|---|---|
| `pytest tests/test_notification_establishment.py -q` | **25 passed**, 0 failed |
| `pytest -q` (full AuthService regression) | **901 passed**, 0 failed (167.93s) |
| `alembic heads` / `alembic history` | single head `d4e5f6a7b8c9`; linear `c3d4e5f6a7b8 → d4e5f6a7b8c9` |
| `npx tsc --noEmit` (frontend) | exit 0 |
| `npx eslint` (3 changed frontend files) | exit 0 |
| `npx next build` | exit 0, all routes compiled, no new route |
| Own from-scratch runtime probe — Part A (7 fixed-code security re-tests) + Part B (pre-fix negative control) | **11/11 checks passed** |

### Non-material observations (7, carried forward — inputs to Gates 2 and 5, not new scope)

1. **N-1** — stale `WPR-001` WP-19 row (under-claims; not a false Gate-1-pass claim; Gate 5 reconciliation item; matches WP-17/WP-18 precedent). *(This recording pass reconciles it additively — see `IMP-REPORT-WP-19 §14` / the WPR-001 maintenance note.)*
2. **N-2** — stale delivery-map C-132 row ("WP not yet chartered"; under-claims; Gate 5 item).
3. **N-3** — `IRA-C132` acceptance recorded via the charter / `WPR-001` note rather than inside `IRA-C132` (matches the `IRA-C023` precedent).
4. **N-4** — `updated_at` column beyond `TDS-C132 §6.6` (established AuthService convention across three sibling tables; no behavioural effect).
5. **N-5** — the F-1 gate's caller-vs-header 403 is not `DENIED`-audited (it is raised in the shared WP-10 dependency before the service is constructed; identical to every other consumer of that gate; the middleware access log still records it). Optional hardening.
6. **N-6** — no distinct `CLAUDE.md §20.6` confirmation state for the non-destructive acknowledge (inline "Acknowledging…" transient + terminal "Acknowledged" label present).
7. **N-7** — SQLite test harness stores `DateTime(timezone=True)` tz-naive and does not enforce FKs like production PostgreSQL (TD-096 / TD-159 / TD-160 class, repository-wide; Gate 2 harness production-parity checklist item, not a WP-19-specific defect).

---

## GATE 1 RE-REVIEW DETERMINATION

**✅ PASS.** F-1 is demonstrably closed (403, zero rows) with a working negative control proving the probe reproduces the pre-fix defect and the fix eliminates it; the caller-vs-header binding is proven; valid same-tenant establish still works; PLATFORM_ADMIN positive and negative controls conform to the WP-10 precedent; recipient-facing isolation and acknowledge idempotency are intact; schema/migration are field-by-field faithful with a single additive Alembic head; the four-route API, audit wiring, and frontend extension are conformant; the full AuthService suite is green (901/901) with no regression; no scope was expanded and no governance document is contradicted. No material tenant-isolation or security defect remains.

**This determination is scoped to WP-19 / C-132 BA-01 only. It is not a capability-wide C-132 readiness statement — C-132 remains 🟡 AMBER (`IRA-C132`, unchanged).**

## RECOMMENDATION FOR GATE 2

~~**Eligible: YES.** WP-19 BA-01 is now eligible for a separate Repository Owner authorization of the Gate 2 Verification & Validation Audit (`CLAUDE.md §19.7b`), to be performed by a further fresh-context reviewer uninvolved in the implementation, the first Gate 1 review, this re-review, or the F-1 remediation. **This document does not authorize or perform Gate 2.**~~ *(Superseded 2026-09-08 — the Gate 2 V&V Audit has since been performed and PASSED.)* A fresh-context reviewer uninvolved in the implementation, the original Gate 1 review, the F-1 remediation, the Gate 1 re-review, or the Gate 1 PASS recording independently returned **✅ Gate 2 V&V PASS** on 2026-09-08 — **24 PASS / 0 PARTIAL / 0 FAIL** Requirements Traceability Matrix, **0 material findings**, **8 non-material observations (O1–O8)**, with a from-scratch negative control that reproduced the pre-fix F-1 defect (HTTP 201 + persisted cross-tenant row) and confirmed the fix closes it (HTTP 403, zero rows), plus independent re-execution of 25/25 targeted + 901/901 full AuthService regression + 40/40 runtime probe + clean `tsc`/`eslint`/`next build` + single Alembic head `d4e5f6a7b8c9`. **The Gate 2 V&V result of record is `IMP-REPORT-WP-19 §15`; `CERT-WP-19` remains the Gate 1 record of record.** The seven non-material observations above (N-1…N-7) plus the Gate 2 reviewer's eight (O1–O8, `IMP-REPORT-WP-19 §15.5`) are inputs to the Gate 5 Release Readiness Audit — particularly **O1** (`SER-001` `SE-018` still "Deferred"; no Strategic Enhancement Review has reclassified it to "Partially Implemented") and **O2** (`WPR-001` / delivery-map WP-19 / C-132 governance-mapping staleness). **Gate 3 and Gate 4 were NOT TRIGGERED** (Gate 2 found no material defect). **Gate 5 remains PENDING / NOT RUN**, awaiting a separate Repository Owner authorization and a further fresh-context reviewer.

---

~~*End of CERT-WP-19 — Gate 1 of 5. Gate 1: ❌ FAIL (first attempt, F-1) → F-1 remediation → ✅ PASS (fresh independent re-review). Gates 2–5: NOT RUN.*~~ *(Superseded 2026-09-08.)*

~~*End of CERT-WP-19 — Gate 1 of 5. Gate 1: ❌ FAIL (first attempt, F-1) → F-1 remediation → ✅ PASS (fresh independent re-review). Gate 2 V&V: ✅ PASSED (fresh independent audit, 2026-09-08 — result of record `IMP-REPORT-WP-19 §15`). Gates 3/4: NOT TRIGGERED. Gate 5: PENDING / NOT RUN. WP-19 is NOT closed, NOT certified, NOT release-ready; C-132 remains 🟡 AMBER.*~~ *(Superseded 2026-09-09.)*

*End of CERT-WP-19. Gate 1: ❌ FAIL (first attempt, F-1) → F-1 remediation → ✅ PASS (fresh independent re-review, 2026-09-06). Gate 2 V&V: ✅ PASSED (fresh independent audit, 2026-09-08 — `IMP-REPORT-WP-19 §15`). Gates 3/4: NOT TRIGGERED. Gate 5 Release Readiness: ✅ PASSED (fresh independent audit, 2026-09-09 — `IMP-REPORT-WP-19 §16`). **WP-19 / C-132 BA-01: FORMALLY CLOSED — CERTIFIED — RELEASE-READY** (`IMP-REPORT-WP-19 §17`, 2026-09-09; repository commit outstanding). Closure applies to WP-19 / BA-01 only; C-132 capability-wide remains 🟡 AMBER; all deferred C-132 scope remains deferred. The original Gate 1 FAIL and the full gate history are preserved verbatim above.*
