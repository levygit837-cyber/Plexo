# Guia Completo GitNexus

## Propósito
Referência completa de ferramentas e recursos GitNexus, incluindo skills, ferramentas MCP, recursos de conhecimento e schema do grafo. Serve como guia rápido para todas as funcionalidades disponíveis.

## Como Funciona
GitNexus é um sistema de conhecimento de código que constrói um grafo de relacionamentos entre símbolos de código (funções, classes, etc.) e permite consultas inteligentes para entender, depurar e refatorar código.

## Quando Usar
- Como ponto de partida para qualquer tarefa GitNexus
- Para descobrir quais skills estão disponíveis
- Para entender o schema do grafo de conhecimento
- Para referência rápida de comandos e recursos
- Para troubleshooting e best practices

## Skills Disponíveis

| Tarefa | Skill para Ler | Descrição |
|--------|----------------|-----------|
| Entender arquitetura / "Como X funciona?" | `gitnexus-exploring` | Exploração de codebases desconhecidos |
| Análise de impacto / "O que quebra se mudar X?" | `gitnexus-impact-analysis` | Análise de blast radius de mudanças |
| Debugging / "Por que X está falhando?" | `gitnexus-debugging` | Rastreamento de bugs e erros |
| Refactoring / Renomear, extrair, dividir | `gitnexus-refactoring` | Operações seguras de refactoring |
| Ferramentas, recursos, schema | `gitnexus-guide` (este arquivo) | Referência completa |
| CLI commands / Index, status, clean | `gitnexus-cli` | Comandos de linha de comando |

## Workflow Recomendado

### Para Qualquer Tarefa GitNexus
1. **Ler `gitnexus://repo/{name}/context`** - Overview do codebase + verificar frescura do índice
2. **Escolher skill apropriada** - Ler arquivo da skill correspondente
3. **Seguir workflow e checklist** - Executar passos recomendados

> Se o passo 1 avisar que o índice está desatualizado, rode `npx gitnexus analyze` no terminal primeiro.

## Ferramentas MCP Reference

### query - Busca de Inteligência de Código
**O que oferece:** Processos agrupados de inteligência de código — execution flows relacionados a um conceito

**Uso típico:**
```bash
gitnexus_query({query: "payment processing"})
→ Processes: CheckoutFlow, RefundFlow, WebhookHandler
→ Symbols grouped by flow with file locations
```

**Quando usar:**
- Encontrar código relacionado a conceito específico
- Descobrir execution flows para funcionalidade
- Mapear código por domínio de negócio

### context - Visão 360 Graus de Símbolo
**O que oferece:** Visão completa de símbolo — refs categorizadas, processos que participa

**Uso típico:**
```bash
gitnexus_context({name: "validateUser"})
→ Incoming calls: loginHandler, apiMiddleware
→ Outgoing calls: checkToken, getUserById  
→ Processes: LoginFlow (step 2/5), TokenRefresh (step 1/3)
```

**Quando usar:**
- Entender dependências de função/classe específica
- Verificar quem chama e o que um símbolo chama
- Identificar processos que usam o símbolo

### impact - Análise de Blast Radius
**O que oferece:** Impacto de símbolo — o que quebra em profundidade 1/2/3 com confiança

**Uso típico:**
```bash
gitnexus_impact({
  target: "validateUser", 
  direction: "upstream",
  minConfidence: 0.8,
  maxDepth: 3
})

→ d=1 (WILL BREAK):
  - loginHandler (src/auth/login.ts:42) [CALLS, 100%]
  - apiMiddleware (src/api/middleware.ts:15) [CALLS, 100%]

→ d=2 (LIKELY AFFECTED):
  - authRouter (src/routes/auth.ts:22) [CALLS, 95%]
```

**Quando usar:**
- Antes de fazer mudanças não-triviais
- Para avaliar segurança de refactoring
- Para entender dependências críticas

### detect_changes - Impacto de Git Diff
**O que oferece:** Mapeamento de mudanças git atuais para flows afetados

**Uso típico:**
```bash
gitnexus_detect_changes({scope: "staged"})

→ Changed: 5 symbols in 3 files
→ Affected: LoginFlow, TokenRefresh, APIMiddlewarePipeline  
→ Risk: MEDIUM
```

**Quando usar:**
- Antes de commit para entender impacto
- Para code review automatizado
- Para validar que mudanças estão no escopo esperado

### rename - Renomeamento Multi-arquivo
**O que oferece:** Renomeamento coordenado com edits marcados por confiança

