// Agent context provider with global agent state management
// FEATURE: Multi-Agent System

import React, { createContext, useContext, useState, useCallback, ReactNode, useEffect } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';
import type { Agent, AgentStats, AgentMessage } from '../types/agent';

interface AgentContextType {
  agents: Agent[];
  selectedAgent: Agent | null;
  agentStats: Record<string, AgentStats>;
  recentMessages: AgentMessage[];
  setAgents: (agents: Agent[]) => void;
  addAgent: (agent: Agent) => void;
  updateAgent: (id: string, updates: Partial<Agent>) => void;
  removeAgent: (id: string) => void;
  selectAgent: (agent: Agent | null) => void;
  updateAgentStats: (agentId: string, stats: AgentStats) => void;
  addMessage: (message: AgentMessage) => void;
  clearMessages: () => void;
}

interface AgentProviderProps {
  children: ReactNode;
}

const AgentContext = createContext<AgentContextType | undefined>(undefined);

const MAX_RECENT_MESSAGES = 100;

export const AgentProvider: React.FC<AgentProviderProps> = ({ children }) => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [agentStats, setAgentStats] = useState<Record<string, AgentStats>>({});
  const [recentMessages, setRecentMessages] = useState<AgentMessage[]>([]);

  const { isConnected } = useWebSocket();

  useEffect(() => {
    if (isConnected) {
      console.log('WebSocket connected, agent context ready for real-time updates');
    }
  }, [isConnected]);

  const addAgent = useCallback((agent: Agent) => {
    setAgents((prev) => {
      const exists = prev.some((a) => a.id === agent.id);
      if (exists) {
        return prev.map((a) => (a.id === agent.id ? agent : a));
      }
      return [...prev, agent];
    });
  }, []);

  const updateAgent = useCallback((id: string, updates: Partial<Agent>) => {
    setAgents((prev) =>
      prev.map((agent) =>
        agent.id === id ? { ...agent, ...updates } : agent
      )
    );

    setSelectedAgent((prev) => {
      if (prev?.id === id) {
        return { ...prev, ...updates };
      }
      return prev;
    });
  }, []);

  const removeAgent = useCallback((id: string) => {
    setAgents((prev) => prev.filter((agent) => agent.id !== id));
    setAgentStats((prev) => {
      const { [id]: _, ...rest } = prev;
      return rest;
    });
    setSelectedAgent((prev) => (prev?.id === id ? null : prev));
  }, []);

  const selectAgent = useCallback((agent: Agent | null) => {
    setSelectedAgent(agent);
  }, []);

  const updateAgentStats = useCallback((agentId: string, stats: AgentStats) => {
    setAgentStats((prev) => ({
      ...prev,
      [agentId]: stats,
    }));
  }, []);

  const addMessage = useCallback((message: AgentMessage) => {
    setRecentMessages((prev) => {
      const updated = [message, ...prev];
      return updated.slice(0, MAX_RECENT_MESSAGES);
    });
  }, []);

  const clearMessages = useCallback(() => {
    setRecentMessages([]);
  }, []);

  const value: AgentContextType = {
    agents,
    selectedAgent,
    agentStats,
    recentMessages,
    setAgents,
    addAgent,
    updateAgent,
    removeAgent,
    selectAgent,
    updateAgentStats,
    addMessage,
    clearMessages,
  };

  return <AgentContext.Provider value={value}>{children}</AgentContext.Provider>;
};

export const useAgentContext = (): AgentContextType => {
  const context = useContext(AgentContext);
  if (context === undefined) {
    throw new Error('useAgentContext must be used within an AgentProvider');
  }
  return context;
};
