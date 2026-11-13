import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// The backend has no CORS: the dev server proxies /api/* to FastAPI (port 8001 unless API_TARGET says otherwise).
const proxy = {
  '/api': {
    target: process.env.API_TARGET ?? 'http://localhost:8001',
    changeOrigin: true,
    rewrite: (path: string) => path.replace(/^\/api/, ''),
  },
}

export default defineConfig({
  plugins: [react()],
  server: { proxy },
  preview: { proxy },
})
