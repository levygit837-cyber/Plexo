# 0009. Real-time Communication Protocol

Data: 2026-03-29

Status: Aceito

## Contexto

O sistema Plexo precisa de um protocolo de comunicação em tempo real entre agentes que suporte:

- Mensagens diretas entre dois agentes (1:1)
- Chat em grupo com múltiplos agentes (1:N)
- Baixa latência para interações síncronas
- Garantia de entrega de mensagens
- Ordenação correta de mensagens
- Suporte a diferentes tipos de conteúdo
- Histórico de conversas
- Presença e status de agentes

## Decisão

Decidimos implementar um **protocolo de comunicação dual** usando XMPP via SPADE, com dois modos distintos:

### 1. Modo de Comunicação: Mensagens Diretas (1:1)

#### Protocolo
- **Base**: XMPP direto via SPADE
- **Formato**: Stanza XMPP `<message>`
- **Garantias**: Entrega garantida, ordenação FIFO
- **Latência**: < 100ms para mensagens locais

#### Message Structure
```python
@dataclass
class DirectMessage:
    """Mensagem direta entre dois agentes"""
    message_id: str
    sender_id: str
    receiver_id: str
    content: str
    message_type: MessageType
    timestamp: datetime
    metadata: Dict[str, Any]
    reply_to: Optional[str] = None
    attachments: List[Attachment] = []
```

#### Message Types
```python
class MessageType(Enum):
    # Comunicação geral
    TEXT = "text"                    # Texto simples
    CODE = "code"                    # Bloco de código
    FILE = "file"                    # Arquivo anexo
    IMAGE = "image"                  # Imagem
    
    # Comandos e ações
    REQUEST = "request"              # Solicitação de ação
    RESPONSE = "response"            # Resposta a solicitação
    COMMAND = "command"              # Comando direto
    
    # Status e controle
    STATUS = "status"                # Atualização de status
    HEARTBEAT = "heartbeat"          # Manter conexão viva
    ACK = "ack"                      # Confirmação de recebimento
    NACK = "nack"                    # Não confirmação
    
    # Colaboração
    QUESTION = "question"            # Pergunta
    ANSWER = "answer"                # Resposta
    SUGGESTION = "suggestion"        # Sugestão
    FEEDBACK = "feedback"            # Feedback
    
    # Artefatos
    ARTIFACT_CREATE = "artifact_create"    # Criar artefato
    ARTIFACT_UPDATE = "artifact_update"    # Atualizar artefato
    ARTIFACT_DELETE = "artifact_delete"    # Deletar artefato
```

#### Communication Flow
```
┌─────────┐                    ┌─────────┐
│ Agent A │                    │ Agent B │
└────┬────┘                    └────┬────┘
     │                              │
     │ 1. Send message              │
     │─────────────────────────────►│
     │                              │
     │ 2. ACK (automatic)           │
     │◄─────────────────────────────│
     │                              │
     │ 3. Process message           │
     │                              │
     │ 4. Send response             │
     │◄─────────────────────────────│
     │                              │
     │ 5. ACK (automatic)           │
     │─────────────────────────────►│
```

### 2. Modo de Comunicação: Chat em Grupo (1:N)

#### Protocolo
- **Base**: XMPP MUC (Multi-User Chat) via SPADE
- **Formato**: Sala de chat persistente
- **Participantes**: Múltiplos agentes simultaneamente
- **Persistência**: Histórico mantido por sessão

#### Group Chat Structure
```python
@dataclass
class GroupChat:
    """Chat em grupo entre múltiplos agentes"""
    chat_id: str
    name: str
    description: str
    participants: List[str]  # agent_ids
    created_at: datetime
    created_by: str
    is_persistent: bool
    max_participants: int
    metadata: Dict[str, Any]
    artifacts: List[Artifact] = []
```

#### Group Message Structure
```python
@dataclass
class GroupMessage:
    """Mensagem em chat de grupo"""
    message_id: str
    chat_id: str
    sender_id: str
    content: str
    message_type: MessageType
    timestamp: datetime
    mentions: List[str] = []      # agent_ids mencionados
    reply_to: Optional[str] = None
    reactions: Dict[str, List[str]] = {}  # emoji → [agent_ids]
    thread_id: Optional[str] = None
    attachments: List[Attachment] = []
```

#### Group Chat Features

**1. Menções**
```python
# Agente pode mencionar outros agentes
"@coder pode implementar essa função?"
"@researcher preciso de documentação sobre X"
"@all vamos discutir a arquitetura?"
```

**2. Threads**
```python
# Mensagens podem criar threads de discussão
original_msg = "Como implementamos autenticação?"
thread_msg1 = "Podemos usar JWT"
thread_msg2 = "Prefiro OAuth2"
thread_msg3 = "Votemos: JWT vs OAuth2"
```

