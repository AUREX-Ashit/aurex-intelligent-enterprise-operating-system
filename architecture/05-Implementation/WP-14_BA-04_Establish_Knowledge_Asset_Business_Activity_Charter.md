# WP-14 — BA-04 (C-091 Knowledge Management) — Establish Knowledge Asset — Business Activity Charter

**Work Package:** WP-14
**Business Activity:** BA-04 — Establish Knowledge Asset
**Capability:** C-091 Knowledge Management
**Status:** **BA-04 AUTHORIZED FOR IMPLEMENTATION** (this update, 2026-08-10) — Classification B, implementation-ready, independent of the unresolved WP-14 hosting-service decision (§8/§20/Final Determinations below). **BA-05 remains separately gated and is NOT authorized by this document.** This authorization exercises `IRA-014 §17`'s own narrower provision ("BA-01 through BA-04... permitted to proceed... once authorized") specifically for BA-04 — it does not itself constitute `IRA-014`'s own document-wide "Accepted" governance status, whose first sentence separately ties full Acceptance to resolving hosting service "for all five" BAs (a genuine textual tension within `IRA-014` itself, disclosed in Final Determinations, not silently resolved).
**Prepared under:** direct Repository Owner instruction ("Charter BA-04"), 2026-08-10. **Authorized under:** direct Repository Owner instruction ("Proceed with the formal implementation authorization for... BA-04"), 2026-08-10, following a focused dependency verification (separate, prior Repository Owner instruction) establishing BA-04's independence from the hosting-service decision.

**A note on document type, disclosed rather than assumed:** this repository's own established convention charters at the **Work Package** level (`WP-XX_<Name>.md`, e.g. `WP-10_Configuration_Management.md`) and specifies each Business Activity's own charter-level detail *within* the governing IRA (`IRA-005 §12`/`IRA-007`/`IRA-008 §5`/`IRA-009 §5`/`IRA-010 §3` precedent: "Business Activities are determined during Gap Analysis, not chartered in advance"). `IRA-014` already performs exactly that function for BA-04 (`IRA-014 §6` BA-04 row, plus §7/§8/§10/§11 cross-cutting sections). **No standalone per-Business-Activity charter document type exists anywhere else in this repository** — this document is therefore a new document shape, produced because it was directly, explicitly instructed, not because repository precedent already established this pattern. It does not restate IRA-014 as a new decision; it organizes IRA-014's own already-governing content into the structure requested, and separately, explicitly surfaces what that re-verification found that IRA-014 itself did not state accurately (§16 below).

**Governing basis for BA-04, stated explicitly per the instruction's own warning:** `CAP-001` (C-091 registration) → `EIA-001` Vol. I §7 / Vol. II §13, §17.5 → `Master_Technical_Architecture.md` AMD-012 (`knowledge_asset_registry`) → `IRA-014 §6` BA-04. **`ADR-023`, `AMD-016`, `RTA-001 §12.9`'s amendment, and `TDS-013` govern BA-05's own tenant-boundary mechanism specifically — none governs BA-04.** Independently re-verified in this pass (§11 below): `knowledge_asset_registry.organization_id` is a standard, mandatory, non-nullable physical FK with a standard RLS policy — structurally nothing like `enterprise_knowledge_graph_registry`'s former nullable/polymorphic gap that required `ADR-023`/`TDS-013` in the first place. BA-04 is not designed backwards from BA-05 anywhere in this document.

---

## Classification Key

- **A** — already determined by governing documents (`CAP-001`, `EIA-001`, `Master_Technical_Architecture.md`, `IRA-014`)
- **B** — determined by repository precedent (already-certified patterns this charter reuses, not invents)
- **C** — an implementation detail (safe to resolve during implementation without a dedicated architecture document)
- **D** — requires a Repository Owner decision (genuinely open, not resolved by any existing document)

---

## 1. Business Activity Identity — [A]

BA-04, WP-14, Capability C-091 Knowledge Management (`CAP-001` D-005, Active). Governed physical Business Object: `knowledge_asset_registry` (AMD-012, LOCKED, `Master_Technical_Architecture.md` line 3226). Chartered in-scope, structurally independent of the Convergence Lifecycle (BA-02/BA-03), per `IRA-014 §5.4`/§6 BA-04.

## 2. Business Intent — [A]

Verbatim, `IRA-014 §6` BA-04: *"Curate a Signal into a governed Knowledge Asset, carrying Provenance from first existence, per EIA-001's own invariant."* Realizes `EIA-001 Vol. I §7`'s own definition: *"a curated, governed unit of knowledge produced from one or more Signals."* Governed by two named EIA-001 invariants, both independently re-verified against the physical schema in this pass: **Provenance** (`EIA-001 Vol. I §7.3`: "no Knowledge Asset without Provenance," physically realized as `provenance_reference`) and **Freshness** (`EIA-001 Vol. II §17.5`: "Freshness Decays Unless Renewed," physically realized as `freshness_last_confirmed_at`).

## 3. Trigger — [A] / [B]

