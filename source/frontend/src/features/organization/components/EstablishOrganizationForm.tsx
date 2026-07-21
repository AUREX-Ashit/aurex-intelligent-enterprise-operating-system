"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { Card, CardTitle, CardDescription } from "@/components/ui/Card";
import { FormField, FormLabel, FormBanner } from "@/components/ui/Form";
import type { EstablishOrganizationState } from "@/features/organization/state/useEstablishOrganization";
import type { EstablishOrganizationRequest } from "@/types/organization";

interface EstablishOrganizationFormProps {
  state: EstablishOrganizationState;
  onEstablish: (fields: EstablishOrganizationRequest) => void;
}

export function EstablishOrganizationForm({ state, onEstablish }: EstablishOrganizationFormProps) {
  const [organizationCode, setOrganizationCode] = useState("");
  const [organizationName, setOrganizationName] = useState("");
  const [organizationType, setOrganizationType] = useState("");
  const [description, setDescription] = useState("");
  const isLoading = state.status === "establishing";

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onEstablish({
      organization_code: organizationCode,
      organization_name: organizationName,
      organization_type: organizationType,
      description: description.trim() === "" ? null : description,
    });
  }

  return (
    <Card>
      <CardTitle>Establish Organization</CardTitle>
      <CardDescription>
        Creates a new organization. Requires the PLATFORM_ADMIN role. The organization code
        must be unique platform-wide.
      </CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <FormField>
          <FormLabel htmlFor="establish-org-code">Organization Code</FormLabel>
          <Input
            id="establish-org-code"
            value={organizationCode}
            onChange={(event) => setOrganizationCode(event.target.value)}
            required
            minLength={1}
            maxLength={50}
            disabled={isLoading}
            placeholder="ACME-CORP-001"
          />
        </FormField>

        <FormField>
          <FormLabel htmlFor="establish-org-name">Organization Name</FormLabel>
          <Input
            id="establish-org-name"
            value={organizationName}
            onChange={(event) => setOrganizationName(event.target.value)}
            required
            minLength={1}
            maxLength={255}
            disabled={isLoading}
            placeholder="Acme Corporation"
          />
        </FormField>

        <FormField>
          <FormLabel htmlFor="establish-org-type">Organization Type</FormLabel>
          <Input
            id="establish-org-type"
            value={organizationType}
            onChange={(event) => setOrganizationType(event.target.value)}
            required
            minLength={1}
            maxLength={50}
            disabled={isLoading}
            placeholder="CORPORATE"
          />
        </FormField>

        <FormField>
          <FormLabel htmlFor="establish-org-description">Description (optional)</FormLabel>
          <Input
            id="establish-org-description"
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            maxLength={1000}
            disabled={isLoading}
          />
        </FormField>

        <Button type="submit" className="w-full" disabled={isLoading}>
          {isLoading && <Spinner className="mr-2" />}
          Establish Organization
        </Button>
      </form>

      {state.status === "error" && (
        <div className="mt-4">
          <FormBanner tone="danger">
            {state.isConflict
              ? "An organization with this code already exists."
              : state.message}
          </FormBanner>
        </div>
      )}
    </Card>
  );
}
