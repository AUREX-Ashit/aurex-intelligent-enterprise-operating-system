"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import { establishDomainPermission } from "@/services/domain-permission-api";
import type { DomainPermissionResponse, EstablishDomainPermissionRequest } from "@/types/domain-permission";

export type EstablishDomainPermissionState =
  | { status: "idle" }
  | { status: "establishing" }
  | { status: "established"; domainPermission: DomainPermissionResponse }
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

export function useEstablishDomainPermission() {
  const [state, setState] = useState<EstablishDomainPermissionState>({ status: "idle" });
  const { notify } = useNotifications();

  const establish = useCallback(
    async (fields: EstablishDomainPermissionRequest) => {
      setState({ status: "establishing" });
      try {
        const domainPermission = await establishDomainPermission(fields);
        setState({ status: "established", domainPermission });
        notify("Domain permission successfully established.", "success");
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
