# 0013. SPADE + LangGraph Orchestration Pattern

Data: 2026-03-29

Status: Aceito

## Contexto

O sistema Plexo precisa coordenar agentes SPADE (comunicação XMPP de baixa latência) com LangGraph (execução de tarefas complexas). Os requisitos incluem:

- Comunicação rápida entre agentes para discussão e tomada de decisão
- Execução de tarefas complexas de escrita de código
- Monitoramento em tempo real do progresso
- Múltiplos agentes analisando e complementando o trabalho
- Baixa latência na orquestração

## Decisão

Decidimos implementar um **padrão de orquestração híbrido SPADE + LangGraph**:

### 1. Arquitetura de Orquestração

**Grupo SPADE (Discussão e Consenso)**
- Coordinator Agent: Orquestra discussão e delegação
- Coder Agent: Implementação e monitoramento do graph
- Critic Agent: Análise crítica e detecção de falhas
- Analyst Agent: Proposição de alternativas

**LangGraph (Execução)**
- Nodes de execução: write_code, test_code, review_code, fix_issues, deploy
- Nodes de monitoramento: track_progress, analyze_execution, propose_alternatives, validate_alternatives

### 2. Padrões de Colaboração

**Padrão A: Discussão e Consenso (SPADE)**
- Agentes discutem tarefa no grupo XMPP
- Cada um contribui com perspectiva única
- Consenso é alcançado via debate estruturado
- Decisão é documentada

**Padrão B: Delegação para LangGraph**
- Tarefas complexas são delegadas para graph
- Coder cria graph com nodes específicos
- Graph executa com monitoramento paralelo
- Agentes acompanham progresso em tempo real

**Padrão C: Monitoramento em Tempo Real**
- Tracker Agent: Rastreia progresso do graph
- Analyzer Agent: Analisa execução em tempo real
- Critic Agent: Identifica falhas e problemas
- Analyst Agent: Propõe alternativas
- Feedback é enviado para graph durante execução

### 3. Agent Roles na Orquestração

**Coordinator Agent**
- Inicia discussão sobre tarefa
- Facilita consenso entre agentes
- Delega para LangGraph quando necessário
- Monitora progresso geral

**Coder Agent**
- Participa de discussões técnicas
- Cria LangGraphs para tarefas complexas
- Executa nodes do graph
- Trackeia progresso em tempo real
- Aplica correções sugeridas

**Critic Agent**
- Analisa código sendo escrito
- Identifica bugs e problemas
- Sugere melhorias
- Valida alternativas propostas
- Documenta decisões críticas

**Analyst Agent**
- Propõe soluções alternativas
- Analisa trade-offs
- Avalia viabilidade de sugestões
- Cria relatórios de análise
- Compartilha conhecimento

### 4. LangGraph Structure

```python
class PlexoAgentGraph:
    def __init__(self):
        self.graph = StateGraph(AgentState)
        self._setup_nodes()
        self._setup_edges()
    
    def _setup_nodes(self):
        # Nodes de execução
        self.graph.add_node("write_code", self.write_code_node)
        self.graph.add_node("test_code", self.test_code_node)
        self.graph.add_node("review_code", self.review_code_node)
        self.graph.add_node("fix_issues", self.fix_issues_node)
        self.graph.add_node("deploy", self.deploy_node)
        
        # Nodes de monitoramento
        self.graph.add_node("track_progress", self.track_progress_node)
        self.graph.add_node("analyze_execution", self.analyze_execution_node)
        self.graph.add_node("propose_alternatives", self.propose_alternatives_node)
        self.graph.add_node("validate_alternatives", self.validate_alternatives_node)
```

### 5. Real-time Monitoring Protocol

```python
class GraphMonitor:
    def __init__(self, graph, spade_group):
        self.graph = graph
        self.spade_group = spade_group
    
    async def monitor_execution(self):
        while self.graph.is_running():
            progress = await self.get_progress()
            analysis = await self.analyze_execution()
            await self.report_to_spade_group(progress, analysis)
            await asyncio.sleep(1)
```

### 6. Communication Flow

**Fase 1: Discussão e Consenso (SPADE)**
- Coordinator inicia discussão
- Agentes contribuem com opiniões
- Debate facilitado
- Consenso alcançado

**Fase 2: Criação do Graph**
- Coder cria LangGraph baseado no consenso
- Nodes configurados para tarefa específica
- Monitoramento preparado

**Fase 3: Execução com Monitoramento**
- Graph executa em background
- Monitoramento roda em paralelo
- Agentes acompanham progresso
- Feedback é aplicado em tempo real

**Fase 4: Revisão e Consolidação (SPADE)**
- Resultado revisado pelo grupo
- Decisões finais documentadas
- Aprendizados compartilhados

### 7. Latency Optimization

**Técnicas de Baixa Latência:**
1. Comunicação SPADE direta (XMPP, < 100ms)
2. Execução paralela de graph e monitoramento
3. Cache de estado em memória
4. Batching de updates (agrupa mensagens)

```python
class LowLatencyOrchestrator:
    async def orchestrate(self, task):
        # Cria grupo SPADE
        spade_muc = await self.create_spade_group(task.agents)
        
        # Executa com monitoramento paralelo
        execution_task = asyncio.create_task(graph.execute())
        monitor_task = asyncio.create_task(monitor.monitor_execution())
        
        result = await execution_task
        await monitor_task
        return result
```

## Consequências

### Positivas
- **Baixa latência**: Comunicação SPADE é rápida (< 100ms)
- **Escalabilidade**: Múltiplos agentes podem monitorar simultaneamente
- **Qualidade**: Análise crítica em tempo real melhora código
- **Flexibilidade**: Combina discussão colaborativa com execução automatizada
- **Resiliência**: Falhas são detectadas e corrigidas rapidamente

### Negativas
- **Complexidade**: Sistema mais complexo de implementar e manter
- **Coordenação**: Sincronização entre SPADE e LangGraph requer cuidado
- **Overhead**: Monitoramento em tempo real tem custo de recursos
- **Debugging**: Fluxos distribuídos são mais difíceis de debugar

### Mitigações
- Logging detalhado de todas as comunicações
- Métricas de latência e throughput
- Testes extensivos de cenários de orquestração
- Documentação clara de fluxos e padrões

## Alternativas Consideradas

### 1. Apenas SPADE (Rejeitada)
- Só comunicação, sem execução de graphs
- Problema: Não suporta tarefas complexas de escrita

### 2. Apenas LangGraph (Rejeitada)
- Só execução, sem discussão entre agentes
- Problema: Sem colaboração, sem análise crítica em tempo real

### 3. Comunicação HTTP (Rejeitada)
- API REST para comunicação entre agentes
- Problema: Alta latência, inadequado para tempo real

## Métricas de Sucesso

- **Latência de comunicação**: < 100ms entre agentes SPADE
- **Tempo de consenso**: < 30 segundos para decisões do grupo
- **Throughput do graph**: > 10 nodes processados por segundo
- **Taxa de detecção de erros**: > 95% durante execução
- **Satisfação dos agentes**: Feedback positivo sobre colaboração

## Próximos Passos

1. Implementar SPADEGroup para comunicação XMPP
2. Criar PlexoAgentGraph com nodes de monitoramento
3. Implementar GraphMonitor para tempo real
4. Criar OrchestrationFlow para coordenação
5. Implementar LowLatencyOrchestrator com batching
6. Otimizar comunicação paralela
7. Testar com cenários complexos
8. Documentar padrões de uso para desenvolvedores
