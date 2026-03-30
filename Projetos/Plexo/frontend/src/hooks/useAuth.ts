// Authentication hook
// FEATURE: Authentication

import { useState, useEffect, useCallback } from 'react';
import { authApi } from '../services/api/auth';
import { apiClient } from '../services/api/client';
import type { ApiError } from '../types/api';

interface User {
  id: string;
  email: string;
  name: string;
  role: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: ApiError | null;
}

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterData {
  email: string;
  password: string;
  name: string;
}

export const useAuth = () => {
  const [state, setState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
    error: null,
  });

  const checkAuth = useCallback(async () => {
    const token = apiClient.getAuthToken();
    
    if (!token) {
      setState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
      return;
    }

    try {
      const response = await authApi.getCurrentUser();
      
      if (response.data) {
        setState({
          user: response.data,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        });
      }
    } catch (err) {
      apiClient.setAuthToken(null);
      setState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: err as ApiError,
      });
    }
  }, []);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const login = useCallback(async (credentials: LoginCredentials) => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await authApi.login(credentials);
      
      if (response.data) {
        setState({
          user: response.data.user,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        });
        return response.data;
      }
    } catch (err) {
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: err as ApiError,
      }));
      throw err;
    }
  }, []);

  const register = useCallback(async (data: RegisterData) => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await authApi.register(data);
      
      if (response.data) {
        setState({
          user: response.data.user,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        });
        return response.data;
      }
    } catch (err) {
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: err as ApiError,
      }));
      throw err;
    }
  }, []);

  const logout = useCallback(async () => {
    setState((prev) => ({ ...prev, isLoading: true }));

    try {
      await authApi.logout();
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      setState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
    }
  }, []);

  const refreshToken = useCallback(async (refreshToken: string) => {
    try {
      const response = await authApi.refreshToken(refreshToken);
      return response.data;
    } catch (err) {
      await logout();
      throw err;
    }
  }, [logout]);

  const requestPasswordReset = useCallback(async (email: string) => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      await authApi.requestPasswordReset({ email });
      setState((prev) => ({ ...prev, isLoading: false }));
    } catch (err) {
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: err as ApiError,
      }));
      throw err;
    }
  }, []);

  const confirmPasswordReset = useCallback(
    async (token: string, newPassword: string) => {
      setState((prev) => ({ ...prev, isLoading: true, error: null }));

      try {
        await authApi.confirmPasswordReset({ token, new_password: newPassword });
        setState((prev) => ({ ...prev, isLoading: false }));
      } catch (err) {
        setState((prev) => ({
          ...prev,
          isLoading: false,
          error: err as ApiError,
        }));
        throw err;
      }
    },
    []
  );

  return {
    user: state.user,
    isAuthenticated: state.isAuthenticated,
    isLoading: state.isLoading,
    error: state.error,
    login,
    register,
    logout,
    refreshToken,
    requestPasswordReset,
    confirmPasswordReset,
    checkAuth,
  };
};
