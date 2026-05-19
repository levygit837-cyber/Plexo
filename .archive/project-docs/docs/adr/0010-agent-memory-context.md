# 0010. Agent Memory and Context Management

Data: 2026-03-29

Status: Aceito

## Contexto

Os agentes do sistema Plexo precisam manter contexto e memória para:

- Lembrar de conversas e decisões anteriores
- Aprender com experiências passadas
- Manter coerência ao longo de múltiplas sessões
- Compartilhar conhecimento entre agentes
- Recuperar informações relevantes rapidamente
- Evitar repetição de erros

## Decisão

Decidimos implementar um **sistema de memória em três camadas** com armazenamento híbrido:

### 1. Arquitetura de Memória

#### Camada 1: Working Memory (Memória de Trabalho)
- **Descrição**: Memória de curto prazo para contexto atual
- **Duração**: Sessão atual (até desconexão)
- **Tamanho**: Limitado (1000 tokens por agente)
- **Acesso**: Rápido (in-memory)
- **Uso**: Contexto de conversa atual, estado de tarefa

```python
@dataclass
class WorkingMemory:
    """Memória de trabalho de curto prazo"""
    agent_id: str
    session_id: str
    current_conversation: List[Message]
    current_task_context: Dict[str, Any]
    recent_artifacts: List[Artifact]
    active_participants: List[str]
    metadata: Dict[str, Any]
    created_at: datetime
    expires_at: datetime
    
    def add_message(self, message: Message):
        """Adiciona mensagem à memória"""
        self.current_conversation.append(message)
        self._trim_if_needed()
    
    def get_context(self, max_tokens: int = 500) -> str:
        """Retorna contexto formatado"""
        pass
    
    def _trim_if_needed(self):
        """Remove mensagens antigas se exceder limite"""
        pass
```

#### Camada 2: Episodic Memory (Memória Episódica)
- **Descrição**: Memória de médio prazo para eventos e experiências
- **Duração**: Dias a semanas
- **Tamanho**: Moderado (10.000 episódios por agente)
- **Acesso**: Médio (PostgreSQL + embeddings)
- **Uso**: Histórico de tarefas, decisões tomadas, resultados

```python
@dataclass
class EpisodicMemory:
    """Memória episódica de médio prazo"""
    memory_id: str
    agent_id: str
    episode_type: EpisodeType
    title: str
    description: str
    context: Dict[str, Any]
    participants: List[str]
    artifacts: List[str]  # artifact_ids
    outcome: Optional[str]
    lessons_learned: List[str]
    embedding: List[float]  # Para busca semântica
    created_at: datetime
    accessed_at: datetime
    access_count: int
    relevance_score: float

class EpisodeType(Enum):
    TASK_COMPLETED = "task_completed"
    BUG_FIXED = "bug_fixed"
    DECISION_MADE = "decision_made"
    LEARNING = "learning"
    COLLABORATION = "collaboration"
    ERROR = "error"
    SUCCESS = "success"
```

#### Camada 3: Semantic Memory (Memória Semântica)
- **Descrição**: Memória de longo prazo para conhecimento geral
- **Duração**: Permanente
- **Tamanho**: Grande (ilimitado)
- **Acesso**: Lento (KuzuDB graph + embeddings)
- **Uso**: Padrões de código, melhores práticas, conhecimento técnico

```python
@dataclass
class SemanticMemory:
    """Memória semântica de longo prazo"""
    memory_id: str
    agent_id: Optional[str]  # None = compartilhado entre agentes
    concept: str
    definition: str
    examples: List[str]
    related_concepts: List[str]
    embedding: List[float]
    confidence: float  # 0-1
    source: str
    created_at: datetime
    updated_at: datetime
    usage_count: int
    success_rate: float
```

### 2. Memory Storage

