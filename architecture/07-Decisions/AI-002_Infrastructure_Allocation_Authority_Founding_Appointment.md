# AI-002 — Appointment Instrument: Founding Appointment of the Dedicated Infrastructure Allocation Authority

**Artifact Type:** Appointment Instrument (per `ADR-030 §9`, extended by `ADR-033 §8`), the second exercise of this format — `AI-001` was the first, for a wholly separate authority and appointment case.

**Status:** Executed — Key 2 (Independent Appointment) performed for Decision 2 only.

**Scope:** Decision 2 (Dedicated Infrastructure Allocation Authority) exclusively. Decision 1 (Dedicated Tenant Establishment Business Governance Authority) and `AI-001` are untouched by this Instrument and remain exactly as `AI-001` left them.

---

## 1. Instrument Identifier

**AI-002.**

---

## 2. Initiated By

**Repository Owner**, per `ADR-033`'s own ratification of Repository Owner as the disclosed operational Key-2 case-opener for a specific, already-Canonized authority (`ADR-033 §2`). This field is deliberately distinct from `Appointer` (§3) — `ADR-033 §5`/`§8` requires the two never be conflated, since Repository Owner's own case-opening act carries no substantive appointment authority of its own.

---

## 3. Appointer

A fresh-context AI subagent instance, engaged specifically for this appointment case, with no prior involvement in Canonizing the Dedicated Infrastructure Allocation Authority (`ADR-029 §11`) or in drafting any ADR in the `ADR-024`–`ADR-033` chain, `AI-001`, or any of the cited RODs. No personal name, institutional title, or standing office is claimed or invented — none exists, and none is created by this Instrument. This Appointer is a wholly separate, independently-engaged instance from the Appointer named in `AI-001` — the two share no continuity, memory, or identity; each independently re-derived its own eligibility determination from primary sources for its own, distinct authority (§8 below).

**This Instrument creates no continuing appointment authority for this Appointer.** Performing this one, single, disclosed appointment act does not make this Appointer, or any future instance of its category, a standing Appointment Authority, a permanent Key-2 institution, or eligible for any future appointment case without its own independent eligibility test, per `ADR-031 §3`–`§4`. Any future appointment case — including any future accountability-point appointment for this same authority — requires its own freshly-engaged, freshly-tested candidate.

---

## 4. Authorization Record

Direct, explicit Repository Owner authorization for this specific act, relayed to this Appointer as a direct quote of what the Repository Owner typed in the live conversation with the coordinating session:

> "Proceed with the Key-2 appointment of the Dedicated Infrastructure Allocation Authority. This is a separate appointment case from AI-001 and is now explicitly authorized by the Repository Owner."

**This Appointer's own judgment on sufficiency:** this authorization is specific to this case (names the Infrastructure Allocation Authority by its own working description, not a generic "proceed"), explicitly distinguishes it from `AI-001`'s own, separate case, and directs the Key-2 appointment act itself rather than merely the operational case-opening `ADR-033` already permits Repository Owner to perform unilaterally. This mirrors, in substance and specificity, the authorization `AI-001 §4` relied upon ("I authorize this appointment directly — proceed with creating AI-001"), which this decision sequence has already treated as sufficient for the structurally identical Decision 1 case. This Appointer independently reaches the same conclusion for Decision 2, on the same reasoning: Repository Owner cannot select or become the appointer (`ADR-033 §5`), but a specific, disclosed instruction directing an already independently-tested, eligible candidate to perform the appointment is exactly the "further explicit authorization" `ROD-C040-Business-Authority-Key-2-Fresh-Context-Selection.md §11`/`§15` identified as the one outstanding, non-constitutional requirement before Key 2 could actually be exercised. This Appointer accepts the relayed quote as sufficient on that basis, while noting — as a stated limitation, not a disqualifying defect — that this Appointer has no means of independently verifying the human's typed words beyond the relay itself, a limitation inherent to this session's own architecture and no different from the limitation `AI-001`'s own Appointer necessarily accepted for the structurally identical relay it relied upon.

---

## 5. Key-1 / Canonization Reference

`ADR-029` — **Tenant Business Approval Authority and Infrastructure Allocation Authority: Architectural Model and Authority Boundaries.** Specifically:

