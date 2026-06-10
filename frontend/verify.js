const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  console.log('📱 Navigating to http://localhost:5173');
  await page.goto('http://localhost:5173', { waitUntil: 'networkidle' });
  
  // Take screenshot of main page
  await page.screenshot({ path: '/tmp/dashboard.png', fullPage: true });
  console.log('✓ Dashboard screenshot saved');
  
  // Check header for theme toggle
  const themeBtn = await page.locator('button[aria-label="Переключить тему"]');
  const themeBtnText = await themeBtn.textContent();
  console.log('🌓 Theme toggle content:', themeBtnText);
  
  // Check for button styles
  const newPosBtn = await page.locator('button:has-text("Новая должность")').first();
  const btnStyle = await newPosBtn.evaluate(el => window.getComputedStyle(el).backgroundColor);
  console.log('🔴 CTA Button BG color:', btnStyle);
  
  // Check for navigation
  const navItems = await page.locator('nav a').allTextContents();
  console.log('📍 Nav items:', navItems);
  
  // Look for old placeholder text
  const hasPlaceholder = await page.locator('text=Черновиков нет').count() > 0;
  console.log('❌ Has old placeholder text:', hasPlaceholder);
  
  // Check KPI cards
  const kpiCards = await page.locator('[class*="glass"]').count();
  console.log('💳 Glass cards found:', kpiCards);
  
  await browser.close();
  console.log('\n✅ All checks complete!');
})().catch(e => {
  console.error('Error:', e.message);
  process.exit(1);
});
