/**
 * Workspace API wrapper — the only module permitted to call
 * GET /workspaces/candidates and POST /workspaces/refresh-status. Built
 * on the shared `apiClient`, not raw fetch. Mirrors AuthService's
 * routers/workspace.py exactly (WP-09 BA-01/BA-02, EX-C008-01/02/10).
 */

import { apiClient } from "@/lib/api-client";
import type { WorkspaceCandidatesResponse, WorkspaceStatusResponse } from "@/types/workspace";

export function getWorkspaceCandidates(): Promise<WorkspaceCandidatesResponse> {
  return apiClient.get<WorkspaceCandidatesResponse>("/workspaces/candidates");
}

export function refreshWorkspaceStatus(): Promise<WorkspaceStatusResponse> {
  return apiClient.post<WorkspaceStatusResponse>("/workspaces/refresh-status");
}
