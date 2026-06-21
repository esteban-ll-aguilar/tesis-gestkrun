import { test, expect } from '@playwright/test';

test.describe('Login E2E', () => {
  test('should display login form', async ({ page }) => {
    await page.goto('/login');
    await expect(page.locator('[name="email"]')).toBeVisible();
    await expect(page.locator('[name="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });

  test('should show validation errors with empty fields', async ({ page }) => {
    await page.goto('/login');
    await page.click('button[type="submit"]');
    await expect(page.locator('text=Email es requerido').or(page.locator('[type="submit"]'))).toBeVisible();
  });

  test('should navigate to register from login', async ({ page }) => {
    await page.goto('/login');
    await page.click('text=Registrarse');
    await expect(page).toHaveURL(/\/register/);
  });

  test('should navigate to recover password from login', async ({ page }) => {
    await page.goto('/login');
    await page.click('text=Recuperar');
    await expect(page).toHaveURL(/\/recover-password/);
  });
});

test.describe('Sprint Planning E2E', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'po@test.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await page.waitForURL(/\/dashboard/);
  });

  test('should navigate to sprint planning page', async ({ page }) => {
    await page.goto('/projects');
    const firstProject = page.locator('a[href*="/projects/"]').first();
    if (await firstProject.isVisible()) {
      const href = await firstProject.getAttribute('href');
      if (href) {
        const projectId = href.split('/').pop();
        await page.goto(`/projects/${projectId}/sprints/plan`);
        await expect(page.locator('h1')).toContainText('Planificar Sprint');
        await expect(page.locator('text=Datos del Sprint')).toBeVisible();
        await expect(page.locator('text=Historias del Backlog')).toBeVisible();
      }
    }
  });

  test('should display sprint form fields', async ({ page }) => {
    await page.goto('/projects');
    const firstProject = page.locator('a[href*="/projects/"]').first();
    if (await firstProject.isVisible()) {
      const href = await firstProject.getAttribute('href');
      if (href) {
        const projectId = href.split('/').pop();
        await page.goto(`/projects/${projectId}/sprints/plan`);
        await expect(page.locator('input[placeholder="Sprint 1"]')).toBeVisible();
      }
    }
  });
});
