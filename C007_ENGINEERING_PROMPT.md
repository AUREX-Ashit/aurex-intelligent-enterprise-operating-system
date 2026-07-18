We are performing a strictly bounded corrective pass on:

PE-001-C007 — Membership Management

The uploaded PE-001-C007_Membership_Management.docx is the current canonical working document and SHALL be updated in place to produce:

PE-001-C007_Membership_Management_v1.1.docx

This is NOT a redesign, expansion, enrichment or general improvement pass.

The existing architecture has already been reviewed.

The following architectural decisions are FROZEN unless a direct contradiction with the uploaded canonical authority is proven:

C-007 capability identity and business intent
CRB-C007
the existing 6 ERBs
the existing 13 Enterprise Experiences
the existing Experience Lifecycle
the seven-dimension Context Engineering methodology
deterministic Membership recognition
separation of Person, Identity and Membership
separation of Membership from Role, Permission and Access
Membership Terms as the umbrella experience construct covering:
home-node anchor
license type
membership type
effective dates
Term Change Context
Standing Context
Multi-Membership Context
Cross-Tenant Visibility Context
Membership Journey Continuity Context
Hand-off Context
C-006 Person precondition
ERG-001 structural authority
URA-001 Membership authority
explicit downstream capability hand-off semantics

Do NOT introduce new ERBs.

Do NOT introduce new Enterprise Experiences unless the effective-date analysis below proves that the existing EX architecture cannot truthfully engineer the required enterprise experience.

The preferred correction is to strengthen the existing ERB and EX architecture.

Do NOT perform stylistic rewriting.

Do NOT add explanatory material merely to make the document longer.

Do NOT add implementation architecture, APIs, services, database tables, events, screens, workflow engines or state-machine design.

Do NOT create local canonical concepts, identifiers, lifecycle policies or governance authorities.

Your task is to correct ONLY the following three defects.

CORRECTION 1 — ENGINEER THE EFFECTIVE-DATE EXPIRY CONSEQUENCE

Canonical authority:

URA-001-21 establishes that Memberships support effective dates and that expired Memberships automatically lose authority.

The current C-007 architecture includes effective dates within Membership Terms but does not explicitly engineer the enterprise-experience consequence of an active Membership reaching its effective end date.

Correct this gap.

You SHALL determine how the existing C-007 architecture represents the following condition:

A Membership may remain recorded with an ACTIVE standing while its effective validity period has ended.

The passage of the effective end date SHALL NOT be silently treated as a human-requested standing transition.

The architecture SHALL explicitly distinguish:

Membership standing
Membership effective validity
authority consequence arising from expiry

C-007 SHALL NOT redefine Access Management or Role & Permission Management.

C-007 SHALL NOT itself grant or revoke access.

C-007 SHALL engineer the Membership-context consequence of expiry and the context made available to downstream capabilities.

Review and strengthen, where required:

Experience Principles
Capability Boundary
Experience Context Model
Experience Lifecycle
ERB-C007-03 — Maintain Membership Terms
ERB-C007-04 — Govern Membership Lifecycle
relevant EX definitions
Experience Contracts
Enterprise Transitions
Exception & Recovery Semantics
Cross-Capability Hand-offs
Traceability Matrix
Experience Architecture Invariants
Context State Authority Matrix
Appendices and Publication Conformance Checklist

Preferred architectural treatment:

Use the existing ERB/EX architecture if it can represent expiry truthfully and completely.

Do NOT create a new EX merely because expiry is a new condition being documented.

Create an additional EX only if you can demonstrate that expiry has:

a genuinely distinct enterprise trigger,
a genuinely distinct business objective,
a distinct context-engineering outcome,
and cannot be truthfully governed by an existing EX.

If no new EX is required, preserve the existing total of 13 EXs and update all affected architecture consistently.

The corrected architecture SHALL make explicit that an expired Membership cannot be represented to downstream capabilities as currently effective merely because its standing remains ACTIVE.

CORRECTION 2 — REMOVE INVENTED REACTIVATION AND LIFECYCLE POLICY SEMANTICS

The current C-007 document implies that suspended, deactivated or archived Memberships may route generally to reactivation.

It also introduces language such as:

“tenant-configured policy”

and

“deterministic permitted-transition semantics”

for Membership standing transitions.

The supplied canonical authority establishes Membership lifecycle states but does not establish a canonical tenant-configurable lifecycle transition policy or a universal transition matrix proving that every non-active standing may directly transition to ACTIVE.

Correct this.

C-007 SHALL NOT invent a Membership lifecycle transition matrix.

C-007 SHALL NOT invent a tenant-configured lifecycle policy unless such authority is explicitly present in the uploaded canonical specifications.

Reactivation SHALL be expressed only as follows in architectural meaning:

A transition to ACTIVE may occur only where the governing Membership lifecycle authority permits transition from the Membership's current standing to ACTIVE.

Do NOT assert that:

every suspended Membership can always reactivate,
every deactivated Membership can always reactivate,
every archived Membership can directly reactivate.

Where the canonical authority does not define the permitted transition matrix, use explicit Pending Canonical Binding or equivalent canonical-boundary language.

Preserve EX-C007-08 — Reactivate Membership if possible.

