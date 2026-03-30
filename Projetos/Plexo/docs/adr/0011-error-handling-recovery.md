# 0011. Error Handling and Recovery

Data: 2026-03-29

Status: Aceito

## Contexto

O sistema multi-agentes Plexo precisa lidar com falhas de forma robusta para:

- Não perder trabalho em andamento
- Recuperar-se automaticamente de erros
- Notificar agentes sobre problemas
- Manter consistência do sistema
- Aprender com erros para evitar repetição
- Fornecer debugging eficiente

## Decisão

Decidimos implementar um **sistema de error handling em camadas** com recuperação automática:

### 1. Error Classification

#### Error Types
```python
class ErrorSeverity(Enum):
    """Severidade do erro"""
    LOW = "low"                    # Erro não crítico
    MEDIUM = "medium"              # Erro que afeta funcionalidade
    HIGH = "high"                  # Erro crítico
    CRITICAL = "critical"          # Erro que para o sistema

class ErrorCategory(Enum):
    """Categoria do erro"""
    # Erros de comunicação
    COMMUNICATION = "communication"    # Falha na comunicação
    TIMEOUT = "timeout"                # Timeout de operação
    CONNECTION = "connection"          # Falha de conexão
    
    # Erros de execução
    EXECUTION = "execution"            # Falha na execução de código
    TOOL_FAILURE = "tool_failure"      # Falha em ferramenta
    VALIDATION = "validation"          # Erro de validação
    
    # Erros de dados
    DATA_CORRUPTION = "data_corruption" # Dados corrompidos
    MEMORY_OVERFLOW = "memory_overflow" # Estouro de memória
    STORAGE = "storage"                # Erro de armazenamento
    
    # Erros de segurança
    AUTHENTICATION = "authentication"  # Falha de autenticação
    AUTHORIZATION = "authorization"    # Falha de autorização
    SECURITY = "security"              # Violação de segurança
    
    # Erros de sistema
    SYSTEM = "system"                  # Erro do sistema
    RESOURCE = "resource"              # Recurso indisponível
    CONFIGURATION = "configuration"    # Erro de configuração
```

#### Error Structure
```python
@dataclass
class PlexoError:
    """Erro do sistema Plexo"""
    error_id: str
    error_type: str
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    details: Dict[str, Any]
    timestamp: datetime
    agent_id: Optional[str]
    task_id: Optional[str]
    chat_id: Optional[str]
    stack_trace: Optional[str]
    context: Dict[str, Any]
    recovery_attempted: bool = False
    recovery_successful: Optional[bool] = None
```

### 2. Error Handling Layers

#### Layer 1: Tool Error Handler
```python
class ToolErrorHandler:
    """Lida com erros de ferramentas"""
    
    async def handle_tool_error(
        self,
        tool_name: str,
        error: Exception,
        agent: Agent,
        parameters: Dict[str, Any]
    ) -> ToolResult:
        """Trata erro de ferramenta"""
        # Cria registro de erro
        plexo_error = PlexoError(
            error_id=generate_id(),
            error_type=type(error).__name__,
            category=ErrorCategory.TOOL_FAILURE,
            severity=self._classify_severity(error),
            message=str(error),
            details={
                'tool_name': tool_name,
                'parameters': parameters
            },
            timestamp=datetime.now(),
            agent_id=agent.id
        )
        
        # Tenta recuperação
        recovery_result = await self._attempt_recovery(
            plexo_error, tool_name, agent, parameters
        )
        
        if recovery_result.successful:
            return recovery_result
        
        # Retorna erro se recuperação falhou
        return ToolResult(
            success=False,
            data=None,
            error=plexo_error.message,
            metadata={'error_id': plexo_error.error_id}
        )
    
    async def _attempt_recovery(
        self,
        error: PlexoError,
        tool_name: str,
        agent: Agent,
        parameters: Dict[str, Any]
    ) -> RecoveryResult:
        """Tenta recuperar de erro"""
        # Estratégias de recuperação baseadas no tipo de erro
        if error.category == ErrorCategory.TIMEOUT:
            return await self._retry_with_backoff(
                tool_name, agent, parameters
            )
        elif error.category == ErrorCategory.CONNECTION:
            return await self._reconnect_and_retry(
                tool_name, agent, parameters
            )
        elif error.category == ErrorCategory.VALIDATION:
            return await self._fix_and_retry(
                tool_name, agent, parameters, error
            )
        else:
            return RecoveryResult(successful=False)
```

