# 0007. Agent Tools and Capabilities

Data: 2026-03-29

Status: Aceito

## Contexto

Os agentes do sistema Plexo precisam acessar ferramentas externas e capacidades específicas para executar tarefas de codificação efetivamente. Os agentes devem ser capazes de:

- Executar código em ambiente seguro
- Acessar e modificar arquivos do sistema
- Pesquisar informações na internet
- Interagir com sistemas de controle de versão (Git)
- Consultar bancos de dados
- Usar modelos de linguagem para geração de código
- Executar comandos de terminal

## Decisão

Decidimos implementar um **sistema de ferramentas modulares** com as seguintes capacidades:

### 1. Ferramentas de Código

#### CodeExecutor
- **Descrição**: Executa código em sandbox seguro
- **Linguagens**: Python, JavaScript/TypeScript, Shell
- **Segurança**: Container Docker isolado com recursos limitados
- **Recursos**:
  - Limite de CPU: 1 core
  - Limite de RAM: 512MB
  - Limite de tempo: 30 segundos
  - Sem acesso à rede (exceto whitelisted)
  - Sistema de arquivos temporário

#### CodeAnalyzer
- **Descrição**: Analisa código sem executar
- **Funcionalidades**:
  - Análise estática (linting, type checking)
  - Detecção de padrões
  - Métricas de complexidade
  - Sugestões de refatoração

#### CodeGenerator
- **Descrição**: Gera código usando LLMs
- **Funcionalidades**:
  - Geração de funções/classes
  - Completar código existente
  - Gerar testes unitários
  - Documentação automática

### 2. Ferramentas de Sistema de Arquivos

#### FileReader
- **Descrição**: Lê arquivos do projeto
- **Funcionalidades**:
  - Leitura de qualquer arquivo de código
  - Suporte a múltiplas codificações
  - Detecção automática de encoding
  - Leitura parcial (por linha ou bloco)

#### FileWriter
- **Descrição**: Escreve/modifica arquivos
- **Funcionalidades**:
  - Criação de novos arquivos
  - Modificação de arquivos existentes
  - Backup automático antes de alterações
  - Validação de sintaxe antes de salvar

#### FileSearcher
- **Descrição**: Busca dentro de arquivos
- **Funcionalidades**:
  - Busca por regex
  - Busca por padrões de código
  - Busca semântica (usando embeddings)
  - Busca em múltiplos arquivos simultaneamente

### 3. Ferramentas de Pesquisa Web

#### WebSearcher
- **Descrição**: Pesquisa informações na internet
- **Funcionalidades**:
  - Busca em mecanismos de busca
  - Busca em documentação oficial
  - Busca em Stack Overflow
  - Busca em repositórios GitHub

#### WebScraper
- **Descrição**: Extrai conteúdo de páginas web
- **Funcionalidades**:
  - Parsing de HTML
  - Extração de conteúdo relevante
  - Conversão para markdown
  - Cache de resultados

### 4. Ferramentas de Git

#### GitOperations
- **Descrição**: Operações com Git
- **Funcionalidades**:
  - `git status`: Verificar estado do repositório
  - `git diff`: Verificar mudanças
  - `git add`: Adicionar arquivos ao staging
  - `git commit`: Criar commits
  - `git branch`: Criar/gerenciar branches
  - `git merge`: Merge de branches
  - `git log`: Verificar histórico
  - `git checkout`: Trocar branches
  - `git pull/push`: Sincronizar com remoto

#### GitWorkflow
- **Descrição**: Workflows de Git automatizados
- **Funcionalidades**:
  - Feature branch workflow
  - Git flow automatizado
  - Pull request automation
  - Code review automation

### 5. Ferramentas de Consulta

#### DatabaseQuery
- **Descrição**: Consulta bancos de dados
- **Funcionalidades**:
  - Query PostgreSQL
  - Query KuzuDB (grafos)
  - Query Redis (cache)
  - Validação de queries antes de executar

#### APIQuery
- **Descrição**: Consulta APIs externas
- **Funcionalidades**:
  - Requisições HTTP/HTTPS
  - Autenticação (OAuth, API keys)
  - Rate limiting automático
  - Retry com backoff

### 6. Ferramentas de Terminal

#### ShellExecutor
- **Descrição**: Executa comandos de shell
- **Funcionalidades**:
  - Comandos bash/zsh
  - Pipes e redirecionamentos
  - Scripts shell
  - Gerenciamento de ambiente

#### ProcessManager
- **Descrição**: Gerencia processos
- **Funcionalidades**:
  - Iniciar processos em background
  - Monitorar processos
  - Terminar processos
  - Capturar output

### 7. Ferramentas de LLM

#### LLMQuery
- **Descrição**: Consulta modelos de linguagem
- **Funcionalidades**:
  - Geração de código
  - Análise de código
  - Explicação de conceitos
  - Tradução entre linguagens

#### RAGSearch
- **Descrição**: Busca por Retrieval Augmented Generation
- **Funcionalidades**:
  - Busca semântica no codebase
  - Busca em documentação
  - Geração contextualizada
  - Manutenção de contexto

## Arquitetura de Ferramentas

