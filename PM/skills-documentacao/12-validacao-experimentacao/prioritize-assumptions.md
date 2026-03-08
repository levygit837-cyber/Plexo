# Priorização de Suposições

## Propósito
Priorizar suposições usando matriz Impacto × Risco com sugestões de experimentos para cada. Ajuda a focar recursos de validação nas suposições mais críticas que, se provadas falsas, mais impactariam o sucesso do produto.

## Como Funciona
A skill mapeia todas as suposições identificadas, avalia cada uma em duas dimensões (impacto se falsa e confiança atual), posiciona na matriz 2x2, sugere experimentos específicos por quadrante e cria roadmap de validação focado em aprendizado rápido.

## Quando Usar
- Após identificar suposições de risco
- Para planejar estratégia de experimentação
- Para alocar recursos limitados de validação
- Para justificar prioridades para stakeholders
- Para criar roadmap de aprendizado

## Passo a Passo

### 1. Mapear Todas as Suposições
Listar todas as suposições identificadas:
- **Suposições de Valor:** As pessoas realmente querem isso?
- **Suposições de Usabilidade:** As pessoas conseguem usar?
- **Suposições de Viabilidade:** Podemos monetizar isso?
- **Suposições de Viabilidade Técnica:** Conseguimos construir?
- **Suposições de GTM:** Conseguimos alcançar clientes?
- **Suposições de Estratégia:** Este é o momento certo?
- **Suposições de Equipe:** Temos as pessoas certas?

### 2. Avaliar Impacto se Falsa
Para cada suposição, avaliar o impacto se for falsa:
- **Crítico (9-10):** Falha mataria o projeto completamente
- **Alto (7-8):** Falha requereria mudança significativa no plano
- **Médio (5-6):** Falha causaria problemas mas é recuperável
- **Baixo (1-4):** Falha causaria inconvenientes menores

### 3. Avaliar Confiança Atual
Para cada suposição, avaliar o nível atual de confiança:
- **Baixa (1-3):** Pouca ou nenhuma evidência, principalmente suposição
- **Média (4-6):** Alguma evidência mas não conclusiva
- **Alta (7-9):** Evidências fortes mas não 100% confirmada
- **Muito Alta (10):** Quase certeza, validado extensivamente

### 4. Posicionar na Matriz
Colocar cada suposição na matriz Impacto × Confiança:

```
          Confiança Alta    Confiança Baixa
Impacto    +----------------+----------------+
Alto       |   Monitorar    |   Testar AGORA  |
           |   (Q4)         |      (Q1)       |
           +----------------+----------------+
Baixo      |   Aceitar      |   Testar DEPOIS |
           |   (Q3)         |      (Q2)       |
           +----------------+----------------+
```

### 5. Sugerir Experimentos por Quadrante

#### Quadrante 1: Alto Impacto, Baixa Confiança (Testar AGORA)
- **Prioridade:** Máxima
- **Timeline:** 1-2 semanas
- **Experimentos:** Rápidos e baratos
- **Exemplo:** Landing page test, fake door, survey

#### Quadrante 2: Baixo Impacto, Baixa Confiança (Testar DEPOIS)
- **Prioridade:** Média
- **Timeline:** 1-2 meses
- **Experimentos:** Mais elaborados se necessário
- **Exemplo:** Protótipo funcional, análise de dados

#### Quadrante 3: Baixo Impacto, Alta Confiança (Aceitar)
- **Prioridade:** Baixa
- **Timeline:** Monitorar ocasionalmente
- **Experimentos:** Não necessários inicialmente
- **Exemplo:** Documentar e revisar trimestralmente

#### Quadrante 4: Alto Impacto, Alta Confiança (Monitorar)
- **Prioridade:** Média
- **Timeline:** Monitorar contínuo
- **Experimentos:** Verificação periódica
- **Exemplo:** Análise de métricas, check-ins mensais

