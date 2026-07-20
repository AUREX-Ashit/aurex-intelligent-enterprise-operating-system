# COM-001: Commercial & Subscription Architecture

### Version 1.0 — Constitutional Baseline (New)

**Status:** LOCKED — certified by EARB under Constitutional Recertification CR-3.0 (Enterprise Operating System Constitutional Architecture Baseline v2.0)
**Classification:** Enterprise Constitutional Architecture (Layer 1, per ARCH-000)
**Scope:** Defines the business semantics of the Commercial & Subscription domain (CAP-001 D-002): what a Subscription, an Offering, a Customer, a Commercial Account, a Billing Arrangement, and a Commercial Contract are, and the rules governing them. It does not define Identity, Membership, Organization, Workspace, Access, Entitlement, Evidence, Enterprise Intelligence, runtime execution, or physical implementation — each remains owned by its own canonical specification and is consumed here strictly as an already-resolved input.
**Primary Specification For:** D-002 Commercial & Subscription (CAP-001) — Capabilities C-020, C-021, C-022, C-024, C-025.
**Companion documents:** ARCH-000 v1.6, CAP-001 v1.5, CMD-001 v1.3, SD-002 v2.2, SD-003 v2.0, URA-001 v2.1, RTA-001 v1.0, EIA-001 v1.0 — all locked or current.

---

## Authoring Note (ARP-001 WP-1A)

