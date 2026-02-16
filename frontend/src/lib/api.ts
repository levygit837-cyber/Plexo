const BASE_URL = "/api";

export interface Profile {
  id: string;
  name: string;
  user_agent: string | null;
  screen_width: number;
  screen_height: number;
  proxy_host: string | null;
  proxy_port: number | null;
  proxy_username: string | null;
  proxy_password: string | null;
  timezone: string | null;
  status: "stopped" | "running";
  created_at: string;
}

export interface ProfileCreate {
  name: string;
  user_agent?: string;
  screen_width?: number;
  screen_height?: number;
  proxy_host?: string;
  proxy_port?: number;
  proxy_username?: string;
  proxy_password?: string;
  timezone?: string;
}

export interface ProxyCheckResult {
  valid: boolean;
  ip: string | null;
  city: string | null;
  country: string | null;
  timezone: string | null;
  error: string | null;
}

export interface ParsedProxy {
  host: string;
  port: number;
  username: string | null;
  password: string | null;
}

export async function fetchProfiles(): Promise<Profile[]> {
  const res = await fetch(`${BASE_URL}/profiles`);
  return res.json();
}

export async function createProfile(data: ProfileCreate): Promise<Profile> {
  const res = await fetch(`${BASE_URL}/profiles`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function deleteProfile(id: string): Promise<void> {
  await fetch(`${BASE_URL}/profiles/${id}`, { method: "DELETE" });
}

export async function startProfile(id: string): Promise<Profile> {
  const res = await fetch(`${BASE_URL}/profiles/${id}/start`, {
    method: "POST",
  });
  return res.json();
}

export async function stopProfile(id: string): Promise<Profile> {
  const res = await fetch(`${BASE_URL}/profiles/${id}/stop`, {
    method: "POST",
  });
  return res.json();
}

export async function parseProxy(raw: string): Promise<ParsedProxy> {
  const res = await fetch(`${BASE_URL}/proxy/parse`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ raw }),
  });
  if (!res.ok) throw new Error("Failed to parse proxy");
  return res.json();
}

export async function validateProxy(data: {
  host: string;
  port: number;
  username?: string;
  password?: string;
}): Promise<ProxyCheckResult> {
  const res = await fetch(`${BASE_URL}/proxy/validate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}
