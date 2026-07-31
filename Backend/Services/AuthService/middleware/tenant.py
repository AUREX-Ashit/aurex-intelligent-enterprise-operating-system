import uuid
from contextvars import ContextVar
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse

# Context variable to hold tenant ID throughout the current coroutine context
tenant_context: ContextVar[uuid.UUID | None] = ContextVar("tenant_context", default=None)

class TenantMiddleware(BaseHTTPMiddleware):
    """
    HTTP Middleware tasked with multi-tenant extraction.
    Interceptors ensure callers provide valid UUID X-Tenant-ID headers.
    """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Skip tenant checks for standard auth-agnostic paths (e.g. docs, openapi, health).
        # /person/recognize and /person/establish are tenant-agnostic on the same basis as
        # /auth/login: Person is independent of any company, role, license, or permission
        # (URA-001-15), and neither EX-C006-01 nor EX-C006-02 states an Organization/tenant
        # context requirement.
        # /ready (WP-00) is platform-scoped, not tenant-scoped, on the same basis as
        # /health: an orchestrator's readiness probe has no tenant context to supply.
        # /organizations and /organizations/{id} (WP-01, BA-01 Establish / BA-02 View)
        # are tenant-agnostic for the same reason as /person/establish: the
        # PLATFORM_ADMIN role these endpoints require (dependencies.require_platform_admin)
        # operates across every organization boundary, so there is no single tenant
        # to scope the request to. Prefix-matched (not exact-listed) because BA-02
        # introduced a path parameter (/organizations/{organization_id}); every future
        # WP-01 Business Activity's endpoint lives under this same prefix and is
        # covered by the same rationale, so it is not re-added per activity.
        # /roles (WP-02, BA-01 Establish Business or System Role) is tenant-agnostic
        # on the same basis: the Role model has no organization_id column — Roles are
        # platform-global (URA-001 Section 3), not tenant-scoped, mirroring
        # /organizations' own rationale exactly (IRA-002 §2.4).
        # /domains (AMD-014, Domain reference/master-data lookup) is tenant-agnostic
        # for the same reason as /roles: the read-only lookup is PLATFORM_ADMIN-gated
        # and Domain rows are platform-seeded/global by default (organization_id
        # nullable), with any tenant-scoping expressed as an explicit query
        # parameter rather than the X-Tenant-ID header this middleware enforces.
        # /domain-permissions (WP-02, BA-02 Establish Domain Permission) is
        # tenant-agnostic, but for a narrower reason than /roles and /domains:
        # a Domain Permission grant IS organization-scoped data in the
        # canonical architecture (Master Technical Architecture's
        # domain_permission_registry RLS policy scopes it one-hop via
        # membership_id -> organization_id, unlike Role's/Domain's own
        # genuinely-global-or-nullable org_id). This endpoint is exempted
        # only because its sole caller today is PLATFORM_ADMIN (TD-022 — no
        # Domain Owner/Domain Admin authority model exists yet to scope it
        # more tightly), and PLATFORM_ADMIN already operates across every
        # organization boundary elsewhere in this codebase. This exemption
        # should be revisited once TD-022 is resolved and a real,
        # Domain-scoped authority replaces PLATFORM_ADMIN here.
        # /approval-authorities (WP-02, BA-03 Establish Approval Authority) is
        # tenant-agnostic for the same narrower reason as /domain-permissions:
        # approval_authority_registry.organization_id is required for every
        # scope (including GLOBAL/COMPANY), so this genuinely is
        # organization-scoped data. Exempted only because PLATFORM_ADMIN is
        # the sole caller today (TD-023 — no Corporate Admin/Domain Owner
        # authority model exists yet), the same disposition as TD-022.
        # /delegation-policies (WP-02, BA-04 Establish Delegation Policy) is
        # tenant-agnostic for the identical narrower reason as
        # /approval-authorities: delegation_policy_registry.organization_id
        # is required for every scope (including ORGANIZATION), so this
        # genuinely is organization-scoped data. Exempted only because
        # PLATFORM_ADMIN is the sole caller today (TD-024 — no Corporate
        # Admin/Domain Owner authority model exists yet), the same
        # disposition as TD-022/TD-023.
        # /runtime-assignment-policies (WP-02, BA-05 Establish Runtime
        # Assignment Policy) is tenant-agnostic for the identical narrower
        # reason as /delegation-policies: runtime_assignment_policy_registry.
        # organization_id is required, so this genuinely is
        # organization-scoped data. Exempted only because PLATFORM_ADMIN is
        # the sole caller today (TD-025 — no Corporate Admin/Domain Admin
        # authority model exists yet), the same disposition as
        # TD-022/TD-023/TD-024.
        # /memberships (WP-03, BA-01 Establish Membership Context) is
        # tenant-agnostic for the identical narrower reason as
        # /domain-permissions: a Membership IS organization-scoped data
        # (memberships.organization_id is required). Exempted only because
        # PLATFORM_ADMIN is the sole caller today (TD-031 — no Membership
        # Steward/Sponsor persona authority model exists yet), the same
        # disposition as TD-021/TD-022/TD-023/TD-024/TD-025.
        # /organization-nodes (WP-04, BA-01 Establish Organization Node) is
        # tenant-agnostic for the same reason as /organizations — but more
        # directly: OrganizationNode carries no organization_id column at
        # all anywhere in Master Technical Architecture's own canonical DDL
        # or this table's current shape (IRA-004 §9), so there is no tenant
        # column to scope by, not merely a PLATFORM_ADMIN-operates-across-
        # tenants argument as with /organizations.
        # /organization-establishment-attempts (IRA-001A, BA-01 amended /
        # BA-01B / BA-01C) is tenant-agnostic for the identical reason as
        # /organization-nodes: an Organization Establishment Attempt
        # carries no organization_id column — it exists prior to any
        # Organization, tenant or otherwise.
        # /structural-change-intents (WP-04, BA-03 Frame Structural Change
        # Intent; SCI-000001, ADR-006, IRA-004 §21) is tenant-agnostic for
        # the identical reason as /organization-nodes: a Structural Change
        # Intent carries no organization_id column anywhere in its own
        # model (models/structural_change_intent.py) — it is an
        # enterprise-structure-level construct, not organization-scoped
        # data.
        # /structural-proposals (WP-04, BA-04 Shape/Refine Proposed
        # Structural Outcome; POC-000001, ADR-008, IRA-004 §22) is
        # tenant-agnostic for the identical reason as
        # /structural-change-intents: a Structural Proposal carries no
        # organization_id column anywhere in its own model
        # (models/structural_proposal.py).
        # /impact-assessments (WP-04, BA-05 Assess Structural
        # Consequence; IMC-000001, ADR-009, IRA-004 §23) is
        # tenant-agnostic for the identical reason as
        # /structural-proposals: an Impact Assessment carries no
        # organization_id column anywhere in its own model
        # (models/impact_assessment.py).
        # /structural-reviews (WP-04, BA-06 Review Proposed Structural
        # Outcome / Resolve Structural Review Concerns; RVC-000001,
        # ADR-011, IRA-004 §25) is tenant-agnostic for the identical
        # reason as /impact-assessments: a Structural Review carries no
        # organization_id column anywhere in its own model
        # (models/structural_review.py).
        # /structural-validations (WP-04, BA-07 Validate Transition
        # Readiness; VLC-000001, ADR-012, IRA-004 §26) is
        # tenant-agnostic for the identical reason as
        # /structural-reviews: a Structural Validation carries no
        # organization_id column anywhere in its own model
        # (models/structural_validation.py).
        # /structural-completions (WP-04, BA-08 Complete Structural
        # Transition; RSC-000001, ADR-013, IRA-004 §27) is
        # tenant-agnostic for the identical reason as
        # /structural-validations: a Structural Completion carries no
        # organization_id column anywhere in its own model
        # (models/structural_completion.py).
        # /access-evaluations (WP-05, BA-01 through BA-04; AEO-000001,
        # ADR-015, IRA-005 §12) is tenant-agnostic for the same narrower
        # reason as /domain-permissions: an Access Evaluation Outcome IS
        # organization-scoped data (derived one-hop via membership_id ->
        # organization_id), but is exempted only because PLATFORM_ADMIN
        # is the sole caller today (the same interim gate every prior WP
        # uses, disclosed as its own Technical Debt entry), not because
        # the evaluation itself is tenant-independent.
        # /person (WP-07, C-006 — BA-01 through BA-10) is tenant-agnostic
        # across its entire prefix, not just /recognize and /establish
        # (the original two-entry exact-list this replaces): Person has
        # no organization_id column anywhere in its own model, nor in any
        # of the four new WP-07 tables (person_distinction_decisions,
        # person_reconciliation_decisions, person_corrections,
        # person_enrichments) — URA-001-15 states a Person is "independent
        # of any company, role, license, or permission." This is a
        # stronger basis than /domain-permissions'/access-evaluations' own
        # exemption (each IS organization-scoped data, merely exempted
        # because PLATFORM_ADMIN is the sole caller today): Person is
        # canonically tenant-independent regardless of which role calls
        # it. Prefix-matched, mirroring every other resource's own
        # convention, so no future WP-07 endpoint needs a repeated entry.
        path = request.url.path
        if path in [
            "/health", "/ready", "/docs", "/redoc", "/openapi.json",
            "/auth/login", "/auth/refresh",
        ] or path == "/person" or path.startswith("/person/") \
          or path == "/organizations" or path.startswith("/organizations/") \
          or path == "/roles" or path.startswith("/roles/") \
          or path == "/domains" or path.startswith("/domains/") \
          or path == "/domain-permissions" or path.startswith("/domain-permissions/") \
          or path == "/approval-authorities" or path.startswith("/approval-authorities/") \
          or path == "/delegation-policies" or path.startswith("/delegation-policies/") \
          or path == "/runtime-assignment-policies" or path.startswith("/runtime-assignment-policies/") \
          or path == "/memberships" or path.startswith("/memberships/") \
          or path == "/organization-nodes" or path.startswith("/organization-nodes/") \
          or path == "/organization-establishment-attempts" or path.startswith("/organization-establishment-attempts/") \
          or path == "/structural-change-intents" or path.startswith("/structural-change-intents/") \
          or path == "/structural-proposals" or path.startswith("/structural-proposals/") \
          or path == "/impact-assessments" or path.startswith("/impact-assessments/") \
          or path == "/structural-reviews" or path.startswith("/structural-reviews/") \
          or path == "/structural-validations" or path.startswith("/structural-validations/") \
          or path == "/structural-completions" or path.startswith("/structural-completions/") \
          or path == "/access-evaluations" or path.startswith("/access-evaluations/"):
            return await call_next(request)

        tenant_header = request.headers.get("X-Tenant-ID")

        if not tenant_header:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Header 'X-Tenant-ID' is required to route requests."}
            )

        try:
            tenant_uuid = uuid.UUID(tenant_header)
        except ValueError:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Header 'X-Tenant-ID' must be a valid RFC 4122 UUID."}
            )

        # Set Context Variable for SQLAlchemy automatic filters or logs
        token = tenant_context.set(tenant_uuid)
        request.state.tenant_id = tenant_uuid

        try:
            response = await call_next(request)
        finally:
            tenant_context.reset(token)

        return response


def get_current_tenant() -> uuid.UUID:
    """
    FastAPI dependency injector to obtain active tenant_id context.
    """
    tenant_id = tenant_context.get()
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Active tenant context is unresolved."
        )
    return tenant_id
