# Resumo de Reuniões

## Propósito
Criar resumos estruturados e acionáveis de reuniões a partir de transcrições ou notas. Transforma conteúdo bruto de reuniões em summaries claros que mantêm equipes alinhadas e responsáveis, garantindo que decisões e action items não se percam.

## Como Funciona
A skill coleta conteúdo da reunião, identifica participantes e tópicos, extrai pontos chave, decisões e action items, estrutura informações em template claro e acessível, e salva como documento markdown para fácil referência e compartilhamento.

## Quando Usar
- Processar transcrições de reuniões importantes
- Documentar decisões estratégicas
- Criar registro para quem não participou
- Manter alinhamento entre equipes multifuncionais
- Estabelecer accountability para action items

## Passo a Passo

### 1. Coletar Conteúdo da Reunião
Se o usuário fornecer transcrição, gravação ou notas da reunião, ler completamente. Se mencionar uma reunião que precisa de contexto, usar web search para encontrar materiais relacionados ou documentos de background.

### 2. Pensar Passo a Passo
- **Quem participou e quais eram seus papéis?**
- **Qual foi o tópico principal ou agenda?**
- **Quais decisões foram tomadas?**
- **Quais são os próximos passos e quem são os responsáveis?**
- **Existem perguntas abertas ou bloqueadores?**

### 3. Extrair Informações Chave
Identificar e organizar:
- **Tópicos Principais:** Pontos de discussão ou decisão
- **Decisões Tomadas:** Resultados importantes da reunião
- **Desacordos ou Preocupações:** Pontos de discordância ou preocupações
- **Action Items:** O que cada pessoa precisa fazer
- **Prazos:** Quando cada action item deve ser completado

### 4. Criar Resumo Estruturado
Usar este template:

```
## Resumo da Reunião

**Data & Hora:** [Data e hora de início/término]

**Participantes:** [Nomes completos e papéis, se disponíveis]

**Tópico:** [Título curto — sobre o que foi a reunião?]

**Resumo**

- **Ponto 1:** [Ponto de discussão ou decisão chave]
- **Ponto 2:** [Ponto de discussão ou decisão chave]
- **Ponto 3:** [Ponto de discussão ou decisão chave]
- [Pontos adicionais conforme necessário]

**Action Items**

| Data Limite | Responsável | Action |
|-------------|-------------|--------|
| [Data] | [Nome] | [O que precisa acontecer] |
| [Data] | [Nome] | [O que precisa acontecer] |

**Decisões Tomadas**
- [Decisão 1]
- [Decisão 2]

**Perguntas Abertas**
- [Pergunta não resolvida 1]
- [Pergunta não resolvida 2]
```

### 5. Usar Linguagem Acessível
Escrever para quem se formou no ensino fundamental. Use termos simples. Evite jargões ou explique brevemente.

### 6. Priorizar Clareza
Foque em:
- **Quais decisões afetam o roadmap ou estratégia?**
- **O que cada pessoa precisa fazer?**
- **Até quando elas precisam fazer?**

### 7. Salvar o Output
Salvar como documento markdown: `Meeting-Summary-[data]-[tópico].md`

## Template Detalhado

### Header Básico
```
## Resumo da Reunião

**Data:** 15 de março de 2026
**Horário:** 14:00 - 15:30
**Tipo:** Reunião de Planejamento de Produto
**Local:** Sala de Reuniões Virtuais / Google Meet
```

### Lista de Participantes
```
**Participantes:**
- João Silva (Product Manager) - Host
- Maria Santos (Lead Designer) 
- Pedro Costa (Tech Lead)
- Ana Oliveira (Marketing Manager)
- Carlos Ferreira (CEO)
```

### Resumo Executivo
```
**Tópico:** Planejamento Q2 2026 - Features Prioritárias

**Resumo:**
- Discutimos prioridades para Q2 baseadas em feedback de clientes
- Decidimos focar em 3 features principais: onboarding melhorado, analytics dashboard, integração com Slack
- Alinhamos timeline e recursos necessários
- Identificamos necessidade de pesquisa adicional com usuários
```

