# Memory-First Project Mapping Rule

## Regra Principal

**SEMPRE usar memória (contextplus) como primeira opção para mapear componentes e estrutura do projeto.**

## Fluxo de Trabalho Obrigatório

### 1. Busca na Memória PRIMEIRO

Antes de ler qualquer arquivo, SEMPRE buscar na memória:

```
search_memory_graph → Encontrar componentes e estrutura
```

**Exemplo de uso:**

```
# ✅ CORRETO: Buscar na memória primeiro
search_memory_graph: "classes Database"
search_memory_graph: "funções de autenticação"
search_memory_graph: "componentes React Login"

# ❌ ERRADO: Ler arquivos sem buscar na memória
read_file: backend/app/models/database.py
read_file: backend/app/services/auth_service.py
```

### 2. Mapeamento de Componentes

Usar memória para mapear:

- **Classes e suas localizações** (linha exata)
- **Funções e métodos** (linha exata)
- **Componentes React** (arquivo e linha)
- **Endpoints da API** (arquivo e linha)
- **Configurações** (arquivo e linha)

**Formato de armazenamento:**

```python
# Exemplo de nó de memória para uma classe
{
  "type": "symbol",
  "label": "Database class",
  "content": "Classe Database localizada em backend/app/models/database.py linha 12. Métodos: __init__ (linha 15), execute_query (linha 28), close (linha 35)",
  "metadata": {
    "file_path": "backend/app/models/database.py",
    "class_name": "Database",
    "line_start": "12",
    "methods": "__init__:15, execute_query:28, close:35"
  }
}
```

### 3. Evitar Leitura Desnecessária

**NÃO ler 20 arquivos para encontrar 1 componente:**

```
# ❌ ERRADO: Ler múltiplos arquivos
read_file: backend/app/models/agent.py
read_file: backend/app/models/task.py
read_file: backend/app/models/message.py
read_file: backend/app/services/agent_service.py
read_file: backend/app/services/task_service.py
... (20 arquivos)

# ✅ CORRETO: Buscar na memória e ler apenas o necessário
search_memory_graph: "Agent class"
# Memória retorna: "Agent class em backend/app/models/agent.py linha 31"
read_file: backend/app/models/agent.py  # Lê apenas o arquivo necessário
```

### 4. Atualização de Memória

**SEMPRE atualizar memória após modificações:**

```
# Após modificar código
upsert_memory_node: Atualizar nó com novas informações
```

**Exemplo:**

```python
# Após adicionar método à classe Database
upsert_memory_node({
  "type": "symbol",
  "label": "Database class",
  "content": "Classe Database em backend/app/models/database.py linha 12. Métodos: __init__ (linha 15), execute_query (linha 28), close (linha 35), get_stats (linha 42)",  # Novo método adicionado
  "metadata": {
    "file_path": "backend/app/models/database.py",
    "class_name": "Database",
    "line_start": "12",
    "methods": "__init__:15, execute_query:28, close:35, get_stats:42"  # Atualizado
  }
})
```

### 5. Persistir Aprendizados

**SEMPRE criar nós de memória para:**

- Decisões arquiteturais
- Padrões de código descobertos
- Relacionamentos entre componentes
- Configurações importantes
- Bugs e soluções encontradas

## Benefícios

1. **Eficiência**: Não lê 20 arquivos para encontrar 1
2. **Velocidade**: Memória é mais rápida que leitura de arquivos
3. **Precisão**: Linhas exatas de classes e funções
4. **Contexto**: Mantém histórico de decisões
5. **Aprendizado**: Acumula conhecimento do projeto

## Integração com MCP

O MCP (contextplus) já retorna linhas exatas de código:

- `get_context_tree`: Retorna árvore com linhas de funções/classes
- `semantic_code_search`: Retorna arquivos com linhas de definição
- `semantic_identifier_search`: Retorna identificadores com linhas

**A memória COMPLEMENTA essas ferramentas:**

- MCP retorna estrutura atual
- Memória mantém histórico e contexto
- Juntos evitam leitura desnecessária

## Padrão de Metadados Estruturados (Obrigatório)

### Schema Base para TODAS as Memórias

