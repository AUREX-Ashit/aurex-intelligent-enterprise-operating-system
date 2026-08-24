# WP-15 (PROPOSED) — BA-01 (C-066 Evidence Management) — Understand Evidence Context — Business Activity Charter

**Work Package:** WP-15 — **PROPOSED, not yet recorded in `WPR-001`/`WP-REG-001`** (see Phase 1 determination, this same governance pass). This charter is prepared under the same evidence-based next-number determination; it is not itself the act of assignment. WP-15 becomes authoritative only once `WPR-001 §2` and `WP-REG-001` are actually updated — a separate, explicit Repository Owner step, not performed by this document. *(Historical drafting-time statement, preserved per this repository's own no-silent-fix discipline — accurate at the moment this charter was first drafted, before formal registration.)*

**Registration status correction (2026-08-24, subsequent governance pass — independent charter review finding M-1, remediated):** the sentence immediately above described WP-15 as "not yet recorded" because it was written before formal registration occurred. **WP-15 has since been formally registered** in `WPR-001 §2` and `WP-REG-001 §5` (a separate, explicit Repository Owner action, per direct instruction "C-066 / WP-15 — Formal WP Registration + Independent BA-01 Charter Review," 2026-08-24) as **PROPOSED/CHARTERED — implementation NOT authorized**, the same status this charter itself carries. This correction updates the charter's own currency, not its substance — WP-15 remains unauthorized for implementation either way; only the "has it been entered in the registers yet" fact has changed, from no to yes.
**Business Activity:** BA-01 — Understand Evidence Context
**Capability:** C-066 Evidence Management (`CAP-001` line 75, Domain D-004 Enterprise Operations, Active)
**Status:** **PROPOSED — NOT YET AUTHORIZED FOR IMPLEMENTATION.** This charter organizes and formalizes the already-accepted `IRA-C066` and the independently reviewed, remediated, and verified `TDS-015`, together with the Repository Owner decisions recorded in `TDS-015 §24`, into the charter-level structure this repository's own precedent (`WP-14 BA-04`) established. It does not itself grant Implementation Authorization (§20 below).
**Prepared under:** direct Repository Owner instruction ("C-066 Evidence Management — WP Assignment and BA-01 Charter Preparation"), 2026-08-24.

**A note on document type, disclosed rather than assumed (mirrors `WP-14 BA-04`'s own identical disclosure):** this repository's own established convention charters at the **Work Package** level (`WP-XX_<Name>.md`), with each Business Activity's own charter-level detail ordinarily specified *within* the governing IRA. `WP-14 BA-04`'s own charter (`WP-14_BA-04_Establish_Knowledge_Asset_Business_Activity_Charter.md`) departed from that convention once already, per direct Repository Owner instruction, establishing a Business-Activity-level charter as a real (if still singular) repository precedent. This document follows that same shape, again per direct instruction, for the same reason: `IRA-C066` and `TDS-015` together already carry BA-01's own full governing content; this charter organizes it, and separately, explicitly records what §16 below newly verifies rather than restating those two documents as new decisions.

**Governing basis for BA-01, stated explicitly:** `CAP-001` (C-066 registration) → `SD-002 §6` (`SD-002-040` through `SD-002-050`) → `Master_Technical_Architecture.md` (`evidence_registry`, pre-AMD base schema — no AMD number governs its own creation, distinct from `AMD-012`-era tables) → `IRA-C066` (accepted, 2026-08-24) → `TDS-015` (independently reviewed, remediated, remediation independently verified) → `TDS-015 §24` (Repository Owner Decision Recording, `RO-DEC-C066-BA01-01` through `-05`).

---

## Classification Key

- **A** — already determined by governing documents (`CAP-001`, `SD-002`, `IRA-C066`, `TDS-015`)
- **B** — determined by repository precedent (already-certified patterns this charter reuses, not invents)
- **C** — an implementation detail (safe to resolve during implementation without a dedicated architecture document)
- **D** — requires a Repository Owner decision (genuinely open, not resolved by any existing document)
- **D → RESOLVED** — was **D**, now resolved by a recorded `RO-DEC-C066-BA01-XX` (`TDS-015 §24`)

---

## 1. Business Activity Identity — [A]

BA-01, proposed WP-15, Capability C-066 Evidence Management (`CAP-001` D-004, Active). Governed physical Business Object: `evidence_registry` (pre-AMD base schema, `Master_Technical_Architecture.md` ~line 2342; not an `AMD-012`-family amendment). Read-only — no lifecycle transition, no write path.

## 2. Business Intent — [A]

Verbatim basis, `IRA-C066 §7`: *"retrieve the current governed state of an Evidence record — by identity, or by a filtered criterion — without establishing, mutating, or altering any object returned."* Realizes `SD-002-040`'s "first-class... governed object" framing for the read side and operationalizes `SD-002-044`'s "reusable across objects" principle by making that reuse queryable for the first time (`TDS-015 §3`).

## 3. Trigger — [A]

Caller-invoked, not event-triggered — a direct `GET` request, the same shape as every existing AIService read endpoint (`TDS-015 §9`). No downstream Business Activity is triggered by BA-01 (pure read, no state change, no Domain Event — §12 below).

## 4. Actor / Persona — [A, resolved by `RO-DEC-C066-BA01-03`]

No `PE-001-C066` capability specification exists (`IRA-C066 §3.7`). Per `RO-DEC-C066-BA01-03` (`TDS-015 §24`, APPROVED Option C): **any authenticated member of the owning Organization** — not `PLATFORM_ADMIN`-only. Gated by `AIService/dependencies.py::get_current_claims` (authentication only); Organization-scoping is performed inside the repository query, not the authorization layer (`TDS-015 §11`).

## 5. Preconditions — [A]

- The caller's own Organization (`organization_master` row) must exist — standard, platform-wide precondition.
- The `evidence_registry` row(s) being read must already exist — established exclusively by WP-11 BA-03 (`create()`) or WP-14 BA-05 (`create_linked()`), both already closed and certified, both outside BA-01's own scope (`TDS-015 §2`, `IRA-C066 §4`). BA-01 has no precondition on any *new* Evidence being created — it reads whatever already exists.

## 6. Input Contract — [A]

Per `TDS-015 §9`:
- `GET /evidence/{evidence_id}` — `evidence_id` (UUID, path parameter).
- `GET /evidence` — `linked_entity_type`, `linked_entity_id`, `evidence_source`, `evidence_type` (all independently optional query parameters).

`organization_id` is never caller-supplied — derived from the caller's own claims (§4), mirroring every existing AIService read precedent.

## 7. Business Rules — [A]

- Read-only — no `evidence_registry` row is created, mutated, transitioned, or deleted (`TDS-015 §5`).
- A caller never receives another Organization's own row (§11 below).
- A foreign Organization's `evidence_id` supplied explicitly is rejected as 404, not 403 — anti-enumeration, `TDS-015 §5`/§13, correctly cited to the WP-12 BA-03 cross-tenant-disclosure precedent + `CLAUDE.md §21.4`(c).

## 8. Persistence Target — [A]

`evidence_registry`, hosted in `AIService` (the existing physical location — zero migration, `TDS-015 §8`). Per `RO-DEC-C066-BA01-01` (`TDS-015 §24`): the table's own three-way logical-service-ownership ambiguity (`IRA-C066 §3.5`) remains open and undecided, but is confirmed **not** a BA-01 precondition — `AIService` proceeds as the pragmatic physical host.

## 9. State / Lifecycle Transition — N/A

Not applicable — `evidence_registry.curation_status` or equivalent lifecycle field does not exist; Evidence rows have no lifecycle state BA-01 observes or changes. BA-01 is a pure projection of already-persisted columns.

## 10. Authorization — [A, resolved by `RO-DEC-C066-BA01-03`]

`get_current_claims` (authenticate-only) + repository-layer Organization scoping, per §4 above. No `PLATFORM_ADMIN` requirement for ordinary same-Organization reads. `PLATFORM_ADMIN` retains cross-Organization access for the single-item `GET /evidence/{evidence_id}` path only (`TDS-015 §9`/§13) — **not** for the list path, per `RO-DEC-C066-BA01-05` (§10a below).

### 10a. `PLATFORM_ADMIN` List-Endpoint Scope — [A, resolved by `RO-DEC-C066-BA01-05`]

`GET /evidence` remains scoped to the caller's own Organization for **every** caller, including `PLATFORM_ADMIN` — no cross-Organization listing capability, no target-Organization query parameter. A future requirement for cross-Organization Evidence listing must be handled as a separately scoped and governed change (`TDS-015 §24`).

## 11. Tenant Boundary — [A]

`evidence_registry.organization_id` is `NOT NULL` (`TDS-015 §4`, independently re-verified against `Backend/Services/AIService/models/search.py`) — every row is strictly Organization-owned. Query predicate is an exact match (`organization_id == caller_organization_id`), never an `OR organization_id IS NULL` fallback — `evidence_registry` has no platform-wide row, structurally distinct from `vector_index_registry` (`TDS-015 §11`).

## 12. Events / Outcomes — [A]

None published — a read has nothing to announce (`IRA-C066 §7`, `TDS-015 §14`, mirroring `IRA-006`'s BA-01 precedent — citation independently corrected in `TDS-015` to `IMP-REPORT-WP-06`/`CERT-WP-06`, not `IRA-006` itself).

## 13. Error / Rejection Conditions — [A]

- `evidence_id` not found, or found but belongs to a different Organization and caller is not `PLATFORM_ADMIN` → **404** (§7 above; not 403 — anti-enumeration).
- Caller unauthenticated → 401/403 per `get_current_claims`'s own existing behavior.
- Malformed query parameter (e.g. non-UUID `linked_entity_id`) → 400, ordinary FastAPI/Pydantic coercion, no bespoke validation (`TDS-015 §13`).
- Success, including an empty list for `GET /evidence` when no row matches → 200 (not 404 — an empty list is a valid answer to a list query).

## 14. Idempotency Expectations — [A]

Naturally idempotent — pure read, no side effect (`IRA-C066 §7`).

## 15. Audit / Observability Expectations — [A]

**Audit: none.** A pure read produces no state change for `SD-002-054`'s seven audit questions to describe — correctly cited in `TDS-015 §14` to `IMP-REPORT-WP-06` line 26 and independently confirmed by `CERT-WP-06`'s own code-level check (`organization_service.py:405`, `structural_completion_service.py:163`, neither calls `record_audit()`/`publish_event()`). Ordinary platform-wide request logging applies; no bespoke observability design is required.

## 16. Dependencies — [A]

None outstanding (`IRA-C066 §12`, `TDS-015 §17`, both independently re-verified this session): `evidence_registry` (pre-existing, populated by WP-11/WP-14, both closed and certified), `organization_master` (pre-existing, cross-service logical FK), and `get_current_claims` (pre-existing, `AIService/dependencies.py`) are all already real and available. No dependency on WP-13's own blocked retrofit scope (no `domain_id` column exists on `evidence_registry`). No dependency on `SE-031`/`evidence_fusion_registry` (`IRA-C066 §3.6`, `TDS-015 §1`) — confirmed a wholly separate, unimplemented table for a materially different purpose.

## 17. Acceptance Criteria — [A]

`GET /evidence/{evidence_id}` returns the caller's own Organization's Evidence row (200) or 404 for any other case (§13). `GET /evidence` returns every Evidence row matching the caller's own Organization and the supplied filters (200, possibly empty). No row from any other Organization is ever returned or disclosed to exist, under any authorization option or filter combination (`CLAUDE.md §21.4`).

## 18. Test Obligations — [A]

Per `TDS-015 §15`: unit tests against the new repository read method(s) (existence, filtering, the exact-match tenant predicate specifically) + API tests (200/404/400/403 paths) + the Mandatory Tenant-Isolation Test Checklist (`CLAUDE.md §21.4`): (a) two distinct, unrelated Organizations seeded, no shared `evidence_registry` row; (b) a caller in one Organization cannot retrieve or infer another Organization's own Evidence row through either endpoint; (c) an unrelated Organization's `evidence_id` supplied explicitly to the single-item endpoint is rejected as 404. Test pattern follows the existing per-file `test_two_orgs_no_shared_row` convention (`TDS-015 §4`, corrected — not a shared `conftest.py` fixture).

## 19. Out-of-Scope Boundaries — [A]

- Evidence creation, update, deletion, or purge — remains WP-11's and WP-14's own exclusive province (`TDS-015 §1`, `IRA-C066 §4`).

**Anticipated Technical Debt (all four items, `TDS-015 §18`, complete carry-forward — independent charter review finding M-3, remediated; two items added, none invented, none reclassified):** none of the following is created or worsened by BA-01, and none is `CLAUDE.md §19.8.5`-class (none defeats BA-01's own stated Business Intent; none weakens an existing tenant-isolation boundary — `organization_id NOT NULL` is enforced at the application layer exactly as every other WP-11-through-WP-14 read path already does), per `TDS-015 §18`'s own unchanged classification:

- No physical RLS enforcement on `evidence_registry` — same class as `TD-150` (BA-05), repository-wide, not C-066-specific (`TDS-015 §18` item 1).
- Retention-floor enforcement (`SD-002-048`, `SE-051`) — disclosed Technical Debt, not a BA-01 blocker (`TDS-015 §18` item 2).
- Cross-object lineage (`SD-002-049`) — genuinely unimplemented for any object type in this repository, not created or worsened by BA-01 (`TDS-015 §18` item 3).
- Interim authorization-granularity gap under `RO-DEC-C066-BA01-03`'s now-selected Option C, if `SD-002-050`'s own "human-governed" framing eventually warrants a distinct Evidence-reviewer persona not yet modeled anywhere in this repository (`TDS-015 §18` item 4).

- `SE-031`/`evidence_fusion_registry`/AI Evidence Fusion — a wholly separate, unimplemented, deferred future enhancement (§16 above).
- Cross-Organization Evidence listing for any caller, including `PLATFORM_ADMIN` — `RO-DEC-C066-BA01-05` (§10a above).
- Any new tenant-header (`X-Tenant-ID` or equivalent) API contract element — `RO-DEC-C066-BA01-03` (§4/§10 above).
- Frontend / Enterprise Experience of any kind — `RO-DEC-C066-BA01-02` (§21 below).
- Any new database migration — `TDS-015 §8` confirms none is required; none is authorized by this charter either way.
- Unrelated Knowledge Management (C-091) / Enterprise Discovery (C-090) / Knowledge Graph (C-092) work — BA-01 touches none of WP-14's own capability scope.

## 20. Implementation Readiness Classification

**Classification: design-complete, decisions recorded, NOT YET IMPLEMENTATION-AUTHORIZED.** All three genuinely open Repository Owner policy decisions this Business Activity required (`RO-DEC-C066-BA01-02/03/05`) are now resolved in principle (`TDS-015 §24`). The two remaining `IRA-C066 §14` items (`-01` hosting ambiguity, `-04` docstring) are confirmed non-blocking. **This charter does not itself grant Implementation Authorization** — **citation corrected (independent charter review finding M-2):** the governance anchor for this no-self-authorization discipline is `CLAUDE.md §19.7`'s self-certification prohibition — verbatim, `CLAUDE.md` line 864: *"The implementation agent SHALL NOT certify its own work."* (an earlier remediation pass of this charter quoted this imprecisely as "the implementing agent"; corrected here to the exact source wording) — together with the established Repository Owner authorization practice this session has followed throughout — not `§19.1` ("Identify Governing Canonical Assets"), which an earlier draft of this charter cited incorrectly. Per that discipline and the two-step chartering-then-authorization precedent `WP-10`/`WP-11`/`WP-12`/`WP-14` each already established, a separate, explicit, subsequent Repository Owner instruction ("WP-15 Implementation Authorization" or equivalent) remains required before implementation may begin.

**Disclosure (independent charter review finding F-3, addressed):** the identical `§19.1` mis-citation this paragraph corrects for this charter is also present, unremediated, in `IRA-C066` (its own §18) and in `TDS-015` (its own §23, and again in §24). Those two documents were **intentionally not modified** by this or any prior remediation pass of this charter — governance-correction scope for each remediation pass has been deliberately confined to the single document under active review, per direct Repository Owner instruction each time. This is a citation/documentation-accuracy issue only: it does not change the authorization status recorded in either document (both `IRA-C066` and `TDS-015` correctly and independently state implementation is not authorized, via their own surrounding text, regardless of which `CLAUDE.md` section is cited for the underlying discipline), and it does not alter any Repository Owner decision, capability, WP, or BA boundary. Correcting it in `IRA-C066`/`TDS-015` themselves, if desired, remains a separate, future, explicitly-scoped task.

## 21. Enterprise Experience Scope Decision — `CLAUDE.md §20.3` [D → RESOLVED, `RO-DEC-C066-BA01-02`]

**RESOLVED, Option A: Backend-only.** Per `RO-DEC-C066-BA01-02` (`TDS-015 §24`, APPROVED): BA-01 is authorized to deliver the backend capability only, as the disclosed exception `CLAUDE.md §20.3` permits — mirroring `WP-14 BA-05`'s own precedent for the identical exception. No frontend, navigation, or Enterprise Experience implementation is authorized as part of BA-01.

## 22. Repository Owner Decisions Recorded (summary — full text and evidentiary basis: `TDS-015 §24`)

| Decision ID | Disposition |
|---|---|
| `RO-DEC-C066-BA01-01` | No new decision required at this stage — hosting-service ambiguity left open, non-blocking (§8 above). |
| `RO-DEC-C066-BA01-02` | APPROVED, Option A — Backend-only (§21 above). |
| `RO-DEC-C066-BA01-03` | APPROVED, Option C — authenticated same-Organization reads, repository-layer scoping, no `PLATFORM_ADMIN` requirement for ordinary reads (§4/§10 above). |
| `RO-DEC-C066-BA01-04` | No governance decision required — editorial/implementation-time docstring correction only. |
| `RO-DEC-C066-BA01-05` | APPROVED, Option (i) — no `PLATFORM_ADMIN` cross-Organization listing via `GET /evidence` (§10a above). |

## Final Determinations

BA-01's own full governing chain — `CAP-001` → `SD-002 §6` → `IRA-C066` (accepted) → `TDS-015` (independently reviewed, remediated, remediation independently verified) → `TDS-015 §24` (Repository Owner decisions recorded) — is now complete and internally consistent, independently re-verified in the preparation of this charter (§1–§19 above). No new architecture, business rule, entity, table, API contract element, or authorization mechanism is introduced by this charter beyond what `TDS-015` already designed and this session's own Repository Owner decisions already resolved. This charter's own only remaining open items are the two already-confirmed-non-blocking `RO-DEC-C066-BA01-01`/`-04` dispositions (§22) — neither requires resolution before Implementation Authorization.

**This charter does NOT itself:** assign WP-15 in `WPR-001`/`WP-REG-001` (a separate, explicit Repository Owner register action — **since performed**, see the Registration status correction near the top of this document); authorize BA-01 for implementation (§20); or authorize any code, migration, test, or frontend work. It is a proposed, uncommitted governance artifact, prepared for Repository Owner review — WP-15 is now formally registered (PROPOSED/CHARTERED)~~, but this charter itself remains un-approved and implementation remains unauthorized~~. *(Historical drafting-time statement, preserved per this repository's own no-silent-fix discipline. Superseded by the "BA-01 — Implementation Authorization" section immediately below: implementation is now authorized, per direct Repository Owner instruction, 2026-08-24. This charter document itself still does not perform code changes of any kind — it records the authorization, it does not constitute the implementation.)*

---

## BA-01 — Implementation Authorization

**Recorded 2026-08-24, per direct Repository Owner instruction ("Repository Owner Instruction — IMPLEMENTATION AUTHORIZATION, WP-15 / C-066 Evidence Management / BA-01 Understand Evidence Context").** This entry is the formal Implementation Authorization gate for BA-01, mirroring the two-step chartering-then-authorization precedent `WP-10`/`WP-11`/`WP-12`/`WP-14` (BA-04, BA-04 Increment, BA-05) each already established. **It authorizes implementation to begin; it does not itself constitute implementation, certification, V&V, or Release Readiness — each remains a distinct, future, independently-gated action per `CLAUDE.md §19.7`/`§19.7b`.** No source code, migration, API, or test is created by this entry.

**Chartering basis (already satisfied, not repeated here):** this charter itself (§1–§22 above), built on `IRA-C066` (accepted) and `TDS-015` (independently reviewed, remediated, remediation independently verified).

**Implementation Authorization basis:**
1. `TDS-015_C066_BA-01_Understand_Evidence_Context_Technical_Design.md` — complete Technical Design Specification (§1–§24), the frozen implementation contract.
2. `RO-DEC-C066-BA01-02` (BA-01 scope, backend-only, Option A) — APPROVED, recorded in `TDS-015 §24` and this charter's own §21/§22.
3. `RO-DEC-C066-BA01-03` (Evidence read authorization, Option C) — APPROVED, recorded in `TDS-015 §24` and this charter's own §4/§10/§22.
4. `RO-DEC-C066-BA01-05` (`PLATFORM_ADMIN` list-endpoint scope, no cross-Organization listing) — APPROVED, recorded in `TDS-015 §24` and this charter's own §10a/§22.
5. `RO-DEC-C066-BA01-01`/`-04` — confirmed non-blocking dispositions, unchanged (§8, §19, §22).
6. This charter itself — independently reviewed (verdict: PASS WITH CONDITIONS, findings M-1/M-2/M-3), remediated, and that remediation independently re-verified across two further rounds (F-1/F-2/F-3 findings, remediated, final verdict: **VERIFIED**, no BLOCKER/HIGH/MEDIUM finding remaining).
7. WP-15 formally registered in `WPR-001`/`WP-REG-001` as PROPOSED/CHARTERED (§ Registration status correction, near the top of this document).

**Decision: BA-01 Implementation is AUTHORIZED**, strictly bounded to `TDS-015`'s own frozen design (§1–§24) and this charter's own §1–§22 — the implementing agent MUST NOT invent or introduce: any endpoint beyond `GET /evidence/{evidence_id}` and `GET /evidence` (§6/§9); any write, mutation, delete, or purge path against `evidence_registry`; any `X-Tenant-ID` or other tenant-header API contract element (`RO-DEC-C066-BA01-03`); any cross-Organization access for ordinary (non-`PLATFORM_ADMIN`) callers; any `PLATFORM_ADMIN` cross-Organization listing via `GET /evidence` or any target-Organization selector parameter (`RO-DEC-C066-BA01-05`); any frontend, navigation, or Enterprise Experience work (`RO-DEC-C066-BA01-02`); `SE-031`, `evidence_fusion_registry`, or any AI Evidence Fusion capability; any new database table, column, or migration; any new Business Activity (no BA-02); or any change to WP-11's or WP-14's own already-certified `evidence_registry` write paths (`create()`, `create_linked()`). Where `TDS-015` does not provide enough information for a genuine implementation question, the implementing agent SHALL STOP and report the gap rather than invent a resolution, per `CLAUDE.md §17`/`§19.4`.

**Implementation-time decisions, explicitly delegated to the implementing agent's own judgment by `TDS-015` itself, not to be escalated into architecture decisions or treated as blockers:** exact routing prefix/path naming beyond `/evidence` as the proposed default (`TDS-015 §9`, `IRA-C066 §6` Category C); exact repository/service method naming; exact response-schema field ordering, provided every `EvidenceRegistryModel` column §4/§8 names is represented. None of these requires a further Repository Owner decision before or during implementation.

**Explicit exclusions, unchanged and unaffected by this authorization:** everything §19 (Out-of-Scope Boundaries) above already lists — evidence creation/update/deletion/purge, retention-floor enforcement, cross-object lineage, `SE-031`/evidence fusion, cross-Organization listing, any new tenant-header contract element, frontend/Enterprise Experience, any new migration, and any unrelated Knowledge Management (C-091) / Enterprise Discovery (C-090) / Knowledge Graph (C-092) work.

**Governance state, as of this authorization:** BA-01 moves from `CHARTERED / VERIFIED` to **`IMPLEMENTATION AUTHORIZED`**. It is explicitly **not** `IMPLEMENTATION COMPLETE`, **not** `CERTIFIED`, and **not** `CLOSED` — each remains a distinct, future gate, per `CLAUDE.md §19.7`/`§19.7b`'s own five-gate closure sequence. The implementing session, once implementation is complete, SHALL NOT self-certify — a fresh, independent Gate 1 reviewer is required, per the same discipline already exercised at every prior gate this capability's own governance sequence has passed through.

**Governance-synchronization note (per the established `WP-14`-family precedent, not a new decision):** `WPR-001`/`WP-REG-001`'s own WP-15 rows currently state "PROPOSED/CHARTERED — implementation NOT authorized," now stale as of this entry. Mirroring the identical precedent `WP-14 BA-04`'s own charter already established (neither BA-04's own nor the BA-04 Increment's own Implementation Authorization triggered an immediate `WPR-001`/`WP-REG-001` update — only their subsequent Closure/Certification did), `WPR-001`/`WP-REG-001` are **not** synchronized by this entry. They will be synchronized at BA-01's own Closure, not before — consistent with this task's own explicit instruction not to modify those registers.

---

*End of charter. No implementation, migration, model, router, service, schema, or test file has been created or modified by this document.* ~~*No WP number has been recorded in `WPR-001` or `WP-REG-001`.*~~ *(Historical drafting-time statement, preserved per this repository's own no-silent-fix discipline — accurate at the moment this footer was first written, before formal registration. Superseded — see the Registration status correction near the top of this document: WP-15 has since been formally registered in `WPR-001` and `WP-REG-001` as PROPOSED/CHARTERED, not by this charter itself but by a separate Repository Owner register action.)* **Implementation Authorization was subsequently GRANTED, 2026-08-24 — see the "BA-01 — Implementation Authorization" section above.** This charter document itself still creates no code, migration, test, or frontend artifact — authorization is recorded here; implementation is performed as a separate, subsequent action. `TDS-015`, `IRA-C066`, `CAP-001`, `SD-002`, `SER-001` were read, not modified, in the preparation of this charter, or in this document's own subsequent remediation and authorization-recording passes.
