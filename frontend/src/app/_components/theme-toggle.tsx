'use client'

import { IconDeviceDesktop, IconMoon, IconSun } from '@tabler/icons-react'
import { useTheme } from 'next-themes'
import { useEffect, useMemo, useState } from 'react'

import { Button } from '@/shared/components/ui/button'

export const ThemeToggle = () => {
  const [mounted, setMounted] = useState(false)
  const { theme, setTheme } = useTheme()

  useEffect(() => {
    setMounted(true)
  }, [])

  const currentTheme = useMemo(() => theme ?? 'system', [theme])

  const { icon: Icon, label } = useMemo(() => {
    if (currentTheme === 'light') {
      return { icon: IconSun, label: '浅色' }
    }
    if (currentTheme === 'dark') {
      return { icon: IconMoon, label: '深色' }
    }
    return { icon: IconDeviceDesktop, label: '跟随系统' }
  }, [currentTheme])

  const cycleTheme = () => {
    if (currentTheme === 'system') {
      setTheme('light')
      return
    }
    if (currentTheme === 'light') {
      setTheme('dark')
      return
    }
    setTheme('system')
  }

  if (!mounted) {
    return null
  }

  return (
    <Button
      variant="outline"
      size="icon"
      type="button"
      onClick={cycleTheme}
      aria-label={`切换主题（当前：${label}）`}
      title={`切换主题（当前：${label}）`}
    >
      <Icon className="size-4" />
    </Button>
  )
}
