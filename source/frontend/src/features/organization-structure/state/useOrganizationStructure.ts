"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import { establishOrganizationNode, getOrganizationNode } from "@/services/organization-node-api";
import type { EstablishOrganizationNodeRequest, OrganizationNodeResponse } from "@/types/organization-node";

/**
 * Enterprise Structure's business-flow state, split into two independent
 * slices (Establish, View) rather than one shared discriminated union.
 * OrganizationStructureScreen renders both sections simultaneously (not
 * tabs), so a single shared union previously meant establishing a new node
 * reset `status` out from under the View section (and vice versa),
 * silently blanking an already-displayed result that had nothing to do
 * with the action just taken.
 */
export type OrganizationStructureEstablishState =
  | { status: "idle" }
  | { status: "establishing" }
  | { status: "established"; node: OrganizationNodeResponse }
  | { status: "establish-error"; message: string; isConflict: boolean };

export type OrganizationStructureViewState =
  | { status: "idle" }
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
  const [establishState, setEstablishState] = useState<OrganizationStructureEstablishState>({ status: "idle" });
  const [viewState, setViewState] = useState<OrganizationStructureViewState>({ status: "idle" });
  const { notify } = useNotifications();

  const establish = useCallback(
    async (fields: EstablishOrganizationNodeRequest) => {
      setEstablishState({ status: "establishing" });
      try {
        const node = await establishOrganizationNode(fields);
        setEstablishState({ status: "established", node });
        notify("Organization node successfully established.", "success");
      } catch (error) {
        const { message, isNetworkError, status } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setEstablishState({ status: "establish-error", message, isConflict: status === 409 });
      }
    },
    [notify],
  );

  const view = useCallback(
    async (organizationNodeId: string) => {
      setViewState({ status: "viewing" });
      try {
        const node = await getOrganizationNode(organizationNodeId);
        setViewState({ status: "viewed", node });
      } catch (error) {
        const { message, isNetworkError, status } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setViewState(status === 404 ? { status: "view-not-found" } : { status: "view-error", message });
      }
    },
    [notify],
  );

  const reset = useCallback(() => {
    setEstablishState({ status: "idle" });
    setViewState({ status: "idle" });
  }, []);

  return { establishState, viewState, establish, view, reset };
}
