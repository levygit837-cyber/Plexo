# Comandos CLI GitNexus

## Propósito
Interface de linha de comando para GitNexus, permitindo analisar, gerenciar e gerar documentação de repositórios de código através de comandos simples executados via `npx` sem instalação global.

## Como Funciona
Todos os comandos usam `npx` — sem necessidade de instalação global. A CLI fornece comandos para analisar repositórios, verificar status, limpar índices, gerar wikis e listar repositórios indexados, integrando-se com o conhecimento de código do GitNexus.

## Quando Usar
- Primeira configuração em um projeto
- Após mudanças significativas no código
- Para verificar se o índice está atualizado
- Antes de usar outras skills GitNexus
- Para gerar documentação automaticamente
- Para troubleshooting de problemas

## Comandos Disponíveis

### analyze — Construir ou atualizar o índice
```bash
npx gitnexus analyze
```

**O que faz:** 
- Parse de todos os arquivos fonte
- Constrói o grafo de conhecimento
- Escreve em `.gitnexus/`
- Gera arquivos de contexto CLAUDE.md/AGENTS.md

**Flags:**
- `--force`: Força re-indexação completa mesmo se atualizado
- `--embeddings`: Habilita geração de embeddings para busca semântica (padrão: off)

**Quando usar:**
- Primeira vez em um projeto
- Após mudanças maiores no código
- Quando `gitnexus://repo/{name}/context` reportar índice desatualizado

**Exemplo:**
```bash
# Análise inicial do projeto
npx gitnexus analyze

# Forçar re-indexação completa
npx gitnexus analyze --force

# Com embeddings para busca semântica
npx gitnexus analyze --embeddings
```

### status — Verificar frescura do índice
```bash
npx gitnexus status
```

**O que faz:**
- Mostra se o repo atual tem índice GitNexus
- Quando foi atualizado pela última vez
- Contagem de símbolos e relacionamentos
- Ajuda a decidir se re-indexação é necessária

**Quando usar:**
- Antes de começar a usar GitNexus
- Para verificar se análise é necessária
- Para troubleshooting

**Exemplo de output:**
```
GitNexus Status for: /home/user/my-project
✓ Index exists
Last updated: 2025-03-06 14:30:00
Symbols: 1,247 functions, 89 classes
Relationships: 3,456 total
Status: FRESH (index up to date)
```

### clean — Deletar o índice
```bash
npx gitnexus clean
```

**O que faz:**
- Deleta diretório `.gitnexus/`
- Remove repo do registro global
- Limpa todos os dados indexados

**Quando usar:**
- Antes de re-indexar se índice estiver corrompido
- Ao remover GitNexus de um projeto
- Para troubleshooting de problemas persistentes

**Flags:**
- `--force`: Pula confirmação
- `--all`: Limpa todos os repos indexados, não apenas o atual

**Exemplo:**
```bash
# Limpar repo atual (com confirmação)
npx gitnexus clean

# Forçar limpeza sem confirmação
npx gitnexus clean --force

# Limpar todos os repos indexados
npx gitnexus clean --all
```

### wiki — Gerar documentação do grafo
```bash
npx gitnexus wiki
```

**O que faz:**
- Gera documentação do repositório usando o grafo de conhecimento
- Requer API key (salva em `~/.gitnexus/config.json` no primeiro uso)
- Cria documentação estruturada e organizada

**Quando usar:**
- Para documentar automaticamente um projeto
- Antes de entregar documentação
- Para onboard de novos desenvolvedores

**Flags:**
- `--force`: Força regeneração completa
- `--model <model>`: Modelo LLM (padrão: minimax/minimax-m2.5)
- `--base-url <url>`: URL base da API LLM
- `--api-key <key>`: API key LLM
- `--concurrency <n>`: Chamadas LLM paralelas (padrão: 3)
- `--gist`: Publica wiki como GitHub Gist público

**Exemplo:**
```bash
# Gerar wiki com modelo padrão
npx gitnexus wiki

# Com modelo específico
npx gitnexus wiki --model gpt-4

# Publicar como GitHub Gist
npx gitnexus wiki --gist
```

### list — Mostrar todos os repos indexados
```bash
npx gitnexus list
```

**O que faz:**
- Lista todos os repos em `~/.gitnexus/registry.json`
- Mesma informação que a ferramenta MCP `list_repos`
- Ajuda a gerenciar múltiplos projetos

**Quando usar:**
- Para descobrir quais projetos estão indexados
- Para gerenciar múltiplos repositórios
- Para troubleshooting

**Exemplo de output:**
```
Indexed Repositories:
1. my-project (/home/user/my-project)
   - Last indexed: 2025-03-06 14:30:00
   - Symbols: 1,247
2. frontend-app (/home/user/frontend-app)
   - Last indexed: 2025-03-05 10:15:00
   - Symbols: 892
```

## Workflow de Uso

