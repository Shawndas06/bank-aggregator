import { test, expect } from '@playwright/test'

test.beforeEach(async ({ page }) => {
  await page.route('**/api/**', (route) => {
    const path = new URL(route.request().url()).pathname
    let data: unknown = []
    if (path === '/api/auth/me')
      data = {
        id: 1,
        name: 'Test User',
        email: 'test@example.test',
        birthDate: '1990-01-01',
        phone: null,
        avatarUrl: null,
        accountType: 'premium',
        isVerified: true,
      }
    if (path === '/api/analytics/overview')
      data = {
        totalBalance: 100,
        accountsCount: 0,
        currentMonth: { expenses: 0, income: 0, expenseChange: 0, incomeChange: 0 },
        topCategories: [],
      }
    return route.fulfill({ json: { success: true, data } })
  })
})

test('profile fields survive the wire adapter and invalid phone shows a controlled error', async ({
  page,
}) => {
  const errors: string[] = []
  page.on('pageerror', (error) => errors.push(error.message))
  await page.goto('/profile')
  await expect(page.getByText('test@example.test', { exact: true }).first()).toBeVisible()
  await page.getByText('Подтвердить', { exact: true }).click()
  await expect(page.getByText('Подтверждение телефона', { exact: true })).toBeVisible()
  await page.getByRole('button', { name: 'Отправить код', exact: true }).click()
  await expect(page.getByText('Введите корректный номер телефона', { exact: true })).toBeVisible()
  expect(errors).toEqual([])
})

test('premium status uses the actual lowercase API value', async ({ page }) => {
  await page.goto('/premium')
  await expect(page.getByRole('heading', { name: 'Вы уже Premium!' })).toBeVisible()
})

test('PWA installs, cleans legacy private caches and serves public UI offline without caching API', async ({
  page,
  context,
}) => {
  await page.route('**/registerSW.js', (route) =>
    route.fulfill({ contentType: 'application/javascript', body: '' })
  )
  await page.goto('/')
  await page.evaluate(async () => {
    for (const name of ['api-cache', 'workbox-precache-v2-legacy', 'bank-app-old', 'unrelated']) {
      const cache = await caches.open(name)
      await cache.put('/api/legacy', new Response('synthetic-private-fixture'))
    }
  })
  await page.unroute('**/registerSW.js')
  await page.reload()
  await page.waitForFunction(() => navigator.serviceWorker.controller !== null)
  await expect.poll(() => page.evaluate(() => caches.keys())).not.toContain('api-cache')
  const keys = await page.evaluate(() => caches.keys())
  expect(keys).not.toContain('workbox-precache-v2-legacy')
  expect(keys).not.toContain('bank-app-old')
  expect(keys).toContain('unrelated')
  expect(keys.some((key) => key.startsWith('bank-app-'))).toBe(true)
  await page.evaluate(async () => {
    await fetch('/api/accounts')
  })
  expect(
    await page.evaluate(async () => {
      for (const name of await caches.keys()) {
        if (await (await caches.open(name)).match('/api/accounts')) return true
      }
      return false
    })
  ).toBe(false)
  await page.unroute('**/api/**')
  await context.setOffline(true)
  await page.goto('/sign-in')
  await expect(page.getByRole('button', { name: 'Войти', exact: true })).toBeVisible()
  expect(
    await page.evaluate(() =>
      fetch('/api/private').then(
        () => false,
        () => true
      )
    )
  ).toBe(true)
})
