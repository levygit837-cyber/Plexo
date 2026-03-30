# FEATURE: Multi-Agent Communication
# Serviço para comunicação P2P entre agentes

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from app.spade.protocols.p2p_protocol import P2PProtocol, P2PMessage, MessageType
from app.services.xmpp_service import XMPPService

logger = logging.getLogger(__name__)


class P2PService:
    """Serviço para comunicação P2P entre agentes"""
    
    def __init__(self, xmpp_service: XMPPService):
        self.xmpp_service = xmpp_service
        self.protocols: Dict[str, P2PProtocol] = {}
        logger.info("P2PService inicializado")
    
    def get_or_create_protocol(self, agent_id: str) -> P2PProtocol:
        """Obtém ou cria protocolo P2P para um agente"""
        if agent_id not in self.protocols:
            self.protocols[agent_id] = P2PProtocol(agent_id, self.xmpp_service.connection_manager)
            logger.info(f"Protocolo P2P criado para agente {agent_id}")
        return self.protocols[agent_id]
    
    async def send_direct_message(
        self,
        from_agent: str,
        to_agent: str,
        content: str,
        urgency: str = "MEDIUM"
    ) -> Dict[str, Any]:
        """Envia mensagem direta entre agentes"""
        try:
            protocol = self.get_or_create_protocol(from_agent)
            result = await protocol.send_direct_message(to_agent, content, urgency)
            logger.info(f"Mensagem direta enviada de {from_agent} para {to_agent}")
            return result
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem direta: {e}")
            return {"success": False, "error": str(e)}
    
    async def send_request(
        self,
        from_agent: str,
        to_agent: str,
        content: str,
        urgency: str = "HIGH"
    ) -> Dict[str, Any]:
        """Envia request que requer resposta"""
        try:
            protocol = self.get_or_create_protocol(from_agent)
            result = await protocol.send_request(to_agent, content, urgency)
            logger.info(f"Request enviada de {from_agent} para {to_agent}")
            return result
        except Exception as e:
            logger.error(f"Erro ao enviar request: {e}")
            return {"success": False, "error": str(e)}
    
    async def send_response(
        self,
        from_agent: str,
        to_agent: str,
        original_message_id: str,
        content: str
    ) -> Dict[str, Any]:
        """Envia response a uma request"""
        try:
            protocol = self.get_or_create_protocol(from_agent)
            result = await protocol.send_response(to_agent, original_message_id, content)
            logger.info(f"Response enviada de {from_agent} para {to_agent}")
            return result
        except Exception as e:
            logger.error(f"Erro ao enviar response: {e}")
            return {"success": False, "error": str(e)}
    
    async def send_urgent_message(
        self,
        from_agent: str,
        to_agent: str,
        content: str
    ) -> Dict[str, Any]:
        """Envia mensagem urgente"""
        try:
            protocol = self.get_or_create_protocol(from_agent)
            result = await protocol.send_urgent_message(to_agent, content)
            logger.info(f"Mensagem urgente enviada de {from_agent} para {to_agent}")
            return result
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem urgente: {e}")
            return {"success": False, "error": str(e)}
    
    async def send_notification(
        self,
        from_agent: str,
        to_agent: str,
        content: str
    ) -> Dict[str, Any]:
        """Envia notificação"""
        try:
            protocol = self.get_or_create_protocol(from_agent)
            result = await protocol.send_notification(to_agent, content)
            logger.info(f"Notificação enviada de {from_agent} para {to_agent}")
            return result
        except Exception as e:
            logger.error(f"Erro ao enviar notificação: {e}")
            return {"success": False, "error": str(e)}
    
    def get_pending_requests(self, agent_id: str) -> List[Dict[str, Any]]:
        """Retorna requests pendentes de um agente"""
        protocol = self.get_or_create_protocol(agent_id)
        return protocol.get_pending_requests()
    
    def get_message_history(self, agent_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Retorna histórico de mensagens de um agente"""
        protocol = self.get_or_create_protocol(agent_id)
        return protocol.get_message_history(limit)
    
    def get_conversation_with(
        self,
        agent_id: str,
        other_agent: str
    ) -> List[Dict[str, Any]]:
        """Retorna conversa com outro agente"""
        protocol = self.get_or_create_protocol(agent_id)
        return protocol.get_conversation_with(other_agent)
    
    def get_stats(self, agent_id: str) -> Dict[str, Any]:
        """Retorna estatísticas do protocolo P2P de um agente"""
        protocol = self.get_or_create_protocol(agent_id)
        return protocol.get_stats()