### Para Novos Projetos
```bash
# 1. Verificar status atual
npx gitnexus status

# 2. Analisar projeto (se necessário)
npx gitnexus analyze

# 3. Verificar resultado
npx gitnexus status

# 4. Gerar documentação (opcional)
npx gitnexus wiki
```

### Para Projetos Existentes
```bash
# 1. Verificar se índice está atualizado
npx gitnexus status

# 2. Se desatualizado, re-analisar
npx gitnexus analyze

# 3. Verificar resultado
npx gitnexus status
```

### Para Troubleshooting
```bash
# 1. Limpar índice corrompido
npx gitnexus clean --force

# 2. Re-analisar do zero
npx gitnexus analyze --force

# 3. Verificar resultado
npx gitnexus status
```

## Exemplos Práticos

### Exemplo 1: Setup Inicial
**Cenário:** Novo projeto React que precisa ser indexado

```bash
$ cd /home/user/my-react-app
$ npx gitnexus status
❌ No GitNexus index found

$ npx gitnexus analyze
🔍 Analyzing repository...
📊 Found 1,247 symbols
🔗 Built 3,456 relationships
✅ Index built successfully

$ npx gitnexus status
✓ Index exists
Last updated: 2025-03-06 14:30:00
Symbols: 1,247 functions, 89 classes
Status: FRESH
```

### Exemplo 2: Após Mudanças Significativas
**Cenário:** Refactoring grande que adicionou novos módulos

```bash
$ npx gitnexus status
⚠️  Index is STALE (last updated 2 days ago)
   Recent changes detected in:
   - src/new-module/
   - src/components/

$ npx gitnexus analyze
🔍 Re-analyzing repository...
📊 Found 1,389 symbols (+142)
🔗 Built 3,789 relationships (+333)
✅ Index updated successfully

$ npx gitnexus status
✓ Index exists
Last updated: 2025-03-06 15:45:00
Symbols: 1,389 functions, 92 classes
Status: FRESH
```

### Exemplo 3: Geração de Wiki
**Cenário:** Documentação necessária para onboard

```bash
$ npx gitnexus wiki --model gpt-4 --concurrency 2
📝 Generating wiki documentation...
🤖 Using model: gpt-4
📊 Processing 1,389 symbols...
✅ Wiki generated successfully
📁 Saved to: ./docs/wiki.md

# Publicar como Gist
$ npx gitnexus wiki --gist
📝 Generating wiki...
🌐 Publishing to GitHub Gist...
✅ Wiki published: https://gist.github.com/abc123
```

## Benefícios

- **Simplicidade:** Comandos intuitivos e fáceis de lembrar
- **Flexibilidade:** Flags para customização avançada
- **Integração:** Funciona com outras skills GitNexus
- **Performance:** Operações otimizadas para grandes projetos
- **Conveniência:** Sem instalação global necessária

## Dicas de Uso

### Melhores Práticas:
1. **Verifique Status Sempre:** Use `status` antes de outras operações
2. **Use --force com Cuidado:** Apenas quando necessário
3. **Monitore Output:** Preste atenção a warnings e erros
4. **Documente Workflow:** Crie scripts para equipes

### Performance Tips:
- Use `--embeddings` apenas se precisar busca semântica
- `--concurrency` pode ser ajustado baseado na API rate limits
- Para projetos grandes, considere rodar `analyze` durante off-hours

### Troubleshooting Comum:
- **"Not inside a git repository"**: Rode de dentro de um repo git
- **"Index is stale"**: Rode `npx gitnexus analyze`
- **Embeddings lentas**: Omita `--embeddings` ou configure API key
- **Problemas de permissão**: Verifique acesso ao diretório

## Recursos Adicionais

- **Documentação:** [GitNexus Official Docs](https://github.com/gitnexus/gitnexus)
- **API Reference:** [GitNexus MCP Server](https://github.com/gitnexus/mcp-server)
- **Troubleshooting:** [Common Issues Guide](https://github.com/gitnexus/troubleshooting)
- **Examples:** [GitNexus Examples](https://github.com/gitnexus/examples)

---

**Comandos Rápidos de Referência:**

```bash
# Verificar status
npx gitnexus status

# Analisar projeto
npx gitnexus analyze [--force] [--embeddings]

# Limpar índice
npx gitnexus clean [--force] [--all]

# Gerar wiki
npx gitnexus wiki [--model MODEL] [--gist]

# Listar repos
npx gitnexus list
```

**Workflow Padrão:**
1. `npx gitnexus status` - Verificar se análise é necessária
2. `npx gitnexus analyze` - Analisar se desatualizado
3. Usar skills GitNexus (exploring, debugging, etc.)
4. `npx gitnexus wiki` - Gerar documentação se necessário

**Próximos Passos:**
- Integrar com CI/CD pipeline
- Criar scripts de automação para equipe
- Configurar API keys para uso compartilhado
- Documentar workflow interno da equipe
