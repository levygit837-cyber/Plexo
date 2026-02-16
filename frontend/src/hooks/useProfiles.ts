import { useCallback, useEffect, useState } from "react";
import {
  fetchProfiles,
  createProfile,
  deleteProfile,
  startProfile,
  stopProfile,
  type Profile,
  type ProfileCreate,
} from "../lib/api";

export function useProfiles() {
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const data = await fetchProfiles();
      setProfiles(data);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const create = async (data: ProfileCreate) => {
    const profile = await createProfile(data);
    setProfiles((prev) => [...prev, profile]);
    return profile;
  };

  const remove = async (id: string) => {
    await deleteProfile(id);
    setProfiles((prev) => prev.filter((p) => p.id !== id));
  };

  const start = async (id: string) => {
    const updated = await startProfile(id);
    setProfiles((prev) => prev.map((p) => (p.id === id ? updated : p)));
  };

  const stop = async (id: string) => {
    const updated = await stopProfile(id);
    setProfiles((prev) => prev.map((p) => (p.id === id ? updated : p)));
  };

  return { profiles, loading, refresh, create, remove, start, stop };
}
