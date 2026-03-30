// Notification context provider with toast notifications
// FEATURE: UI Notifications

import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';

type NotificationType = 'success' | 'error' | 'warning' | 'info';

interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  message?: string;
  duration?: number;
  action?: {
    label: string;
    onClick: () => void;
  };
}

interface NotificationContextType {
  notifications: Notification[];
  showNotification: (notification: Omit<Notification, 'id'>) => string;
  hideNotification: (id: string) => void;
  clearAll: () => void;
  success: (title: string, message?: string, duration?: number) => string;
  error: (title: string, message?: string, duration?: number) => string;
  warning: (title: string, message?: string, duration?: number) => string;
  info: (title: string, message?: string, duration?: number) => string;
}

interface NotificationProviderProps {
  children: ReactNode;
  maxNotifications?: number;
  defaultDuration?: number;
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined);

const DEFAULT_DURATION = 5000;
const MAX_NOTIFICATIONS = 5;

let notificationId = 0;

const generateId = (): string => {
  notificationId += 1;
  return `notification-${notificationId}-${Date.now()}`;
};

export const NotificationProvider: React.FC<NotificationProviderProps> = ({
  children,
  maxNotifications = MAX_NOTIFICATIONS,
  defaultDuration = DEFAULT_DURATION,
}) => {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const hideNotification = useCallback((id: string) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  }, []);

  const showNotification = useCallback(
    (notification: Omit<Notification, 'id'>): string => {
      const id = generateId();
      const duration = notification.duration ?? defaultDuration;

      const newNotification: Notification = {
        ...notification,
        id,
        duration,
      };

      setNotifications((prev) => {
        const updated = [newNotification, ...prev];
        return updated.slice(0, maxNotifications);
      });

      if (duration > 0) {
        setTimeout(() => {
          hideNotification(id);
        }, duration);
      }

      return id;
    },
    [defaultDuration, maxNotifications, hideNotification]
  );

  const clearAll = useCallback(() => {
    setNotifications([]);
  }, []);

  const success = useCallback(
    (title: string, message?: string, duration?: number): string => {
      return showNotification({ type: 'success', title, message, duration });
    },
    [showNotification]
  );

  const error = useCallback(
    (title: string, message?: string, duration?: number): string => {
      return showNotification({ type: 'error', title, message, duration });
    },
    [showNotification]
  );

  const warning = useCallback(
    (title: string, message?: string, duration?: number): string => {
      return showNotification({ type: 'warning', title, message, duration });
    },
    [showNotification]
  );

  const info = useCallback(
    (title: string, message?: string, duration?: number): string => {
      return showNotification({ type: 'info', title, message, duration });
    },
    [showNotification]
  );

  const value: NotificationContextType = {
    notifications,
    showNotification,
    hideNotification,
    clearAll,
    success,
    error,
    warning,
    info,
  };

  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  );
};

export const useNotification = (): NotificationContextType => {
  const context = useContext(NotificationContext);
  if (context === undefined) {
    throw new Error('useNotification must be used within a NotificationProvider');
  }
  return context;
};
