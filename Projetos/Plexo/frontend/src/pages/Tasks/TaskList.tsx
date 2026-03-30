// Task list component with filtering and search
// FEATURE: Task Management
import React, { useState, useMemo } from 'react';
import { Plus } from 'lucide-react';
import { useTasks } from '../../hooks/useTasks';
import { TaskCard } from '../../components/features/tasks/TaskCard';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { Loading } from '../../components/common/Loading';
import type { TaskStatus } from '../../types/task';
import type { Priority } from '../../types/common';

const TaskList: React.FC = () => {
  const { tasks, loading, error } = useTasks();
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<TaskStatus | 'all'>('all');
  const [priorityFilter, setPriorityFilter] = useState<Priority | 'all'>('all');

  const filteredTasks = useMemo(() => {
    return tasks.filter((task) => {
      const matchesSearch = task.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (task.payload && JSON.stringify(task.payload).toLowerCase().includes(searchTerm.toLowerCase()));
      const matchesStatus = statusFilter === 'all' || task.status === statusFilter;
      const matchesPriority = priorityFilter === 'all' || task.priority === priorityFilter;
      return matchesSearch && matchesStatus && matchesPriority;
    });
  }, [tasks, searchTerm, statusFilter, priorityFilter]);

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
        <p className="text-red-500 mb-4">Erro ao carregar tarefas: {error.message}</p>
        <Button onClick={() => window.location.reload()}>Tentar novamente</Button>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Tarefas</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              Gerencie e monitore todas as tarefas do sistema
            </p>
          </div>
          <Button variant="primary" size="md">
            <Plus size={20} className="mr-2" />
            Nova Tarefa
          </Button>
        </div>

        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <Input
              type="text"
              placeholder="Buscar tarefas por ID ou conteúdo..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="flex gap-2">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value as TaskStatus | 'all')}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">Todos os status</option>
              <option value="pending">Pendente</option>
              <option value="running">Em execução</option>
              <option value="completed">Concluída</option>
              <option value="failed">Falhou</option>
              <option value="cancelled">Cancelada</option>
            </select>
            <select
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value as Priority | 'all')}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">Todas as prioridades</option>
              <option value="low">Baixa</option>
              <option value="medium">Média</option>
              <option value="high">Alta</option>
              <option value="urgent">Urgente</option>
            </select>
          </div>
        </div>
      </div>

      {filteredTasks.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 dark:text-gray-400 text-lg">
            {searchTerm || statusFilter !== 'all' || priorityFilter !== 'all'
              ? 'Nenhuma tarefa encontrada com os filtros aplicados'
              : 'Nenhuma tarefa cadastrada ainda'}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredTasks.map((task) => (
            <TaskCard key={task.id} task={task} />
          ))}
        </div>
      )}

      <div className="mt-6 text-center text-sm text-gray-600 dark:text-gray-400">
        Mostrando {filteredTasks.length} de {tasks.length} tarefas
      </div>
    </div>
  );
};

export default TaskList;
