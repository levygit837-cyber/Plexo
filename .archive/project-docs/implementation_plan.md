# Implementation Plan

## [Overview]

Criar estrutura hierárquica base completa para o sistema multi-agentes Plexo, separando backend (FastAPI + LangChain + SPADE) e frontend em diretórios independentes.

Este plano estabelece a fundação arquitetural do Plexo, um sistema multi-agentes que utiliza FastAPI como framework web, LangChain/LangGraph para orquestração de agentes, SPADE (XMPP) para comunicação entre agentes, PostgreSQL para persistência relacional, KuzuDB para embeddings vetoriais, e RabbitMQ para processamento assíncrono. A estrutura é projetada para escalabilidade, manutenibilidade e separação clara de responsabilidades.

O backend seguirá arquitetura em camadas (Controllers → Services → Models) com suporte a operações paralelas, sistema de filas, logging estruturado, tratamento de exceções com métricas p95/p99, e memória de curto/longo prazo para agentes. O frontend será estruturado com separação de concerns (hooks, contexts, pages, components) preparado para integração com o backend via API REST.

## [Types]

Definir schemas Pydantic, interfaces TypeScript e estruturas de dados para comunicação inter-agentes e API.

### Backend Types (Python/Pydantic)

**Schemas Base:**

- `BaseSchema`: Schema base com campos comuns (id, created_at, updated_at)
- `AgentSchema`: Schema para definição de agentes (id, name, type, capabilities, status)
- `MessageSchema`: Schema para mensagens XMPP (sender, receiver, content, timestamp, message_type)
- `TaskSchema`: Schema para tarefas assíncronas (task_id, status, priority, payload, result)
- `ErrorSchema`: Schema para erros estruturados (code, message, details, timestamp, trace_id)

**Interfaces SPADE:**

- `AgentBehavior`: Interface para comportamentos de agentes
- `AgentMessage`: Interface para mensagens entre agentes
- `AgentState`: Interface para estado de agentes

**Memory Schemas:**

- `ShortTermMemory`: Schema para memória de curto prazo (session_id, context, ttl)
- `LongTermMemory`: Schema para memória de longo prazo (agent_id, knowledge, embeddings)

### Frontend Types (TypeScript)

**API Response Types:**

- `ApiResponse<T>`: Generic type para respostas da API
- `PaginatedResponse<T>`: Type para respostas paginadas
- `ErrorResponse`: Type para erros da API

**Domain Types:**

- `Agent`: Interface para agentes no frontend
- `Task`: Interface para tarefas
- `Message`: Interface para mensagens

## [Files]

Criar estrutura completa de diretórios e arquivos de configuração para backend e frontend separados.

