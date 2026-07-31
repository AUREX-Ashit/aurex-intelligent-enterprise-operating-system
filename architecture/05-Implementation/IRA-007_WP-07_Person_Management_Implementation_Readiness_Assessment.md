# IRA-007 — WP-07 Implementation Readiness Assessment

**Work Package:** WP-07 — Person Management (C-006)
**Governing Charter:** `WP-07_Person_Management.md` (CHARTERED, committed `1811985`)
**Governing Capability Specification:** `PE-001-C006_Person_Management.docx`, Version 1.1 (Gold Standard correction pass) — read directly from `word/document.xml` (unzip-and-parse method, per this repository's own established precedent), not from any secondhand summary.
**Primary Specification:** `URA-001` (Person/Identity/Membership semantics, `ADR-001`). Cross-Specification Dependency: `ERG-001` (Membership home-node context only).
**Documents Reviewed:** `CLAUDE.md` (§14, §16, §17, §18, §19.1–§19.8), `METH-002`, `ADR-017`, `IMP-001` (§5.4, §6.2a/§6.2b, §6.3, §6.7), `CMD-001 §26.3a` (Business Object Eligibility Test), `WPR-001`, `WP-REG-001`, `DOC-000`, `WP-07_Person_Management.md`, `PE-001-C006` v1.1 in full (Chapters 1–9), `URA-001` (§2, clauses 13/15/16/17a/17b/28), the existing AuthService repository structure (`models/person.py`, `models/identity.py`, `routers/person.py`, `services/person_recognition_service.py`, `services/establish_person_context_service.py`, `repositories/person_repository.py`, `repositories/identity_repository.py`, `schemas/person.py`, `tests/test_person.py`, `middleware/tenant.py`, `main.py`).

---

## 1. Executive Summary

WP-07 realizes `PE-001-C006` v1.1's full architecture: 1 Capability Experience Blueprint (`CRB-C006`), 7 Enterprise Experience Blueprints (`ERB-C006-01` through `07`), 12 Enterprise Experiences (`EX-C006-01` through `12`), 9 capability-specific Experience Contracts. No Business Capability Gap exists (Chapter 9.5's own CRB–ERB–EX Completeness Test passes: "No EX is orphaned; no ERB is unrealized"). No Capability Amendment is pending.

**Special governance requirement disposition (charter §4):** `EX-C006-01` (Recognize Incoming Person Reference, deterministic tier) and `EX-C006-02` (Establish New Person Context) already have real, working, tested implementation, committed `34cf7fe` — one day before `WP-00`, predating this repository's governance discipline entirely. Direct code review (§8 below) finds this implementation **conforms to `PE-001-C006` v1.1**, not merely to the pre-1.1 draft the specification's own Revision History describes as containing a confidence-based-recognition contradiction: the existing `PersonRecognitionService` is strictly deterministic-only and explicitly, honestly discloses (in its own docstring) that the probabilistic tier is unimplemented rather than silently folding an uncertain match into a confirmed outcome — which is exactly the categorical, two-tier Recognition Authority Rule (`PE-001-C006 §1.7`) v1.1 corrected the specification *to* state, not a violation of it. **Determination: REUSE AND CERTIFY**, not modify, not replace. This determination is based solely on repository evidence (§8), not assumed in either direction, per the charter's own instruction.

Ten Business Activities are proposed (§3), covering all 12 EXs — two EXs (`EX-C006-09`, `EX-C006-12`) are satisfied by construction rather than a dedicated new endpoint, for reasons specific to each and disclosed explicitly, not silently folded in (§3, §7).

