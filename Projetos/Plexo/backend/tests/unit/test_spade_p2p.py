# FEATURE: Multi-Agent Communication
# Testes unitários para protocolo P2P e conexão XMPP

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from app.spade.protocols.p2p_protocol import P2PProtocol, P2PMessage, MessageType
from app.spade.connection.xmpp_connection import XMPPConnectionManager, XMPPConfig


class TestXMPPConfig:
    """Testes para XMPPConfig"""
    
    def test_default_config(self):
        """Testa configuração padrão"""
        config = XMPPConfig()
        assert config.server == "localhost"
        assert config.port == 5222
        assert config.domain == "localhost"
        assert config.use_tls is False
    
    def test_get_jid(self):
        """Testa geração de JID"""
        config = XMPPConfig(domain="plexo.local")
        jid = config.get_jid("executor")
        assert jid == "executor@plexo.local"
    
    def test_custom_config(self):
        """Testa configuração customizada"""
        config = XMPPConfig(
            server="xmpp.example.com",
            port=5223,
            domain="example.com",
            use_tls=True
        )
        assert config.server == "xmpp.example.com"
        assert config.port == 5223
        assert config.domain == "example.com"
        assert config.use_tls is True


class TestP2PMessage:
    """Testes para P2PMessage"""
    
    def test_create_message(self):
        """Testa criação de mensagem"""
        msg = P2PMessage(
            from_agent="executor",
            to_agent="monitor",
            content="Test message",
            message_type=MessageType.DIRECT,
            urgency="MEDIUM"
        )
        assert msg.from_agent == "executor"
        assert msg.to_agent == "monitor"
        assert msg.content == "Test message"
        assert msg.message_type == MessageType.DIRECT
        assert msg.urgency == "MEDIUM"
        assert msg.requires_response is False
    
    def test_message_to_dict(self):
        """Testa conversão para dicionário"""
        msg = P2PMessage(
            from_agent="executor",
            to_agent="monitor",
            content="Test"
        )
        data = msg.to_dict()
        assert data["from_agent"] == "executor"
        assert data["to_agent"] == "monitor"
        assert data["content"] == "Test"
        assert "message_id" in data
        assert "timestamp" in data
    
    def test_message_from_dict(self):
        """Testa criação a partir de dicionário"""
        data = {
            "message_id": "test-123",
            "from_agent": "executor",
            "to_agent": "monitor",
            "content": "Test",
            "message_type": "direct",
            "urgency": "HIGH"
        }
        msg = P2PMessage.from_dict(data)
        assert msg.message_id == "test-123"
        assert msg.from_agent == "executor"
        assert msg.to_agent == "monitor"
        assert msg.urgency == "HIGH"
    
    def test_urgent_message(self):
        """Testa mensagem urgente"""
        msg = P2PMessage(
            from_agent="monitor",
            to_agent="executor",
            content="Alert!",
            message_type=MessageType.URGENT,
            urgency="CRITICAL",
            requires_response=True
        )
        assert msg.message_type == MessageType.URGENT
        assert msg.urgency == "CRITICAL"
        assert msg.requires_response is True
    
    def test_response_message(self):
        """Testa mensagem de resposta"""
        msg = P2PMessage(
            from_agent="monitor",
            to_agent="executor",
            content="Response",
            message_type=MessageType.RESPONSE,
            in_reply_to="original-123"
        )
        assert msg.message_type == MessageType.RESPONSE
        assert msg.in_reply_to == "original-123"


class TestMessageType:
    """Testes para MessageType enum"""
    
    def test_message_types(self):
        """Testa todos os tipos de mensagem"""
        assert MessageType.DIRECT.value == "direct"
        assert MessageType.REQUEST.value == "request"
        assert MessageType.RESPONSE.value == "response"
        assert MessageType.NOTIFICATION.value == "notification"
        assert MessageType.URGENT.value == "urgent"


