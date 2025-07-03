import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('Login Failure', async ({ page }) => {
    // Navigate to login page
    await page.goto('/login');

    // Enter correct email but incorrect password
    await page.getByTestId('email-input').fill('alex@aether.io');
    await page.getByTestId('password-input').fill('invalid-password');

    // Click login button
    await page.getByTestId('login-button').click();

    // Assert URL remains /login
    await expect(page).toHaveURL('/login');

    // Assert error message is visible with correct text
    await expect(page.getByTestId('login-error-message')).toBeVisible();
    await expect(page.getByTestId('login-error-message')).toContainText('Invalid email or password.');
  });
});

test.describe('Core Application Flow (Authenticated)', () => {
  // These tests will use the authenticated state from global.setup.ts
  test.use({ storageState: 'playwright/.auth/user.json' });

  test('Successful Logout', async ({ page }) => {
    // Navigate to dashboard
    await page.goto('/dashboard');

    // Click logout button
    await page.getByTestId('logout-button').click();

    // Assert redirect to login page
    await expect(page).toHaveURL('/login');
  });

  test('Keyword Cluster Generation and Verification', async ({ page }) => {
    // Navigate to dashboard
    await page.goto('/dashboard');

    // Assert welcome header is visible
    await expect(page.getByTestId('welcome-header')).toBeVisible();

    // Define keywords matching the API schema
    const keywords = `what is seo
how to do keyword research
best seo tools
what is search engine optimization`;

    // Enter keywords into textarea
    await page.getByTestId('keyword-textarea').fill(keywords);

    // Assert Generate Clusters button is enabled
    await expect(page.getByTestId('generate-clusters-button')).toBeEnabled();

    // Click Generate Clusters button
    await page.getByTestId('generate-clusters-button').click();

    // Assert button becomes disabled to prevent multiple submissions
    await expect(page.getByTestId('generate-clusters-button')).toBeDisabled();

    // Assert loading indicator is visible
    await expect(page.getByTestId('loading-indicator')).toBeVisible();

    // Assert results container is initially not visible or empty
    await expect(page.getByTestId('results-container')).not.toBeVisible().catch(() => {
      // If it's visible, it should be empty
      expect(page.getByTestId('results-container')).toBeEmpty();
    });

    // Wait for results container to be visible and loading indicator to be hidden
    await expect(page.getByTestId('results-container')).toBeVisible({ timeout: 15000 });
    await expect(page.getByTestId('loading-indicator')).not.toBeVisible();

    // Assert Generate Clusters button is re-enabled
    await expect(page.getByTestId('generate-clusters-button')).toBeEnabled();

    // Results Validation
    // Assert exactly 3 cluster groups are present
    const clusterGroups = page.getByTestId('cluster-group');
    await expect(clusterGroups).toHaveCount(3);

    // First cluster group validation
    const firstCluster = clusterGroups.first();
    await expect(firstCluster.getByTestId('primary-keyword')).toContainText('what is seo');
    
    const firstClusterRelatedList = firstCluster.getByTestId('related-keyword-list');
    await expect(firstClusterRelatedList.getByTestId('related-keyword-item')).toHaveCount(1);
    await expect(firstClusterRelatedList.getByTestId('related-keyword-item')).toContainText('what is search engine optimization');

    // Second cluster group validation
    const secondCluster = clusterGroups.nth(1);
    await expect(secondCluster.getByTestId('primary-keyword')).toContainText('how to do keyword research');
    
    // Assert related keyword list is empty or not present for second cluster
    const secondClusterRelatedList = secondCluster.getByTestId('related-keyword-list');
    await expect(secondClusterRelatedList).not.toBeVisible().catch(async () => {
      // If it's visible, it should be empty
      await expect(secondClusterRelatedList.getByTestId('related-keyword-item')).toHaveCount(0);
    });

    // Third cluster group validation
    const thirdCluster = clusterGroups.nth(2);
    await expect(thirdCluster.getByTestId('primary-keyword')).toContainText('best seo tools');
    
    // Assert related keyword list is empty or not present for third cluster
    const thirdClusterRelatedList = thirdCluster.getByTestId('related-keyword-list');
    await expect(thirdClusterRelatedList).not.toBeVisible().catch(async () => {
      // If it's visible, it should be empty
      await expect(thirdClusterRelatedList.getByTestId('related-keyword-item')).toHaveCount(0);
    });
  });
});