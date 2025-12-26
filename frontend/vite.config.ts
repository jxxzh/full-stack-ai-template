import { defineConfig } from 'vite'
import { tanstackStart } from '@tanstack/react-start/plugin/vite'
import viteReact from '@vitejs/plugin-react'
import viteTsConfigPaths from 'vite-tsconfig-paths'
import tailwindcss from '@tailwindcss/vite'
import { nitro } from 'nitro/vite'
import { devtools } from '@tanstack/devtools-vite'

const config = defineConfig({
  plugins: [
    devtools(),
    nitro(),
    // this is the plugin that enables path aliases
    viteTsConfigPaths({
      projects: ['./tsconfig.json'],
    }),
    tailwindcss(),
    tanstackStart({
      server: {
        entry: 'app/entrypoint/server.ts',
      },
      client: {
        entry: 'app/entrypoint/client.tsx',
      },
      router: {
        entry: 'app/router/index.tsx',
      }
    }),
    viteReact(),
  ],
})

export default config
