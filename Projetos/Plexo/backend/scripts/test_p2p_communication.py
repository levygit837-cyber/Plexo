# FEATURE: Multi-Agent Communication
# Script de teste de comunicação P2P entre agentes

import asyncio
import logging
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.spade.connection.xmpp_connection import XMPPConnectionManager, XMPPConfig
from app.spade.protocols.p2p_protocol import P2PProtocol, P2PMessage, MessageType

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


AGENTES_TESTE = [
    {"username": "executor", "password": "executor123", "role": "Executor"},
    {"username": "monitor", "password": "monitor123", "role": "Monitor"},
    {"username": "specialist", "password": "specialist123", "role": "Specialist"},
    {"username": "coordinator", "password": "coordinator123", "role": "Coordinator"}
]


class AgentTester:
    """Classe para testar comunicação entre agentes"""
    
    def __init__(self):
        self.config = XMPPConfig(
            server="localhost",
            port=5222,
            domain="localhost"
        )
        self.connection_manager = XMPPConnectionManager(self.config)
        self.agents: Dict[str, P2PProtocol] = {}
        self.message_log: List[Dict[str, Any]] = []
    
    async def setup(self) -> bool:
        """Configura ambiente de teste"""
        logger.info("="*60)
        logger.info("INICIANDO TESTE DE COMUNICAÇÃO P2P ENTRE AGENTES")
        logger.info("="*60)
        
        for agente in AGENTES_TESTE:
            result = await self.connection_manager.register_agent(
                username=agente["username"],
                password=agente["password"]
            )
            
            if result.get("success"):
                logger.info(f"✓ Agente {agente['username']} registrado com JID: {result.get('jid')}")
            else:
                logger.error(f"✗ Falha ao registrar {agente['username']}: {result.get('error')}")
                return False
        
        return True
    
    async def connect_agents(self) -> bool:
        """Conecta todos os agentes"""
        logger.info("\n" + "="*60)
        logger.info("CONECTANDO AGENTES AO SERVIDOR XMPP")
        logger.info("="*60)
        
        for agente in AGENTES_TESTE:
            result = await self.connection_manager.connect_agent(
                username=agente["username"],
                password=agente["password"]
            )
            
            if result.get("success"):
                protocol = P2PProtocol(agente["username"], self.connection_manager)
                self.agents[agente["username"]] = protocol
                logger.info(f"✓ Agente {agente['username']} conectado com sucesso")
            else:
                logger.error(f"✗ Falha ao conectar {agente['username']}: {result.get('error')}")
                return False
        
        logger.info(f"\n✓ Total de {len(self.agents)} agentes conectados")
        return True
    
    async def test_direct_message(self) -> None:
        """Testa envio de mensagem direta"""
        logger.info("\n" + "="*60)
        logger.info("TESTE 1: MENSAGEM DIRETA (executor → monitor)")
        logger.info("="*60)
        
        executor = self.agents.get("executor")
        monitor = self.agents.get("monitor")
        
        if not executor or not monitor:
            logger.error("Agentes não encontrados")
            return
        
        result = await executor.send_direct_message(
            to_agent="monitor",
            content="Olá Monitor! Estou executando a tarefa de criação de função.",
            urgency="MEDIUM"
        )
        
        if result.get("success"):
            logger.info(f"✓ Mensagem enviada com sucesso")
            logger.info(f"  De: {result.get('from')}")
            logger.info(f"  Para: {result.get('to')}")
            logger.info(f"  Conteúdo: {result.get('content')}")
            logger.info(f"  Urgência: {result.get('urgency')}")
            self.message_log.append(result)
        else:
            logger.error(f"✗ Falha ao enviar mensagem: {result.get('error')}")
    
    async def test_request_response(self) -> None:
        """Testa envio de request e response"""
        logger.info("\n" + "="*60)
        logger.info("TESTE 2: REQUEST/RESPONSE (specialist → coordinator)")
        logger.info("="*60)
        
        specialist = self.agents.get("specialist")
        coordinator = self.agents.get("coordinator")
        
        if not specialist or not coordinator:
            logger.error("Agentes não encontrados")
            return
        
        result = await specialist.send_request(
            to_agent="coordinator",
            content="Preciso de autorização para modificar o arquivo config.py",
            urgency="HIGH"
        )
        
        if result.get("success"):
            logger.info(f"✓ Request enviada com sucesso")
            logger.info(f"  De: {result.get('from')}")
            logger.info(f"  Para: {result.get('to')}")
            logger.info(f"  Conteúdo: {result.get('content')}")
            logger.info(f"  Urgência: {result.get('urgency')}")
            self.message_log.append(result)
            
            await asyncio.sleep(1)
            
            response_result = await coordinator.send_response(
                to_agent="specialist",
                original_message_id=result.get("message_id", ""),
                content="Autorização concedida. Proceda com a modificação."
            )
            
            if response_result.get("success"):
                logger.info(f"✓ Response enviada com sucesso")
                logger.info(f"  De: {response_result.get('from')}")
                logger.info(f"  Para: {response_result.get('to')}")
                logger.info(f"  Conteúdo: {response_result.get('content')}")
                self.message_log.append(response_result)
        else:
            logger.error(f"✗ Falha ao enviar request: {result.get('error')}")
    
    async def test_urgent_message(self) -> None:
        """Testa envio de mensagem urgente"""
        logger.info("\n" + "="*60)
        logger.info("TESTE 3: MENSAGEM URGENTE (monitor → executor)")
        logger.info("="*60)
        
        monitor = self.agents.get("monitor")
        executor = self.agents.get("executor")
        
        if not monitor or not executor:
            logger.error("Agentes não encontrados")
            return
        
        result = await monitor.send_urgent_message(
            to_agent="executor",
            content="⚠️ ALERTA: Erro detectado na função calculate_sum() na linha 42. Checkpoint necessário!"
        )
        
        if result.get("success"):
            logger.info(f"✓ Mensagem URGENTE enviada com sucesso")
            logger.info(f"  De: {result.get('from')}")
            logger.info(f"  Para: {result.get('to')}")
            logger.info(f"  Conteúdo: {result.get('content')}")
            logger.info(f"  Urgência: {result.get('urgency')}")
            self.message_log.append(result)
        else:
            logger.error(f"✗ Falha ao enviar mensagem urgente: {result.get('error')}")
    
    async def test_notification(self) -> None:
        """Testa envio de notificação"""
        logger.info("\n" + "="*60)
        logger.info("TESTE 4: NOTIFICAÇÃO (coordinator → specialist)")
        logger.info("="*60)
        
        coordinator = self.agents.get("coordinator")
        specialist = self.agents.get("specialist")
        
        if not coordinator or not specialist:
            logger.error("Agentes não encontrados")
            return
        
        result = await coordinator.send_notification(
            to_agent="specialist",
            content="ℹ️ INFO: Nova tarefa disponível no whiteboard. Prioridade: Alta."
        )
        
        if result.get("success"):
            logger.info(f"✓ Notificação enviada com sucesso")
            logger.info(f"  De: {result.get('from')}")
            logger.info(f"  Para: {result.get('to')}")
            logger.info(f"  Conteúdo: {result.get('content')}")
            logger.info(f"  Urgência: {result.get('urgency')}")
            self.message_log.append(result)
        else:
            logger.error(f"✗ Falha ao enviar notificação: {result.get('error')}")
    
    async def test_conversation(self) -> None:
        """Testa conversa entre dois agentes"""
        logger.info("\n" + "="*60)
        logger.info("TESTE 5: CONVERSA (executor ↔ specialist)")
        logger.info("="*60)
        
        executor = self.agents.get("executor")
        specialist = self.agents.get("specialist")
        
        if not executor or not specialist:
            logger.error("Agentes não encontrados")
            return
        
        messages = [
            {"from": "executor", "to": "specialist", "content": "Especialista, preciso de ajuda com esta função.", "urgency": "MEDIUM"},
            {"from": "specialist", "to": "executor", "content": "Claro! Qual é o problema?", "urgency": "MEDIUM"},
            {"from": "executor", "to": "specialist", "content": "A função não está retornando o valor esperado.", "urgency": "MEDIUM"},
            {"from": "specialist", "to": "executor", "content": "Vou verificar. Pode me enviar o código?", "urgency": "MEDIUM"},
            {"from": "executor", "to": "specialist", "content": "Aqui está: def calculate_sum(a, b): return a + b", "urgency": "MEDIUM"},
            {"from": "specialist", "to": "executor", "content": "Encontrei o erro! Faltou o return. Corrigido!", "urgency": "HIGH"}
        ]
        
        for msg in messages:
            agent = self.agents.get(msg["from"])
            if agent:
                result = await agent.send_direct_message(
                    to_agent=msg["to"],
                    content=msg["content"],
                    urgency=msg["urgency"]
                )
                
                if result.get("success"):
                    logger.info(f"✓ [{msg['from']} → {msg['to']}] {msg['content'][:50]}...")
                    self.message_log.append(result)
                
                await asyncio.sleep(0.5)
    
    async def show_stats(self) -> None:
        """Mostra estatísticas finais"""
        logger.info("\n" + "="*60)
        logger.info("ESTATÍSTICAS FINAIS")
        logger.info("="*60)
        
        for username, protocol in self.agents.items():
            stats = protocol.get_stats()
            logger.info(f"\nAgente: {username}")
            logger.info(f"  Total de mensagens: {stats['total_messages']}")
            logger.info(f"  Requests pendentes: {stats['pending_requests']}")
            logger.info(f"  Handlers registrados: {stats['response_handlers']}")
        
        logger.info(f"\nTotal de mensagens no log: {len(self.message_log)}")
        
        connected = self.connection_manager.get_connected_agents()
        logger.info(f"Agentes conectados: {', '.join(connected)}")
    
    async def cleanup(self) -> None:
        """Limpa recursos"""
        logger.info("\n" + "="*60)
        logger.info("LIMPANDO RECURSOS")
        logger.info("="*60)
        
        for username in list(self.agents.keys()):
            await self.connection_manager.disconnect_agent(username)
            logger.info(f"✓ Agente {username} desconectado")
        
        logger.info("\n✓ Todos os agentes desconectados")
    
    async def run(self) -> None:
        """Executa todos os testes"""
        try:
            if not await self.setup():
                logger.error("Falha na configuração. Abortando.")
                return
            
            if not await self.connect_agents():
                logger.error("Falha na conexão. Abortando.")
                return
            
            await asyncio.sleep(2)
            
            await self.test_direct_message()
            await asyncio.sleep(1)
            
            await self.test_request_response()
            await asyncio.sleep(1)
            
            await self.test_urgent_message()
            await asyncio.sleep(1)
            
            await self.test_notification()
            await asyncio.sleep(1)
            
            await self.test_conversation()
            await asyncio.sleep(1)
            
            await self.show_stats()
            
            await self.cleanup()
            
            logger.info("\n" + "="*60)
            logger.info("✓ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
            logger.info("="*60)
        
        except Exception as e:
            logger.error(f"Erro durante execução dos testes: {e}")
            import traceback
            traceback.print_exc()


async def main():
    """Função principal"""
    tester = AgentTester()
    await tester.run()


if __name__ == "__main__":
    asyncio.run(main())
