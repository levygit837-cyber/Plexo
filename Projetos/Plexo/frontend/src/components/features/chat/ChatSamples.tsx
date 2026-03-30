// ChatSamples - Samples zone based on Pencil Frame Base design
const samplePrompts = [
    {
        id: 1,
        title: 'Análise de Código',
        prompt: 'Analise este código e sugira melhorias de performance',
        icon: '🔍',
    },
    {
        id: 2,
        title: 'Gerar Testes',
        prompt: 'Crie testes unitários para esta função',
        icon: '🧪',
    },
    {
        id: 3,
        title: 'Documentação',
        prompt: 'Gere documentação para este módulo',
        icon: '📝',
    },
    {
        id: 4,
        title: 'Refatoração',
        prompt: 'Sugira uma refatoração para este código',
        icon: '♻️',
    },
    {
        id: 5,
        title: 'Debug',
        prompt: 'Ajude a identificar bugs neste código',
        icon: '🐛',
    },
    {
        id: 6,
        title: 'Arquitetura',
        prompt: 'Sugira melhorias na arquitetura do projeto',
        icon: '🏗️',
    },
];

export const ChatSamples = () => {
    const handleSampleClick = (prompt: string) => {
        navigator.clipboard.writeText(prompt);
    };

    return (
        <div className="flex flex-col w-full h-full gap-4">
            <h3 className="text-sm font-medium text-gray-400">
                Prompts Rápidos
            </h3>
            <div className="flex flex-col gap-2 overflow-y-auto">
                {samplePrompts.map((sample) => (
                    <button
                        key={sample.id}
                        onClick={() => handleSampleClick(sample.prompt)}
                        className="flex items-center gap-3 p-3 bg-plexo-bg hover:bg-plexo-bg-secondary rounded-xl transition-colors text-left"
                    >
                        <span className="text-lg">{sample.icon}</span>
                        <div className="flex flex-col flex-1 min-w-0">
                            <span className="text-sm font-medium text-white">
                                {sample.title}
                            </span>
                            <span className="text-xs text-gray-500 truncate">
                                {sample.prompt}
                            </span>
                        </div>
                        <svg
                            className="w-4 h-4 text-gray-600"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                            />
                        </svg>
                    </button>
                ))}
            </div>
        </div>
    );
};
