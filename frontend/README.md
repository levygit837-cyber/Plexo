# Plexo Frontend

Frontend do sistema multi-agentes Plexo, construído com React, TypeScript, Vite e Tailwind CSS.

## 🚀 Tecnologias

- **React 18.2** - Biblioteca UI
- **TypeScript 5.3** - Tipagem estática
- **Vite 5.0** - Build tool e dev server
- **Tailwind CSS 3.4** - Framework CSS utility-first
- **React Router DOM 6.21** - Roteamento
- **Zustand 4.4** - State management
- **React Query 5.17** - Data fetching e cache
- **Axios 1.6** - Cliente HTTP
- **React Hook Form 7.49** - Gerenciamento de formulários
- **Zod 3.22** - Validação de schemas
- **Vitest 1.1** - Framework de testes

## 📁 Estrutura do Projeto

```
frontend/
├── public/              # Arquivos estáticos
├── src/
│   ├── assets/         # Imagens, ícones, estilos
│   ├── components/     # Componentes React
│   │   ├── common/     # Componentes reutilizáveis
│   │   ├── layout/     # Componentes de layout
│   │   └── features/   # Componentes específicos de features
│   ├── pages/          # Páginas da aplicação
│   ├── hooks/          # Custom hooks
│   ├── contexts/       # React contexts
│   ├── services/       # Serviços (API, WebSocket)
│   ├── types/          # Definições TypeScript
│   ├── utils/          # Funções utilitárias
│   ├── constants/      # Constantes da aplicação
│   ├── routes/         # Configuração de rotas
│   └── store/          # State management
└── tests/              # Testes

```

## 🛠️ Configuração

### Pré-requisitos

- Node.js >= 18.0.0
- npm >= 9.0.0

### Instalação

```bash
# Instalar dependências
npm install

# Copiar arquivo de ambiente
cp .env.example .env

# Editar variáveis de ambiente
nano .env
```

### Variáveis de Ambiente

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
VITE_ENV=development
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=true
VITE_AUTH_ENABLED=true
VITE_TOKEN_STORAGE_KEY=plexo_auth_token
VITE_APP_NAME=Plexo
VITE_APP_VERSION=0.1.0
```

## 🚀 Scripts Disponíveis

```bash
# Desenvolvimento
npm run dev              # Inicia servidor de desenvolvimento (porta 3000)

# Build
npm run build            # Compila para produção
npm run preview          # Preview da build de produção

# Qualidade de Código
npm run lint             # Executa ESLint
npm run lint:fix         # Corrige problemas do ESLint automaticamente
npm run format           # Formata código com Prettier
npm run type-check       # Verifica tipos TypeScript

# Testes
npm run test             # Executa testes
npm run test:ui          # Executa testes com UI
npm run test:coverage    # Gera relatório de cobertura
```

## 🎨 Tailwind CSS

O projeto usa Tailwind CSS com configuração customizada:

### Cores Personalizadas

- **Primary**: Tons de azul (#0ea5e9)
- **Secondary**: Tons de roxo (#a855f7)

### Classes Utilitárias Customizadas

```css
.btn-primary     /* Botão primário */
.btn-secondary   /* Botão secundário */
.card            /* Card padrão */
.input           /* Input padrão */
```

### Animações

- `animate-fade-in` - Fade in suave
- `animate-slide-in` - Slide in de cima
- `animate-spin-slow` - Rotação lenta

## 🔗 Path Aliases

O projeto usa path aliases para imports mais limpos:

```typescript
import Button from '@components/common/Button'
import { useAuth } from '@hooks/useAuth'
import { Agent } from '@types/agent'
import { API_URL } from '@constants/api'
```

Aliases disponíveis:

- `@/` → `./src/`
- `@components/` → `./src/components/`
- `@pages/` → `./src/pages/`
- `@hooks/` → `./src/hooks/`
- `@contexts/` → `./src/contexts/`
- `@services/` → `./src/services/`
- `@types/` → `./src/types/`
- `@utils/` → `./src/utils/`
- `@constants/` → `./src/constants/`
- `@assets/` → `./src/assets/`
- `@store/` → `./src/store/`

## 🧪 Testes

O projeto usa Vitest + Testing Library:

```bash
# Executar todos os testes
npm run test

# Executar testes em modo watch
npm run test -- --watch

# Executar testes com cobertura
npm run test:coverage

# Executar testes com UI
npm run test:ui
```

## 📦 Build e Deploy

```bash
# Build para produção
npm run build

# Preview da build
npm run preview
```

Os arquivos compilados estarão em `dist/`.

## 🔌 Integração com Backend

O frontend se comunica com o backend FastAPI através de:

1. **REST API**: Axios + React Query
2. **WebSocket**: Para comunicação em tempo real

Configuração do proxy no `vite.config.ts`:

```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  }
}
```

## 📝 Convenções de Código

- **Componentes**: PascalCase (`Button.tsx`)
- **Hooks**: camelCase com prefixo `use` (`useAuth.ts`)
- **Utilitários**: camelCase (`formatDate.ts`)
- **Constantes**: UPPER_SNAKE_CASE (`API_URL`)
- **Types/Interfaces**: PascalCase (`Agent`, `ApiResponse`)

## 🤝 Contribuindo

1. Siga as convenções de código
2. Escreva testes para novas features
3. Mantenha cobertura de testes > 70%
4. Execute `npm run lint` antes de commitar
5. Use commits semânticos

## 📄 Licença

Este projeto faz parte do sistema Plexo.
