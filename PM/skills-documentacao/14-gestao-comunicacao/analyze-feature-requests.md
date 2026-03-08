# Análise de Requisitos de Features

## Propósito
Categorizar, avaliar e priorizar requisições de features de clientes contra objetivos de produto. Ajuda a transformar feedback bruto em insights acionáveis e roadmap estratégico focado em problemas, não em soluções.

## Como Funciona
A skill coleta requisições de features, categoriza em temas, avalia alinhamento estratégico, prioriza top 3 features baseadas em impacto, esforço, risco e alinhamento, e fornece análise detalhada com alternativas e planos de validação para cada feature priorizada.

## Quando Usar
- Analisar feedback de clientes em escala
- Priorizar backlog de features
- Validar demanda antes do desenvolvimento
- Alinhar roadmap com objetivos estratégicos
- Comunicar decisões de priorização

## Passo a Passo

### 1. Entender o Objetivo
Confirmar o objetivo do produto e outcomes desejados que guiarão a priorização:
- **Qual é a visão do produto?**
- **Quais métricas estamos tentando mover?**
- **Qual é o público alvo principal?**
- **Quais são as restrições (recursos, tempo, tecnologia)?**

### 2. Coletar Requisições de Features
Reunir dados de múltiplas fontes:
- **Customer Support:** Tickets, chats, chamadas
- **Sales Team:** Feedback de prospects e clientes
- **Product Analytics:** Comportamento de usuários
- **Surveys e Interviews:** Feedback direto
- **Community Forums:** Discussões e sugestões
- **Competitor Analysis:** Features que clientes mencionam

### 3. Categorizar Requisições em Temas
Agrupar requisições relacionadas em temas coesos:
- **Funcionalidade:** Features relacionadas a capacidades específicas
- **Experiência:** UI/UX, onboarding, usabilidade
- **Integração:** Conexões com outras ferramentas
- **Performance:** Velocidade, escalabilidade, confiabilidade
- **Preço/Monetização:** Modelos de preços, tiers
- **Plataforma:** Mobile, web, API, etc.

### 4. Avaliar Alinhamento Estratégico
Para cada tema, avaliar quão bem se alinha com objetivos:
- **Impacto no Negócio:** Como afeta receita, retenção, aquisição?
- **Impacto no Cliente:** Quanto melhora a vida do cliente?
- **Impacto na Estratégia:** Suporta visão de longo prazo?
- **Impacto na Competitividade:** Diferencia de concorrentes?

### 5. Priorizar Top 3 Features
Avaliar cada feature principal baseada em critérios:

**Impacto:**
- **Valor para Cliente:** Quantos clientes afetados? Quão importante?
- **Impacto no Negócio:** Receita, retenção, aquisição
- **Alinhamento Estratégico:** Suporta objetivos principais

**Esforço:**
- **Desenvolvimento:** Complexidade técnica, tempo necessário
- **Design:** Esforço de UX/UI, pesquisa necessária
- **Marketing:** Esforço para comunicar e lançar

**Risco:**
- **Technical Risk:** Complexidade, dependências, incerteza
- **Market Risk:** Adoção, timing, competitividade
- **Execution Risk:** Recursos, capacidades, timeline

**Alinhamento Estratégico:**
- **Fit com Visão:** Alinha com roadmap de longo prazo?
- **Synergies:** Cria valor com features existentes?
- **Differentiation:** Fortalece posicionamento?

### 6. Análise Detalhada das Features Priorizadas
Para cada feature no top 3:

**Raciocínio:**
- **Necessidades do Cliente:** Por que eles querem isso?
- **Alinhamento Estratégico:** Como isso suporta nossos objetivos?
- **Oportunidade:** Que problema de mercado isso atende?

**Soluções Alternativas:**
- **Abordagens Diferentes:** Outras formas de resolver o mesmo problema
- **Workarounds:** O que clientes fazem hoje?
- **Simplificações:** Versão MVP ou abordagem incremental

