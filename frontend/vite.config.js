import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig(async ({ mode }) => {
  const isDev = mode === 'development'

  const config = {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src'),
      },
    },
    server: {
      fs: {
        allow: [path.resolve(__dirname, '..')],
      },
    },
  }

  const { default: frappeui } = await import('frappe-ui/vite')
  config.plugins.unshift(
    frappeui({
      frappeProxy: true,
      lucideIcons: true,
      jinjaBootData: true,
      buildConfig: {
        indexHtmlPath: '../onerc_procurement/www/prequal.html',
        emptyOutDir: true,
        sourcemap: false,
      },
    }),
  )

  return config
})
