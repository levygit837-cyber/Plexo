# FEATURE: Multi-Agent Communication
# Gerenciador de conexão XMPP para agentes SPADE

import logging
import asyncio
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class XMPPConfig:
    """Configuração de conexão XMPP"""
    server: str = "localhost"
    port: int = 5222
    domain: str = "localhost"
    use_tls: bool = False
    use_ssl: bool = False
    
    def get_jid(self, username: str) -> str:
        """Gera JID completo para um usuário"""
        return f"{username}@{self.domain}"


class XMPPConnectionManager:
    """Gerenciador de conexões XMPP para agentes"""
    
    def __init__(self, config: XMPPConfig):
        self.config = config
        self.connections: Dict[str, Any] = {}
        self.message_handlers: Dict[str, List[Callable]] = {}
        self.is_running: bool = False
    
    async def register_agent(self, username: str, password: str) -> Dict[str, Any]:
        """Registra um novo agente no servidor XMPP"""
        jid = self.config.get_jid(username)
        
        try:
            import aioxmpp
            
            jid_obj = aioxmpp.JID.fromstr(jid)
            
            registrar = aioxmpp.RegistrationService(jid_obj.localpart, aioxmpp.make_security_layer(password))
            
            form = await registrar.get_registration_form()
            
            form.fields["username"] = username
            form.fields["password"] = password
            
            await registrar.submit_form(form)
            
            logger.info(f"Agente {username} registrado com sucesso")
            
            return {
                "success": True,
                "jid": jid,
                "username": username,
                "message": f"Agente {username} registrado com sucesso"
            }
        
        except Exception as e:
            logger.error(f"Erro ao registrar agente {username}: {e}")
            return {
                "success": False,
                "jid": jid,
                "username": username,
                "error": str(e)
            }
    
    async def connect_agent(self, username: str, password: str, message_handler: Optional[Callable] = None) -> Dict[str, Any]:
        """Conecta um agente ao servidor XMPP"""
        jid = self.config.get_jid(username)
        
        try:
            import aioxmpp
            
            jid_obj = aioxmpp.JID.fromstr(jid)
            
            client = aioxmpp.PresenceManagedClient(
                jid_obj,
                aioxmpp.make_security_layer(password)
            )
            
            async with client.connected() as stream:
                presence = aioxmpp.Presence()
                presence.show = aioxmpp.PresenceShow.CHAT
                presence.status = {None: "Online"}
                await stream.send(presence)
                
                self.connections[username] = {
                    "client": client,
                    "stream": stream,
                    "jid": jid,
                    "connected_at": datetime.now()
                }
                
                if message_handler:
                    self.message_handlers[username] = [message_handler]
                
                logger.info(f"Agente {username} conectado com sucesso")
                
                return {
                    "success": True,
                    "jid": jid,
                    "username": username,
                    "message": f"Agente {username} conectado com sucesso"
                }
        
        except Exception as e:
            logger.error(f"Erro ao conectar agente {username}: {e}")
            return {
                "success": False,
                "jid": jid,
                "username": username,
                "error": str(e)
            }
    
    async def send_message(self, from_username: str, to_username: str, content: str, urgency: str = "MEDIUM") -> Dict[str, Any]:
        """Envia mensagem de um agente para outro"""
        from_jid = self.config.get_jid(from_username)
        to_jid = self.config.get_jid(to_username)
        
        if from_username not in self.connections:
            return {
                "success": False,
                "error": f"Agente {from_username} não está conectado"
            }
        
        try:
            import aioxmpp
            
            msg = aioxmpp.Message(to=aioxmpp.JID.fromstr(to_jid), type_=aioxmpp.MessageType.CHAT)
            msg.body[None] = content
            
            msg_xep = aioxmpp.xso.model.ChildList([aioxmpp.xso.ChildText("urgency", text=urgency)])
            
            conn = self.connections[from_username]
            await conn["stream"].send(msg)
            
            logger.info(f"Mensagem enviada de {from_username} para {to_username}: {content[:50]}...")
            
            return {
                "success": True,
                "from": from_jid,
                "to": to_jid,
                "content": content,
                "urgency": urgency,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def disconnect_agent(self, username: str) -> bool:
        """Desconecta um agente do servidor XMPP"""
        if username in self.connections:
            try:
                conn = self.connections[username]
                
                presence = aioxmpp.Presence(type_=aioxmpp.PresenceType.UNAVAILABLE)
                await conn["stream"].send(presence)
                
                del self.connections[username]
                
                if username in self.message_handlers:
                    del self.message_handlers[username]
                
                logger.info(f"Agente {username} desconectado")
                return True
            
            except Exception as e:
                logger.error(f"Erro ao desconectar agente {username}: {e}")
                return False
        
        return False
    
    def get_connected_agents(self) -> List[str]:
        """Retorna lista de agentes conectados"""
        return list(self.connections.keys())
    
    def is_agent_connected(self, username: str) -> bool:
        """Verifica se um agente está conectado"""
        return username in self.connections
    
    def get_agent_jid(self, username: str) -> Optional[str]:
        """Retorna JID de um agente"""
        if username in self.connections:
            return self.connections[username]["jid"]
        return None
