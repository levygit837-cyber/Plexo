import { useState, useCallback } from "react";
import { parseProxy } from "../lib/proxyParser";
import { validateProxy, type ProxyCheckResult } from "../lib/api";
import { ProxyStatus } from "./ProxyStatus";

interface ProxyInputProps {
  onProxyChange: (data: {
    host: string;
    port: number;
    username: string | null;
    password: string | null;
  }) => void;
  onTimezoneDetected: (timezone: string) => void;
}

export function ProxyInput({
  onProxyChange,
  onTimezoneDetected,
}: ProxyInputProps) {
  const [rawProxy, setRawProxy] = useState("");
  const [parsedHost, setParsedHost] = useState("");
  const [parsedPort, setParsedPort] = useState("");
  const [parsedUser, setParsedUser] = useState("");
  const [parsedPass, setParsedPass] = useState("");
  const [checkResult, setCheckResult] = useState<ProxyCheckResult | null>(
    null
  );
  const [checking, setChecking] = useState(false);

  const handlePaste = useCallback(
    (e: React.ClipboardEvent<HTMLInputElement>) => {
      const text = e.clipboardData.getData("text");
      const parsed = parseProxy(text);
      if (parsed) {
        e.preventDefault();
        setRawProxy(text.trim());
        setParsedHost(parsed.host);
        setParsedPort(String(parsed.port));
        setParsedUser(parsed.username || "");
        setParsedPass(parsed.password || "");
        setCheckResult(null);
        onProxyChange(parsed);
      }
    },
    [onProxyChange]
  );

  const handleCheck = async () => {
    if (!parsedHost || !parsedPort) return;
    setChecking(true);
    setCheckResult(null);
    try {
      const result = await validateProxy({
        host: parsedHost,
        port: parseInt(parsedPort),
        username: parsedUser || undefined,
        password: parsedPass || undefined,
      });
      setCheckResult(result);
      if (result.valid && result.timezone) {
        onTimezoneDetected(result.timezone);
      }
    } finally {
      setChecking(false);
    }
  };

  return (
    <div className="space-y-3">
      <div>
        <label className="block text-sm font-medium text-zinc-300 mb-1">
          Proxy (cole com Ctrl+V)
        </label>
        <input
          type="text"
          value={rawProxy}
          onChange={(e) => setRawProxy(e.target.value)}
          onPaste={handlePaste}
          placeholder="host:port:user:pass"
          className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500"
        />
      </div>

      {parsedHost && (
        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className="block text-xs text-zinc-500 mb-1">Host</label>
            <input
              type="text"
              value={parsedHost}
              onChange={(e) => {
                setParsedHost(e.target.value);
                onProxyChange({
                  host: e.target.value,
                  port: parseInt(parsedPort) || 0,
                  username: parsedUser || null,
                  password: parsedPass || null,
                });
              }}
              className="w-full px-2 py-1.5 bg-zinc-800/50 border border-zinc-700/50 rounded text-sm text-zinc-300"
            />
          </div>
          <div>
            <label className="block text-xs text-zinc-500 mb-1">Porta</label>
            <input
              type="text"
              value={parsedPort}
              onChange={(e) => {
                setParsedPort(e.target.value);
                onProxyChange({
                  host: parsedHost,
                  port: parseInt(e.target.value) || 0,
                  username: parsedUser || null,
                  password: parsedPass || null,
                });
              }}
              className="w-full px-2 py-1.5 bg-zinc-800/50 border border-zinc-700/50 rounded text-sm text-zinc-300"
            />
          </div>
          <div>
            <label className="block text-xs text-zinc-500 mb-1">
              Usuario
            </label>
            <input
              type="text"
              value={parsedUser}
              onChange={(e) => {
                setParsedUser(e.target.value);
                onProxyChange({
                  host: parsedHost,
                  port: parseInt(parsedPort) || 0,
                  username: e.target.value || null,
                  password: parsedPass || null,
                });
              }}
              className="w-full px-2 py-1.5 bg-zinc-800/50 border border-zinc-700/50 rounded text-sm text-zinc-300"
            />
          </div>
          <div>
            <label className="block text-xs text-zinc-500 mb-1">Senha</label>
            <input
              type="text"
              value={parsedPass}
              onChange={(e) => {
                setParsedPass(e.target.value);
                onProxyChange({
                  host: parsedHost,
                  port: parseInt(parsedPort) || 0,
                  username: parsedUser || null,
                  password: e.target.value || null,
                });
              }}
              className="w-full px-2 py-1.5 bg-zinc-800/50 border border-zinc-700/50 rounded text-sm text-zinc-300"
            />
          </div>
        </div>
      )}

      {parsedHost && (
        <button
          onClick={handleCheck}
          disabled={checking}
          className="w-full px-3 py-2 bg-zinc-800 text-zinc-300 rounded-lg text-sm font-medium hover:bg-zinc-700 transition-colors disabled:opacity-50 cursor-pointer"
        >
          {checking ? "Verificando..." : "Verificar Proxy"}
        </button>
      )}

      <ProxyStatus result={checkResult} loading={checking} />
    </div>
  );
}
