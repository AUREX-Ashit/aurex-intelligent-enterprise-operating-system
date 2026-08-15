/**
 * Intelligence Candidate API wrapper — the only module permitted to call
 * AIService's `/intelligence-candidates/*` endpoints. Mirrors AIService's
 * routers/intelligence_candidates.py exactly (WP-14 BA-02, C-090). Only a
 * register call exists — no list/get endpoint is built by this Business
 * Activity (IRA-014 §6 names only POST; a resolution/listing surface is
 * BA-03's own scope). Every call targets `appConfig.aiServiceUrl`,
 * mirroring src/services/discovery-provider-api.ts's own established
 * precedent for an AIService-hosted domain.
 */

import { apiClient } from "@/lib/api-client";
import { appConfig } from "@/lib/config";
import type {
  IntelligenceCandidateResponse,
  RegisterIntelligenceCandidateRequest,
} from "@/types/intelligence-candidate";

const baseUrl = appConfig.aiServiceUrl;

export function registerIntelligenceCandidate(
  request: RegisterIntelligenceCandidateRequest,
): Promise<IntelligenceCandidateResponse> {
  return apiClient.post<IntelligenceCandidateResponse>("/intelligence-candidates", request, { baseUrl });
}
