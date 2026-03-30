// Task card component for displaying task information
// FEATURE: Task Management

import React from 'react';
import type { Task } from '../../../types/task';
import { cn } from '../../../utils/helpers';
import { formatDate } from '../../../utils/formatters';

interface TaskCardProps {
  task: Task;
  onClick?: (task: Task) => void;
  className?: string;
}

const statusColors = {
  pending: 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400',
  running: 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400',
  completed: 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400',
  failed: 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400',
  cancelled: 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400',
};

const priorityColors = {
  low: 'text-gray-600 dark:text-gray-400',
  medium: 'text-yellow-600 dark:text-yellow-400',
  high: 'text-orange-600 dark:text-orange-400',
  urgent: 'text-red-600 dark:text-red-400',
};

export const TaskCard: React.FC<TaskCardProps> = ({ task, onClick, className }) => {
  return (
    <div
      onClick={() => onClick?.(task)}
      className={cn(
        'p-4 rounded-lg border border-gray-200 dark:border-gray-700',
        'bg-white dark:bg-gray-800 shadow-sm',
        'hover:shadow-md transition-shadow',
        onClick && 'cursor-pointer',
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              {task.name}
            </h3>
            <span
              className={cn(
                'text-xs font-medium',
                priorityColors[task.priority as keyof typeof priorityColors] || priorityColors.medium
              )}
            >
              {task.priority}
            </span>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            {task.type}
          </p>
        </div>
        <span
          className={cn(
            'px-2 py-1 rounded-full text-xs font-medium',
            statusColors[task.status as keyof typeof statusColors] || statusColors.pending
          )}
        >
          {task.status}
        </span>
      </div>

      <div className="mt-3 flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
        <span>Created: {formatDate(new Date(task.createdAt))}</span>
        {task.agentId && (
          <span className="px-2 py-1 rounded bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400">
            Agent: {task.agentId.slice(0, 8)}
          </span>
        )}
      </div>
    </div>
  );
};
