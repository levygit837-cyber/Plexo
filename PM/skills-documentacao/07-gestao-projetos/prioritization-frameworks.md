# Frameworks de Priorização

## Propósito
Guia de referência para 9 frameworks de priorização com fórmulas, orientação de quando usar e templates — RICE, ICE, Kano, MoSCoW, Opportunity Score e mais. Usado ao selecionar método de priorização, comparar frameworks como RICE vs ICE ou aprender como diferentes abordagens funcionam.

## Como Funciona
Guia de referência para ajudar a selecionar e aplicar o framework de priorização certo para seu contexto. Fornece comparações detalhadas e templates práticos.

## Quando Usar
- Selecionar framework de priorização para seu time
- Comparar diferentes abordagens de priorização
- Ensinar equipe sobre métodos de priorização
- Tomar decisões estratégicas sobre roadmap
- Alinhar stakeholders em torno de processo

## Princípio Core

**Nunca permita que clientes projetem soluções. Priorize problemas (oportunidades), não features.**

## Frameworks Detalhados

### Opportunity Score (Dan Olsen, *The Lean Product Playbook*)

Framework recomendado para priorizar problemas de clientes.

**Como funciona:**
Survey clientes sobre **Importance** e **Satisfaction** para cada necessidade (normalize para escala 0–1).

**Três fórmulas relacionadas:**
- **Current value** = Importance × Satisfaction
- **Opportunity Score** = Importance × (1 − Satisfaction)
- **Customer value created** = Importance × (S2 − S1), onde S1 = satisfação antes, S2 = satisfação depois

**Aplicação:**
Alta Importância + baixa Satisfação = maior Opportunity Score = melhores oportunidades. Plote em gráfico Importance vs Satisfaction — quadrante superior-esquerdo é o ponto ideal. Prioriza problemas de clientes, não soluções.

### ICE Framework

Útil para priorizar iniciativas e ideias. Considera não apenas valor mas também risco e fatores econômicos.

**Fórmula:**
- **I** (Impact) = Opportunity Score × Número de Clientes afetados
- **C** (Confidence) = Quão confiantes estamos? (1-10). Contabiliza risco.
- **E** (Ease) = Quão fácil é implementar? (1-10). Contabiliza fatores econômicos.

**Score** = I × C × E. Maior = priorizar primeiro.

### RICE Framework

Divide o Impacto do ICE em dois fatores separados. Útil para times maiores que precisam de mais granularidade.

**Fórmula:**
- **R** (Reach) = Número de clientes afetados
- **I** (Impact) = Opportunity Score (valor por cliente)
- **C** (Confidence) = Quão confiantes estamos? (0-100%)
- **E** (Effort) = Quanto esforço para implementar? (pessoa-meses)

**Score** = (R × I × C) / E

### Kano Model

Para entender expectativas dos clientes, não necessariamente para priorizar.

**Categorias:**
- **Must-be:** Básicas esperadas, ausência causa insatisfação
- **Performance:** Quanto melhor, mais satisfação (linear)
- **Attractive:** Surpresa e deleite, ausência não causa insatisfação
- **Indifferent:** Não importa para clientes
- **Reverse:** Presença causa insatisfação

### MoSCoW

Originado em gerenciamento de projetos, cuidado ao usar para priorização de produto.

**Categorias:**
- **Must:** Obrigatório para lançamento
- **Should:** Importante mas não crítico
- **Could:** Nice to have se tempo permitir
- **Won't:** Explicitamente fora de escopo

### Eisenhower Matrix

Para gestão pessoal de tarefas do PM.

**Quadrantes:**
- **Urgent & Important:** Fazer agora
- **Important & Not Urgent:** Planejar
- **Urgent & Not Important:** Delegar
- **Not Urgent & Not Important:** Eliminar

### Impact vs Effort

Simples 2×2 para triagem rápida, não rigoroso para decisões estratégicas.

**Quadrantes:**
- **High Impact, Low Effort:** Quick wins (priorizar)
- **High Impact, High Effort:** Projetos maiores (planejar)
- **Low Impact, Low Effort:** Fill-in tasks (se tempo permitir)
- **Low Impact, High Effort:** Obrigados (evitar)

### Risk vs Reward

Como Impact vs Effort mas contabiliza incerteza.

**Quadrantes:**
- **High Reward, Low Risk:** Priorizar imediatamente
- **High Reward, High Risk:** Investigar mais
- **Low Reward, Low Risk:** Considerar se alinhado
- **Low Reward, High Risk:** Evitar

### Weighted Decision Matrix

Para decisões multi-fator, útil para buy-in de stakeholders.

**Processo:**
1. Definir critérios (ex: ROI, alinhamento estratégico, esforço)
2. Atribuir pesos a cada critério
3. Pontuar cada opção em cada critério
4. Calcular score ponderado

## Visão Geral dos 9 Frameworks

| Framework | Melhor Para | Insight Chave |
|-----------|-------------|---------------|
| Eisenhower Matrix | Tarefas pessoais | Urgente vs Importante — gestão individual PM |
| Impact vs Effort | Tarefas/iniciativas | Simples 2×2 — triagem rápida, não rigoroso |
| Risk vs Reward | Iniciativas | Como Impact vs Effort mas contabiliza incerteza |
| **Opportunity Score** | Problemas de clientes | **Recomendado.** Importance × (1 − Satisfaction). Normalize 0–1. |
| Kano Model | Entender expectativas | Must-be, Performance, Attractive, Indifferent, Reverse |
| Weighted Decision Matrix | Decisões multi-fator | Atribuir pesos, pontuar cada opção. Buy-in stakeholders. |
| **ICE** | Ideias/iniciativas | Impact × Confidence × Ease. Recomendado para priorização rápida. |
| **RICE** | Ideias em escala | (Reach × Impact × Confidence) / Effort. Adiciona Reach ao ICE. |
| MoSCoW | Requisitos | Must/Should/Could/Won't. Cuidado: origem em gestão de projetos. |

