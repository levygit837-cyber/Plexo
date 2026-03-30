// WebSocket hook for real-time communication
// FEATURE: Real-time Communication

import { useEffect, useCallback, useRef, useState } from 'react';
import { wsClient } from '../services/websocket/client';
import type { WebSocketMessage } from '../types/api';

interface UseWebSocketOptions {
  autoConnect?: boolean;
  onConnected?: () => void;
  onDisconnected?: () => void;
  onError?: (error: any) => void;
}

export const useWebSocket = (options?: UseWebSocketOptions) => {
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<any>(null);
  const handlersRef = useRef<Map<string, Set<(data: any) => void>>>(new Map());

  useEffect(() => {
    const handleConnected = () => {
      setIsConnected(true);
      setError(null);
      options?.onConnected?.();
    };

    const handleDisconnected = () => {
      setIsConnected(false);
      options?.onDisconnected?.();
    };

    const handleError = (err: any) => {
      setError(err);
      options?.onError?.(err);
    };

    wsClient.on('connected', handleConnected);
    wsClient.on('disconnected', handleDisconnected);
    wsClient.on('error', handleError);

    if (options?.autoConnect !== false) {
      wsClient.connect().catch((err) => {
        console.error('WebSocket connection failed:', err);
        setError(err);
      });
    }

    return () => {
      wsClient.off('connected', handleConnected);
      wsClient.off('disconnected', handleDisconnected);
      wsClient.off('error', handleError);

      handlersRef.current.forEach((handlers, event) => {
        handlers.forEach((handler) => {
          wsClient.off(event, handler);
        });
      });
      handlersRef.current.clear();
    };
  }, [options]);

  const connect = useCallback(async () => {
    try {
      await wsClient.connect();
    } catch (err) {
      setError(err);
      throw err;
    }
  }, []);

  const disconnect = useCallback(() => {
    wsClient.disconnect();
  }, []);

  const send = useCallback((message: WebSocketMessage) => {
    wsClient.send(message);
  }, []);

  const on = useCallback((event: string, handler: (data: any) => void) => {
    if (!handlersRef.current.has(event)) {
      handlersRef.current.set(event, new Set());
    }
    handlersRef.current.get(event)!.add(handler);
    wsClient.on(event, handler);

    return () => {
      const handlers = handlersRef.current.get(event);
      if (handlers) {
        handlers.delete(handler);
        if (handlers.size === 0) {
          handlersRef.current.delete(event);
        }
      }
      wsClient.off(event, handler);
    };
  }, []);

  const setAuthToken = useCallback((token: string | null) => {
    wsClient.setAuthToken(token);
  }, []);

  return {
    isConnected,
    error,
    connect,
    disconnect,
    send,
    on,
    setAuthToken,
  };
};

export const useWebSocketEvent = <T = any>(
  event: string,
  handler: (data: T) => void,
  deps: React.DependencyList = []
) => {
  const { on } = useWebSocket({ autoConnect: false });

  useEffect(() => {
    const unsubscribe = on(event, handler);
    return unsubscribe;
  }, [event, on, ...deps]);
};
