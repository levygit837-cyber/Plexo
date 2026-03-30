# FEATURE: Multi-Agent Communication
# Serviço para gerenciar conexões XMPP

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from app.spade.connection.xmpp_connection import XMPPConnectionManager, XMPPConfig
from app.config.settings import get_settings

logger = logging.getLogger(__name__)


class XMPPService:
    """Serviço para gerenciar conexões XMPP"""
    
    def __init__(self):
        settings = get_settings()
        self.config = XMPPConfig(
            server=getattr(settings, 'XMPP_SERVER', 'localhost'),
            port=getattr(settings, 'XMPP_PORT', 5222),
            domain=getattr(settings, 'XMPP_DOMAIN', 'localhost')
        )
        self.connection_manager = XMPPConnectionManager(self.config)
        logger.info(f"XMPPService inicializado com servidor: {self.config.server}:{self.config.port}")
    
    async def register_agent(self, username: str, password: str) -> Dict[str, Any]:
        """Registra um novo agente no servidor XMPP"""
        try:
            result = await self.connection_manager.register_agent(username, password)
            if result.get("success"):
                logger.info(f"Agente {username} registrado com sucesso")
            else:
                logger.error(f"Falha ao registrar agente {username}: {result.get('error')}")
            return result
        except Exception as e:
            logger.error(f"Erro ao registrar agente {username}: {e}")
            return {"success": False, "error": str(e)}
    
    async def connect_agent(self, username: str, password: str) -> Dict[str, Any]:
        """Conecta um agente ao servidor XMPP"""
        try:
            result = await self.connection_manager.connect_agent(username, password)
            if result.get("success"):
                logger.info(f"Agente {username} conectado com sucesso")
            else:
                logger.error(f"Falha ao conectar agente {username}: {result.get('error')}")
            return result
        except Exception as e:
            logger.error(f"Erro ao conectar agente {username}: {e}")
            return {"success": False, "error": str(e)}
    
    async def disconnect_agent(self, username: str) -> bool:
        """Desconecta um agente do servidor XMPP"""
        try:
            result = await self.connection_manager.disconnect_agent(username)
            if result:
                logger.info(f"Agente {username} desconectado com sucesso")
            else:
                logger.error(f"Falha ao desconectar agente {username}")
            return result
        except Exception as e:
            logger.error(f"Erro ao desconectar agente {username}: {e}")
            return False
    
    async def send_message(
        self,
        from_username: str,
        to_username: str,
        content: str,
        urgency: str = "MEDIUM"
    ) -> Dict[str, Any]:
        """Envia mensagem entre agentes"""
        try:
            result = await self.connection_manager.send_message(
                from_username=from_username,
                to_username=to_username,
                content=content,
                urgency=urgency
            )
            if result.get("success"):
                logger.info(f"Mensagem enviada de {from_username} para {to_username}")
            else:
                logger.error(f"Falha ao enviar mensagem: {result.get('error')}")
            return result
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
            return {"success": False, "error": str(e)}
    
    def get_connected_agents(self) -> List[str]:
        """Retorna lista de agentes conectados"""
        return self.connection_manager.get_connected_agents()
    
    def is_agent_connected(self, username: str) -> bool:
        """Verifica se um agente está conectado"""
        return self.connection_manager.is_agent_connected(username)
    
    def get_agent_jid(self, username: str) -> Optional[str]:
        """Retorna JID de um agente"""
        return self.connection_manager.get_agent_jid(username)
    
    def get_config(self) -> Dict[str, Any]:
        """Retorna configuração do serviço"""
        return {
            "server": self.config.server,
            "port": self.config.port,
            "domain": self.config.domain,
            "use_tls": self.config.use_tls,
            "use_ssl": self.config.use_ssl
        }
