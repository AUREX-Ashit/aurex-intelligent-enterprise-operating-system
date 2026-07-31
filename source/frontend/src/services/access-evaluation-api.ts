/**
 * Access Evaluation API wrapper — the only module permitted to call
 * POST /access-evaluations. Built on the shared `apiClient`, not raw
 * fetch. Mirrors AuthService's routers/access_evaluation.py's BA-01 only —
 * BA-02 (preserve/expire scope), BA-03 (detect context change), and BA-04
 * (hand-off rejection) are not called here; see
 * AccessEvaluationScreen.tsx's own disclosed scope note.
 */

import { apiClient } from "@/lib/api-client";
import type { AccessEvaluationOutcomeResponse, EvaluateAccessRequest } from "@/types/access-evaluation";

export function evaluateAccess(request: EvaluateAccessRequest): Promise<AccessEvaluationOutcomeResponse> {
  return apiClient.post<AccessEvaluationOutcomeResponse>("/access-evaluations", request);
}
