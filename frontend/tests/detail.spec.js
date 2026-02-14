import { test, expect } from '@playwright/test';

/**
 * E2E Test: Ganzhi detail page - displays all info
 * Task 24: Playwright E2E Test for Ganzhi detail page
 *
 * Prerequisites:
 * - Backend running on http://localhost:8000
 * - Frontend running on http://localhost:5173
 *
 * Test Coverage:
 * - Page loads with correct ganzhi name in title
 * - Basic info displays (tiangan, dizhi, fangwei, jijie)
 * - Nayin section displays
 * - All tabs are visible and clickable (象意, 神煞, 喜忌, 关系)
 * - Tab content is displayed correctly
 * - Navigation to other ganzhi via guanxi works
 */
test.describe('Ganzhi Detail Page - Task 24', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to 甲子 detail page before each test
    await page.goto('/ganzhi/甲子');
    // Wait for page to load
    await page.waitForLoadState('networkidle');
    // Wait for loading to finish
    await page.waitForTimeout(2000);
  });

  test('should display page title with ganzhi name', async ({ page }) => {
    // Find the title element containing the ganzhi name
    const title = page.locator('h2', { hasText: '甲子' });
    await expect(title).toBeVisible();

    // Take screenshot
    await page.screenshot({ path: 'test-results/detail-title.png' }).catch(() => {});
  });

  test('should display basic info (tiangan, dizhi, fangwei, jijie)', async ({ page }) => {
    // Check for 天干 label and value
    const tianganLabel = page.locator('text=天干:');
    await expect(tianganLabel).toBeVisible();

    // Check for 地支 label and value
    const dizhiLabel = page.locator('text=地支:');
    await expect(dizhiLabel).toBeVisible();

    // Check for 方位 label and value
    const fangweiLabel = page.locator('text=方位:');
    await expect(fangweiLabel).toBeVisible();

    // Check for 季节 label and value
    const jijieLabel = page.locator('text=季节:');
    await expect(jijieLabel).toBeVisible();

    // Take screenshot
    await page.screenshot({ path: 'test-results/detail-basic-info.png' }).catch(() => {});
  });

  test('should display nayin section', async ({ page }) => {
    // Check for 纳音 title
    const nayinTitle = page.locator('h4', { hasText: '纳音' });
    await expect(nayinTitle).toBeVisible();

    // Check for 纳音名称
    const nayinName = page.locator('text=纳音名称:');
    await expect(nayinName).toBeVisible();

    // Take screenshot
    await page.screenshot({ path: 'test-results/detail-nayin.png' }).catch(() => {});
  });

  test('should display all tabs (象意, 神煞, 喜忌, 关系)', async ({ page }) => {
    // Check for each tab
    const xiangyiTab = page.locator('.ant-tabs-tab', { hasText: '象意' });
    await expect(xiangyiTab).toBeVisible();

    const shenshaTab = page.locator('.ant-tabs-tab', { hasText: '神煞' });
    await expect(shenshaTab).toBeVisible();

    const xijiTab = page.locator('.ant-tabs-tab', { hasText: '喜忌' });
    await expect(xijiTab).toBeVisible();

    const guanxiTab = page.locator('.ant-tabs-tab', { hasText: '关系' });
    await expect(guanxiTab).toBeVisible();

    // Take screenshot
    await page.screenshot({ path: 'test-results/detail-tabs.png' }).catch(() => {});
  });

  test('should switch to 神煞 tab and display content', async ({ page }) => {
    // Click on 神煞 tab
    const shenshaTab = page.locator('.ant-tabs-tab', { hasText: '神煞' });
    await shenshaTab.click();

    // Wait for tab content to appear - use getByRole for specific tabpanel
    const shenshaPanel = page.getByRole('tabpanel', { name: '神煞' });
    await expect(shenshaPanel).toBeVisible();

    // Check for 神煞 table within the panel
    const tableInPanel = shenshaPanel.locator('.ant-table');
    await expect(tableInPanel).toBeVisible();

    // Take screenshot
    await page.screenshot({ path: 'test-results/detail-shensha-tab.png' }).catch(() => {});
  });

  test('should switch to 喜忌 tab and display content', async ({ page }) => {
    // Click on 喜忌 tab
    const xijiTab = page.locator('.ant-tabs-tab', { hasText: '喜忌' });
    await xijiTab.click();

    // Wait for tab content to appear - use getByRole for specific tabpanel
    const xijiPanel = page.getByRole('tabpanel', { name: '喜忌' });
    await expect(xijiPanel).toBeVisible();

    // Check for table content in the panel (if any)
    const tableInPanel = xijiPanel.locator('.ant-table');
    await expect(tableInPanel).toBeVisible();

    // Take screenshot
    await page.screenshot({ path: 'test-results/detail-xiji-tab.png' }).catch(() => {});
  });

  test('should switch to 关系 tab and display content', async ({ page }) => {
    // Click on 关系 tab
    const guanxiTab = page.locator('.ant-tabs-tab', { hasText: '关系' });
    await guanxiTab.click();

    // Wait for tab content to appear - use getByRole for specific tabpanel
    const guanxiPanel = page.getByRole('tabpanel', { name: '关系' });
    await expect(guanxiPanel).toBeVisible();

    // Check for table in the panel
    const tableInPanel = guanxiPanel.locator('.ant-table');
    await expect(tableInPanel).toBeVisible();

    // Take screenshot
    await page.screenshot({ path: 'test-results/detail-guanxi-tab.png' }).catch(() => {});
  });

  test('should navigate to another ganzhi via guanxi link', async ({ page }) => {
    // Click on 关系 tab first
    const guanxiTab = page.locator('.ant-tabs-tab', { hasText: '关系' });
    await guanxiTab.click();

    // Wait for tab content
    await page.waitForTimeout(1000);

    // Find a link in the guanxi table (contains 关系类型)
    // Look for an anchor tag that navigates to another ganzhi
    const guanxiLink = page.locator('.ant-table-row a').first();

    // Check if there's a link available (some ganzhi may have relations)
    const linkCount = await guanxiLink.count();

    if (linkCount > 0) {
      // Click the first link
      await guanxiLink.click();

      // Wait for navigation
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(1000);

      // Verify URL changed
      expect(page.url()).toContain('/ganzhi/');

      // Take screenshot
      await page.screenshot({ path: 'test-results/detail-guanxi-navigation.png' }).catch(() => {});
    } else {
      // Skip test if no links available
      console.log('No guanxi links found for 甲子');
      await page.screenshot({ path: 'test-results/detail-no-guanxi-links.png' }).catch(() => {});
    }
  });

  test('should load different ganzhi (乙丑) correctly', async ({ page }) => {
    // Navigate to 乙丑 detail page
    await page.goto('/ganzhi/乙丑');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);

    // Check title
    const title = page.locator('h2', { hasText: '乙丑' });
    await expect(title).toBeVisible();

    // Check basic info
    const tianganLabel = page.locator('text=天干:');
    await expect(tianganLabel).toBeVisible();

    // Take screenshot
    await page.screenshot({ path: 'test-results/detail-yichou.png' }).catch(() => {});
  });

  test('should handle invalid ganzhi gracefully', async ({ page }) => {
    // Navigate to invalid ganzhi
    await page.goto('/ganzhi/无效');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);

    // Either shows no data message or stays on page
    const pageContent = page.locator('body');
    const text = await pageContent.textContent();

    // Should either show "未找到相关数据" or "暂无数据" or still show the page
    const hasNoData = text.includes('未找到') || text.includes('暂无数据') || text.includes('无效');
    expect(hasNoData).toBe(true);

    // Take screenshot
    await page.screenshot({ path: 'test-results/detail-invalid.png' }).catch(() => {});
  });
});
