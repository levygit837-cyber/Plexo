// WebSocket event handlers
// FEATURE: Real-time Communication

import type { WebSocketMessage } from '../../types/api';
import type { Agent } from '../../types/agent';
import type { Task } from '../../types/task';

export type WebSocketEventType =
  | 'agent.created'
  | 'agent.updated'
  | 'agent.deleted'
  | 'agent.started'
  | 'agent.stopped'
  | 'agent.message'
  | 'task.created'
  | 'task.updated'
  | 'task.deleted'
  | 'task.completed'
  | 'task.failed'
  | 'notification'
  | 'error';

export interface WebSocketEventData {
  'agent.created': Agent;
  'agent.updated': Agent;
  'agent.deleted': { id: string };
  'agent.started': Agent;
  'agent.stopped': Agent;
  'agent.message': {
    agentId: string;
    message: string;
    timestamp: string;
  };
  'task.created': Task;
  'task.updated': Task;
  'task.deleted': { id: string };
  'task.completed': Task;
  'task.failed': {
    task: Task;
    error: string;
  };
  'notification': {
    type: 'info' | 'success' | 'warning' | 'error';
    title: string;
    message: string;
  };
  'error': {
    code: string;
    message: string;
    details?: any;
  };
}

export type WebSocketEventHandler<T extends WebSocketEventType> = (
  data: WebSocketEventData[T]
) => void;

export class WebSocketHandlerRegistry {
  private handlers: Map<WebSocketEventType, Set<WebSocketEventHandler<any>>> = new Map();

  public register<T extends WebSocketEventType>(
    event: T,
    handler: WebSocketEventHandler<T>
  ): () => void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    this.handlers.get(event)!.add(handler);

    return () => this.unregister(event, handler);
  }

  public unregister<T extends WebSocketEventType>(
    event: T,
    handler: WebSocketEventHandler<T>
  ): void {
    const handlers = this.handlers.get(event);
    if (handlers) {
      handlers.delete(handler);
    }
  }

  public handle(message: WebSocketMessage): void {
    const { event, data } = message;
    const handlers = this.handlers.get(event as WebSocketEventType);

    if (handlers) {
      handlers.forEach((handler) => {
        try {
          handler(data);
        } catch (error) {
          console.error(`Error handling WebSocket event '${event}':`, error);
        }
      });
    }
  }

  public clear(): void {
    this.handlers.clear();
  }
}

export const wsHandlerRegistry = new WebSocketHandlerRegistry();

export const createAgentHandlers = (callbacks: {
  onCreated?: WebSocketEventHandler<'agent.created'>;
  onUpdated?: WebSocketEventHandler<'agent.updated'>;
  onDeleted?: WebSocketEventHandler<'agent.deleted'>;
  onStarted?: WebSocketEventHandler<'agent.started'>;
  onStopped?: WebSocketEventHandler<'agent.stopped'>;
  onMessage?: WebSocketEventHandler<'agent.message'>;
}) => {
  const unsubscribers: Array<() => void> = [];

  if (callbacks.onCreated) {
    unsubscribers.push(wsHandlerRegistry.register('agent.created', callbacks.onCreated));
  }
  if (callbacks.onUpdated) {
    unsubscribers.push(wsHandlerRegistry.register('agent.updated', callbacks.onUpdated));
  }
  if (callbacks.onDeleted) {
    unsubscribers.push(wsHandlerRegistry.register('agent.deleted', callbacks.onDeleted));
  }
  if (callbacks.onStarted) {
    unsubscribers.push(wsHandlerRegistry.register('agent.started', callbacks.onStarted));
  }
  if (callbacks.onStopped) {
    unsubscribers.push(wsHandlerRegistry.register('agent.stopped', callbacks.onStopped));
  }
  if (callbacks.onMessage) {
    unsubscribers.push(wsHandlerRegistry.register('agent.message', callbacks.onMessage));
  }

  return () => unsubscribers.forEach((unsubscribe) => unsubscribe());
};

export const createTaskHandlers = (callbacks: {
  onCreated?: WebSocketEventHandler<'task.created'>;
  onUpdated?: WebSocketEventHandler<'task.updated'>;
  onDeleted?: WebSocketEventHandler<'task.deleted'>;
  onCompleted?: WebSocketEventHandler<'task.completed'>;
  onFailed?: WebSocketEventHandler<'task.failed'>;
}) => {
  const unsubscribers: Array<() => void> = [];

  if (callbacks.onCreated) {
    unsubscribers.push(wsHandlerRegistry.register('task.created', callbacks.onCreated));
  }
  if (callbacks.onUpdated) {
    unsubscribers.push(wsHandlerRegistry.register('task.updated', callbacks.onUpdated));
  }
  if (callbacks.onDeleted) {
    unsubscribers.push(wsHandlerRegistry.register('task.deleted', callbacks.onDeleted));
  }
  if (callbacks.onCompleted) {
    unsubscribers.push(wsHandlerRegistry.register('task.completed', callbacks.onCompleted));
  }
  if (callbacks.onFailed) {
    unsubscribers.push(wsHandlerRegistry.register('task.failed', callbacks.onFailed));
  }

  return () => unsubscribers.forEach((unsubscribe) => unsubscribe());
};
