import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// The backend has no CORS: the dev server proxies /api/* to FastAPI on port 8001.
const proxy = {
  '/api': {
    target: 'http://localhost:8001',
    changeOrigin: true,
    rewrite: (path: string) => path.replace(/^\/api/, ''),
  },
}

export default defineConfig({
  plugins: [react()],
  server: { proxy },
  preview: { proxy },
})
