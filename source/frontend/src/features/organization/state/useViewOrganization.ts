"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import { getOrganization } from "@/services/organization-api";
import type { OrganizationResponse } from "@/types/organization";

/**
 * Single owner of View Organization Details' state (BA-02), mirroring
 * useEstablishOrganization.ts's pattern (BA-01).
 */
export type ViewOrganizationState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "found"; organization: OrganizationResponse }
  | { status: "not-found" }
  | { status: "error"; message: string };

function describeError(error: unknown): { message: string; isNetworkError: boolean; isNotFound: boolean } {
  if (error instanceof ApiError) {
    return { message: error.message, isNetworkError: error.status === 0, isNotFound: error.status === 404 };
  }
  return {
    message: "Unable to reach the server. Check your connection and try again.",
    isNetworkError: true,
    isNotFound: false,
  };
}

export function useViewOrganization() {
  const [state, setState] = useState<ViewOrganizationState>({ status: "idle" });
  const { notify } = useNotifications();

  const view = useCallback(
    async (organizationId: string) => {
      setState({ status: "loading" });

      try {
        const organization = await getOrganization(organizationId);
        setState({ status: "found", organization });
      } catch (error) {
        const { message, isNetworkError, isNotFound } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setState(isNotFound ? { status: "not-found" } : { status: "error", message });
      }
    },
    [notify],
  );

  const reset = useCallback(() => setState({ status: "idle" }), []);

  return { state, view, reset };
}
