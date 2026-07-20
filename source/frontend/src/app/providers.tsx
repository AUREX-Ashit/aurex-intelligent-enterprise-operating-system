"use client";

import { useEffect, type ReactNode } from "react";
import { setAuthTokenProvider, setRefreshHandler } from "@/lib/api-client";
import { authStorage } from "@/lib/auth-storage";
import { refresh as refreshRequest } from "@/services/auth-api";
import { NotificationProvider } from "@/lib/notifications";
import { Toaster } from "@/components/ui/Toaster";

/**
 * Application-wide providers, mounted once in the root layout.
 *
 * Wires the API client's token provider to storage, and its 401
 * refresh-and-retry seam to AuthService's POST /auth/refresh — plumbing
 * only; the decision of when a session is obtained or discarded lives in
 * src/features/auth and src/hooks/useAuth, not here.
 */
export function Providers({ children }: { children: ReactNode }) {
  useEffect(() => {
    setAuthTokenProvider(() => authStorage.getToken());

    setRefreshHandler(async () => {
      const refreshToken = authStorage.getRefreshToken();
      if (!refreshToken) return false;

      try {
        const response = await refreshRequest(refreshToken);
        authStorage.setToken(response.access_token);
        return true;
      } catch {
        authStorage.clearSession();
        return false;
      }
    });
  }, []);

  return (
    <NotificationProvider>
      {children}
      <Toaster />
    </NotificationProvider>
  );
}
