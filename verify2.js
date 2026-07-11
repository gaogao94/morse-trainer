const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 900, height: 1400 } });
  await page.goto('file:///home/admin/coding/morse_trainer/index.html');
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'shot_wide.png' });
  console.log('Screenshot saved');
  
  // Check tree dimensions
  const dims = await page.evaluate(() => {
    const svg = document.getElementById('tree');
    return { w: svg.getAttribute('width'), h: svg.getAttribute('height'), vb: svg.getAttribute('viewBox') };
  });
  console.log('Tree SVG dims:', JSON.stringify(dims));
  
  // Verify timing values
  const timing = await page.evaluate(() => ({
    tC: document.getElementById('tC').textContent,
    tW: document.getElementById('tW').textContent,
    tU: document.getElementById('tU').textContent
  }));
  console.log('Timing display:', JSON.stringify(timing));
  
  await browser.close();
})();
