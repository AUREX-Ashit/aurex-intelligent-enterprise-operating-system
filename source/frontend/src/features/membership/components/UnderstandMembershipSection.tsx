"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { Card, CardTitle, CardDescription } from "@/components/ui/Card";
import { FormField, FormLabel, FormBanner } from "@/components/ui/Form";
import { StatusBadge } from "@/components/ui/StatusBadge";
import type { MembershipManagementState } from "@/features/membership/state/useMembershipManagement";
import type { ChangeMembershipTermsRequest } from "@/types/membership";

/**
 * WP-03 BA-02/BA-03 — Understand Membership Context (view by ID) and
 * Maintain Membership Terms (change reason), composed in one section
 * since Change Terms only ever operates on an already-understood
 * Membership, mirroring ViewOrganizationSection's own "look up by ID"
 * pattern.
 */
export function UnderstandMembershipSection({
  state,
  onUnderstand,
  onChangeTerms,
}: {
  state: MembershipManagementState;
  onUnderstand: (membershipId: string) => void;
  onChangeTerms: (membershipId: string, fields: ChangeMembershipTermsRequest) => void;
}) {
  const [membershipId, setMembershipId] = useState("");
  const [reason, setReason] = useState("");
  const isLoading = state.status === "understanding";
  const isChangingTerms = state.status === "changing-terms";
  const understanding = state.status === "understood" ? state.membership : null;
  const membership = understanding ?? (state.status === "terms-changed" ? state.membership : null);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onUnderstand(membershipId);
  }

  function handleChangeTerms(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!membership) return;
    // BR-C007-003: at least one supplied field must genuinely differ from
    // the Membership's current value, or the request is rejected (409).
    // Toggling license_type is a real, always-different term change to
    // demonstrate Maintain Membership Terms without inventing a field
    // this schema doesn't have.
    const nextLicenseType = membership.license_type === "FULL" ? "LIGHT" : "FULL";
    onChangeTerms(membershipId, {
      license_type: nextLicenseType,
      reason: reason || null,
    });
  }

  return (
    <Card>
      <CardTitle>Understand Membership</CardTitle>
      <CardDescription>Look up a Membership by ID to see its current standing and authority consequence.</CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 flex items-end gap-3">
        <FormField className="flex-1">
          <FormLabel htmlFor="membership-lookup-id">Membership ID</FormLabel>
          <Input
            id="membership-lookup-id"
            value={membershipId}
            onChange={(event) => setMembershipId(event.target.value)}
            required
            disabled={isLoading}
          />
        </FormField>
        <Button type="submit" disabled={isLoading}>
          {isLoading && <Spinner className="mr-2" />}
          Understand
        </Button>
      </form>

      {state.status === "understand-not-found" && (
        <div className="mt-4">
          <FormBanner tone="warning">No Membership exists with this ID.</FormBanner>
        </div>
      )}

      {(state.status === "understand-error" || state.status === "terms-error") && (
        <div className="mt-4">
          <FormBanner tone="danger">{state.message}</FormBanner>
        </div>
      )}

      {membership && (
        <>
          <dl className="mt-4 grid grid-cols-[160px_1fr] gap-y-3 text-sm">
            <dt className="font-semibold text-muted-foreground">Status</dt>
            <dd>
              <StatusBadge tone={membership.membership_status === "ACTIVE" ? "success" : "warning"}>
                {membership.membership_status}
              </StatusBadge>
            </dd>

            <dt className="font-semibold text-muted-foreground">Type / License</dt>
            <dd className="text-foreground">
              {membership.membership_type} / {membership.license_type}
            </dd>

            <dt className="font-semibold text-muted-foreground">Primary</dt>
            <dd className="text-foreground">{membership.is_primary ? "Yes" : "No"}</dd>

            {understanding && (
              <>
                <dt className="font-semibold text-muted-foreground">Currently Effective</dt>
                <dd>
                  <StatusBadge tone={understanding.currently_effective ? "success" : "muted"}>
                    {understanding.currently_effective ? "Yes" : "No"}
                  </StatusBadge>
                </dd>

                <dt className="font-semibold text-muted-foreground">Authority Consequence</dt>
                <dd className="text-foreground">{understanding.authority_consequence}</dd>
              </>
            )}

            <dt className="font-semibold text-muted-foreground">Joined At</dt>
            <dd className="text-foreground">{new Date(membership.joined_at).toLocaleString()}</dd>
          </dl>

          <form onSubmit={handleChangeTerms} className="mt-6 flex items-end gap-3 border-t border-border pt-4">
            <FormField className="flex-1">
              <FormLabel htmlFor="membership-terms-reason">
                Toggle License Type to {membership.license_type === "FULL" ? "LIGHT" : "FULL"} — Reason
              </FormLabel>
              <Input
                id="membership-terms-reason"
                value={reason}
                onChange={(event) => setReason(event.target.value)}
                disabled={isChangingTerms}
                placeholder="Optional business reason"
              />
            </FormField>
            <Button type="submit" variant="secondary" disabled={isChangingTerms}>
              {isChangingTerms && <Spinner className="mr-2" />}
              Change Terms
            </Button>
          </form>

          {state.status === "terms-changed" && (
            <div className="mt-3">
              <FormBanner tone="success">Membership terms updated.</FormBanner>
            </div>
          )}
        </>
      )}
    </Card>
  );
}