**Uso típico:**
```bash
gitnexus_rename({
  symbol_name: "validateUser", 
  new_name: "authenticateUser", 
  dry_run: true
})

→ 12 edits across 8 files
→ 10 graph edits (high confidence), 2 ast_search edits (review)
→ Changes: [{file_path, edits: [...]}]
```

**Quando usar:**
- Renomear funções, classes, variáveis com segurança
- Extrair ou mover código para novos módulos
- Refactoring estrutural seguro

### cypher - Queries Customizadas
**O que oferece:** Queries de grafo brutas (ler `gitnexus://repo/{name}/schema` primeiro)

**Uso típico:**
```cypher
MATCH (caller)-[:CodeRelation {type: 'CALLS'}]->(f:Function {name: "myFunc"})
RETURN caller.name, caller.filePath
```

**Quando usar:**
- Queries complexas não cobertas por outras ferramentas
- Análise customizada de padrões específicos
- Debugging avançado do grafo

### list_repos - Descoberta de Repositórios
**O que oferece:** Lista todos os repositórios indexados

**Uso típico:**
```bash
gitnexus_list_repos()
→ [
    {name: "my-app", path: "/home/user/my-app", ...},
    {name: "frontend", path: "/home/user/frontend", ...}
  ]
```

**Quando usar:**
- Descobrir quais projetos estão indexados
- Gerenciar múltiplos repositórios
- Para troubleshooting

## Recursos de Conhecimento

### Recursos Leves (100-500 tokens)
Para navegação rápida e overview:

| Recurso | Conteúdo |
|---------|----------|
| `gitnexus://repo/{name}/context` | Stats, verificação de frescura |
| `gitnexus://repo/{name}/clusters` | Todas áreas funcionais com scores de coesão |
| `gitnexus://repo/{name}/cluster/{clusterName}` | Membros da área |
| `gitnexus://repo/{name}/processes` | Todos execution flows |
| `gitnexus://repo/{name}/process/{processName}` | Trace passo a passo |
| `gitnexus://repo/{name}/schema` | Schema do grafo para Cypher |

### Exemplos de Uso

#### Context Overview
```bash
READ gitnexus://repo/my-app/context
→ 918 symbols, 45 processes
→ Last indexed: 2025-03-06 14:30:00
→ Status: FRESH
```

#### Cluster Analysis
```bash
READ gitnexus://repo/my-app/clusters
→ Authentication (cohesion: 0.89)
→ Payment Processing (cohesion: 0.85)  
→ User Management (cohesion: 0.82)
→ Analytics (cohesion: 0.78)
```

#### Process Trace
```bash
READ gitnexus://repo/my-app/process/LoginFlow
→ Step 1: loginHandler → validateCredentials
→ Step 2: validateCredentials → checkToken
→ Step 3: checkToken → getUserById
→ Step 4: getUserById → createSession
→ Step 5: createSession → redirectUser
```

## Schema do Grafo de Conhecimento

### Nodes (Nós)
- **File** - Arquivos de código
- **Function** - Funções e métodos
- **Class** - Classes e interfaces
- **Interface** - Interfaces TypeScript/Java
- **Method** - Métodos de classe
- **Community** - Áreas funcionais detectadas
- **Process** - Flows de execução

### Edges (Relacionamentos)
Todos os relacionamentos usam a tabela `CodeRelation` com propriedade `type`:

| Tipo | Descrição |
|------|----------|
| `CALLS` | Chamadas de função/método |
| `IMPORTS` | Importações de módulos |
| `EXTENDS` | Herança de classe |
| `IMPLEMENTS` | Implementação de interface |
| `DEFINES` | Definição de símbolos |
| `MEMBER_OF` | Pertencimento a classe/módulo |
| `STEP_IN_PROCESS` | Passo em execution flow |

### Propriedades de Edges
- **type** (STRING): Tipo do relacionamento
- **confidence** (DOUBLE): Confiança da detecção (0-1)
- **reason** (STRING): Razão da detecção
- **step** (INT32): Número do passo em processos

### Exemplos de Queries Cypher

#### Encontrar Callers de Função
```cypher
MATCH (caller)-[:CodeRelation {type: 'CALLS'}]->(f:Function {name: "validateUser"})
RETURN caller.name, caller.filePath
```

#### Encontrar Membros de Comunidade
```cypher
MATCH (f)-[:CodeRelation {type: 'MEMBER_OF'}]->(c:Community)
WHERE c.heuristicLabel = "Auth"
RETURN f.name, f.filePath
```