#### Working Memory Store
```python
class WorkingMemoryStore:
    """Armazenamento em memória para working memory"""
    
    def __init__(self):
        self.memories: Dict[str, WorkingMemory] = {}
        self.lock = asyncio.Lock()
    
    async def get(self, agent_id: str) -> Optional[WorkingMemory]:
        """Obtém working memory de agente"""
        async with self.lock:
            memory = self.memories.get(agent_id)
            if memory and memory.expires_at > datetime.now():
                return memory
            return None
    
    async def set(self, memory: WorkingMemory):
        """Define working memory de agente"""
        async with self.lock:
            self.memories[memory.agent_id] = memory
    
    async def delete(self, agent_id: str):
        """Remove working memory de agente"""
        async with self.lock:
            self.memories.pop(agent_id, None)
```

#### Episodic Memory Store
```python
class EpisodicMemoryStore:
    """Armazenamento PostgreSQL para episodic memory"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def store(self, memory: EpisodicMemory):
        """Armazena episódio"""
        pass
    
    async def retrieve(
        self,
        agent_id: str,
        query: str,
        limit: int = 10
    ) -> List[EpisodicMemory]:
        """Recupera episódios relevantes"""
        pass
    
    async def search_similar(
        self,
        embedding: List[float],
        limit: int = 5
    ) -> List[EpisodicMemory]:
        """Busca episódios similares por embedding"""
        pass
```

#### Semantic Memory Store
```python
class SemanticMemoryStore:
    """Armazenamento KuzuDB para semantic memory"""
    
    def __init__(self, kuzu_conn: kuzu.Connection):
        self.conn = kuzu_conn
    
    async def store(self, memory: SemanticMemory):
        """Armazena conceito semântico"""
        pass
    
    async def retrieve(
        self,
        concept: str,
        agent_id: Optional[str] = None
    ) -> Optional[SemanticMemory]:
        """Recupera conceito semântico"""
        pass
    
    async def search_similar(
        self,
        embedding: List[float],
        limit: int = 5
    ) -> List[SemanticMemory]:
        """Busca conceitos similares por embedding"""
        pass
    
    async def get_related(
        self,
        concept: str,
        depth: int = 2
    ) -> List[SemanticMemory]:
        """Obtém conceitos relacionados"""
        pass
```

### 3. Memory Operations

#### Memory Manager
```python
class MemoryManager:
    """Gerencia todas as operações de memória"""
    
    def __init__(
        self,
        working_store: WorkingMemoryStore,
        episodic_store: EpisodicMemoryStore,
        semantic_store: SemanticMemoryStore
    ):
        self.working = working_store
        self.episodic = episodic_store
        self.semantic = semantic_store
    
    async def remember_conversation(
        self,
        agent_id: str,
        messages: List[Message]
    ):
        """Armazena conversa na memória"""
        # Working memory
        working = await self.working.get(agent_id)
        if not working:
            working = WorkingMemory(agent_id=agent_id)
        for msg in messages:
            working.add_message(msg)
        await self.working.set(working)
    
    async def remember_episode(
        self,
        agent_id: str,
        episode: EpisodicMemory
    ):
        """Armazena episódio"""
        await self.episodic.store(episode)
    
    async def remember_concept(
        self,
        concept: SemanticMemory
    ):
        """Armazena conceito semântico"""
        await self.semantic.store(concept)
    
    async def recall_relevant(
        self,
        agent_id: str,
        query: str,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Recupera informações relevantes"""
        results = {
            'working': await self.working.get(agent_id),
            'episodic': await self.episodic.retrieve(agent_id, query, limit),
            'semantic': await self.semantic.search_similar(
                self._generate_embedding(query), limit
            )
        }
        return results
```

