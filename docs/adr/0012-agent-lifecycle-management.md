# 0012. Agent Lifecycle Management

Data: 2026-03-29

Status: Aceito

## Contexto

O sistema multi-agentes Plexo precisa gerenciar o ciclo de vida completo dos agentes para:

- Criar agentes dinamicamente conforme necessário
- Pausar e retomar agentes sem perder estado
- Destruir agentes que não são mais necessários
- Atualizar configuração de agentes em runtime
- Monitorar saúde e recursos de agentes
- Escalar número de agentes baseado em demanda

## Decisão

Decidimos implementar um **sistema de gerenciamento de ciclo de vida** com os seguintes estados e transições:

### 1. Agent States

```python
class AgentState(Enum):
    """Estados do ciclo de vida de um agente"""
    # Estados iniciais
    CREATED = "created"              # Agente criado mas não inicializado
    INITIALIZING = "initializing"    # Inicializando componentes
    
    # Estados operacionais
    IDLE = "idle"                    # Disponível para trabalho
    BUSY = "busy"                    # Processando tarefa
    PAUSED = "paused"                # Pausado pelo usuário ou sistema
    
    # Estados de erro
    ERROR = "error"                  # Em estado de erro
    RECOVERING = "recovering"        # Recuperando de erro
    
    # Estados finais
    STOPPING = "stopping"            # Parando graciosamente
    STOPPED = "stopped"              # Parado
    DESTROYED = "destroyed"          # Destruído, recursos liberados
```

### 2. State Transitions

```python
# Transições válidas
VALID_TRANSITIONS = {
    AgentState.CREATED: [AgentState.INITIALIZING, AgentState.DESTROYED],
    AgentState.INITIALIZING: [AgentState.IDLE, AgentState.ERROR],
    AgentState.IDLE: [AgentState.BUSY, AgentState.PAUSED, AgentState.STOPPING],
    AgentState.BUSY: [AgentState.IDLE, AgentState.PAUSED, AgentState.ERROR, AgentState.STOPPING],
    AgentState.PAUSED: [AgentState.IDLE, AgentState.STOPPING],
    AgentState.ERROR: [AgentState.RECOVERING, AgentState.STOPPING],
    AgentState.RECOVERING: [AgentState.IDLE, AgentState.ERROR, AgentState.STOPPING],
    AgentState.STOPPING: [AgentState.STOPPED],
    AgentState.STOPPED: [AgentState.IDLE, AgentState.DESTROYED],
    AgentState.DESTROYED: []  # Estado final, sem transições
}
```

### 3. Agent Lifecycle Manager

