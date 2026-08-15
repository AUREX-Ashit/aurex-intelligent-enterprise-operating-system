/**
 * Intelligence Candidate API wrapper — the only module permitted to call
 * AIService's `/intelligence-candidates/*` endpoints. Mirrors AIService's
 * routers/intelligence_candidates.py exactly (WP-14 BA-02/BA-03, C-090).
 * No list/get endpoint exists — IRA-014 §6 names only POST (register) and
 * POST .../{id}/resolve for this resource. Every call targets
 * `appConfig.aiServiceUrl`, mirroring src/services/discovery-provider-api.ts's
 * own established precedent for an AIService-hosted domain.
 */

import { apiClient } from "@/lib/api-client";
import { appConfig } from "@/lib/config";
import type {
  IntelligenceCandidateResponse,
  RegisterIntelligenceCandidateRequest,
  ResolveIntelligenceCandidateRequest,
  ResolvedIntelligenceCandidateResponse,
} from "@/types/intelligence-candidate";

const baseUrl = appConfig.aiServiceUrl;

export function registerIntelligenceCandidate(
  request: RegisterIntelligenceCandidateRequest,
): Promise<IntelligenceCandidateResponse> {
  return apiClient.post<IntelligenceCandidateResponse>("/intelligence-candidates", request, { baseUrl });
}

export function resolveIntelligenceCandidate(
  unclassifiedId: string,
  request: ResolveIntelligenceCandidateRequest,
): Promise<ResolvedIntelligenceCandidateResponse> {
  return apiClient.post<ResolvedIntelligenceCandidateResponse>(
    `/intelligence-candidates/${unclassifiedId}/resolve`,
    request,
    { baseUrl },
  );
}
