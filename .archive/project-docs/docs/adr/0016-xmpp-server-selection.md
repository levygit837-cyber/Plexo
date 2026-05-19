# FEATURE: Documentation
# ADR-0016: Seleção do Servidor XMPP (ejabberd)

Data: 2026-03-29

Status: Aceito

## Contexto

O sistema Plexo necessita de um servidor XMPP para comunicação real entre agentes. Após análise, decidimos entre duas opções:

1. **ejabberd** - Servidor XMPP robusto escrito em Erlang
2. **Prosody** - Servidor XMPP leve escrito em Lua

## Análise Comparativa

| Critério | ejabberd | Prosody |
|----------|----------|--------|
| Linguagem | Erlang | Lua |
| Robustez | Muito alta | Alta |
| Consumo de recursos | Médio-Alto | Baixo |
| Configuração | Complexa (YAML) | Simples (Lua) |
| Escalabilidade | Excelente (clustering nativo) | Boa |
| XEPs suportados | Muitos | Moderados |
| Interface Web | WebAdmin completa | Básica |
| Docker | Imagem oficial otimizada | Imagem oficial pequena |
| Comunidade | Grande | Média |
| Documentação | Extensa | Boa |
| Produção | Amplamente usado | Usado |
| Desenvolvimento | Adequado | Excelente |

## Decisão

Escolhemos **ejabberd** pelos seguintes motivos:

1. **Robustez**: ejabberd é extremamente robusto e confiável, usado em produção por grandes empresas
2. **Clustering**: Suporte nativo a clustering para alta disponibilidade
3. **XEPs**: Suporte completo a extensões XMPP necessárias para o sistema
4. **MUC**: Multi-User Chat avançado para comunicação em grupo
5. **API HTTP**: API HTTP nativa para gerenciamento programático
6. **Produção**: Amplamente testado em ambientes de produção
7. **Futuro**: Suporte a longo prazo garantido pela comunidade

## Consequências

### Positivas
- Servidor robusto e confiável para produção
- Suporte completo a XMPP e extensões
- Clustering para alta disponibilidade
- API HTTP para gerenciamento automático
- Interface WebAdmin para monitoramento

### Negativas
- Configuração mais complexa que Prosody
- Consome mais recursos (RAM/CPU)
- Curva de aprendizado maior

## Configuração

A configuração do ejabberd está em:
- `backend/docker/ejabberd/ejabberd.yml`

### Portas
- **5222**: Conexão de clientes (c2s)
- **5269**: Conexão servidor-servidor (s2s)
- **5280**: HTTP/BOSH/API/WebSocket

### Domínio
- `localhost` para desenvolvimento
- Configurável via variável de ambiente `XMPP_DOMAIN`

## Agentes de Teste

Os seguintes agentes serão criados para testes:

| Agente | JID | Senha | Função |
|--------|-----|-------|--------|
| executor | executor@localhost | executor123 | Executa tarefas |
| monitor | monitor@localhost | monitor123 | Monitora ações |
| specialist | specialist@localhost | specialist123 | Especialista |
| coordinator | coordinator@localhost | coordinator123 | Coordenador |

## Referências

- [ejabberd Documentation](https://docs.ejabberd.im/)
- [XMPP Protocol](https://xmpp.org/)
- [Prosody vs ejabberd](https://wiki.xmpp.org/web/Comparison_of_XMPP_servers)