### Backend Structure (`backend/`)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Entry point FastAPI
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py            # Configurações (Pydantic Settings)
│   │   ├── database.py            # Configuração PostgreSQL
│   │   ├── kuzu.py                # Configuração KuzuDB
│   │   └── rabbitmq.py            # Configuração RabbitMQ
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                # Dependências FastAPI
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py          # Router principal v1
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── agents.py      # Endpoints de agentes
│   │           ├── tasks.py       # Endpoints de tarefas
│   │           ├── messages.py    # Endpoints de mensagens
│   │           └── health.py      # Health check
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent_service.py       # Lógica de negócio de agentes
│   │   ├── task_service.py        # Lógica de tarefas
│   │   ├── message_service.py     # Lógica de mensagens
│   │   └── infrastructure/
│   │       ├── __init__.py
│   │       ├── database_service.py
│   │       ├── cache_service.py
│   │       └── queue_service.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py                # Base model SQLAlchemy
│   │   ├── agent.py               # Model Agent
│   │   ├── task.py                # Model Task
│   │   ├── message.py             # Model Message
│   │   └── memory/
│   │       ├── __init__.py
│   │       ├── short_term.py      # Memória curto prazo
│   │       └── long_term.py       # Memória longo prazo
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── base.py                # Schemas base
│   │   ├── agent.py               # Schemas de agentes
│   │   ├── task.py                # Schemas de tarefas
│   │   ├── message.py             # Schemas de mensagens
│   │   └── memory.py              # Schemas de memória
│   ├── interfaces/
│   │   ├── __init__.py
│   │   ├── agent_interface.py     # Interface abstrata de agentes
│   │   ├── service_interface.py   # Interface abstrata de serviços
│   │   └── repository_interface.py # Interface abstrata de repositórios
│   ├── spade/
│   │   ├── __init__.py
│   │   ├── agent_base.py          # Base class para agentes SPADE
│   │   ├── behaviors/
│   │   │   ├── __init__.py
│   │   │   ├── base_behavior.py
│   │   │   └── message_behavior.py
│   │   ├── protocols/
│   │   │   ├── __init__.py
│   │   │   └── xmpp_protocol.py
│   │   └── registry/
│   │       ├── __init__.py
│   │       └── agent_registry.py  # Registro de agentes ativos
│   ├── langchain/
│   │   ├── __init__.py
│   │   ├── chains/
│   │   │   ├── __init__.py
│   │   │   └── base_chain.py
│   │   ├── graphs/
│   │   │   ├── __init__.py
│   │   │   └── agent_graph.py
│   │   └── tools/
│   │       ├── __init__.py
│   │       ├── base_tool.py
│   │       └── custom_tools.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── errors/
│   │   │   ├── __init__.py
│   │   │   ├── base.py            # Base exception classes
│   │   │   ├── api_errors.py      # API specific errors
│   │   │   ├── agent_errors.py    # Agent specific errors
│   │   │   └── handlers.py        # Error handlers
│   │   ├── exceptions/
│   │   │   ├── __init__.py
│   │   │   ├── custom_exceptions.py
│   │   │   └── middleware.py      # Exception middleware
│   │   ├── metrics/
│   │   │   ├── __init__.py
│   │   │   ├── collector.py       # Metrics collector
│   │   │   ├── p95_p99.py         # P95/P99 calculator
│   │   │   └── prometheus.py      # Prometheus integration
│   │   └── logging/
│   │       ├── __init__.py
│   │       ├── logger.py          # Logger configuration
│   │       ├── formatters.py      # Log formatters
│   │       └── handlers.py        # Log handlers
│   ├── workers/
│   │   ├── __init__.py
│   │   ├── base_worker.py         # Base worker class
│   │   ├── task_worker.py         # Task processing worker
│   │   └── agent_worker.py        # Agent execution worker
│   ├── queues/
│   │   ├── __init__.py
│   │   ├── producer.py            # RabbitMQ producer
│   │   ├── consumer.py            # RabbitMQ consumer
│   │   └── tasks/
│   │       ├── __init__.py
│   │       ├── agent_tasks.py
│   │       └── background_tasks.py
│   └── utils/
│       ├── __init__.py
│       ├── security.py            # Security utilities
│       ├── validators.py          # Validation utilities
│       └── helpers.py             # General helpers
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest configuration
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_services/
│   │   ├── test_models/
│   │   └── test_utils/
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_api/
│   │   └── test_agents/
│   └── e2e/
│       ├── __init__.py
│       └── test_workflows/
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── scripts/
│   ├── init_db.py
│   ├── seed_data.py
│   └── run_worker.py
├── docker/
│   ├── Dockerfile
│   ├── Dockerfile.worker
│   └── docker-compose.yml
├── .env.example
├── .gitignore
├── pyproject.toml                 # Poetry configuration
├── poetry.lock
├── README.md
└── alembic.ini
```

### Frontend Structure (`frontend/`)

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── main.tsx                   # Entry point
│   ├── App.tsx                    # Root component
│   ├── vite-env.d.ts
│   ├── assets/
│   │   ├── images/
│   │   ├── icons/
│   │   └── styles/
│   │       ├── global.css
│   │       └── variables.css
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button/
│   │   │   ├── Input/
│   │   │   ├── Modal/
│   │   │   └── Loading/
│   │   ├── layout/
│   │   │   ├── Header/
│   │   │   ├── Sidebar/
│   │   │   ├── Footer/
│   │   │   └── Layout/
│   │   └── features/
│   │       ├── agents/
│   │       ├── tasks/
│   │       └── messages/
│   ├── pages/
│   │   ├── Home/
│   │   │   ├── index.tsx
│   │   │   └── Home.module.css
│   │   ├── Agents/
│   │   │   ├── index.tsx
│   │   │   ├── AgentList.tsx
│   │   │   └── AgentDetail.tsx
│   │   ├── Tasks/
│   │   │   ├── index.tsx
│   │   │   └── TaskList.tsx
│   │   └── NotFound/
│   │       └── index.tsx
│   ├── hooks/
│   │   ├── useApi.ts              # API hook
│   │   ├── useAuth.ts             # Authentication hook
│   │   ├── useWebSocket.ts        # WebSocket hook
│   │   ├── useAgents.ts           # Agents hook
│   │   └── useTasks.ts            # Tasks hook
│   ├── contexts/
│   │   ├── AuthContext.tsx        # Authentication context
│   │   ├── ThemeContext.tsx       # Theme context
│   │   ├── AgentContext.tsx       # Agent context
│   │   └── NotificationContext.tsx # Notification context
│   ├── services/
│   │   ├── api/
│   │   │   ├── client.ts          # Axios client
│   │   │   ├── agents.ts          # Agent API calls
│   │   │   ├── tasks.ts           # Task API calls
│   │   │   └── auth.ts            # Auth API calls
│   │   └── websocket/
│   │       ├── client.ts          # WebSocket client
│   │       └── handlers.ts        # WebSocket handlers
│   ├── types/
│   │   ├── index.ts
│   │   ├── agent.ts               # Agent types
│   │   ├── task.ts                # Task types
│   │   ├── api.ts                 # API types
│   │   └── common.ts              # Common types
│   ├── utils/
│   │   ├── formatters.ts          # Data formatters
│   │   ├── validators.ts          # Validators
│   │   └── helpers.ts             # Helper functions
│   ├── constants/
│   │   ├── index.ts
│   │   ├── routes.ts              # Route constants
│   │   └── api.ts                 # API constants
│   ├── routes/
│   │   ├── index.tsx              # Route configuration
│   │   └── PrivateRoute.tsx       # Protected route component
│   └── store/
│       ├── index.ts               # Store configuration
│       └── slices/
│           ├── agentSlice.ts
│           └── taskSlice.ts
├── tests/
│   ├── unit/
│   │   ├── components/
│   │   └── hooks/
│   ├── integration/
│   │   └── pages/
│   └── e2e/
│       └── workflows/
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
└── README.md
```

