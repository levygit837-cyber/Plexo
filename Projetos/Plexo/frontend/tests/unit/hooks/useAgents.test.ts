// Unit tests for useAgents hook
// FEATURE: Testing
import { describe, it, expect, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useAgents } from '../../../src/hooks/useAgents';
import { server } from '../../mocks/server';
import { http, HttpResponse } from 'msw';
import { API_BASE_URL, API_ENDPOINTS } from '../../../src/constants/api';

describe('useAgents Hook', () => {
  it('fetches agents successfully', async () => {
    const { result } = renderHook(() => useAgents());

    expect(result.current.loading).toBe(true);
    expect(result.current.agents).toEqual([]);

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.agents).toHaveLength(2);
    expect(result.current.agents[0].name).toBe('Test Agent 1');
    expect(result.current.error).toBeNull();
  });

  it('handles fetch error', async () => {
    server.use(
      http.get(`${API_BASE_URL}${API_ENDPOINTS.AGENTS}`, () => {
        return HttpResponse.json(
          { error: 'Internal Server Error' },
          { status: 500 }
        );
      })
    );

    const { result } = renderHook(() => useAgents());

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.error).toBeTruthy();
    expect(result.current.agents).toEqual([]);
  });

  it('filters agents by status', async () => {
    const { result } = renderHook(() => useAgents({ status: 'active' }));

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    const activeAgents = result.current.agents.filter(
      (agent) => agent.status === 'active'
    );
    expect(activeAgents).toHaveLength(1);
    expect(activeAgents[0].name).toBe('Test Agent 1');
  });

  it('filters agents by type', async () => {
    const { result } = renderHook(() => useAgents({ type: 'coordinator' }));

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    const coordinatorAgents = result.current.agents.filter(
      (agent) => agent.type === 'coordinator'
    );
    expect(coordinatorAgents).toHaveLength(1);
    expect(coordinatorAgents[0].name).toBe('Test Agent 1');
  });

  it('refetches agents when refresh is called', async () => {
    const { result } = renderHook(() => useAgents());

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    const initialAgents = result.current.agents;
    expect(initialAgents).toHaveLength(2);

    result.current.refresh();

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.agents).toHaveLength(2);
  });
});
