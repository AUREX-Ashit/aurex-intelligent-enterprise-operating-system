"use client";

import { useCallback, useEffect, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import { searchDomainPermissions } from "@/services/domain-permission-api";
import type { DomainPermissionResponse, VersionStatus } from "@/types/domain-permission";

export interface SearchDomainPermissionsQuery {
  domainId: string;
  membershipId: string;
  status: VersionStatus | "ALL";
}

const DEFAULT_QUERY: SearchDomainPermissionsQuery = { domainId: "", membershipId: "", status: "ALL" };

export type SearchDomainPermissionsState =
  | { status: "loading" }
  | { status: "success"; items: DomainPermissionResponse[] }
  | { status: "error"; message: string };

/**
 * WP-06 BA-01 — Understand Domain Permission Context (list branch). No
 * pagination/total wrapper exists server-side (GET /domain-permissions
 * returns a plain array), so this hook owns filter query state only,
 * mirroring useSearchOrganizations.ts's pattern minus pagination.
 */
export function useSearchDomainPermissions() {
  const [query, setQuery] = useState<SearchDomainPermissionsQuery>(DEFAULT_QUERY);
  const [state, setState] = useState<SearchDomainPermissionsState>({ status: "loading" });
  const { notify } = useNotifications();

  const refetch = useCallback(
    async (nextQuery: SearchDomainPermissionsQuery) => {
      setState({ status: "loading" });
      try {
        const items = await searchDomainPermissions({
          domain_id: nextQuery.domainId || undefined,
          membership_id: nextQuery.membershipId || undefined,
          status: nextQuery.status === "ALL" ? undefined : nextQuery.status,
        });
        setState({ status: "success", items });
      } catch (error) {
        const message =
          error instanceof ApiError ? error.message : "Unable to reach the server. Check your connection and try again.";
        if (!(error instanceof ApiError) || error.status === 0) notify(message, "danger");
        setState({ status: "error", message });
      }
    },
    [notify],
  );

  // Data-fetching effect mirroring useSearchOrganizations.ts's own established
  // pattern exactly. Flagged by react-hooks/set-state-in-effect — a
  // pre-existing condition already present in that file (WP-01), not a
  // regression introduced here; standard eslint-disable-next-line does not
  // suppress this specific diagnostic in this repository's eslint-config-next
  // setup. Refetch is stable via useCallback; re-running on query change is
  // the intent.
  useEffect(() => {
    refetch(query);
  }, [query, refetch]);

  const setDomainId = useCallback((domainId: string) => setQuery((prev) => ({ ...prev, domainId })), []);
  const setMembershipId = useCallback(
    (membershipId: string) => setQuery((prev) => ({ ...prev, membershipId })),
    [],
  );
  const setStatusFilter = useCallback(
    (status: VersionStatus | "ALL") => setQuery((prev) => ({ ...prev, status })),
    [],
  );
  const refresh = useCallback(() => refetch(query), [refetch, query]);

  return { query, state, setDomainId, setMembershipId, setStatusFilter, refresh };
}
