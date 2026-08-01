from datetime import datetime
from enum import Enum
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


class WorkspaceContextStatus(str, Enum):
    """
    EX-C008-10's own two-outcome resolution result, mirrored in shape
    from IdentityContextStatus (WP-08 BA-01) but deliberately a distinct
    enum — a governed C-008 concept, not a re-labelled C-001 one, per
    this repository's own precedent of one classification enum per
    governing capability (e.g. IdentityHandoffClassification vs.
    AuthorizationPolicyHandoff's own analogous-but-distinct enum).
    """
    CURRENT = "CURRENT"
    UNRESOLVED = "UNRESOLVED"


class WorkspaceStatusResponse(BaseModel):
    """
    Response for BA-02 — Detect and Resolve Disrupted Workspace Context
    (EX-C008-10). Re-confirms the Membership and structural placement
    underlying the caller's own current session Workspace Context remain
    valid, per IRA-009 §5 — never a silent 200 with stale data: even a
    deactivated or removed Membership resolves to UNRESOLVED (200), not
    a 404, since detecting exactly that disruption is this Business
    Activity's own purpose (IRA-009 §5's own testing note). membership_id
    and organization_id are always echoed back from the caller's own
    session claims, independent of whether the underlying row still
    exists — naming what was checked, not what was found.
    """
    membership_id: UUID
    organization_id: UUID
    status: WorkspaceContextStatus
    checked_at: datetime

    model_config = {"from_attributes": True}
