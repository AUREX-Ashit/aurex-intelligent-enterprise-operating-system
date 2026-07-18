/**
 * `cn` — conditional className joiner.
 *
 * Deliberately a small, dependency-free implementation (accepts strings,
 * falsy values, and one level of arrays) rather than adding clsx/tailwind-
 * merge as new dependencies for something this codebase's component set
 * doesn't yet need more than.
 */
export function cn(...classes: Array<string | false | null | undefined>): string {
  return classes.filter(Boolean).join(" ");
}
