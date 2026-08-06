# ADR-020 — AI Session Management: Conversation and Interaction Constitutional Foundation

**Status:** Accepted
**Classification:** Architecture Governance / Runtime Architecture Extension
**Decided by:** Repository owner (architecture governance authority), through a Repository Owner Constitutional Design Workshop conducted 2026-08-07 — five concepts, each presented with alternatives and approved individually, following the same decision-authority pattern `ADR-006` through `ADR-019` already established. **Disclosure:** the workshop's discovery, ownership-resolution, concept-discovery, governance-validation, compatibility-validation, and migration-planning passes preceding this ADR were conducted in the same session as this ADR's own authoring and were not independently reviewed by a party uninvolved in producing them, unlike the fresh-context reviewer discipline `CLAUDE.md §19.7` requires for Work Package certification. This ADR is the first and only artifact from that process persisted to the repository — no intermediate discovery/validation document exists as a separate repository file.
**Affected Documents:** None edited by this ADR. This ADR records five constitutional decisions and directs, but does not itself perform, a future amendment pass to `RTA-001` (primary), `ARCH-000 §7c`, `CMD-001 §24`, and `SD-002` (cross-reference only) — per the separately-approved ADR Design and Constitutional Migration Plan. `IMP-001`, `SER-001`, and `WP-REG-001` are unaffected by this ADR.
**Affected Code:** None. This ADR is constitutional and implementation-neutral; it authorizes no code, API, schema, or engineering pattern.

---

## 1. Context

The AI-Native Work Package Implementation Readiness Review (session pass preceding this ADR) found that Release D's own named capabilities — `C-094` AI Conversation Management chief among them — require sustained, multi-turn AI interaction, and that no constitutional concept in this repository describes continuity across more than one AI Request Lifecycle (`RTA-001 §13.6`) or Agent Execution Lifecycle (`§13.6a`) instance. A subsequent Constitutional Ownership Audit confirmed this precisely: `CAP-001` already registers `C-094` (Planned, `EIA-001`-owned) and `CMD-001 §24.4` already names "AI Conversation" as a canonical Business Object (Transaction Data), but neither document, nor `RTA-001`, defines Session Identity, Session Boundary, a System of Record, Interaction State continuity, or cross-Interaction Agent Handoff. `RTA-001 §15.7`'s own Cache Ownership table independently corroborates the gap: it assigns a Source of Truth to every cache type it names except **Session Cache** (`§15.5`), an omission the table itself discloses rather than resolves.

A Constitutional Ownership Resolution evaluated `C-094`, `CMD-001`, `RTA-001`, `SER-001`, existing Runtime Components, and `URA-001` as candidate owners against architectural fit, responsibility alignment, dependency impact, separation of concerns, and repository consistency, and found `RTA-001` the correct constitutional owner — its own Purpose statement (`§13.1`) already names "lifecycle management of Artificial Intelligence capabilities" directly, and it already carries the two nearest structural analogues (`§13.6`, `§13.6a`) plus the disclosed, unassigned Session Cache placeholder.

A Constitutional Concept Discovery then reduced the ownership gap to a minimum, non-redundant set of five concepts, consolidating fifteen originally-named responsibilities. A Repository Owner Constitutional Design Workshop worked through each concept individually — alternatives presented, trade-offs evaluated, one decision approved before the next concept began. A Constitutional Compatibility Validation checked all five approved decisions against `ARCH-000`, `CAP-001`, `CMD-001`, `RTA-001`, `SD-001`, `SD-002`, `URA-001`, `SER-001`, `IMP-001`, and `CLAUDE.md`, finding zero conflicts and four resolvable clarifications. This ADR records the five decisions and resolves those four clarifications.

## 2. Problem Statement

