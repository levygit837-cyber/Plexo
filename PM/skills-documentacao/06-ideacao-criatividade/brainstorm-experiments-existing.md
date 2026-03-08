# Brainstorm de Experimentos para Produto Existente

## Propósito
Projetar experimentos para testar suposições para um produto existente — protótipos, testes A/B, spikes e outros métodos de validação de baixo esforço. Usado ao validar suposições, testar ideias de feature barato ou planejar experimentos de produto.

## Como Funciona
Projeta experimentos de baixo esforço para testar suposições de produto antes de comprometer com implementação completa.

## Quando Usar
- Validação de hipóteses antes do desenvolvimento
- Teste de ideias de features com baixo investimento
- Planejamento de experimentos de produto
- Redução de risco em decisões de produto
- Discovery contínuo para produtos existentes

## Instruções

O usuário descreverá sua ideia e suposições. Trabalhe através destes passos:

### 1. Clarificar a Ideia e Suposições
Confirme o que a equipe quer construir e o que precisa validar.

### 2. Sugerir Experimentos
Para cada suposição, considere métodos como:
- **First-click testing** ou task completion com protótipo
- **Feature stubs** ou fake door tests
- **Technical spikes**
- **A/B tests** em produção (com mitigação de risco)
- **Wizard of Oz approaches**
- **Survey-based validation** (comportamental, não baseado em opinião)

### 3. Princípios Chave
- Meça comportamento real, não opiniões dos usuários
- Teste responsavelmente — não coloque usuários ou negócio em risco
- Para testes de produção (ex: A/B tests), explique estratégias de mitigação de risco
- Aponte para aprendizado validado máximo com esforço mínimo

### 4. Para Cada Experimento, Especifique
- **Suposição:** O que acreditamos?
- **Experimento:** O que faremos exatamente para validar?
- **Métrica:** O que será medido?
- **Threshold de Sucesso:** O valor esperado se estivermos certos

## Exemplo Prático

### Brainstorm de Experimentos: FinanControl

### 1. Ideia e Suposições

**Ideia:** Sistema de Alertas Inteligentes que prevê problemas de caixa e envia notificações proativas

**Suposições:**
1. Usuários valorizam alertas proativos vs. reativos
2. Previsão de problemas é tecnicamente viável com dados atuais
3. Alertas falsos positivos não frustram usuários excessivamente
4. Usuários agem em alertas recebidos
5. Sistema reduzirá churn em 10%

### 2. Experimentos Projetados

#### Experimento 1: Fake Door Test
| Componente | Descrição |
|---|---|
| **Suposição** | Usuários valorizam alertas proativos vs. reativos |
| **Experimento** | Adicionar botão "Alertas Inteligentes" no dashboard que leva a página explicando feature futura com formulário de interesse |
| **Métrica** | Taxa de clique no botão, taxa de preenchimento de formulário, tempo na página |
| **Threshold de Sucesso** | >15% de usuários clicam, >8% preenchem formulário |

#### Experimento 2: Manual Wizard of Oz
| Componente | Descrição |
|---|---|
| **Suposição** | Previsão de problemas é tecnicamente viável com dados atuais |
| **Experimento** | Analista manualmente identifica 50 empresas com problemas de caixa baseado em dados históricos e envia alertas manuais via email |
| **Métrica** | Precisão da previsão (problemas reais ocorreram), tempo de análise manual, feedback dos usuários |
| **Threshold de Sucesso** | >70% precisão, <30min por análise, >60% feedback positivo |

#### Experimento 3: Survey Comportamental
| Componente | Descrição |
|---|---|
| **Suposição** | Alertas falsos positivos não frustram usuários excessivamente |
| **Experimento** | Apresentar cenários com diferentes taxas de falsos positivos (10%, 25%, 40%) e medir disposição para usar o sistema |
| **Métrica** | Aceitabilidade por taxa de falso positivo, disposição para pagar, preocupações expressas |
| **Threshold de Sucesso** | >70% aceitável com 25% de falsos positivos |

#### Experimento 4: A/B Test Limitado
| Componente | Descrição |
|---|---|
| **Suposição** | Usuários agem em alertas recebidos |
| **Experimento** | Enviar alertas simples (sem previsão) para 10% de usuários vs. controle, medir ações tomadas |
| **Métrica** | Taxa de abertura de alerta, taxa de clique, ações realizadas após alerta |
| **Threshold de Sucesso** | >40% abertura, >15% clique, >5% ação |

