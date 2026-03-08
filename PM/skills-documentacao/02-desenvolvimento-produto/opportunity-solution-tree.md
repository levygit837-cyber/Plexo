# Árvore de Oportunidades e Soluções

## Propósito
Construir uma Opportunity Solution Tree (OST) para estruturar product discovery — mapear um outcome desejado para oportunidades, soluções e experimentos. Baseado no "Continuous Discovery Habits" de Teresa Torres. Usado ao estruturar trabalho de discovery, mapear oportunidades para soluções ou decidir o que construir next.

## Como Funciona
A Opportunity Solution Tree é um framework visual para estruturar discovery contínuo de produtos. Conecta um **outcome** desejado a **oportunidades** de clientes, **soluções** possíveis e **experimentos** para validá-las. Previne que equipes pulem para soluções forçando-as a mapear primeiro o espaço de oportunidades.

## Quando Usar
- Descoberta contínua de produtos
- Planejamento de discovery trimestral
- Priorização de trabalho de produto
- Alinhamento do Product Trio (PM + Designer + Engineer)
- Decisão sobre o que construir a seguir

## Estrutura (4 Níveis)

### 1. Outcome Desejado (topo)
Métrica mensurável de negócio ou produto que a equipe está buscando. Deve ser uma métrica clara e única (ex: "aumentar retenção de 7 dias para 40%"). Vem dos OKRs ou estratégia de produto.

### 2. Oportunidades (segundo nível)
Necessidades, pontos de dor ou desejos de clientes descobertos através de pesquisa. São problemas vale a pena resolver — não features. Frame da perspectiva do cliente: "Eu luto para..." ou "Eu gostaria de poder..."

**Priorização:** Use Opportunity Score: **Importância × (1 − Satisfação)** (Dan Olsen, *The Lean Product Playbook*). Normalize Importância e Satisfação para 0-1.

### 3. Soluções (terceiro nível)
Formas possíveis de abordar cada oportunidade. Gere múltiplas soluções por oportunidade — não se comprometa com a primeira ideia. O **Product Trio** deve idealizar juntos. "As melhores ideias frequentemente vêm de engenheiros."

### 4. Experimentos (base)
Testes rápidos e baratos para validar se uma solução realmente aborda a oportunidade. Use teste de suposições (riscos de Valor, Usabilidade, Viabilidade, Factibilidade). Prefira experimentos com "skin-in-the-game" (Alberto Savoia) em vez de validação baseada em opinião.

## Princípios-Chave

- **Um outcome por vez.** Não tente resolver tudo. Foque a árvore em um outcome desejado único.
- **Oportunidades, não features.** "Nunca permita que clientes desenhem soluções. Priorize oportunidades (problemas), não features."
- **Compare e contraste.** Sempre gere pelo menos 3 soluções por oportunidade antes de escolher. Evite a armadilha da "primeira ideia".
- **Discovery não é linear.** Volte se experimentos falharem. Mate soluções que não validam. Explore novos ramos.
- **Contínuo, não periódico.** Atualize a árvore semanalmente conforme aprende com entrevistas, analytics e experimentos.

## Passo a Passo

### 1. Definir o Outcome Desejado
Confirme ou ajude a articular um outcome mensurável único no topo da árvore.

**Exemplos:**
- "Aumentar retenção de 7 dias para 40%"
- "Reduzir tempo de onboarding em 50%"
- "Aumentar conversão de trial para pago em 25%"

### 2. Mapear Oportunidades
A partir da pesquisa fornecida, identifique 3-7 oportunidades de clientes (necessidades/dores). Agrupe oportunidades relacionadas. Frame cada uma da perspectiva do cliente.

**Formato de Oportunidade:**
- "Eu luto para [fazer X] quando [contexto]"
- "Eu gostaria de poder [fazer Y] para que [benefício]"
- "Estou frustrado que [problema] acontece"

### 3. Priorizar Oportunidades
Use Opportunity Score ou avaliação qualitativa para ranquear. Foque nas top 2-3.

**Cálculo do Opportunity Score:**
```
Opportunity Score = Importância × (1 − Satisfação)
```

- **Importância:** Quão importante é este problema para o cliente? (0-1)
- **Satisfação:** Quão satisfeito o cliente está com soluções atuais? (0-1)

### 4. Gerar Soluções
Para cada oportunidade priorizada, brainstorm 3+ soluções das perspectivas de PM, Designer e Engineer.

**Diversidade de Soluções:**
- **Solução 1:** Abordagem óbvia/convencional
- **Solução 2:** Abordagem inovadora/tecnológica  
- **Solução 3:** Abordagem simples/minimalista
- **Solução 4:** Abordagem colaborativa/social

### 5. Desenhar Experimentos
Para as soluções mais promissoras, sugira 1-2 experimentos rápidos. Especifique: hipótese, método, métrica, threshold de sucesso.

