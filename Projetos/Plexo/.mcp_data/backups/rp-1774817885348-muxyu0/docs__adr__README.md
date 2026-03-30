# FEATURE: Documentation
# Architecture Decision Records (ADRs)

Este diretório contém os Architecture Decision Records do projeto Plexo.

## Índice de ADRs

| Número | Título | Data | Status |
|--------|--------|------|--------|
| 0001 | Use FastAPI | 2026-01-16 | Aceito |
| 0002 | Use SPADE XMPP | 2026-01-16 | Aceito |
| 0003 | Use LangChain | 2026-01-16 | Aceito |
| 0004 | Use PostgreSQL KuzuDB | 2026-01-16 | Aceito |
| 0005 | Use RabbitMQ | 2026-01-16 | Aceito |
| 0006 | Agent Collaboration Pattern | 2026-03-29 | Aceito |
| 0007 | Agent Tools Capabilities | 2026-03-29 | Aceito |
| 0008 | Agent Specialization Strategy | 2026-03-29 | Aceito |
| 0009 | Real-time Communication Protocol | 2026-03-29 | Aceito |
| 0010 | Agent Memory Context | 2026-03-29 | Aceito |
| 0011 | Error Handling Recovery | 2026-03-29 | Aceito |
| 0012 | Agent Lifecycle Management | 2026-03-29 | Aceito |
| 0013 | SPADE LangGraph Orchestration | 2026-03-29 | Aceito |
| 0014 | Use LlamaCPP TurboQuant | 2026-03-29 | Aceito |
| 0015 | SPADE Protocol Implementation | 2026-03-29 | Aceito |

## Ordem de Implementação

Consulte o arquivo [IMPLEMENTATION_ORDER.md](IMPLEMENTATION_ORDER.md) para a sequência recomendada de implementação.

## Como Criar um Novo ADR

1. Crie um arquivo com o formato `NNNN-titulo-do-adr.md`
2. Use o template abaixo:

```markdown
# NNNN. Título do ADR

Data: YYYY-MM-DD

Status: [Proposto | Aceito | Deprecado | Substituído]

## Contexto

Descreva o contexto que levou à decisão.

## Decisão

Descreva a decisão tomada.

## Consequências

Descreva as consequências positivas e negativas.
```

## ADRs por Categoria

### Infraestrutura
- 0001: FastAPI
- 0004: PostgreSQL KuzuDB
- 0005: RabbitMQ
- 0014: LlamaCPP TurboQuant

### Comunicação
- 0002: SPADE XMPP
- 0009: Real-time Communication Protocol
- 0015: SPADE Protocol Implementation

### Agentes
- 0006: Agent Collaboration Pattern
- 0007: Agent Tools Capabilities
- 0008: Agent Specialization Strategy
- 0010: Agent Memory Context
- 0011: Error Handling Recovery
- 0012: Agent Lifecycle Management
- 0013: SPADE LangGraph Orchestration

### Frameworks
- 0003: LangChain
