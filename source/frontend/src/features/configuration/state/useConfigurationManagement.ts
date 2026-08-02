"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import {
  establishConfiguration,
  listConfigurationEntries,
} from "@/services/configuration-api";
import type { ConfigurationEntryResponse, EstablishConfigurationEntryRequest } from "@/types/configuration";

/**
 * WP-10 BA-02 — Establish/Update Enterprise Configuration (EX-C041-02).
 * Two independent state slices (Establish, Entries list), mirroring
 * useMembershipManagement.ts's own precedent: acting on Establish must
 * never blank an already-loaded Entries list, and vice versa.
 */
export type ConfigurationEstablishState =
  | { status: "idle" }
  | { status: "establishing" }
  | { status: "established"; entry: ConfigurationEntryResponse }
  | { status: "establish-error"; message: string };

export type ConfigurationEntriesState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "loaded"; entries: ConfigurationEntryResponse[] }
  | { status: "error"; message: string };

function describeError(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  return "Unable to reach the server. Check your connection and try again.";
}

export function useConfigurationManagement() {
  const [establishState, setEstablishState] = useState<ConfigurationEstablishState>({ status: "idle" });
  const [entriesState, setEntriesState] = useState<ConfigurationEntriesState>({ status: "idle" });
  const { notify } = useNotifications();

  const loadEntries = useCallback(async () => {
    setEntriesState({ status: "loading" });
    try {
      const response = await listConfigurationEntries();
      setEntriesState({ status: "loaded", entries: response.entries });
    } catch (error) {
      const message = describeError(error);
      if (error instanceof ApiError && error.status === 0) notify(message, "danger");
      setEntriesState({ status: "error", message });
    }
  }, [notify]);

  const establish = useCallback(
    async (request: EstablishConfigurationEntryRequest) => {
      setEstablishState({ status: "establishing" });
      try {
        const entry = await establishConfiguration(request);
        setEstablishState({ status: "established", entry });
        notify(`Configuration "${entry.key}" established for ${entry.facet}.`, "success");
        void loadEntries();
      } catch (error) {
        const message = describeError(error);
        if (error instanceof ApiError && error.status === 0) notify(message, "danger");
        setEstablishState({ status: "establish-error", message });
      }
    },
    [notify, loadEntries],
  );

  return { establishState, entriesState, establish, loadEntries };
}
