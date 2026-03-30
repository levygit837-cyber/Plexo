# 0006. Agent Collaboration Pattern

Data: 2026-03-29

Status: Aceito

## Contexto

O sistema Plexo precisa definir como múltiplos agentes inteligentes colaborarão entre si para executar tarefas de codificação complexas. Os agentes precisam:

- Comunicar-se de forma eficiente e contextual
- Coordenar esforços para dividir e conquistar tarefas
- Tomar decisões coletivas sobre abordagens de implementação
- Manter coerência quando múltiplos agentes trabalham no mesmo código
- Suportar tanto interações síncronas quanto assíncronas

## Decisão

Decidimos implementar um **padrão híbrido de colaboração** que combina:

### 1. Comunicação Peer-to-Peer com Hierarquia Dinâmica

- **Base**: Agentes operam como peers, comunicando-se diretamente
- **Hierarquia contextual**: Agentes podem assumir papéis de liderança temporários baseados em:
  - Especialização no domínio da tarefa
  - Experiência acumulada (memória de longo prazo)
  - Disponibilidade e capacidade atual
- **Rotação de liderança**: O agente "líder" pode mudar conforme a tarefa evolui

### 2. Dois Modos de Comunicação Distintos

#### Modo 1: Mensagens Diretas (1:1)
- Comunicação privada entre dois agentes
- Usada para consultas específicas, validações, transferência de conhecimento
- Protocolo: XMPP direto via SPADE
- Exemplo: Agente A pergunta ao Agente B sobre padrões de design específicos

#### Modo 2: Chat em Grupo (Múltiplos Agentes)
- Sala de discussão colaborativa
- Múltiplos agentes entram simultaneamente
- Discussão tipo "brainstorming" ou "code review"
- Capacidade de criar artefatos durante a discussão
- Pesquisa web integrada durante conversas
- Protocolo: XMPP MUC (Multi-User Chat) via SPADE
- Exemplo: 3 agentes discutem a melhor arquitetura para um módulo

### 3. Padrões de Colaboração Específicos

#### Padrão: Debate Decisório
```
1. Agente A propõe solução
2. Agente B questiona pontos específicos
3. Agente C apresenta alternativa
4. Consenso é alcançado via votação ou argumentação
5. Decisão é documentada na memória compartilhada
```

#### Padrão: Divisão e Conquista
```
1. Agente coordenador analisa tarefa complexa
2. Divide em sub-tarefas especializadas
3. Atribui sub-tarefas a agentes com melhor fit
4. Monitora progresso via mensagens de status
5. Consolida resultados e resolve conflitos
```

#### Padrão: Revisão de Código Colaborativa
```
1. Agente A implementa funcionalidade
2. Agente B revisa código (pull request style)
3. Agente C testa implementação
4. Feedback é discutido em chat de grupo
5. Merge acontece após aprovação coletiva
```

## Consequências

### Positivas
- **Flexibilidade**: Sistema adapta-se a diferentes tipos de tarefas
- **Resiliência**: Sem single point of failure na comunicação
- **Especialização**: Agentes podem focar em suas forças
- **Escalabilidade**: Fácil adicionar novos agentes ao sistema
- **Aprendizado coletivo**: Agentes aprendem uns com os outros

### Negativas
- **Complexidade**: Sistema mais complexo de implementar e debugar
- **Overhead de coordenação**: Comunicação entre agentes tem custo
- **Possíveis conflitos**: Agentes podem discordar e causar deadlock
- **Consistência**: Manter estado consistente entre agentes é desafiador

### Mitigações
- **Timeouts e retry**: Prevenir deadlocks por discordância
- **Logging detalhado**: Facilitar debugging de interações
- **Testes de cenários**: Validar padrões de colaboração antes de produção
- **Monitoramento**: Métricas de tempo de resposta e taxa de sucesso

## Alternativas Consideradas

### 1. Arquitetura Centralizada (Rejeitada)
- Um único orquestrador controla tudo
- Problema: Single point of failure, gargalo de performance

### 2. Comunicação Apenas Assíncrona (Rejeitada)
- Todas as comunicações via filas
- Problema: Latência alta para tarefas que precisam resposta rápida

### 3. Sem Hierarquia (Rejeitada)
- Todos os agentes são sempre iguais
- Problema: Difícil coordenar tarefas complexas sem liderança

## Implementação

### Componentes Necessários

1. **AgentCollaborationManager**: Gerencia padrões de colaboração
2. **GroupChatManager**: Gerencia chats em grupo
3. **RoleAssigner**: Atribui papéis dinamicamente
4. **ConflictResolver**: Resolve conflitos entre agentes
5. **CollaborationMetrics**: Coleta métricas de colaboração

### Fluxo de Comunicação

```
┌─────────────────────────────────────────────────────────┐
│                    Collaboration Hub                    │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐    ┌─────────┐    ┌─────────┐             │
│  │ Agent A │◄──►│ Agent B │◄──►│ Agent C │             │
│  └────┬────┘    └────┬────┘    └────┬────┘             │
│       │              │              │                   │
│       ▼              ▼              ▼                   │
│  ┌─────────────────────────────────────────┐           │
│  │         XMPP MUC (Group Chat)           │           │
│  └─────────────────────────────────────────┘           │
│       │              │              │                   │
│       ▼              ▼              ▼                   │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐             │
│  │ Task A  │    │ Task B  │    │ Task C  │             │
│  └─────────┘    └─────────┘    └─────────┘             │
└─────────────────────────────────────────────────────────┘
```

## Métricas de Sucesso

- **Tempo de consenso**: Tempo para agentes chegarem a decisão conjunta
- **Taxa de conclusão**: Porcentagem de tarefas completadas com sucesso
- **Satisfação de agentes**: Agentes reportam boas experiências de colaboração
- **Qualidade do código**: Código produzido por colaboração tem menos bugs
- **Overhead de comunicação**: Menos de 20% do tempo total em comunicação
