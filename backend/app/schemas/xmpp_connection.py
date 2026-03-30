# FEATURE: Multi-Agent Communication
# Schemas para conexão XMPP

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class XMPPConfigSchema(BaseModel):
    """Schema para configuração XMPP"""
    server: str = Field(default="localhost", description="Servidor XMPP")
    port: int = Field(default=5222, description="Porta XMPP")
    domain: str = Field(default="localhost", description="Domínio XMPP")
    use_tls: bool = Field(default=False, description="Usar TLS")
    use_ssl: bool = Field(default=False, description="Usar SSL")


class XMPPRegisterRequest(BaseModel):
    """Schema para registro de agente"""
    username: str = Field(..., description="Username do agente", min_length=3, max_length=50)
    password: str = Field(..., description="Senha do agente", min_length=6)
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "executor",
                "password": "executor123"
            }
        }


class XMPPConnectRequest(BaseModel):
    """Schema para conexão de agente"""
    username: str = Field(..., description="Username do agente")
    password: str = Field(..., description="Senha do agente")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "executor",
                "password": "executor123"
            }
        }


class XMPPConnectionResponse(BaseModel):
    """Schema de resposta de conexão XMPP"""
    success: bool = Field(..., description="Se a operação foi bem sucedida")
    jid: Optional[str] = Field(default=None, description="JID do agente")
    username: Optional[str] = Field(default=None, description="Username do agente")
    message: Optional[str] = Field(default=None, description="Mensagem de sucesso")
    error: Optional[str] = Field(default=None, description="Mensagem de erro")
    connected_at: Optional[datetime] = Field(default=None, description="Data de conexão")


class XMPPSendMessageRequest(BaseModel):
    """Schema para envio de mensagem XMPP"""
    to_username: str = Field(..., description="Username do destinatário")
    content: str = Field(..., description="Conteúdo da mensagem")
    urgency: str = Field(default="MEDIUM", description="Nível de urgência")
    
    class Config:
        json_schema_extra = {
            "example": {
                "to_username": "monitor",
                "content": "Olá Monitor!",
                "urgency": "MEDIUM"
            }
        }


class XMPPSendMessageResponse(BaseModel):
    """Schema de resposta de envio de mensagem"""
    success: bool = Field(..., description="Se o envio foi bem sucedido")
    from_jid: Optional[str] = Field(default=None, description="JID do remetente")
    to_jid: Optional[str] = Field(default=None, description="JID do destinatário")
    content: Optional[str] = Field(default=None, description="Conteúdo da mensagem")
    urgency: Optional[str] = Field(default=None, description="Nível de urgência")
    timestamp: Optional[datetime] = Field(default=None, description="Timestamp do envio")
    error: Optional[str] = Field(default=None, description="Mensagem de erro")


class ConnectedAgentsResponse(BaseModel):
    """Schema de resposta de agentes conectados"""
    agents: List[str] = Field(..., description="Lista de usernames conectados")
    total: int = Field(..., description="Total de agentes conectados")


class AgentStatusResponse(BaseModel):
    """Schema de resposta de status do agente"""
    username: str = Field(..., description="Username do agente")
    is_connected: bool = Field(..., description="Se está conectado")
    jid: Optional[str] = Field(default=None, description="JID do agente")
