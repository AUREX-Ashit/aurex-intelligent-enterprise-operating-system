"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import {
  closeConversation,
  establishConversation,
  executeInteraction,
  listInteractions,
} from "@/services/conversation-api";
import type { ConversationResponse, InteractionResponse } from "@/types/conversation";

/**
 * WP-12 — AI Conversation Management (C-094). Three state slices
 * (Conversation lifecycle, Interaction list, Interaction execution),
 * mirroring `useSearchManagement.ts`'s own precedent (WP-11): acting on
 * one must never blank an already-loaded slice of another.
 */
export type ConversationLifecycleState =
  | { status: "idle" }
  | { status: "establishing" }
  | { status: "open"; conversation: ConversationResponse }
  | { status: "closed"; conversation: ConversationResponse }
  | { status: "error"; message: string };

export type InteractionListState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "loaded"; interactions: InteractionResponse[] }
  | { status: "error"; message: string };

export type InteractionExecuteState =
  | { status: "idle" }
  | { status: "executing" }
  | { status: "executed"; interaction: InteractionResponse }
  | { status: "validation-error"; message: string }
  | { status: "execute-error"; message: string };

function describeError(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  return "Unable to reach the server. Check your connection and try again.";
}

export function useConversationManagement() {
  const [conversationState, setConversationState] = useState<ConversationLifecycleState>({ status: "idle" });
  const [listState, setListState] = useState<InteractionListState>({ status: "idle" });
  const [executeState, setExecuteState] = useState<InteractionExecuteState>({ status: "idle" });
  const { notify } = useNotifications();

  const loadInteractions = useCallback(
    async (conversationId: string) => {
      setListState({ status: "loading" });
      try {
        const response = await listInteractions(conversationId);
        setListState({ status: "loaded", interactions: response.interactions });
      } catch (error) {
        const message = describeError(error);
        if (error instanceof ApiError && error.status === 0) notify(message, "danger");
        setListState({ status: "error", message });
      }
    },
    [notify],
  );

  const establish = useCallback(async () => {
    setConversationState({ status: "establishing" });
    try {
      const conversation = await establishConversation();
      setConversationState({ status: "open", conversation });
      // A newly-established Conversation has zero Interactions yet — an honest,
      // disclosed empty state (CLAUDE.md §20.6), not a fetch round-trip for a
      // result already known.
      setListState({ status: "loaded", interactions: [] });
    } catch (error) {
      const message = describeError(error);
      if (error instanceof ApiError && error.status === 0) notify(message, "danger");
      setConversationState({ status: "error", message });
    }
  }, [notify]);

  const submitTurn = useCallback(
    async (conversationId: string, inputText: string) => {
      const trimmed = inputText.trim();
      if (!trimmed) {
        setExecuteState({ status: "validation-error", message: "Enter a question or instruction before submitting." });
        return;
      }

      setExecuteState({ status: "executing" });
      try {
        const interaction = await executeInteraction(conversationId, { input_text: trimmed });
        setExecuteState({ status: "executed", interaction });
        void loadInteractions(conversationId);
      } catch (error) {
        const message = describeError(error);
        if (error instanceof ApiError && error.status === 0) notify(message, "danger");
        setExecuteState({ status: "execute-error", message });
      }
    },
    [notify, loadInteractions],
  );

  const close = useCallback(
    async (conversationId: string) => {
      try {
        const conversation = await closeConversation(conversationId);
        setConversationState({ status: "closed", conversation });
        notify("Conversation closed.", "success");
      } catch (error) {
        const message = describeError(error);
        notify(message, "danger");
      }
    },
    [notify],
  );

  return {
    conversationState,
    listState,
    executeState,
    establish,
    loadInteractions,
    submitTurn,
    close,
  };
}