### Root Level Files

- `.gitignore`: Ignorar node_modules, **pycache**, .env, etc.
- `README.md`: Documentação principal do projeto
- `docker-compose.yml`: Orquestração de todos os serviços
- `.env.example`: Template de variáveis de ambiente

## [Functions]

Funções utilitárias base para inicialização, configuração e operações comuns do sistema.

### Backend Functions

**app/main.py:**

- `create_app() -> FastAPI`: Factory function para criar instância FastAPI
- `setup_middleware(app: FastAPI) -> None`: Configurar middlewares
- `setup_routes(app: FastAPI) -> None`: Registrar routers
- `lifespan(app: FastAPI) -> AsyncContextManager`: Gerenciar lifecycle

**app/config/settings.py:**

- `get_settings() -> Settings`: Singleton para configurações
- `validate_settings(settings: Settings) -> bool`: Validar configurações

**app/config/database.py:**

- `get_db_session() -> AsyncGenerator[AsyncSession, None]`: Dependency para sessão DB
- `init_db() -> None`: Inicializar banco de dados

**app/core/logging/logger.py:**

- `get_logger(name: str) -> logging.Logger`: Obter logger configurado
- `setup_logging(level: str = "INFO") -> None`: Configurar sistema de logging

**app/core/metrics/p95_p99.py:**

- `calculate_p95(values: List[float]) -> float`: Calcular percentil 95
- `calculate_p99(values: List[float]) -> float`: Calcular percentil 99
- `track_latency(endpoint: str, duration: float) -> None`: Rastrear latência

**app/queues/producer.py:**

