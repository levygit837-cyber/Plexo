# 0003. Use LangChain for Agent Orchestration

Data: 2026-01-17

Status: Aceito

## Contexto

O sistema Plexo precisa orquestrar múltiplos agentes inteligentes que interagem com LLMs (Large Language Models) para executar tarefas complexas. Os agentes precisam:

- Integrar com múltiplos providers de LLMs (OpenAI, Anthropic, etc.)
- Criar workflows complexos e stateful
- Gerenciar memória e contexto entre interações
- Usar ferramentas customizadas
- Ter observabilidade e debugging
- Suportar chains e graphs de execução

## Decisão

Decidimos usar **LangChain** e **LangGraph** para orquestração de agentes inteligentes.

### Razões

1. **Abstração de LLMs**: Interface unificada para múltiplos providers (OpenAI, Anthropic, Cohere, etc.)
2. **LangGraph**: Framework para criar workflows stateful com grafos de execução
3. **Chains**: Composição de múltiplas chamadas de LLM em sequências lógicas
4. **Tools**: Biblioteca extensível de ferramentas e fácil criação de custom tools
5. **Memory Management**: Gerenciamento automático de contexto e histórico
6. **Observabilidade**: Integração com LangSmith para debugging e monitoring
7. **Comunidade**: Ecossistema rico com templates e integrações
8. **Agents**: Suporte nativo a diferentes tipos de agentes (ReAct, Plan-and-Execute, etc.)

## Consequências

### Positivas

- Desenvolvimento mais rápido com abstrações de alto nível
- Fácil troca entre diferentes providers de LLM
- Workflows complexos com LangGraph (loops, condicionais, paralelismo)
- Reutilização de ferramentas e chains
- Debugging facilitado com LangSmith
- Gerenciamento automático de tokens e custos
- Suporte a streaming de respostas
- Integração com vector stores para RAG (Retrieval-Augmented Generation)

### Negativas

- Dependência de biblioteca externa em rápida evolução
- Curva de aprendizado para LangGraph
- Overhead de abstração pode impactar performance em casos simples
- Versionamento pode quebrar compatibilidade
- Documentação às vezes desatualizada devido a mudanças rápidas

## Alternativas Consideradas

### LlamaIndex

- **Prós**: Focado em RAG, ótima integração com vector stores
- **Contras**: Menos flexível para workflows complexos, comunidade menor
- **Rejeitado**: LangChain oferece mais flexibilidade para nosso caso de uso

### Semantic Kernel (Microsoft)

- **Prós**: Suporte a C# e Python, integração com Azure
- **Contras**: Comunidade menor, menos maduro, focado em Azure
- **Rejeitado**: Preferimos solução mais agnóstica de cloud

### Implementação Custom

- **Prós**: Controle total, sem dependências externas
- **Contras**: Muito trabalho, reinventar a roda, sem observabilidade
- **Rejeitado**: Tempo de desenvolvimento seria muito maior

### Haystack

- **Prós**: Focado em NLP pipelines, boa documentação
- **Contras**: Menos flexível para agentes, comunidade menor
- **Rejeitado**: LangChain tem melhor suporte a agentes

## Implementação

### Estrutura

```
backend/app/langchain/
├── chains/          # Chains customizadas
│   └── base_chain.py
├── graphs/          # LangGraph workflows
│   └── agent_graph.py
└── tools/           # Ferramentas customizadas
    ├── base_tool.py
    └── custom_tools.py
```

### Exemplo de Uso

```python
from langchain.chat_models import ChatOpenAI
from langgraph.graph import StateGraph

# Definir estado do agente
class AgentState(TypedDict):
    messages: List[BaseMessage]
    next_action: str

# Criar grafo de execução
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tools_node)
graph.add_edge("agent", "tools")
graph.add_conditional_edges("tools", should_continue)

# Executar workflow
result = graph.invoke({"messages": [HumanMessage(content="Hello")]})
```

### Integração com SPADE

LangChain será usado **dentro** dos agentes SPADE para processamento de linguagem natural:

```python
class PlexoAgent(Agent):
    async def setup(self):
        self.chain = create_agent_chain()
    
    class MessageBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            # Processar com LangChain
            response = await self.agent.chain.ainvoke(msg.body)
            await self.send(response)
```

## Referências

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangSmith](https://smith.langchain.com/)
- [LangChain Templates](https://github.com/langchain-ai/langchain/tree/master/templates)
