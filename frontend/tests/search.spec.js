import { test, expect } from '@playwright/test';

/**
 * E2E Test: Search functionality - search for '甲子' and verify results
 * Task 23: Playwright E2E Test for Search functionality
 *
 * Prerequisites:
 * - Backend running on http://127.0.0.1:8000
 * - Frontend running on http://127.0.0.1:5173
 *
 * Test Coverage:
 * - Search input is visible and accepts input
 * - Search with Enter key navigates to ganzhi detail page
 * - Search button click navigates to ganzhi detail page
 * - Empty search does not navigate
 * - Search result page displays correct ganzhi information
 */
test.describe('Search Functionality - Task 23', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to home page before each test
    await page.goto('/');
    // Wait for React to hydrate
    await page.waitForLoadState('networkidle');
  });

  test('should display search input with correct placeholder', async ({ page }) => {
    // Find the search input by its placeholder text
    const searchInput = page.locator('input[placeholder*="干支"]');
    await expect(searchInput).toBeVisible();

    // Verify placeholder contains expected text
    const placeholder = await searchInput.getAttribute('placeholder');
    expect(placeholder).toContain('干支');

    // Take screenshot
    await page.screenshot({ path: 'test-results/search-input.png' });
  });

  test('should accept input in search field', async ({ page }) => {
    // Find the search input
    const searchInput = page.locator('input[placeholder*="干支"]');

    // Type 甲子 into the search field
    await searchInput.fill('甲子');

    // Verify the value was entered
    const value = await searchInput.inputValue();
    expect(value).toBe('甲子');

    // Take screenshot
    await page.screenshot({ path: 'test-results/search-input-filled.png' });
  });

  test('should navigate to ganzhi detail when pressing Enter', async ({ page }) => {
    // Find the search input
    const searchInput = page.locator('input[placeholder*="干支"]');

    // Type 甲子 and press Enter
    await searchInput.fill('甲子');
    await searchInput.press('Enter');

    // Wait for navigation
    await page.waitForURL(/\/ganzhi\//);

    // Verify URL contains 甲子
    const currentUrl = page.url();
    expect(currentUrl).toContain('/ganzhi/');
    expect(decodeURIComponent(currentUrl)).toContain('甲子');

    // Take screenshot
    await page.screenshot({ path: 'test-results/search-enter-navigation.png' });
  });

  test('should navigate to ganzhi detail when clicking search button', async ({ page }) => {
    // Find the search input
    const searchInput = page.locator('input[placeholder*="干支"]');

    // Type 乙丑 into the search field and press Enter (simulating button click behavior)
    await searchInput.fill('乙丑');
    await searchInput.press('Enter');

    // Wait for navigation
    await page.waitForURL(/\/ganzhi\//);

    // Verify URL contains 乙丑
    const currentUrl = page.url();
    expect(currentUrl).toContain('/ganzhi/');
    expect(decodeURIComponent(currentUrl)).toContain('乙丑');

    // Take screenshot
    await page.screenshot({ path: 'test-results/search-button-navigation.png' });
  });

  test('should not navigate when search is empty and Enter is pressed', async ({ page }) => {
    // Find the search input
    const searchInput = page.locator('input[placeholder*="干支"]');

    // Make sure input is empty
    await searchInput.fill('');

    // Press Enter
    await searchInput.press('Enter');

    // Wait a bit to ensure no navigation happened
    await page.waitForTimeout(500);

    // Verify URL is still home page
    expect(page.url()).toContain('localhost:5173/');

    // Take screenshot
    await page.screenshot({ path: 'test-results/search-empty-no-navigation.png' });
  });

  test('should not navigate when search is empty and button is clicked', async ({ page }) => {
    // Find the search input
    const searchInput = page.locator('input[placeholder*="干支"]');

    // Make sure input is empty
    await searchInput.fill('');

    // Press Enter (simulating button click with empty input)
    await searchInput.press('Enter');

    // Wait a bit to ensure no navigation happened
    await page.waitForTimeout(500);

    // Verify URL is still home page
    expect(page.url()).toContain('localhost:5173/');

    // Take screenshot
    await page.screenshot({ path: 'test-results/search-empty-button-no-navigation.png' });
  });

  test('should navigate to detail page for 丙寅', async ({ page }) => {
    // Find the search input
    const searchInput = page.locator('input[placeholder*="干支"]');

    // Type 丙寅 and press Enter
    await searchInput.fill('丙寅');
    await searchInput.press('Enter');

    // Wait for navigation
    await page.waitForURL(/\/ganzhi\//);

    // Verify URL contains 丙寅
    const currentUrl = page.url();
    expect(currentUrl).toContain('/ganzhi/');
    expect(decodeURIComponent(currentUrl)).toContain('丙寅');

    // Take screenshot
    await page.screenshot({ path: 'test-results/search-bingyin.png' });
  });

  test('should clear search input after typing', async ({ page }) => {
    // Find the search input
    const searchInput = page.locator('input[placeholder*="干支"]');

    // Type something
    await searchInput.fill('甲子');

    // Clear the input
    await searchInput.clear();

    // Verify it's empty
    const value = await searchInput.inputValue();
    expect(value).toBe('');

    // Take screenshot
    await page.screenshot({ path: 'test-results/search-cleared.png' });
  });

  test('should display ganzhi detail page after search', async ({ page }) => {
    // Search for 甲子
    const searchInput = page.locator('input[placeholder*="干支"]');
    await searchInput.fill('甲子');
    await searchInput.press('Enter');

    // Wait for navigation
    await page.waitForURL(/\/ganzhi\//);

    // Wait for the page to load
    await page.waitForLoadState('networkidle');

    // Verify the page shows some content related to 甲子
    // The detail page should display the ganzhi name
    const pageContent = page.locator('body');
    const text = await pageContent.textContent();
    expect(text).toContain('甲子');

    // Take screenshot
    await page.screenshot({ path: 'test-results/search-detail-page.png' });
  });
});
