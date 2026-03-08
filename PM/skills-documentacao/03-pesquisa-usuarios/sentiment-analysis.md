# Análise de Sentimento

## Propósito
Analisar dados de feedback de usuários para identificar segmentos com scores de sentimento, JTBD e insights de satisfação do produto. Usado ao analisar feedback de usuários em escala, rodar análise de sentimento em reviews ou pesquisas, ou identificar padrões de satisfação.

## Como Funciona
Analisa dados de feedback de usuários em grande escala para identificar segmentos de mercado, medir satisfação e descobrir oportunidades de melhoria do produto. Sintetiza feedback em insights acionáveis organizados por segmento, sentimento e impacto.

## Quando Usar
- Análise de feedback em escala após lançamentos
- Identificação de padrões de satisfação/insatisfação
- Priorização de melhorias do produto
- Análise de reviews de app stores ou pesquisas
- Monitoramento de saúde do produto

## Passo a Passo

### 1. Ingestão de Dados
Leia todas as fontes de feedback e crie inventário:
- Reviews de app stores
- Respostas de pesquisas NPS/CSAT
- Tickets de suporte
- Feedback de comunidades sociais
- Transcrições de entrevistas
- Comentários de blogs e fóruns

### 2. Identificação de Segmentos
Identifique pelo menos 3 segmentos distintos de usuários ou personas do feedback.

### 3. Análise Temática
Extraia temas recorrentes, pontos de dor e feedback positivo por segmento.

### 4. Scoring de Sentimento
Atribua scores de sentimento (-1 a +1) para satisfação geral por segmento.

### 5. Avaliação de Impacto
Priorize insights por frequência, severidade e impacto nos negócios.

### 6. Síntese
Crie perfis de segmento com insights consolidados.

## Estrutura de Saída

Para cada segmento identificado:

### Perfil do Segmento
- Nome/identificador e características comuns
- Contagem de usuários ou proporção no dataset
- Caso de uso ou contexto principal

### Jobs-to-be-Done
- Job principal que este segmento tenta accomplar
- Outcomes desejados associados

### Score de Sentimento e Nível de Satisfação
- Score geral de sentimento (-1 a +1)
- Drivers de satisfação e detratores chave
- Proxy de Net Promoter Score (NPS) se aplicável

### Principais Temas de Feedback Positivo
- O que este segmento ama no produto
- Pontos fortes da perspectiva do usuário
- Exemplos de casos de uso bem-sucedidos

### Principais Pontos de Dor e Críticas
- Queixas ou frustrações mais frequentes
- Necessidades não atendidas ou features faltantes
- Pontos de atrito na jornada do usuário
- Citações diretas do feedback quando disponível

### Avaliação de Adequação Produto-Segmento
- Como bem o produto serve às necessidades deste segmento
- Potencial de melhorar adequação através de mudanças no produto
- Risco de churn ou insatisfação

### Recomendações Acionáveis
- 2-3 melhorias de maior impacto por segmento
- Quick wins vs. iniciativas estratégicas
- Segmentos para priorizar ou despriorizar

## Exemplo Prático

### Análise de Sentimento: FinanControl App Reviews

#### Segmento 1: "Controladores Precisos" (35% dos reviews)

**Perfil do Segmento:**
- Nome: Controladores Precisos
- Proporção: 35% (350/1000 reviews)
- Contexto: Profissionais financeiros focados em precisão

**Jobs-to-be-Done:**
- Job principal: "Garantir 100% de precisão em relatórios financeiros"
- Outcome desejado: Confiança absoluta nos números apresentados

**Score de Sentimento:**
- Score geral: +0.3 (levemente positivo)
- Drivers de satisfação: Exportação detalhada, audit trails
- Detratores: Automação "caixa preta", falta de transparência

**Feedback Positivo Principal:**
- "Exportação em PDF é perfeita para meus relatórios de auditoria"
- "Consigo rastrear cada número até a fonte original"
- "Integração bancária funciona sem erros há 6 meses"

**Pontos de Dor Principais:**
- "Não entendo como o sistema calcula alguns agregados"
- "Prefiro minhas planilhas porque entendo cada fórmula"
- "Faltam opções de validação customizada"

**Avaliação de Adequação:**
- Adequação atual: Média (atende necessidades básicas)
- Potencial de melhoria: Alto (com transparência)
- Risco de churn: Médio (dependem de features específicas)

**Recomendações:**
1. Implementar "modo transparente" com fórmulas visíveis
2. Adicionar validação customizável de regras
3. Criar tutoriais sobre lógica de cálculos

#### Segmento 2: "Gestores Ocupados" (45% dos reviews)

**Perfil do Segmento:**
- Nome: Gestores Ocupados
- Proporção: 45% (450/1000 reviews)
- Contexto: Donos de PME focados em eficiência