No constitutional concept in this repository describes: (a) a stable identity for a sustained AI exchange distinct from a single bounded execution; (b) when such an exchange begins or ends; (c) where its state durably lives; (d) what carries forward from one execution to the next within it; or (e) how execution responsibility may transfer across executions within it. Without these five concepts, `C-094` and any future Release D capability requiring sustained interaction cannot be constitutionally grounded, and any attempt to engineer against them (as the declined IMP-001 authoring attempt earlier in this process demonstrated) would require inventing them ad hoc, in violation of `CLAUDE.md §17`/`§18`/`§19.4`.

## 3. Repository Owner Decisions

### Decision 1 — Session / Conversation Identity

The constitutional model distinguishes **Conversation** (durable business context representing a logical AI engagement) from **Interaction** (a discrete runtime execution occurring within a Conversation — one bounded AI Request Lifecycle together with its associated Agent Execution Lifecycle(s), per `§13.6`/`§13.6a`, unmodified). A Conversation may contain zero or more Interactions. Conversation represents business continuity; Interaction represents execution continuity.

### Decision 2 — Session Boundary Definition

The Conversation Boundary is governed by an explicit **Conversation State Model** — a constitutional concern distinct from the mechanisms that trigger transitions within it. Runtime Policies (`§13.10`, including inactivity timeout) and explicit Repository Owner, system, or user actions may each trigger a lifecycle transition; neither defines the state model itself. Interaction termination remains governed exclusively by the existing AI Request Lifecycle and Agent Execution Lifecycle, unmodified.

### Decision 3 — Session System of Record

Conversation and Interaction each possess a canonical System of Record and are durably persisted. Session Cache (`§15.5`) remains an acceleration mechanism only, resolving its state exclusively from the canonical record; cache invalidation never alters that record. `§15.7`'s existing cache-ownership principle is preserved unmodified.

### Decision 4 — Interaction State / Continuity

Interaction State is Conversation-scoped, structured runtime context — never an unbounded transcript — existing solely to preserve continuity between successive Interactions in the same Conversation. It becomes an additional named input to Context Assembly (`§13.7`) for subsequent Interactions. The existing AI Request Lifecycle, Agent Execution Lifecycle, Context Assembly, Prompt Orchestration (`§13.8`), and Reasoning Contract (`§13.9c`) are preserved unmodified; Interaction State supplies additional structured input to them and redefines none of them.

### Decision 5 — Cross-Lifecycle Agent Handoff

A Handoff is the constitutional transfer of execution responsibility between successive Interactions belonging to the same Conversation. It transfers only the structured Interaction State required for the next Interaction — never runtime execution state, and never ownership of the Conversation itself, which remains the durable business context throughout. Handoff generalizes `§13.6e` Capability Delegation's own grant-gated, resolver-mediated mechanism to this new scope without modifying `§13.6e` itself.

## 4. Constitutional Principles

The following principles are recorded as approved, binding constitutional statements:

1. *"A Runtime Policy may trigger a Conversation state transition, but it shall never define the constitutional lifecycle model itself."* Lifecycle governance and transition mechanisms remain architecturally independent. *(Decision 2)*
2. *"A Session Cache accelerates access to Conversation and Interaction state but shall never become the authoritative owner of that state."* Canonical ownership remains independent of runtime acceleration mechanisms. *(Decision 3)*
3. *"Conversation Continuity and Enterprise Memory are distinct constitutional concerns."* Conversation Continuity is Conversation-scoped, exists only while the Conversation remains open, and supports continuity between Interactions. Enterprise Memory is enterprise-scoped, cross-conversation, independently governed, and remains deferred under `C-095` pending a separate Repository Owner decision to lift `ARCH-000 §7c`'s existing deferral. Conversation Continuity shall never depend upon Enterprise Memory; Enterprise Memory shall never become a prerequisite for Conversation Continuity. *(Decision 4)*
4. *"Conversation ownership remains immutable. Execution responsibility may change. Conversation ownership shall never change."* A Handoff transfers execution responsibility; it does not transfer ownership of the Conversation. *(Decision 5)*
5. Handoff may occur only while the Conversation remains Open; shall never cross Conversation boundaries; shall never depend upon Enterprise Memory; and remains subject to existing Runtime authorization, capability resolution, and policy evaluation. *(Decision 5)*

