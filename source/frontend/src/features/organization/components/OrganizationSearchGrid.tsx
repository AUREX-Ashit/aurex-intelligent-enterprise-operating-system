"use client";

import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { Card, CardTitle, CardDescription } from "@/components/ui/Card";
import { FormBanner } from "@/components/ui/Form";
import { Table, TableBody, TableCell, TableHead, TableHeaderCell, TableRow } from "@/components/ui/Table";
import { useSearchOrganizations } from "@/features/organization/state/useSearchOrganizations";
import type { OrganizationResponse, OrganizationSortField, OrganizationStatus } from "@/types/organization";

const STATUS_FILTERS: Array<{ label: string; value: OrganizationStatus | "ALL" }> = [
  { label: "All", value: "ALL" },
  { label: "Active", value: "ACTIVE" },
  { label: "Suspended", value: "SUSPENDED" },
];

const SORTABLE_COLUMNS: Array<{ label: string; field: OrganizationSortField }> = [
  { label: "Name", field: "organization_name" },
  { label: "Code", field: "organization_code" },
  { label: "Created", field: "created_at" },
];

interface OrganizationSearchGridProps {
  onCreateOrganization: () => void;
  onViewOrganization: (organization: OrganizationResponse) => void;
}

/**
 * BA-03: the primary Organization Management screen — search, status
 * filter, sortable columns, pagination, per-row View Details, and a
 * Create Organization action. Composed entirely from existing ui/
 * primitives (Table, Card, Button, Input, StatusBadge, Spinner,
 * FormBanner) — no new DS-001 component invented.
 */
export function OrganizationSearchGrid({ onCreateOrganization, onViewOrganization }: OrganizationSearchGridProps) {
  const { query, state, setSearchText, setStatusFilter, setSort, nextPage, previousPage, refresh } =
    useSearchOrganizations();

  const isLoading = state.status === "loading";
  const items = state.status === "success" ? state.items : [];
  const total = state.status === "success" ? state.total : 0;
  const currentPageStart = total === 0 ? 0 : query.skip + 1;
  const currentPageEnd = Math.min(query.skip + query.limit, total);
  const hasPreviousPage = query.skip > 0;
  const hasNextPage = query.skip + query.limit < total;

  function toggleSort(field: OrganizationSortField) {
    if (query.sortBy === field) {
      setSort(field, query.sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSort(field, "asc");
    }
  }

  return (
    <Card>
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <CardTitle>Organizations</CardTitle>
          <CardDescription>Search, filter, and manage every organization on the platform.</CardDescription>
        </div>
        <Button onClick={onCreateOrganization}>Create Organization</Button>
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-3">
        <Input
          value={query.q}
          onChange={(event) => setSearchText(event.target.value)}
          placeholder="Search by name or code…"
          className="max-w-xs"
          aria-label="Search organizations"
        />
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

      {state.status === "error" && (
        <div className="mt-4">
          <FormBanner tone="danger">
            {state.message}{" "}
            <button type="button" onClick={refresh} className="ml-2 underline">
              Retry
            </button>
          </FormBanner>
        </div>
      )}

      <div className="mt-4">
        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <Spinner />
          </div>
        ) : items.length === 0 && state.status === "success" ? (
          <div className="py-12 text-center">
            <p className="text-sm font-medium text-foreground">No organizations found.</p>
            <p className="mt-1 text-sm text-muted-foreground">
              {query.q || query.status !== "ALL"
                ? "Try adjusting your search text or status filter."
                : "Get started by creating the first organization."}
            </p>
            {!query.q && query.status === "ALL" && (
              <Button className="mt-4" onClick={onCreateOrganization}>
                Create Organization
              </Button>
            )}
          </div>
        ) : (
          <Table>
            <TableHead>
              <TableRow>
                {SORTABLE_COLUMNS.map((column) => (
                  <TableHeaderCell key={column.field}>
                    <button
                      type="button"
                      onClick={() => toggleSort(column.field)}
                      className="flex items-center gap-1 hover:text-foreground"
                    >
                      {column.label}
                      {query.sortBy === column.field && (query.sortOrder === "asc" ? "▲" : "▼")}
                    </button>
                  </TableHeaderCell>
                ))}
                <TableHeaderCell>Type</TableHeaderCell>
                <TableHeaderCell>Status</TableHeaderCell>
                <TableHeaderCell>
                  <span className="sr-only">Actions</span>
                </TableHeaderCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {items.map((organization) => (
                <TableRow key={organization.id}>
                  <TableCell>{organization.organization_name}</TableCell>
                  <TableCell>{organization.organization_code}</TableCell>
                  <TableCell>{new Date(organization.created_at).toLocaleDateString()}</TableCell>
                  <TableCell>{organization.organization_type}</TableCell>
                  <TableCell>
                    <StatusBadge tone={organization.status === "ACTIVE" ? "success" : "warning"}>
                      {organization.status}
                    </StatusBadge>
                  </TableCell>
                  <TableCell>
                    <Button variant="ghost" onClick={() => onViewOrganization(organization)}>
                      View Details
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>

      {!isLoading && total > 0 && (
        <div className="mt-4 flex items-center justify-between text-sm text-muted-foreground">
          <span>
            Showing {currentPageStart}–{currentPageEnd} of {total}
          </span>
          <div className="flex gap-2">
            <Button variant="secondary" disabled={!hasPreviousPage} onClick={previousPage}>
              Previous
            </Button>
            <Button variant="secondary" disabled={!hasNextPage} onClick={nextPage}>
              Next
            </Button>
          </div>
        </div>
      )}
    </Card>
  );
}
