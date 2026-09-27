"use client";

import { useMemo, useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { FormBanner, FormField, FormHelperText, FormLabel } from "@/components/ui/Form";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { StatusBadge } from "@/components/ui/StatusBadge";
import type { EstablishState } from "@/features/offering-catalog/state/useOfferingCatalog";
import type {
  EstablishOfferingDefinitionRequest,
  OfferingKind,
} from "@/types/offering";

const OFFERING_KINDS: OfferingKind[] = ["PRODUCT", "SERVICE"];

/**
 * C-021 WP-20 BA-01 — establish one standalone Atomic Offering Definition in
 * `draft` (ROD-C021 D4/D7). `category_ref` and `list_price_reference` are
 * optional, opaque references only (RO decision O2; ROD-C021 D6) — no
 * taxonomy picker, no price calculator. There is no publish / retire /
 * composition / relationship control here — those are excluded from BA-01.
 */
export function EstablishOfferingDefinitionSection({
  state,
  onEstablish,
}: {
  state: EstablishState;
  onEstablish: (fields: EstablishOfferingDefinitionRequest) => void;
}) {
  const [offeringName, setOfferingName] = useState("");
  const [offeringKind, setOfferingKind] = useState<OfferingKind>("SERVICE");
  const [categoryRef, setCategoryRef] = useState("");
  const [listPriceReference, setListPriceReference] = useState("");

  const isLoading = state.status === "establishing";
  const canSubmit = offeringName.trim().length > 0 && !isLoading;

  const request = useMemo<EstablishOfferingDefinitionRequest>(() => {
    const body: EstablishOfferingDefinitionRequest = {
      offering_name: offeringName.trim(),
      offering_kind: offeringKind,
    };
    if (categoryRef.trim().length > 0) body.category_ref = categoryRef.trim();
    if (listPriceReference.trim().length > 0) body.list_price_reference = listPriceReference.trim();
    return body;
  }, [offeringName, offeringKind, categoryRef, listPriceReference]);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (canSubmit) onEstablish(request);
  }

  return (
    <Card>
      <CardTitle>Establish Offering Definition</CardTitle>
      <CardDescription>
        Create the enterprise&apos;s authoritative definition of a standalone Atomic Offering. It is
        established in <strong>draft</strong>; its Offering Reference is assigned by the platform
        (COM-001-001). Publication, retirement, composition, pricing, and availability are out of
        scope for this Business Activity.
      </CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <div className="grid gap-4 sm:grid-cols-2">
          <FormField>
            <FormLabel htmlFor="offering-name">Offering Name</FormLabel>
            <Input
              id="offering-name"
              value={offeringName}
              onChange={(event) => setOfferingName(event.target.value)}
              required
              disabled={isLoading}
              placeholder="e.g. Enterprise ESG Reporting"
            />
          </FormField>

          <FormField>
            <FormLabel>Classification</FormLabel>
            <div className="flex gap-2">
              {OFFERING_KINDS.map((kind) => (
                <Button
                  key={kind}
                  type="button"
                  variant={offeringKind === kind ? "primary" : "secondary"}
                  onClick={() => setOfferingKind(kind)}
                  disabled={isLoading}
                >
                  {kind === "PRODUCT" ? "Product" : "Service"}
                </Button>
              ))}
            </div>
          </FormField>
        </div>

        <FormField>
          <FormLabel htmlFor="offering-category">Category Reference</FormLabel>
          <Input
            id="offering-category"
            value={categoryRef}
            onChange={(event) => setCategoryRef(event.target.value)}
            disabled={isLoading}
            placeholder="Optional — opaque reference only"
          />
          <FormHelperText>
            Optional. An opaque reference, not a governed taxonomy value — there is no category
            catalog to choose from.
          </FormHelperText>
        </FormField>

        <FormField>
          <FormLabel htmlFor="offering-list-price">List-Price Reference</FormLabel>
          <Input
            id="offering-list-price"
            value={listPriceReference}
            onChange={(event) => setListPriceReference(event.target.value)}
            disabled={isLoading}
            placeholder="Optional — a reference string, never a price"
          />
          <FormHelperText>
            Optional. A reference to an externally-held list price. C-021 never computes, rates, or
            discounts a price.
          </FormHelperText>
        </FormField>

        <Button type="submit" disabled={!canSubmit}>
          {isLoading && <Spinner className="mr-2" />}
          Establish Offering Definition
        </Button>
      </form>

      {state.status === "established" && (
        <div className="mt-4 space-y-2">
          <FormBanner tone="success">
            Established <strong>{state.offering.offering_reference}</strong> — “{state.offering.offering_name}”.
          </FormBanner>
          <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
            <StatusBadge tone="info">{state.offering.offering_kind}</StatusBadge>
            <StatusBadge tone="muted">state: {state.offering.state}</StatusBadge>
            <span>Offering Reference: {state.offering.offering_reference}</span>
          </div>
        </div>
      )}

      {state.status === "error" && (
        <div className="mt-4">
          <FormBanner tone="danger">
            {state.isAuthDenied
              ? "You do not hold the PLATFORM_ADMIN role required to manage the catalog."
              : state.isConflict
                ? "The platform could not allocate a unique Offering Reference — please retry."
                : state.message}
          </FormBanner>
        </div>
      )}
    </Card>
  );
}
