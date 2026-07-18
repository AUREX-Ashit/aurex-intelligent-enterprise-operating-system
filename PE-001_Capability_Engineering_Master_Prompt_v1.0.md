# PE-001 Capability Engineering Master Prompt v1.0

> Reusable master prompt for Claude Code / Claude Desktop. Use this
> boilerplate at the beginning of every capability engineering session,
> then append the capability-specific section (for example C-021, C-022,
> etc.).

------------------------------------------------------------------------

# Repository & Document Availability Protocol

Before beginning:

1.  Determine whether the canonical repository is available.
2.  If the repository is available, inspect the canonical documents
    directly.
3.  If the repository is not available, use the documents uploaded in
    the current session.
4.  If any mandatory canonical document is unavailable:
    -   STOP.
    -   Do not guess.
    -   Do not rely on memory.
    -   Respond only with:

```{=html}
<!-- -->
```
    MISSING CANONICAL INPUT

    Required document:
    <document>

    Reason required:
    <reason>

Never fabricate missing canonical content.

------------------------------------------------------------------------

# Canonical Source Precedence

1.  Canonical repository
2.  Documents uploaded in the current conversation
3.  Nothing else

If memory conflicts with available documents, the available documents
always win.

------------------------------------------------------------------------

# Mandatory Repository Inspection

Before engineering:

-   Inspect CAP-001.
-   Confirm capability identity.
-   Preserve Business Intent verbatim.
-   Confirm Primary Specification.
-   Search the repository for all references to the capability.
-   Inspect dependent frozen capability specifications where relevant.
-   Never assume historical content exists.

------------------------------------------------------------------------

# Gold Standard Engineering Discipline

Follow the PE-001-C005 engineering sequence:

1.  Verify capability identity.
2.  Establish ownership boundary.
3.  Derive Guiding Architectural Question.
4.  Derive capability outcomes.
5.  Engineer one CRB.
6.  Independently derive ERBs.
7.  Independently derive EXs.
8.  Engineer seven Context Engineering dimensions for every ERB and EX.
9.  Derive Experience Contracts.
10. Bind Business Activities / EACs canonically.
11. Bind EIOs canonically.
12. Engineer governance.
13. Perform ownership and substitution tests.
14. Self-review before publication.

Do NOT copy ERB counts, EX counts, context models, stages or contracts
from previous capabilities.

------------------------------------------------------------------------

# Capability Boundary Rules

The capability owns only its canonical Business Intent.

Consume context from adjacent capabilities.

Never silently absorb: - Identity - Person - Membership - Organization -
Workspace - Access - Subscription - Billing - Contract - Entitlement or
any adjacent authority unless CAP-001 explicitly assigns ownership.

------------------------------------------------------------------------

# Seven-Dimension Context Engineering

Every ERB and EX must explicitly define:

-   Required
-   Created
-   Consumed
-   Preserved
-   Produced
-   Superseded
-   Invalidated

Created ≠ Produced.

Superseded ≠ Invalidated.

------------------------------------------------------------------------

# Canonical Binding Rules

Never fabricate:

-   Business Activity IDs
-   EAC IDs
-   EIO IDs

If unavailable:

**Pending Canonical Binding**

------------------------------------------------------------------------

# AI Governance

AI may assist.

AI shall not become authoritative.

Do not allow AI to: - approve, - grant, - deny, - establish
authoritative state, - create canonical enterprise facts, unless
explicitly permitted by canonical authority.

------------------------------------------------------------------------

# Anti-Hallucination Rules

-   Never invent missing policy.
-   Never invent lifecycle transitions.
-   Never invent identifiers.
-   Never invent canonical ownership.
-   Never infer repository content that is unavailable.
-   Ask for missing documents when required.

------------------------------------------------------------------------

# Anti-Template Test

If replacing the capability name with another capability still produces
a coherent document, the architecture is too generic.

Rewrite it.

------------------------------------------------------------------------

# Ownership Test

Confirm the capability does not redefine adjacent capability ownership.

------------------------------------------------------------------------

# Final Validation Checklist

Before publication confirm:

-   Business Intent preserved verbatim.
-   One CRB.
-   Every ERB justified.
-   Every EX has one governing ERB.
-   Seven Context Engineering dimensions present.
-   No fabricated identifiers.
-   Pending Canonical Binding used where appropriate.
-   AI boundaries preserved.
-   Capability boundaries preserved.
-   Substitution test passed.
-   Ownership test passed.

------------------------------------------------------------------------

# Output

Generate only:

-   Microsoft Word document
-   Validation summary
-   Publication Ready / Correction Required

Do not generate review reports unless explicitly requested.
