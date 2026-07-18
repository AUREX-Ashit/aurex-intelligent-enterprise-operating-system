import type { HTMLAttributes, LabelHTMLAttributes, ReactNode } from "react";
import { cn } from "@/lib/utils";

export function FormField({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div {...props} className={cn("block space-y-1", className)} />;
}

export function FormLabel({ className, ...props }: LabelHTMLAttributes<HTMLLabelElement>) {
  return (
    <label {...props} className={cn("block text-sm font-semibold text-foreground", className)} />
  );
}

export function FormHelperText({ className, ...props }: HTMLAttributes<HTMLParagraphElement>) {
  return <p {...props} className={cn("text-xs text-muted-foreground", className)} />;
}

export function FormError({ children, className, ...props }: HTMLAttributes<HTMLParagraphElement>) {
  if (!children) return null;
  return (
    <p role="alert" {...props} className={cn("text-xs font-medium text-danger", className)}>
      {children}
    </p>
  );
}

export function FormBanner({
  tone = "danger",
  children,
}: {
  tone?: "danger" | "success" | "warning" | "info";
  children: ReactNode;
}) {
  const tones: Record<string, string> = {
    danger: "border-danger/20 bg-danger-bg text-danger",
    success: "border-success/20 bg-success-bg text-success",
    warning: "border-warning/20 bg-warning-bg text-warning",
    info: "border-info/20 bg-info-bg text-info",
  };

  return (
    <div
      role={tone === "danger" ? "alert" : "status"}
      className={cn("rounded-md border px-3 py-2 text-sm font-medium", tones[tone])}
    >
      {children}
    </div>
  );
}
