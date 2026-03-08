# Gerador de Queries SQL

## Propósito
Transformar requisitos em linguagem natural em queries SQL otimizadas para múltiplos bancos de dados. Ajuda Product Managers, analistas e engenheiros a gerar queries precisas sem trabalho manual de sintaxe.

## Como Funciona
O processo segue quatro etapas principais: entender o schema do banco (ler arquivos ou diagramas), processar o requisito (clarificar dados necessários e dialeto SQL), gerar query otimizada (com comentários e considerações de performance), e explicar/testar (explicar lógica e sugerir validação).

## Quando Usar
- Análise de dados de produtos e usuários
- Criação de dashboards e relatórios
- Extração de insights para decisões de produto
- Testes de hipóteses com dados reais
- Geração de datasets para apresentações
- Otimização de queries existentes

## Passo a Passo

### 1. Entendimento do Schema do Banco
**Opções de Input:**
- Arquivo de schema SQL
- Documentação do banco
- Descrição de diagrama
- Lista de tabelas e colunas

**Extração Automática:**
- Nomes de tabelas e colunas
- Tipos de dados e relacionamentos
- Chaves primárias e estrangeiras
- Estratégias de indexação

### 2. Processamento do Requisito
**Clarificar:**
- Dados exatos necessários
- Filtros e agregações requeridas
- Dialeto SQL (BigQuery, PostgreSQL, MySQL, etc.)
- Requisitos adicionais (performance, volume)

**Exemplos de Requisitos:**
- "Usuários que se cadastraram nos últimos 30 dias com pelo menos 5 sessões ativas"
- "Receita por região e tier de cliente com crescimento YoY"
- "Taxa de conversão por canal de marketing Q1 2026"

### 3. Geração de Query Otimizada
**Elementos Incluídos:**
- Sintaxe correta para o dialeto especificado
- Comentários explicando lógica complexa
- Considerações de performance para grandes datasets
- Abordagens alternativas se aplicável
- Boas práticas de SQL

### 4. Explicação e Validação
**Explicação:**
- Lógica da query em linguagem simples
- Como cada parte funciona
- Por que certas escolhas foram feitas

**Validação:**
- Como testar resultados
- Verificações de sanidade
- Sugestões de otimização

## Exemplos Práticos

### Exemplo 1: Query a partir de Schema
**Input:** Arquivo schema.sql + "Encontrar usuários cadastrados últimos 30 dias com 5+ sessões ativas"

**Resultado:**
```sql
-- Query para encontrar usuários recentes engajados
-- Filtra usuários criados nos últimos 30 dias com 5+ sessões
SELECT 
    u.user_id,
    u.email,
    u.created_at,
    COUNT(s.session_id) as session_count,
    MAX(s.created_at) as last_session
FROM users u
LEFT JOIN sessions s ON u.user_id = s.user_id
WHERE u.created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
    AND s.created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY u.user_id, u.email, u.created_at
HAVING COUNT(s.session_id) >= 5
ORDER BY session_count DESC, last_session DESC;

-- Performance: Considerar índice em (user_id, created_at) na tabela sessions
```

### Exemplo 2: Análise Complexa
**Requisito:** "Análise de receita por região e tier com crescimento YoY"

**Resultado BigQuery:**
```sql
-- Análise de receita com crescimento ano sobre ano
-- Particionado por região e tier de cliente
WITH 
monthly_revenue AS (
    SELECT
        DATE_TRUNC(order_date, MONTH) as month,
        region,
        customer_tier,
        SUM(order_value) as revenue,
        COUNT(DISTINCT customer_id) as customer_count
    FROM orders
    WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 25 MONTH)
    GROUP BY 1,2,3
),

year_over_year AS (
    SELECT
        month,
        region,
        customer_tier,
        revenue,
        customer_count,
        LAG(revenue, 12) OVER (PARTITION BY region, customer_tier ORDER BY month) as revenue_prev_year,
        LAG(customer_count, 12) OVER (PARTITION BY region, customer_tier ORDER BY month) as customers_prev_year
    FROM monthly_revenue
)

SELECT
    FORMAT_DATE('%Y-%m', month) as month_formatted,
    region,
    customer_tier,
    revenue,
    customer_count,
    revenue_prev_year,
    SAFE_DIVIDE(revenue - revenue_prev_year, revenue_prev_year) * 100 as revenue_growth_pct,
    SAFE_DIVIDE(customer_count - customers_prev_year, customers_prev_year) * 100 as customer_growth_pct
FROM year_over_year
WHERE revenue_prev_year IS NOT NULL
ORDER BY region, customer_tier, month DESC;

-- Nota: Usar SAFE_DIVIDE para evitar divisão por zero
-- Considerar materializar esta view para dashboards
```

