# Análise de Teste A/B

## Propósito
Analisar resultados de teste A/B com significância estatística, validação de tamanho de amostra, intervalos de confiança e recomendações de ship/extend/stop. Usado ao avaliar resultados de experimentos, verificar se teste alcançou significância, interpretar dados de split test ou decidir se implementar variante.

## Como Funciona
Avalia resultados de teste A/B com rigor estatístico e traduz achados em decisões claras de produto. Inclui validação de setup do teste, cálculos estatísticos e recomendações acionáveis baseadas nos resultados.

## Quando Usar
- Análise de resultados de experimentos de produto
- Validação de hipóteses de UI/UX ou features
- Decisão sobre implementação de mudanças
- Verificação de significância estatística
- Análise de impacto em métricas de negócio

## Passo a Passo

### 1. Entender o Experimento
- Qual era a hipótese?
- O que foi mudado (a variante)?
- Qual é a métrica primária? Algumas métricas de guarda?
- Quanto tempo o teste rodou?
- Qual é o split de tráfego?

### 2. Validar Setup do Teste

#### Tamanho da Amostra
A amostra é grande o suficiente para o tamanho de efeito esperado?
- Use a fórmula: n = (Z²α/2 × 2 × p × (1-p)) / MDE²
- Sinalize se o teste está underpowered (<80% de poder)

#### Duração
O teste rodou por pelo menos 1-2 ciclos de negócio completos?

#### Randomização
Há evidência de sample ratio mismatch (SRM)?

#### Efeitos de Novidade/Primazia
Houve tempo suficiente para lavar mudanças comportamentais iniciais?

### 3. Calcular Significância Estatística
- **Taxa de conversão** para controle e variante
- **Lift relativo:** (variante - controle) / controle × 100
- **p-value:** Usando teste z de duas caudas ou teste qui-quadrado
- **Intervalo de confiança:** 95% CI para a diferença
- **Significância estatística:** p < 0.05?
- **Significância prática:** O lift é significativo para o negócio?

Se o usuário fornecer dados brutos, gere e execute um script Python para calcular estes.

### 4. Verificar Métricas de Guarda
- Alguma métrica de guarda (receita, engajamento, tempo de carregamento) degradou?
- Uma métrica primária vencedora com guarda degradada pode não ser uma vitória real

### 5. Interpretar Resultados

| Outcome | Recomendação |
|---|---|
| Lift positivo significativo, sem problemas de guarda | **Ship it** — implementar para 100% |
| Lift positivo significativo, preocupações de guarda | **Investigate** — entender trade-offs antes de implementar |
| Não significativo, tendência positiva | **Extend the test** — precisa de mais dados ou efeito maior |
| Não significativo, plano | **Stop the test** — nenhuma diferença significativa detectada |
| Lift negativo significativo | **Don't ship** — reverter para controle, analisar por quê |

### 6. Fornecer Resumo da Análise
```
## A/B Test Results: [Nome do Teste]

**Hipótese**: [O que esperávamos]
**Duração**: [X dias] | **Amostra**: [N controle / M variante]

| Métrica | Controle | Variante | Lift | p-value | Significativo? |
|---|---|---|---|---|---|
| [Primária] | X% | Y% | +Z% | 0.0X | Sim/Não |
| [Guarda] | ... | ... | ... | ... | ... |

**Recomendação**: [Ship / Extend / Stop / Investigate]
**Raciocínio**: [Por quê]
**Próximos passos**: [O que fazer]
```

## Exemplo Prático

### Análise de Teste A/B: FinanControl

#### 1. Entendimento do Experimento
- **Hipótese:** "Nova interface de dashboard aumentará engajamento em 15%"
- **Variante:** Dashboard redesenhado com gráficos interativos e layout simplificado
- **Métrica Primária:** Taxa de usuários ativos diários (DAU)
- **Métricas de Guarda:** Tempo de carregamento, taxa de cliques em relatórios
- **Duração:** 21 dias
- **Split:** 50/50

#### 2. Validação do Setup

**Tamanho da Amostra:**
- Baseline DAU: 25%
- MDE esperado: 15% (para 3.75% absoluto)
- Poder estatístico: 85% (acima de 80% ✅)
- Amostra necessária: 10.000 usuários por grupo
- Amostra real: 12.500 controle, 12.800 variante ✅

**Duração:**
- 21 dias = 3 semanas (cobriu padrão semanal) ✅

**Randomização:**
- Teste SRM: p = 0.87 (sem evidência de desbalanceamento) ✅

**Efeitos de Novidade:**
- Primeiros 3 dias excluídos da análise ✅

#### 3. Cálculos Estatísticos

**Taxa de Conversão (DAU):**
- Controle: 25.2% (3.150/12.500)
- Variante: 28.9% (3.702/12.800)
- Lift relativo: +14.7%

