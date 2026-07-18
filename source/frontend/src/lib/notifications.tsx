"use client";

/**
 * Notification abstraction.
 *
 * A minimal React Context store — no external toast library, no global
 * state manager. Any component calls `useNotifications().notify(...)`;
 * rendering is handled once, centrally, by `<Toaster />`
 * (`src/components/ui/Toaster.tsx`) mounted in the root layout.
 */

import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from "react";

export type NotificationTone = "info" | "success" | "warning" | "danger";

export interface Notification {
  id: string;
  message: string;
  tone: NotificationTone;
}

interface NotificationContextValue {
  notifications: Notification[];
  notify: (message: string, tone?: NotificationTone) => void;
  dismiss: (id: string) => void;
}

const NotificationContext = createContext<NotificationContextValue | null>(null);

const DEFAULT_DURATION_MS = 5000;

export function NotificationProvider({ children }: { children: ReactNode }) {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const dismiss = useCallback((id: string) => {
    setNotifications((current) => current.filter((notification) => notification.id !== id));
  }, []);

  const notify = useCallback(
    (message: string, tone: NotificationTone = "info") => {
      const id = crypto.randomUUID();
      setNotifications((current) => [...current, { id, message, tone }]);
      setTimeout(() => dismiss(id), DEFAULT_DURATION_MS);
    },
    [dismiss],
  );

  const value = useMemo(() => ({ notifications, notify, dismiss }), [notifications, notify, dismiss]);

  return <NotificationContext.Provider value={value}>{children}</NotificationContext.Provider>;
}

export function useNotifications(): NotificationContextValue {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error("useNotifications must be used within a NotificationProvider.");
  }
  return context;
}
