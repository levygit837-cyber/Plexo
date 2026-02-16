import { useState } from "react";
import { ProxyInput } from "./ProxyInput";
import type { ProfileCreate } from "../lib/api";

const USER_AGENTS = [
  {
    label: "Chrome 120 - Windows 10",
    value:
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  },
  {
    label: "Chrome 120 - macOS",
    value:
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  },
  {
    label: "Chrome 120 - Linux",
    value:
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  },
  {
    label: "Firefox 121 - Windows",
    value:
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
  },
  {
    label: "Firefox 121 - Linux",
    value:
      "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
  },
];

const RESOLUTIONS = [
  { label: "1920x1080 (Full HD)", width: 1920, height: 1080 },
  { label: "1366x768", width: 1366, height: 768 },
  { label: "1440x900", width: 1440, height: 900 },
  { label: "1536x864", width: 1536, height: 864 },
  { label: "2560x1440 (2K)", width: 2560, height: 1440 },
];

interface CreateProfileModalProps {
  open: boolean;
  onClose: () => void;
  onCreate: (data: ProfileCreate) => Promise<void>;
}

export function CreateProfileModal({
  open,
  onClose,
  onCreate,
}: CreateProfileModalProps) {
  const [name, setName] = useState("");
  const [userAgent, setUserAgent] = useState(USER_AGENTS[0].value);
  const [customUA, setCustomUA] = useState("");
  const [useCustomUA, setUseCustomUA] = useState(false);
  const [resolution, setResolution] = useState(0);
  const [proxyData, setProxyData] = useState<{
    host: string;
    port: number;
    username: string | null;
    password: string | null;
  } | null>(null);
  const [timezone, setTimezone] = useState("");
  const [creating, setCreating] = useState(false);

  if (!open) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;

    setCreating(true);
    try {
      const selectedRes = RESOLUTIONS[resolution];
      await onCreate({
        name: name.trim(),
        user_agent: useCustomUA ? customUA : userAgent,
        screen_width: selectedRes.width,
        screen_height: selectedRes.height,
        proxy_host: proxyData?.host,
        proxy_port: proxyData?.port,
        proxy_username: proxyData?.username ?? undefined,
        proxy_password: proxyData?.password ?? undefined,
        timezone: timezone || undefined,
      });
      setName("");
      setProxyData(null);
      setTimezone("");
      onClose();
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div className="bg-zinc-900 border border-zinc-800 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between px-6 py-4 border-b border-zinc-800">
          <h2 className="text-lg font-semibold text-white">Criar Perfil</h2>
          <button
            onClick={onClose}
            className="text-zinc-500 hover:text-white transition-colors cursor-pointer text-xl"
          >
            X
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-5">
          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-1">
              Nome do Perfil
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Meu Perfil"
              required
              className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-1">
              User-Agent
            </label>
            {!useCustomUA ? (
              <select
                value={userAgent}
                onChange={(e) => setUserAgent(e.target.value)}
                className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
              >
                {USER_AGENTS.map((ua) => (
                  <option key={ua.value} value={ua.value}>
                    {ua.label}
                  </option>
                ))}
              </select>
            ) : (
              <input
                type="text"
                value={customUA}
                onChange={(e) => setCustomUA(e.target.value)}
                placeholder="Mozilla/5.0 ..."
                className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500"
              />
            )}
            <button
              type="button"
              onClick={() => setUseCustomUA(!useCustomUA)}
              className="mt-1 text-xs text-blue-400 hover:text-blue-300 cursor-pointer"
            >
              {useCustomUA ? "Usar lista" : "Customizar"}
            </button>
          </div>

          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-1">
              Resolucao de Tela
            </label>
            <select
              value={resolution}
              onChange={(e) => setResolution(Number(e.target.value))}
              className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
            >
              {RESOLUTIONS.map((res, i) => (
                <option key={res.label} value={i}>
                  {res.label}
                </option>
              ))}
            </select>
          </div>

          <ProxyInput
            onProxyChange={setProxyData}
            onTimezoneDetected={setTimezone}
          />

          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-1">
              Timezone{" "}
              <span className="text-zinc-500">(auto-detectado pela proxy)</span>
            </label>
            <input
              type="text"
              value={timezone}
              onChange={(e) => setTimezone(e.target.value)}
              placeholder="America/Sao_Paulo"
              className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2.5 bg-zinc-800 text-zinc-300 rounded-lg font-medium hover:bg-zinc-700 transition-colors cursor-pointer"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={creating || !name.trim()}
              className="flex-1 px-4 py-2.5 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-500 transition-colors disabled:opacity-50 cursor-pointer"
            >
              {creating ? "Criando..." : "Criar Perfil"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
