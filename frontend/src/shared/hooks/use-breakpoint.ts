'use client'

import { useSyncExternalStore } from 'react'

const BREAKPOINT_KEYS = ['xs', 'sm', 'md', 'lg', 'xl', '2xl'] as const

// 断点配置类型
type BreakpointKey = (typeof BREAKPOINT_KEYS)[number]
type BreakpointConfig = Record<BreakpointKey, number>
type BreakpointInfo = Record<BreakpointKey, boolean>

// 全局状态
const subscribers = new Set<() => void>()
let breakpointInfo: BreakpointInfo
let isListening = false

// 断点配置（与 Tailwind 保持一致）
const BREAKPOINTS: BreakpointConfig = {
  'xs': 0, // => @media (min-width: 0px)
  'sm': 640, // => @media (min-width: 640px)
  'md': 768, // => @media (min-width: 768px)
  'lg': 1024, // => @media (min-width: 1024px)
  'xl': 1280, // => @media (min-width: 1280px)
  '2xl': 1536, // => @media (min-width: 1536px)
} as const

// 缓存服务端默认值
const defaultBreakpointInfo: BreakpointInfo = BREAKPOINT_KEYS.reduce((acc, key) => {
  acc[key as BreakpointKey] = false
  return acc
}, {} as BreakpointInfo)

/**
 * 计算当前窗口的响应式信息
 */
function calculateBreakpoints(): boolean {
  if (typeof window === 'undefined')
    return false

  const width = window.innerWidth
  const newInfo = {} as BreakpointInfo
  let shouldUpdate = false

  for (const key of BREAKPOINT_KEYS) {
    newInfo[key] = width >= BREAKPOINTS[key]
    if (!breakpointInfo || newInfo[key] !== breakpointInfo[key]) {
      shouldUpdate = true
    }
  }

  if (shouldUpdate) {
    breakpointInfo = newInfo
    return true
  }
  return false
}

/**
 * 处理窗口大小变化
 */
function handleResize() {
  const hasChanged = calculateBreakpoints()
  if (!hasChanged)
    return

  for (const subscriber of subscribers) {
    subscriber()
  }
}

/**
 * 初始化全局监听器
 */
function initializeListener() {
  if (typeof window === 'undefined' || isListening)
    return

  // 初始计算
  if (!breakpointInfo) {
    calculateBreakpoints()
  }

  window.addEventListener('resize', handleResize)
  isListening = true

  return () => {
    window.removeEventListener('resize', handleResize)
    isListening = false
  }
}

function getCurrentBreakpoint(breakpointInfo: BreakpointInfo): BreakpointKey {
  for (const key of BREAKPOINT_KEYS) {
    if (breakpointInfo[key])
      return key
  }
  return 'xs'
}

/**
 * 响应式 Hook
 */
function useBreakpointInfo(): {
  info: BreakpointInfo
  current: BreakpointKey
} {
  const info = useSyncExternalStore(
    // subscribe
    (callback) => {
      if (typeof window === 'undefined')
        return () => {}

      // 确保全局监听器已初始化
      const cleanup = initializeListener()

      // 添加订阅
      subscribers.add(callback)

      // 返回清理函数
      return () => {
        subscribers.delete(callback)
        cleanup?.()
      }
    },
    // getSnapshot
    () => {
      if (typeof window === 'undefined') {
        return defaultBreakpointInfo
      }

      if (!breakpointInfo) {
        calculateBreakpoints()
      }
      return breakpointInfo
    },
    // getServerSnapshot - 使用缓存的默认值
    () => defaultBreakpointInfo,
  )
  return {
    info,
    current: getCurrentBreakpoint(info),
  }
}

/**
 * 移动端检测 Hook
 * @returns boolean - 是否为移动端设备
 */
function useIsMobile(): boolean {
  const { info } = useBreakpointInfo()
  return !info.md
}

export {
  BREAKPOINTS,
  useBreakpointInfo,
  useIsMobile,
}
