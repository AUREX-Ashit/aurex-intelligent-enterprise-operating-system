/**
 * Organization API wrapper — the only module permitted to call
 * GET /organizations, GET /organizations/{id}, and (since IRA-001A,
 * TD-049) POST /organization-establishment-attempts. Built on the shared
 * `apiClient`, not raw fetch. Mirrors AuthService's routers/organization.py
 * and routers/organization_establishment_attempt.py exactly. The bearer
 * token is attached automatically by apiClient's tokenProvider (see
 * src/app/providers.tsx) — every endpoint here requires the
 * PLATFORM_ADMIN role, enforced server-side.
 */

import { apiClient } from "@/lib/api-client";
import type {
  EstablishOrganizationRequest,
  OrganizationEstablishmentAttemptResponse,
  OrganizationListResponse,
  OrganizationResponse,
  SearchOrganizationsParams,
  UpdateOrganizationProfileRequest,
} from "@/types/organization";

/**
 * IRA-001A (TD-049): establishing an Organization is now a two-step,
 * governed backend flow (create the Organization Establishment Attempt,
 * then activate it) — PE-001-C004's BR-C004-01/Contract 5.4 correction.
 * This function still returns Promise<OrganizationResponse>, the exact
 * contract every existing caller (useEstablishOrganization.ts) already
 * expects, by performing both steps internally. The Establish Organization
 * form collects no domain claim, so activation always proceeds via the
 * governed no-domain path (BR-C004-09) with a fixed, honest reason.
 */
export async function establishOrganization(
  request: EstablishOrganizationRequest,
): Promise<OrganizationResponse> {
  const attempt = await apiClient.post<OrganizationEstablishmentAttemptResponse>(
    "/organization-establishment-attempts",
    request,
  );
  return apiClient.post<OrganizationResponse>(
    `/organization-establishment-attempts/${attempt.id}/activate`,
    { no_domain_activation_reason: "No primary domain provided at establishment." },
  );
}

export function getOrganization(organizationId: string): Promise<OrganizationResponse> {
  return apiClient.get<OrganizationResponse>(`/organizations/${organizationId}`);
}

export function updateOrganization(
  organizationId: string,
  request: UpdateOrganizationProfileRequest,
): Promise<OrganizationResponse> {
  return apiClient.put<OrganizationResponse>(`/organizations/${organizationId}`, request);
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
