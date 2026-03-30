# FEATURE: Multi-Agent Communication
# Agente especialista em área específica

import uuid
from enum import Enum
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, field


class SpecialistType(Enum):
    """Tipos de agentes especialistas"""
    CODE_WRITER = "code_writer"         # Especialista em escrever código
    CODE_REVIEWER = "code_reviewer"     # Especialista em revisar código
    TESTER = "tester"                   # Especialista em testes
    ARCHITECT = "architect"             # Especialista em arquitetura
    DEBUGGER = "debugger"               # Especialista em debug
    OPTIMIZER = "optimizer"             # Especialista em otimização
    DOCUMENTATION = "documentation"     # Especialista em documentação
    SECURITY = "security"               # Especialista em segurança


@dataclass
class Assignment:
    """Designação de tarefa para especialista"""
    assignment_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str = ""
    specialist_type: str = ""
    description: str = ""
    priority: int = 1
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "assignment_id": self.assignment_id,
            "task_id": self.task_id,
            "specialist_type": self.specialist_type,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "metadata": self.metadata
        }


class SpecialistAgent:
    """Agente especialista em área específica"""
    
    def __init__(self, agent_id: str, specialist_type: SpecialistType):
        self.agent_id = agent_id
        self.specialist_type = specialist_type
        self.expertise_level: float = 1.0
        self.current_assignment: Optional[Assignment] = None
        self.assignment_history: List[Assignment] = []
        self.is_available: bool = True
        self.skills: List[str] = []
        self.metadata: Dict[str, Any] = {}
    
    def accept_assignment(self, assignment: Assignment) -> bool:
        """Aceita designação de tarefa"""
        if not self.is_available:
            return False
        
        if not self._can_handle(assignment):
            return False
        
        self.current_assignment = assignment
        assignment.status = "accepted"
        self.is_available = False
        return True
    
    def complete_assignment(self, result: Optional[Dict[str, Any]] = None) -> bool:
        """Completa designação atual"""
        if not self.current_assignment:
            return False
        
        self.current_assignment.status = "completed"
        self.current_assignment.completed_at = datetime.now()
        
        if result:
            self.current_assignment.metadata["result"] = result
        
        self.assignment_history.append(self.current_assignment)
        self.current_assignment = None
        self.is_available = True
        return True
    
    def fail_assignment(self, reason: str) -> bool:
        """Falha na designação atual"""
        if not self.current_assignment:
            return False
        
        self.current_assignment.status = "failed"
        self.current_assignment.metadata["failure_reason"] = reason
        
        self.assignment_history.append(self.current_assignment)
        self.current_assignment = None
        self.is_available = True
        return True
    
    def _can_handle(self, assignment: Assignment) -> bool:
        """Verifica se pode lidar com a tarefa"""
        required_type = assignment.specialist_type
        return required_type == self.specialist_type.value
    
    def get_capabilities(self) -> List[str]:
        """Retorna capacidades do especialista"""
        base_capabilities = {
            SpecialistType.CODE_WRITER: [
                "escrever_funcoes",
                "escrever_classes",
                "implementar_algoritmos",
                "criar_interfaces"
            ],
            SpecialistType.CODE_REVIEWER: [
                "revisar_codigo",
                "identificar_problemas",
                "sugerir_melhorias",
                "verificar_padroes"
            ],
            SpecialistType.TESTER: [
                "criar_testes",
                "executar_testes",
                "analisar_cobertura",
                "identificar_bugs"
            ],
            SpecialistType.ARCHITECT: [
                "projetar_sistemas",
                "definir_padroes",
                "criar_documentacao",
                "analisar_requisitos"
            ],
            SpecialistType.DEBUGGER: [
                "identificar_erros",
                "depurar_codigo",
                "analisar_logs",
                "corrigir_bugs"
            ],
            SpecialistType.OPTIMIZER: [
                "otimizar_performance",
                "reduzir_complexidade",
                "melhorar_eficiencia",
                "analisar_metricas"
            ],
            SpecialistType.DOCUMENTATION: [
                "escrever_documentacao",
                "criar_tutoriais",
                "documentar_apis",
                "manter_readme"
            ],
            SpecialistType.SECURITY: [
                "auditar_seguranca",
                "identificar_vulnerabilidades",
                "implementar_seguranca",
                "revisar_autenticacao"
            ]
        }
        
        return base_capabilities.get(self.specialist_type, [])
    
    def update_expertise(self, delta: float) -> None:
        """Atualiza nível de expertise"""
        self.expertise_level = max(0.0, min(2.0, self.expertise_level + delta))
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do especialista"""
        completed = sum(1 for a in self.assignment_history if a.status == "completed")
        failed = sum(1 for a in self.assignment_history if a.status == "failed")
        
        return {
            "agent_id": self.agent_id,
            "specialist_type": self.specialist_type.value,
            "expertise_level": self.expertise_level,
            "is_available": self.is_available,
            "current_assignment": self.current_assignment.assignment_id if self.current_assignment else None,
            "total_assignments": len(self.assignment_history),
            "completed_assignments": completed,
            "failed_assignments": failed,
            "success_rate": completed / len(self.assignment_history) if self.assignment_history else 0.0
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "agent_id": self.agent_id,
            "specialist_type": self.specialist_type.value,
            "expertise_level": self.expertise_level,
            "is_available": self.is_available,
            "skills": self.skills,
            "current_assignment": self.current_assignment.to_dict() if self.current_assignment else None,
            "assignment_history": [a.to_dict() for a in self.assignment_history],
            "capabilities": self.get_capabilities(),
            "metadata": self.metadata,
            "stats": self.get_stats()
        }