**Business Object Eligibility (§26.3a):** four new persisted, audit/traceability-grade constructs are required (`PersonDistinctionDecision`, `PersonReconciliationDecision`, `PersonCorrection`, `PersonEnrichment`). Each is tested against `CMD-001 §26.3a`'s three-step eligibility procedure (§9 below) and **fails** the Cross-Experience Reference Test and the Governed Lifecycle test — none is retrieved by identity as Required/Consumed Context by a separately-invoked *later* EX; each is produced and consumed only within its own realizing EX's audit trail. **No new canonical Business Object registration, and no new ADR, is required** — the same negative-eligibility outcome `WP-04`'s own Comparison Context and Downstream Continuation Context already established precedent for.

**Readiness Decision: READY, at full scope (all 12 EXs, addressed via 10 Business Activities).** No external blocker exists (unlike `WP-05`'s own `WP-RTA-001` dependency) — `PE-001-C006`'s own Out-of-Scope list confirms Identity, Membership, Access, Role/Permission, Structure, and Workspace are none of them required inputs; the two hand-off EXs (`EX-C006-10`/`11`) transfer bounded context and record a caller-reported outcome only, mirroring `WP-02` `BA-10`'s and `WP-03`'s own already-accepted hand-off precedent, never calling into another capability's own API.

---

## 2. Capability Analysis

### 2.1 CRB-C006 (Chapter 2)

Experience Boundary: person-context establishment, recognition, understanding, distinction, ambiguity resolution, duplicate review, correction, enrichment, preservation and cross-capability hand-off. Eight Experience Outcomes (`C006-O01` through `O08`). Capability Collaboration (2.9): C-006 hands off to `C-001` (Identity) and `C-007` (Membership) as context-preserving hand-offs, never ownership transfers; `C-003`/`C-002` consume a resolved Person only downstream of Membership, never directly from C-006.

### 2.2 ERB Portfolio (Chapter 3)

| ERB | Name | Stage | Realizing EX |
|---|---|---|---|
| `ERB-C006-01` | Establish Person Context | Establish | `EX-C006-01`, `02` |
| `ERB-C006-02` | Understand Authoritative Person Context | Understand | `EX-C006-03` |
| `ERB-C006-03` | Distinguish and Resolve Person Ambiguity | Distinguish | `EX-C006-04`, `05` |
| `ERB-C006-04` | Review Potential Duplicate Person Context | Review Duplicate | `EX-C006-06` |
| `ERB-C006-05` | Correct Person Context | Correct | `EX-C006-07` |
| `ERB-C006-06` | Enrich Person Context | Enrich | `EX-C006-08` |
| `ERB-C006-07` | Preserve / Hand Off | Preserve / Hand Off | `EX-C006-09` through `12` |

### 2.3 Recognition Authority Rule (§1.7, load-bearing across every EX)

Deterministic recognition of an already-governed reference (e.g., an existing `Identity.email`) confirms an Authoritative Person Context with no new confirmation. Every probabilistic match — of any confidence, any candidate count, including exactly one candidate — always yields a Candidate Person Context and **SHALL NEVER become authoritative without explicit governed human confirmation.** No numeric confidence threshold exists anywhere in this specification.

### 2.4 Full Business Rule set (Chapter 7.3)

`BR-C006-001` through `012` — no new Authoritative Person Context without prior recognition; no Candidate ever treated as authoritative; ambiguity (including single-candidate) always human-decided; conflict always classified before resolution; duplicate always human-reviewed, never auto-merged; correction always preserves the prior value; enrichment always additive/sourced/sensitivity-classified; continuity persists without forced re-establishment; hand-off transfers only what's required and records an explicit outcome; a downstream rejection never alters the underlying Person; AI observations always distinguishable from authoritative fact; cross-tenant visibility governed exclusively by `URA-001-17a`.

---

## 3. Business Activities (candidate proposal — Pending Canonical Binding, per every prior IRA's own disposition for its own capability's EXs)

| BA | Realizes | Type | Disposition |
|---|---|---|---|
| **BA-01** | `EX-C006-01` (deterministic tier only) | Query/Recognize | **Reuse & Certify** existing `PersonRecognitionService` |
| **BA-02** | `EX-C006-02` | Create | **Reuse & Certify** existing `EstablishPersonContextService` |
| **BA-03** | `EX-C006-03` | Query | New — `GET /person/{person_id}` |
| **BA-04** | `EX-C006-04` | Update (decision) | New — `POST /person/distinguish` |
| **BA-05** | `EX-C006-05` | Update (classification) | New — `POST /person/{person_id}/resolve-conflict` |
| **BA-06** | `EX-C006-06` | Update (decision) | New — `POST /person/reconcile` |
| **BA-07** | `EX-C006-07` | Update | New — `POST /person/{person_id}/correct` |
| **BA-08** | `EX-C006-08` | Update | New — `POST /person/{person_id}/enrich` |
| **BA-09** | `EX-C006-10` | Update (hand-off) | New — `POST /person/{person_id}/handoff-to-identity` |
| **BA-10** | `EX-C006-11` | Update (hand-off) | New — `POST /person/{person_id}/handoff-to-membership` |
| — | `EX-C006-09` | (satisfied by construction) | No dedicated BA — see §7.1 |
| — | `EX-C006-12` | (satisfied by construction) | No dedicated BA — see §7.2 |

10 Business Activities cover all 12 EXs. This is the full authorized scope — no minimum-scope narrowing is applied, per §1's own readiness finding (no external blocker exists).

---

## 4. Context Discovery (IMP-001 §6.2a, Bounded Scan)

Scanned: `models/`, `repositories/`, `services/`, `routers/`, `schemas/` for `Person`, `Identity`, `Membership` (WP-03), and every existing `EX-C0XX` reference repository-wide (`grep -rohE "EX-C[0-9]{3}-[0-9]+"` — confirmed only `C001` through `C007` appear anywhere, and `C001` only as a citation, never an implementation). Confirmed: `Person`/`Identity` models and their two existing services are the entirety of pre-existing C-006 surface area; no other file references any `EX-C006-*` identifier.

---

## 5. Business Object Eligibility Analysis (CMD-001 §26.3a)

Applied to each of the four new persisted, audit/traceability constructs this Work Package requires:

| Candidate | Step 1 (Independent Identity) | Step 2 (Cross-Experience Reference) | Step 3 (Governed Lifecycle) | Result |
|---|---|---|---|---|
| `PersonDistinctionDecision` (`EX-C006-04`'s own decision record) | Pass — persists beyond the request | **Fail** — no other EX names it as Required/Consumed Context; only the resulting Authoritative Person Context (already-existing `Person`) is consumed downstream, not the decision record itself | Fail — created once, never later invalidated by a subsequent event | **Not eligible.** Negative Indicator 1 applies verbatim (named only within `EX-C006-04`'s own Produced Context). |
| `PersonReconciliationDecision` (`EX-C006-06`) | Pass | **Fail** — Chapter 6.3 states a confirmed-distinct decision invalidates the *signal*, not the decision record; no later EX retrieves the decision by identity | Fail — same reasoning | **Not eligible.** Same Negative Indicator. |
| `PersonCorrection` (`EX-C006-07`) | Pass | **Fail** — downstream EXs (`EX-C006-03`, `10`, `11`) consume the *corrected Person fact itself* (already on the `Person` row), never the `PersonCorrection` record by identity | Fail — the prior value is superseded at the moment of correction, not later | **Not eligible.** Same Negative Indicator. |
| `PersonEnrichment` (`EX-C006-08`) | Pass | **Fail** — same reasoning as `PersonCorrection` | Fail — same reasoning | **Not eligible.** Same Negative Indicator. |

**Finding, identical in kind to `WP-04`'s own precedent (Comparison Context, `TD-054`; Downstream Continuation Context, `BA-09`'s own disposition — neither registered, same test):** none of the four constructs is a canonical Business Object. Each is implemented as an ordinary audit/traceability table satisfying its own governing Business Rule (`BR-C006-003`/`005`/`006`/`007` respectively) — not registered under `CMD-001 §26.3`/`§26.4`, and no new ADR is raised for any of the four. This is a disclosed negative finding, not a silent omission, per `§26.3a`'s own closing sentence.

