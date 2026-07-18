"use client";

import { useNotifications, type NotificationTone } from "@/lib/notifications";
import { cn } from "@/lib/utils";

const toneStyles: Record<NotificationTone, string> = {
  info: "border-info/20 bg-info-bg text-info",
  success: "border-success/20 bg-success-bg text-success",
  warning: "border-warning/20 bg-warning-bg text-warning",
  danger: "border-danger/20 bg-danger-bg text-danger",
};

/** Renders the notification stack. Mounted once, in `src/app/providers.tsx`. */
export function Toaster() {
  const { notifications, dismiss } = useNotifications();

  if (notifications.length === 0) return null;

  return (
    <div className="fixed bottom-4 right-4 z-50 flex w-full max-w-sm flex-col gap-2">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          role="status"
          className={cn(
            "flex items-start justify-between gap-3 rounded-md border px-3 py-2 text-sm font-medium shadow-sm",
            toneStyles[notification.tone],
          )}
        >
          <span>{notification.message}</span>
          <button
            type="button"
            onClick={() => dismiss(notification.id)}
            aria-label="Dismiss notification"
            className="shrink-0 opacity-60 transition hover:opacity-100"
          >
            ×
          </button>
        </div>
      ))}
    </div>
  );
}
