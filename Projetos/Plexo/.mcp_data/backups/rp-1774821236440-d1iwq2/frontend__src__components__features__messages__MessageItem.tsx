// Message item component for displaying agent messages
// FEATURE: Multi-Agent System

import React from 'react';
import type { AgentMessage } from '../../../types/agent';
import { cn } from '../../../utils/helpers';
import { formatDateTime } from '../../../utils/formatters';

interface MessageItemProps {
  message: AgentMessage;
  className?: string;
}

const messageTypeColors = {
  info: 'bg-blue-50 border-blue-200 dark:bg-blue-900/20 dark:border-blue-800',
  success: 'bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-800',
  warning: 'bg-yellow-50 border-yellow-200 dark:bg-yellow-900/20 dark:border-yellow-800',
  error: 'bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-800',
};

export const MessageItem: React.FC<MessageItemProps> = ({ message, className }) => {
  return (
    <div
      className={cn(
        'p-4 rounded-lg border',
        messageTypeColors[message.type as keyof typeof messageTypeColors] || messageTypeColors.info,
        className
      )}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-gray-900 dark:text-white">
              {message.sender}
            </span>
            <svg className="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {message.receiver}
            </span>
          </div>
          <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
            {message.content}
          </p>
        </div>
        <span className="text-xs text-gray-500 dark:text-gray-400 whitespace-nowrap">
          {formatDateTime(new Date(message.timestamp))}
        </span>
      </div>
    </div>
  );
};
