// E2E tests for navigation workflow
// FEATURE: Testing
import { test, expect } from '@playwright/test';

test.describe('Navigation Workflow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173');
  });

  test('navigates from home to agents page', async ({ page }) => {
    await expect(page.locator('h1')).toContainText('Dashboard');
    
    await page.click('text=Ver todos');
    
    await expect(page).toHaveURL(/.*agents/);
    await expect(page.locator('h1')).toContainText('Agentes');
  });

  test('navigates from home to tasks page', async ({ page }) => {
    await expect(page.locator('h1')).toContainText('Dashboard');
    
    const verTodosLinks = page.locator('text=Ver todos');
    await verTodosLinks.nth(1).click();
    
    await expect(page).toHaveURL(/.*tasks/);
    await expect(page.locator('h1')).toContainText('Tarefas');
  });

  test('displays 404 page for invalid route', async ({ page }) => {
    await page.goto('http://localhost:5173/invalid-route');
    
    await expect(page.locator('h1')).toContainText('404');
    await expect(page.locator('h2')).toContainText('Página não encontrada');
  });

  test('navigates back from 404 page', async ({ page }) => {
    await page.goto('http://localhost:5173/invalid-route');
    
    await page.click('text=Ir para Home');
    
    await expect(page).toHaveURL('http://localhost:5173/');
    await expect(page.locator('h1')).toContainText('Dashboard');
  });

  test('filters agents by status', async ({ page }) => {
    await page.goto('http://localhost:5173/agents');
    
    await page.selectOption('select', 'active');
    
    const agentCards = page.locator('[data-testid="agent-card"]');
    await expect(agentCards).toHaveCount(1);
  });

  test('searches for agents', async ({ page }) => {
    await page.goto('http://localhost:5173/agents');
    
    await page.fill('input[placeholder*="Buscar"]', 'Test Agent 1');
    
    const agentCards = page.locator('[data-testid="agent-card"]');
    await expect(agentCards).toHaveCount(1);
    await expect(page.locator('text=Test Agent 1')).toBeVisible();
  });

  test('views agent details', async ({ page }) => {
    await page.goto('http://localhost:5173/agents');
    
    await page.click('text=Test Agent 1');
    
    await expect(page).toHaveURL(/.*agents\/agent-1/);
    await expect(page.locator('h1')).toContainText('Test Agent 1');
    await expect(page.locator('text=Informações')).toBeVisible();
  });

  test('switches tabs in agent detail page', async ({ page }) => {
    await page.goto('http://localhost:5173/agents/agent-1');
    
    await page.click('text=Mensagens');
    await expect(page.locator('text=Histórico de Mensagens')).toBeVisible();
    
    await page.click('text=Configuração');
    await expect(page.locator('pre')).toBeVisible();
  });
});
