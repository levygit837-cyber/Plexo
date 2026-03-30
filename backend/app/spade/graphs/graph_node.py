# FEATURE: Multi-Agent Communication
# Nó do graph de execução

import uuid
from enum import Enum
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, field


class NodeStatus(Enum):
    """Status do nó"""
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class GraphNode:
    """Nó do graph de execução"""
    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    action: str = ""
    specialist_type: str = ""
    status: NodeStatus = NodeStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)
    assigned_agent_id: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_ready(self, completed_nodes: List[str]) -> bool:
        """Verifica se nó está pronto para execução"""
        if self.status != NodeStatus.PENDING:
            return False
        
        for dep_id in self.dependencies:
            if dep_id not in completed_nodes:
                return False
        
        return True
    
    def start(self, agent_id: str) -> bool:
        """Inicia execução do nó"""
        if self.status != NodeStatus.READY:
            return False
        
        self.status = NodeStatus.RUNNING
        self.assigned_agent_id = agent_id
        self.started_at = datetime.now()
        return True
    
    def complete(self, result: Optional[Dict[str, Any]] = None) -> bool:
        """Completa execução do nó"""
        if self.status != NodeStatus.RUNNING:
            return False
        
        self.status = NodeStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result = result
        return True
    
    def fail(self, error: str) -> bool:
        """Falha na execução do nó"""
        if self.status != NodeStatus.RUNNING:
            return False
        
        self.status = NodeStatus.FAILED
        self.completed_at = datetime.now()
        self.error = error
        return True
    
    def skip(self) -> bool:
        """Pula execução do nó"""
        if self.status != NodeStatus.PENDING:
            return False
        
        self.status = NodeStatus.SKIPPED
        return True
    
    def get_duration(self) -> Optional[float]:
        """Retorna duração da execução em segundos"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "node_id": self.node_id,
            "name": self.name,
            "action": self.action,
            "specialist_type": self.specialist_type,
            "status": self.status.value,
            "dependencies": self.dependencies,
            "dependents": self.dependents,
            "assigned_agent_id": self.assigned_agent_id,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error": self.error,
            "duration": self.get_duration(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GraphNode':
        """Cria instância a partir de dicionário"""
        node = cls(
            node_id=data.get("node_id", str(uuid.uuid4())),
            name=data.get("name", ""),
            action=data.get("action", ""),
            specialist_type=data.get("specialist_type", ""),
            status=NodeStatus(data.get("status", "pending")),
            dependencies=data.get("dependencies", []),
            dependents=data.get("dependents", []),
            assigned_agent_id=data.get("assigned_agent_id"),
            result=data.get("result"),
            error=data.get("error"),
            metadata=data.get("metadata", {})
        )
        
        if data.get("started_at"):
            node.started_at = datetime.fromisoformat(data["started_at"])
        if data.get("completed_at"):
            node.completed_at = datetime.fromisoformat(data["completed_at"])
        
        return node
