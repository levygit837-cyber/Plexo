// Agent list component with filtering and search
// Displays all agents with status, type, and capabilities
import React, { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { Plus } from 'lucide-react';
import { useAgents } from '../../hooks/useAgents';
import { AgentCard } from '../../components/features/agents/AgentCard';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { Loading } from '../../components/common/Loading';
import { ROUTES } from '../../constants/routes';
import type { AgentStatus, AgentType } from '../../types/agent';

const AgentList: React.FC = () => {
  const { agents, loading, error } = useAgents();
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<AgentStatus | 'all'>('all');
  const [typeFilter, setTypeFilter] = useState<AgentType | 'all'>('all');

  const filteredAgents = useMemo(() => {
    return agents.filter((agent) => {
      const matchesSearch = agent.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        agent.id.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesStatus = statusFilter === 'all' || agent.status === statusFilter;
      const matchesType = typeFilter === 'all' || agent.type === typeFilter;
      return matchesSearch && matchesStatus && matchesType;
    });
  }, [agents, searchTerm, statusFilter, typeFilter]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <Loading size="lg" variant="spinner" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 text-center">
        <p className="text-red-500 mb-4">Erro ao carregar agentes: {error.message}</p>
        <Button onClick={() => window.location.reload()}>Tentar novamente</Button>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Agentes</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              Gerencie e monitore todos os agentes do sistema
            </p>
          </div>
          <Button variant="primary" size="md">
            <Plus size={20} className="mr-2" />
            Novo Agente
          </Button>
        </div>

        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <Input
              type="text"
              placeholder="Buscar agentes por nome ou ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="flex gap-2">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value as AgentStatus | 'all')}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">Todos os status</option>
              <option value="active">Ativo</option>
              <option value="idle">Ocioso</option>
              <option value="busy">Ocupado</option>
              <option value="error">Erro</option>
              <option value="offline">Offline</option>
            </select>
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value as AgentType | 'all')}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">Todos os tipos</option>
              <option value="coordinator">Coordenador</option>
              <option value="worker">Trabalhador</option>
              <option value="monitor">Monitor</option>
              <option value="analyzer">Analisador</option>
            </select>
          </div>
        </div>
      </div>

      {filteredAgents.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 dark:text-gray-400 text-lg">
            {searchTerm || statusFilter !== 'all' || typeFilter !== 'all'
              ? 'Nenhum agente encontrado com os filtros aplicados'
              : 'Nenhum agente cadastrado ainda'}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredAgents.map((agent) => (
            <Link key={agent.id} to={ROUTES.AGENT_DETAIL.replace(':agentId', agent.id)}>
              <AgentCard agent={agent} />
            </Link>
          ))}
        </div>
      )}

      <div className="mt-6 text-center text-sm text-gray-600 dark:text-gray-400">
        Mostrando {filteredAgents.length} de {agents.length} agentes
      </div>
    </div>
  );
};

export default AgentList;
