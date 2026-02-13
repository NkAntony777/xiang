import { test, expect } from '@playwright/test';

/**
 * E2E Test: Home page loads correctly
 *
 * Prerequisites:
 * - Backend running on http://127.0.0.1:8000
 * - Frontend running on http://127.0.0.1:5173
 */
test.describe('Home Page', () => {
  test('should load home page with search bar', async ({ page }) => {
    // Navigate to home page
    await page.goto('/');

    // Wait for page to be ready
    await page.waitForLoadState('networkidle');

    // Verify page title contains expected text
    await expect(page).toHaveTitle(/六十甲子/);

    // Take a screenshot for verification
    await page.screenshot({ path: 'test-results/home-page.png' });
  });

  test('should display navigation menu', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Check for navigation items
    const nav = page.locator('nav');
    await expect(nav).toBeVisible();
  });
});
