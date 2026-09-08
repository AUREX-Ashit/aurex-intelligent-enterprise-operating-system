"use client";

import { useCallback, useRef, useState } from "react";
import { useOverlay } from "@/hooks/useOverlay";
import { ApiError } from "@/lib/api-client";
import { cn } from "@/lib/utils";
import { acknowledgeNotification, listMyNotifications } from "@/services/notification-api";
import type { NotificationResponse } from "@/types/notification";

/**
 * Reusable Platform Asset — Notification Area. A fixed, discoverable
 * location for platform notifications, per SD-003 §8 (Notifications,
 * Attention & Cognitive Load Laws).
 *
 * C-132 WP-19 BA-01 ("Establish / Manage Enterprise Notification Context")
 * connects this shell to the real AuthService `/notifications` API — list
 * and acknowledge only. Delivery channels, digest controls, interruption
 * ceilings, and channel/provider configuration are all out of scope
 * (`ROD-C132` RO Decision 3 / 3a; WP-19 charter §19) and are not rendered
 * here. The three-element composition (What Happened / Why It Matters /
 * What Happens Next) and the four-value severity taxonomy are DS-001
 * Chapter 21 (`DS-001-351` / `DS-001-350`).
 */

type PanelState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "loaded"; items: NotificationResponse[] }
  | { status: "error"; message: string };

const SEVERITY_LABEL: Record<string, string> = {
  success: "Success",
  info: "Info",
  warning: "Warning",
  danger: "Action needed",
};

export function NotificationCenter() {
  const [open, setOpen] = useState(false);
  const [state, setState] = useState<PanelState>({ status: "idle" });
  const [acknowledging, setAcknowledging] = useState<string | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);

  useOverlay({
    open,
    onClose: () => setOpen(false),
    containerRef,
    trapRef: panelRef,
    closeOnOutsideClick: true,
  });

  const load = useCallback(async () => {
    setState({ status: "loading" });
    try {
      const items = await listMyNotifications();
      setState({ status: "loaded", items });
    } catch (error) {
      const message =
        error instanceof ApiError
          ? error.message
          : "Unable to load notifications. Check your connection and try again.";
      setState({ status: "error", message });
    }
  }, []);

  const toggle = useCallback(() => {
    const next = !open;
    setOpen(next);
    if (next) {
      void load();
    }
  }, [open, load]);

  const onAcknowledge = useCallback(async (id: string) => {
    setAcknowledging(id);
    try {
      const updated = await acknowledgeNotification(id);
      setState((current) =>
        current.status === "loaded"
          ? {
              status: "loaded",
              items: current.items.map((item) => (item.id === id ? updated : item)),
            }
          : current,
      );
    } catch {
      // A failed acknowledge leaves the item unchanged; the next panel
      // open re-fetches authoritative state.
    } finally {
      setAcknowledging(null);
    }
  }, []);

  const unreadCount =
    state.status === "loaded" ? state.items.filter((item) => item.status === "UNREAD").length : 0;

  return (
    <div ref={containerRef} className="relative inline-block">
      <button
        type="button"
        aria-haspopup="true"
        aria-expanded={open}
        aria-label={
          unreadCount > 0 ? `Notifications, ${unreadCount} unread` : "Notifications"
        }
        onClick={toggle}
        className="inline-flex h-9 items-center rounded-md border border-border bg-surface px-3 text-sm text-muted-foreground transition hover:bg-surface-muted"
      >
        Notifications
        {unreadCount > 0 && (
          <span className="ml-2 rounded-full bg-surface-muted px-1.5 text-xs font-bold text-foreground">
            {unreadCount}
          </span>
        )}
      </button>

      {open && (
        <div
          ref={panelRef}
          role="region"
          aria-label="Notifications"
          tabIndex={-1}
          className={cn(
            "absolute right-0 z-40 mt-2 w-96 rounded-md border border-border bg-surface p-4 shadow-lg outline-none",
          )}
        >
          <h2 className="text-sm font-bold text-foreground">Notifications</h2>

          {state.status === "loading" && (
            <p className="mt-2 text-sm text-muted-foreground">Loading notifications&hellip;</p>
          )}

          {state.status === "error" && (
            <div className="mt-2">
              <p className="text-sm text-danger">{state.message}</p>
              <button
                type="button"
                onClick={() => void load()}
                className="mt-2 inline-flex h-8 items-center rounded-md border border-border bg-surface px-2.5 text-xs text-foreground transition hover:bg-surface-muted"
              >
                Try again
              </button>
            </div>
          )}

          {state.status === "loaded" && state.items.length === 0 && (
            <p className="mt-2 text-sm text-muted-foreground">
              You&rsquo;re all caught up. Nothing needs your attention right now.
            </p>
          )}

          {state.status === "loaded" && state.items.length > 0 && (
            <ul className="mt-2 max-h-96 space-y-3 overflow-y-auto">
              {state.items.map((item) => (
                <li
                  key={item.id}
                  className={cn(
                    "rounded-md border border-border p-3",
                    item.status === "UNREAD" ? "bg-surface" : "bg-surface-muted",
                  )}
                >
                  <p className="text-xs font-bold uppercase tracking-wide text-muted-foreground">
                    {SEVERITY_LABEL[item.severity] ?? item.severity}
                  </p>
                  <p className="mt-1 text-sm font-bold text-foreground">{item.what_happened}</p>
                  {item.why_it_matters && (
                    <p className="mt-1 text-sm text-muted-foreground">{item.why_it_matters}</p>
                  )}
                  {item.what_happens_next && (
                    <p className="mt-1 text-sm text-muted-foreground">{item.what_happens_next}</p>
                  )}
                  {item.status === "UNREAD" ? (
                    <button
                      type="button"
                      onClick={() => void onAcknowledge(item.id)}
                      disabled={acknowledging === item.id}
                      className="mt-2 inline-flex h-8 items-center rounded-md border border-border bg-surface px-2.5 text-xs text-foreground transition hover:bg-surface-muted disabled:opacity-60"
                    >
                      {acknowledging === item.id ? "Acknowledging…" : "Acknowledge"}
                    </button>
                  ) : (
                    <p className="mt-2 text-xs text-muted-foreground">Acknowledged</p>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
