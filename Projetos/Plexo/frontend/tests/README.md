# Frontend Testing Guide

Este guia documenta a estrutura de testes do frontend do Plexo e como executá-los.

## Estrutura de Testes

```
tests/
├── setup.ts                 # Configuração global de testes
├── mocks/                   # Mock Service Worker
│   ├── server.ts           # Servidor MSW
│   └── handlers.ts         # Handlers de API
├── unit/                    # Testes unitários
│   ├── components/         # Testes de componentes
│   └── hooks/              # Testes de hooks
├── integration/             # Testes de integração
│   └── pages/              # Testes de páginas completas
└── e2e/                     # Testes end-to-end
    └── workflows/          # Testes de fluxos completos
```

## Tecnologias Utilizadas

- **Vitest**: Framework de testes unitários e de integração
- **Testing Library**: Biblioteca para testar componentes React
- **MSW (Mock Service Worker)**: Mock de requisições HTTP
- **Playwright**: Framework para testes E2E

## Executando os Testes

### Testes Unitários e de Integração

```bash
# Executar todos os testes
npm test

# Executar testes em modo watch
npm test:watch

# Executar testes com coverage
npm test:coverage

# Executar testes de um arquivo específico
npm test Button.test.tsx
```

### Testes E2E

```bash
# Instalar browsers do Playwright (primeira vez)
npx playwright install

# Executar testes E2E
npm run test:e2e

# Executar testes E2E em modo UI
npm run test:e2e:ui

# Executar testes E2E em um browser específico
npx playwright test --project=chromium
```

## Escrevendo Testes

### Testes Unitários de Componentes

```typescript
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Button } from '../Button';

describe('Button', () => {
  it('renders button text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
});
```

### Testes de Hooks

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { useAgents } from '../useAgents';

describe('useAgents', () => {
  it('fetches agents', async () => {
    const { result } = renderHook(() => useAgents());
    
    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });
    
    expect(result.current.agents).toHaveLength(2);
  });
});
```

### Testes de Integração

```typescript
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Home from '../Home';

describe('Home Page', () => {
  it('renders dashboard', () => {
    render(
      <BrowserRouter>
        <Home />
      </BrowserRouter>
    );
    
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
  });
});
```

### Testes E2E

```typescript
import { test, expect } from '@playwright/test';

test('navigates to agents page', async ({ page }) => {
  await page.goto('http://localhost:5173');
  await page.click('text=Ver todos');
  await expect(page).toHaveURL(/.*agents/);
});
```

## Mocking de API

Os testes usam MSW para mockar requisições HTTP. Os handlers estão em `tests/mocks/handlers.ts`.

### Adicionando Novos Handlers

```typescript
export const handlers = [
  http.get('/api/v1/agents', () => {
    return HttpResponse.json({
      data: mockAgents,
      success: true,
    });
  }),
];
```

### Sobrescrevendo Handlers em Testes

```typescript
import { server } from '../mocks/server';
import { http, HttpResponse } from 'msw';

it('handles error', async () => {
  server.use(
    http.get('/api/v1/agents', () => {
      return HttpResponse.json(
        { error: 'Error' },
        { status: 500 }
      );
    })
  );
  
  // seu teste aqui
});
```

## Coverage

O projeto tem como meta mínima de coverage:

- Lines: 70%
- Functions: 70%
- Branches: 70%
- Statements: 70%

Para visualizar o relatório de coverage:

```bash
npm test:coverage
# Abrir coverage/index.html no browser
```

## CI/CD

Os testes são executados automaticamente no CI/CD:

- Testes unitários e de integração em cada PR
- Testes E2E em cada merge para main
- Relatório de coverage é gerado e enviado para o Codecov

## Boas Práticas

1. **Teste comportamento, não implementação**: Foque no que o usuário vê e faz
2. **Use data-testid com moderação**: Prefira queries por texto ou role
3. **Evite testar detalhes de implementação**: Não teste state interno ou métodos privados
4. **Mantenha testes isolados**: Cada teste deve ser independente
5. **Use mocks com cuidado**: Mock apenas o necessário
6. **Escreva testes legíveis**: Use describes e its descritivos
7. **Teste casos de erro**: Não teste apenas o happy path

## Troubleshooting

### Testes falhando localmente mas passando no CI

- Limpe o cache: `npm test -- --clearCache`
- Verifique variáveis de ambiente
- Certifique-se de que o banco de dados de teste está limpo

### Testes E2E lentos

- Use `fullyParallel: true` no playwright.config.ts
- Execute apenas os testes necessários: `npx playwright test navigation`
- Use `--project=chromium` para testar em apenas um browser

### Erros de timeout

- Aumente o timeout: `test.setTimeout(30000)`
- Verifique se o servidor está rodando
- Verifique se há requisições pendentes