**Caller-invoked, not event-triggered.** No governing document states BA-04 itself is triggered by an upstream Domain Event — it is a direct `POST /knowledge-assets` establish action, the same shape `IRA-014 §6` BA-01/BA-02 and the certified `WP-10 BA-02`/`WP-11 BA-03` precedents already use [B]. BA-04 is, separately, the **trigger source for BA-05** (its own `ACCEPTED` transition is `enterprise_knowledge_graph_registry`'s own synchronization trigger, `IRA-014 §6` BA-05 Dependencies row) — this is recorded here as an existing downstream fact (§12 below), not used to shape BA-04's own trigger, per the governing instruction's own explicit prohibition on designing BA-04 backwards from BA-05.

## 4. Actor / Persona — [A] / [B]

No `PE-001-C091` capability specification exists (confirmed, `IRA-014` Governing Specification line and §6 BA-04 row: "No `PE-001-C091` names one"). Interim: `PLATFORM_ADMIN` only. **Not a fresh interim assumption** — `IRA-014 §10` names two already-certified precedents governing the identical resource shape (Organization-scoped only, no Domain anchor, a write/establish action): `routers/configuration.py::establish_configuration` (`WP-10`, CLOSED — CERTIFIED) and `AIService/routers/search.py::register_content` (`WP-11`, CLOSED — CERTIFIED), each independently reaching the same `PLATFORM_ADMIN`-only conclusion. Directly re-verified in this pass: `establish_configuration` (`Backend/Services/AuthService/routers/configuration.py:92-95`) is gated by `Depends(require_platform_admin)` exactly as described.

## 5. Preconditions — [A] / [D — see §16]

- The caller's own Organization (`organization_master` row) must exist — standard, platform-wide precondition, no BA-04-specific mechanism.
- **No precondition on BA-01, BA-02, or BA-03** — independently, explicitly stated twice by `IRA-014` (§5.4: "structurally independent of BA-02/BA-03's own CDE-resolution path"; §6 BA-04 Dependencies row: "Structurally independent of BA-02/BA-03"). No FK from `knowledge_asset_registry` to `discovery_provider_registry` (BA-01's own table) exists either — independently confirmed against the physical schema in this pass.
- **`data_ingestion_registry` existing as a real, populated table is NOT a genuine precondition** — see §16, a correction to `IRA-014`'s own framing.

## 6. Input Contract — [A]

Per `knowledge_asset_registry`'s own physical schema (AMD-012, directly re-read in this pass, `Master_Technical_Architecture.md:3226-3239`), caller-supplied fields at establishment:

| Field | Type | Mandatory (schema) | Mandatory (business rule) |
|---|---|---|---|
| `knowledge_asset_name` | VARCHAR(255) | No (no `NOT NULL`) | Not stated by any governing document — **[D]**, see §16 |
| `knowledge_asset_type` | VARCHAR(255) | No | Not stated — **[D]**, see §16 |
| `provenance_reference` | VARCHAR(255) | No (schema-level) | **Yes** — `EIA-001 Vol. I §7.3`, enforced at the application layer, mirroring this repository's own existing precedent for schema-vs-application-layer conditional rules (`TD-097`) |
| `source_ingestion_id` | UUID, FK | No | Not business-rule-mandatory (distinct from `provenance_reference`, see §16) |
| `confidence_rule_id` | UUID, FK | No | Not stated |

`organization_id` is derived from the caller's own tenant context (`get_current_tenant`/JWT claim), never caller-supplied, mirroring `establish_configuration`'s own precedent. `curation_status`, `freshness_last_confirmed_at`, `graph_engine_reference`, `active_flag`, `created_at` are system-managed, not caller input.

## 7. Business Rules — [A] / [C]

- `curation_status` begins `PROPOSED` (DB `DEFAULT`, `CHECK` constraint enumerates exactly `PROPOSED`/`VALIDATED`/`ACCEPTED`/`REJECTED`/`SUPERSEDED`, `EIA-001 Vol. II §13`) — [A].
- `provenance_reference` mandatory at establishment, application-layer enforced, not DB-enforced — [A, rule] / [C, enforcement mechanism, precedented].
- `freshness_last_confirmed_at` — *"Freshness Decays Unless Renewed"* (`EIA-001 Vol. II §17.5`). **The read-path/staleness decay mechanics are explicitly left open by `IRA-014` itself** ("determined at Technical Design," §6 BA-04 row) — [C]: this is a routine implementation-time decision (a staleness threshold/read-path check), not a comparable gate to BA-05's own former architectural gap; no dedicated Technical Design Specification is needed for it (§20).

## 8. Persistence Target — [A] / [B — corrected this update]

`knowledge_asset_registry` (AMD-012, LOCKED, zero rows anywhere, independently re-confirmed in this pass — no model, migration, or row exists in any service). **Corrected this update, per a focused dependency verification performed under separate Repository Owner instruction:** this section previously framed hosting service as a shared, blocking `[D]` item across BA-01/02/03/04/05. That framing was imprecise and is corrected here — **[B]**, resolved by repository precedent, not open. `IRA-014 §11` item 2 names hosting service as an open item at the *IRA-drafting* stage, but `IRA-014 §17`'s own authorization language never re-elevates it to a blocking condition for BA-01–BA-04 specifically — only BA-05 is explicitly gated on its own further Technical Design work. The technical reason hosting placement is architecturally consequential is BA-05-specific (`TDS-013 §9`'s own `EntityOwnershipResolver`, which must read *other tables'* `organization_id` columns to derive `enterprise_knowledge_graph_registry`'s own boundary — a genuine same-database-vs-cross-service design question). BA-04 has no analogous cross-table read — it writes to exactly one table. `AIService` is directly evidenced as the correctly-supported existing physical service for `knowledge_asset_registry`: it already hosts sibling AMD-012 tables (`vector_index_registry`, `document_chunk_registry`) using the identical "logical, not physical FK" `organization_id` pattern this table would need, and already hosts `evidence_registry`, directly cited by this Business Activity's own Evidence/provenance requirement. `Master_Technical_Architecture.md`'s own PART F ADDENDUM ("Knowledge Graph Service," lines 4967-4970) names a logical component grouping shared with `enterprise_knowledge_graph_registry` — a component-design note, not a physical-service gate; no physical service by that name exists, and none is created by this authorization. **The broader, formal WP-14-wide hosting-service determination remains a separate, open BA-05/architectural matter (Final Determinations below) — it is not resolved by this authorization and is not a BA-04 prerequisite.**

## 9. State / Lifecycle Transition — [A] / [D]

`curation_status`: `PROPOSED` → `VALIDATED`/`ACCEPTED`/`REJECTED`/`SUPERSEDED` (`EIA-001 Vol. II §13`, DB `CHECK`-enumerated). **Two distinct open items, deliberately not conflated:**
- **Transition endpoint shape** (a single generic transition endpoint vs. named action endpoints) — `IRA-014 §6` BA-04 row states this explicitly: "exact transition shape... determined at Technical Design," naming `OrganizationService.activate()`/`suspend()` as the precedent. Directly re-verified: `activate()`/`suspend()` exist (`Backend/Services/AuthService/services/organization_service.py:486,583`). **[C]** — a routine, already-precedented implementation choice, not requiring its own Technical Design Specification document.
- **The transition graph itself** (which of the five states may transition to which others — e.g., whether `REJECTED` may later become `VALIDATED`, whether `SUPERSEDED` is terminal) — **no governing document specifies this anywhere**, independently checked in this pass against `EIA-001 Vol. II §13`'s own five-state naming (states named, transition rules not). **[D]** — inventing this graph would be inventing a business rule no governing document states, which this charter does not do.

## 10. Authorization — [A] / [B]

Interim `PLATFORM_ADMIN`-only, per §4 above. **WP-13's Authorization Runtime Engine (`enforce_domain_permission`) does not apply** — `knowledge_asset_registry` carries no `domain_id` column (independently re-verified against the physical schema in this pass, confirming `IRA-014 §10`'s own finding). No new authorization mechanism, persona, or claim is introduced by this charter.

## 11. Tenant Boundary — [A]

`organization_id UUID NOT NULL REFERENCES organization_master(organization_id)` (`Master_Technical_Architecture.md:3238`) — a standard, mandatory, non-nullable physical FK. RLS policy independently re-verified (`Master_Technical_Architecture.md:4561-4563`): `CREATE POLICY org_isolation ON knowledge_asset_registry USING (organization_id = current_setting('app.organization_id')::uuid)` — the same unqualified (non-nullable) form used by every standard tenant-scoped table in this repository, structurally distinct from `enterprise_knowledge_graph_registry`'s own nullable-aware policy. **This is the direct evidentiary basis for §20's conclusion that BA-04 does not need its own Technical Design Specification** — there is no tenant-boundary ambiguity of the kind `ADR-023`/`TDS-013` existed to resolve for BA-05.

## 12. Events / Outcomes — [A] / [D — not invented]

`RTA-001 §12.14`: *"Knowledge updates are triggered by Domain Events rather than direct Business Activity invocation."* `IRA-014 §6` BA-05's own Dependencies row states BA-05 "Fires from BA-04 (Knowledge Asset acceptance)" — confirming BA-04's `ACCEPTED` transition is expected to be the trigger point for BA-05's own future consumption. **No concrete event name, event version, or event schema exists anywhere in this repository for this outcome** — independently re-confirmed in this pass (no `BaseEvent` subclass, no registered event-type string, matching the identical finding already made during the BA-05 gating review's own Item 2). Per this charter's own explicit governing instruction, **this event is not invented here.** What BA-04 must eventually publish (a Domain Event naming the `ACCEPTED` transition, using the real `Backend/Shared/Events` framework — `TD-105` Closed, confirmed importable and available, the same platform-wide fact already established during the BA-05 gating review and equally applicable here since it is not BA-05-specific) is recorded as **[D]** — a Repository Owner or BA-04's-own-implementation-time decision, exactly mirroring the unresolved state already reported for BA-05's own trigger-mapping side of this identical gap.

## 13. Error / Rejection Conditions — [A] / [C]

- Missing `provenance_reference` → 422 (`IRA-014 §6` BA-04 acceptance criteria: "a Knowledge Asset with no Provenance is rejected (422)") — [A].
- Caller lacks `PLATFORM_ADMIN` → 403, standard dependency rejection, precedented (`establish_configuration`) — [B].
- Invalid `curation_status` value on an eventual transition call → application-layer validation before the DB `CHECK` constraint is reached, mirroring existing precedent of validating enum-shaped inputs at the schema/router layer rather than relying on a raw DB constraint violation to surface as a 500 — [C].

## 14. Idempotency Expectations — [D]

**No governing document specifies a duplicate-establishment or idempotency mechanism for Knowledge Asset creation** — unlike BA-05's own natural-key design (`TDS-013 §17`), no analogous discussion exists anywhere for BA-04. Two candidate precedents exist in this repository (check-before-insert, `TDS-013`'s own recommendation for BA-05; version-superseding-on-repeat-establish, `WP-10`'s own `establish_configuration` pattern) but neither is stated as governing BA-04 specifically. **Not decided here** — flagged honestly as unspecified rather than assumed.

