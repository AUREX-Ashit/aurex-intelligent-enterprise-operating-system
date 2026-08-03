"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import {
  establishIndexConfiguration,
  executeSearch as executeSearchRequest,
  listIndexConfigurations,
  registerSearchContent,
} from "@/services/search-api";
import type {
  EstablishIndexConfigurationRequest,
  ExecuteSearchRequest,
  IndexConfigurationResponse,
  RegisterContentRequest,
  RegisteredContentResponse,
  SearchResponse,
} from "@/types/search";

/**
 * WP-11 — Enterprise Search (C-093). Four independent state slices
 * (Establish Index, Index List, Register Content, Execute Search),
 * mirroring useConfigurationManagement.ts's own precedent: acting on one
 * must never blank an already-loaded slice of another.
 */
export type IndexEstablishState =
  | { status: "idle" }
  | { status: "establishing" }
  | { status: "established"; index: IndexConfigurationResponse }
  | { status: "establish-error"; message: string };

export type IndexListState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "loaded"; indexConfigurations: IndexConfigurationResponse[] }
  | { status: "error"; message: string };

export type RegisterContentState =
  | { status: "idle" }
  | { status: "registering" }
  | { status: "registered"; result: RegisteredContentResponse }
  | { status: "register-error"; message: string };

export type SearchQueryState =
  | { status: "idle" }
  | { status: "searching" }
  | { status: "searched"; response: SearchResponse }
  | { status: "search-error"; message: string };

function describeError(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  return "Unable to reach the server. Check your connection and try again.";
}

export function useSearchManagement() {
  const [establishState, setEstablishState] = useState<IndexEstablishState>({ status: "idle" });
  const [listState, setListState] = useState<IndexListState>({ status: "idle" });
  const [registerState, setRegisterState] = useState<RegisterContentState>({ status: "idle" });
  const [searchState, setSearchState] = useState<SearchQueryState>({ status: "idle" });
  const { notify } = useNotifications();

  const loadIndexConfigurations = useCallback(async () => {
    setListState({ status: "loading" });
    try {
      const response = await listIndexConfigurations();
      setListState({ status: "loaded", indexConfigurations: response.index_configurations });
    } catch (error) {
      const message = describeError(error);
      if (error instanceof ApiError && error.status === 0) notify(message, "danger");
      setListState({ status: "error", message });
    }
  }, [notify]);

  const establishIndex = useCallback(
    async (request: EstablishIndexConfigurationRequest) => {
      setEstablishState({ status: "establishing" });
      try {
        const index = await establishIndexConfiguration(request);
        setEstablishState({ status: "established", index });
        notify(`Search index "${index.index_name}" established.`, "success");
        void loadIndexConfigurations();
      } catch (error) {
        const message = describeError(error);
        if (error instanceof ApiError && error.status === 0) notify(message, "danger");
        setEstablishState({ status: "establish-error", message });
      }
    },
    [notify, loadIndexConfigurations],
  );

  const registerContent = useCallback(
    async (request: RegisterContentRequest) => {
      setRegisterState({ status: "registering" });
      try {
        const result = await registerSearchContent(request);
        setRegisterState({ status: "registered", result });
        notify(`Registered ${result.chunk_count} chunk(s) as searchable content.`, "success");
      } catch (error) {
        const message = describeError(error);
        if (error instanceof ApiError && error.status === 0) notify(message, "danger");
        setRegisterState({ status: "register-error", message });
      }
    },
    [notify],
  );

  const executeSearch = useCallback(
    async (request: ExecuteSearchRequest) => {
      setSearchState({ status: "searching" });
      try {
        const response = await executeSearchRequest(request);
        setSearchState({ status: "searched", response });
      } catch (error) {
        const message = describeError(error);
        if (error instanceof ApiError && error.status === 0) notify(message, "danger");
        setSearchState({ status: "search-error", message });
      }
    },
    [notify],
  );

  return {
    establishState,
    listState,
    registerState,
    searchState,
    establishIndex,
    loadIndexConfigurations,
    registerContent,
    executeSearch,
  };
}
