# FEATURE: Multi-Agent Communication
# ADR-0015: Implementação do Protocolo SPADE

Data: 2026-03-29

Status: Aceito

## Contexto

O sistema Plexo necessita de um protocolo de comunicação robusto para múltiplos agentes inteligentes. Com base nos ADRs anteriores (0002, 0006, 0009), implementamos a estrutura base do protocolo SPADE com XMPP.

## Decisão

Implementamos a estrutura completa do módulo SPADE com os seguintes componentes:

### 1. Sistema de Urgência de Mensagens

**Arquivo:** `backend/app/spade/protocols/urgency_protocol.py`

- **UrgencyLevel:** Enum com 4 níveis (LOW, MEDIUM, HIGH, CRITICAL)
- **UrgentMessage:** Classe para mensagens com urgência
- **UrgencyProtocol:** Gerenciador de mensagens urgentes com fila prioritária

**Funcionalidades:**
- Mensagens CRITICAL exigem checkpoint imediato
- Mensagens HIGH interrompem tarefa atual
- Fila de mensagens ordenada por urgência
- Estatísticas de mensagens pendentes

### 2. Checkpoint Behavior

**Arquivo:** `backend/app/spade/behaviors/checkpoint_behavior.py`

- **CheckpointStatus:** Status do checkpoint (CREATED, ACTIVE, PAUSED, RESUMED, COMPLETED, FAILED)
- **Checkpoint:** Representa um checkpoint de tarefa
- **CheckpointManager:** Gerencia checkpoints de um agente

**Funcionalidades:**
- Criar checkpoint do estado atual
- Pausar tarefa quando mensagem urgente chega
- Retomar tarefa a partir de checkpoint
- Limpeza automática de checkpoints antigos

### 3. Teams of Agents

**Arquivos:**
- `backend/app/spade/teams/team.py` - Classe Team
- `backend/app/spade/teams/team_chat.py` - Chat em grupo (MUC)
- `backend/app/spade/teams/team_manager.py` - Gerenciador de teams

**Funcionalidades:**
- Times com múltiplos membros
- Chat em grupo usando MUC (Multi-User Chat)
- Referência de mensagens para chamar atenção
- Estatísticas de times e membros

### 4. Whiteboard Compartilhado

**Arquivos:**
- `backend/app/spade/whiteboard/whiteboard.py` - Quadro branco
- `backend/app/spade/whiteboard/whiteboard_entry.py` - Entradas com tipos de ação
- `backend/app/spade/whiteboard/whiteboard_manager.py` - Gerenciador

**Funcionalidades:**
- 21 tipos de ação (FUNCTION_CREATED, CLASS_CREATED, TEST_PASSED, etc.)
- Descrições amigáveis das ações do executor
- Busca e filtros por autor, tipo, arquivo
- Bloqueio/desbloqueio para escrita

### 5. Agentes de Monitoramento

**Arquivo:** `backend/app/spade/agents/monitor_agent.py`

- **MonitorRole:** TRACKER e VALIDATOR
- **MonitorAgent:** Agente de monitoramento em tempo real
- **MonitorAction:** Ação monitorada

**Funcionalidades:**
- Tracker: Escreve ações no whiteboard de forma descritiva
- Validator: Identifica erros e executa testes automáticos
- Estatísticas de monitoramento

### 6. Agentes Especialistas

**Arquivo:** `backend/app/spade/agents/specialist_agent.py`

- **SpecialistType:** 8 tipos (CODE_WRITER, CODE_REVIEWER, TESTER, ARCHITECT, etc.)
- **SpecialistAgent:** Agente especialista
- **Assignment:** Designação de tarefa

**Funcionalidades:**
- Especialistas aceitam/rejeitam tarefas
- Histórico de designações
- Nível de expertise ajustável
- Capacidades específicas por tipo

### 7. Executor de Graphs

**Arquivos:**
- `backend/app/spade/graphs/graph_node.py` - Nó do graph
- `backend/app/spade/graphs/agent_graph.py` - Graph de execução
- `backend/app/spade/graphs/graph_executor.py` - Executor

