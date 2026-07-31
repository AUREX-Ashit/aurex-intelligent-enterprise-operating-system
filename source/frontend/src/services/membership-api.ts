/**
 * Membership API wrapper — the only module permitted to call
 * POST /memberships, GET /memberships/{id}, GET /memberships/my-portfolio,
 * and POST /memberships/{id}/terms. Built on the shared `apiClient`, not
 * raw fetch. Mirrors AuthService's routers/membership.py exactly. No
 * search/list-all endpoint exists for Membership (WP-03 built no such
 * Business Activity), so none is called here.
 */

import { apiClient } from "@/lib/api-client";
import type {
  ChangeMembershipTermsRequest,
  EstablishMembershipRequest,
  MembershipPortfolioResponse,
  MembershipResponse,
  MembershipUnderstandingResponse,
} from "@/types/membership";

export function establishMembership(request: EstablishMembershipRequest): Promise<MembershipResponse> {
  return apiClient.post<MembershipResponse>("/memberships", request);
}

export function understandMembership(membershipId: string): Promise<MembershipUnderstandingResponse> {
  return apiClient.get<MembershipUnderstandingResponse>(`/memberships/${membershipId}`);
}

export function changeMembershipTerms(
  membershipId: string,
  request: ChangeMembershipTermsRequest,
): Promise<MembershipResponse> {
  return apiClient.post<MembershipResponse>(`/memberships/${membershipId}/terms`, request);
}

export function getOwnMembershipPortfolio(): Promise<MembershipPortfolioResponse> {
  return apiClient.get<MembershipPortfolioResponse>("/memberships/my-portfolio");
}
