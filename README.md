# Plexo - Sistema Multi-Agentes

Plexo é um sistema multi-agentes avançado que utiliza FastAPI, LangChain/LangGraph, e SPADE (XMPP) para orquestração e comunicação entre agentes inteligentes.

## 🏗️ Arquitetura

O sistema é dividido em duas partes principais:

- **Backend**: FastAPI + LangChain + SPADE + PostgreSQL + KuzuDB + RabbitMQ
- **Frontend**: React + TypeScript + Vite + Tailwind CSS

### Componentes Principais

- **FastAPI**: Framework web para API REST
- **LangChain/LangGraph**: Orquestração de agentes e chains
- **SPADE**: Comunicação entre agentes via XMPP
- **PostgreSQL**: Banco de dados relacional
- **KuzuDB**: Banco de dados vetorial para embeddings
- **RabbitMQ**: Sistema de filas para processamento assíncrono
- **Redis**: Cache e sessões
- **Prometheus + Grafana**: Monitoramento e métricas

## 🚀 Quick Start

### Pré-requisitos

- Docker e Docker Compose
- Node.js 18+ (para desenvolvimento local)
- Python 3.11+ (para desenvolvimento local)

### Executando com Docker

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/Plexo.git
cd Plexo

# Inicie todos os serviços
docker-compose up -d

# Aguarde os serviços iniciarem (pode levar alguns minutos)
docker-compose logs -f
```

Serviços disponíveis:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **RabbitMQ Management**: http://localhost:15672 (user: plexo, pass: plexo_dev_password)
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (user: admin, pass: admin)

### Desenvolvimento Local

#### Backend

```bash
cd backend

# Instalar dependências com Poetry
poetry install

# Ativar ambiente virtual
poetry shell

# Configurar variáveis de ambiente
cp .env.example .env

# Executar migrations
alembic upgrade head

# Seed inicial (opcional)
python scripts/seed_data.py

# Iniciar servidor de desenvolvimento
uvicorn app.main:app --reload

# Executar testes
pytest

# Executar testes com coverage
pytest --cov=app --cov-report=html
```

#### Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env

# Iniciar servidor de desenvolvimento
npm run dev

# Executar testes unitários
npm test

# Executar testes com coverage
npm run test:coverage

# Executar testes E2E
npm run test:e2e
```

## 📁 Estrutura do Projeto

```
Plexo/
├── backend/                 # Backend FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints REST
│   │   ├── config/         # Configurações
│   │   ├── core/           # Core (errors, logging, metrics)
│   │   ├── interfaces/     # Interfaces abstratas
│   │   ├── langchain/      # LangChain chains e graphs
│   │   ├── models/         # Models SQLAlchemy
│   │   ├── schemas/        # Schemas Pydantic
│   │   ├── services/       # Lógica de negócio
│   │   ├── spade/          # Agentes SPADE
│   │   ├── workers/        # Workers assíncronos
│   │   └── queues/         # RabbitMQ producers/consumers
│   ├── tests/              # Testes
│   ├── scripts/            # Scripts utilitários
│   └── docker/             # Dockerfiles
├── frontend/               # Frontend React
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── pages/          # Páginas
│   │   ├── hooks/          # Custom hooks
│   │   ├── contexts/       # Context providers
│   │   ├── services/       # API clients
│   │   ├── types/          # TypeScript types
│   │   └── utils/          # Utilitários
│   └── tests/              # Testes
├── design/                 # Diagramas e designs
└── docker-compose.yml      # Orquestração completa
```

## 🧪 Testes

### Backend

- **Unitários**: Testes de serviços, models e utils
- **Integração**: Testes de API e agentes
- **E2E**: Testes de workflows completos
- **Coverage mínimo**: 80%

```bash
cd backend
pytest                          # Todos os testes
pytest tests/unit              # Apenas unitários
pytest tests/integration       # Apenas integração
pytest --cov=app               # Com coverage
```

