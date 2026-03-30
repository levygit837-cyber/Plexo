// Agent domain types and interfaces
// FEATURE: Multi-Agent System

import { BaseEntity, Status } from './common';

export type AgentType = 'coordinator' | 'executor' | 'analyzer' | 'monitor';

export type AgentStatus = 'active' | 'inactive' | 'pending' | 'error' | 'busy' | 'offline';

export type AgentCapability =
  | 'task_execution'
  | 'data_analysis'
  | 'coordination'
  | 'monitoring'
  | 'communication'
  | 'decision_making';

export interface AgentConfig {
  maxConcurrentTasks?: number;
  timeout?: number;
  retryAttempts?: number;
  priority?: number;
  [key: string]: unknown;
}

export interface Agent extends BaseEntity {
  name: string;
  type: AgentType;
  status: Status;
  capabilities: AgentCapability[];
  config: AgentConfig;
  description?: string;
  lastActiveAt?: string;
  metadata?: Record<string, unknown>;
}

export interface AgentCreate {
  name: string;
  type: AgentType;
  capabilities: AgentCapability[];
  config?: AgentConfig;
  description?: string;
}

export interface AgentUpdate {
  name?: string;
  status?: Status;
  capabilities?: AgentCapability[];
  config?: AgentConfig;
  description?: string;
}

export interface AgentStats {
  agentId: string;
  tasksCompleted: number;
  tasksInProgress: number;
  tasksFailed: number;
  averageExecutionTime: number;
  uptime: number;
  lastError?: string;
}

export interface AgentMessage {
  id: string;
  senderId: string;
  receiverId: string;
  content: string;
  messageType: 'request' | 'response' | 'notification' | 'error';
  timestamp: string;
  metadata?: Record<string, unknown>;
}

export interface AgentListFilters {
  type?: AgentType;
  status?: Status;
  capabilities?: AgentCapability[];
  search?: string;
}
