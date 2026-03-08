# SQL Queries

## Propósito
Gerar SQL queries de descrições em linguagem natural. Suporta BigQuery, PostgreSQL, MySQL e outros dialetos. Lê schemas de banco de dados de diagramas ou documentação uploaded. Usado ao escrever SQL, construir relatórios de dados, explorar bancos de dados ou traduzir perguntas de negócio em queries.

## Como Funciona
Transforma requisitos de linguagem natural em queries SQL otimizadas através de múltiplas plataformas de banco de dados. Ajuda product managers, analistas e engenheiros a gerar queries precisas sem trabalho manual de sintaxe.

## Quando Usar
- Análise de dados para decisões de produto
- Criação de relatórios e dashboards
- Exploração de padrões em dados
- Validação de hipóteses com dados
- Extração de insights de bancos de dados

## Como Funciona

### Passo 1: Entender Schema do Banco de Dados
- Se você fornecer arquivo de schema (SQL, documentação ou descrição de diagrama), vou ler e analisar
- Extrair nomes de tabelas, definições de colunas, tipos de dados e relacionamentos
- Identificar chaves primárias, chaves estrangeiras e estratégias de indexação

### Passo 2: Processar Sua Requisição
- Clarificar os dados exatos que você precisa recuperar ou analisar
- Confirmar o dialeto SQL (BigQuery, PostgreSQL, MySQL, Snowflake, etc.)
- Pedir requisitos adicionais (filtros, agregações, ordenação)

### Passo 3: Gerar Query Otimizada
- Escrever SQL eficiente que aproveita sua estrutura de banco de dados
- Incluir comentários explicando lógica complexa
- Adicionar considerações de performance para grandes datasets
- Fornecer abordagens alternativas se aplicável

### Passo 4: Explicar e Testar
- Explicar lógica da query em inglês simples
- Sugerir como testar ou validar resultados
- Oferecer dicas para otimização de performance
- Se quiser, gerar script de teste ou dados amostrais

## Exemplos de Uso

### Exemplo 1: Query de Arquivo Schema
```
Upload seu arquivo database_schema.sql e diga:
"Gerar query para encontrar usuários que se inscreveram nos últimos 30 dias
e tiveram pelo menos 5 sessões ativas"
```

### Exemplo 2: Query de Descrição de Diagrama
```
"Aqui está meu banco: tabela Users (id, email, created_at), tabela Sessions
(id, user_id, timestamp, duration). Gerar query para duração média de sessão
por usuário em janeiro de 2026."
```

### Exemplo 3: Query de Análise Complexa
```
"Criar query BigQuery para analisar nossa receita por região e tier de cliente,
incluindo taxas de crescimento ano a ano."
```

## Capacidades Chave

- **Suporte Multi-Dialeto:** Funciona com BigQuery, PostgreSQL, MySQL, Snowflake, SQL Server
- **Leitura de Arquivos:** Lê arquivos de schema, dumps SQL e documentação de dados
- **Otimização de Query:** Sugere indexes, partitioning e melhorias de performance
- **Explicação:** Detalha queries para aprendizado e documentação
- **Teste:** Pode gerar queries de teste e scripts de dados amostrais
- **Execução de Script:** Criar scripts SQL executáveis para seu banco de dados

## Exemplo Prático

### SQL Queries: FinanControl Analytics

### Passo 1: Schema do Banco de Dados

```
-- Estrutura principal
users (id, email, created_at, company_id, plan_id)
companies (id, name, size, industry, created_at)
plans (id, name, price, features)
sessions (id, user_id, timestamp, duration, actions_count)
transactions (id, user_id, amount, type, timestamp, bank_id)
reports (id, user_id, type, generated_at, views_count)
support_tickets (id, user_id, created_at, status, category)
```

### Passo 2: Requisições de Análise

#### Query 1: Engajamento de Usuários por Plano
```
"Analisar engajamento médio de usuários por tipo de plano nos últimos 90 dias.
Incluir duração média de sessão, ações por sessão e relatórios gerados."
```

#### Query 2: Retenção por Cohort
```
"Calcular taxa de retenção de usuários por cohort de inscrição mensal.
Mostrar retenção nos dias 7, 30, 60, 90."
```

#### Query 3: Análise de Receita
```
"Analisar receita mensal por plano, região e tamanho de empresa.
Incluir crescimento mês a mês e previsão para próximos 3 meses."
```

### Passo 3: Queries Otimizadas

#### Query 1: Engajamento por Plano (PostgreSQL)