- `publish_task(queue: str, task: dict) -> None`: Publicar tarefa na fila

**app/workers/base_worker.py:**

- `start_worker() -> None`: Iniciar worker
- `process_task(task: dict) -> Any`: Processar tarefa

**app/spade/agent_base.py:**

- `register_agent(agent: Agent) -> None`: Registrar agente
- `send_message(to: str, content: str) -> None`: Enviar mensagem XMPP

### Frontend Functions

**src/services/api/client.ts:**

- `createApiClient(baseURL: string) -> AxiosInstance`: Criar cliente API
- `handleApiError(error: AxiosError) -> void`: Tratar erros da API

**src/services/websocket/client.ts:**

- `connectWebSocket(url: string) -> WebSocket`: Conectar WebSocket
- `sendMessage(message: any) -> void`: Enviar mensagem via WebSocket

**src/utils/formatters.ts:**

- `formatDate(date: Date, format: string) -> string`: Formatar data
- `formatDuration(ms: number) -> string`: Formatar duração

## [Classes]

Classes base e abstratas para agentes, serviços, repositórios e componentes do sistema.

### Backend Classes

**app/models/base.py:**

```python
class BaseModel(DeclarativeBase):
    """Base class for all SQLAlchemy models"""
    id: Mapped[int]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    
    def to_dict(self) -> dict
    def from_dict(cls, data: dict) -> Self
```

**app/models/agent.py:**

```python
class Agent(BaseModel):
    """Agent model for database persistence"""
    __tablename__ = "agents"
    
    name: Mapped[str]
    type: Mapped[str]
    status: Mapped[str]
    capabilities: Mapped[dict]
    config: Mapped[dict]
```

**app/spade/agent_base.py:**

```python
class PlexoAgent(Agent):
    """Base class for all SPADE agents"""
    
    async def setup(self) -> None
    async def on_message(self, msg: Message) -> None
    async def send_to_agent(self, to_jid: str, content: str) -> None
```

**app/services/agent_service.py:**

```python
class AgentService:
    """Service layer for agent operations"""
    
    async def create_agent(self, data: AgentCreate) -> Agent
    async def get_agent(self, agent_id: int) -> Agent | None
    async def list_agents(self, filters: dict) -> List[Agent]
```

**app/workers/base_worker.py:**

```python
class BaseWorker(ABC):
    """Abstract base class for all workers"""
    
    async def start(self) -> None
    async def stop(self) -> None
    @abstractmethod
    async def process_task(self, task: dict) -> Any
```

**app/core/errors/base.py:**

```python
class PlexoException(Exception):
    """Base exception for all Plexo errors"""
    
    def to_dict(self) -> dict
    def log(self, logger: logging.Logger) -> None
```

**app/core/metrics/collector.py:**

```python
class MetricsCollector:
    """Collect and aggregate system metrics"""
    
    def record_latency(self, endpoint: str, duration: float) -> None
    def get_p95(self, metric: str) -> float
    def get_p99(self, metric: str) -> float
```

### Frontend Classes

**src/services/api/client.ts:**

```typescript
class ApiClient {
  async get<T>(url: string): Promise<T>
  async post<T>(url: string, data?: any): Promise<T>
  setAuthToken(token: string): void
}
```

**src/services/websocket/client.ts:**

```typescript
class WebSocketClient {
  connect(): Promise<void>
  send(message: any): void
  on(event: string, callback: (data: any) => void): void
}
```

## [Dependencies]

Dependências Python (Poetry) e Node necessárias para o projeto.

### Backend Dependencies (pyproject.toml)

**Core:**

- `python = "^3.11"`
- `fastapi = "^0.109.0"`
- `uvicorn[standard] = "^0.27.0"`
- `pydantic = "^2.5.0"`
- `pydantic-settings = "^2.1.0"`

**Database:**

- `sqlalchemy = "^2.0.25"`
- `asyncpg = "^0.29.0"`
- `alembic = "^1.13.0"`
- `kuzu = "^0.1.0"`

**LangChain:**

- `langchain = "^0.1.0"`
- `langgraph = "^0.0.20"`
- `langchain-openai = "^0.0.2"`

