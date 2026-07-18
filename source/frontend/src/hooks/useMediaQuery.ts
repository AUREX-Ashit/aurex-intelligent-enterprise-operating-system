import { useEffect, useState } from "react";

/**
 * Tracks whether a CSS media query currently matches. Starts `false` and
 * corrects itself post-mount, deliberately: `window.matchMedia` doesn't
 * exist during SSR, so reading it in a `useState` initializer would return
 * a different value on the server than on the client's first paint,
 * causing a hydration mismatch. The synchronous `setMatches` call below
 * (react-hooks/set-state-in-effect would otherwise flag this) is the
 * correct fix for exactly that reason, not an oversight.
 */
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const mediaQueryList = window.matchMedia(query);
    // eslint-disable-next-line react-hooks/set-state-in-effect -- see comment above
    setMatches(mediaQueryList.matches);

    function handleChange(event: MediaQueryListEvent) {
      setMatches(event.matches);
    }

    mediaQueryList.addEventListener("change", handleChange);
    return () => mediaQueryList.removeEventListener("change", handleChange);
  }, [query]);

  return matches;
}