**3. Reações**
```python
# Agentes podem reagir a mensagens
👍 - Concordo
👎 - Discordo
✅ - Implementado
❌ - Rejeitado
❓ - Preciso de esclarecimento
```

**4. Artefatos Colaborativos**
```python
@dataclass
class Artifact:
    """Artefato criado durante discussão"""
    artifact_id: str
    chat_id: str
    name: str
    content: str
    artifact_type: ArtifactType
    created_by: str
    created_at: datetime
    updated_at: datetime
    version: int
    collaborators: List[str]
    comments: List[Comment]

class ArtifactType(Enum):
    CODE = "code"                    # Código fonte
    DOCUMENT = "document"            # Documentação
    DIAGRAM = "diagram"             # Diagrama
    PROPOSAL = "proposal"           # Proposta de solução
    REVIEW = "review"               # Revisão de código
    TEST = "test"                   # Caso de teste
    CONFIG = "config"               # Configuração
```

**5. Pesquisa Web Integrada**
```python
# Agentes podem pesquisar durante discussão
"/search Como implementar WebSocket em FastAPI?"
"/docs FastAPI WebSocket documentation"
"/stackoverflow Python async best practices"
```

#### Chat Workflow
```
┌─────────────────────────────────────────────────────────┐
│                    Group Chat Room                       │
├─────────────────────────────────────────────────────────┤
│  Agent A: "Como implementamos autenticação?"          │
│  Agent B: "@researcher pode pesquisar JWT vs OAuth2?" │
│  Agent C: "Vou pesquisar..."                           │
│  Agent C: "/search JWT vs OAuth2 comparison"          │
│  Agent C: "Aqui estão os resultados: ..."             │
│  Agent A: "Vamos criar um artefato com a decisão"     │
│  Agent A: [Cria artefato: AUTH_DECISION.md]           │
│  Agent B: "Concordo com OAuth2" 👍                    │
│  Agent C: "Também concordo" 👍                        │
│  Agent A: "Decisão tomada! Vamos implementar"         │
└─────────────────────────────────────────────────────────┘
```

### 3. Presence and Status

#### Agent Presence
```python
class AgentPresence:
    """Status de presença de um agente"""
    agent_id: str
    status: PresenceStatus
    status_message: Optional[str]
    last_seen: datetime
    current_chat: Optional[str]
    current_task: Optional[str]
    capabilities_available: List[str]

class PresenceStatus(Enum):
    ONLINE = "online"              # Disponível
    BUSY = "busy"                  # Ocupado
    AWAY = "away"                  # Ausente
    DO_NOT_DISTURB = "dnd"         # Não perturbe
    OFFLINE = "offline"            # Desconectado
```

#### Presence Protocol
```python
class PresenceManager:
    """Gerencia presença de agentes"""
    
    async def broadcast_presence(
        self,
        agent: Agent,
        status: PresenceStatus
    ):
        """Broadcast status de presença"""
        pass
    
    async def get_agent_presence(
        self,
        agent_id: str
    ) -> AgentPresence:
        """Obtém presença de agente"""
        pass
    
    async def subscribe_to_presence(
        self,
        subscriber: Agent,
        target: Agent
    ):
        """Inscreve para receber atualizações de presença"""
        pass
```

### 4. Message Routing and Delivery

#### Router
```python
class MessageRouter:
    """Roteia mensagens entre agentes"""
    
    async def route_message(
        self,
        message: Union[DirectMessage, GroupMessage]
    ) -> bool:
        """Roteia mensagem para destino correto"""
        if isinstance(message, DirectMessage):
            return await self._route_direct(message)
        else:
            return await self._route_group(message)
    
    async def _route_direct(
        self,
        message: DirectMessage
    ) -> bool:
        """Roteia mensagem direta"""
        # Verifica se receptor está online
        presence = await self.presence_manager.get_agent_presence(
            message.receiver_id
        )
        
        if presence.status == PresenceStatus.OFFLINE:
            # Armazena para entrega posterior
            await self.store_offline_message(message)
            return False
        
        # Envia mensagem
        return await self.send_to_agent(message.receiver_id, message)
    
    async def _route_group(
        self,
        message: GroupMessage
    ) -> bool:
        """Roteia mensagem de grupo"""
        # Obtém participantes do chat
        chat = await self.get_group_chat(message.chat_id)
        
        # Envia para todos os participantes
        for participant_id in chat.participants:
            if participant_id != message.sender_id:
                await self.send_to_agent(participant_id, message)
        
        return True
```

#### Delivery Guarantees

**1. At-least-once Delivery**
- Mensagens são reenviadas até receber ACK
- Timeout de 30 segundos para ACK
- Máximo de 3 tentativas

