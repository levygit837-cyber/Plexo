// ChatMessages - Messages zone based on Pencil Frame Base design
import { useAgentContext } from '../../../contexts/AgentContext';
import type { AgentMessage } from '../../../types/agent';

export const ChatMessages = () => {
    const { messages, selectedAgent } = useAgentContext();

    const formatTime = (date: string | Date) => {
        const d = new Date(date);
        return d.toLocaleTimeString('pt-BR', {
            hour: '2-digit',
            minute: '2-digit',
        });
    };

    return (
        <div className="flex flex-col flex-1 h-full bg-plexo-bg-secondary rounded-2xl p-5 gap-4">
            {/* Header */}
            <div className="flex items-center gap-3 pb-4 border-b border-plexo-bg-tertiary">
                <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
                    <span className="text-sm font-medium text-white">
                        {selectedAgent?.name?.charAt(0).toUpperCase() || 'A'}
                    </span>
                </div>
                <div className="flex flex-col">
                    <span className="text-sm font-medium text-white">
                        {selectedAgent?.name || 'Selecione um agente'}
                    </span>
                    <span className="text-xs text-gray-400">
                        {selectedAgent?.status === 'active'
                            ? 'Online'
                            : selectedAgent?.status === 'busy'
                                ? 'Ocupado'
                                : 'Offline'}
                    </span>
                </div>
            </div>

            {/* Messages Area */}
            <div className="flex flex-col flex-1 overflow-y-auto gap-4">
                {messages?.map((message: AgentMessage) => (
                    <div
                        key={message.id}
                        className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div
                            className={`max-w-[80%] rounded-2xl px-4 py-3 ${message.sender === 'user'
                                ? 'bg-blue-600 text-white'
                                : 'bg-plexo-bg-tertiary text-gray-100'
                                }`}
                        >
                            <p className="text-sm whitespace-pre-wrap">
                                {message.content}
                            </p>
                            <span
                                className={`text-xs mt-2 block ${message.sender === 'user'
                                    ? 'text-blue-200'
                                    : 'text-gray-500'
                                    }`}
                            >
                                {formatTime(message.timestamp || message.created_at)}
                            </span>
                        </div>
                    </div>
                ))}

                {(!messages || messages.length === 0) && (
                    <div className="flex flex-col items-center justify-center flex-1 text-gray-500">
                        <svg
                            className="w-16 h-16 mb-4"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={1.5}
                                d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                            />
                        </svg>
                        <p className="text-sm">Nenhuma mensagem ainda</p>
                        <p className="text-xs text-gray-600 mt-1">
                            Inicie uma conversa com um agente
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
};
