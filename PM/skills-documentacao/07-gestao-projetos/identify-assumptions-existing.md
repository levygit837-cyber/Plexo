# Identificar Suposições (Produto Existente)

## Propósito
Identificar suposições arriscadas para uma ideia de feature em produto existente através de Value, Usability, Viability e Feasibility. Usa pensamento de devil's advocate multi-perspectiva. Usado ao stress-test ideia de feature, fazer avaliação de risco ou preparar para assumption mapping.

## Como Funciona
Análise de devil's advocate para superficiar suposições arriscadas através de quatro áreas de risco. Força pensamento crítico sobre por que uma feature pode falhar.

## Quando Usar
- Stress-test de ideias de features antes do desenvolvimento
- Avaliação de risco para novas funcionalidades
- Preparação para assumption mapping
- Identificação de hipóteses para validação
- Tomada de decisão informada sobre prioridades

## Instruções

O usuário descreverá produto, objetivo, segmento de mercado e ideia de feature. Trabalhe através destes passos:

### 1. Pensar de Três Perspectivas
Por que esta feature pode falhar:
- **Perspectiva de Product Manager:** Viabilidade de negócio, market fit, alinhamento estratégico
- **Perspectiva de Designer:** Usabilidade, experiência do usuário, barreiras de adoção
- **Perspectiva de Engineer:** Viabilidade técnica, performance, desafios de integração

### 2. Identificar Suposições através de Quatro Áreas de Risco

#### Value (Valor)
Criará valor para clientes? Resolve um problema real?

#### Usability (Usabilidade)
Usuários conseguirão usar? A curva de aprendizado é aceitável?

#### Viability (Viabilidade)
Marketing, vendas, finanças e legal podem suportar?

#### Feasibility (Viabilidade Técnica)
Pode ser construído com tecnologia existente? Há riscos de integração?

### 3. Para Cada Suposição
- O que especificamente pode dar errado
- Quão confiante você está (High/Medium/Low)
- Maneira sugerida de testar

## Exemplo Prático

### Identificar Suposições: FinanControl

### Contexto
- **Produto:** Plataforma de gestão financeira para PMEs
- **Feature:** Alertas Inteligentes Proativos
- **Objetivo:** Reduzir churn através de prevenção de problemas
- **Segmento:** PMEs brasileiras (50-500 funcionários)

### Análise Multi-Perspectiva

#### Perspectiva de Product Manager

**Por que pode falhar:**
- PMEs não valorizam prevenção vs. reação
- Custo de implementação supera benefício percebido
- Concorrência oferece similar gratuitamente

**Suposições Value:**
1. **PMEs pagarão por prevenção** (Medium) - Testar: Survey com 50 PMEs sobre disposição para pagar
2. **Alertas reduzem churn significativamente** (High) - Testar: A/B test com grupo controle
3. **Prevenção é mais valiosa que solução reativa** (Medium) - Testar: Entrevistas sobre preferências

**Suposições Viability:**
1. **Marketing pode comunicar valor de prevenção** (Medium) - Testar: Teste de messaging com landing page
2. **Vendas pode vender feature proativa** (Low) - Testar: Role-play com equipe de vendas
3. **Suporte pode lidar com falsos positivos** (Medium) - Testar: Simular volume de tickets

#### Perspectiva de Designer

**Por que pode falhar:**
- Interface de alertas é muito complexa
- Usuários ignoram notificações proativas
- Configuração de alertas é muito técnica

**Suposições Usability:**
1. **Usuários entendem o que cada alerta significa** (High) - Testar: Testes de usabilidade com protótipo
2. **Configuração é intuitiva para não-técnicos** (Medium) - Testar: Onboarding com usuários reais
3. **Alertas não causam ansiedade excessiva** (High) - Testar: Survey de stress com diferentes frequências

**Suposições Value:**
1. **Interface clara aumenta confiança no sistema** (Medium) - Testar: A/B test de designs diferentes
2. **Personalização de alertas melhora adoção** (Low) - Testar: Teste com diferentes perfis de personalização

#### Perspectiva de Engineer

**Por que pode falhar:**
- Previsão de problemas é tecnicamente impossível
- Sistema não escala com volume de dados
- Integração com sistemas existentes falha

**Suposições Feasibility:**
1. **Modelo de ML pode prever problemas com 80% acurácia** (High) - Testar: Protótipo com dados históricos
2. **Sistema processa alertas em tempo real (<1s)** (Medium) - Testar: Teste de carga com dados simulados
3. **APIs bancárias fornecem dados necessários** (Medium) - Testar: Validação técnica com cada banco
4. **Arquitetura suporta 10x crescimento** (High) - Testar: Teste de escalabilidade

### Suposições Priorizadas por Risco

#### High Risk (Testar Imediatamente)

1. **Previsão de problemas é tecnicamente impossível** (Feasibility - High)
   - **O que pode dar errado:** Modelo não consegue identificar padrões reais
   - **Confiança:** Medium - Temos dados históricos, mas padrões podem ser complexos
   - **Teste:** Construir protótipo com 6 meses de dados, medir acurácia

2. **Usuários entendem o que cada alerta significa** (Usability - High)
   - **O que pode dar errado:** Alertas são muito técnicos ou abstratos
   - **Confiança:** Medium - Interface pode ser clara, mas conceitos financeiros são complexos
   - **Teste:** Testes de usabilidade com 20 PMEs, medir compreensão

