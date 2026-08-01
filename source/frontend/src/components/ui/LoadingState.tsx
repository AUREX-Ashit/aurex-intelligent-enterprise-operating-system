import { Spinner } from "@/components/ui/Spinner";
import { cn } from "@/lib/utils";

/**
 * Shared Loading State — DS-001 "Loading Indicator" component. Used both
 * as a full-viewport loading screen (pre-shell, e.g. session resolution in
 * AdminShell) and as an in-shell section loading state (every Next.js
 * route-segment `loading.tsx` boundary), so every Workspace gets identical
 * loading treatment instead of re-implementing the same spinner+message
 * markup per call site.
 */
export function LoadingState({
  label = "Loading…",
  fullScreen = false,
  className,
}: {
  label?: string;
  fullScreen?: boolean;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "flex items-center justify-center text-muted-foreground",
        fullScreen ? "min-h-screen bg-background" : "flex-1 py-16",
        className,
      )}
    >
      <Spinner className="mr-2 h-5 w-5" />
      <span className="text-sm font-medium">{label}</span>
    </div>
  );
}
