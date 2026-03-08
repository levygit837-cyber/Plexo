# Pre-mortem

## Propósito
Realizar análise de risco pre-mortem em PRD ou plano de lançamento. Categoriza riscos como Tigers (problemas reais), Paper Tigers (preocupações exageradas) e Elephants (preocupações não faladas), então classifica como launch-blocking, fast-follow ou track. Usado ao preparar para lançamento, stress-test plano de produto ou identificar o que pode dar errado.

## Como Funciona
Análise de risco estruturada que força equipes a pensar criticamente sobre o que pode dar errado antes do lançamento, quando ainda há tempo para agir. Ao assumir falha, revela preocupações ocultas e separa ameaças legítimas de preocupações exageradas.

## Quando Usar
- Preparação para lançamento de produto
- Stress-test de plano de produto
- Identificação de riscos em projetos críticos
- Planejamento de mitigação de riscos
- Alinhamento de equipe em torno de potenciais problemas

## Instruções

### 1. Coletar o PRD
Se o usuário fornecer PRD ou plano de produto, leia completamente. Entenda o produto, mercado alvo, suposições chave e timeline.

### 2. Pensar Passo a Passo
- Imagine o produto lança em 14 dias
- Agora imagine que falha — clientes não adotam, metas de receita não são atingidas, reputação sofre
- O que deu errado?
- O que perdemos ou não executamos bem?
- Em que estávamos superconfiantes?

### 3. Categorizar Riscos
Classifique cada falha potencial como um de três tipos:

#### Tigers (Tigres)
Problemas reais que você pessoalmente vê que poderiam descarrilar o projeto
- Baseados em evidência, experiência passada ou lógica clara
- Devem manter você acordado à noite
- Requerem ação

#### Paper Tigers (Tigres de Papel)
Problemas que outros podem se preocupar, mas você não acredita neles
- Preocupações válidas na superfície, mas improváveis ou exageradas
- Não valem investimento significativo de recursos
- Vale documentar para alinhar stakeholders

#### Elephants (Elefantes)
Algo que você não tem certeza se é problema, mas a equipe não está discutindo o suficiente
- Preocupações não faladas ou suposições que ninguém está validando
- Podem ser reais; você não tem certeza
- Merecem investigação antes do lançamento

### 4. Classificar Tigers por Urgência

#### Launch-Blocking (Bloqueia Lançamento)
Devem ser resolvidos antes do lançamento
- Ex: Feature principal quebrada, bloqueio regulatório, dependência de cliente chave não atendida

#### Fast-Follow (Acompanhamento Rápido)
Devem ser resolvidos em 30 dias pós-lançamento
- Ex: Problemas de performance, features secundárias incompletas

#### Track (Monitorar)
Monitorar pós-lançamento; resolver se se tornar problema
- Ex: Features nice-to-have, edge cases

### 5. Criar Planos de Ação
Para cada Tiger Launch-Blocking:
- Descreva o risco claramente
- Sugira ação de mitigação concreta
- Identifique o melhor owner (função/pessoa)
- Defina data de decisão/conclusão

## Exemplo Prático

### Pre-mortem: FinanControl v2.0

### Contexto
- **Produto:** Plataforma de gestão financeira para PMEs
- **Lançamento:** Em 14 dias
- **Features:** Alertas inteligentes, dashboard personalizável, ML categorização
- **Timeline:** Q3 2026

### Análise de Riscos

#### Tigers (Riscos Reais)

##### 1. Integração Bancária Não Funciona (Launch-Blocking)
**Risco:** APIs dos bancos brasileiros podem ter mudanças não documentadas ou instabilidade
**Impacto:** Produto principal fica inutilizável, perda completa de credibilidade
**Evidência:** Histórico de mudanças em APIs bancárias brasileiras sem aviso prévio

##### 2. Modelo de ML Não Generaliza (Launch-Blocking)
**Risco:** Categorização automática funciona bem com dados de treinamento mas falha com clientes reais
**Impacto:** Feature principal não entrega valor, frustração massiva de usuários
**Evidência:** Dados de treinamento limitados, padrões de transação variam por setor

##### 3. Performance do Dashboard (Fast-Follow)
**Risco:** Dashboard personalizável pode ser lento com grandes volumes de dados
**Impacto:** Experiência do usuário degradada, possível churn
**Evidência:** Protótipos mostraram lentidão com >100 transações

##### 4. Suporte Não Preparado (Fast-Follow)
**Risco:** Equipe de suporte não treinada em novas features, aumento de tickets
**Impacto:** Insatisfação de clientes, sobrecarga da equipe de suporte
**Evidência:** Timeline de treinamento apertada, features complexas

##### 5. Documentação Insuficiente (Track)
**Risco:** Guia de usuário não cobre cenários avançados, usuários ficam perdidos
**Impacto:** Menor engajamento, aumento de solicitações de suporte básicas
**Evidência:** Documentação focada em features básicas

#### Paper Tigers (Preocupações Exageradas)

##### 1. Concorrência Imediata
**Preocupação:** Concorrentes copiarão features imediatamente após lançamento
**Análise:** Features são complexas e requerem dados significativos, cópia rápida é improvável
**Ação:** Monitorar mas não alocar recursos preventivamente