- `ADR-029 §9` — Decision, Architectural Model: formalizes the two-stage sequence (Business Approval → Infrastructure Allocation → Technical Provisioning) and confirms both authorities' identities were left `PENDING CANONICAL BINDING` by that ADR.
- `ADR-029 §11` — **Infrastructure Allocation Authority — Architectural Boundaries**: the Purpose, Scope, MAY, and MUST NOT list constituting this authority's own Canonization (§6 below). Verified directly, by this Appointer, in this task: `ADR-029 §11` is its own distinct section, separate from and not mirroring `§10`'s own Business Approval Authority section verbatim — its Purpose, Scope, MAY, and MUST NOT lists are specific to the allocation function and were read and cited on their own terms, not assumed.

Per `ADR-032 §6`'s own definition of Key-1 completion ("the ratification of an authority's own Stage-2 charter... exactly as `ADR-029` already did"), `ADR-029 §11` is Key-1 completion for this authority — confirmed by this Appointer through direct reading of both `ADR-029 §11` and `ADR-032 §6`, not assumed from `AI-001`'s own analogous finding for `ADR-029 §10`. This Instrument does not amend, reopen, or add to `ADR-029` in any respect.

---

## 6. Stage-2 Charter Reference — Authority Boundaries (Cited, Not Restated)

The MAY/MUST NOT boundaries constituted by `ADR-029 §11` govern this authority in full and are not restated here beyond this brief, non-additive summary, verified directly against the primary text:

The authority **may**: allocate a canonical Tenant identity for an approved Tenant establishment request; confirm that the request satisfies allocation prerequisites (a valid, referenced Business Approval decision exists); establish the Tenant identity/boundary allocation itself, consistent with `SD-002-108`'s Universal Identity requirement and `ADR-025`'s 1:1 cardinality; record the allocation decision as a discrete, auditable, attributable act referencing the specific Business Approval decision it allocates against; reject an allocation request lacking a valid, referenced Business Approval decision; and delegate the technical execution of the allocation operation to an automated mechanism, where decision and execution are split.

