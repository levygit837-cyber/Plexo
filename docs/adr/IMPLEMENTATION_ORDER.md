# Ordem de Implementação dos ADRs

Este documento define a sequência de implementação dos ADRs do projeto Plexo, baseada em dependências entre componentes.

## Visão Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                    Fase 1: Fundação                             │
├─────────────────────────────────────────────────────────────────┤
│  ADR-0001: FastAPI          (Base do Backend)                   │
│  ADR-0004: PostgreSQL+KuzuDB (Armazenamento)                    │
│  ADR-0005: RabbitMQ          (Filas Assíncronas)                 │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Fase 2: Comunicação                          │
├─────────────────────────────────────────────────────────────────┤
│  ADR-0002: SPADE XMPP       (Comunicação Agentes)               │
│  ADR-0009: Real-time Protocol (Protocolo de Comunicação)        │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Fase 3: Agentes Base                         │
├─────────────────────────────────────────────────────────────────┤
│  ADR-0012: Lifecycle Management (Ciclo de Vida)                 │
│  ADR-0007: Tools & Capabilities (Ferramentas)                   │
│  ADR-0010: Memory & Context (Memória)                           │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Fase 4: Orquestração                         │
├─────────────────────────────────────────────────────────────────┤
│  ADR-0003: LangChain/LangGraph (Orquestração LLM)               │
│  ADR-0013: SPADE+LangGraph (Orquestração Híbrida)               │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Fase 5: Colaboração                          │
├─────────────────────────────────────────────────────────────────┤
│  ADR-0006: Collaboration Pattern (Padrões de Colaboração)       │
│  ADR-0008: Specialization Strategy (Especialização)             │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Fase 6: Resiliência                          │
├─────────────────────────────────────────────────────────────────┤
│  ADR-0011: Error Handling & Recovery (Tratamento de Erros)      │
└─────────────────────────────────────────────────────────────────┘
```

## Fase 1: Fundação (Semana 1-2)

### ADR-0001: FastAPI
**Status**: ✅ Já implementado
**Dependências**: Nenhuma
**Entregáveis**:
- Configuração do FastAPI
- Estrutura de projeto
- Endpoints básicos de health check

### ADR-0004: PostgreSQL + KuzuDB
**Status**: ✅ Já implementado
**Dependências**: Nenhuma
**Entregáveis**:
- Configuração do PostgreSQL
- Configuração do KuzuDB
- Models básicos (Agent, Task, Message)
- Schemas Pydantic
- Migrations com Alembic

### ADR-0005: RabbitMQ
**Status**: ✅ Já implementado
**Dependências**: Nenhuma
**Entregáveis**:
- Configuração do RabbitMQ
- Producer para filas
- Consumer para filas
- Workers básicos

## Fase 2: Comunicação (Semana 3-4)

### ADR-0002: SPADE XMPP
**Status**: ✅ Já implementado
**Dependências**: ADR-0001 (FastAPI)
**Entregáveis**:
- Configuração do ejabberd
- Classe base PlexoAgent
- Comunicação XMPP básica
- Presence management

### ADR-0009: Real-time Communication Protocol
**Status**: 📋 A implementar
**Dependências**: ADR-0002 (SPADE)
**Entregáveis**:
- Message structure (DirectMessage, GroupMessage)
- MessageType enum
- GroupChat com MUC
- PresenceManager
- MessageRouter
- Comunicação 1:1 e 1:N

## Fase 3: Agentes Base (Semana 5-6)

### ADR-0012: Agent Lifecycle Management
**Status**: 📋 A implementar
**Dependências**: ADR-0002 (SPADE), ADR-0004 (PostgreSQL)
**Entregáveis**:
- AgentState enum
- AgentLifecycleManager
- ManagedAgent class
- AgentHealth monitoring
- ResourceManager
- AgentScaler
- Transições de estado

### ADR-0007: Agent Tools and Capabilities
**Status**: 📋 A implementar
**Dependências**: ADR-0012 (Lifecycle)
**Entregáveis**:
- BaseTool abstract class
- ToolRegistry
- Code Tools (executor, analyzer, generator)
- File Tools (reader, writer, searcher)
- Web Tools (searcher, scraper)
- Git Tools (operations, workflow)
- Query Tools (database, api)
- Terminal Tools (shell, process manager)
- LLM Tools (query, rag)
- AgentPermissions system
- SecurityValidator

### ADR-0010: Agent Memory and Context
**Status**: 📋 A implementar
**Dependências**: ADR-0004 (PostgreSQL, KuzuDB), ADR-0012 (Lifecycle)
**Entregáveis**:
- WorkingMemory (in-memory)
- EpisodicMemory (PostgreSQL)
- SemanticMemory (KuzuDB)
- WorkingMemoryStore
- EpisodicMemoryStore
- SemanticMemoryStore
- MemoryManager
- MemoryRetriever
- SharedMemoryProtocol
- KnowledgeGraph
- ContextWindow management
- MemoryConsolidator
- MemorySearcher

## Fase 4: Orquestração (Semana 7-8)

### ADR-0003: LangChain/LangGraph
**Status**: ✅ Já implementado
**Dependências**: ADR-0007 (Tools), ADR-0010 (Memory)
**Entregáveis**:
- BaseChain class
- BaseAgentGraph class
- SimpleAgentGraph
- ConditionalAgentGraph
- AgentQueryTool
- Integração com LLMs

### ADR-0013: SPADE + LangGraph Orchestration
**Status**: 📋 A implementar
**Dependências**: ADR-0002 (SPADE), ADR-0003 (LangGraph), ADR-0009 (Protocol)
**Entregáveis**:
- PlexoAgentGraph class
- GraphMonitor
- NaturalLanguageTracker
- OrchestrationFlow
- LowLatencyOrchestrator
- SPADE Group Chat integration
- Real-time monitoring
- Progress tracking em linguagem natural

## Fase 5: Colaboração (Semana 9-10)

### ADR-0006: Agent Collaboration Pattern
**Status**: 📋 A implementar
**Dependências**: ADR-0009 (Protocol), ADR-0013 (Orchestration)
**Entregáveis**:
- AgentCollaborationManager
- GroupChatManager
- RoleAssigner
- ConflictResolver
- CollaborationMetrics
- Padrões de colaboração:
  - Debate decisório
  - Divisão e conquista
  - Revisão de código colaborativa

### ADR-0008: Agent Specialization Strategy
**Status**: 📋 A implementar
**Dependências**: ADR-0006 (Collaboration), ADR-0007 (Tools), ADR-0012 (Lifecycle)
**Entregáveis**:
- AgentType classes (CODER, RESEARCHER, COORDINATOR, TESTER, ARCHITECT, DEVOPS)
- TaskMatcher
- DynamicRoleManager
- HandoffProtocol
- SkillDeveloper
- Knowledge sharing entre agentes

## Fase 6: Resiliência (Semana 11-12)

### ADR-0011: Error Handling and Recovery
**Status**: 📋 A implementar
**Dependências**: Todos os ADRs anteriores
**Entregáveis**:
- PlexoError class
- ErrorCategory e ErrorSeverity enums
- ToolErrorHandler
- AgentErrorHandler
- TaskErrorHandler
- SystemErrorHandler
- RetryStrategy (exponential backoff)
- CircuitBreaker
- FallbackStrategy
- ErrorNotifier
- ErrorLogger
- ErrorMetrics
- ErrorPatternDetector
- ErrorPreventer

## Cronograma Detalhado

| Semana | Fase | ADRs | Entregáveis Principais |
|--------|------|------|------------------------|
| 1-2 | Fundação | 0001, 0004, 0005 | Backend, DB, Filas |
| 3-4 | Comunicação | 0002, 0009 | SPADE, Protocolo |
| 5-6 | Agentes Base | 0012, 0007, 0010 | Lifecycle, Tools, Memory |
| 7-8 | Orquestração | 0003, 0013 | LangGraph, Orchestration |
| 9-10 | Colaboração | 0006, 0008 | Collaboration, Specialization |
| 11-12 | Resiliência | 0011 | Error Handling |

## Dependências Críticas

### Bloqueadores
1. **ADR-0009** depende de **ADR-0002** (SPADE)
2. **ADR-0012** depende de **ADR-0002** e **ADR-0004**
3. **ADR-0007** depende de **ADR-0012**
4. **ADR-0010** depende de **ADR-0004** e **ADR-0012**
5. **ADR-0013** depende de **ADR-0002**, **ADR-0003**, **ADR-0009**
6. **ADR-0006** depende de **ADR-0009**, **ADR-0013**
7. **ADR-0008** depende de **ADR-0006**, **ADR-0007**, **ADR-0012**
8. **ADR-0011** depende de todos os anteriores

### Paralelismo Possível
- **ADR-0007** e **ADR-0010** podem ser implementados em paralelo
- **ADR-0006** e **ADR-0008** podem ser implementados em paralelo

## Validação por Fase

### Validação Fase 1
- [ ] FastAPI respondendo health check
- [ ] PostgreSQL conectado e com tables criadas
- [ ] KuzuDB conectado e com schema criado
- [ ] RabbitMQ conectado e filas funcionando

### Validação Fase 2
- [ ] Agentes SPADE se comunicando via XMPP
- [ ] Mensagens diretas funcionando (1:1)
- [ ] Chat em grupo funcionando (1:N)
- [ ] Presence sendo reportado

### Validação Fase 3
- [ ] Agentes criados com lifecycle correto
- [ ] Transições de estado funcionando
- [ ] Tools sendo executadas com sucesso
- [ ] Memory sendo persistida e recuperada

### Validação Fase 4
- [ ] LangGraph executando tarefas complexas
- [ ] Monitoramento em tempo real funcionando
- [ ] Orquestração SPADE+LangGraph coordenada
- [ ] Progress tracking em linguagem natural

### Validação Fase 5
- [ ] Agentes colaborando em discussões
- [ ] Consenso sendo alcançado
- [ ] Especialização funcionando
- [ ] Handoff entre agentes suave

### Validação Fase 6
- [ ] Erros sendo capturados corretamente
- [ ] Recovery automático funcionando
- [ ] Circuit breaker prevenindo cascata
- [ ] Logs estruturados disponíveis

## Métricas de Progresso

- **Fase 1**: 100% (já implementado)
- **Fase 2**: 50% (SPADE implementado, Protocol pendente)
- **Fase 3**: 0%
- **Fase 4**: 50% (LangChain implementado, Orchestration pendente)
- **Fase 5**: 0%
- **Fase 6**: 0%

**Progresso Total**: ~25%

## Próximos Passos Imediatos

1. **Implementar ADR-0009**: Real-time Communication Protocol
   - Criar Message structures
   - Implementar GroupChat com MUC
   - Criar PresenceManager
   - Implementar MessageRouter

2. **Implementar ADR-0012**: Agent Lifecycle Management
   - Criar AgentState e transições
   - Implementar AgentLifecycleManager
   - Criar ManagedAgent
   - Implementar ResourceManager
   - Criar AgentScaler

3. **Implementar ADR-0007**: Agent Tools and Capabilities
   - Criar BaseTool e ToolRegistry
   - Implementar ferramentas básicas (file, code, git)
   - Criar sistema de permissões
   - Integrar com LangChain