3. **Alertas não causam ansiedade excessiva** (Usability - High)
   - **O que pode dar errado:** Muitos alertas criam estresse, levam ao churn
   - **Confiança:** Medium - Equilíbrio é difícil, depende do perfil do usuário
   - **Teste:** Survey com diferentes frequências, medir stress e satisfação

#### Medium Risk (Testar em Paralelo)

4. **PMEs pagarão por prevenção** (Value - Medium)
   - **O que pode dar errado:** PMEs preferem gastar com solução de problemas existentes
   - **Confiança:** Low - Comportamento de compra B2B é imprevisível
   - **Teste:** Survey com 50 PMEs, teste de precificação com feature real

5. **Sistema processa alertas em tempo real** (Feasibility - Medium)
   - **O que pode dar errado:** Latência alta torna alertas inúteis
   - **Confiança:** Medium - Arquitetura atual suporta, mas volume pode ser problema
   - **Teste:** Teste de carga com volume esperado de transações

6. **Modelo de ML pode prever problemas com 80% acurácia** (Feasibility - High)
   - **O que pode dar errado:** Acurácia real é muito menor, levendo a falsa confiança
   - **Confiança:** Medium - Dados disponíveis, mas generalização é arriscada
   - **Teste:** Validação cruzada com dados holdout, teste em diferentes setores

#### Low Risk (Monitorar)

7. **Configuração é intuitiva para não-técnicos** (Usability - Medium)
   - **O que pode dar errado:** Interface muito técnica, abandono durante setup
   - **Confiança:** High - Temos experiência com configuração de features similares
   - **Teste:** Onboarding com 10 usuários beta, medir tempo de configuração

8. **APIs bancárias fornecem dados necessários** (Feasibility - Medium)
   - **O que pode dar errado:** APIs não têm dados necessários para previsão
   - **Confiança:** High - Já integramos com APIs principais, sabemos o que está disponível
   - **Teste:** Validação técnica completa com cada banco

## Framework de Teste

### Métodos de Validação

#### Para Suposições de Value
- **Surveys:** Medir disposição para pagar e percepção de valor
- **A/B Tests:** Testar diferentes abordagens e mensagens
- **Entrevistas:** Entender motivações e barreiras
- **Fake Door Tests:** Testar interesse antes de construir

#### Para Suposições de Usability
- **Testes de Usabilidade:** Observar usuários interagindo com protótipos
- **Eye Tracking:** Medir onde usuários olham e o que ignoram
- **Think Aloud Sessions:** Capturar processo mental dos usuários
- **Task Completion:** Medir taxas de sucesso e tempo

#### Para Suposições de Viability
- **Landing Page Tests:** Medir conversão e interesse
- **Preço Sensitivity:** Testar diferentes pontos de preço
- **Canal Tests:** Testar diferentes canais de marketing
- **Stakeholder Interviews:** Validar suporte organizacional

#### Para Suposições de Feasibility
- **Protótipos Técnicos:** Construir versões simplificadas
- **Proof of Concepts:** Testar tecnologias específicas
- **Load Testing:** Testar performance sob carga
- **Integration Tests:** Validar conexões com sistemas

## Priorização de Testes

### Matriz de Risco vs. Esforço

| Risco | Esforço Baixo | Esforço Médio | Esforço Alto |
|---|---|---|---|
| **Alto** | Testar agora | Testar agora | Considerar cancelar |
| **Médio** | Testar em paralelo | Priorizar | Planejar |
| **Baixo** | Monitorar | Monitorar | Considerar depois |

### Cronograma Sugerido

**Semana 1-2:** Testes de High Risk, Baixo Esforço
- Testes de usabilidade com protótipos
- Validação técnica de APIs
- Surveys rápidas de disposição

**Semana 3-4:** Testes de High Risk, Esforço Médio
- Protótipos técnicos mais complexos
- A/B tests de messaging
- Entrevistas detalhadas

**Semana 5-6:** Testes de Medium Risk, Baixo Esforço
- Monitoramento de métricas
- Testes de integração finais
- Validação final de stakeholders

## Benefícios
- **Redução de Risco:** Identifica problemas antes do investimento pesado
- **Foco:** Direciona recursos para suposições mais críticas
- **Aprendizado:** Gera insights profundos sobre necessidades dos usuários
- **Alinhamento:** Alinha equipe em torno de hipóteses a validar

## Dicas de Uso
- Seja brutalmente honesto — objetivo é fortalecer a ideia, não matá-la
- Envolva perspectivas diferentes para cobertura completa
- Priorize testes baseados em risco e confiança
- Documente aprendizados para informar decisões futuras
- Esteja preparado para pivotar baseado nos resultados

## Recursos Adicionais
- [Assumption Prioritization Canvas: How to Identify And Test The Right Assumptions](https://www.productcompass.pm/p/assumption-prioritization-canvas)
- [How to Manage Risks as a Product Manager](https://www.productcompass.pm/p/how-to-manage-risks-as-a-product-manager)
- [Continuous Product Discovery Masterclass (CPDM)](https://www.productcompass.pm/p/cpdm) (video course)
- [Lean Experimentation: Testing Assumptions](https://www.productcompass.pm/p/lean-experimentation-guide)
