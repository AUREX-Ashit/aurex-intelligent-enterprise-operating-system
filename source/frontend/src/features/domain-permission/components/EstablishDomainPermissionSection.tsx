"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { FormBanner, FormField, FormLabel } from "@/components/ui/Form";
import type { EstablishDomainPermissionState } from "@/features/domain-permission/state/useEstablishDomainPermission";
import type { DomainPermissionLevel, EstablishDomainPermissionRequest } from "@/types/domain-permission";

const PERMISSION_LEVELS: DomainPermissionLevel[] = [
  "VIEW",
  "ENTER",
  "EDIT",
  "REVIEW",
  "APPROVE",
  "ASSIGN",
  "DELEGATE",
  "ADMIN",
];

export function EstablishDomainPermissionSection({
  state,
  onEstablish,
}: {
  state: EstablishDomainPermissionState;
  onEstablish: (fields: EstablishDomainPermissionRequest) => void;
}) {
  const [membershipId, setMembershipId] = useState("");
  const [domainId, setDomainId] = useState("");
  const [permissionLevel, setPermissionLevel] = useState<DomainPermissionLevel>("VIEW");
  const isLoading = state.status === "establishing";

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onEstablish({ membership_id: membershipId, domain_id: domainId, permission_level: permissionLevel });
  }

  return (
    <Card>
      <CardTitle>Establish Domain Permission</CardTitle>
      <CardDescription>Grant a standing-authority permission level on a Domain to a Membership.</CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <div className="grid gap-4 sm:grid-cols-2">
          <FormField>
            <FormLabel htmlFor="dp-establish-membership-id">Membership ID</FormLabel>
            <Input
              id="dp-establish-membership-id"
              value={membershipId}
              onChange={(event) => setMembershipId(event.target.value)}
              required
              disabled={isLoading}
            />
          </FormField>

          <FormField>
            <FormLabel htmlFor="dp-establish-domain-id">Domain ID</FormLabel>
            <Input
              id="dp-establish-domain-id"
              value={domainId}
              onChange={(event) => setDomainId(event.target.value)}
              required
              disabled={isLoading}
            />
          </FormField>
        </div>

        <FormField>
          <FormLabel>Permission Level</FormLabel>
          <div className="flex flex-wrap gap-2">
            {PERMISSION_LEVELS.map((level) => (
              <Button
                key={level}
                type="button"
                variant={permissionLevel === level ? "primary" : "secondary"}
                onClick={() => setPermissionLevel(level)}
                disabled={isLoading}
              >
                {level}
              </Button>
            ))}
          </div>
        </FormField>

        <Button type="submit" disabled={isLoading}>
          {isLoading && <Spinner className="mr-2" />}
          Establish Domain Permission
        </Button>
      </form>

      {state.status === "error" && (
        <div className="mt-4">
          <FormBanner tone="danger">
            {state.isConflict ? "This Membership already has a Domain Permission on this Domain." : state.message}
          </FormBanner>
        </div>
      )}

      {state.status === "established" && (
        <div className="mt-4">
          <FormBanner tone="success">
            Domain permission {state.domainPermission.permission_level} established for Membership{" "}
            {state.domainPermission.membership_id}.
          </FormBanner>
        </div>
      )}
    </Card>
  );
}
