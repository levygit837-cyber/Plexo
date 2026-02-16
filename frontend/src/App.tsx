import { useState } from "react";
import { ProfileList } from "./components/ProfileList";
import { useProfiles } from "./hooks/useProfiles";

function App() {
  const { profiles, loading, create, remove, start, stop } = useProfiles();
  const [showCreate, setShowCreate] = useState(false);

  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      <header className="border-b border-zinc-800 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <h1 className="text-xl font-bold">Browser Manager</h1>
          <button
            onClick={() => setShowCreate(true)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-500 transition-colors cursor-pointer"
          >
            + Criar Perfil
          </button>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        <ProfileList
          profiles={profiles}
          loading={loading}
          onStart={start}
          onStop={stop}
          onDelete={remove}
        />
      </main>
    </div>
  );
}

export default App;
