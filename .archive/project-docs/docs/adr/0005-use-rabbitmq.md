# 0005. Use RabbitMQ for Async Tasks

Data: 2026-01-19

Status: Aceito

## Contexto

O sistema Plexo precisa processar tarefas de forma assíncrona para não bloquear a API e melhorar a experiência do usuário. Os requisitos incluem:

- Processamento assíncrono de tarefas longas
- Desacoplamento entre API e workers
- Garantia de entrega de mensagens
- Retry automático em caso de falhas
- Dead letter queues para mensagens problemáticas
- Escalabilidade horizontal de workers
- Priorização de tarefas
- Monitoramento de filas

## Decisão

Decidimos usar **RabbitMQ** como message broker para processamento assíncrono de tarefas.

### Razões

1. **Message Broker Maduro**: 15+ anos de desenvolvimento, battle-tested em produção
2. **Garantia de Entrega**: Acknowledgments e persistência de mensagens
3. **Routing Flexível**: Exchanges (direct, topic, fanout, headers) e bindings
4. **Dead Letter Queues**: Tratamento automático de mensagens com falha
5. **Prioridades**: Suporte a priorização de mensagens
6. **TTL**: Time-to-live para mensagens e filas
7. **Management UI**: Interface web para monitoramento e administração
8. **Plugins**: Ecossistema rico (delayed messages, federation, shovel)
9. **Clustering**: Suporte nativo a alta disponibilidade
10. **AMQP Protocol**: Protocolo padrão, interoperável com outras linguagens

## Consequências

### Positivas

- **Desacoplamento**: API e workers completamente independentes
- **Escalabilidade**: Adicionar workers horizontalmente sem mudanças no código
- **Resiliência**: Retry automático e dead letter queues
- **Performance**: API responde imediatamente, processamento em background
- **Observabilidade**: Management UI mostra estado das filas em tempo real
- **Flexibilidade**: Diferentes tipos de exchanges para diferentes padrões
- **Garantias**: Mensagens não são perdidas mesmo com crashes
- **Priorização**: Tarefas críticas processadas primeiro

### Negativas

- **Infraestrutura Adicional**: Requer servidor RabbitMQ separado
- **Complexidade**: Mais componentes para gerenciar e monitorar
- **Latência**: Overhead de rede entre API e RabbitMQ
- **Debugging**: Mais difícil debugar fluxos assíncronos
- **Consistência Eventual**: Dados podem estar temporariamente inconsistentes
- **Custos**: Recursos adicionais de infraestrutura

## Alternativas Consideradas

### Celery + Redis

- **Prós**: Celery é popular em Python, Redis é rápido
- **Contras**: Redis não garante entrega, sem dead letter queues nativas
- **Rejeitado**: Falta de garantias de entrega é crítica para nosso caso

### AWS SQS

- **Prós**: Gerenciado, escalável, sem servidor para manter
- **Contras**: Vendor lock-in, latência maior, custos variáveis
- **Rejeitado**: Preferimos solução self-hosted e agnóstica de cloud

### Apache Kafka

- **Prós**: Alta throughput, streaming de eventos, retenção longa
- **Contras**: Overhead de infraestrutura, complexo para casos simples
- **Rejeitado**: Overkill para nosso volume de mensagens

### Redis Streams

- **Prós**: Rápido, já usamos Redis para cache
- **Contras**: Menos maduro que RabbitMQ, ferramentas limitadas
- **Rejeitado**: RabbitMQ tem melhor suporte a padrões de messaging

### Google Cloud Tasks

- **Prós**: Gerenciado, integração com GCP
- **Contras**: Vendor lock-in, custos variáveis
- **Rejeitado**: Preferimos solução self-hosted

## Implementação

### Arquitetura

```
┌─────────┐      ┌──────────┐      ┌─────────┐
│ FastAPI │─────▶│ RabbitMQ │─────▶│ Workers │
│   API   │      │  Broker  │      │ (Async) │
└─────────┘      └──────────┘      └─────────┘
     │                 │                 │
     │                 │                 │
     ▼                 ▼                 ▼
┌──────────────────────────────┐
│           PostgreSQL Database            │
└──────────────────────────────────────────┘
```

