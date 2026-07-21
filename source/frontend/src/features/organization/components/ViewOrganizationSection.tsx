"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { Card, CardTitle, CardDescription } from "@/components/ui/Card";
import { FormField, FormLabel, FormBanner } from "@/components/ui/Form";
import { OrganizationDetailsList } from "@/features/organization/components/OrganizationDetailsList";
import type { ViewOrganizationState } from "@/features/organization/state/useViewOrganization";

interface ViewOrganizationSectionProps {
  state: ViewOrganizationState;
  onView: (organizationId: string) => void;
}

export function ViewOrganizationSection({ state, onView }: ViewOrganizationSectionProps) {
  const [organizationId, setOrganizationId] = useState("");
  const isLoading = state.status === "loading";

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onView(organizationId);
  }

  return (
    <Card>
      <CardTitle>View Organization Details</CardTitle>
      <CardDescription>Look up an organization by its ID.</CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 flex items-end gap-3">
        <FormField className="flex-1">
          <FormLabel htmlFor="view-org-id">Organization ID</FormLabel>
          <Input
            id="view-org-id"
            value={organizationId}
            onChange={(event) => setOrganizationId(event.target.value)}
            required
            disabled={isLoading}
            placeholder="e.g. 550e8400-e29b-41d4-a716-446655440000"
          />
        </FormField>
        <Button type="submit" disabled={isLoading}>
          {isLoading && <Spinner className="mr-2" />}
          View
        </Button>
      </form>

      {state.status === "not-found" && (
        <div className="mt-4">
          <FormBanner tone="warning">No organization exists with this ID.</FormBanner>
        </div>
      )}

      {state.status === "error" && (
        <div className="mt-4">
          <FormBanner tone="danger">{state.message}</FormBanner>
        </div>
      )}

      {state.status === "found" && <OrganizationDetailsList organization={state.organization} />}
    </Card>
  );
}
