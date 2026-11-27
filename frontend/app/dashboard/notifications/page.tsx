"use client";

import { useEffect, useState } from "react";
import { notificationRepository, NotificationResponse } from "@/repositories/notificationRepository";
import { Bell, Check, Clock, AlertCircle } from "lucide-react";
import toast from "react-hot-toast";

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState<NotificationResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await notificationRepository.getNotifications();
      setNotifications(data);
    } catch (err: any) {
      setError(err.message || "Failed to load notifications");
      toast.error(err.message || "Failed to load notifications");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  const handleMarkAsRead = async (id: string) => {
    try {
      await notificationRepository.markAsRead(id);
      setNotifications((prev) =>
        prev.map((n) => (n.id === id ? { ...n, status: "read" } : n))
      );
      toast.success("Marked as read");
    } catch (err: any) {
      toast.error(err.message || "Failed to mark as read");
    }
  };

  if (loading) {
    return (
      <div className="p-6 md:p-8 max-w-5xl mx-auto space-y-6 animate-pulse">
        <div className="h-8 w-48 bg-border rounded"></div>
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-24 bg-surface rounded-xl border border-border"></div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 md:p-8 max-w-5xl mx-auto space-y-6">
        <div className="flex items-center gap-2 text-destructive">
          <AlertCircle className="w-6 h-6" />
          <h1 className="text-2xl font-bold tracking-tight">Failed to Load Notifications</h1>
        </div>
        <p className="text-muted-foreground">{error}</p>
        <button
          onClick={fetchNotifications}
          className="px-4 py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 md:p-8 max-w-5xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground flex items-center gap-2">
            <Bell className="w-6 h-6 text-primary" />
            Notifications
          </h1>
          <p className="text-muted-foreground mt-1">Stay updated with your latest alerts and tasks</p>
        </div>
      </div>

      {notifications.length === 0 ? (
        <div className="bg-surface border border-border rounded-xl p-12 text-center">
          <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
            <Bell className="w-6 h-6 text-primary" />
          </div>
          <h3 className="text-lg font-semibold text-foreground mb-1">No notifications</h3>
          <p className="text-muted-foreground">You're all caught up!</p>
        </div>
      ) : (
        <div className="space-y-4">
          {notifications.map((notification) => {
            const timeAgo = (dateStr: string) => {
              const seconds = Math.floor((new Date().getTime() - new Date(dateStr).getTime()) / 1000);
              if (seconds < 60) return "just now";
              const minutes = Math.floor(seconds / 60);
              if (minutes < 60) return `${minutes}m ago`;
              const hours = Math.floor(minutes / 60);
              if (hours < 24) return `${hours}h ago`;
              return `${Math.floor(hours / 24)}d ago`;
            };

            return (
              <div
                key={notification.id}
                className={`bg-surface border rounded-xl p-5 transition-all ${
                  notification.status === "unread"
                    ? "border-primary/30 shadow-sm"
                    : "border-border opacity-70"
                }`}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span
                        className={`text-xs font-semibold px-2 py-0.5 rounded-full uppercase tracking-wider ${
                          notification.notification_type === "alert"
                            ? "bg-destructive/10 text-destructive"
                            : "bg-primary/10 text-primary"
                        }`}
                      >
                        {notification.notification_type}
                      </span>
                      <span className="text-xs text-muted-foreground flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {timeAgo(notification.created_at)}
                      </span>
                    </div>
                    <h4 className="text-base font-medium text-foreground">{notification.subject}</h4>
                    <p className="text-sm text-muted-foreground">
                      Sent via {notification.channel}
                    </p>
                  </div>
                  {notification.status === "unread" && (
                    <button
                      onClick={() => handleMarkAsRead(notification.id)}
                      className="flex items-center gap-1.5 px-3 py-1.5 bg-surface-hover hover:bg-border text-sm font-medium rounded-lg transition-colors text-foreground whitespace-nowrap"
                    >
                      <Check className="w-4 h-4" />
                      Mark as read
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
