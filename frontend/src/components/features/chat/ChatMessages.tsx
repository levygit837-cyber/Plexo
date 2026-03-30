// ChatMessages - Messages zone based on Pencil Frame Base design
// FEATURE: Multi-Agent System

import type { AgentMessage } from '../../../types/agent';
import { cn } from '../../../utils/helpers';

interface ChatMessagesProps {
  messages: AgentMessage[];
  loading?: boolean;
  error?: string | null;
  className?: string;
}

export const ChatMessages = ({
  messages,
  loading,
  error,
  className
}: ChatMessagesProps) => {
  if (loading) {
    return (
      <div className={cn(
        'flex items-center justify-center h-full',
        className
      )}>
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
      </div>
    );
  }

  if (error) {
    return (
      <div className={cn(
        'flex items-center justify-center h-full text-destructive',
        className
      )}>
        <p>{error}</p>
      </div>
    );
  }

  if (!messages || messages.length === 0) {
    return (
      <div className={cn(
        'flex items-center justify-center h-full text-muted-foreground',
        className
      )}>
        <p>No messages yet. Start a conversation!</p>
      </div>
    );
  }

  return (
    <div className={cn(
      'flex flex-col gap-4 overflow-y-auto',
      className
    )}>
      {messages.map((message: AgentMessage) => (
        <div
          key={message.id}
          className={cn(
            'flex flex-col gap-2 p-4 rounded-lg',
            message.senderId === 'user' ? 'bg-primary/10 ml-auto' : 'bg-muted'
          )}
        >
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium">
              {message.senderId}
            </span>
            <span className="text-xs text-muted-foreground">
              {new Date(message.timestamp).toLocaleString()}
            </span>
          </div>
          <p className="text-sm">{message.content}</p>
        </div>
      ))}
    </div>
  );
};
