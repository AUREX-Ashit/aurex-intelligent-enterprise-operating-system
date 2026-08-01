"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import { refreshWorkspaceStatus } from "@/services/workspace-api";
import type { WorkspaceStatusResponse } from "@/types/workspace";

/**
 * Single owner of Workspace disruption self-check state (WP-09 BA-02,
 * EX-C008-10), mirroring useIdentityManagement.ts's own "checking-status"
 * slice exactly. Per IRA-009 §7, this Enterprise Experience is
 * diagnostic — "likely surfaced only diagnostically, not as a primary
 * user-facing action" — so this hook is a standalone, composable unit
 * rather than being forced into WorkspaceSwitcher.tsx (BA-01's own
 * already-completed, already-approved implementation, not revisited
 * here).
 */
export type WorkspaceStatusState =
  | { status: "idle" }
  | { status: "checking" }
  | { status: "checked"; result: WorkspaceStatusResponse }
  | { status: "check-error"; message: string };

function describeError(error: unknown): { message: string; isNetworkError: boolean } {
  if (error instanceof ApiError) {
    return { message: error.message, isNetworkError: error.status === 0 };
  }
  return {
    message: "Unable to reach the server. Check your connection and try again.",
    isNetworkError: true,
  };
}

export function useWorkspaceStatus() {
  const [state, setState] = useState<WorkspaceStatusState>({ status: "idle" });
  const { notify } = useNotifications();

  const checkStatus = useCallback(async () => {
    setState({ status: "checking" });

    try {
      const result = await refreshWorkspaceStatus();
      setState({ status: "checked", result });
      if (result.status === "UNRESOLVED") {
        notify("Your current Workspace context could not be re-confirmed.", "warning");
      }
    } catch (error) {
      const { message, isNetworkError } = describeError(error);
      if (isNetworkError) notify(message, "danger");
      setState({ status: "check-error", message });
    }
  }, [notify]);

  return { state, checkStatus };
}
