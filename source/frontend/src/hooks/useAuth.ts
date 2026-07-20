"use client";

import { useCallback, useEffect, useState } from "react";
import { authStorage } from "@/lib/auth-storage";
import { decodeJwtPayload } from "@/lib/jwt";
import { refresh as refreshRequest } from "@/services/auth-api";
import { ApiError } from "@/lib/api-client";
import type { AuthClaims } from "@/types/auth";

export type AuthSession =
  | { status: "loading" }
  | { status: "unauthenticated" }
  | { status: "authenticated"; claims: AuthClaims };

function decodeIfValid(token: string): AuthClaims | null {
  const claims = decodeJwtPayload<AuthClaims>(token);
  if (!claims) return null;
  if (claims.exp && claims.exp * 1000 <= Date.now()) return null;
  return claims;
}

/**
 * Resolves the session on load. If the stored access token is missing or
 * expired but a refresh token is on hand, attempts one silent renewal
 * (AuthService's POST /auth/refresh) before falling back to
 * "unauthenticated" — this is Session Expiry Handling for the case where a
 * user returns after the short-lived access token has expired but their
 * longer-lived refresh token has not.
 */
async function resolveSession(): Promise<AuthSession> {
  const accessToken = authStorage.getToken();
  if (accessToken) {
    const claims = decodeIfValid(accessToken);
    if (claims) return { status: "authenticated", claims };
  }

  const refreshToken = authStorage.getRefreshToken();
  if (!refreshToken) {
    authStorage.clearSession();
    return { status: "unauthenticated" };
  }

  try {
    const response = await refreshRequest(refreshToken);
    authStorage.setToken(response.access_token);
    const claims = decodeIfValid(response.access_token);
    if (claims) return { status: "authenticated", claims };
    authStorage.clearSession();
    return { status: "unauthenticated" };
  } catch (error) {
    if (!(error instanceof ApiError)) {
      // Network failure, not a rejected refresh — do not discard a token
      // that might still be valid once connectivity returns.
      return { status: "unauthenticated" };
    }
    authStorage.clearSession();
    return { status: "unauthenticated" };
  }
}

/**
 * Reads the current session from stored tokens (see
 * src/lib/auth-storage.ts), silently renewing an expired access token via
 * the stored refresh token where possible, and decodes its claims (see
 * src/lib/jwt.ts). Single owner of "am I logged in, and as whom" for
 * client components.
 */
export function useAuth() {
  const [session, setSession] = useState<AuthSession>({ status: "loading" });

  useEffect(() => {
    let cancelled = false;

    resolveSession().then((result) => {
      if (!cancelled) setSession(result);
    });

    return () => {
      cancelled = true;
    };
  }, []);

  const logout = useCallback(() => {
    authStorage.clearSession();
    setSession({ status: "unauthenticated" });
  }, []);

  const refreshSession = useCallback(() => {
    setSession({ status: "loading" });
    resolveSession().then(setSession);
  }, []);

  return { session, logout, refreshSession };
}
