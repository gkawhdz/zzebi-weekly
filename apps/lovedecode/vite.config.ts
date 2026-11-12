import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import { vite as aitDevtools } from '@apps-in-toss/devtools/unplugin'

// https://vite.dev/config/
export default defineConfig({
  base: './',
  plugins: [react(), aitDevtools()],
})
