# TDS-017 — C-040 (Tenant Administration) — Authority Runtime Enforcement — Technical Design Specification

**Document ID:** TDS-017
**Capability:** C-040 — Tenant Administration (`CAP-001` line 80)
**Scope:** the runtime-authorization mechanism by which `AI-001`/`AI-002` become enforceable at an API layer. **A separate workstream from `TDS-016`** (`tenant_registry` schema/transaction remediation) — not a continuation of it, per explicit instruction.
**Basis:** `TDS-016 §12`'s own corrected finding (2026-08-26 amendment): the runtime mechanism is undetermined; `approval_authority_registry` is organization-scoped and structurally incompatible with a pre-Organization authority, per `ADR-031 §8`.
**Governing constitutional authority (cited, not restated):** `ADR-016`, `ADR-029 §10`/`§11`/`§12`, `ADR-030`, `ADR-031 §8`, `ADR-033 §9`, `ADR-035`, `AI-001`–`AI-003`, `URA-001-04`/`-41`/`-42`/`-75`/`-76`/`-77`, `ADR-002 §17a`/`§18`, `TD-157`.

**Document-naming note:** next number in the flat, sequential TDS series after `TDS-016`; capability-first, no WP exists for C-040 (identical basis to `TDS-015`/`TDS-016`'s own precedent).

**Status:** Technical Design — implementation NOT authorized. No runtime authorization object is created, no ADR is created, no one is assigned to any object, `AI-002` is not populated.

---

## 1. Purpose

Determine how `AI-001`/`AI-002` — constitutionally established, appointed (or not) via the Two-Key mechanism — are intended to become enforceable runtime authorization controls, given that no canonical artifact currently performs this translation and the obvious candidate (`approval_authority_registry`) is structurally incompatible with a pre-Organization authority.

## 2. Scope

**In scope:** tracing every existing ADR-016/`URA-001-76` tier and every implemented authorization-adjacent construct in `AuthService`/`Backend/Runtime/AuthorizationEngine/` against `AI-001`/`AI-002`'s own requirements; identifying which existing mechanism, if any, can satisfy them without constitutional change; precisely bounding the residual technical gap.

**Out of scope (§13, restated as a closing checklist at §17):** `tenant_registry` implementation, `TenantMiddleware` redesign, `X-Tenant-ID` repointing, `AI-002` appointment, the Sarika Rath evidence loop, new governance membership, new constitutional authority, the fresh IRA, actual runtime-object creation.

## 3. Constitutional Baseline

`AI-001` (populated, Ashit Padhi via `AI-003`) and `AI-002` (constitutionally established, unpopulated, `TD-157` Open — BLOCKED) each hold an exclusive MAY grant (`ADR-029 §10`/`§11`) with explicit MUST-NOT prohibitions including self-approval and inheriting `PLATFORM_ADMIN`'s bypass semantics. Both are platform-wide, pre-Organization (`ADR-031 §8`, `ADR-033 §9`). `ADR-035 §9`/`AI-003 §15` explicitly state no runtime object (role, System Role, Business Role, Group, Approval Authority object) is created by any Appointment Instrument. None of this is reopened, reinterpreted, or narrowed here.

## 4. Runtime Authorization Baseline

`ADR-016` confirms `Backend/Runtime/AuthorizationEngine/` (`WP-RTA-001`) as the single, authoritative Authorization Runtime, implementing `URA-001-76`'s five-tier precedence model: Named User > Group > Approval Authority > Business Role > Domain Permission. Directly re-verified against the actual source (`authorization/models.py`, `authorization/tier_resolvers.py`) for this design, not assumed from any prior citation.

**Question 1 — Constitutional→runtime translation mechanism. Answer: none is currently defined.** No ADR, `AI-001`/`AI-002`/`AI-003`, or `URA-001` provision states how an Appointment Instrument becomes a runtime-enforceable claim. This is stated as a fact, not invented here.

## 5. Existing Authorization Machinery — Full Trace

**Question 2/3 — tier mapping and `approval_authority_registry` inspection.**

- **`AuthorizationContext` (the Engine's own shared input, `models.py`):** `organization_id: str` — **mandatory, no default, no `Optional`.** This is a structural property of the Engine's own certified input contract (`RTA-001 S11.5`), affecting **every** tier's invocation, not only tier 3. **This is a broader finding than `TDS-016 §12`/`ADR-031 §8` identified** — those examined the `approval_authorities` table specifically; the same constraint exists one level deeper, in the Engine's own shared Context model.
- **Tier 3 — Approval Authority (`ApprovalAuthority`, `models/approval_authority.py`):** real, migrated (WP-02). `organization_id: Mapped[uuid.UUID] = mapped_column(..., nullable=False, ...)`, docstring: *"Required for every scope, including GLOBAL/COMPANY."* **Confirms `ADR-031 §8`'s own finding directly against the actual code** — cited, not rediscovered as new. `GLOBAL`/`COMPANY` scope types exist in `ApprovalScopeType` but **do not exempt the row from carrying `organization_id`** — "GLOBAL" here means global *within* one Organization's own approval structure, not platform-wide across Organizations. **Not usable for `AI-001`/`AI-002` as currently structured.**
- **Tier 1 — Named User (`NamedUserResolver`):** the resolver's own docstring names no Organization/Membership dependency — it resolves "a direct, object-scoped assignment" per `URA-001-77` ("Object Scoped, Event Scoped, and Time Scoped"), conceptually the most promising tier. **However:** the actual assignment-*policy* table implementing this tier, `RuntimeAssignmentPolicy` (`models/runtime_assignment_policy.py`), **also carries `organization_id: Mapped[uuid.UUID] = mapped_column(..., nullable=False, ...)`** — the identical constraint. Its own docstring further states: *"this model never holds a specific object_type/object_id anchor or assignee — those belong exclusively to the (not yet implemented in `AuthService`) `runtime_assignment_registry`."* **The actual Named User assignment-instance registry does not exist anywhere in this repository's implemented code.** This is a second, independent confirmation of the same pattern, and a genuinely new finding this design surfaces.
- **Tier 2 — Group, Tier 5 — Domain Permission:** not independently re-verified to the same depth (out of proportion to this design's own purpose, since neither offers named-individual binding — §9), but both are consumed through the same `organization_id`-mandatory `AuthorizationContext`.
- **Tier 4 — Business Role (`Role` model):** confirmed elsewhere in this repository (`AuthService/middleware/tenant.py`'s own comment: *"Roles are platform-global (`URA-001` Section 3), not tenant-scoped"*) to carry no `organization_id` column — the one tier that is genuinely platform-global as implemented. **Not usable regardless**, because a Business Role is held by *anyone* granted that role — it cannot bind to one specific, named human individual, which `AI-001`/`AI-002` require (§9).
- **A separate, already-certified, non-tiered mechanism exists: `require_platform_admin` (`AuthService/dependencies.py`).** Directly re-verified: `claims.get("role_code") != PLATFORM_ADMIN_ROLE_CODE` → 403; nothing else. This function is **not part of the five-tier Engine at all** — it reads the caller's JWT claims directly and compares one field. `ADR-002 §18` independently confirms `PLATFORM_ADMIN`/`AUREX_ADMIN` sit outside the five-tier model ("`system_role_registry`/`AUREX_ADMIN` is not added to, or wired into, the five-tier model"). **This pattern — a direct, simple claims-comparison dependency, with zero `organization_id` involvement — is the one already-proven, already-certified mechanism in this repository with no organization dependency of any kind.**

## 6. `AI-001` Runtime Requirements

To enforce `AI-001`'s exclusive MAY grant, named accountable human (Ashit Padhi), self-approval prohibition, and `PLATFORM_ADMIN`-bypass prohibition, a runtime check must: (a) identify the caller's specific individual identity (not role, not Organization) from an already-authenticated request; (b) compare it against the currently-appointed `AI-001` holder; (c) never accept a `PLATFORM_ADMIN` claim as a substitute (`ADR-029 §10`, `ADR-002 §17a`'s own bypass-scope question remains separately unresolved and is not touched here). **Not created here — design only.**

## 7. `AI-002` Runtime Requirements

Identical shape to §6, applied to whichever individual is eventually appointed. **`AI-002` remains unpopulated.** This section defines the mechanism that *would* apply once an accountability point exists — it does not create, simulate, assume, or imply a current holder. Any runtime check for `AI-002` today would correctly and permanently deny every caller, since no comparison value exists to match against (`TD-157`).

## 8. Pre-Organization Requirements

**Question 9 — the critical question.** No existing implemented mechanism among the five `ADR-016`/`URA-001-76` tiers can operate without `organization_id`, confirmed at two independent levels (§5): the Engine's own shared `AuthorizationContext`, and every implemented tier-adjacent table examined (`approval_authorities`, `runtime_assignment_policies`). **Classification: not a constitutional gap.** Nothing in `ADR-016`, `URA-001`, or `RTA-001` states the five-tier model must be used for every authorization decision on this platform — `require_platform_admin`'s own existence and `ADR-002 §18`'s own confirmation that `PLATFORM_ADMIN`/`AUREX_ADMIN` sit outside the five-tier model prove a second, simpler, already-certified enforcement pattern already coexists with it. **This is a technical gap in the five-tier model's own applicability to pre-Organization authorities specifically — correctly resolved by using the already-proven alternative pattern (§5's last bullet), not by inventing a new mechanism or reopening `ADR-016`.**

**Authentication prerequisite — a distinct, deeper gap, confirmed by direct inspection of `Backend/Services/AuthService/services/auth_service.py::authenticate_user`:** the runtime authorization comparison itself (Option C) does not require `organization_id` and does not construct `AuthorizationContext` or invoke `AuthorizationEngine` (§5, §11). **However, the current JWT issuance/login path is not organization-independent.** `authenticate_user` requires the caller to already hold at least one active Organization Membership before any token is issued at all (`if not memberships: raise HTTPException(403, ...)`); every issued token carries a `Membership`-derived `organization_id`. **Therefore true pre-Organization runtime enforcement is not yet achieved by Option C alone** — Option C's own comparison logic is organization-independent, but the authentication step that must succeed before that comparison is ever reached is not. **Classification: C — an implementation design gap**, not a constitutional gap, not a Repository Owner governance decision, and not a reason to create a new ADR: nothing in `ADR-029`, `ADR-030`, `ADR-031`, or `ADR-033` requires or forbids any particular login/token-issuance mechanism, and resolving this does not touch `AI-001`/`AI-002`'s own constitutional boundaries.

**Consequence, stated precisely, no claim made beyond the evidence:** for `AI-001` today, Ashit Padhi can obtain a token because he incidentally holds active Organization Memberships elsewhere in the system — this does not itself demonstrate the mechanism is correctly designed for a platform-wide, pre-Organization authority. For a future `AI-002` holder, or a future `AI-001` successor, who holds no Organization Membership anywhere, the current login flow would block token issuance before the Option C dependency (§9) is ever reached. **No claim is made here about whether such a person currently exists or will be appointed** — only that the login flow's own current shape does not accommodate that case. **Not designed or resolved here:** any new login flow, token type, authentication mechanism, global user role, or Organization bypass — this is documented as a required future implementation-design step only (§16, §18).

## 9. Named-Human Binding

**Question 8.** The `require_platform_admin`-shaped pattern is directly reusable **as a template**, not as literal shared code: a new dependency function reading `claims.get("person_id")` (already a live JWT claim — confirmed directly, `dependencies.py`'s own `established_by = UUID(claims["person_id"])` pattern used elsewhere) and comparing it against the specific, currently-appointed holder's own identifier — never a role, never `PLATFORM_ADMIN`, never a Group, never an Organization membership. This satisfies named-human binding without touching the certified `AuthorizationContext`, `approval_authorities`, or `runtime_assignment_policies`.

**Residual, genuinely open implementation question, not resolved here:** where the "currently-appointed holder's identifier" itself is persisted for the comparison to read. No existing table can hold it without either violating its own `organization_id NOT NULL` constraint or requiring a schema change to already-certified WP-02 tables. Candidate options (not selected, §14):
1. A small, new, purpose-built table with no `organization_id` column at all (a genuine implementation act, its own `CMD-001 §26.3a` eligibility question, analogous in kind to `tenant_registry`'s own situation — realizing an already-decided constitutional fact, not deciding a new one).
2. A configuration/environment value.
3. A schema change to `approval_authorities` (e.g., making `organization_id` nullable for a `PLATFORM`-scope row) — touches an already-certified WP-02 table, the highest-friction option.

**Distinguishing the three layers involved, per the independent review's own framing (not to be conflated):**
- **(A) Authentication prerequisite:** a valid, authenticated identity/token must exist before any comparison can occur — **currently gated on Organization Membership** (§8), not itself part of Option C's own design.
- **(B) Authorization:** the proposed dependency compares the authenticated person's own `person_id` against the appointed authority holder's identifier (above).
- **(C) Organization independence:** the authorization comparison itself (B) is fully organization-independent; the authentication prerequisite (A) currently is not (§8). These are two distinct claims, not restated as one.

## 10. Separation-of-Duties Enforcement

**Question 6, classified precisely, per `ADR-029 §12`:**
- **A. Constitutionally required:** no single actor may hold both `AI-001` and `AI-002` for the same Tenant establishment request.
- **B. Runtime implementation requirement:** a straightforward equality check within the Establishment transaction (`TDS-016 §8`) — `allocated_by_actor_id != approved_by_actor_id` for the same establishment record. This is ordinary application logic, not a five-tier-Engine concern, and does not require the runtime-mechanism question (§9) to be resolved first — it is a comparison between two already-recorded actor-identifier fields (`TDS-016 §5`), independent of how either identifier was itself authenticated.
- **C. Not currently specified:** any mechanism for a future multi-member expansion of either authority's own separation-of-duties enforcement — `ADR-035`'s own extensibility clause is unused today (one member only) and not addressed further here.

## 11. `PLATFORM_ADMIN` Boundary

**Question 7.** Re-verified directly, not reinterpreted: `ADR-002 §17a` leaves the `PLATFORM_ADMIN`/`AUREX_ADMIN` universal-bypass scope an explicit, separate, unresolved follow-on decision, entirely outside the five-tier model (`§18`). `ADR-029 §10`/`§11` independently and explicitly prohibit `AI-001`/`AI-002` from inheriting that bypass. **This design does not weaken, narrow, or touch that prohibition** — the named-human dependency proposed in §9 checks a specific `person_id`, never a role or claim `PLATFORM_ADMIN` could satisfy, and explicitly does not fall back to `require_platform_admin` under any circumstance.

## 12. API Enforcement Point (Conceptual — No API Modified)

The conceptual enforcement point is a FastAPI dependency (mirroring `require_platform_admin`'s own shape, §5/§9) attached to whichever future endpoint(s) implement `ADR-026`'s Step 1 (Business Approval decision) and Step 2 (Infrastructure Allocation decision) respectively — the same endpoints `TDS-016 §8`'s Establishment transaction already describes conceptually. **No API is created, modified, or designed in further detail here** — this section identifies *where* enforcement would attach, not its implementation.

## 13. Audit / Attribution

Cross-referenced, not re-derived: `TDS-016 §11` already designs `approved_by_actor_id`/`approved_at` and `allocated_by_actor_id`/`allocated_at` fields on `tenant_registry`, satisfying `SD-002-056` ("no approval exists without an audit record"). This design adds nothing beyond confirming those fields would be populated from the same `person_id` claim the §9 dependency validates — one consistent identity source across authorization and audit, not two.

## 14. Options Analysis

| Option | Constitutional compat. | Pre-Org compat. | Named-human binding | Separation-of-duties | `PLATFORM_ADMIN` handling | Impl. complexity | Reuses existing machinery | Schema/code change | New ADR? |
|---|---|---|---|---|---|---|---|---|---|
| **A — Five-tier Engine, Approval Authority tier (`approval_authorities`)** | Compatible in principle | **Incompatible** (`organization_id NOT NULL`, `ADR-031 §8`) | Would work if usable | N/A — unusable | N/A | High (schema change to certified WP-02 table) | Partial (existing table, wrong shape) | **Yes — `organization_id` nullability change to a certified table** | No, but touches certified code |
| **B — Five-tier Engine, Named User tier (`runtime_assignment_registry`)** | Compatible in principle | **Incompatible** (`runtime_assignment_policies.organization_id NOT NULL`; instance registry not implemented at all) | Would work if built | Would work if built | N/A | Highest (build an unimplemented registry + resolve its own org constraint) | Minimal (policy table exists, wrong shape; instance table absent) | **Yes — new implementation + schema change** | No |
| **C — Direct claims-check dependency (`require_platform_admin` pattern, new comparison target)** | **Compatible** — no five-tier Engine involvement, no `AuthorizationContext` | **Compatible** — zero `organization_id` dependency, already proven (`require_platform_admin` itself) | **Compatible** — compares a specific `person_id`, not a role | Compatible — independent equality check (§10) | **Compatible** — explicitly never falls back to `PLATFORM_ADMIN` | Lowest — reuses an already-certified pattern verbatim in shape | **Highest** — literal architectural precedent already in production | Only the "where is the holder's ID stored" question (§9, three sub-options, none constitutional) | **No** |

## 15. Recommended Existing Mechanism

**Option C — the direct-claims-check dependency pattern, mirroring `require_platform_admin`'s own already-certified shape — is sufficient and requires no new architecture.** Options A and B both require modifying or completing already-certified or partially-built WP-02 constructs whose own `organization_id NOT NULL` design was correct for their own certified scope (C-003, entirely Organization-scoped) and should not be reinterpreted or weakened to accommodate a platform-wide authority those constructs were never designed for. Option C is not a new mechanism — it is the same pattern this repository already uses for `PLATFORM_ADMIN`, applied with a narrower, named-individual comparison instead of a role comparison. **This is a technical recommendation only, not self-executing** (mirroring `TDS-015 §10`'s own established discipline for separating technical judgment from Repository Owner decision).

## 16. Required Implementation Changes (Not Performed Here)

If Option C is eventually pursued: one new FastAPI dependency function per authority (`AI-001`, and `AI-002` once populated), each reading `person_id` from already-verified claims and comparing against a persisted holder-identifier value; and a decision among §9's three storage sub-options for where that holder-identifier is persisted. Additionally — not part of Option C's own dependency logic, but a precondition for reaching it — the login flow's own Organization-Membership requirement (§8) would need its own, separately-designed resolution before a genuinely pre-Organization holder could authenticate at all. **None of this is implemented, scaffolded, or scheduled by this document.**

## 17. Explicit Non-Goals

This document does not: create any runtime authorization object; assign Ashit Padhi or anyone else to a runtime object; populate `AI-002`; change constitutional authority, membership, or boundaries; create an ADR; implement code; modify schema; create a migration; modify `TenantMiddleware`, `X-Tenant-ID`, or any certified WP-10 behavior; modify `TDS-016`, `tenant_registry`, or `organization_master`; reopen the Sarika Rath evidence loop; run the fresh IRA; change C-040's status.

## 18. Dependencies

- `AI-002` population (`TD-157`, frozen) — independent of this design's own completeness; §7's mechanism applies once populated, not before.
- A future Repository Owner/implementation-time choice among §9's three holder-identifier storage options.
- The login flow's own Organization-Membership prerequisite for JWT issuance (§8) — a distinct implementation dependency from holder-identifier persistence, both required before Option C is fully operable for a genuinely pre-Organization holder.
- `TDS-016`'s own Establishment transaction (§8/§10 there) — this design's §10 (separation-of-duties check) operates on fields `TDS-016 §5`/`§11` already define; no conflict, no modification to that document.
- `ADR-002 §17a`'s own separate, unresolved bypass-scope decision — unaffected by, and not a precondition for, this design.

## 19. Governance / ADR Assessment

**No new ADR is required.** `ADR-016`'s own five-tier model is not modified, weakened, or bypassed by recommending a *different*, already-existing, already-certified mechanism (`require_platform_admin`'s own pattern) for a class of authority (`platform-wide, pre-Organization`) the five-tier model's own implemented tables were never built to represent. No constitutional authority is created, changed, or reinterpreted. The one implementation question left open (§9, holder-identifier storage) is ordinary implementation design, resolvable via `CMD-001 §26.3a`-style eligibility analysis at the time it is actually pursued — not a governance gap requiring Repository Owner adjudication now, and not requiring a new ADR to resolve. The login-flow Organization-Membership prerequisite disclosed at §8 is classified identically: **C — implementation design gap**, not **D** (no Repository Owner decision required) and not **E** (no new ADR required) — resolving it is ordinary authentication-layer implementation work, unrelated to `AI-001`/`AI-002`'s own constitutional boundaries.

## 20. Implementation Authorization Boundary

**This document does not authorize implementation.** Per `CLAUDE.md §19.1`'s own no-self-authorization discipline (the same discipline `TDS-015`/`TDS-016` each already applied): any future implementation of Option C, BA chartering, WP assignment, and Implementation Authorization each remain separate, subsequent, explicit Repository Owner actions.

**Independent-review determination (incorporated here): READY FOR IMPLEMENTATION DESIGN ONLY.** The central Option C design — a direct, `person_id`-based claims-comparison dependency, outside the five-tier Engine, not using `AuthorizationContext`, not using `PLATFORM_ADMIN`, not requiring `approval_authority_registry`, not creating a new constitutional authority or a sixth `ADR-016` tier — is validated. **Two implementation dependencies remain open, neither requiring a Repository Owner governance decision or a new ADR at this stage:** (1) the login flow's own Organization-Membership prerequisite for JWT issuance (§8); (2) holder-identifier persistence (§9, §14). **Implementation authorization must wait until both are resolved in a future implementation design step** — this document is a design baseline only, not a build authorization, for either gap.

**Explicitly preserved, unchanged by this document:**
- `AI-002` remains constitutionally established, unpopulated, `TD-157` Open — BLOCKED, evidence loop frozen.
- C-040 remains RED — Not Implementation Ready.
- `TDS-016` is unmodified.
- `TECH-DEBT.md` and `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md` are unmodified — no update was found to be required by this repository's own TDS convention, mirroring `TDS-015`'s/`TDS-016`'s own precedent.
- No ADR, AI artifact, runtime authorization object, schema, migration, or code was created or modified.

---

## 21. Amendment — Design Resolution (2026-08-26)

**Provenance note, mirroring `TDS-015 §24`'s own established convention:** this amendment records the completed implementation-design resolution for the two dependencies §20 above left open (the login-flow Organization-Membership prerequisite; holder-identifier persistence). **§§1–20 above are preserved unchanged, not rewritten** — this amendment records what has since been resolved at the design level; it does not alter the original analysis or its own independent-review validation. This amendment was performed by the same session that authored the original document and §§1–20's own corrections; it is not itself independently re-reviewed as of this recording — a fresh independent review of this amendment remains available as a subsequent, separate action, not performed automatically by it. **No implementation, code, schema, migration, runtime object, or ADR is created by this amendment.**

## 22. Authentication — Resolved Design

The existing `Person`/`Identity` model (`models/person.py`, `models/identity.py`) is already Organization-independent — neither carries an `organization_id` column, confirmed by direct inspection, consistent with the same `URA-001-15` basis `TenantMiddleware`'s own `/person`/`/identity` exemptions already rely on. The gap is confined to `services/auth_service.py::authenticate_user` (which requires at least one active Membership before issuing any token) and `schemas/auth.py::TokenPayload` (`organization_id: UUID` and `membership_id: UUID`, both currently non-Optional).

**Resolved design:** a narrowly scoped **parallel** authentication path for a platform-wide, pre-Organization accountability point, leaving the ordinary Organization-scoped login flow completely unchanged. For this authority-specific path only: `TokenPayload.organization_id` and `.membership_id` become `Optional[UUID] = None`; `person_id` remains the identity binding, unchanged. No new constitutional authority is created; `PLATFORM_ADMIN`/`AUREX_ADMIN` semantics are not touched; `AuthorizationContext` and `Backend/Runtime/AuthorizationEngine/` are not touched.

**Mandatory constraint, not optional:** this path must **not** become a generic zero-Membership login bypass. Before issuing the special token, the authentication path must itself confirm the authenticated person's `person_id` corresponds to the currently active holder record (§23) — the same record the request-time authorization check (§24) reads. **The runtime authorization check remains a live lookup against the holder record on every request, never a claim trusted from the token itself** — this is the property that makes stale-appointment and revoked-appointment tokens self-correcting rather than requiring token revocation machinery (§25).

**Verified, not assumed:** existing Organization-scoped endpoints continue to correctly reject a pre-Organization token with no further code change — `require_matching_tenant_or_platform_admin` compares the caller's JWT `organization_id` claim against `X-Tenant-ID`; `None` cannot match a real UUID, so rejection is automatic by construction.

## 23. Holder Persistence — Resolved Design (Option 1, Recommended)

**Selected design:** a new, purpose-built, Organization-independent table — no `organization_id` column of any kind. Minimum columns, reusing the already-proven versioning shape `approval_authorities`/`runtime_assignment_policies` already establish (SD-002-010/-011), without their `organization_id NOT NULL` constraint:

| Column | Purpose |
|---|---|
| `id` | PK |
| `authority_identity` | e.g. `AI-001` / `AI-002` — which constitutional authority this row concerns |
| `holder_person_id` | FK → `persons.id` |
| `appointment_instrument_ref` | e.g. `"AI-003"` — citation, not embedding, of the governance record |
| `version`, `status` (`ACTIVE`/`SUPERSEDED`) | `SD-002-011` |
| `effective_from`, `effective_to` | `SD-002-011` |
| `supersedes_id` | Prior-version link, mirroring `approval_authorities`'s own pattern |
| `created_at` | Audit |

**Active-holder uniqueness/concurrency protection:** a partial unique index on `authority_identity` `WHERE status = 'ACTIVE'` — natively supported, prevents two simultaneously-active holders for the same authority.

**Options 2 (config/environment value) and 3 (modify `approval_authorities` to permit a nullable `organization_id`) were evaluated and not selected** — Option 2 on auditability/integrity grounds (no FK, no in-app audit trail); Option 3 because it would touch already-certified `WP-02` code and, on inspection, does not by itself solve holder representation (`approval_authorities` is a policy/catalog object, not a holder record) — it would still require the equivalent of this same new table in addition to the schema change, at higher risk for no compensating benefit. **No constitutional tenure/revocation rule is invented by this table's own existence** — it records who currently holds an already-appointed authority; it does not decide when a change should occur (§25).

**This table is a runtime implementation source of truth. It is not, and does not replace, the Appointment Instrument** (§24).

## 24. Appointment Binding — Resolved Chain

```text
Appointment Instrument (e.g. AI-003, a governance document)
        │  names the appointed human
        ▼
Resolved AuthService person_id (an implementation act)
        │
        ▼
Runtime authority-holder record (§23 table)
        │
        ▼
Request-time person_id authorization check (§22, live lookup)
```

**Explicitly confirmed:** the Appointment Instrument remains a governance artifact throughout — it is never queried by running code and is not, and must not become, the runtime authorization source of truth. That role belongs exclusively to §23's table.

## 25. Lifecycle — Resolved Scope

**Buildable now, as ordinary implementation:** the §23 table itself; its replacement/versioning mechanism (insert a new row, supersede the prior one — the same pattern `approval_authorities` already proves); deactivation (a status change / `effective_to` set); stale-holder prevention (already structurally solved by §22's live-lookup design, not a separate mechanism). `AI-001`'s own initial row is buildable now, since `AI-003` already constitutionally settles its holder; `AI-002`'s is not, since no Appointment Instrument populates it (`TD-157`, untouched by this document).

**Must remain future governance work, not invented here:** the constitutional *rules* for when replacement, succession, tenure, or revocation must occur — `AI-001 §10` and `ADR-031 §13` both leave these explicitly open, and this document does not close them. The mechanism above sits unused until a future Appointment Instrument actually triggers it.

## 26. Implementation Sequence (Derived)

```text
A. Holder-persistence implementation (§23)  ──┐
                                                ├──► C. Runtime authorization dependency (§22/§24)
B. Pre-Organization authentication (§22)   ──┘        │
                                                        ▼
                                              D. Audit wiring (TDS-016 §11)
                                                        │
                                                        ▼
                                              E. Security / negative-path tests
                                                        │
                                                        ▼
                                              F. Explicit Implementation Authorization
```

**A and B are mutually independent and may proceed in parallel** — neither's design depends on the other. **C depends on both.** D depends on C. E depends on A–D existing to test against. F is the separate, explicit Repository Owner gate (§27).

## 27. Updated Classification and Readiness

| Item | Classification |
|---|---|
| `TokenPayload` change (`Optional` `organization_id`/`membership_id`) | **C** |
| Parallel login path | **C** |
| Holder persistence, Option 1 | **C** |
| Appointment Instrument remains governance-only, not runtime source | **A** |
| Runtime replacement/deactivation mechanism | **C** |
| Constitutional replacement/revocation rules | **F** — future governance work |
| `PLATFORM_ADMIN`/`AUREX_ADMIN`/`AuthorizationContext` untouched | **A** |
| Organization-scoped endpoint leakage protection | **A** |

**No item is classified D or E.** No Repository Owner governance decision and no new ADR are required by anything in this amendment.

**Readiness, restated and unchanged from §20's own determination: READY FOR IMPLEMENTATION DESIGN ONLY — not READY FOR IMPLEMENTATION.** Both dependencies §20 identified now have complete, evidence-grounded designs; neither requires further architectural analysis. Actual implementation still requires a separate, explicit Repository Owner authorization act, per `CLAUDE.md §19.1` — this amendment does not, and cannot, self-authorize it.

**Explicitly preserved, unchanged by this amendment:**
- `AI-001` remains populated with Ashit Padhi (`AI-003`).
- `AI-002` remains constitutionally established, unpopulated, `TD-157` Open — BLOCKED, evidence loop frozen.
- C-040 remains RED — Not Implementation Ready.
- No `AI-004`. No new constitutional authority. No new ADR. `ADR-016` is not modified. No certified `WP-02` authorization table (`approval_authorities`, `runtime_assignment_policies`) is modified.
- No implementation, code, schema, migration, or runtime authorization object was created by this amendment.

---

*End of TDS-017 (as amended 2026-08-26). No implementation, migration, model, repository method, router, service, schema, or test file has been created or modified by this document or its amendment. No WP number has been assigned or implied. No other governance document (`CAP-001`, `SD-002`, `SER-001`, `TECH-DEBT.md`, `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`, `Master_Technical_Architecture.md`, `ADR-002`, `ADR-016`, `ADR-024`–`035`, `AI-001`–`003`, `TDS-016`, `CLAUDE.md`) was modified in the preparation of this design or its amendment. No CBOR entry, runtime authorization object, or ADR was created. `AI-002` was not touched. C-040 remains RED — Not Implementation Ready.*