## 15. Audit / Observability Expectations — [A] / [B]

`created_at` (standard audit column, present on the physical schema). **Corrected this update:** `confidence_rule_id`'s own target, `confidence_scoring_registry` (AMD-003), was previously described here as "real, existing." Directly re-verified: it is architecturally real and LOCKED (AMD-003) but, like `data_ingestion_registry` (§16), **has no physical Backend model anywhere in this repository** — confirmed by direct search. This does not change `confidence_rule_id`'s own disposition (nullable, not required at establishment, §16) — it is disclosed here for accuracy, not treated as a new blocker. If/when BA-04 publishes the Domain Event named in §12, it should use the real `Backend/Shared/Events`/`Backend/Shared/Logging` framework directly (`TD-105` Closed) rather than `AuthService/observability.py`'s local, explicitly-temporary substitute — the identical correction already made to `TDS-013` for BA-05 applies here on the same evidentiary basis, since the fix is platform-wide, not BA-05-specific.

## 16. Dependencies — [A] / [B] / [D — one correction to IRA-014]

Distinguished precisely, per the governing instruction's own explicit requirement:

- **Hard technical dependency:** `organization_id → organization_master` (real, existing, `NOT NULL`) — every establish call requires a valid caller tenant. This is the only genuine hard dependency.
- **Sequencing dependency on BA-01/BA-02/BA-03: NONE.** Independently, directly re-verified against the physical schema in this pass (no FK from `knowledge_asset_registry` to `discovery_provider_registry` or `unclassified_intelligence_registry` or `customer_metric_registry` exists) — confirms `IRA-014 §5.4`/§6's own "structurally independent" finding exactly. BA-04 may be implemented in any order relative to BA-01/02/03.
- **Optional/soft dependency:** `confidence_rule_id → confidence_scoring_registry` — **corrected this update:** `confidence_scoring_registry` is architecturally real and LOCKED (AMD-003) but, directly re-verified, **has no physical Backend model anywhere in this repository** (same disposition as `data_ingestion_registry`, immediately below). `confidence_rule_id` remains nullable and is not required at establishment — this does not block BA-04, mirroring `source_ingestion_id`'s own identical treatment.
- **Correction to `IRA-014`'s own framing (new finding, this pass):** `IRA-014 §6` BA-04's own Dependencies row states `source_ingestion_id → data_ingestion_registry` is *"pre-existing, real, `WP-11`"*. **This is not accurate.** `data_ingestion_registry` is real and LOCKED **at the architecture-document level only** (`Master_Technical_Architecture.md:3626`, its own `CREATE TABLE` and RLS policy exist) — but directly re-verified in this pass, **no physical Backend model exists for it anywhere in the repository.** `IngestionService/models/{upload.py,document.py}` implement a differently-named, non-canonical pair of tables (`aurex_upload_trackers`, `aurex_documents`) using a non-standard tenant representation (`tenant_id: String(100)`, not this repository's own standard `organization_id: UUID FK organization_master` pattern) — these are not `data_ingestion_registry` under another name; they are a separate, non-conformant implementation `WP-11` actually built for document upload, not the canonical AMD table `knowledge_asset_registry.source_ingestion_id` references. **This does not block BA-04** — `source_ingestion_id` is nullable in the physical schema and is not itself the business-rule-mandatory Provenance field (`provenance_reference` is, and carries no FK dependency at all) — BA-04 can establish a Knowledge Asset with `source_ingestion_id` left `NULL`, mirroring the already-precedented pattern of `graph_engine_reference` remaining `NULL` until live Neo4j infrastructure exists. This is reported here, not silently corrected in `IRA-014` itself (governance rules for this pass prohibit modifying `IRA-014`).
- **Downstream (not a BA-04 dependency; BA-04 is a dependency *for* this):** BA-05 depends on BA-04 reaching `ACCEPTED` (§12).

## 17. Acceptance Criteria — [A]

Verbatim, `IRA-014 §6` BA-04: *"A Knowledge Asset establishes in `PROPOSED` state with mandatory Provenance; a Knowledge Asset with no Provenance is rejected (422)."*

## 18. Test Obligations — [A]

Per `IRA-014 §6` BA-04 Testing requirements row: Unit (Provenance mandatory; `curation_status` transitions correctly bounded) + API (200/201, 401/403, 422) + the Mandatory Tenant-Isolation Test Checklist (`CLAUDE.md §21.4`): (a) two distinct, unrelated Organizations seeded, no shared row; (b) a caller in one Organization cannot retrieve or infer another Organization's own Knowledge Asset; (c) an explicit probe of whether a caller-supplied (not claims-derived) foreign identifier is accepted by any id-scoped endpoint.

## 19. Out-of-Scope Boundaries — [A]

- The live Neo4j write and `graph_engine_reference` population — `IRA-014 §5.5`, BA-05's own scope, not BA-04's.
- Signal's own physical schema — `Master_Technical_Architecture.md`'s own schema comment (`:3224`) discloses this as an unresolved **ASSUMPTION**, not silently resolved by this charter: *"no repository document specifies Signal's own physical schema... A human reviewer should confirm this treatment is acceptable."* Carried forward here as **[D]**, not decided.
- The bridge between a resolved Convergence candidate (BA-03) and a Knowledge Asset (BA-04) — explicitly disclosed as not existing anywhere in governing text (`IRA-014 §5.4`, `TD-candidate-M`). Not built by BA-04.
- BA-05's own event-triggered synchronization mechanism and its own Technical Design (`TDS-013`) — a separate Business Activity's own scope.

## 20. Implementation Readiness Classification

**Classification B — architecturally unblocked**, the same classification `IRA-014 §11` already assigns BA-04 (shared with BA-01/BA-02/BA-03/BA-05). Unchanged by this charter.

**BA-04 does NOT require its own dedicated Technical Design Specification document, distinct from BA-05.** The reasoning is direct and evidentiary, not assumed: BA-05 required `ADR-023` and `TDS-013` specifically because `enterprise_knowledge_graph_registry` carried no tenant-boundary column at all, with polymorphic, untyped endpoint references — a genuine `CLAUDE.md §19.8.5`-class architectural gap. Independently re-verified in this pass (§11 above), `knowledge_asset_registry.organization_id` is a standard, mandatory, non-nullable FK with the same standard RLS policy every other tenant-scoped table in this repository already uses. No comparable gap exists for BA-04. Its remaining open items are routine implementation-time details with existing repository precedent (transition endpoint shape, §9) — none has ever independently triggered a dedicated TDS document for any other Business Activity in this Work Package.

**AUTHORIZED (this update):** Per a focused dependency verification (separate, prior Repository Owner instruction), hosting service is not a BA-04 prerequisite (§8, corrected). BA-04 is therefore authorized for implementation now, using `AIService` as the evidenced hosting service, without waiting for the broader WP-14 hosting-service question (BA-05's own architectural matter) to be formally closed.

## 21. Enterprise Experience Scope Decision — `CLAUDE.md §20.3`/`§20.7` [D → resolved, this remediation]

**Repository Owner decision, recorded explicitly this remediation, per `CLAUDE.md §20.3`'s own required mechanism** — that section's own text: *"Unless a Work Package's own charter explicitly designates it infrastructure-only... or a specific Business Activity within it explicitly backend-only, every Work Package SHALL deliver, for each Business Activity it charters: [backend + Frontend/Navigation/Enterprise Experience + the end-to-end journey]... A Work Package that implements only the backend half of this list, without disclosing and justifying the frontend/Enterprise Experience half as out of scope through the Gap Analysis (§19.3) and an explicit repository-owner charter decision, is incomplete."* The Independent Certification of this Business Activity (Gate 1) found no such decision had been recorded anywhere in this charter — corrected here, not by building a frontend.

**BA-04 is intentionally delivered as BACKEND-ONLY for this implementation increment.** This is a specific Business Activity within WP-14 explicitly designated backend-only, per `CLAUDE.md §20.3`'s own stated exception clause ("...or a specific Business Activity within it explicitly backend-only") — WP-14 as a whole, and BA-01/BA-02/BA-03/BA-05 individually, are each unaffected and retain their own independent Enterprise Experience obligation under `IRA-014 §6`/`CLAUDE.md §20.3` unless and until each records its own equivalent decision.

Stated explicitly, per this decision's own governing requirement:

1. **This BA-04 implementation authorization covers the backend establishment/retrieval behavior only** — `POST /knowledge-assets` and `GET /knowledge-assets/{id}` (§8 above), against `knowledge_asset_registry`, gated by the existing interim `PLATFORM_ADMIN` pattern (§10).
2. **No frontend/Enterprise Experience implementation is included in this BA-04 increment.** `IRA-014 §6` BA-04's own row names "Establish + status view" under Frontend/UX required — that work is not performed by this implementation and is not silently folded into it.
3. **This is an explicit Repository Owner scope decision, not an accidental omission.** It is recorded here specifically because Independent Certification found no such decision had been recorded, per `CLAUDE.md §20.3`'s own text that an undisclosed backend-only delivery "is incomplete."
4. **Any future Enterprise Experience/UI work for BA-04 must be separately authorized** — a future, separately-scoped increment, not assumed, invented, or silently built under this same authorization.

**Consequence for `CLAUDE.md §20.7`:** per that section's own text, *"Where a Work Package is explicitly chartered infrastructure-only or backend-only (§20.3), this extension does not apply to it — the charter's own disclosed scope decision governs, per §19.4."* This decision is that governing disclosure for BA-04 specifically.

**No new Business Activity, screen, UX requirement, capability, or architecture is introduced by this decision** — it narrows what this specific implementation increment delivers; it adds nothing.

---

## Final Determinations

**BA-04 Charter status:** **AUTHORIZED FOR IMPLEMENTATION** (this update, 2026-08-10, under direct Repository Owner instruction, following a focused dependency verification performed under a separate, prior Repository Owner instruction). Supersedes this document's own prior DRAFTED status. Governing basis (`IRA-014 §6` BA-04, plus cross-cutting §7/§8/§10/§11) is unchanged and not superseded by this update — this update records an authorization decision on top of that already-established basis, plus two accuracy corrections found during the dependency verification (§8 hosting-service framing; §15/§16 `confidence_scoring_registry`).

**Implementation readiness classification:** Classification B — architecturally unblocked. Unchanged from `IRA-014`.

**Blockers:** None. No security, tenant-isolation, or data-integrity defect exists in BA-04's own design as chartered.

**Authorization scope, stated explicitly per the governing instruction's own requirement:**
1. **BA-04 is Classification B / implementation-ready.** Confirmed above (§1–§19), unchanged by this update.
2. **BA-04 is authorized independently of the unresolved hosting-service decision.** `IRA-014 §17` permits BA-01 through BA-04 "to proceed... once authorized" without conditioning that on hosting-service resolution; only BA-05 is explicitly gated on further Technical Design work (`§15`/`§17`, `ADR-023 §6`). BA-04's own design has no cross-table ownership-resolution mechanism of the kind that makes hosting placement architecturally consequential for BA-05 (`TDS-013 §9`) — see §8, corrected this update.
3. **The hosting-service decision remains an open WP-14/BA-05 architectural matter and is NOT a prerequisite for BA-04.** `AIService` is the evidenced, already-supported existing physical service for `knowledge_asset_registry` (§8) — BA-04's own implementation may proceed against it without waiting for the Repository Owner's own broader, formal hosting-service determination for the WP-14 table set as a whole.
4. **BA-05 remains separately gated and is NOT authorized by this instruction.** `ADR-023 §6`, `TDS-013 §26`, and `IRA-014 §17` each independently state BA-05 requires its own completed Technical Design and a separate implementation authorization — unaffected, unchanged, not granted here.
5. **BA-04 must use existing repository architecture and implementation patterns** — `establish_configuration` (`WP-10`)/`register_content` (`WP-11`) for the establish endpoint shape, `OrganizationService.activate()`/`suspend()` for the eventual transition endpoint shape, the standard `organization_id`/RLS tenant-isolation pattern (§11), and the interim `PLATFORM_ADMIN` authorization pattern (§10) — all already-certified precedents, none newly invented by this authorization.
6. **No new architecture, capability, persona, authorization mechanism, or Business Object is invented by this authorization** — `knowledge_asset_registry` is an already-LOCKED, already-registered canonical table (AMD-012); no new table, column, service, endpoint pattern, or persona is introduced.

**Implementation authorization conditions, confirmed directly against the repository (re-verified this update, not merely restated):**
- `knowledge_asset_registry.organization_id` is `NOT NULL REFERENCES organization_master` — a mandatory tenant boundary. Confirmed (§11).
- The existing `org_isolation` RLS pattern (`Master_Technical_Architecture.md:4561-4563`) is directly reusable, unqualified/non-nullable form — no new isolation mechanism required. Confirmed (§11).
- The existing interim `PLATFORM_ADMIN` authorization pattern (`require_platform_admin`) is directly reusable; no new authorization architecture is required. Confirmed (§10).
- `source_ingestion_id` remains nullable and is correctly treated as **not** a dependency on a currently-nonexistent physical `data_ingestion_registry` model. Confirmed (§16).
- `confidence_rule_id` remains nullable and is correctly treated as **not** a dependency on a currently-nonexistent physical `confidence_scoring_registry` model — **newly corrected this update** (§15/§16); the prior charter text inaccurately described `confidence_scoring_registry` as "real, existing," which direct re-verification found false (architecturally real/LOCKED only, no physical Backend model anywhere).
- `provenance_reference` and other mandatory business rules follow the governing schema/business rules exactly as stated (§6/§7). No contradiction found.
- BA-04 has no implementation dependency on BA-01, BA-02, or BA-03 — confirmed directly against the physical schema (no FK exists to `discovery_provider_registry`, `unclassified_intelligence_registry`, or `customer_metric_registry`), consistent with `IRA-014`'s own "structurally independent" finding (§16). No contradiction found.

None of the above findings contradicted the repository — no STOP condition was triggered.

**Open Repository Owner decisions, corrected this update:**
1. **Hosting service is no longer listed as a BA-04-blocking item** — reclassified above (§8) as a WP-14/BA-05 architectural matter, not a BA-04 prerequisite. The formal, WP-14-wide hosting determination (`AuthService`/`AIService`/other, across all five tables) remains open and is not resolved or required by this authorization.
2. `curation_status`'s own transition graph (which of the five states may transition to which others) — not specified anywhere; an implementation-time detail (§9), not a gate.
3. Idempotency / duplicate-establishment policy — not specified anywhere; an implementation-time detail (§14), not a gate. **Registered as `TD-141` (`TECH-DEBT.md`) during Certification Remediation** — see the Remediation Record below.
4. BA-04's own outcome-event name, version, and schema (for BA-05's eventual consumption) — explicitly not invented by this charter or this authorization (§12); does not block BA-04's own establish/status-transition implementation, only the eventual event-publication step.
5. **A genuine textual tension in `IRA-014 §17` itself, disclosed, not silently resolved:** its own first sentence ties `IRA-014`'s document-wide "Accepted" governance status to resolving "the open items this IRA surfaces for BA-01–05... hosting service — all five" — a broader condition than what this authorization relies on. This authorization instead exercises `IRA-014 §17`'s own separate, narrower sentence permitting "BA-01 through BA-04... to proceed... once authorized." This authorization does not purport to grant `IRA-014`'s own full document-wide Acceptance — only BA-04's own implementation-readiness, within the scope `IRA-014 §17` itself already carves out for BA-01–BA-04 distinctly from BA-05.
6. The `data_ingestion_registry` correction and the new `confidence_scoring_registry` correction (§15/§16) should both be reflected in `IRA-014` at the Repository Owner's own direction — this document does not modify `IRA-014` itself.

**Whether a BA-04 Technical Design is required:** No — unchanged, see §20's reasoning.

**Recommended next step:** BA-04 may proceed directly to implementation under `IMP-001`'s standard methodology, reusing the already-certified `establish_configuration`/`register_content`/`OrganizationService.activate()`/`suspend()` patterns, hosted in `AIService`, without a dedicated Technical Design Specification document and without waiting for the broader WP-14 hosting-service determination or BA-05's own Technical Design/implementation authorization. **Whether this authorization should also be synchronized into `WP-REG-001`** (per that register's own §3 update triggers — "an IRA is accepted," "implementation begins") **is a distinct governance-recording question this document flags but does not resolve** — `WP-REG-001`'s own WP-14 row currently reads "Not yet decomposed into formal BAs," and this authorization is the first BA-level decomposition for that row; per this task's own explicit "explain the required change before making it" instruction, this is surfaced for Repository Owner direction, not performed in this update.

## Remediation Record — Independent Certification Gate 1 (2026-08-11)

Backend implementation was completed against this charter's own authorization (§21 above records the one omission that pass surfaced). An independent, fresh-context Gate 1 reviewer (`CLAUDE.md §19.7`/`§19.7b`) certified the result **CONDITIONAL — REMEDIATION REQUIRED**: no `A — Certification Blocker` (schema, migration, authorization reuse, and tenant isolation were all independently verified sound), but three `B — Remediation Required` findings. This charter update, plus a corresponding backend change and a `TECH-DEBT.md` registration, remediate all three:

1. **Missing Enterprise Experience scope decision** (`CLAUDE.md §20.3`/`§20.7`) — remediated by §21 above (this update).
2. **`record_audit` omission**, in tension with WP-12's own closer, same-service precedent (`TDS-012 §8`) — remediated in code: `services/knowledge_asset_service.py::establish()` now calls `record_audit(action="ESTABLISH_KNOWLEDGE_ASSET", ...)` immediately after successful persistence, mirroring `services/conversation_service.py::establish()`'s own identical shape exactly (same `observability.py` local-substitute mechanism, no new framework). Covered by a new test (`test_establish_knowledge_asset_writes_audit_record`).
3. **Idempotency gap never formally registered** (`CLAUDE.md §19.8.2`) — registered as `TD-141` in `TECH-DEBT.md`.

The `D — Observation` the same certification raised (`WP-REG-001`'s WP-14 row is stale) was explicitly **not** remediated here, per the Repository Owner's own instruction that it is a separate, Gate-5-class governance action, not one of the three Gate-1 remediation findings.

A fresh, independent Gate 1 re-certification is required before this Business Activity may be marked CERTIFIED — this remediation does not self-certify.

---

## Second Independent Certification & Enterprise Experience Remediation Record

A second, genuinely fresh-context, independent reviewer — uninvolved in the implementation, the original Gate 1 certification, or the Gate 1 remediation above — re-certified this Business Activity against this charter and its own governing specifications (`CLAUDE.md §19.7`/`§19.7b`). Result: **CONDITIONAL — REMEDIATION REQUIRED**, disposing of the prior remediation's own three findings as follows:

- **B2 — Audit Logging: CLOSED.** The Gate 1 remediation's `record_audit` addition (above) was independently re-verified sound.
- **B3 — Technical Debt: CLOSED.** `TD-141`'s registration in `TECH-DEBT.md` was independently re-verified sufficient.
- **B1 — Enterprise Experience Scope: REMAINED OPEN.** The second reviewer found that §21 above's backend-only scope decision could not stand as this Business Activity's final disposition.

**Why B1 remained open:** `IRA-014 §16`'s own Self-Review explicitly states — independent of, and not overridden by, this charter's own §21 decision — that BA-01 through BA-04 each specify Frontend/UX requirements (`IRA-014 §6`), and that BA-05 alone is the explicit, separately-justified backend-only exception (`RTA-001 §12.3`'s own asynchronous, system-triggered design). §21's backend-only scope decision, framed there as an interim, separately-authorizable increment, did not — and per `IRA-014 §16` could not — convert BA-04 into a second, undocumented backend-only exception alongside BA-05.

**Repository Owner remediation decision:** rather than attempting to override or reinterpret `IRA-014 §16`, the Repository Owner authorized implementation of the minimum Frontend/UX requirement `IRA-014 §6` already specifies for BA-04 — **"Establish + status view"** — closing B1 on that basis rather than by contesting the second certification's finding.

**What the minimum Enterprise Experience now provides**, implemented under `source/frontend/src/features/knowledge-asset/` (`EstablishKnowledgeAssetSection.tsx`, `KnowledgeAssetStatusSection.tsx`, `useKnowledgeAssetManagement.ts`, `services/knowledge-asset-api.ts`, `types/knowledge-asset.ts`), composed onto the existing `enterprise-intelligence` route slot alongside `WP-11`'s own `EnterpriseSearchScreen`:

- Establish a Knowledge Asset (`POST /knowledge-assets`), collecting only the fields the backend contract accepts.
- Display the resulting Knowledge Asset and its current status.
- Retrieve a Knowledge Asset by id (`GET /knowledge-assets/{knowledge_asset_id}`), scoped to the caller's own Organization.
- `provenance_reference` mandatory; `organization_id` never exposed as user-editable input.
- No lifecycle-transition controls, no list/search/edit/delete, no Knowledge Graph or BA-05 functionality — deliberately out of this minimum scope.

The frontend implementation reused existing AUREX frontend architecture and components exactly — the existing `Card`/`Button`/`Form*`/`Input`/`Spinner`/`LoadingState`/`StatusBadge` components, the existing `apiClient`/`useNotifications`/`appConfig` conventions, and `EnterpriseSearchScreen`'s own existing slot-composition/`useSearchManagement`'s own dual-state-slice precedents. No new component, token, theme, route, persona, or architecture was introduced.

**Validation evidence:**

- TypeScript (`tsc --noEmit`): clean.
- ESLint: 0 findings.
- BA-04 backend test suite: 13/13 passing.
- Full AIService regression suite: 68/68 passing.
- Live Establish → Status View journey, verified against a running AIService instance: `POST /knowledge-assets` → 201 with the full `KnowledgeAssetResponse`; `GET /knowledge-assets/{id}` → 200 with the same asset; missing `provenance_reference` → 422; unknown/cross-tenant identifier → 404.
- No frontend test framework exists anywhere in this repository — independently confirmed during validation, not a BA-04-specific gap.

**B1 remediation is now complete.** This record does **not** constitute certification of BA-04 — it documents that the second certification's own B1 finding has been remediated. **BA-04 is awaiting a further fresh independent re-certification.**

---

## BA-04 Increment — Repository Owner Decision Recording (`RO-DEC-WP14-BA05-01`)

**Recorded 2026-08-16, per direct Repository Owner instruction ("WP-14 — Repository Owner Decision Recording, BA-05 Knowledge Graph Synchronization").** This section records a governance **decision**, not an implementation. It authorizes no code change to BA-04's own already-certified behavior and does not itself constitute BA-04 Increment implementation authorization.

**Context:** the independent WP-14 BA-05 Technical Design Authorization Review found BA-05's sole documented trigger — a Knowledge Asset reaching `ACCEPTED` and a corresponding Domain Event — does not exist in this Business Activity's own delivered, certified scope. This was not a newly-discovered defect: §9 ("Two distinct open items"), §12, and §183 items 2 and 4 of this charter (above) already, explicitly disclosed at this Business Activity's own original authorization (2026-08-10) that the `curation_status` transition graph and BA-04's own outcome-event name/version/schema were both genuinely open `[D]` items, "not invented" by that authorization. A subsequent Repository Owner Decision Package (`WP-14 BA-05 Repository Owner Decision Package`) analyzed the available trigger models and found exactly one — completion of this already-disclosed, already-deferred scope — consistent with `RTA-001 §12.14`'s own governing text ("Knowledge updates are triggered by Domain Events rather than direct Business Activity invocation," which forecloses a caller-invoked alternative).

**Decision `RO-DEC-WP14-BA05-01` — APPROVED:** BA-05 shall be triggered by a Domain Event emitted when a Knowledge Asset completes its governed lifecycle transition to `ACCEPTED`. That trigger shall be produced by BA-04, via a formally authorized **BA-04 Increment** completing this charter's own already-disclosed, deferred transition/event scope (§183 items 2 and 4).

**What this decision explicitly does NOT do:**
- It does **not** characterize BA-04's existing certified `establish()`/`get_by_id()` behavior as defective. That behavior is unchanged, unaffected, and not reopened by this decision.
- It does **not** authorize BA-04 Increment implementation. The Increment requires its own Technical Design, its own implementation authorization, and its own independent certification/V&V per `CLAUDE.md §19.7`/`§19.7b`, exactly as BA-04's own original scope did.
- It does **not** decide any implementation detail of the Increment — endpoint naming, request/response schema, the transition graph (which of the five `curation_status` states may transition to which others), event class name, event version, event payload schema, transaction implementation, idempotency mechanism, or event delivery mechanism. All remain open, to be resolved during the BA-04 Increment's own Technical Design, per this charter's own established `[C]`/`[D]` discipline.
- It does **not** authorize BA-05 implementation. `RO-DEC-WP14-BA05-02` (the concrete Knowledge Graph relationship/event-type mapping BA-05 itself needs) remains **OPEN** — see `TECH-DEBT.md`/`TDS-013` for its current status. BA-05 remains **DESIGNED / NOT AUTHORIZED / ZERO IMPLEMENTATION**. *(This "remains OPEN" statement was accurate at the moment this section was recorded, 2026-08-16, before the mapping decision below was made later the same day — preserved here as the historical record, not deleted, per `ADR-017`/`METH-002`'s no-silent-fix discipline.)* **Superseded — see "BA-05 — Repository Owner Decision Recording (`RO-DEC-WP14-BA05-02`, `RO-DEC-WP14-BA05-03`)" below:** `RO-DEC-WP14-BA05-02` was subsequently approved and is now independently recorded in this charter. That resolution does **not** change BA-05's own governance state above — BA-05 remains **DESIGNED / NOT AUTHORIZED / ZERO IMPLEMENTATION** regardless; approving the mapping decision does not itself authorize BA-05 implementation.

**Expected BA-04 Increment scope, named but not designed here:**
1. A Knowledge Asset status-transition capability: `PROPOSED` → `VALIDATED`/`ACCEPTED`/`REJECTED` (the transition endpoint `IRA-014 §6` BA-04's own row already names; its own graph — which states may reach which others — remains undecided, `[D]`, per §183 item 2, unchanged by this decision).
2. Domain Event publication when a Knowledge Asset reaches `ACCEPTED`, carrying sufficient tenant/context information for BA-05 to process it safely — the exact payload shape is not invented here and remains an Increment Technical Design item.

**Next governed step for this Increment (as of this recording, 2026-08-16):** BA-04 Increment Technical Design and its own separate Repository Owner implementation authorization — not performed by this recording.

### RO-DEC-BA04-INC-007 — Database / Domain Event Consistency Posture

**Recorded 2026-08-16, per direct Repository Owner instruction ("WP-14 BA-04 Increment — Record RO-DEC-BA04-INC-007 in BA-04 Charter").** This entry independently records, in this charter, a decision already made and already fully recorded in `TDS-014_WP-14_BA-04_Increment_Knowledge_Asset_Lifecycle_Transition_Technical_Design.md` (its own §9/§19/§21) — mirroring the same pattern this section already established for `RO-DEC-WP14-BA05-01` above (recorded here as well as referenced by `TDS-013 §26a`), so that this decision is not evidenced solely by the one artifact whose own design depends on it. **This entry does not modify `TDS-014`, does not change the decision's own substance, and does not decide anything new.**

**Sequence, preserved accurately, not backdated:** this charter's own §9/§12/§183 (above) disclosed the transition/event scope as deferred at BA-04's original authorization (2026-08-10) → `RO-DEC-WP14-BA05-01` approved the BA-04 Increment as BA-05's trigger mechanism (recorded above, this same section) → the BA-04 Increment Technical Design (`TDS-014`) was subsequently authored, and identified the DB/Domain-Event consistency posture as its own one remaining open Repository Owner decision (`BA04-INC-DEC-007`) → the Repository Owner approved best-effort event delivery → `TDS-014` was updated to record that approval → a fresh, independent Technical Design Authorization Review of the completed `TDS-014` returned **AUTHORIZED WITH CONDITIONS**, with exactly one condition: that this decision also be independently recorded here, in the charter, distinct from `TDS-014` itself → this entry satisfies that condition.

**Status:** APPROVED.

**Decision:** best-effort event delivery is accepted for the current BA-04 Increment.

**Consistency invariant:** `DATABASE COMMIT → DOMAIN EVENT PUBLISH ATTEMPT`. The Knowledge Asset state transition commits before any event-publish attempt is made. A rollback means no publish attempt occurs at all. A successful commit results in exactly one publish attempt.

**Accepted failure modes, explicitly accepted by the Repository Owner, not characterized as a defect in the BA-04 state transition itself:**
1. The event publisher is unavailable, or the event is not actually delivered anywhere, under the current mock-only infrastructure (`Backend/Shared/Events/event_publisher.py::KafkaEventPublisher.publish()`'s own real broker dispatch call is commented out — independently verified, not assumed).
2. The process crashes after the DB commit but before the publish attempt is reached.
3. The publish attempt itself raises an exception.
4. No automatic retry occurs in this Increment.
5. If the `ACCEPTED` event is not delivered, BA-05 will not execute for that transition under the current architecture — an explicitly accepted limitation of this Increment, not a defect.

**Explicitly excluded guarantees — not claimed, not weakened or reinterpreted by this entry:** guaranteed event delivery; exactly-once event delivery; automatic retry; replay; a transactional outbox; a durable event store; guaranteed recovery after process failure.

**Future platform concern, not decided or scheduled here:** durable Domain Event delivery remains a future, platform-level design concern. Potential future mechanisms — a transactional outbox, a durable event store, retry, replay, dead-letter handling, guaranteed-delivery semantics — are named for awareness only; none is selected, authorized, or implemented by this entry or by `TDS-014`.

**What this entry explicitly does NOT do:** it does not reopen `RO-DEC-BA04-INC-007`'s own substance; does not change best-effort delivery to an outbox or any other mechanism; does not add retry; does not change the commit-then-publish ordering, the event contract, the BA-05 trigger, the BA-05 relationship (`Governed By`), the state machine, authorization, or the concurrency mechanism (`TDS-014 §6`); does not authorize BA-04 Increment implementation; does not modify `TDS-014`, `RTA-001`, `ONT-001`, or `CLAUDE.md`.

**Next governed step (as recorded at the time of the `RO-DEC-BA04-INC-007` entry above):** with that recording, the fresh independent Technical Design Authorization Review's own single condition was closed. Implementation authorization for the BA-04 Increment was, at that time, a distinct, separate, not-yet-granted Repository Owner action — granted by the entry immediately below.

### BA-04 Increment — Implementation Authorization

**Recorded 2026-08-16, per direct Repository Owner instruction ("WP-14 BA-04 Increment — Implementation Authorization").** This entry is the formal Implementation Authorization gate for the BA-04 Increment. **It authorizes implementation to begin; it does not itself constitute implementation, certification, V&V, or Release Readiness — each remains a distinct, future, independently-gated action per `CLAUDE.md §19.7`/`§19.7b`.** No source code, migration, API, or test is created by this entry.

**Authorization basis:**
1. `TDS-014_WP-14_BA-04_Increment_Knowledge_Asset_Lifecycle_Transition_Technical_Design.md` — complete Technical Design Specification.
2. `RO-DEC-BA04-INC-007` (Database/Domain Event Consistency Posture) — approved by the Repository Owner and recorded in `TDS-014` (§9/§19/§21).
3. A fresh, independent Technical Design Authorization Review of the completed `TDS-014` — **AUTHORIZED WITH CONDITIONS**, one condition (independent recording of `RO-DEC-BA04-INC-007` outside `TDS-014` itself).
4. That condition closed by the `RO-DEC-BA04-INC-007` entry immediately above, in this same charter section.
5. No technical-design rework was required by the independent review — sixteen of seventeen readiness dimensions were confirmed READY on first review; the seventeenth (event consistency) was confirmed READY once condition 3/4 above closed.

**Decision: BA-04 Increment implementation is AUTHORIZED**, strictly bounded to `TDS-014`'s own frozen design — the implementing agent MUST NOT invent lifecycle transitions beyond `PROPOSED`→{`VALIDATED`,`ACCEPTED`,`REJECTED`}, `ACCEPTED` semantics, authorization rules, API semantics, the event name/version/payload, tenant rules, the concurrency mechanism, idempotency semantics, event ordering, or BA-05 relationship semantics — every one of these is already frozen by `TDS-014` (§2–§13, §18) and by this section's own prior `RO-DEC-WP14-BA05-01`/`RO-DEC-BA04-INC-007` entries. Where `TDS-014` does not provide enough information for a genuine implementation question, the implementing agent SHALL STOP and report the gap rather than invent a resolution, per `CLAUDE.md §17`/`§19.4`.

**Explicit exclusions, unchanged and unaffected by this authorization:** no BA-05 implementation of any kind (no `enterprise_knowledge_graph_registry` code, no `Knowledge Asset —[Governed By]→ Organization` relationship creation — BA-04 produces only the `ACCEPTED` fact); no live Neo4j graph writes; no Knowledge Graph implementation; no additional lifecycle-transition edge beyond the three named above; no transactional outbox, retry infrastructure, replay mechanism, or durable event store (`RO-DEC-BA04-INC-007`'s own explicit exclusions, unchanged); no modification of BA-01, BA-02, or BA-03; no new Capability, Business Activity, SER, or relationship kind; no change to `RTA-001`, `ONT-001`, or any other canonical architecture document.

**Governance state, as of this authorization:** `BA-04 Increment` moves from `DESIGNED / TECHNICAL DESIGN AUTHORIZATION CONDITION CLOSED` to **`IMPLEMENTATION AUTHORIZED`**. It is explicitly **not** `IMPLEMENTATION COMPLETE`, **not** `CERTIFIED`, and **not** `RELEASED` — each remains a distinct, future gate, per `CLAUDE.md §19.7`/`§19.7b`'s own five-gate closure sequence, applied to this Increment exactly as it was already applied to BA-03 and to BA-04's own original scope. The implementing session, once implementation is complete, SHALL NOT self-certify — a fresh, independent Gate 1 reviewer is required, per the same discipline already exercised at every gate this Work Package has passed through so far.

## BA-05 — Repository Owner Decision Recording (`RO-DEC-WP14-BA05-02`, `RO-DEC-WP14-BA05-03`)

**Recorded in this charter 2026-08-23, remediating Finding `F-01` of the independent WP-14/BA-05 Technical Design Authorization Review of `TDS-013`.** That review found `RO-DEC-WP14-BA05-02` and `RO-DEC-WP14-BA05-03` — both originally made and recorded by the Repository Owner on 2026-08-16, in `TDS-013 §26a` — were evidenced **solely by the one artifact (`TDS-013`) whose own design depends on them**, with no independent record elsewhere in the repository. This is the identical insufficiency the `RO-DEC-BA04-INC-007` entry above was created to correct for a different decision, applied here to these two. **This entry independently records, in this charter, decisions already made and already fully recorded in `TDS-013` (§20/§26a) — it does not modify `TDS-013`, does not change either decision's own substance, does not decide anything new, and does not itself authorize BA-05 implementation.**

**Sequence, preserved accurately, not backdated:** `RO-DEC-WP14-BA05-01` approved the BA-04 Increment as BA-05's trigger mechanism (recorded above, this same charter, 2026-08-16) → the Repository Owner separately decided BA-05's own hosting service and per-trigger relationship mapping the same day, recorded at the time only in `TDS-013 §26a` → a subsequent `TDS-013` reconciliation pass integrated those decisions into `TDS-013`'s own main body (§7–§10, §20, §24, §25) → a fresh, independent Technical Design Authorization Review of the reconciled `TDS-013` returned **AUTHORIZED WITH CONDITIONS**, with two blocking findings, one of which (`F-01`) was exactly this decisions'-own insufficient, single-artifact evidentiary basis → this entry, together with the accompanying `TDS-013` correction of `F-02`, satisfies `F-01`.

### `RO-DEC-WP14-BA05-03` — Hosting Service

**Decision — APPROVED, 2026-08-16 (originally recorded `TDS-013 §26a`, independently re-recorded here 2026-08-23):** `AIService` is the confirmed hosting service for `enterprise_knowledge_graph_registry` (`AMD-012`/`AMD-016`), per `TDS-013 §20`'s own recommendation and evidentiary analysis — no longer merely a recommendation requiring further Repository Owner concurrence.

**Scope, precisely bounded — this decision resolves ONLY the hosting-service question for `enterprise_knowledge_graph_registry`.** It does **not** resolve hosting for BA-01–BA-04's own tables (`AMD-013`/`AMD-004`/`AMD-005` — a separate, still-open determination, unaffected by this decision, per `TDS-013 §20`'s own explicit statement). It does not authorize any migration, model, or schema change — none is created by this entry or by `TDS-013`. It does not authorize BA-05 implementation.

### `RO-DEC-WP14-BA05-02` — Per-Trigger Relationship Mapping

**Decision — APPROVED, 2026-08-16 (originally recorded in full, with source/target/relationship-kind/cardinality/tenant-rule/idempotency/evidence-audit rationale, in `TDS-013 §26a`; independently re-recorded here 2026-08-23, restated in summary, not duplicated in full):** upon a Knowledge Asset reaching `ACCEPTED`, BA-05 shall establish exactly one relationship — `source_entity_type = KNOWLEDGE_ASSET`, `relationship_type = Governed By` (the exact, unmodified `RTA-001 §12.9` vocabulary value), `target_entity_type = ORGANIZATION`, target identified by the Knowledge Asset's own authoritative, persisted `organization_id`.

**Scope, precisely bounded — this decision authorizes ONLY the one mapping stated above.** It does **not** create a Knowledge Asset→CDE relationship; does **not** create a Knowledge Asset→source-ingestion-owner relationship; and does **not** authorize a mapping for any trigger event other than Knowledge Asset `ACCEPTED`. Any future trigger event or additional relationship kind remains open and requires its own separate Repository Owner decision — this entry does not generalize `RO-DEC-WP14-BA05-02` into a blanket per-trigger-mapping authorization. The idempotency mechanism (database `UNIQUE` constraint vs. check-before-insert) is not decided by this entry or by `RO-DEC-WP14-BA05-02` itself — unchanged, still an implementation-time choice (`TDS-013 §17`/§24 item 4).

**Reconciles this charter's own §254 (above, "BA-04 Increment — Repository Owner Decision Recording"):** that entry's own statement that `RO-DEC-WP14-BA05-02` "remains OPEN" was accurate at the moment it was written (2026-08-16, before this mapping decision was made later the same day). It is superseded by this entry — preserved there as the historical record, not deleted, per `ADR-017`/`METH-002`'s no-silent-fix discipline; marked as superseded there with a cross-reference to this section.

**What neither entry above does:** authorize BA-05 implementation; modify `TDS-013`, `RTA-001`, `ONT-001`, `AMD-012`, `AMD-016`, or `Master_Technical_Architecture.md`; decide any BA-05 implementation-time detail (idempotency mechanism, event schema, handler code, read-endpoint schema).

**Governance state, as of this recording:** `RO-DEC-WP14-BA05-02` and `RO-DEC-WP14-BA05-03` are now independently evidenced in this charter, in addition to `TDS-013 §26a`. BA-05 remains **`DESIGNED / NOT AUTHORIZED / ZERO IMPLEMENTATION`** — unaffected by this recording; a fresh, independent Technical Design Authorization Review of `TDS-013` as reconciled and remediated (`F-01`/`F-02`/`F-03`) is required before BA-05 implementation may be authorized, per `CLAUDE.md §19.7`.

## BA-05 — Implementation Authorization

**Recorded 2026-08-23, per direct Repository Owner instruction ("Authorize BA-05 implementation and proceed to chartering").** This entry is the formal Implementation Authorization gate for BA-05, mirroring exactly the "BA-04 Increment — Implementation Authorization" entry above — the same two-step chartering-then-authorization precedent `WP-10`/`WP-11`/`WP-12` each established, applied here to BA-05. **It authorizes implementation to begin; it does not itself constitute implementation, certification, V&V, or Release Readiness — each remains a distinct, future, independently-gated action per `CLAUDE.md §19.7`/`§19.7b`.** No source code, migration, API, or test is created by this entry.

**Chartering basis (the first step of the precedent, already satisfied, not repeated here):** `IRA-014 §6`/`§17` charters BA-05 as in-scope, Classification B — architecturally unblocked (per `ADR-023`/`AMD-016`) — and explicitly states BA-05's own authorization "is not assumed to be automatic or bundled with BA-01–04's own authorization" (`IRA-014 §17`), requiring its own separate Technical Design and its own separate implementation authorization. `IRA-014`'s own chartering disposition for BA-05 is unmodified by this entry.

**Implementation Authorization basis:**
1. `TDS-013_WP-14_BA-05_Enterprise_Knowledge_Graph_Synchronization_Technical_Design.md` — complete Technical Design Specification (§1–§26, §26a).
2. `RO-DEC-WP14-BA05-01` (trigger model) — APPROVED, recorded above and in `TDS-013 §26a`.
3. `RO-DEC-WP14-BA05-02` (per-trigger relationship mapping) and `RO-DEC-WP14-BA05-03` (hosting service) — APPROVED, independently recorded above (this charter's own "BA-05 — Repository Owner Decision Recording" section, `F-01` remediation) and in `TDS-013 §20`/`§26a`.
4. The BA-04 Increment (`RO-DEC-WP14-BA05-01`'s own trigger dependency) — CLOSED, CERTIFIED, committed `4c86813`, governance-synchronized `8b3f475` — independently re-verified as part of `F-02` remediation, not merely asserted.
5. A fresh, independent Technical Design Authorization Review of `TDS-013` as reconciled and remediated (`F-01`/`F-02`/`F-03`) — **AUTHORIZED**, no blocking findings. Two non-blocking conditions were named (the idempotency mechanism remains an implementation-time decision, per item 6 below; this charter's own governance-sync treatment, per the note below).
6. Independent verification of the `F-01`/`F-02`/`F-03` remediation itself, performed by a separate fresh-context reviewer prior to item 5 — **REMEDIATION VERIFIED**.
7. No technical-design rework was required by the independent review — the review found no blocking finding across architectural alignment, repository evidence, BA-05 scope, the BA-04 Increment dependency, persistence/RLS design, event/synchronization design, security/tenancy, or governance integrity.

**Decision: BA-05 Implementation is AUTHORIZED**, strictly bounded to `TDS-013`'s own frozen design (§1–§26, §26a) — the implementing agent MUST NOT invent: any trigger event other than Knowledge Asset reaching `ACCEPTED`; any relationship kind other than the one `Governed By` mapping `RO-DEC-WP14-BA05-02` decides (specifically, no Knowledge Asset→CDE relationship and no Knowledge Asset→source-ingestion-owner relationship); a live Neo4j graph write; generalized ontology-mapping logic beyond `RTA-001 §12.9`'s own closed-list-membership check; a new microservice or physical component; any change to BA-01–BA-04 or the BA-04 Increment's own certified behavior; or any database object, column, or migration beyond what `AMD-012`/`AMD-016` already architect. Where `TDS-013` does not provide enough information for a genuine implementation question, the implementing agent SHALL STOP and report the gap rather than invent a resolution, per `CLAUDE.md §17`/`§19.4`.

**Implementation-time decisions, explicitly delegated to the implementing agent's own judgment by `TDS-013` itself, not to be escalated into architecture decisions or treated as blockers:** the idempotency mechanism (database `UNIQUE` constraint vs. check-before-insert, `TDS-013 §17`/§24 item 4); the `get_session()` reuse adaptation detail (`TDS-013 §15`); the optional read-endpoint's exact request/response schema, if built (`TDS-013 §19`). None of these requires a further Repository Owner decision before implementation begins.

**Explicit exclusions, unchanged and unaffected by this authorization:** no live Neo4j graph write (`SE-025`, disclosed, deferred, out of scope); no additional trigger event beyond Knowledge Asset `ACCEPTED`; no Knowledge Asset→CDE or Knowledge Asset→source-ingestion-owner relationship; no modification of BA-01, BA-02, BA-03, BA-04, or the BA-04 Increment's own certified behavior; no new Capability, Business Activity, SER, or relationship kind; no change to `RTA-001`, `ONT-001`, `ADR-023`, `AMD-012`, `AMD-016`, `Master_Technical_Architecture.md`, or any other canonical architecture document; no live message-bus/broker implementation (`AzureServiceBusStub`/mock publishers remain unchanged — a disclosed, non-blocking infrastructure-maturity gap, `TDS-013 §24` item 2, not this authorization's own concern to resolve).

**Governance-synchronization note (per the established precedent, not a new decision):** `WP-REG-001`'s WP-14 row currently states BA-05 is "not yet Technical-Design-complete or separately authorized" — stale as of this entry. Per the established precedent this charter itself already carries (the BA-04 Increment's own Implementation Authorization, recorded 2026-08-16, did **not** trigger a `WP-REG-001` update at that time — only its subsequent Closure/Certification did, via `8b3f475` on 2026-08-19), `WP-REG-001` is **not** synchronized by this entry. It will be synchronized at BA-05's own Closure, mirroring that same precedent exactly — not before.

**Governance state, as of this authorization:** `BA-05` moves from `DESIGNED / TECHNICAL DESIGN AUTHORIZED` to **`IMPLEMENTATION AUTHORIZED`**. It is explicitly **not** `IMPLEMENTATION COMPLETE`, **not** `CERTIFIED`, and **not** `RELEASED` — each remains a distinct, future gate, per `CLAUDE.md §19.7`/`§19.7b`'s own five-gate closure sequence, applied to BA-05 exactly as it was already applied to BA-01–BA-04 and to the BA-04 Increment. The implementing session, once implementation is complete, SHALL NOT self-certify — a fresh, independent Gate 1 reviewer is required, per the same discipline already exercised at every gate this Work Package has passed through so far, including this authorization's own two independent reviews (remediation verification, then Technical Design Authorization).

---

*End of this charter. Backend implementation (model, migration, repository, service, router, schemas, tests, and audit logging) exists under `Backend/Services/AIService/` per the authorization above and the Remediation Record. The minimum Enterprise Experience (Establish + status view) exists under `source/frontend/src/features/knowledge-asset/` per the Second Independent Certification & Enterprise Experience Remediation Record above. A BA-04 Increment (status-transition capability + Domain Event publication) is fully designed (`TDS-014`), independently reviewed (AUTHORIZED WITH CONDITIONS, condition closed), **IMPLEMENTATION AUTHORIZED**, implemented, and **CLOSED — CERTIFIED** (`4c86813`, governance-synchronized `8b3f475`). BA-05 is now fully designed (`TDS-013`, reconciled and remediated), independently reviewed (AUTHORIZED, no blocking findings), **IMPLEMENTATION AUTHORIZED** (above), and **IMPLEMENTED** (`a7ebb4b`) — Gate 1 Implementation Review and Gate 2 Verification & Validation Audit have each PASSED WITH CONDITIONS, each condition remediated and independently verified — but BA-05 is **NOT YET CERTIFIED** and **NOT YET CLOSED**; BA-01–BA-04's own existing certified behavior and the BA-04 Increment's own certified behavior are unchanged throughout. `ADR-023`, `AMD-016`, `RTA-001`, `ONT-001`, `IRA-014`, `TDS-013`, `TDS-014`, `CLAUDE.md`, and the Enterprise Search specification are unmodified by this recording.*
