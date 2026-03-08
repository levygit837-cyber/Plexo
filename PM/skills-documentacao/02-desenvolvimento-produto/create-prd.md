# Criar Documento de Requisitos de Produto (PRD)

## Propósito
Criar um Documento de Requisitos de Produto usando um template abrangente de 8 seções cobrindo problema, objetivos, segmentos, propostas de valor, solução e planejamento de lançamento. Usado ao escrever PRDs, documentar requisitos de produto, preparar especificações de features ou revisar PRDs existentes.

## Como Funciona
Um PRD bem estruturado comunica claramente o quê, porquê e como de sua iniciativa de produto. Esta skill usa um template de 8 seções comprovado para comunicar efetivamente a visão do produto para engenheiros, designers, leadership e stakeholders.

## Quando Usar
- Início de novos produtos ou features significativas
- Documentação de iniciativas complexas
- Alinhamento de equipes multifuncionais
- Base para desenvolvimento e testes
- Comunicação com stakeholders externos

## Passo a Passo

### 1. Coleta de Informações
- Leia cuidadosamente todos os arquivos fornecidos
- Use web search para contexto adicional e insights de mercado
- Entenda o problema, público-alvo e restrições

### 2. Análise Prévia
Antes de escrever, analise:
- Qual problema estamos resolvendo?
- Para quem estamos resolvendo?
- Como mediremos o sucesso?
- Quais são nossas restrições e suposições?

### 3. Template PRD (8 Seções)

#### 1. Resumo (2-3 frases)
Sobre o que é este documento?
- Visão geral concisa da iniciativa
- Principal problema sendo resolvido
- Impacto esperado

#### 2. Contatos
Nome, função e comentários para stakeholders chave
- Product Manager: [nome] - Responsável geral
- Engineering Lead: [nome] - Viabilidade técnica
- Design Lead: [nome] - Experiência do usuário
- Business Stakeholder: [nome] - Alinhamento de negócios

#### 3. Contexto
Contexto: Sobre o que é esta iniciativa?
- Qual é o problema ou oportunidade?
- Por que agora? Algo mudou recentemente?
- Isso se tornou possível apenas recentemente?

#### 4. Objetivo
Qual o objetivo? Por que importa?
- Como beneficia a empresa e clientes?
- Como se alinha com visão e estratégia?
- Key Results: Como medir o sucesso? (Use formato SMART OKR)

**Exemplo de OKR:**
- **Objective:** Aumentar engajamento de usuários no FinanControl
- **Key Result 1:** Aumentar tempo médio de sessão de 5 para 8 minutos
- **Key Result 2:** Reduzir churn mensal de 15% para 10%
- **Key Result 3:** Atingir 85% de satisfação (NPS) na nova feature

#### 5. Segmentos de Mercado
Para quem estamos construindo isto?
- Quais restrições existem?
- Nota: Mercados são definidos por problemas/jobs das pessoas, não demografia

**Exemplo:**
- **Segmento Primário:** PMEs brasileiras (50-500 funcionários) com dificuldades em gestão financeira
- **Restrições:** Orçamento limitado (<R$10k/mês), equipe técnica pequena, necessidade de implementação rápida

#### 6. Propostas de Valor
Quais jobs/necessidades dos clientes estamos abordando?
- O que os clientes ganharão?
- Quais dores evitarão?
- Quais problemas resolvemos melhor que concorrentes?
- Considere framework Value Curve

**Exemplo:**
- **Job Before:** Gestores perdem 10h/semana em planilhas financeiras
- **How:** Automação de categorização e relatórios inteligentes
- **What After:** Recuperam 8h/semana para atividades estratégicas
- **Alternatives:** Excel, planilhas manuais, outros softwares complexos

#### 7. Solução
##### 7.1 UX/Protótipos (wireframes, user flows)
- Link para Figma/Miro com designs
- Fluxos de usuário principais
- Protótipos interativos

##### 7.2 Features Principais (descrições detalhadas)
Liste as features essenciais com descrições claras
- Feature 1: [Descrição detalhada]
- Feature 2: [Descrição detalhada]
- Feature 3: [Descrição detalhada]

