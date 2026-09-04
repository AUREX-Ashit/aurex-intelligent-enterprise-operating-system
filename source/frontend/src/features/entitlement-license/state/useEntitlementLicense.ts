"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import {
  establishEntitlementLicenseContext,
  getEntitlementLicenseOutcome,
} from "@/services/entitlement-license-api";
import type {
  ContextOutcomeResponse,
  EstablishEntitlementLicenseRequest,
  EstablishEntitlementLicenseResponse,
} from "@/types/entitlement-license";

/**
 * C-023 WP-17 BA-01 state — two independent slices for the two authorized
 * frontend items (TDS-C023 §17): Establish, and Display Resulting Outcome.
 * Independent slices (mirroring useMembershipManagement.ts) so acting in
 * one section never blanks the other's last result.
 */
export type EstablishState =
  | { status: "idle" }
  | { status: "establishing" }
  | { status: "established"; result: EstablishEntitlementLicenseResponse }
  | { status: "error"; message: string; isConflict: boolean; isAuthDenied: boolean };

export type OutcomeState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "loaded"; outcome: ContextOutcomeResponse }
  | { status: "not-found" }
  | { status: "error"; message: string };

function describeError(error: unknown): {
  message: string;
  isNetworkError: boolean;
  status: number;
} {
  if (error instanceof ApiError) {
    return { message: error.message, isNetworkError: error.status === 0, status: error.status };
  }
  return {
    message: "Unable to reach the server. Check your connection and try again.",
    isNetworkError: true,
    status: 0,
  };
}

export function useEntitlementLicense() {
  const [establishState, setEstablishState] = useState<EstablishState>({ status: "idle" });
  const [outcomeState, setOutcomeState] = useState<OutcomeState>({ status: "idle" });
  const { notify } = useNotifications();

  const establish = useCallback(
    async (fields: EstablishEntitlementLicenseRequest) => {
      setEstablishState({ status: "establishing" });
      try {
        const result = await establishEntitlementLicenseContext(fields);
        setEstablishState({ status: "established", result });
        notify("Authoritative Entitlement/License Context established.", "success");
      } catch (error) {
        const { message, isNetworkError, status } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setEstablishState({
          status: "error",
          message,
          isConflict: status === 409,
          isAuthDenied: status === 403,
        });
      }
    },
    [notify],
  );

  const loadOutcome = useCallback(
    async (contextId: string) => {
      setOutcomeState({ status: "loading" });
      try {
        const outcome = await getEntitlementLicenseOutcome(contextId);
        setOutcomeState({ status: "loaded", outcome });
      } catch (error) {
        const { message, isNetworkError, status } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setOutcomeState(status === 404 ? { status: "not-found" } : { status: "error", message });
      }
    },
    [notify],
  );

  const reset = useCallback(() => {
    setEstablishState({ status: "idle" });
    setOutcomeState({ status: "idle" });
  }, []);

  return { establishState, outcomeState, establish, loadOutcome, reset };
}
