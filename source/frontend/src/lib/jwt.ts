/**
 * Decodes a JWT's payload for client-side display/routing purposes only
 * (e.g. reading `role_code` to gate navigation). This never verifies the
 * signature — verification is AuthService's responsibility on every
 * request; a client-side decode is not a trust boundary.
 */
export function decodeJwtPayload<T>(token: string): T | null {
  const segments = token.split(".");
  if (segments.length !== 3) return null;

  try {
    const base64 = segments[1].replace(/-/g, "+").replace(/_/g, "/");
    const padded = base64.padEnd(base64.length + ((4 - (base64.length % 4)) % 4), "=");
    const json = decodeURIComponent(
      atob(padded)
        .split("")
        .map((char) => "%" + char.charCodeAt(0).toString(16).padStart(2, "0"))
        .join(""),
    );
    return JSON.parse(json) as T;
  } catch {
    return null;
  }
}