```python
class AgentLifecycleManager:
    """Gerencia ciclo de vida de agentes"""
    
    def __init__(
        self,
        agent_registry: AgentRegistry,
        resource_manager: ResourceManager
    ):
        self.registry = agent_registry
        self.resources = resource_manager
        self.agents: Dict[str, ManagedAgent] = {}
        self.state_machine = AgentStateMachine()
    
    async def create_agent(
        self,
        agent_config: AgentConfig
    ) -> ManagedAgent:
        """Cria novo agente"""
        # Verifica recursos disponíveis
        if not await self.resources.can_allocate(agent_config):
            raise ResourceError("Insufficient resources")
        
        # Cria agente
        agent = ManagedAgent(config=agent_config)
        
        # Aloca recursos
        await self.resources.allocate(agent.id, agent_config.resources)
        
        # Registra agente
        self.agents[agent.id] = agent
        await self.registry.register(agent)
        
        # Transição para INITIALIZING
        await self.state_machine.transition(
            agent, AgentState.INITIALIZING
        )
        
        # Inicializa agente
        await self._initialize_agent(agent)
        
        return agent
    
    async def start_agent(self, agent_id: str) -> bool:
        """Inicia agente"""
        agent = self.agents.get(agent_id)
        if not agent:
            raise AgentNotFoundError(f"Agent {agent_id} not found")
        
        # Verifica se pode iniciar
        if agent.state not in [AgentState.CREATED, AgentState.STOPPED]:
            raise InvalidStateError(
                f"Cannot start agent in state {agent.state}"
            )
        
        # Inicializa se necessário
        if agent.state == AgentState.CREATED:
            await self._initialize_agent(agent)
        
        # Transição para IDLE
        await self.state_machine.transition(agent, AgentState.IDLE)
        
        # Inicia agente
        await agent.start()
        
        return True
    
    async def pause_agent(self, agent_id: str) -> bool:
        """Pausa agente"""
        agent = self.agents.get(agent_id)
        if not agent:
            raise AgentNotFoundError(f"Agent {agent_id} not found")
        
        # Verifica se pode pausar
        if agent.state not in [AgentState.IDLE, AgentState.BUSY]:
            raise InvalidStateError(
                f"Cannot pause agent in state {agent.state}"
            )
        
        # Salva estado atual
        await self._save_agent_state(agent)
        
        # Transição para PAUSED
        await self.state_machine.transition(agent, AgentState.PAUSED)
        
        # Pausa agente
        await agent.pause()
        
        return True
    
    async def resume_agent(self, agent_id: str) -> bool:
        """Resume agente pausado"""
        agent = self.agents.get(agent_id)
        if not agent:
            raise AgentNotFoundError(f"Agent {agent_id} not found")
        
        # Verifica se pode resumir
        if agent.state != AgentState.PAUSED:
            raise InvalidStateError(
                f"Cannot resume agent in state {agent.state}"
            )
        
        # Restaura estado
        await self._restore_agent_state(agent)
        
        # Transição para IDLE
        await self.state_machine.transition(agent, AgentState.IDLE)
        
        # Resume agente
        await agent.resume()
        
        return True
    
    async def stop_agent(
        self,
        agent_id: str,
        graceful: bool = True
    ) -> bool:
        """Para agente"""
        agent = self.agents.get(agent_id)
        if not agent:
            raise AgentNotFoundError(f"Agent {agent_id} not found")
        
        # Verifica se pode parar
        if agent.state in [AgentState.STOPPED, AgentState.DESTROYED]:
            return True  # Já parado
        
        # Transição para STOPPING
        await self.state_machine.transition(agent, AgentState.STOPPING)
        
        # Para agente
        if graceful:
            await agent.stop_gracefully()
        else:
            await agent.stop_immediately()
        
        # Transição para STOPPED
        await self.state_machine.transition(agent, AgentState.STOPPED)
        
        return True
    
    async def destroy_agent(self, agent_id: str) -> bool:
        """Destrói agente e libera recursos"""
        agent = self.agents.get(agent_id)
        if not agent:
            raise AgentNotFoundError(f"Agent {agent_id} not found")
        
        # Para agente se necessário
        if agent.state not in [AgentState.STOPPED, AgentState.DESTROYED]:
            await self.stop_agent(agent_id, graceful=False)
        
        # Transição para DESTROYED
        await self.state_machine.transition(agent, AgentState.DESTROYED)
        
        # Libera recursos
        await self.resources.release(agent.id)
        
        # Remove do registro
        await self.registry.unregister(agent)
        del self.agents[agent_id]
        
        return True
    
    async def update_agent_config(
        self,
        agent_id: str,
        new_config: AgentConfig
    ) -> bool:
        """Atualiza configuração de agente"""
        agent = self.agents.get(agent_id)
        if not agent:
            raise AgentNotFoundError(f"Agent {agent_id} not found")
        
        # Verifica se pode atualizar
        if agent.state == AgentState.BUSY:
            raise InvalidStateError(
                "Cannot update config while agent is busy"
            )
        
        # Pausa agente se necessário
        was_running = agent.state == AgentState.IDLE
        if was_running:
            await self.pause_agent(agent_id)
        
        # Atualiza configuração
        agent.config = new_config
        
        # Realloca recursos se necessário
        await self.resources.reallocate(agent.id, new_config.resources)
        
        # Resume agente se estava rodando
        if was_running:
            await self.resume_agent(agent_id)
        
        return True
```

### 4. Managed Agent

```python
class ManagedAgent:
    """Agente gerenciado pelo lifecycle manager"""
    
    def __init__(self, config: AgentConfig):
        self.id = generate_id()
        self.config = config
        self.state = AgentState.CREATED
        self.created_at = datetime.now()
        self.last_state_change = datetime.now()
        self.state_history: List[StateTransition] = []
        self.saved_state: Optional[Dict[str, Any]] = None
        self.health: AgentHealth = AgentHealth()
        self.metrics: AgentMetrics = AgentMetrics()
    
    async def start(self):
        """Inicia agente"""
        # Cria instância do agente SPADE
        self.spade_agent = PlexoAgent(
            jid=self.config.jid,
            password=self.config.password
        )
        
        # Configura comportamentos
        for behavior in self.config.behaviors:
            self.spade_agent.add_behaviour(behavior)
        
        # Inicia agente
        await self.spade_agent.start()
        
        # Inicia monitoramento de saúde
        asyncio.create_task(self._monitor_health())
    
    async def pause(self):
        """Pausa agente"""
        # Pausa comportamentos
        for behavior in self.spade_agent.behaviours:
            behavior.pause()
        
        # Atualiza métricas
        self.metrics.paused_at = datetime.now()
    
    async def resume(self):
        """Resume agente"""
        # Resume comportamentos
        for behavior in self.spade_agent.behaviours:
            behavior.resume()
        
        # Atualiza métricas
        self.metrics.resumed_at = datetime.now()
    
    async def stop_gracefully(self):
        """Para agente graciosamente"""
        # Aguarda tarefas em andamento
        await self._wait_for_tasks()
        
        # Para agente
        await self.spade_agent.stop()
    
    async def stop_immediately(self):
        """Para agente imediatamente"""
        await self.spade_agent.stop()
    
    async def _monitor_health(self):
        """Monitora saúde do agente"""
        while self.state not in [AgentState.STOPPED, AgentState.DESTROYED]:
            # Verifica saúde
            health_status = await self._check_health()
            self.health.update(health_status)
            
            # Atualiza métricas
            self.metrics.update()
            
            # Verifica se precisa de recovery
            if self.health.status == HealthStatus.CRITICAL:
                await self._trigger_recovery()
            
            await asyncio.sleep(10)  # Verifica a cada 10 segundos
```

