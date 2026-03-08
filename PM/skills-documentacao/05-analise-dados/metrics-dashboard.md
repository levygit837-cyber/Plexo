# Dashboard de Métricas

## Propósito
Definir e projetar um dashboard de métricas de produto com métricas chave, fontes de dados, tipos de visualização e thresholds de alerta. Usado ao criar dashboard de métricas, definir KPIs, configurar analytics de produto ou construir plano de monitoramento de dados.

## Como Funciona
Projeta um dashboard abrangente de métricas de produto com as métricas certas, visualizações e thresholds de alerta. Organiza métricas em camadas desde North Star até métricas operacionais.

## Quando Usar
- Configuração inicial de analytics de produto
- Redesenho de dashboards existentes
- Definição de KPIs para OKRs
- Monitoramento de saúde do produto
- Alinhamento de equipe em torno de métricas

## Contexto de Domínio

### Métricas vs. KPIs vs. NSM
- **Métricas:** Todas as coisas mensuráveis
- **KPIs:** Algumas métricas quantitativas chave rastreadas por período mais longo
- **North Star Metric:** Único KPI centrado no cliente que é indicador líder de sucesso do negócio

### 4 critérios para uma boa métrica (Ben Yoskovitz, *Lean Analytics*)
1. **Compreensível** — cria linguagem comum
2. **Comparativa** — ao longo do tempo, não snapshot
3. **Razão ou Taxa** — mais reveladora que números inteiros
4. **Mudança de Comportamento** — Regra de Ouro: "Se uma métrica não mudar como você se comporta, é uma má métrica"

### 8 tipos de métricas
- **Vanity vs. Acionável** (somente métricas acionáveis mudam comportamento)
- **Qualitativa vs. Quantitativa** (O QUÊ vs. POR QUÊ — você precisa de ambos)
- **Exploratória vs. Reporting** (explorar dados para descobrir insights inesperados)
- **Lagging vs. Leading** (indicadores líderes permitem ciclos de aprendizado mais rápidos)

## Passo a Passo

### 1. Identificar Framework de Métricas — Organizar métricas em camadas

#### North Star Metric
A métrica única que melhor captura entrega de valor principal

#### Métricas de Input (3-5)
As alavancas que impulsionam o North Star

#### Métricas de Saúde
Guardrails que garantem saúde geral do produto

#### Métricas de Negócio
Receita, custos e unit economics

### 2. Para cada métrica, defina:

| Métrica | Definição | Fonte de Dados | Visualização | Alvo | Threshold de Alerta |
|---|---|---|---|---|---|
| [Nome] | [Cálculo exato: numerador/denominador, janela de tempo] | [Onde os dados vêm] | [Gráfico de linha / Barra / Número / Funil] | [Valor alvo] | [Quando disparar alerta] |

### 3. Projetar Layout do Dashboard

```
┌─────────────────────────────────────────────┐
│  NORTH STAR: [Métrica] — [Valor Atual]     │
│  Trend: [↑/↓ X% vs. último período]        │
├──────────────────┬──────────────────────────┤
│  Input Metric 1  │  Input Metric 2          │
│  [Sparkline]     │  [Sparkline]             │
├──────────────────┼──────────────────────────┤
│  Input Metric 3  │  Input Metric 4          │
│  [Sparkline]     │  [Sparkline]             │
├──────────────────┴──────────────────────────┤
│  SAÚDE: [Latência] [Taxa de Erro] [NPS]   │
├─────────────────────────────────────────────┤
│  NEGÓCIO: [MRR] [CAC] [LTV] [Churn]       │
└─────────────────────────────────────────────┘
```

### 4. Definir Cadência de Revisão
- **Diário:** Saúde operacional (erros, latência, fluxos críticos)
- **Semanal:** Métricas de input e tendências de engajamento
- **Mensal:** North Star, métricas de negócio, progresso OKR
- **Trimestral:** Revisão estratégica e recalibração de métricas

### 5. Definir Alertas
- Quais thresholds disparam investigação?
- Quem recebe alerta e através de qual canal?
- Qual é o tempo de resposta esperado?

### 6. Recomendar Ferramentas
Baseado no contexto do usuário:
- **Amplitude, Mixpanel, PostHog** para analytics de produto
- **Looker, Metabase, Mode** para dashboards baseados em SQL
- **Datadog, Grafana** para saúde operacional

## Exemplo Prático

### Dashboard de Métricas: FinanControl

### 1. Framework de Métricas

#### North Star Metric
**"Horas economizadas por mês por PME"**
- Captura valor principal entregue ao cliente
- Métrica centrada no cliente, não interna
- Indicador líder de sucesso do negócio

#### Métricas de Input (4)
1. **Usuários Ativos Diários (DAU)** — Indica uso regular
2. **Taxa de Ativação (7 dias)** — Mostra valor rápido
3. **Integrações Bancárias Conectadas** — Profundidade de uso
4. **Relatórios Gerados por Mês** — Engajamento com features

#### Métricas de Saúde
- **Tempo de Carregamento do Dashboard**
- **Taxa de Erros de API**
- **NPS (Net Promoter Score)**
- **Taxa de Suporte por Usuário**

#### Métricas de Negócio
- **MRR (Monthly Recurring Revenue)**
- **CAC (Customer Acquisition Cost)**
- **LTV (Lifetime Value)**
- **Churn Rate**

### 2. Definição Detalhada

