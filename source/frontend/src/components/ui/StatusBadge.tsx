import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

export interface StatusBadgeProps {
  children: ReactNode;
  tone?: "brand" | "success" | "warning" | "danger" | "info" | "muted";
}

const tones: Record<NonNullable<StatusBadgeProps["tone"]>, string> = {
  brand: "border-brand/20 bg-brand/10 text-brand-strong",
  success: "border-success/20 bg-success-bg text-success",
  warning: "border-warning/20 bg-warning-bg text-warning",
  danger: "border-danger/20 bg-danger-bg text-danger",
  info: "border-info/20 bg-info-bg text-info",
  muted: "border-border-muted bg-surface-muted text-muted-foreground",
};

export function StatusBadge({ children, tone = "muted" }: StatusBadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-semibold",
        tones[tone],
      )}
    >
      {children}
    </span>
  );
}
