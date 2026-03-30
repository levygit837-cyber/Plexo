// API endpoint constants and configuration
// FEATURE: API Communication

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const API_VERSION = 'v1';

export const API_TIMEOUT = 30000;

export const API_ENDPOINTS = {
  HEALTH: '/health',
  AGENTS: '/agents',
  TASKS: '/tasks',
  MESSAGES: '/messages',
  AUTH: '/auth',
} as const;

export const WEBSOCKET_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';

export const WEBSOCKET_RECONNECT_INTERVAL = 5000;

export const WEBSOCKET_MAX_RECONNECT_ATTEMPTS = 5;

export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  CONFLICT: 409,
  UNPROCESSABLE_ENTITY: 422,
  INTERNAL_SERVER_ERROR: 500,
  SERVICE_UNAVAILABLE: 503,
} as const;

export const API_HEADERS = {
  CONTENT_TYPE: 'Content-Type',
  AUTHORIZATION: 'Authorization',
  ACCEPT: 'Accept',
} as const;

export const CONTENT_TYPES = {
  JSON: 'application/json',
  FORM_DATA: 'multipart/form-data',
  URL_ENCODED: 'application/x-www-form-urlencoded',
} as const;

export const DEFAULT_PAGE_SIZE = 20;

export const MAX_PAGE_SIZE = 100;

export const QUERY_KEYS = {
  AGENTS: 'agents',
  AGENT_DETAIL: 'agent-detail',
  AGENT_STATS: 'agent-stats',
  TASKS: 'tasks',
  TASK_DETAIL: 'task-detail',
  TASK_STATS: 'task-stats',
  MESSAGES: 'messages',
  HEALTH: 'health',
} as const;
