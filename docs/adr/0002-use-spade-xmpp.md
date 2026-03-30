# 0002. Use SPADE for Agent Communication

Data: 2026-01-16

Status: Aceito

## Contexto

O sistema Plexo requer comunicação eficiente e confiável entre múltiplos agentes inteligentes. Os agentes precisam:

- Trocar mensagens de forma assíncrona
- Descobrir outros agentes dinamicamente
- Suportar diferentes padrões de comunicação (request-response, publish-subscribe)
- Manter histórico de conversas
- Garantir entrega de mensagens

## Decisão

Decidimos usar **SPADE (Smart Python Agent Development Environment)** com protocolo **XMPP** para comunicação entre agentes.

### Razões:

1. **Protocolo Padrão**: XMPP é um protocolo aberto e bem estabelecido para mensagens
2. **SPADE Framework**: Framework Python específico para sistemas multi-agentes
3. **Behaviors**: Sistema de behaviors facilita implementação de padrões de comunicação
4. **Presença**: Suporte nativo a presença e descoberta de agentes
5. **Escalabilidade**: XMPP escala bem para muitos agentes
6. **Histórico**: Mensagens podem ser armazenadas e recuperadas
7. **Segurança**: Suporte a TLS e autenticação

## Consequências

### Positivas

- Comunicação assíncrona e não-bloqueante entre agentes
- Descoberta automática de agentes via presença XMPP
- Padrões de comunicação bem definidos (behaviors)
- Histórico de mensagens para análise e debugging
- Integração com servidores XMPP existentes (ejabberd, Prosody)
- Suporte a múltiplos tipos de mensagens (chat, groupchat, etc.)

### Negativas

- Requer servidor XMPP adicional (ejabberd)
- Curva de aprendizado do protocolo XMPP
- Overhead de XML para mensagens (mitigado com compressão)
- Debugging pode ser mais complexo

## Alternativas Consideradas

### RabbitMQ Direto
- **Prós**: Já usamos para tarefas assíncronas, alta performance
- **Contras**: Não tem conceito de presença, mais baixo nível
- **Rejeitado**: Falta de features específicas para agentes

### Redis Pub/Sub
- **Prós**: Simples, rápido, já usamos Redis
- **Contras**: Sem garantia de entrega, sem histórico, sem presença
- **Rejeitado**: Muito básico para comunicação entre agentes

### gRPC
- **Prós**: Alta performance, type-safe, streaming bidirecional
- **Contras**: Mais complexo, sem presença, requer definição de proto
- **Rejeitado**: Overhead de manutenção de schemas proto

### WebSockets Customizado
- **Prós**: Controle total, flexível
- **Contras**: Precisaríamos implementar tudo do zero
- **Rejeitado**: Reinventar a roda, XMPP já resolve

## Implementação

### Servidor XMPP

Usaremos **ejabberd** como servidor XMPP:
- Maduro e estável
- Alta performance
- Fácil configuração com Docker
- Suporte a clustering

### Integração

```python
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

class PlexoAgent(Agent):
    class MessageBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                await self.process_message(msg)
```

## Referências

- [SPADE Documentation](https://spade-mas.readthedocs.io/)
- [XMPP Standards](https://xmpp.org/)
- [ejabberd Documentation](https://docs.ejabberd.im/)
- [Multi-Agent Systems with SPADE](https://github.com/javipalanca/spade)
