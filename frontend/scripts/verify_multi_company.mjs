import { chromium } from "playwright";

const browser = await chromium.launch({
  headless: true,
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
});

try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 960 } });
  await page.goto("http://127.0.0.1:5173/", { waitUntil: "networkidle" });
  await page.screenshot({ path: "/tmp/jeval-auth.png", fullPage: true });

  await page.getByRole("button", { name: "Регистрация" }).click();
  await page.getByLabel("Имя").fill("Муслима Тест");
  await page.getByLabel("Email").fill(`visual-${Date.now()}@example.com`);
  await page.getByLabel("Пароль").fill("visual-test-123");
  await page.getByRole("button", { name: "Продолжить" }).click();
  await page.getByText("Добро пожаловать, Муслима!").waitFor();
  await page.screenshot({ path: "/tmp/jeval-onboarding.png", fullPage: true });

  await page.getByRole("button", { name: /Оценка должностей/ }).click();
  await page.getByRole("button", { name: "Продолжить" }).click();
  await page.getByRole("button", { name: "HR / C&B" }).click();
  await page.getByRole("button", { name: "Продолжить" }).click();
  await page.getByRole("button", { name: "251–1 000" }).click();
  await page.getByRole("button", { name: "Продолжить" }).click();
  await page.getByLabel("Название рабочего пространства").fill("KMG Demo");
  await page.getByRole("button", { name: "Создать компанию" }).click();
  await page.getByText("KMG Demo").first().waitFor();
  await page.screenshot({ path: "/tmp/jeval-dashboard.png", fullPage: true });

  await page.getByRole("button", { name: /Муслима Тест/ }).click();
  await page.getByText("Добавить компанию").waitFor();
  await page.screenshot({ path: "/tmp/jeval-company-menu.png", fullPage: true });

  const mobile = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await mobile.goto("http://127.0.0.1:5173/", { waitUntil: "networkidle" });
  await mobile.screenshot({ path: "/tmp/jeval-auth-mobile.png", fullPage: true });

  process.stdout.write("auth,onboarding,dashboard,company-menu,mobile screenshots created\n");
} finally {
  await browser.close();
}