```sql
-- Análise de engajamento de usuários por plano (últimos 90 dias)
WITH user_sessions AS (
    SELECT 
        u.id as user_id,
        u.email,
        p.name as plan_name,
        p.price as plan_price,
        COUNT(s.id) as session_count,
        AVG(s.duration) as avg_session_duration,
        SUM(s.actions_count) as total_actions,
        COUNT(DISTINCT DATE(s.timestamp)) as active_days
    FROM users u
    JOIN plans p ON u.plan_id = p.id
    LEFT JOIN sessions s ON u.id = s.user_id 
        AND s.timestamp >= CURRENT_DATE - INTERVAL '90 days'
    WHERE u.created_at <= CURRENT_DATE - INTERVAL '7 days' -- Excluir usuários muito novos
    GROUP BY u.id, u.email, p.name, p.price
),
user_reports AS (
    SELECT 
        user_id,
        COUNT(id) as reports_generated
    FROM reports
    WHERE generated_at >= CURRENT_DATE - INTERVAL '90 days'
    GROUP BY user_id
)
SELECT 
    plan_name,
    plan_price,
    COUNT(*) as total_users,
    AVG(session_count) as avg_sessions_per_user,
    AVG(avg_session_duration) as avg_duration_minutes,
    AVG(total_actions) as avg_actions_per_user,
    AVG(active_days) as avg_active_days,
    AVG(COALESCE(ur.reports_generated, 0)) as avg_reports_per_user
FROM user_sessions us
LEFT JOIN user_reports ur ON us.user_id = ur.user_id
GROUP BY plan_name, plan_price
ORDER BY plan_price DESC;

-- Performance Notes:
-- Índice recomendado: sessions(timestamp, user_id)
-- Índice recomendado: reports(generated_at, user_id)
-- Partition por mês para grandes datasets
```

#### Query 2: Retenção por Cohort (BigQuery)

```sql
-- Retenção de usuários por cohort de inscrição mensal
WITH user_cohorts AS (
    SELECT 
        user_id,
        DATE_TRUNC(created_at, MONTH) as cohort_month,
        EXTRACT(DAY FROM CURRENT_DATE - created_at) as days_since_signup
    FROM users
    WHERE created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
),
retention_data AS (
    SELECT 
        uc.cohort_month,
        uc.days_since_signup,
        COUNT(DISTINCT CASE WHEN uc.days_since_signup >= 7 THEN uc.user_id END) as day_7_users,
        COUNT(DISTINCT CASE WHEN uc.days_since_signup >= 30 THEN uc.user_id END) as day_30_users,
        COUNT(DISTINCT CASE WHEN uc.days_since_signup >= 60 THEN uc.user_id END) as day_60_users,
        COUNT(DISTINCT CASE WHEN uc.days_since_signup >= 90 THEN uc.user_id END) as day_90_users,
        COUNT(DISTINCT uc.user_id) as cohort_size
    FROM user_cohorts uc
    GROUP BY uc.cohort_month
)
SELECT 
    cohort_month,
    cohort_size,
    ROUND(day_7_users * 100.0 / cohort_size, 2) as day_7_retention_pct,
    ROUND(day_30_users * 100.0 / cohort_size, 2) as day_30_retention_pct,
    ROUND(day_60_users * 100.0 / cohort_size, 2) as day_60_retention_pct,
    ROUND(day_90_users * 100.0 / cohort_size, 2) as day_90_retention_pct
FROM retention_data
ORDER BY cohort_month DESC;

-- Performance Notes:
-- Cluster by cohort_month para melhor performance
-- Usar DATE_TRUNC para otimizar comparações de datas
-- Considerar materializar cohorts para queries frequentes
```

#### Query 3: Análise de Receita (MySQL)