**Suposições de Alto Risco:**
- **Adoção:** Clientes realmente usarão?
- **Valor:** Isso realmente resolve o problema?
- **Viabilidade:** Podemos construir e manter?

**Como Testar com Mínimo Esforço:**
- **Fake Door:** Testar interesse sem construir
- **Concierge MVP:** Entregar valor manualmente
- **Survey:** Validar necessidade e willingness to pay
- **Prototype:** Testar usabilidade e valor

## Framework de Opportunity Score

### Cálculo do Opportunity Score
**Opportunity Score = Importance × (1 - Satisfaction)**

**Importance (1-10):**
- Quão importante é este problema para o cliente?
- Com que frequência eles enfrentam este problema?
- Qual é o impacto de não resolver?

**Satisfaction (1-10):**
- Quão satisfeitos estão com soluções atuais?
- Quão bem as alternativas atuais funcionam?
- Quão fácil é resolver com workarounds?

**Interpretação:**
- **Alto Score (7-10):** Oportunidade clara, alta demanda
- **Médio Score (4-6):** Oportunidade moderada, validar mais
- **Baixo Score (1-3):** Baixa prioridade, considerar depois

## Exemplo Prático

**Produto:** "CollabSync" - Plataforma de colaboração para equipes remotas

### Objetivo do Produto
- **Visão:** Tornar trabalho remoto tão produtivo quanto presencial
- **Métricas:** Redução de reuniões, aumento de produtividade
- **Público:** Equipes 20-200 funcionários, distribuídas globalmente

### Requisições Coletadas (Exemplo)
1. "Integração com Slack para notificações"
2. "Modo dark mode para interface"
3. "Templates de projetos prontos"
4. "Gravação de reuniões automática"
5. "Analytics de engajamento da equipe"
6. "API para customizações"
7. "Suporte a múltiplos idiomas"
8. "Integração com calendário"
9. "Kanban boards visual"
10. "Time tracking integrado"

### Categorização em Temas
- **Integrações:** Slack, calendário, API
- **Experiência:** Dark mode, templates, kanban boards
- **Analytics:** Engajamento da equipe, time tracking
- **Core Features:** Gravação de reuniões, múltiplos idiomas

### Avaliação de Alinhamento Estratégico
**Integrações (Score 8/10):** Aumenta produtividade, reduz switching
**Experiência (Score 6/10):** Melhora usabilidade, mas não core
**Analytics (Score 7/10):** Mede sucesso, ajuda justificar valor
**Core Features (Score 9/10):** Diretamente ligado à visão

### Top 3 Features Priorizadas

**1. Gravação de Reuniões Automática**
- **Impacto:** Alto - resolve dor principal de equipes remotas
- **Esforço:** Médio - tecnologia existente, integração necessária
- **Risco:** Médio - storage costs, compliance
- **Alinhamento:** Alto - core à visão do produto

**2. Integração com Calendário**
- **Impacto:** Alto - melhora scheduling e context
- **Esforço:** Baixo - APIs padrão disponíveis
- **Risco:** Baixo - tecnologia madura
- **Alinhamento:** Alto - suporta produtividade

**3. Analytics de Engajamento**
- **Impacto:** Médio - ajuda medir valor, justificar ROI
- **Esforço:** Médio - requer desenvolvimento específico
- **Risco:** Baixo - dados já disponíveis
- **Alinhamento:** Médio - suporta estratégia mas não core

### Análise Detalhada - Gravação de Reuniões

**Raciocínio:**
- **Necessidade:** Equipes remotas perdem contexto, têm muitas reuniões
- **Alinhamento:** Diretamente ligado à redução de reuniões (métrica chave)
- **Oportunidade:** Mercado crescente, poucos concorrentes focados em remote