**2. Ordering**
- Mensagens ordenadas por timestamp
- Sequence numbers para garantir ordem
- Buffer para mensagens fora de ordem

**3. Deduplication**
- Message IDs únicos
- Cache de mensagens recentes
- Detecção e descarte de duplicatas

### 5. Security and Authentication

#### Authentication
```python
class MessageAuthentication:
    """Autenticação de mensagens"""
    
    def sign_message(
        self,
        message: Union[DirectMessage, GroupMessage],
        sender_private_key: str
    ) -> str:
        """Assina mensagem com chave privada"""
        pass
    
    def verify_signature(
        self,
        message: Union[DirectMessage, GroupMessage],
        signature: str,
        sender_public_key: str
    ) -> bool:
        """Verifica assinatura da mensagem"""
        pass
```

#### Encryption
```python
class MessageEncryption:
    """Criptografia de mensagens"""
    
    def encrypt_message(
        self,
        message: str,
        recipient_public_key: str
    ) -> str:
        """Criptografa mensagem"""
        pass
    
    def decrypt_message(
        self,
        encrypted_message: str,
        recipient_private_key: str
    ) -> str:
        """Descriptografa mensagem"""
        pass
```

#### Authorization
```python
class MessageAuthorization:
    """Autorização de mensagens"""
    
    def can_send_to_agent(
        self,
        sender: Agent,
        receiver: Agent
    ) -> bool:
        """Verifica se sender pode enviar para receiver"""
        pass
    
    def can_join_chat(
        self,
        agent: Agent,
        chat: GroupChat
    ) -> bool:
        """Verifica se agente pode entrar no chat"""
        pass
```

### 6. Monitoring and Metrics

#### Metrics
```python
class CommunicationMetrics:
    """Métricas de comunicação"""
    
    # Latência
    direct_message_latency: Histogram
    group_message_latency: Histogram
    
    # Throughput
    messages_per_second: Gauge
    
    # Entrega
    delivery_success_rate: Gauge
    delivery_failure_rate: Gauge
    
    # Chat
    active_chats: Gauge
    messages_per_chat: Counter
    
    # Presença
    online_agents: Gauge
    busy_agents: Gauge
```

#### Logging
```python
class CommunicationLogger:
    """Logger para comunicação"""
    
    def log_message_sent(
        self,
        message: Union[DirectMessage, GroupMessage]
    ):
        pass
    
    def log_message_received(
        self,
        message: Union[DirectMessage, GroupMessage]
    ):
        pass
    
    def log_message_failed(
        self,
        message: Union[DirectMessage, GroupMessage],
        error: str
    ):
        pass
```

## Consequências

### Positivas
- **Flexibilidade**: Dois modos de comunicação distintos
- **Colaboração**: Chat em grupo facilita discussões
- **Artefatos**: Agentes podem criar artefatos juntos
- **Presença**: Saber quando agentes estão disponíveis
- **Escalabilidade**: XMPP suporta muitos agentes
- **Padronização**: XMPP é protocolo bem estabelecido

### Negativas
- **Complexidade**: Sistema mais complexo de implementar
- **Overhead**: Chat em grupo tem mais overhead
- **Persistência**: Gerenciar histórico de chats
- **Segurança**: Mais vetores de ataque

### Mitigações
- **Cache**: Cache de mensagens para performance
- **Limites**: Limitar número de participantes por chat
- **Monitoramento**: Métricas para detectar problemas
- **Auditoria**: Log de todas as comunicações

## Alternativas Consideradas

### 1. Apenas Mensagens Diretas (Rejeitada)
- Só comunicação 1:1
- Problema: Sem discussão em grupo, menos colaboração

### 2. Apenas Chat em Grupo (Rejeitada)
- Só comunicação 1:N
- Problema: Sem privacidade para comunicação direta

### 3. WebSocket customizado (Rejeitada)
- Protocolo próprio sobre WebSocket
- Problema: Reinventar a roda, menos robusto

### 4. gRPC bidirectional (Rejeitada)
- Streaming bidirecional via gRPC
- Problema: Mais complexo, menos suporte para chat

## Métricas de Sucesso

- **Latência média**: < 100ms para mensagens diretas
- **Latência de grupo**: < 500ms para mensagens de grupo
- **Taxa de entrega**: > 99.9% das mensagens entregues
- **Uptime**: > 99.9% de disponibilidade
- **Satisfação**: Agentes reportam boa experiência de comunicação

## Próximos Passos

1. Implementar DirectMessage e GroupMessage classes
2. Criar PresenceManager
3. Implementar MessageRouter
4. Criar GroupChatManager
5. Implementar MessageAuthentication e Encryption
6. Adicionar CommunicationMetrics
7. Testar com múltiplos agentes
8. Otimizar performance
