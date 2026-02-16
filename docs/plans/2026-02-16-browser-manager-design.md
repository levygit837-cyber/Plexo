# Browser Manager — Design Document

**Data:** 2026-02-16
**Status:** Aprovado

## Objetivo

Criar um gerenciador de perfis de navegador anti-detect, similar ao Dolphin Anty e GoLogin, porém mais simples. Cada perfil tem seu próprio navegador Chromium isolado com proxy, user-agent, resolução e timezone customizáveis.

## Decisões de Arquitetura

- **Abordagem:** Monolito (FastAPI + React SPA + SQLite + Playwright)
- **Interface:** Web App local (localhost:8000)
- **Backend:** Python 3.11+ com FastAPI
- **Frontend:** React 18 + TypeScript + Vite + Tailwind CSS
- **Navegador:** Chromium via Playwright
- **Banco:** SQLite via SQLModel
- **Proxy:** HTTP/HTTPS com autenticação (formato Webshare)

## Funcionalidades Principais (v1)

### 1. Gerenciamento de Perfis
- Listar todos os perfis com status (Rodando/Parado)
- Criar perfil com: nome, user-agent, resolução, proxy, timezone
- Editar perfil existente
- Deletar perfil
- Abrir navegador (Chromium isolado com configurações do perfil)
- Fechar navegador

### 2. Proxy — Automatizador (Ctrl+V)
- Campo único de proxy no formulário
- Ao colar (Ctrl+V), parseia automaticamente:
  - `host:port:user:pass` (formato Webshare)
  - `user:pass@host:port`
  - `host:port` (sem auth)
  - `http://user:pass@host:port`
- Preenche campos de host, porta, user, password automaticamente

### 3. Proxy — Verificador
- Botão "Verificar Proxy" no formulário
- Faz request via proxy para ip-api.com
- Retorna: IP, cidade, país, timezone
- Auto-preenche timezone do perfil
- Badge visual: verde (válida) ou vermelho (inválida)

### 4. Fingerprint Customizável
- **User-Agent:** Dropdown com opções comuns + campo custom
- **Resolução de tela:** Dropdown (1920x1080, 1366x768, 1440x900, etc.)
- **Timezone:** Auto-detectado pela proxy ou manual

## Modelo de Dados

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID | Identificador único |
| `name` | string | Nome do perfil |
| `user_agent` | string | User-Agent customizado |
| `screen_width` | int | Largura da tela |
| `screen_height` | int | Altura da tela |
| `proxy_host` | string | Host da proxy |
| `proxy_port` | int | Porta da proxy |
| `proxy_username` | string | Usuário da proxy |
| `proxy_password` | string | Senha da proxy |
| `timezone` | string | Timezone |
| `status` | enum | "stopped" / "running" |
| `created_at` | datetime | Data de criação |

## API Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/api/profiles` | Lista todos os perfis |
| `POST` | `/api/profiles` | Cria novo perfil |
| `PUT` | `/api/profiles/{id}` | Atualiza perfil |
| `DELETE` | `/api/profiles/{id}` | Deleta perfil |
| `POST` | `/api/profiles/{id}/start` | Abre navegador do perfil |
| `POST` | `/api/profiles/{id}/stop` | Fecha navegador do perfil |
| `POST` | `/api/proxy/validate` | Valida proxy e retorna IP + localização |
| `POST` | `/api/proxy/parse` | Parseia string de proxy |

## Estrutura de Pastas

```
browser-manager/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── models.py
│   ├── database.py
│   ├── routers/
│   │   ├── profiles.py
│   │   └── proxy.py
│   ├── services/
│   │   ├── browser.py
│   │   ├── proxy_parser.py
│   │   └── proxy_checker.py
│   └── data/
│       ├── profiles.db
│       └── browser_data/
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── src/
│       ├── App.tsx
│       ├── main.tsx
│       ├── components/
│       │   ├── ProfileList.tsx
│       │   ├── ProfileCard.tsx
│       │   ├── CreateProfileModal.tsx
│       │   ├── ProxyInput.tsx
│       │   └── ProxyStatus.tsx
│       ├── hooks/
│       │   └── useProfiles.ts
│       └── lib/
│           ├── api.ts
│           └── proxyParser.ts
├── tests/
│   ├── test_proxy_parser.py
│   ├── test_proxy_checker.py
│   ├── test_profiles_api.py
│   └── test_browser_service.py
└── docs/plans/
```

## Fluxos Principais

### Criar Perfil
1. Clica "Criar Perfil" → abre modal
2. Preenche nome, seleciona user-agent, resolução
3. Cola proxy (Ctrl+V) → parser automático preenche campos
4. Clica "Verificar Proxy" → mostra IP, localização, timezone auto
5. Clica "Criar" → salva no SQLite, aparece na lista

### Abrir Navegador
1. Clica "Abrir" no perfil
2. Playwright cria BrowserContext isolado com proxy, user-agent, viewport, timezone
3. Diretório de dados persistente por perfil (cookies, localStorage salvos)
4. Status muda para "Rodando"

### Fechar Navegador
1. Clica "Parar" no perfil
2. Playwright fecha BrowserContext
3. Dados persistem no diretório do perfil
4. Status volta para "Parado"
