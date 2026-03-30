// Agents page component with list and detail views
// Manages agent display, filtering, and navigation
import React from 'react';
import { useParams } from 'react-router-dom';
import AgentList from './AgentList';
import AgentDetail from './AgentDetail';

const AgentsPage: React.FC = () => {
  const { agentId } = useParams<{ agentId?: string }>();

  if (agentId) {
    return <AgentDetail agentId={agentId} />;
  }

  return <AgentList />;
};

export default AgentsPage;
