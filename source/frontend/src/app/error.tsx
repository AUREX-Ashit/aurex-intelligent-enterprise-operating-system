"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { logger } from "@/lib/logger";

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
  useEffect(() => {
    logger.error("Unhandled UI error", { message: error.message, digest: error.digest });
  }, [error]);

  return (
    <div className="flex flex-1 items-center justify-center py-16">
      <Card className="max-w-md text-center">
        <CardTitle>Something went wrong</CardTitle>
        <CardDescription>
          An unexpected error occurred while rendering this page. You can try again, or return
          later.
        </CardDescription>
        <Button className="mt-6" onClick={reset}>
          Try again
        </Button>
      </Card>
    </div>
  );
}
