"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import { establishOrganization } from "@/services/organization-api";
import type { EstablishOrganizationRequest, OrganizationResponse } from "@/types/organization";

/**
 * Single owner of Establish Organization's business-flow state, mirroring
 * usePersonManagement.ts's pattern exactly: the form component owns only
 * its own transient input values; everything about the outcome and any
 * error lives here once.
 */
export type EstablishOrganizationState =
  | { status: "idle" }
  | { status: "establishing" }
  | { status: "established"; organization: OrganizationResponse }
  | { status: "error"; message: string; isConflict: boolean };

function describeError(error: unknown): { message: string; isNetworkError: boolean; isConflict: boolean } {
  if (error instanceof ApiError) {
    return { message: error.message, isNetworkError: error.status === 0, isConflict: error.status === 409 };
  }
  return {
    message: "Unable to reach the server. Check your connection and try again.",
    isNetworkError: true,
    isConflict: false,
  };
}

export function useEstablishOrganization() {
  const [state, setState] = useState<EstablishOrganizationState>({ status: "idle" });
  const { notify } = useNotifications();

  const establish = useCallback(
    async (fields: EstablishOrganizationRequest) => {
      setState({ status: "establishing" });

      try {
        const organization = await establishOrganization(fields);
        setState({ status: "established", organization });
        notify("Organization successfully established.", "success");
      } catch (error) {
        const { message, isNetworkError, isConflict } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setState({ status: "error", message, isConflict });
      }
    },
    [notify],
  );

  const reset = useCallback(() => setState({ status: "idle" }), []);

  return { state, establish, reset };
}