### Configuração

```python
# backend/app/config/rabbitmq.py
from aio_pika import connect_robust, ExchangeType

async def get_rabbitmq_connection():
    return await connect_robust(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        login=settings.RABBITMQ_USER,
        password=settings.RABBITMQ_PASSWORD,
    )

async def setup_queues(channel):
    # Exchange principal
    exchange = await channel.declare_exchange(
        "plexo.tasks",
        ExchangeType.TOPIC,
        durable=True
    )
    
    # Fila de tarefas de agentes
    agent_queue = await channel.declare_queue(
        "agent.tasks",
        durable=True,
        arguments={
            "x-dead-letter-exchange": "plexo.dlx",
            "x-message-ttl": 3600000,  # 1 hora
        }
    )
    
    await agent_queue.bind(exchange, routing_key="agent.*")
```

### Producer (API)

```python
# backend/app/queues/producer.py
class QueueProducer:
    async def publish_task(
        self,
        routing_key: str,
        message: dict,
        priority: int = 0
    ):
        await self.exchange.publish(
            Message(
                body=json.dumps(message).encode(),
                priority=priority,
                delivery_mode=DeliveryMode.PERSISTENT,
            ),
            routing_key=routing_key
        )
```

### Consumer (Worker)

```python
# backend/app/queues/consumer.py
class QueueConsumer:
    async def consume(self, queue_name: str):
        queue = await self.channel.get_queue(queue_name)
        
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        await self.process_message(message)
                    except Exception as e:
                        logger.error(f"Error processing: {e}")
                        # Mensagem vai para DLQ automaticamente
                        raise
```

### Tipos de Tarefas

**Tarefas de Agentes:**

- `agent.create` - Criar novo agente
- `agent.execute` - Executar tarefa de agente
- `agent.message` - Processar mensagem entre agentes

**Tarefas de Background:**

- `task.process` - Processar tarefas pendentes
- `task.cleanup` - Limpar tarefas antigas
- `metrics.collect` - Coletar métricas

**Tarefas de Notificação:**

- `notification.send` - Enviar notificações
- `email.send` - Enviar emails

### Dead Letter Queue

```python
# Configurar DLX (Dead Letter Exchange)
dlx = await channel.declare_exchange(
    "plexo.dlx",
    ExchangeType.FANOUT,
    durable=True
)

dlq = await channel.declare_queue(
    "dead.letters",
    durable=True
)

await dlq.bind(dlx)
```

### Monitoramento

- **Management UI**: <http://localhost:15672>
- **Métricas**: Prometheus exporter para RabbitMQ
- **Alertas**: Alertas quando filas crescem muito
- **Logs**: Logs estruturados de processamento

## Integração com SPADE

RabbitMQ é usado para tarefas assíncronas, enquanto SPADE/XMPP é usado para comunicação entre agentes:

- **RabbitMQ**: Tarefas de background, processamento assíncrono
- **SPADE/XMPP**: Comunicação em tempo real entre agentes

```python
# API recebe requisição
@router.post("/agents/{agent_id}/execute")
async def execute_agent_task(agent_id: str, task: TaskCreate):
    # Publicar tarefa no RabbitMQ
    await producer.publish_task(
        routing_key="agent.execute",
        message={"agent_id": agent_id, "task": task.dict()}
    )
    return {"status": "queued"}

# Worker processa tarefa
async def process_agent_task(message: dict):
    agent_id = message["agent_id"]
    
    # Enviar mensagem XMPP para o agente
    await spade_agent.send_message(
        to=f"{agent_id}@localhost",
        body=json.dumps(message["task"])
    )
```

## Referências

- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [AMQP Protocol](https://www.amqp.org/)
- [aio-pika Documentation](https://aio-pika.readthedocs.io/)
- [RabbitMQ Best Practices](https://www.rabbitmq.com/best-practices.html)
