/**
 * Mirrors AuthService's JWT claim shape (TokenPayload) exactly.
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

/**
 * Mirrors AuthService's schemas/auth.py exactly. No field added, renamed,
 * or omitted relative to the backend contract (R-001 authentication flow).
 */
export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  refresh_token: string;
}

export interface OrganizationOption {
  organization_id: string;
  organization_name: string;
  role_code: string;
}

export interface OrganizationSelectionResponse {
  requires_organization_selection: true;
  organizations: OrganizationOption[];
}

export type LoginResponse = TokenResponse | OrganizationSelectionResponse;

export function isOrganizationSelectionResponse(
  response: LoginResponse,
): response is OrganizationSelectionResponse {
  return "requires_organization_selection" in response;
}

export interface RefreshTokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}
