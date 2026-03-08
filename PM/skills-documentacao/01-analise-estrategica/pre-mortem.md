# Pré-Mortem: Análise de Risco para Lançamento de Produto

## Propósito
Realizar análise pré-mortem em um PRD ou plano de lançamento. Categoriza riscos como Tigres (problemas reais), Tigres de Papel (preocupações exageradas) e Elefantes (preocupações não ditas), depois classifica como bloqueadores de lançamento, acompanhamento rápido ou monitoramento. Usado ao se preparar para lançamento, testar plano de produto ou identificar o que pode dar errado.

## Como Funciona
Um pré-mortem é um exercício estruturado de identificação de riscos que força equipes a pensar criticamente sobre o que pode dar errado antes do lançamento, quando ainda há tempo para agir. Ao assumir o fracasso, identificamos preocupações ocultas e separamos ameaças legítimas de preocupações exageradas.

## Quando Usar
- 2-4 semanas antes de lançamentos importantes
- Revisão de planos de produto complexos
- Planejamento de iniciativas de alto risco
- Avaliação de projetos críticos para o negócio
- Antes de apresentar planos para leadership

## Passo a Passo

### 1. Contextualização
Imagine que o produto lança em 14 dias e falha completamente:
- Clientes não adotam
- Metas de receita não são alcançadas
- Reputação da empresa é afetada negativamente

### 2. Categorização de Riscos

#### Tigres: Problemas Reais
- Baseados em evidências, experiência ou lógica clara
- Devem mantê-lo acordado à noite
- Requerem ação

#### Tigres de Papel: Preocupações Exageradas
- Preocupações válidas na superfície, mas improváveis ou exageradas
- Não valem investimento significativo de recursos
- Valem a documentação para alinhar stakeholders

#### Elefantes: Preocupações Não Ditas
- Preocupações ou suposições não discutidas o suficiente pela equipe
- Podem ser reais; você não tem certeza
- Merecem investigação antes do lançamento

### 3. Classificação de Urgência dos Tigres

#### Bloqueadores de Lançamento
Devem ser resolvidos antes do lançamento
- Exemplo: Feature principal quebrada, bloqueio regulatório, dependência de cliente chave não atendida

#### Acompanhamento Rápido
Devem ser resolvidos em até 30 dias pós-lançamento
- Exemplo: Problemas de performance, features secundárias incompletas

#### Monitoramento
Monitorar pós-lançamento; resolver se se tornar problema
- Exemplo: Features nice-to-have, edge cases

### 4. Planos de Ação
Para cada Bloqueador de Lançamento:
- Descrever o risco claramente
- Sugerir ação de mitigação concreta
- Identificar melhor owner (função/pessoa)
- Definir data de decisão/conclusão

## Exemplo Prático

### Pré-Mortem: App de Finanças Pessoais "FinanControl"

#### Tigres (Riscos Reais)

**Bloqueadores de Lançamento:**
1. **Integração bancária falhando** - API do banco central instável
   - **Mitigação:** Desenvolver fallback manual, testar com 3 bancos principais
   - **Owner:** Engenharia (Maria)
   - **Prazo:** 7 dias

2. **Problema de segurança detectado** - Vulnerabilidade em criptografia de dados
   - **Mitigação:** Auditoria de segurança externa, implementar patches
   - **Owner:** Tech Lead (Carlos)
   - **Prazo:** 5 dias

**Acompanhamento Rápido:**
3. **Performance lenta em dispositivos antigos** - App demora >5s para abrir
   - **Mitigação:** Otimizar inicialização, testar em dispositivos mínimos
   - **Owner:** Mobile (Ana)
   - **Prazo:** 20 dias pós-lançamento

**Monitoramento:**
4. **Falta de tutorial para novos usuários** - Taxa de abandono 40% no primeiro dia
   - **Mitigação:** Adicionar onboarding interativo
   - **Owner:** Produto (Pedro)
   - **Prazo:** Monitorar por 60 dias

#### Tigres de Papel (Preocupações Exageradas)

1. **"Concorrente vai lançar produto similar"** - Sem evidências de roadmap deles
   - **Por que não é risco:** Foco em nosso diferencial, mercado grande
   - **Ação:** Monitorar mas不影响 lançamento

2. **"Usuários não vão gostar do design"** - Testes mostraram 85% aprovação
   - **Por que não é risco:** Pesquisa valida design
   - **Ação:** Documentar resultados, manter confiança

#### Elefantes (Preocupações Não Ditas)

1. **"Equipe de vendas não sabe vender produto novo"** - Capacitação não planejada
   - **Investigação:** Entrevistar head de vendas, preparar materiais
   - **Risco potencial:** Pode afetar metas comerciais

2. **"Suporte ao cliente não está preparado"** - Volume esperado não calculado
   - **Investigação:** Projetar tickets, treinar equipe
   - **Risco potencial:** Pode criar má experiência inicial

#### Planos de Ação para Bloqueadores

| Risco | Mitigação | Owner | Prazo |
|---|---|---|---|
| Integração bancária instável | Desenvolver fallback manual + testes | Maria (Eng) | 7 dias |
| Vulnerabilidade de segurança | Auditoria externa + patches | Carlos (Tech) | 5 dias |

## Estrutura de Saída

```
## Análise Pré-Mortem: [Nome do Produto]

### Tigres (Riscos Reais)
[Listar cada risco real com categoria e plano de mitigação]

### Tigres de Papel (Preocupações Exageradas)
[Listar cada, explicar por que não é risco verdadeiro]

### Elefantes (Preocupações Não Ditas)
[Listar cada, recomendar abordagem de investigação]

### Planos de Ação para Bloqueadores de Lançamento
[Para cada: Risco, Mitigação, Owner, Prazo]
```

## Benefícios
- **Prevenção:** Identifica problemas antes que afetem o lançamento
- **Alinhamento:** Alinha equipe em torno dos riscos críticos
- **Foco:** Prioriza recursos nos problemas mais importantes
- **Preparação:** Reduz surpresas durante e após o lançamento

## Dicas de Uso
- Seja honesto e construtivo — objetivo é melhorar prontidão, não atribuir culpa
- Use "Tigre" se tiver dúvida; melhor abordar riscos cedo
- Envolva perspectivas multifuncionais (engenharia, design, go-to-market) na análise
- Revisar pré-mortem 2-3 semanas antes do lançamento para verificar mitigações em andamento
- Documente suposições e incertezas para validação futura

## Recursos Adicionais
- [How Meta and Instagram Use Pre-Mortems to Avoid Post-Mortems](https://www.productcompass.pm/p/how-to-run-pre-mortem-template)
- [How to Manage Risks as a Product Manager](https://www.productcompass.pm/p/how-to-manage-risks-as-a-product-manager)
- [Risk Management in Product Development](https://www.productcompass.pm/p/risk-management-product-development)
