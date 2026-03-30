# FEATURE: Multi-Agent Communication
# Protocolo de Urgência de Mensagens para o sistema Plexo

import uuid
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List


class UrgencyLevel(Enum):
    """Níveis de urgência para mensagens entre agentes"""
    LOW = "low"           # Pode esperar, processar quando disponível
    MEDIUM = "medium"     # Prioridade normal, processar na fila
    HIGH = "high"         # Prioridade alta, interromper tarefa atual se necessário
    CRITICAL = "critical" # Checkpoint imediato, pausar tudo e responder

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            order = {
                UrgencyLevel.LOW: 0,
                UrgencyLevel.MEDIUM: 1,
                UrgencyLevel.HIGH: 2,
                UrgencyLevel.CRITICAL: 3
            }
            return order[self] < order[other]
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            order = {
                UrgencyLevel.LOW: 0,
                UrgencyLevel.MEDIUM: 1,
                UrgencyLevel.HIGH: 2,
                UrgencyLevel.CRITICAL: 3
            }
            return order[self] <= order[other]
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            order = {
                UrgencyLevel.LOW: 0,
                UrgencyLevel.MEDIUM: 1,
                UrgencyLevel.HIGH: 2,
                UrgencyLevel.CRITICAL: 3
            }
            return order[self] > order[other]
        return NotImplemented

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            order = {
                UrgencyLevel.LOW: 0,
                UrgencyLevel.MEDIUM: 1,
                UrgencyLevel.HIGH: 2,
                UrgencyLevel.CRITICAL: 3
            }
            return order[self] >= order[other]
        return NotImplemented


@dataclass
class UrgentMessage:
    """Mensagem com nível de urgência"""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender_jid: str = ""
    receiver_jid: str = ""
    urgency: UrgencyLevel = UrgencyLevel.MEDIUM
    content: str = ""
    requires_checkpoint: bool = False
    timestamp: datetime = field(default_factory=datetime.now)
    context: Optional[Dict[str, Any]] = None
    
    def should_interrupt(self) -> bool:
        """Verifica se deve interromper tarefa atual"""
        return self.urgency in [UrgencyLevel.HIGH, UrgencyLevel.CRITICAL]
    
    def requires_immediate_response(self) -> bool:
        """Verifica se precisa de resposta imediata"""
        return self.urgency == UrgencyLevel.CRITICAL
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "message_id": self.message_id,
            "sender_jid": self.sender_jid,
            "receiver_jid": self.receiver_jid,
            "urgency": self.urgency.value,
            "content": self.content,
            "requires_checkpoint": self.requires_checkpoint,
            "timestamp": self.timestamp.isoformat(),
            "context": self.context or {}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UrgentMessage':
        """Cria instância a partir de dicionário"""
        return cls(
            message_id=data.get("message_id", str(uuid.uuid4())),
            sender_jid=data.get("sender_jid", ""),
            receiver_jid=data.get("receiver_jid", ""),
            urgency=UrgencyLevel(data.get("urgency", "medium")),
            content=data.get("content", ""),
            requires_checkpoint=data.get("requires_checkpoint", False),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            context=data.get("context")
        )


class UrgencyProtocol:
    """Protocolo para gerenciamento de mensagens urgentes"""
    
    def __init__(self):
        self.pending_messages: Dict[str, List[UrgentMessage]] = {}
        self.message_history: List[UrgentMessage] = []
    
    def create_urgent_message(
        self,
        sender_jid: str,
        receiver_jid: str,
        content: str,
        urgency: UrgencyLevel = UrgencyLevel.MEDIUM,
        requires_checkpoint: bool = False,
        context: Optional[Dict[str, Any]] = None
    ) -> UrgentMessage:
        """Cria mensagem urgente"""
        message = UrgentMessage(
            sender_jid=sender_jid,
            receiver_jid=receiver_jid,
            content=content,
            urgency=urgency,
            requires_checkpoint=requires_checkpoint,
            context=context
        )
        
        if receiver_jid not in self.pending_messages:
            self.pending_messages[receiver_jid] = []
        self.pending_messages[receiver_jid].append(message)
        
        self.pending_messages[receiver_jid].sort(
            key=lambda m: [
                UrgencyLevel.LOW,
                UrgencyLevel.MEDIUM,
                UrgencyLevel.HIGH,
                UrgencyLevel.CRITICAL
            ].index(m.urgency),
            reverse=True
        )
        
        return message
    
    def get_pending_messages(self, receiver_jid: str) -> List[UrgentMessage]:
        """Retorna mensagens pendentes para um receptor"""
        return self.pending_messages.get(receiver_jid, [])
    
    def get_urgent_messages(self, receiver_jid: str) -> List[UrgentMessage]:
        """Retorna apenas mensagens urgentes (HIGH ou CRITICAL)"""
        messages = self.get_pending_messages(receiver_jid)
        return [m for m in messages if m.urgency in [UrgencyLevel.HIGH, UrgencyLevel.CRITICAL]]
    
    def mark_as_processed(self, message_id: str, receiver_jid: str) -> bool:
        """Marca mensagem como processada"""
        if receiver_jid in self.pending_messages:
            for i, msg in enumerate(self.pending_messages[receiver_jid]):
                if msg.message_id == message_id:
                    processed_msg = self.pending_messages[receiver_jid].pop(i)
                    self.message_history.append(processed_msg)
                    return True
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do protocolo"""
        total_pending = sum(len(msgs) for msgs in self.pending_messages.values())
        urgent_pending = sum(
            len([m for m in msgs if m.urgency in [UrgencyLevel.HIGH, UrgencyLevel.CRITICAL]])
            for msgs in self.pending_messages.values()
        )
        
        return {
            "total_pending": total_pending,
            "urgent_pending": urgent_pending,
            "total_processed": len(self.message_history),
            "receivers_with_pending": len(self.pending_messages)
        }
