export interface ParsedProxy {
  host: string;
  port: number;
  username: string | null;
  password: string | null;
}

export function parseProxy(raw: string): ParsedProxy | null {
  const trimmed = raw.trim();
  if (!trimmed) return null;

  // Format: http(s)://user:pass@host:port
  const urlMatch = trimmed.match(
    /^https?:\/\/([^:]+):([^@]+)@([^:]+):(\d+)$/
  );
  if (urlMatch) {
    return {
      host: urlMatch[3],
      port: parseInt(urlMatch[4]),
      username: urlMatch[1],
      password: urlMatch[2],
    };
  }

  // Format: user:pass@host:port
  const atMatch = trimmed.match(/^([^:]+):([^@]+)@([^:]+):(\d+)$/);
  if (atMatch) {
    return {
      host: atMatch[3],
      port: parseInt(atMatch[4]),
      username: atMatch[1],
      password: atMatch[2],
    };
  }

  const parts = trimmed.split(":");

  // Format: host:port:user:pass
  if (parts.length === 4) {
    const port = parseInt(parts[1]);
    if (!isNaN(port)) {
      return {
        host: parts[0],
        port,
        username: parts[2],
        password: parts[3],
      };
    }
  }

  // Format: host:port
  if (parts.length === 2) {
    const port = parseInt(parts[1]);
    if (!isNaN(port)) {
      return { host: parts[0], port, username: null, password: null };
    }
  }

  return null;
}