**SPADE:**

- `spade = "^3.3.0"`
- `aioxmpp = "^0.13.0"`

**Queue:**

- `aio-pika = "^9.3.0"`
- `celery = "^5.3.0"`

**Utilities:**

- `python-jose[cryptography] = "^3.3.0"`
- `passlib[bcrypt] = "^1.7.4"`
- `python-multipart = "^0.0.6"`
- `httpx = "^0.26.0"`
- `redis = "^5.0.0"`

**Monitoring:**

- `prometheus-client = "^0.19.0"`
- `structlog = "^24.1.0"`

**Dev Dependencies:**

- `pytest = "^7.4.0"`
- `pytest-asyncio = "^0.21.0"`
- `pytest-cov = "^4.1.0"`
- `black = "^23.12.0"`
- `ruff = "^0.1.0"`
- `mypy = "^1.8.0"`

### Frontend Dependencies (package.json)

**Core:**

- `react = "^18.2.0"`
- `react-dom = "^18.2.0"`
- `react-router-dom = "^6.21.0"`
- `typescript = "^5.3.0"`

**State Management:**

- `zustand = "^4.4.0"` (ou `@reduxjs/toolkit = "^2.0.0"`)

**API:**

- `axios = "^1.6.0"`
- `@tanstack/react-query = "^5.17.0"`

**UI:**

- `tailwindcss = "^3.4.0"`
- `@headlessui/react = "^1.7.0"`
- `lucide-react = "^0.303.0"`

**Forms:**

- `react-hook-form = "^7.49.0"`
- `zod = "^3.22.0"`

**Dev Dependencies:**

- `vite = "^5.0.0"`
- `@vitejs/plugin-react = "^4.2.0"`
- `@types/react = "^18.2.0"`
- `@types/react-dom = "^18.2.0"`
- `eslint = "^8.56.0"`
- `prettier = "^3.1.0"`
- `vitest = "^1.1.0"`
- `@testing-library/react = "^14.1.0"`

## [Testing]

Estrutura de testes unitários, integração e e2e para backend e frontend.

### Backend Testing

**Estrutura:**

- `tests/unit/`: Testes unitários de serviços, models e utils
- `tests/integration/`: Testes de integração de API e agentes
- `tests/e2e/`: Testes end-to-end de workflows completos

**Configuração:**

- `conftest.py`: Fixtures compartilhadas (db session, test client, mock agents)
- `pytest.ini`: Configuração pytest com markers e coverage
- Coverage mínimo: 80%

**Fixtures Principais:**

- `test_db`: Banco de dados de teste (SQLite in-memory)
- `test_client`: Cliente FastAPI para testes
- `mock_agent`: Mock de agente SPADE
- `mock_rabbitmq`: Mock de RabbitMQ

### Frontend Testing

**Estrutura:**

- `tests/unit/`: Testes de componentes e hooks
- `tests/integration/`: Testes de páginas completas
- `tests/e2e/`: Testes com Playwright/Cypress

**Configuração:**

- Vitest para testes unitários
- Testing Library para componentes React
- MSW (Mock Service Worker) para mock de API
- Coverage mínimo: 70%

## [Implementation Order]

Ordem lógica de criação dos diretórios e arquivos base para minimizar conflitos.

### Fase 1: Configuração Inicial (Backend)

1. Criar estrutura de diretórios do backend
2. Criar `pyproject.toml` com dependências
3. Criar `.env.example` e `.gitignore`
4. Criar `app/__init__.py` e `app/main.py` (básico)
5. Criar `app/config/settings.py` com Pydantic Settings

### Fase 2: Core Infrastructure (Backend)

1. Criar `app/core/logging/` com logger básico
2. Criar `app/core/errors/` com exception classes
3. Criar `app/core/metrics/` com collector e p95/p99
4. Criar `app/config/database.py` com SQLAlchemy setup
5. Criar `app/config/kuzu.py` com KuzuDB setup
6. Criar `app/config/rabbitmq.py` com RabbitMQ setup

### Fase 3: Models e Schemas (Backend)