This document is an extraction and constitutional formalization exercise, not new business invention, per the WP-1A Mandatory Authoring Rules. Every business concept defined below — Subscription, Offering Definition, Customer, Commercial Account, Customer–Account Relationship, Billing Arrangement, Billing Period, Billing Standing — already exists, fully engineered, in the four Active PE-001-Cxxx Experience specifications (PE-001-C020 v1.1, PE-001-C021 v1.1, PE-001-C022 v1.2, PE-001-C024 v1.1), each of which originated this content independently because no Constitutional-layer document existed to define it first (the exact condition Stage I's certification identified and this document resolves). This document consolidates that already-engineered content into Constitutional-layer form, in the register SD-002 and URA-001 already use, and becomes the Primary Specification those four documents' own "Primary Specification Reference" fields already point to. Contract (C-025) has no PE-001-Cxxx specification to extract from (confirmed: `docs/Product/PE-001/capabilities/C-025` does not exist) and no capability-level content beyond CAP-001's own registered business intent ("Manage commercial contracts") and the "contract reference" / "contractual dependency reference" consumed-by-others pattern the other four specifications already establish. §7 below is accordingly foundational rather than fully engineered, and records what remains open as Pending Canonical Binding rather than inventing it.

Where this document's numbered principles restate content from PE-001-C020/021/022/024, that restatement is the intended, certified purpose of this document — those four specifications' own "Primary Specification Reference" fields already named SD-001/URA-001 as placeholders precisely because COM-001 did not yet exist; this document is that missing reference now supplied.

---

## 1. Purpose

COM-001 establishes the Commercial & Subscription domain's canonical business semantics: what a commercial commitment is, what is being commercially offered, who the enterprise's commercial counterparties are, what is owed for a commercial commitment over time, and what governs the commercial terms between the enterprise and a customer. It is the Primary Specification CAP-001 designates for C-020 (Subscription Management), C-021 (Product & Service Catalog), C-022 (Customer & Account Management), C-024 (Billing Management), and C-025 (Contract Management).

## 2. Domain Ownership & Explicit Boundaries

COM-001 owns the business semantics of Subscription, Offering Definition, Customer, Commercial Account, Customer–Account Relationship, Billing Arrangement, Billing Period, and Billing Standing. It does not own, and explicitly defers to:

- **URA-001** — Identity, Membership, Organization boundary, Licensing & Entitlement (C-023 remains correctly owned by URA-001 §8; this document does not redefine License, Entitlement, or the Membership-keyed authority URA-001-111/116 establish).
- **SD-002** — the Universal Business Object Model every construct below inherits (Universal Identity, Evidence, Lifecycle, Audit), and the Business Activity Rules every commercial action conforms to.
- **CMD-001** — the canonical data/registry mechanism (CBOR, BAR) through which every construct below is catalogued once implemented; this document defines what these objects and activities *are*, never their physical schema.
- **SD-003** — the interaction laws (approval, review, notification) governing how a commercial decision is routed and confirmed.
- **RTA-001** — the runtime execution of every transition described below; this document defines the business rule, never the execution mechanism.
- **EIA-001** — Enterprise Intelligence; a commercial fact may be a Source or Signal for Enterprise Discovery, but COM-001 does not define Enterprise Intelligence semantics.
- **A future Order/Fulfillment authority** — not yet identified anywhere in the canonical baseline; physical delivery, logistics, invoicing, payment, and accounting/revenue recognition remain explicitly out of scope, recorded Pending Canonical Binding, not invented here (consistent with PE-001-C024 v1.1's own recorded boundary).

## 3. Canonical Enterprise Hierarchy Position

Per CMD-001 §3.3 (as clarified by CMD-001 §3.1's CERT-023 note): CAP-001 remains the sole authority for Commercial & Subscription's capability and domain identity (D-002, C-020/021/022/024/025). COM-001 defines the business semantics within that already-identified domain; it does not redefine domain or capability identity.

---

## SECTION 4: Universal Commercial Construct Model

*(Every construct in Sections 5–9 inherits this section in full, mirroring SD-002 §2's inheritance discipline. Sections 5–9 state only what is distinctive to each construct.)*

**COM-001-001: Universal Identity**
Every commercial object possesses a globally unique, permanent identity in `PREFIX-NNNNNN` form, per SD-002-004, alongside a canonical name and version. Business labels may vary by tenant; canonical identity never does.

**COM-001-002: Anchor / Authoritative / Resulting Is the Universal Commercial Lifecycle Pattern**
Every commercial construct below distinguishes three roles, never conflated: an **Anchor Context** (experience-scoped, non-authoritative, resolves which candidate object an action concerns), an **Authoritative Context** (the single current, canonical fact — exactly one per anchor at any time, produced and superseded only through a committed transition), and a **Resulting Context** (the commit-produced transition outcome, which immediately assumes Authoritative status for its anchor; the superseded Authoritative Context is retained in lineage as historically valid for its own effective period, never discarded). No Anchor Context is itself authoritative. No two Authoritative Contexts exist concurrently for the same anchor.

**COM-001-003: Intent Precedes Proposal**
Every commercial action states its business reason and target outcome (an Intent Context) before any candidate change (a Proposed Context) is shaped. A Proposed Context is never authoritative and carries the Intent Context that motivated it.

**COM-001-004: Advisory Assessment Is Never Authoritative**
Every commercial construct's cross-capability impact (an Assessment Context — entitlement impact, billing impact, contractual dependency, or equivalent) is advisory and explainable; it is never treated as a decision or as another capability's authoritative state.

**COM-001-005: Registration Precedes Implementation**
Per CMD-001 §26.3, no persistent commercial Business Object shall be implemented until registered in the CBOR. No commercial Business Activity shall be executed until registered in the BAR (IMP-001 §6.22), per SD-002-004/034's WP-3 formalization.

**COM-001-006: Non-Authority Across Domains**
No construct defined in this document substitutes for Identity, Membership, Organization, Access, Role, Permission, Entitlement, or Evidence. A commercial fact is never treated as authorizing an action; authorization remains exclusively URA-001/RTA-001 §11's concern.

---

## SECTION 5: Subscription (C-020)

**COM-001-010: Subscription Defined**
A Subscription is the enterprise's canonical record of what a Customer or Commercial Account currently subscribes to: subscription identity, a referenced Offering Definition, a referenced subscriber (Customer or Commercial Account), an effective term, and a current standing (e.g., active, proposed-only, terminated).

**COM-001-011: Subscription Anchor Context**
The resolved reference pair — a subscriber/account reference (Section 7) and an Offering reference (Section 6) — establishing which commercial relationship a Subscription action concerns. Non-authoritative; consumed, never recomputed, from the Customer/Account and Offering constructs it references.

**COM-001-012: Authoritative Subscription Context**
Exactly one exists per Subscription Anchor Context at any time, per COM-001-002. Produced and superseded only through a committed Subscription transition.

**COM-001-013: Subscription Intent, Proposal, and Consequence**
A Subscription Intent Context (establish, change, renew, or terminate) precedes a Proposed Subscription Change Context (target Offering reference, term, commercial parameters). A Subscription Consequence Assessment Context carries advisory references to downstream impact — entitlement (C-023), billing (C-024), contractual dependency (C-025) — per COM-001-004.

**COM-001-014: Subscription Hand-off**
A committed Subscription transition's outcome (Resulting Subscription Context) is preserved, with hand-off reason, for consumption by Licensing & Entitlement (C-023) and Billing (C-024). Subscription never manufactures those capabilities' outcomes; a downstream rejection returns a signal, never an override of Subscription validity, unless the destination canonically owns the rejected fact.

**COM-001-015: Subscription Non-Authority**
A Subscription's standing is never treated as a substitute for Entitlement, Access, Role, or Permission (URA-001 remains authoritative for all four).

---

## SECTION 6: Offering Definition, Product & Service Catalog (C-021)

**COM-001-020: Offering Definition Defined**
An Offering Definition is the authoritative business description of what may be commercially offered: identity, category, composition, key attributes (including a list-price reference where applicable), and current offering state (draft, published/orderable, retired). An Offering Definition never itself constitutes a commercial transaction, a Subscription, or an operational delivery.

**COM-001-021: Product and Service**
A Product is an Offering Definition whose value is realized primarily through a defined, standalone deliverable unit. A Service is an Offering Definition whose value is realized primarily through enterprise activity performed on a customer's behalf. A Digital Offering and a Physical Offering are Offering Definitions distinguished by delivery means; delivery, fulfillment, and logistics remain owned by whichever operational capability realizes them — none redefined here, and, where no such capability is yet canonically identified, recorded Pending Canonical Binding.

**COM-001-022: Offering Composition**
An Atomic Offering has no constituent offering references. A Composite Offering is composed of two or more constituent Offering References. A Bundle is a Composite Offering whose constituents are defined to be offered together as one referenceable unit. A Package is a named, stable configuration of a Bundle's constituents. A Variant shares a common base identity with another Offering but differs in a defined attribute (size, tier, region); an Edition is a Variant distinguished by capability tier. An Optional Component is a non-mandatory constituent of a Composite Offering; an Add-on extends an Offering without being one of its constituents. Composition is a catalog-definitional fact; it is never itself a commercial commitment, which remains Subscription's (C-020) concern, nor a price, which remains Billing's (C-024) concern.

**COM-001-023: Offering Relationships**
Offering Definitions carry named catalog-fact relationships — replaces/superseded-by, successor/predecessor, depends-on, bundled-with, optional-with, mutually-exclusive, complementary — recorded as facts only. Evaluating or enforcing a relationship at the moment of a customer commitment remains Subscription's (C-020) concern, consuming the relationship by reference.

**COM-001-024: Catalog Taxonomy**
A Category is a business-meaningful grouping of Offering Definitions; a Subcategory refines a Category. An Offering may belong to more than one Category where its business meaning genuinely spans both. Where no canonical enterprise taxonomy authority exists, Category alignment is Pending Canonical Binding, not invented here.

**COM-001-025: Offering Version Management**
The Current Definition is the Authoritative Offering Definition Context's present state. A Future Definition is a Proposed Offering Definition Context scheduled for a future Effective Date. A Historical Definition is a superseded Authoritative Offering Definition Context, retained in lineage. Retirement is a terminal transition to Historical status, never a deletion.

**COM-001-026: Publication Is Not Availability**
Definition (what the offering is), Approval (a fitness-to-publish decision, where a canonical approval authority exists — otherwise Pending Canonical Binding), Publication (the catalog-state transition making a definition referenceable), and Availability (whether a specific customer may currently commit against it) are four distinct concepts. Publishing an Offering changes its referenceability; it never asserts commercial availability to any given customer — that determination is made by the consuming capability (typically C-020), never by this section.

---

## SECTION 7: Customer & Commercial Account (C-022)

**COM-001-030: Three Independent Authorities**
Because a single Customer may be organized through one or more Commercial Accounts, and a single Commercial Account may associate with more than one Customer, Customer authority, Commercial Account authority, and the Customer–Account association are three independently keyed authoritative concerns. None is a combined anchor; none is duplicated merely because a Customer participates in more than one Account or an Account associates with more than one Customer.

**COM-001-031: Commercial Party Anchor Context**
A strictly non-authoritative, experience-scoped resolution context identifying which candidate Customer Anchor, Commercial Account Anchor, or pair a commercial-party action concerns. For a proposed new commercial party, it anchors the establishment thread only and asserts explicitly that no Authoritative Customer Context or Authoritative Account Context yet exists — it never itself creates one.

**COM-001-032: Authoritative Customer Context**
The single current, canonical identity fact for a Customer: legal-entity or person identity reference, classification, and status. Keyed only to its own Customer Anchor; exactly one per anchor.

**COM-001-033: Authoritative Account Context**
The single current, canonical commercial-container fact for a Commercial Account: identity, Account-to-Account hierarchy position, and status. Keyed only to its own Commercial Account Anchor. Never equivalent to a Workspace, Organization, Identity, Membership, or Billing Account.

**COM-001-034: Authoritative Customer–Account Relationship Context**
The single current, canonical fact of the commercial association between one Customer Anchor and one Commercial Account Anchor. Keyed to that specific pair. Never duplicates or redefines Customer authority or Account authority; never redefines C-004 Organization, C-006 Person, Subscription, Entitlement, Billing, Contract, Identity, or Access semantics.

**COM-001-035: Independent Promotion**
A committed Customer-authority, Account-authority, or Relationship-authority transition promotes only the specific concern(s) it actually changed — never an undifferentiated combined promotion. A Relationship-authority commit never alters Customer or Account authority unless the same accepted proposal independently changed it.

**COM-001-036: Commercial Reference Distribution**
The stable Customer Reference, Commercial Account Reference, and/or Customer–Account Relationship Reference, plus Account hierarchy and status, are made available for consumption by Subscription (C-020), Product & Service Catalog (C-021, conditional segment reference), Licensing & Entitlement (C-023), Billing (C-024), and Contract (C-025).

---

## SECTION 8: Billing (C-024)

**COM-001-040: Three Independent Billing Authorities**
A Billing Arrangement's configuration, a specific Billing Period's temporal boundary, and a specific Period's Billing Standing are three independently keyed authoritative concerns, applying the same discipline as Section 7 independently to Billing's own shape.

**COM-001-041: Authoritative Billing Arrangement Context**
The single current, canonical configuration fact for a Billing Arrangement: Bill-To Designation, billing cycle/frequency, currency reference, and status. Never equivalent to a Commercial Account, a Subscription, or an ERP billing master record.

**COM-001-042: Authoritative Billing Period Context**
The single current, canonical temporal-boundary fact for one billing cycle instance: start, end, sequence, status (open, closed, corrected). Keyed to a Billing Arrangement Anchor / Period Sequence pair.

**COM-001-043: Authoritative Billing Standing Context**
The single current, canonical "what is owed" fact for a specific Billing Arrangement and Billing Period. Never duplicates Arrangement or Period authority; never redefines Subscription, Catalog/Pricing, Customer/Account, Entitlement, or Contract semantics; never equivalent to an Invoice, a Payment Standing, or a Ledger entry.

**COM-001-044: Bill-To Designation Is Derived, Not Independent**
Bill-To Designation is an attribute of the Authoritative Billing Arrangement Context, determined by consuming Customer, Commercial Account, and Relationship/hierarchy facts produced by Section 7, applying any canonical billing-responsibility governance where one exists (otherwise Pending Canonical Binding). It is not an independently authoritative construct.

**COM-001-045: Billing Excludes Invoice, Payment, and Accounting**
Billing determines what is currently owed for a Billing Arrangement over a Billing Period. It deliberately excludes Invoice generation, Payment processing, and Accounting/Revenue Recognition, none of which is canonically established as any capability's authority in the current CAP-001 registry. The Billing Reference Distribution Context is made available for consumption by capabilities not yet canonically identified that may in future own these concerns — Pending Canonical Binding, not invented here.

**COM-001-046: Billing Source Facts**
An initial Billing Standing determination consumes, as advisory source facts: an active Subscription commitment-standing reference (C-020), a price reference (C-021), a Customer/Account/Relationship reference (C-022), an Entitlement reference where canonically established (C-023), and a Contract reference where canonically established (C-025). None of these source facts is itself authoritative for Billing; Billing's own commit alone produces the authoritative Standing.

---

## SECTION 9: Commercial Contract (C-025)

*(Foundational only — see the Authoring Note. No PE-001-Cxxx specification exists to extract from; this section states what CAP-001 and the other four sections' own cross-references already establish, and nothing beyond that.)*

**COM-001-050: Contract Defined**
A Commercial Contract is the enterprise's canonical record of negotiated commercial terms between the enterprise and a Customer or Commercial Account, referenced by Subscription (C-020), Offering (C-021), and Billing (C-024) as a "contractual dependency" or "contract reference" where one exists for a given commercial commitment.

**COM-001-051: Contract Non-Authority**
A Contract reference consumed by another Commercial & Subscription construct is advisory and explainable, per COM-001-004; it is never treated as itself authoritative for Subscription standing, Offering availability, or Billing Standing unless this section's own governed transition has produced it.

**COM-001-052: Contract Scope Reserved**
The internal structure of a Commercial Contract — clause model, term negotiation lifecycle, contracted billing schedule or rate override authority referenced by COM-001-046, and renewal/amendment mechanics — is not engineered by this baseline. It is recorded Pending Canonical Binding, consistent with CAP-001's "Planned" status for C-025, and is not invented here. A future capability-level specification for C-025 is expected to conform to this section rather than restate it, per the same discipline PE-001-C020/021/022/024 already apply to their own capability-level specifications.

---

## SECTION 10: Cross-Document Integration

**COM-001-060: BAR Integration**
Every commercial action described in Sections 5–9 (establish, change, renew, terminate, define, revise, publish, retire, reclassify, merge, split, relate, transfer, determine, adjust, reverse) is a Business Activity per SD-002 §5, registered in the Business Activity Registry (IMP-001 §6.22) once implemented, per COM-001-005.

**COM-001-061: CBOR Integration**
Every construct in Sections 5–9 (Subscription, Offering Definition, Customer, Commercial Account, Customer–Account Relationship, Billing Arrangement, Billing Period, Billing Standing, Contract) is a Business Object per SD-002 §2, registered in the Canonical Business Object Register (CMD-001 §26) once implemented, per COM-001-005. Each becomes an Enterprise Information Object (CMD-001 §26.4b) upon that registration.

**COM-001-062: Identity, Organization, and Membership**
No construct in this document redefines Person, Identity, Membership, or Organization (URA-001, ERG-001). A Customer that is itself an enterprise Organization, or a Customer contact that is a Person, is consumed by reference from those documents, never re-derived here.

**COM-001-063: Evidence**
Every commercial fact governed by this document is capable of carrying Evidence per SD-002 §6; this document does not restate SD-002's Evidence rules, only confirms they apply.

**COM-001-064: Enterprise Intelligence**
A committed commercial fact (a new Subscription, a published Offering, a Billing Standing) may serve as a Source or Signal for Enterprise Discovery (EIA-001 Vol. II Ch.3), consumed there by reference; this document does not define Enterprise Intelligence semantics.

**COM-001-065: AI Governance**
Any AI-assisted commercial observation, consequence reference, or recommendation is subject to ARCH-000 §7c's Governance Ownership Map in full — evidence-first, human-approved where the action requires it (SD-003 §6), and never itself authoritative, per ARCH-000 Principle 12.

---

## Full Principle Index

| ID Range | Section |
|---|---|
| COM-001-001 – 006 | Section 4 — Universal Commercial Construct Model |
| COM-001-010 – 015 | Section 5 — Subscription (C-020) |
| COM-001-020 – 026 | Section 6 — Offering Definition, Product & Service Catalog (C-021) |
| COM-001-030 – 036 | Section 7 — Customer & Commercial Account (C-022) |
| COM-001-040 – 046 | Section 8 — Billing (C-024) |
| COM-001-050 – 052 | Section 9 — Commercial Contract (C-025) |
| COM-001-060 – 065 | Section 10 — Cross-Document Integration |

## Freeze Statement

This document was submitted in Draft status for EARB constitutional certification per ARCH-000 §12.4 and §12.6, and is certified LOCKED under Constitutional Recertification CR-3.0. Its Version remains 1.0. CAP-001's Primary Specification for C-020, C-021, C-022, C-024, and C-025 now references COM-001 with full eligibility per ARCH-000 §12.7(1), per WP-1A's completion and this certification.

---

# End of Document

**Document ID:** COM-001
**Document Name:** Commercial & Subscription Architecture
**Status:** LOCKED — Certified (CR-3.0, Constitutional Baseline v2.0)
