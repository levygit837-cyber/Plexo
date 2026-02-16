import type { Profile } from "../lib/api";

interface ProfileCardProps {
  profile: Profile;
  onStart: (id: string) => void;
  onStop: (id: string) => void;
  onDelete: (id: string) => void;
}

export function ProfileCard({
  profile,
  onStart,
  onStop,
  onDelete,
}: ProfileCardProps) {
  const isRunning = profile.status === "running";

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-5 flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white">{profile.name}</h3>
        <span
          className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium ${
            isRunning
              ? "bg-emerald-500/10 text-emerald-400"
              : "bg-zinc-700/50 text-zinc-400"
          }`}
        >
          <span
            className={`w-1.5 h-1.5 rounded-full ${
              isRunning ? "bg-emerald-400" : "bg-zinc-500"
            }`}
          />
          {isRunning ? "Rodando" : "Parado"}
        </span>
      </div>

      <div className="text-sm text-zinc-400 space-y-1">
        {profile.proxy_host && (
          <p>
            Proxy: {profile.proxy_host}:{profile.proxy_port}
          </p>
        )}
        <p>
          Tela: {profile.screen_width}x{profile.screen_height}
        </p>
        {profile.timezone && <p>Timezone: {profile.timezone}</p>}
      </div>

      <div className="flex gap-2 mt-auto pt-2">
        {isRunning ? (
          <button
            onClick={() => onStop(profile.id)}
            className="flex-1 px-3 py-2 bg-red-500/10 text-red-400 rounded-lg text-sm font-medium hover:bg-red-500/20 transition-colors cursor-pointer"
          >
            Parar
          </button>
        ) : (
          <button
            onClick={() => onStart(profile.id)}
            className="flex-1 px-3 py-2 bg-emerald-500/10 text-emerald-400 rounded-lg text-sm font-medium hover:bg-emerald-500/20 transition-colors cursor-pointer"
          >
            Abrir
          </button>
        )}
        <button
          onClick={() => onDelete(profile.id)}
          disabled={isRunning}
          className="px-3 py-2 bg-zinc-800 text-zinc-400 rounded-lg text-sm font-medium hover:bg-zinc-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
        >
          Deletar
        </button>
      </div>
    </div>
  );
}