## Templates

### Template Opportunity Score
[Opportunity Score intro (PDF)](https://drive.google.com/file/d/1ENbYPmk1i1AKO7UnfyTuULL5GucTVufW/view)

### Template Importance vs Satisfaction
[Importance vs Satisfaction Template — Dan Olsen (Google Slides)](https://docs.google.com/presentation/d/1jg-LuF_3QHsf6f1nE1f98i4C0aulnRNMOO1jftgti8M/edit#slide=id.g796641d975_0_3)

### Template ICE
[ICE Template (Google Sheets)](https://docs.google.com/spreadsheets/d/1LUfnsPolhZgm7X2oij-7EUe0CJT-Dwr-/edit?usp=share_link&ouid=111307342557889008106&rtpof=true&sd=true)

### Template RICE
[RICE Template (Google Sheets)](https://docs.google.com/spreadsheets/d/1S-6QpyOz5MCrV7B67LUWdZkAzn38Eahv/edit?usp=sharing&ouid=111307342557889008106&rtpof=true&sd=true)

## Exemplo Prático

### Aplicação: FinanControl Feature Prioritization

#### Opportunity Score para Problemas de Clientes

| Problema | Importance | Satisfaction | Opportunity Score |
|---|---|---|---|
| Tempo perdido com planilhas | 0.9 | 0.3 | 0.63 |
| Dificuldade de prever fluxo | 0.8 | 0.4 | 0.48 |
| Erros manuais em relatórios | 0.7 | 0.5 | 0.35 |
| Falta de visão consolidada | 0.6 | 0.6 | 0.24 |

**Resultado:** Tempo perdido com planilhas é maior oportunidade (0.63)

#### ICE Score para Soluções

| Solução | Impact (Opportunity × #Clientes) | Confidence | Ease | ICE Score |
|---|---|---|---|---|
| Alertas Inteligentes | 0.63 × 1000 = 630 | 7 | 6 | 26,460 |
| Dashboard Personalizável | 0.48 × 800 = 384 | 9 | 8 | 27,648 |
| ML Categorização | 0.35 × 1200 = 420 | 6 | 4 | 10,080 |

**Resultado:** Dashboard Personalizável > Alertas Inteligentes > ML Categorização

#### RICE Score para Validação

| Iniciativa | Reach | Impact | Confidence | Effort | RICE Score |
|---|---|---|---|---|---|
| MVP Alertas | 200 | 0.63 | 80% | 2 | 50.4 |
| Protótipo Dashboard | 100 | 0.48 | 90% | 1 | 43.2 |
| Teste ML | 50 | 0.35 | 60% | 3 | 3.5 |

**Resultado:** MVP Alertas > Protótipo Dashboard > Teste ML

## Guia de Seleção

### Quando Usar Cada Framework

#### Para Descoberta de Problemas
- **Opportunity Score:** Melhor para identificar problemas de clientes a resolver
- **Kano Model:** Para entender expectativas vs. delight

#### Para Priorização de Soluções
- **ICE:** Rápido e simples para times pequenos
- **RICE:** Mais rigoroso para times maiores
- **Weighted Matrix:** Quando múltiplos stakeholders precisam alinhar

#### Para Gestão Pessoal
- **Eisenhower Matrix:** Organizar tarefas diárias do PM
- **Impact vs Effort:** Triagem rápida de backlog

#### Para Decisões Estratégicas
- **Risk vs Reward:** Quando incerteza é alta
- **Weighted Matrix:** Para decisões complexas com múltiplos critérios

### Comparações Chave

#### ICE vs RICE
- **ICE:** Simples, rápido, bom para times pequenos
- **RICE:** Mais granular, considera Reach separadamente, melhor para escala

#### Opportunity Score vs ICE/RICE
- **Opportunity Score:** Para priorizar PROBLEMAS (o que resolver)
- **ICE/RICE:** Para priorizar SOLUÇÕES (como resolver)

#### Kano vs Outros
- **Kano:** Para entender TIPOS de valor, não para ranquear
- **Outros:** Para ranquear e priorizar

## Benefícios
- **Clareza:** Frameworks estruturam pensamento e decisão
- **Alinhamento:** Processos consistentes alinham equipes
- **Eficiência:** Foca recursos no que mais importa
- **Defesa:** Dados e lógica para justificar decisões

## Dicas de Uso
- Comece com Opportunity Score para identificar problemas
- Use ICE para triagem rápida de soluções
- Adote RICE quando time crescer e precisar de mais rigor
- Combine frameworks quando necessário (ex: Opportunity + RICE)
- Documente processo para consistência futura
- Envolva stakeholders no processo para buy-in

## Recursos Adicionais
- [The Product Management Frameworks Compendium + Templates](https://www.productcompass.pm/p/the-product-frameworks-compendium)
- [Kano Model: How to Delight Your Customers Without Becoming a Feature Factory](https://www.productcompass.pm/p/kano-model-how-to-delight-your-customers)
- [Continuous Product Discovery Masterclass (CPDM)](https://www.productcompass.pm/p/cpdm) (video course)
- [Prioritization in Product Management: Complete Guide](https://www.productcompass.pm/p/prioritization-guide)
