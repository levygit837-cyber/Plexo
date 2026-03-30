// Agent context provider with global agent state management
// FEATURE: Multi-Agent System

import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import type { Agent, AgentMessage } from '../types/agent';
import { useAgents } from '../hooks/useAgents';
import { agentApi } from '../services/api/agents';

interface AgentContextType {
  agents: Agent[];
  selectedAgent: Agent | null;
  recentMessages: AgentMessage[];
  messages: AgentMessage[];
  loading: boolean;
  error: string | null;
  selectAgent: (agent: Agent | null) => void;
  addMessage: (message: AgentMessage) => void;
  sendMessage: (content: string) => Promise<void>;
  refetch: () => Promise<void>;
}

interface AgentProviderProps {
  children: React.ReactNode;
}

const AgentContext = createContext<AgentContextType | undefined>(undefined);
const MAX_RECENT_MESSAGES = 100;

export const AgentProvider: React.FC<AgentProviderProps> = ({ children }) => {
  const { agents, loading, error, refetch } = useAgents();
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [recentMessages, setRecentMessages] = useState<AgentMessage[]>([]);
  const [messages, setMessages] = useState<AgentMessage[]>([]);

  const selectAgent = useCallback((agent: Agent | null) => {
    setSelectedAgent(agent);
  }, []);

  const addMessage = useCallback((message: AgentMessage) => {
    setRecentMessages(prev => {
      const newMessages = [...prev, message];
      if (newMessages.length > MAX_RECENT_MESSAGES) {
        return newMessages.slice(-MAX_RECENT_MESSAGES);
      }
      return newMessages;
    });
    setMessages(prev => [...prev, message]);
  }, []);

  const sendMessage = useCallback(async (content: string) => {
    if (!selectedAgent || !content.trim()) return;
    
    try {
      const response = await agentApi.sendMessage(selectedAgent.id, content, 'user');
      if (response.data) {
        addMessage(response.data);
      }
    } catch (err) {
      console.error('Failed to send message:', err);
    }
  }, [selectedAgent, addMessage]);

  const wsUrl = typeof window !== 'undefined' 
    ? (window as any).REACT_APP_WS_URL || 'ws://localhost:8000/ws'
    : 'ws://localhost:8000/ws';

  useEffect(() => {
    const ws = new WebSocket(wsUrl);
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'message') {
          const message: AgentMessage = {
            id: data.payload.id || Date.now().toString(),
            senderId: data.payload.senderId || 'system',
            receiverId: data.payload.receiverId || 'user',
            content: data.payload.content,
            messageType: data.payload.messageType || 'notification',
            timestamp: data.payload.timestamp || new Date().toISOString(),
          };
          addMessage(message);
        }
      } catch (err) {
        console.error('Failed to parse WebSocket message:', err);
      }
    };

    return () => {
      ws.close();
    };
  }, [wsUrl, addMessage]);

  return (
    <AgentContext.Provider
      value={{
        agents,
        selectedAgent,
        recentMessages,
        messages,
        loading,
        error: error ? String(error) : null,
        selectAgent,
        addMessage,
        sendMessage,
        refetch,
      }}
    >
      {children}
    </AgentContext.Provider>
  );
};

export const useAgentContext = (): AgentContextType => {
  const context = useContext(AgentContext);
  if (context === undefined) {
    throw new Error('useAgentContext must be used within an AgentProvider');
  }
  return context;
};
