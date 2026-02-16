import type { ProxyCheckResult } from "../lib/api";

interface ProxyStatusProps {
  result: ProxyCheckResult | null;
  loading: boolean;
}

export function ProxyStatus({ result, loading }: ProxyStatusProps) {
  if (loading) {
    return (
      <div className="flex items-center gap-2 px-3 py-2 bg-zinc-800 rounded-lg text-sm text-zinc-400">
        <div className="w-4 h-4 border-2 border-zinc-500 border-t-blue-400 rounded-full animate-spin" />
        Verificando proxy...
      </div>
    );
  }

  if (!result) return null;

  if (result.valid) {
    return (
      <div className="px-3 py-2 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-sm">
        <div className="flex items-center gap-2 text-emerald-400 font-medium">
          <span>Proxy valida</span>
        </div>
        <div className="text-zinc-400 mt-1 space-y-0.5">
          <p>IP: {result.ip}</p>
          <p>
            Local: {result.city}, {result.country}
          </p>
          <p>Timezone: {result.timezone}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="px-3 py-2 bg-red-500/10 border border-red-500/20 rounded-lg text-sm">
      <div className="flex items-center gap-2 text-red-400 font-medium">
        <span>Proxy invalida</span>
      </div>
      {result.error && (
        <p className="text-zinc-400 mt-1">{result.error}</p>
      )}
    </div>
  );
}
