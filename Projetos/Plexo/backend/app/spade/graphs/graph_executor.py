# FEATURE: Multi-Agent Communication
# Executor de graphs de tarefas

import uuid
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
from dataclasses import dataclass, field
from .agent_graph import AgentGraph, GraphStatus
from .graph_node import GraphNode, NodeStatus


class GraphExecutor:
    """Executor de graphs de tarefas"""
    
    def __init__(self, graph: AgentGraph):
        self.graph = graph
        self.executor_id = str(uuid.uuid4())
        self.is_running: bool = False
        self.execution_log: List[Dict[str, Any]] = []
        self.node_handlers: Dict[str, Callable] = {}
    
    def register_handler(self, specialist_type: str, handler: Callable) -> None:
        """Registra handler para tipo de especialista"""
        self.node_handlers[specialist_type] = handler
    
    def execute(self) -> bool:
        """Executa graph completo"""
        if self.is_running:
            return False
        
        if not self.graph.start():
            return False
        
        self.is_running = True
        
        try:
            while self.graph.status == GraphStatus.RUNNING:
                ready_nodes = self.graph.get_ready_nodes()
                
                if not ready_nodes:
                    running = self.graph.get_running_nodes()
                    if not running:
                        self.graph.complete()
                        break
                    continue
                
                for node in ready_nodes:
                    self._execute_node(node)
                
                if self.graph.get_failed_nodes():
                    self.graph.fail()
                    break
            
            self.is_running = False
            return self.graph.status == GraphStatus.COMPLETED
        
        except Exception as e:
            self.graph.fail()
            self.is_running = False
            self._log_event("error", {"error": str(e)})
            return False
    
    def _execute_node(self, node: GraphNode) -> bool:
        """Executa um nó"""
        handler = self.node_handlers.get(node.specialist_type)
        
        if not handler:
            node.fail(f"No handler for specialist type: {node.specialist_type}")
            self._log_event("node_failed", {
                "node_id": node.node_id,
                "error": f"No handler for {node.specialist_type}"
            })
            return False
        
        node.start(self.executor_id)
        self._log_event("node_started", {"node_id": node.node_id})
        
        try:
            result = handler(node)
            node.complete(result)
            self._log_event("node_completed", {
                "node_id": node.node_id,
                "result": result
            })
            return True
        
        except Exception as e:
            node.fail(str(e))
            self._log_event("node_failed", {
                "node_id": node.node_id,
                "error": str(e)
            })
            return False
    
    def execute_node(self, node_id: str) -> bool:
        """Executa nó específico"""
        node = self.graph.get_node(node_id)
        if not node:
            return False
        
        completed = [
            nid for nid, n in self.graph.nodes.items()
            if n.status == NodeStatus.COMPLETED
        ]
        
        if not node.is_ready(completed):
            return False
        
        return self._execute_node(node)
    
    def pause(self) -> bool:
        """Pausa execução"""
        if self.graph.status == GraphStatus.RUNNING:
            self.graph.pause()
            self._log_event("paused", {})
            return True
        return False
    
    def resume(self) -> bool:
        """Retoma execução"""
        if self.graph.status == GraphStatus.PAUSED:
            self.graph.resume()
            self._log_event("resumed", {})
            return True
        return False
    
    def cancel(self) -> bool:
        """Cancela execução"""
        if self.graph.status in [GraphStatus.RUNNING, GraphStatus.PAUSED]:
            self.graph.cancel()
            self.is_running = False
            self._log_event("cancelled", {})
            return True
        return False
    
    def _log_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Registra evento no log"""
        self.execution_log.append({
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        })
    
    def get_execution_log(self) -> List[Dict[str, Any]]:
        """Retorna log de execução"""
        return self.execution_log.copy()
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do executor"""
        return {
            "executor_id": self.executor_id,
            "graph_id": self.graph.graph_id,
            "is_running": self.is_running,
            "graph_status": self.graph.status.value,
            "total_events": len(self.execution_log),
            "progress": self.graph.get_progress()
        }