### Action Items Detalhados
```
**Action Items:**

| Data Limite | Responsável | Action | Status |
|-------------|-------------|--------|--------|
| 22/03/2026 | Maria Santos | Criar wireframes para onboarding | Em andamento |
| 25/03/2026 | Pedro Costa | Avaliar esforço técnico para integração Slack | Não iniciado |
| 29/03/2026 | João Silva | Conduzir 5 entrevistas com usuários sobre analytics | Não iniciado |
| 01/04/2026 | Ana Oliveira | Preparar plano de marketing para Q2 | Não iniciado |
```

### Decisões Importantes
```
**Decisões Tomadas:**
- Priorizar onboarding melhorado como feature #1 do Q2
- Alocar 40% do budget de desenvolvimento para analytics dashboard
- Adiar integração com Salesforce para Q3
- Contratar 1 designer freelance para ajudar com onboarding
```

### Perguntas em Aberto
```
**Perguntas Abertas:**
- Qual será o pricing para novo plano com analytics avançado?
- Como mediremos sucesso do novo onboarding?
- Precisamos de aprovação legal para mudanças de termos?
```

### Próximos Passos
```
**Próximos Passos:**
- Próxima reunião de acompanhamento: 29/03/2026
- Revisão de wireframes: 24/03/2026
- Apresentação ao leadership: 05/04/2026
```

## Exemplo Prático

**Contexto:** Reunião de planejamento de produto para Q2

### Resumo Gerado

```
## Resumo da Reunião

**Data & Hora:** 15 de março de 2026, 14:00 - 15:30

**Participantes:**
- João Silva (Product Manager) - Host
- Maria Santos (Lead Designer)
- Pedro Costa (Tech Lead)
- Ana Oliveira (Marketing Manager)
- Carlos Ferreira (CEO)

**Tópico:** Planejamento Q2 2026 - Features Prioritárias

**Resumo**

- **Feedback de Clientes:** Analisamos 50+ tickets de suporte e requests de features
- **Prioridades Q2:** Decidimos focar em experiência do usuário e métricas
- **Recursos:** Temos capacidade para 2 features grandes + 1 pequena
- **Timeline:** Lançamentos planejados para maio e junho

**Action Items**

| Data Limite | Responsável | Action |
|-------------|-------------|--------|
| 22/03/2026 | Maria Santos | Criar wireframes para onboarding melhorado |
| 25/03/2026 | Pedro Costa | Avaliar esforço técnico para analytics dashboard |
| 29/03/2026 | João Silva | Conduzir entrevistas com 5 usuários sobre analytics |
| 01/04/2026 | Ana Oliveira | Preparar plano de marketing para lançamentos Q2 |

**Decisões Tomadas**
- Priorizar onboarding melhorado como feature principal do Q2
- Incluir analytics dashboard básico no lançamento de maio
- Adiar integração avançada com Slack para Q3
- Alocar budget adicional para pesquisa com usuários

**Perguntas Abertas**
- Como mediremos sucesso do novo onboarding?
- Qual será o pricing para plano com analytics?
- Precisamos de aprovação legal para mudanças?

**Próxima Reunião:** 29/03/2026 - Revisão de wireframes e progresso técnico
```

## Benefícios

- **Alinhamento:** Todos entendem o que foi decidido
- **Accountability:** Responsáveis e prazos claramente definidos
- **Memória Institucional:** Registro para referência futura
- **Inclusão:** Pessoas que não participam ficam atualizadas
- **Eficiência:** Foco no que realmente importa

## Dicas de Uso

### Para Melhores Resultados:
1. **Seja Objetivo:** Resuma o que foi discutido, não opiniões pessoais
2. **Destaque Action Items:** Garanta que nada caia pelas fissuras
3. **Use Linguagem Simples:** Evite jargões técnicos desnecessários
4. **Seja Específico:** Inclua nomes, datas e detalhes concretos

