import { createHash } from 'node:crypto'
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import type { Plugin } from 'vite'
import { serviceWorkerSource } from './service-worker.ts'

// Precache only the built application shell, never financial API responses.
export function pwa(): Plugin {
  const icons = ['app.svg', 'icon-180x180.png', 'icon-192x192.png', 'icon-512x512.png']
  let root = ''
  return {
    name: 'application-pwa',
    configResolved(config) {
      root = config.root
    },
    apply: 'build',
    enforce: 'post',
    transformIndexHtml() {
      return [
        {
          tag: 'link',
          attrs: { rel: 'manifest', href: '/manifest.webmanifest' },
          injectTo: 'head',
        },
        { tag: 'script', attrs: { src: '/registerSW.js', defer: true }, injectTo: 'head' },
      ]
    },
    generateBundle(_, bundle) {
      const files = Object.keys(bundle)
        .filter((name) => /\.(html|js|css|svg|png)$/.test(name))
        .sort()
      const version = createHash('sha256')
        .update(
          files
            .map((name) => {
              const item = bundle[name]
              return item.type === 'chunk' ? item.code : item.source
            })
            .join('\n')
        )
        .update(
          Buffer.concat(icons.map((name) => readFileSync(resolve(root, 'public/icons', name))))
        )
        .digest('hex')
        .slice(0, 16)
      this.emitFile({
        type: 'asset',
        fileName: 'sw.js',
        source: serviceWorkerSource(version, [
          ...new Set([
            ...files.map((name) => '/' + name),
            '/index.html',
            '/',
            '/registerSW.js',
            ...icons.map((name) => '/icons/' + name),
          ]),
        ]),
      })
      this.emitFile({
        type: 'asset',
        fileName: 'registerSW.js',
        source:
          "if('serviceWorker' in navigator){window.addEventListener('load',()=>{navigator.serviceWorker.register('/sw.js').catch(console.error)})}",
      })
      this.emitFile({
        type: 'asset',
        fileName: 'manifest.webmanifest',
        source: JSON.stringify({
          name: 'Банк Агрегатор',
          short_name: 'BankApp',
          description: 'Управляй всеми банковскими счетами в одном месте',
          theme_color: '#9333ea',
          background_color: '#ffffff',
          display: 'standalone',
          start_url: '/',
          scope: '/',
          orientation: 'portrait',
          icons: [
            {
              src: '/icons/icon-192x192.png',
              sizes: '192x192',
              type: 'image/png',
              purpose: 'any maskable',
            },
            {
              src: '/icons/icon-512x512.png',
              sizes: '512x512',
              type: 'image/png',
              purpose: 'any maskable',
            },
            { src: '/icons/app.svg', sizes: 'any', type: 'image/svg+xml', purpose: 'any maskable' },
          ],
        }),
      })
    },
  }
}
