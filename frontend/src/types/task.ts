// Task domain types and interfaces
// FEATURE: Task Management

import { BaseEntity, Priority, Status } from './common';

export type TaskStatus = 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';

export type TaskType = 'analysis' | 'execution' | 'coordination' | 'monitoring';

export interface TaskPayload {
  [key: string]: unknown;
}

export interface TaskResult {
  success: boolean;
  data?: unknown;
  error?: string;
  executionTime?: number;
  metadata?: Record<string, unknown>;
}

export interface Task extends BaseEntity {
  name: string;
  type: TaskType;
  status: TaskStatus;
  priority: Priority;
  agentId?: string;
  payload: TaskPayload;
  result?: TaskResult;
  startedAt?: string;
  completedAt?: string;
  estimatedDuration?: number;
  actualDuration?: number;
  retryCount?: number;
  maxRetries?: number;
  parentTaskId?: string;
  metadata?: Record<string, unknown>;
}

export interface TaskCreate {
  name: string;
  type: TaskType;
  priority?: Priority;
  agentId?: string;
  payload: TaskPayload;
  estimatedDuration?: number;
  maxRetries?: number;
  parentTaskId?: string;
}

export interface TaskUpdate {
  name?: string;
  status?: TaskStatus;
  priority?: Priority;
  agentId?: string;
  result?: TaskResult;
}

export interface TaskStats {
  total: number;
  pending: number;
  running: number;
  completed: number;
  failed: number;
  cancelled: number;
  averageExecutionTime: number;
}

export interface TaskListFilters {
  type?: TaskType;
  status?: TaskStatus;
  priority?: Priority;
  agentId?: string;
  search?: string;
  dateFrom?: string;
  dateTo?: string;
}

export interface TaskDependency {
  taskId: string;
  dependsOn: string[];
  blockedBy?: string[];
}