**Hand-off outcomes (`BA-09`/`10`) are not persisted at all** — mirroring `WP-02 BA-10`'s own `HandoffRejectionOutcome` precedent (a computed classification response plus an audit-log entry, no dedicated table), since `BR-C006-009`'s own "record an explicit accepted or returned outcome" is satisfied by `record_audit()`, the same basis every prior hand-off Business Activity in this repository already uses.

---

## 6. Context Lifecycle

| Context Construct | Realizing EX | Lifecycle |
|---|---|---|
| Authoritative Person Context | `EX-C006-01`/`02` (produced), `03`/`09`/`12` (read), `07`/`08` (mutated), `10`/`11` (referenced) | Long-lived — the `Person` row itself |
| Candidate Person Context | `EX-C006-01` (probabilistic tier — **not implemented**, see §8) | N/A within this Work Package's authorized scope |
| Ambiguity Context / `PersonDistinctionDecision` | `EX-C006-04` | Created once, closed on decision; audit-trail only (§5) |
| Reconciliation Decision / `PersonReconciliationDecision` | `EX-C006-06` | Created once, closed on decision; audit-trail only (§5) |
| Correction Context / `PersonCorrection` | `EX-C006-07` | Created once per correction; audit-trail only (§5) |
| Enrichment Context / `PersonEnrichment` | `EX-C006-08` | Created once per enrichment; audit-trail only (§5) |
| Hand-off Outcome | `EX-C006-10`/`11` | Ephemeral — computed response + audit log, never persisted (§5) |

