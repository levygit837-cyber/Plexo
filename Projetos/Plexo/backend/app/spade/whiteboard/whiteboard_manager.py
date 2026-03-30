# FEATURE: Multi-Agent Communication
# Gerenciador de whiteboards

import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from .whiteboard import Whiteboard, WhiteboardStatus
from .whiteboard_entry import WhiteboardEntry, ActionType


class WhiteboardManager:
    """Gerenciador de whiteboards"""
    
    def __init__(self):
        self.whiteboards: Dict[str, Whiteboard] = {}
    
    def create_whiteboard(
        self,
        name: str,
        owner_id: str,
        description: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Whiteboard:
        """Cria novo whiteboard"""
        whiteboard = Whiteboard(
            name=name,
            owner_id=owner_id,
            description=description,
            metadata=metadata or {}
        )
        
        self.whiteboards[whiteboard.whiteboard_id] = whiteboard
        return whiteboard
    
    def get_whiteboard(self, whiteboard_id: str) -> Optional[Whiteboard]:
        """Retorna whiteboard por ID"""
        return self.whiteboards.get(whiteboard_id)
    
    def get_whiteboard_by_name(self, name: str) -> Optional[Whiteboard]:
        """Retorna whiteboard por nome"""
        for wb in self.whiteboards.values():
            if wb.name == name:
                return wb
        return None
    
    def get_all_whiteboards(self) -> List[Whiteboard]:
        """Retorna todos os whiteboards"""
        return list(self.whiteboards.values())
    
    def get_active_whiteboards(self) -> List[Whiteboard]:
        """Retorna whiteboards ativos"""
        return [wb for wb in self.whiteboards.values() if wb.status == WhiteboardStatus.ACTIVE]
    
    def get_owner_whiteboards(self, owner_id: str) -> List[Whiteboard]:
        """Retorna whiteboards de um dono"""
        return [wb for wb in self.whiteboards.values() if wb.owner_id == owner_id]
    
    def delete_whiteboard(self, whiteboard_id: str) -> bool:
        """Remove whiteboard"""
        if whiteboard_id in self.whiteboards:
            del self.whiteboards[whiteboard_id]
            return True
        return False
    
    def update_whiteboard(
        self,
        whiteboard_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Whiteboard]:
        """Atualiza whiteboard"""
        whiteboard = self.get_whiteboard(whiteboard_id)
        if not whiteboard:
            return None
        
        if name is not None:
            whiteboard.name = name
        if description is not None:
            whiteboard.description = description
        if metadata is not None:
            whiteboard.metadata.update(metadata)
        
        return whiteboard
    
    def add_entry(
        self,
        whiteboard_id: str,
        author_id: str,
        action_type: ActionType,
        content: str,
        line_number: Optional[int] = None,
        file_path: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[WhiteboardEntry]:
        """Adiciona entrada ao whiteboard"""
        whiteboard = self.get_whiteboard(whiteboard_id)
        if not whiteboard:
            return None
        
        entry = WhiteboardEntry(
            whiteboard_id=whiteboard_id,
            author_id=author_id,
            action_type=action_type,
            content=content,
            line_number=line_number,
            file_path=file_path,
            metadata=metadata or {}
        )
        
        if whiteboard.add_entry(entry):
            return entry
        return None
    
    def add_function_entry(
        self,
        whiteboard_id: str,
        author_id: str,
        function_name: str,
        description: str,
        line_number: Optional[int] = None,
        file_path: Optional[str] = None
    ) -> Optional[WhiteboardEntry]:
        """Adiciona entrada de criação de função"""
        entry = WhiteboardEntry.create_function_entry(
            whiteboard_id=whiteboard_id,
            author_id=author_id,
            function_name=function_name,
            description=description,
            line_number=line_number,
            file_path=file_path
        )
        
        whiteboard = self.get_whiteboard(whiteboard_id)
        if whiteboard and whiteboard.add_entry(entry):
            return entry
        return None
    
    def add_class_entry(
        self,
        whiteboard_id: str,
        author_id: str,
        class_name: str,
        description: str,
        line_number: Optional[int] = None,
        file_path: Optional[str] = None
    ) -> Optional[WhiteboardEntry]:
        """Adiciona entrada de criação de classe"""
        entry = WhiteboardEntry.create_class_entry(
            whiteboard_id=whiteboard_id,
            author_id=author_id,
            class_name=class_name,
            description=description,
            line_number=line_number,
            file_path=file_path
        )
        
        whiteboard = self.get_whiteboard(whiteboard_id)
        if whiteboard and whiteboard.add_entry(entry):
            return entry
        return None
    
    def add_test_entry(
        self,
        whiteboard_id: str,
        author_id: str,
        test_name: str,
        passed: bool,
        details: str = ""
    ) -> Optional[WhiteboardEntry]:
        """Adiciona entrada de teste"""
        entry = WhiteboardEntry.create_test_entry(
            whiteboard_id=whiteboard_id,
            author_id=author_id,
            test_name=test_name,
            passed=passed,
            details=details
        )
        
        whiteboard = self.get_whiteboard(whiteboard_id)
        if whiteboard and whiteboard.add_entry(entry):
            return entry
        return None
    
    def add_error_entry(
        self,
        whiteboard_id: str,
        author_id: str,
        error_message: str,
        file_path: Optional[str] = None,
        line_number: Optional[int] = None
    ) -> Optional[WhiteboardEntry]:
        """Adiciona entrada de erro"""
        entry = WhiteboardEntry.create_error_entry(
            whiteboard_id=whiteboard_id,
            author_id=author_id,
            error_message=error_message,
            file_path=file_path,
            line_number=line_number
        )
        
        whiteboard = self.get_whiteboard(whiteboard_id)
        if whiteboard and whiteboard.add_entry(entry):
            return entry
        return None
    
    def get_entries(
        self,
        whiteboard_id: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Retorna entradas do whiteboard"""
        whiteboard = self.get_whiteboard(whiteboard_id)
        if whiteboard:
            return [e.to_dict() for e in whiteboard.get_entries(limit)]
        return []
    
    def search_entries(
        self,
        whiteboard_id: str,
        query: str
    ) -> List[Dict[str, Any]]:
        """Busca entradas no whiteboard"""
        whiteboard = self.get_whiteboard(whiteboard_id)
        if whiteboard:
            return [e.to_dict() for e in whiteboard.search_entries(query)]
        return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do gerenciador"""
        total_entries = sum(len(wb.entries) for wb in self.whiteboards.values())
        active_whiteboards = len(self.get_active_whiteboards())
        
        return {
            "total_whiteboards": len(self.whiteboards),
            "active_whiteboards": active_whiteboards,
            "total_entries": total_entries,
            "average_entries_per_whiteboard": total_entries / len(self.whiteboards) if self.whiteboards else 0
        }