**Significância Estatística:**
- p-value: 0.003 (usando teste z de duas caudas)
- Intervalo de confiança 95%: [+2.1%, +5.3%]
- Significativo: Sim ✅

**Significância Prática:**
- Lift de 14.7% próximo ao esperado de 15% ✅
- Impacto no negócio: +552 usuários ativos diários

#### 4. Métricas de Guarda

| Métrica | Controle | Variante | Mudança | Impacto |
|---|---|---|---|---|
| Tempo de Carregamento | 2.1s | 2.4s | +14% | Aceitável |
| Cliques em Relatórios | 8.3% | 7.9% | -5% | Dentro da margem |
| Taxa de Suporte | 2.1% | 2.3% | +9% | Monitorar |

#### 5. Interpretação dos Resultados

**Outcome:** Lift positivo significativo (+14.7%), métricas de guarda estáveis

**Recomendação:** **Ship it** — implementar para 100%

#### 6. Resumo da Análise
```
## A/B Test Results: Dashboard Redesign

**Hipótese**: Nova interface aumentará engajamento em 15%
**Duração**: 21 dias | **Amostra**: 12.500 controle / 12.800 variante

| Métrica | Controle | Variante | Lift | p-value | Significativo? |
|---|---|---|---|---|---|
| DAU | 25.2% | 28.9% | +14.7% | 0.003 | Sim |
| Tempo Carregamento | 2.1s | 2.4s | +14% | N/A | Aceitável |
| Cliques Relatórios | 8.3% | 7.9% | -5% | N/A | OK |

**Recomendação**: Ship it
**Raciocínio**: Lift estatisticamente significativo (p=0.003) com impacto prático (+552 DAUs). Métricas de guarda estáveis.
**Próximos passos**: Implementar para 100% dos usuários, monitorar métricas de guarda por 2 semanas.
```

## Modelos de Análise

### Teste de Pricing
```
Hipótese: Novo preço R$299 vs R$199 aumentará receita por usuário
Métrica primária: ARPU (Average Revenue Per User)
Guardas: Taxa de conversão, churn rate
Análise: Comparar ARPU, verificar se aumento compensa queda em conversão
```

### Teste de Onboarding
```
Hipótese: Onboarding gamificado aumentará ativação em 20%
Métrica primária: Taxa de usuários ativos após 7 dias
Guardas: Tempo para primeiro valor, suporte tickets
Análise: Medir ativação, verificar se não aumenta suporte
```

### Teste de Feature
```
Hipótese: Nova feature de exportação PDF aumentará retenção
Métrica primária: Retenção de 30 dias
Guardas: Engajamento geral, tempo de uso
Análise: Comparar retenção, verificar canibalização de outras features
```

## Frameworks Estatísticos

### Teste Z para Proporções
```python
import statsmodels.stats.api as sms
import numpy as np

# Dados do exemplo
control_conversions = 3150
control_total = 12500
variant_conversions = 3702
variant_total = 12800

# Taxas de conversão
p1 = control_conversions / control_total
p2 = variant_conversions / variant_total

# Estatística Z e p-value
count = np.array([control_conversions, variant_conversions])
nobs = np.array([control_total, variant_total])
z_stat, p_value = sms.proportions_ztest(count, nobs, alternative='two-sided')
```

### Intervalo de Confiança
```python
import scipy.stats as stats

# Diferença de proporções
diff = p2 - p1
se = np.sqrt(p1*(1-p1)/control_total + p2*(1-p2)/variant_total)

# Intervalo de confiança 95%
ci_low = diff - 1.96*se
ci_high = diff + 1.96*se
```

## Benefícios
- **Rigor Estatístico:** Garante decisões baseadas em evidências
- **Clareza:** Traduz dados complexos em recomendações claras
- **Mitigação de Risco:** Identifica problemas antes de implementação em larga escala
- **Aprendizado:** Gera insights para futuros experimentos

## Dicas de Uso
- Sempre valide o setup do teste antes de analisar resultados
- Considere significância prática além da estatística
- Monitore métricas de guarda para detectar efeitos colaterais
- Documente aprendizados para informar futuros testes
- Use poder estatístico adequado para evitar falsos negativos

## Recursos Adicionais
- [A/B Testing 101 + Examples](https://www.productcompass.pm/p/ab-testing-101-for-pms)
- [Testing Product Ideas: The Ultimate Validation Experiments Library](https://www.productcompass.pm/p/the-ultimate-experiments-library)
- [Are You Tracking the Right Metrics?](https://www.productcompass.pm/p/are-you-tracking-the-right-metrics)
- [Statistical Significance: The Complete Guide](https://www.productcompass.pm/p/statistical-significance-guide)
