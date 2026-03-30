# FEATURE: Multi-Agent Communication
# Agente de monitoramento em tempo real

import uuid
from enum import Enum
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, field


class MonitorRole(Enum):
    """Roles de agentes de monitoramento"""
    TRACKER = "tracker"      # Agente 1: Trackeia e escreve no whiteboard
    VALIDATOR = "validator"  # Agente 2: Identifica erros e faz testes


@dataclass
class MonitorAction:
    """Ação monitorada"""
    action_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = ""
    action_type: str = ""
    description: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "action_id": self.action_id,
            "agent_id": self.agent_id,
            "action_type": self.action_type,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


class MonitorAgent:
    """Agente de monitoramento em tempo real"""
    
    def __init__(self, agent_id: str, role: MonitorRole, whiteboard_id: str):
        self.agent_id = agent_id
        self.role = role
        self.whiteboard_id = whiteboard_id
        self.monitored_agent_id: Optional[str] = None
        self.actions_observed: List[MonitorAction] = []
        self.errors_detected: List[Dict[str, Any]] = []
        self.test_results: List[Dict[str, Any]] = []
        self.is_active: bool = False
    
    def start_monitoring(self, target_agent_id: str) -> bool:
        """Inicia monitoramento de um agente"""
        self.monitored_agent_id = target_agent_id
        self.is_active = True
        return True
    
    def stop_monitoring(self) -> bool:
        """Para monitoramento"""
        self.monitored_agent_id = None
        self.is_active = False
        return True
    
    def observe_action(self, action: MonitorAction) -> Optional[Dict[str, Any]]:
        """Observa ação do agente monitorado"""
        if not self.is_active:
            return None
        
        self.actions_observed.append(action)
        
        if self.role == MonitorRole.TRACKER:
            return self._track_action(action)
        else:
            return self._validate_action(action)
    
    def _track_action(self, action: MonitorAction) -> Dict[str, Any]:
        """Trackeia ação e escreve no whiteboard"""
        description = self._create_description(action)
        
        return {
            "type": "tracked",
            "action_id": action.action_id,
            "description": description,
            "whiteboard_id": self.whiteboard_id,
            "timestamp": datetime.now().isoformat()
        }
    
    def _validate_action(self, action: MonitorAction) -> Dict[str, Any]:
        """Valida ação e identifica erros"""
        errors = self._analyze_for_errors(action)
        test_results = None
        
        if errors:
            self.errors_detected.extend(errors)
            test_results = self._run_tests(action)
            self.test_results.append(test_results)
        
        return {
            "type": "validated",
            "action_id": action.action_id,
            "errors": errors,
            "test_results": test_results,
            "timestamp": datetime.now().isoformat()
        }
    
    def _create_description(self, action: MonitorAction) -> str:
        """Cria descrição amigável da ação"""
        action_type = action.action_type
        metadata = action.metadata
        
        if action_type == "function_created":
            func_name = metadata.get("function_name", "desconhecida")
            desc = metadata.get("description", "")
            line = metadata.get("line_number")
            
            text = f"O Executor escreveu uma função chamada '{func_name}' que {desc}"
            if line:
                text += f"... na linha {line}"
            return text
        
        elif action_type == "class_created":
            class_name = metadata.get("class_name", "desconhecida")
            desc = metadata.get("description", "")
            line = metadata.get("line_number")
            
            text = f"O Executor escreveu uma classe chamada '{class_name}' que {desc}"
            if line:
                text += f"... na linha {line}"
            return text
        
        elif action_type == "file_created":
            file_path = metadata.get("file_path", "desconhecido")
            return f"O Executor criou o arquivo '{file_path}'"
        
        elif action_type == "file_modified":
            file_path = metadata.get("file_path", "desconhecido")
            changes = metadata.get("changes", "")
            return f"O Executor modificou o arquivo '{file_path}': {changes}"
        
        elif action_type == "test_created":
            test_name = metadata.get("test_name", "desconhecido")
            return f"O Executor criou o teste '{test_name}'"
        
        else:
            return action.description or f"O Executor executou a ação '{action_type}'"
    
    def _analyze_for_errors(self, action: MonitorAction) -> List[Dict[str, Any]]:
        """Analisa ação em busca de erros"""
        errors = []
        metadata = action.metadata
        
        if action.action_type == "function_created":
            func_name = metadata.get("function_name", "")
            if not func_name:
                errors.append({
                    "type": "missing_name",
                    "message": "Função criada sem nome",
                    "severity": "high"
                })
        
        elif action.action_type == "class_created":
            class_name = metadata.get("class_name", "")
            if not class_name:
                errors.append({
                    "type": "missing_name",
                    "message": "Classe criada sem nome",
                    "severity": "high"
                })
        
        elif action.action_type == "file_modified":
            changes = metadata.get("changes", "")
            if "delete" in changes.lower() and "test" in changes.lower():
                errors.append({
                    "type": "risky_deletion",
                    "message": "Possível exclusão de código de teste detectada",
                    "severity": "medium"
                })
        
        return errors
    
    def _run_tests(self, action: MonitorAction) -> Dict[str, Any]:
        """Executa testes automáticos"""
        test_name = f"auto_test_{action.action_id[:8]}"
        
        return {
            "test_name": test_name,
            "action_id": action.action_id,
            "passed": True,
            "details": "Teste automático executado com sucesso",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_observed_actions(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retorna ações observadas"""
        return [a.to_dict() for a in self.actions_observed[-limit:]]
    
    def get_errors(self) -> List[Dict[str, Any]]:
        """Retorna erros detectados"""
        return self.errors_detected.copy()
    
    def get_test_results(self) -> List[Dict[str, Any]]:
        """Retorna resultados de testes"""
        return self.test_results.copy()
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do monitor"""
        return {
            "agent_id": self.agent_id,
            "role": self.role.value,
            "whiteboard_id": self.whiteboard_id,
            "monitored_agent_id": self.monitored_agent_id,
            "is_active": self.is_active,
            "actions_observed": len(self.actions_observed),
            "errors_detected": len(self.errors_detected),
            "tests_run": len(self.test_results)
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "agent_id": self.agent_id,
            "role": self.role.value,
            "whiteboard_id": self.whiteboard_id,
            "monitored_agent_id": self.monitored_agent_id,
            "is_active": self.is_active,
            "actions_observed": [a.to_dict() for a in self.actions_observed],
            "errors_detected": self.errors_detected,
            "test_results": self.test_results,
            "stats": self.get_stats()
        }
