// Agent detail component with full information and actions
// Displays agent status, capabilities, messages, and controls
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Play, Pause, Trash2, RefreshCw, MessageSquare } from 'lucide-react';
import { useAgents, useAgentMessages } from '../../hooks/useAgents';
import { Button } from '../../components/common/Button';
import { Loading } from '../../components/common/Loading';
import { MessageItem } from '../../components/features/messages/MessageItem';
import { ROUTES } from '../../constants/routes';
import { formatDateTime } from '../../utils/formatters';

interface AgentDetailProps {
  agentId: string;
}

const AgentDetail: React.FC<AgentDetailProps> = ({ agentId }) => {
  const navigate = useNavigate();
  const { agents, loading, error, updateAgent, deleteAgent } = useAgents();
  const agent = agents.find(a => a.id === agentId) || null;
  const { messages, loading: messagesLoading } = useAgentMessages(agentId);
  const [activeTab, setActiveTab] = useState<'info' | 'messages' | 'config'>('info');

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <Loading size="lg" variant="spinner" />
      </div>
    );
  }

  if (error || !agent) {
    return (
      <div className="p-8 text-center">
        <p className="text-red-500 mb-4">
          {error?.message || 'Agente não encontrado'}
        </p>
        <Button onClick={() => navigate(ROUTES.AGENTS)}>Voltar para lista</Button>
      </div>
    );
  }

  const handleStart = async () => {
    await updateAgent(agentId, { status: 'active' });
  };

  const handleStop = async () => {
    await updateAgent(agentId, { status: 'inactive' });
  };

  const handleDelete = async () => {
    if (window.confirm('Tem certeza que deseja deletar este agente?')) {
      await deleteAgent(agentId);
      navigate(ROUTES.AGENTS);
    }
  };

  const statusColors: Record<string, string> = {
    active: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    idle: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200',
    busy: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    error: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    offline: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200',
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => navigate(ROUTES.AGENTS)}
          className="mb-4"
        >
          <ArrowLeft size={20} className="mr-2" />
          Voltar
        </Button>

        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              {agent.name}
            </h1>
            <div className="flex items-center gap-3">
              <span
                className={`px-3 py-1 rounded-full text-sm font-medium ${statusColors[agent.status]}`}
              >
                {agent.status}
              </span>
              <span className="text-gray-600 dark:text-gray-400 text-sm">
                Tipo: {agent.type}
              </span>
              <span className="text-gray-600 dark:text-gray-400 text-sm">
                ID: {agent.id}
              </span>
            </div>
          </div>

          <div className="flex gap-2">
            {agent.status === 'active' ? (
              <Button variant="secondary" size="md" onClick={handleStop}>
                <Pause size={20} className="mr-2" />
                Pausar
              </Button>
            ) : (
              <Button variant="primary" size="md" onClick={handleStart}>
                <Play size={20} className="mr-2" />
                Iniciar
              </Button>
            )}
            <Button variant="secondary" size="md">
              <RefreshCw size={20} />
            </Button>
            <Button variant="danger" size="md" onClick={handleDelete}>
              <Trash2 size={20} />
            </Button>
          </div>
        </div>
      </div>

      <div className="mb-6 border-b border-gray-200 dark:border-gray-700">
        <nav className="flex gap-4">
          <button
            onClick={() => setActiveTab('info')}
            className={`px-4 py-2 font-medium border-b-2 transition-colors ${activeTab === 'info'
              ? 'border-blue-500 text-blue-600 dark:text-blue-400'
              : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
              }`}
          >
            Informações
          </button>
          <button
            onClick={() => setActiveTab('messages')}
            className={`px-4 py-2 font-medium border-b-2 transition-colors ${activeTab === 'messages'
              ? 'border-blue-500 text-blue-600 dark:text-blue-400'
              : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
              }`}
          >
            Mensagens ({messages.length})
          </button>
          <button
            onClick={() => setActiveTab('config')}
            className={`px-4 py-2 font-medium border-b-2 transition-colors ${activeTab === 'config'
              ? 'border-blue-500 text-blue-600 dark:text-blue-400'
              : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
              }`}
          >
            Configuração
          </button>
        </nav>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
        {activeTab === 'info' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                Capacidades
              </h3>
              <div className="flex flex-wrap gap-2">
                {agent.capabilities.map((capability) => (
                  <span
                    key={capability}
                    className="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-sm"
                  >
                    {capability}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                Detalhes
              </h3>
              <dl className="grid grid-cols-2 gap-4">
                <div>
                  <dt className="text-sm font-medium text-gray-500 dark:text-gray-400">
                    Criado em
                  </dt>
                  <dd className="mt-1 text-sm text-gray-900 dark:text-white">
                    {formatDateTime(agent.createdAt)}
                  </dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500 dark:text-gray-400">
                    Última atualização
                  </dt>
                  <dd className="mt-1 text-sm text-gray-900 dark:text-white">
                    {formatDateTime(agent.updatedAt)}
                  </dd>
                </div>
              </dl>
            </div>
          </div>
        )}

        {activeTab === 'messages' && (
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Histórico de Mensagens
            </h3>
            {messagesLoading ? (
              <div className="flex justify-center py-8">
                <Loading size="md" variant="spinner" />
              </div>
            ) : messages.length === 0 ? (
              <div className="text-center py-8">
                <MessageSquare size={48} className="mx-auto text-gray-400 mb-2" />
                <p className="text-gray-500 dark:text-gray-400">
                  Nenhuma mensagem ainda
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                {messages.map((message) => (
                  <MessageItem key={message.id} message={message} />
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'config' && (
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Configuração
            </h3>
            <pre className="bg-gray-100 dark:bg-gray-900 p-4 rounded-lg overflow-auto text-sm">
              {JSON.stringify(agent.config, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default AgentDetail;
