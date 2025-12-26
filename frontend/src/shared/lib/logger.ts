import { createConsola } from 'consola'

const logger = createConsola({
  level: import.meta.env.PROD ? 0 : 5, // 生产环境只打印 error 日志
})

function createTagLogger(tag: string) {
  return logger.create({
    defaults: {
      tag,
    },
  })
}

export { createTagLogger, logger }
