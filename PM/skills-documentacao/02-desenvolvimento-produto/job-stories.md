# Job Stories

## Propósito
Criar job stories usando o formato "Quando [situação], eu quero [motivação], para que [outcome]" com critérios de aceitação detalhados. Usado ao escrever job stories, criar itens de backlog estilo JTBD ou expressar situações e motivações de usuários.

## Como Funciona
Job stories focam no contexto e situação do usuário em vez de personas fixas. O formato "Quando...eu quero...para que" captura a situação, motivação e resultado desejado, alinhando com framework Jobs-to-be-Done (JTBD).

## Quando Usar
- Foco em contexto do usuário em vez de roles
- Desenvolvimento centrado em situações reais
- Criação de backlog JTBD-style
- Expressão de motivações subjacentes
- Design de soluções contextuais

## Passo a Passo

### 1. Identificação de Situações
Identifique situações que disparam a necessidade do usuário.

### 2. Definição de Motivações
Defina as motivações subjacentes ao comportamento do usuário.

### 3. Clarificação de Outcomes
Clarifique os resultados que o usuário quer alcançar.

### 4. Aplicação Framework JTBD
Foque no job, não no role ou persona.

### 5. Criação de Critérios de Aceitação
Crie critérios que validem que o outcome foi alcançado.

### 6. Linguagem Observável e Mensurável
Use linguagem que possa ser observada e medida.

### 7. Links para Mockups
Referencie designs e protótipos.

### 8. Saída Estruturada
Output job stories com critérios de aceitação detalhados.

## Template de Story

**Título:** [Outcome ou resultado do job]

**Descrição:** Quando [situação], eu quero [motivação], para que [outcome].

**Design:** [Link para arquivos de design]

**Critérios de Aceitação:**
1. [Situação é propriamente reconhecida]
2. [Sistema permite a motivação desejada]
3. [Progresso ou feedback é visível]
4. [Outcome é alcançado eficientemente]
5. [Edge cases são tratados gracefulmente]
6. [Integração e notificações funcionam]

## Exemplo de Job Story

**Título:** Rastrear Gastos Semanais de Lanches

**Descrição:** Quando estou preparando minha mesada semanal para lanches (situação), eu quero ver rapidamente quanto gastei até agora (motivação), para que possa garantir que não ficarei sem dinheiro antes do fim de semana (outcome).

**Design:** [Link Figma]

**Critérios de Aceitação:**
1. Exibir Resumo de Gastos com seção "Visão Geral de Gastos Semanais"
2. Atualização em Tempo Real quando despesa registrada
3. Indicador de Progresso (barra mostrando 0-100% do orçamento semanal)
4. Destaque para Orçamento Restante em cor proeminente
5. Log Detalhado de Gastos com breakdown por categoria
6. Notificações aos 80% do orçamento
7. Lembrede Específico de Fim de Semana aos 90% na quinta-feira à noite
8. Acesso Fácil e Navegação para breakdown detalhado

## Exemplo Prático

### Job Stories: App de Finanças Pessoais "FinanControl"

#### Job Story 1: Planejamento de Compras

**Título:** Controlar Orçamento de Supermercado

**Descrição:** Quando estou fazendo minha lista de compras do mês (situação), eu quero ver quanto ainda posso gastar em cada categoria (motivação), para que não ultrapasse meu orçamento e precise cortar outros gastos essenciais (outcome).

**Design:** [Link Figma - Planejamento de Compras]

**Critérios de Aceitação:**
1. Exibir Categorias de Orçamento com valores restantes destacados
2. Atualização Automática quando compra registrada
3. Alertas Visuais quando categoria approaching 80% do limite
4. Sugestões de Rebalanceamento quando categoria excedida
5. Histórico de Compras por Categoria para referência
6. Comparação com Mês Anterior para contexto
7. Modo "Planejamento" para simular compras antes de sair
8. Integração com Listas de Compras existentes

#### Job Story 2: Identificação de Gastos Anômalos

**Título:** Detectar Despesas Inesperadas