### Tool Registry
```python
class ToolRegistry:
    """Registro central de ferramentas disponíveis"""
    
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self.categories: Dict[str, List[str]] = {}
    
    def register(self, tool: BaseTool):
        """Registra uma ferramenta"""
        pass
    
    def get_tool(self, name: str) -> BaseTool:
        """Obtém ferramenta por nome"""
        pass
    
    def get_tools_by_category(self, category: str) -> List[BaseTool]:
        """Obtém ferramentas por categoria"""
        pass
```

### Tool Base Class
```python
class BaseTool(ABC):
    """Classe base para todas as ferramentas"""
    
    name: str
    description: str
    category: str
    parameters: Dict[str, Any]
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """Executa a ferramenta"""
        pass
    
    def validate_parameters(self, **kwargs) -> bool:
        """Valida parâmetros de entrada"""
        pass
    
    def get_schema(self) -> Dict[str, Any]:
        """Retorna schema JSON da ferramenta"""
        pass
```

### Tool Result
```python
@dataclass
class ToolResult:
    success: bool
    data: Any
    error: Optional[str]
    metadata: Dict[str, Any]
    execution_time: float
```

## Segurança e Permissões

### Sistema de Permissões por Agente

```python
class AgentPermissions:
    """Permissões de um agente"""
    
    def __init__(self, agent_type: AgentType):
        self.allowed_tools: Set[str] = set()
        self.restricted_paths: List[str] = []
        self.max_execution_time: int = 300
        self.max_memory_mb: int = 1024
        self._setup_permissions(agent_type)
    
    def _setup_permissions(self, agent_type: AgentType):
        if agent_type == AgentType.CODER:
            self.allowed_tools = {
                'code_executor', 'code_analyzer', 'file_reader',
                'file_writer', 'git_operations', 'shell_executor'
            }
        elif agent_type == AgentType.RESEARCHER:
            self.allowed_tools = {
                'web_searcher', 'web_scraper', 'file_reader',
                'rag_search', 'llm_query'
            }
        elif agent_type == AgentType.COORDINATOR:
            self.allowed_tools = {
                'file_reader', 'database_query', 'api_query',
                'llm_query', 'rag_search'
            }
```

### Validação de Segurança

```python
class SecurityValidator:
    """Valida segurança de execução de ferramentas"""
    
    def validate_tool_execution(
        self,
        agent: Agent,
        tool: BaseTool,
        parameters: Dict[str, Any]
    ) -> Tuple[bool, Optional[str]]:
        """Valida se agente pode executar ferramenta"""
        pass
    
    def sanitize_parameters(
        self,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Sanitiza parâmetros de entrada"""
        pass
```

## Implementação com LangChain Tools

### Integração com LangChain

```python
from langchain.tools import Tool

def create_langchain_tool(plexo_tool: BaseTool) -> Tool:
    """Converte ferramenta Plexo para formato LangChain"""
    return Tool(
        name=plexo_tool.name,
        description=plexo_tool.description,
        func=plexo_tool.execute,
        args_schema=plexo_tool.get_schema()
    )
```

### Tool Categories

1. **Code Tools**: code_executor, code_analyzer, code_generator
2. **File Tools**: file_reader, file_writer, file_searcher
3. **Web Tools**: web_searcher, web_scraper
4. **Git Tools**: git_operations, git_workflow
5. **Query Tools**: database_query, api_query
6. **Terminal Tools**: shell_executor, process_manager
7. **LLM Tools**: llm_query, rag_search

## Monitoramento e Métricas

### Métricas de Uso de Ferramentas

- **Chamadas por ferramenta**: Contagem de execuções
- **Tempo de execução**: Média, p95, p99
- **Taxa de sucesso**: Sucesso vs falha
- **Uso por agente**: Quais agentes usam quais ferramentas
- **Erros frequentes**: Padrões de erro

### Logging de Execução

```python
class ToolExecutionLogger:
    """Logger para execução de ferramentas"""
    
    def log_execution(
        self,
        agent_id: str,
        tool_name: str,
        parameters: Dict[str, Any],
        result: ToolResult,
        duration: float
    ):
        """Log de execução de ferramenta"""
        pass
```

## Consequências

### Positivas
- **Modularidade**: Facilidade de adicionar novas ferramentas
- **Segurança**: Controle granular de permissões
- **Reusabilidade**: Ferramentas podem ser usadas por múltiplos agentes
- **Monitorabilidade**: Métricas detalhadas de uso
- **Flexibilidade**: Agentes podem combinar ferramentas livremente

### Negativas
- **Complexidade**: Sistema mais complexo de gerenciar
- **Overhead**: Validação de segurança tem custo
- **Manutenção**: Mais código para manter
- **Debugging**: Mais difícil debugar uso de ferramentas

## Alternativas Consideradas

### 1. Acesso Direto ao Sistema (Rejeitada)
- Agentes teriam acesso direto ao sistema operacional
- Problema: Segurança comprometida, difícil de auditar

### 2. Ferramentas Monolíticas (Rejeitada)
- Todas as capacidades em uma única classe
- Problema: Difícil de estender e manter

### 3. Ferramentas por Agente (Rejeitada)
- Cada agente tem suas próprias ferramentas
- Problema: Código duplicado, inconsistências

## Próximos Passos

1. Implementar ToolRegistry e BaseTool
2. Criar ferramentas básicas (file, code, git)
3. Implementar sistema de permissões
4. Integrar com LangChain
5. Adicionar monitoramento e logging
6. Criar ferramentas avançadas (web, llm)
7. Testar com diferentes tipos de agentes
