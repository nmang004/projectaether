import { test as setup, expect } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('authenticate', async ({ page }) => {
  // Navigate to login page
  await page.goto('/login');

  // Fill login form with provided credentials
  await page.getByTestId('email-input').fill('alex@aether.io');
  await page.getByTestId('password-input').fill('U@T_P@ssw0rd_Alex');

  // Click login button
  await page.getByTestId('login-button').click();

  // Wait for navigation to dashboard
  await page.waitForURL('/dashboard');

  // Assert successful login by checking welcome header
  await expect(page.getByTestId('welcome-header')).toBeVisible();

  // Save the authenticated state (localStorage and cookies)
  await page.context().storageState({ path: authFile });
});