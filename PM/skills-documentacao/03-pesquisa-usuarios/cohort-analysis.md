# Análise de Cohort

## Propósito
Realizar análise de cohort em dados de engajamento de usuários — curvas de retenção, tendências de adoção de features e insights em nível de segmento. Usado ao analisar retenção por cohort, estudar adoção de features ao longo do tempo, investigar padrões de churn ou identificar tendências de engajamento.

## Como Funciona
Analisa padrões de engajamento e retenção de usuários por cohort para identificar tendências em comportamento de usuários, adoção de features e engajamento de longo prazo. Combina insights quantitativos com recomendações de pesquisa qualitativa.

## Quando Usar
- Análise de saúde do produto trimestral
- Investigação de churn inesperado
- Avaliação de impacto de novas features
- Comparação de performance entre cohorts
- Planejamento de estratégias de retenção

## Como Funciona

### Passo 1: Ler e Validar Dados
- Aceite arquivos CSV, Excel ou JSON com informações de cohort de usuários
- Verifique estrutura de dados: identificador de cohort, períodos de tempo, métricas de engajamento
- Verifique valores ausentes e problemas de qualidade de dados
- Resuma estatísticas chave (tamanhos de cohort, intervalos de datas, métricas disponíveis)

### Passo 2: Gerar Análise Quantitativa
- Calcule taxas de retenção de cohort e tendências de engajamento
- Identifique curvas de retenção, padrões de drop-off e anomalias
- Calcule taxas de adoção de features entre cohorts
- Calcule mudanças mês a mês ou período a período
- Gere scripts de análise Python usando pandas e numpy se solicitado

### Passo 3: Criar Visualizações
- Gere heatmaps de retenção (cohorts vs. períodos de tempo)
- Crie gráficos de linha mostrando progressão de cohort
- Construa gráficos de comparação para adoção de features
- Visualize pontos de drop-off e tendências de engajamento
- Output como gráficos interativos ou imagens estáticas

### Passo 4: Identificar Insights e Padrões
- Identifique um ou mais padrões significativos:
  - Churn precoce em cohorts específicos
  - Mudanças de engajamento em estágio tardio
  - Clusters de adoção de features
  - Tendências sazonais ou temporais
- Destaque achados surpreendentes e desvios
- Compare performance de cohort para estabelecer baselines

### Passo 5: Sugerir Pesquisa de Seguimento
- Recomende métodos de pesquisa qualitativa:
  - Entrevistas direcionadas com usuários em churn
  - Pesquisas de uso de features com cohorts engajados
  - Replays de sessão de padrões de interação chave
  - Análise win/loss para cohorts de alta vs. baixa retenção
- Projetar estudos quantitativos de seguimento
- Sugerir testes A/B ou experimentos de features

## Exemplos de Uso

### Exemplo 1: Upload de Dados CSV
```
Upload cohort_engagement.csv com colunas: cohort_month, weeks_active,
user_id, feature_x_usage, engagement_score

Request: "Analyze retention patterns and identify why Q4 2025 cohorts
underperform compared to Q3"
```

### Exemplo 2: Descrever Formato de Dados
```
"I have monthly user cohorts from Jan-Dec 2025. Each row shows:
cohort date, user ID, purchase frequency, and support tickets.
Analyze which cohorts show best long-term retention."
```

### Exemplo 3: Análise de Adoção de Features
```
Upload feature_usage.xlsx com dados de adoção de cohort.

Request: "Compare adoption curves for our new feature across cohorts.
Which cohorts adopted fastest? Any patterns?"
```

## Capacidades Chave

- **Leitura de Dados:** Importar CSV, Excel, JSON, resultados de query SQL
- **Análise de Retenção:** Calcular e visualizar taxas de retenção ao longo do tempo
- **Comparação de Cohort:** Comparar métricas entre grupos de cohort
- **Detecção de Anomalias:** Sinalizar padrões incomuns ou drop-offs
- **Scripts Python:** Gerar código de análise reutilizável para análise contínua
- **Visualizações:** Criar heatmaps, gráficos e dashboards interativos
- **Design de Pesquisa:** Sugerir estudos de seguimento direcionados e abordagens de entrevista
- **Resumo Estatístico:** Fornecer métricas quantitativas e análise de correlação

## Exemplo Prático

### Análise de Cohort: FinanControl

#### Resumo dos Dados
- **Período:** Janeiro - Dezembro de 2025
- **Cohorts:** Mensais por mês de signup
- **Métricas:** Retenção semanal, adoção de features, LTV
- **Volume:** 12 cohorts, 5.000 usuários totais