**Funcionalidades:**
- Graphs com dependências entre nós
- Execução automática de nós prontos
- Handlers personalizados por tipo de especialista
- Log de execução completo

## Estrutura de Diretórios

```
backend/app/spade/
├── __init__.py                    # Exportações principais
├── agent_base.py                  # PlexoAgent (existente)
├── agents/
│   ├── __init__.py
│   ├── executor_agent.py          # ExecutorAgent
│   ├── monitor_agent.py           # MonitorAgent
│   └── specialist_agent.py        # SpecialistAgent
├── behaviors/
│   ├── __init__.py
│   ├── base_behavior.py           # BaseBehavior (existente)
│   ├── checkpoint_behavior.py     # CheckpointManager
│   └── message_behavior.py        # MessageBehavior (existente)
├── graphs/
│   ├── __init__.py
│   ├── agent_graph.py             # AgentGraph
│   ├── graph_executor.py          # GraphExecutor
│   └── graph_node.py              # GraphNode
├── protocols/
│   ├── __init__.py
│   ├── urgency_protocol.py        # UrgencyProtocol
│   └── xmpp_protocol.py           # XMPPProtocol (existente)
├── registry/
│   ├── __init__.py
│   └── agent_registry.py          # AgentRegistry (existente)
├── teams/
│   ├── __init__.py
│   ├── team.py                    # Team
│   ├── team_chat.py               # TeamChat
│   └── team_manager.py            # TeamManager
└── whiteboard/
    ├── __init__.py
    ├── whiteboard.py              # Whiteboard
    ├── whiteboard_entry.py        # WhiteboardEntry
    └── whiteboard_manager.py      # WhiteboardManager
```

## Componentes Implementados

| Componente | Arquivo | Status |
|------------|---------|--------|
| UrgencyProtocol | protocols/urgency_protocol.py | ✅ Implementado |
| CheckpointManager | behaviors/checkpoint_behavior.py | ✅ Implementado |
| Team | teams/team.py | ✅ Implementado |
| TeamChat | teams/team_chat.py | ✅ Implementado |
| TeamManager | teams/team_manager.py | ✅ Implementado |
| Whiteboard | whiteboard/whiteboard.py | ✅ Implementado |
| WhiteboardEntry | whiteboard/whiteboard_entry.py | ✅ Implementado |
| WhiteboardManager | whiteboard/whiteboard_manager.py | ✅ Implementado |
| MonitorAgent | agents/monitor_agent.py | ✅ Implementado |
| SpecialistAgent | agents/specialist_agent.py | ✅ Implementado |
| ExecutorAgent | agents/executor_agent.py | ✅ Implementado |
| GraphNode | graphs/graph_node.py | ✅ Implementado |
| AgentGraph | graphs/agent_graph.py | ✅ Implementado |
| GraphExecutor | graphs/graph_executor.py | ✅ Implementado |

## Integração com Sistema Existente

### Modelos SQLAlchemy

Para integrar com o banco de dados, os seguintes modelos precisam ser criados:

1. **TeamModel** - Para persistir times
2. **WhiteboardModel** - Para persistir whiteboards
3. **CheckpointModel** - Para persistir checkpoints
4. **MessageModel** - Atualizar com campo urgency

### Schemas Pydantic

Para a API REST, os seguintes schemas precisam ser criados:

1. **TeamCreate/TeamResponse** - Para criação e resposta de times
2. **WhiteboardCreate/WhiteboardResponse** - Para whiteboards
3. **CheckpointCreate/CheckpointResponse** - Para checkpoints
4. **MessageCreate** - Atualizar com campo urgency

## Próximos Passos

1. **Criar modelos SQLAlchemy** para persistência
2. **Criar schemas Pydantic** para API REST
3. **Implementar endpoints** para teams, whiteboards, checkpoints
4. **Integrar com PlexoAgent** existente
5. **Criar testes unitários** para cada componente
6. **Documentar APIs** com OpenAPI

## Conclusão

A estrutura base do protocolo SPADE está completa e pronta para integração com o sistema existente. Todos os componentes seguem o padrão de design do projeto e estão documentados.