## 5. Clarifications

The Constitutional Compatibility Validation identified four clarifications required before this decision set could be considered complete. Each is resolved below, using only principles already approved in §3–§4 — no new constitutional concept is introduced by this section.

**Clarification 1 — Interaction has no existing `CMD-001` Business Object registration.** Resolved: Interaction is not a new, independent top-level Business Object. "AI Conversation" (`CMD-001 §24.4`, already registered) remains the sole registered Business Object; Interaction is a subordinate record realized within AI Conversation's own future `§24.5` decomposition, mirroring how "AI Recommendation" decomposes into `recommendation` / `recommendation_context` / `recommendation_feedback` / `recommendation_audit`. This follows directly from Decision 1's own framing ("A Conversation may contain zero or more Interactions") and avoids the duplicate-registration risk the Constitutional Compatibility Validation named.

**Clarification 2 — Relationship between Interaction and the existing "Prompt Execution" Business Object (`CMD-001 §24.4`) is undefined.** Resolved: Prompt Execution is the finer-grained record of a single reasoning/model invocation (`§13.9c` Reasoning Contract Execution); Interaction is the coarser-grained record of one complete AI Request Lifecycle/Agent Execution Lifecycle instance, which may itself invoke a Reasoning Engine more than once (`§13.9b`'s own "Multi-LLM delegation within one execution"). An Interaction therefore contains, and is realized partly through, one or more Prompt Execution records — a containment relationship, not a duplicate or competing concept.

**Clarification 3 — Business Activity accountability across a multi-Interaction Conversation is not explicit.** Resolved: accountability remains per-Interaction, unchanged from `§13.2`/`§13.3`. Each Interaction is itself one Business-Activity-invoked AI Request Lifecycle instance; Conversation is a Runtime-side continuity construct only and does not create, replace, or aggregate Business Activity accountability. `§13.2`'s own principle — "Business Activities remain the authoritative mechanism for executing business intent... Business Activities provide accountability" — governs unchanged.

**Clarification 4 — Tenant isolation is not explicitly restated for Conversation/Interaction.** Resolved: Conversation and Interaction are subject, upon realization, to the same unconditional tenant-isolation discipline `SD-002 §13`/`URA-001` already establishes platform-wide, and to `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist, exactly as every other canonical Business Object already is. This is a cross-reference to an existing, unmodified rule, not a new one — consistent with the Migration Plan's own "New Cross Reference Only" classification for `SD-002`.

## 6. Architectural Consequences

- Two new constitutional concepts (Conversation, Interaction) and five principles (§4) now exist within `RTA-001`'s ownership, extending but not modifying `§13.6`, `§13.6a`, `§13.6e`, `§13.7`, `§13.8`, `§13.9c`, `§15.5`, and `§15.7`.
- `RTA-001 §15.7`'s previously-disclosed Session Cache Source-of-Truth omission is now resolvable — the canonical System of Record established by Decision 3 is the answer that row was missing.
- No capability, entity, permission, navigation model, or Business Activity is created, modified, or reassigned by this ADR. `C-094` remains Planned, unchanged.
- `IMP-001 §13.17`'s constitutional-precedes-engineering discipline is satisfied: this ADR supplies the constitutional grounding a future Engineering Specialization pass would require, which did not exist prior to this ADR (the reason an earlier attempt in this same process to author that specialization directly was declined).
- Enterprise Memory (`C-095`) remains wholly unaffected — its own deferral under `ARCH-000 §7c` is neither lifted nor referenced as a dependency by any decision in this ADR (Principle 3, §4).

## 7. Impacted Documents

*(Classification per the ADR Design and Constitutional Migration Plan; none amended by this ADR itself.)*

| Document | Classification | Nature of future amendment |
|---|---|---|
| `RTA-001` | Minor Amendment | New subsections under `§13` recording Decisions 1–5 and Principles 1–5; resolution of the `§15.7` Session Cache row |
| `ARCH-000` | Minor Amendment | One new row in `§7c`'s AI Governance Ownership Map ("Session Governance — Owned"), mirroring the `ARM-001`/`AR-001` precedent |
| `CMD-001` | Minor Amendment | `§24` amended per Clarifications 1–2 — no new Aggregate Root, no Domain restructuring |
| `SD-002` | New Cross Reference Only | A pointer from `RTA-001`'s new text to `§13`'s existing tenant-isolation discipline, per Clarification 4 |
| `SER-001` | Minor Amendment | One new Strategic Enhancement entry, status Deferred, mirroring `SE-024`–`SE-027` |
| `CAP-001` | No Change | `C-094` status and definition untouched |
| `SD-001` | No Change | No overlap with presentation architecture |
| `URA-001` | No Change | Session Ownership already fully owned by the existing tenant-isolation mechanism |
| `IMP-001` | No Change (by this ADR) | A future, separately-authorized Engineering Specialization pass, not performed here |
| `WP-REG-001` | No Change | No Work Package chartered by this ADR |

## 8. Migration Guidance

Per the separately-approved ADR Design and Constitutional Migration Plan, future amendment (not performed by this ADR) should proceed: `RTA-001` first (the primary owner every other document references), then `ARCH-000 §7c` (so its ownership-map citation matches finalized `RTA-001` text), then `CMD-001` and the `SD-002` cross-reference together, then `SER-001`. An `IMP-001` Engineering Specialization pass and any Work Package chartering are explicitly out of this migration's scope and require separate, future Repository Owner authorization — mirroring the two-step chartering-then-authorization precedent `WP-09`/`WP-10`/`WP-11` each already established.

## 9. Deferred Topics

The following are explicitly not decided by this ADR, per the Repository Owner's own instruction at every stage of this process:

- Database schemas, storage engines, physical repositories, persistence technology
- Transcript representation, summarization strategies, context reduction algorithms
- Scheduling, orchestration algorithms, routing, planner implementation, agent selection algorithms
- Execution engines, message protocols, serialization
- APIs, endpoints, request/response contracts
- Any engineering pattern under `IMP-001` (deferred to a future Engineering Specialization pass)
- Enterprise Memory (`C-095`) itself, and the Repository Owner decision to lift its `ARCH-000 §7c` deferral
- Chartering of any Work Package consuming this foundation

## 10. References

- `RTA-001 §13.1`, `§13.2`, `§13.3`, `§13.6`, `§13.6a`, `§13.6b`, `§13.6e`, `§13.7`, `§13.8`, `§13.9b`, `§13.9c`, `§13.10`, `§13.12a`, `§15.5`, `§15.7`, `§22.12`
- `CMD-001 §24.3`–`§24.7` (Knowledge & AI Domain)
- `CAP-001` — `C-094` (AI Conversation Management, Planned)
- `ARCH-000 §7c` (Enterprise Intelligence & AI Governance Ownership Map), `§8` (Architectural Dependency Model)
- `IMP-001 §13.17` (Engineering Specialization Framework)
- `CLAUDE.md §6`, `§8`, `§12`, `§15`, `§17`, `§18`, `§19` (including `§19.7`), `§21.4`
- `ADR-006` through `ADR-019` (decision-authority and Business-Object-registration precedent)
- Repository Owner Constitutional Design Workshop session record, 2026-08-07 — Constitutional Ownership Audit, Constitutional Ownership Resolution, Constitutional Concept Discovery, IMP-001 Engineering Specialization Governance Validation, five-concept Design Workshop, Constitutional Compatibility Validation, ADR Design and Constitutional Migration Plan (not separately persisted as repository documents; this ADR is their sole recorded output)

## 11. Status

**Accepted.**