---

## 7. Gap Analysis (IMP-001 §6.2b, category A–E)

**Category C** (Architecture requires completion — implementation-level only) for every Business Activity. No governance question, no missing Business Object (§5), no missing canonical dependency (§4).

### 7.1 `EX-C006-09` (Preserve Person Context Across Enterprise Journeys) — satisfied by construction, no dedicated BA

`EX-C006-09`'s own Trigger ("A recognized Person continues into a further Enterprise Journey") and Context Produced ("Person Journey Continuity Context... delivered to the next Enterprise Experience") describe exactly the same technical operation `BA-03`'s `GET /person/{person_id}` already performs: a caller who already holds a `person_id` re-invokes the same read rather than re-establishing. Unlike `WP-04`'s `EX-C005-12` (which produced a genuinely distinct persisted resource, `RSC-000001`, that its own prior Business Activity's endpoint could not serve), `EX-C006-09` produces no distinct resource of its own — there is nothing for a dedicated endpoint to expose that `BA-03` does not already expose. Disclosed explicitly, not silently folded in.

### 7.2 `EX-C006-12` (Continue from Person Context Decision) — satisfied by construction, no dedicated BA

Every one of `BA-01` through `BA-10`'s own response already returns the resulting Authoritative Person Context (or a decision record referencing it by `person_id`) directly to its caller — `EX-C006-12`'s own Business Value ("the next Enterprise Experience begins from a known, authoritative state rather than reconstructing it") is satisfied by that same already-returned response, plus `BA-03`'s own general-purpose read for any caller needing to re-fetch it later. No distinct "completion" resource exists in `C-006`'s own architecture for a dedicated endpoint to expose (contrast `WP-04`'s `RSC-000001`, a real, distinct, persisted completion record `EX-C005-12`'s own dedicated `BA-09` genuinely needed to expose). Disclosed explicitly.

### 7.3 `EX-C006-01`'s probabilistic tier — pre-existing, already-disclosed scope boundary, not newly narrowed by this IRA

