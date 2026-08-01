import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

/**
 * Shared Page Layout — SD-001-034 Universal Header (title + context) for
 * every screen hosted inside a Workspace shell. Extracted so the identical
 * title+description markup every screen currently repeats individually has
 * one canonical implementation to converge on.
 */
export function PageHeader({
  title,
  description,
  actions,
  className,
}: {
  title: string;
  description?: string;
  actions?: ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("flex flex-wrap items-start justify-between gap-4", className)}>
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">{title}</h1>
        {description && <p className="mt-1 text-sm text-muted-foreground">{description}</p>}
      </div>
      {actions && <div className="flex shrink-0 items-center gap-2">{actions}</div>}
    </div>
  );
}
