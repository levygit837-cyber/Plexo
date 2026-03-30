// Zustand store configuration and setup
// FEATURE: State Management

import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { agentSlice, AgentSlice } from './slices/agentSlice';
import { taskSlice, TaskSlice } from './slices/taskSlice';

export interface RootState extends AgentSlice, TaskSlice {}

export const useStore = create<RootState>()((
  devtools(
    persist(
      (...args) => ({
        ...agentSlice(...args),
        ...taskSlice(...args),
      }),
      {
        name: 'plexo-storage',
        partialize: (state) => ({
          agents: state.agents,
          tasks: state.tasks,
        }),
      }
    ),
    {
      name: 'Plexo Store',
      enabled: import.meta.env.DEV,
    }
  )
));

export const useAgentStore = () => useStore((state) => ({
  agents: state.agents,
  selectedAgentId: state.selectedAgentId,
  setAgents: state.setAgents,
  addAgent: state.addAgent,
  updateAgent: state.updateAgent,
  removeAgent: state.removeAgent,
  selectAgent: state.selectAgent,
}));

export const useTaskStore = () => useStore((state) => ({
  tasks: state.tasks,
  selectedTaskId: state.selectedTaskId,
  setTasks: state.setTasks,
  addTask: state.addTask,
  updateTask: state.updateTask,
  removeTask: state.removeTask,
  selectTask: state.selectTask,
}));
