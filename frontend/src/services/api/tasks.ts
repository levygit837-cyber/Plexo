// Task API endpoints
// FEATURE: Task Management

import { apiClient } from './client';
import { API_ENDPOINTS } from '../../constants/api';
import type { ApiResponse, PaginatedResponse } from '../../types/api';
import type {
  Task,
  TaskCreate,
  TaskUpdate,
  TaskStats,
  TaskListFilters,
  TaskDependency,
} from '../../types/task';
import type { PaginationParams } from '../../types/common';

export const taskApi = {
  list: async (
    filters?: TaskListFilters,
    pagination?: PaginationParams
  ): Promise<PaginatedResponse<Task>> => {
    const params = new URLSearchParams();

    if (filters?.status) params.append('status', filters.status);
    if (filters?.type) params.append('type', filters.type);
    if (filters?.priority) params.append('priority', filters.priority);
    if (filters?.agentId) params.append('agent_id', filters.agentId);
    if (filters?.search) params.append('search', filters.search);
    if (filters?.startDate) params.append('start_date', filters.startDate);
    if (filters?.endDate) params.append('end_date', filters.endDate);
    if (pagination?.page) params.append('page', pagination.page.toString());
    if (pagination?.pageSize) params.append('page_size', pagination.pageSize.toString());

    const response = await apiClient.get<Task[]>(
      `${API_ENDPOINTS.TASKS}?${params.toString()}`
    );

    return {
      data: response.data || [],
      meta: {
        page: pagination?.page || 1,
        pageSize: pagination?.pageSize || 10,
        total: response.data?.length || 0,
        totalPages: Math.ceil((response.data?.length || 0) / (pagination?.pageSize || 10)),
      },
    };
  },

  get: async (id: string): Promise<ApiResponse<Task>> => {
    return apiClient.get<Task>(`${API_ENDPOINTS.TASKS}/${id}`);
  },

  create: async (data: TaskCreate): Promise<ApiResponse<Task>> => {
    return apiClient.post<Task>(API_ENDPOINTS.TASKS, data);
  },

  update: async (id: string, data: TaskUpdate): Promise<ApiResponse<Task>> => {
    return apiClient.patch<Task>(`${API_ENDPOINTS.TASKS}/${id}`, data);
  },

  delete: async (id: string): Promise<ApiResponse<void>> => {
    return apiClient.delete<void>(`${API_ENDPOINTS.TASKS}/${id}`);
  },

  cancel: async (id: string): Promise<ApiResponse<Task>> => {
    return apiClient.post<Task>(`${API_ENDPOINTS.TASKS}/${id}/cancel`);
  },

  retry: async (id: string): Promise<ApiResponse<Task>> => {
    return apiClient.post<Task>(`${API_ENDPOINTS.TASKS}/${id}/retry`);
  },

  getStats: async (): Promise<ApiResponse<TaskStats>> => {
    return apiClient.get<TaskStats>(`${API_ENDPOINTS.TASKS}/stats`);
  },

  getDependencies: async (id: string): Promise<ApiResponse<TaskDependency[]>> => {
    return apiClient.get<TaskDependency[]>(`${API_ENDPOINTS.TASKS}/${id}/dependencies`);
  },

  addDependency: async (id: string, dependsOn: string): Promise<ApiResponse<TaskDependency>> => {
    return apiClient.post<TaskDependency>(`${API_ENDPOINTS.TASKS}/${id}/dependencies`, {
      depends_on: dependsOn,
    });
  },

  removeDependency: async (id: string, dependencyId: string): Promise<ApiResponse<void>> => {
    return apiClient.delete<void>(`${API_ENDPOINTS.TASKS}/${id}/dependencies/${dependencyId}`);
  },
};