**Descrição:** Quando estou revisando meu extrato bancário no fim do mês (situação), eu quero identificar rapidamente gastos que fogem do meu padrão normal (motivação), para que possa investigar possíveis erros, fraudes ou esquecimentos de assinaturas (outcome).

**Design:** [Link Figma - Análise de Anomalias]

**Critérios de Aceitação:**
1. Detecção Automática de Anomalias baseada em histórico de 3 meses
2. Destaque Visual para transações suspeitas (cor diferente, ícone)
3. Explicação Simples do porquê foi marcada como anomalia
4. Opção de "Marcar como Normal" para ensinar o sistema
5. Alertas Push para anomalias acima de R$500
6. Dashboard de Resumo com top 5 anomalias do mês
7. Filtros por valor, categoria e frequência
8. Exportação de Relatório de Anomalias para contestação bancária

#### Job Story 3: Otimização de Assinaturas

**Título:** Revisar Assinaturas Mensais

**Descrição:** Quando recebo meu extrato no fim do mês e vejo muitas cobranças recorrentes (situação), eu quero visualizar todas minhas assinaturas em um só lugar com seus custos e benefícios (motivação), para que possa decidir quais manter, cancelar ou renegociar (outcome).

**Design:** [Link Figma - Gestão de Assinaturas]

**Critérios de Aceitação:**
1. Detecção Automática de Cobranças Recorrentes baseada em padrão
2. Dashboard Central de Todas Assinaturas com logo e categoria
3. Cálculo de Custo Anual Total para cada assinatura
4. Indicador de Uso (baseado em transações relacionadas)
5. Alertas para Assinaturas Não Utilizadas (>60 dias sem uso)
6. Comparação de Preços com alternativas de mercado
7. Botões Diretos para Cancelar (quando disponível)
8. Lembretes Mensais antes de renovações automáticas

#### Job Story 4: Preparação para Impostos

**Título:** Organizar Documentos Fiscais

**Descrição:** Quando se aproxima a época de declarar imposto de renda (situação), eu quero organizar e categorizar todas minhas despesas dedutíveis do ano (motivação), para que possa maximizar minha restituição e evitar problemas com a receita federal (outcome).

**Design:** [Link Figma - Preparação Fiscal]

**Critérios de Aceitação:**
1. Identificação Automática de Despesas Dedutíveis (saúde, educação, etc.)
2. Cálculo do Valor Total Dedutível por Categoria
3. Geração de Relatório em Formato Aceito pela Receita Federal
4. Upload e Organização de Notas Fiscais e Comprovantes
5. Validação de CPF/CNPJ em Notas Fiscais
6. Timeline de Documentos ao Longo do Ano
7. Alertas de Documentos Faltantes
8. Exportação para Planilha ou Contador

## Deliverables de Saída

- Conjunto completo de job stories para a feature
- Cada story segue formato "Quando...eu quero...para que"
- 6-8 critérios de aceitação focados em outcomes
- Stories enfatizam situações e motivações do usuário
- Links claros para designs e protótipos

## Benefícios
- **Contexto:** Foco em situações reais do usuário
- **Motivação:** Entendimento profundo do "porquê"
- **Flexibilidade:** Menos rígido que personas fixas
- **Inovação:** Abre espaço para soluções criativas

## Dicas de Uso
- Observe usuários reais em seus ambientes naturais
- Capture situações específicas, não cenários genéricos
- Foque no progresso que o usuário quer alcançar
- Use job stories para descobrir necessidades não expressas
- Combine com user stories para especificação completa

## Recursos Adicionais
- [Jobs-to-be-Done Masterclass with Tony Ulwick and Sabeen Sattar](https://www.productcompass.pm/p/jobs-to-be-done-masterclass-with) (video course)
- [JTBD Theory: The Complete Guide](https://www.productcompass.pm/p/jtbd-theory-complete-guide)
- [Customer Jobs: How to Identify and Serve Them](https://www.productcompass.pm/p/customer-jobs-identify-serve)
