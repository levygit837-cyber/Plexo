// Agents hook with CRUD operations and real-time updates
// FEATURE: Multi-Agent System

import { useState, useEffect, useCallback } from 'react';
import { agentApi } from '../services/api/agents';
import { useWebSocketEvent } from './useWebSocket';
import type {
  Agent,
  AgentCreate,
  AgentUpdate,
  AgentListFilters,
  AgentStats,
  AgentMessage,
} from '../types/agent';
import type { PaginationParams } from '../types/common';
import type { ApiError } from '../types/api';

interface UseAgentsState {
  agents: Agent[];
  loading: boolean;
  error: ApiError | null;
}

export const useAgents = (filters?: AgentListFilters, pagination?: PaginationParams) => {
  const [state, setState] = useState<UseAgentsState>({
    agents: [],
    loading: true,
    error: null,
  });

  const fetchAgents = useCallback(async () => {
    setState((prev) => ({ ...prev, loading: true, error: null }));

    try {
      const response = await agentApi.list(filters, pagination);
      setState({
        agents: response.data,
        loading: false,
        error: null,
      });
    } catch (err) {
      setState({
        agents: [],
        loading: false,
        error: err as ApiError,
      });
    }
  }, [filters, pagination]);

  useEffect(() => {
    fetchAgents();
  }, [fetchAgents]);

  useWebSocketEvent<Agent>('agent.created', (agent) => {
    setState((prev) => ({
      ...prev,
      agents: [...prev.agents, agent],
    }));
  });

  useWebSocketEvent<Agent>('agent.updated', (updatedAgent) => {
    setState((prev) => ({
      ...prev,
      agents: prev.agents.map((agent) =>
        agent.id === updatedAgent.id ? updatedAgent : agent
      ),
    }));
  });

  useWebSocketEvent<{ id: string }>('agent.deleted', ({ id }) => {
    setState((prev) => ({
      ...prev,
      agents: prev.agents.filter((agent) => agent.id !== id),
    }));
  });

  const createAgent = useCallback(async (data: AgentCreate) => {
    const response = await agentApi.create(data);
    return response.data;
  }, []);

  const updateAgent = useCallback(async (id: string, data: AgentUpdate) => {
    const response = await agentApi.update(id, data);
    return response.data;
  }, []);

  const deleteAgent = useCallback(async (id: string) => {
    await agentApi.delete(id);
  }, []);

  const startAgent = useCallback(async (id: string) => {
    const response = await agentApi.start(id);
    return response.data;
  }, []);

  const stopAgent = useCallback(async (id: string) => {
    const response = await agentApi.stop(id);
    return response.data;
  }, []);

  const restartAgent = useCallback(async (id: string) => {
    const response = await agentApi.restart(id);
    return response.data;
  }, []);

  return {
    agents: state.agents,
    loading: state.loading,
    error: state.error,
    refetch: fetchAgents,
    createAgent,
    updateAgent,
    deleteAgent,
    startAgent,
    stopAgent,
    restartAgent,
  };
};

export const useAgent = (id: string) => {
  const [state, setState] = useState<{
    agent: Agent | null;
    loading: boolean;
    error: ApiError | null;
  }>({
    agent: null,
    loading: true,
    error: null,
  });

  const fetchAgent = useCallback(async () => {
    setState((prev) => ({ ...prev, loading: true, error: null }));

    try {
      const response = await agentApi.get(id);
      setState({
        agent: response.data || null,
        loading: false,
        error: null,
      });
    } catch (err) {
      setState({
        agent: null,
        loading: false,
        error: err as ApiError,
      });
    }
  }, [id]);

  useEffect(() => {
    fetchAgent();
  }, [fetchAgent]);

  useWebSocketEvent<Agent>('agent.updated', (updatedAgent) => {
    if (updatedAgent.id === id) {
      setState((prev) => ({
        ...prev,
        agent: updatedAgent,
      }));
    }
  });

  return {
    agent: state.agent,
    loading: state.loading,
    error: state.error,
    refetch: fetchAgent,
  };
};

export const useAgentStats = (id: string) => {
  const [state, setState] = useState<{
    stats: AgentStats | null;
    loading: boolean;
    error: ApiError | null;
  }>({
    stats: null,
    loading: true,
    error: null,
  });

  const fetchStats = useCallback(async () => {
    setState((prev) => ({ ...prev, loading: true, error: null }));

    try {
      const response = await agentApi.getStats(id);
      setState({
        stats: response.data || null,
        loading: false,
        error: null,
      });
    } catch (err) {
      setState({
        stats: null,
        loading: false,
        error: err as ApiError,
      });
    }
  }, [id]);

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  return {
    stats: state.stats,
    loading: state.loading,
    error: state.error,
    refetch: fetchStats,
  };
};

export const useAgentMessages = (id: string, pagination?: PaginationParams) => {
  const [state, setState] = useState<{
    messages: AgentMessage[];
    loading: boolean;
    error: ApiError | null;
  }>({
    messages: [],
    loading: true,
    error: null,
  });

  const fetchMessages = useCallback(async () => {
    setState((prev) => ({ ...prev, loading: true, error: null }));

    try {
      const response = await agentApi.getMessages(id, pagination);
      setState({
        messages: response.data,
        loading: false,
        error: null,
      });
    } catch (err) {
      setState({
        messages: [],
        loading: false,
        error: err as ApiError,
      });
    }
  }, [id, pagination]);

  useEffect(() => {
    fetchMessages();
  }, [fetchMessages]);

  useWebSocketEvent<{ agentId: string; message: string; timestamp: string }>(
    'agent.message',
    (data) => {
      if (data.agentId === id) {
        setState((prev) => ({
          ...prev,
          messages: [
            ...prev.messages,
            {
              id: `${Date.now()}`,
              agentId: data.agentId,
              content: data.message,
              timestamp: data.timestamp,
              senderId: data.agentId,
              receiverId: '',
              messageType: 'notification',
            },
          ],
        }));
      }
    }
  );

  const sendMessage = useCallback(
    async (content: string, to: string) => {
      const response = await agentApi.sendMessage(id, content, to);
      return response.data;
    },
    [id]
  );

  return {
    messages: state.messages,
    loading: state.loading,
    error: state.error,
    refetch: fetchMessages,
    sendMessage,
  };
};
