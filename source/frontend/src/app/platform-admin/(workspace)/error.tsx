"use client";

import { ErrorState } from "@/components/layout/ErrorState";

/**
 * Error boundary scoped to the Platform Administrator Workspace (Next.js
 * App Router convention: error.tsx catches rendering errors in its route
 * segment and below). Shares src/app/error.tsx's own ErrorState component.
 */
export default function PlatformAdminError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <ErrorState
      error={error}
      reset={reset}
      scope="Platform Administrator Workspace"
      description="An unexpected error occurred while rendering this section of the Platform Administrator Workspace. You can try again, or return to the dashboard."
    />
  );
}
