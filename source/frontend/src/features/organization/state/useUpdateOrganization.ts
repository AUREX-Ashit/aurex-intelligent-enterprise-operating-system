"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import { updateOrganization } from "@/services/organization-api";
import type { OrganizationResponse, UpdateOrganizationProfileRequest } from "@/types/organization";

/**
 * Single owner of Update Organization Profile's state (BA-04), mirroring
 * useEstablishOrganization.ts's pattern (BA-01).
 */
export type UpdateOrganizationState =
  | { status: "idle" }
  | { status: "updating" }
  | { status: "updated"; organization: OrganizationResponse }
  | { status: "error"; message: string; isNotFound: boolean };

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

export function useUpdateOrganization() {
  const [state, setState] = useState<UpdateOrganizationState>({ status: "idle" });
  const { notify } = useNotifications();

  const update = useCallback(
    async (organizationId: string, fields: UpdateOrganizationProfileRequest) => {
      setState({ status: "updating" });

      try {
        const organization = await updateOrganization(organizationId, fields);
        setState({ status: "updated", organization });
        notify("Organization profile updated.", "success");
      } catch (error) {
        const { message, isNetworkError, isNotFound } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setState({ status: "error", message, isNotFound });
      }
    },
    [notify],
  );

  const reset = useCallback(() => setState({ status: "idle" }), []);

  return { state, update, reset };
}