### Erros Comuns a Evitar:
- Incluir demasiados detalhes irrelevantes
- Não definir responsáveis claros para action items
- Usar linguagem muito técnica ou corporativa
- Esquecer de incluir decisões importantes

## Formato de Saída

**Documento Markdown Estruturado Incluindo:**
- Header com informações básicas da reunião
- Lista de participantes e papéis
- Resumo executivo dos pontos principais
- Tabela de action items com responsáveis e prazos
- Lista de decisões tomadas
- Perguntas abertas e próximos passos

## Melhores Práticas

### Durante a Reunião
- **Tire Notas:** Registre pontos importantes em tempo real
- **Identifique Action Items:** Anote quem disse que faria o quê
- **Confirme Decisões:** Repita decisões para garantir alinhamento
- **Marque Prazos:** Anote quando as coisas precisam ser feitas

### Após a Reunião
- **Revise Notas:** Verifique se faltou algo importante
- **Envie Rápido:** Compartilhe summary dentro de 24 horas
- **Peça Feedback:** Confirme se está claro e completo
- **Arquive:** Salve em local acessível para referência futura

## Recursos Adicionais

- **Meeting Facilitation:** [Effective Meeting Guide](https://www.productcompass.pm/p/effective-meetings)
- **Action Management:** [Action Item Tracking](https://www.productcompass.pm/p/action-tracking)

---

## Template Avançado

### Para Reuniões Estratégicas
```
## Resumo da Reunião Estratégica

**Contexto:** [Por que esta reunião foi necessária]
**Objetivos:** [O que esperávamos alcançar]
**Participantes:** [Níveis senioridade presentes]

**Insights Chave:**
- [Insight 1 com dados]
- [Insight 2 com dados]
- [Insight 3 com dados]

**Decisões Estratégicas:**
- [Decisão 1] - Impacto: [Alto/Médio/Baixo]
- [Decisão 2] - Impacto: [Alto/Médio/Baixo]

**Mudanças no Roadmap:**
- [Mudança 1] - Timeline: [Nova data]
- [Mudança 2] - Recursos: [Adicionais/Reduzidos]

**Riscos Identificados:**
- [Risco 1] - Plano de mitigação: [Ação]
- [Risco 2] - Plano de mitigação: [Ação]
```

### Para Reuniões de Status
```
## Resumo da Reunião de Status

**Período:** [Período coberto]
**Métricas Chave:**
- [Métrica 1]: [Valor atual vs meta]
- [Métrica 2]: [Valor atual vs meta]

**Progresso por Initiative:**
- [Initiative 1]: [Status] - [Próximos passos]
- [Initiative 2]: [Status] - [Próximos passos]

**Bloqueadores:**
- [Bloqueador 1]: [Responsável pela resolução] - [Prazo]
- [Bloqueador 2]: [Responsável pela resolução] - [Prazo]

**Celebrations:**
- [Sucesso 1] - [Mérito]
- [Sucesso 2] - [Mérito]
```

## Checklist de Qualidade

### Conteúdo
- [ ] Todos os participantes listados com papéis
- [ ] Tópico principal claramente identificado
- [ ] Pontos chave resumidos de forma concisa
- [ ] Decisões importantes destacadas
- [ ] Action items com responsáveis e prazos

### Clareza
- [ ] Linguagem simples e acessível
- [ ] Estrutura lógica e fácil de seguir
- [ ] Formatação consistente
- [ ] Sem jargões desnecessários

### Completude
- [ ] Próximos passos definidos
- [ ] Perguntas abertas documentadas
- [ ] Informações de contato se necessário
- [ ] Links para recursos relevantes

---

**Próximos Passos:**
- Enviar summary para todos os participantes
- Agendar follow-ups para action items
- Arquivar para referência futura
- Usar como input para próximas reuniões
- Monitorar completion de action items
