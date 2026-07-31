"use client";

import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { DataGrid, type DataGridColumn } from "@/components/ui/DataGrid";
import { FormField, FormLabel } from "@/components/ui/Form";
import { Input } from "@/components/ui/Input";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { useSearchDomainPermissions } from "@/features/domain-permission/state/useSearchDomainPermissions";
import type { DomainPermissionResponse, VersionStatus } from "@/types/domain-permission";

const STATUS_FILTERS: Array<{ label: string; value: VersionStatus | "ALL" }> = [
  { label: "All", value: "ALL" },
  { label: "Active", value: "ACTIVE" },
  { label: "Superseded", value: "SUPERSEDED" },
  { label: "Deprecated", value: "DEPRECATED" },
  { label: "Retired", value: "RETIRED" },
];

const COLUMNS: DataGridColumn<DomainPermissionResponse>[] = [
  { key: "domain_id", label: "Domain ID", render: (row) => row.domain_id },
  { key: "membership_id", label: "Membership ID", render: (row) => row.membership_id },
  { key: "permission_level", label: "Permission Level", render: (row) => row.permission_level },
  {
    key: "status",
    label: "Status",
    render: (row) => (
      <StatusBadge tone={row.status === "ACTIVE" ? "success" : row.status === "RETIRED" ? "muted" : "warning"}>
        {row.status}
      </StatusBadge>
    ),
  },
  { key: "version", label: "Version", render: (row) => row.version },
];

/**
 * WP-06 BA-01 — Understand Domain Permission Context (list branch). First
 * consumer of the new reusable DataGrid platform asset.
 */
export function DomainPermissionSearchGrid() {
  const { query, state, setDomainId, setMembershipId, setStatusFilter, refresh } = useSearchDomainPermissions();

  const isLoading = state.status === "loading";
  const items = state.status === "success" ? state.items : [];

  return (
    <Card>
      <CardTitle>Domain Permissions</CardTitle>
      <CardDescription>
        Filter by Domain, Membership, or status. No free-text search endpoint exists server-side.
      </CardDescription>

      <div className="mt-4 flex flex-wrap items-end gap-3">
        <FormField>
          <FormLabel htmlFor="dp-domain-id">Domain ID</FormLabel>
          <Input
            id="dp-domain-id"
            value={query.domainId}
            onChange={(event) => setDomainId(event.target.value)}
            placeholder="Filter by Domain ID"
            className="w-64"
          />
        </FormField>
        <FormField>
          <FormLabel htmlFor="dp-membership-id">Membership ID</FormLabel>
          <Input
            id="dp-membership-id"
            value={query.membershipId}
            onChange={(event) => setMembershipId(event.target.value)}
            placeholder="Filter by Membership ID"
            className="w-64"
          />
        </FormField>
        <div className="flex gap-2">
          {STATUS_FILTERS.map((filter) => (
            <Button
              key={filter.value}
              variant={query.status === filter.value ? "primary" : "secondary"}
              onClick={() => setStatusFilter(filter.value)}
            >
              {filter.label}
            </Button>
          ))}
        </div>
      </div>

      <div className="mt-4">
        <DataGrid
          columns={COLUMNS}
          rows={items}
          getRowKey={(row) => row.id}
          isLoading={isLoading}
          error={state.status === "error" ? state.message : null}
          onRetry={refresh}
          emptyTitle="No domain permissions found."
          emptyDescription="Try adjusting the Domain ID, Membership ID, or status filter."
        />
      </div>
    </Card>
  );
}
