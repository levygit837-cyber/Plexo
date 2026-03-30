# FEATURE: Multi-Agent Communication
# Graph de execução de tarefas

import uuid
from enum import Enum
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, field
from .graph_node import GraphNode, NodeStatus


class GraphStatus(Enum):
    """Status do graph"""
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class AgentGraph:
    """Graph de execução de tarefas"""
    graph_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    status: GraphStatus = GraphStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    nodes: Dict[str, GraphNode] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_node(self, node: GraphNode) -> bool:
        """Adiciona nó ao graph"""
        if node.node_id in self.nodes:
            return False
        
        self.nodes[node.node_id] = node
        return True
    
    def remove_node(self, node_id: str) -> bool:
        """Remove nó do graph"""
        if node_id not in self.nodes:
            return False
        
        node = self.nodes[node_id]
        
        for dep_id in node.dependencies:
            if dep_id in self.nodes:
                self.nodes[dep_id].dependents.remove(node_id)
        
        for dep_id in node.dependents:
            if dep_id in self.nodes:
                self.nodes[dep_id].dependencies.remove(node_id)
        
        del self.nodes[node_id]
        return True
    
    def get_node(self, node_id: str) -> Optional[GraphNode]:
        """Retorna nó por ID"""
        return self.nodes.get(node_id)
    
    def get_ready_nodes(self) -> List[GraphNode]:
        """Retorna nós prontos para execução"""
        completed = [
            nid for nid, n in self.nodes.items()
            if n.status == NodeStatus.COMPLETED
        ]
        
        return [
            node for node in self.nodes.values()
            if node.is_ready(completed)
        ]
    
    def get_running_nodes(self) -> List[GraphNode]:
        """Retorna nós em execução"""
        return [
            node for node in self.nodes.values()
            if node.status == NodeStatus.RUNNING
        ]
    
    def get_completed_nodes(self) -> List[GraphNode]:
        """Retorna nós completados"""
        return [
            node for node in self.nodes.values()
            if node.status == NodeStatus.COMPLETED
        ]
    
    def get_failed_nodes(self) -> List[GraphNode]:
        """Retorna nós falhados"""
        return [
            node for node in self.nodes.values()
            if node.status == NodeStatus.FAILED
        ]
    
    def start(self) -> bool:
        """Inicia execução do graph"""
        if self.status != GraphStatus.CREATED:
            return False
        
        self.status = GraphStatus.RUNNING
        self.started_at = datetime.now()
        return True
    
    def pause(self) -> bool:
        """Pausa execução do graph"""
        if self.status != GraphStatus.RUNNING:
            return False
        
        self.status = GraphStatus.PAUSED
        return True
    
    def resume(self) -> bool:
        """Retoma execução do graph"""
        if self.status != GraphStatus.PAUSED:
            return False
        
        self.status = GraphStatus.RUNNING
        return True
    
    def complete(self) -> bool:
        """Completa execução do graph"""
        if self.status != GraphStatus.RUNNING:
            return False
        
        all_completed = all(
            n.status in [NodeStatus.COMPLETED, NodeStatus.SKIPPED]
            for n in self.nodes.values()
        )
        
        if all_completed:
            self.status = GraphStatus.COMPLETED
            self.completed_at = datetime.now()
            return True
        
        return False
    
    def fail(self) -> bool:
        """Falha na execução do graph"""
        if self.status not in [GraphStatus.RUNNING, GraphStatus.PAUSED]:
            return False
        
        self.status = GraphStatus.FAILED
        self.completed_at = datetime.now()
        return True
    
    def cancel(self) -> bool:
        """Cancela execução do graph"""
        if self.status in [GraphStatus.COMPLETED, GraphStatus.FAILED]:
            return False
        
        self.status = GraphStatus.CANCELLED
        self.completed_at = datetime.now()
        return True
    
    def get_progress(self) -> Dict[str, Any]:
        """Retorna progresso da execução"""
        total = len(self.nodes)
        completed = len(self.get_completed_nodes())
        failed = len(self.get_failed_nodes())
        running = len(self.get_running_nodes())
        
        return {
            "graph_id": self.graph_id,
            "status": self.status.value,
            "total_nodes": total,
            "completed_nodes": completed,
            "failed_nodes": failed,
            "running_nodes": running,
            "pending_nodes": total - completed - failed - running,
            "progress_percent": (completed / total * 100) if total > 0 else 0.0
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do graph"""
        return {
            "graph_id": self.graph_id,
            "name": self.name,
            "status": self.status.value,
            "total_nodes": len(self.nodes),
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "progress": self.get_progress()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "graph_id": self.graph_id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "nodes": {nid: n.to_dict() for nid, n in self.nodes.items()},
            "metadata": self.metadata,
            "stats": self.get_stats()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentGraph':
        """Cria instância a partir de dicionário"""
        graph = cls(
            graph_id=data.get("graph_id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            status=GraphStatus(data.get("status", "created")),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            metadata=data.get("metadata", {})
        )
        
        if data.get("started_at"):
            graph.started_at = datetime.fromisoformat(data["started_at"])
        if data.get("completed_at"):
            graph.completed_at = datetime.fromisoformat(data["completed_at"])
        
        for node_id, node_data in data.get("nodes", {}).items():
            graph.nodes[node_id] = GraphNode.from_dict(node_data)
        
        return graph
