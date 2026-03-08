# User Stories

## Propósito
Criar user stories seguindo os 3 Cs (Card, Conversation, Confirmation) e critérios INVEST com descrições, links de design e critérios de aceitação. Usado ao escrever user stories, dividir features em itens de backlog ou definir critérios de aceitação.

## Como Funciona
User stories são descrições concisas de features do ponto de vista do usuário, seguindo o formato "Como um [tipo de usuário], eu quero [ação] para que [benefício]". Cada story inclui critérios de aceitação claros e links para designs.

## Quando Usar
- Planejamento de sprints
- Divisão de features em unidades gerenciáveis
- Comunicação com equipe de desenvolvimento
- Definição de critérios de teste
- Priorização de trabalho

## Passo a Passo

### 1. Análise da Feature
- Analise a feature baseada no design e contexto fornecidos
- Identifique user roles e jornadas distintas
- Entenda o problema sendo resolvido

### 2. Aplicação dos 3 Cs Framework
- **Card:** Título simples e one-liner
- **Conversation:** Discussão detalhada da intenção
- **Confirmation:** Critérios de aceitação claros

### 3. Respeito aos Critérios INVEST
- **Independent:** Stories podem ser desenvolvidas em qualquer ordem
- **Negotiable:** Convidam conversação, não restrições
- **Valuable:** Entregam valor mensurável para usuário ou negócio
- **Estimable:** Tamanho pode ser estimado
- **Small:** Pequenas o suficiente para um sprint
- **Testable:** Resultados são observáveis e verificáveis

### 4. Linguagem Acessível
Use linguagem que um graduado do ensino fundamental entenda.

### 5. Links para Design
Referencie arquivos de design para contexto visual.

### 6. Saída Estruturada
Apresente user stories em formato estruturado.

## Template de Story

**Título:** [Nome da feature]

**Descrição:** Como um [user role], eu quero [action], para que [benefit].

**Design:** [Link para arquivos de design]

**Critérios de Aceitação:**
1. [Critério claro e testável]
2. [Comportamento observável]
3. [Sistema valida corretamente]
4. [Tratamento de edge cases]
5. [Consideração de performance ou acessibilidade]
6. [Ponto de integração]

## Exemplo de User Story

**Título:** Seção de Produtos Visualizados Recentemente

**Descrição:** Como um Comprador Online, eu quero ver uma seção 'Visualizados recentemente' na página do produto para revisitar facilmente itens que considerei.

**Design:** [Link Figma]

**Critérios de Aceitação:**
1. A seção 'Visualizados recentemente' é exibida na parte inferior da página do produto para todo usuário que visualizou pelo menos 1 produto anteriormente.
2. Não é exibida para usuários visitando a primeira página de produto da sessão.
3. O produto atual é excluído dos itens exibidos.
4. A seção exibe cards de produtos com imagens, títulos e preços.
5. Cada card de produto indica quando foi visualizado (ex: 'Visualizado há 5 minutos').
6. Clicar em um card de produto leva o usuário à página correspondente.

## Exemplo Prático

### User Stories: Dashboard Financeiro "FinanControl"

#### Story 1: Visualização de Saldo

**Título:** Saldo em Tempo Real

**Descrição:** Como um Gestor Financeiro, eu quero ver meu saldo atualizado em tempo real para tomar decisões imediatas.

**Design:** [Link Figma - Dashboard Principal]

**Critérios de Aceitação:**
1. O saldo total é exibido no topo do dashboard em fonte grande e destacada.
2. O saldo atualiza automaticamente a cada 30 segundos.
3. Indicador visual mostra quando dados foram atualizados pela última vez.
4. Saldo é formatado em moeda brasileira (R$ 1.234,56).
5. Cores diferenciam saldo positivo (verde) de negativo (vermelho).
6. Funciona offline exibindo último saldo conhecido com indicador "sem conexão".

#### Story 2: Filtros de Período

**Título:** Filtro por Período

**Descrição:** Como um Analista Financeiro, eu quero filtrar transações por período personalizado para analisar tendências específicas.

**Design:** [Link Figma - Componente Filtros]

**Critérios de Aceitação:**
1. Campo de seleção permite escolher períodos predefinidos (Hoje, Esta Semana, Este Mês, Este Ano).
2. Opção "Período Personalizado" abre calendários para selecionar data início e fim.
3. Filtros aplicados atualizam instantaneamente todos os gráficos e tabelas.
4. Período selecionado é exibido claramente acima dos dados.
5. Botão "Limpar Filtros" reseta para período padrão (últimos 30 dias).
6. Sistema valida que data fim não seja anterior à data início.

#### Story 3: Exportação de Relatórios

**Título:** Exportar para PDF

**Descrição:** Como um Diretor, eu quero exportar relatórios financeiros em PDF para compartilhar com investidores e equipe.

**Design:** [Link Figma - Modal Exportação]

**Critérios de Aceitação:**
1. Botão "Exportar PDF" está disponível em cada seção de relatório.
2. Ao clicar, modal oferece opções de formato (A4, Carta) e orientação (retrato, paisagem).
3. PDF gerado inclui logo da empresa, data de geração e período analisado.
4. Gráficos são exportados com qualidade suficiente para impressão.
5. Nome do arquivo segue padrão: "FinanControl_Relatorio_[YYYY-MM-DD].pdf".
6. Download inicia automaticamente após geração (máximo 10 segundos).

## Deliverables de Saída

- Conjunto completo de user stories para a feature
- Cada story inclui título, descrição, link de design e 4-6 critérios de aceitação
- Stories são independentes e podem ser desenvolvidas em qualquer ordem
- Stories dimensionadas para um ciclo de sprint
- Stories referenciam documentação de design relacionada

## Benefícios
- **Clareza:** Foco no valor para o usuário
- **Comunicação:** Linguagem simples e compartilhada
- **Testabilidade:** Critérios claros para validação
- **Flexibilidade:** Stories podem ser reordenadas e priorizadas

## Dicas de Uso
- Escreva stories em colaboração com equipe
- Mantenha stories pequenas e focadas
- Use critérios de aceitação observáveis
- Inclua sempre o "porquê" (benefício)
- Revise stories regularmente com base em feedback

## Recursos Adicionais
- [How to Write User Stories: The Ultimate Guide](https://www.productcompass.pm/p/how-to-write-user-stories)
- [Agile Estimation: Story Points vs Hours](https://www.productcompass.pm/p/agile-estimation-guide)
- [Acceptance Criteria: How to Write Testable Requirements](https://www.productcompass.pm/p/acceptance-criteria-guide)
