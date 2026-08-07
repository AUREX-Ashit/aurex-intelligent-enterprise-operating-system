"use client";

import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { EvidencePanel } from "@/components/ui/EvidencePanel";
import { LoadingState } from "@/components/ui/LoadingState";
import { StatusBadge } from "@/components/ui/StatusBadge";
import type { InteractionListState } from "@/features/conversation/state/useConversationManagement";

const STATUS_TONE: Record<string, "success" | "warning" | "danger" | "muted"> = {
  COMPLETE: "success",
  PENDING: "warning",
  FAILED: "danger",
};

/**
 * WP-12 BA-03 — Retrieve Conversation. Renders prior Interactions in
 * sequence order (`ADR-022` Decision 1 — identity, ordering, and
 * accountability preserved), each output composed with the Evidence Panel
 * (`SD-001-020`) rather than rendered as raw text.
 */
export function ConversationTurnList({ state }: { state: InteractionListState }) {
  if (state.status === "idle" || state.status === "loading") {
    return <LoadingState label="Loading conversation history…" />;
  }

  if (state.status === "error") {
    return <p className="py-6 text-sm text-danger">{state.message}</p>;
  }

  if (state.interactions.length === 0) {
    return (
      <p className="py-8 text-center text-sm text-muted-foreground">
        No turns yet — this conversation is open and ready for its first turn.
      </p>
    );
  }

  return (
    <div className="space-y-4">
      {state.interactions.map((interaction) => (
        <Card key={interaction.interaction_id}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <CardTitle>Turn #{interaction.sequence_number}</CardTitle>
              <CardDescription>{interaction.input_reference}</CardDescription>
            </div>
            <StatusBadge tone={STATUS_TONE[interaction.status] ?? "muted"}>{interaction.status}</StatusBadge>
          </div>

          {interaction.status === "COMPLETE" && (
            <div className="mt-4 space-y-2">
              <p className="text-sm text-foreground">{interaction.output_reference}</p>
              <EvidencePanel
                confidenceScore={interaction.confidence_score}
                evidenceReference={interaction.evidence_reference}
                auditTrail={[
                  { label: "Interaction created", timestamp: interaction.created_at },
                  ...(interaction.completed_at
                    ? [{ label: "Interaction completed", timestamp: interaction.completed_at }]
                    : []),
                ]}
              />
            </div>
          )}
        </Card>
      ))}
    </div>
  );
}
