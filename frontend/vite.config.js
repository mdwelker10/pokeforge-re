import { fileURLToPath, URL } from 'node:url'

import vue from '@vitejs/plugin-vue'
import { defineConfig, loadEnv } from 'vite'
import vueDevTools from 'vite-plugin-vue-devtools'

export default ({ mode }) => {
  const env = loadEnv(mode, process.cwd());
  return defineConfig({
    plugins: [
      vue(),
      vueDevTools(),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
    server: {
      port: 3000,
      host: true,
      hmr: { clientPort: 3000 },
      timeout: 200000,
      proxyTimeout: 200000,
      '/api': {
        target: env.VITE_SERVER_PROXY,
        headers: {
          "Access-Control-Allow-Origin": ["*"] // CORS - Change for production
        }
      }
    }
  })
}
