"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import { establishRole } from "@/services/role-api";
import type { EstablishRoleRequest, RoleResponse } from "@/types/role";

export type EstablishRoleState =
  | { status: "idle" }
  | { status: "establishing" }
  | { status: "established"; role: RoleResponse }
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

export function useEstablishRole() {
  const [state, setState] = useState<EstablishRoleState>({ status: "idle" });
  const { notify } = useNotifications();

  const establish = useCallback(
    async (fields: EstablishRoleRequest) => {
      setState({ status: "establishing" });
      try {
        const role = await establishRole(fields);
        setState({ status: "established", role });
        notify("Role successfully established.", "success");
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
