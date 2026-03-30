import { useState } from 'react'

function App() {
    const [count, setCount] = useState(0)

    return (
        <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 flex items-center justify-center">
            <div className="text-center">
                <h1 className="text-6xl font-bold text-primary-600 mb-4">
                    Plexo
                </h1>
                <p className="text-xl text-gray-600 mb-8">
                    Sistema Multi-Agentes
                </p>
                <div className="bg-white rounded-lg shadow-lg p-8 max-w-md mx-auto">
                    <p className="text-gray-700 mb-4">
                        Frontend configurado com sucesso!
                    </p>
                    <button
                        onClick={() => setCount((count) => count + 1)}
                        className="bg-primary-500 hover:bg-primary-600 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
                    >
                        Contador: {count}
                    </button>
                    <div className="mt-6 text-sm text-gray-500">
                        <p>React + TypeScript + Vite + Tailwind CSS</p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default App