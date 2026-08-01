"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { logger } from "@/lib/logger";

/**
 * Shared Error State — every Next.js `error.tsx` boundary (root and each
 * Workspace) renders this identically, differing only in which segment it
 * guards and what to say about it, so the recovery UI stays consistent
 * platform-wide instead of each boundary re-implementing the same
 * Card/logger pairing.
 */
export function ErrorState({
  error,
  reset,
  scope,
  description,
}: {
  error: Error & { digest?: string };
  reset: () => void;
  scope: string;
  description: string;
}) {
  useEffect(() => {
    logger.error(`Unhandled ${scope} error`, { message: error.message, digest: error.digest });
  }, [error, scope]);

  return (
    <div className="flex flex-1 items-center justify-center py-16">
      <Card className="max-w-md text-center">
        <CardTitle>Something went wrong</CardTitle>
        <CardDescription>{description}</CardDescription>
        <Button className="mt-6" onClick={reset}>
          Try again
        </Button>
      </Card>
    </div>
  );
}
