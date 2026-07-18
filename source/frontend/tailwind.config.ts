import type { Config } from "tailwindcss";

// Tailwind v4 is CSS-first (see src/styles/theme.css's @theme block for the
// canonical token values); this file exists to declare content sources
// explicitly and to hold non-token configuration (e.g. plugins) as the
// application grows, rather than relying solely on v4's auto-detection.
// Referenced explicitly via `@config` in src/app/globals.css.
const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
};

export default config;
