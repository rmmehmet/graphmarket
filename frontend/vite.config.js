import path from 'node:path'
import { fileURLToPath } from 'node:url'
import react from '@vitejs/plugin-react'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
import { defineConfig } from 'vite'

// mobile (React Native) pins an exact React version different from frontend's,
// so npm workspaces can't hoist a single copy — it installs a second one nested
// in frontend/node_modules. Force every import (including hoisted deps like
// @tanstack/react-query) to resolve to that one copy, or two React instances
// end up mounted at once and hooks break with "Cannot read properties of null".
export default defineConfig({
  plugins: [react()],
  resolve: {
    dedupe: ['react', 'react-dom'],
    alias: {
      react: path.resolve(__dirname, 'node_modules/react'),
      'react-dom': path.resolve(__dirname, 'node_modules/react-dom'),
    },
  },
})
