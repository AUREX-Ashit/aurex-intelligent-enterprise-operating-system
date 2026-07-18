/**
 * Mirrors AuthService's JWT claim shape (TokenPayload) exactly. Login is
 * not implemented here — this type exists so future auth code has a single,
 * correct shape to decode into, rather than each call site guessing it.
 */
export interface AuthClaims {
  person_id: string;
  identity_id: string;
  organization_id: string;
  membership_id: string;
  role_code: string;
  exp?: number;
  type?: "access" | "refresh";
}
