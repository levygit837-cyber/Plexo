import type { Profile } from "../lib/api";
import { ProfileCard } from "./ProfileCard";

interface ProfileListProps {
  profiles: Profile[];
  loading: boolean;
  onStart: (id: string) => void;
  onStop: (id: string) => void;
  onDelete: (id: string) => void;
}

export function ProfileList({
  profiles,
  loading,
  onStart,
  onStop,
  onDelete,
}: ProfileListProps) {
  if (loading) {
    return (
      <div className="text-center text-zinc-500 py-12">Carregando...</div>
    );
  }

  if (profiles.length === 0) {
    return (
      <div className="text-center text-zinc-500 py-12">
        <p className="text-lg">Nenhum perfil criado</p>
        <p className="text-sm mt-1">
          Clique em "Criar Perfil" para comecar
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {profiles.map((profile) => (
        <ProfileCard
          key={profile.id}
          profile={profile}
          onStart={onStart}
          onStop={onStop}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