Its purpose SHALL remain prevention of duplicate Membership establishment where an existing non-active Membership already governs the Person-Organization pair.

However, EX-C007-08 SHALL NOT itself define which source standings are permitted to reactivate.

If transition to ACTIVE is not permitted by the governing lifecycle authority, the experience SHALL preserve the existing Membership context and return an explicit unresolved or rejected transition outcome.

Update all affected references consistently, including:

ERB-C007-01
ERB-C007-04
EX-C007-01
EX-C007-07
EX-C007-08
Experience Flow descriptions
Enterprise Decisions
Context Engineering
Enterprise Transitions
Exception & Recovery Semantics
Experience Contracts
Experience Decision Record
Traceability Matrix
Architecture Invariants
Publication Conformance Checklist

Remove or correct every unsupported occurrence of:

tenant-configured lifecycle policy
universal reactivation assumptions
deterministic permitted-transition semantics where no canonical transition authority exists

Do not replace them with another invented policy.

CORRECTION 3 — RESTORE THE EXACT C-004 / C-005 / ERG-001 AUTHORITY BOUNDARY

The current document correctly states in some places that:

C-004 owns Organization Management
C-005 owns Enterprise Structure Management
ERG-001 owns enterprise structure and relationship semantics

However, other sections use wording such as:

“valid Organization governed by C-004/C-005”

or route unavailable Organization context interchangeably to Organization Management or Enterprise Structure Management.

This is architecturally imprecise.

Correct the authority boundary throughout the complete document.

The canonical boundary SHALL be:

C-004 — Organization Management
Authority for Organization existence, Organization identity and Organization validity as an enterprise entity.

C-005 — Enterprise Structure Management
Experience capability governing the enterprise structure in which organizational and enterprise nodes participate.

ERG-001 — Enterprise Structure & Relationship Management
Canonical structural and relationship semantics, including Enterprise Node and home-node structural context.

C-007 — Membership Management
Consumes:

an Authoritative Person Context from C-006
a valid Organization Context from C-004
home-node and structural validation context from C-005 / ERG-001

C-007 SHALL NOT treat C-005 as an alternative authority for Organization existence or Organization validity.

The following distinctions SHALL be explicit:

Organization unavailable or invalid
→ route to C-004 — Organization Management.

Enterprise structural context unavailable, home-node candidate unavailable, or structural congruence cannot be validated
→ route to C-005 / ERG-001 governed structural context.

Membership context unavailable or unresolved
→ remain within or route back to C-007 as appropriate.

Correct this boundary everywhere it appears, including:

Capability Boundary
Out of Scope
Entry Context
ERB-C007-01
EX-C007-01
EX-C007-02
Membership Context Contract
Membership Terms & Home-Node Contract
Exception & Recovery Semantics
Cross-Capability Hand-offs
Dependencies
Traceability Matrix
Architecture Invariants
Appendices
Publication Conformance Checklist

Do not modify C-004, C-005 or ERG-001.

This pass corrects only C-007's references to their authority.

MANDATORY VALIDATION AFTER CORRECTION

After applying the three corrections, perform a complete document consistency scan.

Validate specifically that:

The document still contains exactly 6 ERBs unless a canonical contradiction is discovered.
The document still contains exactly 13 EXs unless Correction 1 proves a new EX architecturally unavoidable.
Every EX has exactly one governing ERB.
Every ERB has at least one realizing EX.
Effective-date expiry is explicitly engineered.
Membership standing and effective validity remain distinct.
Expiry does not silently become a human standing transition.
An expired Membership is not represented downstream as currently effective merely because standing is ACTIVE.
C-007 does not grant or revoke Access.
C-007 does not assign or remove Roles or Permissions.
EX-C007-08 does not invent permitted source standings for reactivation.
No unsupported tenant-configured Membership lifecycle transition policy remains.
No universal reactivation assumption remains.
Organization existence and validity authority resolve exclusively to C-004.
Home-node and structural validation resolve to C-005 / ERG-001.
C-005 is never presented as an alternative Organization authority.
The seven Context Engineering dimensions remain explicit for every ERB and EX.
Created remains distinguished from Produced.
Superseded remains distinguished from Invalidated.
Traceability remains internally consistent.
Appendix A counts are correct.
Appendix B ERB-to-EX mapping is correct.
Appendix C Publication Conformance Checklist reflects the corrected architecture.
No new local Business Activity identifiers are invented.
No new local EIO identifiers are invented.
No new Enterprise Journey identifiers are invented.
No implementation architecture has been introduced.

OUTPUT REQUIREMENT

Update the uploaded Word document directly.

Produce:

PE-001-C007_Membership_Management_v1.1.docx

Return the complete updated Microsoft Word document.

Do not return a replacement architecture in chat.

Do not provide chapter-by-chapter commentary.

Do not provide a general critique.

After the document is generated, provide only:

the downloadable PE-001-C007_Membership_Management_v1.1.docx
a concise correction summary listing the three corrected defects
confirmation of the final ERB count
confirmation of the final EX count
confirmation whether a new EX was required for effective-date expiry

This is a bounded corrective pass.

Do not modify anything outside the three stated defects except where a dependent sentence, table, traceability entry, count or conformance statement must change to maintain internal consistency.