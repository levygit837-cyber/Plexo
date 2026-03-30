// Agent card component for displaying agent information
// FEATURE: Multi-Agent System

import React from 'react';
import type { Agent } from '../../../types/agent';
import { cn } from '../../../utils/helpers';

interface AgentCardProps {
  agent: Agent;
  onClick?: (agent: Agent) => void;
  className?: string;
}

const statusColors = {
  active: 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400',
  idle: 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400',
  busy: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400',
  error: 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400',
};

export const AgentCard: React.FC<AgentCardProps> = ({ agent, onClick, className }) => {
  return (
    <div
      onClick={() => onClick?.(agent)}
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
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            {agent.name}
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            {agent.type}
          </p>
        </div>
        <span
          className={cn(
            'px-2 py-1 rounded-full text-xs font-medium',
            statusColors[agent.status as keyof typeof statusColors] || statusColors.idle
          )}
        >
          {agent.status}
        </span>
      </div>
      
      {agent.capabilities && agent.capabilities.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-2">
          {agent.capabilities.slice(0, 3).map((capability, index) => (
            <span
              key={index}
              className="px-2 py-1 rounded bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400 text-xs"
            >
              {capability}
            </span>
          ))}
          {agent.capabilities.length > 3 && (
            <span className="px-2 py-1 text-xs text-gray-500 dark:text-gray-400">
              +{agent.capabilities.length - 3} more
            </span>
          )}
        </div>
      )}
    </div>
  );
};
