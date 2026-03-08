# Planejamento de Sprint

## Propósito
Planejar um sprint com estimativa de capacidade, seleção de stories, mapeamento de dependências e identificação de riscos. Usado ao se preparar para planejamento de sprint, estimar capacidade da equipe, selecionar stories ou equilibrar escopo do sprint contra velocity.

## Como Funciona
Planejamento de sprint estruturado que estima capacidade da equipe, seleciona e sequencia stories apropriados, identifica dependências e riscos, e cria um plano claro com objetivo de sprint definido.

## Quando Usar
- Planejamento de sprint (quinzenal/mensal)
- Replanejamento de sprint em andamento
- Onboarding de novas equipes ágeis
- Melhoria de processo de planejamento
- Capacitação de Product Owners

## Passo a Passo

### 1. Estimar Capacidade da Equipe
- **Número de membros da equipe e disponibilidade** (PTO, reuniões, on-call)
- **Velocity histórica** (média de story points por sprint dos últimos 3 sprints)
- **Buffer de capacidade**: reserve 15-20% para trabalho inesperado, bugs e tech debt
- **Calcular capacidade disponível** em story points ou ideal hours

**Cálculo de Capacidade:**
```
Capacidade Bruta = (Membros × Dias úteis × Horas/dia) - Horas de reuniões
Capacidade Líquida = Capacidade Bruta × (1 - Buffer %)
```

### 2. Revisar e Selecionar Stories
- **Puxe do backlog priorizado** (maior prioridade primeiro)
- **Verifique se cada story atende Definition of Ready** (AC claros, estimado, sem bloqueadores)
- **Sinalize stories que precisam de refinement antes de comprometer**
- **Pare de adicionar stories quando capacidade for alcançada**

**Definition of Ready Checklist:**
- ✅ Critérios de aceitação claros e testáveis
- ✅ Estimativa de story points ou ideal hours
- ✅ Dependências identificadas e bloqueadas
- ✅ Design e especificações técnicas disponíveis
- ✅ Valor de negócio claro e prioridade definida

### 3. Mapear Dependências
- **Identifique stories que dependem de outras stories ou equipes externas**
- **Sequencie stories dependentes apropriadamente**
- **Sinalize dependências externas e owners**
- **Identifique o caminho crítico**

**Tipos de Dependências:**
- **Técnicas:** Story B precisa que Story A implemente API primeiro
- **Funcionais:** Story C só faz sentido após Story B estar funcionando
- **Externas:** Story D depende de equipe de infraestrutura ou terceiros
- **Dados:** Story E precisa que Story F migre dados primeiro

### 4. Identificar Riscos e Mitigações
- **Stories com alta incerteza ou complexidade**
- **Dependências externas que podem atrasar**
- **Concentração de conhecimento** (apenas uma pessoa consegue fazer)
- **Sugerir mitigações para cada risco**

**Categorias de Risco:**
- **Técnicos:** Tecnologia desconhecida, integrações complexas
- **De Pessoas:** Férias, doença, conhecimento concentrado
- **Escopo:** Requisitos ambíguos, mudanças late-binding
- **Externos:** Dependências de outras equipes, terceiros

### 5. Criar Resumo do Plano de Sprint

```
Objetivo do Sprint: [Uma frase descrevendo o que o sucesso parece]
Duração: [2 semanas / 1 semana / etc.]
Capacidade da Equipe: [X story points]
Stories Comprometidos: [Y story points em Z stories]
Buffer: [capacidade restante]

Stories:
1. [Título da Story] — [pontos] — [owner] — [dependências]
...

Riscos:
- [Risco] → [Mitigação]
```

### 6. Definir Objetivo do Sprint
Uma frase clara e única que captura a entrega primária de valor do sprint.

**Formatos de Objetivo de Sprint:**
- **Focado no Cliente:** "Capacitar usuários a [fazer X] para que [benefício Y]"
- **Focado no Negócio:** "Aumentar [métrica] em [X]% através de [features]"
- **Focado na Equipe:** "Entregar [value] para validar [learning]"

## Exemplo Prático

### Planejamento de Sprint: FinanControl v2.1

#### 1. Estimativa de Capacidade
- **Equipe:** 6 membros (1 PM, 1 Designer, 4 Devs)
- **Dias úteis:** 10 dias (2 semanas)
- **Disponibilidade:** 80% (considerando reuniões, cerimônias)
- **Velocity histórica:** 28 points/sprint (média últimos 3 sprints)
- **Buffer:** 20% para bugs inesperados

**Cálculo:**
- Capacidade bruta: 28 points
- Buffer: 28 × 20% = 5.6 points
- **Capacidade líquida: 22.4 points**