#### Memory Retrieval
```python
class MemoryRetriever:
    """Recupera memórias relevantes para contexto"""
    
    async def get_context_for_task(
        self,
        agent_id: str,
        task: Task
    ) -> str:
        """Obtém contexto relevante para tarefa"""
        # Busca episódios similares
        episodes = await self.episodic.retrieve(
            agent_id,
            task.description,
            limit=5
        )
        
        # Busca conceitos relacionados
        concepts = await self.semantic.search_similar(
            self._generate_embedding(task.description),
            limit=3
        )
        
        # Formata contexto
        context = self._format_context(episodes, concepts)
        return context
    
    async def get_context_for_conversation(
        self,
        agent_id: str,
        chat_id: str
    ) -> str:
        """Obtém contexto para conversa"""
        # Working memory
        working = await self.working.get(agent_id)
        
        # Histórico do chat
        chat_history = await self.get_chat_history(chat_id)
        
        # Formata contexto
        context = self._format_conversation_context(
            working, chat_history
        )
        return context
```

### 4. Memory Sharing Between Agents

#### Shared Memory Protocol
```python
class SharedMemoryProtocol:
    """Protocolo para compartilhar memória entre agentes"""
    
    async def share_episode(
        self,
        from_agent: Agent,
        to_agent: Agent,
        episode: EpisodicMemory
    ):
        """Compartilha episódio com outro agente"""
        # Verifica permissões
        if not self.can_share(from_agent, to_agent, episode):
            raise PermissionError("Cannot share this episode")
        
        # Copia episódio para agente destino
        shared_episode = episode.copy()
        shared_episode.agent_id = to_agent.id
        shared_episode.source_agent_id = from_agent.id
        
        await self.episodic.store(shared_episode)
    
    async def share_concept(
        self,
        from_agent: Agent,
        concept: SemanticMemory
    ):
        """Compartilha conceito com todos os agentes"""
        # Marca como compartilhado
        concept.agent_id = None  # None = compartilhado
        
        await self.semantic.store(concept)
```

#### Knowledge Graph
```python
class KnowledgeGraph:
    """Grafo de conhecimento entre agentes"""
    
    def __init__(self, kuzu_conn: kuzu.Connection):
        self.conn = kuzu_conn
    
    async def add_concept(
        self,
        concept: str,
        definition: str,
        agent_id: Optional[str] = None
    ):
        """Adiciona conceito ao grafo"""
        pass
    
    async def add_relation(
        self,
        concept1: str,
        concept2: str,
        relation_type: str,
        weight: float = 1.0
    ):
        """Adiciona relação entre conceitos"""
        pass
    
    async def get_related_concepts(
        self,
        concept: str,
        depth: int = 2
    ) -> List[str]:
        """Obtém conceitos relacionados"""
        pass
```

### 5. Context Window Management

#### Context Window
```python
class ContextWindow:
    """Gerencia janela de contexto para LLMs"""
    
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.messages: List[Message] = []
        self.system_prompt: str = ""
        self.context: str = ""
    
    def add_message(self, message: Message):
        """Adiciona mensagem ao contexto"""
        self.messages.append(message)
        self._trim_if_needed()
    
    def set_context(self, context: str):
        """Define contexto adicional"""
        self.context = context
    
    def get_prompt(self) -> str:
        """Retorna prompt completo"""
        parts = [self.system_prompt]
        
        if self.context:
            parts.append(f"Context: {self.context}")
        
        for msg in self.messages:
            parts.append(f"{msg.role}: {msg.content}")
        
        return "\n".join(parts)
    
    def _trim_if_needed(self):
        """Remove mensagens antigas se exceder limite"""
        while self._count_tokens() > self.max_tokens:
            if len(self.messages) > 1:
                self.messages.pop(0)
            else:
                break
```

### 6. Memory Consolidation

