# 0004. Use PostgreSQL and KuzuDB

Data: 2026-01-18

Status: Aceito

## Contexto

O sistema Plexo precisa armazenar diferentes tipos de dados com requisitos distintos:

- **Dados Relacionais**: Agentes, tarefas, mensagens, usuários (estrutura tabular)
- **Dados de Grafo**: Relacionamentos entre agentes, dependências de tarefas, redes de conhecimento
- **Embeddings Vetoriais**: Representações vetoriais para busca semântica e RAG
- **Histórico e Auditoria**: Logs de execução, métricas, eventos

Precisávamos escolher uma estratégia de armazenamento que suportasse todos esses casos de uso de forma eficiente.

## Decisão

Decidimos usar **PostgreSQL** como banco de dados relacional principal e **KuzuDB** como banco de dados de grafos embarcado.

### Razões

**PostgreSQL:**

1. **ACID Compliant**: Transações confiáveis e consistência de dados
2. **Maturidade**: Banco de dados maduro com 30+ anos de desenvolvimento
3. **JSON Support**: Suporte nativo a JSON/JSONB para dados semi-estruturados
4. **Extensões**: pgvector para embeddings, pg_trgm para busca textual
5. **Performance**: Excelente performance para queries relacionais
6. **Ferramentas**: Ecossistema rico (Alembic, SQLAlchemy, pgAdmin)
7. **Escalabilidade**: Suporte a replicação e sharding

**KuzuDB:**

1. **Graph Native**: Otimizado para queries de grafos (relacionamentos complexos)
2. **Embarcado**: Não requer servidor separado, roda in-process
3. **Cypher-like**: Linguagem de query similar ao Neo4j
4. **Vector Embeddings**: Suporte nativo a embeddings vetoriais
5. **Performance**: Muito rápido para traversals de grafos
6. **Leve**: Footprint pequeno, ideal para desenvolvimento local
7. **Open Source**: Licença MIT, sem custos de licenciamento

## Consequências

### Positivas

- **Separação de Responsabilidades**: Cada banco otimizado para seu caso de uso
- **PostgreSQL**: Dados relacionais, transações ACID, integridade referencial
- **KuzuDB**: Queries de grafos rápidas, análise de relacionamentos, embeddings
- **Desenvolvimento Local**: KuzuDB embarcado facilita setup local
- **Flexibilidade**: Podemos usar o melhor de cada mundo
- **Custo**: KuzuDB é gratuito e não requer infraestrutura adicional
- **Backup**: PostgreSQL tem ferramentas maduras de backup e restore

### Negativas

- **Complexidade**: Gerenciar dois bancos de dados diferentes
- **Sincronização**: Dados podem precisar ser replicados entre os dois bancos
- **Consistência**: Garantir consistência entre PostgreSQL e KuzuDB
- **Curva de Aprendizado**: Equipe precisa aprender duas tecnologias
- **Deployment**: Mais componentes para gerenciar em produção
- **Debugging**: Mais complexo debugar problemas que envolvem ambos os bancos

## Alternativas Consideradas

### PostgreSQL + pgvector (Apenas PostgreSQL)

- **Prós**: Um único banco, mais simples, pgvector para embeddings
- **Contras**: Queries de grafos são lentas, não otimizado para traversals
- **Rejeitado**: Performance ruim para análise de relacionamentos complexos

### Neo4j

- **Prós**: Graph database maduro, Cypher nativo, ferramentas ricas
- **Contras**: Custo de licenciamento, requer servidor separado, mais pesado
- **Rejeitado**: Overhead de infraestrutura e custo para desenvolvimento

### MongoDB

- **Prós**: Flexível, JSON nativo, fácil de usar
- **Contras**: Não é ACID por padrão, não otimizado para grafos
- **Rejeitado**: Preferimos ACID para dados críticos

### DGraph

- **Prós**: Graph database distribuído, GraphQL nativo
- **Contras**: Comunidade menor, menos maduro que Neo4j
- **Rejeitado**: KuzuDB é mais leve e suficiente para nosso caso

### Apenas KuzuDB

- **Prós**: Um único banco, otimizado para grafos
- **Contras**: Menos maduro para dados relacionais, ferramentas limitadas
- **Rejeitado**: PostgreSQL é melhor para dados relacionais tradicionais

## Implementação

### Estrutura de Dados

**PostgreSQL (Dados Relacionais):**

```sql
-- Agentes
CREATE TABLE agents (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    config JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tarefas
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    agent_id UUID REFERENCES agents(id),
    title VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    priority INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**KuzuDB (Grafo de Conhecimento):**

```python
# Criar schema de grafo
conn.execute("""
    CREATE NODE TABLE Agent(
        id STRING,
        name STRING,
        embedding FLOAT[1536],
        PRIMARY KEY(id)
    )
""")

conn.execute("""
    CREATE REL TABLE COMMUNICATES_WITH(
        FROM Agent TO Agent,
        message_count INT64,
        last_interaction TIMESTAMP
    )
""")

# Query de grafo
result = conn.execute("""
    MATCH (a:Agent)-[r:COMMUNICATES_WITH*1..3]->(b:Agent)
    WHERE a.id = $agent_id
    RETURN b.name, COUNT(r) as path_length
    ORDER BY path_length
""")
```

### Sincronização

Usaremos eventos de domínio para manter sincronização:

```python
class AgentCreatedEvent:
    async def handle(self):
        # Salvar no PostgreSQL
        await db.agents.create(self.agent)
        
        # Criar nó no KuzuDB
        await kuzu.execute("""
            CREATE (a:Agent {
                id: $id,
                name: $name,
                embedding: $embedding
            })
        """, self.agent)
```

### Casos de Uso

**PostgreSQL:**

- CRUD de agentes, tarefas, mensagens
- Queries relacionais (JOIN, GROUP BY)
- Transações ACID
- Histórico e auditoria

**KuzuDB:**

- Análise de relacionamentos entre agentes
- Busca semântica com embeddings
- Recomendações baseadas em grafos
- Análise de dependências de tarefas

## Referências

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [KuzuDB Documentation](https://kuzudb.com/)
- [pgvector Extension](https://github.com/pgvector/pgvector)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
