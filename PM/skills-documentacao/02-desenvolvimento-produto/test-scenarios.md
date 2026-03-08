# Cenários de Teste

## Propósito
Criar cenários de teste abrangentes de user stories com objetivos de teste, condições iniciais, papéis de usuário, ações passo a passo e resultados esperados. Usado ao escrever casos de teste QA, criar planos de teste, definir testes de aceitação ou preparar para validação de features.

## Como Funciona
Cenários de teste transformam user stories em casos de teste detalhados que validam se o software funciona conforme esperado. Cada cenário inclui objetivo, configuração, passos e resultados esperados para execução pela equipe QA.

## Quando Usar
- Preparação para testes de aceitação
- Criação de planos de teste QA
- Validação de implementação de user stories
- Documentação de processos de teste
- Garantia de qualidade antes de lançamentos

## Passo a Passo

### 1. Revisão da User Story
Revise a user story e critérios de aceitação.

### 2. Definição de Objetivos de Teste
O que específico validar neste teste?

### 3. Estabelecimento de Condições Iniciais
Estado do sistema, configuração de dados, preparação.

### 4. Identificação de Papéis de Usuário
Quem executa as ações de teste?

### 5. Criação de Passos de Teste
Divida interações passo a passo.

### 6. Definição de Resultados Esperados
Resultados observáveis após cada passo.

### 7. Consideração de Edge Cases
Inputs inválidos, condições de limite.

### 8. Saída Detalhada
Cenários prontos para execução pela equipe QA.

## Template de Cenário

**Cenário de Teste:** [Nome claro do cenário]

**Objetivo de Teste:** [O que este teste valida]

**Condições Iniciais:**
- [Estado do sistema necessário]
- [Dados ou configuração necessários]
- [Configuração de usuário ou permissões]

**Papel do Usuário:** [Quem executa o teste]

**Passos de Teste:**
1. [Primeira ação e resultado esperado]
2. [Segunda ação e resultado observável]
3. [Terceira ação e comportamento do sistema]
4. [Ação de conclusão e estado final]

**Resultados Esperados:**
- [Resultado observável 1]
- [Resultado observável 2]
- [Resultado observável 3]

## Exemplo de Cenário de Teste

**Cenário de Teste:** Visualizar Produtos Visualizados Recentemente na Página de Produto

**Objetivo de Teste:** Verificar que a seção 'Visualizados recentemente' exibe corretamente e exclui o produto atual.

**Condições Iniciais:**
- Usuário está logado ou tem histórico habilitado
- Usuário visualizou pelo menos 2 produtos na sessão atual
- Usuário agora está em uma página de produto diferente dos itens visualizados

**Papel do Usuário:** Comprador Online

**Passos de Teste:**
1. Navegar para qualquer página de produto → Seção deve aparecer na parte inferior com itens visualizados anteriormente
2. Rolar para baixo da página → Seção "Visualizados recentemente" está visível com cards de produtos
3. Verificar miniaturas de produtos → Imagens, títulos e preços exibidos corretamente
4. Verificar produto atual → Produto atual NÃO está na lista de visualizados recentes
5. Clicar em card de produto → Usuário navega para página correspondente

**Resultados Esperados:**
- Seção de visualizados recentes aparece apenas após visualizar pelo menos 1 produto anterior
- Seção exibe 4-8 cards de produtos com informações completas
- Produto atual é excluído da lista
- Cada card mostra "Visualizado há X minutos/horas"
- Clicar nos cards navega para páginas corretas
- Performance: Seção carrega em menos de 2 segundos

## Exemplo Prático

### Cenários de Teste: Dashboard Financeiro "FinanControl"

#### Cenário 1: Exibição de Saldo

**Cenário de Teste:** Exibição de Saldo em Tempo Real

**Objetivo de Teste:** Verificar exibição correta do saldo com atualização automática e formatação adequada.

**Condições Iniciais:**
- Usuário está logado no app FinanControl
- Usuário tem conta bancária conectada
- Sistema possui transações recentes (últimas 24h)

**Papel do Usuário:** Gestor Financeiro

**Passos de Teste:**
1. Abrir app FinanControl → Saldo total exibido em destaque na tela principal
2. Aguardar 30 segundos → Saldo atualiza automaticamente se houver novas transações
3. Verificar formatação → Valor exibido em formato brasileiro (R$ 1.234,56)
4. Verificar cores → Saldo positivo em verde, negativo em vermelho
5. Testar offline → Desconectar internet e verificar comportamento

**Resultados Esperados:**
- Saldo exibido em fonte grande e proeminente
- Atualização automática dentro de 30 segundos
- Formatação correta da moeda brasileira
- Cores diferenciadas para positivo/negativo
- Offline: exibe último saldo conhecido com indicador "sem conexão"

