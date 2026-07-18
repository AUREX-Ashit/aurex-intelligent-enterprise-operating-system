import { Card, CardTitle } from "@/components/ui/Card";
import { StatusBadge } from "@/components/ui/StatusBadge";
import type { PersonManagementState } from "@/features/person/state/usePersonManagement";
import type { PersonRecognitionOutcome } from "@/types/person";

// The Recognition Outcome shown here is always the actual value the backend
// returned from recognition — for an established person, that is
// NO_CANDIDATE (the precondition that made establishment possible in the
// first place), never a fabricated third value. establishPerson's response
// (AuthoritativePersonContext) has no outcome field of its own to report.
const OUTCOME_BY_STATUS: Partial<Record<PersonManagementState["status"], PersonRecognitionOutcome>> = {
  matched: "MATCHED",
  established: "NO_CANDIDATE",
};

export function PersonResultPanel({ state }: { state: PersonManagementState }) {
  const person = state.status === "matched" || state.status === "established" ? state.person : null;
  const outcome = OUTCOME_BY_STATUS[state.status];

  return (
    <Card>
      <CardTitle>Result</CardTitle>

      {!person && (
        <p className="mt-2 text-sm text-muted-foreground">Recognize a person to see results here.</p>
      )}

      {person && (
        <dl className="mt-4 grid grid-cols-[140px_1fr] gap-y-3 text-sm">
          <dt className="font-semibold text-muted-foreground">Person ID</dt>
          <dd className="text-foreground">{person.person_id}</dd>

          <dt className="font-semibold text-muted-foreground">Display Name</dt>
          <dd className="text-foreground">{person.display_name}</dd>

          <dt className="font-semibold text-muted-foreground">Recognition Outcome</dt>
          <dd>
            <StatusBadge tone={outcome === "MATCHED" ? "success" : "warning"}>{outcome}</StatusBadge>
          </dd>
        </dl>
      )}
    </Card>
  );
}
