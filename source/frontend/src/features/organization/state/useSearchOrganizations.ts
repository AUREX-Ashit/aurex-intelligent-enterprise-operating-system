"use client";

import { useCallback, useEffect, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import { searchOrganizations } from "@/services/organization-api";
import type {
  OrganizationResponse,
  OrganizationSortField,
  OrganizationStatus,
  SortOrder,
} from "@/types/organization";

const DEFAULT_LIMIT = 20;

export interface SearchOrganizationsQuery {
  q: string;
  status: OrganizationStatus | "ALL";
  skip: number;
  limit: number;
  sortBy: OrganizationSortField;
  sortOrder: SortOrder;
}

const DEFAULT_QUERY: SearchOrganizationsQuery = {
  q: "",
  status: "ALL",
  skip: 0,
  limit: DEFAULT_LIMIT,
  sortBy: "organization_name",
  sortOrder: "asc",
};

export type SearchOrganizationsState =
  | { status: "loading" }
  | { status: "success"; items: OrganizationResponse[]; total: number }
  | { status: "error"; message: string };

/**
 * BA-03: Search & List Organizations state — owns the query parameters
 * (search text, status filter, pagination, sort) and the resulting page,
 * mirroring useEstablishOrganization.ts / useViewOrganization.ts's
 * pattern (BA-01/BA-02). Fetches on mount and whenever the query changes.
 */
export function useSearchOrganizations() {
  const [query, setQuery] = useState<SearchOrganizationsQuery>(DEFAULT_QUERY);
  const [state, setState] = useState<SearchOrganizationsState>({ status: "loading" });
  const { notify } = useNotifications();

  const refetch = useCallback(
    async (nextQuery: SearchOrganizationsQuery) => {
      setState({ status: "loading" });
      try {
        const result = await searchOrganizations({
          q: nextQuery.q || undefined,
          status: nextQuery.status === "ALL" ? undefined : nextQuery.status,
          skip: nextQuery.skip,
          limit: nextQuery.limit,
          sort_by: nextQuery.sortBy,
          sort_order: nextQuery.sortOrder,
        });
        setState({ status: "success", items: result.items, total: result.total });
      } catch (error) {
        const message =
          error instanceof ApiError ? error.message : "Unable to reach the server. Check your connection and try again.";
        if (!(error instanceof ApiError) || error.status === 0) notify(message, "danger");
        setState({ status: "error", message });
      }
    },
    [notify],
  );

  // eslint-disable-next-line react-hooks/exhaustive-deps -- refetch is stable via useCallback; re-running on query change is the intent
  useEffect(() => {
    refetch(query);
  }, [query, refetch]);

  const setSearchText = useCallback((q: string) => setQuery((prev) => ({ ...prev, q, skip: 0 })), []);
  const setStatusFilter = useCallback(
    (status: OrganizationStatus | "ALL") => setQuery((prev) => ({ ...prev, status, skip: 0 })),
    [],
  );
  const setSort = useCallback(
    (sortBy: OrganizationSortField, sortOrder: SortOrder) =>
      setQuery((prev) => ({ ...prev, sortBy, sortOrder, skip: 0 })),
    [],
  );
  const nextPage = useCallback(
    () => setQuery((prev) => ({ ...prev, skip: prev.skip + prev.limit })),
    [],
  );
  const previousPage = useCallback(
    () => setQuery((prev) => ({ ...prev, skip: Math.max(0, prev.skip - prev.limit) })),
    [],
  );
  const refresh = useCallback(() => refetch(query), [refetch, query]);

  return { query, state, setSearchText, setStatusFilter, setSort, nextPage, previousPage, refresh };
}
