"use client";

import { useEffect, useState } from "react";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { Spinner } from "@/components/ui/Spinner";
import { FormBanner } from "@/components/ui/Form";
import { fetchHealth } from "@/services/health-service";
import type { HealthCheckResponse } from "@/types/health";
import { ApiError } from "@/lib/api-client";

export default function HealthPage() {
  const [result, setResult] = useState<HealthCheckResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    fetchHealth()
      .then((response) => {
        if (!cancelled) setResult(response);
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        setError(err instanceof ApiError ? err.message : "Unable to reach AuthService.");
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Health</h1>
        <p className="mt-1 text-sm text-muted-foreground">Backend connectivity check.</p>
      </div>

      <Card className="max-w-md">
        <CardTitle>AuthService</CardTitle>
        <CardDescription>GET /health</CardDescription>

        <div className="mt-4">
          {isLoading && (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Spinner />
              Checking…
            </div>
          )}

          {!isLoading && error && <FormBanner tone="danger">{error}</FormBanner>}

          {!isLoading && result && (
            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-foreground">Status</span>
                <StatusBadge tone={result.status === "healthy" ? "success" : "warning"}>
                  {result.status}
                </StatusBadge>
              </div>
              <div>
                <span className="font-semibold text-foreground">Service</span>{" "}
                <span className="text-muted-foreground">{result.service}</span>
              </div>
              <div>
                <span className="font-semibold text-foreground">Dependencies</span>
                <ul className="mt-1 space-y-1">
                  {Object.entries(result.dependencies).map(([name, status]) => (
                    <li key={name} className="flex items-center gap-2 text-muted-foreground">
                      <span>{name}:</span>
                      <StatusBadge tone="muted">{status}</StatusBadge>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      </Card>
    </div>
  );
}
