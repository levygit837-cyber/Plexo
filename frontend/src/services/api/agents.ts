// Agent API endpoints
// FEATURE: Multi-Agent System

import { apiClient } from './client';
import { API_ENDPOINTS } from '../../constants/api';
import type { ApiResponse, PaginatedResponse } from '../../types/api';
import type {
  Agent,
  AgentCreate,
  AgentUpdate,
  AgentStats,
  AgentMessage,
  AgentListFilters,
} from '../../types/agent';
import type { PaginationParams } from '../../types/common';

export const agentApi = {
  list: async (
    filters?: AgentListFilters,
    pagination?: PaginationParams
  ): Promise<PaginatedResponse<Agent>> => {
    const params = new URLSearchParams();

    if (filters?.type) params.append('type', filters.type);
    if (filters?.status) params.append('status', filters.status);
    if (filters?.search) params.append('search', filters.search);
    if (pagination?.page) params.append('page', pagination.page.toString());
    if (pagination?.pageSize) params.append('page_size', pagination.pageSize.toString());

    const response = await apiClient.get<Agent[]>(
      `${API_ENDPOINTS.AGENTS}?${params.toString()}`
    );

    const totalItems = response.data?.length || 0;
    const pageSize = pagination?.pageSize || 10;
    const currentPage = pagination?.page || 1;
    const totalPages = Math.ceil(totalItems / pageSize);

    return {
      data: response.data || [],
      meta: {
        currentPage,
        pageSize,
        totalPages,
        totalItems,
        hasNext: currentPage < totalPages,
        hasPrevious: currentPage > 1,
      },
    };
  },

  get: async (id: string): Promise<ApiResponse<Agent>> => {
    return apiClient.get<Agent>(`${API_ENDPOINTS.AGENTS}/${id}`);
  },

  create: async (data: AgentCreate): Promise<ApiResponse<Agent>> => {
    return apiClient.post<Agent>(API_ENDPOINTS.AGENTS, data);
  },

  update: async (id: string, data: AgentUpdate): Promise<ApiResponse<Agent>> => {
    return apiClient.patch<Agent>(`${API_ENDPOINTS.AGENTS}/${id}`, data);
  },

  delete: async (id: string): Promise<ApiResponse<void>> => {
    return apiClient.delete<void>(`${API_ENDPOINTS.AGENTS}/${id}`);
  },

  start: async (id: string): Promise<ApiResponse<Agent>> => {
    return apiClient.post<Agent>(`${API_ENDPOINTS.AGENTS}/${id}/start`);
  },

  stop: async (id: string): Promise<ApiResponse<Agent>> => {
    return apiClient.post<Agent>(`${API_ENDPOINTS.AGENTS}/${id}/stop`);
  },

  restart: async (id: string): Promise<ApiResponse<Agent>> => {
    return apiClient.post<Agent>(`${API_ENDPOINTS.AGENTS}/${id}/restart`);
  },

  getStats: async (id: string): Promise<ApiResponse<AgentStats>> => {
    return apiClient.get<AgentStats>(`${API_ENDPOINTS.AGENTS}/${id}/stats`);
  },

  getMessages: async (
    id: string,
    pagination?: PaginationParams
  ): Promise<PaginatedResponse<AgentMessage>> => {
    const params = new URLSearchParams();
    if (pagination?.page) params.append('page', pagination.page.toString());
    if (pagination?.pageSize) params.append('page_size', pagination.pageSize.toString());

    const response = await apiClient.get<AgentMessage[]>(
      `${API_ENDPOINTS.AGENTS}/${id}/messages?${params.toString()}`
    );

    const totalItems = response.data?.length || 0;
    const pageSize = pagination?.pageSize || 10;
    const currentPage = pagination?.page || 1;
    const totalPages = Math.ceil(totalItems / pageSize);

    return {
      data: response.data || [],
      meta: {
        currentPage,
        pageSize,
        totalPages,
        totalItems,
        hasNext: currentPage < totalPages,
        hasPrevious: currentPage > 1,
      },
    };
  },

  sendMessage: async (id: string, content: string, to: string): Promise<ApiResponse<AgentMessage>> => {
    return apiClient.post<AgentMessage>(`${API_ENDPOINTS.AGENTS}/${id}/messages`, {
      content,
      to,
    });
  },
};
