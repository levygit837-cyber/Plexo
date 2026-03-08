# Priorização de Features

## Propósito
Priorizar backlog de ideias de features baseado em impacto, esforço, risco e alinhamento estratégico com top 5 recomendações. Usado ao priorizar backlog de features, tomar decisões de scope ou ranquear ideias de produto.

## Como Funciona
Avalia e ranqueia backlog de ideias de features para identificar as top 5 a perseguir. Usa frameworks de priorização como Opportunity Score, ICE e RICE.

## Quando Usar
- Priorização de backlog de produto
- Tomada de decisões de scope e roadmap
- Ranqueamento de ideias de produto
- Alocação de recursos limitados
- Alinhamento estratégico de features

## Contexto de Domínio

Para orientação de seleção de framework, veja a skill `prioritization-frameworks`. Recomendações chave:

### Opportunity Score (Dan Olsen, *The Lean Product Playbook*)
Recomendado para avaliar problemas de clientes: Opportunity Score = Importance × (1 − Satisfaction), normalizado para 0–1. Alta Importância + baixa Satisfação = melhores oportunidades. Priorize **problemas (oportunidades)**, não soluções.

### ICE
Recomendado para scoring rápido de iniciativas: Impact (Opportunity Score × # Clientes) × Confidence × Ease.

### RICE
Adiciona Reach como fator separado para times maiores.

## Instruções

O usuário descreverá objetivo do produto, outcomes desejados e fornecerá ideias de features. Trabalhe através destes passos:

### 1. Entender Prioridades
Confirme o objetivo do produto e métricas de sucesso.

### 2. Avaliar Cada Feature
- **Impacto:** Quanto move a agulha nos outcomes desejados? Considere Opportunity Score se dados de clientes disponíveis.
- **Esforço:** Quanto desenvolvimento, design e coordenação necessários?
- **Risco:** Quanta incerteza existe? Que suposições precisam ser testadas?
- **Alinhamento Estratégico:** Quão bem se encaixa na visão do produto e metas atuais?

### 3. Recomendar Top 5 Features
- Ranking claro (1-5)
- Breve raciocínio para cada seleção
- Trade-offs chave considerados
- O que foi despriorizado e por quê

### 4. Apresentar como Tabela de Priorização
Se útil, apresente resultados como tabela.

## Exemplo Prático

### Priorização de Features: FinanControl

### 1. Entender Prioridades
- **Objetivo do Produto:** Reduzir churn de 15% para 8% em 6 meses
- **Métricas de Sucesso:** Churn rate, NPS, tempo para valor, ativação
- **Restrições:** Equipe de 6 engenheiros, orçamento limitado, timeline apertado

### 2. Ideias de Features para Avaliar

#### Lista de Features (Backlog)
1. Alertas Inteligentes Proativos
2. Dashboard Personalizável
3. Machine Learning para Categorização
4. Benchmarking Anônimo
5. Onboarding Gamificado
6. Integração com Sistemas de RH
7. Relatórios Avançados Customizados
8. API para Desenvolvedores
9. Modo Offline
10. Exportação em Múltiplos Formatos

### 3. Avaliação Detalhada

#### Framework ICE (Impact × Confidence × Ease)

| Feature | Impacto (1-10) | Confidence (1-10) | Ease (1-10) | Score ICE | Ranking |
|---|---|---|---|---|---|
| Alertas Inteligentes | 9 | 8 | 6 | 432 | 1 |
| ML Categorização | 8 | 7 | 4 | 224 | 3 |
| Dashboard Personalizável | 7 | 9 | 8 | 504 | 2 |
| Benchmarking Anônimo | 6 | 6 | 5 | 180 | 4 |
| Onboarding Gamificado | 8 | 8 | 7 | 448 | 5 |

#### Análise de Risco e Alinhamento

| Feature | Risco (Alto/Médio/Baixo) | Alinhamento Estratégico | Trade-offs Principais |
|---|---|---|---|
| Alertas Inteligentes | Médio (precisão do modelo) | Alto (reduz churn diretamente) | Complexidade técnica vs. valor |
| Dashboard Personalizável | Baixo (UX conhecido) | Médio (melhora engajamento) | Esforço de desenvolvimento vs. impacto |
| ML Categorização | Alto (dados de treinamento) | Alto (automatização de dor) | Custo computacional vs. benefício |
| Benchmarking Anônimo | Médio (adoção) | Médio (diferenciação) | Privacidade vs. valor |
| Onboarding Gamificado | Baixo (gamificação conhecida) | Alto (ativação crítica) | Sofisticação vs. simplicidade |

### 4. Recomendações Top 5

#### 1. Dashboard Personalizável (Rank 1)
**Raciocínio:** Alto impacto em engajamento, baixo risco, alta confiança. Melhora satisfação do usuário e retenção.

**Trade-offs:** Esforço moderado de desenvolvimento, mas benefício claro e mensurável.

#### 2. Alertas Inteligentes Proativos (Rank 2)
**Raciocínio:** Impacto direto no churn (objetivo principal), valor claro para usuários.

**Trade-offs:** Risco técnico na precisão do modelo, mas mitigável com abordagem incremental.

#### 3. Onboarding Gamificado (Rank 3)
**Raciocínio:** Crítico para ativação, baixo risco, alto alinhamento com objetivo de reduzir churn inicial.

**Trade-offs:** Precisa balancear gamificação com profissionalismo do público B2B.

#### 4. Machine Learning para Categorização (Rank 4)
**Raciocínio:** Automatiza tarefa manual dolorosa, alto valor percebido, diferencial competitivo.

**Trade-offs:** Alto risco técnico e custo computacional, mas benefício transformador.

#### 5. Benchmarking Anônimo (Rank 5)
**Raciocínio:** Diferenciação forte, cria network effects, valor claro para negócios.

**Trade-offs:** Depende de adoção para gerar valor, risco de baixa participação inicial.

### 5. Features Despriorizadas e Justificativa

#### Fora do Top 5:
- **Integração RH:** Baixo alinhamento com objetivo atual, esforço alto
- **Relatórios Customizados:** Impacto limitado vs. esforço, pode esperar
- **API para Desenvolvedores:** Baixo impacto no churn atual, mercado pequeno
- **Modo Offline:** Baixa prioridade para produto SaaS B2B
- **Exportação Múltiplos Formatos:** Feature de conveniência, não crítica para retenção

## Frameworks de Priorização

### RICE Score
```
RICE = (Reach × Impact × Confidence) / Effort

Exemplo para Alertas Inteligentes:
Reach: 80% de usuários afetados
Impact: 8/10 (reduz churn significativamente)
Confidence: 80% (viamos protótipo funcionar)
Effort: 6 pessoas-mês

RICE = (0.8 × 8 × 0.8) / 6 = 0.85
```

### Opportunity Score
```
Opportunity Score = Importance × (1 - Satisfaction)

Exemplo para Categorização:
Importance: 9/10 (tarefa muito dolorosa)
Satisfaction: 2/10 (solução atual ruim)
Score = 9 × (1 - 0.2) = 7.2
```

### Kano Model
```
Must-Have: Features básicas esperadas
Performance: Features que melhoram linearmente
Excitement: Features que encantam se presentes
```

## Template de Priorização

### Planilha de Priorização

| Feature | Impacto | Esforço | Risco | Alinhamento | Score ICE | RICE | Decisão |
|---|---|---|---|---|---|---|---|
| [Nome] | [1-10] | [pessoas-mês] | [A/M/B] | [H/M/L] | [calculo] | [calculo] | [Prioridade] |

### Categorias de Decisão
- **Now:** Top prioridade, iniciar imediatamente
- **Next:** Segunda onda, planejar após Now
- **Later:** Considerar futuramente, baixo impacto atual
- **Never:** Baixo valor, alto esforço, descartar

## Benefícios
- **Foco:** Concentra recursos nas features mais valiosas
- **Alinhamento:** Garante que trabalho suporta objetivos estratégicos
- **Transparência:** Processo claro e documentado de decisões
- **Eficiência:** Maximiza ROI de desenvolvimento

## Dicas de Uso
- Use dados reais sempre que possível em vez de opiniões
- Envolva stakeholders chave no processo de priorização
- Revisite priorizações regularmente (mínimo trimestral)
- Considere interdependências entre features
- Documente raciocínio para futuras referências

## Recursos Adicionais
- [Kano Model: How to Delight Your Customers Without Becoming a Feature Factory](https://www.productcompass.pm/p/kano-model-how-to-delight-your-customers)
- [The Product Management Frameworks Compendium + Templates](https://www.productcompass.pm/p/the-product-frameworks-compendium)
- [Continuous Product Discovery Masterclass (CPDM)](https://www.productcompass.pm/p/cpdm) (video course)
- [Prioritization Frameworks: Complete Guide](https://www.productcompass.pm/p/prioritization-frameworks-guide)
