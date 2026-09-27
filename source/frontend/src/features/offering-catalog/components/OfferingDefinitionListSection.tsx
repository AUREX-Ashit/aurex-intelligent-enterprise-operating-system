"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { FormBanner } from "@/components/ui/Form";
import { LoadingState } from "@/components/ui/LoadingState";
import { StatusBadge } from "@/components/ui/StatusBadge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeaderCell,
  TableRow,
} from "@/components/ui/Table";
import type {
  DetailState,
  ListState,
} from "@/features/offering-catalog/state/useOfferingCatalog";

/**
 * C-021 WP-20 BA-01 — list the one platform-global offering catalog and read
 * one Offering Definition (TDS-C021 §13/§14). No tenant scoping — the
 * catalog is enterprise-wide (ROD-C021 D8). Selecting a row loads its
 * full Authoritative Offering Definition Context inline.
 */
export function OfferingDefinitionListSection({
  listState,
  detailState,
  onLoad,
  onSelect,
}: {
  listState: ListState;
  detailState: DetailState;
  onLoad: () => void;
  onSelect: (offeringId: string) => void;
}) {
  useEffect(() => {
    onLoad();
    // Loads once on mount — onLoad is a stable useCallback identity.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Card>
      <div className="flex items-center justify-between">
        <div>
          <CardTitle>Offering Catalog</CardTitle>
          <CardDescription>
            Every Offering Definition in the platform-global C-021 catalog, newest first.
          </CardDescription>
        </div>
        {listState.status === "loaded" && (
          <Button type="button" variant="secondary" onClick={onLoad}>
            Refresh
          </Button>
        )}
      </div>

      <div className="mt-4">
        {listState.status === "idle" || listState.status === "loading" ? (
          <LoadingState label="Loading the offering catalog…" />
        ) : listState.status === "error" ? (
          <div className="space-y-3">
            <FormBanner tone="danger">{listState.message}</FormBanner>
            <Button type="button" variant="secondary" onClick={onLoad}>
              Retry
            </Button>
          </div>
        ) : listState.offerings.length === 0 ? (
          <p className="py-8 text-center text-sm text-muted-foreground">
            No Offering Definitions have been established yet. Use the form above to create the
            first one.
          </p>
        ) : (
          <Table>
            <TableHead>
              <TableRow>
                <TableHeaderCell>Offering Reference</TableHeaderCell>
                <TableHeaderCell>Name</TableHeaderCell>
                <TableHeaderCell>Classification</TableHeaderCell>
                <TableHeaderCell>Category</TableHeaderCell>
                <TableHeaderCell>State</TableHeaderCell>
                <TableHeaderCell aria-label="Actions" />
              </TableRow>
            </TableHead>
            <TableBody>
              {listState.offerings.map((offering) => (
                <TableRow key={offering.id}>
                  <TableCell className="font-mono text-xs">{offering.offering_reference}</TableCell>
                  <TableCell>{offering.offering_name}</TableCell>
                  <TableCell>
                    <StatusBadge tone="info">{offering.offering_kind}</StatusBadge>
                  </TableCell>
                  <TableCell className="text-muted-foreground">
                    {offering.category_ref ?? "—"}
                  </TableCell>
                  <TableCell>
                    <StatusBadge tone="muted">{offering.state}</StatusBadge>
                  </TableCell>
                  <TableCell>
                    <Button
                      type="button"
                      variant="secondary"
                      onClick={() => onSelect(offering.id)}
                    >
                      View
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>

      {detailState.status !== "idle" && (
        <div className="mt-6 border-t border-border-muted pt-4">
          <CardTitle>Offering Definition Detail</CardTitle>
          <div className="mt-3">
            {detailState.status === "loading" ? (
              <LoadingState label="Loading Offering Definition…" />
            ) : detailState.status === "not-found" ? (
              <FormBanner tone="warning">No Offering Definition exists with that id.</FormBanner>
            ) : detailState.status === "error" ? (
              <FormBanner tone="danger">{detailState.message}</FormBanner>
            ) : (
              <dl className="grid gap-x-6 gap-y-2 text-sm sm:grid-cols-2">
                <Detail label="Offering Reference" value={detailState.offering.offering_reference} mono />
                <Detail label="Identity" value={detailState.offering.id} mono />
                <Detail label="Name" value={detailState.offering.offering_name} />
                <Detail label="Classification" value={detailState.offering.offering_kind} />
                <Detail label="Category Reference" value={detailState.offering.category_ref ?? "—"} />
                <Detail
                  label="List-Price Reference"
                  value={detailState.offering.list_price_reference ?? "—"}
                />
                <Detail label="State" value={detailState.offering.state} />
                <Detail label="Version" value={String(detailState.offering.version)} />
                <Detail label="Created" value={detailState.offering.created_at} />
              </dl>
            )}
          </div>
        </div>
      )}
    </Card>
  );
}

function Detail({ label, value, mono = false }: { label: string; value: string; mono?: boolean }) {
  return (
    <div>
      <dt className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">{label}</dt>
      <dd className={mono ? "font-mono text-xs text-foreground" : "text-foreground"}>{value}</dd>
    </div>
  );
}
