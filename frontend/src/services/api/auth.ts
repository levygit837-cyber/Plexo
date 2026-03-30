// Authentication API endpoints
// FEATURE: Authentication

import { apiClient } from './client';
import { API_ENDPOINTS } from '../../constants/api';
import type { ApiResponse } from '../../types/api';

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterData {
  email: string;
  password: string;
  name: string;
}

interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: {
    id: string;
    email: string;
    name: string;
    role: string;
  };
}

interface RefreshTokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

interface PasswordResetRequest {
  email: string;
}

interface PasswordResetConfirm {
  token: string;
  new_password: string;
}

export const authApi = {
  login: async (credentials: LoginCredentials): Promise<ApiResponse<AuthResponse>> => {
    const response = await apiClient.post<AuthResponse>(API_ENDPOINTS.AUTH.LOGIN, credentials);
    if (response.data?.access_token) {
      apiClient.setAuthToken(response.data.access_token);
    }
    return response;
  },

  register: async (data: RegisterData): Promise<ApiResponse<AuthResponse>> => {
    const response = await apiClient.post<AuthResponse>(API_ENDPOINTS.AUTH.REGISTER, data);
    if (response.data?.access_token) {
      apiClient.setAuthToken(response.data.access_token);
    }
    return response;
  },

  logout: async (): Promise<ApiResponse<void>> => {
    const response = await apiClient.post<void>(API_ENDPOINTS.AUTH.LOGOUT);
    apiClient.setAuthToken(null);
    return response;
  },

  refreshToken: async (refreshToken: string): Promise<ApiResponse<RefreshTokenResponse>> => {
    const response = await apiClient.post<RefreshTokenResponse>(API_ENDPOINTS.AUTH.REFRESH, {
      refresh_token: refreshToken,
    });
    if (response.data?.access_token) {
      apiClient.setAuthToken(response.data.access_token);
    }
    return response;
  },

  getCurrentUser: async (): Promise<ApiResponse<AuthResponse['user']>> => {
    return apiClient.get<AuthResponse['user']>(API_ENDPOINTS.AUTH.ME);
  },

  requestPasswordReset: async (data: PasswordResetRequest): Promise<ApiResponse<void>> => {
    return apiClient.post<void>(API_ENDPOINTS.AUTH.PASSWORD_RESET, data);
  },

  confirmPasswordReset: async (data: PasswordResetConfirm): Promise<ApiResponse<void>> => {
    return apiClient.post<void>(API_ENDPOINTS.AUTH.PASSWORD_RESET_CONFIRM, data);
  },

  verifyToken: async (): Promise<ApiResponse<boolean>> => {
    try {
      await apiClient.get<void>(API_ENDPOINTS.AUTH.VERIFY);
      return { success: true, data: true };
    } catch {
      return { success: false, data: false };
    }
  },
};
