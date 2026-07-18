"use client";

import { useCallback, useEffect, useState } from "react";
import { authStorage } from "@/lib/auth-storage";
import { decodeJwtPayload } from "@/lib/jwt";
import type { AuthClaims } from "@/types/auth";

export type AuthSession =
  | { status: "loading" }
  | { status: "unauthenticated" }
  | { status: "authenticated"; claims: AuthClaims };

function readSession(): AuthSession {
  const token = authStorage.getToken();
  if (!token) return { status: "unauthenticated" };

  const claims = decodeJwtPayload<AuthClaims>(token);
  if (!claims) return { status: "unauthenticated" };

  if (claims.exp && claims.exp * 1000 <= Date.now()) {
    return { status: "unauthenticated" };
  }

  return { status: "authenticated", claims };
}

/**
 * Reads the current session from the stored access token (see
 * src/lib/auth-storage.ts) and decodes its claims (see src/lib/jwt.ts).
 * Single owner of "am I logged in, and as whom" for client components.
 */
export function useAuth() {
  const [session, setSession] = useState<AuthSession>({ status: "loading" });

  useEffect(() => {
    // localStorage is unavailable during SSR; this hydrates the real
    // session immediately post-mount, matching useMediaQuery's pattern.
    // eslint-disable-next-line react-hooks/set-state-in-effect -- see comment above
    setSession(readSession());
  }, []);

  const logout = useCallback(() => {
    authStorage.clearToken();
    setSession({ status: "unauthenticated" });
  }, []);

  const refreshSession = useCallback(() => {
    setSession(readSession());
  }, []);

  return { session, logout, refreshSession };
}
