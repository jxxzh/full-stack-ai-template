'use client'

import { atom, useAtom } from 'jotai'
import { createStore } from 'jotai/vanilla'
import type React from 'react'
import { useCallback, useState } from 'react'

import {
  AlertDialog,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/shared/components/ui/alert-dialog'
import { Button } from '@/shared/components/ui/button'
import { Spinner } from '@/shared/components/ui/spinner'

type ButtonVariant = React.ComponentProps<typeof Button>['variant']

interface AlertDialogQuickOpenOptions {
  title: React.ReactNode
  description?: React.ReactNode
  confirmText?: React.ReactNode
  cancelText?: React.ReactNode
  confirmVariant?: ButtonVariant
  cancelVariant?: ButtonVariant
  onConfirm?: () => void | Promise<void>
  onCancel?: () => void | Promise<void>
}

const store = createStore()

interface AlertDialogQuickOpenState {
  id: number
  options: AlertDialogQuickOpenOptions
}

const staticAlertDialogUIAtom = atom<{
  open: boolean
  state: AlertDialogQuickOpenState | null
}>({
  open: false,
  state: null,
})

let dialogId = 0

function StaticAlertDialog() {
  const [uiState, setUiState] = useAtom(staticAlertDialogUIAtom, { store })
  const current = uiState.state
  const options = current?.options

  const {
    title,
    description,
    confirmText = '确认',
    cancelText,
    confirmVariant = 'default',
    cancelVariant = 'outline',
    onConfirm,
    onCancel,
  } = options ?? {}

  const [isConfirmLoading, setIsConfirmLoading] = useState(false)
  const [isCancelLoading, setIsCancelLoading] = useState(false)

  const close = useCallback(() => {
    setUiState((prev) => ({ ...prev, open: false }))
  }, [setUiState])

  const handleConfirm = useCallback(async () => {
    if (!onConfirm) {
      close()
      return
    }
    setIsConfirmLoading(true)
    try {
      await onConfirm()
      close()
    } finally {
      setIsConfirmLoading(false)
    }
  }, [close, onConfirm])

  const handleCancel = useCallback(async () => {
    setIsCancelLoading(true)
    try {
      if (onCancel) {
        await onCancel()
      }
      close()
    } finally {
      setIsCancelLoading(false)
    }
  }, [close, onCancel])

  const isLoading = isConfirmLoading || isCancelLoading

  return (
    <AlertDialog
      open={uiState.open}
      onOpenChange={(open) => setUiState((prev) => ({ ...prev, open }))}
    >
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>{title}</AlertDialogTitle>
          {description && (
            <AlertDialogDescription>{description}</AlertDialogDescription>
          )}
        </AlertDialogHeader>
        <AlertDialogFooter>
          {cancelText && (
            <Button
              variant={cancelVariant}
              disabled={isLoading}
              onClick={handleCancel}
            >
              {isCancelLoading && <Spinner className="size-4" />}
              {cancelText}
            </Button>
          )}
          <Button
            variant={confirmVariant}
            disabled={isLoading}
            onClick={handleConfirm}
          >
            {isConfirmLoading && <Spinner className="size-4" />}
            {confirmText}
          </Button>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}

function openAlertDialog(options: AlertDialogQuickOpenOptions) {
  const id = ++dialogId
  store.set(staticAlertDialogUIAtom, { state: { id, options }, open: true })
}

function closeAlertDialog() {
  store.set(staticAlertDialogUIAtom, (prev) => ({ ...prev, open: false }))
}

export type { AlertDialogQuickOpenOptions }
export { StaticAlertDialog, openAlertDialog, closeAlertDialog }
