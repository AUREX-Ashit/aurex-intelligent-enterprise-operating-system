/**
 * Reusable access-token storage primitive.
 *
 * Infrastructure only: get/set/clear a token client-side. Does not call any
 * AuthService endpoint, does not decode or validate anything, and does not
 * decide when a token is obtained or discarded — that is login's
 * responsibility, deliberately not implemented here.
 */

const STORAGE_KEY = "corpstage.access_token";

export const authStorage = {
  getToken(): string | null {
    if (typeof window === "undefined") return null;
    return window.localStorage.getItem(STORAGE_KEY);
  },
  setToken(token: string): void {
    if (typeof window === "undefined") return;
    window.localStorage.setItem(STORAGE_KEY, token);
  },
  clearToken(): void {
    if (typeof window === "undefined") return;
    window.localStorage.removeItem(STORAGE_KEY);
  },
};
