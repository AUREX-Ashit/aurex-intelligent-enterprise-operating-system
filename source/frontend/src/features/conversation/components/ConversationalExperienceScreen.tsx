"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { FormBanner } from "@/components/ui/Form";
import { LoadingState } from "@/components/ui/LoadingState";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { ConversationTurnComposer } from "@/features/conversation/components/ConversationTurnComposer";
import { ConversationTurnList } from "@/features/conversation/components/ConversationTurnList";
import { useConversationManagement } from "@/features/conversation/state/useConversationManagement";

/**
 * WP-12 — AI Conversation Management (C-094). Composes BA-01 (establish/
 * close lifecycle), BA-02 (execute Interaction), and BA-03 (retrieve
 * Conversation) on a new, minimal nav slot (`IRA-012 §7` — no existing
 * slot exists for C-094, unlike WP-11's own reused `enterprise-intelligence`
 * placeholder). Scope is deliberately narrow: a single Conversation per
 * screen visit, no cross-Conversation aggregation, no multi-agent
 * visualization — disclosed as narrow, not oversold as a general-purpose
 * copilot (`IRA-012 §7`).
 */
export function ConversationalExperienceScreen() {
  const { conversationState, listState, executeState, establish, submitTurn, close } = useConversationManagement();

  useEffect(() => {
    void establish();
    // Establishes exactly one Conversation per screen visit — re-running on
    // every render would establish a new Conversation on each re-render.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">AI Conversation</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Exchange turns within a bounded Conversation and review evidence-cited responses (C-094).
          </p>
        </div>
        {conversationState.status === "open" && (
          <div className="flex items-center gap-2">
            <StatusBadge tone="success">OPEN</StatusBadge>
            <Button variant="secondary" onClick={() => void close(conversationState.conversation.conversation_id)}>
              Close conversation
            </Button>
          </div>
        )}
        {conversationState.status === "closed" && <StatusBadge tone="muted">CLOSED</StatusBadge>}
      </div>

      {conversationState.status === "idle" || conversationState.status === "establishing" ? (
        <LoadingState label="Establishing conversation…" />
      ) : conversationState.status === "error" ? (
        <FormBanner tone="danger">{conversationState.message}</FormBanner>
      ) : (
        <>
          <Card>
            <CardTitle>Submit a turn</CardTitle>
            <CardDescription>
              {conversationState.status === "closed"
                ? "This conversation is closed. Reload the page to start a new one."
                : "Each turn is recorded as an Interaction and answered against this conversation's own prior turns only."}
            </CardDescription>
            <div className="mt-4">
              <ConversationTurnComposer
                state={executeState}
                disabled={conversationState.status !== "open"}
                onSubmit={(inputText) => void submitTurn(conversationState.conversation.conversation_id, inputText)}
              />
            </div>
          </Card>

          <div>
            <h2 className="mb-3 text-lg font-bold text-foreground">Conversation history</h2>
            <ConversationTurnList state={listState} />
          </div>
        </>
      )}
    </div>
  );
}
