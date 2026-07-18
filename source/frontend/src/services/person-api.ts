/**
 * Person Management API wrapper — the only module permitted to call
 * POST /person/recognize or POST /person/establish. Built on the shared
 * `apiClient` (src/lib/api-client.ts), not raw fetch. No endpoint beyond
 * these two exists here; none is invented.
 */

import { apiClient } from "@/lib/api-client";
import type {
  EstablishPersonRequest,
  PersonReferenceRequest,
  PersonRecognitionResponse,
  AuthoritativePersonContext,
} from "@/types/person";

export function recognizePerson(request: PersonReferenceRequest): Promise<PersonRecognitionResponse> {
  return apiClient.post<PersonRecognitionResponse>("/person/recognize", request);
}

export function establishPerson(request: EstablishPersonRequest): Promise<AuthoritativePersonContext> {
  return apiClient.post<AuthoritativePersonContext>("/person/establish", request);
}
