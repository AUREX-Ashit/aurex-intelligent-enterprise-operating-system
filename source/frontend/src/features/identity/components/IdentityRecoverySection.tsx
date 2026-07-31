"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { FormBanner, FormField, FormLabel } from "@/components/ui/Form";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { StatusBadge } from "@/components/ui/StatusBadge";
import type { IdentityManagementState } from "@/features/identity/state/useIdentityManagement";

/**
 * WP-08 BA-02 — Recover Inaccessible Identity Context, self-service
 * scope (EX-C001-07). Requests recovery for the caller's own person_id
 * only; never performs the technical credential-recovery mechanism
 * itself, and never executes the routed-to establishment/resolution —
 * only records the request and its routing determination.
 */
export function IdentityRecoverySection({
  state,
  personId,
  onRequestRecovery,
}: {
  state: IdentityManagementState;
  personId: string;
  onRequestRecovery: (personId: string, reason: string) => void;
}) {
  const [reason, setReason] = useState("");
  const isLoading = state.status === "recovering";
  const result = state.status === "recovery-requested" ? state.result : null;

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onRequestRecovery(personId, reason);
  }

  return (
    <Card>
      <CardTitle>Recover Inaccessible Identity</CardTitle>
      <CardDescription>
        Request governed recovery if your established Identity has become unusable — for example, a
        lost authentication device. This does not reset a credential; it records a recovery request
        and routes you toward the applicable governed path.
      </CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <FormField>
          <FormLabel htmlFor="recovery-reason">Reason</FormLabel>
          <Input
            id="recovery-reason"
            value={reason}
            onChange={(event) => setReason(event.target.value)}
            required
            minLength={1}
            disabled={isLoading}
            placeholder="e.g. Lost access to my registered authentication device."
          />
        </FormField>

        <Button type="submit" className="w-full" disabled={isLoading || reason.trim().length === 0}>
          {isLoading && <Spinner className="mr-2" />}
          Request Recovery
        </Button>
      </form>

      {state.status === "recovery-error" && (
        <div className="mt-4">
          <FormBanner tone="danger">{state.message}</FormBanner>
        </div>
      )}

      {result && (
        <dl className="mt-4 grid grid-cols-[140px_1fr] gap-y-3 text-sm">
          <dt className="font-semibold text-muted-foreground">Routed Path</dt>
          <dd>
            <StatusBadge tone="brand">{result.routed_path}</StatusBadge>
          </dd>

          <dt className="font-semibold text-muted-foreground">Status</dt>
          <dd className="text-foreground">{result.status}</dd>

          <dt className="font-semibold text-muted-foreground">Requested At</dt>
          <dd className="text-foreground">{new Date(result.created_at).toLocaleString()}</dd>
        </dl>
      )}
    </Card>
  );
}