### 6. Criar Roadmap de Validação
Definir sequência e timing:
- **Fase 1 (Semanas 1-2):** Testar suposições Q1
- **Fase 2 (Semanas 3-4):** Analisar resultados Q1, ajustar
- **Fase 3 (Meses 2-3):** Testar suposições Q2 se necessário
- **Fase 4 (Contínuo):** Monitorar Q3, verificar Q4

## Matriz de Priorização Detalhada

### Quadrante 1: Testar AGORA (Alto Impacto, Baixa Confiança)

**Características:**
- Falha destas suposições mataria o projeto
- Pouca ou nenhuma evidência atual
- Maior risco e incerteza

**Tipos de Experimentos:**
- **Landing Page Test:** Testar interesse e demanda
- **Fake Door Test:** Testar interesse em funcionalidades
- **Survey Validation:** Testar suposições com prospects
- **Concierge MVP:** Testar valor com serviço manual
- **Pre-order Campaign:** Testar disposição para pagar

**Exemplos:**
- "As pessoas pagariam $50/mês por isso" → Landing page com pricing test
- "Conseguimos alcançar nosso público alvo" → Teste de canal com pequeno orçamento

---

### Quadrante 2: Testar DEPOIS (Baixo Impacto, Baixa Confiança)

**Características:**
- Falha causaria problemas mas é recuperável
- Alguma incerteza mas não crítica
- Importante para otimização futura

**Tipos de Experimentos:**
- **Protótipo Funcional:** Testar usabilidade e fluxos
- **Análise Competitiva:** Testar posicionamento
- **Teste de Performance:** Validar requisitos técnicos
- **Survey de Satisfação:** Testar experiência do usuário

**Exemplos:**
- "Os usuários preferem workflow A vs B" → A/B test com protótipos
- "Nossa UI é intuitiva" → Testes de usabilidade detalhados

---

### Quadrante 3: Aceitar (Baixo Impacto, Alta Confiança)

**Características:**
- Falha causaria inconvenientes menores
- Evidências fortes ou validação anterior
- Baixo risco, alta confiança

**Ação:**
- Aceitar como verdade para agora
- Monitorar periodicamente
- Documentar para referência futura

**Exemplos:**
- "Tecnologia X suporta nossos requisitos" → Aceitar, monitorar performance
- "Equipe tem skills básicas necessárias" → Aceitar, revisar anualmente

---

### Quadrante 4: Monitorar (Alto Impacto, Alta Confiança)

**Características:**
- Falha seria crítica mas temos alta confiança
- Evidências fortes mas mercado pode mudar
- Importante manter validação atual

**Ação:**
- Monitorar métricas relevantes
- Verificar periodicamente com dados
- Estar pronto para pivotar se necessário

**Exemplos:**
- "Nosso preço de $50/mês é ótimo" → Monitorar conversão e churn
- "Nosso canal principal é LinkedIn" → Monitorar CAC e performance

## Exemplo Prático

**Produto:** "AI Meeting Assistant"

### Suposições Mapeadas

| Suposição | Impacto | Confiança | Quadrante | Experimento |
|------------|---------|-----------|-----------|-------------|
| Pessoas pagam $50/mês | 9 | 3 | Q1 | Landing page com pricing |
| Tech suporta 95% precisão | 8 | 2 | Q1 | POC técnico |
| Usuários entendem sem treino | 6 | 4 | Q2 | Protótipo testado |
| LinkedIn ads funcionam | 7 | 6 | Q4 | Monitorar CAC mensalmente |
| UI é intuitiva | 4 | 7 | Q3 | Aceitar, monitorar feedback |

### Roadmap de Validação

**Semanas 1-2 (Q1):**
- Teste de pricing com landing page
- POC técnico de precisão

**Semanas 3-4:**
- Analisar resultados Q1
- Se pricing validado, testar usabilidade (Q2)

**Mês 2-3:**
- Testar protótipo funcional se necessário
- Continuar monitoramento Q4

**Contínuo:**
- Monitorar métricas de GTM
- Revisar suposições Q3 trimestralmente

## Benefícios

