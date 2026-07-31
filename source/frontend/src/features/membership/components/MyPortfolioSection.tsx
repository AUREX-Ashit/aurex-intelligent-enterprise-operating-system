"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import { Card, CardTitle, CardDescription } from "@/components/ui/Card";
import { FormBanner } from "@/components/ui/Form";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { Table, TableBody, TableCell, TableHead, TableHeaderCell, TableRow } from "@/components/ui/Table";
import type { MembershipManagementState } from "@/features/membership/state/useMembershipManagement";

/**
 * WP-03 BA-08 — Present the caller's own cross-organization Membership
 * portfolio. No person_id input: this is always and only the
 * authenticated caller's own data (BR-C007-009).
 */
export function MyPortfolioSection({
  state,
  onLoad,
}: {
  state: MembershipManagementState;
  onLoad: () => void;
}) {
  const isLoading = state.status === "loading-portfolio";
  const portfolio = state.status === "portfolio-loaded" ? state.portfolio : null;

  useEffect(() => {
    onLoad();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Card>
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <CardTitle>My Membership Portfolio</CardTitle>
          <CardDescription>Every ACTIVE Membership you hold, across every organization.</CardDescription>
        </div>
        <Button variant="secondary" onClick={onLoad} disabled={isLoading}>
          {isLoading && <Spinner className="mr-2" />}
          Refresh
        </Button>
      </div>

      {state.status === "portfolio-error" && (
        <div className="mt-4">
          <FormBanner tone="danger">{state.message}</FormBanner>
        </div>
      )}

      <div className="mt-4">
        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <Spinner />
          </div>
        ) : portfolio && portfolio.memberships.length === 0 ? (
          <p className="py-6 text-center text-sm text-muted-foreground">
            No active Memberships found for your account.
          </p>
        ) : portfolio ? (
          <Table>
            <TableHead>
              <TableRow>
                <TableHeaderCell>Organization ID</TableHeaderCell>
                <TableHeaderCell>Type</TableHeaderCell>
                <TableHeaderCell>License</TableHeaderCell>
                <TableHeaderCell>Status</TableHeaderCell>
                <TableHeaderCell>Primary</TableHeaderCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {portfolio.memberships.map((membership) => (
                <TableRow key={membership.id}>
                  <TableCell>{membership.organization_id}</TableCell>
                  <TableCell>{membership.membership_type}</TableCell>
                  <TableCell>{membership.license_type}</TableCell>
                  <TableCell>
                    <StatusBadge tone={membership.membership_status === "ACTIVE" ? "success" : "warning"}>
                      {membership.membership_status}
                    </StatusBadge>
                  </TableCell>
                  <TableCell>{membership.is_primary ? "Yes" : "No"}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        ) : null}
      </div>
    </Card>
  );
}