It **must not**, automatically or by implication: decide whether a Tenant should exist in the first place (`ADR-026`'s own Business Approval step, `ADR-029 §10` — the separate authority `AI-001` populated); override, second-guess, or substitute its own judgment for a Business Approval decision; approve its own allocation request; create or provision infrastructure resources (Technical Provisioning, a separate, still entirely undecided authority); modify Organization identity or administer Organization data; change Tenant–Organization cardinality (`ADR-025`, unaffected); bypass any authorization control, including the certified five-tier Authorization Runtime Engine (`ADR-016`) or `DomainPermission` resolution; inherit `PLATFORM_ADMIN`'s historical universal-bypass semantics (`ADR-002 §17a`, separately unresolved); arbitrarily change an already-allocated Tenant's boundary once established; implement, adopt, or modify `tenant_registry` (remains DEFERRED); change the Tenant schema or any physical implementation detail; or migrate existing data of any kind.

**This Instrument adds nothing to this list and narrows nothing on this list.** The authoritative text is `ADR-029 §11` itself.

**Separation of duties (`ADR-029 §12`), restated as governing context, not narrowed or added to:** no single actor may hold both Business Approval Authority and Infrastructure Allocation Authority for the same Tenant establishment request; Infrastructure Allocation Authority's decision is strictly gated on a valid, referenced Business Approval decision; neither authority may perform Technical Provisioning. `ADR-026`'s own Approval ≠ Allocation ≠ Provisioning framing (`ADR-026 §10`) is the origin of this distinction and remains fully authoritative, unaffected by this Instrument.

---

## 7. Authority Being Constituted

**"Dedicated Infrastructure Allocation Authority"** — the working description used consistently throughout this decision sequence (`ADR-029 §11`/`§16`/`§18` item 2, `ADR-030 §15`, `ADR-031 §10`/`§14`, `ADR-032 §14`, `ADR-033 §11`, `ROD-C040-Dedicated-Tenant-Authority-Model-Selection.md §2`/`§30`/`§74`). Verified directly in this task: `ROD-C040-Dedicated-Tenant-Authority-Model-Selection.md §74` states explicitly that neither "Dedicated Tenant Establishment Business Governance Authority" nor "Dedicated Infrastructure Allocation Authority" is canonized as a proper name by that record. This Instrument does not purport to canonize this description as a proper name either — it is used here only as the identifying label the rest of this decision sequence, and `AI-001` itself, already uses, following the same discipline `AI-001 §7` applied to its own, separate authority.

---

## 8. Four-Condition Independence Attestation

Determinations reached independently by this Appointer, from direct primary-source reading in this task, not inherited from `AI-001`'s own analogous findings:

1. **No prior involvement in Canonization** — satisfied. This Appointer's context began with this task's own assigning prompt; it did not draft `ADR-029` (or any ADR in the `ADR-024`–`ADR-033` chain), and had no role in the four decision-support briefs `ADR-029 §8` cites as its own evidentiary basis for §11 specifically (`ROD-C040-Infrastructure-Allocation-Authority-Resolution.md`, `ROD-C040-Infrastructure-Allocation-Authority-Definition.md`).

2. **Not a prospective member of the authority** — satisfied. This Instrument's own act is limited to appointment/constitution; this Appointer is not named as, and does not become, the accountability point, executor, or any member of the Infrastructure Allocation Authority (§10 below leaves the accountability point entirely unpopulated).

3. **No circular appointment dependency** — satisfied, reasoned through directly rather than assumed either way, as this Instrument's own governing task required. Two distinct questions were considered:

   (a) *Does this authority have any evidenced role in appointing its own future Key-2 appointers?* No — `ADR-029 §11` grants the Infrastructure Allocation Authority only the allocation function itself (§6 above); nothing in `ADR-029`, `ADR-030`, `ADR-031`, `ADR-032`, or `ADR-033` gives any constituted C-040 authority a role in selecting or testing its own or the other authority's future Key-2 appointer. No closed loop is created by this act.

   (b) *Does the separation-of-duties rule (`ADR-026 §8` Decision Driver 4; `ADR-029 §12` — "no single actor may hold both Business Approval Authority and Infrastructure Allocation Authority for the same Tenant establishment request") bear on this Appointer's own eligibility, given a different fresh-context agent already performed the analogous Key-2 act for the Business Governance Authority, recorded in `AI-001`?* On direct reading of `ADR-029 §12`, this rule prohibits a single actor from **holding** — i.e., being the constituted accountability point/member of — both authorities for the same Tenant establishment request. It is a constraint on who the two authorities' own future accountability points may be, not a constraint on who may perform the Key-2 populate-the-authority act for each. Neither `AI-001`'s own Appointer nor this Instrument's own Appointer becomes a member, chair, or accountability point of either authority (condition 2, both Instruments) — each performed only the one-level-removed act of constituting the authority as an existing, populated constitutional matter, not the act of holding or exercising either authority's own substantive function. Because neither Appointer holds either authority, `ADR-029 §12`'s own prohibition is not engaged by either appointment, individually or in combination. Independently, the two Appointers are, by `ADR-030 §7`'s own per-case mechanism, separate freshly-engaged instances with no shared continuity, memory, or identity — there is no single actor common to both acts for `ADR-029 §12` to apply to even if its prohibition extended to the Key-2 act itself (which, on the text, it does not). **Condition 3 is satisfied**, on both grounds independently.

4. **Genuine fresh-context substantive independence** — satisfied. This Instrument's own eligibility determination was independently re-derived from primary sources in this task: `ADR-024` through `ADR-033`, `ADR-026`, `AI-001`, `ROD-C040-Business-Authority-Key-2-Fresh-Context-Selection.md`, and `ROD-C040-Dedicated-Tenant-Authority-Model-Selection.md` were each read directly and in full by this Appointer in this task; `ADR-029 §11`'s own text was independently checked against `ADR-032 §6`'s definition of Key-1 completion rather than assumed to mirror `AI-001`'s own finding for `§10`. No conclusion above is adopted from a prior session's own say-so without this Appointer's own direct verification.

A previously-discussed fifth condition, "no direct beneficiary relationship" (`ADR-031 §5`, `ADR-030 §16`), remains explicitly proposed and unresolved in this repository's own governance history — it is not treated as canonical here, consistent with `ADR-031 §5`'s own explicit non-adoption.

---

## 9. Appointment Decision — What This Instrument Actually Does

**This Instrument constitutes the Dedicated Infrastructure Allocation Authority as an existing, populated constitutional authority — it does not itself allocate any Tenant identity, and it does not itself decide, confirm, or reject any allocation request.**

`ADR-029 §11`'s own MAY list defines this authority's *function* once constituted: to allocate the canonical Tenant identity for an approved Tenant establishment request, per `ADR-026`'s Infrastructure Allocation step. **That function is not exercised by this Instrument.** No Tenant establishment request exists, no Business Approval decision has been made (`AI-001` populated the Business Governance Authority but performed no approval — `AI-001 §9`), and no allocation request exists to confirm or reject. This Instrument's own act is one level removed — it is the Key-2 act of populating the authority itself, so that it exists and is capable of exercising the function `ADR-029 §11` already bounded, at a future time, against a future, properly-gated allocation request.

**Consequence:** no Tenant identity is allocated by this Instrument. No Tenant is established, approved, or provisioned. `tenant_registry` is untouched. No Business Activity is authorized. This Instrument's own effect is limited strictly to the existence of the authority named in §7, within the boundaries of §6, populated as recorded in §10.

---

## 10. What Is, and Is Not, Populated by This Instrument

**Populated:** the authority now exists as a constitutional matter, per this Instrument, within the boundaries `ADR-029 §11` already fixed.

**Not populated, not decided, explicitly left open — none of the following is resolved by this Instrument, and none is inferred from anything above:**

- Accountability point — who or what actually holds the Infrastructure Allocation Authority.
- Executor — whether decision and execution are split, and if so, to whom execution is delegated (`ADR-029 §11`'s own MAY list permits delegating technical execution, but does not name a delegate, and this Instrument names none).
- Relationship to `AUREX_ADMIN` beyond what `ADR-029 §13` already states. Verified directly: `ADR-029 §13` addresses both authorities jointly — "This ADR does **not** state that `AUREX_ADMIN` is the Business Approval Authority. This ADR does **not** state that `AUREX_ADMIN` is the Infrastructure Allocation Authority" — and this Instrument does not disturb that, for either authority.
- Technical Provisioning Authority (`ADR-026 §13`, `ADR-029 §11`/`§14`, untouched — remains a separate, entirely undecided authority, expressly prohibited to this authority itself, §6 above).
- Tenant System-of-Record custodianship (`ADR-027`, `ADR-029 §14`, untouched — `ADR-029 §14` expressly states custodianship "is not assumed to travel with either authority").
- Membership structure, quorum, voting, chair, tenure, succession, replacement, or revocation — none of these concepts is evidenced as applicable to this authority's own narrow, single-accountability-point shape (`ADR-031 §10`: "narrower in content — one accountability point rather than multiple members"), and none is invented here.

Each of these remains its own separate, future constitutional or operational decision, exactly as every ADR and ROD in this sequence has consistently preserved them. **This Instrument does not narrow, default, or imply an answer to any of them.**

---

## 11. No New ADR

**No `ADR-034` or any other new ADR is created by this Instrument.** Per `ADR-030 §9` and `ADR-033 §8`, the Appointment Instrument is itself the canonical appointment record — no additional ADR is required to make this specific appointment canonical. `ADR-024` through `ADR-033` are not modified, amended, reopened, or extended by this Instrument in any respect; each remains Accepted exactly as before. `AI-001` is not modified, amended, or reopened by this Instrument.

---

## 12. Effective Date and Status

**2026-08-25** — consistent with every ADR (`ADR-024` through `ADR-033`), `AI-001`, and every ROD in this decision sequence, each dated 2026-08-25, and consistent with this repository's own recorded convention for this decision sequence. This Instrument has no independent means of confirming a calendar date beyond what this repository's own governance documents already record for the surrounding sequence; it adopts that same date rather than asserting a separately-verified one.

**Status: Executed.** This is not a draft or a proposal — the appointment act (§9) is performed by this Instrument's own creation, under the direct authorization recorded in §4.

---

## 13. C-040 Impact

**This Instrument does not change C-040's own implementation-readiness status. C-040 remains RED — Not Implementation Ready.**

The Dedicated Infrastructure Allocation Authority now constitutionally exists and is populated as a matter of Key-2 appointment, but cannot yet act: it has no accountability point resolved (§10), no executor, no relationship to any request-intake mechanism, and no valid Business Approval decision could yet exist for it to gate against even in principle. Technical Provisioning Authority and Tenant System-of-Record custodianship remain unresolved. No code, API, migration, or Business Activity exists to give this authority any operative capability.

**Decision 1 / the Business Governance Authority / `AI-001` is explicitly confirmed untouched by this Instrument.** `AI-001` remains exactly as it left the Business Governance Authority: constitutionally populated, but with no membership, executor, or operative capability resolved. Both authorities now exist as constitutional matters, but neither can yet exercise its function — no Tenant establishment request exists, no Business Approval decision has been made, and no allocation could yet occur even if requested.

---

## 14. Audit / Reference Trail

Documents this appointment relies upon, in full, each read directly by this Appointer in this task:

- `ADR-026_Tenant_Dual_Approval_Allocation_Authority.md` — Approval ≠ Allocation ≠ Provisioning framing (§6, §8 condition 3 above).
- `ADR-029_Tenant_Business_Approval_and_Infrastructure_Allocation_Authority_Architectural_Model.md` — Key-1/Canonization reference (§5, §6 above), specifically `§11`.
- `ADR-030_Stage-3_Founding_Provision_and_Per-Case_Appointment_Mechanism.md` — Two-Key Model, four independence conditions, Appointment Instrument specification.
- `ADR-031_Per-Case_Independent_Key-2_Eligibility.md` — per-case eligibility test, no permanent pool, Technical Authority Application (§10).
- `ADR-032_Key-1_Completion_Triggers_Key-2_Availability.md` — confirms Key-2 availability for this authority once Key 1 (`ADR-029 §11`) is complete.
- `ADR-033_Repository_Owner_Operational_Key-2_Case_Opening.md` — Initiated By basis (§2 above), Appointment Instrument field specification (`Initiated by` / `Appointer` distinction, §8), Infrastructure Authority Application (§11).
- `AI-001_Business_Governance_Authority_Founding_Appointment.md` — the structural pattern this Instrument follows for the separate, first Decision-1 case; independently verified as untouched and unaffected by this Instrument (§13 above).
- `ROD-C040-Dedicated-Tenant-Authority-Model-Selection.md` — naming/working-description basis (§7 above).
- `ROD-C040-Business-Authority-Key-2-Fresh-Context-Selection.md` — the analogous eligibility-determination discipline this Appointer independently re-applied, for a different authority, in this task (§8, §4 above); not treated as dispositive for this authority, only as evidence of the discipline and the "further explicit authorization" requirement.
- The direct human authorization quoted in §4 above, relayed to this Appointer in the conversation that produced this Instrument.

---

## 15. Explicit Non-Decisions

This Instrument does **not**:

- Allocate any Tenant identity, confirm any allocation prerequisite, or reject any allocation request.
- Decide, approve, or reject any Tenant establishment request (that function belongs exclusively to the separate Business Approval Authority, `ADR-029 §10`, `ADR-026`).
- Resolve accountability point, executor, membership structure, quorum, voting method, chair, tenure, succession, replacement, or revocation for the Infrastructure Allocation Authority.
- Establish any relationship to `AUREX_ADMIN` beyond what `ADR-029 §13` already states (none, for either authority).
- Resolve Technical Provisioning Authority (`ADR-026 §13`, `ADR-029 §11`/`§14`).
- Resolve Tenant System-of-Record custodianship (`ADR-027`, `ADR-029 §14`).
- Touch, modify, reopen, or re-appoint anything related to Decision 1, the Business Governance Authority, or `AI-001`.
- Create `ADR-034` or any other new ADR.
- Modify `ADR-024` through `ADR-033`, or `AI-001`.
- Modify `URA-001`, `SD-002`, `RTA-001`, `ARCH-000`, `CMD-001`, or `CLAUDE.md`.
- Adopt, activate, reject, or modify `tenant_registry` — remains DEFERRED.
- Create code, migrations, APIs, or a Business Activity.
- Authorize `WP-16` or any Work Package.
- Establish this Appointer, or any instance of its category, as a standing or continuing Appointment Authority.
- Change C-040's implementation-readiness status — remains RED.

---

## 16. Change Control

**Files created:** this document only — `architecture/07-Decisions/AI-002_Infrastructure_Allocation_Authority_Founding_Appointment.md`.

**Files modified:** none. `ADR-024` through `ADR-033`, `AI-001`, every prior `ROD-*` brief, `URA-001`, `SD-002`, `RTA-001`, `ARCH-000`, `CMD-001`, `CLAUDE.md`, `WP-REG-001`, `WPR-001`, `tenant_registry`, the Authorization Runtime Engine, and `DomainPermission` were all read-only for this task.

**No implementation performed:** no code, migration, API, or Business Activity was created or modified; `WP-16` was not created or authorized; `tenant_registry` was not adopted; Decision 1, the Business Governance Authority, and `AI-001` were not touched. `ADR-024`–`ADR-033` remain Accepted, unchanged. C-040 remains RED — Not Implementation Ready.