#### Análise Quantitativa

**Taxas de Retenção por Cohort:**
```
Cohort    Semana 1  Semana 4  Semana 8  Semana 12
Jan-25    85%       62%       48%       41%
Fev-25    87%       65%       52%       45%
Mar-25    82%       58%       44%       38%
Abr-25    88%       68%       55%       49%
Mai-25    90%       72%       60%       54%
Jun-25    91%       75%       63%       58%
```

**Adoção de Features (Dashboard Avançado):**
```
Cohort    Taxa Adoção 4 Semanas  Tempo para Adoção
Jan-25    35%                    18 dias
Fev-25    38%                    15 dias
Mar-25    32%                    22 dias
Abr-25    45%                    12 dias
Mai-25    52%                    8 dias
Jun-25    58%                    6 dias
```

#### Visualizações Identificadas

**Heatmap de Retenção:**
- Padrão claro de melhoria de retenção cohorts mais recentes
- Drop-off significativo entre semanas 4-8 para cohorts mais antigos
- Cohorts pós-abril mostram retenção 15% maior em 12 semanas

**Gráfico de Adoção de Features:**
- Curva de adoção mais rápida para cohorts mais recentes
- Correlação entre tempo de adoção e retenção de longo prazo
- Ponto de inflexão em abril correspondendo a lançamento de tutorial

#### Insights e Padrões

1. **Melhoria Contínua:** Retenção melhorou 40% de Jan para Jun
2. **Onboarding Impactante:** Lançamento de tutorial em abril correlaciona com adoção mais rápida
3. **Feature Stickiness:** Usuários que adotam dashboard avançado têm 2.5x mais retenção
4. **Sazonalidade:** Leve queda em cohorts de março (fim de verão no Brasil)

#### Recomendações de Pesquisa

**Qualitativas:**
- Entrevistar usuários de cohorts antigos vs. novos sobre experiência de onboarding
- Pesquisar usuários que abandonaram dashboard avançado após uso inicial
- Análise de win/loss comparando usuários que adotaram vs. não adotaram features

**Quantitativas:**
- Teste A/B de onboarding simplificado vs. atual
- Análise de correlação entre tempo de primeira feature e LTV
- Estudo de impacto de notificações de adoção de features

## Dicas para Melhores Resultados

1. **Inclua Dimensão Temporal:** Forneça dados através de múltiplos períodos de tempo
2. **Defina Cohort Claramente:** Torne agrupamento de cohort explícito (mês de signup, data de lançamento de feature, etc.)
3. **Forneça Contexto:** Explique mudanças de produto, lançamentos ou eventos durante o período
4. **Múltiplas Métricas:** Inclua retenção, engajamento, uso de features, receita, etc.
5. **Dados Suficientes:** Pelo menos 3-4 cohorts para identificação de padrões significativos
6. **Peça Output Específico:** Peça visualizações, scripts Python ou recomendações de pesquisa

## Formato de Saída

Você receberá:
- **Resumo de Dados:** Visão geral de cohort e avaliação de qualidade de dados
- **Achados Quantitativos:** Métricas chave, taxas de retenção e análise de tendências
- **Visualizações:** Gráficos mostrando curvas de retenção, padrões de adoção
- **Identificação de Padrões:** 2-3 insights significativos dos dados
- **Recomendações de Pesquisa:** Seguimentos qualitativos e quantitativos específicos
- **Scripts de Análise** (se solicitado): Código Python para análise reproduzível
- **Próximos Passos:** Ações priorizadas baseadas em achados

## Benefícios
- **Visão de Longo Prazo:** Entende saúde do produto ao longo do tempo
- **Identificação de Padrões:** Descobre tendências que não são visíveis em snapshots
- **Otimização:** Identifica cohorts de alto desempenho para replicar
- **Prevenção de Churn:** Detecta sinais de problemas antes de afetarem negócio

## Recursos Adicionais
- [Cohort Analysis 101: How to Reduce Churn and Make Better Product Decisions](https://www.productcompass.pm/p/cohort-analysis)
- [The Product Analytics Playbook: AARRR, HEART, Cohorts & Funnels for PMs](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
- [Are You Tracking the Right Metrics?](https://www.productcompass.pm/p/are-you-tracking-the-right-metrics)
- [Retention Analysis: Best Practices](https://www.productcompass.pm/p/retention-analysis-guide)
