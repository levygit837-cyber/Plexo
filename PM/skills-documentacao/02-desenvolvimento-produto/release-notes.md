# Notas de Lançamento

## Propósito
Gerar notas de lançamento voltadas para usuários a partir de tickets, PRDs ou changelogs. Cria resumos claros e envolventes organizados por categoria (novas features, melhorias, correções). Usado ao escrever notas de lançamento, criar changelogs, anunciar atualizações de produto ou resumir o que foi lançado.

## Como Funciona
Transforma tickets técnicos, PRDs ou changelogs internos em notas de lançamento polidas e voltadas para o usuário final. O processo foca nos benefícios do usuário em vez de mudanças técnicas, usando linguagem acessível e estrutura clara.

## Quando Usar
- Lançamentos regulares de produto (semanais, quinzenais, mensais)
- Comunicar atualizações significativas para clientes
- Criar histórico de mudanças do produto
- Alinhar equipe interna em torno do valor entregue
- Documentação de versões para suporte ao cliente

## Passo a Passo

### 1. Coleta de Material Bruto
Leia todos os tickets, changelogs ou descrições fornecidos. Extraia:
- O que mudou (feature, melhoria ou correção)
- Quem afeta (qual segmento de usuário)
- Por que importa (benefício para o usuário)

### 2. Categorização de Mudanças
- **Novas Features:** Capacidades completamente novas
- **Melhorias:** Aprimoramentos de features existentes
- **Correções de Bugs:** Problemas resolvidos
- **Mudanças Quebrantes:** Qualquer coisa que requer ação do usuário (migrações, mudanças de API)
- **Depreciações:** Features sendo descontinuadas

### 3. Escrita de Cada Entrada
Siga estes princípios:
- Comece com o benefício do usuário, não a mudança técnica
- Use linguagem simples — evite jargões, nomes de código internos ou números de tickets
- Mantenha cada entrada com 1-3 frases
- Inclua visuais ou screenshots se fornecidos

**Exemplos de Transformação:**
- **Técnico:** "Implementada camada de cache Redis para endpoints de API do dashboard"
- **Voltada para Usuário:** "Dashboards agora carregam até 3× mais rápidos, então você passa menos tempo esperando e mais tempo analisando."

- **Técnico:** "Corrigida condição de corrida no fluxo de checkout concorrente"
- **Voltada para Usuário:** "Corrigido problema onde alguns pedidos poderiam falhar durante períodos de alto tráfego."

### 4. Estrutura das Notas de Lançamento

```
# [Nome do Produto] — [Versão / Data]

## Novas Features
- **[Nome da Feature]**: [Descrição de 1-2 frases do que faz e por que importa]

## Melhorias
- **[Área]**: [O que melhorou e como ajuda]

## Correções de Bugs
- Corrigido [descrição do problema em termos do usuário]

## Mudanças Quebrantes (se houver)
- **Ação necessária**: [O que os usuários precisam fazer]
```

### 5. Ajuste de Tom
Ajuste o tom para combinar com a voz do produto — profissional para B2B, amigável para consumidor, focado em desenvolvedores para APIs.

## Exemplo Prático

### Notas de Lançamento: FinanControl v2.1.0

```
# FinanControl — Versão 2.1.0 — 15 de Março de 2026

## Novas Features
- **Alertas Inteligentes de Orçamento**: Receba notificações proativas quando approaching limites de gastos, para que nunca seja pego de surpresa novamente.

- **Categorização Automática com IA**: Transações são agora categorizadas automaticamente usando machine learning, economizando tempo manual e garantindo consistência.

## Melhorias
- **Performance do Dashboard**: Tempo de carregamento reduzido em 60%, permitindo acesso instantâneo às suas finanças.

- **Interface de Filtros**: Nova experiência intuitiva para filtrar transações por período, categoria ou valor, facilitando encontrar exatamente o que procura.

- **Exportação Avançada**: Opções adicionais de exportação incluindo CSV personalizado e relatórios em PDF com gráficos.

## Correções de Bugs
- Corrigido problema onde saldo atualizado não aparecia imediatamente após registrar transações.

- Resolvido erro de login em dispositivos Android mais antigos.

- Corrigida formatação incorreta de valores em relatórios mensais para moedas estrangeiras.

## Mudanças Quebrantes
- **Ação necessária**: Usuários da versão gratuita precisarão reautenticar após atualização para manter segurança aprimorada.

## Em Breve
- Planejamos lançar recursos colaborativos para equipes no próximo trimestre.
```

## Exemplo de Transformação Técnica → Usuário

### Antes (Técnico)
```
- Implemented Redis caching layer for dashboard API endpoints
- Fixed race condition in concurrent checkout flow  
- Added pagination to transaction history API
- Updated authentication middleware to use JWT tokens
```

### Depois (Voltada para Usuário)
```
## Novas Features
- **Histórico de Transações Paginado**: Navegue facilmente por meses de transações sem sobrecarregar o sistema.

## Melhorias  
- **Dashboards Mais Rápidos**: Carregamento até 3× mais rápido para acesso instantâneo às suas finanças.

## Correções de Bugs
- Corrigido problema onde alguns pedidos poderiam falhar durante períodos de alto tráfego.

- Melhorada segurança geral para proteger seus dados financeiros.
```

## Modelos por Tipo de Produto

### B2B (Tom Profissional)
```
# [Produto] v[X.X] - [Data]

## Novas Capacidades
- **[Feature]**: [Benefício de negócio e ROI]

## Aprimoramentos
- **[Área]**: [Impacto operacional e eficiência]

## Resoluções
- Corrigido [problema afetando operações]

## Ações Requeridas
- [Mudanças que afetam processos atuais]
```

### B2C (Tom Amigável)
```
# [Produto] v[X.X] - Novidades!

🎉 **O que há de novo:**
- **[Feature]**: [Como torna sua vida melhor]

✨ **Melhorias:**
- **[Área]**: [O que ficou mais fácil]

🐛 **Correções:**
- Resolvido [problema que estava te incomodando]
```

### API/Dev (Tom Técnico)
```
# [API] v[X.X] - Release Notes

## New Endpoints
- `POST /transactions/auto-categorize`: AI-powered transaction categorization

## Enhanced Endpoints  
- `GET /dashboard`: Added caching, 3x performance improvement
- `GET /transactions`: Now supports pagination and advanced filtering

## Bug Fixes
- Fixed concurrent checkout race condition
- Resolved authentication token expiration issue

## Breaking Changes
- Authentication now requires JWT tokens (OAuth1 deprecated)
```

## Benefícios
- **Clareza:** Comunicação focada no valor, não na técnica
- **Engajamento:** Usuários entendem e se importam com as mudanças
- **Consistência:** Formato padronizado para fácil leitura
- **Profissionalismo:** Tom alinhado com marca do produto

## Dicas de Uso
- Sempre comece com "por que isso importa para o usuário"
- Use números e dados específicos quando possível (3× mais rápido, 50% menos tempo)
- Evite jargões técnicos a menos que seja API para desenvolvedores
- Inclua calls-to-action quando relevante ("Experimente agora!", "Saiba mais")
- Mantenha o foco nos benefícios, não nas features

## Recursos Adicionais
- [Release Notes Best Practices](https://www.productcompass.pm/p/release-notes-best-practices)
- [User Communication: How to Announce Product Changes](https://www.productcompass.pm/p/user-communication-guide)
- [Changelog Management: The Complete Guide](https://www.productcompass.pm/p/changelog-management)
