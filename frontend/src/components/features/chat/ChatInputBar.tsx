// ChatInputBar - Input bar zone based on Pencil Frame Base design
import { useState, useRef, useEffect } from 'react';
import { useAgentContext } from '../../../contexts/AgentContext';

export const ChatInputBar = () => {
    const [message, setMessage] = useState('');
    const textareaRef = useRef<HTMLTextAreaElement>(null);
    const { selectedAgent, sendMessage } = useAgentContext();

    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
        }
    }, [message]);

    const handleSend = () => {
        if (!message.trim() || !selectedAgent) return;
        sendMessage(message.trim());
        setMessage('');
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="flex items-center h-[120px] bg-plexo-bg-secondary rounded-2xl p-5 gap-4">
            {/* Composer */}
            <div className="flex items-center flex-1 h-full bg-plexo-bg-composer rounded-[18px] px-[18px] gap-4">
                {/* Attachment Button */}
                <button className="p-2 text-gray-500 hover:text-gray-300 transition-colors">
                    <svg
                        className="w-5 h-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"
                        />
                    </svg>
                </button>

                {/* Textarea */}
                <textarea
                    ref={textareaRef}
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder={
                        selectedAgent
                            ? `Mensagem para ${selectedAgent.name}...`
                            : 'Selecione um agente para começar...'
                    }
                    disabled={!selectedAgent}
                    className="flex-1 bg-transparent text-white placeholder-gray-500 text-sm resize-none focus:outline-none disabled:opacity-50 min-h-[40px] max-h-[80px]"
                    rows={1}
                />

                {/* Emoji Button */}
                <button className="p-2 text-gray-500 hover:text-gray-300 transition-colors">
                    <svg
                        className="w-5 h-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                    </svg>
                </button>
            </div>

            {/* Send Button */}
            <button
                onClick={handleSend}
                disabled={!message.trim() || !selectedAgent}
                className="flex items-center justify-center w-12 h-12 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded-xl transition-colors"
            >
                <svg
                    className="w-5 h-5 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                    />
                </svg>
            </button>
        </div>
    );
};
