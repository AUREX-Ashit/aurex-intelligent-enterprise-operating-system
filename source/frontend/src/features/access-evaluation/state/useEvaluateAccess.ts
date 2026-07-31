"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import { evaluateAccess } from "@/services/access-evaluation-api";
import type { AccessEvaluationOutcomeResponse, EvaluateAccessRequest } from "@/types/access-evaluation";

export type EvaluateAccessState =
  | { status: "idle" }
  | { status: "evaluating" }
  | { status: "evaluated"; outcome: AccessEvaluationOutcomeResponse }
  | { status: "error"; message: string; isNotImplemented: boolean };

// A Permitted/Denied determination (as opposed to Unresolved/Deferred) is
// outside this Work Package's authorized scope (IRA-005 S12) and the
// backend returns 501 with an internal governance-reference detail message
// not meant for an end user — the same class of case every other establish
// screen already special-cases via its own `isConflict` (409) branch.
function describeError(error: unknown): { message: string; isNetworkError: boolean; isNotImplemented: boolean } {
  if (error instanceof ApiError) {
    return { message: error.message, isNetworkError: error.status === 0, isNotImplemented: error.status === 501 };
  }
  return {
    message: "Unable to reach the server. Check your connection and try again.",
    isNetworkError: true,
    isNotImplemented: false,
  };
}

export function useEvaluateAccess() {
  const [state, setState] = useState<EvaluateAccessState>({ status: "idle" });
  const { notify } = useNotifications();

  const evaluate = useCallback(
    async (fields: EvaluateAccessRequest) => {
      setState({ status: "evaluating" });
      try {
        const outcome = await evaluateAccess(fields);
        setState({ status: "evaluated", outcome });
        notify(`Access evaluation recorded: ${outcome.outcome_type}.`, "success");
      } catch (error) {
        const { message, isNetworkError, isNotImplemented } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setState({ status: "error", message, isNotImplemented });
      }
    },
    [notify],
  );

  const reset = useCallback(() => setState({ status: "idle" }), []);

  return { state, evaluate, reset };
}
