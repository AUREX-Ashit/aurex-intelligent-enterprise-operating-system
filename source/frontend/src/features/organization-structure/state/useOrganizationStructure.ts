"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import { establishOrganizationNode, getOrganizationNode } from "@/services/organization-node-api";
import type { EstablishOrganizationNodeRequest, OrganizationNodeResponse } from "@/types/organization-node";

/**
 * Single owner of Enterprise Structure's business-flow state (Establish
 * Organization Node, Understand Structural Position), mirroring
 * useMembershipManagement.ts's combined-hook pattern.
 */
export type OrganizationStructureState =
  | { status: "idle" }
  | { status: "establishing" }
  | { status: "established"; node: OrganizationNodeResponse }
  | { status: "establish-error"; message: string; isConflict: boolean }
  | { status: "viewing" }
  | { status: "viewed"; node: OrganizationNodeResponse }
  | { status: "view-not-found" }
  | { status: "view-error"; message: string };

function describeError(error: unknown): { message: string; isNetworkError: boolean; status: number } {
  if (error instanceof ApiError) {
    return { message: error.message, isNetworkError: error.status === 0, status: error.status };
  }
  return {
    message: "Unable to reach the server. Check your connection and try again.",
    isNetworkError: true,
    status: 0,
  };
}

export function useOrganizationStructure() {
  const [state, setState] = useState<OrganizationStructureState>({ status: "idle" });
  const { notify } = useNotifications();

  const establish = useCallback(
    async (fields: EstablishOrganizationNodeRequest) => {
      setState({ status: "establishing" });
      try {
        const node = await establishOrganizationNode(fields);
        setState({ status: "established", node });
        notify("Organization node successfully established.", "success");
      } catch (error) {
        const { message, isNetworkError, status } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setState({ status: "establish-error", message, isConflict: status === 409 });
      }
    },
    [notify],
  );

  const view = useCallback(
    async (organizationNodeId: string) => {
      setState({ status: "viewing" });
      try {
        const node = await getOrganizationNode(organizationNodeId);
        setState({ status: "viewed", node });
      } catch (error) {
        const { message, isNetworkError, status } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setState(status === 404 ? { status: "view-not-found" } : { status: "view-error", message });
      }
    },
    [notify],
  );

  const reset = useCallback(() => setState({ status: "idle" }), []);

  return { state, establish, view, reset };
}
