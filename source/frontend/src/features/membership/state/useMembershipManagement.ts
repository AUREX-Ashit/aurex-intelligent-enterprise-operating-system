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
 * Single owner of Membership Management's business-flow state (Establish,
 * Understand, Change Terms, My Portfolio), mirroring
 * useIdentityManagement.ts's combined-hook pattern for a multi-action
 * feature screen: form components own only their own transient input
 * values; everything about each action's own outcome, and any error from
 * producing it, lives here exactly once.
 */
export type MembershipManagementState =
  | { status: "idle" }
  | { status: "establishing" }
  | { status: "established"; membership: MembershipResponse }
  | { status: "establish-error"; message: string; isConflict: boolean }
  | { status: "understanding" }
  | { status: "understood"; membership: MembershipUnderstandingResponse }
  | { status: "understand-not-found" }
  | { status: "understand-error"; message: string }
  | { status: "changing-terms" }
  | { status: "terms-changed"; membership: MembershipResponse }
  | { status: "terms-error"; message: string }
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
  const [state, setState] = useState<MembershipManagementState>({ status: "idle" });
  const { notify } = useNotifications();

  const establish = useCallback(
    async (fields: EstablishMembershipRequest) => {
      setState({ status: "establishing" });
      try {
        const membership = await establishMembership(fields);
        setState({ status: "established", membership });
        notify("Membership successfully established.", "success");
      } catch (error) {
        const { message, isNetworkError, status } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setState({ status: "establish-error", message, isConflict: status === 409 });
      }
    },
    [notify],
  );

  const understand = useCallback(
    async (membershipId: string) => {
      setState({ status: "understanding" });
      try {
        const membership = await understandMembership(membershipId);
        setState({ status: "understood", membership });
      } catch (error) {
        const { message, isNetworkError, status } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setState(status === 404 ? { status: "understand-not-found" } : { status: "understand-error", message });
      }
    },
    [notify],
  );

  const changeTerms = useCallback(
    async (membershipId: string, fields: ChangeMembershipTermsRequest) => {
      setState({ status: "changing-terms" });
      try {
        const membership = await changeMembershipTerms(membershipId, fields);
        setState({ status: "terms-changed", membership });
        notify("Membership terms updated.", "success");
      } catch (error) {
        const { message, isNetworkError } = describeError(error);
        if (isNetworkError) notify(message, "danger");
        setState({ status: "terms-error", message });
      }
    },
    [notify],
  );

  const loadPortfolio = useCallback(async () => {
    setState({ status: "loading-portfolio" });
    try {
      const portfolio = await getOwnMembershipPortfolio();
      setState({ status: "portfolio-loaded", portfolio });
    } catch (error) {
      const { message, isNetworkError } = describeError(error);
      if (isNetworkError) notify(message, "danger");
      setState({ status: "portfolio-error", message });
    }
  }, [notify]);

  const reset = useCallback(() => setState({ status: "idle" }), []);

  return { state, establish, understand, changeTerms, loadPortfolio, reset };
}
