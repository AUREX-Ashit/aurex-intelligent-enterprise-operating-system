"use client";

import { useCallback, useState } from "react";
import { useRouter } from "next/navigation";
import { ApiError } from "@/lib/api-client";
import { authStorage } from "@/lib/auth-storage";
import { useNotifications } from "@/lib/notifications";
import { login as loginRequest } from "@/services/auth-api";
import { isOrganizationSelectionResponse } from "@/types/auth";
import type { OrganizationOption } from "@/types/auth";
import { ADMIN_WORKSPACE_ROOT } from "@/config/admin-navigation";

/**
 * Single owner of the Platform Administrator login flow's state, mirroring
 * the R-001 authentication flow exactly: submit email/password, land on
 * a token (redirect) or an organization-selection prompt (re-submit with
 * the chosen organization), never anything else.
 */
export type LoginState =
  | { status: "idle" }
  | { status: "submitting" }
  | { status: "selecting-organization"; email: string; password: string; organizations: OrganizationOption[] }
  | { status: "error"; message: string };

function describeError(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  return "Unable to reach the server. Check your connection and try again.";
}

export function useLogin() {
  const [state, setState] = useState<LoginState>({ status: "idle" });
  const { notify } = useNotifications();
  const router = useRouter();

  const completeLogin = useCallback(
    (accessToken: string) => {
      authStorage.setToken(accessToken);
      notify("Signed in.", "success");
      router.push(ADMIN_WORKSPACE_ROOT);
    },
    [notify, router],
  );

  const submit = useCallback(
    async (email: string, password: string) => {
      setState({ status: "submitting" });

      try {
        const response = await loginRequest({ email, password });

        if (isOrganizationSelectionResponse(response)) {
          setState({
            status: "selecting-organization",
            email,
            password,
            organizations: response.organizations,
          });
          return;
        }

        completeLogin(response.access_token);
      } catch (error) {
        setState({ status: "error", message: describeError(error) });
      }
    },
    [completeLogin],
  );

  const selectOrganization = useCallback(
    async (organizationId: string) => {
      if (state.status !== "selecting-organization") return;
      const { email, password } = state;
      setState({ status: "submitting" });

      try {
        const response = await loginRequest({ email, password }, organizationId);

        if (isOrganizationSelectionResponse(response)) {
          setState({
            status: "selecting-organization",
            email,
            password,
            organizations: response.organizations,
          });
          return;
        }

        completeLogin(response.access_token);
      } catch (error) {
        setState({ status: "error", message: describeError(error) });
      }
    },
    [state, completeLogin],
  );

  const reset = useCallback(() => setState({ status: "idle" }), []);

  return { state, submit, selectOrganization, reset };
}