## Benefícios

- **Produtividade:** Gera queries complexas rapidamente
- **Precisão:** Evita erros de sintaxe e lógica
- **Performance:** Inclui otimizações e melhores práticas
- **Aprendizado:** Explicações ajudam a entender SQL
- **Flexibilidade:** Suporta múltiplos dialetos e casos de uso

## Dicas de Uso

### Para Melhores Resultados:
1. **Forneça Contexto:** Compartilhe schema ou estrutura do banco
2. **Seja Específico:** Descreva claramente os dados necessários
3. **Mencione o Banco:** Especifique qual dialeto SQL usar
4. **Inclua Restrições:** Volume de dados, time ranges, necessidades de performance
5. **Solicite Formato:** Peça formato específico de output se necessário

### Boas Práticas:
- Testar queries em ambiente de desenvolvimento primeiro
- Verificar volumes de dados antes de rodar em produção
- Usar LIMIT para testes iniciais
- Considerar partições e índices para performance

## Formatos de Saída

### Query Otimizada
- Sintaxe correta para o dialeto
- Comentários explicativos
- Formatação limpa e legível

### Explicação Detalhada
- O que a query faz
- Como funciona cada parte
- Por que certas escolhas foram feitas

### Considerações de Performance
- Índices recomendados
- Otimizações para grandes volumes
- Alternativas se necessário

### Script de Teste (se solicitado)
- Dados de exemplo
- Queries de validação
- Verificações de sanidade

## Recursos Adicionais

- **Documentação:** [BigQuery SQL Reference](https://cloud.google.com/bigquery/docs/reference/standard-sql)
- **Performance:** [SQL Optimization Guide](https://www.cockroachlabs.com/blog/sql-performance-tuning/)
- **Analytics:** [Product Analytics Playbook](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
- **Learning:** [How to Become Technology-Literate PM](https://www.productcompass.pm/p/how-to-become-technology-literate)

---

**Exemplos de Uso Comum:**

**Análise de Retenção:**
```sql
-- Cohort analysis para retenção mensal
WITH user_cohorts AS (
    SELECT 
        user_id,
        DATE_TRUNC(created_at, MONTH) as cohort_month
    FROM users
    WHERE created_at >= '2025-01-01'
),

monthly_activity AS (
    SELECT 
        u.user_id,
        c.cohort_month,
        DATE_TRUNC(s.created_at, MONTH) as activity_month
    FROM user_cohorts u
    JOIN sessions s ON u.user_id = s.user_id
    WHERE s.created_at >= '2025-01-01'
)

SELECT
    cohort_month,
    activity_month,
    COUNT(DISTINCT u.user_id) as cohort_size,
    COUNT(DISTINCT a.user_id) as active_users,
    COUNT(DISTINCT a.user_id) * 100.0 / COUNT(DISTINCT u.user_id) as retention_rate
FROM user_cohorts u
LEFT JOIN monthly_activity a ON u.user_id = a.user_id
GROUP BY 1,2
ORDER BY cohort_month, activity_month;
```

**Funil de Conversão:**
```sql
-- Análise de funil por etapa
SELECT
    funnel_step,
    COUNT(DISTINCT user_id) as users,
    COUNT(DISTINCT user_id) * 100.0 / LAG(COUNT(DISTINCT user_id)) OVER (ORDER BY step_order) as conversion_rate
FROM (
    SELECT 
        user_id,
        'Visit' as funnel_step,
        1 as step_order
    FROM page_views
    WHERE page_url = '/landing'
    
    UNION ALL
    
    SELECT 
        user_id,
        'Signup' as funnel_step,
        2 as step_order
    FROM users
    WHERE created_at >= '2025-01-01'
    
    UNION ALL
    
    SELECT 
        user_id,
        'First Purchase' as funnel_step,
        3 as step_order
    FROM orders
    WHERE order_date >= '2025-01-01'
) funnel_steps
GROUP BY funnel_step, step_order
ORDER BY step_order;
```

**Próximos Passos:**
- Testar queries em ambiente seguro
- Validar resultados com esperado
- Implementar em dashboards
- Documentar para equipe
- Agendar execuções regulares se necessário
