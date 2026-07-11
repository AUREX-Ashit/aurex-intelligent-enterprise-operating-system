# URA-001: User, Role, Permission, Event & Assignment Architecture
### Version 2.1 — GOLD STANDARD (Supersedes v2.0)

**Status:** LOCKED
**Scope:** Defines the authorization model — who may act, who owns what, who approves what, and how work is assigned and delegated — within CorpStage.
**Companion documents:** SD-001 (Screen Design, v2.0), SD-002 (Universal Business Object Rules, v2.0), SD-003 (Interaction Laws, v2.0), ERG-001 (Enterprise Structure & Relationship Management, v2.0) — all locked.
**Governing framework:** CorpStage Blueprint v2.1 — 39 Laws, 39 Screens, Two Journeys, Three Layers, One Platform

---

## Changelog from v2.0

One targeted fix, added during joint cross-review with ERG-001: **URA-001-17b (Home Enterprise Node)**. v2.0's Organization Membership was scoped to "an organization" with no reference to ERG-001's EnterpriseNode graph — meaning "member of ABC Ltd" was ambiguous once ABC Ltd is modeled as a graph of many nodes (subsidiaries, plants, business units) rather than a single flat entity. Every Membership now anchors to exactly one home node, distinct from the access granted via ERG-001's NodePermissionAssignment. No other changes from v2.0.

---

## Changelog from v1.0 Draft

URA-001 v1.0 had the best structural hygiene of any document reviewed to date — 150 principles, sequential, zero gaps, zero collisions. This version fixes one real conflict with an already-locked document, adds one missing boundary statement, disambiguates one naming collision, and completes the language purge.

| Fix | Detail |
|---|---|
| **CIL governance realigned to SD-002 v2.0** | v1.0 gave final Global/Industry CIL promotion authority to a single "CorpStage Admin" role (URA-001-31, URA-001-123, URA-001-145). SD-002 v2.0 — already locked — assigns this to a multi-tier stewardship model (Company Steward → Industry Intelligence Council → CorpStage Governance Board, SD-002-065/066). All three affected principles are corrected below: CorpStage Admin is now explicitly an *operational* role that executes Board/Council decisions, not the decision-maker. |
| **Explicit URA-001/SD-003 boundary added** | v1.0 claimed "assignments," "delegations," and "how work is assigned" as its own scope with no stated boundary against SD-003's Section 5 (Ownership, Assignment & Work Routing) and Section 7 (Delegation, Escalation & Exception Management), which claim the same nouns. New principle (URA-001-01a) states the split explicitly: URA-001 answers *who is authorized*; SD-003 answers *how humans experience that authorization*. |
| **Precedence models disambiguated** | v1.0's URA-001-76 ("Assignment Precedence Rules") and SD-002 v2.0's SD-002-113 ("Configuration Hierarchy Precedence") both used "most specific wins" language for different questions. URA-001-76 is renamed **Authorization Resolution Precedence** and now states explicitly what it is not. |
| **External-user delegation restricted** | New principle (URA-001-108a) closes a gap: external users granted Delegate authority may no longer delegate to internal employees or to other external organizations without Corporate Admin pre-approval. |
| **Cross-tenant Person visibility stated** | New principle (URA-001-17a) states that a Person's memberships at other organizations are never visible to an organization they don't belong to, mirroring SD-002 v2.0's Multi-Tenancy section. |
| **Deferral to Technical Architecture stated** | New principle (URA-001-150a) explicitly defers database schema and authorization-engine implementation to the Technical Architecture document, closing a silent gap the review identified. |
| **Escalation cycle protection added** | New principle (URA-001-94a) requires a stated maximum escalation depth and cycle detection. |
| **Language purge completed** | All ESG/Sustainability/Carbon/CSRD/BRSR/GRI/ISSB/Climate examples replaced per the binding substitution table — the highest violation count of any document reviewed (26 occurrences across Groups, Business Roles, Domains, Events, Entitlements, and CIL proposal examples). |
| **Numbering** | Original 150 principles retained with their numbers; 5 sub-numbered additions (URA-001-01a, 17a, 76 renamed not renumbered, 94a, 108a, 150a) preserve the existing reference scheme rather than triggering a full renumber, since no consolidation was needed. |
| Format | Compact prose per rule, matching the efficient format used for SD-003 v2.0 — full treatment given only to amended and new principles. |

---

## SECTION 1: Purpose & Design Principles

**URA-001-01a [new]: The URA-001 / SD-003 Boundary**

*(Closes a gap identified in review: v1.0 claimed "assignments" and "delegations" as its own scope with no stated boundary against SD-003, which claims the same nouns.)*

**URA-001 governs WHO may perform an action** — the authorization model: what an Assignment object contains, who structurally holds delegated authority, how competing authorization claims resolve, and what an Approval Authority or Domain Permission actually grants. **SD-003 governs HOW a human experiences that authorization** — the interaction sequencing, notification behavior, and UX pattern by which an assignment, delegation, or escalation is communicated to and acted upon by a person. Where SD-003 has a section with an overlapping name (Section 5, Ownership/Assignment/Work Routing; Section 7, Delegation/Escalation/Exception Management), that section governs the *interaction law*, never the *authorization data model* — the data model is exclusively URA-001's.

