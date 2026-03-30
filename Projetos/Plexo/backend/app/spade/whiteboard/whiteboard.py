# FEATURE: Multi-Agent Communication
# Quadro branco compartilhado para monitoramento

import uuid
from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
from .whiteboard_entry import WhiteboardEntry, ActionType


class WhiteboardStatus(Enum):
    """Status do whiteboard"""
    ACTIVE = "active"
    ARCHIVED = "archived"
    LOCKED = "locked"


@dataclass
class Whiteboard:
    """Quadro branco compartilhado para monitoramento"""
    whiteboard_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    status: WhiteboardStatus = WhiteboardStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    owner_id: str = ""
    entries: List[WhiteboardEntry] = field(default_factory=list)
    max_entries: int = 10000
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_entry(self, entry: WhiteboardEntry) -> bool:
        """Adiciona entrada ao whiteboard"""
        if self.status == WhiteboardStatus.LOCKED:
            return False
        
        entry.whiteboard_id = self.whiteboard_id
        self.entries.append(entry)
        
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[-self.max_entries:]
        
        return True
    
    def get_entries(self, limit: int = 100) -> List[WhiteboardEntry]:
        """Retorna entradas mais recentes"""
        return self.entries[-limit:]
    
    def get_entries_by_author(self, author_id: str) -> List[WhiteboardEntry]:
        """Retorna entradas de um autor"""
        return [e for e in self.entries if e.author_id == author_id]
    
    def get_entries_by_type(self, action_type: ActionType) -> List[WhiteboardEntry]:
        """Retorna entradas por tipo de ação"""
        return [e for e in self.entries if e.action_type == action_type]
    
    def get_entries_by_file(self, file_path: str) -> List[WhiteboardEntry]:
        """Retorna entradas relacionadas a um arquivo"""
        return [e for e in self.entries if e.file_path == file_path]
    
    def search_entries(self, query: str) -> List[WhiteboardEntry]:
        """Busca entradas por conteúdo"""
        query_lower = query.lower()
        return [e for e in self.entries if query_lower in e.content.lower()]
    
    def get_recent_entries(self, minutes: int = 60) -> List[WhiteboardEntry]:
        """Retorna entradas dos últimos X minutos"""
        cutoff = datetime.now().timestamp() - (minutes * 60)
        return [
            e for e in self.entries
            if e.timestamp.timestamp() > cutoff
        ]
    
    def get_entry(self, entry_id: str) -> Optional[WhiteboardEntry]:
        """Retorna entrada por ID"""
        for entry in self.entries:
            if entry.entry_id == entry_id:
                return entry
        return None
    
    def delete_entry(self, entry_id: str) -> bool:
        """Remove entrada"""
        for i, entry in enumerate(self.entries):
            if entry.entry_id == entry_id:
                self.entries.pop(i)
                return True
        return False
    
    def clear_entries(self) -> int:
        """Limpa todas as entradas"""
        count = len(self.entries)
        self.entries = []
        return count
    
    def archive(self) -> bool:
        """Arquiva whiteboard"""
        if self.status == WhiteboardStatus.ACTIVE:
            self.status = WhiteboardStatus.ARCHIVED
            return True
        return False
    
    def lock(self) -> bool:
        """Bloqueia whiteboard para escrita"""
        if self.status == WhiteboardStatus.ACTIVE:
            self.status = WhiteboardStatus.LOCKED
            return True
        return False
    
    def unlock(self) -> bool:
        """Desbloqueia whiteboard"""
        if self.status == WhiteboardStatus.LOCKED:
            self.status = WhiteboardStatus.ACTIVE
            return True
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do whiteboard"""
        action_counts = {}
        for entry in self.entries:
            action_type = entry.action_type.value
            action_counts[action_type] = action_counts.get(action_type, 0) + 1
        
        authors = set(e.author_id for e in self.entries)
        files = set(e.file_path for e in self.entries if e.file_path)
        
        return {
            "whiteboard_id": self.whiteboard_id,
            "name": self.name,
            "status": self.status.value,
            "total_entries": len(self.entries),
            "unique_authors": len(authors),
            "unique_files": len(files),
            "action_counts": action_counts,
            "created_at": self.created_at.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "whiteboard_id": self.whiteboard_id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "owner_id": self.owner_id,
            "entries": [e.to_dict() for e in self.entries],
            "max_entries": self.max_entries,
            "metadata": self.metadata,
            "stats": self.get_stats()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Whiteboard':
        """Cria instância a partir de dicionário"""
        whiteboard = cls(
            whiteboard_id=data.get("whiteboard_id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            status=WhiteboardStatus(data.get("status", "active")),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            owner_id=data.get("owner_id", ""),
            max_entries=data.get("max_entries", 10000),
            metadata=data.get("metadata", {})
        )
        
        for entry_data in data.get("entries", []):
            whiteboard.entries.append(WhiteboardEntry.from_dict(entry_data))
        
        return whiteboard
