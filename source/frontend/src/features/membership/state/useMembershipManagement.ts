"use client";

import { useCallback, useState } from "react";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import {
  changeMembershipTerms,
  establishMembership,
  getOwnMembershipPortfolio,
  understandMembership,
} from "@/services/membership-api";
import type {
  ChangeMembershipTermsRequest,
  EstablishMembershipRequest,
  MembershipPortfolioResponse,
  MembershipResponse,
  MembershipUnderstandingResponse,
} from "@/types/membership";

/**
 * Membership Management's business-flow state, split into three
 * independent slices (Establish, Understand/Change Terms, My Portfolio)
 * rather than one shared discriminated union. MembershipManagementScreen
 * renders all three sections simultaneously (not tabs), so a single shared
 * union previously meant acting in one section (e.g. Establish) reset
 * `status` out from under the other two, silently blanking an
 * already-displayed result (e.g. the Portfolio table or an Understood
 * Membership) that had nothing to do with the action just taken.
 * Independent slices preserve each section's own last result regardless of
 * what the others are doing, mirroring useOrganizationStructure.ts's own
 * per-section state slices.
 */
export type MembershipEstablishState =
  | { status: "idle" }
  | { status: "establishing" }
  | { status: "established"; membership: MembershipResponse }
  | { status: "establish-error"; message: string; isConflict: boolean };

export type MembershipUnderstandState =
  | { status: "idle" }
  | { status: "understanding" }
  | { status: "understood"; membership: MembershipUnderstandingResponse }
  | { status: "understand-not-found" }
  | { status: "understand-error"; message: string }
  | { status: "changing-terms" }
  | { status: "terms-changed"; membership: MembershipResponse }
  | { status: "terms-error"; message: string };

export type MembershipPortfolioState =
  | { status: "idle" }
  | { status: "loading-portfolio" }
  | { status: "portfolio-loaded"; portfolio: MembershipPortfolioResponse }
  | { status: "portfolio-error"; message: string };

function describeError(error: unknown): { message: string; isNetworkError: boolean; status: number } {
  if (error instanceof ApiError) {
    return { message: error.message, isNetworkError: error.status === 0, status: error.status };
  }
  return {
    message: "Unable to reach the server. Check your connection and try again.",
    isNetworkError: true,
    status: 0,
  };
}

export function useMembershipManagement() {
  const [establishState, setEstablishState] = useState<MembershipEstablishState>({ status: "idle" });
  const [understandState, setUnderstandState] = useState<MembershipUnderstandState>({ status: "idle" });
  const [portfolioState, setPortfolioState] = useState<MembershipPortfolioState>({ status: "idle" });
  const { notify } = useNotifications();

  const establish = useCallback(
    async (fields: EstablishMembershipRequest) => {
      setEstablishState({ status: "establishing" });
      try {
        const membership = await establishMembership(fields);
        setEstablishState({ status: "established", membership });
        notify("Membership successfully established.", "success");
      } catch (error) {
        const { message, isNetworkError, status } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setEstablishState({ status: "establish-error", message, isConflict: status === 409 });
      }
    },
    [notify],
  );

  const understand = useCallback(
    async (membershipId: string) => {
      setUnderstandState({ status: "understanding" });
      try {
        const membership = await understandMembership(membershipId);
        setUnderstandState({ status: "understood", membership });
      } catch (error) {
        const { message, isNetworkError, status } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setUnderstandState(
          status === 404 ? { status: "understand-not-found" } : { status: "understand-error", message },
        );
      }
    },
    [notify],
  );

  const changeTerms = useCallback(
    async (membershipId: string, fields: ChangeMembershipTermsRequest) => {
      setUnderstandState({ status: "changing-terms" });
      try {
        const membership = await changeMembershipTerms(membershipId, fields);
        setUnderstandState({ status: "terms-changed", membership });
        notify("Membership terms updated.", "success");
      } catch (error) {
        const { message, isNetworkError } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setUnderstandState({ status: "terms-error", message });
      }
    },
    [notify],
  );

  const loadPortfolio = useCallback(async () => {
    setPortfolioState({ status: "loading-portfolio" });
    try {
      const portfolio = await getOwnMembershipPortfolio();
      setPortfolioState({ status: "portfolio-loaded", portfolio });
    } catch (error) {
      const { message, isNetworkError } = describeError(error);
      if (isNetworkError) notify(message, "danger");
      setPortfolioState({ status: "portfolio-error", message });
    }
  }, [notify]);

  const reset = useCallback(() => {
    setEstablishState({ status: "idle" });
    setUnderstandState({ status: "idle" });
    setPortfolioState({ status: "idle" });
  }, []);

  return {
    establishState,
    understandState,
    portfolioState,
    establish,
    understand,
    changeTerms,
    loadPortfolio,
    reset,
  };
}