#### 2. Stories Selecionadas

**Stories Prioritárias do Backlog:**
1. **Dashboard de Saldo em Tempo Real** — 8 points
2. **Categorização Automática com IA** — 5 points  
3. **Alertas de Orçamento** — 3 points
4. **Exportação PDF de Relatórios** — 3 points
5. **Melhorias de Performance** — 2 points

**Total:** 21 points (dentro da capacidade de 22.4)

#### 3. Mapeamento de Dependências

**Dependências Identificadas:**
- **Story 1** depende de **Infraestrutura** (Redis setup) - **Owner: Time DevOps**
- **Story 2** depende de **Story 1** (dados do dashboard) - **Interna**
- **Story 3** independente - **Sem dependências**
- **Story 4** depende de **Story 1** (dados de relatórios) - **Interna**
- **Story 5** independente - **Sem dependências**

**Sequenciamento:**
1. Week 1: Story 1 (com dependência DevOps), Story 3, Story 5
2. Week 2: Story 2, Story 4

#### 4. Riscos e Mitigações

**Riscos Identificados:**
- **Risco Técnico:** Integração Redis pode ser mais complexa que esperado
  - **Mitigação:** Spike técnico no dia 1, plano B de cache local
- **Risco de Pessoas:** Apenas 1 dev conhece algoritmos de ML
  - **Mitigação:** Pair programming, documentação antecipada
- **Risco Externo:** API do banco pode ter rate limiting
  - **Mitigação:** Testes de carga, implementação de retry
- **Risco de Escopo:** Requisitos de categorização podem mudar
  - **Mitigação:** Daily check-in com PM, protótipo rápido

#### 5. Resumo do Plano

```
Objetivo do Sprint: Capacitar usuários a monitorar finanças em tempo real e economizar tempo através de automação inteligente
Duração: 2 semanas
Capacidade da Equipe: 22.4 story points
Stories Comprometidos: 21 story points em 5 stories
Buffer: 1.4 points para bugs inesperados

Stories:
1. Dashboard de Saldo em Tempo Real — 8 points — Maria — Dep: DevOps (Redis)
2. Categorização Automática com IA — 5 points — João — Dep: Story 1
3. Alertas de Orçamento — 3 points — Ana — Sem dependências
4. Exportação PDF de Relatórios — 3 points — Pedro — Dep: Story 1
5. Melhorias de Performance — 2 points — Carlos — Sem dependências

Riscos:
- Complexidade Redis → Spike técnico dia 1, plano B cache local
- Conhecimento ML concentrado → Pair programming, docs antecipadas
- Rate limiting API banco → Testes carga, implementação retry
- Mudança requisitos categorização → Daily check-in PM, protótipo rápido
```

## Modelos por Tipo de Sprint

### Sprint de Descoberta
```
Objetivo: Validar [hipótese] através de [experimentos] para informar roadmap
Capacidade: Foco em aprendizado vs. entrega
Stories: Protótipos, entrevistas, testes A/B
Riscos: Hipóteses podem ser invalidadas
```

### Sprint de Técnico
```
Objetivo: Modernizar [infraestrutura] para permitir [escala/segurança]
Capacidade: Foco em trabalho técnico vs. features visíveis
Stories: Migrações, refactoring, performance
Riscos: Complexidade técnica, regressões
```

### Sprint de Crescimento
```
Objetivo: Aumentar [métrica] em [X]% através de [otimizações]
Capacidade: Foco em otimizações vs. novas funcionalidades
Stories: A/B tests, otimizações de conversão, analytics
Riscos: Impacto menor que esperado
```

## Benefícios
- **Realismo:** Planos baseados em capacidade real vs. otimismo
- **Clareza:** Objetivo claro alinha equipe em torno do valor
- **Preparação:** Identificação proativa de riscos e dependências
- **Foco:** Commitment realista vs. over-commitment

## Dicas de Uso
- Use dados históricos reais para estimar capacidade
- Envolva toda a equipe no planejamento (não apenas PM)
- Seja conservador no primeiro sprint com nova equipe
- Revise e ajuste o plano durante o sprint se necessário
- Documente aprendizados para melhorar próximos sprints

## Recursos Adicionais
- [Product Owner vs Product Manager: What's the difference?](https://www.productcompass.pm/p/product-manager-vs-product-owner)
- [Agile Estimation: Story Points vs Hours](https://www.productcompass.pm/p/agile-estimation-guide)
- [Sprint Retrospectives: How to Run Effective Retros](https://www.productcompass.pm/p/sprint-retrospectives-guide)
- [Velocity Management: Best Practices](https://www.productcompass.pm/p/velocity-management)