| Métrica | Definição | Fonte de Dados | Visualização | Alvo | Alerta |
|---|---|---|---|---|---|
| **Horas Economizadas** | (Tempo médio manual - Tempo no sistema) × Usuários Ativos | App analytics + survey | Número grande + sparkline | 500h/mês | < 400h/mês |
| **DAU** | Usuários únicos ativos em 24h | App analytics | Gráfico de linha | 1.200 | < 1.000 |
| **Taxa Ativação** | % usuários que conectam banco em 7 dias | App analytics | Funnel | 85% | < 80% |
| **Integrações** | Média de bancos conectados por usuário | Database | Barra | 2.5 | < 2.0 |
| **Relatórios/Mês** | Total relatórios gerados / usuários ativos | App analytics | Gráfico de barras | 12 | < 8 |
| **Latência** | Tempo médio carregamento dashboard | Monitoring | Gauge | < 2s | > 3s |
| **Taxa Erros** | Erros API / total requisições | Monitoring | Sparkline | < 1% | > 2% |
| **NPS** | Promotores - Detratores | Survey | Número | 50 | < 30 |
| **MRR** | Soma de assinaturas mensais | Stripe | Gráfico de linha | R$45K | < R$40K |
| **CAC** | Custo marketing / novos clientes | Marketing | Número | R$300 | > R$400 |
| **LTV** | Receita média por cliente | Financeiro | Número | R$3.600 | < R$3.000 |
| **Churn** | % clientes cancelam/mês | Financeiro | Gráfico de linha | < 5% | > 8% |

### 3. Layout do Dashboard

```
┌─────────────────────────────────────────────────────┐
│  NORTH STAR: Horas Economizadas — 523h/mês         │
│  Trend: ↑ 12% vs. mês passado                    │
├──────────────────────┬──────────────────────────────┤
│  DAU: 1.247           │  Taxa Ativação: 87%        │
│  [sparkline ↑]        │  [funnel ↑]                │
├──────────────────────┼──────────────────────────────┤
│  Integrações: 2.8     │  Relatórios/Mês: 14        │
│  [bar ↑]             │  [bar ↑]                  │
├──────────────────────┴──────────────────────────────┤
│  SAÚDE: Latência 1.8s ✅ | Erros 0.8% ✅ | NPS 52 ✅ │
├─────────────────────────────────────────────────────┤
│  NEGÓCIO: MRR R$47K ↑ | CAC R$285 ↓ | LTV R$3.8K ↑ │
└─────────────────────────────────────────────────────┘
```

### 4. Cadência de Revisão

#### Diário (10:00)
- Latência do dashboard
- Taxa de erros de API
- Novos usuários inscritos

#### Semanal (Segunda-feira)
- Revisão completa de métricas de input
- Análise de tendências de engajamento
- Progresso OKRs semanais

#### Mensal (Primeiro dia útil)
- North Star e métricas de negócio
- Revisão estratégica de metas
- Planejamento de experimentos

#### Trimestral
- Revisão completa do framework de métricas
- Recalibração de alvos
- Avaliação de ferramentas e processos

### 5. Sistema de Alertas

#### Alertas Críticos (Slack #prod-alerts)
- Latência > 3s: Imediato
- Taxa de erros > 2%: Imediato
- DAU < 1.000: 15 minutos

#### Alertas de Atenção (Email diário)
- NPS < 30: Diário às 9:00
- Churn > 8%: Segunda-feira
- CAC > R$400: Terça-feira

#### Alertas de Oportunidade (Semanal)
- Novos picos de uso: Sexta-feira
- Melhorias em métricas: Sexta-feira
- Insights de dados: Sexta-feira

### 6. Recomendação de Ferramentas

**Analytics de Produto:**
- **PostHog** (open-source, auto-hospedado)
- **Amplitude** (para comportamento detalhado)

**Dashboards:**
- **Metabase** (SQL-based, open-source)
- **Looker** (para análises complexas)

**Monitoring:**
- **Datadog** (para saúde operacional)
- **Grafana** (para métricas técnicas)

## Modelos de Dashboard

### Dashboard de Growth
```
North Star: Usuários Ativos Semanais
Inputs: Aquisição, Ativação, Retenção, Referral
Saúde: Performance, Bugs, UX
Negócio: CAC, LTV, Burn Rate
```

### Dashboard de E-commerce
```
North Star: GMV (Gross Merchandise Value)
Inputs: Visitas, Conversão, Ticket Médio, Frequência
Saúde: Carrinho Abandonado, Disponibilidade, Tempo de Site
Negócio: Margem, CAC, LTV, Churn
```

### Dashboard de SaaS B2B
```
North Star: MRR Growth
Inputs: Leads, Demos, Conversão, Expansão
Saúde: Uptime, Support Tickets, NPS
Negócio: ARR, Churn, LTV:CAC, CAC Payback
```

## Benefícios
- **Clareza:** Visão unificada da saúde do produto
- **Alinhamento:** Equipe focada nas mesmas métricas
- **Proatividade:** Alertas permitem ação preventiva
- **Aprendizado:** Revela padrões e oportunidades

## Dicas de Uso
- Audite métricas contra os 4 critérios de boa métrica
- Identifique métricas de vanity — use com cuidado
- Classifique indicadores líderes vs. retardadores
- Escolha um problema e aprofunde nos dados
- Revisite e ajuste dashboards trimestralmente

## Recursos Adicionais
- [The Ultimate List of Product Metrics](https://www.productcompass.pm/p/the-ultimate-list-of-product-metrics)
- [The North Star Framework 101](https://www.productcompass.pm/p/the-north-star-framework-101)
- [The Product Analytics Playbook: AARRR, HEART, Cohorts & Funnels for PMs](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
- [AARRR (Pirate) Metrics: The 5-Stage Framework for Growth](https://www.productcompass.pm/p/aarrr-pirate-metrics)
- [The Google HEART Framework: Your Guide to Measuring User-Centric Success](https://www.productcompass.pm/p/the-google-heart-framework)
