# Why-What-Acceptance (WWA)

## Propósito
Criar itens de backlog de produto em formato Why-What-Acceptance — itens independentes, valiosos e testáveis com contexto estratégico. Usado ao escrever itens de backlog estruturados, dividir features em itens de trabalho ou usar formato WWA.

## Como Funciona
O formato WWA conecta trabalho a objetivos de negócio e equipe, mantendo descrições concisas e critérios de aceitação de alto nível. Cada item é independente, negociável e dimensionado para conclusão em um sprint.

## Quando Usar
- Escrita de itens de backlog
- Criação de incrementos de produto
- Divisão de features em itens de trabalho
- Comunicação de intenção estratégica para equipes
- Planejamento de sprints

## Passo a Passo

### 1. Definir o Why Estratégico
Conecte o trabalho a objetivos de negócio e da equipe.

### 2. Descrever o What
Mantenha descrições concisas, referencie designs.

### 3. Escrever Critérios de Aceitação
Critérios de alto nível, não especificações detalhadas.

### 4. Garantir Independência
Itens podem ser desenvolvidos em qualquer ordem.

### 5. Manter Itens Negociáveis
Convide conversação da equipe, não restrições.

### 6. Tornar Itens Valiosos
Cada item entrega valor mensurável para usuário ou negócio.

### 7. Garantir Testabilidade
Outcomes são observáveis e verificáveis.

### 8. Dimensionar Apropriadamente
Pequeno o suficiente para estimativa de um sprint.

## Template de Item

**Título:** [O que será entregue]

**Why:** [1-2 frases conectando ao contexto estratégico e objetivos da equipe]

**What:** [Descrição curta e link de design. Máximo 2 parágrafos. Lembrete de discussão, não especificação detalhada.]

**Critérios de Aceitação:**
- [Outcome observável 1]
- [Outcome observável 2]
- [Outcome observável 3]
- [Outcome observável 4]

## Exemplo de Item WWA

**Título:** Implementar Rastreador de Gastos em Tempo Real

**Why:** Usuários precisam de feedback imediato sobre gastos para tomar decisões conscientes de orçamento. Isso apoia diretamente nosso objetivo de melhorar consciência financeira e reduzir overspending.

**What:** Adicionar rastreador de gastos em tempo real que atualiza conforme usuários registram despesas. O rastreador exibe gastos da semana atual contra orçamento definido. Designs disponíveis em [link Figma]. Isso é um lembrete de nossas discussões - especificações detalhadas emergirão durante conversas de desenvolvimento com a equipe.

**Critérios de Aceitação:**
- Totais de gastos atualizam dentro de 2 segundos de registrar despesa
- Progresso do orçamento é indicado visualmente com barra de progresso
- Usuários podem ver valor restante do orçamento à primeira vista
- Sistema lida corretamente com múltiplas categorias de despesas

## Exemplo Prático

### Itens WWA: Dashboard Financeiro "FinanControl"

#### Item 1: Widget de Saldo Principal

**Título:** Widget de Saldo em Tempo Real

**Why:** Usuários precisam ver sua situação financeira atual imediatamente ao abrir o app para tomar decisões informadas. Isso reduz ansiedade e aumenta confiança na gestão financeira.

**What:** Implementar widget principal exibindo saldo total disponível com atualização automática. Widget deve mostrar saldo atual, variação do dia e indicador visual de saúde financeira. Designs em [Figma link]. Lembrete de nossas discussões - detalhes técnicos serão definidos em colaboração com engenharia.

**Critérios de Aceitação:**
- Saldo total exibido em destaque na tela principal
- Valores atualizam automaticamente a cada 30 segundos
- Indicador visual (verde/vermelho) baseado em metas de orçamento
- Formatação brasileira de moeda (R$ 1.234,56)
- Performance: carrega em menos de 2 segundos

#### Item 2: Categorização Inteligente

**Título:** Categorização Automática de Despesas

**Why:** Usuários perdem tempo categorizando manualmente cada despesa, o que reduz adoção do app. Automação aumenta engajamento e valor percebido.

**What:** Implementar sistema de categorização automática baseado em regras e machine learning. Sistema deve aprender com correções do usuário e sugerir categorias para novas transações. Designs em [Figma link]. Especificações detalhadas serão definidas com equipe de ML e engenharia.

**Critérios de Aceitação:**
- 80% das transações categorizadas automaticamente corretamente
- Usuário pode corrigir categoria com 1 toque
- Sistema melhora acurácia com base em correções
- Sugestões aparecem em tempo real durante registro
- Fallback para categorização manual sempre disponível

#### Item 3: Alertas de Orçamento

**Título:** Sistema de Alertas de Orçamento

**Why:** Usuários frequentemente excedem orçamentos porque não são alertados atempadamente. Alertas proativos ajudam a manter disciplina financeira.

**What:** Criar sistema de notificações push e in-app para alertas de orçamento. Sistema deve enviar alertas em pontos críticos (50%, 80%, 100%) do orçamento. Designs em [Figma link]. Timing e frequência serão ajustados com base em feedback do usuário.

**Critérios de Aceitação:**
- Alertas enviados aos 50%, 80% e 100% do orçamento
- Notificações push funcionam em iOS e Android
- Usuário pode personalizar thresholds de alerta
- Opção de silenciar alertas por período
- Histórico de alertas disponível para referência

#### Item 4: Relatórios Mensais

**Título:** Geração de Relatórios Mensais

**Why:** Usuários precisam entender padrões de gastos ao longo do tempo para tomar decisões financeiras estratégicas. Relatórios mensais fornecem visão essencial.

**What:** Implementar funcionalidade de gerar relatórios mensais com breakdown por categoria, tendências e insights. Relatórios devem ser exportáveis em PDF e compartilháveis. Designs em [Figma link]. Formato e conteúdo serão refinados com base em feedback inicial.

**Critérios de Aceitação:**
- Relatório inclui resumo, categorias, tendências e insights
- Exportação em PDF com layout profissional
- Comparação com mês anterior e ano anterior
- Insights acionáveis baseados em padrões detectados
- Geração em menos de 10 segundos

## Deliverables de Saída

- Conjunto completo de itens de backlog para a feature
- Cada item inclui seções Why, What e Critérios de Aceitação
- Itens são independentes e entregáveis em qualquer ordem
- Itens dimensionados para estimativa e conclusão em um sprint
- Contexto estratégico claro para tomada de decisão da equipe
- Referências de design incluídas para orientação de implementação

## Benefícios
- **Estratégia:** Conecta trabalho tático a objetivos estratégicos
- **Clareza:** Foco em outcomes em vez de features
- **Flexibilidade:** Permite adaptação durante desenvolvimento
- **Alinhamento:** Equipe entende o "porquê" do trabalho

## Dicas de Uso
- Use o Why para motivar a equipe e justificar prioridade
- Mantenha o What conciso para permitir autonomia técnica
- Critérios de aceitação devem testar outcomes, não implementação
- Revise itens regularmente com base em aprendizados
- Use WWA para iniciativas complexas que requerem alinhamento estratégico

## Recursos Adicionais
- [How to Write User Stories: The Ultimate Guide](https://www.productcompass.pm/p/how-to-write-user-stories)
- [Strategic Product Management: Connecting Work to Outcomes](https://www.productcompass.pm/p/strategic-product-management)
- [Backlog Management: Best Practices](https://www.productcompass.pm/p/backlog-management-best-practices)
