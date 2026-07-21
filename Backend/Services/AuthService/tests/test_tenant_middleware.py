import uuid

from fastapi.testclient import TestClient


def test_tenant_exemption_prefix_matches_organizations_and_subpaths(client: TestClient) -> None:
    """
    TD-001: TenantMiddleware's /organizations/* prefix exemption (added in
    BA-02, generalized from an exact-match list entry to also cover BA-05's
    /activate sub-path without further middleware edits) is tested directly
    here rather than only incidentally through each endpoint's own tests.
    A request with no X-Tenant-ID header to any path under this prefix must
    reach the application itself (an app-level `detail` error/response),
    never the middleware's own `message` "X-Tenant-ID is required" body —
    proving the exemption, independent of which specific endpoint exists.
    """
    exempt_paths = [
        "/organizations",
        f"/organizations/{uuid.uuid4()}",
        f"/organizations/{uuid.uuid4()}/activate",
    ]
    for path in exempt_paths:
        response = client.get(path)  # deliberately no X-Tenant-ID, no Authorization
        body = response.json()
        assert "detail" in body, f"{path} was blocked by TenantMiddleware, not the application ({body})"


def test_tenant_exemption_does_not_over_match_similar_paths(client: TestClient) -> None:
    """
    Guards the prefix-match's specificity (BA-02's own risk note): a path
    that merely starts with the string 'organizations' but is not actually
    under the /organizations/ prefix (no separating slash, not the exact
    "/organizations" path) must still require X-Tenant-ID like any other
    tenant-scoped route.
    """
    response = client.get("/organizationsfoo")

    assert response.status_code == 400
    assert response.json().get("message", "").startswith("Header 'X-Tenant-ID'")
