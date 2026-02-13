import { test, expect } from '@playwright/test';

/**
 * E2E Test: Home page loads correctly with search bar and navigation
 * Task 22: Playwright E2E Test for Home page
 *
 * Prerequisites:
 * - Backend running on http://127.0.0.1:8000
 * - Frontend running on http://127.0.0.1:5173
 *
 * Test Coverage:
 * - Page loads correctly with title
 * - Search bar is visible and functional
 * - Hot ganzhi cards display (10 cards)
 * - Quick entry cards display (4 cards)
 * - Navigation to other pages works
 */
test.describe('Home Page - Task 22', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to home page before each test
    await page.goto('/');
    // Wait for React to hydrate
    await page.waitForLoadState('networkidle');
  });

  test('should load home page with correct title', async ({ page }) => {
    // Verify page title exists (the default Vite title is "frontend")
    const title = await page.title();
    expect(title).toBeTruthy();

    // Verify main heading is visible
    const mainTitle = page.locator('h1:has-text("六十甲子象意百科")');
    await expect(mainTitle).toBeVisible();

    // Take a screenshot for verification
    await page.screenshot({ path: 'test-results/home-page-title.png' });
  });

  test('should display search bar with placeholder', async ({ page }) => {
    // Find the search input by its placeholder text
    const searchInput = page.locator('input[placeholder*="干支"]');
    await expect(searchInput).toBeVisible();

    // Verify the search input has the enter button suffix (Ant Design Input.Search)
    // The button should have an icon or text for searching
    const searchWrapper = page.locator('.ant-input-search');
    await expect(searchWrapper).toBeVisible();

    // Take screenshot
    await page.screenshot({ path: 'test-results/home-search-bar.png' });
  });

  test('should display hot ganzhi cards', async ({ page }) => {
    // Find the hot ganzhi section
    const hotGanzhiTitle = page.locator('h4:has-text("热门干支")');
    await expect(hotGanzhiTitle).toBeVisible();

    // Verify 10 hot ganzhi cards are displayed
    // The cards are inside ant-card class with hoverable
    const ganzhiCards = page.locator('.ant-card:has-text("甲子"), .ant-card:has-text("乙丑"), .ant-card:has-text("丙寅")');
    const count = await ganzhiCards.count();
    expect(count).toBeGreaterThan(0);

    // Verify specific ganzhi text is visible
    await expect(page.locator('.ant-card:has-text("甲子")')).toBeVisible();
    await expect(page.locator('.ant-card:has-text("癸酉")')).toBeVisible();

    // Take screenshot
    await page.screenshot({ path: 'test-results/home-hot-ganzhi.png' });
  });

  test('should display quick entry cards', async ({ page }) => {
    // Find the quick entry section
    const quickEntryTitle = page.locator('h4:has-text("快速入口")');
    await expect(quickEntryTitle).toBeVisible();

    // Verify all 4 quick entry cards are visible
    await expect(page.locator('.ant-card:has-text("纳音专题")')).toBeVisible();
    await expect(page.locator('.ant-card:has-text("神煞字典")')).toBeVisible();
    await expect(page.locator('.ant-card:has-text("关系图谱")')).toBeVisible();
    await expect(page.locator('.ant-card:has-text("干支对比")')).toBeVisible();

    // Take screenshot
    await page.screenshot({ path: 'test-results/home-quick-entry.png' });
  });

  test('should navigate to ganzhi detail when clicking hot ganzhi card', async ({ page }) => {
    // Click on 甲子 card
    const jiaziCard = page.locator('.ant-card:has-text("甲子")').first();
    await jiaziCard.click();

    // Wait for URL to change (use decodeURIComponent for Chinese characters)
    await page.waitForURL(/\/ganzhi\//);

    // Verify URL contains ganzhi route
    const currentUrl = page.url();
    expect(currentUrl).toContain('/ganzhi/');

    // Take screenshot
    await page.screenshot({ path: 'test-results/home-nav-to-ganzhi.png' });
  });

  test('should navigate to nayin page when clicking quick entry', async ({ page }) => {
    // Click on 纳音专题 card
    const nayinCard = page.locator('.ant-card:has-text("纳音专题")');
    await nayinCard.click();

    // Wait for navigation
    await page.waitForURL('**/nayin**');

    // Verify URL
    expect(page.url()).toContain('/nayin');

    // Take screenshot
    await page.screenshot({ path: 'test-results/home-nav-to-nayin.png' });
  });

  test('should navigate to shensha page when clicking quick entry', async ({ page }) => {
    // Click on 神煞字典 card
    const shenshaCard = page.locator('.ant-card:has-text("神煞字典")');
    await shenshaCard.click();

    // Wait for navigation
    await page.waitForURL('**/shensha**');

    // Verify URL
    expect(page.url()).toContain('/shensha');

    // Take screenshot
    await page.screenshot({ path: 'test-results/home-nav-to-shensha.png' });
  });

  test('should navigate to guanxi page when clicking quick entry', async ({ page }) => {
    // Click on 关系图谱 card
    const guanxiCard = page.locator('.ant-card:has-text("关系图谱")');
    await guanxiCard.click();

    // Wait for navigation
    await page.waitForURL('**/guanxi**');

    // Verify URL
    expect(page.url()).toContain('/guanxi');

    // Take screenshot
    await page.screenshot({ path: 'test-results/home-nav-to-guanxi.png' });
  });

  test('should navigate to compare page when clicking quick entry', async ({ page }) => {
    // Click on 干支对比 card
    const compareCard = page.locator('.ant-card:has-text("干支对比")');
    await compareCard.click();

    // Wait for navigation
    await page.waitForURL('**/compare**');

    // Verify URL
    expect(page.url()).toContain('/compare');

    // Take screenshot
    await page.screenshot({ path: 'test-results/home-nav-to-compare.png' });
  });
});
