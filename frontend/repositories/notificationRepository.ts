import { notificationApi } from "@/lib/axios";
import axios from "axios";

export interface NotificationResponse {
  id: string;
  recipient_id: string;
  channel: string;
  notification_type: string;
  subject: string;
  status: string;
  created_at: string;
  sent_at: string | null;
}

const handleApiError = (err: unknown, defaultMessage: string): never => {
  if (axios.isAxiosError(err) && err.response?.data) {
    const detail = err.response.data.detail;
    if (typeof detail === 'string') {
      throw new Error(detail);
    }
  }
  throw new Error(err instanceof Error ? err.message : defaultMessage);
};

export const notificationRepository = {
  // Wait, there's no backend for fetching notifications yet.
  // The user says "If APIs are missing but the service/domain already supports notifications, implement the missing APIs."
  async getNotifications(): Promise<NotificationResponse[]> {
    try {
      const response = await notificationApi.get<NotificationResponse[]>("/notifications");
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to fetch notifications.");
    }
  },
  
  async getUnreadCount(): Promise<number> {
    try {
      const response = await notificationApi.get<number>("/notifications/unread-count");
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to fetch unread notification count.");
    }
  },
  
  async markAsRead(id: string): Promise<void> {
    try {
      await notificationApi.put(`/notifications/${id}/read`);
    } catch (err: unknown) {
      return handleApiError(err, "Failed to mark notification as read.");
    }
  }
};
