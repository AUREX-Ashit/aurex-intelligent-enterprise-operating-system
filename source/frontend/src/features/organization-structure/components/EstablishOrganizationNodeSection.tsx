"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { Card, CardTitle, CardDescription } from "@/components/ui/Card";
import { FormField, FormLabel, FormBanner, FormHelperText } from "@/components/ui/Form";
import type { OrganizationStructureState } from "@/features/organization-structure/state/useOrganizationStructure";
import type { EstablishOrganizationNodeRequest } from "@/types/organization-node";

export function EstablishOrganizationNodeSection({
  state,
  onEstablish,
}: {
  state: OrganizationStructureState;
  onEstablish: (fields: EstablishOrganizationNodeRequest) => void;
}) {
  const [nodeCode, setNodeCode] = useState("");
  const [nodeName, setNodeName] = useState("");
  const [nodeType, setNodeType] = useState("");
  const [legalEntityName, setLegalEntityName] = useState("");
  const [businessUnit, setBusinessUnit] = useState("");
  const [sector, setSector] = useState("");
  const isLoading = state.status === "establishing";

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onEstablish({
      node_code: nodeCode,
      node_name: nodeName,
      node_type: nodeType,
      legal_entity_name: legalEntityName || null,
      business_unit: businessUnit || null,
      sector: sector || null,
      operational_status: "ACTIVE",
    });
  }

  return (
    <Card>
      <CardTitle>Establish Organization Node</CardTitle>
      <CardDescription>
        Register a structural entity (holding, region, entity, site, supplier, joint venture) in
        the enterprise structure.
      </CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <div className="grid gap-4 sm:grid-cols-2">
          <FormField>
            <FormLabel htmlFor="node-code">Node Code</FormLabel>
            <Input id="node-code" value={nodeCode} onChange={(event) => setNodeCode(event.target.value)} required disabled={isLoading} />
          </FormField>

          <FormField>
            <FormLabel htmlFor="node-name">Node Name</FormLabel>
            <Input id="node-name" value={nodeName} onChange={(event) => setNodeName(event.target.value)} required disabled={isLoading} />
          </FormField>

          <FormField>
            <FormLabel htmlFor="node-type">Node Type</FormLabel>
            <Input
              id="node-type"
              value={nodeType}
              onChange={(event) => setNodeType(event.target.value)}
              required
              disabled={isLoading}
              placeholder="e.g. HOLDING, REGION, ENTITY, SITE"
            />
            <FormHelperText>Free text — not a closed list.</FormHelperText>
          </FormField>

          <FormField>
            <FormLabel htmlFor="node-legal-entity-name">Legal Entity Name</FormLabel>
            <Input
              id="node-legal-entity-name"
              value={legalEntityName}
              onChange={(event) => setLegalEntityName(event.target.value)}
              disabled={isLoading}
              placeholder="Optional"
            />
          </FormField>

          <FormField>
            <FormLabel htmlFor="node-business-unit">Business Unit</FormLabel>
            <Input
              id="node-business-unit"
              value={businessUnit}
              onChange={(event) => setBusinessUnit(event.target.value)}
              disabled={isLoading}
              placeholder="Optional"
            />
          </FormField>

          <FormField>
            <FormLabel htmlFor="node-sector">Sector</FormLabel>
            <Input
              id="node-sector"
              value={sector}
              onChange={(event) => setSector(event.target.value)}
              disabled={isLoading}
              placeholder="Optional"
            />
          </FormField>
        </div>

        <Button type="submit" disabled={isLoading}>
          {isLoading && <Spinner className="mr-2" />}
          Establish Node
        </Button>
      </form>

      {state.status === "establish-error" && (
        <div className="mt-4">
          <FormBanner tone="danger">
            {state.isConflict ? "An organization node with this node_code already exists." : state.message}
          </FormBanner>
        </div>
      )}

      {state.status === "established" && (
        <div className="mt-4">
          <FormBanner tone="success">
            Organization node {state.node.node_name} ({state.node.id}) established.
          </FormBanner>
        </div>
      )}
    </Card>
  );
}