##### 2. Rejeição de Mercado
**Preocupação:** PME brasileiras não adotarão automação financeira
**Análise:** Pesquisa mostra forte dor e demanda por automação, tendência de digitalização
**Ação:** Focar em marketing educativo, não mudar produto

##### 3. Problemas de Segurança
**Preocupação:** Hackers explorarão novas features para roubar dados financeiros
**Análise:** Arquitetura de segurança robusta, auditorias regulares em dia
**Ação:** Manter monitoramento de segurança padrão

#### Elephants (Preocupações Não Faladas)

##### 1. Mudança de Comportamento do Usuário
**Preocupação:** Usuários acostumados com planilhas podem resistir à automação completa
**Análise:** Não há dados suficientes sobre adoção, mudança comportamental é arriscada
**Investigação:** Pesquisa com usuários beta sobre hábitos atuais e resistência à mudança

##### 2. Custo de Suporte Subestimado
**Preocupação:** Suporte a novas features pode ser mais complexo que estimado
**Análise:** Equipe não validou complexidade de suporte para features de IA
**Investigação:** Simular cenários de suporte com equipe atual, estimar carga real

##### 3. Dependência de Terceiros
**Preocupação:** APIs de terceiros podem ter limites de uso que afetam escala
**Análise:** Não verificamos termos de uso e limites das APIs bancárias
**Investigação:** Revisar contratos e limites de todas as integrações

### Planos de Ação para Tigers Launch-Blocking

#### 1. Integração Bancária Não Funciona
- **Risco:** APIs instáveis ou quebradas
- **Mitigação:** Implementar fallback manual + testes intensivos com todos os bancos
- **Owner:** CTO + Engenharia Backend
- **Due Date:** 7 dias antes do lançamento

#### 2. Modelo de ML Não Generaliza
- **Risco:** Baixa acurácia em dados reais
- **Mitigação:** Expandir dataset de treinamento, implementar modo manual como fallback
- **Owner:** Head de Data Science + CTO
- **Due Date:** 5 dias antes do lançamento

### Estrutura de Saída

```
## Pre-Mortem Analysis: FinanControl v2.0

### Tigers (Real Risks)
1. Integração Bancária Não Funciona (Launch-Blocking)
2. Modelo de ML Não Generaliza (Launch-Blocking)
3. Performance do Dashboard (Fast-Follow)
4. Suporte Não Preparado (Fast-Follow)
5. Documentação Insuficiente (Track)

### Paper Tigers (Overblown Concerns)
1. Concorrência Imediata - Cópia rápida é improvável sem dados
2. Rejeição de Mercado - Pesquisa mostra forte demanda
3. Problemas de Segurança - Arquitetura robusta já existente

### Elephants (Unspoken Worries)
1. Mudança de Comportamento - Pesquisar adoção com usuários beta
2. Custo de Suporte Subestimado - Simular carga de trabalho
3. Dependência de Terceiros - Revisar termos e limites das APIs

### Action Plans for Launch-Blocking Tigers
**Risk:** Integração Bancária Não Funciona
**Mitigation:** Testes intensivos + fallback manual
**Owner:** CTO + Engenharia Backend
**Due Date:** 7 dias antes do lançamento

**Risk:** Modelo de ML Não Generaliza
**Mitigation:** Expandir dataset + modo manual
**Owner:** Head Data Science + CTO
**Due Date:** 5 dias antes do lançamento
```

## Framework de Implementação

### Fase 1: Identificação (Semanas -2 a -1)
- Realizar sessão de pre-mortem com equipe cross-functional
- Documentar todos os riscos potenciais
- Categorizar e priorizar riscos

### Fase 2: Mitigação (Semanas -1 a 0)
- Implementar planos de ação para Tigers launch-blocking
- Investigar Elephants para determinar se são reais
- Documentar Paper Tigers para alinhar stakeholders

### Fase 3: Validação (Semana 0)
- Testar mitigações implementadas
- Verificar se novos riscos surgiram
- Preparar plano de contingência

### Fase 4: Monitoramento (Pós-lançamento)
- Monitorar riscos Fast-Follow e Track
- Atualizar plano de riscos baseado em aprendizado
- Realizar post-mortem se necessário

## Benefícios
- **Prevenção:** Identifica problemas antes que se tornem críticos
- **Preparação:** Força equipe a pensar em cenários de falha
- **Alinhamento:** Cria entendimento compartilhado de riscos
- **Resiliência:** Construi capacidade de resposta a problemas

## Dicas de Uso
- Seja honesto e construtivo — objetivo é melhorar prontidão, não atribuir culpa
- Default para "Tiger" se incerto — melhor endereçar riscos cedo
- Envolva perspectivas cross-funcionais (engenharia, design, go-to-market)
- Revisite pre-mortem 2-3 semanas antes do lançamento para verificar mitigações

## Recursos Adicionais
- [How Meta and Instagram Use Pre-Mortems to Avoid Post-Mortems](https://www.productcompass.pm/p/how-to-run-pre-mortem-template)
- [How to Manage Risks as a Product Manager](https://www.productcompass.pm/p/how-to-manage-risks-as-a-product-manager)
- [Risk Management Framework: Complete Guide](https://www.productcompass.pm/p/risk-management-framework)
- [Product Launch Checklist: The Ultimate Guide](https://www.productcompass.pm/p/product-launch-checklist)