##### 7.3 Tecnologia (opcional, apenas se relevante)
- Stack requirements ou restrições
- Integrações necessárias
- Considerações de performance

##### 7.4 Suposições (no que acreditamos mas não comprovamos)
- Suposição 1: [Descrição]
- Suposição 2: [Descrição]
- Como validaremos cada suposição

#### 8. Lançamento
Quanto tempo pode levar?
- O que vai na primeira versão vs. versões futuras?
- Evite datas exatas; use timeframe relativo

**Exemplo:**
- **MVP (4-6 semanas):** Features essenciais para validação
- **V1.0 (8-10 semanas):** Feature completa para lançamento geral
- **V2.0 (12-16 semanas):** Features avançadas e integrações

### 4. Linguagem Acessível
Escreva para um graduado do ensino fundamental. Evite jargões. Use frases claras e curtas.

### 5. Estrutura de Saída
Apresente o PRD como documento markdown bem formatado com cabeçalhos e seções claras.

### 6. Salvamento
Se o PRD for substancial (o que será), salve como: `PRD-[nome-produto].md`

## Exemplo Prático

### PRD: FinanControl Analytics Dashboard

#### 1. Resumo
Este documento especifica os requisitos para um dashboard analytics que ajuda PMEs a entender sua saúde financeira através de visualizações intuitivas e insights acionáveis.

#### 2. Contatos
- Product Manager: João Silva - Responsável geral
- Engineering Lead: Maria Santos - Viabilidade técnica
- Design Lead: Pedro Costa - Experiência do usuário
- Business Stakeholder: Ana Oliveira - Alinhamento de negócios

#### 3. Contexto
PMEs brasileiras perdem em média 10 horas por semana gerenciando finanças em planilhas. A pandemia acelerou digitalização, criando demanda por soluções acessíveis.

#### 4. Objetivo
**Objective:** Capacitar PMEs a tomar decisões financeiras informadas através de analytics acessíveis.
**Key Results:**
- KR1: Reduzir tempo de análise financeira em 70%
- KR2: Aumentar identificação de oportunidades de economia em 40%
- KR3: Atingir 90% de adoção em 30 dias pós-implementação

#### 5. Segmentos de Mercado
PMEs brasileiras (50-500 funcionários) com faturamento R$5M-50M, equipe financeira 1-5 pessoas, atualmente usando Excel/planilhas.

#### 6. Propostas de Valor
**Before:** Gestores gastam 10h/semana consolidando dados manualmente
**How:** Dashboard automático com insights em tempo real
**After:** Recuperam 7h/semana para análise estratégica
**Alternatives:** Consultorias caras, softwares enterprise complexos

#### 7. Solução
**7.1 UX/Protótipos:** [Link Figma com wireframes e protótipos]
**7.2 Features Principais:**
- Dashboard principal com KPIs financeiros
- Relatórios personalizáveis
- Alertas inteligentes de anomalias
- Exportação para PDF/Excel
**7.3 Suposições:**
- PMEs valorizam economia de tempo mais que features avançadas
- Usuários preferem visualizações simples a análises complexas

#### 8. Lançamento
**MVP (4 semanas):** Dashboard básico com 3 KPIs principais
**V1.0 (8 semanas):** Feature completa com relatórios e alertas
**V2.0 (12 semanas):** Previsões e benchmarking setorial

## Benefícios
- **Alinhamento:** Garante que todos entendam o quê e porquê
- **Clareza:** Reduz ambiguidade e mal-entendidos
- **Foco:** Mantém equipe focada nos objetivos do usuário
- **Métricas:** Estabelece critérios claros de sucesso

## Dicas de Uso
- Seja específico e data-driven onde possível
- Conecte cada seção de volta à estratégia geral
- Sinalize suposições claramente para validação pela equipe
- Mantenha documento conciso mas completo
- Atualize regularmente conforme aprendizados

## Recursos Adicionais
- [How to Write a Product Requirements Document? The Best PRD Template.](https://www.productcompass.pm/p/prd-template)
- [A Proven AI PRD Template by Miqdad Jaffer (Product Lead @ OpenAI)](https://www.productcompass.pm/p/ai-prd-template)
- [Product Requirements: The Complete Guide](https://www.productcompass.pm/p/product-requirements-guide)
