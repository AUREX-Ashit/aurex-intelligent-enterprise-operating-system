/**
 * Enterprise Notifications API wrapper (C-132, WP-19 BA-01) — the only
 * module permitted to call the AuthService `/notifications` endpoints.
 * Built on the shared `apiClient` (which attaches Authorization and
 * X-Tenant-ID), not raw fetch. Mirrors AuthService's routers/notification.py
 * exactly.
 *
 * WP-19 BA-01 charters establish / list / read / acknowledge only — no
 * delivery, no channel configuration, no digest controls (`ROD-C132` RO
 * Decision 3; charter §19). None of those is called here.
 */

import { apiClient } from "@/lib/api-client";
import type {
  EstablishNotificationRequest,
  NotificationResponse,
} from "@/types/notification";

export function establishNotification(
  request: EstablishNotificationRequest,
): Promise<NotificationResponse> {
  return apiClient.post<NotificationResponse>("/notifications", request);
}

export function listMyNotifications(): Promise<NotificationResponse[]> {
  return apiClient.get<NotificationResponse[]>("/notifications");
}

export function readNotification(notificationId: string): Promise<NotificationResponse> {
  return apiClient.get<NotificationResponse>(`/notifications/${notificationId}`);
}

export function acknowledgeNotification(notificationId: string): Promise<NotificationResponse> {
  return apiClient.post<NotificationResponse>(`/notifications/${notificationId}/acknowledge`, {});
}
