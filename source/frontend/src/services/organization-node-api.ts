/**
 * Organization Node API wrapper — the only module permitted to call
 * POST /organization-nodes and GET /organization-nodes/{id}. Built on the
 * shared `apiClient`, not raw fetch. Mirrors AuthService's
 * routers/organization_node.py exactly. No search/list-all endpoint
 * exists yet (WP-04 built Establish and Understand Structural Position
 * only), so none is called here.
 */

import { apiClient } from "@/lib/api-client";
import type { EstablishOrganizationNodeRequest, OrganizationNodeResponse } from "@/types/organization-node";

export function establishOrganizationNode(
  request: EstablishOrganizationNodeRequest,
): Promise<OrganizationNodeResponse> {
  return apiClient.post<OrganizationNodeResponse>("/organization-nodes", request);
}

export function getOrganizationNode(organizationNodeId: string): Promise<OrganizationNodeResponse> {
  return apiClient.get<OrganizationNodeResponse>(`/organization-nodes/${organizationNodeId}`);
}
