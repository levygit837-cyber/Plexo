# Estratégia de Precificação

## Propósito
Analisar e desenhar estratégias de precificação incluindo modelos de precificação, análise competitiva de preços, estimativa de willingness-to-pay e elasticidade de preços. Usado ao definir preços, avaliar modelos de precificação, preparar para mudança de preços ou comparar abordagens freemium vs. pagas.

## Como Funciona
Desenha estratégia de precificação fundamentada na entrega de valor, posicionamento competitivo e disposição para pagar. Analisa valor entregue, modelos de precificação, cenário competitivo e sensibilidade ao preço.

## Quando Usar
- Lançamento de novos produtos ou features
- Mudanças em estrutura de preços existentes
- Análise competitiva de precificação
- Validação de hipóteses de precificação
- Otimização de conversão e receita

## Passo a Passo

### 1. Entender o Valor Entregue
- Qual é a proposta de valor principal?
- Qual é a alternativa do cliente (e seu custo)?
- Que resultados quantificáveis o produto entrega? (tempo economizado, receita gerada, custo reduzido)
- Qual é a disposição do cliente para pagar baseada nesse valor?

### 2. Avaliar Modelos de Precificação — Recomende o melhor fit:

| Modelo | Melhor Para | Exemplo |
|---|---|---|
| **Flat-rate** | Produtos simples, custos previsíveis | Basecamp ($99/mês flat) |
| **Per-seat** | Ferramentas colaborativas, produtos de equipe | Slack, Figma |
| **Usage-based** | Infraestrutura, produtos API | AWS, Twilio |
| **Tiered** | Produtos com segmentos distintos de usuários | A maioria de SaaS (Free/Pro/Enterprise) |
| **Freemium** | Produtos com efeitos virais/de rede | Spotify, Notion |
| **Freemium + usage** | Produtos de plataforma | Vercel, OpenAI API |
| **Value-based** | Ferramentas enterprise de alto impacto | Salesforce, Palantir |

### 3. Analisar Precificação Competitiva
- Mapeie tiers de precificação de concorrentes e o que está incluído
- Identifique onde seu produto se posiciona (premium, mid-market, budget)
- Encontre lacunas ou oportunidades de precificação
- Note quaisquer convenções de precificação da indústria

### 4. Desenhar Estrutura de Precificação
- **Tiers:** Defina 2-4 tiers com diferenciação clara
- **Feature gating:** Quais features vão em qual tier? (Use métricas de valor, não limites arbitrários)
- **Value metric:** Em que unidade você cobra? (usuários, eventos, armazenamento, chamadas de API)
- **Anchor pricing:** Defina o tier mais popular para parecer a escolha óbvia
- **Annual discount:** Tipicamente 15-20% de desconto sobre precificação mensal

### 5. Estimar Sensibilidade de Preço
- **Van Westendorp Price Sensitivity Meter** (se dados de survey disponíveis):
  - Muito barato → preocupações de qualidade
  - Barato → bom valor
  - Caro → começando a hesitar
  - Muito caro → não comprará
- Alternativamente, estime baseado em precificação competitiva e valor entregue

### 6. Planejar Experimentos de Precificação
- Teste A/B de páginas de precificação (diferentes pontos de preço, nomes de tier, bundles de features)
- Conversas de vendas lideradas por fundador para testar disposição para pagar
- Testes de landing page com diferentes âncoras de preço
- Análise de cohort de taxas de conversão por ponto de preço

### 7. Output de Recomendação de Precificação
```
Modelo Recomendado: [Tipo de modelo]
Value Metric: [No que você cobra]

| Tier | Preço | Segmento Alvo | Features Chave | Posicionamento |
|---|---|---|---|---|

Suposições Chave:
- [Suposição] → [Como testar]

Riscos:
- [Risco] → [Mitigação]
```

## Exemplo Prático

### Estratégia de Precificação: FinanControl

### 1. Valor Entregue
- **Proposta de Valor:** Automação de gestão financeira para PMEs brasileiras
- **Alternativa:** Excel + planilhas manuais (custo: 15-20h/semana de tempo + risco de erros)
- **Resultados Quantificáveis:** Economia de 80% do tempo, eliminação de 95% de erros, visão em tempo real
- **Disposição para Pagar:** PMEs gastam R$500-2.000/mês em contadores e softwares financeiros

### 2. Modelo Avaliado: **Tiered SaaS** (melhor fit para produto B2B com diferentes segmentos)

### 3. Análise Competitiva
- **Concorrentes:**
  - QuickBooks: R$80-400/mês (foco contabilidade)
  - Xero: R$120-600/mês (internacional, complexo)
  - Planilhas: "Grátis" mas alto custo de tempo
- **Posicionamento:** Meio-termo entre planilhas e enterprise
- **Oportunidade:** Foco em simplicidade + mercado brasileiro

### 4. Estrutura de Precificação Projetada

