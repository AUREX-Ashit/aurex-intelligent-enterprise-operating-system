"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import {
  establishOfferingDefinition,
  getOfferingDefinition,
  listOfferingDefinitions,
} from "@/services/offering-api";
import type {
  EstablishOfferingDefinitionRequest,
  OfferingDefinitionResponse,
} from "@/types/offering";

/**
 * C-021 WP-20 BA-01 state — three independent slices for the three
 * authorized operations (TDS-C021 §13/§14): Establish, List, Read one.
 * Independent slices (mirroring useEntitlementLicense.ts) so acting in one
 * section never blanks another's last result.
 */
export type EstablishState =
  | { status: "idle" }
  | { status: "establishing" }
  | { status: "established"; offering: OfferingDefinitionResponse }
  | { status: "error"; message: string; isConflict: boolean; isAuthDenied: boolean };

export type ListState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "loaded"; offerings: OfferingDefinitionResponse[] }
  | { status: "error"; message: string };

export type DetailState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "loaded"; offering: OfferingDefinitionResponse }
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

export function useOfferingCatalog() {
  const [establishState, setEstablishState] = useState<EstablishState>({ status: "idle" });
  const [listState, setListState] = useState<ListState>({ status: "idle" });
  const [detailState, setDetailState] = useState<DetailState>({ status: "idle" });
  const { notify } = useNotifications();

  const loadList = useCallback(async () => {
    setListState({ status: "loading" });
    try {
      const offerings = await listOfferingDefinitions();
      setListState({ status: "loaded", offerings });
    } catch (error) {
      const { message, isNetworkError } = describeError(error);
      if (isNetworkError) notify(message, "danger");
      setListState({ status: "error", message });
    }
  }, [notify]);

  const establish = useCallback(
    async (fields: EstablishOfferingDefinitionRequest) => {
      setEstablishState({ status: "establishing" });
      try {
        const offering = await establishOfferingDefinition(fields);
        setEstablishState({ status: "established", offering });
        notify(`Offering Definition ${offering.offering_reference} established (draft).`, "success");
        await loadList();
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
    [notify, loadList],
  );

  const loadDetail = useCallback(
    async (offeringId: string) => {
      setDetailState({ status: "loading" });
      try {
        const offering = await getOfferingDefinition(offeringId);
        setDetailState({ status: "loaded", offering });
      } catch (error) {
        const { message, isNetworkError, status } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setDetailState(status === 404 ? { status: "not-found" } : { status: "error", message });
      }
    },
    [notify],
  );

  const reset = useCallback(() => {
    setEstablishState({ status: "idle" });
    setDetailState({ status: "idle" });
  }, []);

  return { establishState, listState, detailState, establish, loadList, loadDetail, reset };
}
