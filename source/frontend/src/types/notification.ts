/**
 * Mirrors AuthService's schemas/notification.py exactly (C-132, WP-19
 * BA-01 — "Establish / Manage Enterprise Notification Context"). No field
 * added, renamed, or omitted relative to the backend contract.
 *
 * DS-001 Chapter 21 (`DS-001-350`/`DS-001-351`) governs the severity
 * taxonomy and the three-element composition — realized here as data only.
 */

/** DS-001's four closed severity values (`DS-001-350`). */
export type NotificationSeverity = "success" | "info" | "warning" | "danger";

/** The minimum lifecycle (`TDS-C132 §10`). One-directional. */
export type NotificationStatus = "UNREAD" | "ACKNOWLEDGED";

export interface EstablishNotificationRequest {
  membership_id: string;
  severity: NotificationSeverity;
  what_happened: string;
  why_it_matters?: string | null;
  what_happens_next?: string | null;
  source_type: string;
  source_id?: string | null;
}

export interface NotificationResponse {
  id: string;
  membership_id: string;
  severity: string;
  what_happened: string;
  why_it_matters: string | null;
  what_happens_next: string | null;
  source_type: string;
  source_id: string | null;
  status: string;
  created_at: string;
  acknowledged_at: string | null;
}