#### Traçar Processo Completo
```cypher
MATCH (s)-[r:CodeRelation {type: 'STEP_IN_PROCESS'}]->(p:Process)
WHERE p.heuristicLabel = "UserLogin"
RETURN s.name, r.step ORDER BY r.step
```

#### Encontrar Símbolos por Tipo
```cypher
MATCH (n:Function)
WHERE n.name CONTAINS "validate"
RETURN n.name, n.filePath
```

## Workflows por Tipo de Tarefa

### Exploração de Codebase
1. `READ gitnexus://repo/{name}/context` - Overview
2. `gitnexus_query({query: "conceito"})` - Encontrar código relacionado
3. `gitnexus_context({name: "símbolo"})` - Deep dive específico
4. `READ gitnexus://repo/{name}/process/{name}` - Trace execution

### Debugging
1. `gitnexus_query({query: "erro ou sintoma"})` - Encontrar código relacionado
2. `gitnexus_context({name: "suspeito"})` - Verificar callers/callees
3. `READ gitnexus://repo/{name}/process/{name}` - Trace execution
4. `gitnexus_cypher({query: "..."})` - Queries customizadas se necessário

### Impact Analysis
1. `gitnexus_impact({target: "X", direction: "upstream"})` - Map dependents
2. `READ gitnexus://repo/{name}/processes` - Verificar flows afetados
3. `gitnexus_detect_changes()` - Verificar mudanças atuais
4. Avaliar risco e reportar

### Refactoring
1. `gitnexus_impact({target: "X", direction: "upstream"})` - Map dependents
2. `gitnexus_query({query: "X"})` - Encontrar flows envolvidos
3. `gitnexus_context({name: "X"})` - Verificar todos os refs
4. Planejar ordem de atualização

## Troubleshooting Comum

### Problemas Frequentes

**"Index is stale"**
- Solução: Rode `npx gitnexus analyze`
- Causa: Mudanças no código desde última análise

**"Not inside a git repository"**
- Solução: Rode de dentro de um diretório git
- Causa: Comando executado fora de repo

**"No results found"**
- Solução: Verificar spelling, usar termos mais genéricos
- Causa: Query muito específica ou símbolo não existe

**Performance lenta**
- Solução: Use `--embeddings` apenas se necessário
- Causa: Geração de embeddings é computacionalmente intensiva

### Debugging Avançado

**Verificar Schema:**
```bash
READ gitnexus://repo/{name}/schema
```

**Listar Repos Indexados:**
```bash
gitnexus_list_repos()
```

**Verificar Status do Repo:**
```bash
READ gitnexus://repo/{name}/context
```

## Benefícios

- **Visão Completa:** Entendimento holístico do codebase
- **Queries Inteligentes:** Busca por conceito, não apenas texto
- **Impact Analysis:** Avaliação segura de mudanças
- **Refactoring Seguro:** Operações coordenadas e validadas
- **Documentation Automática:** Geração de wiki e docs

## Dicas de Uso

### Para Máxima Efetividade:
1. **Sempre comece com context** - Verifica status e dá overview
2. **Use a skill certa** - Cada tarefa tem skill otimizada
3. **Verifique confiança** - Menor confiança = revisar manualmente
4. **Combine ferramentas** - Use múltiplas approaches para problemas complexos

### Para Performance:
1. **Use queries específicas** - Evite buscas muito amplas
2. **Limite profundidade** - Use `maxDepth` apropriado
3. **Cache resultados** - Reuse context para múltiplas operações
4. **Evite embeddings** - A menos que busca semântica seja necessária

## Recursos Adicionais

- **CLI Commands:** [gitnexus-cli skill](gitnexus-cli.md)
- **Examples:** [GitNexus Examples Repository](https://github.com/gitnexus/examples)
- **API Reference:** [MCP Server Documentation](https://github.com/gitnexus/mcp-server)
- **Community:** [GitNexus Discord](https://discord.gg/gitnexus)

---

**Quick Reference Card:**

```bash
# 1. Verificar status
READ gitnexus://repo/{name}/context

# 2. Escolher skill baseado na tarefa:
#    - Explorar: gitnexus-exploring
#    - Debug: gitnexus-debugging  
#    - Impact: gitnexus-impact-analysis
#    - Refactor: gitnexus-refactoring

# 3. Executar workflow da skill

# 4. Se necessário: CLI commands
npx gitnexus analyze|status|clean|wiki|list
```

**Próximos Passos:**
- Escolher skill apropriada para sua tarefa
- Seguir workflow recomendado
- Usar recursos de conhecimento para navegação
- Combinar ferramentas para análise complexa
- Documentar aprendizados para equipe
