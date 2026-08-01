from uuid import UUID

from pydantic import BaseModel, Field


class WorkspaceCandidate(BaseModel):
    """
    A single candidate Workspace Context, resolved from one of the
    caller's own active Memberships (WP-09 BA-01, EX-C008-01/02).

    Per BR-C008-01a, this does not determine which PE-001 §13.5
    Workspace Type(s) the structural anchor (organization_id,
    home_node_id) may host — Pending Canonical Binding, disclosed in
    the WP-09 charter's own Out of Scope. Candidates are returned keyed
    to their structural anchor only, not as a governed Workspace Context
    (that transition is ERB-C008-02, excluded from this Work Package's
    scope per IRA-009 §4.2).
    """
    membership_id: UUID
    organization_id: UUID
    organization_name: str
    role_code: str
    role_name: str
    home_node_id: UUID | None = Field(
        None, description="URA-001-17b/ERG-001-03 home-node anchor. Nullable per TD-032 — no Business Activity anywhere establishes an OrganizationNode row today."
    )
    is_primary: bool

    model_config = {"from_attributes": True}


class WorkspaceCandidatesResponse(BaseModel):
    """
    Response for BA-01 — Resolve and Present Available Workspace
    Candidates (EX-C008-01/02). Read-only discovery, distinct from
    governed Workspace entry (ERB-C008-02, excluded from this Work
    Package's scope, IRA-009 §4.2).
    """
    candidates: list[WorkspaceCandidate]
