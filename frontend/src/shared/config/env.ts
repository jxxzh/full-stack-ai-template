import { createEnv } from '@t3-oss/env-nextjs'
import { z } from 'zod'

export const env = createEnv({
  server: {},

  client: {
    NEXT_PUBLIC_ENV: z.enum(['dev', 'prod']),
    NEXT_PUBLIC_API_BASE_URL: z.url(),
  },

  // Next.js 打包环境变量时只包含明确访问的变量，所以需要手动解构
  // 对于 Next.js >= 13.4.4, 只需要解构客户端变量
  experimental__runtimeEnv: {
    NEXT_PUBLIC_ENV: process.env.NEXT_PUBLIC_ENV,
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL,
  },

  emptyStringAsUndefined: true,
})