- **Foco Estratégico:** Recursos focados nos maiores riscos
- **Aprendizado Rápido:** Validação das incertezas mais críticas primeiro
- **Gestão de Riscos:** Visão clara do perfil de risco do projeto
- **Alinhamento de Equipe:** Consenso sobre prioridades de validação
- **Adaptabilidade:** Flexibilidade para ajustar estratégia baseada em aprendizados

## Dicas de Uso

### Para Melhores Resultados:
1. **Seja Conservador:** Subestime confiança, superestime impacto
2. **Envolve a Equipe:** Discuta prioridades com diferentes perspectivas
3. **Atualize Regularmente:** Revisar matriz a cada aprendizado significativo
4. **Documente Tudo:** Mantenha registro de suposições e resultados

### Erros Comuns a Evitar:
- Ignorar suposições por parecerem "óbvias"
- Testar tudo ao mesmo tempo sem priorização
- Não atualizar confiança baseada em novos dados
- Esquecer de monitorar suposições de alta confiança

## Formato de Saída

**Matriz de Priorização Incluindo:**
- Todas as suposições mapeadas e categorizadas
- Avaliação de impacto e confiança para cada
- Posicionamento na matriz 2x2
- Experimentos específicos por quadrante
- Timeline de validação e recursos necessários
- Critérios de decisão e próximos passos

## Framework

Baseado em metodologia de priorização de suposições com matriz de risco vs incerteza. Foca em aprendizado rápido e gestão eficiente de recursos de validação.

## Recursos Adicionais

- **Assumption Canvas:** [Assumption Prioritization Canvas](https://www.productcompass.pm/p/assumption-prioritization-canvas)
- **Risk Management:** [Product Risk Management](https://www.productcompass.pm/p/product-risk-management)
- **Experimentation:** [Ultimate Validation Experiments](https://www.productcompass.pm/p/the-ultimate-experiments-library)

---

## Critérios de Scoring

### Impacto se Falsa (1-10)
- **9-10 (Crítico):** Falha = projeto cancelado
- **7-8 (Alto):** Falha = mudança significativa necessária
- **5-6 (Médio):** Falha = problemas sérios mas recuperáveis
- **3-4 (Baixo):** Falha = inconvenientes, ajustes menores
- **1-2 (Mínimo):** Falha = impacto negligível

### Confiança Atual (1-10)
- **1-3 (Baixa):** Principalmente suposição, pouca evidência
- **4-6 (Média):** Alguma evidência, não conclusiva
- **7-9 (Alta):** Evidências fortes, quase validado
- **10 (Muito Alta):** Validado extensivamente, quase certeza

## Template de Documentação

### Para Cada Suposição:
```
**Suposição:** [Descrição clara e específica]
**Categoria:** [Value/Usability/Viability/Feasibility/etc.]
**Impacto se Falsa:** [1-10] - [Justificativa]
**Confiança Atual:** [1-10] - [Justificativa]
**Quadrante:** [Q1/Q2/Q3/Q4]
**Experimento Proposto:** [Descrição detalhada]
**Timeline:** [Semanas necessárias]
**Sucesso Criteria:** [Como saber se validado]
```

## Checklist de Implementação

### Mapeamento
- [ ] Todas as suposições identificadas e listadas
- [ ] Cada suposição claramente definida
- [ ] Categorias atribuídas consistentemente
- [ ] Interdependências identificadas

### Avaliação
- [ ] Impacto avaliado para cada suposição
- [ ] Confiança avaliada para cada suposição
- [ ] Posicionamento na matriz verificado
- [ ] Prioridades estabelecidas

### Planejamento
- [ ] Experimentos designados por quadrante
- [ ] Timeline de validação criado
- [ ] Recursos alocados adequadamente
- [ ] Critérios de sucesso definidos

---

**Próximos Passos:**
- Executar experimentos Q1 imediatamente
- Monitorar métricas Q4 continuamente
- Revisar matriz a cada aprendizado significativo
- Compartilhar resultados com stakeholders
- Ajustar estratégia baseado em validações
