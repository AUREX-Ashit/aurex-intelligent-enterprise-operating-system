/**
 * Organization API wrapper — the only module permitted to call
 * POST /organizations, GET /organizations, and GET /organizations/{id}.
 * Built on the shared `apiClient`, not raw fetch. Mirrors AuthService's
 * routers/organization.py exactly. The bearer token is attached
 * automatically by apiClient's tokenProvider (see src/app/providers.tsx)
 * — every endpoint here requires the PLATFORM_ADMIN role, enforced
 * server-side.
 */

import { apiClient } from "@/lib/api-client";
import type {
  EstablishOrganizationRequest,
  OrganizationListResponse,
  OrganizationResponse,
  SearchOrganizationsParams,
} from "@/types/organization";

export function establishOrganization(
  request: EstablishOrganizationRequest,
): Promise<OrganizationResponse> {
  return apiClient.post<OrganizationResponse>("/organizations", request);
}

export function getOrganization(organizationId: string): Promise<OrganizationResponse> {
  return apiClient.get<OrganizationResponse>(`/organizations/${organizationId}`);
}

export function searchOrganizations(
  params: SearchOrganizationsParams = {},
): Promise<OrganizationListResponse> {
  const query = new URLSearchParams();
  if (params.q) query.set("q", params.q);
  if (params.status) query.set("status", params.status);
  if (params.skip !== undefined) query.set("skip", String(params.skip));
  if (params.limit !== undefined) query.set("limit", String(params.limit));
  if (params.sort_by) query.set("sort_by", params.sort_by);
  if (params.sort_order) query.set("sort_order", params.sort_order);

  const queryString = query.toString();
  return apiClient.get<OrganizationListResponse>(
    `/organizations${queryString ? `?${queryString}` : ""}`,
  );
}
