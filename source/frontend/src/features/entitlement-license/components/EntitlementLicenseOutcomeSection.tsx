"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { Card, CardTitle, CardDescription } from "@/components/ui/Card";
import { FormField, FormLabel, FormBanner } from "@/components/ui/Form";
import type { OutcomeState } from "@/features/entitlement-license/state/useEntitlementLicense";

export function EntitlementLicenseOutcomeSection({
  state,
  onLoad,
}: {
  state: OutcomeState;
  onLoad: (contextId: string) => void;
}) {
  const [contextId, setContextId] = useState("");
  const isLoading = state.status === "loading";

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (contextId.trim()) onLoad(contextId.trim());
  }

  return (
    <Card>
      <CardTitle>Resulting Establishment / Status Outcome</CardTitle>
      <CardDescription>
        Look up the immediate outcome of an establish action — type, anchor, effective period, and
        current status — for one Authoritative License or Entitlement Context in your Organization.
        This is the establish result, not a standing dashboard.
      </CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 flex flex-wrap items-end gap-3">
        <FormField className="min-w-[22rem] flex-1">
          <FormLabel htmlFor="elc-outcome-id">Context ID</FormLabel>
          <Input
            id="elc-outcome-id"
            value={contextId}
            onChange={(event) => setContextId(event.target.value)}
            placeholder="License or Entitlement Context ID"
            required
            disabled={isLoading}
          />
        </FormField>
        <Button type="submit" disabled={isLoading || contextId.trim().length === 0}>
          {isLoading && <Spinner className="mr-2" />}
          Show Outcome
        </Button>
      </form>

      <div className="mt-4">
        {state.status === "idle" && (
          <p className="text-muted-foreground text-sm">Enter a Context ID to see its outcome.</p>
        )}
        {state.status === "loading" && <p className="text-muted-foreground text-sm">Loading…</p>}
        {state.status === "not-found" && (
          <FormBanner tone="warning">
            No such context in your Organization. A Context ID from another Organization is not
            shown.
          </FormBanner>
        )}
        {state.status === "error" && <FormBanner tone="danger">{state.message}</FormBanner>}
        {state.status === "loaded" && <OutcomeDetail state={state} />}
      </div>
    </Card>
  );
}

function OutcomeDetail({ state }: { state: Extract<OutcomeState, { status: "loaded" }> }) {
  const { outcome } = state;
  const row = outcome.kind === "LICENSE" ? outcome.license : outcome.entitlement;
  if (!row) return null;

  const anchor =
    outcome.kind === "LICENSE" && outcome.license
      ? `Membership ${outcome.license.membership_id}`
      : outcome.entitlement
        ? `Organization ${outcome.entitlement.organization_id}${
            outcome.entitlement.domain_id ? ` · Domain ${outcome.entitlement.domain_id}` : ""
          } · ${outcome.entitlement.entitlement_type_ref}`
        : "";

  return (
    <dl className="grid gap-x-6 gap-y-2 text-sm sm:grid-cols-2">
      <Field label="Kind">{outcome.kind}</Field>
      <Field label="Status">
        <StatusBadge tone={row.status === "ACTIVE" ? "success" : "muted"}>{row.status}</StatusBadge>
      </Field>
      <Field label="Context ID">
        <span className="font-mono text-xs">{row.id}</span>
      </Field>
      <Field label="Anchor">{anchor}</Field>
      {outcome.kind === "LICENSE" && outcome.license?.c023_license_type && (
        <Field label="Specialized License Type">{outcome.license.c023_license_type}</Field>
      )}
      <Field label="Effective From">{new Date(row.effective_from).toLocaleString()}</Field>
      <Field label="Effective To">
        {row.effective_to ? new Date(row.effective_to).toLocaleString() : "open-ended"}
      </Field>
      <Field label="Source Reference">{row.entitlement_source_reference ?? "—"}</Field>
      <Field label="Authorized By">
        <span className="font-mono text-xs">{row.approval_authority_id}</span>
      </Field>
      <Field label="Committed By">
        <span className="font-mono text-xs">{row.committed_by_actor_id}</span>
      </Field>
      <Field label="Committed At">{new Date(row.committed_at).toLocaleString()}</Field>
    </dl>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <dt className="text-muted-foreground text-xs font-semibold tracking-wide uppercase">
        {label}
      </dt>
      <dd className="text-foreground mt-0.5">{children}</dd>
    </div>
  );
}