URA-001-01 One Person, Multiple Organizations — a person may belong to multiple organizations, each with independent roles (e.g., CFO at one company, Board Member at another), without duplicate identities.
URA-001-02 Identity Is Separate From Organization Membership — authentication (who you are) and authorization (what you can do inside a specific organization) are always separated.
URA-001-03 System Roles Are Separate From Business Roles — administrative responsibilities (Corporate Admin, Security Admin) and business responsibilities (CEO, CFO, Plant Head) remain independent.
URA-001-04 Business Roles Are Separate From Approval Authorities — holding the CFO business role never automatically grants Financial Statement Approver authority; approval powers are assigned independently.
URA-001-05 Domain Permissions Define Permanent Access — standing authority within a domain (View, Edit, Review, Approve) is granted independently of role or authority.
URA-001-06 Events Drive Work — work is driven by configurable business events (ENTER, REVIEW, APPROVE, BOARD_APPROVAL, CFO_SIGNOFF), not static permission checks alone.
URA-001-07 Runtime Assignments Override Default Access — an explicit, object-scoped assignment temporarily grants authority beyond a user's standing permissions (e.g., an HR Analyst assigned to review one specific Revenue CDE).
URA-001-08 Groups Are First-Class Business Objects — users belong to Groups (Board Committee, Audit Committee, Finance Leadership Team) supporting ANY_ONE/ALL/MAJORITY/SEQUENTIAL approval strategies.
URA-001-09 External Users Are Enterprise Participants — auditors, consultants, suppliers, board members, regulators, and partners default to View/Comment/Upload Evidence, gaining Enter/Review/Approve/Reject/Delegate only when explicitly assigned.
URA-001-10 Human Governance Is Mandatory — AI may recommend reviewers, approvers, and assignments and detect duplicates; only humans approve, reject, delegate, or escalate.
URA-001-11 Everything Is Metadata Driven — business roles, approval authorities, groups, events, domains, permissions, and delegation policies are all tenant-configurable without code changes.
URA-001-12 Everything Must Be Auditable — every action (user creation, role assignment, permission change, approval) generates a permanent audit record.
URA-001-13 Users Are Never Deleted — only activated, deactivated, or archived, preserving the integrity of historical approvals, assignments, and audit trails.
URA-001-14 Enterprise Scale Is a First-Class Concern — the model supports thousands of users, thousands of domains, and millions of assignments across multiple organizations without redesign.

---

## SECTION 2: Identity, User & Organization Membership Model

URA-001-15 Person Is the Master Human Entity — a Person represents a real human being, independent of any company, role, license, or permission.
URA-001-16 Identity Represents Authentication — how a person logs in (Google SSO, Entra ID, Okta); a Person may hold multiple identities, and authentication is always separate from authorization.
URA-001-17 Organization Membership Defines Authority — membership determines what a person can do within a specific organization; a person may be CFO at one company and Board Member at another simultaneously.

**URA-001-17b [new — added during ERG-001 cross-review]: Every Membership Anchors to a Home Enterprise Node**

*(New — closes a real integration gap: URA-001's Membership was scoped to "an organization," but ERG-001 v2.0 models an organization as a graph of many EnterpriseNodes — subsidiaries, plants, business units, shared service centers. "Member of ABC Ltd" is ambiguous without stating which node. This is distinct from ERG-001's NodePermissionAssignment, which governs granted *access*, not organizational *home placement*.)*

