// Task slice for Zustand store
// FEATURE: Task Management

import { StateCreator } from 'zustand';
import type { Task } from '../../types/task';

export interface TaskSlice {
  tasks: Task[];
  selectedTaskId: string | null;
  setTasks: (tasks: Task[]) => void;
  addTask: (task: Task) => void;
  updateTask: (id: string, updates: Partial<Task>) => void;
  removeTask: (id: string) => void;
  selectTask: (id: string | null) => void;
  getTaskById: (id: string) => Task | undefined;
  getTasksByStatus: (status: string) => Task[];
  getTasksByType: (type: string) => Task[];
  getTasksByPriority: (priority: string) => Task[];
  getTasksByAgent: (agentId: string) => Task[];
}

export const taskSlice: StateCreator<TaskSlice> = (set, get) => ({
  tasks: [],
  selectedTaskId: null,

  setTasks: (tasks) => set({ tasks }),

  addTask: (task) =>
    set((state) => {
      const exists = state.tasks.some((t) => t.id === task.id);
      if (exists) {
        return {
          tasks: state.tasks.map((t) => (t.id === task.id ? task : t)),
        };
      }
      return { tasks: [...state.tasks, task] };
    }),

  updateTask: (id, updates) =>
    set((state) => ({
      tasks: state.tasks.map((task) =>
        task.id === id ? { ...task, ...updates } : task
      ),
    })),

  removeTask: (id) =>
    set((state) => ({
      tasks: state.tasks.filter((task) => task.id !== id),
      selectedTaskId: state.selectedTaskId === id ? null : state.selectedTaskId,
    })),

  selectTask: (id) => set({ selectedTaskId: id }),

  getTaskById: (id) => {
    const state = get();
    return state.tasks.find((task) => task.id === id);
  },

  getTasksByStatus: (status) => {
    const state = get();
    return state.tasks.filter((task) => task.status === status);
  },

  getTasksByType: (type) => {
    const state = get();
    return state.tasks.filter((task) => task.type === type);
  },

  getTasksByPriority: (priority) => {
    const state = get();
    return state.tasks.filter((task) => task.priority === priority);
  },

  getTasksByAgent: (agentId) => {
    const state = get();
    return state.tasks.filter((task) => task.agent_id === agentId);
  },
});
