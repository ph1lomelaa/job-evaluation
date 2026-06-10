import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  console.log('📱 Navigating to http://localhost:5173');
  await page.goto('http://localhost:5173', { waitUntil: 'networkidle' });
  
  // Take screenshot
  await page.screenshot({ path: '/tmp/dashboard.png', fullPage: true });
  console.log('✓ Screenshot saved');
  
  // Check theme toggle
  const themeBtn = await page.locator('button[aria-label="Переключить тему"]');
  const themeBtnText = await themeBtn.textContent();
  console.log('🌓 Theme toggle shows:', themeBtnText);
  
  // Check navigation
  const navLinks = await page.locator('nav a').allTextContents();
  console.log('📍 Navigation:', navLinks);
  
  // Check for red button
  const newPosBtn = await page.locator('button').filter({ hasText: 'Новая должность' }).first();
  const btnColor = await newPosBtn.evaluate(el => {
    const style = window.getComputedStyle(el);
    return { bgColor: style.backgroundColor, color: style.color };
  });
  console.log('🔴 CTA Button color:', btnColor);
  
  // Check for placeholder text (should be gone)
  const hasOldText = await page.locator('text=Черновиков нет').count() > 0;
  console.log('✗ Has old "Черновиков нет" text:', hasOldText > 0);
  
  // Check for "Быстрый доступ" (should be gone)
  const hasFastAccess = await page.locator('text=БЫСТРЫЙ ДОСТУП').count() > 0;
  console.log('✗ Has old "БЫСТРЫЙ ДОСТУП" section:', hasFastAccess > 0);
  
  // Check for KPI cards
  const cards = await page.locator('.glass').count();
  console.log('💳 Glass-style cards found:', cards);
  
  await browser.close();
  console.log('\n✅ Verification complete!');
})().catch(e => {
  console.error('❌ Error:', e.message);
  process.exit(1);
});
