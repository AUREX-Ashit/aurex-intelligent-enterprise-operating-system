"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import { establishDiscoveryProvider, listDiscoveryProviders } from "@/services/discovery-provider-api";
import type { DiscoveryProviderResponse, EstablishDiscoveryProviderRequest } from "@/types/discovery-provider";

/**
 * WP-14 BA-01 — Establish Discovery Provider Configuration (C-090). Two
 * independent state slices (Establish, List), mirroring
 * useSearchManagement.ts's own precedent: a successful establish also
 * reloads the list slice, so the newly-created provider appears without a
 * manual refresh, the same behavior `establishIndex` already provides.
 */
export type DiscoveryProviderEstablishState =
  | { status: "idle" }
  | { status: "establishing" }
  | { status: "established"; provider: DiscoveryProviderResponse }
  | { status: "establish-error"; message: string };

export type DiscoveryProviderListState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "loaded"; providers: DiscoveryProviderResponse[] }
  | { status: "error"; message: string };

function describeError(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  return "Unable to reach the server. Check your connection and try again.";
}

export function useDiscoveryProviderManagement() {
  const [establishState, setEstablishState] = useState<DiscoveryProviderEstablishState>({ status: "idle" });
  const [listState, setListState] = useState<DiscoveryProviderListState>({ status: "idle" });
  const { notify } = useNotifications();

  const loadProviders = useCallback(async () => {
    setListState({ status: "loading" });
    try {
      const response = await listDiscoveryProviders();
      setListState({ status: "loaded", providers: response.discovery_providers });
    } catch (error) {
      const message = describeError(error);
      if (error instanceof ApiError && error.status === 0) notify(message, "danger");
      setListState({ status: "error", message });
    }
  }, [notify]);

  const establish = useCallback(
    async (request: EstablishDiscoveryProviderRequest) => {
      setEstablishState({ status: "establishing" });
      try {
        const provider = await establishDiscoveryProvider(request);
        setEstablishState({ status: "established", provider });
        notify(`Discovery Provider "${provider.provider_type}" established.`, "success");
        void loadProviders();
      } catch (error) {
        const message = describeError(error);
        if (error instanceof ApiError && error.status === 0) notify(message, "danger");
        setEstablishState({ status: "establish-error", message });
      }
    },
    [notify, loadProviders],
  );

  return { establishState, listState, establish, loadProviders };
}
