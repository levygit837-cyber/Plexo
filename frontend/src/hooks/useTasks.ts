// Tasks hook with CRUD operations and real-time updates
// FEATURE: Task Management

import { useState, useEffect, useCallback } from 'react';
import { taskApi } from '../services/api/tasks';
import { useWebSocketEvent } from './useWebSocket';
import type {
  Task,
  TaskCreate,
  TaskUpdate,
  TaskListFilters,
  TaskStats,
  TaskDependency,
} from '../types/task';
import type { PaginationParams } from '../types/common';
import type { ApiError } from '../types/api';

interface UseTasksState {
  tasks: Task[];
  loading: boolean;
  error: ApiError | null;
}

export const useTasks = (filters?: TaskListFilters, pagination?: PaginationParams) => {
  const [state, setState] = useState<UseTasksState>({
    tasks: [],
    loading: true,
    error: null,
  });

  const fetchTasks = useCallback(async () => {
    setState((prev) => ({ ...prev, loading: true, error: null }));

    try {
      const response = await taskApi.list(filters, pagination);
      setState({
        tasks: response.data,
        loading: false,
        error: null,
      });
    } catch (err) {
      setState({
        tasks: [],
        loading: false,
        error: err as ApiError,
      });
    }
  }, [filters, pagination]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  useWebSocketEvent<Task>('task.created', (task) => {
    setState((prev) => ({
      ...prev,
      tasks: [...prev.tasks, task],
    }));
  });

  useWebSocketEvent<Task>('task.updated', (updatedTask) => {
    setState((prev) => ({
      ...prev,
      tasks: prev.tasks.map((task) =>
        task.id === updatedTask.id ? updatedTask : task
      ),
    }));
  });

  useWebSocketEvent<{ id: string }>('task.deleted', ({ id }) => {
    setState((prev) => ({
      ...prev,
      tasks: prev.tasks.filter((task) => task.id !== id),
    }));
  });

  useWebSocketEvent<Task>('task.completed', (completedTask) => {
    setState((prev) => ({
      ...prev,
      tasks: prev.tasks.map((task) =>
        task.id === completedTask.id ? completedTask : task
      ),
    }));
  });

  useWebSocketEvent<{ task: Task; error: string }>('task.failed', ({ task: failedTask }) => {
    setState((prev) => ({
      ...prev,
      tasks: prev.tasks.map((task) =>
        task.id === failedTask.id ? failedTask : task
      ),
    }));
  });

  const createTask = useCallback(async (data: TaskCreate) => {
    const response = await taskApi.create(data);
    return response.data;
  }, []);

  const updateTask = useCallback(async (id: string, data: TaskUpdate) => {
    const response = await taskApi.update(id, data);
    return response.data;
  }, []);

  const deleteTask = useCallback(async (id: string) => {
    await taskApi.delete(id);
  }, []);

  const cancelTask = useCallback(async (id: string) => {
    const response = await taskApi.cancel(id);
    return response.data;
  }, []);

  const retryTask = useCallback(async (id: string) => {
    const response = await taskApi.retry(id);
    return response.data;
  }, []);

  return {
    tasks: state.tasks,
    loading: state.loading,
    error: state.error,
    refetch: fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    cancelTask,
    retryTask,
  };
};

export const useTask = (id: string) => {
  const [state, setState] = useState<{
    task: Task | null;
    loading: boolean;
    error: ApiError | null;
  }>({
    task: null,
    loading: true,
    error: null,
  });

  const fetchTask = useCallback(async () => {
    setState((prev) => ({ ...prev, loading: true, error: null }));

    try {
      const response = await taskApi.get(id);
      setState({
        task: response.data || null,
        loading: false,
        error: null,
      });
    } catch (err) {
      setState({
        task: null,
        loading: false,
        error: err as ApiError,
      });
    }
  }, [id]);

  useEffect(() => {
    fetchTask();
  }, [fetchTask]);

  useWebSocketEvent<Task>('task.updated', (updatedTask) => {
    if (updatedTask.id === id) {
      setState((prev) => ({
        ...prev,
        task: updatedTask,
      }));
    }
  });

  useWebSocketEvent<Task>('task.completed', (completedTask) => {
    if (completedTask.id === id) {
      setState((prev) => ({
        ...prev,
        task: completedTask,
      }));
    }
  });

  useWebSocketEvent<{ task: Task; error: string }>('task.failed', ({ task: failedTask }) => {
    if (failedTask.id === id) {
      setState((prev) => ({
        ...prev,
        task: failedTask,
      }));
    }
  });

  return {
    task: state.task,
    loading: state.loading,
    error: state.error,
    refetch: fetchTask,
  };
};

export const useTaskStats = () => {
  const [state, setState] = useState<{
    stats: TaskStats | null;
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
      const response = await taskApi.getStats();
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
  }, []);

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

export const useTaskDependencies = (id: string) => {
  const [state, setState] = useState<{
    dependencies: TaskDependency[];
    loading: boolean;
    error: ApiError | null;
  }>({
    dependencies: [],
    loading: true,
    error: null,
  });

  const fetchDependencies = useCallback(async () => {
    setState((prev) => ({ ...prev, loading: true, error: null }));

    try {
      const response = await taskApi.getDependencies(id);
      setState({
        dependencies: response.data || [],
        loading: false,
        error: null,
      });
    } catch (err) {
      setState({
        dependencies: [],
        loading: false,
        error: err as ApiError,
      });
    }
  }, [id]);

  useEffect(() => {
    fetchDependencies();
  }, [fetchDependencies]);

  const addDependency = useCallback(
    async (dependsOn: string) => {
      const response = await taskApi.addDependency(id, dependsOn);
      await fetchDependencies();
      return response.data;
    },
    [id, fetchDependencies]
  );

  const removeDependency = useCallback(
    async (dependencyId: string) => {
      await taskApi.removeDependency(id, dependencyId);
      await fetchDependencies();
    },
    [id, fetchDependencies]
  );

  return {
    dependencies: state.dependencies,
    loading: state.loading,
    error: state.error,
    refetch: fetchDependencies,
    addDependency,
    removeDependency,
  };
};
