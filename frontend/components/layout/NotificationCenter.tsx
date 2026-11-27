"use client";

import { useEffect, useState } from "react";
import { notificationRepository, NotificationResponse } from "@/repositories/notificationRepository";
import { Bell, Check } from "lucide-react";

export function NotificationCenter() {
  const [notifications, setNotifications] = useState<NotificationResponse[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [notifs, count] = await Promise.all([
        notificationRepository.getNotifications(),
        notificationRepository.getUnreadCount()
      ]);
      setNotifications(notifs);
      setUnreadCount(count);
    } catch (e) {
      console.error(e);
    }
  };

  const markAsRead = async (id: string) => {
    try {
      await notificationRepository.markAsRead(id);
      await fetchData();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="relative">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 text-muted-foreground hover:text-foreground rounded-full hover:bg-surface-hover transition-colors"
      >
        <span className="sr-only">View notifications</span>
        <Bell className="h-5 w-5" aria-hidden="true" />
        {unreadCount > 0 && (
          <span className="absolute top-1.5 right-1.5 block h-2 w-2 rounded-full bg-destructive ring-2 ring-background" />
        )}
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 bg-surface border border-border-strong rounded-xl shadow-lg z-50 overflow-hidden">
          <div className="p-4 border-b border-border/40 flex justify-between items-center bg-surface-hover/30">
            <h3 className="text-sm font-semibold text-foreground">Notifications</h3>
            <span className="text-xs font-medium text-muted-foreground">{unreadCount} unread</span>
          </div>
          <div className="max-h-96 overflow-y-auto">
            {notifications.length === 0 ? (
              <div className="p-8 text-sm text-muted-foreground text-center">No notifications</div>
            ) : (
              <ul className="divide-y divide-border/40">
                {notifications.map((notification) => (
                  <li key={notification.id} className="p-4 hover:bg-surface-hover/50 transition-colors">
                    <div className="flex justify-between items-start gap-2">
                      <div className="flex-1">
                        <p className="text-sm font-medium text-foreground leading-tight">{notification.subject}</p>
                        <p className="text-[11px] text-muted-foreground mt-1.5">{new Date(notification.created_at).toLocaleString()}</p>
                      </div>
                      {notification.status !== 'READ' && notification.status !== 'DELIVERED' && (
                        <button 
                          onClick={() => markAsRead(notification.id)}
                          className="ml-2 text-primary/70 hover:text-primary transition-colors mt-0.5"
                          title="Mark as read"
                        >
                          <Check className="h-4 w-4" />
                        </button>
                      )}
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
