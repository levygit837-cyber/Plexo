# Architecture Overview

Visão geral da arquitetura do sistema multi-agentes Plexo.

## Stack Tecnológico

### Backend
- FastAPI (Web Framework)
- LangChain/LangGraph (Agent Orchestration)
- SPADE (Agent Communication)
- PostgreSQL (Relational DB)
- KuzuDB (Vector DB)
- Redis (Cache)
- RabbitMQ (Message Queue)
- ejabberd (XMPP Server)

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS

### Infrastructure
- Docker & Docker Compose
- Prometheus (Metrics)
- Grafana (Dashboards)

## Camadas

### 1. Presentation Layer
- React UI
- WebSocket Client
- API Client

### 2. API Layer
- FastAPI Endpoints
- Pydantic Validation
- Authentication/Authorization
- WebSocket Server

### 3. Business Logic Layer
- Agent Services
- Task Services
- LangChain Chains
- SPADE Agents

### 4. Data Layer
- PostgreSQL (structured data)
- KuzuDB (embeddings)
- Redis (cache, sessions)

### 5. Infrastructure Layer
- RabbitMQ (async tasks)
- ejabberd (agent communication)
- Prometheus (monitoring)

## Padrões Arquiteturais

- **Layered Architecture**: Separação clara de responsabilidades
- **Event-Driven**: Comunicação assíncrona via eventos
- **CQRS**: Separação de commands e queries
- **Repository Pattern**: Abstração de acesso a dados
- **Service Layer**: Lógica de negócio isolada

## Escalabilidade

- API: Horizontal scaling com load balancer
- Workers: Múltiplos workers por fila
- Agents: Distribuídos via XMPP
- Database: Read replicas
- Cache: Redis cluster

## Segurança

- JWT Authentication
- RBAC Authorization
- Rate Limiting
- CORS Configuration
- Input Validation
- TLS/SSL

## Monitoramento

- Prometheus metrics
- Grafana dashboards
- Structured logging
- Distributed tracing
- Health checks
