"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { logger } from "@/lib/logger";

/**
 * Error boundary scoped to the Platform Administrator Workspace (Next.js
 * App Router convention: error.tsx catches rendering errors in its route
 * segment and below). Mirrors src/app/error.tsx's treatment.
 */
export default function PlatformAdminError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    logger.error("Unhandled Platform Administrator Workspace error", {
      message: error.message,
      digest: error.digest,
    });
  }, [error]);

  return (
    <div className="flex flex-1 items-center justify-center py-16">
      <Card className="max-w-md text-center">
        <CardTitle>Something went wrong</CardTitle>
        <CardDescription>
          An unexpected error occurred while rendering this section of the Platform Administrator
          Workspace. You can try again, or return to the dashboard.
        </CardDescription>
        <Button className="mt-6" onClick={reset}>
          Try again
        </Button>
      </Card>
    </div>
  );
}
