# Resumo de Entrevista com Cliente

## Propósito
Resumir transcript de entrevista com cliente em template estruturado com JTBD, sinais de satisfação e itens de ação. Usado ao processar gravações ou transcrições de entrevistas, sintetizar entrevistas de discovery ou criar resumos de entrevistas.

## Como Funciona
Transforma transcript de entrevista em resumo estruturado focado em Jobs to Be Done, satisfação e itens de ação. Extrai insights essenciais do raw data para facilitar análise e compartilhamento com a equipe.

## Quando Usar
- Após cada entrevista de usuário
- Síntese de múltiplas entrevistas
- Preparação para apresentação ao time
- Identificação de padrões entre entrevistas
- Documentação de pesquisa de discovery

## Passo a Passo

### 1. Ler o Transcript Completo
Leia cuidadosamente todo o transcript antes de resumir. Procure por:
- Padrões de comportamento repetidos
- Emoções fortes (frustração, encanto)
- Citações memoráveis
- Comportamentos específicos vs. opiniões genéricas

### 2. Preencher Template de Resumo
Use "-" se informação não estiver disponível. Substitua valores numéricos por descrições qualitativas se necessário (ex: "não satisfeito").

### 3. Usar Linguagem Clara e Simples
Um graduado do ensino fundamental deve conseguir entender o resumo.

## Template de Saída

```
**Data**: [Data e hora da entrevista]
**Participantes**: [Nomes completos e funções]
**Background**: [Informações de background sobre o cliente]

**Solução Atual**: [O que usam atualmente]

**O Que Gostam na Solução Atual**:
- [JTBD, outcome desejado, importância e nível de satisfação]

**Problemas com Solução Atual**:
- [JTBD, outcome desejado, importância e nível de satisfação]

**Insights Principais**:
- [Descobertas inesperadas ou citações notáveis]

**Itens de Ação**:
- [Data, Owner, Ação — ex: "2025-01-15, João, Seguir com cliente sobre precificação"]
```

## Exemplo Prático

### Resumo: Entrevista com Maria Silva - FinanControl

```
**Data**: 15 de Março de 2026, 14:30
**Participantes**: Maria Silva (Gerente Financeira, PME Tech), João Santos (Product Manager)
**Background**: Contadora em PME de tecnologia com 30 funcionários, 5 anos de experiência, responsável por finanças de 3 clientes

**Solução Atual**: Excel + QuickBooks + planilhas personalizadas

**O Que Gostam na Solução Atual**:
- Excel: "Total controle sobre formatação e cálculos" - Importância alta, satisfação 7/10
- QuickBooks: "Integração com banco funciona bem" - Importância média, satisfação 6/10
- Planilhas: "Customizadas para meu negócio específico" - Importância alta, satisfação 8/10

**Problemas com Solução Atual**:
- Conciliação de dados: "Perco 8 horas por mês juntando informações" - Importância alta, satisfação 2/10
- Erros manuais: "Ja enviei relatório errado por erro de fórmula" - Importância alta, satisfação 1/10
- Tempo real: "Não sei como estou até fim do dia" - Importância média, satisfação 3/10
- Backup: "Tenho medo de perder dados do Excel" - Importância baixa, satisfação 4/10

**Insights Principais**:
- Surpresa: "Confio mais em minhas planilhas do que em sistemas porque entendo cada fórmula"
- Citação memorável: "Se o sistema erra, eu não sei como corrigir. Se eu erro no Excel, sei exatamente onde foi"
- Comportamento: Verifica saldos 3x ao dia durante fechamento mensal
- Emoção: Visível frustração ao falar de conciliação manual

**Itens de Ação**:
- 2025-03-20, João, Enviar demo de conciliação automática
- 2025-03-22, Maria, Compartilhar template de planilha atual
- 2025-03-25, Equipe Design, Criar protótipo de "modo transparente"
```

## Exemplo de Múltiplas Entrevistas

### Síntese: 5 Entrevistas - Gestão Financeira PME

