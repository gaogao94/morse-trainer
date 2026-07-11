const { chromium } = require('playwright-core');

(async () => {
  const exe = '/home/admin/.cache/ms-playwright';
  const fs = require('fs');
  let browser;
  // Try to find chromium binary
  try {
    browser = await chromium.launch({ headless: true });
  } catch(e) {
    console.log('launch error:', e.message);
    return;
  }
  const page = await browser.newPage({ viewport: { width: 580, height: 1200 } });
  await page.goto('file:///home/admin/coding/morse_trainer/index.html');
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'v_study.png' });
  console.log('study captured');

  await page.click('[data-mode="test"]');
  await page.waitForTimeout(300);
  await page.screenshot({ path: 'v_test.png' });
  console.log('test captured');

  await page.click('[data-mode="study"]');
  await page.waitForTimeout(200);
  await page.setViewportSize({ width: 390, height: 1000 });
  await page.waitForTimeout(200);
  await page.screenshot({ path: 'v_mobile.png' });
  console.log('mobile captured');

  await browser.close();
})();
