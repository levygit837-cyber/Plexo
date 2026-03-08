# Retrospectiva de Sprint

## Propósito
Facilitar uma retrospectiva de sprint estruturada — o que deu certo, o que não deu certo, e itens de ação priorizados com owners e prazos. Usado ao rodar retrospectivas, refletir sobre um sprint, criar itens de ação do feedback da equipe ou aprender a rodar retrospectivas eficazes.

## Como Funciona
Retrospectiva estruturada que gera insights e produz melhorias acionáveis. O processo usa formatos testados para coletar feedback, analisar performance do sprint e criar itens de ação concretos com responsáveis e métricas de sucesso.

## Quando Usar
- Final de cada sprint (quinzenal/mensal)
- Após projetos significativos
- Quando a equipe enfrenta desafios recorrentes
- Para melhoria contínua de processos
- Onboarding de novas equipes ágeis

## Formatos de Retrospectiva

### Formato A — Start / Stop / Continue
- **Start**: O que devemos começar a fazer?
- **Stop**: O que devemos parar de fazer?
- **Continue**: O que está funcionando bem que devemos manter?

**Ideal para:** Equipes novas, mudanças de processo, foco em comportamento

### Formato B — 4Ls (Liked / Learned / Lacked / Longed For)
- **Liked**: O que a equipe gostou?
- **Learned**: Que novo conhecimento foi adquirido?
- **Lacked**: O que estava faltando?
- **Longed For**: O que gostaríamos de ter?

**Ideal para:** Projetos complexos, aprendizado técnico, reflexão profunda

### Formato C — Sailboat
- **Wind (propels us)**: O que nos impulsiona para frente?
- **Anchor (holds us back)**: O que nos desacelera?
- **Rocks (risks)**: Que perigos à frente?
- **Island (goal)**: Para onde estamos tentando chegar?

**Ideal para:** Visão estratégica, identificação de riscos, alinhamento de equipe

## Passo a Passo

### 1. Escolher Formato de Retro
Baseado no contexto ou deixe a equipe escolher. Considere:
- Maturidade da equipe
- Natureza dos desafios recentes
- Objetivos específicos da retrospectiva
- Tempo disponível

### 2. Coletar Feedback Bruto
Se o usuário fornecer feedback bruto (notas adesivas, respostas de survey, mensagens Slack):
- Agrupe itens similares em temas
- Identifique os tópicos mais mencionados
- Note padrões de sentimento (frustração, energia, confusão)

### 3. Analisar Performance do Sprint
- **Objetivo do Sprint:** alcançado ou não?
- **Velocity vs. Commitment:** over-committed? under-committed?
- **Blockers encontrados** e como foram resolvidos
- **Padrões de colaboração** (o que funcionou, o que não)

### 4. Gerar Itens de Ação Priorizados

| Prioridade | Item de Ação | Owner | Prazo | Métrica de Sucesso |
|---|---|---|---|---|
| 1 | [Melhoria específica e acionável] | [Nome/Função] | [Data] | [Como saberemos que funcionou] |

**Diretrizes:**
- Limite a 2-3 itens de ação (mais não serão feitos)
- Cada um deve ser específico, atribuível e mensurável
- Referencie ações de retrospectivas anteriores se disponível

### 5. Criar Resumo da Retrospectiva

```
## Sprint [X] Retrospective — [Data]

### Performance do Sprint
- Objetivo: [Alcançado / Parcialmente / Perdido]
- Comprometido: [X pts] | Completo: [Y pts]

### Temas Principais
1. [Tema] — [resumo]

### Itens de Ação
1. [Ação] — [Owner] — [Até data]

### Carry-over da Retrospectiva Anterior
- [Ação anterior] — [Status: Feito / Em Progresso / Não Iniciado]
```

## Exemplo Prático

### Retrospectiva Sprint 12 - FinanControl

#### Contexto
- **Sprint:** 2 semanas, 21 points comprometidos
- **Equipe:** 6 membros (1 PM, 1 Designer, 4 Devs)
- **Formato:** 4Ls (Liked / Learned / Lacked / Longed For)

#### Coleta de Feedback (Notas Adesivas)

**Liked (8 notas):**
- "Colaboração excelente entre devs"
- "Daily calls produtivas"
- "Code review rigoroso"
- "Suporte mútuo em problemas complexos"
- "Design entregue no prazo"
- "Bugs resolvidos rapidamente"
- "Comunicação clara com PM"
- "Celebração de pequenas vitórias"

**Learned (6 notas):**
- "Redis mais complexo que esperávamos"
- "ML precisa de mais dados de treinamento"
- "API do banco tem limites não documentados"
- "Performance impacta adoção do usuário"
- "Testes automatizados salvaram tempo"
- "Documentação técnica é crucial"

**Lacked (7 notas):**
- "Tempo suficiente para spikes técnicos"
- "Clareza em alguns requisitos"
- "Ambiente de staging estável"
- "Ferramentas de debugging adequadas"
- "Mentoria para dev júnior"
- "Comunicação com time DevOps"
- "Processo de deploy claro"

