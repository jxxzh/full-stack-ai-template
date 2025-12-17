import { ofetch } from 'ofetch'
import { env } from '@/shared/config/env'

export const apiRequest = ofetch.create({
  baseURL: env.NEXT_PUBLIC_API_BASE_URL,
})