**Tipos de Experimentos:**
- **Testes de Valor:** Landing pages, protótipos de papel, entrevistas de solução
- **Testes de Usabilidade:** Protótipos interativos, testes A/B, testes de usabilidade
- **Testes de Viabilidade:** Análise de mercado, pesquisa de precificação, validação de modelo de negócio
- **Testes de Factibilidade:** Provas de conceito técnico, spikes de arquitetura

### 6. Visualizar a Árvore
Apresente a OST completa em formato hierárquico claro.

## Exemplo Prático

### Opportunity Solution Tree: FinanControl

#### Outcome Desejado
**Aumentar retenção de usuários após 30 dias de 25% para 40%**

#### Oportunidades (Priorizadas)

**Oportunidade 1 (Score: 0.85):** "Eu luto para entender para onde meu dinheiro está indo no fim do mês"
- **Importância:** 0.9 (muito importante)
- **Satisfação:** 0.2 (muito insatisfeito)
- **Score:** 0.9 × (1-0.2) = 0.72

**Oportunidade 2 (Score: 0.72):** "Eu gostaria de receber alertas antes de gastar demais"
- **Importância:** 0.8  
- **Satisfação:** 0.1
- **Score:** 0.8 × (1-0.1) = 0.72

**Oportunidade 3 (Score: 0.45):** "Estou frustrado que categorizar transações leva muito tempo"
- **Importância:** 0.6
- **Satisfação:** 0.25  
- **Score:** 0.6 × (1-0.25) = 0.45

#### Soluções por Oportunidade

**Para Oportunidade 1 (Entender para onde o dinheiro vai):**
- **Solução 1.1:** Dashboard visual com breakdown por categoria
- **Solução 1.2:** Relatório mensal automatizado com insights
- **Solução 1.3:** Chatbot que responde "para onde foi meu dinheiro este mês?"
- **Solução 1.4:** Mapa de calor de gastos ao longo do tempo

**Para Oportunidade 2 (Alertas de gastos):**
- **Solução 2.1:** Notificações push quando approaching limites
- **Solução 2.2:** Widget no homescreen com orçamento restante
- **Solução 2.3:** Email semanal com status do orçamento
- **Solução 2.4:** Alertas por SMS para transações grandes

#### Experimentos

**Para Solução 1.1 (Dashboard visual):**
- **Hipótese:** Se fornecermos dashboard visual, usuários entenderão melhor seus gastos e ficarão mais engajados
- **Experimento:** Protótipo interativo com 10 usuários
- **Métrica:** 80% conseguem identificar top 3 categorias de gastos
- **Sucesso:** >70% acham o dashboard útil

**Para Solução 2.1 (Notificações push):**
- **Hipótese:** Se enviarmos alertas push, usuários reduzirão overspending
- **Experimento:** Landing page descrevendo feature + survey
- **Métrica:** 60% dizem que usariam feature
- **Sucesso:** >50% expressam intenção de uso

## Visualização da Árvore

```
Outcome: Aumentar retenção 30 dias de 25% → 40%

├── Oportunidade 1: Entender para onde o dinheiro vai (Score: 0.72)
│   ├── Solução 1.1: Dashboard visual
│   │   └── Experimento: Protótipo interativo
│   ├── Solução 1.2: Relatório mensal automatizado
│   │   └── Experimento: Mockup + feedback
│   └── Solução 1.3: Chatbot de gastos
│       └── Experimento: Script de conversação
├── Oportunidade 2: Alertas antes de gastar demais (Score: 0.72)
│   ├── Solução 2.1: Notificações push
│   │   └── Experimento: Landing page
│   └── Solução 2.2: Widget homescreen
│       └── Experimento: Design mockup
└── Oportunidade 3: Categorização demora (Score: 0.45)
    ├── Solução 3.1: Categorização automática
    │   └── Experimento: Prova de conceito ML
    └── Solução 3.2: Interface simplificada
        └── Experimento: Protótipo simplificado
```

## Benefícios
- **Foco:** Evita pulo prematuro para soluções
- **Alinhamento:** Product Trio trabalhando nos mesmos problemas
- **Aprendizado:** Estrutura para descoberta contínua
- **Priorização:** Framework objetivo para escolher o que trabalhar

## Dicas de Uso
- Atualize a árvore semanalmente com novos aprendizados
- Use em sessões de discovery com Product Trio
- Não se preocupe com perfeição — foque em progresso
- Mude a árvore conforme descobre novas oportunidades
- Compartilhe com stakeholders para mostrar processo de discovery

## Recursos Adicionais
- [The Extended Opportunity Solution Tree](https://www.productcompass.pm/p/the-extended-opportunity-solution-tree)
- [What Is Product Discovery? The Ultimate Guide Step-by-Step](https://www.productcompass.pm/p/what-exactly-is-product-discovery)
- [Product Trio: Beyond the Obvious](https://www.productcompass.pm/p/product-trio)
- [Continuous Product Discovery Masterclass (CPDM)](https://www.productcompass.pm/p/cpdm) (video course)
- [Opportunity Solution Tree Examples](https://www.productcompass.pm/p/ost-examples)
