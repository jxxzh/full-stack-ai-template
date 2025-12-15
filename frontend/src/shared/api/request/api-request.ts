import { env } from '@/shared/config/env'
import { ofetch } from 'ofetch'

export const apiRequest = ofetch.create({
  baseURL: env.VITE_BASE_URL,
})
