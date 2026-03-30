// Message item component for displaying agent messages
// FEATURE: Multi-Agent System

import type { AgentMessage } from '../../../types/agent';
import { cn } from '../../../utils/helpers';

interface MessageItemProps {
  message: AgentMessage;
  className?: string;
}

const messageTypeColors: Record<string, string> = {
  text: 'bg-blue-500/10 text-blue-500',
  task: 'bg-green-500/10 text-green-500',
  alert: 'bg-red-500/10 text-red-500',
  system: 'bg-gray-500/10 text-gray-500',
};

export const MessageItem: React.FC<MessageItemProps> = ({ message, className }) => {
  return (
    <div className={cn(
      'flex flex-col gap-2 p-4 rounded-lg border',
      className
    )}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className={cn(
            'px-2 py-1 rounded-full text-xs font-medium',
            messageTypeColors[message.messageType] || messageTypeColors.text
          )}>
            {message.messageType}
          </span>
          <span className="text-sm text-muted-foreground">
            From: {message.senderId}
          </span>
          <span className="text-sm text-muted-foreground">
            To: {message.receiverId}
          </span>
        </div>
        <span className="text-xs text-muted-foreground">
          {new Date(message.timestamp).toLocaleString()}
        </span>
      </div>
      <p className="text-sm">{message.content}</p>
    </div>
  );
};
