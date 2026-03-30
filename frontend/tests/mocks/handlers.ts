// MSW request handlers for API mocking
// FEATURE: Testing
import { http, HttpResponse } from 'msw';
import { API_BASE_URL, API_ENDPOINTS } from '../../src/constants/api';
import type { Agent } from '../../src/types/agent';
import type { Task } from '../../src/types/task';

const mockAgents: Agent[] = [
  {
    id: 'agent-1',
    name: 'Test Agent 1',
    type: 'coordinator',
    status: 'active',
    capabilities: ['planning', 'coordination'],
    config: {},
    createdAt: new Date('2026-01-01'),
    updatedAt: new Date('2026-01-01'),
  },
  {
    id: 'agent-2',
    name: 'Test Agent 2',
    type: 'worker',
    status: 'idle',
    capabilities: ['execution'],
    config: {},
    createdAt: new Date('2026-01-01'),
    updatedAt: new Date('2026-01-01'),
  },
];

const mockTasks: Task[] = [
  {
    id: 'task-1',
    status: 'running',
    priority: 'high',
    type: 'processing',
    payload: { data: 'test' },
    result: null,
    agentId: 'agent-1',
    createdAt: new Date('2026-01-01'),
    updatedAt: new Date('2026-01-01'),
    startedAt: new Date('2026-01-01'),
    completedAt: null,
  },
];

export const handlers = [
  // Agents endpoints
  http.get(`${API_BASE_URL}${API_ENDPOINTS.AGENTS}`, () => {
    return HttpResponse.json({
      data: mockAgents,
      success: true,
    });
  }),

  http.get(`${API_BASE_URL}${API_ENDPOINTS.AGENTS}/:id`, ({ params }) => {
    const agent = mockAgents.find((a) => a.id === params.id);
    if (!agent) {
      return HttpResponse.json(
        { error: 'Agent not found' },
        { status: 404 }
      );
    }
    return HttpResponse.json({
      data: agent,
      success: true,
    });
  }),

  http.post(`${API_BASE_URL}${API_ENDPOINTS.AGENTS}`, async ({ request }) => {
    const body = await request.json();
    const newAgent: Agent = {
      id: `agent-${Date.now()}`,
      ...(body as any),
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    return HttpResponse.json(
      {
        data: newAgent,
        success: true,
      },
      { status: 201 }
    );
  }),

  // Tasks endpoints
  http.get(`${API_BASE_URL}${API_ENDPOINTS.TASKS}`, () => {
    return HttpResponse.json({
      data: mockTasks,
      success: true,
    });
  }),

  http.get(`${API_BASE_URL}${API_ENDPOINTS.TASKS}/:id`, ({ params }) => {
    const task = mockTasks.find((t) => t.id === params.id);
    if (!task) {
      return HttpResponse.json(
        { error: 'Task not found' },
        { status: 404 }
      );
    }
    return HttpResponse.json({
      data: task,
      success: true,
    });
  }),

  // Health check
  http.get(`${API_BASE_URL}/health`, () => {
    return HttpResponse.json({
      status: 'ok',
      timestamp: new Date().toISOString(),
    });
  }),
];