```sql
-- Análise de receita mensal por plano e segmento
WITH monthly_revenue AS (
    SELECT 
        DATE_FORMAT(t.timestamp, '%Y-%m-01') as month,
        p.name as plan_name,
        c.size as company_size,
        c.industry as industry,
        SUM(t.amount) as revenue,
        COUNT(DISTINCT t.user_id) as paying_users,
        AVG(t.amount) as avg_transaction_value
    FROM transactions t
    JOIN users u ON t.user_id = u.id
    JOIN plans p ON u.plan_id = p.id
    JOIN companies c ON u.company_id = c.id
    WHERE t.type = 'subscription'
        AND t.timestamp >= DATE_SUB(CURRENT_DATE, INTERVAL 24 MONTH)
    GROUP BY month, plan_name, company_size, industry
),
revenue_growth AS (
    SELECT 
        month,
        plan_name,
        company_size,
        revenue,
        paying_users,
        LAG(revenue) OVER (PARTITION BY plan_name, company_size ORDER BY month) as prev_month_revenue,
        ROUND((revenue - LAG(revenue) OVER (PARTITION BY plan_name, company_size ORDER BY month)) * 100.0 / 
             LAG(revenue) OVER (PARTITION BY plan_name, company_size ORDER BY month), 2) as revenue_growth_pct
    FROM monthly_revenue
)
SELECT 
    month,
    plan_name,
    company_size,
    revenue,
    paying_users,
    avg_transaction_value,
    revenue_growth_pct,
    -- Previsão simples baseada em tendência de 3 meses
    ROUND(revenue * (1 + AVG(revenue_growth_pct) OVER (
        PARTITION BY plan_name, company_size 
        ORDER BY month 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) / 100), 2) as projected_revenue_next_month
FROM revenue_growth
ORDER BY month DESC, plan_name, company_size;

-- Performance Notes:
-- Índice composto: transactions(timestamp, type, user_id)
-- Índice composto: users(plan_id, company_id)
-- Considerar particionar por ano para dados históricos
```

## Modelos de Queries por Tipo

### Queries de Funil
```sql
-- Funil de conversão de onboarding
SELECT 
    step,
    COUNT(DISTINCT user_id) as users,
    LAG(COUNT(DISTINCT user_id)) OVER (ORDER BY step) as previous_step_users,
    ROUND(COUNT(DISTINCT user_id) * 100.0 / 
         LAG(COUNT(DISTINCT user_id)) OVER (ORDER BY step), 2) as conversion_rate
FROM (
    SELECT 
        user_id,
        'signup' as step,
        MIN(created_at) as event_time
    FROM users
    GROUP BY user_id
    
    UNION ALL
    
    SELECT 
        user_id,
        'bank_connected' as step,
        MIN(timestamp) as event_time
    FROM transactions
    WHERE type = 'bank_link'
    GROUP BY user_id
    
    UNION ALL
    
    SELECT 
        user_id,
        'first_report' as step,
        MIN(generated_at) as event_time
    FROM reports
    GROUP BY user_id
) events
GROUP BY step
ORDER BY step;
```

### Queries de Cohort
```sql
-- Análise de comportamento por cohort
WITH user_behavior AS (
    SELECT 
        u.id as user_id,
        DATE_TRUNC(u.created_at, MONTH) as cohort,
        DATE_TRUNC(s.timestamp, MONTH) as activity_month,
        EXTRACT(MONTH FROM AGE(s.timestamp, u.created_at)) as months_since_signup,
        COUNT(s.id) as sessions_count
    FROM users u
    LEFT JOIN sessions s ON u.id = s.user_id
    WHERE u.created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
    GROUP BY u.id, cohort, activity_month, months_since_signup
)
SELECT 
    cohort,
    months_since_signup,
    AVG(sessions_count) as avg_sessions_per_user,
    COUNT(DISTINCT user_id) as active_users
FROM user_behavior
GROUP BY cohort, months_since_signup
ORDER BY cohort, months_since_signup;
```

## Dicas para Melhores Resultados

1. **Forneça Contexto:** Compartilhe schema ou estrutura do banco de dados
2. **Seja Específico:** Descreva claramente quais dados você precisa e filtros
3. **Mencione Banco:** Especifique qual dialeto SQL você está usando
4. **Inclua Restrições:** Mencione volume de dados, ranges de tempo e necessidades de performance
5. **Peça Formato:** Peça formato de resultado da query se precisar de output específico

## Formato de Saída

Você receberá:
- **Query SQL:** Código SQL pronto para produção com comentários
- **Explicação:** O que a query faz e como funciona
- **Notas de Performance:** Dicas de otimização e considerações
- **Script de Teste** (se solicitado): Dados amostrais e queries de validação

## Benefícios
- **Eficiência:** Gera queries complexas sem trabalho manual
- **Precisão:** Sintaxe otimizada para dialetos específicos
- **Aprendizado:** Explicações ajudam a entender SQL
- **Performance:** Queries otimizadas para grandes datasets

## Recursos Adicionais
- [The Product Analytics Playbook: AARRR, HEART, Cohorts & Funnels for PMs](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
- [How to Become a Technology-Literate PM](https://www.productcompass.pm/p/how-to-become-a-technology-literate)
- [SQL for Product Managers: Complete Guide](https://www.productcompass.pm/p/sql-for-product-managers)
- [Database Optimization Best Practices](https://www.productcompass.pm/p/database-optimization-guide)