Every Membership references exactly one `home_node_id` — the specific EnterpriseNode (ERG-001) representing where that membership is organizationally anchored (e.g., Plant A, India Operations, Corporate HQ), independent of and prior to any explicit NodePermissionAssignment. The home node answers "where does this person organizationally sit," not "what can they access" — a Plant A-anchored Finance Analyst may still hold a NodePermissionAssignment granting them INCLUDE_DESCENDANTS access from India Operations; the home node and the granted access are separate facts, and a membership with no stated home node is an invalid state once ERG-001 is active for a tenant. Home node also supplies the default landing context (SD-001's screen-rendering layer resolves "which node's dashboard renders first" from this field), and reassignment of home node is itself an audited event (URA-001-12), never a silent field update.

**URA-001-17a [new]: Cross-Tenant Membership Visibility Is Restricted**

*(Closes a gap identified in review, mirroring SD-002 v2.0's Multi-Tenancy & Data Isolation section.)* A Person's physical identity (single login, single Person record) may span multiple organizations, but an organization may never see that same Person's roles, permissions, or memberships at any other organization they belong to, absent an explicit, named, audited cross-tenant sharing agreement. Organization A knowing that a shared Person is "also CFO somewhere else" without knowing where is the correct default; Organization A seeing the specific other organization's name or role detail is a data isolation failure.

URA-001-18 Internal and External Users Are Membership Types — external users share the same identity model as internal users; the same person may be INTERNAL at one organization and EXTERNAL at another.
URA-001-19 User Licenses Are Membership Attributes — Full Licenses (internal users: create, edit, configure, administer, approve) and Light Licenses (external users: view, enter, review, approve when assigned, upload evidence) belong to the membership, not the person.
URA-001-20 Membership Lifecycle Is Independent — memberships activate, suspend, deactivate, or archive independently per organization; nothing is permanently deleted.
URA-001-21 Memberships Support Effective Dates — organization memberships carry validity periods (e.g., Board Member 2027–2029); expired memberships automatically lose authority.
URA-001-22 Memberships Support Multiple Roles — a single membership may hold multiple business roles (CFO, Board Member, Risk Committee Member) additively.
URA-001-23 Memberships Support Multiple Groups — users may belong to multiple groups (Board Committee, Finance Leadership Team) with independent effective dates.
URA-001-24 User Profiles Are Extensible — organizations extend user profiles (Employee Number, Plant Code, Region) without code changes, layered as Global Fields → Company Extensions.
URA-001-25 SSO Is the Preferred Enterprise Model — Entra ID, Google Workspace, Okta, SAML, and OAuth2 are all supported, with local authentication remaining available.
URA-001-26 User Preferences Are Personal — theme, language, and notification preferences belong to the Person and remain independent of any organization.
URA-001-27 Membership Preferences Are Organizational — default domain, dashboard, and report preferences belong to the membership, not the person globally.
URA-001-28 Users Are Never Deleted — restated structurally: activation, suspension, deactivation, and archiving are the only lifecycle transitions; hard deletion is prohibited to preserve assignment, approval, and audit history.

---

## SECTION 3: System Roles & Business Roles

URA-001-29 System Roles Govern Platform Administration — CorpStage Admin, Corporate Admin, User Admin, Security Admin, and Domain Admin control users, licenses, metadata, security, and platform operations; they do not represent business accountability.
URA-001-30 Business Roles Represent Business Identity — CEO, CFO, COO, CHRO, CSO, CISO, Company Secretary, Finance Manager, Plant Head, and Board Member represent organizational responsibility and never automatically grant administrative, approval, or user-management rights.

**URA-001-31 [amended]: CorpStage Admin Is a Platform Operational Role, Not the Canonical Governance Authority**

*(Amended — this is the root of the CIL governance conflict with SD-002 v2.0. v1.0 listed "Global CIL Governance" and "Industry CIL Governance" as direct CorpStage Admin capabilities. Corrected below.)*

CorpStage Admins belong to CorpStage, not to any customer organization, and are responsible for: corporate onboarding, global user support, platform configuration, license management, and subscription management. **CorpStage Admins execute the decisions of the CorpStage Governance Board and the Industry Intelligence Council (SD-002-065/066) — they do not independently decide Global CIL or Industry CIL promotion.** Where a CorpStage Admin action implements a canonical promotion, that action must reference the specific Governance Board or Industry Council decision it is executing; a CIL promotion event with no referenced Board or Council decision is an invalid state, not a valid shortcut.

URA-001-32 Corporate Admin Is the Highest Company Authority — every organization has one or more Corporate Admins who create users, assign licenses and roles, create domains, and approve domain-level proposals; in CIL governance terms, the Corporate Admin functions as the Company Steward (SD-002-065).
URA-001-33 User Admin Is a Specialized System Role — may invite, deactivate, and assign roles to users, but not manage licenses, domains, or approve CDE promotions unless explicitly granted.
URA-001-34 Security Admin Is a Specialized System Role — governs SSO, MFA, password policy, IP restrictions, and access reviews independently of business metadata or CDE governance.
URA-001-35 Domain Admin Is an Operational Role — manages domain operations (assign work, manage domain events and views, create CDE/BQ/Activity proposals) but never creates users or assigns licenses.
URA-001-36 Domain Owner Is Separate From Domain Admin — the Domain Owner (e.g., CFO for Finance) holds business accountability and strategic direction; the Domain Admin (e.g., Finance Controller) holds operational management — the same Owner/Admin separation SD-002 v2.0 requires at the object level.
URA-001-37 Multiple Business Roles Are Supported — a user may hold CFO, Board Member, and Risk Committee Member simultaneously, additively and auditable.
URA-001-38 Business Roles Are Metadata Driven — organizations create custom business roles (Chief Innovation Officer, Group Controller, Business Resilience Champion) without code changes, layered as Global Roles → Company Roles.
URA-001-39 Business Roles Support Effective Dates — role assignments carry validity periods (e.g., Interim CFO for a defined window); expired roles automatically lose authority.
URA-001-40 Business Roles Do Not Inherit Permissions — restated structurally: CFO alone grants nothing; CFO plus explicitly-assigned Finance Domain Approver plus Annual Report Approver grants approval authority.
URA-001-41 Approval Authorities Are First-Class Objects — Annual Report Approver, Financial Statement Approver, Board Resolution Approver, and Policy Approver exist and are managed independently of business role.
URA-001-42 Approval Authorities Support Multiple Strategies — ANY_ONE, ALL, MAJORITY, and SEQUENTIAL strategies apply per approval authority (e.g., Board Approval as MAJORITY of Board Committee, Annual Report Approval as SEQUENTIAL CFO → CEO → Board).

---

## SECTION 4: Domain Ownership & Domain Permissions

URA-001-43 Domains Are First-Class Business Objects — Finance, HR, Risk, Supply Chain, Cyber Security, Legal, and Business Resilience are logical business ownership areas; organizations may add domains such as Innovation, Manufacturing Excellence, or Investor Relations.
URA-001-44 Domain Hierarchies Shall Be Supported — domains may contain sub-domains (Finance → Accounting, Treasury, Taxation, Investor Relations) with configurable inheritance and overrides.
URA-001-45 Domain Owners Define Business Accountability — every domain has one or more owners (Finance → CFO, HR → CHRO) holding business governance, strategic direction, and policy ownership.
URA-001-46 Domain Admins Manage Operations — assign work, create domain events, and create CDE/BQ/Activity proposals within their domain.
URA-001-47 Domain Permissions Define Standing Authority — VIEW, ENTER, EDIT, REVIEW, APPROVE, ASSIGN, DELEGATE, and ADMIN represent permanent access within a domain.
URA-001-48 Domain Permissions Are Independent of Business Roles — restated structurally: CFO does not automatically become Finance Approver; the permission must be explicitly granted alongside the role.
URA-001-49 Runtime Assignments Override Domain Permissions — an explicit, object-scoped assignment temporarily extends a user's standing domain permission (e.g., an HR Manager with Finance VIEW granted temporary REVIEW on one specific Revenue CDE).
URA-001-50 Domains Support Visibility Rules — each domain defines who may see it (Finance visible to CFO, Finance Team, Corporate Admin, Auditors), scoped by user, role, group, or external-user type.
URA-001-51 Domain-Specific Events Are Supported — Finance (CFO_SIGNOFF, FINANCIAL_REVIEW), Legal (LEGAL_APPROVAL, COMPLIANCE_REVIEW), and HR (HR_POLICY_REVIEW) each define their own events at Global, Company, or Domain scope.
URA-001-52 Domain Metadata Is Extensible — organizations extend domains with Region, Business Unit, Plant Code, and Cost Center fields without code changes.
URA-001-53 Domain Permissions Support Effective Dates — permissions may be time-bound (e.g., Interim Risk Reviewer for 90 days); expired permissions automatically deactivate.
URA-001-54 Domain Groups Are First-Class Objects — domains maintain their own groups (Finance Leadership Team, Treasury Committee, Plant Managers) supporting all four approval strategies.
URA-001-55 Domains Support Internal and External Participants — external users may hold domain-scoped permissions (External Auditor → Finance: REVIEW, APPROVE) but never ADMIN, USER_MANAGEMENT, or LICENSE_MANAGEMENT.
URA-001-56 Domain Governance Is Metadata Driven — domain structure, sub-domains, permissions, events, groups, and visibility rules are all tenant-configurable.

---

## SECTION 5: Groups & Approval Authorities

URA-001-57 Groups Are First-Class Business Objects — Board Committee, Audit Committee, Finance Leadership Team, Risk Committee, and Plant Managers Group support named users, business roles, external users, and mixed membership.
URA-001-58 Groups Support Effective Dates — group memberships are time-bound (e.g., a 6-month external consultant membership); expired memberships automatically become inactive.
URA-001-59 Groups Support Hierarchies — groups may contain sub-groups (Board → Audit Committee, Risk Committee, Business Resilience Committee) with configurable inheritance.
URA-001-60 Approval Authorities Are First-Class Objects — Annual Report Approver, Financial Statement Approver, Board Resolution Approver, Policy Approver, Supplier Approval Authority, and Risk Acceptance Authority all exist independently of business role.
URA-001-61 Approval Authorities Support Multiple Scopes — Global, Company, Domain, and Object-level approval authorities (e.g., Global Framework Approval vs. Revenue CDE Approval) are all supported.
URA-001-62 Approval Strategies Are Configurable — ANY_ONE (any one member approves), ALL (every member must approve), MAJORITY (configurable threshold), and SEQUENTIAL (predefined order) are all available per approval authority.
URA-001-63 Approval Authorities Support Delegation — approval powers may be temporarily delegated (CFO → Finance Controller, 1 week, reason: travel) with full delegator/delegatee/scope/date/reason attributes, always auditable.
URA-001-64 Temporary Substitutions Are Supported — organizations define temporary replacements (Acting CFO during leave, Interim Board Member on resignation) with start date, end date, and business justification.
URA-001-65 Approval Authorities Support External Users — Independent Directors may hold Board Resolution Approval authority; External Auditors may hold Audit Confirmation Approval authority — without receiving administrative or user-management rights.
URA-001-66 Runtime Assignments Override Default Authorities — restated structurally per URA-001-07/49, applied at the approval-authority level, using Authorization Resolution Precedence (see URA-001-76 below).
URA-001-67 Approval Chains Are Metadata Driven — Simple (Manager → Approve), Sequential (Finance Manager → CFO → CEO), and Committee (Board Committee → MAJORITY) chains are all tenant-configurable.
URA-001-68 Approval Actions Generate Events — APPROVED, REJECTED, DELEGATED, ESCALATED, RECALLED, and REASSIGNED all generate immutable, versioned audit events.
URA-001-69 Approval Authorities Support Effective Dates — approval powers are time-bound (e.g., Interim CFO Approval Authority for 90 days); expired authorities automatically become inactive.
URA-001-70 Groups and Approval Authorities Are Metadata Driven — organizations create custom groups (Innovation Council, Business Resilience Committee) and approval authorities (Transition Risk Approval, Investor Communication Approval) without code changes.

---

## SECTION 6: Event Architecture & Runtime Assignment Model

URA-001-71 Events Are First-Class Business Objects — ENTER, EDIT, REVIEW, APPROVE, REJECT, ASSIGN, DELEGATE, ESCALATE, ARCHIVE, and PUBLISH each carry identity, scope, assignment rules, escalation rules, audit, and versioning.
URA-001-72 Event Scopes Are Hierarchical — Global (APPROVE, REVIEW, ASSIGN), Company (BOARD_APPROVAL, LEGAL_REVIEW, AUDIT_CONFIRMATION), and Domain (CFO_SIGNOFF, HR_POLICY_APPROVAL) scopes are all supported.
URA-001-73 Events Are Metadata Driven — Corporate Admins create events without code changes, including company-specific events such as BOARD_APPROVAL and SUPPLIER_CERTIFICATION.
URA-001-74 Runtime Assignments Are First-Class Objects — assignments (Review Revenue CDE, Approve Annual Report) carry Assignment ID, Object Type, Object ID, Event, Assigned By, Assigned To, Start/End Date, Status, and Comments.
URA-001-75 Assignment Targets Are Flexible — assignments may target Named Users, Business Roles, Groups, or External Users; the platform resolves the actual assignee dynamically.

**URA-001-76 [renamed and amended]: Authorization Resolution Precedence**

*(Renamed from "Assignment Precedence Rules." Distinct from SD-002-113, Configuration Hierarchy Precedence — the two govern different questions and use similar "most specific wins" language, creating a real risk of conflation. This principle now states the distinction explicitly.)*

For any authorization question — who may act on a specific object, right now — the most specific source wins: **Named User > Group > Approval Authority > Business Role > Domain Permission**. Runtime assignments temporarily override standing permissions. **This precedence governs authorization only — who is permitted to act. It is a distinct system from SD-002-113 (Metadata Resolution Precedence), which governs which configuration value applies for a tenant.** An engineer implementing either system must confirm which question is being answered before applying either precedence chain; the two are never interchangeable and never share an implementation.

**Resolution against ERG-001's Node Permission Assignment (added during joint cross-review):** ERG-001 v2.0 introduces a third, graph-based authorization path — access granted against an EnterpriseNode with an inheritance scope (NODE_ONLY, INCLUDE_DESCENDANTS, INCLUDE_ANCESTORS, VIEW_CONSTRAINED, CUSTOM_TRAVERSAL). This is not a competing precedence system; it is a **source that feeds into this same chain at the Domain Permission level.** A NodePermissionAssignment resolves to an effective Domain Permission for the relevant node before this precedence chain is evaluated — meaning a Named User's direct object-level assignment still overrides a node-inherited permission, exactly as it would override any other Domain Permission. Node-based access is never a parallel authority; it is always expressed as the weakest, most-easily-overridden layer of this same precedence chain.

URA-001-77 Runtime Permissions Are Object Scoped — assignments never create global permissions (Review: Revenue CDE is allowed; Review: Entire Finance Domain is not, unless explicitly granted); assignments are always Object Scoped, Event Scoped, and Time Scoped.
URA-001-78 Assignment Lifecycles Are Configurable — CREATED, ASSIGNED, ACCEPTED, IN_PROGRESS, COMPLETED, REJECTED, ESCALATED, EXPIRED, and ARCHIVED are default states; companies may add states such as BOARD_APPROVED.
URA-001-79 Delegations Are First-Class Objects — assignments may be delegated (CFO → Finance Controller, 5 days) with delegator, delegatee, object, event, dates, reason, and sub-delegation flag, always auditable.
URA-001-80 Escalations Are Metadata Driven — escalation policies support Time Based, Role Based, Manager Based, and Manual Escalation rules.
URA-001-81 Assignment Acceptance Is Configurable — organizations choose Auto Accept (Assigned → Active) or Manual Accept (Assigned → Accept → In Progress).
URA-001-82 Groups Support Work Distribution Strategies — ANY_ONE, ALL, MAJORITY (configurable 50/66/75/100% threshold), and SEQUENTIAL all apply to group-targeted assignments.
URA-001-83 Event Templates Are Reusable — organizations define reusable workflows (Annual Report: Prepare → Finance Review → CFO Signoff → CEO Approval → Board Approval → Publish) as metadata.
URA-001-84 Runtime Assignments Support External Users — Suppliers (ENTER, UPLOAD_EVIDENCE), External Auditors (REVIEW, APPROVE), and Consultants (ENTER, REVIEW) may receive assignments; external users never receive USER_MANAGEMENT, LICENSE_MANAGEMENT, or DOMAIN_ADMIN.
URA-001-85 Event Histories Are Immutable — every event (ASSIGNED, ACCEPTED, DELEGATED, APPROVED, REJECTED, ESCALATED, COMPLETED) generates a permanent audit record capturing who, what, when, why, previous state, and new state.
URA-001-86 Event Policies Are Metadata Driven — restated structurally: events, assignment rules, escalation policies, delegation policies, approval strategies, and templates are all tenant-configurable.

---

## SECTION 7: Delegation, Escalation & Exception Management

URA-001-87 Delegation Is a First-Class Business Object — delegations (CFO → Finance Controller, 5 days, reason: business travel) carry identity, scope, duration, approvals, and audit history.
URA-001-88 Delegations Are Always Temporary — every delegation requires a start date, end date, and reason; permanent delegations are not allowed.
URA-001-89 Delegation Scopes Are Granular — Organization, Domain, Object, and Event-level delegation scopes are all supported.
URA-001-90 Delegation Types Are Configurable — TEMPORARY, OUT_OF_OFFICE, EMERGENCY, ACTING_ROLE, and PROJECT_BASED are standard types; companies may define custom types (INTERIM_CFO, BOARD_SUBSTITUTE).
URA-001-91 Delegations Preserve Original Accountability — the original owner remains accountable; the audit trail records "Approved By: Finance Controller, On Behalf Of: CFO" — delegated authority is never transferred accountability.
URA-001-92 Sub-Delegation Is Policy Driven — organizations explicitly permit or prohibit further delegation of an already-delegated authority.
URA-001-93 Escalations Are First-Class Business Objects — escalations (Review Pending → 3 Days → Escalate to Finance Head) support Time Rules, Hierarchy Rules, Manual Rules, and Emergency Rules.

**URA-001-94a [new]: Escalation Chains Require Stated Depth Limits and Cycle Detection**

*(New — closes a gap identified in review: no principle stated a maximum escalation depth or cycle-detection safeguard.)* Every configured escalation chain declares a maximum depth (default: 5 hops) beyond which an unresolved item is automatically routed to the Domain Owner (SD-002-007) rather than continuing to escalate indefinitely. Before an escalation policy is activated, the platform validates that it contains no cycle (a chain that could route an item back to an assignee earlier in the same chain) — a cyclical escalation policy is rejected at configuration time, not discovered at runtime when an item silently loops.

URA-001-94 Escalation Strategies Are Configurable — Time-Based, Hierarchy-Based, Role-Based, and Group-Based escalation models are all supported.
URA-001-95 Manager Hierarchies Are Supported — reporting structures (Analyst → Manager → Director → CFO) are metadata-driven and usable as escalation targets.
URA-001-96 Out-of-Office Management Is Built In — users configure temporary absence with auto-delegate, auto-escalate, auto-reject, or hold-assignment behavior.
URA-001-97 Acting Roles Are Supported — temporary acting roles (Interim CFO, 90 days) carry business role, approval authority, and domain permission with explicit effective dates.
URA-001-98 Exception Handling Is First-Class — the platform supports named business exceptions (Approver Resigned, Committee Quorum Not Met, Supplier Not Responding) with reassign, escalate, delegate, override, or suspend-workflow actions, always auditable.
URA-001-99 Emergency Access Is Controlled — break-glass mechanisms (Emergency Financial Approval, Emergency Board Approval) require business justification, start/end date, approvals, and audit logging.
URA-001-100 Exception Policies Are Metadata Driven — delegation, escalation, OOO, and emergency policies are all tenant-configurable, with domain-specific timing (Finance: 3 days, Legal: 5 days, HR: 7 days).
URA-001-101 Delegations Generate Immutable Events — DELEGATED, ACCEPTED, REJECTED, REVOKED, EXPIRED, and COMPLETED all generate permanent audit events.
URA-001-102 Escalations Generate Immutable Events — ESCALATED_TO_MANAGER, ESCALATED_TO_DOMAIN_OWNER, MANUAL_ESCALATION, and AUTO_ESCALATION are all permanently recorded.
URA-001-103 Exception Handling Supports Human Overrides — Corporate Admins may perform controlled overrides (Override Approval Chain, Skip Inactive User) requiring reason, approver, audit trail, and effective duration.
URA-001-104 Enterprise Continuity Is the Primary Objective — no workflow fails because an individual is unavailable; delegations, escalations, substitutions, emergency access, and human overrides together guarantee this.

---

## SECTION 8: External Users, Licensing & Entitlements

URA-001-105 External Users Are First-Class Participants — auditors, consultants, suppliers, partners, board members, independent directors, regulators, customers, and investors all support authentication, assignments, approvals, evidence upload, audit trails, and delegation.
URA-001-106 External Users Are Membership Types — external users use the same identity model as internal users; membership type (INTERNAL/EXTERNAL) is set per organization, so the same Person may be INTERNAL at one organization and EXTERNAL at another (e.g., Independent Director).
URA-001-107 External Users Are Restricted From Administrative Capabilities — restated structurally: User Management, License Management, Corporate Configuration, Domain Administration, Global Metadata Management, Framework Management, and CIL Promotions are never available to external users.
URA-001-108 External Users May Participate Through Assignments — Suppliers (ENTER, UPLOAD_EVIDENCE), External Auditors (REVIEW, APPROVE, COMMENT), Consultants (ENTER, REVIEW, DELEGATE), and Independent Directors (BOARD_APPROVAL, VOTE, COMMENT) may all be explicitly assigned.

**URA-001-108a [new]: External-User Delegation Requires Governed Boundaries**

*(New — closes a gap identified in review: v1.0 permitted external users to hold Delegate authority with no stated boundary on who they could delegate to.)* An external user granted Delegate authority may delegate only to another external user within the same external organization pool by default. Any delegation from an external user to an internal employee, or to an external user from a *different* organization (e.g., a Consultant delegating to a Supplier), requires explicit Corporate Admin pre-approval as a distinct, named, auditable governance event — it is never a default consequence of holding the Delegate permission.

URA-001-109 Explicit Assignments Override Default Access — external users receive authority only through assignment; default access remains View, Comment, Upload Evidence.
URA-001-110 External Users Support Runtime Events — SUPPLIER_CERTIFICATION, BOARD_APPROVAL, AUDIT_CONFIRMATION, and CONSULTANT_REVIEW are all available to external users, remaining Object Scoped, Event Scoped, and Time Scoped.
URA-001-111 License Types Are First-Class Objects — Full User License (internal: administration, configuration, approvals, metadata, CDE/BQ creation) and Light User License (external: view, enter, review, approve when assigned, upload evidence) are both supported.
URA-001-112 Entitlements Are Separate From Licenses — licenses define user counts; entitlements define capabilities (IFRS Enabled, Annual Report Enabled, AI Discovery Enabled, Supplier Portal Enabled).
URA-001-113 Entitlements Are Metadata Driven — CorpStage Admins create global entitlements (Regulatory Reporting Module, Integrated Reporting, Business Resilience Module); Corporate Admins enable company features, industry packages, and optional modules.
URA-001-114 Domain-Level Entitlements Are Supported — Finance (Annual Report Generation, IFRS Reporting), HR (Talent Competitiveness Analytics, Employee Engagement), and Business Resilience (Regulatory Reporting Module) domains each enable their own feature sets.
URA-001-115 External Users May Consume Specialized Licenses — Supplier License, Auditor License, Board Member License, and Consultant License support lower cost, higher collaboration, and flexible pricing.
URA-001-116 License Enforcement Is Centralized — Corporate Admins manage users only within purchased limits; exceeding a limit blocks new user creation pending upgrade, always auditable.
URA-001-117 Feature Entitlements Support Effective Dates — entitlements are time-bound (e.g., a 90-day Supplier Portal trial) and automatically deactivate on expiry.
URA-001-118 Trial and Sandbox Entitlements Are Supported — AI Discovery Trial and Annual Report Beta carry start date, end date, usage limits, and feature restrictions.
URA-001-119 Entitlement Changes Generate Events — ENTITLEMENT_ENABLED, ENTITLEMENT_DISABLED, TRIAL_STARTED, TRIAL_EXPIRED, and LICENSE_UPGRADED are all immutably recorded.
URA-001-120 External Collaboration Is a Core Platform Capability — suppliers, auditors, consultants, independent directors, regulators, and partners are treated as first-class ecosystem participants, not administrative afterthoughts.

---

## SECTION 9: CDE, BQ & Business Activity Governance Workflow

URA-001-121 Domain Admins May Create Proposals — proposals for new CDEs, BQs, and Business Activities (e.g., Finance: Energy Cost & Transition Exposure Liability; HR: Employee Wellbeing Index; Supply Chain: Supplier Circularity Score) may be created, never directly modifying canonical libraries.
URA-001-122 Corporate Admin Approval Is Mandatory — every proposal requires Corporate Admin business validation, duplicate check, organizational relevance assessment, and ownership assignment before CorpStage review — Corporate Admin here functions as Company Steward (SD-002-065).

**URA-001-123 [amended]: CIL Promotion Follows the SD-002 Stewardship Model**

*(Amended — this was the primary source of the conflict with SD-002 v2.0. Corrected to route through the multi-tier stewardship model rather than a single CorpStage Admin decision.)*

Final canonical promotion decisions follow SD-002-065/066 exactly: **Company → Industry promotion requires Industry Intelligence Council approval; Industry → Global promotion requires CorpStage Governance Board approval.** CorpStage Admin executes the resulting decision (updating the CIL record, notifying stakeholders, versioning the promoted object) but is not the deciding authority for either tier. The full workflow is: Domain Admin creates proposal → Corporate Admin (Company Steward) validates and approves at company level → AI similarity analysis runs → Industry Intelligence Council decides Company-to-Industry promotion where applicable → CorpStage Governance Board decides Industry-to-Global promotion where applicable → CorpStage Admin executes the decision as Global CIL, Industry CIL, Company CIL, Merge, or Reject. A canonical promotion record with no referenced Council or Board decision is invalid.

URA-001-124 AI Similarity Detection Is Mandatory — the platform performs duplicate analysis before approval (e.g., "Delivery Cost" detected as 94% similar to "Cost Of Delivery"), suggesting reuse, merge, or escalation; AI recommendations remain advisory and humans make the final decision.
URA-001-125 CDE Ownership Must Be Defined — every approved CDE has a named owner (Revenue → Finance Domain; Talent Competitiveness → HR Domain) supporting governance, review, approval, and lifecycle management.
URA-001-126 Company CIL Extensions Are Supported — organizations maintain company-specific CDEs (Internal Innovation Index, Plant Efficiency Rating, Company Business Resilience Index), remaining visible, versioned, auditable, and upgradeable, with later promotion available through URA-001-123's stewardship chain.
URA-001-127 Hide, Archive, and Purge Are Different Actions — Hide (invisible, restorable), Archive (inactive, historically accessible), and Purge (governed administrative removal requiring Corporate Approval, audit records, and retention validation) are distinct, non-interchangeable actions.
URA-001-128 Business Activities Are Preferred Over Questionnaires — users perform named business activities (Cost Of Delivery, 10 inputs, 3 minutes) rather than answering isolated numbered questions.
URA-001-129 BQs Are Reusable Business Assets — a single Business Question (e.g., "What is your total energy consumption?") may support multiple frameworks and internal dashboards simultaneously.
URA-001-130 CDEs Represent Enterprise Truth — Canonical Data Elements remain framework-independent (Revenue From Operations maps to IFRS, Annual Report, Board Reporting) under One Truth, Multiple Views.
URA-001-131 Governance Workflows Are Metadata Driven — approval chains, review steps, promotion rules, visibility rules, and ownership models are all tenant-configurable.
URA-001-132 CDE Lifecycle States Are Configurable — PROPOSED, UNDER_REVIEW, APPROVED, ACTIVE, ARCHIVED, and SUPERSEDED are default states; companies may add states such as BOARD_APPROVED.
URA-001-133 Governance Actions Generate Events — CDE_PROPOSED, CDE_APPROVED, CDE_REJECTED, CDE_MERGED, and CDE_ARCHIVED are all permanently recorded.
URA-001-134 Canonical Intelligence Evolves Continuously — the CIL improves through customer proposals, industry standards, framework changes, AI recommendations, and regulatory updates — Living Intelligence, not static configuration.

---

## SECTION 10: Universal Design Principles & Freeze Summary

URA-001-135 One Person, Multiple Organizations — restated as constitutional law: one person, multiple identities, multiple memberships, multiple roles.
URA-001-136 Human Governance Is Mandatory — restated as constitutional law: AI recommends, suggests, detects, and predicts; humans approve, reject, delegate, escalate, and override.
URA-001-137 Everything Is Metadata Driven — roles, groups, events, approval authorities, domains, permissions, entitlements, delegation and escalation policies are all configuration, never code.
URA-001-138 Events Drive Enterprise Work — permissions provide standing authority; events drive actual work.
URA-001-139 Runtime Assignments Override Standing Permissions — restated using the corrected terminology: Authorization Resolution Precedence (URA-001-76) governs which assignment source wins, always Object Scoped, Event Scoped, and Time Scoped.
URA-001-140 External Collaboration Is Native — auditors, suppliers, consultants, independent directors, regulators, and partners are first-class participants who may enter data, review, approve, and upload evidence when assigned, and never become administrators.
URA-001-141 Business Continuity Is Mandatory — no workflow fails because an individual is unavailable, through delegation, escalation, out-of-office handling, acting roles, emergency access, and human override.
URA-001-142 Everything Is Auditable — all actions generate immutable events capturing who, what, when, why, previous state, and new state.
URA-001-143 Nothing Is Hard Deleted — Hide, Archive, and governed Purge are the only visibility-reducing actions; users, assignments, approvals, audit events, and evidence are never hard-deleted.
URA-001-144 One Truth, Multiple Views — the same business object (Revenue) appears across Finance Domain, Annual Report, IFRS, and Board Dashboard as one canonical object with multiple perspectives.

**URA-001-145 [amended]: Local Innovation With Global Governance — Corrected Workflow**

*(Amended — v1.0 restated the same single-admin CIL workflow error found in URA-001-123. Corrected identically here for consistency.)* Organizations innovate locally while preserving canonical integrity: Domain Admin → Corporate Admin (Company Steward) → Industry Intelligence Council (for Industry promotion) → CorpStage Governance Board (for Global promotion) → CorpStage Admin executes the decision as Global CIL, Industry CIL, Company CIL, Merge, or Reject. Innovation with governance — governed by councils and boards, executed by CorpStage Admin, never decided by CorpStage Admin alone.

URA-001-146 Enterprise Scale Is a First-Class Concern — restated structurally: thousands of users, thousands of domains, millions of assignments, hundreds of organizations, multiple industries, without redesign.
URA-001-147 Security Is Layered — Identity Layer (SSO, MFA), Membership Layer (roles, groups, permissions), Runtime Layer (assignments, delegations, approvals), and Audit Layer (events, history, retention) together provide defense in depth.
URA-001-148 Entitlements Are Independent of Licenses — restated structurally: licenses define user counts; entitlements define capabilities (IFRS, Annual Reports, AI Discovery, Supplier Portal) — users are not features.
URA-001-149 Enterprise Intelligence Requires Collaboration — employees, suppliers, auditors, consultants, board members, and regulators all participate in the same enterprise intelligence ecosystem.

**URA-001-150 [retained]: URA-001 Is the Single Source of Truth for Identity, Access, Roles, Permissions, Groups, Events, Assignments, Delegations, Licensing, Entitlements, and Governance**

All future implementations conform to URA-001.

**URA-001-150a [new]: Database and Authorization-Engine Design Are Deferred to Technical Architecture**

*(New — closes a gap identified in review: the document contained zero reference to schema or authorization-engine implementation, leaving the boundary to be inferred rather than stated.)* URA-001 defines the authorization *model* — the entities, relationships, and precedence rules that must exist. It deliberately does not specify database schema, indexing strategy, or the specific authorization-engine implementation (policy engine, claims format, token structure) that enforces this model at runtime — those are Technical Architecture's responsibility. Any Technical Architecture implementation must be traceable to a specific URA-001 principle; a technical capability with no corresponding URA-001 principle is either a missing principle here (raise it for addition) or an implementation detail correctly out of this document's scope.

**Universal Architecture Summary**

```
Person
 └── Identity (authentication)
      └── Organization Membership (authority)
           ├── System Roles
           ├── Business Roles
           ├── Approval Authorities
           ├── Groups
           ├── Domain Permissions
           └── Runtime Assignments
                ├── Delegations
                └── Escalations
```

---

## Full Principle Index

| Range | Section |
|---|---|
| URA-001-01 – 14, 01a (new) | Section 1 — Purpose & Design Principles |
| URA-001-15 – 28, 17a (new) | Section 2 — Identity, User & Organization Membership Model |
| URA-001-29 – 42, 31 (amended) | Section 3 — System Roles & Business Roles |
| URA-001-43 – 56 | Section 4 — Domain Ownership & Domain Permissions |
| URA-001-57 – 70 | Section 5 — Groups & Approval Authorities |
| URA-001-71 – 86, 76 (renamed/amended) | Section 6 — Event Architecture & Runtime Assignment Model |
| URA-001-87 – 104, 94a (new) | Section 7 — Delegation, Escalation & Exception Management |
| URA-001-105 – 120, 108a (new) | Section 8 — External Users, Licensing & Entitlements |
| URA-001-121 – 134, 123 (amended) | Section 9 — CDE, BQ & Business Activity Governance Workflow |
| URA-001-135 – 150, 145 (amended), 150a (new) | Section 10 — Universal Design Principles & Freeze Summary |

**Total: 150 original principles retained, 3 amended to resolve the CIL governance conflict (URA-001-31, 123, 145), 1 renamed and amended for disambiguation (URA-001-76), 5 newly added (URA-001-01a, 17a, 94a, 108a, 150a). Final addressable count: 155 principles across 10 sections, zero gaps, zero collisions in the original numbering.**

---

## Freeze Statement

URA-001 v2.0 is ready for lock. The CIL governance conflict with SD-002 v2.0 is fully resolved — CorpStage Admin is now consistently, in all three affected locations (URA-001-31, 123, 145), an operational role executing the decisions of the Industry Intelligence Council and CorpStage Governance Board, never the canonical decision-maker itself. The URA-001/SD-003 boundary is now explicit (URA-001-01a). The two "most specific wins" precedence systems are disambiguated by name and by stated scope (URA-001-76 vs. SD-002-113). The language purge is complete — 26 occurrences corrected using the binding substitution table, not synonym substitution. Cross-tenant Person visibility, external-user delegation boundaries, escalation cycle protection, and deferral to Technical Architecture are all now explicitly stated rather than left to inference.

**No open cross-document conflicts remain.** All four foundational documents — SD-001, SD-002, SD-003, and URA-001 — are now at Gold Standard v2.0 and consistent with one another.
