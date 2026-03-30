# FEATURE: Multi-Agent Communication
# Protocolo de comunicação peer-to-peer entre agentes

import uuid
import logging
import asyncio
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """Tipos de mensagem P2P"""
    DIRECT = "direct"
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    URGENT = "urgent"


@dataclass
class P2PMessage:
    """Mensagem peer-to-peer"""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    from_agent: str = ""
    to_agent: str = ""
    content: str = ""
    message_type: MessageType = MessageType.DIRECT
    urgency: str = "MEDIUM"
    requires_response: bool = False
    in_reply_to: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "message_id": self.message_id,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "content": self.content,
            "message_type": self.message_type.value,
            "urgency": self.urgency,
            "requires_response": self.requires_response,
            "in_reply_to": self.in_reply_to,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'P2PMessage':
        """Cria instância a partir de dicionário"""
        return cls(
            message_id=data.get("message_id", str(uuid.uuid4())),
            from_agent=data.get("from_agent", ""),
            to_agent=data.get("to_agent", ""),
            content=data.get("content", ""),
            message_type=MessageType(data.get("message_type", "direct")),
            urgency=data.get("urgency", "MEDIUM"),
            requires_response=data.get("requires_response", False),
            in_reply_to=data.get("in_reply_to"),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            metadata=data.get("metadata", {})
        )


class P2PProtocol:
    """Protocolo de comunicação peer-to-peer"""
    
    def __init__(self, agent_id: str, connection_manager: Any):
        self.agent_id = agent_id
        self.connection_manager = connection_manager
        self.pending_requests: Dict[str, P2PMessage] = {}
        self.message_history: List[P2PMessage] = []
        self.response_handlers: Dict[str, Callable] = {}
        self.is_listening: bool = False
    
    async def send_direct_message(self, to_agent: str, content: str, urgency: str = "MEDIUM") -> Dict[str, Any]:
        """Envia mensagem direta para outro agente"""
        message = P2PMessage(
            from_agent=self.agent_id,
            to_agent=to_agent,
            content=content,
            message_type=MessageType.DIRECT,
            urgency=urgency
        )
        
        result = await self.connection_manager.send_message(
            from_username=self.agent_id,
            to_username=to_agent,
            content=content,
            urgency=urgency
        )
        
        if result.get("success"):
            self.message_history.append(message)
            logger.info(f"Mensagem direta enviada de {self.agent_id} para {to_agent}")
        
        return result
    
    async def send_request(self, to_agent: str, content: str, urgency: str = "HIGH") -> Dict[str, Any]:
        """Envia mensagem que requer resposta"""
        message = P2PMessage(
            from_agent=self.agent_id,
            to_agent=to_agent,
            content=content,
            message_type=MessageType.REQUEST,
            urgency=urgency,
            requires_response=True
        )
        
        self.pending_requests[message.message_id] = message
        
        result = await self.connection_manager.send_message(
            from_username=self.agent_id,
            to_username=to_agent,
            content=content,
            urgency=urgency
        )
        
        if result.get("success"):
            self.message_history.append(message)
            logger.info(f"Request enviada de {self.agent_id} para {to_agent}")
        
        return result
    
    async def send_response(self, to_agent: str, original_message_id: str, content: str) -> Dict[str, Any]:
        """Envia resposta a uma request"""
        message = P2PMessage(
            from_agent=self.agent_id,
            to_agent=to_agent,
            content=content,
            message_type=MessageType.RESPONSE,
            in_reply_to=original_message_id
        )
        
        result = await self.connection_manager.send_message(
            from_username=self.agent_id,
            to_username=to_agent,
            content=content,
            urgency="MEDIUM"
        )
        
        if result.get("success"):
            self.message_history.append(message)
            logger.info(f"Response enviada de {self.agent_id} para {to_agent}")
        
        return result
    
    async def send_urgent_message(self, to_agent: str, content: str) -> Dict[str, Any]:
        """Envia mensagem urgente (requer checkpoint)"""
        message = P2PMessage(
            from_agent=self.agent_id,
            to_agent=to_agent,
            content=content,
            message_type=MessageType.URGENT,
            urgency="CRITICAL",
            requires_response=True
        )
        
        result = await self.connection_manager.send_message(
            from_username=self.agent_id,
            to_username=to_agent,
            content=content,
            urgency="CRITICAL"
        )
        
        if result.get("success"):
            self.message_history.append(message)
            logger.info(f"Mensagem URGENTE enviada de {self.agent_id} para {to_agent}")
        
        return result
    
    async def send_notification(self, to_agent: str, content: str) -> Dict[str, Any]:
        """Envia notificação (não requer resposta)"""
        message = P2PMessage(
            from_agent=self.agent_id,
            to_agent=to_agent,
            content=content,
            message_type=MessageType.NOTIFICATION,
            urgency="LOW",
            requires_response=False
        )
        
        result = await self.connection_manager.send_message(
            from_username=self.agent_id,
            to_username=to_agent,
            content=content,
            urgency="LOW"
        )
        
        if result.get("success"):
            self.message_history.append(message)
            logger.info(f"Notification enviada de {self.agent_id} para {to_agent}")
        
        return result
    
    async def process_incoming_message(self, message_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Processa mensagem recebida"""
        message = P2PMessage.from_dict(message_data)
        self.message_history.append(message)
        
        if message.message_type == MessageType.REQUEST and message.requires_response:
            return {
                "action": "send_response",
                "to": message.from_agent,
                "original_message_id": message.message_id,
                "content": f"Recebi sua mensagem: {message.content}"
            }
        
        if message.message_type == MessageType.URGENT:
            logger.warning(f"Mensagem URGENTE recebida de {message.from_agent}: {message.content}")
            return {
                "action": "checkpoint_required",
                "from": message.from_agent,
                "message_id": message.message_id
            }
        
        return None
    
    def register_response_handler(self, message_id: str, handler: Callable) -> None:
        """Registra handler para resposta de uma mensagem"""
        self.response_handlers[message_id] = handler
    
    def get_pending_requests(self) -> List[Dict[str, Any]]:
        """Retorna requests pendentes"""
        return [msg.to_dict() for msg in self.pending_requests.values()]
    
    def get_message_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retorna histórico de mensagens"""
        return [msg.to_dict() for msg in self.message_history[-limit:]]
    
    def get_conversation_with(self, other_agent: str) -> List[Dict[str, Any]]:
        """Retorna conversa com outro agente"""
        return [
            msg.to_dict() for msg in self.message_history
            if msg.from_agent == other_agent or msg.to_agent == other_agent
        ]
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do protocolo"""
        return {
            "agent_id": self.agent_id,
            "total_messages": len(self.message_history),
            "pending_requests": len(self.pending_requests),
            "response_handlers": len(self.response_handlers),
            "is_listening": self.is_listening
        }
