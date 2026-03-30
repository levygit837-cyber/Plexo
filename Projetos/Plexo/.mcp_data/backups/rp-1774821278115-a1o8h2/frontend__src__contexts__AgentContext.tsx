// Agent context provider with global agent state management | FEATURE: Multi-Agent System
import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import type { Agent, AgentStats, AgentMessage } from '../types/agent';
import { useAgents, useAgentMessages } from '../hooks/useAgents';
import { useWebSocket, useWebSocketEvent } from '../hooks/useWebSocket';

interface AgentContextType {
    agents: Agent[];
    selectedAgent: Agent | null;
    selectAgent: (agent: Agent | null) => void;
    recentMessages: AgentMessage[];
    messages: AgentMessage[];
    addMessage: (message: AgentMessage) => void;
    sendMessage: (content: string) => void;
    stats: AgentStats | null;
    isLoading: boolean;
    error: string | null;
    refreshAgents: () => Promise<void>;
    clearError: () => void;
}

interface AgentProviderProps {
    children: React.ReactNode;
}

const AgentContext = createContext<AgentContextType | undefined>(undefined);
const MAX_RECENT_MESSAGES = 100;

export const AgentProvider: React.FC<AgentProviderProps> = ({ children }) => {
    const { agents, isLoading, error, refresh } = useAgents();
    const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
    const [recentMessages, setRecentMessages] = useState<AgentMessage[]>([]);
    const [stats, setStats] = useState<AgentStats | null>(null);
    const { messages: agentMessages, sendMessage: sendAgentMessage } = useAgentMessages(selectedAgent?.id || '');
    const { send } = useWebSocket();

    const selectAgent = useCallback((agent: Agent | null) => {
        setSelectedAgent(agent);
        if (agent) {
            setRecentMessages([]);
        }
    }, []);

    const addMessage = useCallback((message: AgentMessage) => {
        setRecentMessages(prev => {
            const newMessages = [...prev, message];
            if (newMessages.length > MAX_RECENT_MESSAGES) {
                return newMessages.slice(-MAX_RECENT_MESSAGES);
            }
            return newMessages;
        });
    }, []);

    const sendMessage = useCallback((content: string) => {
        if (!selectedAgent || !content.trim()) return;

        const message: AgentMessage = {
            id: Date.now().toString(),
            content: content.trim(),
            sender: 'user',
            timestamp: new Date().toISOString(),
            agentId: selectedAgent.id,
        };

        addMessage(message);

        if (sendAgentMessage) {
            sendAgentMessage(content, 'user');
        } else {
            send({
                type: 'message',
                payload: {
                    agentId: selectedAgent.id,
                    content: content.trim(),
                },
            });
        }
    }, [selectedAgent, addMessage, sendAgentMessage, send]);

    const clearError = useCallback(() => {
        // Error is managed by useAgents hook
    }, []);

    useWebSocketEvent('agent_message', (data) => {
        if (data.agentId === selectedAgent?.id) {
            addMessage(data.message);
        }
    });

    useEffect(() => {
        if (agents.length > 0 && !selectedAgent) {
            const activeAgent = agents.find(a => a.status === 'active') || agents[0];
            setSelectedAgent(activeAgent);
        }
    }, [agents, selectedAgent]);

    useEffect(() => {
        const calculateStats = () => {
            const activeAgents = agents.filter(a => a.status === 'active').length;
            const totalAgents = agents.length;
            const totalMessages = recentMessages.length;

            setStats({
                totalAgents,
                activeAgents,
                totalMessages,
                averageResponseTime: 0,
                successRate: 100,
            });
        };

        calculateStats();
    }, [agents, recentMessages]);

    const value: AgentContextType = {
        agents,
        selectedAgent,
        selectAgent,
        recentMessages,
        messages: agentMessages || recentMessages,
        addMessage,
        sendMessage,
        stats,
        isLoading,
        error,
        refreshAgents: refresh,
        clearError,
    };

    return (
        <AgentContext.Provider value={value}>
            {children}
        </AgentContext.Provider>
    );
};

export const useAgentContext = (): AgentContextType => {
    const context = useContext(AgentContext);
    if (context === undefined) {
        throw new Error('useAgentContext must be used within an AgentProvider');
    }
    return context;
};
