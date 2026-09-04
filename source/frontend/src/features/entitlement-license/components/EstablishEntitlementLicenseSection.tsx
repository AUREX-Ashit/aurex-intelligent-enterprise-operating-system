"use client";

import { useMemo, useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { Card, CardTitle, CardDescription } from "@/components/ui/Card";
import { FormField, FormLabel, FormBanner, FormHelperText } from "@/components/ui/Form";
import type { EstablishState } from "@/features/entitlement-license/state/useEntitlementLicense";
import type {
  C023LicenseType,
  EstablishEntitlementLicenseRequest,
} from "@/types/entitlement-license";

const SPECIALIZED_LICENSE_TYPES: C023LicenseType[] = [
  "SUPPLIER",
  "AUDITOR",
  "BOARD_MEMBER",
  "CONSULTANT",
];

function toIsoOrNull(local: string): string | null {
  if (!local) return null;
  const parsed = new Date(local);
  return Number.isNaN(parsed.getTime()) ? null : parsed.toISOString();
}

export function EstablishEntitlementLicenseSection({
  state,
  onEstablish,
}: {
  state: EstablishState;
  onEstablish: (fields: EstablishEntitlementLicenseRequest) => void;
}) {
  const [membershipId, setMembershipId] = useState("");
  const [licenseType, setLicenseType] = useState<C023LicenseType | "">("");
  const [organizationId, setOrganizationId] = useState("");
  const [domainId, setDomainId] = useState("");
  const [entitlementTypeRef, setEntitlementTypeRef] = useState("");
  const [sourceReference, setSourceReference] = useState("");
  const [effectiveFrom, setEffectiveFrom] = useState("");
  const [effectiveTo, setEffectiveTo] = useState("");

  const isLoading = state.status === "establishing";
  const establishLicense = membershipId.trim().length > 0;
  const establishEntitlement = organizationId.trim().length > 0;
  const entitlementIncomplete = establishEntitlement && entitlementTypeRef.trim().length === 0;
  const canSubmit =
    (establishLicense || establishEntitlement) && !entitlementIncomplete && !isLoading;

  const request = useMemo<EstablishEntitlementLicenseRequest>(() => {
    const body: EstablishEntitlementLicenseRequest = {};
    if (establishLicense) {
      body.membership_id = membershipId.trim();
      if (licenseType) body.c023_license_type = licenseType;
    }
    if (establishEntitlement) {
      body.organization_id = organizationId.trim();
      body.entitlement_type_ref = entitlementTypeRef.trim();
      if (domainId.trim()) body.domain_id = domainId.trim();
    }
    if (sourceReference.trim()) body.entitlement_source_reference = sourceReference.trim();
    const from = toIsoOrNull(effectiveFrom);
    const to = toIsoOrNull(effectiveTo);
    if (from) body.effective_from = from;
    if (to) body.effective_to = to;
    return body;
  }, [
    establishLicense,
    establishEntitlement,
    membershipId,
    licenseType,
    organizationId,
    entitlementTypeRef,
    domainId,
    sourceReference,
    effectiveFrom,
    effectiveTo,
  ]);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!canSubmit) return;
    onEstablish(request);
  }

  return (
    <Card>
      <CardTitle>Establish License / Entitlement</CardTitle>
      <CardDescription>
        Commits exactly one Authoritative License Context (per Membership) and/or one Authoritative
        Entitlement Context (per Organization, optionally Domain-scoped), with an{" "}
        <span className="font-semibold">ACTIVE</span> continuing outcome. Requires the
        currently-active &ldquo;Entitlement/License Commit Authority&rdquo; for your Organization.
        The base FULL/LIGHT license classification stays on the Membership and is never changed
        here.
      </CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 space-y-6">
        <fieldset
          className="border-border-muted space-y-4 rounded-md border p-4"
          disabled={isLoading}
        >
          <legend className="text-foreground px-1 text-sm font-semibold">
            License (Membership-anchored)
          </legend>
          <FormField>
            <FormLabel htmlFor="elc-membership-id">Membership ID</FormLabel>
            <Input
              id="elc-membership-id"
              value={membershipId}
              onChange={(event) => setMembershipId(event.target.value)}
              placeholder="Leave blank to establish an Entitlement only"
            />
            <FormHelperText>
              Must belong to the Organization this session is scoped to.
            </FormHelperText>
          </FormField>
          <FormField>
            <FormLabel>Specialized License Type</FormLabel>
            <div className="flex flex-wrap gap-2">
              <Button
                type="button"
                variant={licenseType === "" ? "primary" : "secondary"}
                onClick={() => setLicenseType("")}
              >
                None
              </Button>
              {SPECIALIZED_LICENSE_TYPES.map((type) => (
                <Button
                  key={type}
                  type="button"
                  variant={licenseType === type ? "primary" : "secondary"}
                  onClick={() => setLicenseType(type)}
                >
                  {type}
                </Button>
              ))}
            </div>
            <FormHelperText>
              Optional. One of the four URA-001-115 specialized types — never FULL or LIGHT.
            </FormHelperText>
          </FormField>
        </fieldset>

        <fieldset
          className="border-border-muted space-y-4 rounded-md border p-4"
          disabled={isLoading}
        >
          <legend className="text-foreground px-1 text-sm font-semibold">
            Entitlement (Organization-anchored)
          </legend>
          <div className="grid gap-4 sm:grid-cols-2">
            <FormField>
              <FormLabel htmlFor="elc-organization-id">Organization ID</FormLabel>
              <Input
                id="elc-organization-id"
                value={organizationId}
                onChange={(event) => setOrganizationId(event.target.value)}
                placeholder="Must equal your Organization"
              />
            </FormField>
            <FormField>
              <FormLabel htmlFor="elc-domain-id">Domain ID</FormLabel>
              <Input
                id="elc-domain-id"
                value={domainId}
                onChange={(event) => setDomainId(event.target.value)}
                placeholder="Optional — organization-wide if blank"
              />
            </FormField>
          </div>
          <FormField>
            <FormLabel htmlFor="elc-entitlement-type">Entitlement Type</FormLabel>
            <Input
              id="elc-entitlement-type"
              value={entitlementTypeRef}
              onChange={(event) => setEntitlementTypeRef(event.target.value)}
              placeholder="An already-recognized Entitlement Type identifier"
              aria-invalid={entitlementIncomplete}
            />
            {entitlementIncomplete && (
              <FormHelperText>Required when an Organization ID is provided.</FormHelperText>
            )}
            <FormHelperText>
              This Business Activity references already-recognized Entitlement Types only and never
              creates one. The Global Entitlement Type Catalog is not yet available, so the
              Entitlement path is currently expected to be rejected.
            </FormHelperText>
          </FormField>
        </fieldset>

        <div className="grid gap-4 sm:grid-cols-3">
          <FormField>
            <FormLabel htmlFor="elc-source-ref">Entitlement Source Reference</FormLabel>
            <Input
              id="elc-source-ref"
              value={sourceReference}
              onChange={(event) => setSourceReference(event.target.value)}
              placeholder="Defaults to ADMINISTRATIVE"
              disabled={isLoading}
            />
          </FormField>
          <FormField>
            <FormLabel htmlFor="elc-effective-from">Effective From</FormLabel>
            <Input
              id="elc-effective-from"
              type="datetime-local"
              value={effectiveFrom}
              onChange={(event) => setEffectiveFrom(event.target.value)}
              disabled={isLoading}
            />
            <FormHelperText>Defaults to now.</FormHelperText>
          </FormField>
          <FormField>
            <FormLabel htmlFor="elc-effective-to">Effective To</FormLabel>
            <Input
              id="elc-effective-to"
              type="datetime-local"
              value={effectiveTo}
              onChange={(event) => setEffectiveTo(event.target.value)}
              disabled={isLoading}
            />
            <FormHelperText>Blank = open-ended.</FormHelperText>
          </FormField>
        </div>

        {!establishLicense && !establishEntitlement && (
          <FormHelperText>
            Enter a Membership ID (to establish a License), an Organization ID with an Entitlement
            Type (to establish an Entitlement), or both.
          </FormHelperText>
        )}

        <Button type="submit" disabled={!canSubmit}>
          {isLoading && <Spinner className="mr-2" />}
          Establish
        </Button>
      </form>

      {state.status === "error" && (
        <div className="mt-4">
          <FormBanner tone="danger">
            {state.isAuthDenied
              ? "The “Entitlement/License Commit Authority” is not satisfied for this request, or an anchor belongs to a different Organization."
              : state.isConflict
                ? "A current Authoritative Context already exists for this anchor (INV-C023-09 / INV-C023-10)."
                : state.message}
          </FormBanner>
        </div>
      )}

      {state.status === "established" && (
        <div className="mt-4 space-y-2">
          <FormBanner tone="success">Establishment committed.</FormBanner>
          {state.result.license && (
            <EstablishedRow
              label="License Context"
              id={state.result.license.id}
              badge={state.result.license.status}
              detail={
                state.result.license.c023_license_type
                  ? `Membership ${state.result.license.membership_id} · ${state.result.license.c023_license_type}`
                  : `Membership ${state.result.license.membership_id}`
              }
              from={state.result.license.effective_from}
              to={state.result.license.effective_to}
            />
          )}
          {state.result.entitlement && (
            <EstablishedRow
              label="Entitlement Context"
              id={state.result.entitlement.id}
              badge={state.result.entitlement.status}
              detail={`Organization ${state.result.entitlement.organization_id} · ${state.result.entitlement.entitlement_type_ref}`}
              from={state.result.entitlement.effective_from}
              to={state.result.entitlement.effective_to}
            />
          )}
        </div>
      )}
    </Card>
  );
}

function EstablishedRow({
  label,
  id,
  badge,
  detail,
  from,
  to,
}: {
  label: string;
  id: string;
  badge: string;
  detail: string;
  from: string;
  to: string | null;
}) {
  return (
    <div className="border-border-muted bg-surface-muted rounded-md border p-3 text-sm">
      <div className="flex items-center justify-between gap-2">
        <span className="text-foreground font-semibold">{label}</span>
        <StatusBadge tone={badge === "ACTIVE" ? "success" : "muted"}>{badge}</StatusBadge>
      </div>
      <p className="text-muted-foreground mt-1">{detail}</p>
      <p className="text-muted-foreground mt-1 font-mono text-xs">{id}</p>
      <p className="text-muted-foreground mt-1 text-xs">
        Effective {new Date(from).toLocaleString()} &rarr;{" "}
        {to ? new Date(to).toLocaleString() : "open-ended"}
      </p>
    </div>
  );
}
