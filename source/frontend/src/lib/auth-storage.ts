/**
 * Reusable access/refresh-token storage primitive.
 *
 * Infrastructure only: get/set/clear tokens client-side. Does not call any
 * AuthService endpoint and does not decode or validate anything — that is
 * login's (src/features/auth) and the session hook's (src/hooks/useAuth)
 * responsibility.
 */

const ACCESS_TOKEN_KEY = "corpstage.access_token";
const REFRESH_TOKEN_KEY = "corpstage.refresh_token";

export const authStorage = {
  getToken(): string | null {
    if (typeof window === "undefined") return null;
    return window.localStorage.getItem(ACCESS_TOKEN_KEY);
  },
  setToken(token: string): void {
    if (typeof window === "undefined") return;
    window.localStorage.setItem(ACCESS_TOKEN_KEY, token);
  },
  clearToken(): void {
    if (typeof window === "undefined") return;
    window.localStorage.removeItem(ACCESS_TOKEN_KEY);
  },

  getRefreshToken(): string | null {
    if (typeof window === "undefined") return null;
    return window.localStorage.getItem(REFRESH_TOKEN_KEY);
  },
  setRefreshToken(token: string): void {
    if (typeof window === "undefined") return;
    window.localStorage.setItem(REFRESH_TOKEN_KEY, token);
  },
  clearRefreshToken(): void {
    if (typeof window === "undefined") return;
    window.localStorage.removeItem(REFRESH_TOKEN_KEY);
  },

  clearSession(): void {
    authStorage.clearToken();
    authStorage.clearRefreshToken();
  },
};
