/**
 * Mirrors AuthService's schemas/person.py exactly. No field added, renamed,
 * or omitted relative to the backend contract (EX-C006-01, EX-C006-02).
 */

export interface PersonReferenceRequest {
  email: string;
}

export interface EstablishPersonRequest {
  email: string;
  first_name: string;
  last_name: string;
  display_name: string;
}

export interface AuthoritativePersonContext {
  person_id: string;
  first_name: string;
  last_name: string;
  display_name: string;
}

export type PersonRecognitionOutcome = "MATCHED" | "NO_CANDIDATE";

export interface PersonRecognitionResponse {
  outcome: PersonRecognitionOutcome;
  person: AuthoritativePersonContext | null;
}
