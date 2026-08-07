"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { FormBanner, FormError, FormField, FormLabel } from "@/components/ui/Form";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import type { InteractionExecuteState } from "@/features/conversation/state/useConversationManagement";

/**
 * WP-12 BA-02 — Execute Interaction. Submits one Conversation turn.
 * `disabled` reflects the Conversation Boundary State (`ADR-020` Decision 2)
 * — a Closed Conversation accepts no further Interactions, enforced here
 * as UI affordance in addition to the backend's own 409 (`CLAUDE.md §20.6`
 * validation/error state discipline).
 */
export function ConversationTurnComposer({
  state,
  disabled,
  onSubmit,
}: {
  state: InteractionExecuteState;
  disabled: boolean;
  onSubmit: (inputText: string) => void;
}) {
  const [inputText, setInputText] = useState("");
  const isExecuting = state.status === "executing";

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onSubmit(inputText);
    if (inputText.trim()) setInputText("");
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <FormField>
        <FormLabel htmlFor="conversation-turn-input">Your turn</FormLabel>
        <Input
          id="conversation-turn-input"
          value={inputText}
          onChange={(event) => setInputText(event.target.value)}
          placeholder={disabled ? "This conversation is closed." : "Ask a question or give an instruction…"}
          disabled={disabled || isExecuting}
          invalid={state.status === "validation-error"}
        />
        <FormError>{state.status === "validation-error" ? state.message : null}</FormError>
      </FormField>

      <Button type="submit" disabled={disabled || isExecuting || inputText.trim().length === 0}>
        {isExecuting && <Spinner className="mr-2" />}
        Submit turn
      </Button>

      {state.status === "execute-error" && <FormBanner tone="danger">{state.message}</FormBanner>}
      {state.status === "executed" && (
        <FormBanner tone="success">Turn recorded as Interaction #{state.interaction.sequence_number}.</FormBanner>
      )}
    </form>
  );
}