### 5. Agent Health Monitoring

```python
class AgentHealth:
    """Monitora saúde de um agente"""
    
    def __init__(self):
        self.status = HealthStatus.HEALTHY
        self.last_check = datetime.now()
        self.checks: Dict[str, HealthCheck] = {}
        self.issues: List[HealthIssue] = []
    
    async def check(self) -> HealthStatus:
        """Executa verificações de saúde"""
        checks = [
            self._check_memory_usage(),
            self._check_cpu_usage(),
            self._check_connection(),
            self._check_response_time(),
            self._check_error_rate()
        ]
        
        results = await asyncio.gather(*checks, return_exceptions=True)
        
        # Analisa resultados
        issues = []
        for result in results:
            if isinstance(result, HealthIssue):
                issues.append(result)
        
        self.issues = issues
        self.last_check = datetime.now()
        
        # Determina status geral
        if any(issue.severity == 'critical' for issue in issues):
            self.status = HealthStatus.CRITICAL
        elif any(issue.severity == 'warning' for issue in issues):
            self.status = HealthStatus.WARNING
        else:
            self.status = HealthStatus.HEALTHY
        
        return self.status
    
    async def _check_memory_usage(self) -> Optional[HealthIssue]:
        """Verifica uso de memória"""
        memory_percent = psutil.virtual_memory().percent
        
        if memory_percent > 90:
            return HealthIssue(
                type='memory',
                severity='critical',
                message=f'High memory usage: {memory_percent}%'
            )
        elif memory_percent > 75:
            return HealthIssue(
                type='memory',
                severity='warning',
                message=f'Elevated memory usage: {memory_percent}%'
            )
        
        return None
    
    async def _check_response_time(self) -> Optional[HealthIssue]:
        """Verifica tempo de resposta"""
        response_time = self._measure_response_time()
        
        if response_time > 5.0:  # 5 segundos
            return HealthIssue(
                type='performance',
                severity='critical',
                message=f'Slow response time: {response_time}s'
            )
        elif response_time > 2.0:  # 2 segundos
            return HealthIssue(
                type='performance',
                severity='warning',
                message=f'Elevated response time: {response_time}s'
            )
        
        return None
```

### 6. Resource Management

```python
class ResourceManager:
    """Gerencia recursos dos agentes"""
    
    def __init__(self, total_resources: ResourcePool):
        self.total = total_resources
        self.allocated: Dict[str, ResourceAllocation] = {}
        self.available = total_resources.copy()
    
    async def can_allocate(
        self,
        config: AgentConfig
    ) -> bool:
        """Verifica se recursos estão disponíveis"""
        required = config.resources
        
        return (
            self.available.cpu >= required.cpu and
            self.available.memory >= required.memory and
            self.available.storage >= required.storage
        )
    
    async def allocate(
        self,
        agent_id: str,
        resources: ResourceRequirements
    ) -> ResourceAllocation:
        """Aloca recursos para agente"""
        if not await self.can_allocate_from_resources(resources):
            raise ResourceError("Insufficient resources")
        
        # Cria alocação
        allocation = ResourceAllocation(
            agent_id=agent_id,
            cpu=resources.cpu,
            memory=resources.memory,
            storage=resources.storage,
            allocated_at=datetime.now()
        )
        
        # Atualiza disponíveis
        self.available.cpu -= resources.cpu
        self.available.memory -= resources.memory
        self.available.storage -= resources.storage
        
        # Registra alocação
        self.allocated[agent_id] = allocation
        
        return allocation
    
    async def release(self, agent_id: str):
        """Libera recursos de agente"""
        allocation = self.allocated.get(agent_id)
        if not allocation:
            return
        
        # Devolve recursos
        self.available.cpu += allocation.cpu
        self.available.memory += allocation.memory
        self.available.storage += allocation.storage
        
        # Remove alocação
        del self.allocated[agent_id]
    
    async def reallocate(
        self,
        agent_id: str,
        new_resources: ResourceRequirements
    ) -> ResourceAllocation:
        """Realoca recursos de agente"""
        # Libera recursos atuais
        await self.release(agent_id)
        
        # Aloca novos recursos
        return await self.allocate(agent_id, new_resources)
```

