"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { Card, CardTitle, CardDescription } from "@/components/ui/Card";
import { FormField, FormLabel, FormBanner, FormHelperText } from "@/components/ui/Form";
import type { MembershipManagementState } from "@/features/membership/state/useMembershipManagement";
import type { EstablishMembershipRequest, LicenseType, MembershipType } from "@/types/membership";

const MEMBERSHIP_TYPES: MembershipType[] = ["INTERNAL", "EXTERNAL"];
const LICENSE_TYPES: LicenseType[] = ["FULL", "LIGHT"];

export function EstablishMembershipSection({
  state,
  onEstablish,
}: {
  state: MembershipManagementState;
  onEstablish: (fields: EstablishMembershipRequest) => void;
}) {
  const [personId, setPersonId] = useState("");
  const [organizationId, setOrganizationId] = useState("");
  const [roleId, setRoleId] = useState("");
  const [homeNodeId, setHomeNodeId] = useState("");
  const [membershipType, setMembershipType] = useState<MembershipType>("INTERNAL");
  const [licenseType, setLicenseType] = useState<LicenseType>("FULL");
  const isLoading = state.status === "establishing";

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onEstablish({
      person_id: personId,
      organization_id: organizationId,
      role_id: roleId,
      home_node_id: homeNodeId || null,
      membership_type: membershipType,
      license_type: licenseType,
    });
  }

  return (
    <Card>
      <CardTitle>Establish Membership</CardTitle>
      <CardDescription>
        Connects a Person to an Organization through a Role. Requires the Person, Organization,
        and Role IDs already established elsewhere in the platform.
      </CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <div className="grid gap-4 sm:grid-cols-2">
          <FormField>
            <FormLabel htmlFor="membership-person-id">Person ID</FormLabel>
            <Input
              id="membership-person-id"
              value={personId}
              onChange={(event) => setPersonId(event.target.value)}
              required
              disabled={isLoading}
            />
          </FormField>

          <FormField>
            <FormLabel htmlFor="membership-organization-id">Organization ID</FormLabel>
            <Input
              id="membership-organization-id"
              value={organizationId}
              onChange={(event) => setOrganizationId(event.target.value)}
              required
              disabled={isLoading}
            />
          </FormField>

          <FormField>
            <FormLabel htmlFor="membership-role-id">Role ID</FormLabel>
            <Input
              id="membership-role-id"
              value={roleId}
              onChange={(event) => setRoleId(event.target.value)}
              required
              disabled={isLoading}
            />
          </FormField>

          <FormField>
            <FormLabel htmlFor="membership-home-node-id">Home Node ID</FormLabel>
            <Input
              id="membership-home-node-id"
              value={homeNodeId}
              onChange={(event) => setHomeNodeId(event.target.value)}
              disabled={isLoading}
              placeholder="Optional"
            />
            <FormHelperText>Optional structural anchor, if an Organization Node already exists.</FormHelperText>
          </FormField>
        </div>

        <FormField>
          <FormLabel>Membership Type</FormLabel>
          <div className="flex gap-2">
            {MEMBERSHIP_TYPES.map((type) => (
              <Button
                key={type}
                type="button"
                variant={membershipType === type ? "primary" : "secondary"}
                onClick={() => setMembershipType(type)}
                disabled={isLoading}
              >
                {type}
              </Button>
            ))}
          </div>
        </FormField>

        <FormField>
          <FormLabel>License Type</FormLabel>
          <div className="flex gap-2">
            {LICENSE_TYPES.map((type) => (
              <Button
                key={type}
                type="button"
                variant={licenseType === type ? "primary" : "secondary"}
                onClick={() => setLicenseType(type)}
                disabled={isLoading}
              >
                {type}
              </Button>
            ))}
          </div>
        </FormField>

        <Button type="submit" disabled={isLoading}>
          {isLoading && <Spinner className="mr-2" />}
          Establish Membership
        </Button>
      </form>

      {state.status === "establish-error" && (
        <div className="mt-4">
          <FormBanner tone="danger">
            {state.isConflict
              ? "A Membership already exists for this Person and Organization, or the supplied home node is not active."
              : state.message}
          </FormBanner>
        </div>
      )}

      {state.status === "established" && (
        <div className="mt-4">
          <FormBanner tone="success">
            Membership {state.membership.id} established — status {state.membership.membership_status}.
          </FormBanner>
        </div>
      )}
    </Card>
  );
}
