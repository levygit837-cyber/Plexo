// ChatLayout - Main container based on Pencil Frame Base design (Plexo Chat Components)
// FEATURE: Multi-Agent System

import { ChatHeader } from './ChatHeader';
import { ChatSidebar } from './ChatSidebar';
import { ChatMessages } from './ChatMessages';
import { ChatSamples } from './ChatSamples';
import { ChatInputBar } from './ChatInputBar';
import { useAgentContext } from '../../../contexts/AgentContext';

export const ChatLayout = () => {
  const { messages, loading, error } = useAgentContext();

  return (
    <div className="flex flex-col h-screen bg-background">
      <ChatHeader />
      <div className="flex flex-1 overflow-hidden">
        <ChatSidebar />
        <div className="flex flex-col flex-1">
          <ChatMessages 
            messages={messages}
            loading={loading}
            error={error}
          />
          <ChatSamples />
        </div>
      </div>
      <ChatInputBar />
    </div>
  );
};
