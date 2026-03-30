# FEATURE: Multi-Agent Communication
# Classe Team para grupos de agentes

import uuid
from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field


class TeamStatus(Enum):
    """Status do time"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PAUSED = "paused"
    ARCHIVED = "archived"


@dataclass
class TeamMember:
    """Membro de um time"""
    agent_jid: str
    role: str = "member"
    joined_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Team:
    """Representa um time de agentes"""
    team_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    muc_room_jid: str = ""
    whiteboard_id: Optional[str] = None
    status: TeamStatus = TeamStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    members: List[TeamMember] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_member(self, agent_jid: str, role: str = "member") -> bool:
        """Adiciona membro ao time"""
        for member in self.members:
            if member.agent_jid == agent_jid:
                return False
        
        self.members.append(TeamMember(agent_jid=agent_jid, role=role))
        return True
    
    def remove_member(self, agent_jid: str) -> bool:
        """Remove membro do time"""
        for i, member in enumerate(self.members):
            if member.agent_jid == agent_jid:
                self.members.pop(i)
                return True
        return False
    
    def get_member(self, agent_jid: str) -> Optional[TeamMember]:
        """Retorna membro por JID"""
        for member in self.members:
            if member.agent_jid == agent_jid:
                return member
        return None
    
    def get_all_members(self) -> List[str]:
        """Retorna JIDs de todos os membros ativos"""
        return [m.agent_jid for m in self.members if m.is_active]
    
    def get_member_count(self) -> int:
        """Retorna número de membros ativos"""
        return len([m for m in self.members if m.is_active])
    
    def has_member(self, agent_jid: str) -> bool:
        """Verifica se agente é membro do time"""
        return any(m.agent_jid == agent_jid and m.is_active for m in self.members)
    
    def set_member_role(self, agent_jid: str, role: str) -> bool:
        """Define role de um membro"""
        member = self.get_member(agent_jid)
        if member:
            member.role = role
            return True
        return False
    
    def deactivate_member(self, agent_jid: str) -> bool:
        """Desativa membro sem remover"""
        member = self.get_member(agent_jid)
        if member:
            member.is_active = False
            return True
        return False
    
    def activate_member(self, agent_jid: str) -> bool:
        """Reativa membro"""
        member = self.get_member(agent_jid)
        if member:
            member.is_active = True
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "team_id": self.team_id,
            "name": self.name,
            "description": self.description,
            "muc_room_jid": self.muc_room_jid,
            "whiteboard_id": self.whiteboard_id,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "members": [
                {
                    "agent_jid": m.agent_jid,
                    "role": m.role,
                    "joined_at": m.joined_at.isoformat(),
                    "is_active": m.is_active,
                    "metadata": m.metadata
                }
                for m in self.members
            ],
            "metadata": self.metadata,
            "member_count": self.get_member_count()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Team':
        """Cria instância a partir de dicionário"""
        team = cls(
            team_id=data.get("team_id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            muc_room_jid=data.get("muc_room_jid", ""),
            whiteboard_id=data.get("whiteboard_id"),
            status=TeamStatus(data.get("status", "active")),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            metadata=data.get("metadata", {})
        )
        
        for member_data in data.get("members", []):
            team.members.append(TeamMember(
                agent_jid=member_data.get("agent_jid", ""),
                role=member_data.get("role", "member"),
                joined_at=datetime.fromisoformat(member_data.get("joined_at", datetime.now().isoformat())),
                is_active=member_data.get("is_active", True),
                metadata=member_data.get("metadata", {})
            ))
        
        return team
