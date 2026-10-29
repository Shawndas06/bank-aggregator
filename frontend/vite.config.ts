import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { pwa } from './pwa/pwa'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    pwa()
  ],
  resolve: {
    alias: {
      '@app': path.resolve(__dirname, './src/app'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@widgets': path.resolve(__dirname, './src/widgets'),
      '@features': path.resolve(__dirname, './src/features'),
      '@entities': path.resolve(__dirname, './src/entities'),
      '@shared': path.resolve(__dirname, './src/shared'),
    }
  },
  server: {
    port: 5173,
    host: '0.0.0.0', // Позволяет доступ с других устройств в сети
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // Backend на localhost:8000
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
