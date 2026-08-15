"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import { registerIntelligenceCandidate } from "@/services/intelligence-candidate-api";
import type {
  IntelligenceCandidateResponse,
  RegisterIntelligenceCandidateRequest,
} from "@/types/intelligence-candidate";

/**
 * WP-14 BA-02 — Register Enterprise Intelligence Candidate (C-090). A
 * single Register state slice — no List slice exists, mirroring the
 * backend's own deliberate scope decision (no GET/list endpoint; a
 * resolution/listing surface is BA-03's own "resolution queue" scope,
 * IRA-014 §9 Plan B). The just-registered candidate is shown directly
 * from the register response — no polling/lookup capability.
 */
export type IntelligenceCandidateRegisterState =
  | { status: "idle" }
  | { status: "registering" }
  | { status: "registered"; candidate: IntelligenceCandidateResponse }
  | { status: "register-error"; message: string };

function describeError(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  return "Unable to reach the server. Check your connection and try again.";
}

export function useIntelligenceCandidateManagement() {
  const [registerState, setRegisterState] = useState<IntelligenceCandidateRegisterState>({ status: "idle" });
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

  return { registerState, register };
}