#### Layer 2: Agent Error Handler
```python
class AgentErrorHandler:
    """Lida com erros de agentes"""
    
    async def handle_agent_error(
        self,
        agent: Agent,
        error: PlexoError
    ) -> bool:
        """Trata erro de agente"""
        # Notifica agente sobre erro
        await self._notify_agent(agent, error)
        
        # Atualiza status do agente
        await self._update_agent_status(agent, error)
        
        # Tenta recuperação
        recovery_successful = await self._recover_agent(agent, error)
        
        # Registra erro na memória
        await self._store_error_in_memory(agent, error)
        
        return recovery_successful
    
    async def _recover_agent(
        self,
        agent: Agent,
        error: PlexoError
    ) -> bool:
        """Recupera agente de erro"""
        if error.severity == ErrorSeverity.CRITICAL:
            # Reinicia agente
            return await self._restart_agent(agent)
        elif error.severity == ErrorSeverity.HIGH:
            # Pausa e reconfigura agente
            return await self._pause_and_reconfigure(agent)
        elif error.severity == ErrorSeverity.MEDIUM:
            # Ajusta configuração
            return await self._adjust_configuration(agent)
        else:
            # Apenas loga erro
            return True
```

#### Layer 3: Task Error Handler
```python
class TaskErrorHandler:
    """Lida com erros de tarefas"""
    
    async def handle_task_error(
        self,
        task: Task,
        error: PlexoError
    ) -> bool:
        """Trata erro de tarefa"""
        # Atualiza status da tarefa
        await self._update_task_status(task, TaskStatus.FAILED)
        
        # Notifica agentes envolvidos
        await self._notify_agents(task, error)
        
        # Tenta recuperação
        recovery_successful = await self._recover_task(task, error)
        
        if not recovery_successful:
            # Escalona para retry ou falha permanente
            await self._escalate_task(task, error)
        
        return recovery_successful
    
    async def _recover_task(
        self,
        task: Task,
        error: PlexoError
    ) -> bool:
        """Recupera tarefa de erro"""
        # Verifica se pode fazer retry
        if task.can_retry():
            return await self._retry_task(task)
        
        # Tenta reatribuir para outro agente
        alternative_agent = await self._find_alternative_agent(task)
        if alternative_agent:
            return await self._reassign_task(task, alternative_agent)
        
        # Divide tarefa em sub-tarefas menores
        if task.can_be_divided():
            return await self._divide_task(task)
        
        return False
```

#### Layer 4: System Error Handler
```python
class SystemErrorHandler:
    """Lida com erros de sistema"""
    
    async def handle_system_error(
        self,
        error: PlexoError
    ) -> bool:
        """Trata erro de sistema"""
        # Loga erro crítico
        await self._log_critical_error(error)
        
        # Notifica administradores
        await self._notify_administrators(error)
        
        # Tenta recuperação automática
        recovery_successful = await self._recover_system(error)
        
        if not recovery_successful:
            # Ativa modo de emergência
            await self._activate_emergency_mode()
        
        return recovery_successful
    
    async def _recover_system(
        self,
        error: PlexoError
    ) -> bool:
        """Recupera sistema de erro"""
        if error.category == ErrorCategory.RESOURCE:
            return await self._free_resources()
        elif error.category == ErrorCategory.CONFIGURATION:
            return await self._reload_configuration()
        elif error.category == ErrorCategory.STORAGE:
            return await self._recover_storage()
        else:
            return False
```

### 3. Recovery Strategies

