"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import { establishKnowledgeAsset, getKnowledgeAsset } from "@/services/knowledge-asset-api";
import type { EstablishKnowledgeAssetRequest, KnowledgeAssetResponse } from "@/types/knowledge-asset";

/**
 * WP-14 BA-04 — Establish Knowledge Asset (C-091). Two independent state
 * slices (Establish, Retrieve), mirroring useSearchManagement.ts's own
 * precedent: acting on one must never blank an already-loaded slice of
 * the other. Establishing successfully also populates the Retrieve slice
 * directly from the establish response — no extra network round trip is
 * needed to show the resulting status view, but the explicit lookup path
 * (BA-04's own GET endpoint) remains independently available and tested.
 */
export type KnowledgeAssetEstablishState =
  | { status: "idle" }
  | { status: "establishing" }
  | { status: "established"; asset: KnowledgeAssetResponse }
  | { status: "establish-error"; message: string };

export type KnowledgeAssetRetrieveState =
  | { status: "idle" }
  | { status: "retrieving" }
  | { status: "retrieved"; asset: KnowledgeAssetResponse }
  | { status: "retrieve-error"; message: string };

function describeError(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  return "Unable to reach the server. Check your connection and try again.";
}

export function useKnowledgeAssetManagement() {
  const [establishState, setEstablishState] = useState<KnowledgeAssetEstablishState>({ status: "idle" });
  const [retrieveState, setRetrieveState] = useState<KnowledgeAssetRetrieveState>({ status: "idle" });
  const { notify } = useNotifications();

  const establish = useCallback(
    async (request: EstablishKnowledgeAssetRequest) => {
      setEstablishState({ status: "establishing" });
      try {
        const asset = await establishKnowledgeAsset(request);
        setEstablishState({ status: "established", asset });
        setRetrieveState({ status: "retrieved", asset });
        notify(`Knowledge Asset established — status ${asset.curation_status}.`, "success");
      } catch (error) {
        const message = describeError(error);
        if (error instanceof ApiError && error.status === 0) notify(message, "danger");
        setEstablishState({ status: "establish-error", message });
      }
    },
    [notify],
  );

  const retrieve = useCallback(
    async (knowledgeAssetId: string) => {
      setRetrieveState({ status: "retrieving" });
      try {
        const asset = await getKnowledgeAsset(knowledgeAssetId);
        setRetrieveState({ status: "retrieved", asset });
      } catch (error) {
        const message = describeError(error);
        if (error instanceof ApiError && error.status === 0) notify(message, "danger");
        setRetrieveState({ status: "retrieve-error", message });
      }
    },
    [notify],
  );

  return { establishState, retrieveState, establish, retrieve };
}
