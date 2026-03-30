// Integration tests for Home page
// FEATURE: Testing
import { describe, it, expect } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Home from '../../../src/pages/Home';
import { AuthProvider } from '../../../src/contexts/AuthContext';
import { ThemeProvider } from '../../../src/contexts/ThemeContext';
import { NotificationProvider } from '../../../src/contexts/NotificationContext';
import { AgentProvider } from '../../../src/contexts/AgentContext';

const AllProviders = ({ children }: { children: React.ReactNode }) => (
  <BrowserRouter>
    <ThemeProvider>
      <AuthProvider>
        <NotificationProvider>
          <AgentProvider>
            {children}
          </AgentProvider>
        </NotificationProvider>
      </AuthProvider>
    </ThemeProvider>
  </BrowserRouter>
);

describe('Home Page Integration', () => {
  it('renders dashboard title and subtitle', async () => {
    render(
      <AllProviders>
        <Home />
      </AllProviders>
    );

    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(
      screen.getByText('Visão geral do sistema multi-agentes Plexo')
    ).toBeInTheDocument();
  });

  it('displays statistics cards', async () => {
    render(
      <AllProviders>
        <Home />
      </AllProviders>
    );

    await waitFor(() => {
      expect(screen.getByText('Agentes Ativos')).toBeInTheDocument();
      expect(screen.getByText('Tarefas em Execução')).toBeInTheDocument();
      expect(screen.getByText('Tarefas Concluídas')).toBeInTheDocument();
      expect(screen.getByText('Mensagens Trocadas')).toBeInTheDocument();
    });
  });

  it('displays recent agents section', async () => {
    render(
      <AllProviders>
        <Home />
      </AllProviders>
    );

    await waitFor(() => {
      expect(screen.getByText('Agentes Recentes')).toBeInTheDocument();
      expect(screen.getByText('Ver todos')).toBeInTheDocument();
    });
  });

  it('displays recent tasks section', async () => {
    render(
      <AllProviders>
        <Home />
      </AllProviders>
    );

    await waitFor(() => {
      expect(screen.getByText('Tarefas Recentes')).toBeInTheDocument();
    });
  });

  it('shows loading state initially', () => {
    render(
      <AllProviders>
        <Home />
      </AllProviders>
    );

    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('renders agent cards when data is loaded', async () => {
    render(
      <AllProviders>
        <Home />
      </AllProviders>
    );

    await waitFor(() => {
      expect(screen.getByText('Test Agent 1')).toBeInTheDocument();
      expect(screen.getByText('Test Agent 2')).toBeInTheDocument();
    });
  });

  it('renders task cards when data is loaded', async () => {
    render(
      <AllProviders>
        <Home />
      </AllProviders>
    );

    await waitFor(() => {
      expect(screen.getByText('task-1')).toBeInTheDocument();
    });
  });

  it('navigation links work correctly', async () => {
    render(
      <AllProviders>
        <Home />
      </AllProviders>
    );

    await waitFor(() => {
      const verTodosLinks = screen.getAllByText('Ver todos');
      expect(verTodosLinks).toHaveLength(2);
      
      verTodosLinks.forEach(link => {
        expect(link).toHaveAttribute('href');
      });
    });
  });
});
