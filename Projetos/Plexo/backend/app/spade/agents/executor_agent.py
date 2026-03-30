# FEATURE: Multi-Agent Communication
# Agente executor de graphs de tarefas

import uuid
from enum import Enum
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, field


class ExecutorStatus(Enum):
    """Status do executor"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ExecutionStep:
    """Passo de execução"""
    step_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    step_number: int = 0
    action: str = ""
    status: str = "pending"
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "step_id": self.step_id,
            "step_number": self.step_number,
            "action": self.action,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "metadata": self.metadata
        }


class ExecutorAgent:
    """Agente executor de graphs de tarefas"""
    
    def __init__(self, agent_id: str, whiteboard_id: Optional[str] = None):
        self.agent_id = agent_id
        self.whiteboard_id = whiteboard_id
        self.status = ExecutorStatus.IDLE
        self.current_graph_id: Optional[str] = None
        self.current_step: Optional[ExecutionStep] = None
        self.execution_history: List[ExecutionStep] = []
        self.metadata: Dict[str, Any] = {}
    
    def start_execution(self, graph_id: str, steps: List[Dict[str, Any]]) -> bool:
        """Inicia execução de um graph"""
        if self.status != ExecutorStatus.IDLE:
            return False
        
        self.current_graph_id = graph_id
        self.status = ExecutorStatus.RUNNING
        
        for i, step_data in enumerate(steps):
            step = ExecutionStep(
                step_number=i + 1,
                action=step_data.get("action", ""),
                metadata=step_data.get("metadata", {})
            )
            self.execution_history.append(step)
        
        return True
    
    def execute_next_step(self) -> Optional[ExecutionStep]:
        """Executa próximo passo"""
        if self.status != ExecutorStatus.RUNNING:
            return None
        
        next_step = None
        for step in self.execution_history:
            if step.status == "pending":
                next_step = step
                break
        
        if not next_step:
            self.status = ExecutorStatus.COMPLETED
            return None
        
        next_step.status = "running"
        next_step.started_at = datetime.now()
        self.current_step = next_step
        
        return next_step
    
    def complete_step(self, result: Optional[Dict[str, Any]] = None) -> bool:
        """Completa passo atual"""
        if not self.current_step:
            return False
        
        self.current_step.status = "completed"
        self.current_step.completed_at = datetime.now()
        self.current_step.result = result
        
        self.current_step = None
        return True
    
    def fail_step(self, error: str) -> bool:
        """Falha no passo atual"""
        if not self.current_step:
            return False
        
        self.current_step.status = "failed"
        self.current_step.completed_at = datetime.now()
        self.current_step.metadata["error"] = error
        
        self.status = ExecutorStatus.FAILED
        self.current_step = None
        return True
    
    def pause_execution(self) -> bool:
        """Pausa execução"""
        if self.status == ExecutorStatus.RUNNING:
            self.status = ExecutorStatus.PAUSED
            return True
        return False
    
    def resume_execution(self) -> bool:
        """Retoma execução"""
        if self.status == ExecutorStatus.PAUSED:
            self.status = ExecutorStatus.RUNNING
            return True
        return False
    
    def get_progress(self) -> Dict[str, Any]:
        """Retorna progresso da execução"""
        total_steps = len(self.execution_history)
        completed_steps = sum(1 for s in self.execution_history if s.status == "completed")
        failed_steps = sum(1 for s in self.execution_history if s.status == "failed")
        
        return {
            "graph_id": self.current_graph_id,
            "status": self.status.value,
            "total_steps": total_steps,
            "completed_steps": completed_steps,
            "failed_steps": failed_steps,
            "pending_steps": total_steps - completed_steps - failed_steps,
            "progress_percent": (completed_steps / total_steps * 100) if total_steps > 0 else 0.0,
            "current_step": self.current_step.to_dict() if self.current_step else None
        }
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Retorna histórico de execução"""
        return [s.to_dict() for s in self.execution_history]
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do executor"""
        completed = sum(1 for s in self.execution_history if s.status == "completed")
        failed = sum(1 for s in self.execution_history if s.status == "failed")
        
        return {
            "agent_id": self.agent_id,
            "whiteboard_id": self.whiteboard_id,
            "status": self.status.value,
            "current_graph_id": self.current_graph_id,
            "total_steps_executed": len(self.execution_history),
            "successful_steps": completed,
            "failed_steps": failed,
            "success_rate": completed / len(self.execution_history) if self.execution_history else 0.0
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "agent_id": self.agent_id,
            "whiteboard_id": self.whiteboard_id,
            "status": self.status.value,
            "current_graph_id": self.current_graph_id,
            "current_step": self.current_step.to_dict() if self.current_step else None,
            "execution_history": self.get_execution_history(),
            "metadata": self.metadata,
            "stats": self.get_stats()
        }
