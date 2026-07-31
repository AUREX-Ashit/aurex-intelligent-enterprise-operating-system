"use client";

import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { FormBanner } from "@/components/ui/Form";
import { Spinner } from "@/components/ui/Spinner";
import { StatusBadge } from "@/components/ui/StatusBadge";
import type { IdentityManagementState } from "@/features/identity/state/useIdentityManagement";

/**
 * WP-08 BA-01 — Detect and Resolve Disrupted Identity Context
 * (EX-C001-06). Re-confirms the current Identity Context against C-006
 * rather than trusting the last-known session claim state (Contract 5.6).
 */
export function IdentityStatusSection({
  state,
  onCheckStatus,
}: {
  state: IdentityManagementState;
  onCheckStatus: () => void;
}) {
  const isLoading = state.status === "checking-status";
  const result = state.status === "status-checked" ? state.result : null;

  return (
    <Card>
      <div className="flex items-start justify-between gap-4">
        <div>
          <CardTitle>Identity Status</CardTitle>
          <CardDescription>
            Re-confirm your current Identity Context against its Authoritative Person Context.
          </CardDescription>
        </div>
        {result && (
          <StatusBadge tone={result.status === "CURRENT" ? "success" : "warning"}>
            {result.status}
          </StatusBadge>
        )}
      </div>

      <Button className="mt-4" variant="secondary" onClick={onCheckStatus} disabled={isLoading}>
        {isLoading && <Spinner className="mr-2" />}
        Refresh Identity Status
      </Button>

      {result && (
        <dl className="mt-4 grid grid-cols-[140px_1fr] gap-y-3 text-sm">
          <dt className="font-semibold text-muted-foreground">Identity ID</dt>
          <dd className="break-all text-foreground">{result.identity_id}</dd>

          <dt className="font-semibold text-muted-foreground">Person ID</dt>
          <dd className="break-all text-foreground">{result.person_id}</dd>

          <dt className="font-semibold text-muted-foreground">Checked At</dt>
          <dd className="text-foreground">{new Date(result.checked_at).toLocaleString()}</dd>
        </dl>
      )}

      {state.status === "status-error" && (
        <div className="mt-4">
          <FormBanner tone="danger">{state.message}</FormBanner>
        </div>
      )}
    </Card>
  );
}
