# Plexo Documentation

Documentação completa do sistema multi-agentes Plexo.

## 📚 Índice

### [Architecture](./architecture/)

Documentação da arquitetura do sistema:

- [Overview](./architecture/overview.md) - Visão geral da arquitetura
- [Backend Architecture](./architecture/backend.md) - Arquitetura do backend
- [Frontend Architecture](./architecture/frontend.md) - Arquitetura do frontend
- [Diagrams](./architecture/diagrams/) - Diagramas de arquitetura

### [ADR - Architecture Decision Records](./adr/)

Registros de decisões arquiteturais:

- [ADR Template](./adr/README.md) - Template para novos ADRs
- [0001 - Use FastAPI](./adr/0001-use-fastapi.md)
- [0002 - Use SPADE for Agent Communication](./adr/0002-use-spade-xmpp.md)
- [0003 - Use LangChain for Agent Orchestration](./adr/0003-use-langchain.md)
- [0004 - Use PostgreSQL and KuzuDB](./adr/0004-use-postgresql-kuzudb.md)
- [0005 - Use RabbitMQ for Async Tasks](./adr/0005-use-rabbitmq.md)

### [Features](./features/)

Documentação de funcionalidades:

- [Agents System](./features/agents.md) - Sistema de agentes
- [Tasks System](./features/tasks.md) - Sistema de tarefas
- [Messaging System](./features/messaging.md) - Sistema de mensagens
- [Memory System](./features/memory.md) - Sistema de memória
- [Monitoring](./features/monitoring.md) - Sistema de monitoramento

### [API Documentation](./api/)

Documentação da API REST:

- [API Overview](./api/README.md) - Visão geral da API
- [Endpoints](./api/endpoints.md) - Lista completa de endpoints
- [Schemas](./api/schemas.md) - Schemas Pydantic
- [Authentication](./api/authentication.md) - Autenticação e autorização

### [Deployment](./deployment/)

Guias de deployment:

- [Docker Deployment](./deployment/docker.md) - Deploy com Docker
- [Production Deployment](./deployment/production.md) - Deploy em produção
- [Monitoring Setup](./deployment/monitoring.md) - Configuração de monitoramento
- [Scaling](./deployment/scaling.md) - Estratégias de escalabilidade

### [Development](./development/)

Guias de desenvolvimento:

- [Setup Guide](./development/setup.md) - Configuração do ambiente
- [Contributing](./development/contributing.md) - Como contribuir
- [Testing Guide](./development/testing.md) - Guia de testes
- [Code Standards](./development/code-standards.md) - Padrões de código

### [Guides](./guides/)

Guias diversos:

- [Getting Started](./guides/getting-started.md) - Primeiros passos
- [Troubleshooting](./guides/troubleshooting.md) - Resolução de problemas
- [FAQ](./guides/faq.md) - Perguntas frequentes

## 🔍 Busca Rápida

### Por Tópico

- **Arquitetura**: [architecture/](./architecture/)
- **Decisões**: [adr/](./adr/)
- **Features**: [features/](./features/)
- **API**: [api/](./api/)
- **Deploy**: [deployment/](./deployment/)
- **Dev**: [development/](./development/)

### Por Persona

#### Desenvolvedor Novo
1. [Getting Started](./guides/getting-started.md)
2. [Setup Guide](./development/setup.md)
3. [Architecture Overview](./architecture/overview.md)
4. [Contributing](./development/contributing.md)

#### Desenvolvedor Experiente
1. [Architecture](./architecture/)
2. [ADRs](./adr/)
3. [API Documentation](./api/)
4. [Code Standards](./development/code-standards.md)

#### DevOps/SRE
1. [Docker Deployment](./deployment/docker.md)
2. [Production Deployment](./deployment/production.md)
3. [Monitoring Setup](./deployment/monitoring.md)
4. [Scaling](./deployment/scaling.md)

#### Product Manager
1. [Features](./features/)
2. [Architecture Overview](./architecture/overview.md)
3. [ADRs](./adr/)

## 📝 Contribuindo com a Documentação

Para adicionar ou atualizar documentação:

1. Siga o template apropriado (ADR, Feature, etc.)
2. Use Markdown para formatação
3. Adicione diagramas quando necessário (Mermaid ou imagens)
4. Atualize este README.md com links para novos documentos
5. Mantenha a documentação sincronizada com o código

## 🔄 Versionamento

A documentação segue o versionamento do projeto. Cada release deve ter sua documentação atualizada.

## 📧 Contato

Para dúvidas sobre a documentação, abra uma issue no repositório.