### 7. Agent Scaling

```python
class AgentScaler:
    """Escala número de agentes baseado em demanda"""
    
    def __init__(
        self,
        lifecycle_manager: AgentLifecycleManager,
        resource_manager: ResourceManager
    ):
        self.lifecycle = lifecycle_manager
        self.resources = resource_manager
        self.min_agents = 1
        self.max_agents = 10
        self.scale_up_threshold = 0.8  # 80% de utilização
        self.scale_down_threshold = 0.3  # 30% de utilização
    
    async def evaluate_scaling(self):
        """Avalia necessidade de scaling"""
        # Calcula utilização atual
        utilization = self._calculate_utilization()
        
        # Verifica se precisa escalar
        if utilization > self.scale_up_threshold:
            await self._scale_up()
        elif utilization < self.scale_down_threshold:
            await self._scale_down()
    
    def _calculate_utilization(self) -> float:
        """Calcula utilização do sistema"""
        agents = list(self.lifecycle.agents.values())
        if not agents:
            return 0.0
        
        busy_agents = sum(
            1 for agent in agents
            if agent.state == AgentState.BUSY
        )
        
        return busy_agents / len(agents)
    
    async def _scale_up(self):
        """Aumenta número de agentes"""
        current_count = len(self.lifecycle.agents)
        
        if current_count >= self.max_agents:
            return  # Já no máximo
        
        # Verifica recursos disponíveis
        if not await self.resources.can_allocate(self._get_agent_config()):
            return  # Sem recursos
        
        # Cria novo agente
        await self.lifecycle.create_agent(self._get_agent_config())
        
        logger.info(f"Scaled up to {current_count + 1} agents")
    
    async def _scale_down(self):
        """Diminui número de agentes"""
        current_count = len(self.lifecycle.agents)
        
        if current_count <= self.min_agents:
            return  # Já no mínimo
        
        # Encontra agente idle para remover
        idle_agents = [
            agent for agent in self.lifecycle.agents.values()
            if agent.state == AgentState.IDLE
        ]
        
        if not idle_agents:
            return  # Sem agentes idle
        
        # Remove agente idle mais antigo
        agent_to_remove = min(idle_agents, key=lambda a: a.created_at)
        await self.lifecycle.destroy_agent(agent_to_remove.id)
        
        logger.info(f"Scaled down to {current_count - 1} agents")
```

## Consequências

### Positivas
- **Controle granular**: Controle completo sobre ciclo de vida
- **Persistência**: Estado preservado entre pausas/resumes
- **Recuperação**: Agentes podem se recuperar de erros
- **Escalabilidade**: Sistema escala automaticamente
- **Monitoramento**: Saúde e recursos monitorados
- **Flexibilidade**: Configuração atualizada em runtime

### Negativas
- **Complexidade**: Sistema mais complexo de gerenciar
- **Overhead**: Custo de gerenciamento de estado
- **Dependências**: Mais componentes para coordenar
- **Debugging**: Mais difícil debugar estados

### Mitigações
- **Logging detalhado**: Log de todas as transições de estado
- **Métricas**: Monitorar performance do gerenciamento
- **Testes**: Testar todos os cenários de transição
- **Documentação**: Documentar comportamento esperado

## Alternativas Consideradas

### 1. Sem Gerenciamento de Estado (Rejeitada)
- Agentes criados e destruídos sem controle
- Problema: Perda de estado, sem recuperação

### 2. Estado Persistente Apenas (Rejeitada)
- Estado sempre salvo no banco
- Problema: Overhead de I/O, latência

### 3. Sem Pausa/Resume (Rejeitada)
- Agentes ou rodando ou parados
- Problema: Não pode preservar estado durante manutenção

## Métricas de Sucesso

- **Disponibilidade**: > 99.9% de agentes disponíveis
- **Tempo de inicialização**: < 5 segundos para criar agente
- **Tempo de recovery**: < 30 segundos para recuperar de erro
- **Uso de recursos**: < 80% de utilização média
- **Eficiência de scaling**: Scaling em < 60 segundos

## Próximos Passos

1. Implementar AgentState e transições
2. Criar AgentLifecycleManager
3. Implementar ManagedAgent
4. Criar AgentHealth monitoring
5. Implementar ResourceManager
6. Criar AgentScaler
7. Implementar persistência de estado
8. Adicionar métricas e logging
9. Testar cenários de ciclo de vida
10. Documentar operações de gerenciamento