#### Consolidation Process
```python
class MemoryConsolidator:
    """Consolida memórias periodicamente"""
    
    async def consolidate_working_memory(
        self,
        agent_id: str
    ):
        """Consolida working memory em episodic memory"""
        working = await self.working.get(agent_id)
        if not working:
            return
        
        # Cria episódio a partir de working memory
        episode = EpisodicMemory(
            agent_id=agent_id,
            episode_type=EpisodeType.COLLABORATION,
            title=f"Conversation in {working.session_id}",
            description=self._summarize_conversation(working),
            context=working.current_task_context,
            participants=working.active_participants,
            artifacts=[a.id for a in working.recent_artifacts],
            created_at=datetime.now()
        )
        
        await self.episodic.store(episode)
    
    async def extract_semantic_knowledge(
        self,
        agent_id: str
    ):
        """Extrai conhecimento semântico de episódios"""
        # Busca episódios recentes
        episodes = await self.episodic.retrieve(
            agent_id,
            "",
            limit=100
        )
        
        # Extrai padrões e conceitos
        concepts = self._extract_concepts(episodes)
        
        # Armazena como conhecimento semântico
        for concept in concepts:
            await self.semantic.store(concept)
```

### 7. Memory Search and Retrieval

#### Semantic Search
```python
class MemorySearcher:
    """Busca semântica em memórias"""
    
    async def search(
        self,
        query: str,
        memory_types: List[str] = ['working', 'episodic', 'semantic'],
        limit: int = 10
    ) -> Dict[str, List[Any]]:
        """Busca em todos os tipos de memória"""
        results = {}
        
        query_embedding = self._generate_embedding(query)
        
        if 'working' in memory_types:
            working = await self.working.get(agent_id)
            if working:
                results['working'] = [working]
        
        if 'episodic' in memory_types:
            results['episodic'] = await self.episodic.search_similar(
                query_embedding, limit
            )
        
        if 'semantic' in memory_types:
            results['semantic'] = await self.semantic.search_similar(
                query_embedding, limit
            )
        
        return results
```

## Consequências

### Positivas
- **Contexto Rico**: Agentes têm acesso a histórico completo
- **Aprendizado**: Sistema melhora com experiência
- **Coerência**: Manter consistência ao longo do tempo
- **Compartilhamento**: Agentes aprendem uns com os outros
- **Performance**: Camadas otimizadas para diferentes usos

### Negativas
- **Complexidade**: Sistema mais complexo de gerenciar
- **Armazenamento**: Mais espaço necessário
- **Privacidade**: Questões de privacidade ao compartilhar memória
- **Overhead**: Custo de manter e buscar memórias

### Mitigações
- **Limite de tamanho**: Limitar quantidade de memória por agente
- **Compressão**: Comprimir memórias antigas
- **Políticas de retenção**: Definir quando limpar memórias
- **Criptografia**: Proteger memórias sensíveis

## Alternativas Consideradas

### 1. Apenas Context Window (Rejeitada)
- Só memória de curto prazo
- Problema: Sem aprendizado, sem histórico

### 2. Apenas Banco de Dados (Rejeitada)
- Tudo no banco de dados
- Problema: Latência alta para contexto atual

### 3. Memória por Agente Isolada (Rejeitada)
- Cada agente tem memória separada
- Problema: Sem compartilhamento de conhecimento

## Métricas de Sucesso

- **Hit rate**: Porcentagem de buscas que retornam resultados relevantes
- **Latência de busca**: Tempo para recuperar memórias
- **Uso de armazenamento**: Espaço utilizado por memória
- **Qualidade de contexto**: Avaliação de quão útil é o contexto recuperado
- **Aprendizado**: Melhoria de performance ao longo do tempo

## Próximos Passos

1. Implementar classes de memória (Working, Episodic, Semantic)
2. Criar stores de memória (in-memory, PostgreSQL, KuzuDB)
3. Implementar MemoryManager e MemoryRetriever
4. Criar SharedMemoryProtocol
5. Implementar KnowledgeGraph
6. Adicionar ContextWindow management
7. Criar MemoryConsolidator
8. Implementar MemorySearcher
9. Testar com agentes reais
10. Otimizar performance e armazenamento
