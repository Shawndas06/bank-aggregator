import { strict as assert } from 'node:assert'
import { test } from 'node:test'
import { runInNewContext } from 'node:vm'
import { serviceWorkerSource } from '../build/service-worker.ts'

type Request = { url: string; method: string; mode?: string }
type Event = {
  request?: Request
  waitUntil?: (promise: Promise<unknown>) => void
  respondWith?: (response: Promise<unknown>) => void
}

function environment(installFails = false) {
  const listeners: Record<string, (event: Event) => void> = {}
  const stores = new Map<string, Map<string, string>>()
  let online = true,
    claimed = false,
    waitingSkipped = false
  const caches = {
    keys: async () => [...stores.keys()],
    delete: async (key: string) => stores.delete(key),
    open: async (name: string) => {
      if (!stores.has(name)) stores.set(name, new Map())
      const store = stores.get(name)!
      return {
        addAll: async (urls: string[]) => {
          if (installFails) throw new Error('asset unavailable')
          urls.forEach((url) => store.set(url, 'cached:' + url))
        },
        match: async (url: string) => store.get(url),
      }
    },
  }
  runInNewContext(serviceWorkerSource('new', ['/index.html', '/assets/app.js']), {
    URL,
    caches,
    fetch: async () => {
      if (!online) throw new Error('offline')
      return 'network'
    },
    self: {
      location: { origin: 'https://bank.example' },
      clients: {
        claim: async () => {
          claimed = true
        },
      },
      skipWaiting: async () => {
        waitingSkipped = true
      },
      addEventListener: (name: string, listener: (event: Event) => void) => {
        listeners[name] = listener
      },
    },
  })
  return {
    stores,
    caches,
    setOffline: () => {
      online = false
    },
    claimed: () => claimed,
    waitingSkipped: () => waitingSkipped,
    lifecycle: async (name: string) => {
      let pending: Promise<unknown> | undefined
      listeners[name]({
        waitUntil: (promise) => {
          pending = promise
        },
      })
      await pending
    },
    fetch: async (path: string, method = 'GET', mode = 'cors') => {
      let response: Promise<unknown> | undefined
      listeners.fetch({
        request: { url: new URL(path, 'https://bank.example').href, method, mode },
        respondWith: (promise) => {
          response = promise
        },
      })
      return response === undefined ? null : response
    },
  }
}

test('offline app shell and hashed assets are available after successful install', async () => {
  const env = environment()
  await env.lifecycle('install')
  assert.equal(env.waitingSkipped(), true)
  assert.equal(await env.fetch('/accounts', 'GET', 'navigate'), 'network')
  env.setOffline()
  assert.equal(await env.fetch('/accounts', 'GET', 'navigate'), 'cached:/index.html')
  assert.equal(await env.fetch('/assets/app.js'), 'cached:/assets/app.js')
})
for (const path of [
  '/api',
  '/api/accounts',
  '/api/payments/history',
  '/api/auth/me',
  'https://other.example/assets/app.js',
]) {
  test(`worker never intercepts or caches private/foreign request: ${path}`, async () => {
    const env = environment()
    await env.lifecycle('install')
    assert.equal(await env.fetch(path), null)
    assert.equal(await env.fetch(path, 'POST'), null)
    env.setOffline()
    assert.equal(await env.fetch(path, 'GET', 'navigate'), null)
  })
}
test('update removes stale app and legacy private API caches without deleting unrelated caches', async () => {
  const env = environment()
  for (const name of ['bank-app-old', 'api-cache', 'workbox-precache-v2-test', 'other-app'])
    await env.caches.open(name)
  await env.lifecycle('install')
  await env.lifecycle('activate')
  assert.deepEqual([...env.stores.keys()].sort(), ['bank-app-new', 'other-app'])
  assert.equal(env.claimed(), true)
})
test('failed asset install never activates an incomplete new worker', async () => {
  const env = environment(true)
  await assert.rejects(env.lifecycle('install'), /asset unavailable/)
  assert.equal(env.waitingSkipped(), false)
  assert.equal(env.claimed(), false)
})