**Longed For (5 notas):**
- "Mais tempo para refactoring"
- "Better integration testing"
- "Automated deployment pipeline"
- "Pair programming regular"
- "Technical debt allocation"

#### Análise de Performance do Sprint
- **Objetivo:** "Capacitar usuários a monitorar finanças em tempo real" — **Parcialmente alcançado**
- **Comprometido:** 21 points | **Completo:** 18 points (86%)
- **Blockers:** Problemas com Redis (2 dias), dependência DevOps (1 dia)
- **Colaboração:** Excelente, mas comunicação com times externas precisa melhorar

#### Temas Principais Identificados

1. **Técnico e Complexidade:** Desafios com Redis e ML, necessidade de mais tempo técnico
2. **Processo e Ferramentas:** Falta de ambiente estável, pipeline de deploy automatizado
3. **Colaboração:** Excelente trabalho interno, comunicação externa precisa melhorar
4. **Crescimento e Aprendizado:** Equipe aprendeu muito, mas precisa de mais mentorship

#### Itens de Ação Priorizados

| Prioridade | Item de Ação | Owner | Prazo | Métrica de Sucesso |
|---|---|---|---|---|
| 1 | Configurar ambiente de staging estável com Redis | Maria (DevOps) | 5 dias | 100% de deploys bem-sucedidos |
| 2 | Implementar pipeline de deploy automatizado | João (Tech Lead) | 2 semanas | Deploy <5 minutos, zero manual |
| 3 | Alocar 10% do sprint para technical debt | Pedro (PM) | Próximo sprint | Redução de 20% em bugs de regressão |

#### Carry-over da Retrospectiva Anterior
- **Ação anterior:** "Melhorar documentação de API" — **Status: Feito**
- **Ação anterior:** "Implementar mais testes unitários" — **Status: Em Progresso (70%)**

#### Resumo Final

```
## Sprint 12 Retrospective — 15 de Março de 2026

### Performance do Sprint
- Objetivo: Parcialmente alcançado (funcionalidades principais entregues, com atrasos técnicos)
- Comprometido: 21 pts | Completo: 18 pts (86%)

### Temas Principais
1. Desafios Técnicos — Redis e ML mais complexos que previsto, impactando timeline
2. Processos de Deploy — Ambiente instável e deploy manual atrasando entregas
3. Colaboração Interna — Excelente trabalho em equipe, comunicação clara
4. Crescimento Técnico — Equipe aprendendo rapidamente, precisa de mais estrutura

### Itens de Ação
1. Configurar ambiente staging estável — Maria — Até 20/03
2. Implementar pipeline deploy automatizado — João — Até 29/03  
3. Alocar 10% capacity para technical debt — Pedro — Próximo sprint

### Carry-over da Retrospectiva Anterior
- Melhorar documentação de API — Status: Feito
- Implementar mais testes unitários — Status: Em Progresso (70%)
```

## Modelos Adicionais

### Retro de Projeto (Não Sprint)
```
## Projeto [Nome] Retrospective — [Data]

### Resultados do Projeto
- Objetivos: [Alcançados / Parciais / Não alcançados]
- Timeline: [No prazo / Com atrasos / Adiantado]
- Orçamento: [Dentro / Acima / Abaixo]

### Lições Aprendidas
- [Técnico]: [Aprendizados técnicos]
- [Processo]: [Melhorias de processo]
- [Pessoas]: [Dinâmicas de equipe]

### Recomendações para Próximos Projetos
1. [Recomendação específica]
2. [Melhoria de processo]
3. [Alocação de recursos]
```

### Retro de Problema
```
## Retrospective: [Problema Específico] — [Data]

### O Que Aconteceu
- [Descrição do problema]
- [Impacto no time/produto]
- [Como foi resolvido]

### Causas Raiz
- [Causa 1]: [Descrição]
- [Causa 2]: [Descrição]

### Prevenção Futura
1. [Ação preventiva 1]
2. [Ação preventiva 2]
```

## Benefícios
- **Melhoria Contínua:** Identificação sistemática de melhorias
- **Engajamento:** Equipe se sente ouvida e valorizada
- **Aprendizado:** Captura de lições antes que se percam
- **Responsabilidade:** Itens de ação com owners claros

## Dicas de Uso
- Mantenha tom construtivo — objetivo é melhoria, não culpa
- Facilite participação de todos os membros
- Use timer para manter discussões focadas
- Documente e compartilhe resultados com stakeholders
- Acompanhe itens de ação entre retrospectivas

## Recursos Adicionais
- [Sprint Retrospectives: How to Run Effective Retros](https://www.productcompass.pm/p/sprint-retrospectives-guide)
- [Agile Ceremonies: The Complete Guide](https://www.productcompass.pm/p/agile-ceremonies-guide)
- [Team Health: How to Measure and Improve](https://www.productcompass.pm/p/team-health-measure-improve)
- [Psychological Safety in Teams](https://www.productcompass.pm/p/psychological-safety-teams)