```javascript
{
  "type": "concept|file|symbol|note",
  "label": "Nome Descritivo",
  "content": "Conteúdo detalhado (mínimo 3-5 linhas)...",
  "metadata": {
    // CAMPOS OBRIGATÓRIOS
    "created_at": "2026-03-29T17:00:00",  // ISO 8601
    "category": "architecture|implementation|config|decision|reference",
    "subcategory": "adr|model|service|tool|api|frontend|backend|database",
    "importance": "high|medium|low",
    "status": "active|deprecated|draft",
    "tags": "tag1,tag2,tag3",  // Separadas por vírgula (NÃO array)
    
    // CAMPOS OPCIONAIS POR CATEGORIA
    "adr_number": "0014",           // Para ADRs
    "file_path": "backend/...",     // Para files/symbols
    "line_start": "28",             // Para symbols
    "line_end": "57",               // Para symbols
    "methods": "m1,m2,m3",          // Para classes (string separada por vírgula)
    "dependencies": "dep1,dep2",    // Dependências (string separada por vírgula)
    "related_files": "file1,file2", // Arquivos relacionados
    
    // CAMPOS DE RASTREAMENTO
    "source": "user|ai|migration",
    "version": "1.0",
    "last_verified": "2026-03-29"
  }
}
```

### Regras Obrigatórias

1. **NUNCA criar nós sem metadata estruturada**
2. **Content mínimo de 3-5 linhas descritivas**
3. **Mínimo 2-3 tags por memória** (separadas por vírgula)
4. **Timestamps sempre presentes** (created_at, last_verified)
5. **Categorização clara** (category + subcategory)
6. **IMPORTANTE: Metadata aceita APENAS strings** - converter arrays para string separada por vírgulas

### Categorias de Memória

| Categoria | Subcategoria | Exemplo | Campos Específicos |
|-----------|--------------|---------|-------------------|
| `architecture` | `adr` | ADR-0014 | adr_number, status, decision_date |
| `architecture` | `pattern` | Design Patterns | pattern_type, use_cases |
| `implementation` | `model` | Agent Model | file_path, fields, relationships |
| `implementation` | `service` | AgentService | file_path, methods, dependencies |
| `implementation` | `tool` | MemorySearchTool | file_path, parameters, return_type |
| `config` | `database` | PostgreSQL | config_file, env_vars, defaults |
| `config` | `api` | FastAPI Endpoints | routes, middleware |
| `decision` | `technical` | Tech Choice | alternatives, rationale |
| `reference` | `documentation` | ADR Index | doc_path, sections |

### Exemplo de Memória Bem Formatada

```javascript
upsert_memory_node({
  "type": "symbol",
  "label": "AgentService",
  "content": "Serviço de lógica de negócio para agentes. Gerencia CRUD completo com validação de status e capabilities. Implementa padrão Repository com AsyncSession do SQLAlchemy. Métodos: create_agent(), get_agent(), update_agent(), delete_agent(), list_agents().",
  "metadata": {
    "created_at": "2026-03-29T17:09:45",
    "category": "implementation",
    "subcategory": "service",
    "importance": "high",
    "status": "active",
    "file_path": "backend/app/services/agent_service.py",
    "line_start": "12",
    "line_end": "145",
    "methods": "create_agent,get_agent,update_agent,delete_agent,list_agents",
    "dependencies": "AsyncSession,Agent Model,DatabaseService",
    "tags": "service,agents,crud,async,sqlalchemy",
    "source": "ai",
    "version": "2.0",
    "last_verified": "2026-03-29"
  }
})
```

## Exemplo Prático de Fluxo

```markdown
# Tarefa: Encontrar e modificar classe UserAuth

## Passo 1: Buscar na memória
search_memory_graph: "UserAuth class"
# Resultado: "UserAuth class em backend/app/models/user.py linha 45"

## Passo 2: Ler apenas o arquivo necessário
read_file: backend/app/models/user.py
# Lê apenas o arquivo onde UserAuth está

## Passo 3: Modificar código
replace_in_file: Adicionar método à classe UserAuth

## Passo 4: Atualizar memória
upsert_memory_node: Atualizar nó UserAuth com novo método

## Resultado
- ✅ Encontrou classe rapidamente
- ✅ Leu apenas 1 arquivo (não 20)
- ✅ Memória atualizada para próximas buscas
```

## Regras de Validação

### Obrigatório

- [ ] Buscar na memória antes de ler arquivos
- [ ] Atualizar memória após modificações
- [ ] Usar formato padrão para nós de memória
- [ ] Incluir linhas exatas em metadados

### Opcional

- [ ] Criar relações entre nós de memória
- [ ] Adicionar tags para categorização
- [ ] Manter histórico de acessos

## Exceções

**Quando NÃO usar memória:**

1. Arquivo nunca visto antes (primeira leitura)
2. Busca por conteúdo específico (não por componente)
3. Análise de código completo (não apenas estrutura)

**Nesses casos:**

- Ler arquivo diretamente
- Criar nó de memória após leitura
- Próxima busca usará memória

## Conclusão

**Memória primeiro, leitura depois.**

A memória é o mapa do projeto. Use-a para navegar rapidamente e ler apenas o necessário. Evite leitura desnecessária de múltiplos arquivos quando a memória já tem a resposta.
