"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { Card, CardTitle, CardDescription } from "@/components/ui/Card";
import { FormField, FormLabel, FormBanner } from "@/components/ui/Form";
import type { UpdateOrganizationState } from "@/features/organization/state/useUpdateOrganization";
import type { OrganizationResponse, UpdateOrganizationProfileRequest } from "@/types/organization";

interface UpdateOrganizationFormProps {
  organization: OrganizationResponse;
  state: UpdateOrganizationState;
  onUpdate: (fields: UpdateOrganizationProfileRequest) => void;
}

/**
 * BA-04: Update Organization Profile. Pre-filled from the organization
 * passed in. organization_code is shown read-only for context — it is
 * the immutable natural key (see schemas/organization.py's
 * UpdateOrganizationProfileRequest docstring) and is not part of this
 * Business Activity's request contract.
 */
export function UpdateOrganizationForm({ organization, state, onUpdate }: UpdateOrganizationFormProps) {
  const [organizationName, setOrganizationName] = useState(organization.organization_name);
  const [organizationType, setOrganizationType] = useState(organization.organization_type);
  const [description, setDescription] = useState(organization.description ?? "");
  const isLoading = state.status === "updating";

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onUpdate({
      organization_name: organizationName,
      organization_type: organizationType,
      description: description.trim() === "" ? null : description,
    });
  }

  return (
    <Card>
      <CardTitle>Update Organization Profile</CardTitle>
      <CardDescription>
        Updates this organization&apos;s name, type, and description. Requires the PLATFORM_ADMIN
        role. The organization code cannot be changed.
      </CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <FormField>
          <FormLabel htmlFor="update-org-code">Organization Code</FormLabel>
          <Input id="update-org-code" value={organization.organization_code} disabled />
        </FormField>

        <FormField>
          <FormLabel htmlFor="update-org-name">Organization Name</FormLabel>
          <Input
            id="update-org-name"
            value={organizationName}
            onChange={(event) => setOrganizationName(event.target.value)}
            required
            minLength={1}
            maxLength={255}
            disabled={isLoading}
          />
        </FormField>

        <FormField>
          <FormLabel htmlFor="update-org-type">Organization Type</FormLabel>
          <Input
            id="update-org-type"
            value={organizationType}
            onChange={(event) => setOrganizationType(event.target.value)}
            required
            minLength={1}
            maxLength={50}
            disabled={isLoading}
          />
        </FormField>

        <FormField>
          <FormLabel htmlFor="update-org-description">Description (optional)</FormLabel>
          <Input
            id="update-org-description"
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            maxLength={1000}
            disabled={isLoading}
          />
        </FormField>

        <Button type="submit" className="w-full" disabled={isLoading}>
          {isLoading && <Spinner className="mr-2" />}
          Save Changes
        </Button>
      </form>

      {state.status === "error" && (
        <div className="mt-4">
          <FormBanner tone="danger">
            {state.isNotFound ? "This organization no longer exists." : state.message}
          </FormBanner>
        </div>
      )}
    </Card>
  );
}