The existing `PersonRecognitionService`'s own docstring already discloses: *"This service implements only the deterministic tier of the Recognition Authority Rule... It does not perform probabilistic matching, similarity scoring, AI-assisted matching, or candidate ranking."* This IRA does not invent this boundary — it is inherited, unmodified, from the pre-existing, already-tested implementation being certified (§1, §8). Building a genuine similarity/fuzzy-matching engine is a substantial, separate algorithmic undertaking `PE-001-C006` itself does not specify a concrete mechanism for (it specifies only the *governance* of a probabilistic result once produced, never how one is computed) — inventing a scoring algorithm here would be an unauthorized architectural addition, not an implementation detail, per `CLAUDE.md §18`.

**Consequence for `BA-04` (Distinguish):** `EX-C006-04`'s own Context Required is "Candidate Person Context, of any size — including exactly one candidate." Since `EX-C006-01`'s own probabilistic tier that would normally produce this input is out of this Work Package's authorized scope (§7.3 above, inherited not invented), `BA-04` is implemented as a **governance mechanism operating on a caller-supplied candidate set** (one or more `person_id`s identified by a Person Steward through some means outside this Work Package's own scope — manual observation, a future AI signal, a future probabilistic matcher) rather than one fed automatically by `EX-C006-01`. This still delivers `EX-C006-04`'s own real Business Value (governed, non-auto-selecting confirmation, identical treatment of a single-candidate and multi-candidate set, per the Recognition Authority Rule) without fabricating the separate, unspecified candidate-generation algorithm. Disclosed as `TD` (§10), not silently narrowed.

---

## 8. Existing Reusable Implementation — Special Governance Requirement Disposition

Per the charter's own explicit instruction: *"Base this determination solely on repository evidence. Do not assume reuse. Do not assume replacement."*

**Files reviewed in full:** `models/person.py`, `models/identity.py`, `schemas/person.py`, `repositories/person_repository.py`, `repositories/identity_repository.py`, `services/person_recognition_service.py`, `services/establish_person_context_service.py`, `routers/person.py`, `tests/test_person.py` (9 tests), `middleware/tenant.py` (existing `/person/recognize`/`/person/establish` exemption), `main.py` (existing `/person` router registration).

**Conformance findings, each independently checked against `PE-001-C006` v1.1's own text, not assumed:**

1. **Recognition Authority Rule (§1.7) conformance — PASS.** `PersonRecognitionService.recognize()` performs deterministic lookup only (`IdentityRepository.get_by_email_with_person()`), returns exactly `MATCHED` or `NO_CANDIDATE` — never a probabilistic, confidence-scored, or auto-confirmed result. This is the corrected v1.1 rule, not the pre-1.1 draft's confidence-based contradiction the specification's own Revision History describes fixing.
2. **`BR-C006-001` conformance — PASS.** `EstablishPersonContextService.establish()` re-runs recognition as a runtime precondition (not trusting the caller's own claim that recognition already ran) before creating a `Person` — matching `EX-C006-02`'s own stated Trigger exactly.
3. **Scope boundary (`PE-001-C006 §1.4`) conformance — PASS.** Neither service creates an `Identity` or `Membership` — confirmed by full-method code read, no `Identity(...)`/`Membership(...)` construction anywhere in either file.
4. **Tenant-independence (`URA-001-15`) conformance — PASS.** `/person/recognize` and `/person/establish` are both exact-listed in `middleware/tenant.py`'s exemption, confirmed by two dedicated tests (`test_recognize_does_not_require_tenant_header`, `test_establish_person_does_not_require_tenant_header`).
5. **No Authorization dependency — matches `EX-C006-01`/`02`'s own text (URA-001-15's bootstrap-safe design), disclosed explicitly in both router docstrings, not silently omitted.**
6. **9/9 existing tests pass** (independently re-run, §12).

**Disclosed pre-existing limitations, found by this review, not previously registered (§10 Technical Debt):**

