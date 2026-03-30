// Axios API client configuration and setup
// FEATURE: API Communication

import axios, { AxiosInstance, AxiosError, AxiosRequestConfig, InternalAxiosRequestConfig } from 'axios';
import { API_BASE_URL, API_TIMEOUT, API_HEADERS } from '../../constants/api';
import type { ApiResponse, ApiError, ApiClientConfig } from '../../types/api';

class ApiClient {
  private instance: AxiosInstance;
  private authToken: string | null = null;

  constructor(config?: ApiClientConfig) {
    this.instance = axios.create({
      baseURL: config?.baseURL || API_BASE_URL,
      timeout: config?.timeout || API_TIMEOUT,
      headers: {
        ...API_HEADERS,
        ...config?.headers,
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    this.instance.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        if (this.authToken && config.headers) {
          config.headers.Authorization = `Bearer ${this.authToken}`;
        }
        return config;
      },
      (error: AxiosError) => Promise.reject(error)
    );

    this.instance.interceptors.response.use(
      (response) => response,
      (error: AxiosError<ApiError>) => {
        const apiError = this.handleApiError(error);
        return Promise.reject(apiError);
      }
    );
  }

  private handleApiError(error: AxiosError<ApiError>): ApiError {
    if (error.response) {
      return {
        code: error.response.data?.code || error.response.status.toString(),
        message: error.response.data?.message || error.message,
        details: error.response.data?.details,
        timestamp: error.response.data?.timestamp || new Date().toISOString(),
        path: error.config?.url,
      };
    }

    if (error.request) {
      return {
        code: 'NETWORK_ERROR',
        message: 'Network error. Please check your connection.',
        timestamp: new Date().toISOString(),
        path: error.config?.url,
      };
    }

    return {
      code: 'UNKNOWN_ERROR',
      message: error.message || 'An unknown error occurred',
      timestamp: new Date().toISOString(),
    };
  }

  public setAuthToken(token: string | null): void {
    this.authToken = token;
    if (token) {
      localStorage.setItem('auth_token', token);
    } else {
      localStorage.removeItem('auth_token');
    }
  }

  public getAuthToken(): string | null {
    if (!this.authToken) {
      this.authToken = localStorage.getItem('auth_token');
    }
    return this.authToken;
  }

  public async get<T>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    const response = await this.instance.get<ApiResponse<T>>(url, config);
    return response.data;
  }

  public async post<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    const response = await this.instance.post<ApiResponse<T>>(url, data, config);
    return response.data;
  }

  public async put<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    const response = await this.instance.put<ApiResponse<T>>(url, data, config);
    return response.data;
  }

  public async patch<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    const response = await this.instance.patch<ApiResponse<T>>(url, data, config);
    return response.data;
  }

  public async delete<T>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    const response = await this.instance.delete<ApiResponse<T>>(url, config);
    return response.data;
  }
}

export const apiClient = new ApiClient();

export const createApiClient = (config?: ApiClientConfig): ApiClient => {
  return new ApiClient(config);
};

export { ApiClient };
