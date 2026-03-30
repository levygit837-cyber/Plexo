# FEATURE: Multi-Agent Communication
# Schemas para comunicação P2P entre agentes

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    """Tipos de mensagem P2P"""
    DIRECT = "direct"
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    URGENT = "urgent"


class UrgencyLevel(str, Enum):
    """Níveis de urgência"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class P2PMessageCreate(BaseModel):
    """Schema para criação de mensagem P2P"""
    to_agent: str = Field(..., description="Username do agente destinatário")
    content: str = Field(..., description="Conteúdo da mensagem")
    message_type: MessageType = Field(default=MessageType.DIRECT, description="Tipo da mensagem")
    urgency: UrgencyLevel = Field(default=UrgencyLevel.MEDIUM, description="Nível de urgência")
    requires_response: bool = Field(default=False, description="Se requer resposta")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadados adicionais")
    
    class Config:
        json_schema_extra = {
            "example": {
                "to_agent": "monitor",
                "content": "Olá Monitor! Estou executando a tarefa.",
                "message_type": "direct",
                "urgency": "MEDIUM",
                "requires_response": False
            }
        }


class P2PMessageResponse(BaseModel):
    """Schema de resposta de mensagem P2P"""
    message_id: str = Field(..., description="ID da mensagem")
    from_agent: str = Field(..., description="Username do agente remetente")
    to_agent: str = Field(..., description="Username do agente destinatário")
    content: str = Field(..., description="Conteúdo da mensagem")
    message_type: str = Field(..., description="Tipo da mensagem")
    urgency: str = Field(..., description="Nível de urgência")
    requires_response: bool = Field(..., description="Se requer resposta")
    timestamp: datetime = Field(..., description="Timestamp da mensagem")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadados")


class P2PRequestCreate(BaseModel):
    """Schema para criação de request P2P"""
    to_agent: str = Field(..., description="Username do agente destinatário")
    content: str = Field(..., description="Conteúdo da request")
    urgency: UrgencyLevel = Field(default=UrgencyLevel.HIGH, description="Nível de urgência")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadados")


class P2PResponseCreate(BaseModel):
    """Schema para criação de response P2P"""
    to_agent: str = Field(..., description="Username do agente destinatário")
    original_message_id: str = Field(..., description="ID da mensagem original")
    content: str = Field(..., description="Conteúdo da response")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadados")


class P2PUrgentMessageCreate(BaseModel):
    """Schema para criação de mensagem urgente P2P"""
    to_agent: str = Field(..., description="Username do agente destinatário")
    content: str = Field(..., description="Conteúdo da mensagem urgente")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadados")


class P2PNotificationCreate(BaseModel):
    """Schema para criação de notificação P2P"""
    to_agent: str = Field(..., description="Username do agente destinatário")
    content: str = Field(..., description="Conteúdo da notificação")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadados")


class ConversationResponse(BaseModel):
    """Schema de resposta de conversa"""
    agent_id: str = Field(..., description="ID do agente")
    other_agent: str = Field(..., description="Username do outro agente")
    messages: list[P2PMessageResponse] = Field(..., description="Lista de mensagens")
    total: int = Field(..., description="Total de mensagens")


class P2PStatsResponse(BaseModel):
    """Schema de resposta de estatísticas P2P"""
    agent_id: str = Field(..., description="ID do agente")
    total_messages: int = Field(..., description="Total de mensagens")
    pending_requests: int = Field(..., description="Requests pendentes")
    response_handlers: int = Field(..., description="Handlers registrados")
    is_listening: bool = Field(..., description="Se está ouvindo mensagens")