| Tier | Preço | Segmento Alvo | Features Chave | Posicionamento |
|---|---|---|---|---|
| **Starter** | R$99/mês | Micro PMEs (5-20 funcionários) | Dashboard básico, 1 banco, relatórios simples | "Comece a organizar" |
| **Professional** | R$299/mês | PMEs (20-100 funcionários) | Múltiplos bancos, analytics avançados, alertas | "Cresça com controle" |
| **Enterprise** | Custom | Grandes PMEs (100+ funcionários) | Customização, API, suporte dedicado | "Solução corporativa" |

**Feature Gating:**
- **Starter:** 1 usuário, 1 banco, 50 transações/mês
- **Professional:** 5 usuários, 5 bancos, transações ilimitadas, exportação
- **Enterprise:** Usuários ilimitados, bancos ilimitados, API, SLA

**Anchor Pricing:** Professional como opção mais popular (60% margin sobre Starter)

### 5. Sensibilidade de Preço (Van Westendorp)
- **Muito Barato (<R$50):** "Não confio, deve ser limitado"
- **Barato (R$50-150):** "Bom valor para começar"
- **Caro (R$300-500):** "Começando a hesitar, mas vale se economizar tempo"
- **Muito Caro (>R$500):** "Só para grandes empresas"

**Range Ótimo:** R$150-350 para PMEs médias

### 6. Experimentos de Precificação
- **Teste A/B:** R$249 vs. R$299 para tier Professional
- **Landing Page:** Testar nomes de tiers ("Starter" vs. "Básico")
- **Conversas Fundador:** Validar disposição para pagar com 10 prospects
- **Cohort Analysis:** Conversão por fonte de tráfego e preço

### 7. Recomendação Final

```
Modelo Recomendado: Tiered SaaS
Value Metric: Por empresa (não por usuário)

| Tier | Preço | Segmento Alvo | Features Chave | Posicionamento |
|---|---|---|---|---|
| Starter | R$99/mês | Micro PMEs | Essencial, 1 banco | Comece organizado |
| Professional | R$299/mês | PMEs | Completo, analytics | Cresça controlado |
| Enterprise | Custom | Grandes PMEs | Custom, API | Solução corporativa |

Suposições Chave:
- PME média economiza R$2.000/mês → Testar com cálculo ROI
- Concorrência não foca em simplicidade → Validar diferencial
- Adoção mobile é importante → Incluir em todos os tiers

Riscos:
- Churn alto em Starter → Mitigar com onboarding melhorado
- Pressão competitiva → Defender com conhecimento local
- Resistência a preços anuais → Oferecer mensais primeiro
```

## Modelos de Precificação Avançados

### Freemium + Usage
```
Grátis: Features básicas, 100 transações/mês
Pro: R$149/mês + R$0.01 por transação extra
Enterprise: R$499/mês + R$0.005 por transação
```

### Value-Based Pricing
```
Preço base: R$199/mês
Adicional: 10% do valor economizado (máximo R$500/mês)
ROI garantido: Reembolso se não economizar 2x o preço
```

### Hybrid Per-Seat + Usage
```
Base: R$50/usuário/mês
Inclui: 100 transações/usuário/mês
Extra: R$0.005 por transação adicional
```

## Métricas de Sucesso

### Conversão e Adoção
- Taxa de conversão trial → pago
- Tempo para primeiro valor
- Taxa de upgrade entre tiers

### Receita e Retenção
- MRR (Monthly Recurring Revenue)
- ARPU (Average Revenue Per User)
- Churn rate por tier
- LTV:CAC ratio

### Posicionamento de Mercado
- Share de wallet vs. alternativas
- Percepção de preço vs. valor
- Índice de satisfação por tier

## Benefícios
- **Otimização:** Encontra equilíbrio entre volume e margem
- **Crescimento:** Alinha precificação com valor entregue
- **Competitividade:** Posiciona estrategicamente no mercado
- **Escalabilidade:** Modela crescimento de receita previsível

## Dicas de Uso
- Preços podem ser mudados; relacionamentos com clientes são mais difíceis de reconstruir
- Use value metrics que cresçam com o sucesso do cliente
- Considere psychological pricing (R$99 vs. R$100)
- Teste diferentes anchors e frames de referência
- Monitore sensibilidade ao preço por segmento

## Recursos Adicionais
- [Product Pricing Strategies 101](https://www.productcompass.pm/p/product-pricing-strategies-101)
- [The AI Product Pricing Masterclass: OpenAI Product Lead on Why SaaS Pricing Fails in AI (and How to Fix It)](https://www.productcompass.pm/p/ai-product-pricing) (video course)
- [Price Elasticity: How to Measure and Use](https://www.productcompass.pm/p/price-elasticity-guide)
- [Pricing Psychology: Behavioral Economics](https://www.productcompass.pm/p/pricing-psychology)