#### Cenário 2: Filtros de Período

**Cenário de Teste:** Funcionalidade de Filtros por Período

**Objetivo de Teste:** Validar funcionamento correto dos filtros de período e atualização dos dados.

**Condições Iniciais:**
- Usuário com histórico de transações de 6 meses
- Dashboard aberto na visualização padrão (últimos 30 dias)

**Papel do Usuário:** Analista Financeiro

**Passos de Teste:**
1. Clicar em dropdown de período → Opções predefinidas aparecem (Hoje, Esta Semana, Este Mês, Este Ano)
2. Selecionar "Esta Semana" → Todos os gráficos e tabelas atualizam para dados da semana atual
3. Selecionar "Período Personalizado" → Calendários aparecem para selecionar datas
4. Selecionar datas inválidas (fim antes do início) → Sistema exibe mensagem de erro
5. Clicar "Limpar Filtros" → Sistema retorna para período padrão (últimos 30 dias)

**Resultados Esperados:**
- Opções predefinidas funcionam corretamente
- Período personalizado aceita datas válidas
- Validação impede seleção de datas inválidas
- Todos os componentes visuais atualizam com novo período
- Período selecionado exibido claramente acima dos dados

#### Cenário 3: Exportação de Relatórios

**Cenário de Teste:** Exportação de Relatórios em PDF

**Objetivo de Teste:** Verificar geração correta de relatórios PDF com todas as informações necessárias.

**Condições Iniciais:**
- Usuário com permissões de administrador
- Dashboard com dados completos do último mês
- Conexão internet estável

**Papel do Usuário:** Diretor Financeiro

**Passos de Teste:**
1. Clicar botão "Exportar PDF" na seção de relatórios → Modal de opções aparece
2. Selecionar formato A4 e orientação retrato → Opções confirmadas
3. Clicar "Gerar PDF" → Indicador de progresso aparece
4. Aguardar geração (máximo 10 segundos) → Download inicia automaticamente
5. Abrir PDF baixado → Verificar conteúdo e formatação

**Resultados Esperados:**
- PDF gerado dentro de 10 segundos
- Logo da empresa e data de geração incluídos
- Gráficos com qualidade suficiente para impressão
- Nome do arquivo segue padrão "FinanControl_Relatorio_YYYY-MM-DD.pdf"
- Todos os dados do dashboard presentes no PDF

#### Cenário 4: Detecção de Anomalias

**Cenário de Teste:** Detecção Automática de Transações Anômalas

**Objetivo de Teste:** Validar identificação correta de gastos suspeitos baseados em histórico.

**Condições Iniciais:**
- Usuário com 3 meses de histórico de transações
- Sistema treinado com padrões de gastos do usuário
- Transações de teste incluídas (uma anômala, uma normal)

**Papel do Usuário:** Analista de Riscos

**Passos de Teste:**
1. Acessar seção de anomalias → Dashboard exibe transações suspeitas destacadas
2. Verificar transação anômala de teste → Destacada com cor diferente e ícone
3. Clicar na transação anômala → Explicação aparece do porquê foi marcada
4. Clicar "Marcar como Normal" → Sistema atualiza e aprende com correção
5. Adicionar nova transação anômala → Sistema detecta em tempo real

**Resultados Esperados:**
- Anomalias detectadas com base em padrões históricos
- Destaque visual claro para transações suspeitas
- Explicações compreensíveis para marcações
- Sistema aprende com correções do usuário
- Detecção funciona para novas transações em tempo real

## Deliverables de Saída

- Cenários de teste abrangentes para cada critério de aceitação
- Objetivos de teste claros alinhados com intenção da user story
- Ações de teste passo a passo detalhadas
- Resultados esperados observáveis após cada passo
- Cobertura de edge cases e cenários de erro
- Prontos para execução pela equipe QA e documentação

## Benefícios
- **Qualidade:** Garante validação completa das features
- **Clareza:** Passos explícitos reduzem ambiguidade
- **Consistência:** Padroniza processo de teste
- **Eficiência:** Testes estruturados aceleram validação

## Dicas de Uso
- Envolva a equipe QA na criação dos cenários
- Teste tanto caminhos felizes quanto edge cases
- Inclui testes de performance e acessibilidade
- Mantenha cenários atualizados com mudanças no produto
- Use automação onde possível para testes repetitivos

## Recursos Adicionais
- [QA Testing: The Complete Guide](https://www.productcompass.pm/p/qa-testing-complete-guide)
- [Test-Driven Development: Best Practices](https://www.productcompass.pm/p/test-driven-development-guide)
- [User Acceptance Testing: How to Run UAT](https://www.productcompass.pm/p/user-acceptance-testing)
