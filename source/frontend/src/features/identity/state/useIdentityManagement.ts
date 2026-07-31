"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import { recoverIdentity, refreshIdentityStatus } from "@/services/identity-api";
import type { IdentityRecoveryRequestResponse, IdentityStatusResponse } from "@/types/identity";

/**
 * Single owner of Identity Management's business-flow state (BA-01
 * refresh-status, BA-02 recover), mirroring usePersonManagement.ts's own
 * pattern exactly: form components own only their own transient input
 * values while typing; everything about the outcome, and any error from
 * producing it, lives here exactly once.
 */
export type IdentityManagementState =
  | { status: "idle" }
  | { status: "checking-status" }
  | { status: "status-checked"; result: IdentityStatusResponse }
  | { status: "status-error"; message: string }
  | { status: "recovering" }
  | { status: "recovery-requested"; result: IdentityRecoveryRequestResponse }
  | { status: "recovery-error"; message: string };

function describeError(error: unknown): { message: string; isNetworkError: boolean } {
  if (error instanceof ApiError) {
    return { message: error.message, isNetworkError: error.status === 0 };
  }
  return {
    message: "Unable to reach the server. Check your connection and try again.",
    isNetworkError: true,
  };
}

export function useIdentityManagement() {
  const [state, setState] = useState<IdentityManagementState>({ status: "idle" });
  const { notify } = useNotifications();

  const checkStatus = useCallback(async () => {
    setState({ status: "checking-status" });

    try {
      const result = await refreshIdentityStatus();
      setState({ status: "status-checked", result });
    } catch (error) {
      const { message, isNetworkError } = describeError(error);
      if (isNetworkError) notify(message, "danger");
      setState({ status: "status-error", message });
    }
  }, [notify]);

  const requestRecovery = useCallback(
    async (personId: string, reason: string) => {
      setState({ status: "recovering" });

      try {
        const result = await recoverIdentity({ person_id: personId, reason });
        setState({ status: "recovery-requested", result });
        notify("Identity recovery request submitted.", "success");
      } catch (error) {
        const { message, isNetworkError } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setState({ status: "recovery-error", message });
      }
    },
    [notify],
  );

  const reset = useCallback(() => setState({ status: "idle" }), []);

  return { state, checkStatus, requestRecovery, reset };
}
