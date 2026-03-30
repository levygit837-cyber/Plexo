// Generic API hook with loading and error states
// FEATURE: API Communication

import { useState, useCallback } from 'react';
import type { AsyncState } from '../types/common';

interface UseApiOptions<T> {
  onSuccess?: (data: T) => void;
  onError?: (error: Error) => void;
  initialData?: T;
}

interface UseApiReturn<T, P extends any[]> {
  data: T | null;
  error: string | null;
  loading: boolean;
  execute: (...params: P) => Promise<T | null>;
  reset: () => void;
  state: AsyncState<T>;
}

export const useApi = <T, P extends any[] = []>(
  apiFunction: (...params: P) => Promise<{ data?: T }>,
  options?: UseApiOptions<T>
): UseApiReturn<T, P> => {
  const [state, setState] = useState<AsyncState<T>>({
    data: options?.initialData || null,
    error: null,
    loading: false,
    status: 'idle',
  });

  const execute = useCallback(
    async (...params: P): Promise<T | null> => {
      setState((prev) => ({ ...prev, loading: true, error: null }));

      try {
        const response = await apiFunction(...params);
        const data = response.data || null;

        setState({ data, error: null, loading: false, status: 'success' });

        if (data && options?.onSuccess) {
          options.onSuccess(data);
        }

        return data;
      } catch (err) {
        const error = err instanceof Error ? err : new Error(String(err));
        setState({ data: null, error: error.message, loading: false, status: 'error' });

        if (options?.onError) {
          options.onError(error as Error);
        }

        return null;
      }
    },
    [apiFunction, options]
  );

  const reset = useCallback(() => {
    setState({
      data: options?.initialData || null,
      error: null,
      loading: false,
      status: 'idle',
    });
  }, [options?.initialData]);

  return {
    data: state.data,
    error: state.error,
    loading: state.loading,
    execute,
    reset,
    state,
  };
};

export const useApiMutation = <T, P extends any[] = []>(
  apiFunction: (...params: P) => Promise<{ data?: T }>,
  options?: UseApiOptions<T>
) => {
  return useApi(apiFunction, options);
};

export const useApiQuery = <T, P extends any[] = []>(
  apiFunction: (...params: P) => Promise<{ data?: T }>,
  params: P,
  options?: UseApiOptions<T> & { enabled?: boolean }
) => {
  const api = useApi(apiFunction, options);

  useState(() => {
    if (options?.enabled !== false) {
      api.execute(...params);
    }
  });

  return api;
};
