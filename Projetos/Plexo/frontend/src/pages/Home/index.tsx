/**
 * Home page component with dashboard overview
 * Displays system statistics, recent agents, and tasks
 */
import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, Users, CheckSquare, MessageSquare } from 'lucide-react';
import { useAgents } from '../../hooks/useAgents';
import { useTasks } from '../../hooks/useTasks';
import { AgentCard } from '../../components/features/agents/AgentCard';
import { TaskCard } from '../../components/features/tasks/TaskCard';
import { Loading } from '../../components/common/Loading';
import { ROUTES } from '../../constants/routes';
import styles from './Home.module.css';

interface StatCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  color: string;
  link: string;
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon, color, link }) => (
  <Link to={link} className={styles.statCard} style={{ borderColor: color }}>
    <div className={styles.statIcon} style={{ color }}>
      {icon}
    </div>
    <div className={styles.statContent}>
      <h3 className={styles.statTitle}>{title}</h3>
      <p className={styles.statValue}>{value}</p>
    </div>
  </Link>
);

const Home: React.FC = () => {
  const { agents, loading: agentsLoading } = useAgents();
  const { tasks, loading: tasksLoading } = useTasks();
  const isLoading = agentsLoading || tasksLoading;

  if (isLoading) {
    return (
      <div className={styles.loadingContainer}>
        <Loading size="lg" variant="spinner" />
      </div>
    );
  }

  const recentAgents = agents.slice(0, 3);
  const recentTasks = tasks.slice(0, 3);

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1 className={styles.title}>Dashboard</h1>
        <p className={styles.subtitle}>Visão geral do sistema multi-agentes Plexo</p>
      </header>

      <section className={styles.statsGrid}>
        <StatCard
          title="Agentes Ativos"
          value={agents.filter(a => a.status === 'active').length}
          icon={<Users size={24} />}
          color="#3b82f6"
          link={ROUTES.AGENTS}
        />
        <StatCard
          title="Tarefas em Execução"
          value={tasks.filter(t => t.status === 'running').length}
          icon={<Activity size={24} />}
          color="#10b981"
          link={ROUTES.TASKS}
        />
        <StatCard
          title="Tarefas Concluídas"
          value={tasks.filter(t => t.status === 'completed').length}
          icon={<CheckSquare size={24} />}
          color="#8b5cf6"
          link={ROUTES.TASKS}
        />
        <StatCard
          title="Mensagens Trocadas"
          value={agents.reduce((acc, a) => acc + (a.metadata?.tasksCompleted as number || 0), 0)}
          icon={<MessageSquare size={24} />}
          color="#f59e0b"
          link={ROUTES.AGENTS}
        />
      </section>

      <div className={styles.contentGrid}>
        <section className={styles.section}>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>Agentes Recentes</h2>
            <Link to={ROUTES.AGENTS} className={styles.sectionLink}>
              Ver todos
            </Link>
          </div>
          <div className={styles.cardGrid}>
            {recentAgents.length > 0 ? (
              recentAgents.map((agent) => (
                <AgentCard key={agent.id} agent={agent} />
              ))
            ) : (
              <p className={styles.emptyMessage}>Nenhum agente encontrado</p>
            )}
          </div>
        </section>

        <section className={styles.section}>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>Tarefas Recentes</h2>
            <Link to={ROUTES.TASKS} className={styles.sectionLink}>
              Ver todas
            </Link>
          </div>
          <div className={styles.cardGrid}>
            {recentTasks.length > 0 ? (
              recentTasks.map((task) => (
                <TaskCard key={task.id} task={task} />
              ))
            ) : (
              <p className={styles.emptyMessage}>Nenhuma tarefa encontrada</p>
            )}
          </div>
        </section>
      </div>
    </div>
  );
};

export default Home;