#### Retry with Exponential Backoff
```python
class RetryStrategy:
    """Estratégia de retry com backoff exponencial"""
    
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
    
    async def execute_with_retry(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Executa função com retry"""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_error = e
                
                if attempt < self.max_retries - 1:
                    delay = min(
                        self.base_delay * (self.exponential_base ** attempt),
                        self.max_delay
                    )
                    await asyncio.sleep(delay)
        
        raise last_error
```

#### Circuit Breaker
```python
class CircuitBreaker:
    """Circuit breaker para prevenir cascata de falhas"""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        half_open_max_calls: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self.half_open_calls = 0
    
    async def call(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Executa função com circuit breaker"""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_recovery():
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
            else:
                raise CircuitBreakerOpenError("Circuit breaker is open")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Chamado em caso de sucesso"""
        if self.state == CircuitState.HALF_OPEN:
            self.half_open_calls += 1
            if self.half_open_calls >= self.half_open_max_calls:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
        else:
            self.failure_count = 0
    
    def _on_failure(self):
        """Chamado em caso de falha"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
```

#### Fallback Strategy
```python
class FallbackStrategy:
    """Estratégia de fallback"""
    
    def __init__(self, fallback_funcs: List[Callable]):
        self.fallback_funcs = fallback_funcs
    
    async def execute_with_fallback(
        self,
        primary_func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Executa função com fallback"""
        try:
            return await primary_func(*args, **kwargs)
        except Exception as primary_error:
            for fallback_func in self.fallback_funcs:
                try:
                    return await fallback_func(*args, **kwargs)
                except Exception:
                    continue
            
            raise primary_error
```

### 4. Error Notification

#### Notification System
```python
class ErrorNotifier:
    """Sistema de notificação de erros"""
    
    async def notify_agent(
        self,
        agent: Agent,
        error: PlexoError
    ):
        """Notifica agente sobre erro"""
        message = self._format_error_message(error)
        await agent.send_message(message)
    
    async def notify_coordinator(
        self,
        coordinator: Agent,
        error: PlexoError
    ):
        """Notifica coordenador sobre erro"""
        message = self._format_error_report(error)
        await coordinator.send_message(message)
    
    async def notify_administrator(
        self,
        error: PlexoError
    ):
        """Notifica administrador sobre erro crítico"""
        # Email
        await self._send_email(error)
        
        # Slack/Discord
        await self._send_webhook(error)
        
        # Dashboard
        await self._update_dashboard(error)
```

### 5. Error Logging and Monitoring

#### Structured Logging
```python
class ErrorLogger:
    """Logger estruturado de erros"""
    
    def log_error(self, error: PlexoError):
        """Loga erro de forma estruturada"""
        log_entry = {
            'timestamp': error.timestamp.isoformat(),
            'error_id': error.error_id,
            'error_type': error.error_type,
            'category': error.category.value,
            'severity': error.severity.value,
            'message': error.message,
            'agent_id': error.agent_id,
            'task_id': error.task_id,
            'details': error.details
        }
        
        if error.severity == ErrorSeverity.CRITICAL:
            logger.critical(json.dumps(log_entry))
        elif error.severity == ErrorSeverity.HIGH:
            logger.error(json.dumps(log_entry))
        elif error.severity == ErrorSeverity.MEDIUM:
            logger.warning(json.dumps(log_entry))
        else:
            logger.info(json.dumps(log_entry))
```

#### Error Metrics
```python
class ErrorMetrics:
    """Métricas de erros"""
    
    def __init__(self):
        self.error_counter = Counter(
            'plexo_errors_total',
            'Total number of errors',
            ['category', 'severity', 'agent_id']
        )
        
        self.error_duration = Histogram(
            'plexo_error_recovery_duration_seconds',
            'Time spent recovering from errors',
            ['category']
        )
        
        self.circuit_breaker_state = Gauge(
            'plexo_circuit_breaker_state',
            'Circuit breaker state (0=closed, 1=half-open, 2=open)',
            ['service']
        )
    
    def record_error(self, error: PlexoError):
        """Registra erro em métricas"""
        self.error_counter.labels(
            category=error.category.value,
            severity=error.severity.value,
            agent_id=error.agent_id or 'unknown'
        ).inc()
```

