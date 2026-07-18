"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import { recognizePerson, establishPerson } from "@/services/person-api";
import type { AuthoritativePersonContext, EstablishPersonRequest } from "@/types/person";

/**
 * Single owner of Person Management's business-flow state (Sections 1/2,
 * States 1–5). Form components own only their own transient input values
 * while typing; everything about what was recognized/established, and any
 * error from doing so, lives here exactly once.
 */
export type PersonManagementState =
  | { status: "idle" }
  | { status: "recognizing"; email: string }
  | { status: "matched"; email: string; person: AuthoritativePersonContext }
  | { status: "no-candidate"; email: string }
  | { status: "establishing"; email: string }
  | { status: "established"; email: string; person: AuthoritativePersonContext }
  | { status: "recognize-error"; email: string; message: string }
  | { status: "establish-error"; email: string; message: string };

function describeError(error: unknown): { message: string; isNetworkError: boolean } {
  if (error instanceof ApiError) {
    return { message: error.message, isNetworkError: error.status === 0 };
  }
  return {
    message: "Unable to reach the server. Check your connection and try again.",
    isNetworkError: true,
  };
}

export function usePersonManagement() {
  const [state, setState] = useState<PersonManagementState>({ status: "idle" });
  const { notify } = useNotifications();

  const recognize = useCallback(
    async (email: string) => {
      setState({ status: "recognizing", email });

      try {
        const result = await recognizePerson({ email });

        if (result.outcome === "MATCHED") {
          if (!result.person) {
            // Contract violation, not a normal outcome — surfaced distinctly
            // rather than silently treated as no-candidate.
            setState({
              status: "recognize-error",
              email,
              message: "Recognition reported a match but returned no person data.",
            });
            return;
          }
          setState({ status: "matched", email, person: result.person });
          return;
        }

        setState({ status: "no-candidate", email });
      } catch (error) {
        const { message, isNetworkError } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setState({ status: "recognize-error", email, message });
      }
    },
    [notify],
  );

  const establish = useCallback(
    async (fields: Omit<EstablishPersonRequest, "email">) => {
      if (state.status !== "no-candidate" && state.status !== "establish-error") {
        return;
      }
      const email = state.email;
      setState({ status: "establishing", email });

      try {
        const person = await establishPerson({ email, ...fields });
        setState({ status: "established", email, person });
        notify("Person successfully established.", "success");
      } catch (error) {
        const { message, isNetworkError } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setState({ status: "establish-error", email, message });
      }
    },
    [state, notify],
  );

  const reset = useCallback(() => setState({ status: "idle" }), []);

  return { state, recognize, establish, reset };
}
