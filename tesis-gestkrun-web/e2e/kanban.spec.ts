import { test, expect } from '@playwright/test';

test.describe('Kanban Board E2E', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'po@test.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await page.waitForURL(/\/dashboard/);
  });

  test('should display login page', async ({ page }) => {
    await page.goto('/login');
    await expect(page.locator('h1')).toContainText('GESTKRUN');
    await expect(page.locator('[name="email"]')).toBeVisible();
    await expect(page.locator('[name="password"]')).toBeVisible();
  });

  test('should show project list after login', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'po@test.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await page.waitForURL(/\/dashboard/);
    await page.goto('/projects');
    await expect(page.locator('h1')).toContainText('Proyectos');
  });

  test('should navigate to project detail and view tabs', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'po@test.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await page.waitForURL(/\/dashboard/);
    await page.goto('/projects');
    const firstProject = page.locator('a[href*="/projects/"]').first();
    if (await firstProject.isVisible()) {
      await firstProject.click();
      await page.waitForURL(/\/projects\//);
      await expect(page.locator('text=Módulos').or(page.locator('text=Equipo'))).toBeVisible();
    }
  });

  test('should display backlog page', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'po@test.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await page.waitForURL(/\/dashboard/);
    await page.goto('/projects');
    const firstProject = page.locator('a[href*="/projects/"]').first();
    if (await firstProject.isVisible()) {
      const href = await firstProject.getAttribute('href');
      if (href) {
        const projectId = href.split('/').pop();
        await page.goto(`/projects/${projectId}/backlog`);
        await expect(page.locator('h1')).toContainText('Product Backlog');
        await expect(page.locator('text=Nueva Épica')).toBeVisible();
      }
    }
  });

  test('should display sprint list page', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'po@test.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await page.waitForURL(/\/dashboard/);
    await page.goto('/projects');
    const firstProject = page.locator('a[href*="/projects/"]').first();
    if (await firstProject.isVisible()) {
      const href = await firstProject.getAttribute('href');
      if (href) {
        const projectId = href.split('/').pop();
        await page.goto(`/projects/${projectId}/sprints`);
        await expect(page.locator('h1')).toContainText('Sprints');
        await expect(page.locator('text=Planificar Sprint')).toBeVisible();
      }
    }
  });

  test('should create new epic in backlog', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'po@test.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await page.waitForURL(/\/dashboard/);
    await page.goto('/projects');
    const firstProject = page.locator('a[href*="/projects/"]').first();
    if (await firstProject.isVisible()) {
      const href = await firstProject.getAttribute('href');
      if (href) {
        const projectId = href.split('/').pop();
        await page.goto(`/projects/${projectId}/backlog`);
        await page.click('text=Nueva Épica');
        await page.fill('input[placeholder="Título de la épica"]', 'E2E Test Epic');
        await page.click('text=Guardar');
      }
    }
  });
});