### 6. Error Learning

#### Error Pattern Detection
```python
class ErrorPatternDetector:
    """Detecta padrões de erros"""
    
    async def detect_patterns(
        self,
        errors: List[PlexoError]
    ) -> List[ErrorPattern]:
        """Detecta padrões em erros"""
        patterns = []
        
        # Agrupa por categoria
        by_category = defaultdict(list)
        for error in errors:
            by_category[error.category].append(error)
        
        # Analisa cada categoria
        for category, category_errors in by_category.items():
            # Detecta clusters temporais
            temporal_clusters = self._detect_temporal_clusters(
                category_errors
            )
            
            # Detecta similaridade de mensagens
            message_clusters = self._detect_message_clusters(
                category_errors
            )
            
            # Cria padrões
            for cluster in temporal_clusters + message_clusters:
                pattern = ErrorPattern(
                    category=category,
                    errors=cluster,
                    frequency=len(cluster),
                    time_span=self._calculate_time_span(cluster)
                )
                patterns.append(pattern)
        
        return patterns
```

#### Error Prevention
```python
class ErrorPreventer:
    """Previne erros baseado em padrões"""
    
    async def prevent_errors(
        self,
        patterns: List[ErrorPattern]
    ):
        """Implementa prevenção baseada em padrões"""
        for pattern in patterns:
            if pattern.frequency > 10:
                # Padrão frequente, implementa prevenção
                await self._implement_prevention(pattern)
    
    async def _implement_prevention(
        self,
        pattern: ErrorPattern
    ):
        """Implementa prevenção específica"""
        if pattern.category == ErrorCategory.TIMEOUT:
            # Aumenta timeouts
            await self._increase_timeouts(pattern)
        elif pattern.category == ErrorCategory.VALIDATION:
            # Melhora validação
            await self._improve_validation(pattern)
        elif pattern.category == ErrorCategory.RESOURCE:
            # Adiciona recursos
            await self._add_resources(pattern)
```

## Consequências

### Positivas
- **Robustez**: Sistema resiliente a falhas
- **Recuperação automática**: Menos intervenção manual
- **Aprendizado**: Sistema melhora com experiência
- **Debugging**: Logs estruturados facilitam debug
- **Monitoramento**: Métricas para detectar problemas

### Negativas
- **Complexidade**: Sistema mais complexo
- **Overhead**: Custo de monitoramento e recovery
- **Falso positivo**: Recovery pode mascarar problemas reais
- **Dependência**: Sistema depende de mecanismos de recovery

### Mitigações
- **Testes extensivos**: Testar cenários de erro
- **Monitoramento**: Métricas para detectar problemas
- **Alertas**: Notificar sobre erros críticos
- **Documentação**: Documentar estratégias de recovery

## Alternativas Consideradas

### 1. Sem Recovery Automático (Rejeitada)
- Apenas loga erros
- Problema: Sistema para em caso de erro

### 2. Retry ilimitado (Rejeitada)
- Tenta indefinidamente
- Problema: Pode causar loops infinitos

### 3. Falha rápida (Rejeitada)
- Para sistema em qualquer erro
- Problema: Baixa disponibilidade

## Métricas de Sucesso

- **Taxa de recovery**: Porcentagem de erros recuperados com sucesso
- **Tempo de recovery**: Tempo médio para recuperar de erros
- **Disponibilidade**: Porcentagem de tempo que sistema está disponível
- **MTTR**: Mean Time To Recovery
- **MTBF**: Mean Time Between Failures

## Próximos Passos

1. Implementar classes de erro (PlexoError, ErrorCategory, ErrorSeverity)
2. Criar error handlers (Tool, Agent, Task, System)
3. Implementar estratégias de recovery (Retry, CircuitBreaker, Fallback)
4. Criar sistema de notificação
5. Implementar logging estruturado
6. Adicionar métricas de erro
7. Criar ErrorPatternDetector
8. Implementar ErrorPreventer
9. Testar cenários de erro
10. Documentar estratégias de recovery
