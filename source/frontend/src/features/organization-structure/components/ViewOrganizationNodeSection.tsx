"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { Card, CardTitle, CardDescription } from "@/components/ui/Card";
import { FormField, FormLabel, FormBanner } from "@/components/ui/Form";
import { StatusBadge } from "@/components/ui/StatusBadge";
import type { OrganizationStructureState } from "@/features/organization-structure/state/useOrganizationStructure";

export function ViewOrganizationNodeSection({
  state,
  onView,
}: {
  state: OrganizationStructureState;
  onView: (organizationNodeId: string) => void;
}) {
  const [nodeId, setNodeId] = useState("");
  const isLoading = state.status === "viewing";
  const node = state.status === "viewed" ? state.node : null;

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onView(nodeId);
  }

  return (
    <Card>
      <CardTitle>Understand Structural Position</CardTitle>
      <CardDescription>Look up an organization node by its ID.</CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 flex items-end gap-3">
        <FormField className="flex-1">
          <FormLabel htmlFor="node-lookup-id">Organization Node ID</FormLabel>
          <Input id="node-lookup-id" value={nodeId} onChange={(event) => setNodeId(event.target.value)} required disabled={isLoading} />
        </FormField>
        <Button type="submit" disabled={isLoading}>
          {isLoading && <Spinner className="mr-2" />}
          View
        </Button>
      </form>

      {state.status === "view-not-found" && (
        <div className="mt-4">
          <FormBanner tone="warning">No organization node exists with this ID.</FormBanner>
        </div>
      )}

      {state.status === "view-error" && (
        <div className="mt-4">
          <FormBanner tone="danger">{state.message}</FormBanner>
        </div>
      )}

      {node && (
        <dl className="mt-4 grid grid-cols-[160px_1fr] gap-y-3 text-sm">
          <dt className="font-semibold text-muted-foreground">Node Code</dt>
          <dd className="text-foreground">{node.node_code}</dd>

          <dt className="font-semibold text-muted-foreground">Node Name</dt>
          <dd className="text-foreground">{node.node_name}</dd>

          <dt className="font-semibold text-muted-foreground">Node Type</dt>
          <dd className="text-foreground">{node.node_type}</dd>

          <dt className="font-semibold text-muted-foreground">Legal Entity</dt>
          <dd className="text-foreground">{node.legal_entity_name ?? "—"}</dd>

          <dt className="font-semibold text-muted-foreground">Business Unit</dt>
          <dd className="text-foreground">{node.business_unit ?? "—"}</dd>

          <dt className="font-semibold text-muted-foreground">Sector</dt>
          <dd className="text-foreground">{node.sector ?? "—"}</dd>

          <dt className="font-semibold text-muted-foreground">Active</dt>
          <dd>
            <StatusBadge tone={node.active_flag ? "success" : "muted"}>
              {node.active_flag ? "Active" : "Inactive"}
            </StatusBadge>
          </dd>
        </dl>
      )}
    </Card>
  );
}