- A **known, disclosed, unresolved race condition** in `establish()`: recognition (read) and creation (write) are not isolated within the surrounding request transaction — two concurrent requests for the same reference can both pass recognition before either commits, producing two `Person` rows. The implementer's own code comment discloses this in detail and explicitly defers a fix "until this capability's canonical persistence strategy defines how duplicate-creation races should be handled." Carried forward, not silently inherited.
- Two `TODO(metrics)`/`TODO(events)` comments citing a document, `FC-IB-001`, that **does not exist anywhere in this repository** — confirmed by repository-wide search. This is a dangling citation from before this Work Package's own chartering, not something this IRA can resolve (the cited document cannot be located to verify what it actually specified); disclosed as a Technical Debt item (§10), not silently carried or silently deleted.
- `PersonRecognitionOutcome` enum has only `MATCHED`/`NO_CANDIDATE` — the schema's own comment already discloses a third, `CANDIDATE`, outcome is deliberately absent because the probabilistic tier is unimplemented (§7.3). Consistent, not a new finding.

**Determination: REUSE AND CERTIFY.** No modification to `BA-01`/`BA-02`'s existing code is required or performed by this Work Package. Both proceed directly to Independent Certification alongside the eight new Business Activities.

---

## 9. Readiness Decision

**READY**, at full scope (all 12 EXs, addressed by 10 Business Activities per §3, plus two EXs satisfied by construction per §7.1/§7.2). No governance question outstanding. No missing Business Object. No missing dependency (§4). No external blocker (unlike `WP-05`'s own `WP-RTA-001` dependency) — every input `PE-001-C006`'s own architecture requires already exists in this repository or is self-contained within this Work Package's own scope.

---

## 10. Recommendations / Anticipated Technical Debt

The following are anticipated, not yet raised (raised formally in `TECH-DEBT.md` at implementation time, per `CLAUDE.md §19.8`, mirroring every prior IRA's own disposition):

1. `BA-03` through `BA-10` gated on the existing `PLATFORM_ADMIN` role claim only — `PE-001-C006`'s own Participating Personas name "Person Steward" (and, for self-service paths, "Person Context Subject"/"External Collaboration Persona"), none of which exists as a distinct, enforceable claim today. Same class of gap as `TD-021` through `TD-090`.
2. The pre-existing, disclosed race condition in `establish()` (§8) — inherited, not introduced by this Work Package, carried forward as its own tracked entry rather than left only in a code comment (`CLAUDE.md §19.8.2`).
3. The dangling `FC-IB-001` citation (§8) — recorded so a future reviewer does not need to re-discover that the cited document cannot be located.
4. `EX-C006-01`'s probabilistic tier (§7.3) and `EX-C006-04`'s consequent dependency on a caller-supplied, not platform-generated, candidate set — a future, separately-scoped capability (fuzzy/AI-assisted candidate generation) would complete `EX-C006-04`'s own upstream feed.
5. `person_corrections`/`person_enrichments` operate on `Person`'s three existing fields (`first_name`/`last_name`/`display_name` for correction) or a free-form `attribute_name` (for enrichment, since `Person` has no other structured fields to enrich) — a future capability could extend `Person`'s own schema with additional structured fields as real enrichment consumers emerge, not invented speculatively here.

---

## 11. Business Object Registration

**None required.** See §5 — all four candidate constructs fail `CMD-001 §26.3a`'s eligibility test (Steps 2 and 3), matching `WP-04`'s own precedent for Comparison Context and Downstream Continuation Context. No new ADR is raised by this Work Package for Business Object registration.

---

## 12. Repository-Owner Authorization to Begin

Authorized to begin at **full scope** (10 Business Activities, all 12 EXs addressed), per the Repository Owner's own explicit execution authorization ("You are now authorized to execute WP-07... Otherwise continue autonomously until WP-07 reaches CLOSED status through every mandatory repository quality gate"). No further authorization checkpoint is required before implementation begins, per that same instruction.

**Independently re-run at IRA time:** `pytest tests/test_person.py -v` — 9/9 passed. `alembic heads` — single head, `f3a7c5e9b2d8`, unchanged.

---

*End of IRA-007.*
