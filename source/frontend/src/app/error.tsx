"use client";

import { ErrorState } from "@/components/layout/ErrorState";

/**
 * Root error boundary (Next.js App Router convention: `error.tsx` at any
 * route segment catches rendering errors in that segment and below).
 */
export default function GlobalError({
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
      scope="UI"
      description="An unexpected error occurred while rendering this page. You can try again, or return later."
    />
  );
}
