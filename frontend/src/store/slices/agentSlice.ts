// Agent slice for Zustand store
// FEATURE: Multi-Agent System

import { StateCreator } from 'zustand';
import type { Agent } from '../../types/agent';

export interface AgentSlice {
  agents: Agent[];
  selectedAgentId: string | null;
  setAgents: (agents: Agent[]) => void;
  addAgent: (agent: Agent) => void;
  updateAgent: (id: string, updates: Partial<Agent>) => void;
  removeAgent: (id: string) => void;
  selectAgent: (id: string | null) => void;
  getAgentById: (id: string) => Agent | undefined;
  getAgentsByType: (type: string) => Agent[];
  getAgentsByStatus: (status: string) => Agent[];
}

export const agentSlice: StateCreator<AgentSlice> = (set, get) => ({
  agents: [],
  selectedAgentId: null,

  setAgents: (agents) => set({ agents }),

  addAgent: (agent) =>
    set((state) => {
      const exists = state.agents.some((a) => a.id === agent.id);
      if (exists) {
        return {
          agents: state.agents.map((a) => (a.id === agent.id ? agent : a)),
        };
      }
      return { agents: [...state.agents, agent] };
    }),

  updateAgent: (id, updates) =>
    set((state) => ({
      agents: state.agents.map((agent) =>
        agent.id === id ? { ...agent, ...updates } : agent
      ),
    })),

  removeAgent: (id) =>
    set((state) => ({
      agents: state.agents.filter((agent) => agent.id !== id),
      selectedAgentId: state.selectedAgentId === id ? null : state.selectedAgentId,
    })),

  selectAgent: (id) => set({ selectedAgentId: id }),

  getAgentById: (id) => {
    const state = get();
    return state.agents.find((agent) => agent.id === id);
  },

  getAgentsByType: (type) => {
    const state = get();
    return state.agents.filter((agent) => agent.type === type);
  },

  getAgentsByStatus: (status) => {
    const state = get();
    return state.agents.filter((agent) => agent.status === status);
  },
});