#### Experimento 5: Protótipo Interativo
| Componente | Descrição |
|---|---|
| **Suposição** | Sistema reduzirá churn em 10% |
| **Experimento** | Criar protótipo clicável com sistema completo de alertas, testar com 20 usuários em sessões de 30 minutos |
| **Métrica** | Compreensão do sistema, confiança nas previsões, intenção de uso, percepção de valor |
| **Threshold de Sucesso** | >80% compreensão, >70% confiança, >60% intenção de uso |

### 3. Estratégia de Mitigação de Risco

#### Para A/B Test em Produção
- **Segmentação:** Limitar a usuários com >3 meses de uso
- **Rollback:** Botão de desligar imediato
- **Monitoramento:** Alertas para métricas negativas
- **Comunicação:** Aviso transparente sobre teste

#### Para Fake Door Test
- **Transparência:** Indicar claramente "em desenvolvimento"
- **Coleta:** Capturar email para notificar quando disponível
- **Alternativa:** Oferecer solução manual temporária

### 4. Cronograma de Experimentos

| Semana | Experimento | Objetivo |
|---|---|---|
| 1-2 | Fake Door Test | Validar interesse geral |
| 2-3 | Manual Wizard of Oz | Testar viabilidade técnica |
| 3-4 | Survey Comportamental | Entender tolerância a erros |
| 4-5 | Protótipo Interativo | Validar experiência completa |
| 5-6 | A/B Test Limitado | Medir comportamento real |

## Modelos de Experimentos

### Fake Door Test
```
Suposição: Usuários querem feature X
Experimento: Botão que leva a página "em breve"
Métrica: Taxa de clique, inscrição em waitlist
Threshold: >10% interesse
```

### Wizard of Oz
```
Suposição: Funcionalidade é tecnicamente viável
Experimento: Backend manual com frontend automatizado
Métrica: Tempo de operação, qualidade do resultado
Threshold: <5min por operação, >80% satisfação
```

### Concierge MVP
```
Suposição: Serviço resolve problema real
Experimento: Serviço totalmente manual para clientes
Métrica: Satisfação, tempo para resolver, aprendizado
Threshold: >70% satisfação, <30min por cliente
```

### Prototype Test
```
Suposição: Design é intuitivo e valioso
Experimento: Protótipo clicável com usuários reais
Métrica: Task completion, tempo, percepção de valor
Threshold: >80% completion, <5min por task
```

### A/B Test
```
Suposição: Mudança melhora métrica X
Experimento: 50/50 split com métrica principal
Métrica: Conversão, engajamento, receita
Threshold: >5% lift com 95% confiança
```

## Framework de Priorização

### Urgência vs. Esforço
```
Alta Urgência, Baixo Esforço: Fazer agora
Alta Urgência, Alto Esforço: Planejar
Baixa Urgência, Baixo Esforço: Quick win
Baixa Urgência, Alto Esforço: Depois
```

### Risco vs. Aprendizado
```
Alto Risco, Alto Aprendizado: Prioridade máxima
Alto Risco, Baixo Aprendizado: Evitar
Baixo Risco, Alto Aprendizado: Fazer rápido
Baixo Risco, Baixo Aprendizado: Opcional
```

## Benefícios
- **Redução de Risco:** Valida hipóteses antes de investimento pesado
- **Aprendizado Rápido:** Máximo aprendizado com mínimo esforço
- **Foco no Cliente:** Testa comportamento real, não opiniões
- **Eficiência:** Evita desenvolvimento de features não desejadas

## Dicas de Uso
- Comece com experimentos de menor esforço e maior aprendizado
- Meça comportamento, não opiniões declaradas
- Teste uma suposição de cada vez
- Documente aprendizados para informar próximos passos
- Esteja preparado para matear ideias baseado em resultados

## Recursos Adicionais
- [Testing Product Ideas: The Ultimate Validation Experiments Library](https://www.productcompass.pm/p/the-ultimate-experiments-library)
- [Assumption Prioritization Canvas: How to Identify And Test The Right Assumptions](https://www.productcompass.pm/p/assumption-prioritization-canvas)
- [What Is Product Discovery? The Ultimate Guide Step-by-Step](https://www.productcompass.pm/p/what-exactly-is-product-discovery)
- [Continuous Product Discovery Masterclass (CPDM)](https://www.productcompass.pm/p/cpdm) (video course)
- [Lean Experimentation: The Complete Guide](https://www.productcompass.pm/p/lean-experimentation-guide)