class TestP2PProtocol:
    """Testes para P2PProtocol"""
    
    @pytest.fixture
    def mock_connection_manager(self):
        """Cria mock do connection manager"""
        manager = MagicMock()
        manager.send_message = AsyncMock(return_value={"success": True})
        manager.register_agent = AsyncMock(return_value={"success": True})
        manager.connect_agent = AsyncMock(return_value={"success": True})
        manager.disconnect_agent = AsyncMock(return_value=True)
        manager.get_connected_agents = MagicMock(return_value=["executor", "monitor"])
        manager.is_agent_connected = MagicMock(return_value=True)
        manager.get_agent_jid = MagicMock(return_value="executor@localhost")
        return manager
    
    @pytest.fixture
    def protocol(self, mock_connection_manager):
        """Cria protocolo P2P"""
        return P2PProtocol("executor", mock_connection_manager)
    
    def test_protocol_creation(self, protocol):
        """Testa criação do protocolo"""
        assert protocol.agent_id == "executor"
        assert len(protocol.pending_requests) == 0
        assert len(protocol.message_history) == 0
    
    @pytest.mark.asyncio
    async def test_send_direct_message(self, protocol, mock_connection_manager):
        """Testa envio de mensagem direta"""
        result = await protocol.send_direct_message(
            to_agent="monitor",
            content="Hello!",
            urgency="MEDIUM"
        )
        
        assert result.get("success") is True
        mock_connection_manager.send_message.assert_called_once()
        assert len(protocol.message_history) == 1
    
    @pytest.mark.asyncio
    async def test_send_request(self, protocol, mock_connection_manager):
        """Testa envio de request"""
        result = await protocol.send_request(
            to_agent="monitor",
            content="Need help",
            urgency="HIGH"
        )
        
        assert result.get("success") is True
        assert len(protocol.pending_requests) == 1
        assert len(protocol.message_history) == 1
    
    @pytest.mark.asyncio
    async def test_send_response(self, protocol, mock_connection_manager):
        """Testa envio de response"""
        result = await protocol.send_response(
            to_agent="monitor",
            original_message_id="test-123",
            content="Here is the answer"
        )
        
        assert result.get("success") is True
        assert len(protocol.message_history) == 1
    
    @pytest.mark.asyncio
    async def test_send_urgent_message(self, protocol, mock_connection_manager):
        """Testa envio de mensagem urgente"""
        result = await protocol.send_urgent_message(
            to_agent="monitor",
            content="Critical error!"
        )
        
        assert result.get("success") is True
        assert len(protocol.message_history) == 1
    
    @pytest.mark.asyncio
    async def test_send_notification(self, protocol, mock_connection_manager):
        """Testa envio de notificação"""
        result = await protocol.send_notification(
            to_agent="monitor",
            content="FYI: New task available"
        )
        
        assert result.get("success") is True
        assert len(protocol.message_history) == 1
    
    def test_get_pending_requests(self, protocol):
        """Testa obtenção de requests pendentes"""
        assert len(protocol.get_pending_requests()) == 0
    
    def test_get_message_history(self, protocol):
        """Testa obtenção de histórico"""
        assert len(protocol.get_message_history()) == 0
    
    def test_get_conversation_with(self, protocol):
        """Testa obtenção de conversa"""
        assert len(protocol.get_conversation_with("monitor")) == 0
    
    def test_get_stats(self, protocol):
        """Testa obtenção de estatísticas"""
        stats = protocol.get_stats()
        assert stats["agent_id"] == "executor"
        assert stats["total_messages"] == 0
        assert stats["pending_requests"] == 0


class TestXMPPConnectionManager:
    """Testes para XMPPConnectionManager"""
    
    @pytest.fixture
    def config(self):
        """Cria configuração de teste"""
        return XMPPConfig(domain="localhost")
    
    @pytest.fixture
    def manager(self, config):
        """Cria gerenciador de conexão"""
        return XMPPConnectionManager(config)
    
    def test_manager_creation(self, manager):
        """Testa criação do gerenciador"""
        assert manager.config.domain == "localhost"
        assert len(manager.connections) == 0
        assert manager.is_running is False
    
    def test_get_connected_agents_empty(self, manager):
        """Testa obtenção de agentes conectados vazio"""
        assert len(manager.get_connected_agents()) == 0
    
    def test_is_agent_connected_false(self, manager):
        """Testa verificação de agente não conectado"""
        assert manager.is_agent_connected("executor") is False
    
    def test_get_agent_jid_none(self, manager):
        """Testa obtenção de JID de agente não conectado"""
        assert manager.get_agent_jid("executor") is None
