"use client";

import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { useOrganizationStructure } from "@/features/organization-structure/state/useOrganizationStructure";
import { EstablishOrganizationNodeSection } from "@/features/organization-structure/components/EstablishOrganizationNodeSection";
import { ViewOrganizationNodeSection } from "@/features/organization-structure/components/ViewOrganizationNodeSection";

export function OrganizationStructureScreen() {
  const { establishState, viewState, establish, view } = useOrganizationStructure();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Enterprise Structure</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Establish and view organization nodes (C-005).
        </p>
      </div>

      <ViewOrganizationNodeSection state={viewState} onView={view} />
      <EstablishOrganizationNodeSection state={establishState} onEstablish={establish} />

      <Card>
        <CardTitle>Structural Transitions</CardTitle>
        <CardDescription>
          Structural Change Intents, Proposals, Impact Assessments, Reviews, Validations, and
          Completions (WP-04&rsquo;s own multi-step structural transition lifecycle) are not yet
          surfaced in this Workspace — this screen covers Establish and Understand Structural
          Position only. Extending this screen to the full transition lifecycle is a distinct,
          larger scope not attempted in this pass.
        </CardDescription>
      </Card>
    </div>
  );
}
