"use client";

import { useEffect, type ReactNode } from "react";
import { setAuthTokenProvider } from "@/lib/api-client";
import { authStorage } from "@/lib/auth-storage";
import { NotificationProvider } from "@/lib/notifications";
import { Toaster } from "@/components/ui/Toaster";

/**
 * Application-wide providers, mounted once in the root layout.
 *
 * Wires the API client's token provider to storage — plumbing only; it
 * reads whatever token (if any) already exists, it does not obtain one.
 * Login remains unimplemented.
 */
export function Providers({ children }: { children: ReactNode }) {
  useEffect(() => {
    setAuthTokenProvider(() => authStorage.getToken());
  }, []);

  return (
    <NotificationProvider>
      {children}
      <Toaster />
    </NotificationProvider>
  );
}
