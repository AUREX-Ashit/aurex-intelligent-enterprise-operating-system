"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import { registerIntelligenceCandidate, resolveIntelligenceCandidate } from "@/services/intelligence-candidate-api";
import type {
  IntelligenceCandidateResponse,
  RegisterIntelligenceCandidateRequest,
  ResolveIntelligenceCandidateRequest,
  ResolvedIntelligenceCandidateResponse,
} from "@/types/intelligence-candidate";

/**
 * WP-14 BA-02/BA-03 — Register + Resolve Enterprise Intelligence
 * Candidate (C-090). Two independent state slices, mirroring
 * useSearchManagement.ts's own established precedent (multiple Business
 * Activities on one shared resource, acting on one never blanks the
 * other). No List slice exists — no GET/list endpoint is built by either
 * Business Activity (IRA-014 §6 names only POST register and POST
 * .../resolve for this resource); BA-03's own resolve path takes a
 * caller-supplied candidate id directly, mirroring BA-04's own
 * established "status view by id" precedent, not a browsable queue.
 */
export type IntelligenceCandidateRegisterState =
  | { status: "idle" }
  | { status: "registering" }
  | { status: "registered"; candidate: IntelligenceCandidateResponse }
  | { status: "register-error"; message: string };

export type IntelligenceCandidateResolveState =
  | { status: "idle" }
  | { status: "resolving" }
  | { status: "resolved"; result: ResolvedIntelligenceCandidateResponse }
  | { status: "resolve-error"; message: string };

function describeError(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  return "Unable to reach the server. Check your connection and try again.";
}

export function useIntelligenceCandidateManagement() {
  const [registerState, setRegisterState] = useState<IntelligenceCandidateRegisterState>({ status: "idle" });
  const [resolveState, setResolveState] = useState<IntelligenceCandidateResolveState>({ status: "idle" });
  const { notify } = useNotifications();

  const register = useCallback(
    async (request: RegisterIntelligenceCandidateRequest) => {
      setRegisterState({ status: "registering" });
      try {
        const candidate = await registerIntelligenceCandidate(request);
        setRegisterState({ status: "registered", candidate });
        notify(`Intelligence candidate registered — status ${candidate.resolution_status}.`, "success");
      } catch (error) {
        const message = describeError(error);
        if (error instanceof ApiError && error.status === 0) notify(message, "danger");
        setRegisterState({ status: "register-error", message });
      }
    },
    [notify],
  );

  const resolve = useCallback(
    async (unclassifiedId: string, request: ResolveIntelligenceCandidateRequest) => {
      setResolveState({ status: "resolving" });
      try {
        const result = await resolveIntelligenceCandidate(unclassifiedId, request);
        setResolveState({ status: "resolved", result });
        notify(`Candidate resolved — outcome ${result.resolution_status}.`, "success");
      } catch (error) {
        const message = describeError(error);
        if (error instanceof ApiError && error.status === 0) notify(message, "danger");
        setResolveState({ status: "resolve-error", message });
      }
    },
    [notify],
  );

  return { registerState, register, resolveState, resolve };
}
