# FEATURE: Multi-Agent Communication
# Comportamento de Checkpoint para agentes SPADE

import uuid
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum


class CheckpointStatus(Enum):
    """Status do checkpoint"""
    CREATED = "created"
    ACTIVE = "active"
    PAUSED = "paused"
    RESUMED = "resumed"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Checkpoint:
    """Representa um checkpoint de tarefa"""
    checkpoint_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str = ""
    agent_id: str = ""
    status: CheckpointStatus = CheckpointStatus.CREATED
    task_state: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    resumed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "checkpoint_id": self.checkpoint_id,
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "status": self.status.value,
            "task_state": self.task_state,
            "created_at": self.created_at.isoformat(),
            "resumed_at": self.resumed_at.isoformat() if self.resumed_at else None,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Checkpoint':
        """Cria instância a partir de dicionário"""
        return cls(
            checkpoint_id=data.get("checkpoint_id", str(uuid.uuid4())),
            task_id=data.get("task_id", ""),
            agent_id=data.get("agent_id", ""),
            status=CheckpointStatus(data.get("status", "created")),
            task_state=data.get("task_state", {}),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            resumed_at=datetime.fromisoformat(data["resumed_at"]) if data.get("resumed_at") else None,
            metadata=data.get("metadata", {})
        )


class CheckpointManager:
    """Gerenciador de checkpoints para agentes"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.checkpoints: Dict[str, Checkpoint] = {}
        self.current_task: Optional[Dict[str, Any]] = None
        self.task_history: List[Dict[str, Any]] = []
    
    def create_checkpoint(
        self,
        task_id: str,
        task_state: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Checkpoint:
        """Cria checkpoint do estado atual da tarefa"""
        checkpoint = Checkpoint(
            task_id=task_id,
            agent_id=self.agent_id,
            status=CheckpointStatus.CREATED,
            task_state=task_state,
            metadata=metadata or {}
        )
        
        self.checkpoints[checkpoint.checkpoint_id] = checkpoint
        
        if self.current_task and self.current_task.get("task_id") == task_id:
            self.current_task["status"] = "checkpointed"
            self.current_task["last_checkpoint"] = checkpoint.checkpoint_id
        
        return checkpoint
    
    def pause_task(self, task_id: str) -> Optional[Checkpoint]:
        """Pausa tarefa e cria checkpoint"""
        if self.current_task and self.current_task.get("task_id") == task_id:
            checkpoint = self.create_checkpoint(
                task_id=task_id,
                task_state=self.current_task.copy(),
                metadata={"reason": "paused_for_urgent_message"}
            )
            checkpoint.status = CheckpointStatus.PAUSED
            self.current_task["status"] = "paused"
            return checkpoint
        return None
    
    def resume_task(self, checkpoint_id: str) -> bool:
        """Retoma tarefa a partir de checkpoint"""
        if checkpoint_id in self.checkpoints:
            checkpoint = self.checkpoints[checkpoint_id]
            self.current_task = checkpoint.task_state.copy()
            self.current_task["status"] = "running"
            checkpoint.status = CheckpointStatus.RESUMED
            checkpoint.resumed_at = datetime.now()
            return True
        return False
    
    def get_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """Retorna checkpoint por ID"""
        return self.checkpoints.get(checkpoint_id)
    
    def get_task_checkpoints(self, task_id: str) -> List[Checkpoint]:
        """Retorna checkpoints de uma tarefa"""
        return [c for c in self.checkpoints.values() if c.task_id == task_id]
    
    def get_latest_checkpoint(self, task_id: str) -> Optional[Checkpoint]:
        """Retorna checkpoint mais recente de uma tarefa"""
        checkpoints = self.get_task_checkpoints(task_id)
        if checkpoints:
            return max(checkpoints, key=lambda c: c.created_at)
        return None
    
    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """Remove checkpoint"""
        if checkpoint_id in self.checkpoints:
            del self.checkpoints[checkpoint_id]
            return True
        return False
    
    def cleanup_old_checkpoints(self, max_age_hours: int = 24) -> int:
        """Remove checkpoints antigos"""
        now = datetime.now()
        to_delete = []
        
        for checkpoint_id, checkpoint in self.checkpoints.items():
            age_hours = (now - checkpoint.created_at).total_seconds() / 3600
            if age_hours > max_age_hours:
                to_delete.append(checkpoint_id)
        
        for checkpoint_id in to_delete:
            del self.checkpoints[checkpoint_id]
        
        return len(to_delete)
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do gerenciador"""
        active_checkpoints = sum(
            1 for c in self.checkpoints.values()
            if c.status in [CheckpointStatus.CREATED, CheckpointStatus.ACTIVE]
        )
        
        paused_checkpoints = sum(
            1 for c in self.checkpoints.values()
            if c.status == CheckpointStatus.PAUSED
        )
        
        return {
            "agent_id": self.agent_id,
            "total_checkpoints": len(self.checkpoints),
            "active_checkpoints": active_checkpoints,
            "paused_checkpoints": paused_checkpoints,
            "current_task": self.current_task.get("task_id") if self.current_task else None,
            "current_task_status": self.current_task.get("status") if self.current_task else None
        }
