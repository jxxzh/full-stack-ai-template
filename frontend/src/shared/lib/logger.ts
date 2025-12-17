import { createConsola } from 'consola'
import { env } from '../config/env'

const logger = createConsola({
  level: env.NEXT_PUBLIC_ENV === 'prod' ? 0 : 5, // 生产环境只打印 error 日志
})

function createTagLogger(tag: string) {
  return logger.create({
    defaults: {
      tag,
    },
  })
}

export { createTagLogger, logger }
