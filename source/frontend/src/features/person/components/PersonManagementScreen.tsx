"use client";

import { usePersonManagement } from "@/features/person/state/usePersonManagement";
import { RecognizePersonSection } from "@/features/person/components/RecognizePersonSection";
import { EstablishPersonSection } from "@/features/person/components/EstablishPersonSection";
import { PersonResultPanel } from "@/features/person/components/PersonResultPanel";

export function PersonManagementScreen() {
  const { state, recognize, establish } = usePersonManagement();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Person Management</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Recognize an existing person, or establish a new one when none exists.
        </p>
      </div>

      <RecognizePersonSection state={state} onRecognize={recognize} />

      {(state.status === "no-candidate" ||
        state.status === "establishing" ||
        state.status === "establish-error") && (
        <EstablishPersonSection state={state} email={state.email} onEstablish={establish} />
      )}

      <PersonResultPanel state={state} />
    </div>
  );
}
