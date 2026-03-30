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

Descreva o contexto e o problema que levou à necessidade desta decisão.

## Decisão

Descreva a decisão tomada e por quê.

## Consequências

### Positivas

- Lista de consequências positivas

### Negativas

- Lista de consequências negativas ou trade-offs

## Alternativas Consideradas

- Alternativa 1: descrição e por que foi rejeitada
- Alternativa 2: descrição e por que foi rejeitada

## Referências

- Links para discussões, RFCs, documentação relevante
```

## Lista de ADRs

| # | Título | Status | Data |
|---|--------|--------|------|
| [0001](./0001-use-fastapi.md) | Use FastAPI as Web Framework | Aceito | 2026-01-15 |
| [0002](./0002-use-spade-xmpp.md) | Use SPADE for Agent Communication | Aceito | 2026-01-16 |
| [0003](./0003-use-langchain.md) | Use LangChain for Agent Orchestration | Aceito | 2026-01-17 |
| [0004](./0004-use-postgresql-kuzudb.md) | Use PostgreSQL and KuzuDB | Aceito | 2026-01-18 |
| [0005](./0005-use-rabbitmq.md) | Use RabbitMQ for Async Tasks | Aceito | 2026-01-19 |

**Status:** Todos os 5 ADRs principais estão completos e documentados.

## Como Criar um Novo ADR

1. Copie o template acima
2. Crie um novo arquivo com o próximo número sequencial: `XXXX-titulo-kebab-case.md`
3. Preencha todas as seções
4. Adicione uma entrada na tabela acima
5. Abra um PR para revisão

## Quando Criar um ADR

Crie um ADR quando:

- Escolher uma tecnologia ou framework principal
- Definir padrões arquiteturais
- Tomar decisões que afetam múltiplos componentes
- Escolher entre alternativas com trade-offs significativos
- Definir convenções de código ou estrutura

## Quando NÃO Criar um ADR

- Decisões triviais ou reversíveis facilmente
- Detalhes de implementação específicos
- Configurações temporárias
- Decisões que afetam apenas um componente isolado