### Frontend

- **Unitários**: Testes de componentes e hooks
- **Integração**: Testes de páginas completas
- **E2E**: Testes com Playwright
- **Coverage mínimo**: 70%

```bash
cd frontend
npm test                       # Todos os testes
npm test:coverage              # Com coverage
npm run test:e2e               # E2E com Playwright
```

## 📊 Monitoramento

### Métricas

- **Prometheus**: Coleta de métricas (latência, throughput, erros)
- **Grafana**: Visualização de dashboards
- **P95/P99**: Percentis de latência rastreados

### Logging

- **Structured logging**: JSON logs com contexto
- **Log levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Trace IDs**: Rastreamento de requisições

## 🔧 Configuração

### Variáveis de Ambiente

#### Backend (.env)

```env
DATABASE_URL=postgresql://plexo:password@localhost:5432/plexo
REDIS_URL=redis://localhost:6379/0
RABBITMQ_URL=amqp://plexo:password@localhost:5672/
XMPP_SERVER=localhost
XMPP_PORT=5222
ENVIRONMENT=development
LOG_LEVEL=INFO
```

#### Frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código

#### Backend

- **Formatter**: Black
- **Linter**: Ruff
- **Type checker**: MyPy
- **Docstrings**: Google style

```bash
black app/
ruff check app/
mypy app/
```

#### Frontend

- **Formatter**: Prettier
- **Linter**: ESLint
- **Type checker**: TypeScript

```bash
npm run format
npm run lint
npm run type-check
```

## 📝 Documentação

- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc
- **Backend README**: [backend/README.md](backend/README.md)
- **Frontend README**: [frontend/README.md](frontend/README.md)
- **Testing Guide**: [frontend/tests/README.md](frontend/tests/README.md)

## 🏛️ Arquitetura Detalhada

### Backend

```
Controllers (API) → Services → Models (Database)
                  ↓
              Agents (SPADE)
                  ↓
            Chains (LangChain)
                  ↓
              Workers (RabbitMQ)
```

### Comunicação entre Agentes

- **XMPP (SPADE)**: Comunicação síncrona entre agentes
- **RabbitMQ**: Tarefas assíncronas e background jobs
- **WebSocket**: Comunicação real-time com frontend

### Memória

- **Curto prazo**: Redis (sessões, cache)
- **Longo prazo**: PostgreSQL (dados relacionais) + KuzuDB (embeddings)

## 🔐 Segurança

- **Authentication**: JWT tokens
- **Authorization**: Role-based access control (RBAC)
- **Rate limiting**: Por IP e por usuário
- **CORS**: Configurado para origens permitidas
- **Input validation**: Pydantic schemas

## 📈 Performance

- **Async/await**: Operações I/O não-bloqueantes
- **Connection pooling**: PostgreSQL e Redis
- **Caching**: Redis para dados frequentes
- **Lazy loading**: Componentes React
- **Code splitting**: Vite chunks

## 🐛 Troubleshooting

### Backend não inicia

```bash
# Verificar logs
docker-compose logs backend

# Verificar banco de dados
docker-compose exec postgres psql -U plexo -d plexo

# Recriar containers
docker-compose down -v
docker-compose up -d
```

### Frontend não conecta ao backend

```bash
# Verificar variáveis de ambiente
cat frontend/.env

# Verificar se backend está rodando
curl http://localhost:8000/health

# Verificar logs do frontend
docker-compose logs frontend
```

### Testes falhando

```bash
# Limpar cache
cd backend && pytest --cache-clear
cd frontend && npm test -- --clearCache

# Reinstalar dependências
cd backend && poetry install
cd frontend && npm ci
```

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Seu Nome** - *Trabalho Inicial* - [seu-usuario](https://github.com/seu-usuario)

## 🙏 Agradecimentos

- FastAPI pela excelente framework
- LangChain pela orquestração de agentes
- SPADE pela comunicação XMPP
- Comunidade open source
