'use client'

import { Button } from '@/shared/components/ui/button'
import { openAlertDialog } from '@/shared/lib/alert-dialog-helper'

export function AlertDialogQuickOpen() {
  const handleOpen = () => {
    openAlertDialog({
      title: '删除条目？',
      description: '此操作不可撤销，请确认是否继续。',
      confirmText: '删除',
      cancelText: '取消',
      confirmVariant: 'destructive',
      cancelVariant: 'outline',
      onCancel: async () => {
        await new Promise((resolve) => setTimeout(resolve, 1200))
      },
      onConfirm: async () => {
        await new Promise((_, reject) => setTimeout(reject, 1200))
      },
    })
  }

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-xl font-semibold">AlertDialog quickOpen 示例</h1>
      <p className="text-sm text-muted-foreground">
        通过静态 helper 快速打开一次性 AlertDialog，包含 async 确认与 loading。
      </p>
      <Button variant="outline" onClick={handleOpen}>
        打开弹窗
      </Button>
    </div>
  )
}
