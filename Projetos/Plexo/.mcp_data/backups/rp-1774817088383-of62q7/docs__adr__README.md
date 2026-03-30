# Architecture Decision Records (ADR)

Este diretório contém os Architecture Decision Records (ADRs) do projeto Plexo.

## O que é um ADR?

Um ADR é um documento que captura uma decisão arquitetural importante junto com seu contexto e consequências.

## Formato

Cada ADR segue este template:

```markdown
# [número]. [título da decisão]

Data: YYYY-MM-DD

Status: [Proposto | Aceito | Rejeitado | Depreciado | Substituído por ADR-XXXX]

## Contexto

[Descreva o problema ou situação que motivou esta decisão]

## Decisão

[Descreva a decisão tomada]

## Consequências

[Descreva as consequências positivas e negativas da decisão]
```

## ADRs do Projeto

### Decisões de Infraestrutura

- [0001-use-fastapi.md](0001-use-fastapi.md) - Usar FastAPI como framework web
- [0002-use-spade-xmpp.md](0002-use-spade-xmpp.md) - Usar SPADE com XMPP para comunicação entre agentes
- [0003-use-langchain.md](0003-use-langchain.md) - Usar LangChain/LangGraph para orquestração de agentes
- [0004-use-postgresql-kuzudb.md](0004-use-postgresql-kuzudb.md) - Usar PostgreSQL e KuzuDB para armazenamento
- [0005-use-rabbitmq.md](0005-use-rabbitmq.md) - Usar RabbitMQ para processamento assíncrono de tarefas
- [0014-use-llamacpp-turboquant.md](0014-use-llamacpp-turboquant.md) - Usar llama.cpp com TurboQuant para inferência local

### Decisões de Arquitetura de Agentes

- [0006-agent-collaboration-pattern.md](0006-agent-collaboration-pattern.md) - Padrão de colaboração híbrido entre agentes
- [0007-agent-tools-capabilities.md](0007-agent-tools-capabilities.md) - Sistema de ferramentas modulares para agentes
- [0008-agent-specialization-strategy.md](0008-agent-specialization-strategy.md) - Estratégia de especialização de agentes por papéis
- [0009-real-time-communication-protocol.md](0009-real-time-communication-protocol.md) - Protocolo de comunicação em tempo real
- [0010-agent-memory-context.md](0010-agent-memory-context.md) - Sistema de memória em três camadas
- [0011-error-handling-recovery.md](0011-error-handling-recovery.md) - Sistema de error handling e recovery
- [0012-agent-lifecycle-management.md](0012-agent-lifecycle-management.md) - Gerenciamento de ciclo de vida de agentes
- [0013-spade-langgraph-orchestration.md](0013-spade-langgraph-orchestration.md) - Orquestração híbrida SPADE + LangGraph

## Status dos ADRs

| ADR | Título | Status | Data |
|-----|--------|--------|------|
| 0001 | Use FastAPI | Aceito | 2026-01-15 |
| 0002 | Use SPADE XMPP | Aceito | 2026-01-16 |
| 0003 | Use LangChain | Aceito | 2026-01-17 |
| 0004 | Use PostgreSQL KuzuDB | Aceito | 2026-01-18 |
| 0005 | Use RabbitMQ | Aceito | 2026-01-19 |
| 0006 | Agent Collaboration Pattern | Aceito | 2026-03-29 |
| 0007 | Agent Tools Capabilities | Aceito | 2026-03-29 |
| 0008 | Agent Specialization Strategy | Aceito | 2026-03-29 |
| 0009 | Real-time Communication Protocol | Aceito | 2026-03-29 |
| 0010 | Agent Memory Context | Aceito | 2026-03-29 |
| 0011 | Error Handling Recovery | Aceito | 2026-03-29 |
| 0012 | Agent Lifecycle Management | Aceito | 2026-03-29 |
| 0013 | SPADE + LangGraph Orchestration | Aceito | 2026-03-29 |
| 0014 | Use llama.cpp with TurboQuant | Aceito | 2026-03-29 |

## Como Criar um Novo ADR

1. Crie um novo arquivo `XXXX-titulo-da-decisao.md`
2. Siga o formato padrão
3. Defina o status como "Proposto"
4. Apresente para revisão da equipe
5. Atualize status para "Aceito" após aprovação
6. Atualize este README

## Processo de Revisão

1. **Proposta**: Autor cria ADR com status "Proposto"
2. **Discussão**: Equipe discute prós e contras
3. **Revisão**: Revisores analisam impactos
4. **Aprovação**: Decisão é aceita ou rejeitada
5. **Implementação**: Decisão é implementada no código
6. **Monitoramento**: Acompanhar resultados da decisão

## Referências

- [Documentação ADR](https://adr.github.io/)
- [Michael Nygard's ADR](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [GitHub ADR](https://github.com/joelparkerhenderson/architecture-decision-record)