**Jobs-to-be-Done:**
- Job principal: "Tomar decisões rápidas com dados confiáveis"
- Outcome desejado: Visão clara da saúde financeira em 5 minutos

**Score de Sentimento:**
- Score geral: +0.7 (bastante positivo)
- Drivers de satisfação: Dashboard simples, alertas úteis, mobile app
- Detratores: Ocasionais lentidão, complexidade excessiva

**Feedback Positivo Principal:**
- "Dashboard me mostra exatamente o que preciso em um olhar"
- "Alertas me salvaram de problemas de caixa várias vezes"
- "App mobile funciona perfeitamente para checar rápido"

**Pontos de Dor Principais:**
- "Às vezes o app demora para carregar dados recentes"
- "Gostaria de mais opções de personalização no dashboard"
- "Notificações poderiam ser mais inteligentes"

**Avaliação de Adequação:**
- Adequação atual: Alta (atende necessidades principais)
- Potencial de melhoria: Médio (otimizações)
- Risco de churn: Baixo (alta satisfação, dependência)

**Recomendações:**
1. Melhorar performance de carregamento
2. Adicionar widgets customizáveis ao dashboard
3. Implementar notificações baseadas em comportamento

#### Segmento 3: "Estudantes Iniciantes" (20% dos reviews)

**Perfil do Segmento:**
- Nome: Estudantes Iniciantes
- Proporção: 20% (200/1000 reviews)
- Contexto: Jovens aprendendo gestão financeira

**Jobs-to-be-Done:**
- Job principal: "Aprender a organizar finanças sem complicação"
- Outcome desejado: Compreensão clara de para onde vai o dinheiro

**Score de Sentimento:**
- Score geral: -0.2 (levemente negativo)
- Drivers de satisfação: Interface amigável, dicas educativas
- Detratores: Curva de aprendizado íngreme, falta de suporte

**Feedback Positivo Principal:**
- "Interface é bonita e fácil de entender no início"
- "Dicas de economia são muito úteis"
- "Gosto dos gráficos coloridos"

**Pontos de Dor Principais:**
- "Não entendo a diferença entre tantos tipos de gráficos"
- "Suporte nunca responde minhas dúvidas"
- "Fica complicado depois de um mês de uso"
- "Precisa de mais tutoriais para iniciantes"

**Avaliação de Adequação:**
- Adequação atual: Baixa (não atende necessidades de aprendizado)
- Potencial de melhoria: Alto (com features educacionais)
- Risco de churn: Alto (abandono após período inicial)

**Recomendações:**
1. Criar "modo aprendizagem" com tutoriais guiados
2. Implementar suporte via chat para iniciantes
3. Simplificar interface para primeiros 30 dias
4. Adicionar conteúdo educacional integrado

## Modelos de Análise

### Análise de App Store
```
Fonte: Reviews iOS/Android
Período: Últimos 3 meses
Volume: 1000+ reviews
Segmentos: Identificados por padrões de uso
Métricas: Score médio, NPS proxy, temas recorrentes
```

### Análise de Pesquisas NPS
```
Fonte: Survey NPS trimestral
Respondentes: 500+ clientes ativos
Segmentação: Por tipo de plano, antiguidade, setor
Análise: Promoters vs Detractors por segmento
Ação: Identificar drivers de churn e expansão
```

### Análise de Tickets de Suporte
```
Fonte: Sistema de tickets (Zendesk, etc.)
Período: Últimos 6 meses
Volume: 2000+ tickets
Categorias: Problemas técnicos, dúvidas, solicitações
Sentimento: Inferido por linguagem e resolução
```

## Benefícios
- **Escalabilidade:** Analisa milhares de feedbacks automaticamente
- **Objetividade:** Scores quantitativos vs. impressões qualitativas
- **Priorização:** Foco nos problemas mais impactantes
- **Segmentação:** Entende diferentes necessidades de grupos

## Dicas de Uso
- Baseie todos os achados em feedback real de usuários
- Identifique perspectivas majoritárias e minoritárias dentro dos segmentos
- Distinga entre solicitações de features e pontos de dor fundamentais
- Considere contexto e restrições que enfrentam os usuários
- Sinalize segmentos com amostras pequenas ou sentimento incerto
- Procure padrões cross-segmentos e pontos de dor universais
- Forneça visão balanceada de forças e fraquezas do produto

## Recursos Adicionais
- [Market Research: Advanced Techniques](https://www.productcompass.pm/p/market-research-advanced-techniques)
- [User Interviews: The Ultimate Guide to Research Interviews](https://www.productcompass.pm/p/interviewing-customers-the-ultimate)
- [Customer Feedback Analysis: The Complete Guide](https://www.productcompass.pm/p/customer-feedback-analysis)
- [Sentiment Analysis: Methods and Tools](https://www.productcompass.pm/p/sentiment-analysis-methods)
