"use client";

import type { ReactNode } from "react";
import { Button } from "@/components/ui/Button";
import { FormBanner } from "@/components/ui/Form";
import { Spinner } from "@/components/ui/Spinner";
import { Table, TableBody, TableCell, TableHead, TableHeaderCell, TableRow } from "@/components/ui/Table";

export interface DataGridColumn<T> {
  key: string;
  label: string;
  render: (row: T) => ReactNode;
  sortable?: boolean;
}

export interface DataGridPagination {
  currentStart: number;
  currentEnd: number;
  total: number;
  hasPrevious: boolean;
  hasNext: boolean;
  onPrevious: () => void;
  onNext: () => void;
}

export interface DataGridProps<T> {
  columns: DataGridColumn<T>[];
  rows: T[];
  getRowKey: (row: T) => string;
  isLoading: boolean;
  error?: string | null;
  onRetry?: () => void;
  emptyTitle?: string;
  emptyDescription?: string;
  emptyAction?: ReactNode;
  sortField?: string | null;
  sortOrder?: "asc" | "desc";
  onSort?: (field: string) => void;
  rowActions?: (row: T) => ReactNode;
  pagination?: DataGridPagination;
}

/**
 * Reusable Platform Asset — generic list/search/sort/paginate grid.
 * Presentational only: query state, filtering, and data-fetching remain
 * owned by each feature's own state hook (mirrors the existing
 * useSearchOrganizations pattern), consistent with this codebase's own
 * established convention of a single-owner state hook per feature. This
 * component only renders loading/empty/error/data states and pagination
 * controls, so every list screen built against it automatically implements
 * CLAUDE.md §20.6's own interaction-state baseline without re-deriving it
 * per screen.
 */
export function DataGrid<T>({
  columns,
  rows,
  getRowKey,
  isLoading,
  error,
  onRetry,
  emptyTitle = "No results found.",
  emptyDescription = "Try adjusting your search or filters.",
  emptyAction,
  sortField,
  sortOrder,
  onSort,
  rowActions,
  pagination,
}: DataGridProps<T>) {
  return (
    <div>
      {error && (
        <div className="mb-4">
          <FormBanner tone="danger">
            {error}{" "}
            {onRetry && (
              <button type="button" onClick={onRetry} className="ml-2 underline">
                Retry
              </button>
            )}
          </FormBanner>
        </div>
      )}

      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <Spinner />
        </div>
      ) : rows.length === 0 ? (
        <div className="py-12 text-center">
          <p className="text-sm font-medium text-foreground">{emptyTitle}</p>
          <p className="mt-1 text-sm text-muted-foreground">{emptyDescription}</p>
          {emptyAction && <div className="mt-4">{emptyAction}</div>}
        </div>
      ) : (
        <Table>
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableHeaderCell key={column.key}>
                  {column.sortable && onSort ? (
                    <button
                      type="button"
                      onClick={() => onSort(column.key)}
                      className="flex items-center gap-1 hover:text-foreground"
                    >
                      {column.label}
                      {sortField === column.key && (sortOrder === "asc" ? "▲" : "▼")}
                    </button>
                  ) : (
                    column.label
                  )}
                </TableHeaderCell>
              ))}
              {rowActions && (
                <TableHeaderCell>
                  <span className="sr-only">Actions</span>
                </TableHeaderCell>
              )}
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((row) => (
              <TableRow key={getRowKey(row)}>
                {columns.map((column) => (
                  <TableCell key={column.key}>{column.render(row)}</TableCell>
                ))}
                {rowActions && (
                  <TableCell>
                    <div className="flex gap-2">{rowActions(row)}</div>
                  </TableCell>
                )}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}

      {!isLoading && pagination && pagination.total > 0 && (
        <div className="mt-4 flex items-center justify-between text-sm text-muted-foreground">
          <span>
            Showing {pagination.currentStart}–{pagination.currentEnd} of {pagination.total}
          </span>
          <div className="flex gap-2">
            <Button variant="secondary" disabled={!pagination.hasPrevious} onClick={pagination.onPrevious}>
              Previous
            </Button>
            <Button variant="secondary" disabled={!pagination.hasNext} onClick={pagination.onNext}>
              Next
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