**Soluções Alternativas:**
- **Integração com Zoom:** Mais rápido, menos controle
- **Notas AI-driven:** Mais barato, menos completo
- **Transcrição apenas:** Simples, mas sem vídeo

**Suposições de Alto Risco:**
- **Adoção:** Equipes permitirão gravação? (privacidade)
- **Valor:** Realmente reduzirá número de reuniões?
- **Viabilidade:** Conseguimos escalar storage?

**Como Testar:**
- **Fake Door:** Botão "Gravar Reunião" no dashboard atual
- **Survey:** Validar necessidade e willingness to pay
- **Concierge MVP:** Gravação manual para 10 equipes

## Benefícios

- **Foco Estratégico:** Alinha desenvolvimento com objetivos de negócio
- **Voz do Cliente:** Transforma feedback em insights acionáveis
- **Priorização Baseada em Dados:** Decisões justificáveis e transparentes
- **Redução de Risco:** Validação antes de investimento pesado
- **Comunicação Clara:** Base para explicar decisões aos stakeholders

## Dicas de Uso

### Para Melhores Resultados:
1. **Foque em Problemas:** Não deixe clientes designar soluções
2. **Use Dados Quantitativos:** Métricas para justificar priorizações
3. **Envolva Stakeholders:** Inclua vendas, suporte, engenharia
4. **Seja Transparente:** Compartilhe critérios e raciocínio

### Erros Comuns a Evitar:
- Aceitar todas as requisições sem análise
- Priorizar baseado apenas em volume de requests
- Ignorar alinhamento estratégico
- Não validar suposições críticas

## Formato de Saída

**Análise Completa Incluindo:**
- Categorização de requisições em temas
- Avaliação de alinhamento estratégico
- Top 3 features priorizadas com raciocínio
- Análise detalhada de cada feature prioritária
- Planos de validação de baixo esforço
- Recomendações de implementação

## Framework

Baseado em Opportunity Score de Dan Olsen. Foca em identificar oportunidades (problemas) em vez de features, usando a fórmula: Opportunity Score = Importance × (1 - Satisfaction).

## Recursos Adicionais

- **Kano Model:** [Kano Model Guide](https://www.productcompass.pm/p/kano-model-how-to-delight-your-customers)
- **CPDM:** [Continuous Product Discovery Masterclass](https://www.productcompass.pm/p/cpdm)

---

## Template de Análise

### Para Cada Feature Priorizada
```
**Feature:** [Nome da feature]
**Priority Score:** [Impacto × Esforço × Alinhamento]

**Raciocínio:**
- Necessidades do cliente: [Descrição]
- Alinhamento estratégico: [Como suporta objetivos]
- Oportunidade: [Problema de mercado]

**Soluções Alternativas:**
- [Alternativa 1]: [Prós/Contras]
- [Alternativa 2]: [Prós/Contras]

**Suposições de Alto Risco:**
- [Suposição 1]: [Como testar]
- [Suposição 2]: [Como testar]

**Plano de Validação:**
- [Experimento]: [Descrição]
- [Timeline]: [Semanas]
- [Success Criteria]: [Como saber se validado]
```

## Checklist de Implementação

### Coleta e Análise
- [ ] Requisições coletadas de múltiplas fontes
- [ ] Dados limpos e padronizados
- [ ] Categorização em temas completada
- [ ] Alinhamento estratégico avaliado

### Priorização
- [ ] Critérios de priorização definidos
- [ ] Scores calculados consistentemente
- [ ] Top 3 features selecionadas
- [ ] Raciocínio documentado

### Validação
- [ ] Planos de validação criados
- [ ] Experimentos de baixo esforço definidos
- [ ] Critérios de sucesso estabelecidos
- [ ] Timeline de execução planejado

---

**Próximos Passos:**
- Executar planos de validação
- Monitorar métricas de adoption
- Iterar baseado em aprendizados
- Comunicar decisões e roadmap
- Revisar priorizações trimestralmente