1. Criar `app/models/base.py` com BaseModel
2. Criar `app/schemas/base.py` com BaseSchema
3. Criar `app/interfaces/` com interfaces abstratas
4. Criar `app/models/agent.py`, `task.py`, `message.py`
5. Criar `app/schemas/agent.py`, `task.py`, `message.py`
6. Criar `app/models/memory/` com short_term e long_term

### Fase 4: Services e API (Backend)

1. Criar `app/services/infrastructure/` com database, cache, queue services
2. Criar `app/services/agent_service.py`, `task_service.py`, `message_service.py`
3. Criar `app/api/deps.py` com dependências FastAPI
4. Criar `app/api/v1/endpoints/` com health, agents, tasks, messages
5. Criar `app/api/v1/router.py` agregando endpoints

### Fase 5: SPADE e LangChain (Backend)

1. Criar `app/spade/agent_base.py` com PlexoAgent
2. Criar `app/spade/behaviors/` com base_behavior e message_behavior
3. Criar `app/spade/protocols/` com xmpp_protocol
4. Criar `app/spade/registry/` com agent_registry
5. Criar `app/langchain/chains/` com base_chain
6. Criar `app/langchain/graphs/` com agent_graph
7. Criar `app/langchain/tools/` com base_tool e custom_tools

### Fase 6: Workers e Queues (Backend)

1. Criar `app/queues/producer.py` e `consumer.py`
2. Criar `app/queues/tasks/` com agent_tasks e background_tasks
3. Criar `app/workers/base_worker.py`
4. Criar `app/workers/task_worker.py` e `agent_worker.py`

### Fase 7: Testing e Scripts (Backend)

1. Criar `tests/conftest.py` com fixtures
2. Criar estrutura de `tests/unit/`, `integration/`, `e2e/`
3. Criar `scripts/init_db.py`, `seed_data.py`, `run_worker.py`
4. Criar `alembic/` com configuração de migrations

### Fase 8: Docker (Backend)

1. Criar `docker/Dockerfile` para aplicação
2. Criar `docker/Dockerfile.worker` para workers
3. Criar `docker/docker-compose.yml` com todos os serviços

### Fase 9: Configuração Inicial (Frontend)

1. Criar estrutura de diretórios do frontend
2. Criar `package.json` com dependências
3. Criar `vite.config.ts`, `tsconfig.json`, `tailwind.config.js`
4. Criar `.env.example` e `.gitignore`
5. Criar `src/main.tsx` e `src/App.tsx` (básico)

### Fase 10: Types e Constants (Frontend)

1. Criar `src/types/` com agent, task, api, common types
2. Criar `src/constants/` com routes e api constants
3. Criar `src/utils/` com formatters, validators, helpers

### Fase 11: Services e Hooks (Frontend)

1. Criar `src/services/api/client.ts` com Axios setup
2. Criar `src/services/api/` com agents, tasks, auth endpoints
3. Criar `src/services/websocket/` com WebSocket client
4. Criar `src/hooks/` com useApi, useAuth, useWebSocket, useAgents, useTasks

### Fase 12: Contexts e Store (Frontend)

1. Criar `src/contexts/` com AuthContext, ThemeContext, AgentContext, NotificationContext
2. Criar `src/store/` com configuração de state management (se usar)

### Fase 13: Components (Frontend)

1. Criar `src/components/common/` com Button, Input, Modal, Loading
2. Criar `src/components/layout/` com Header, Sidebar, Footer, Layout
3. Criar `src/components/features/` com componentes de agents, tasks, messages

### Fase 14: Pages e Routes (Frontend)

1. Criar `src/pages/` com Home, Agents, Tasks, NotFound
2. Criar `src/routes/` com configuração de rotas e PrivateRoute

### Fase 15: Testing (Frontend)

1. Criar estrutura de `tests/unit/`, `integration/`, `e2e/`
2. Configurar Vitest, Testing Library, MSW

### Fase 16: Finalização

1. Criar README.md para backend e frontend
2. Criar docker-compose.yml root com todos os serviços
3. Criar .gitignore root
4. Validar estrutura completa
