"use client";

import { useEffect } from "react";
import { resolveConfiguration } from "@/services/configuration-api";

/**
 * WP-10 BA-01 — Resolve Enterprise Configuration (EX-C041-01), Theme
 * facet only. Applies the caller's own resolved theme_class
 * (PLATFORM_DEFAULT "LIGHT" or a TENANT/USER override — DS-001 §11.3's
 * own four in-scope classes: Light, Dark, High-Contrast, Boardroom;
 * White-label excluded per IRA-010 §4.3) to `<html data-theme>`, the
 * same attribute styles/theme.css's own `:root[data-theme=...]`
 * selectors key off.
 *
 * Progressive enhancement, not a loading gate: every screen already
 * renders correctly under the Light default before this resolves, and
 * a failed/slow resolve leaves that default in place rather than
 * blocking or erroring the shell — Configuration Management augments
 * existing certified screens, it does not gate them (IRA-010 §7).
 */
export function useResolvedTheme(enabled: boolean): void {
  useEffect(() => {
    if (!enabled) return;
    let cancelled = false;

    resolveConfiguration(["THEME"])
      .then((bundle) => {
        if (cancelled) return;
        const themeClass = bundle.facets.THEME?.find((v) => v.key === "theme_class")?.value;
        if (typeof themeClass === "string") {
          document.documentElement.setAttribute("data-theme", themeClass.toLowerCase().replace(/_/g, "-"));
        }
      })
      .catch(() => {
        // Silently keep the Light default — this hook augments an
        // already-correct baseline, it never blocks or errors the shell.
      });

    return () => {
      cancelled = true;
    };
  }, [enabled]);
}