```
**Período**: 10-15 Março de 2026
**Participantes**: 5 gerentes financeiros de PMEs diferentes
**Background**: Empresas 20-200 funcionários, setores diversos

**Soluções Atuais**: Excel (100%), QuickBooks (60%), planilhas customizadas (80%), outros sistemas (40%)

**Padrões - O Que Gostam**:
- Controle total do Excel (mencionado por todos) - Importância alta, satisfação média 7/10
- Flexibilidade de customização (4/5) - Importância alta, satisfação 8/10
- Familiaridade com ferramentas (5/5) - Importância média, satisfação 9/10

**Padrões - Problemas**:
- Tempo gasto em conciliação (5/5) - Importância alta, satisfação 2/10
- Erros manuais (4/5) - Importância alta, satisfação 1/10
- Falta de visão em tempo real (3/5) - Importância média, satisfação 3/10
- Risco de perda de dados (2/5) - Importância baixa, satisfação 4/10

**Insights Principais**:
- Surpresa: Todos preferem controle sobre automação
- Pad rão: "Se entendo, confio. Se não entendo, não confio"
- Comportamento: Verificação múltipla diária é comum
- Emoção: Ansiedade alta durante fechamento mensal

**Itens de Ação Consolidados**:
- 2025-03-20, Equipe Produto, Priorizar feature "audit trail" visível
- 2025-03-22, Design, Criar interface "Excel-like" para familiaridade
- 2025-03-25, Engineering, Implementar backup automático visível
- 2025-03-28, Todos, Testar hipótese de controle vs. automação
```

## Modelos por Tipo de Entrevista

### Entrevista de Validação de Problema
Foco em dor e comportamento atual:
```
**Problema Validado**: [Nome do problema]
**Intensidade**: [Alta/Média/Baixa] baseada em emoção
**Frequência**: [Como afeta diariamente/semanalmente/mensalmente]
**Workaround Atual**: [Como resolvem agora]
**Custo do Problema**: [Tempo/money/frustração]
```

### Entrevista de Teste de Conceito
Foco em reação a solução específica:
```
**Reação Inicial**: [Primeira impressão]
**Compreensão**: [Entenderam a proposta?]
**Comparação**: [Como vs. solução atual]
**Objecções**: [Preocupações levantadas]
**Disposição a Testar**: [Interesse em experimentar]
```

### Entrevista de Pós-Implementação
Foco em uso real e satisfação:
```
**Adoção Real**: [Como usam no dia a dia]
**Valor Realizado**: [Benefícios obtidos]
**Problemas Inesperados**: [Dificuldades não previstas]
**Sugestões**: [Melhorias solicitadas]
**NPS/Lealdade**: [Recomendariam? Continuariam?]
```

## Benefícios
- **Eficiência:** Transforma 1h de transcript em 5min de insights
- **Compartilhamento:** Formato padronizado para fácil consumo
- **Análise:** Facilita identificação de padrões entre entrevistas
- **Ação:** Gera itens concretos para seguimento

## Dicas de Uso
- Capture citações exatas quando memoráveis
- Note emoções e linguagem corporal (se entrevista presencial)
- Seja específico sobre comportamentos, não opiniões
- Inclua contexto do negócio quando relevante
- Use números quando disponíveis (horas, %, frequência)

## Processo de Trabalho Sugerido

### Individual
1. Grave entrevista
2. Transcreva (ou use serviço de transcrição)
3. Preencha template imediatamente
4. Compartilhe com equipe em 24h

### Múltiplas Entrevistas
1. Resuma cada entrevista individualmente
2. Crie síntese consolidada ao final
3. Identifique padrões e divergências
4. Apresente insights para stakeholders

## Recursos Adicionais
- [User Interviews: The Ultimate Guide to Research Interviews](https://www.productcompass.pm/p/interviewing-customers-the-ultimate)
- [Continuous Product Discovery Masterclass (CPDM)](https://www.productcompass.pm/p/cpdm) (video course)
- [Note-Taking for User Research](https://www.productcompass.pm/p/note-taking-user-research)
- [Customer Interview Analysis](https://www.productcompass.pm/p/customer-interview-analysis)
